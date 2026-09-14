"""P3 R7 feasibility probe: eligible-student (C) on current machinery.

Executed, not read. Uses the real evaluator and evaluate_pairing_scoped_rule.
Presentation uses build_presentation_model over synthetic publications and
dispositions — not live_coordinate_run, not a durable presentation file,
not citation-walk.v1.html. No packages/ content is written. Synthetic
demo.* identities only.
"""

from __future__ import annotations

import json
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT))

from packages.derivation.evaluator import (  # noqa: E402
    BLOCK_ABSENT,
    BLOCK_INVALID,
    BLOCK_LOOKUP_MISS,
    AccessLog,
    Environment,
    EvalBlocked,
    evaluate,
)
from packages.derivation.loader import DerivationSchemas  # noqa: E402
from packages.derivation.pairing_dispatch import (  # noqa: E402
    PairingPublish,
    evaluate_pairing_scoped_rule,
)
from packages.derivation.presentation_projection import (  # noqa: E402
    build_presentation_model,
)
from packages.derivation.runner import Publication, SourceFact  # noqa: E402
from packages.kernel.findings import FindingState  # noqa: E402

SEP = "=" * 78

ELIGIBILITY_TYPE = "demo.sli.institution-eligibility"
COURSE_LOAD = "demo.sli.course-load"
BOX1 = "demo.sli.box1"
STANDARD_ID = "demo.sli.half-time-standard-id"
HALF_TIME_PARAM = "demo.sli.parameter.half-time-threshold"

# Partial mechanics witness — not the full eligible-student (C) tree.
# Reads institution eligibility (categorical ref) and the keyed numeric
# half-time threshold. Does not read program classification. Do not treat
# a successful evaluate() as proof that all three (C) determinations ran.
VALUE_EXPR: dict[str, Any] = {
    "op": "choose",
    "when": {
        "op": "categorical_compare",
        "cmp": "eq",
        "left": {"op": "ref", "name": ELIGIBILITY_TYPE},
        "right": {
            "op": "category_literal",
            "fact_type": ELIGIBILITY_TYPE,
            "value": "not-eligible",
        },
    },
    "then": 0,
    "else": {
        "op": "choose",
        "when": {
            "op": "compare",
            "cmp": "lt",
            "left": {"op": "ref", "name": COURSE_LOAD},
            "right": {
                "op": "parameter",
                "parameter_id": HALF_TIME_PARAM,
                "key": {"op": "ref", "name": STANDARD_ID},
            },
        },
        "then": 0,
        "else": {"op": "ref", "name": BOX1},
    },
}

PARAMETERS = {
    HALF_TIME_PARAM: {
        "id": HALF_TIME_PARAM,
        "values": {
            "demo.standard.riverside.ba-biology.fall-2024": "6",
            "demo.standard.riverside.ba-biology.spring-2024": "6",
        },
    }
}

DOMAINS = {ELIGIBILITY_TYPE: ["eligible", "not-eligible"]}

FIELD = {
    "schema": "form-field.v3",
    "id": "demo.sli.field.line-21",
    "version": "v1",
    "form": {
        "authority": "IRS",
        "form_id": "1040-SCH-1",
        "tax_year": 2025,
        "jurisdiction": "US-federal",
    },
    "line": "sch1-21",
    "label": "Student loan interest deduction",
    "description": "Probe field.",
    "binds_symbol": "demo.sli.eligible-student-supported-interest",
    "citation": {"id": "demo.sli.citation.line-21", "version": "v1"},
    "dispositions": {
        "published_value": {
            "render": "{value}",
            "explain": "Static published explain: eligible-student-supported interest as to (C) only.",
        },
        "computed_zero": {
            "render": "0",
            "explain": "Static computed-zero explain: does not name a statement or predicate.",
        },
        "closure_backed_zero": {"render": "0", "explain": "e"},
        "blocked": {
            "render": "",
            "explain": "Static blocked explain: a dependency is absent or composition is unknown.",
            "codes": ["DEPENDENCY_ABSENT", "LOOKUP_MISS"],
        },
        "guard_inapplicable": {"render": "", "explain": "e"},
    },
}
RULE = {
    "id": "demo.sli.rule.eligible-student",
    "schema": "rule-artifact.v2",
    "publishes": "demo.sli.eligible-student-supported-interest",
}


