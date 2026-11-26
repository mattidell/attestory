"""Full-surface replay of the recorded lists: core v107 against published v108.

Run from the repository root:
  python3 docs/phases/engine-breadth/milestones/code-b-basis-sentence-evidence/replay.py \
      --part <part-file-outside-repo> [--workers N] [--out replay-v108.json]
  python3 .../replay.py --controls --keys <list,...> --out controls-v108.json

A thin wrapper over sale-explanation-wording's replay.py. Its PlainWordsCompare
(whole-string sentence substitution on the v107 output, reasons re-sorted and
reasonIndices remapped as the projection does, then a strict comparison with
v108) is reused unchanged; only the declared table and version expectations
differ: the four wording.json rows, the four v2 -> v3 explanation moves and
core v107 -> v108. All recorded lists run in one shared recorded_replay.replay
process pool. Any difference no expectation names fails the list.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import recorded_replay as rr  # noqa: E402

_NAME = "sew_replay_for_cbbs"
if _NAME in sys.modules:
    sew = sys.modules[_NAME]
else:
    _spec = importlib.util.spec_from_file_location(_NAME, HERE.parent / "sale-explanation-wording-evidence" / "replay.py")
    assert _spec is not None and _spec.loader is not None
    sew = importlib.util.module_from_spec(_spec)
    sys.modules[_NAME] = sew
    _spec.loader.exec_module(sew)

P = "tax.us.2025."
CORES = ("v107", "v108")


def _rows() -> list[dict]:
    return list(json.loads((HERE / "wording.json").read_text(encoding="utf-8"))["replacements"])


def expectations() -> list:
    build = json.loads((HERE / "build.json").read_text(encoding="utf-8"))
    out = [rr.version_change(s["id"], s["old_version"], s["new_version"]) for s in build["successors"]]
    out.append(rr.version_change(P + "package.core-calculations", *CORES))
    return out


class CodeBCompare(sew.PlainWordsCompare):
    """PlainWordsCompare with the four code B sentences and v107 -> v108 version moves."""

    def __init__(self, max_unexpected: int = 40) -> None:
        self.choices = {}
        for r in _rows():
            if r["new"] not in self.choices.setdefault(r["old"], []):
                self.choices[r["old"]].append(r["new"])
        self.table = {old: news[0] for old, news in self.choices.items()}
        self.expectations = expectations()
        self.max_unexpected = max_unexpected


def controls(keys: list[str]) -> dict:
    """The real comparison passes; " X" on every new sentence and an empty table both fail."""
    lists = dict(rr.recorded_lists())
    cores = tuple(rr.resolve_core(c) for c in CORES)
    rows = []
    for key in keys:
        real, wrong, empty = CodeBCompare(), CodeBCompare(), CodeBCompare()
        wrong.choices = {old: [new + " X" for new in news] for old, news in wrong.choices.items()}
        wrong.table = {old: news[0] for old, news in wrong.choices.items()}
        empty.choices, empty.table = {}, {}
        result: dict = {"list": key}
        for name, compare in (("real", real), ("wrong_sentence", wrong), ("no_substitution", empty)):
            verdict = compare(key, lists[key], cores)
            result[name] = {"class": verdict["class"], "unexpected": verdict["unexpected_total"],
                            "sentences_replaced": sum(verdict["sentences_replaced"].values())}
        result["controls_fail"] = (result["real"]["class"] != "unexpected"
                                   and result["wrong_sentence"]["class"] == "unexpected"
                                   and result["no_substitution"]["class"] == "unexpected")
        rows.append(result)
    return {"format": "plain-words-controls.v1", "cores": [rr.core_fingerprint(c) for c in cores],
            "lists": rows, "all_controls_fail": all(r["controls_fail"] for r in rows)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--part")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--keys", default="")
    parser.add_argument("--controls", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()
    if args.controls:
        body = controls(args.keys.split(","))
        text = json.dumps(body, indent=1) + "\n"
        rr._check_no_local_paths(text, "controls")
        if args.out:
            Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return
    lists = rr.recorded_lists()
    if args.keys:
        wanted = set(args.keys.split(","))
        lists = [item for item in lists if item[0] in wanted]
    started = time.monotonic()
    cores = tuple(rr.resolve_core(c) for c in CORES)
    compare = CodeBCompare()
    results = rr.replay(lists, cores, compare, workers=args.workers, part=args.part)
    summary = sew.summarize(results, compare, cores)
    summary["wall_time_s"] = round(time.monotonic() - started, 1)
    summary["lists_reaching_a_declared_sentence"] = sorted(k for k, r in results.items() if r["sentences_replaced"])
    text = json.dumps(summary, indent=1) + "\n"
    rr._check_no_local_paths(text, "summary")
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("lists", "classes", "passing", "failing", "unexpected_differences",
                                              "expectations_declared", "expectations_used", "outcomes",
                                              "sentence_changes", "sentences_not_reached",
                                              "lines_with_reordered_reasons", "raw_by_kind_attribute",
                                              "wall_time_s")}, indent=1))


if __name__ == "__main__":
    main()
