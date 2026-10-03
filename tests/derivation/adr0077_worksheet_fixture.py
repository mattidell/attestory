"""The Track 1a-4 worksheet declaration as a real v13 rule in a v35 package.

ADR 0077 Parts 3 and 4. One ``rule-artifact.v13`` worksheet selects between
the old path (five per-statement answer statuses) and the new path (one
per-statement support conclusion), or refuses when both are present. Its
default holds the closed-empty branch.

The old path's value is the production Student Loan Interest Deduction
worksheet's nonempty branch (``rule.sli-worksheet.json``, ``value.else``)
with its five answer collects read through ``reads_subject_results``, as
Track 1a-4 item 1 states. The new path is that branch with the five
collects replaced by one collect of the statement conclusion. The phase-out
and limit arithmetic are the production bytes, unchanged.

One deliberate difference from the Track 1a-4 text. Its default blocked
through a probe-only ``missing_subjects`` field on ``block``.
``rule-artifact.v13`` has no such field: its ``block`` carries only a code.
The default here names the statements the way the grammar allows: it
declares ``reads_subject_results`` for one answer status and collects it.
With neither path present no statement has an answer, so every status
entry is a block and the declared read refuses ``DEPENDENCY_INVALID``
naming each box fact id, sorted. Closed-empty takes the ``then`` branch and
reads nothing.

Every case goes through ``validate_package``, ``_resolved_run_material``
and ``marshal_run_context`` over a kernel state with a real fact lattice.
No ``RunContext`` is built by hand.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from packages.derivation.live import _resolved_run_material
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.marshal import marshal_run_context
from packages.derivation.package_validation import (
    PackageValidation,
    package_instance_checksum,
    validate_package,
)
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import RunContext, RunResult, run
from packages.kernel.currency import CurrencyView
from packages.kernel.facts import KernelState

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"

SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}
ADOPTION_PIN = {"role": "adoption", "id": "demo.package.adr0077-worksheet", "version": "v1"}
GOVERNANCE_PINS = [{"role": "governance", "id": "demo.governance.adr0077-worksheet", "version": "v1"}]

FAMILY = "tax.us.2025.f1098e.1"
BOX1 = "tax.us.2025.f1098e.box1-student-loan-interest"
CLOSURE_TYPE = "tax.us.2025.f1098e.1.source-closure"
LINE1_SUBTOTAL = "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal"
LINE21 = "tax.us.2025.schedule1.line21-sli-deduction"
FILING_STATUS = "tax.us.2025.filing-status"
TOTAL_INCOME = "tax.us.2025.income.total-income"
ROUNDING = "rounding.convention"

INCL = "tax.us.2025.sli.statement-inclusion-relationship"
FIN = "tax.us.2025.sli.financing-relationship"
LOAN = "demo.tax.adr0077.loan-paid-only-school-costs"
ENROLL = "demo.tax.adr0077.enrolled-half-time-for-this-loan"

ANSWER_TAILS = (
    "no-related-person-interest",
    "no-qualified-employer-plan-interest",
    "no-non-qualified-loan-component",
    "no-employer-educational-assistance-interest",
    "no-qtp-earnings-used",
)
ANSWERS = tuple(f"tax.us.2025.f1098e.{tail}" for tail in ANSWER_TAILS)
STATUS = {answer: f"demo.tax.adr0077.status.{tail}" for answer, tail in zip(ANSWERS, ANSWER_TAILS)}
STATUS_RULE = {answer: f"demo.rule.adr0077.status.{tail}" for answer, tail in zip(ANSWERS, ANSWER_TAILS)}

SCOPE_FACTS = (
    "tax.us.2025.sli-scope.no-form-2555",
    "tax.us.2025.sli-scope.no-form-4563",
    "tax.us.2025.sli-scope.no-puerto-rico-or-samoa-income",
    *(
        f"tax.us.2025.schedule1-adjustments-scope.no-line{n}"
        for n in (
            "11-educator", "12-business-expenses", "13-hsa", "14-moving",
            "15-deductible-se", "16-se-retirement", "17-se-health", "18-penalty",
            "19-alimony-paid", "20-ira-deduction", "23-archer-msa", "25-other-adjustments",
        )
    ),
    "tax.us.2025.sli-scope.not-claimed-as-dependent",
    "tax.us.2025.sli-scope.legally-obligated-for-interest",
)

COUNT = "demo.tax.adr0077.financing-count"
SUPPORT = "demo.tax.adr0077.inclusion-support"
CONCLUSION = "demo.tax.adr0077.statement-conclusion"
COUNT_RULE = "demo.rule.adr0077.financing-count"
SUPPORT_RULE = "demo.rule.adr0077.inclusion-support"
STATEMENT_RULE = "demo.rule.adr0077.statement-conclusion"
WORKSHEET = "demo.rule.adr0077.worksheet"
COVERAGE_PARAM = "demo.param.adr0077.coverage-empty"

PLAIN = "plain-case-supported"
NOT = "not-supported"
BOTH_TOKEN = "old-and-new-sli-inputs-both-present"

BOX_KEYS = ("lender", "statement", "tax-year")
INCL_KEYS = ("lender", "statement", "tax-year", "borrowing")
FIN_KEYS = ("borrowing", "period", "institution", "programme")
LOAN_KEYS = ("borrowing",)
YEAR_KEYS = ("tax-year",)

FILING_STATUSES = [
    "single", "married_filing_jointly", "married_filing_separately",
    "head_of_household", "qualifying_surviving_spouse",
]

BASIS = {
    "said": [
        "The loan-cost answer is yes for the named borrowing.",
        "The enrollment answer is yes for the named borrowing.",
        "The person affirmed that the borrowing financed the schooling.",
        "The person affirmed that the statement includes interest on the borrowing.",
    ],
    "derived": ["The inclusion count is 1.", "The financing count is 1."],
    "assumed": ["Box 1 holds no loan the person did not record."],
    "left_with_person": ["The institution is an eligible educational institution."],
}


# ---------------------------------------------------------------------------
# Citizens
# ---------------------------------------------------------------------------


def _load(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((CONTENT / name).read_text("utf-8"))
    return loaded


def fact_type(fact_id: str, key_names: tuple[str, ...], values: list[str] | None = None,
              *, value_schema: dict[str, Any] | None = None) -> dict[str, Any]:
    schema: dict[str, Any]
    if value_schema is not None:
        schema = value_schema
    elif values is None:
        schema = {"type": "string", "minLength": 1}
    else:
        schema = {"type": "string", "enum": values}
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": "v1",
        "title": fact_id,
        "nature": "determinable",
        "identity_keys": [{"name": name, "kind": "literal", "values": ["placeholder"]} for name in key_names],
        "value_schema": schema,
        "supersession": {"policy": "free"},
    }


def rule(rule_id: str, *, publishes: str, value: Any, subject: str | None = None,
         joined: str | None = None, direction: str | None = None,
         requires: list[str] | None = None, when: Any = True) -> dict[str, Any]:
    citizen: dict[str, Any] = {
        "schema": "rule-artifact.v13",
        "id": rule_id,
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": list(requires or []),
        "pins": [],
        "when": when,
        "value": value,
        "publishes": publishes,
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
    }
    if subject is not None:
        citizen["subject"] = {"id": subject, "version": "v1"}
    if joined is not None:
        citizen["joined"] = {"id": joined, "version": "v1"}
    if direction is not None:
        citizen["direction"] = direction
    return citizen


def _eq(left: Any, right: Any) -> dict[str, Any]:
    return {"op": "compare", "cmp": "eq", "left": left, "right": right}


def _answer_yes(name: str) -> dict[str, Any]:
    return {
        "op": "categorical_compare",
        "cmp": "eq",
        "left": {"op": "ref", "name": name},
        "right": {"op": "category_literal", "fact_type": {"id": name, "version": "v1"}, "value": "yes"},
    }


def _all_equal(symbol: str, value: str) -> dict[str, Any]:
    return {
        "op": "collect_categorical_all_equal",
        "name": symbol,
        "value": {"op": "category_literal", "fact_type": {"id": symbol, "version": "v1"}, "value": value},
    }


def _read(symbol: str) -> dict[str, Any]:
    return {"symbol": symbol, "subject": {"id": BOX1, "version": "v1"}}


def _status_rule(answer: str) -> dict[str, Any]:
    """Track 1a-4's per-statement answer status: the answer, or a block."""
    value = {
        "op": "choose",
        "when": _eq({"op": "link_count", "links": answer}, 0),
        "then": {"op": "block", "code": "DEPENDENCY_INVALID"},
        "else": {"op": "ref", "name": answer},
    }
    return rule(STATUS_RULE[answer], publishes=STATUS[answer], value=value, subject=BOX1,
                joined=answer, direction="joined_contains_subject", requires=[answer])


