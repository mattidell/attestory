"""Full-surface replay of published core v103 against published core v104.

Run: python3 replay_track1.py --shard I/N --part <part-file>
     python3 replay_track1.py --summarize <part-files...> --out replay-v104.json

Expectations name the two ceiling-rule versions and the package version.
A numeric value that changes does not match them.
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


def _p0():
    spec = importlib.util.spec_from_file_location("hnw_t1_p0_replay", HERE / "replay.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expectations() -> list[rr.Expectation]:
    p0 = _p0()
    return [
        rr.version_change(p0.LINE6, "v1", "v2", "worksheet line 6 reads the status-test answer"),
        rr.version_change(p0.LINE13, "v1", "v2", "worksheet line 13 reads the status-test answer"),
        rr.version_change(p0.PACKAGE, "v103", "v104", "published package version"),
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard", default="0/1")
    parser.add_argument("--part")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--summarize", nargs="*")
    parser.add_argument("--out")
    args = parser.parse_args()
    p0 = _p0()
    specs = expectations()
    cores = [rr.core_fingerprint("v103"), rr.core_fingerprint("v104")]
    if args.summarize:
        results: dict = {}
        for part in args.summarize:
            results.update(json.loads(Path(part).read_text(encoding="utf-8"))["results"])
        summary = p0._summary(results, specs, cores)
        text = json.dumps(summary, indent=1) + "\n"
        p0._check(text, "summary")
        Path(args.out).write_text(text, encoding="utf-8")
        print(json.dumps({key: summary[key] for key in (
            "lists", "classes", "passing", "failing", "unexpected_differences", "number_change_lists",
            "expectations_declared", "expectations_used", "unused_expectations", "expected_by_note", "outcomes",
        )}, indent=1))
        return
    index, total = (int(part) for part in args.shard.split("/"))
    lists = rr.recorded_lists()[index::total]
    started = time.monotonic()
    results = rr.replay(lists, (rr.resolve_core("v103"), rr.resolve_core("v104")), rr.FullSurfaceCompare(specs),
                        workers=args.workers, part=args.part)
    summary = p0._summary(results, specs, cores)
    print(json.dumps({"shard": args.shard, "wall_time_s": round(time.monotonic() - started, 1),
                      **{key: summary[key] for key in (
                          "lists", "classes", "passing", "failing", "unexpected_differences", "number_change_lists",
                          "expected_by_note", "outcomes")}}, indent=1))


if __name__ == "__main__":
    main()
