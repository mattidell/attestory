"""Published core v91 names the eight questions on the preferential base.

Measured reason: each case uses live_coordinate_run and the presentation
projection, so the module is outside the 3.0 second fast-lane budget.
Authority, matrix, late, recorded, and blocked-names-question claims share
one result for each distinct act list on each core. Hand values are the
2025-instruction literals in Track 0. A case whose id says unanswered does
not receive the sale or the Path B answer from a shared helper.
"""

from __future__ import annotations

import copy
import hashlib
import json
import multiprocessing
import os
import tempfile
from pathlib import Path
from typing import Any

import pytest

from tests import evidence_loader


pytestmark = pytest.mark.live

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/preferential-base-reason-evidence"
BNQ = REPO / "docs/phases/engine-breadth/milestones/blocked-names-question-evidence"
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
OWNER = "tests.test_preferential_base_reason_v91"
PATH_B = "tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments"
EIGHT = [
    "f1099b.noncovered-sold.source-closure",
    "f8949.no1099b-sold.source-closure",
    "schedule-d-boundary.no-form8949-sources",
    "schedule-d-boundary.no-other-form8949-adjustments",
    "exception1.only-box2a-capital-gains",
    "exception1.no-capital-losses",
    "exception1.no-qof-deferral",
    "exception1.no-boxes-2b-2c-2d",
]
FIELDS = [
    "form1040.line-7a",
    "form1040.line-9",
    "form1040.line-11a",
    "form1040.line-11b",
    "form1040.line-13b",
    "form1040.line-14",
    "form1040.line-15",
    "form1040.line-6b",
    "form1040.line-19",
    "form1040.line-24",
    "form1040.line-27a",
    "form1040.line-28",
    "form1040.line-32",
    "form1040.line-33",
    "form1040.line-34",
    "form1040.line-35a",
    "form1040.line-37",
    "form1040.tax-after-credits",
    "form.eic-worksheet-a.line-3",
    "form.eic-worksheet-a.line-5",
    "form.eic-worksheet-a.line-6",
    "form.sch8812.line-14",
    "form.sch8812.line-17",
]
RECORDED_HAND = {
    "schedule-d.line-3": -6000,
    "schedule-d.line-7": -6000,
    "schedule-d.line-21": 3000,
    "form1040.line-7a": -3000,
    "form1040.line-11a": 47000,
    "form1040.line-15": 31250,
    "form1040.line-16": 3515,
    "form1040.line-24": 3515,
    "form1040.line-33": 4500,
    "form1040.line-37": 0,
}


def _track() -> Any:
    evidence_loader.load(EVIDENCE / "probe.py", "probe")
    evidence_loader.load(EVIDENCE / "prototype.py", "prototype")
    evidence_loader.load(EVIDENCE / "rerun.py", "rerun")
    return evidence_loader.load(EVIDENCE / "track0.py", "pbr_t1_v91_track0")


def _digest(acts: list[dict[str, Any]]) -> str:
    return hashlib.sha256(json.dumps(acts, sort_keys=True).encode("utf-8")).hexdigest()


def _asserted_fact_ids(acts: list[dict[str, Any]]) -> list[str]:
    found = []
    for act in acts:
        if act.get("kind") != "assertion":
            continue
        payload = act.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if isinstance(finding, dict):
            found.append(str(finding.get("fact_id") or ""))
    return found


def _leave_unanswered(case_id: str, acts: list[dict[str, Any]]) -> None:
    """A case named unanswered keeps that fact out of its assertions."""
    if "unanswered" not in case_id:
        return
    if case_id.endswith("/unanswered") and "pbr-sale" in json.dumps(acts):
        raise AssertionError(case_id + " includes the shared sale answer")
    if case_id == "bnq/sd_path_b_unanswered":
        prefix = PATH_B + "|"
        if any(fact_id.startswith(prefix) for fact_id in _asserted_fact_ids(acts)):
            raise AssertionError(case_id + " asserts Path B")


