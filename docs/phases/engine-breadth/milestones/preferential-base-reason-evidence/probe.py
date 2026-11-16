"""Reproduce reasonless blocked lines on published core v90.

Evidence for the preferential-base-reason milestone. Every case is one
``live_coordinate_run`` of synthetic ``demo.*`` acts through the production
coordinator and the presentation projection. Nothing here edits packages/
or tests/.

The four recorded v82 lists are the ones blocked-names-question review note
BNQ-R7 names. The other lists are the blocked-names-question builders and a
blank return, used to see whether another producer leaves a filer-visible
field blocked with no question.
"""

from __future__ import annotations

import json
import multiprocessing
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tests import evidence_loader  # noqa: E402

P = "tax.us.2025."
OWNER = "pbr_p0_probe"
BNQ = REPO / "docs/phases/engine-breadth/milestones/blocked-names-question-evidence"
AGE = REPO / "docs/phases/engine-breadth/milestones/age-blindness-asked-evidence"
RECORDED = (
    "m_2a_only_exc1_only2a_no",
    "m_empty_exc1_nolosses_no",
    "m_empty_exc1_only2a_no",
    "t4_s1_removed",
)
PREFERENTIAL = "capital-gains.selected-preferential-base"
CONCLUSION = "schedule-d-required.conclusion"
# BNQ-R7's stated reasonless lines. The live table confirms or corrects this.
BNQ_R7_FIELDS = [
    "form1040.line-7a", "form1040.line-7b", "form1040.line-8", "form1040.line-9",
    "form1040.line-10", "form1040.line-11a", "form1040.line-11b", "form1040.line-12a",
    "form1040.line-12b", "form1040.line-12c", "form1040.line-12d", "form1040.line-12e",
    "form1040.line-13a", "form1040.line-13b", "form1040.line-14", "form1040.line-15",
    "form1040.line-24", "form1040.line-33", "form1040.line-37",
]
# Published v90 rules whose when contains a conditional_dependency_set.
# "same" means the set can skip its members while a sibling conjunct is false
# and that skipped member is still an answer the filer must give.
GUARD_SHAPES = {
    "selected-preferential-base": {
        "same_pattern": True,
        "why": "Activity false skips the Schedule D boundary answers. The sibling conjunct then requires schedule-d-required.conclusion = no, so a required Schedule D with no recorded sale makes the guard false.",
    },
    "schedule3-line1-direct-ftc": {
        "same_pattern": False,
        "why": "The scope answers are read only when foreign-tax box 7 is above zero. With no foreign tax the credit does not apply, and a blocked box 7 family blocks the guard instead of turning it false.",
    },
    "ss-benefits-worksheet": {
        "same_pattern": False,
        "why": "The benefits-scope answers are read only when net benefits are above zero, and the lived-apart answer only when filing status is married filing separately. Neither is open on a return the worksheet does not apply to.",
    },
    "form1040-line6d": {
        "same_pattern": False,
        "why": "The lived-apart answer is read when filing status is married filing separately. Any other status makes the line inapplicable; the answer is not open.",
    },
    "form1040-line6d-not-checked": {
        "same_pattern": False,
        "why": "Same filing-status gate as line 6d.",
    },
    "form1040-line12d-spouse-age": {
        "same_pattern": False,
        "why": "The spouse age and separate-return answers sit under a filing-status choose whose other branch is inapplicable. The set condition is constantly true, so an applicable branch reads the answer.",
    },
    "form1040-line12d-spouse-age-not-checked": {
        "same_pattern": False,
        "why": "Same filing-status gate as the spouse age box.",
    },
    "form1040-line12d-spouse-blind": {
        "same_pattern": False,
        "why": "Same filing-status gate as the spouse age box.",
    },
    "form1040-line12d-spouse-blind-not-checked": {
        "same_pattern": False,
        "why": "Same filing-status gate as the spouse age box.",
    },
    "form1040-line2a": {
        "same_pattern": False,
        "why": "The box 8 subtotal set has a constantly true condition, so the guard reads it whenever the line is attempted.",
    },
    "capital-loss-carryover.short-term": {
        "same_pattern": False,
        "why": "The prior-return set has a constantly true condition. An open carryover answer blocks; it does not make the guard false.",
    },
    "capital-loss-carryover.long-term": {
        "same_pattern": False,
        "why": "Same constantly true set as the short-term carryover.",
    },
    "schedule-d-required.conclusion": {
        "same_pattern": False,
        "why": "The Exception 1 set has a constantly true condition, so an open Exception 1 answer blocks the conclusion instead of publishing it.",
    },
    "form1040-line12e": {
        "same_pattern": False,
        "why": "The Schedule A total is read whenever the guard is attempted. The guard itself cannot be a silent false.",
    },
    "dtb-child.tie-breaker-clear": {
        "same_pattern": False,
        "why": "Its sets do not give the guard a false result. An open tie-breaker answer blocks.",
    },
    "schedule-a-line16": {
        "same_pattern": False,
        "why": "The gambling-loss set does not give the guard a false result.",
    },
    "form1040-line12d-you-age": {
        "same_pattern": False,
        "why": "The age answer is under a constantly true set.",
    },
    "form1040-line12d-you-age-not-checked": {
        "same_pattern": False,
        "why": "The age answer is under a constantly true set.",
    },
    "form1040-line12d-you-blind": {
        "same_pattern": False,
        "why": "The blindness answer is under a constantly true set.",
    },
    "form1040-line12d-you-blind-not-checked": {
        "same_pattern": False,
        "why": "The blindness answer is under a constantly true set.",
    },
}