def _support_value() -> dict[str, Any]:
    count = {"op": "shared_key_count", "fact_type": FIN, "key": "borrowing"}
    return {
        "op": "choose",
        "when": {"op": "all", "args": [_eq(count, 1), _answer_yes(LOAN), _answer_yes(ENROLL)]},
        "then": 1,
        "else": 0,
    }


def _statement_value() -> dict[str, Any]:
    coverage = {
        "op": "link_coverage",
        "links": INCL,
        "reductions": SUPPORT,
        "empty": {"parameter": {"id": COVERAGE_PARAM, "version": "v1"}},
    }
    return {
        "op": "choose",
        "when": {"op": "all", "args": [_eq({"op": "link_count", "links": INCL}, 1), _eq(coverage, 1)]},
        "then": PLAIN,
        "else": NOT,
    }


def _iter_refs(expr: Any) -> list[str]:
    found: list[str] = []
    if isinstance(expr, dict):
        if expr.get("op") == "ref" and isinstance(expr.get("name"), str):
            found.append(expr["name"])
        for item in expr.values():
            found.extend(_iter_refs(item))
    elif isinstance(expr, list):
        for item in expr:
            found.extend(_iter_refs(item))
    return found


def _old_path_value() -> Any:
    """The production nonempty branch, its five answer collects renamed."""
    production = _load("rule.sli-worksheet.json")

    def rename(node: Any) -> Any:
        if isinstance(node, list):
            return [rename(item) for item in node]
        if not isinstance(node, dict):
            return node
        renamed = {key: rename(item) for key, item in node.items()}
        if renamed.get("op") == "collect_categorical_all_equal" and renamed.get("name") in STATUS:
            renamed = _all_equal(STATUS[renamed["name"]], "yes")
        return renamed

    return rename(copy.deepcopy(production["value"]["else"]))


