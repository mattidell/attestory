"""The 298 recorded v83 lists retain every numeric line on published v89.

Measured reason: 298 production ``live_coordinate_run`` calls take minutes.
They run in at most four worker processes and read the fixture in place.
"""

from __future__ import annotations

import json
import multiprocessing
import os
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any, cast

import pytest

from tests import evidence_loader


pytestmark = pytest.mark.live

REPO = Path(__file__).resolve().parents[1]
QW = REPO / "docs/phases/engine-breadth/milestones/question-wording-evidence"
AGE = REPO / "docs/phases/engine-breadth/milestones/age-blindness-asked-evidence"


def _number(value: Any) -> int | float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        try:
            parsed = float(value)
        except ValueError:
            return None
        return int(parsed) if parsed.is_integer() else parsed
    return None


def _numeric_diffs(expected: dict[str, Any], actual: dict[str, Any]) -> list[str]:
    diffs: list[str] = []
    for field, value in (expected.get("lines") or {}).items():
        wanted = _number(value)
        if wanted is None:
            continue
        got = _number((actual.get("lines") or {}).get(field))
        if got != wanted:
            diffs.append(f"{field}: fixture {wanted!r}, v89 {got!r}")
    wanted_base = _number(expected.get("base"))
    if wanted_base is not None and _number(actual.get("base")) != wanted_base:
        diffs.append(f"base: fixture {wanted_base!r}, v89 {_number(actual.get('base'))!r}")
    return diffs


def _recorded_shard(work: list[tuple[str, list[dict[str, Any]]]]) -> dict[str, Any]:
    owner = "tests.test_blocked_names_question_v89_recorded"
    evidence_loader.activate(owner)
    try:
        return _recorded_shard_body(work)
    finally:
        evidence_loader.finish(owner)


def _recorded_shard_body(work: list[tuple[str, list[dict[str, Any]]]]) -> dict[str, Any]:
    import tests.test_f1099b_backup_withholding_v83 as v83_test

    qw_rerun = evidence_loader.load(QW / "rerun.py", "bnq_t1_qw_rerun")
    age = evidence_loader.load(AGE / "rerun.py", "bnq_t1_age_rerun")
    harness = v83_test.track0().h
    core89 = harness.Core("v89", "v87", "v87")
    core88 = harness.Core("v88", "v86", "v86")
    expected = json.loads(qw_rerun.EXPECTED.read_text(encoding="utf-8"))
    failures: list[dict[str, Any]] = []
    for key, acts in work:
        fixture_key = key.removeprefix("v83/")
        prepared = age.adopt_v88(core88, age.answered(acts, age.implied(acts)))
        pin = cast(dict[str, Any], qw_rerun._pin_run(
            v83_test, core89, prepared,
            "demo.bnq.t1.v89.recorded." + fixture_key.replace("/", ".")))
        bad = _numeric_diffs(qw_rerun.recorded_pin(expected, fixture_key), pin)
        if bad:
            failures.append({"id": fixture_key, "diffs": bad[:12]})
    return {"runs": len(work), "failures": failures}


def test_recorded_v83_numbers_on_v89() -> None:
    import tests.test_f1099b_backup_withholding_v83 as v83_test

    qw_rerun = evidence_loader.load(QW / "rerun.py", "bnq_t1_qw_rerun")
    harness = evidence_loader.load(
        REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py",
        "bnq_t1_audit_harness",
    )
    expected = json.loads(qw_rerun.EXPECTED.read_text(encoding="utf-8"))
    asks = set(json.loads(
        (REPO / "docs/phases/engine-breadth/milestones/f1099b-box4-only-evidence/track0-neighbour.json"
         ).read_text(encoding="utf-8")
    )["asks_no_sale_present_ids"])
    work = [
        (f"v83/{key}", acts)
        for key, acts in qw_rerun.tasks(v83_test, harness, expected, asks)
    ]
    only = {item for item in os.environ.get("BNQ_V89_RECORDED_ONLY", "").split(",") if item}
    if only:
        work = [item for item in work if item[0].removeprefix("v83/") in only]
    else:
        assert len(work) == 298
    workers = min(4, max(1, (os.cpu_count() or 2) - 1))
    shards = [work[index::workers] for index in range(workers) if work[index::workers]]
    started = time.perf_counter()
    failures: list[dict[str, Any]] = []
    runs = 0
    context = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(max_workers=workers, mp_context=context) as pool:
        for part in pool.map(_recorded_shard, shards):
            runs += int(part["runs"])
            failures.extend(cast(list[dict[str, Any]], part["failures"]))
    wall = time.perf_counter() - started
    print(
        f"BNQ_V89_RECORDED runs={runs} wall_s={wall:.1f} workers={workers} "
        f"numeric_diffs={len(failures)}",
        flush=True,
    )
    for row in failures[:12]:
        print(f"BNQ_V89_RECORDED_DIFF {row['id']} {row['diffs']}", flush=True)
    assert runs == len(work)
    assert failures == []

