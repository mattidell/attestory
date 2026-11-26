"""Full-surface replay: published core v108 against scratch core v109.

Run inside the scratch export that scratch_build.py made (so both cores run
on the scratch code, which is what a Track 1 build would publish):
  python3 docs/phases/engine-breadth/milestones/line16-next-step-evidence/replay.py \
      --part <part-file-outside-repo> [--workers N] [--only-probe] [--out replay.json]

One shared tools.recorded_replay.replay process pool runs every recorded list
(recorded_lists(), 775) plus the 26 probe lists (probe.cases(), keyed
"probe/..."). Each list runs on both cores through the full-surface snapshot
(FullSurfaceCompare) and is classified strictly: any difference that no
expectation below names fails the list. The expectations are only:

- the package version v108 -> v109 wherever it is recorded;
- an added reason whose sentence is exactly one of the four declared answer
  explanations (read from the citizens in scratch.diff), at a new trailing
  reason index;
- the reasons list order record of a line that gained such a reason (every
  existing reason keeps its index and sentence, which other records check).

No value, disposition, code, question group, question reference or row may
change. --controls re-checks one changed list with an empty expectation set
and with a wrong sentence, both of which must fail.
"""
from __future__ import annotations

import argparse
import importlib.util
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
CORES = ("v108", "v109")


def _probe():
    name = "l16ns_probe_for_replay"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, HERE / "probe.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def explanations() -> dict[str, str]:
    """slug -> declared sentence, from the new citizen files in scratch.diff."""
    text = (HERE / "scratch.diff").read_text(encoding="utf-8")
    found = {}
    for block in re.split(r"(?m)^diff --git ", text):
        if "answer-explanation.exception1-" not in block.split("\n", 1)[0]:
            continue
        body = "\n".join(line[1:] for line in block.splitlines() if line.startswith("+") and not line.startswith("+++"))
        citizen = json.loads(body)
        found[citizen["fact_type"]["id"].removeprefix(P + "exception1.")] = citizen["explanation"]
    assert len(found) == 4, found
    return found


def expectations(sentences: dict[str, str] | None = None) -> list:
    sentences = explanations() if sentences is None else sentences
    out = [rr.version_change(P + "package.core-calculations", *CORES)]
    for slug, sentence in sorted(sentences.items()):
        out.append(rr.Expectation(("page",), "sentence", r"/resolved\.reasons\[\[\d+\]\]$", "added",
                                  after=sentence, note=f"answer-explanation:{slug}"))
    out.append(rr.Expectation(("page",), r"resolved\.reasons@order", "", "changed",
                              note="reasons order record of a line that gained an explanation"))
    return out


def lists(only_probe: bool) -> list:
    probe = [("probe/" + key, acts) for key, acts in _probe().cases()]
    return probe if only_probe else rr.recorded_lists() + probe


def summarize(results: dict, specs: list, cores: tuple) -> dict:
    classes = Counter(row["class"] for row in results.values())
    used = {index for row in results.values() for index in row.get("used", [])}
    by_attribute: dict[str, dict] = {}
    for key, row in results.items():
        for item in row["unexpected"]:
            slot = by_attribute.setdefault(f"{item['kind']}|{item['change']}|{re.sub(r'[0-9]+', 'N', item['attribute'])}",
                                           {"lists": set(), "samples": []})
            slot["lists"].add(key)
            if len(slot["samples"]) < 3:
                slot["samples"].append({"list": key, **item})
    expected = sum((Counter(row["expected_by_note"]) for row in results.values()), Counter())
    changed = sorted(key for key, row in results.items() if row["class"] == "expected_changes")
    recorded = [key for key in results if not key.startswith("probe/")]
    return {
        "format": "line16-next-step-replay.v1",
        "cores": [rr.core_fingerprint(core) for core in cores],
        "lists": len(results),
        "recorded_lists": len(recorded),
        "probe_lists": len(results) - len(recorded),
        "classes": dict(sorted(classes.items())),
        "passing": sum(1 for row in results.values() if row["class"] != "unexpected"),
        "failing": sum(1 for row in results.values() if row["class"] == "unexpected"),
        "unexpected_differences": sum(row["unexpected_total"] for row in results.values()),
        "unexpected_by_kind_attribute": {name: {"lists": len(slot["lists"]), "samples": slot["samples"]}
                                         for name, slot in sorted(by_attribute.items())},
        "expectations": [rr.describe_expectation(spec) for spec in specs],
        "expectations_used": len(used),
        "expected_by_note": dict(sorted(expected.items())),
        "outcomes": dict(sorted(Counter("/".join(row["outcomes"]) for row in results.values()).items())),
        "lists_with_added_explanations": [key for key in changed
                                          if any(n.startswith("answer-explanation:") for n in results[key]["expected_by_note"])],
        "lists_with_only_version_moves": [key for key in changed
                                          if not any(n.startswith("answer-explanation:") for n in results[key]["expected_by_note"])][:5],
        "list_classes": {key: row["class"] for key, row in sorted(results.items())},
        "failing_lists": {key: row["unexpected_total"] for key, row in sorted(results.items()) if row["class"] == "unexpected"},
    }


