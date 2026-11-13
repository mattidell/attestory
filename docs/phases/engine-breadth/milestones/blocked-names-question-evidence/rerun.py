"""Replay question-wording's 775-list neighbour set on v87 and scratch v88.

The launcher materializes the predecessor's exact de-duplicated act lists
once, then runs CPU-count-minus-one subprocess shards. Each shard executes
both cores for its slice. Part files and the shared replay stay outside the
repository; only the compact merged classification is committed.

    python3 rerun.py run <scratch-core.json> <outside-parts-directory>
"""

from __future__ import annotations

import contextlib
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any, Iterator

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import common  # noqa: E402
import prototype  # noqa: E402
from packages.derivation import loader  # noqa: E402

QW_TRACK0 = REPO / "docs/phases/engine-breadth/milestones/question-wording-evidence/track0.py"


def module(name: str, path: Path) -> Any:
    from tests import evidence_loader

    if evidence_loader.current_owner() is None:
        evidence_loader.activate("bnq_evidence")
    return evidence_loader.load(path, name)


def predecessor() -> Any:
    return module("bnq_qw_track0", QW_TRACK0)


def cores(test: Any, core_path: Path) -> tuple[Any, Any]:
    h = test.track0().h
    body = json.loads(core_path.read_text(encoding="utf-8"))
    old = h.Core("v87", "v85", "v85")
    new = h.Core(body["version"], body["registry"], body["release_version"],
                 content=Path(body["content"]), releases=Path(body["releases"]),
                 loader_from=body.get("loader_from"))
    return old, new


@contextlib.contextmanager
def scratch_runtime(track: Any, schemas: Any) -> Iterator[None]:
    """Lend the unchanged v87 harness the prototype schema and evaluator."""
    original_schemas = loader.DerivationSchemas
    original_live = track.live_coordinate_run

    def live(*args: Any, **kwargs: Any) -> Any:
        kwargs["schemas"] = schemas
        return original_live(*args, **kwargs)

    loader.DerivationSchemas = lambda: schemas  # type: ignore[assignment]
    track.live_coordinate_run = live
    try:
        with prototype.block_missing_runtime():
            yield
    finally:
        track.live_coordinate_run = original_live
        loader.DerivationSchemas = original_schemas  # type: ignore[assignment]


def pin(test: Any, core: Any, acts: list[dict[str, Any]], run_id: str,
        *, schemas: Any | None = None) -> dict[str, Any]:
    track = test.track0()
    if schemas is None:
        return test.pin(track.run_coordinate(core, acts, run_id))
    with scratch_runtime(track, schemas):
        return test.pin(track.run_coordinate(core, acts, run_id))


def questions(row: dict[str, Any]) -> set[str]:
    return {str(item) for item in row.get("questions") or []}


def computed(row: dict[str, Any]) -> bool:
    if "error" in row:
        return False
    return not any("blocked" in str(value) for value in (row.get("lines") or {}).values())


def run_shard(core_path: Path, replay_path: Path, shard: int, count: int, part: Path) -> None:
    qw = predecessor()
    rr = qw.rerun()
    test = rr.load_test()
    old, new = cores(test, core_path)
    schemas = prototype.PrototypeSchemas()
    work = json.loads(replay_path.read_text(encoding="utf-8"))
    if len(work) != 775:
        raise SystemExit(f"expected 775 shared lists, found {len(work)}")
    found: dict[str, Any] = {}
    for index, item in enumerate(work):
        if index % count != shard:
            continue
        key, acts = str(item["id"]), item["acts"]
        slug = re.sub(r"[^A-Za-z0-9_.-]", ".", key)
        old_pin = pin(test, old, acts, "demo.bnq.rerun.v87." + slug)
        new_pin = pin(test, new, acts, "demo.bnq.rerun.v88." + slug, schemas=schemas)
        row = rr.classify(old_pin, new_pin)
        gained = sorted(questions(new_pin) - questions(old_pin))
        row["new_questions"] = gained
        row["computed_before"] = computed(old_pin)
        row["new_question_on_computed"] = bool(gained and row["computed_before"])
        found[key] = row
        part.write_text(json.dumps(found, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"shard": shard, "runs": len(found)}), flush=True)