def line(msg: str = "") -> None:
    print(msg)


def header(title: str) -> None:
    line()
    line(SEP)
    line(title)
    line(SEP)


def _env(**overrides: object) -> Environment:
    kwargs: dict[str, object] = dict(
        symbols={},
        sources={},
        closed_sets=frozenset(),
        parameters=PARAMETERS,
        canon={},
        symbol_fact_types={ELIGIBILITY_TYPE: ELIGIBILITY_TYPE},
        categorical_domains=DOMAINS,
    )
    kwargs.update(overrides)
    return Environment(**kwargs)  # type: ignore[arg-type]


def _eval(env: Environment) -> tuple[Any, AccessLog]:
    access = AccessLog()
    return evaluate(VALUE_EXPR, env, access), access


def statement_local_evaluate(
    *,
    box1: str,
    course_load: str,
    eligibility: str,
    standard_id: str,
) -> tuple[Any, AccessLog]:
    """Hand-built local env for VALUE_EXPR. Not a committed coordinator."""
    env = _env(
        symbols={
            BOX1: box1,
            COURSE_LOAD: course_load,
            ELIGIBILITY_TYPE: eligibility,
            STANDARD_ID: standard_id,
        }
    )
    return _eval(env)


def probe_categorical_parameter_fails() -> dict[str, Any]:
    env = _env(
        symbols={"demo.institution.id": "demo.institution.riverside"},
        parameters={
            "demo.sli.parameter.eligibility": {
                "id": "demo.sli.parameter.eligibility",
                "values": {"demo.institution.riverside": "eligible"},
            }
        },
    )
    access = AccessLog()
    try:
        evaluate(
            {
                "op": "parameter",
                "parameter_id": "demo.sli.parameter.eligibility",
                "key": {"op": "ref", "name": "demo.institution.id"},
            },
            env,
            access,
        )
        raise AssertionError("categorical parameter should not evaluate")
    except EvalBlocked as exc:
        return {
            "category": exc.category,
            "missing": exc.missing,
            "expected": BLOCK_INVALID,
            "ok": exc.category == BLOCK_INVALID,
        }


def probe_pairing_binds_only_two() -> dict[str, Any]:
    left = SourceFact(
        name="demo.sli.box1-student-loan-interest",
        value="2000",
        finding_id="demo.finding.box1.a",
        fact_id="demo.fact.box1.a",
    )
    right = SourceFact(
        name="demo.sli.enrollment",
        value=json.dumps({"course_load": "12", "program_id": "demo.program.ba-biology"}),
        finding_id="demo.finding.enroll.a",
        fact_id="demo.fact.enroll.a",
    )
    extra = SourceFact(
        name=ELIGIBILITY_TYPE,
        value="eligible",
        finding_id="demo.finding.elig.a",
        fact_id="demo.fact.elig.a",
    )
    pairing = SourceFact(
        name="demo.sli.association",
        value=json.dumps(
            {
                "left_fact_id": "demo.fact.box1.a",
                "right_fact_id": "demo.fact.enroll.a",
                "institution_eligibility_fact_id": "demo.fact.elig.a",
            }
        ),
        finding_id="demo.finding.assoc.a",
        fact_id="demo.fact.assoc.a",
    )
    seen: dict[str, Any] = {}

    def evaluate_one(binding: Any) -> PairingPublish:
        seen["left_id"] = binding.left.finding_id
        seen["right_id"] = binding.right.finding_id
        seen["payload_keys"] = sorted(binding.pairing_value)
        seen["has_eligibility_attr"] = hasattr(binding, "institution_eligibility")
        return PairingPublish(value=binding.left_value)

    result = evaluate_pairing_scoped_rule(
        sources=[left, right, extra, pairing],
        pairing_type="demo.sli.association",
        left_type="demo.sli.box1-student-loan-interest",
        right_type="demo.sli.enrollment",
        rule_id="demo.sli.rule.eligible-student",
        rule_version="v1",
        symbol_for=lambda b: f"demo.sli.ess|{b.pairing_fact_id}",
        evaluate_one=evaluate_one,
        schemas=DerivationSchemas(),
    )
    pin_ids = {p["id"] for p in result.publications[0]["pins"]} if result.publications else set()
    return {
        "publications": len(result.publications),
        "left_bound": seen.get("left_id"),
        "right_bound": seen.get("right_id"),
        "payload_keys": seen.get("payload_keys"),
        "eligibility_on_binding": seen.get("has_eligibility_attr"),
        "eligibility_finding_pinned": "demo.finding.elig.a" in pin_ids,
        "ok": (
            seen.get("left_id") == "demo.finding.box1.a"
            and seen.get("right_id") == "demo.finding.enroll.a"
            and "demo.finding.elig.a" not in pin_ids
            and seen.get("has_eligibility_attr") is False
        ),
    }


