"""Summarize downloaded CI shard artifacts into a sanitized JSON document.

Usage: python3 -I analyze.py ARTIFACT_DIR DURATIONS_JSON > traces-summary.json

ARTIFACT_DIR holds one directory per downloaded `pytest-durations-shard-N`
artifact, named `<run id>-s<N>`. Reads only fixed numeric/enumerated fields:
no paths, hosts or raw browser output are copied. Browser-test node ids are
repository test names, which are not sensitive.
"""
import json
import re
import sys
from pathlib import Path

BROWSER_MODULES = ("tests/test_sli_correction_resumption.py",
                   "tests/test_sli_correction_session.py",
                   "tests/test_chrome_test_resources.py")
SAMPLE_KEYS = ("ms", "state", "threads", "rss_kb", "fds", "cpu_user_ticks", "cpu_system_ticks")


def wall_seconds(text):
    m = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([\d:.]+)", text)
    total = 0.0
    for p in m.group(1).split(":"):
        total = total * 60 + float(p)
    return round(total, 1)


def launch(rec):
    out = {k: rec.get(k) for k in ("label", "outcome", "readiness_ms", "advertised_ms",
                                   "elapsed_ms", "queue_ms", "stderr_bytes", "exit_kind",
                                   "deadline_monotonic_ms")}
    out["stderr_categories"] = rec.get("stderr_categories", [])
    out["file_states"] = rec.get("file_states", [])
    out["samples"] = [{k: s.get(k) for k in SAMPLE_KEYS} for s in rec.get("samples", [])]
    return out


def main(artifacts, durations_path):
    known = set(json.load(open(durations_path))["durations"])
    shards = []
    for d in sorted(Path(artifacts).iterdir(), key=lambda p: p.name):
        run, shard = d.name.rsplit("-s", 1)
        man = json.load(open(d / "shard-manifest.json"))
        ids = [e["nodeid"] for e in man["executions"]]
        rec = {"run": run, "shard": int(shard),
               "failed": man["junit"]["failures"] + man["junit"]["errors"] > 0,
               "wall_seconds": wall_seconds((d / "rusage.txt").read_text()),
               "assigned": len(ids),
               "unknown_to_durations": sum(1 for i in ids if i not in known),
               "browser_tests": sum(1 for i in ids if i.split("::")[0] in BROWSER_MODULES),
               "browser_tests_unknown": sum(1 for i in ids if i.split("::")[0] in BROWSER_MODULES and i not in known)}
        trace = d / "chrome-startup.jsonl"
        rec["has_trace"] = trace.exists()
        if trace.exists():
            rec["launches"] = [launch(json.loads(l)) for l in trace.read_text().splitlines() if l.strip()]
        probe = d / "chrome-probe.jsonl"
        if probe.exists():
            rows = [json.loads(l) for l in probe.read_text().splitlines() if l.strip()]
            rec["probe_readiness_ms"] = {k: [r["readiness_ms"] for r in rows if r["label"] == k]
                                         for k in ("isolated", "parallel")}
        shards.append(rec)
    json.dump({"format": 1, "shards": shards}, sys.stdout, indent=1)
    print()


if __name__ == "__main__":
    main(*sys.argv[1:3])
