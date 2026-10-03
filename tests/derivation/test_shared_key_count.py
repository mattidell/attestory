"""ADR 0077 Part 1: ``shared_key_count`` on the validated live path.

Every runtime case goes through ``validate_package`` (a real
``artifact-package.v35`` package of ``rule-artifact.v13`` rules),
``live._resolved_run_material`` on the validated members, and
``marshal_run_context`` over a kernel state with a real fact lattice. Both
``run`` and ``run_reference`` execute and must agree. No ``RunContext`` is
built or edited by hand: a row with no identity, or without the counted key,
is produced by the state the marshaller reads.

The cases are the ADR's "Runtime" items 1-3 and "Pins", and Track 0d
evidence 5's production list. One case recovers a saved ActLog written by
the real relationship recorder.
"""

from __future__ import annotations

import copy
import json
import unittest
from typing import Any

from packages.derivation.live import _resolved_run_material
from packages.derivation.loader import DerivationSchemas
from packages.derivation.marshal import marshal_run_context
from packages.derivation.package_validation import (
    PackageValidation,
    package_instance_checksum,
    validate_package,
)
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import RunContext, run
from packages.kernel.currency import CurrencyView
from packages.kernel.facts import KernelState

SCOPE = {"tax_year": 2025, "jurisdiction": "us", "family": "demo-student-loan"}
ADOPTION_PIN = {"role": "adoption", "id": "demo.package.shared-key-count", "version": "v1"}
GOVERNANCE_PINS = [{"role": "governance", "id": "demo.governance.shared-key-count", "version": "v1"}]

BOX1 = "tax.us.2025.f1098e.box1-student-loan-interest"
INCL = "tax.us.2025.sli.statement-inclusion-relationship"
FIN = "tax.us.2025.sli.financing-relationship"
LOAN = "demo.tax.skc.loan-paid-only-school-costs"
ENROLL = "demo.tax.skc.enrolled-half-time-for-this-loan"

BOX_KEYS = ("lender", "statement", "tax-year")
INCL_KEYS = ("lender", "statement", "tax-year", "borrowing")
FIN_KEYS = ("borrowing", "period", "institution", "programme")
LOAN_KEYS = ("borrowing",)

COUNT = "demo.tax.skc.financing-count"
SUPPORT = "demo.tax.skc.inclusion-support"
CONCLUSION = "demo.tax.skc.statement-conclusion"
COUNT_RULE = "demo.rule.skc.financing-count"
SUPPORT_RULE = "demo.rule.skc.inclusion-support"
STATEMENT_RULE = "demo.rule.skc.statement-conclusion"
COVERAGE_PARAM = "demo.param.skc.coverage-empty"

PLAIN = "plain-case-supported"
NOT = "not-supported"
KEYS_UNAVAILABLE = "link-coverage-keys-unavailable"

BASIS = {
    "said": [
        "The loan-cost answer is yes for the named borrowing.",
        "The enrollment answer is yes for the named period, institution, and programme.",
        "The person affirmed that the borrowing financed the schooling.",
        "The person affirmed that the statement includes interest on the borrowing.",
    ],
    "derived": [
        "The inclusion count is 1.",
        "The financing count is 1.",
    ],
    "assumed": [
        "The expenses fall in a reasonable period.",
        "Box 1 holds no loan the person did not record.",
    ],
    "left_with_person": [
        "The institution is an eligible educational institution.",
        "The enrollment meets that institution's half-time standard.",
    ],
}


# ---------------------------------------------------------------------------
# Package: three v13 rules and the fact surface they read.
# ---------------------------------------------------------------------------


def _fact_type(fact_id: str, key_names: tuple[str, ...], values: list[str] | None = None) -> dict[str, Any]:
    value_schema: dict[str, Any] = {"type": "string", "minLength": 1} if values is None else {"type": "string", "enum": values}
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": "v1",
        "title": fact_id,
        "nature": "determinable",
        "identity_keys": [{"name": name, "kind": "literal", "values": ["placeholder"]} for name in key_names],
        "value_schema": value_schema,
        "supersession": {"policy": "free"},
    }


