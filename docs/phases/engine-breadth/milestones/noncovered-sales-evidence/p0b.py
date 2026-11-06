"""Scratch proof for the noncovered-sales closure contract. Not production.

One recorded answer admits the eight basis-not-reported families. Decisions
8 and 9, applied here and nowhere under packages/:

- A current "yes" stops admitting a family once a member-transition for that
  family is recorded after the answer. A later answer admits it again. A
  "no" beside any current member admits nothing for that family.
- A current covered sale whose basis was not reported blocks with
  BASIS_NOT_REPORTED_ON_COVERED in the row's missing list, and the page
  says to record the sale as a noncovered sale. The published derivation
  record enum has no slot for that token, so the row code stays
  DEPENDENCY_INVALID.

The package still carries eight source-closure-mapping.v3 citizens. They
all name one fact. The monkeypatch is the v4 admission rule.

    python3 docs/phases/engine-breadth/milestones/noncovered-sales-evidence/p0b.py
"""

from __future__ import annotations

import copy
import json
import shutil
import tempfile
import traceback
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]

import sys

sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

import probe  # noqa: E402
import prototype as proto  # noqa: E402
import track0  # noqa: E402
from packages.derivation import live as live_mod  # noqa: E402
from packages.derivation import marshal as marshal_mod  # noqa: E402
from packages.derivation import presentation_projection as presentation_mod  # noqa: E402
from packages.derivation import runner as runner_mod  # noqa: E402
from packages.derivation.source_authority import (  # noqa: E402
    ClosureAdmission,
    ClosureFindingRecord,
    validate_mapping_against_family,
)
from packages.kernel.facts import fact_id_for  # noqa: E402
from tests.helpers import current_core_returns as ccr  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _attested  # noqa: E402

P = proto.P
SHARED = P + "f1099b.noncovered-sold.source-closure"
QUESTION = "Did you sell any securities whose basis was not reported to the IRS?"
OUT = HERE / "track0b-output.json"
REFUSAL_CODE = "BASIS_NOT_REPORTED_ON_COVERED"
EXPLANATION = (
    "Record this sale as a noncovered sale. The broker did not report its basis to the IRS."
)
COVERED_OBJECTS = {
    P + "f1099b.covered-lt-txn": P + "f1099b.covered-lt",
    P + "f1099b.covered-st-txn": P + "f1099b.covered-st",
    P + "f1099b.covered-ltcg-txn": P + "f1099b.covered-ltcg",
    P + "f1099b.covered-w-lt-txn": P + "f1099b.covered-w-lt",
    P + "f1099b.covered-w-st-txn": P + "f1099b.covered-w-st",
}
ORIGINAL_MARSHAL = marshal_mod.marshal_closure_authority
ORIGINAL_RESOLVE = runner_mod.resolve_closure_admissions
ORIGINAL_LIVE = live_mod.live_coordinate_run
ORIGINAL_RECORD_BLOCKED = runner_mod._Run._record_blocked
ORIGINAL_QUESTIONS = presentation_mod._closure_question_reasons
ORIGINAL_DECL = __import__(
    "packages.tax.loader", fromlist=["domain_package_companion_declarations"]
).domain_package_companion_declarations

MEMBER_COUNTS: dict[str, int] = {}
FLAG_NO: set[str] = set()
STALE: set[str] = set()
GROUP_ACTIVE = False
CURRENT_ACTS: list[dict[str, Any]] = []


def _type_id(mapping: dict[str, Any]) -> str:
    fact_type = mapping["closure_fact_type"]
    if isinstance(fact_type, dict):
        return str(fact_type["id"])
    return str(fact_type)


def _declare_once() -> None:
    def with_v79() -> dict[tuple[str, str], dict[str, Any]]:
        declarations = dict(ORIGINAL_DECL())
        declarations[(P + "package.core-calculations", "v79")] = declarations[
            (P + "package.core-calculations", "v78")
        ]
        return declarations

    proto.loader.domain_package_companion_declarations = with_v79  # type: ignore[method-assign]