def controls(key: str) -> dict:
    """The real comparison passes; no expectations, or a wrong sentence, fails."""
    chosen = dict(lists(only_probe=key.startswith("probe/")))
    cores = tuple(rr.resolve_core(c) for c in CORES)
    wrong = {slug: sentence + " X" for slug, sentence in explanations().items()}
    rows = {}
    gains = False
    for name, specs in (("real", expectations()), ("no_expectations", []), ("wrong_sentence", expectations(wrong))):
        verdict = rr.FullSurfaceCompare(specs)(key, chosen[key], cores)
        rows[name] = {"class": verdict["class"], "differences": verdict["differences"],
                      "unexpected": verdict["unexpected_total"]}
        if name == "real":
            gains = any(note.startswith("answer-explanation:") for note in verdict["expected_by_note"])
    # A wrong sentence can only fail a list that gains an explanation; on any
    # other list it must change nothing (the explanations are not reached).
    wrong_ok = (rows["wrong_sentence"]["class"] == "unexpected") if gains else (rows["wrong_sentence"]["class"] != "unexpected")
    return {"list": key, "gains_explanation": gains, **rows,
            "controls_hold": rows["real"]["class"] != "unexpected" and rows["no_expectations"]["class"] == "unexpected"
            and wrong_ok}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--part")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--only-probe", action="store_true")
    parser.add_argument("--controls", default=None, help="comma-separated list keys")
    parser.add_argument("--max-new", type=int, default=None,
                        help="run at most this many lists not yet in --part, then stop (foreground-sized steps)")
    parser.add_argument("--out")
    args = parser.parse_args()
    if args.controls:
        body = {"format": "line16-next-step-controls.v1", "lists": [controls(k) for k in args.controls.split(",")]}
        body["all_controls_hold"] = all(row["controls_hold"] for row in body["lists"])
    else:
        started = time.monotonic()
        cores = tuple(rr.resolve_core(c) for c in CORES)
        specs = expectations()
        chosen = lists(args.only_probe)
        steps: list = []
        done: set = set()
        if args.part:
            part = Path(args.part)
            done = set((json.loads(part.read_text(encoding="utf-8")).get("results") or {}) if part.exists() else ())
            sidecar = part.with_name(part.name + ".steps.json")
            steps = json.loads(sidecar.read_text(encoding="utf-8")) if sidecar.exists() else []
            if args.max_new is not None:
                pending = [item for item in chosen if item[0] not in done][: args.max_new]
                step = [item for item in chosen if item[0] in done] + pending
            else:
                step = chosen
        else:
            step = chosen
        results = rr.replay(step, cores, rr.FullSurfaceCompare(specs), workers=args.workers, part=args.part)
        elapsed = round(time.monotonic() - started, 1)
        if args.part:
            steps.append({"new_lists": len(step) - len(done), "wall_time_s": elapsed})
            sidecar.write_text(json.dumps(steps) + "\n", encoding="utf-8")
        if len(results) < len(chosen):
            print(json.dumps({"done": len(results), "of": len(chosen), "step_wall_time_s": elapsed}))
            return
        body = summarize(results, specs, cores)
        body["workers"] = args.workers or "cpu_count - 1"
        body["steps"] = steps
        body["wall_time_s"] = round(sum(s["wall_time_s"] for s in steps), 1) if steps else elapsed
    text = json.dumps(body, indent=1, ensure_ascii=False) + "\n"
    rr._check_no_local_paths(text, "replay summary")
    if args.out:
        (HERE / args.out).write_text(text, encoding="utf-8")
    print(json.dumps({k: v for k, v in body.items() if k not in ("list_classes", "expectations")}, indent=1)[:6000])


if __name__ == "__main__":
    main()
