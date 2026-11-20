"""Identity dump of every recorded list on published core v100, in shards.

Run (scratch must be outside the repository):
  python3 vcr_dump.py materialize <scratch>
  python3 vcr_dump.py shard <label> <scratch> I/N [--workers W]
  python3 vcr_dump.py summarize <label> <scratch> N
  python3 vcr_dump.py compare <label-a> <label-b>

``materialize`` writes the 775 recorded lists once (lists.json in scratch);
every shard of every label reads that one file, so before and after replay
the same acts in the same order. A shard replays lists I, I+N, I+2N, ...
through rust-kernel-experiment's ``track1_dump.per_list`` (SHA-256 of the
canonical report and published values, of the saved page bytes and of the
presentation bytes; for an erroring list the exception class and message,
temporary directory masked). ``summarize`` joins the shards and writes
summary-<label>.json beside this file (counts and one per-list digest;
the full per-list dump stays in scratch); ``compare`` diffs two labels'
full dumps per list and writes compare-<a>-<b>.json.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vcr_common as vc  # noqa: E402


def per_list(key: str, acts: list[dict[str, Any]], core: Any) -> dict[str, Any]:
    result: dict[str, Any] = vc.dump.per_list(key, acts, core)
    return result


def _lists(scratch: Path) -> list[tuple[str, list[dict[str, Any]]]]:
    body = json.loads((scratch / "lists.json").read_text("utf-8"))
    return [(key, acts) for key, acts in body["lists"]]


def _line(key: str, r: dict[str, Any]) -> str:
    return (f"{key}\t{r['outcome']}\t{r.get('result_sha')}\t{r.get('page_sha')}\t"
            f"{r.get('presentation_sha')}\t{r.get('error')}\t{r.get('message')}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("materialize", "shard", "summarize", "compare"))
    parser.add_argument("args", nargs="*")
    parser.add_argument("--workers", type=int, default=9)
    ns = parser.parse_args()
    if ns.command == "compare":
        a, b, scratch = ns.args[0], ns.args[1], Path(ns.args[2]).resolve()
        left = json.loads((scratch / f"dump-{a}.json").read_text())["lists"]
        right = json.loads((scratch / f"dump-{b}.json").read_text())["lists"]
        differing = sorted(k for k in set(left) | set(right) if left.get(k) != right.get(k))
        out = {"a": a, "b": b, "lists_a": len(left), "lists_b": len(right),
               "lists_compared": len(set(left) & set(right)), "differing_lists": len(differing),
               "differing_keys": differing[:50]}
        vc.write(vc.HERE / f"compare-{a}-{b}.json", out)
        print(out)
        return
    if ns.command == "materialize":
        scratch = Path(ns.args[0]).resolve()
        assert vc.REPO not in scratch.parents
        scratch.mkdir(parents=True, exist_ok=True)
        lists = vc.rr.recorded_lists()
        assert len(lists) == 775, len(lists)
        (scratch / "lists.json").write_text(json.dumps({"lists": lists}, sort_keys=True), "utf-8")
        print(len(lists))
        return
    label, scratch = ns.args[0], Path(ns.args[1]).resolve()
    assert vc.REPO not in scratch.parents
    if ns.command == "shard":
        index, count = (int(x) for x in ns.args[2].split("/"))
        lists = _lists(scratch)[index - 1::count]
        vc.release_evidence_owner()
        core = vc.core()
        t0 = time.monotonic()
        results = vc.rr.replay(lists, core, per_list, workers=ns.workers,
                               part=scratch / f"dump-part-{label}-{index}of{count}.json")
        wall = round(time.monotonic() - t0, 1)
        (scratch / f"dump-{label}-{index}of{count}.json").write_text(
            json.dumps({"lists": results, "wall_s": wall}, indent=1, sort_keys=True) + "\n")
        print({"shard": f"{index}/{count}", "lists": len(results), "wall_s": wall})
        return
    count = int(ns.args[2])
    joined: dict[str, Any] = {}
    walls = []
    for index in range(1, count + 1):
        part = json.loads((scratch / f"dump-{label}-{index}of{count}.json").read_text())
        joined.update(part["lists"])
        walls.append(part["wall_s"])
    assert len(joined) == 775, len(joined)
    (scratch / f"dump-{label}.json").write_text(json.dumps({"lists": joined}, indent=1, sort_keys=True) + "\n")
    lines = [_line(k, r) for k, r in sorted(joined.items())]
    summary = {
        "label": label, "core": vc.CORE, "lists": len(joined),
        "outcomes": {o: sum(r["outcome"] == o for r in joined.values()) for o in ("success", "error", "refused")},
        "errors": sorted({r["error"] for r in joined.values() if r["outcome"] == "error"}),
        "per_list_digest": vc.dump._sha("\n".join(lines).encode("utf-8")),
        "shards": count, "shard_wall_s": walls,
    }
    vc.write(vc.HERE / f"summary-{label}.json", summary)
    print(summary)


if __name__ == "__main__":
    main()