def probe_two_statements_and_correction() -> dict[str, Any]:
    # A: eligible, load 12 >= threshold 6 → 2000
    val_a, access_a = statement_local_evaluate(
        box1="2000",
        course_load="12",
        eligibility="eligible",
        standard_id="demo.standard.riverside.ba-biology.fall-2024",
    )
    # B: eligible, load 3 < 6 → supported negative 0
    val_b, access_b = statement_local_evaluate(
        box1="1000",
        course_load="3",
        eligibility="eligible",
        standard_id="demo.standard.riverside.ba-biology.spring-2024",
    )
    a_amount = Decimal(str(val_a))
    b_amount = Decimal(str(val_b))
    # B missing eligibility → DEPENDENCY_ABSENT
    missing_ok = False
    missing_category = None
    try:
        env_miss = _env(
            symbols={
                BOX1: "1000",
                COURSE_LOAD: "3",
                STANDARD_ID: "demo.standard.riverside.ba-biology.spring-2024",
            }
        )
        _eval(env_miss)
    except EvalBlocked as exc:
        missing_ok = exc.category == BLOCK_ABSENT and ELIGIBILITY_TYPE in exc.missing
        missing_category = exc.category
    # Catalog miss on half-time key
    lookup_ok = False
    try:
        statement_local_evaluate(
            box1="1000",
            course_load="3",
            eligibility="eligible",
            standard_id="demo.standard.unknown",
        )
    except EvalBlocked as exc:
        lookup_ok = exc.category == BLOCK_LOOKUP_MISS
    # Correction: A's load 12 → 3, same identities, re-evaluate
    val_a_corrected, _ = statement_local_evaluate(
        box1="2000",
        course_load="3",
        eligibility="eligible",
        standard_id="demo.standard.riverside.ba-biology.fall-2024",
    )
    a_refs = set(access_a.refs)
    b_refs = set(access_b.refs)
    # AccessLog records symbol names in a hand-built env. That is not
    # finding-level pin isolation. Pin isolation is not-proven.
    return {
        "a_value": str(a_amount),
        "b_value": str(b_amount),
        "a_supported_favorable": a_amount == Decimal("2000"),
        "b_supported_negative": b_amount == Decimal("0"),
        "missing_support_blocks": missing_ok,
        "missing_category": missing_category,
        "lookup_miss_blocks": lookup_ok,
        "a_corrected_to_negative": Decimal(str(val_a_corrected)) == Decimal("0"),
        "a_refs": sorted(a_refs),
        "b_refs": sorted(b_refs),
        "b_did_not_read_box1": BOX1 not in b_refs,
        "pin_isolation": "not-proven",
        "value_expr_disposition": "narrowed",
        "ok": (
            a_amount == Decimal("2000")
            and b_amount == Decimal("0")
            and missing_ok
            and lookup_ok
            and Decimal(str(val_a_corrected)) == Decimal("0")
        ),
    }