def _matrix(track: Any) -> list[tuple[str, list[dict[str, Any]]]]:
    lists: list[tuple[str, list[dict[str, Any]]]] = []
    for case_id, acts in track._recorded():
        lists.append((case_id + "/unanswered", acts))
        lists.append((case_id + "/answered", track._age(track._sale_answer(acts))))
    for name, fact in (
        ("exc1-only2a-no", "exception1.only-box2a-capital-gains"),
        ("exc1-nolosses-no", "exception1.no-capital-losses"),
    ):
        unanswered = track._exception(track._base(), "no")
        unanswered = track._say(unanswered, fact, "no", fact)
        unanswered = track._activity(unanswered, "none")
        lists.append((name + "/unanswered", track._age(unanswered)))
        answered = track._boundary(track._exception(copy.deepcopy(unanswered), "no"), "answered", sale=False)
        answered = track._say(answered, fact, "yes", fact + "-yes")
        lists.append((name + "/answered", track._age(answered)))
    box = track.add_box2a(track._activity(track._exception(track._base(), "no"), "none"))
    lists.append(("box2a-only/unanswered", track._age(box)))
    lists.append(("box2a-only/answered", track._age(track._boundary(copy.deepcopy(box), "answered", sale=False))))
    nothing = track._activity(track._exception(track._base(), "no"), "none")
    lists.append(("nothing/unanswered", track._age(nothing)))
    lists.append(("nothing/answered", track._age(track._boundary(copy.deepcopy(nothing), "answered", sale=False))))
    carry = track._activity(track._exception(track._base(), "no"), "amount")
    lists.append(("carryover/unanswered", track._age(carry)))
    lists.append(("carryover/answered", track._age(track._boundary(copy.deepcopy(carry), "answered", sale=False))))
    mistaken = track._exception(track._base(), "no")
    mistaken = track._say(mistaken, "exception1.only-box2a-capital-gains", "no", "only2a")
    mistaken = track.add_box2a(track._activity(mistaken, "none"))
    lists.append(("other-source-box2a/unanswered", track._age(mistaken)))
    corrected = track._say(copy.deepcopy(mistaken), "exception1.only-box2a-capital-gains", "yes", "only2a-yes")
    lists.append(("other-source-box2a/answered", track._age(track._boundary(corrected, "answered", sale=False))))
    return lists


def _late(track: Any) -> list[tuple[str, list[dict[str, Any]]]]:
    blocked = track._age(track._boundary(
        track._activity(track._exception(track._base(), "required"), "none"),
        "answered",
        sale=False,
    ))
    sold = track._age(track._sale_answer(blocked))
    removed = track.remove_sale(sold, "no1099b", "st", "pbr-sale")
    exception_yes = track._age(track._exception(copy.deepcopy(blocked), "no"))
    return [
        ("late/blocked", blocked),
        ("late/sale-entered", sold),
        ("late/sale-removed", track._age(removed)),
        ("late/exception-yes", exception_yes),
    ]


def _cases(track: Any) -> list[tuple[str, list[dict[str, Any]]]]:
    lists: list[tuple[str, list[dict[str, Any]]]] = []
    for activity in track.ACTIVITIES:
        for conclusion in track.CONCLUSIONS:
            for boundary in track.BOUNDARIES:
                case_id = f"authority/{activity}/{conclusion}/{boundary}"
                lists.append((case_id, track.cell_acts(activity, conclusion, boundary)))
    lists.extend(_matrix(track))
    lists.extend(_late(track))
    probe = evidence_loader.load(BNQ / "probe.py", "pbr_t1_v91_bnq_probe")
    for case_id, (group, build, _note) in probe.CASES.items():
        if group == "internal-subtotal":
            continue
        lists.append(("bnq/" + case_id, build()))
    for case_id, acts in lists:
        _leave_unanswered(case_id, acts)
    return lists


def _v91_core_json() -> str:
    handle = tempfile.NamedTemporaryFile(prefix="pbr-v91-", suffix=".json", delete=False)
    handle.write(json.dumps({
        "version": "v91",
        "registry": "v89",
        "release_version": "v89",
        "content": str(CONTENT),
        "releases": str(RELEASES),
    }).encode("utf-8") + b"\n")
    handle.close()
    return handle.name