def _new_path_value(old: Any) -> Any:
    """The same branch with the five status collects replaced by one conclusion collect."""
    status_names = set(STATUS.values())

    def replace(node: Any) -> Any:
        if isinstance(node, list):
            return [replace(item) for item in node]
        if not isinstance(node, dict):
            return node
        replaced = {key: replace(item) for key, item in node.items()}
        args = replaced.get("args")
        if replaced.get("op") == "all" and isinstance(args, list):
            kept = [arg for arg in args if not (isinstance(arg, dict) and arg.get("name") in status_names)]
            if len(kept) != len(args):
                replaced["args"] = [*kept, _all_equal(CONCLUSION, PLAIN)]
        return replaced

    return replace(copy.deepcopy(old))


def _path_pins(requires: list[str]) -> list[dict[str, Any]]:
    pins: list[dict[str, Any]] = []
    for name in requires:
        if name == "filing_status":
            pins.append({"role": "choice", "id": name, "version": "v1"})
        else:
            pins.append({"role": "input", "id": name, "version": "v1", "origin": "assertion"})
    return pins


def worksheet() -> dict[str, Any]:
    old_value = _old_path_value()
    new_value = _new_path_value(old_value)
    old_requires = sorted(set(_iter_refs(old_value)))
    new_requires = sorted(set(_iter_refs(new_value)))
    box_count = {"op": "count", "name": BOX1, "source_set": FAMILY}
    first_status = STATUS[ANSWERS[0]]
    default_value = {
        "op": "choose",
        "when": _eq(box_count, 0),
        "then": 0,
        "else": {
            "op": "choose",
            "when": _all_equal(first_status, "yes"),
            "then": {"op": "block", "code": "DEPENDENCY_INVALID"},
            "else": {"op": "block", "code": "DEPENDENCY_INVALID"},
        },
    }
    return {
        "schema": "rule-artifact.v13",
        "id": WORKSHEET,
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "citations": [
            {"id": "tax.us.2025.citation.form1040.sli-worksheet", "version": "v1"},
            {"id": "tax.us.2025.citation.schedule1.line-21", "version": "v1"},
        ],
        "publishes": LINE21,
        "when": True,
        "requires": [],
        "pins": [],
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
        "selection": {
            "mode": "exclusive_presence",
            "conflict": "refuse",
            "paths": [
                {
                    "id": "old",
                    "activity": {
                        "kind": "source_nonempty",
                        "source_family": {"id": FAMILY, "version": "v1"},
                        "member_fact_types": [{"id": answer, "version": "v1"} for answer in ANSWERS],
                    },
                    "reads_subject_results": [_read(STATUS[answer]) for answer in ANSWERS],
                    "requires": old_requires,
                    "pins": _path_pins(old_requires),
                    "when": True,
                    "value": old_value,
                },
                {
                    "id": "new",
                    "activity": {
                        "kind": "source_nonempty",
                        "member_fact_types": [{"id": INCL, "version": "v1"}],
                    },
                    "reads_subject_results": [_read(CONCLUSION)],
                    "requires": new_requires,
                    "pins": _path_pins(new_requires),
                    "when": True,
                    "value": new_value,
                },
            ],
            "default": {
                "id": "neither",
                "reads_subject_results": [_read(first_status)],
                "requires": [],
                "pins": [],
                "when": True,
                "value": default_value,
            },
            "refusal": {"code": "DEPENDENCY_INVALID", "missing": [BOTH_TOKEN], "pins": []},
        },
    }