def probe_missing_association_coverage() -> dict[str, Any]:
    """Two current box-1 SourceFacts; one pairing for A only.

    Calls evaluate_pairing_scoped_rule. Completeness over box-1 members is
    computed by hand and labeled conceptual: no committed coordinator
    performs it.
    """
    box1_a = SourceFact(
        name="demo.sli.box1-student-loan-interest",
        value="2000",
        finding_id="demo.finding.box1.a",
        fact_id="demo.fact.box1.a",
    )
    box1_b = SourceFact(
        name="demo.sli.box1-student-loan-interest",
        value="1000",
        finding_id="demo.finding.box1.b",
        fact_id="demo.fact.box1.b",
    )
    enroll_a = SourceFact(
        name="demo.sli.enrollment",
        value=json.dumps({"course_load": "12"}),
        finding_id="demo.finding.enroll.a",
        fact_id="demo.fact.enroll.a",
    )
    pairing_a = SourceFact(
        name="demo.sli.association",
        value=json.dumps(
            {
                "left_fact_id": "demo.fact.box1.a",
                "right_fact_id": "demo.fact.enroll.a",
            }
        ),
        finding_id="demo.finding.assoc.a",
        fact_id="demo.fact.assoc.a",
    )
    result = evaluate_pairing_scoped_rule(
        sources=[box1_a, box1_b, enroll_a, pairing_a],
        pairing_type="demo.sli.association",
        left_type="demo.sli.box1-student-loan-interest",
        right_type="demo.sli.enrollment",
        rule_id="demo.sli.rule.eligible-student",
        rule_version="v1",
        symbol_for=lambda b: f"demo.sli.ess|{b.pairing_fact_id}",
        evaluate_one=lambda b: PairingPublish(value=b.left_value),
        schemas=DerivationSchemas(),
    )
    pub_values = [str(p["value"]) for p in result.publications]
    pub_pin_ids: set[str] = set()
    for pub in result.publications:
        for pin in pub.get("pins") or []:
            if isinstance(pin, dict) and isinstance(pin.get("id"), str):
                pub_pin_ids.add(pin["id"])
    dispatcher_emits_only_a = (
        len(result.publications) == 1
        and len(result.blocked) == 0
        and pub_values == ["2000"]
        and "demo.finding.box1.a" in pub_pin_ids
        and "demo.finding.box1.b" not in pub_pin_ids
    )

    # Conceptual only — no committed coordinator performs this check.
    box1_ids = {"demo.fact.box1.a", "demo.fact.box1.b"}
    associated_left_ids = {"demo.fact.box1.a"}
    conceptual_missing = sorted(box1_ids - associated_left_ids)
    conceptual_complete = not conceptual_missing
    return {
        "dispatcher": "evaluate_pairing_scoped_rule",
        "dispatcher_publication_count": len(result.publications),
        "dispatcher_blocked_count": len(result.blocked),
        "dispatcher_values": pub_values,
        "dispatcher_pin_ids": sorted(pub_pin_ids),
        "dispatcher_emits_only_a_cannot_account_for_b": dispatcher_emits_only_a,
        "conceptual_box1_completeness": {
            "label": "conceptual: no committed coordinator performs this; the probe computes it by hand",
            "every_current_box1_has_exactly_one_association": conceptual_complete,
            "box1_members_without_association": conceptual_missing,
            "would_block_aggregate": not conceptual_complete,
        },
        "ok": dispatcher_emits_only_a and conceptual_missing == ["demo.fact.box1.b"],
    }


