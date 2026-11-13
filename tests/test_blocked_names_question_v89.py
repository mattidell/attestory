"""Published core v89 runs the de-duplicated Track 0 behavior surface.

Measured reason: each case uses ``live_coordinate_run`` and the production
presentation model, so the module is outside the 3.0 second fast-lane budget.
Authority, matrix, late, and surface claims share one result for each distinct
act list. Hand values are the instruction-derived literals in Track 0.
"""

from __future__ import annotations

import copy
import hashlib
import json
import multiprocessing
import os
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest

from tests import evidence_loader


pytestmark = pytest.mark.live

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/blocked-names-question-evidence"
AGE = REPO / "docs/phases/engine-breadth/milestones/age-blindness-asked-evidence"
P = "tax.us.2025."
PRESENT_NO_SALE_BOX4 = P + "f1099b.no-sale-box4-present"
V82_LINE16_RETURNS = (
    "m_2a_only_exc1_only2a_no",
    "m_empty_exc1_nolosses_no",
    "m_empty_exc1_only2a_no",
    "t4_s1_removed",
)
LINE16_AND_BELOW = (
    "form1040.line-16",
    "form1040.line-24",
    "form1040.line-33",
    "form1040.line-37",
)


def _track0() -> ModuleType:
    evidence_loader.load(EVIDENCE / "common.py", "common")
    evidence_loader.load(EVIDENCE / "probe.py", "probe")
    evidence_loader.load(EVIDENCE / "prototype.py", "prototype")
    return evidence_loader.load(EVIDENCE / "track0.py", "bnq_t1_v89_track0")


def _age() -> ModuleType:
    return evidence_loader.load(AGE / "rerun.py", "bnq_t1_v89_age")


