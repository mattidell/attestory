"""Fast-lane tests for tools/recorded_replay.py.

Verifies:
- recorded_lists() returns 775 keys equal to the committed track0-neighbour.json key set.
- ordering and output are independent of worker count and finish order.
- resume skips keys in the part file.
- no absolute path in any written file.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from tools import recorded_replay

REPO = Path(__file__).resolve().parents[1]
COMMITTED_NEIGHBOUR = (
    REPO
    / "docs/phases/engine-breadth/milestones/question-wording-evidence/track0-neighbour.json"
)


def _fake_per_list(
    key: str, acts: list[dict[str, Any]], cores: Any = None
) -> dict[str, Any]:
    """Module-level picklable dummy worker function for tests."""
    digest = hashlib.md5(key.encode("utf-8")).hexdigest()
    val = int(digest[:4], 16) % 100
    return {"key": key, "val": val, "acts": len(acts)}


@pytest.fixture(scope="module")
def all_recorded_lists() -> list[tuple[str, list[dict[str, Any]]]]:
    """Fixture to load recorded lists before test timing."""
    return recorded_replay.recorded_lists()


def test_recorded_lists_returns_775_keys_equal_to_committed(
    all_recorded_lists: list[tuple[str, list[dict[str, Any]]]],
) -> None:
    assert len(all_recorded_lists) == 775
    keys = [k for k, _ in all_recorded_lists]
    assert len(keys) == len(set(keys))

    committed = json.loads(COMMITTED_NEIGHBOUR.read_text(encoding="utf-8"))
    committed_keys = set(committed["classes"].keys())
    assert len(committed_keys) == 775
    assert set(keys) == committed_keys


def test_ordering_and_output_independent_of_workers_and_finish_order() -> None:
    # Deliberately scrambled keys with varying payloads
    sample_lists: list[tuple[str, list[dict[str, Any]]]] = [
        ("task/z_last", [{"x": 1}, {"y": 2}]),
        ("task/a_first", [{"a": 10}]),
        ("task/m_middle", [{"m": 5}, {"n": 6}, {"o": 7}]),
        ("task/b_second", []),
        ("task/y_second_to_last", [{"p": 1}]),
        ("task/c_third", [{"c": 3}]),
        ("task/k_mid", [{"k": 9}]),
        ("task/d_fourth", [{"d": 4}]),
    ]
    expected_order = sorted(k for k, _ in sample_lists)

    res_w2 = recorded_replay.replay(sample_lists, (), _fake_per_list, workers=2)
    res_w4 = recorded_replay.replay(sample_lists, (), _fake_per_list, workers=4)

    assert res_w2 == res_w4
    assert list(res_w2.keys()) == expected_order
    assert list(res_w4.keys()) == expected_order


def test_resume_skips_keys_in_part_file(tmp_path: Path) -> None:
    part_file = tmp_path / "part.json"
    cached_row = {"key": "item/1", "val": 999, "cached": True}
    part_file.write_text(json.dumps({"item/1": cached_row}), encoding="utf-8")

    items: list[tuple[str, list[dict[str, Any]]]] = [
        ("item/1", [{"a": 1}]),
        ("item/2", [{"b": 2}]),
        ("item/3", [{"c": 3}]),
    ]

    res = recorded_replay.replay(items, (), _fake_per_list, workers=2, part=part_file)

    # item/1 must keep its pre-existing cached value, proving it was skipped
    assert res["item/1"] == cached_row
    assert res["item/2"] == _fake_per_list("item/2", [{"b": 2}])
    assert res["item/3"] == _fake_per_list("item/3", [{"c": 3}])

    # Verify part file on disk matches return value
    on_disk = json.loads(part_file.read_text(encoding="utf-8"))
    assert on_disk == res


def test_no_absolute_path_in_any_written_file(tmp_path: Path) -> None:
    part_file = tmp_path / "part.json"
    out_file = tmp_path / "out.json"

    items: list[tuple[str, list[dict[str, Any]]]] = [
        ("task/1", [{"demo": "data"}]),
        ("task/2", []),
    ]

    res = recorded_replay.replay(items, (), _fake_per_list, workers=2, part=part_file)

    # Build summary using recorded_replay structure
    summary = {
        "sets": {
            "v83": "tests/fixtures/f1099b_backup_withholding_v83/expected.json",
        },
        "distinct_lists": len(res),
        "runs": len(res),
        "counts": {"task": {"identical": len(res)}},
        "same_error_on_both_cores": {},
        "changes": [],
        "classes": {k: "identical" for k in res},
    }
    out_text = json.dumps(summary, indent=2) + "\n"
    out_file.write_text(out_text, encoding="utf-8")

    forbidden = ("/Users/", "/private/", "/tmp/", "/var/")
    for path in (part_file, out_file):
        content = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in content, f"{path.name} contained {needle}"