def probe_catalog_is_not_a_production_catalog() -> dict[str, Any]:
    """Synthetic categorical findings test evaluation only.

    fact-type.v2 declares vocabulary. It does not admit a current
    institution-eligibility or program-classification finding. This probe
    injects those values into Environment.symbols. Production still has no
    authoritative producer or adopted categorical catalog.
    """
    return {
        "probe_injects_eligibility_as_symbol": True,
        "fact_type_v2_supplies_current_finding": False,
        "production_producer_exists": False,
        "adopted_categorical_parameter_exists": False,
        "remaining_choice": (
            "authoritative institutional determinations become current "
            "findings through a defined evidence/producer path, or the rule "
            "grammar gains an adopted categorical catalog/parameter mechanism"
        ),
        "ok": True,
    }


def probe_presentation() -> dict[str, Any]:
    """Presentation projection over synthetic publications and dispositions.

    Pins on derived findings are authored by the probe, not assembled from
    AccessLog. Citation isolation here is not finding-level pin isolation.
    """
    raw_a = {
        "schema": "finding.v1",
        "id": "demo.finding.box1.a",
        "fact_id": "demo.fact.box1.a",
        "value": 2000,
        "basis": "attested",
        "evidence_ids": [],
    }
    raw_b = {
        "schema": "finding.v1",
        "id": "demo.finding.box1.b",
        "fact_id": "demo.fact.box1.b",
        "value": 1000,
        "basis": "attested",
        "evidence_ids": [],
    }
    state = FindingState(findings={"demo.finding.box1.a": raw_a, "demo.finding.box1.b": raw_b})
    published = {
        "schema": "derived-finding.v2",
        "id": "demo.derived.ess.a",
        "symbol": "demo.sli.eligible-student-supported-interest",
        "value": "2000",
        "version": "v2",
        "pins": [{"role": "input", "id": "demo.finding.box1.a", "version": "v1"}],
    }
    pub_row = {
        "artifact_id": "demo.sli.rule.eligible-student",
        "disposition": "published",
        "finding_id": "demo.derived.ess.a",
        "symbol": "demo.sli.eligible-student-supported-interest",
        "pins": published["pins"],
    }
    pub_model = build_presentation_model(
        run_id="demo.sli.probe.pub",
        resolved_members=[FIELD, RULE],
        state=state,
        publications=[Publication(act={}, finding=published)],
        dispositions=[pub_row],
    )
    blocked_row = {
        "artifact_id": "demo.sli.rule.eligible-student",
        "disposition": "blocked",
        "code": "DEPENDENCY_ABSENT",
        "missing": [ELIGIBILITY_TYPE],
        "pins": [],
    }
    blocked_model = build_presentation_model(
        run_id="demo.sli.probe.block",
        resolved_members=[FIELD, RULE],
        state=state,
        publications=[],
        dispositions=[blocked_row],
    )
    unknown_code_row = {
        "artifact_id": "demo.sli.rule.eligible-student",
        "disposition": "blocked",
        "code": "SLI_COMPOSITION_UNKNOWN",
        "missing": [],
        "pins": [],
    }
    unknown_model = build_presentation_model(
        run_id="demo.sli.probe.unknown",
        resolved_members=[FIELD, RULE],
        state=state,
        publications=[],
        dispositions=[unknown_code_row],
    )
    pub_section = pub_model["sections"][0]
    block_section = blocked_model["sections"][0]
    unknown_section = unknown_model["sections"][0]
    pub_explain = FIELD["dispositions"]["published_value"]["explain"]
    block_explain = FIELD["dispositions"]["blocked"]["explain"]
    return {
        "published_disposition": pub_section["resolved"]["disposition"],
        "published_value": pub_section["resolved"]["value"],
        "published_citation_pins": [s["pinId"] for s in pub_section["citationSites"]],
        "published_cites_b": "demo.finding.box1.b" in [s["pinId"] for s in pub_section["citationSites"]],
        "blocked_disposition": block_section["resolved"]["disposition"],
        "blocked_codes": block_section["resolved"].get("activeCodes"),
        "unknown_code_active": unknown_section["resolved"].get("activeCodes"),
        "published_explain_static": pub_explain,
        "blocked_explain_static": block_explain,
        "explain_names_statement_or_predicate": False,
        "evidence_level": "presentation projection over synthetic publications and dispositions",
        "pin_isolation": "not-proven",
        "projector_keeps_unknown_code": (
            unknown_section["resolved"].get("activeCodes") == ["SLI_COMPOSITION_UNKNOWN"]
        ),
        "ok": (
            pub_section["resolved"]["disposition"] == "published_value"
            and pub_section["resolved"]["value"] == 2000
            and pub_section["citationSites"][0]["pinId"] == "demo.finding.box1.a"
            and "demo.finding.box1.b" not in [s["pinId"] for s in pub_section["citationSites"]]
            and block_section["resolved"]["disposition"] == "blocked"
            and block_section["resolved"]["activeCodes"] == ["DEPENDENCY_ABSENT"]
            and unknown_section["resolved"].get("activeCodes") == ["SLI_COMPOSITION_UNKNOWN"]
        ),
    }


