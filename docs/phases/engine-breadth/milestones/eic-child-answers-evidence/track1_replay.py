"""Full-surface replay: published v100 against published v101 (Track 1: every roster member's missing answer is asked).

Run: python3 track1_replay.py --shard I/N --part <part-file-outside-repo>
     python3 track1_replay.py --summarize <part-files...> --out track1-replay.json
     python3 track1_replay.py --probe --shard I/N --part <part-file-outside-repo>
     python3 track1_replay.py --probe --summarize <part-files...> --out track1-replay-probe.json

Uses tools/recorded_replay.py unchanged (snapshots, diff, strict
``classify_full`` through ``FullSurfaceCompare``): every saved page field,
attachment, explanation-graph node and report row on both cores; every
difference no expectation below names fails the list. No normalisation is
added. Both cores run on the same projection (ADR 0087 walk), so every
difference is v101's content: twenty-six input questions.

``--probe`` replays P0's probe.py lists and Track 1's track1_probe.py lists
(every case; the named answer is left unanswered for the named member,
nothing is pre-filled for it).
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
BASE = "v100"
TARGET = "v101"


def _design():
    return rr._module("eicc_t1_design", HERE / "track1_design.py")


def _p0_probe():
    return rr._module("eicc_p0_probe", HERE / "probe.py")


def _t1_probe():
    return rr._module("eicc_t1_probe", HERE / "track1_probe.py")


def expectations() -> list[rr.Expectation]:
    d = _design()
    specs = [rr.version_change(P + "package.core-calculations", BASE, TARGET)]
    for fact, text in sorted(d.QUESTIONS.items()):
        # A line that waits only on members' answers with a declared question shows each question as a sentence
        # (on v100 the same line shows no sentence at all).
        specs.append(rr.Expectation(("page", "model"), r"sentence", r"", "added", rr.ANY, text,
                                    note="question shown:" + fact.removeprefix(P)))
    # Each such reason names its member by the member's recorded label (ADR 0087 Decision 2).
    specs.append(rr.Expectation(("page", "model"), r"memberLabel", r"", "added", rr.ANY, rr.ANY,
                                note="member label shown beside the question"))
    # The order record of a reasons list that is new on the line; "added" only, so a reorder still fails.
    specs.append(rr.Expectation(("page", "model"), r"resolved\.reasons@order", r"^sections\[", "added", None, rr.ANY,
                                note="reasons list added on a line that had none"))
    return specs


def probe_lists() -> list:
    p0, t1 = _p0_probe(), _t1_probe()
    return ([(f"probe/{case}", p0.build(case)) for case in p0.CASES]
            + [(f"track1/{case}", t1.build(case)) for case in t1.CASES])


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
    parser.add_argument("--shard", default="0/1")
    parser.add_argument("--part")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--summarize", nargs="*")
    parser.add_argument("--probe", action="store_true", help="the P0 and Track 1 probe lists instead of the recorded lists")
    parser.add_argument("--out")
    args = parser.parse_args()
    specs = expectations()
    cores = [rr.core_fingerprint(BASE), rr.core_fingerprint(TARGET)]
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
    results = rr.replay(lists, (rr.resolve_core(BASE), rr.resolve_core(TARGET)), rr.FullSurfaceCompare(specs),
                        workers=args.workers, part=args.part)
    summary = _summary(results, specs, cores)
    print(json.dumps({"shard": args.shard, "wall_time_s": round(time.monotonic() - started, 1),
                      **{k: summary[k] for k in ("lists", "classes", "passing", "failing", "unexpected_differences",
                                                 "expected_by_note", "outcomes")},
                      "unexpected": {k: v["lists"] for k, v in summary["unexpected_by_kind_attribute"].items()}}, indent=1))


if __name__ == "__main__":
    main()
