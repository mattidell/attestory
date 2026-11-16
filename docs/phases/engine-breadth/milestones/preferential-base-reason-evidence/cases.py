"""Plan cases on published v90 and scratch core v91.

Unanswered returns must name a question on every blocked field that v90 left
silent because the preferential base was inapplicable. Answered returns must
reach the 2025-instruction hand values. A return with no Schedule D, and a
return that already has a sale, must not gain a question or change a number.

    python3 cases.py <scratch-core.json>
"""

from __future__ import annotations

import copy
import json
import multiprocessing
import os
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tests import evidence_loader  # noqa: E402

import probe  # noqa: E402

BNQ = probe.BNQ
WATCH = (
    "form1040.line-7a", "form1040.line-11a", "form1040.line-15", "form1040.line-16",
    "form1040.line-24", "form1040.line-33", "form1040.line-37",
    "schedule-d.line-1b", "schedule-d.line-2", "schedule-d.line-3",
    "schedule-d.line-7", "schedule-d.line-16", "schedule-d.line-21",
)
# Instruction values recorded by blocked-names-question Track 0.
HAND = {
    "sd_yes_nothing": {"schedule-d.line-2": -6000, "schedule-d.line-7": -6000, "schedule-d.line-21": 3000},
    "sd_8949_no_unadmitted": {"schedule-d.line-3": -6000, "schedule-d.line-7": -6000, "schedule-d.line-21": 3000},
    "sd_sale_beside_8949_yes": {"schedule-d.line-3": -6000, "form1040.line-7a": -3000, "form1040.line-11a": 47000},
    "sd_amounts_disagree": {"schedule-d.line-3": -6000},
    "sd_path_b_unanswered": {"schedule-d.line-3": -6000, "schedule-d.line-21": 3000},
    "codeb_yes_nothing": {"schedule-d.line-1b": 6000},
    "codeb_sale_beside_8949_yes": {"schedule-d.line-1b": 6000, "form1040.line-7a": 6000, "form1040.line-11a": 56000},
    "codeb_amounts_disagree": {"schedule-d.line-1b": 6000},
    "exception1_personal_loss_8949": {
        "schedule-d.line-3": -6000, "schedule-d.line-7": -6000, "schedule-d.line-21": 3000,
        "form1040.line-7a": -3000, "form1040.line-11a": 47000,
    },
    "wash_adjustment_open": {"schedule-d.line-1b": -5000},
}
# The review's truthful sale on the four recorded returns. The dividend
# return may differ on the income and tax lines; the sale lines are shared.
RECORDED_HAND = {
    "schedule-d.line-3": -6000, "schedule-d.line-7": -6000, "schedule-d.line-21": 3000,
    "form1040.line-7a": -3000, "form1040.line-11a": 47000,
    "form1040.line-16": 3515, "form1040.line-24": 3515,
    "form1040.line-33": 4500, "form1040.line-37": 0,
}


def num(value: Any) -> Any:
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, (int, float)):
        return int(value) if float(value).is_integer() else value
    try:
        number = float(value)
    except (TypeError, ValueError):
        return value
    return int(number) if number.is_integer() else number


def compact(row: dict[str, Any]) -> dict[str, Any]:
    lines = {field: num((row.get("lines") or {}).get(field)) for field in WATCH}
    blocked = row.get("blocked_fields") or []
    return {
        "outcome": row.get("outcome"),
        "error": row.get("message"),
        "reasonless": row.get("reasonless_fields") or [],
        "page_questions": row.get("page_questions") or [],
        "silent_preferential": [
            field["field"] for field in blocked
            if not field.get("questions") and "capital-gains.selected-preferential-base" in (field.get("inapplicable") or [])
        ],
        "named": [field["field"] for field in blocked if field.get("questions")],
        "lines": lines,
        "producer": (row.get("producers") or {}).get("capital-gains.selected-preferential-base"),
    }


def _worker(payload: tuple[str | None, list[tuple[str, list[dict[str, Any]]]]]) -> list[dict[str, Any]]:
    core_json, shard = payload
    evidence_loader.activate(probe.OWNER)
    try:
        found = []
        for case_id, acts in shard:
            found.append({"id": case_id, **compact(probe.run_case(case_id, acts, core_json))})
        return found
    finally:
        evidence_loader.finish(probe.OWNER)