def _run_shard(work: list[dict[str, Any]]) -> list[dict[str, Any]]:
    evidence_loader.activate(OWNER)
    try:
        track = _track()
        core_json = _v91_core_json()
        rows = []
        try:
            for item in work:
                case_id = "run-" + str(item["digest"])[:16]
                acts = item["acts"]
                v90 = track.compact(track.execute(case_id + "-v90", acts, None))
                v91 = track.compact(track.execute(case_id + "-v91", acts, core_json))
                rows.append({"digest": item["digest"], "v90": v90, "v91": v91})
        finally:
            Path(core_json).unlink(missing_ok=True)
        return rows
    finally:
        evidence_loader.finish_all()


def _blocked_map(row: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {field["field"]: field for field in row.get("blocked") or []}


def _view(row: dict[str, Any]) -> dict[str, Any]:
    blocked = {
        field: {"missing": item.get("missing"), "questions": item.get("questions")}
        for field, item in sorted(_blocked_map(row).items())
    }
    return {"lines": row.get("lines"), "values": row.get("values"), "questions": row.get("page_questions"), "blocked": blocked}


def _failures(runs: dict[str, dict[str, Any]], lists: list[tuple[str, list[dict[str, Any]]]]) -> list[str]:
    track = _track()
    by_id = {case_id: runs[_digest(acts)] for case_id, acts in lists}
    failures: list[str] = []

    def pair(case_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
        row = by_id[case_id]
        return row["v90"], row["v91"]

    for activity in track.ACTIVITIES:
        for conclusion in track.CONCLUSIONS:
            for boundary in track.BOUNDARIES:
                case_id = f"authority/{activity}/{conclusion}/{boundary}"
                v90, v91 = pair(case_id)
                if v90.get("outcome") != "success" or v91.get("outcome") != "success":
                    failures.append(f"{case_id} outcome {v90.get('outcome')} {v91.get('outcome')}")
                    continue
                seen = track.observed_activity({**v90["lines"], **v90["values"]})
                seen_conclusion = track.observed_conclusion(v90)
                open_counts = boundary == "open" and v90["producer"].get("disposition") == "blocked" and any(
                    str(name).endswith("-count") for name in v90["producer"].get("missing") or []
                )
                axes = seen_conclusion == conclusion and (seen == activity or open_counts)
                if not axes:
                    failures.append(f"{case_id} axes {seen} {seen_conclusion}")
                    continue
                differs = v90["producer"] != v91["producer"]
                realized = (
                    activity == "none" and conclusion == "required" and boundary == "answered"
                    and seen == "none" and seen_conclusion == "required"
                )
                if realized:
                    names = (
                        v91["producer"].get("disposition") == "blocked"
                        and v91["producer"].get("code") == "DEPENDENCY_ABSENT"
                        and v91["producer"].get("missing") == EIGHT
                        and v90["producer"].get("disposition") == "inapplicable"
                    )
                    if not names or not differs:
                        failures.append(f"{case_id} did not name the eight questions")
                elif differs:
                    failures.append(f"{case_id} changed another cell")

    hands = {
        "exc1-only2a-no": track.WAGE_HAND,
        "exc1-nolosses-no": track.WAGE_HAND,
        "box2a-only": track.BOX2A_HAND,
        "nothing": track.WAGE_HAND,
        "carryover": track.CARRY_HAND,
        "other-source-box2a": track.BOX2A_HAND,
    }
    matrix_ids = [
        case_id for case_id, _acts in lists
        if case_id.endswith("/answered") and not case_id.startswith(("authority/", "late/"))
    ]
    for case_id in matrix_ids:
        stem = case_id[: -len("/answered")]
        unanswered_v91 = pair(stem + "/unanswered")[1]
        v90, v91 = pair(case_id)
        hand = RECORDED_HAND if stem.startswith("recorded/") else hands[stem]
        misses = track.hand_misses(v91, hand)
        if unanswered_v91.get("silent"):
            failures.append(f"{stem} unanswered silent {unanswered_v91.get('silent')}")
        if misses or v90.get("lines") != v91.get("lines") or v91.get("outcome") != "success":
            failures.append(f"{stem} hand {misses} lines_same={v90.get('lines') == v91.get('lines')}")

    blocked_v90, blocked = pair("late/blocked")
    sale_v90, sale = pair("late/sale-entered")
    removed_v90, removed = pair("late/sale-removed")
    wage_v90, wage = pair("late/exception-yes")
    del blocked_v90
    if blocked["producer"].get("disposition") != "blocked" or blocked["producer"].get("missing") != EIGHT:
        failures.append("late blocked start does not name the eight")
    if blocked.get("silent"):
        failures.append(f"late blocked silent {blocked.get('silent')}")
    if sale["producer"].get("disposition") != "published" or track.hand_misses(sale, RECORDED_HAND):
        failures.append(f"late sale hand {track.hand_misses(sale, RECORDED_HAND)}")
    if sale_v90.get("lines") != sale.get("lines"):
        failures.append("late sale lines differ from v90")
    removal_same = track.signature(removed["producer"]) == track.signature(removed_v90["producer"])
    removal_allowed = (
        removed["producer"].get("disposition") == "blocked"
        and removed["producer"].get("missing") == EIGHT
        and removed_v90["producer"].get("disposition") == "inapplicable"
    )
    if removed.get("lines") != removed_v90.get("lines") or not (removal_same or removal_allowed):
        failures.append("late removal does not drop the sale with v90")
    if wage["producer"].get("disposition") != "published" or track.hand_misses(wage, track.WAGE_HAND):
        failures.append(f"late exception yes hand {track.hand_misses(wage, track.WAGE_HAND)}")
    if wage_v90.get("lines") != wage.get("lines"):
        failures.append("late exception yes lines differ from v90")

    for name in (
        "m_2a_only_exc1_only2a_no",
        "m_empty_exc1_nolosses_no",
        "m_empty_exc1_only2a_no",
        "t4_s1_removed",
    ):
        v90, v91 = pair("recorded/" + name + "/unanswered")
        if v91.get("outcome") != "success":
            failures.append(f"{name} outcome {v91.get('outcome')}")
            continue
        blocked_fields = _blocked_map(v91)
        if v91.get("silent"):
            failures.append(f"{name} silent {v91.get('silent')}")
        if v91.get("duplicate_questions"):
            failures.append(f"{name} duplicate {v91.get('duplicate_questions')}")
        for field in FIELDS:
            row = blocked_fields.get(field)
            if row is None:
                failures.append(f"{name} {field} is not blocked")
            elif row.get("questions") is None or len(row.get("questions") or []) != 8:
                failures.append(f"{name} {field} questions {len(row.get('questions') or [])}")
        for field, value in v90.get("lines", {}).items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                if field in blocked_fields:
                    failures.append(f"{name} {field} computed on v90 and blocked on v91")

    for case_id, _acts in lists:
        if not case_id.startswith("bnq/"):
            continue
        v90, v91 = pair(case_id)
        if _view(v90) != _view(v91) or v90.get("outcome") != "success" or v91.get("outcome") != "success":
            failures.append(f"{case_id} changed names, questions, or values")
    return failures


def test_published_v91_names_the_eight_questions() -> None:
    evidence_loader.finish_all()
    track = _track()
    lists = _cases(track)
    grouped: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for case_id, acts in lists:
        digest = _digest(acts)
        if digest not in grouped:
            grouped[digest] = {"digest": digest, "acts": acts, "ids": []}
            order.append(digest)
        grouped[digest]["ids"].append(case_id)
    evidence_loader.finish_all()

    workers = max(1, (os.cpu_count() or 2) - 1)
    shards = [ [grouped[digest] for digest in order[index::workers]] for index in range(workers) ]
    shards = [shard for shard in shards if shard]
    found: dict[str, dict[str, Any]] = {}
    context = multiprocessing.get_context("spawn")
    with context.Pool(len(shards)) as pool:
        for part in pool.map(_run_shard, shards):
            for row in part:
                found[str(row["digest"])] = row
    assert set(found) == set(order)
    failures = _failures(found, lists)
    assert failures == []