ATTACHMENT = {
    "schema": "attachment-rule.v4",
    "id": "demo.sli.attachment.schedule-1",
    "version": "v1",
    "title": "Schedule 1: Form 1098-E box 1 reported student loan interest",
    "publishes": "demo.sli.attachment.disposition",
    "attachment": {
        "authority": "IRS",
        "form_id": "1040-SCH-1",
        "jurisdiction": "US-federal",
        "tax_year": 2025,
    },
}


def probe_mixed_and_all_negative_presentation() -> dict[str, Any]:
    """Projection over synthetic publications/dispositions, including a
    manually supplied attachment inapplicable row. The committed attachment
    requirement (not-required when line 21 is 0) was established in P2, not
    re-executed here. Pins are authored by the probe: isolation not-proven.
    """
    raw_a = {
        "schema": "finding.v1",
        "id": "demo.finding.box1.a",
        "fact_id": "demo.fact.box1.a",
        "value": 2000,
        "basis": "attested",
        "evidence_ids": [],
    }
    raw_b = {
        "schema": "finding.v1",
        "id": "demo.finding.box1.b",
        "fact_id": "demo.fact.box1.b",
        "value": 1000,
        "basis": "attested",
        "evidence_ids": [],
    }
    state = FindingState(findings={"demo.finding.box1.a": raw_a, "demo.finding.box1.b": raw_b})

    mixed_finding = {
        "schema": "derived-finding.v2",
        "id": "demo.derived.ess.mixed",
        "symbol": "demo.sli.eligible-student-supported-interest",
        "value": "2000",
        "version": "v2",
        "pins": [{"role": "input", "id": "demo.finding.box1.a", "version": "v1"}],
    }
    mixed_row = {
        "artifact_id": "demo.sli.rule.eligible-student",
        "disposition": "published",
        "finding_id": "demo.derived.ess.mixed",
        "symbol": "demo.sli.eligible-student-supported-interest",
        "pins": mixed_finding["pins"],
    }
    mixed_model = build_presentation_model(
        run_id="demo.sli.probe.mixed",
        resolved_members=[FIELD, RULE],
        state=state,
        publications=[Publication(act={}, finding=mixed_finding)],
        dispositions=[mixed_row],
    )
    mixed_section = mixed_model["sections"][0]
    mixed_pins = [s["pinId"] for s in mixed_section["citationSites"]]

    zero_finding = {
        "schema": "derived-finding.v2",
        "id": "demo.derived.ess.zero",
        "symbol": "demo.sli.eligible-student-supported-interest",
        "value": "0",
        "version": "v2",
        "pins": [
            {"role": "input", "id": "demo.finding.box1.a", "version": "v1"},
            {"role": "input", "id": "demo.finding.box1.b", "version": "v1"},
        ],
    }
    zero_row = {
        "artifact_id": "demo.sli.rule.eligible-student",
        "disposition": "published",
        "finding_id": "demo.derived.ess.zero",
        "symbol": "demo.sli.eligible-student-supported-interest",
        "pins": zero_finding["pins"],
    }
    att_inapplicable = {
        "artifact_id": "demo.sli.attachment.schedule-1",
        "disposition": "inapplicable",
        "guard_result": False,
        "pins": [],
        "symbol": "demo.sli.attachment.disposition",
    }
    zero_model = build_presentation_model(
        run_id="demo.sli.probe.zero",
        resolved_members=[FIELD, RULE, ATTACHMENT],
        state=state,
        publications=[Publication(act={}, finding=zero_finding)],
        dispositions=[zero_row, att_inapplicable],
    )
    zero_section = zero_model["sections"][0]
    attachments = zero_model.get("attachments") or []
    citation_groups = zero_model.get("citationGroups") or []
    att_disp = attachments[0]["resolved"]["disposition"] if attachments else None
    return {
        "mixed_disposition": mixed_section["resolved"]["disposition"],
        "mixed_value": mixed_section["resolved"]["value"],
        "mixed_cites_a": "demo.finding.box1.a" in mixed_pins,
        "mixed_cites_b": "demo.finding.box1.b" in mixed_pins,
        "mixed_explain_names_b_negative": False,
        "all_negative_disposition": zero_section["resolved"]["disposition"],
        "all_negative_value": zero_section["resolved"]["value"],
        "attachment_disposition": att_disp,
        "attachment_inapplicable_is_manually_supplied_row": True,
        "attachment_requirement_behavior_established_in": "P2",
        "evidence_level": "presentation projection over synthetic publications and dispositions",
        "pin_isolation": "not-proven",
        "attachment_citation_groups": len(citation_groups),
        "ok": (
            mixed_section["resolved"]["disposition"] == "published_value"
            and mixed_section["resolved"]["value"] == 2000
            and mixed_pins == ["demo.finding.box1.a"]
            and zero_section["resolved"]["disposition"] == "computed_zero"
            and zero_section["resolved"]["value"] == 0
            and att_disp == "guard_inapplicable"
            and citation_groups == []
        ),
    }