def truthful_sale(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    evidence_loader.activate(probe.OWNER)
    common = evidence_loader.load(BNQ / "common.py", "common")
    harness = common.harness()
    sold = harness.sale(copy.deepcopy(acts), "no1099b", "st", proceeds=2000, basis=8000, tag="pbr-sale")
    return harness.answer(
        sold, q2="yes", form8949="no", path_b="no", ic80="yes",
        exc1_only_2a="no", exc1_no_losses="no",
    )


def build(core_json: str) -> list[tuple[str, list[dict[str, Any]]]]:
    evidence_loader.activate(probe.OWNER)
    base = probe.build_lists()
    # track0.py imports the name "probe". The interpreter's module dict still
    # holds this directory's probe.py, and that is what the import binds, so
    # point that dict at the blocked-names-question probe for the load only.
    bnq_probe = evidence_loader.load(BNQ / "probe.py", "bnq_probe")
    real = evidence_loader._interpreter_modules
    saved_real = real.get("probe")
    saved_visible = sys.modules.get("probe")
    real["probe"] = bnq_probe
    sys.modules["probe"] = bnq_probe
    try:
        track = evidence_loader.load(BNQ / "track0.py", "bnq_track0_cases")
    finally:
        if saved_real is not None:
            real["probe"] = saved_real
        else:
            real.pop("probe", None)
        if saved_visible is not None:
            sys.modules["probe"] = saved_visible
        else:
            sys.modules.pop("probe", None)
    lists = [(case_id, acts) for case_id, acts in base if not case_id.startswith("internal-subtotal/")]
    for case_id, acts in base:
        if case_id.startswith("recorded/"):
            lists.append((case_id + "/sale", truthful_sale(acts)))
    for case_id in HAND:
        lists.append(("answered/" + case_id, probe._state_age(track.resolved(case_id, Path(core_json)))))
    evidence_loader.finish(probe.OWNER)
    return lists


def run(core_json: str | None, lists: list[tuple[str, list[dict[str, Any]]]]) -> dict[str, Any]:
    workers = max(1, (os.cpu_count() or 2) - 1)
    shards = [(core_json, lists[index::workers]) for index in range(workers) if lists[index::workers]]
    found: list[dict[str, Any]] = []
    context = multiprocessing.get_context("spawn")
    with context.Pool(workers) as pool:
        for part in pool.map(_worker, shards):
            found.extend(part)
    return {row["id"]: row for row in found}


def hand_misses(row: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    misses = []
    for field, wanted in expected.items():
        got = (row.get("lines") or {}).get(field)
        if got != wanted:
            misses.append(f"{field}: hand {wanted}, live {got}")
    return misses


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: cases.py <scratch-core.json>")
    core_json = sys.argv[1]
    lists = build(core_json)
    v91 = run(core_json, lists)
    v90 = run(None, lists)
    plan_fields = [
        "form1040.line-7a", "form1040.line-9", "form1040.line-11a", "form1040.line-11b",
        "form1040.line-13b", "form1040.line-14", "form1040.line-15", "form1040.line-24",
        "form1040.line-33", "form1040.line-37",
    ]
    unanswered = {}
    for name in probe.RECORDED:
        row = v91["recorded/" + name]
        unanswered[name] = {
            "reasonless": row["reasonless"],
            "silent_preferential": row["silent_preferential"],
            "plan_fields_without_a_question": [
                field for field in plan_fields if field not in row["named"]
            ],
            "producer": row["producer"],
            "page_questions": row["page_questions"],
        }
    answered_recorded = {}
    for name in probe.RECORDED:
        row = v91["recorded/" + name + "/sale"]
        answered_recorded[name] = {
            "reasonless": row["reasonless"],
            "lines": row["lines"],
            "hand_misses": hand_misses(row, RECORDED_HAND),
            "same_numbers_as_v90": v90["recorded/" + name + "/sale"]["lines"] == row["lines"],
        }
    ten = {}
    for case_id, expected in HAND.items():
        opened = v91.get("schedule-d-refused/" + case_id) or v91.get("code-b-refused/" + case_id) or v91.get("exception1-no/" + case_id) or v91.get("wash-admission/" + case_id)
        # The builders are stored under their group prefix. Find the unanswered row.
        opened = next(row for key, row in v91.items() if key.endswith("/" + case_id) and not key.startswith("answered/"))
        done = v91["answered/" + case_id]
        ten[case_id] = {
            "unanswered_has_question": bool(opened["page_questions"]) and not opened["silent_preferential"],
            "hand_misses": hand_misses(done, expected),
            "same_numbers_as_v90": v90["answered/" + case_id]["lines"] == done["lines"],
            "answered_reasonless": done["reasonless"],
        }
    blank90, blank91 = v90["blank/opened"], v91["blank/opened"]
    sale_case = "answered/sd_sale_beside_8949_yes"
    payload = {
        "unanswered_recorded": unanswered,
        "answered_recorded": answered_recorded,
        "track0": ten,
        "no_schedule_d": {
            "v90_page_questions": blank90["page_questions"],
            "v91_page_questions": blank91["page_questions"],
            "new_questions": sorted(set(blank91["page_questions"]) - set(blank90["page_questions"])),
            "same_lines": blank90["lines"] == blank91["lines"],
        },
        "sale_and_schedule_d_required": {
            "case": sale_case,
            "same_lines": v90[sale_case]["lines"] == v91[sale_case]["lines"],
            "v90_lines": v90[sale_case]["lines"],
            "v91_lines": v91[sale_case]["lines"],
        },
    }
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit("cases output contains a local path")
    (HERE / "cases-output.json").write_text(text, encoding="utf-8")
    print(json.dumps({
        "unanswered_reasonless": {name: row["reasonless"] for name, row in unanswered.items()},
        "recorded_hand": {name: row["hand_misses"] for name, row in answered_recorded.items()},
        "track0_hand": {name: row["hand_misses"] for name, row in ten.items()},
        "no_schedule_d_new": payload["no_schedule_d"]["new_questions"],
        "sale_same": payload["sale_and_schedule_d_required"]["same_lines"],
    }, indent=2))


if __name__ == "__main__":
    main()
