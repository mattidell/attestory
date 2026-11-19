"""Full-surface replay: published v99 against the scratch v100 (an input question for each unasked earned income credit answer).

Run: python3 replay.py <scratch-core.json> --shard I/N --part <part-file-outside-repo>
     python3 replay.py <scratch-core.json> --summarize <part-files...> --out replay.json
     python3 replay.py <scratch-core.json> --probe --shard I/N --part <part-file-outside-repo>
     python3 replay.py <scratch-core.json> --probe --summarize <part-files...> --out replay-probe.json

Uses tools/recorded_replay.py unchanged (snapshots, diff, strict
``classify_full`` through ``FullSurfaceCompare``): every saved page field,
attachment, explanation-graph node and report row on both cores; every
difference no expectation below names fails the list. No normalisation is
added: the change adds members only and no rule reads anything new.

``--probe`` replays the probe.py lists instead (every case, with the named
answers left unanswered; nothing is pre-filled for them).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import recorded_replay as rr  # noqa: E402

P = "tax.us.2025."
BASE = "v99"


def _design():
    return rr._module("eicq_p0_design", HERE / "design.py")


def _probe():
    return rr._module("eicq_p0_probe", HERE / "probe.py")


def expectations() -> list[rr.Expectation]:
    d = _design()
    specs = [rr.version_change(P + "package.core-calculations", "v99", "v100")]
    for name, text in d.QUESTIONS.items():
        # A line that waits only on answers with a declared question shows each question as a sentence
        # (on v99 the same line shows no sentence at all).
        specs.append(rr.Expectation(("page", "model"), r"sentence", r"", "added", rr.ANY, text,
                                    note=f"question shown:eic.{name}"))
    # The order record of a reasons list that is new on the line (v99 shows no reason there); "added" only, so a
    # reorder of an existing list still fails.
    specs.append(rr.Expectation(("page", "model"), r"resolved\.reasons@order", r"^sections\[", "added", None, rr.ANY,
                                note="reasons list added on a line that had none"))
    return specs


def probe_lists() -> list:
    probe = _probe()
    return [(f"probe/{probe.case_id(key, removed)}", probe.build(key, removed)) for key, removed in probe.CASES]


def _summary(results: dict, specs: list, cores: list) -> dict:
    classes = Counter(row["class"] for row in results.values())
    used_by: dict = {}
    for key, row in results.items():
        for i in row.get("used", []):
            used_by.setdefault(i, []).append(key)
    by_attribute: dict = {}
    for key, row in results.items():
        for item in row["unexpected"]:
            slot = by_attribute.setdefault(f"{item['kind']}|{item['change']}|{re.sub(r'[0-9]+', 'N', item['attribute'])}",
                                           {"lists": set(), "samples": []})
            slot["lists"].add(key)
            if len(slot["samples"]) < 3:
                slot["samples"].append({"list": key, **item})
    return {
        "format": "full-surface-replay.v1", "cores": cores, "lists": len(results),
        "classes": dict(sorted(classes.items())),
        "passing": sum(1 for r in results.values() if r["class"] != "unexpected"),
        "failing": sum(1 for r in results.values() if r["class"] == "unexpected"),
        "unexpected_differences": sum(r["unexpected_total"] for r in results.values()),
        "unexpected_by_kind_attribute": {k: {"lists": len(v["lists"]), "samples": v["samples"]} for k, v in sorted(by_attribute.items())},
        "expectations_declared": len(specs), "expectations_used": len(used_by),
        "unused_expectations": [rr.describe_expectation(s)["note"] for i, s in enumerate(specs) if i not in used_by],
        "expectation_lists": {rr.describe_expectation(s)["note"]: (len(used_by.get(i, [])) if len(used_by.get(i, [])) > 12
                                                                     else sorted(used_by.get(i, [])))
                              for i, s in enumerate(specs)},
        "expected_by_note": dict(sorted(sum((Counter(r["expected_by_note"]) for r in results.values()), Counter()).items())),
        "outcomes": dict(sorted(Counter("/".join(r["outcomes"]) for r in results.values()).items())),
        "list_classes": {k: r["class"] for k, r in sorted(results.items())},
        "failing_lists": {k: r["unexpected_total"] for k, r in sorted(results.items()) if r["class"] == "unexpected"},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("core")
    parser.add_argument("--shard", default="0/1")
    parser.add_argument("--part")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--summarize", nargs="*")
    parser.add_argument("--probe", action="store_true", help="the probe.py lists instead of the recorded lists")
    parser.add_argument("--out")
    args = parser.parse_args()
    specs = expectations()
    cores = [rr.core_fingerprint(BASE), rr.core_fingerprint(args.core)]
    if args.summarize:
        results: dict = {}
        for part in args.summarize:
            results.update(json.loads(Path(part).read_text(encoding="utf-8"))["results"])
        summary = _summary(results, specs, cores)
        summary["lists_set"] = "probe" if args.probe else "recorded"
        text = json.dumps(summary, indent=1) + "\n"
        rr._check_no_local_paths(text, "summary")
        Path(args.out).write_text(text, encoding="utf-8")
        print(json.dumps({k: summary[k] for k in ("lists", "classes", "passing", "failing", "unexpected_differences",
                                                   "expectations_declared", "expectations_used", "unused_expectations",
                                                   "expected_by_note", "outcomes")}, indent=1))
        return
    index, total = (int(x) for x in args.shard.split("/"))
    if args.probe:
        lists = probe_lists()
        from tests import evidence_loader  # as rr.recorded_lists does, release the loader before spawning workers

        owner = evidence_loader.current_owner()
        if owner:
            evidence_loader.release(owner)
    else:
        lists = rr.recorded_lists()
    lists = lists[index::total]
    started = time.monotonic()
    results = rr.replay(lists, (rr.resolve_core(BASE), rr.resolve_core(args.core)), rr.FullSurfaceCompare(specs),
                        workers=args.workers, part=args.part)
    summary = _summary(results, specs, cores)
    print(json.dumps({"shard": args.shard, "wall_time_s": round(time.monotonic() - started, 1),
                      **{k: summary[k] for k in ("lists", "classes", "passing", "failing", "unexpected_differences",
                                                 "expected_by_note", "outcomes")},
                      "unexpected": {k: v["lists"] for k, v in summary["unexpected_by_kind_attribute"].items()}}, indent=1))


if __name__ == "__main__":
    main()