def _install_content_shape() -> None:
    original_mapping = proto._mapping
    original_boundary = proto._boundary_bundle

    def mapping(term: str, kind: str | None) -> dict[str, Any]:
        body = original_mapping(term, kind)
        body["closure_fact_type"] = {"id": SHARED, "version": "v1"}
        body["closure_question"] = QUESTION
        return body

    def boundary() -> dict[str, Any]:
        body = original_boundary()
        body["fact_types"].append(
            proto._fact(
                SHARED,
                QUESTION,
                {"enum": ["yes", "no"]},
                [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
            )
        )
        return body

    proto._mapping = mapping  # type: ignore[method-assign]
    proto._boundary_bundle = boundary  # type: ignore[method-assign]


def _scan(state: Any, currency: Any) -> None:
    MEMBER_COUNTS.clear()
    FLAG_NO.clear()
    grouped: dict[str, str] = {}
    for mapping in getattr(_scan, "group", []):
        grouped[mapping["family"]["id"]] = _member_type(mapping)
    counts = {family_id: 0 for family_id in grouped}
    for finding_id in currency.current_finding_ids:
        finding = state.findings.get(finding_id)
        if finding is None:
            continue
        fact_id = str(finding["fact_id"])
        fact_type = fact_id.split("|", 1)[0]
        for family_id, member_type in grouped.items():
            if fact_type == member_type:
                counts[family_id] += 1
        covered = COVERED_OBJECTS.get(fact_type)
        if covered is None:
            continue
        value = finding.get("value")
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except ValueError:
                value = None
        if isinstance(value, dict) and value.get("basis_reported_to_irs") == "no":
            FLAG_NO.add(covered)
    MEMBER_COUNTS.update(counts)


def _member_type(mapping: dict[str, Any]) -> str:
    member = mapping["member_fact_type"]
    if isinstance(member, dict):
        return str(member["id"])
    return str(member)


def _mark_stale(group: list[dict[str, Any]]) -> None:
    """A member-transition after the current answer is the horizon move.

    Today's per-family closure is keyed to the horizon current at the
    answer, so a later transition no longer matches. This fact is keyed
    by tax year only. The same cut is the act order: the current answer
    is the last assertion of the shared fact, and a transition for one
    listed family after that assertion drops that family only.
    """
    STALE.clear()
    families = {mapping["family"]["id"] for mapping in group}
    answer_at = None
    for index, act in enumerate(CURRENT_ACTS):
        if act.get("kind") != "assertion":
            continue
        finding = (act.get("payload") or {}).get("finding") or {}
        fact_id = str(finding.get("fact_id") or "")
        if fact_id.split("|", 1)[0] == SHARED:
            answer_at = index
    if answer_at is None:
        return
    for index, act in enumerate(CURRENT_ACTS):
        if index <= answer_at or act.get("kind") != "member-transition":
            continue
        family = ((act.get("payload") or {}).get("family") or {}).get("id")
        if family in families:
            STALE.add(str(family))


def _live(capability: Any, **kwargs: Any) -> Any:
    global CURRENT_ACTS
    CURRENT_ACTS = [dict(act) for act in kwargs.get("authoritative_acts") or ()]
    return ORIGINAL_LIVE(capability, **kwargs)


def _refusing_record_blocked(self: Any, rule: dict[str, Any], access: Any, code: str, missing: list[str]) -> None:
    if GROUP_ACTIVE and FLAG_NO:
        rewritten: list[str] = []
        hit = False
        for item in missing:
            if str(item) in FLAG_NO:
                hit = True
                if REFUSAL_CODE not in rewritten:
                    rewritten.append(REFUSAL_CODE)
            else:
                rewritten.append(str(item))
        if hit:
            code = "DEPENDENCY_INVALID"
            missing = rewritten
    ORIGINAL_RECORD_BLOCKED(self, rule, access, code, missing)


def _questions_with_explanation(row: dict[str, Any], *args: Any, **kwargs: Any) -> list[dict[str, Any]]:
    reasons = list(ORIGINAL_QUESTIONS(row, *args, **kwargs))
    by_symbol = kwargs.get("by_symbol") or {}
    seen: set[str] = set()

    def hit(current: dict[str, Any]) -> bool:
        missing = current.get("missing") or []
        if not isinstance(missing, list):
            return False
        for item in missing:
            key = str(item)
            if key == REFUSAL_CODE:
                return True
            if key in seen:
                continue
            seen.add(key)
            for child in by_symbol.get(key, []):
                if child.get("disposition") == "blocked" and hit(child):
                    return True
        return False

    if not hit(row):
        return reasons
    if any(str(reason.get("sentence")) == EXPLANATION for reason in reasons):
        return reasons
    return [{"sentence": EXPLANATION}] + reasons


def _patched_marshal(state: Any, currency: Any, mappings: list[dict[str, Any]]):
    global GROUP_ACTIVE
    group = [mapping for mapping in mappings if _type_id(mapping) == SHARED]
    rest = [mapping for mapping in mappings if _type_id(mapping) != SHARED]
    GROUP_ACTIVE = bool(group)
    if not group:
        MEMBER_COUNTS.clear()
        FLAG_NO.clear()
        return ORIGINAL_MARSHAL(state, currency, mappings)
    records, horizons = ORIGINAL_MARSHAL(state, currency, rest) if rest else ([], {})
    quiet = []
    for mapping in group:
        clone = copy.deepcopy(mapping)
        clone["closure_fact_type"] = {"id": SHARED + ".unused", "version": "v1"}
        quiet.append(clone)
    _unused, group_horizons = ORIGINAL_MARSHAL(state, currency, quiet)
    horizons.update(group_horizons)
    for finding_id in sorted(currency.current_finding_ids):
        finding = state.findings.get(finding_id)
        if finding is None or not marshal_mod._fact_id_has_type(finding["fact_id"], SHARED):
            continue
        records.append(
            ClosureFindingRecord(
                finding_id=finding_id,
                fact_type=SHARED,
                horizon_id="*",
                value=finding["value"],
            )
        )
    _scan.group = group  # type: ignore[attr-defined]
    _scan(state, currency)
    _mark_stale(group)
    return records, horizons


def _patched_resolve(
    mappings: list[dict[str, Any]],
    declarations: list[dict[str, Any]],
    closure_findings: list[ClosureFindingRecord],
    current_horizons: dict[str, str],
) -> dict[str, ClosureAdmission]:
    group = [mapping for mapping in mappings if _type_id(mapping) == SHARED]
    rest = [mapping for mapping in mappings if _type_id(mapping) != SHARED]
    admissions = ORIGINAL_RESOLVE(rest, declarations, closure_findings, current_horizons)
    if not group:
        return admissions
    for family_id in FLAG_NO:
        admissions.pop(family_id, None)
    by_id = {declaration["id"]: declaration for declaration in declarations}
    answers = [
        record
        for record in closure_findings
        if record.fact_type == SHARED and record.horizon_id == "*"
    ]
    if len(answers) != 1:
        return admissions
    answer = answers[0]
    for mapping in group:
        family_id = mapping["family"]["id"]
        declared = by_id.get(family_id)
        if declared is None:
            continue
        validate_mapping_against_family(mapping, declared)
        current = current_horizons.get(family_id)
        if current is None:
            continue
        members = MEMBER_COUNTS.get(family_id, 0)
        if answer.value == "no":
            admit = members == 0
        elif answer.value == "yes":
            admit = family_id not in STALE
        else:
            admit = False
        if not admit:
            continue
        admissions[family_id] = ClosureAdmission(
            family_id=family_id,
            mapping_id=mapping["id"],
            mapping_version=mapping["version"],
            declaration_id=declared["id"],
            declaration_version=declared["version"],
            horizon_id=current,
            closure_finding_id=answer.finding_id,
        )
    return admissions


def _schedule_d_attachment(content: Path, members: list[dict[str, Any]], entrypoints: list[dict[str, Any]]) -> None:
    """Do not publish Schedule D while line 1a or line 8a is blocked.

    v6 publishes from the proceeds subtotals alone. A blocked direct line
    left the attachment disposition published with a null page value.
    """
    source = json.loads((content / "attachment.schedule-d.v6.json").read_text(encoding="utf-8"))
    source["version"] = "v7"
    subtotals = list(source["requirement"]["subtotals"])
    for symbol in (P + "schedule-d.line-1a-gain", P + "schedule-d.line-8a-gain"):
        if symbol not in subtotals:
            subtotals.append(symbol)
    source["requirement"]["subtotals"] = subtotals
    (content / "attachment.schedule-d.v7.json").write_text(
        json.dumps(source, indent=2) + "\n", encoding="utf-8"
    )
    members.append({
        "op": "replace",
        "old": {
            "id": source["id"],
            "version": "v6",
            "schema": "attachment-rule.v8",
            "role": "attachment-rule",
        },
        "new": {
            "id": source["id"],
            "version": "v7",
            "schema": source["schema"],
            "role": "attachment-rule",
        },
    })
    entrypoints.append({
        "op": "replace",
        "old": {"id": source["id"], "version": "v6"},
        "new": {"id": source["id"], "version": "v7"},
    })


def _install_engine() -> None:
    marshal_mod.marshal_closure_authority = _patched_marshal
    runner_mod.resolve_closure_admissions = _patched_resolve
    runner_mod._Run._record_blocked = _refusing_record_blocked  # type: ignore[method-assign]
    presentation_mod._closure_question_reasons = _questions_with_explanation
    live_mod.live_coordinate_run = _live
    track0.live_coordinate_run = _live


def _assert_answer(acts: list[dict[str, Any]], value: str, tag: str) -> None:
    probe._add(
        acts,
        "assertion",
        {
            "finding": _attested(
                f"demo.ns.p0b.{tag}",
                fact_id_for(SHARED, (("tax-year", probe.YEAR),)),
                value,
            )
        },
    )


def _open(acts: list[dict[str, Any]], answer: str | None) -> None:
    for bundle in proto.BUILT["bundles"].values():
        proto._adopt(acts, bundle)
    for family_id in proto.BUILT["families"]:
        slug = family_id.removeprefix(P + "f1099b.")
        probe._add(
            acts,
            "horizon-genesis",
            {
                "family": {"id": family_id, "version": "v1"},
                "scope": {"tax-year": probe.YEAR, "subject": "demo.primary"},
                "horizon_id": f"demo.ns.p0b.{slug}.h0",
            },
        )
    if answer is not None:
        _assert_answer(acts, answer, answer)


def _with_answer(acts: list[dict[str, Any]], answer: str | None) -> list[dict[str, Any]]:
    out = copy.deepcopy(acts)
    _open(out, answer)
    return ccr._renumbered(out)


def _lt_sale(acts: list[dict[str, Any]], tag: str) -> None:
    value: dict[str, Any] = {
        "proceeds": 6000.0,
        "basis": 2000.0,
        "basis_reported_to_irs": "no",
        "long_term": "yes",
        "wash_disallowed": 0,
    }
    proto._record(acts, proto._family_id("lt", None), value, tag, close=False)
    proto._record(acts, proto._family_id("lt", "proceeds"), 6000.0, tag, close=False)
    proto._record(acts, proto._family_id("lt", "basis"), 2000.0, tag, close=False)


def _neighbors() -> dict[str, list[dict[str, Any]]]:
    base = ccr.base_return()
    built: dict[str, list[dict[str, Any]]] = {
        "wage": base,
        "foreign_tax": ccr.add_foreign_tax_1099div(base, [601.0]),
        "exempt_interest": ccr.add_tax_exempt_interest_1099int(base, [50.0]),
        "exempt_dividend": ccr.add_exempt_interest_dividends_1099div(base, [50.0]),
        "student_loan": ccr.add_student_loan_interest_1098e(base, [200.0]),
        "gambling_loss": ccr.add_gambling_losses(base, [500.0]),
        "mortgage": ccr.add_mortgage_itemizer(base, 4000.0),
        "itemized": ccr.add_itemized_assertion(base, 8000.0),
    }
    try:
        built["part_ii_b"] = ccr.part_ii_b_return(box4=200.0, box6=300.0)
    except Exception as exc:  # noqa: BLE001 — the harness builder is recorded, not hidden
        built["part_ii_b"] = []
        built["_part_ii_b_build_error"] = [{"error": type(exc).__name__, "message": probe.scrub(str(exc))[:500]}]
    return built


def _object_flag(family_id: str, value: dict[str, Any], tag: str, proceeds: float, basis: float) -> list[dict[str, Any]]:
    acts = probe.record(_with_answer(ccr.base_return(), "no"), family_id, value, tag)
    acts = probe.record(acts, family_id + "-proceeds", proceeds, tag + "p")
    return probe.record(acts, family_id + "-basis", basis, tag + "b")


def _covered_flag_cases() -> dict[str, list[dict[str, Any]]]:
    yes_txn = probe.txn(proceeds=6000.0, basis=2000.0, long_term="yes", reported="yes", covered="yes")
    no_txn = probe.txn(proceeds=6000.0, basis=2000.0, long_term="yes", reported="no", covered="yes")
    prepared = _with_answer(ccr.base_return(), "no")
    flagged = probe.direct(prepared, "lt", 6000.0, 2000.0, "mis")
    flagged_st = probe.direct(copy.deepcopy(prepared), "st", 2000.0, 8000.0, "misst")
    flagged_w_lt = probe.wash(copy.deepcopy(prepared), "lt", 4000.0, 7000.0, 1000.0, "wlt")
    flagged_w_st = probe.wash(copy.deepcopy(prepared), "st", 4000.0, 7000.0, 1000.0, "wst")
    corrected = probe.record(prepared, P + "f1099b.covered-lt", yes_txn, "corr")
    corrected = probe.record(corrected, P + "f1099b.covered-lt-proceeds", 6000.0, "corrp")
    corrected = probe.record(corrected, P + "f1099b.covered-lt-basis", 2000.0, "corrb")
    corrected_no = probe.correct(copy.deepcopy(corrected), P + "f1099b.covered-lt", no_txn, "corr")
    corrected_yes = probe.correct(copy.deepcopy(flagged), P + "f1099b.covered-lt", yes_txn, "miso")
    return {
        "covered_flag_no_path_a": flagged,
        "covered_flag_no_st": flagged_st,
        "covered_flag_no_w_lt": flagged_w_lt,
        "covered_flag_no_w_st": flagged_w_st,
        "covered_flag_yes": corrected,
        "covered_flag_corrected_to_no": corrected_no,
        "covered_flag_corrected_to_yes": corrected_yes,
    }


def _after_sale(answer_first: str, answer_last: str | None, tag: str) -> list[dict[str, Any]]:
    acts = copy.deepcopy(ccr.base_return())
    _open(acts, answer_first)
    _lt_sale(acts, tag)
    if answer_last is not None:
        _assert_answer(acts, answer_last, answer_last + "-" + tag)
    return proto._with_boundaries(acts, "yes")


def _class_sale(term: str, proceeds: float, basis: float, tag: str, adjustment: float | None = None) -> list[dict[str, Any]]:
    """Record the sale, then answer yes, so the answer is not stale."""
    acts = copy.deepcopy(ccr.base_return())
    _open(acts, None)
    proto._sale(acts, term, proceeds, basis, tag, adjustment=adjustment)
    _assert_answer(acts, "yes", "yes-" + tag)
    return proto._with_boundaries(acts, "yes")


def _cases() -> dict[str, list[dict[str, Any]]]:
    neighbors = _neighbors()
    build_error = neighbors.pop("_part_ii_b_build_error", None)
    cases: dict[str, list[dict[str, Any]]] = {
        "wage_unclosed": ccr._renumbered(ccr.base_return()),
        "one_finding": _with_answer(ccr.base_return(), "no"),
    }
    for name, acts in neighbors.items():
        if not acts:
            continue
        cases["one_" + name] = _with_answer(acts, "no")
    cases["late_member_unclosed"] = _after_sale("no", None, "late")
    cases["late_member_reopened"] = _after_sale("no", "yes", "re")
    cases["late_yes_stale"] = _after_sale("yes", None, "stale")
    cases["late_yes_reanswered"] = _after_sale("yes", "yes", "again")
    cases["yes_then_no_with_member"] = _after_sale("yes", "no", "flip")
    cases["st_loss"] = _class_sale("st", 2000.0, 8000.0, "stloss")
    cases["wash"] = _class_sale("lt", 4000.0, 7000.0, "wash", adjustment=1000.0)
    cases["lt_gain"] = _class_sale("lt", 6000.0, 2000.0, "ltgain")
    cases["code_w_on_gain"] = _class_sale("lt", 6000.0, 2000.0, "badw", adjustment=500.0)
    cases["boundary_no_without_member"] = proto._with_boundaries(_with_answer(ccr.base_return(), "no"), "no")
    bound_member = copy.deepcopy(ccr.base_return())
    _open(bound_member, "no")
    _lt_sale(bound_member, "bno")
    cases["boundary_no_with_member"] = proto._with_boundaries(bound_member, "no")
    both = probe.direct(_with_answer(ccr.base_return(), "no"), "lt", 6000.0, 2000.0, "cno")
    cases["covered_both_boundaries_no"] = probe.boundary(both, "no", "no")
    dup = copy.deepcopy(ccr.base_return())
    for bundle in proto.BUILT["bundles"].values():
        proto._adopt(dup, bundle)
    for family_id in proto.BUILT["families"]:
        probe._add(
            dup,
            "horizon-genesis",
            {
                "family": {"id": family_id, "version": "v1"},
                "scope": {"tax-year": probe.YEAR, "subject": "demo.primary"},
                "horizon_id": "demo.ns.p0b.shared.h0",
            },
        )
    cases["duplicate_horizon"] = ccr._renumbered(dup)
    cases.update(_covered_flag_cases())
    if build_error is not None:
        cases["_part_ii_b_build_error"] = build_error  # type: ignore[assignment]
    return cases


def _line(result: dict[str, Any], field_id: str) -> dict[str, Any] | None:
    lines = (result.get("lines") or {})
    row = lines.get(field_id)
    return row if isinstance(row, dict) else None


def _money(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "line15": _line(result, P + "form1040.line-15"),
        "line16": _line(result, P + "form1040.line-16"),
        "line1a": _line(result, P + "schedule-d.line-1a"),
        "line2": _line(result, P + "schedule-d.line-2"),
        "line8a": _line(result, P + "schedule-d.line-8a"),
        "line9": _line(result, P + "schedule-d.line-9"),
        "line21": _line(result, P + "schedule-d.line-21"),
        "line7a": _line(result, P + "form1040.line-7a"),
    }


def _save(payload: dict[str, Any]) -> None:
    text = probe.scrub(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUT.write_text(text, encoding="utf-8")


def _run(name: str, acts: list[dict[str, Any]], payload: dict[str, Any], bucket: str) -> dict[str, Any]:
    print("run", bucket, name, flush=True)
    raw = track0._execute(acts, f"demo.ns.p0b.{bucket}.{name}")
    digested = track0._digest(raw)
    digested["money"] = _money(digested)
    page = []
    for row in raw.get("lines") or []:
        field_id = str(row.get("id") or "")
        if not any(token in field_id for token in ("line-1a", "line-2", "line-8a", "line-9", "line-7a", "line-15")):
            continue
        if row.get("reasons") or row.get("disposition") == "blocked":
            page.append({
                "id": field_id,
                "disposition": row.get("disposition"),
                "value": row.get("value"),
                "reasons": row.get("reasons") or [],
            })
    if page:
        digested["page"] = page
    refusal_rows = [
        {"artifact_id": row.get("artifact_id"), "code": row.get("code"), "missing": row.get("missing")}
        for row in (raw.get("blocked") or [])
        if REFUSAL_CODE in (row.get("missing") or [])
    ]
    if refusal_rows:
        digested["refusal_rows"] = refusal_rows[:8]
    if isinstance(raw, dict) and raw.get("error") is None:
        missing = []
        for row in raw.get("blocked") or []:
            for item in row.get("missing") or []:
                if "noncovered" in str(item):
                    missing.append(str(item))
        if missing:
            digested["noncovered_blocked"] = sorted(set(missing))
    payload[bucket][name] = digested
    _save(payload)
    print(" ", name, digested.get("error") or digested.get("stop_reason"), digested.get("seconds"), flush=True)
    return digested


def main() -> None:
    proto.USE_V2 = True
    proto.EXTRAS = [_schedule_d_attachment]
    _install_content_shape()
    _install_engine()
    proto._declare_v79 = _declare_once  # type: ignore[method-assign]
    rules = HERE / "prototype-rules"
    backup = Path(tempfile.mkdtemp(prefix="p0b-rules-"))
    shutil.copytree(rules, backup / "rules")
    payload: dict[str, Any] = {
        "source_ref": "0a7fc60f5ab42ed8d568362f1a5c9a750d7394c0",
        "refusal_code": REFUSAL_CODE,
        "covered_ltcg_absent": (
            "tax.us.2025.f1099b.covered-ltcg is not a member of core v78 or this v79 "
            "successor. Line 8a v4 and v5 read tax.us.2025.f1099b.covered-lt. The "
            "gain-only family has no recorded horizon on the harness return."
        ),
        "shared_fact": SHARED,
        "question": QUESTION,
        "v79": {},
        "v78": {},
    }
    scratch_root = Path(tempfile.mkdtemp(prefix="p0b-")).resolve()
    try:
        try:
            report = proto.build(scratch_root / "s")
            payload["successor"] = {
                "package": (report.get("package") or {}).get("version"),
                "release": (report.get("release") or {}).get("version"),
                "members": report.get("members"),
            }
            _save(payload)
            v79 = track0._snapshot()
            cases = _cases()
            build_note = cases.pop("_part_ii_b_build_error", None)
            if build_note is not None:
                payload["part_ii_b_build_error"] = build_note
            for name, acts in cases.items():
                _run(name, acts, payload, "v79")
            track0._use_v78()
            neighbors = _neighbors()
            neighbors.pop("_part_ii_b_build_error", None)
            for name, acts in neighbors.items():
                if not acts:
                    continue
                _run(name, ccr._renumbered(acts), payload, "v78")
            before = probe.direct(ccr.base_return(), "lt", 6000.0, 2000.0, "v78flag")
            _run("covered_flag_no_path_a", before, payload, "v78")
            track0._restore(v79)
            payload["duplicate_horizon_is_kernel"] = (
                payload["v79"].get("duplicate_horizon", {}).get("error") == "HorizonModelError"
                or payload["v79"].get("duplicate_horizon", {}).get("horizon_refused") is True
            )
            _save(payload)
        except Exception:
            payload["crash"] = probe.scrub(traceback.format_exc())[-2000:]
            _save(payload)
            raise
    finally:
        if rules.exists():
            shutil.rmtree(rules)
        shutil.copytree(backup / "rules", rules)
        shutil.rmtree(backup, ignore_errors=True)
        shutil.rmtree(scratch_root, ignore_errors=True)


if __name__ == "__main__":
    main()