def _stated_v88_facts(track: ModuleType, acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    age = _age()
    prepared = age.answered(acts, age.implied(acts))
    if not age.recorded(prepared, PRESENT_NO_SALE_BOX4):
        prepared = track.h.say(prepared, PRESENT_NO_SALE_BOX4, "no", "bnq-r1-box4")
    return cast(list[dict[str, Any]], prepared)


def _digest(acts: list[dict[str, Any]]) -> str:
    return hashlib.sha256(json.dumps(acts, sort_keys=True).encode("utf-8")).hexdigest()


def _late_rows(track: ModuleType, core_path: Path) -> list[dict[str, Any]]:
    start = track.probe.empty(form8949="yes", path_b="yes")
    added = track.h.sale(start, "no1099b", "st", proceeds=2000, basis=8000,
                         tag="late-form8949-sale")
    added = track.probe.answered(
        added, q2="yes", form8949="yes", path_b="no", ic80="yes",
        exc1_only_2a="no", exc1_no_losses="no",
    )
    rows = [
        {"id": "sale_after_form8949_yes.sale_added_old_yes", "acts": added, "open": True},
    ]

    start = track.probe.sale("no1099b", rows={"basis": 2000})
    rows.extend([
        {"id": "amount_corrected.disagrees", "acts": start, "open": True},
    ])

    start = track.probe.sale("w", form8949="no", path_b="yes")
    family = P + "f1099b.covered-w-st-adjustment"
    added = track.h.sale(copy.deepcopy(start), "w", "st", proceeds=500, basis=700, wash=200,
                         tag="late-wash-sale")
    added = track.statement_reported_no(
        added, "demo.sfa.late-wash-sale.statement", "late-wash")
    added = track.h.strip(added, family + ".source-closure")
    reclosed = track.statement_box4_zero(
        track.close_family(copy.deepcopy(added), family, "late-wash"))
    rows.extend([
        {"id": "wash_adjustment_after_close.adjustment_added_open", "acts": added, "open": True},
        {"id": "wash_adjustment_after_close.reclosed", "acts": reclosed,
         "hand": {"schedule-d.line-1b": -5000}},
    ])
    return rows


def _run_case_shard(work: list[dict[str, Any]]) -> dict[str, Any]:
    owner = "tests.test_blocked_names_question_v89"
    evidence_loader.activate(owner)
    try:
        return _run_case_shard_body(work)
    finally:
        evidence_loader.finish(owner)


def _run_case_shard_body(work: list[dict[str, Any]]) -> dict[str, Any]:
    track = _track0()
    core = track.h.Core("v89", "v87", "v87")
    question_sentences = {
        str(entry["question"])
        for entry in track.resolver_catalog(core).values()
        if entry.get("question")
    }
    failures: list[str] = []
    for group in work:
        digest = str(group["digest"])
        result = track.run(
            core, group["acts"], "demo.bnq.t1.v89." + digest[:16], scratch=False)
        if result.get("outcome") != "success":
            failures.append(
                f"{digest[:12]} outcome {result.get('outcome')}: {result.get('error')}")
            continue
        if any(claim["category"] == "surface" for claim in group["claims"]):
            silent = [
                field
                for blocked in result.get("blocked") or []
                if not set(blocked.get("reasons") or []) & question_sentences
                for field in blocked.get("fields") or []
            ]
            if silent:
                failures.append(f"{digest[:12]} blocked fields without a question: {silent}")
        for claim in group["claims"]:
            if claim.get("open") and not result.get("questions"):
                failures.append(f"{claim['category']} {claim['id']}: no question")
            hand = cast(dict[str, Any], claim.get("hand") or {})
            bad = track.hand_failures(result, hand)
            if bad:
                failures.append(f"{claim['category']} {claim['id']}: {bad}")
    return {"runs": len(work), "failures": failures}


def test_track0_authority_matrix_late_and_surface_on_v89(tmp_path: Path) -> None:
    track = _track0()
    core = track.h.Core("v89", "v87", "v87")
    core_path = tmp_path / "core.json"
    core_path.write_text(json.dumps({
        "version": "v89", "registry": "v87", "release_version": "v87",
        "content": str(core.content), "releases": str(core.releases),
    }) + "\n", encoding="utf-8")

    rows: list[dict[str, Any]] = []
    for case_id, builder in track.BUILDERS.items():
        unresolved = builder()
        resolved = track.resolved(case_id, core_path)
        for category in ("authority", "matrix", "surface"):
            rows.append({"category": category, "id": case_id + ".unanswered",
                         "acts": unresolved, "open": True})
            rows.append({"category": category, "id": case_id + ".truthful_answer",
                         "acts": resolved, "hand": track.HAND.get(case_id, {})})
    for case_id, acts in track.long_term_authority_cases().items():
        rows.append({"category": "authority", "id": case_id, "acts": acts, "open": True})
    rows.extend({"category": "late", **row} for row in _late_rows(track, core_path))
    age = _age()
    for row in rows:
        row["acts"] = age.answered(row["acts"], age.implied(row["acts"]))

    grouped: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for row in rows:
        digest = _digest(cast(list[dict[str, Any]], row["acts"]))
        if digest not in grouped:
            grouped[digest] = {"acts": row["acts"], "claims": []}
            order.append(digest)
        grouped[digest]["claims"].append(row)

    work = [{"digest": digest, **grouped[digest]} for digest in order]
    workers = min(4, max(1, (os.cpu_count() or 2) - 1))
    shards = [work[index::workers] for index in range(workers) if work[index::workers]]
    failures: list[str] = []
    runs = 0
    started = time.perf_counter()
    context = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(max_workers=workers, mp_context=context) as pool:
        for part in pool.map(_run_case_shard, shards):
            runs += int(part["runs"])
            failures.extend(cast(list[str], part["failures"]))
    wall = time.perf_counter() - started
    print(
        f"BNQ_V89_CASES runs={runs} wall_s={wall:.1f} workers={workers} "
        f"claims={len(rows)} failed={len(failures)}",
        flush=True,
    )
    assert runs == len(order)
    assert failures == []


def test_v82_recorded_line16_and_below_name_their_questions() -> None:
    """BNQ-R1: the four recorded v82 returns name questions on line 16 and below."""
    import tests.test_sale_family_audit_v82 as sfa

    track = _track0()
    sfa_track = sfa.track0()
    core82 = sfa.v82(sfa_track)
    core = track.h.Core("v89", "v87", "v87")
    failures: list[str] = []
    for name in V82_LINE16_RETURNS:
        acts = _stated_v88_facts(
            track, sfa.track0_acts(sfa_track, name, "honest", core82))
        result = track.run(
            core, acts, "demo.bnq.r1.v82." + name.replace("_", "-"), scratch=False)
        if result.get("outcome") != "success":
            failures.append(f"{name} outcome {result.get('outcome')}: {result.get('error')}")
            continue
        blocked = list(result.get("blocked") or [])
        line16 = next(
            (item for item in blocked if "form1040.line-16" in (item.get("fields") or [])),
            None,
        )
        if line16 is None:
            failures.append(f"{name} form1040.line-16 is not blocked")
        elif not line16.get("questions"):
            failures.append(
                f"{name} form1040.line-16 names no question missing={line16.get('missing')!r}")
        if not result.get("questions"):
            failures.append(f"{name} page names no question")
        for field in LINE16_AND_BELOW[1:]:
            row = next((item for item in blocked if field in (item.get("fields") or [])), None)
            if row is None:
                failures.append(f"{name} {field} is not blocked")
    assert failures == []


def test_named_cases_reach_instruction_hand_values(tmp_path: Path) -> None:
    """BNQ-R2: the three named truthful returns reach their 2025-instruction values."""
    track = _track0()
    age = _age()
    core = track.h.Core("v89", "v87", "v87")
    core_path = tmp_path / "core.json"
    core_path.write_text(json.dumps({
        "version": "v89", "registry": "v87", "release_version": "v87",
        "content": str(core.content), "releases": str(core.releases),
    }) + "\n", encoding="utf-8")
    failures: list[str] = []
    for case_id in (
        "exception1_personal_loss_8949",
        "sd_sale_beside_8949_yes",
        "codeb_sale_beside_8949_yes",
    ):
        acts = track.resolved(case_id, core_path)
        acts = age.answered(acts, age.implied(acts))
        result = track.run(
            core, acts, "demo.bnq.r2." + case_id.replace("_", "-"), scratch=False)
        hand = track.HAND[case_id]
        bad = track.hand_failures(result, hand)
        if result.get("outcome") != "success":
            failures.append(f"{case_id} outcome {result.get('outcome')}: {result.get('error')}")
        if bad:
            failures.append(f"{case_id}: {bad}")
    assert failures == []

