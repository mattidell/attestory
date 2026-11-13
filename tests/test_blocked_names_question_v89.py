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
P = "tax.us.2025."


def _track0() -> ModuleType:
    evidence_loader.load(EVIDENCE / "common.py", "common")
    evidence_loader.load(EVIDENCE / "probe.py", "probe")
    evidence_loader.load(EVIDENCE / "prototype.py", "prototype")
    return evidence_loader.load(EVIDENCE / "track0.py", "bnq_t1_v89_track0")


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
    corrected = track.answer(added, track.NO_8949, "no", "late-form8949-no", core_path)
    rows = [
        {"id": "sale_after_form8949_yes.form8949_yes", "acts": start},
        {"id": "sale_after_form8949_yes.sale_added_old_yes", "acts": added, "open": True},
        {"id": "sale_after_form8949_yes.truthful_no", "acts": corrected,
         "hand": {"schedule-d.line-3": -6000}},
    ]

    start = track.probe.sale("no1099b", rows={"basis": 2000})
    corrected = track.correct_member(start, "f8949.no1099b-st-txn.basis|", 8000,
                                     "late-correct-basis")
    rows.extend([
        {"id": "amount_corrected.disagrees", "acts": start, "open": True},
        {"id": "amount_corrected.corrected", "acts": corrected,
         "hand": {"schedule-d.line-3": -6000}},
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
        {"id": "wash_adjustment_after_close.closed", "acts": start},
        {"id": "wash_adjustment_after_close.adjustment_added_open", "acts": added, "open": True},
        {"id": "wash_adjustment_after_close.reclosed", "acts": reclosed,
         "hand": {"schedule-d.line-1b": -5000}},
    ])
    return rows


def _run_case_shard(work: list[dict[str, Any]]) -> dict[str, Any]:
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
            if bad and not result.get("questions"):
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