def parts(*, statement_rule: dict[str, Any] | None = None,
          worksheet_rule: dict[str, Any] | None = None) -> list[tuple[dict[str, Any], str]]:
    statement = statement_rule or rule(
        STATEMENT_RULE, subject=BOX1, joined=INCL, direction="joined_contains_subject",
        publishes=CONCLUSION, value=_statement_value(),
    )
    statement.setdefault("basis", copy.deepcopy(BASIS))
    yes_no = ["yes", "no"]
    citizens: list[tuple[dict[str, Any], str]] = [
        (fact_type(BOX1, BOX_KEYS), "fact-type"),
        (fact_type(CLOSURE_TYPE, ("family-horizon",), value_schema={"type": "boolean"}), "fact-type"),
        (fact_type(INCL, INCL_KEYS, ["sli.statement-inclusion.affirmed"]), "fact-type"),
        (fact_type(FIN, FIN_KEYS, ["sli.financing.affirmed", "sli.financing.cannot-tell"]), "fact-type"),
        (fact_type(LOAN, LOAN_KEYS, ["yes", "no", "cannot-tell"]), "fact-type"),
        (fact_type(ENROLL, LOAN_KEYS, ["yes", "no", "cannot-tell"]), "fact-type"),
        (fact_type(CONCLUSION, BOX_KEYS, [PLAIN, NOT]), "fact-type"),
        (fact_type(FILING_STATUS, YEAR_KEYS, FILING_STATUSES), "fact-type"),
        (fact_type(TOTAL_INCOME, YEAR_KEYS), "fact-type"),
    ]
    for answer in ANSWERS:
        citizens.append((fact_type(answer, BOX_KEYS, yes_no), "fact-type"))
        citizens.append((fact_type(STATUS[answer], BOX_KEYS, yes_no), "fact-type"))
    for scope_fact in SCOPE_FACTS:
        citizens.append((fact_type(scope_fact, YEAR_KEYS, yes_no), "fact-type"))
    citizens.extend([
        (_load("family.f1098e-1.json"), "source-family"),
        (_load("closure-mapping.f1098e.1.json"), "source-closure-mapping"),
        (_load("parameter.sli-interest-cap.json"), "parameter"),
        (_load("parameter.sli-magi-threshold.json"), "parameter"),
        (_load("parameter.sli-magi-phase-range.json"), "parameter"),
        (_load("citation.form1040.sli-worksheet.json"), "citation"),
        (_load("citation.schedule1.line-21.json"), "citation"),
        ({"schema": "parameter-declaration.v1", "id": COVERAGE_PARAM, "version": "v1",
          "scope": dict(SCOPE), "values": "0"}, "parameter"),
        (_load("rule.sli-worksheet-line1-subtotal.json"), "computation"),
        (rule(COUNT_RULE, subject=INCL, publishes=COUNT,
              value={"op": "shared_key_count", "fact_type": FIN, "key": "borrowing"}), "computation"),
        (rule(SUPPORT_RULE, subject=INCL, joined=LOAN, direction="subject_contains_joined",
              requires=[LOAN, ENROLL], publishes=SUPPORT, value=_support_value()), "computation"),
        (statement, "computation"),
    ])
    for answer in ANSWERS:
        citizens.append((_status_rule(answer), "computation"))
    citizens.append((worksheet_rule or worksheet(), "computation"))
    return citizens


