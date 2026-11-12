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


@pytest.mark.live
def test_recorded_lists_returns_775_keys_equal_to_committed() -> None:
    # Full fixture export and harness gathering takes ~45-70 s, so this integration test
    # belongs in the live lane under tests/conftest.py.
    lists = recorded_replay.recorded_lists()
    assert len(lists) == 775
    keys = [k for k, _ in lists]
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
    # Part file includes cached row and an extra stale row not in the requested list set
    part_payload = {
        "_metadata": {"cores": []},
        "results": {
            "item/1": cached_row,
            "extra_stale": {"key": "extra_stale", "cached": True},
        },
    }
    part_file.write_text(json.dumps(part_payload), encoding="utf-8")

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
    # Extra key in part file must not be in returned dictionary
    assert "extra_stale" not in res

    # Verify part file on disk matches results
    on_disk = json.loads(part_file.read_text(encoding="utf-8"))
    assert on_disk["results"]["item/1"] == cached_row
    assert on_disk["results"]["item/2"] == res["item/2"]
    assert on_disk["results"]["item/3"] == res["item/3"]


def test_stale_part_file_for_different_cores_is_refused(tmp_path: Path) -> None:
    part_file = tmp_path / "part.json"
    c85_meta = recorded_replay.core_fingerprint("v85")
    c86_meta = recorded_replay.core_fingerprint("v86")
    part_payload = {
        "_metadata": {"cores": [c85_meta, c86_meta]},
        "results": {"k1": {"class": "identical"}},
    }
    part_file.write_text(json.dumps(part_payload), encoding="utf-8")

    with pytest.raises(ValueError, match="recorded for different cores"):
        recorded_replay.replay(
            [("k1", [])],
            ("v86", "v87"),
            _fake_per_list,
            workers=1,
            part=part_file,
        )


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


def test_baseline_other_than_v86_records_identical_errors() -> None:
    # Finding F3: Baseline other than v86 must record identical errors when both cores error
    pin_err_1 = {"error": "SameTaxError", "lines": {}}
    pin_err_2 = {"error": "SameTaxError", "lines": {}}

    res = recorded_replay.classify(pin_err_1, pin_err_2, name_a="v87", name_b="v88")
    assert res["class"] == "identical"
    assert res["v87_error"] == "SameTaxError"
    assert res["error"] == "SameTaxError"


def test_summarize_rerun_from_replay_pins() -> None:
    # Finding F4: summarize_rerun extracts pins from replay output and produces valid P0 rerun table
    pin_v86 = {"lines": {"l1": 100}, "questions": {}, "reasons": {}, "blocked_reasons": {}}
    pin_v87 = {"lines": {"l1": 100}, "questions": {}, "reasons": {}, "blocked_reasons": {}}
    fake_results = {
        "v83/track0/s0/b4_amount_no_answer": {
            "class": "identical",
            "pins": {"v86": pin_v86, "v87": pin_v87},
        }
    }
    summary = recorded_replay.summarize_rerun(fake_results, baseline_version="v86", comparison_version="v87")
    assert summary["runs"] == 1
    assert summary["counts"] == {"identical": 1}
    assert "track0/s0/b4_amount_no_answer" in summary["classes"]