def merge(parts: list[Path], *, shards: int, wall_time: float, output_name: str = "rerun-output.json") -> None:
    found: dict[str, Any] = {}
    for part in parts:
        found.update(json.loads(part.read_text(encoding="utf-8")))
    if len(found) != 775:
        raise SystemExit(f"expected 775 merged lists, found {len(found)}")
    for row in found.values():
        # The predecessor classifier treats every `rows` change as numeric.
        # This successor intentionally changes blocked-row missing metadata.
        # An empty line-value diff plus row-only fields is explanation metadata,
        # not a changed number.
        if (row["class"] == "numbers_changed" and not row.get("lines")
                and row.get("number_fields")
                and all(str(field).startswith("rows.") for field in row["number_fields"])):
            row["class"] = "numbers_identical_block_metadata_changed"
        # The repair turns one terminal guard disposition into a named block.
        # String-valued line dispositions are not computed numbers.
        line_diffs = row.get("lines") or []
        if (row["class"] == "numbers_changed" and line_diffs
                and not row.get("v86_error") and not row.get("v87_error")
                and all(str(field).startswith(("lines.", "rows."))
                        for field in row.get("number_fields") or [])
                and all(not isinstance(diff.get(side), (int, float))
                        or isinstance(diff.get(side), bool)
                        for diff in line_diffs for side in ("v86", "v87"))):
            row["class"] = "numbers_identical_dispositions_changed"
    counts = Counter(row["class"] for row in found.values())
    by_set: dict[str, Counter[str]] = {}
    for key, row in found.items():
        by_set.setdefault(key.split("/", 1)[0], Counter())[row["class"]] += 1
    changes = [{"id": key, **row} for key, row in sorted(found.items()) if row["class"] != "identical"]
    payload = {
        "replay": "question-wording Track 0 neighbour set, exact 775 de-duplicated recorded act lists",
        "cores": "published core v87 and one scratch successor after v87",
        "shards": shards,
        "wall_time_seconds": round(wall_time, 3),
        "distinct_lists": len(found),
        "live_runs": len(found) * 2,
        "counts": dict(sorted(counts.items())),
        "counts_by_set": {key: dict(sorted(value.items())) for key, value in sorted(by_set.items())},
        "new_question_on_computed_count": sum(1 for row in found.values() if row["new_question_on_computed"]),
        "classes": {key: row["class"] for key, row in sorted(found.items())},
        "changes": changes,
    }
    common.write(output_name, payload)
    print(json.dumps({key: payload[key] for key in (
        "distinct_lists", "live_runs", "shards", "wall_time_seconds", "counts",
        "new_question_on_computed_count")}, indent=2))


def launch(core_path: Path, parts_dir: Path, *, output_name: str = "rerun-output.json") -> None:
    if parts_dir == REPO or REPO in parts_dir.parents:
        raise SystemExit("parts directory must be outside the repository")
    parts_dir.mkdir(parents=True, exist_ok=False)
    tasks = predecessor().neighbour_tasks()
    if len(tasks) != 775 or len({key for key, _acts in tasks}) != 775:
        raise SystemExit(f"expected 775 distinct predecessor lists, found {len(tasks)}")
    replay = parts_dir / "replay.json"
    replay.write_text(json.dumps([{"id": key, "acts": acts} for key, acts in tasks]) + "\n", encoding="utf-8")
    shards = min(4, max(1, (os.cpu_count() or 2) - 1))
    parts = [parts_dir / f"part-{index}.json" for index in range(shards)]
    started = time.monotonic()
    processes = [subprocess.Popen([
        sys.executable, str(Path(__file__).resolve()), "shard", str(core_path), str(replay),
        str(index), str(shards), str(parts[index]),
    ]) for index in range(shards)]
    failures = [process.wait() for process in processes]
    if any(failures):
        raise SystemExit(f"rerun shard failures: {failures}")
    merge(parts, shards=shards, wall_time=time.monotonic() - started, output_name=output_name)


def main() -> None:
    if len(sys.argv) == 4 and sys.argv[1] == "run":
        launch(Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve())
        return
    if len(sys.argv) == 4 and sys.argv[1] == "repair":
        launch(Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve(),
               output_name="rerun-repair-output.json")
        return
    if len(sys.argv) == 7 and sys.argv[1] == "shard":
        run_shard(Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve(),
                  int(sys.argv[4]), int(sys.argv[5]), Path(sys.argv[6]).resolve())
        return
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