def package_for(citizens: list[tuple[dict[str, Any], str]], *,
                entrypoints: list[str] | None = None) -> dict[str, Any]:
    package: dict[str, Any] = {
        "schema": "artifact-package.v35",
        "id": "demo.package.adr0077-worksheet",
        "version": "v1",
        "scope": dict(SCOPE),
        "admitted_schemas": sorted({citizen["schema"] for citizen, _role in citizens}),
        "members": [
            {"role": role, "schema": citizen["schema"], "id": citizen["id"], "version": citizen["version"]}
            for citizen, role in citizens
        ],
        "input_bindings": [
            {"symbol": "filing_status", "fact_type": {"id": FILING_STATUS, "version": "v1"}, "mode": "required"},
        ] if any(citizen["id"] == FILING_STATUS for citizen, _role in citizens) else [],
        "entrypoints": [
            {"id": citizen["id"], "version": citizen["version"]}
            for citizen, _role in citizens
            if entrypoints is None or citizen["id"] in entrypoints
        ],
        "composition_obligations": [],
    }
    package["package_checksum"] = package_instance_checksum(package)
    return package


def validate(citizens: list[tuple[dict[str, Any], str]], **kwargs: Any) -> tuple[dict[str, Any], PackageValidation]:
    package = package_for(citizens, **kwargs)
    corpus = {(citizen["id"], citizen["version"]): citizen for citizen, _role in citizens}
    return package, validate_package(package, corpus, DerivationSchemas())


# ---------------------------------------------------------------------------
# Kernel state
# ---------------------------------------------------------------------------


class _HorizonState:
    def __init__(self, current_by_chain: dict[tuple[str, str, str], str]) -> None:
        self.current_by_chain = current_by_chain


class _State:
    def __init__(self, findings: dict[str, dict[str, Any]], lattice: dict[str, dict[str, Any]],
                 current_by_chain: dict[tuple[str, str, str], str]) -> None:
        self.findings = findings
        self.horizon_state = _HorizonState(current_by_chain)
        self.fact_state = KernelState(fact_types=lattice)


def row(fid: str, type_id: str, keys: tuple[tuple[str, str], ...], value: Any, *,
        basis: str = "attested", current: bool = True) -> dict[str, Any]:
    return {"id": fid, "type": type_id, "keys": keys, "value": value, "basis": basis, "current": current}


def world(rows: list[dict[str, Any]], *, closed: bool = True) -> tuple[_State, list[str]]:
    findings: dict[str, dict[str, Any]] = {}
    names: dict[str, list[str]] = {}
    values: dict[str, dict[str, set[str]]] = {}
    all_rows = list(rows)
    if closed:
        all_rows.append(row("demo.finding.f1098e-closure", CLOSURE_TYPE, (("family-horizon", "demo-h0"),), True))
    for item in all_rows:
        rendered = ",".join(f"{name}={value}" for name, value in item["keys"])
        findings[item["id"]] = {
            "id": item["id"], "fact_id": f"{item['type']}|{rendered}",
            "value": item["value"], "basis": item["basis"],
        }
        order = names.setdefault(item["type"], [])
        bucket = values.setdefault(item["type"], {})
        for name, value in item["keys"]:
            if name not in order:
                order.append(name)
            bucket.setdefault(name, set()).add(value)
    lattice = {
        type_id: {
            "id": type_id,
            "nature": "record",
            "identity_keys": [
                {"name": name, "kind": "literal", "values": sorted(values[type_id][name])}
                for name in order
            ],
        }
        for type_id, order in names.items()
        if order
    }
    chains = {(FAMILY, "v1", "demo-scope"): "demo-h0"}
    return _State(findings, lattice, chains), [item["id"] for item in all_rows if item["current"]]


class _Graph:
    def __init__(self, resolved_members: Any, package: dict[str, Any]) -> None:
        self.resolved_members = resolved_members
        self.package = package


def marshal(citizens: list[tuple[dict[str, Any], str]], rows: list[dict[str, Any]], *,
            closed: bool = True, run_id: str = "demo.run.adr0077-worksheet") -> RunContext:
    package, validation = validate(citizens)
    if not validation.ok:
        raise AssertionError(validation.issues)
    state, current = world(rows, closed=closed)
    material = _resolved_run_material(_Graph(list(validation.resolved_members), package))
    rules, parameters, families, mappings, fact_types, bindings, collect_names = material
    schemas = DerivationSchemas()
    return marshal_run_context(
        run_id=run_id,
        state=state,  # type: ignore[arg-type]
        currency=CurrencyView(
            current_finding_ids=frozenset(current),
            displaced_finding_ids=frozenset(),
            current_evidence_ids=frozenset(),
            displaced_evidence_ids=frozenset(),
        ),
        rules=rules,
        parameters=parameters,
        canon=load_canon(schemas),
        adoption_pin=ADOPTION_PIN,
        governance_pins=GOVERNANCE_PINS,
        family_declarations=families,
        closure_mappings=mappings,
        fact_types=fact_types,
        input_bindings=bindings,
        collect_source_names=collect_names,
        emission_only_source_names=list(material.emission_only_names),
        parameter_index=material.parameter_index,
    )