def main() -> int:
    results: dict[str, Any] = {}
    header("1. Categorical parameter (defect 1)")
    results["categorical_parameter"] = probe_categorical_parameter_fails()
    line(json.dumps(results["categorical_parameter"], indent=2))

    header("2. Pairing primitive binds left and right only (defect 2)")
    results["pairing_two_facts"] = probe_pairing_binds_only_two()
    line(json.dumps(results["pairing_two_facts"], indent=2))

    header("3. Partial VALUE_EXPR in a hand-built local env")
    results["two_statements"] = probe_two_statements_and_correction()
    line(json.dumps(results["two_statements"], indent=2))

    header("4. Presentation projection over synthetic publications (defect 4)")
    results["presentation"] = probe_presentation()
    line(json.dumps(results["presentation"], indent=2))

    header("5. Missing association via evaluate_pairing_scoped_rule")
    results["missing_association"] = probe_missing_association_coverage()
    line(json.dumps(results["missing_association"], indent=2))

    header("6. Injected categoricals are not a production catalog")
    results["catalog_gap"] = probe_catalog_is_not_a_production_catalog()
    line(json.dumps(results["catalog_gap"], indent=2))

    header("7. Mixed presentation and all-negative attachment-absent")
    results["mixed_and_zero"] = probe_mixed_and_all_negative_presentation()
    line(json.dumps(results["mixed_and_zero"], indent=2))

    header("Verdict")
    all_ok = all(results[k]["ok"] for k in results)
    line(f"assertions_hold={all_ok}")
    line(
        "outcome: needs-owner-decision — evaluate_pairing_scoped_rule emits "
        "only A when B has no pairing; box-1 completeness is conceptual "
        "(hand-computed); VALUE_EXPR is a partial mechanics witness; pin "
        "isolation is not-proven; presentation is projection over synthetic "
        "rows. 2a and 2b not discharged."
    )
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