def scrub(text: str) -> str:
    text = text.replace(str(REPO), ".")
    return re.sub(r"/(?:Users|private|tmp|var|opt)/\S+", "<path>", text)


def short(name: Any) -> str:
    return str(name).removeprefix(P + "rule.").removeprefix(P)


def core_v90() -> Any:
    evidence_loader.activate(OWNER)
    common = evidence_loader.load(BNQ / "common.py", "common")
    return common.harness().Core("v90", "v88", "v88")


def _questions(sentences: list[str]) -> list[str]:
    return [sentence for sentence in sentences if "?" in sentence]


def _inapplicable_along(row: dict[str, Any], by_symbol: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Inapplicable producers reached by walking this blocked row's missing names.

    A name with no disposition row is a fact. The projection can turn that fact
    into a question. An inapplicable producer is not a question and not a
    blocked row, so the walk stops there.
    """
    found: dict[str, dict[str, Any]] = {}
    seen: set[str] = set()

    def walk(current: dict[str, Any]) -> None:
        for item in current.get("missing") or []:
            key = str(item)
            if key in seen:
                continue
            seen.add(key)
            rows = by_symbol.get(key, [])
            for producer in rows:
                if producer.get("disposition") != "inapplicable":
                    continue
                found[key] = {
                    "symbol": short(key),
                    "artifact": short(producer.get("artifact_id")),
                    "guard_result": producer.get("guard_result"),
                }
            for child in rows:
                if child.get("disposition") == "blocked":
                    walk(child)

    walk(row)
    return [found[key] for key in sorted(found)]


def summarize(core: Any, outcome: Any) -> dict[str, Any]:
    common = evidence_loader.load(BNQ / "common.py", "common")
    if outcome.refusal is not None:
        return {"outcome": "refused", "reason": outcome.refusal.reason,
                "detail": scrub(str(outcome.refusal.detail))[:300]}
    publishes = common.rule_publishes(core)
    report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
    model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    rows = report.get("dispositions") or []
    by_symbol: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        symbol = row.get("symbol") or publishes.get(str(row.get("artifact_id")))
        if symbol:
            by_symbol.setdefault(str(symbol), []).append(row)
    fields: list[dict[str, Any]] = []
    shown: dict[str, str] = {}
    page_questions: set[str] = set()
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        resolved = section.get("resolved") or {}
        disposition = str(resolved.get("disposition"))
        field_id = short(field.get("id"))
        if "blocked" not in disposition:
            value = resolved.get("value")
            shown[field_id] = disposition if value is None else str(value)
            continue
        sentences = [scrub(str(reason.get("sentence") or "").strip())
                     for reason in resolved.get("reasons") or []
                     if isinstance(reason, dict) and str(reason.get("sentence") or "").strip()]
        asked = _questions(sentences)
        page_questions.update(asked)
        symbol = str(field.get("binds_symbol") or "")
        own = [row for row in by_symbol.get(symbol, []) if row.get("disposition") == "blocked"]
        row = own[0] if own else {}
        stops = _inapplicable_along(row, by_symbol) if row else []
        fields.append({
            "field": field_id,
            "artifact": short(row.get("artifact_id")),
            "code": row.get("code"),
            "missing": [short(item) for item in row.get("missing") or []],
            "questions": asked,
            "inapplicable": [item["symbol"] for item in stops],
        })
        shown[field_id] = "blocked"
    interesting = {}
    for symbol in (P + PREFERENTIAL, P + CONCLUSION):
        found = by_symbol.get(symbol) or []
        if not found:
            interesting[short(symbol)] = None
            continue
        row = found[0]
        interesting[short(symbol)] = {
            "artifact": short(row.get("artifact_id")),
            "disposition": row.get("disposition"),
            "code": row.get("code"),
            "guard_result": row.get("guard_result"),
            "missing": [short(item) for item in row.get("missing") or []],
        }
    reasonless = [field["field"] for field in fields if not field["questions"]]
    return {
        "outcome": "success",
        "page_questions": sorted(page_questions),
        "lines": shown,
        "blocked_fields": fields,
        "reasonless_fields": reasonless,
        "producers": interesting,
    }


def _core_from(harness: Any, core_json: str | None) -> Any:
    if not core_json:
        return harness.Core("v90", "v88", "v88")
    body = json.loads(Path(core_json).read_text(encoding="utf-8"))
    return harness.Core(
        body["version"], body["registry"], body["release_version"],
        content=Path(body["content"]), releases=Path(body["releases"]),
        loader_from=body.get("loader_from"),
    )


def run_case(case_id: str, acts: list[dict[str, Any]], core_json: str | None = None) -> dict[str, Any]:
    evidence_loader.activate(OWNER)
    common = evidence_loader.load(BNQ / "common.py", "common")
    harness = common.harness()
    core = _core_from(harness, core_json)
    surface = core.surface()
    run_id = "demo.pbr.p0." + case_id.replace("_", "-")
    try:
        with harness.loader_entries(core):
            finished = harness._handover(
                harness._finish(
                    json.loads(json.dumps(acts)),
                    package_path=core.package_path,
                    package_version=core.version,
                    release_path=core.release_path,
                    release_version=core.release_version,
                    note=run_id,
                ),
                surface=surface,
                reconfirm=True,
            )
            with tempfile.TemporaryDirectory() as tmp:
                outcome = harness.live_coordinate_run(
                    harness.WorkspaceCapability(Path(tmp) / "L"),
                    repo_root=REPO,
                    authoritative_acts=finished,
                    workspace_revision=len(finished),
                    run_scope={"jurisdiction": "us", "year": harness.YEAR},
                    scope_user=harness.ccr.USER,
                    request={"schema": "run-request.v1"},
                    run_id=run_id,
                    governance_pins=[],
                    surface=surface,
                    output_name="out.json",
                )
                return {"id": case_id, **summarize(core, outcome)}
    except Exception as exc:  # noqa: BLE001 - a rejected list is a result
        return {"id": case_id, "outcome": "error", "error": type(exc).__name__,
                "message": scrub(str(exc))[:400]}


def _worker(payload: tuple[str | None, list[tuple[str, list[dict[str, Any]]]]]) -> list[dict[str, Any]]:
    core_json, shard = payload
    evidence_loader.activate(OWNER)
    try:
        return [run_case(case_id, acts, core_json) for case_id, acts in shard]
    finally:
        evidence_loader.finish(OWNER)


def _state_age(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    evidence_loader.activate(OWNER)
    age = evidence_loader.load(AGE / "rerun.py", "pbr_age")
    common = evidence_loader.load(BNQ / "common.py", "common")
    prepared = age.answered(acts, age.implied(acts))
    box4 = P + "f1099b.no-sale-box4-present"
    if not age.recorded(prepared, box4):
        prepared = common.harness().say(prepared, box4, "no", "pbr-box4")
    return prepared


def build_lists() -> list[tuple[str, list[dict[str, Any]]]]:
    evidence_loader.activate(OWNER)
    import tests.test_sale_family_audit_v82 as sfa

    common = evidence_loader.load(BNQ / "common.py", "common")
    probe = evidence_loader.load(BNQ / "probe.py", "probe")
    sfa_track = sfa.track0()
    core82 = sfa.v82(sfa_track)
    lists: list[tuple[str, list[dict[str, Any]]]] = []
    for name in RECORDED:
        acts = sfa.track0_acts(sfa_track, name, "honest", core82)
        lists.append(("recorded/" + name, _state_age(acts)))
    for case_id, (group, build, _note) in probe.CASES.items():
        lists.append((group + "/" + case_id, _state_age(build())))
    lists.append(("blank/opened", _state_age(common.harness().opened())))
    return lists


def _compare_bnq(recorded: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for name in RECORDED:
        row = recorded["recorded/" + name]
        got = row.get("reasonless_fields") or []
        out[name] = {
            "reasonless_fields": got,
            "matches_bnq_r7": got == BNQ_R7_FIELDS or set(got) == set(BNQ_R7_FIELDS),
            "added": sorted(set(got) - set(BNQ_R7_FIELDS)),
            "absent": sorted(set(BNQ_R7_FIELDS) - set(got)),
            "page_questions": row.get("page_questions"),
            "producer": (row.get("producers") or {}).get(PREFERENTIAL),
        }
    return out


def write(name: str, payload: Any) -> None:
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"{name} contains a local path")
    (HERE / name).write_text(text, encoding="utf-8")


def main() -> None:
    lists = build_lists()
    evidence_loader.finish(OWNER)
    workers = max(1, (os.cpu_count() or 2) - 1)
    shards = [(None, lists[index::workers]) for index in range(workers) if lists[index::workers]]
    found: list[dict[str, Any]] = []
    context = multiprocessing.get_context("spawn")
    with context.Pool(workers) as pool:
        for part in pool.map(_worker, shards):
            found.extend(part)
    by_id = {row["id"]: row for row in found}
    stops: dict[str, list[str]] = {}
    for row in found:
        if row.get("outcome") != "success":
            continue
        for field in row.get("blocked_fields") or []:
            if field.get("questions"):
                continue
            names = field.get("inapplicable") or ["none"]
            for stop in names:
                stops.setdefault(str(stop), []).append(row["id"] + ":" + field["field"])
    payload = {
        "core": "v90",
        "runs": len(found),
        "errors": [row for row in found if row.get("outcome") != "success"],
        "bnq_r7": _compare_bnq(by_id),
        "cases": {row["id"]: row for row in sorted(found, key=lambda item: item["id"])},
        "reasonless_stops": {key: sorted(value) for key, value in sorted(stops.items())},
        "guard_shapes": GUARD_SHAPES,
    }
    write("probe-output.json", payload)
    print(json.dumps({
        "runs": len(found),
        "errors": len(payload["errors"]),
        "stops": {key: len(value) for key, value in payload["reasonless_stops"].items()},
        "bnq_match": {name: row["matches_bnq_r7"] for name, row in payload["bnq_r7"].items()},
    }, indent=2))


if __name__ == "__main__":
    main()