def both_runners(ctx: RunContext) -> tuple[RunResult, RunResult]:
    schemas = DerivationSchemas()
    return run(ctx, schemas), run_reference(ctx, schemas)


# ---------------------------------------------------------------------------
# Rows
# ---------------------------------------------------------------------------


def box_keys(statement: str) -> tuple[tuple[str, str], ...]:
    return (("lender", "demo-lender"), ("statement", statement), ("tax-year", "2025"))


def box_fact_id(statement: str) -> str:
    return f"{BOX1}|" + ",".join(f"{name}={value}" for name, value in box_keys(statement))


def box(statement: str = "demo-stmt", amount: str = "3000") -> dict[str, Any]:
    return row(f"demo.finding.box.{statement}", BOX1, box_keys(statement), amount)


def answers(statement: str = "demo-stmt", value: str = "yes") -> list[dict[str, Any]]:
    return [
        row(f"demo.finding.answer.{tail}.{statement}", answer, box_keys(statement), value)
        for answer, tail in zip(ANSWERS, ANSWER_TAILS)
    ]


def links(statement: str = "demo-stmt", loan: str = "demo-loan", *,
          loan_answer: str | None = "yes") -> list[dict[str, Any]]:
    rows = [
        row(f"demo.finding.inclusion.{statement}.{loan}", INCL, box_keys(statement) + (("borrowing", loan),),
            "sli.statement-inclusion.affirmed"),
        row(f"demo.finding.financing.{loan}", FIN,
            (("borrowing", loan), ("period", "demo-2022"), ("institution", "demo-college"),
             ("programme", "demo-programme")),
            "sli.financing.affirmed"),
        row(f"demo.finding.enroll-answer.{loan}", ENROLL, (("borrowing", loan),), "yes"),
    ]
    if loan_answer is not None:
        rows.append(row(f"demo.finding.loan-answer.{loan}", LOAN, (("borrowing", loan),), loan_answer))
    return rows


def return_inputs(total_income: str = "50000", filing_status: str = "single") -> list[dict[str, Any]]:
    year = (("tax-year", "2025"),)
    rows = [
        row("demo.finding.filing-status", FILING_STATUS, year, filing_status, basis="elective"),
        row("demo.finding.total-income", TOTAL_INCOME, year, total_income),
        row("demo.finding.rounding", ROUNDING, (), "half_up"),
    ]
    rows.extend(
        row(f"demo.finding.scope.{fact.rsplit('.', 1)[-1]}", fact, year, "yes")
        for fact in SCOPE_FACTS
    )
    return rows


def case_rows(name: str) -> list[dict[str, Any]]:
    base = return_inputs()
    if name == "old-only":
        return [*base, box(), *answers()]
    if name == "new-only":
        return [*base, box(), *links()]
    if name == "both":
        return [*base, box(), *links(), *answers()]
    if name == "closed-empty":
        return base
    if name == "nonempty-neither":
        return [*base, box()]
    raise KeyError(name)


# ---------------------------------------------------------------------------
# Reading results
# ---------------------------------------------------------------------------


def line21(result: RunResult) -> dict[str, Any]:
    """The worksheet's one outcome: a publication or a block."""
    for publication in result.publications:
        if publication.finding["symbol"] == LINE21:
            return {"value": publication.finding["value"], "finding": publication.finding}
    rows = [item for item in result.dispositions if item.get("artifact_id") == WORKSHEET]
    if len(rows) != 1:
        raise AssertionError(rows)
    return {"disposition": rows[0]["disposition"], "code": rows[0].get("code"),
            "missing": rows[0].get("missing"), "pins": rows[0]["pins"]}


def signature(result: RunResult) -> str:
    """Values, pins and blocked rows, without publication order."""
    published = sorted(
        (pub.finding["symbol"], pub.finding["value"], json.dumps(pub.finding["pins"], sort_keys=True))
        for pub in result.publications
    )
    blocked = sorted(json.dumps(item, sort_keys=True) for item in result.blocked)
    dispositions = sorted(json.dumps(item, sort_keys=True) for item in result.dispositions)
    return json.dumps([published, blocked, dispositions])