def _rule(rule_id: str, *, subject: str | None, publishes: str, value: Any, joined: str | None = None,
          direction: str | None = None, requires: list[str] | None = None, when: Any = True,
          schema: str = "rule-artifact.v13") -> dict[str, Any]:
    rule: dict[str, Any] = {
        "schema": schema,
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
        rule["subject"] = {"id": subject, "version": "v1"}
    if joined is not None:
        rule["joined"] = {"id": joined, "version": "v1"}
    if direction is not None:
        rule["direction"] = direction
    return rule


def _count(fact_type: str = FIN, key: str = "borrowing") -> dict[str, Any]:
    return {"op": "shared_key_count", "fact_type": fact_type, "key": key}


def _eq(left: Any, right: Any) -> dict[str, Any]:
    return {"op": "compare", "cmp": "eq", "left": left, "right": right}


def _answer_yes(name: str) -> dict[str, Any]:
    return {
        "op": "categorical_compare",
        "cmp": "eq",
        "left": {"op": "ref", "name": name},
        "right": {"op": "category_literal", "fact_type": {"id": name, "version": "v1"}, "value": "yes"},
    }


def _support_value() -> dict[str, Any]:
    return {
        "op": "choose",
        "when": {"op": "all", "args": [_eq(_count(), 1), _answer_yes(LOAN), _answer_yes(ENROLL)]},
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


def chain_parts(*, basis: dict[str, Any] | None = None) -> list[tuple[dict[str, Any], str]]:
    """The direct count, the inclusion support, and the statement conclusion."""
    statement = _rule(
        STATEMENT_RULE, subject=BOX1, joined=INCL, direction="joined_contains_subject",
        publishes=CONCLUSION, value=_statement_value(),
    )
    statement["basis"] = copy.deepcopy(BASIS if basis is None else basis)
    return [
        (_fact_type(BOX1, BOX_KEYS), "fact-type"),
        (_fact_type(INCL, INCL_KEYS, ["sli.statement-inclusion.affirmed"]), "fact-type"),
        (_fact_type(FIN, FIN_KEYS, ["sli.financing.affirmed", "sli.financing.cannot-tell"]), "fact-type"),
        (_fact_type(LOAN, LOAN_KEYS, ["yes", "no", "cannot-tell"]), "fact-type"),
        (_fact_type(ENROLL, LOAN_KEYS, ["yes", "no", "cannot-tell"]), "fact-type"),
        ({"schema": "parameter-declaration.v1", "id": COVERAGE_PARAM, "version": "v1",
          "scope": dict(SCOPE), "values": "0"}, "parameter"),
        (_rule(COUNT_RULE, subject=INCL, publishes=COUNT, value=_count()), "computation"),
        (_rule(SUPPORT_RULE, subject=INCL, joined=LOAN, direction="subject_contains_joined",
               requires=[LOAN, ENROLL], publishes=SUPPORT, value=_support_value()), "computation"),
        (statement, "computation"),
    ]


def package_for(parts: list[tuple[dict[str, Any], str]], *, schema: str = "artifact-package.v35",
                package_id: str = "demo.package.shared-key-count") -> dict[str, Any]:
    package: dict[str, Any] = {
        "schema": schema,
        "id": package_id,
        "version": "v1",
        "scope": dict(SCOPE),
        "admitted_schemas": sorted({citizen["schema"] for citizen, _role in parts}),
        "members": [
            {"role": role, "schema": citizen["schema"], "id": citizen["id"], "version": citizen["version"]}
            for citizen, role in parts
        ],
        "input_bindings": [],
        "entrypoints": [{"id": citizen["id"], "version": citizen["version"]} for citizen, _role in parts],
        "composition_obligations": [],
    }
    package["package_checksum"] = package_instance_checksum(package)
    return package


def validate(parts: list[tuple[dict[str, Any], str]], **kwargs: Any) -> tuple[dict[str, Any], PackageValidation]:
    package = package_for(parts, **kwargs)
    corpus = {(citizen["id"], citizen["version"]): citizen for citizen, _role in parts}
    return package, validate_package(package, corpus, DerivationSchemas())


def codes(validation: PackageValidation) -> list[str]:
    return [issue.code for issue in validation.issues]


# ---------------------------------------------------------------------------
# Kernel state: findings plus the fact lattice the marshaller reads keys from.
# ---------------------------------------------------------------------------


class _HorizonState:
    def __init__(self) -> None:
        self.current_by_chain: dict[tuple[str, str, str], str] = {}


class _State:
    def __init__(self, findings: dict[str, dict[str, Any]], lattice: dict[str, dict[str, Any]]) -> None:
        self.findings = findings
        self.horizon_state = _HorizonState()
        self.fact_state = KernelState(fact_types=lattice)


def row(fid: str, type_id: str, keys: tuple[tuple[str, str], ...], value: str, *,
        unlisted: bool = False, current: bool = True) -> dict[str, Any]:
    """One finding. ``unlisted`` keeps its keys out of the lattice, so the
    marshaller reads no identity for it (keys None)."""
    return {"id": fid, "type": type_id, "keys": keys, "value": value, "unlisted": unlisted, "current": current}


def world(rows: list[dict[str, Any]]) -> tuple[_State, list[str]]:
    findings: dict[str, dict[str, Any]] = {}
    names: dict[str, list[str]] = {}
    values: dict[str, dict[str, set[str]]] = {}
    for item in rows:
        rendered = ",".join(f"{name}={value}" for name, value in item["keys"])
        findings[item["id"]] = {
            "id": item["id"], "fact_id": f"{item['type']}|{rendered}",
            "value": item["value"], "basis": "attested",
        }
        if item["unlisted"]:
            continue
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
    }
    return _State(findings, lattice), [item["id"] for item in rows if item["current"]]


class _Graph:
    def __init__(self, resolved_members: Any, package: dict[str, Any]) -> None:
        self.resolved_members = resolved_members
        self.package = package


def marshal(parts: list[tuple[dict[str, Any], str]], state: Any, current: list[str]) -> RunContext:
    package, validation = validate(parts)
    if not validation.ok:
        raise AssertionError(validation.issues)
    material = _resolved_run_material(_Graph(list(validation.resolved_members), package))
    rules, parameters, families, mappings, fact_types, bindings, collect_names = material
    return marshal_run_context(
        run_id="demo.run.shared-key-count",
        state=state,
        currency=CurrencyView(
            current_finding_ids=frozenset(current),
            displaced_finding_ids=frozenset(),
            current_evidence_ids=frozenset(),
            displaced_evidence_ids=frozenset(),
        ),
        rules=rules,
        parameters=parameters,
        canon={},
        adoption_pin=ADOPTION_PIN,
        governance_pins=GOVERNANCE_PINS,
        family_declarations=families,
        closure_mappings=mappings,
        fact_types=fact_types,
        input_bindings=bindings,
        collect_source_names=collect_names,
        emission_only_source_names=list(material.emission_only_names),
    )


def both_runners(ctx: RunContext) -> tuple[Any, Any]:
    schemas = DerivationSchemas()
    return run(ctx, schemas), run_reference(ctx, schemas)


def outcome(result: Any, symbol: str) -> dict[str, Any]:
    """One subject's outcome: its published value and pins, or its block."""
    for publication in result.publications:
        if publication.finding["symbol"] == symbol:
            return {"value": publication.finding["value"], "pins": publication.finding["pins"]}
    rows = [item for item in result.dispositions if item.get("symbol") == symbol]
    if len(rows) != 1:
        raise AssertionError(f"{symbol}: {rows}")
    return {"blocked": rows[0]["code"], "missing": rows[0]["missing"], "pins": rows[0]["pins"]}


def inputs(pins: list[dict[str, Any]]) -> set[str]:
    return {str(pin["id"]) for pin in pins if pin.get("role") == "input"}


def keyed(symbol: str, fact_type: str, keys: tuple[tuple[str, str], ...]) -> str:
    return f"{symbol}|{fact_type}|" + ",".join(f"{name}={value}" for name, value in keys)


def box_keys(statement: str) -> tuple[tuple[str, str], ...]:
    return (("lender", "demo-lender"), ("statement", statement), ("tax-year", "2025"))


def incl_keys(statement: str, loan: str) -> tuple[tuple[str, str], ...]:
    return box_keys(statement) + (("borrowing", loan),)


def fin_keys(loan: str, period: str) -> tuple[tuple[str, str], ...]:
    return (("borrowing", loan), ("period", period), ("institution", "demo-college"), ("programme", "demo-programme"))


def box(statement: str, amount: str = "3000") -> dict[str, Any]:
    return row(f"demo.finding.box.{statement}", BOX1, box_keys(statement), amount)


def inclusion(statement: str, loan: str, **kwargs: Any) -> dict[str, Any]:
    return row(f"demo.finding.inclusion.{statement}.{loan}", INCL, incl_keys(statement, loan),
               "sli.statement-inclusion.affirmed", **kwargs)


def financing(loan: str, period: str, value: str = "sli.financing.affirmed", **kwargs: Any) -> dict[str, Any]:
    return row(f"demo.finding.financing.{loan}.{period}", FIN, fin_keys(loan, period), value, **kwargs)


def answers(loan: str) -> list[dict[str, Any]]:
    return [
        row(f"demo.finding.loan-answer.{loan}", LOAN, (("borrowing", loan),), "yes"),
        row(f"demo.finding.enroll-answer.{loan}", ENROLL, (("borrowing", loan),), "yes"),
    ]


def plain(statement: str = "demo-stmt", loan: str = "demo-loan",
          periods: tuple[str, ...] = ("demo-2022",)) -> list[dict[str, Any]]:
    rows = [box(statement), inclusion(statement, loan), *answers(loan)]
    rows.extend(financing(loan, period) for period in periods)
    return rows


def run_rows(rows: list[dict[str, Any]], parts: list[tuple[dict[str, Any], str]] | None = None) -> tuple[Any, Any]:
    state, current = world(rows)
    forward, reference = both_runners(marshal(parts or chain_parts(), state, current))
    return forward, reference


def signature(result: Any, symbols: list[str]) -> list[Any]:
    out = []
    for symbol in symbols:
        item = outcome(result, symbol)
        out.append((symbol, item.get("value"), item.get("blocked"), tuple(item.get("missing", ())),
                    json.dumps(item["pins"], sort_keys=True)))
    return out


COUNT_DEMO = keyed(COUNT, INCL, incl_keys("demo-stmt", "demo-loan"))
SUPPORT_DEMO = keyed(SUPPORT, INCL, incl_keys("demo-stmt", "demo-loan"))
CONCLUSION_DEMO = keyed(CONCLUSION, BOX1, box_keys("demo-stmt"))


class SharedKeyCountRuntime(unittest.TestCase):
    """Runtime items 1-3 and Pins, as Track 0d evidence 5's direct table."""

    def assert_agree(self, forward: Any, reference: Any, symbols: list[str]) -> None:
        self.assertEqual(signature(forward, symbols), signature(reference, symbols))

    def test_two_periods_with_equal_values_count_two_and_pin_both(self) -> None:
        forward, reference = run_rows(plain(periods=("demo-2022", "demo-2023")))
        self.assert_agree(forward, reference, [COUNT_DEMO, SUPPORT_DEMO, CONCLUSION_DEMO])
        for result in (forward, reference):
            count = outcome(result, COUNT_DEMO)
            self.assertEqual(count["value"], "2")
            self.assertEqual(inputs(count["pins"]), {
                "demo.finding.inclusion.demo-stmt.demo-loan",
                "demo.finding.financing.demo-loan.demo-2022",
                "demo.finding.financing.demo-loan.demo-2023",
            })
            for pin in count["pins"]:
                if pin["id"].startswith("demo.finding.financing."):
                    self.assertEqual(pin, {"role": "input", "id": pin["id"], "version": "v1", "origin": "assertion"})
            support = outcome(result, SUPPORT_DEMO)
            self.assertEqual(support["value"], "0")
            self.assertEqual(inputs(support["pins"]), {
                "demo.finding.inclusion.demo-stmt.demo-loan",
                "demo.finding.financing.demo-loan.demo-2022",
                "demo.finding.financing.demo-loan.demo-2023",
            })
            self.assertEqual(outcome(result, CONCLUSION_DEMO)["value"], NOT)

    def test_one_matching_row_counts_one_and_the_chain_supports(self) -> None:
        forward, reference = run_rows(plain())
        self.assert_agree(forward, reference, [COUNT_DEMO, SUPPORT_DEMO, CONCLUSION_DEMO])
        for result in (forward, reference):
            count = outcome(result, COUNT_DEMO)
            self.assertEqual(count["value"], "1")
            self.assertEqual(inputs(count["pins"]), {
                "demo.finding.inclusion.demo-stmt.demo-loan",
                "demo.finding.financing.demo-loan.demo-2022",
            })
            support = outcome(result, SUPPORT_DEMO)
            self.assertEqual(support["value"], "1")
            self.assertEqual(inputs(support["pins"]), {
                "demo.finding.loan-answer.demo-loan",
                "demo.finding.enroll-answer.demo-loan",
                "demo.finding.financing.demo-loan.demo-2022",
                "demo.finding.inclusion.demo-stmt.demo-loan",
            })
            self.assertEqual(outcome(result, CONCLUSION_DEMO)["value"], PLAIN)

    def test_no_current_match_is_zero_with_no_counted_pin(self) -> None:
        cases = {
            "no financing row": [box("demo-stmt"), inclusion("demo-stmt", "demo-loan"), *answers("demo-loan")],
            "financing not current": [
                box("demo-stmt"), inclusion("demo-stmt", "demo-loan"), *answers("demo-loan"),
                financing("demo-loan", "demo-2022", current=False),
            ],
            "financing for another borrowing": [
                box("demo-stmt"), inclusion("demo-stmt", "demo-loan"), *answers("demo-loan"),
                financing("demo-other-loan", "demo-2022"),
            ],
        }
        for name, rows in cases.items():
            with self.subTest(name):
                forward, reference = run_rows(rows)
                self.assert_agree(forward, reference, [COUNT_DEMO, SUPPORT_DEMO, CONCLUSION_DEMO])
                for result in (forward, reference):
                    count = outcome(result, COUNT_DEMO)
                    self.assertEqual(count["value"], "0")
                    self.assertEqual(inputs(count["pins"]), {"demo.finding.inclusion.demo-stmt.demo-loan"})
                    support = outcome(result, SUPPORT_DEMO)
                    self.assertEqual(support["value"], "0")
                    self.assertEqual(inputs(support["pins"]), {"demo.finding.inclusion.demo-stmt.demo-loan"})
                    self.assertEqual(outcome(result, CONCLUSION_DEMO)["value"], NOT)

    def test_values_are_not_read(self) -> None:
        rows = plain(periods=())
        rows.append(financing("demo-loan", "demo-2022", "sli.financing.cannot-tell"))
        forward, reference = run_rows(rows)
        self.assert_agree(forward, reference, [COUNT_DEMO])
        for result in (forward, reference):
            count = outcome(result, COUNT_DEMO)
            self.assertEqual(count["value"], "1")
            self.assertIn("demo.finding.financing.demo-loan.demo-2022", inputs(count["pins"]))

    def test_two_statements_two_borrowings_each_pin_their_own_financing(self) -> None:
        rows = plain("demo-stmt", "demo-loan") + plain("demo-stmt-b", "demo-loan-b")
        forward, reference = run_rows(rows)
        count_b = keyed(COUNT, INCL, incl_keys("demo-stmt-b", "demo-loan-b"))
        support_b = keyed(SUPPORT, INCL, incl_keys("demo-stmt-b", "demo-loan-b"))
        conclusion_b = keyed(CONCLUSION, BOX1, box_keys("demo-stmt-b"))
        symbols = [COUNT_DEMO, count_b, SUPPORT_DEMO, support_b, CONCLUSION_DEMO, conclusion_b]
        self.assert_agree(forward, reference, symbols)
        for result in (forward, reference):
            self.assertEqual(outcome(result, COUNT_DEMO)["value"], "1")
            self.assertEqual(outcome(result, count_b)["value"], "1")
            pins_a = inputs(outcome(result, SUPPORT_DEMO)["pins"])
            pins_b = inputs(outcome(result, support_b)["pins"])
            self.assertIn("demo.finding.financing.demo-loan.demo-2022", pins_a)
            self.assertNotIn("demo.finding.financing.demo-loan-b.demo-2022", pins_a)
            self.assertIn("demo.finding.financing.demo-loan-b.demo-2022", pins_b)
            self.assertNotIn("demo.finding.financing.demo-loan.demo-2022", pins_b)
            self.assertEqual(outcome(result, CONCLUSION_DEMO)["value"], PLAIN)
            self.assertEqual(outcome(result, conclusion_b)["value"], PLAIN)

    def test_a_counted_row_with_null_keys_blocks_and_is_pinned(self) -> None:
        rows = plain()
        rows.append(financing("demo-loan", "demo-unlisted", unlisted=True))
        forward, reference = run_rows(rows)
        self.assert_agree(forward, reference, [COUNT_DEMO, SUPPORT_DEMO])
        bad = "demo.finding.financing.demo-loan.demo-unlisted"
        for result in (forward, reference):
            count = outcome(result, COUNT_DEMO)
            self.assertEqual(count.get("blocked"), "DEPENDENCY_INVALID")
            self.assertEqual(count["missing"], [bad])
            self.assertIn(bad, inputs(count["pins"]))
            self.assertNotIn("value", count)
            support = outcome(result, SUPPORT_DEMO)
            self.assertEqual(support.get("blocked"), "DEPENDENCY_INVALID")
            self.assertEqual(support["missing"], [bad])
            self.assertNotIn(CONCLUSION_DEMO, {p.finding["symbol"] for p in result.publications})

    def test_a_counted_row_without_the_key_blocks_every_inclusion(self) -> None:
        # The kernel's financing identity here has no `borrowing`; the package
        # declares it. Every row then lacks the counted key.
        rows = [
            *[r for r in plain("demo-stmt", "demo-loan") if r["type"] != FIN],
            *[r for r in plain("demo-stmt-b", "demo-loan-b") if r["type"] != FIN],
            row("demo.finding.financing.no-borrowing", FIN,
                (("period", "demo-2022"), ("institution", "demo-college"), ("programme", "demo-programme")),
                "sli.financing.affirmed"),
        ]
        forward, reference = run_rows(rows)
        support_b = keyed(SUPPORT, INCL, incl_keys("demo-stmt-b", "demo-loan-b"))
        conclusion_b = keyed(CONCLUSION, BOX1, box_keys("demo-stmt-b"))
        symbols = [SUPPORT_DEMO, support_b, CONCLUSION_DEMO, conclusion_b]
        self.assert_agree(forward, reference, symbols)
        for result in (forward, reference):
            for symbol in (SUPPORT_DEMO, support_b):
                support = outcome(result, symbol)
                self.assertEqual(support.get("blocked"), "DEPENDENCY_INVALID")
                self.assertEqual(support["missing"], ["demo.finding.financing.no-borrowing"])
                self.assertIn("demo.finding.financing.no-borrowing", inputs(support["pins"]))
            for symbol, inclusion_id in (
                (CONCLUSION_DEMO, "demo.finding.inclusion.demo-stmt.demo-loan"),
                (conclusion_b, "demo.finding.inclusion.demo-stmt-b.demo-loan-b"),
            ):
                conclusion = outcome(result, symbol)
                self.assertEqual(conclusion.get("blocked"), "DEPENDENCY_INVALID")
                self.assertEqual(conclusion["missing"], [inclusion_id])

    def test_subject_keys_null_blocks_without_naming_a_counted_row(self) -> None:
        rows = [box("demo-stmt"), inclusion("demo-stmt", "demo-loan-unlisted", unlisted=True),
                *answers("demo-loan-unlisted"), financing("demo-loan-unlisted", "demo-2022")]
        forward, reference = run_rows(rows)
        symbol = keyed(COUNT, INCL, incl_keys("demo-stmt", "demo-loan-unlisted"))
        self.assert_agree(forward, reference, [symbol])
        for result in (forward, reference):
            count = outcome(result, symbol)
            self.assertEqual(count.get("blocked"), "DEPENDENCY_INVALID")
            self.assertEqual(count["missing"], [KEYS_UNAVAILABLE])
            self.assertEqual(inputs(count["pins"]), {"demo.finding.inclusion.demo-stmt.demo-loan-unlisted"})

    def test_subject_map_without_the_key_blocks_without_naming_a_counted_row(self) -> None:
        # The kernel's inclusion identity here has no `borrowing`.
        rows = [box("demo-stmt"),
                row("demo.finding.inclusion.no-borrowing", INCL, box_keys("demo-stmt"),
                    "sli.statement-inclusion.affirmed"),
                financing("demo-loan", "demo-2022")]
        forward, reference = run_rows(rows)
        symbol = keyed(COUNT, INCL, box_keys("demo-stmt"))
        self.assert_agree(forward, reference, [symbol])
        for result in (forward, reference):
            count = outcome(result, symbol)
            self.assertEqual(count.get("blocked"), "DEPENDENCY_INVALID")
            self.assertEqual(count["missing"], [KEYS_UNAVAILABLE])
            self.assertNotIn("demo.finding.financing.demo-loan.demo-2022", inputs(count["pins"]))

    def test_counted_type_reaches_the_run_as_a_source(self) -> None:
        state, current = world(plain())
        ctx = marshal(chain_parts(), state, current)
        self.assertIn(FIN, {source.name for source in ctx.sources})
        material_parts = chain_parts()
        package, validation = validate(material_parts)
        material = _resolved_run_material(_Graph(list(validation.resolved_members), package))
        self.assertIn(FIN, material.emission_only_names)


class SharedKeyCountValidation(unittest.TestCase):
    """ADR 0077 Part 1, "Validation"."""

    def _count_rule(self, parts: list[tuple[dict[str, Any], str]]) -> dict[str, Any]:
        return next(citizen for citizen, _ in parts if citizen["id"] == COUNT_RULE)

    def test_chain_validates(self) -> None:
        _package, validation = validate(chain_parts())
        self.assertTrue(validation.ok, validation.issues)

    def test_return_level_rule_is_refused(self) -> None:
        parts = chain_parts()
        self._count_rule(parts).pop("subject")
        _package, validation = validate(parts)
        self.assertIn("SHARED_KEY_COUNT_INVALID", codes(validation))
        self.assertTrue(any("return-level" in issue.detail for issue in validation.issues))

    def test_once_in_value_never_in_when(self) -> None:
        parts = chain_parts()
        self._count_rule(parts)["when"] = _eq(_count(), 1)
        _package, validation = validate(parts)
        self.assertIn("SHARED_KEY_COUNT_INVALID", codes(validation))
        parts = chain_parts()
        self._count_rule(parts)["value"] = {"op": "add", "args": [_count(), _count()]}
        _package, validation = validate(parts)
        self.assertIn("SHARED_KEY_COUNT_INVALID", codes(validation))

    def test_key_must_name_identity_of_subject_and_counted_type(self) -> None:
        parts = chain_parts()
        self._count_rule(parts)["value"] = _count(key="period")
        _package, validation = validate(parts)
        self.assertIn("SHARED_KEY_COUNT_INVALID", codes(validation))
        self.assertTrue(any("of subject" in issue.detail for issue in validation.issues))
        parts = chain_parts()
        self._count_rule(parts)["value"] = _count(key="lender")
        _package, validation = validate(parts)
        self.assertTrue(any("of counted fact type" in issue.detail for issue in validation.issues))

    def test_counted_type_must_be_on_the_fact_surface(self) -> None:
        parts = chain_parts()
        self._count_rule(parts)["value"] = _count(fact_type="demo.tax.skc.undeclared")
        _package, validation = validate(parts)
        self.assertIn("SHARED_KEY_COUNT_INVALID", codes(validation))

    def test_v12_rule_and_v34_package_reject_the_operator(self) -> None:
        parts = chain_parts()
        self._count_rule(parts)["schema"] = "rule-artifact.v12"
        _package, validation = validate(parts)
        self.assertIn("MEMBER_SCHEMA_INVALID", codes(validation))
        _package, validation = validate(chain_parts(), schema="artifact-package.v34")
        self.assertIn("PACKAGE_SCHEMA_INVALID", codes(validation))

    def test_a_v13_selection_is_refused_until_parts_3_and_4_run(self) -> None:
        parts = chain_parts()
        selection_rule = _rule("demo.rule.skc.worksheet", subject=None, publishes="demo.tax.skc.line21", value=0)
        selection_rule.pop("value")
        selection_rule["selection"] = {
            "mode": "exclusive_presence",
            "conflict": "refuse",
            "paths": [
                {"id": path_id, "activity": {"kind": "source_nonempty", "member_fact_types": [{"id": member, "version": "v1"}]},
                 "reads_subject_results": [], "requires": [], "pins": [], "when": True, "value": 1}
                for path_id, member in (("old", LOAN), ("new", INCL))
            ],
            "default": {"id": "neither", "reads_subject_results": [], "requires": [], "pins": [], "when": True, "value": 0},
            "refusal": {"code": "DEPENDENCY_INVALID", "missing": ["demo-both-present"], "pins": []},
        }
        parts.append((selection_rule, "computation"))
        _package, validation = validate(parts)
        self.assertIn("RULE_SELECTION_UNAUTHORIZED", codes(validation))

    def test_a_return_level_v13_value_rule_validates_and_runs(self) -> None:
        parts = chain_parts()
        parts.append((_rule("demo.rule.skc.constant", subject=None, publishes="demo.tax.skc.constant", value=7),
                      "computation"))
        state, current = world(plain())
        forward, reference = both_runners(marshal(parts, state, current))
        for result in (forward, reference):
            self.assertEqual(outcome(result, "demo.tax.skc.constant")["value"], "7")


class V12Unchanged(unittest.TestCase):
    """A v12 rule keeps validating and running, in a v34 or a v35 package."""

    def test_v12_link_count_runs_in_both_package_versions(self) -> None:
        rule = _rule("demo.rule.skc.v12-link-count", subject=BOX1, joined=INCL, direction="joined_contains_subject",
                     publishes="demo.tax.skc.v12-link-count", value={"op": "link_count", "links": INCL},
                     schema="rule-artifact.v12")
        parts = [
            (_fact_type(BOX1, BOX_KEYS), "fact-type"),
            (_fact_type(INCL, INCL_KEYS, ["sli.statement-inclusion.affirmed"]), "fact-type"),
            (rule, "computation"),
        ]
        state, current = world([box("demo-stmt"), inclusion("demo-stmt", "demo-loan")])
        symbol = keyed("demo.tax.skc.v12-link-count", BOX1, box_keys("demo-stmt"))
        values = []
        for schema in ("artifact-package.v34", "artifact-package.v35"):
            package, validation = validate(parts, schema=schema)
            self.assertTrue(validation.ok, validation.issues)
            material = _resolved_run_material(_Graph(list(validation.resolved_members), package))
            rules, parameters, families, mappings, fact_types, bindings, collect_names = material
            ctx = marshal_run_context(
                run_id="demo.run.v12", state=state,  # type: ignore[arg-type]
                currency=CurrencyView(frozenset(current), frozenset(), frozenset(), frozenset()),
                rules=rules, parameters=parameters, canon={}, adoption_pin=ADOPTION_PIN,
                governance_pins=GOVERNANCE_PINS, family_declarations=families, closure_mappings=mappings,
                fact_types=fact_types, input_bindings=bindings, collect_source_names=collect_names,
                emission_only_source_names=list(material.emission_only_names),
            )
            forward, reference = both_runners(ctx)
            for result in (forward, reference):
                values.append(outcome(result, symbol)["value"])
        self.assertEqual(values, ["1", "1", "1", "1"])


class SharedKeyCountFromSavedLog(unittest.TestCase):
    """The real recorder writes the financing rows; a fresh ActLog recovers them."""

    def test_recovered_financing_rows_are_counted_and_withdrawal_drops_one(self) -> None:
        from packages.kernel.act_log import ActLog
        from packages.kernel.currency import compute_currency
        from packages.kernel.findings import project
        from packages.tax.sli_relationship_recording import (
            SCHOOLING,
            record_submission_durably,
            withdraw_relationship_claim_durably,
        )
        from tests.support import act, demo_entity
        from tests.test_sli_relationship_recording import OrdinaryRelationshipRecording, _append_source

        raw, log, registry, refs = OrdinaryRelationshipRecording()._workspace()
        with raw:
            for identity, label, kind in (
                ("demo.skc.period.spring25", "Spring 2025", "tax.us.educational-period"),
            ):
                revision = log.read().revision
                log.append(act(revision, "entity-introduced", {"entity": demo_entity(identity, label, kind)}),
                           expected_revision=revision)
            school_b = _append_source(
                log, registry, SCHOOLING,
                (("period", "demo.skc.period.spring25"), ("institution", "demo.track14.institution.river"),
                 ("programme", "demo.track14.programme.bsc")),
                "Riverside College, BSc, spring 2025", "school-b",
            )
            first = record_submission_durably(log, {
                "submission_id": "demo.skc.submission.first", "evidence_id": "demo.evidence.skc.first",
                "actor": "demo.user.filer", "at": "2026-10-02T12:00:00Z",
                "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
                "statement_fact_id": refs["statement"], "financing_response": "yes",
                "inclusion_response": "yes", "interest_portion_response": "unknown",
            }, registry)
            second = record_submission_durably(log, {
                "submission_id": "demo.skc.submission.second", "evidence_id": "demo.evidence.skc.second",
                "actor": "demo.user.filer", "at": "2026-10-02T12:01:00Z",
                "borrowing_ref": refs["borrowing"], "schooling_fact_id": school_b,
                "statement_fact_id": refs["statement"], "financing_response": "yes",
                "inclusion_response": "unanswered", "interest_portion_response": "unknown",
            }, registry)
            inclusion_id = first["claims"]["statement-inclusion"]["finding_id"]
            financing_ids = {first["claims"]["financing"]["finding_id"], second["claims"]["financing"]["finding_id"]}

            def recovered_count() -> tuple[list[Any], list[Any]]:
                fresh = ActLog(log.path.parent, registry)
                state = project(fresh.read().acts, registry)
                currency = compute_currency(state)
                parts = [p for p in chain_parts() if p[0]["id"] in {
                    BOX1, INCL, FIN, COUNT_RULE}]
                package, validation = validate(parts)
                self.assertTrue(validation.ok, validation.issues)
                material = _resolved_run_material(_Graph(list(validation.resolved_members), package))
                rules, parameters, families, mappings, fact_types, bindings, collect_names = material
                ctx = marshal_run_context(
                    run_id="demo.run.skc.saved", state=state, currency=currency, rules=rules,
                    parameters=parameters, canon={}, adoption_pin=ADOPTION_PIN, governance_pins=GOVERNANCE_PINS,
                    family_declarations=families, closure_mappings=mappings, fact_types=fact_types,
                    input_bindings=bindings, collect_source_names=collect_names,
                    emission_only_source_names=list(material.emission_only_names),
                )
                forward, reference = both_runners(ctx)
                inclusion_fact = state.findings[inclusion_id]["fact_id"]
                symbol = f"{COUNT}|{inclusion_fact}"
                return [outcome(forward, symbol), outcome(reference, symbol)], [symbol]

            before, _ = recovered_count()
            self.assertEqual(before[0], before[1])
            self.assertEqual(before[0]["value"], "2")
            self.assertEqual(inputs(before[0]["pins"]), financing_ids | {inclusion_id})

            withdraw_relationship_claim_durably(
                log, registry, finding_id=second["claims"]["financing"]["finding_id"],
                actor="demo.user.filer", at="2026-10-02T12:02:00Z",
            )
            after, _ = recovered_count()
            self.assertEqual(after[0], after[1])
            self.assertEqual(after[0]["value"], "1")
            self.assertEqual(inputs(after[0]["pins"]), {first["claims"]["financing"]["finding_id"], inclusion_id})


if __name__ == "__main__":
    unittest.main()
