"""Does zero links alone produce the favourable conclusion or the responsibility?

HAND-DISPATCHED. Nothing in this module is a production schedule. Each case
calls ``_Run.evaluate_subject_scoped_rule`` in the chain's order. Synthetic
``demo.*`` identities only. Rules are ``rule-artifact.v10`` and the package is
accepted by ``validate_package`` before any dispatch.

The chain, per Form 1098-E statement (subject: its box-1 fact):

- count: ``link_coverage`` over statement-to-borrowing links with a presence
  marker. A stand-in for the proposed ``link_count``, which is not built.
- a statement-wide scope claim ("the loans on this statement paid for ..."),
  keyed on the statement plus the applied circumstance, classified by its own
  rule (subject: the claim) as 1 for an enumerated adverse use and 0 otherwise;
- adverse total: ``link_coverage`` over those claims and classifications, with
  a "no statement-scope claim" parameter of 0;
- the named conclusion "no enumerated adverse circumstance bears on the
  interest this statement reports": requires count and adverse total, and
  publishes only when both are 0;
- the statement amount (box 1 minus linked reductions, unchanged);
- three responsibility rules: require the conclusion and the amount, and read
  both in their guard (conclusion is the favourable token, amount > 0), because
  a pin records what a rule read, not what it listed in ``requires``.

The ``old`` responsibility shape (requires count and amount, guards count == 0)
is kept to show the defect the repair removes. No ``optional_default`` is
declared anywhere.
"""

from __future__ import annotations

import unittest
from decimal import Decimal, InvalidOperation
from typing import Any
from unittest.mock import patch

from packages.derivation.loader import DerivationSchemas
from packages.derivation.marshal import marshal_run_context
from packages.derivation.runner import SourceFact, _Run
from packages.derivation.subject_dispatch import DEPENDENCY_ABSENT, DEPENDENCY_INVALID, SubjectScopedResult
from packages.kernel.currency import CurrencyView
from tests.derivation.test_link_coverage_contract import (
    BOX1,
    LINKS,
    PARAM_ID,
    REDUCTIONS,
    SCOPE,
    _citation,
    _coverage,
    _fact_type,
    _parameter,
    _reduction,
    _validate,
)

MARKER = "demo.tax.link-presence-marker"
COUNT = "demo.tax.link-count"
CLAIMS = "demo.tax.statement-scope-use-of-proceeds"
ADVERSE_MARK = "demo.tax.statement-scope-adverse-mark"
ADVERSE_TOTAL = "demo.tax.statement-scope-adverse-total"
CONCLUSION = "demo.tax.no-enumerated-adverse-for-statement"
# Workaround, recorded as a gap: a keyed same-run publication carries no fact
# type downstream (``subject_dispatch._fact_type_of`` falls back to the symbol
# name), so the token type is given the symbol's own id.
CONCLUSION_TYPE = CONCLUSION
AMOUNT = "demo.tax.statement-facing-amount"
RESP_TYPE = "demo.tax.responsibility-token"
RESPONSIBILITIES = (
    "demo.tax.responsibility.eligible-institution",
    "demo.tax.responsibility.recognised-credential",
    "demo.tax.responsibility.half-time",
)
OLD_RESPONSIBILITY = "demo.tax.responsibility.old-shape"
NO_CLAIM_PARAM = "demo.param.no-statement-scope-claim"
ADOPTION = {"role": "adoption", "id": "demo.package.link-coverage", "version": "v2"}
GOVERNANCE = [{"role": "governance", "id": "demo.governance.probe", "version": "v1"}]

YEAR = "2025"
S1 = ("demo-lender-a", "demo-statement-1")
S2 = ("demo-lender-b", "demo-statement-2")
BOX_S1, BOX_S1_FINDING = "demo.fact.box1.s1", "demo.finding.box1.s1"
BOX_S2, BOX_S2_FINDING = "demo.fact.box1.s2", "demo.finding.box1.s2"


def _rule(
    rule_id: str,
    publishes: str,
    value: Any,
    *,
    requires: list[str] | None = None,
    when: Any = True,
    role: str = "computation",
) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v10",
        "id": rule_id,
        "version": "v1",
        "scope": dict(SCOPE),
        "role": role,
        "requires": list(requires or []),
        "pins": [],
        "when": when,
        "value": value,
        "publishes": publishes,
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
        "citations": [{"id": _citation()["id"], "version": "v1"}],
    }


def _eq_zero(name: str) -> dict[str, Any]:
    return {"op": "compare", "cmp": "eq", "left": {"op": "ref", "name": name}, "right": 0}


def _coverage_of(links: str, reductions: str, param: str) -> dict[str, Any]:
    return {
        "op": "link_coverage",
        "links": links,
        "reductions": reductions,
        "empty": {"parameter": {"id": param, "version": "v1"}},
    }


def _token(fact_type: str, value: str) -> dict[str, Any]:
    return {"op": "category_literal", "fact_type": {"id": fact_type, "version": "v1"}, "value": value}


RULES: dict[str, dict[str, Any]] = {
    "marker": _rule("demo.rule.link-presence-marker", MARKER, 1),
    "count": _rule("demo.rule.link-count", COUNT, _coverage_of(LINKS, MARKER, PARAM_ID)),
    "classify": _rule(
        "demo.rule.statement-scope-adverse-mark",
        ADVERSE_MARK,
        {
            "op": "choose",
            "when": {
                "op": "categorical_compare",
                "cmp": "eq",
                "left": {"op": "ref", "name": CLAIMS},
                "right": _token(CLAIMS, "vehicle"),
            },
            "then": 1,
            "else": 0,
        },
    ),
    "total": _rule(
        "demo.rule.statement-scope-adverse-total",
        ADVERSE_TOTAL,
        _coverage_of(CLAIMS, ADVERSE_MARK, NO_CLAIM_PARAM),
    ),
    "conclusion": _rule(
        "demo.rule.no-enumerated-adverse-for-statement",
        CONCLUSION,
        _token(CONCLUSION_TYPE, "no-enumerated-adverse"),
        requires=[COUNT, ADVERSE_TOTAL],
        when={"op": "all", "args": [_eq_zero(COUNT), _eq_zero(ADVERSE_TOTAL)]},
        role="applicability",
    ),
    "reduction": _reduction(),
    "amount": _coverage(),
    "old": _rule(
        "demo.rule.responsibility.old-shape",
        OLD_RESPONSIBILITY,
        _token(RESP_TYPE, "applies"),
        requires=[COUNT, AMOUNT],
        when=_eq_zero(COUNT),
        role="applicability",
    ),
}
for _symbol in RESPONSIBILITIES:
    RULES[_symbol] = _rule(
        "demo.rule." + _symbol.split(".", 2)[2],
        _symbol,
        _token(RESP_TYPE, "applies"),
        requires=[CONCLUSION, AMOUNT],
        # Pins record what a rule read, not what it required: the guard reads both.
        when={
            "op": "all",
            "args": [
                {
                    "op": "categorical_compare",
                    "cmp": "eq",
                    "left": {"op": "ref", "name": CONCLUSION},
                    "right": _token(CONCLUSION_TYPE, "no-enumerated-adverse"),
                },
                {"op": "compare", "cmp": "gt", "left": {"op": "ref", "name": AMOUNT}, "right": 0},
            ],
        },
        role="applicability",
    )

# (key into RULES, subject type), in chain order.
CHAIN: list[tuple[str, str]] = [
    ("marker", LINKS),
    ("count", BOX1),
    ("classify", CLAIMS),
    ("total", BOX1),
    ("conclusion", BOX1),
    ("reduction", LINKS),
    ("amount", BOX1),
    ("old", BOX1),
    *[(symbol, BOX1) for symbol in RESPONSIBILITIES],
]


def _enum_type(fact_id: str, values: list[str]) -> dict[str, Any]:
    fact = _fact_type(fact_id, fact_id)
    fact["value_schema"] = {"enum": values}
    return fact


def _no_claim_parameter() -> dict[str, Any]:
    param = _parameter()
    param["id"] = NO_CLAIM_PARAM
    return param


def _parts() -> list[tuple[dict[str, Any], str]]:
    parts: list[tuple[dict[str, Any], str]] = [
        (rule, "applicability" if rule["role"] == "applicability" else "computation") for rule in RULES.values()
    ]
    parts += [
        (_parameter(), "parameter"),
        (_no_claim_parameter(), "parameter"),
        (_fact_type(LINKS, "Demo statement to borrowing link"), "fact-type"),
        (_enum_type(CLAIMS, ["tuition", "vehicle"]), "fact-type"),
        (_enum_type(CONCLUSION_TYPE, ["no-enumerated-adverse"]), "fact-type"),
        (_enum_type(RESP_TYPE, ["applies"]), "fact-type"),
        (_citation(), "citation"),
    ]
    return parts


class _State:
    def __init__(self) -> None:
        self.findings: dict[str, dict[str, Any]] = {}
        self.horizon_state = type("Horizon", (), {"current_by_chain": {}})()


def _statement_keys(statement: tuple[str, str]) -> tuple[tuple[str, str], ...]:
    return (("lender", statement[0]), ("statement", statement[1]), ("tax-year", YEAR))


def _box(fact_id: str, finding_id: str, statement: tuple[str, str], value: str) -> SourceFact:
    return SourceFact(name=BOX1, value=value, finding_id=finding_id, fact_id=fact_id, keys=_statement_keys(statement))


def _claim(statement: tuple[str, str], circumstance: str, value: str) -> SourceFact:
    tag = f"{statement[1]}.{circumstance}"
    return SourceFact(
        name=CLAIMS,
        value=value,
        finding_id=f"demo.finding.scope-claim.{tag}",
        fact_id=f"demo.fact.scope-claim.{tag}",
        keys=_statement_keys(statement) + (("circumstance", circumstance),),
    )


def _drive(sources: list[SourceFact], *, skip: frozenset[str] = frozenset()) -> dict[str, SubjectScopedResult]:
    """HAND-DISPATCHED, in CHAIN order. No scheduler."""
    parts = _parts()
    validated, package = _validate(
        parts,
        bindings=[],
        entrypoints=[{"id": RULES[s]["id"], "version": "v1"} for s in (*RESPONSIBILITIES, "old")]
        + [{"id": CONCLUSION_TYPE, "version": "v1"}, {"id": RESP_TYPE, "version": "v1"}],
    )
    if not validated.ok:
        raise AssertionError(validated.issues)
    if package["input_bindings"] != []:
        raise AssertionError(package["input_bindings"])
    rules = [citizen for citizen, _role in parts if str(citizen.get("schema", "")).startswith("rule-artifact.")]
    fact_types = [citizen for citizen, _role in parts if citizen.get("schema") == "fact-type.v2"]
    ctx = marshal_run_context(
        run_id="demo.run.bare-statement-chain",
        state=_State(),  # type: ignore[arg-type]
        currency=CurrencyView(
            current_finding_ids=frozenset(),
            displaced_finding_ids=frozenset(),
            current_evidence_ids=frozenset(),
            displaced_evidence_ids=frozenset(),
        ),
        rules=rules,
        parameters={PARAM_ID: _parameter(), NO_CLAIM_PARAM: _no_claim_parameter()},
        canon={},
        adoption_pin=ADOPTION,
        governance_pins=GOVERNANCE,
        fact_types=fact_types,
        collect_source_names=[BOX1, LINKS, MARKER, REDUCTIONS, CLAIMS, ADVERSE_MARK],
    )
    prepared = _Run(ctx, DerivationSchemas())
    prepared.live_sources = list(sources)
    results: dict[str, SubjectScopedResult] = {}
    for key, subject_type in CHAIN:
        if key in skip:
            continue
        results[key] = prepared.evaluate_subject_scoped_rule(subject_type=subject_type, rule=RULES[key])
    return results


def _by_fact(result: SubjectScopedResult) -> dict[str, dict[str, Any]]:
    return {str(f["symbol"]).split("|", 1)[1]: f for f in result.publications}


def _inputs(finding: dict[str, Any]) -> set[str]:
    return {str(pin["id"]) for pin in finding["pins"] if pin["role"] == "input"}


def _blocked(result: SubjectScopedResult) -> dict[str, Any]:
    return {row.subject_fact_id: row for row in result.blocked}


def _base() -> list[SourceFact]:
    return [_box(BOX_S1, BOX_S1_FINDING, S1, "400"), _box(BOX_S2, BOX_S2_FINDING, S2, "700")]


class BareStatementChain(unittest.TestCase):
    def _assert_favourable(self, results: dict[str, SubjectScopedResult], fact_id: str, box_finding: str) -> None:
        conclusion = _by_fact(results["conclusion"])[fact_id]
        count = _by_fact(results["count"])[fact_id]
        total = _by_fact(results["total"])[fact_id]
        self.assertEqual(conclusion["value"], "no-enumerated-adverse")
        self.assertEqual(_inputs(conclusion), {box_finding, count["id"], total["id"]})
        # The basis is the conclusion itself: no parameter pin, no declared default.
        self.assertEqual([p for p in conclusion["pins"] if p["role"] == "parameter"], [])
        self.assertNotIn("declared_default", {p.get("origin") for p in conclusion["pins"]})
        amount = _by_fact(results["amount"])[fact_id]
        for symbol in RESPONSIBILITIES:
            resp = _by_fact(results[symbol])[fact_id]
            self.assertEqual(_inputs(resp), {box_finding, conclusion["id"], amount["id"]})

    def test_both_bare_no_claims_both_favourable(self) -> None:
        """HAND-DISPATCHED. No link and no scope claim: count 0, total 0 by the parameter."""
        results = _drive(_base())
        for fact_id, box_finding in ((BOX_S1, BOX_S1_FINDING), (BOX_S2, BOX_S2_FINDING)):
            total = _by_fact(results["total"])[fact_id]
            self.assertEqual(total["value"], "0")
            self.assertIn(NO_CLAIM_PARAM, {p["id"] for p in total["pins"] if p["role"] == "parameter"})
            self._assert_favourable(results, fact_id, box_finding)

    def test_adverse_statement_scope_claim_stops_conclusion_and_responsibilities(self) -> None:
        """HAND-DISPATCHED. The discriminating case: zero links, one adverse scope claim on S1."""
        car = _claim(S1, "vehicle-purchase", "vehicle")
        results = _drive(_base() + [car])

        self.assertEqual(_by_fact(results["count"])[BOX_S1]["value"], "0")
        total = _by_fact(results["total"])[BOX_S1]
        self.assertEqual(total["value"], "1")
        self.assertIn(car.finding_id, _inputs(total))

        # No favourable conclusion for S1: the guard is false, so inapplicable.
        self.assertNotIn(BOX_S1, _by_fact(results["conclusion"]))
        self.assertIn(BOX_S1, {row.subject_fact_id for row in results["conclusion"].inapplicable})

        # The responsibilities lapse: ordinary absence of the conclusion.
        for symbol in RESPONSIBILITIES:
            self.assertNotIn(BOX_S1, _by_fact(results[symbol]))
            row = _blocked(results[symbol])[BOX_S1]
            self.assertEqual(row.code, DEPENDENCY_ABSENT)
            self.assertEqual(list(row.missing), [CONCLUSION])

        # The defect the repair removes: the old shape publishes on zero links alone.
        self.assertIn(BOX_S1, _by_fact(results["old"]))

        # Recorded, not repaired here: the amount does not read the conclusion.
        self.assertEqual(_by_fact(results["amount"])[BOX_S1]["value"], "400")

        # S2 is untouched by S1's claim.
        self.assertNotIn(car.finding_id, _inputs(_by_fact(results["total"])[BOX_S2]))
        self._assert_favourable(results, BOX_S2, BOX_S2_FINDING)

    def test_other_statements_adverse_claim_does_not_change_this_one(self) -> None:
        """HAND-DISPATCHED. The claim is on S2; S1 publishes exactly as with no claim."""
        car = _claim(S2, "vehicle-purchase", "vehicle")
        with_claim = _drive(_base() + [car])
        without = _drive(_base())
        self.assertNotIn(BOX_S2, _by_fact(with_claim["conclusion"]))
        for key in ("count", "total", "conclusion", "amount", *RESPONSIBILITIES):
            self.assertEqual(_by_fact(with_claim[key])[BOX_S1], _by_fact(without[key])[BOX_S1], key)

    def test_non_adverse_scope_claim_is_examined_and_pinned(self) -> None:
        """HAND-DISPATCHED. A tuition claim is read, classified 0, and pinned by the total."""
        tuition = _claim(S1, "riverside-bsc", "tuition")
        results = _drive(_base() + [tuition])
        total = _by_fact(results["total"])[BOX_S1]
        self.assertEqual(total["value"], "0")
        self.assertIn(tuition.finding_id, _inputs(total))
        self.assertEqual([p for p in total["pins"] if p["role"] == "parameter"], [])
        self._assert_favourable(results, BOX_S1, BOX_S1_FINDING)

    def test_unclassified_scope_claim_fails_closed(self) -> None:
        """HAND-DISPATCHED. A claim with no classification is not read as not adverse."""
        car = _claim(S1, "vehicle-purchase", "vehicle")
        results = _drive(_base() + [car], skip=frozenset({"classify"}))
        row = _blocked(results["total"])[BOX_S1]
        self.assertEqual(row.code, DEPENDENCY_INVALID)
        self.assertNotIn(BOX_S1, _by_fact(results["conclusion"]))
        for symbol in RESPONSIBILITIES:
            self.assertNotIn(BOX_S1, _by_fact(results[symbol]))


# --- Why is the conclusion absent? -----------------------------------------
#
# REFERENCE CLASSIFICATION, not the projector (which is not built). It reads
# only this statement's own dispositions, looked up by the keyed symbol
# ``<publishes>|<statement fact id>``: never a downstream missing list, and
# never another statement's rows. Two axes, then the conclusion itself.


def _outcome(result: SubjectScopedResult | None, symbol: str) -> tuple[str, Any]:
    """published/inapplicable/blocked/not-computed for one keyed symbol."""
    if result is None:
        return ("not-computed", None)
    for finding in result.publications:
        if finding["symbol"] == symbol:
            return ("published", finding)
    for row in result.inapplicable:
        if row.symbol == symbol:
            return ("inapplicable", row)
    for blocked_row in result.blocked:
        if blocked_row.symbol == symbol:
            return ("blocked", blocked_row)
    return ("not-computed", None)


def _numeric_axis(kind: str, row: Any, zero: str, positive: str) -> str:
    """Reference display classification, not a new engine disposition."""
    if kind == "not-computed":
        return "not-computed"
    if kind != "published":
        # An inapplicable producer ran; it is not a missing producer.
        return "unresolved"
    try:
        value = Decimal(str(row["value"]))
    except (InvalidOperation, ValueError):
        return "unresolved"
    # These two producers promise non-negative counts of rows/classifications.
    if not value.is_finite() or value < 0 or value != value.to_integral_value():
        return "unresolved"
    return zero if value == 0 else positive


def _statement_outcome(results: dict[str, SubjectScopedResult], fact_id: str) -> dict[str, str]:
    count_kind, count = _outcome(results.get("count"), f"{COUNT}|{fact_id}")
    total_kind, total = _outcome(results.get("total"), f"{ADVERSE_TOTAL}|{fact_id}")
    conclusion_kind, _row = _outcome(results.get("conclusion"), f"{CONCLUSION}|{fact_id}")
    route = _numeric_axis(count_kind, count, "bare", "linked")
    scope = _numeric_axis(total_kind, total, "none-adverse", "adverse-established")
    return {"route": route, "statement_scope": scope, "conclusion": conclusion_kind}


class WhyTheConclusionIsAbsent(unittest.TestCase):
    """HAND-DISPATCHED. Four causes, one downstream symptom, four distinct outcomes."""

    def _link_sources(self) -> list[SourceFact]:
        keys = _statement_keys(S1) + (("borrowing", "demo-borrowing-x"),)
        link = SourceFact(name=LINKS, value="100", finding_id="demo.finding.link.x", fact_id="demo.fact.link.x", keys=keys)
        return [link]

    def _scenarios(self) -> dict[str, dict[str, SubjectScopedResult]]:
        car = _claim(S1, "vehicle-purchase", "vehicle")
        return {
            "adverse-established": _drive(_base() + [car]),
            "unresolved-classification": _drive(_base() + [car], skip=frozenset({"classify"})),
            "missing-producer": _drive(_base(), skip=frozenset({"count"})),
            "linked-route": _drive(_base() + self._link_sources()),
        }

    def test_downstream_symptom_is_identical_and_the_amount_still_publishes(self) -> None:
        symptoms = set()
        for name, results in self._scenarios().items():
            for symbol in RESPONSIBILITIES:
                row = _blocked(results[symbol])[BOX_S1]
                symptoms.add((row.code, tuple(row.missing)))
            self.assertIn(BOX_S1, _by_fact(results["amount"]), name)
        self.assertEqual(symptoms, {(DEPENDENCY_ABSENT, (CONCLUSION,))})

    def test_upstream_outcomes_distinguish_the_four_causes(self) -> None:
        got = {name: _statement_outcome(results, BOX_S1) for name, results in self._scenarios().items()}
        self.assertEqual(
            got,
            {
                "adverse-established": {"route": "bare", "statement_scope": "adverse-established", "conclusion": "inapplicable"},
                "unresolved-classification": {"route": "bare", "statement_scope": "unresolved", "conclusion": "blocked"},
                "missing-producer": {"route": "not-computed", "statement_scope": "none-adverse", "conclusion": "blocked"},
                "linked-route": {"route": "linked", "statement_scope": "none-adverse", "conclusion": "inapplicable"},
            },
        )
        baseline = _statement_outcome(_drive(_base()), BOX_S1)
        self.assertEqual(baseline, {"route": "bare", "statement_scope": "none-adverse", "conclusion": "published"})

    def test_each_cause_names_its_own_evidence(self) -> None:
        scenarios = self._scenarios()
        car_id = _claim(S1, "vehicle-purchase", "vehicle").finding_id

        adverse = scenarios["adverse-established"]
        total = _by_fact(adverse["total"])[BOX_S1]
        self.assertEqual(total["value"], "1")
        self.assertIn(car_id, _inputs(total))
        marks = _by_fact(adverse["classify"])
        self.assertEqual([f["value"] for f in marks.values()], ["1"])

        unresolved = scenarios["unresolved-classification"]
        row = _blocked(unresolved["total"])[BOX_S1]
        self.assertEqual(row.code, DEPENDENCY_INVALID)
        self.assertIn(car_id, row.missing)
        self.assertEqual(list(_blocked(unresolved["conclusion"])[BOX_S1].missing), [ADVERSE_TOTAL])

        missing = scenarios["missing-producer"]
        self.assertNotIn("count", missing)
        self.assertEqual(list(_blocked(missing["conclusion"])[BOX_S1].missing), [COUNT])

        linked = scenarios["linked-route"]
        self.assertEqual(_by_fact(linked["count"])[BOX_S1]["value"], "1")
        amount = _by_fact(linked["amount"])[BOX_S1]
        self.assertEqual(amount["value"], "300")
        self.assertIn("demo.finding.link.x", _inputs(amount))

    def test_the_unrelated_statement_is_unchanged_in_every_case(self) -> None:
        baseline = _drive(_base())
        for name, results in self._scenarios().items():
            if name == "missing-producer":
                # The count rule did not run for anyone; S2 shows the same cause.
                self.assertEqual(_statement_outcome(results, BOX_S2)["route"], "not-computed")
                continue
            for key in ("count", "total", "conclusion", "amount", *RESPONSIBILITIES):
                self.assertEqual(_by_fact(results[key])[BOX_S2], _by_fact(baseline[key])[BOX_S2], (name, key))

    def test_duplicate_and_nonnumeric_classifications_have_identical_block_evidence(self) -> None:
        claim = _claim(S1, "vehicle-purchase", "vehicle")
        rows = {}
        for name, values in (("absent", []), ("duplicate", ["1", "1"]), ("nonnumeric", ["not-a-number"])):
            marks = [
                SourceFact(
                    name=ADVERSE_MARK, value=value,
                    finding_id=f"demo.finding.injected-mark.{index}",
                    fact_id=f"demo.fact.injected-mark.{index}", keys=claim.keys,
                )
                for index, value in enumerate(values)
            ]
            # Synthetic malformed sources test the real coverage consumer, not
            # the valid classifier's ability to emit these malformed values.
            results = _drive(_base() + [claim] + marks, skip=frozenset({"classify"}))
            rows[name] = _blocked(results["total"])[BOX_S1]
            self.assertEqual(rows[name].code, DEPENDENCY_INVALID)
            self.assertEqual(rows[name].missing, (claim.finding_id,))
            self.assertEqual(_statement_outcome(results, BOX_S1)["statement_scope"], "unresolved")
            self.assertEqual(_blocked(results["conclusion"])[BOX_S1].missing, (ADVERSE_TOTAL,))
        # Even code + missing + pins cannot discriminate these two causes.
        self.assertEqual(rows["duplicate"], rows["nonnumeric"])
        self.assertIn(claim.finding_id, {pin["id"] for pin in rows["absent"].pins})

    def test_inapplicable_count_is_not_reported_as_a_producer_that_did_not_run(self) -> None:
        with patch.dict(RULES, {"count": {**RULES["count"], "when": False}}):
            results = _drive(_base())
        kind, _row = _outcome(results["count"], f"{COUNT}|{BOX_S1}")
        self.assertEqual(kind, "inapplicable")
        self.assertEqual(_statement_outcome(results, BOX_S1)["route"], "unresolved")

    def test_linked_route_can_coexist_with_an_unresolved_scope_and_blocked_conclusion(self) -> None:
        claim = _claim(S1, "vehicle-purchase", "vehicle")
        results = _drive(_base() + self._link_sources() + [claim], skip=frozenset({"classify"}))
        self.assertEqual(
            _statement_outcome(results, BOX_S1),
            {"route": "linked", "statement_scope": "unresolved", "conclusion": "blocked"},
        )
        self.assertEqual(_blocked(results["conclusion"])[BOX_S1].missing, (ADVERSE_TOTAL,))

    def test_missing_total_is_distinct_from_a_total_that_blocked(self) -> None:
        results = _drive(_base(), skip=frozenset({"total"}))
        self.assertEqual(_statement_outcome(results, BOX_S1)["statement_scope"], "not-computed")
        self.assertEqual(_blocked(results["conclusion"])[BOX_S1].missing, (ADVERSE_TOTAL,))

    def test_published_conclusion_does_not_prove_a_responsibility_published(self) -> None:
        symbol = RESPONSIBILITIES[0]
        missing = "demo.tax.missing-responsibility-input"
        with patch.dict(RULES, {symbol: {**RULES[symbol], "requires": [CONCLUSION, AMOUNT, missing]}}):
            results = _drive(_base())
        self.assertEqual(_statement_outcome(results, BOX_S1)["conclusion"], "published")
        self.assertEqual(_blocked(results[symbol])[BOX_S1].missing, (missing,))
        self.assertNotIn(BOX_S1, _by_fact(results[symbol]))

    def test_numeric_axis_uses_numeric_meaning_not_string_format(self) -> None:
        # Reference-classifier unit test only: no claim of new runtime cases.
        for value in ("0", "0.0", "0.00"):
            self.assertEqual(_numeric_axis("published", {"value": value}, "bare", "linked"), "bare")
        for value in ("-1", "0.5", "NaN", "Infinity", "not-a-number"):
            self.assertEqual(_numeric_axis("published", {"value": value}, "bare", "linked"), "unresolved")

    def test_sharing_a_source_pin_does_not_make_a_calculation_a_responsibility(self) -> None:
        results = _drive(_base())
        amount = _by_fact(results["amount"])[BOX_S1]
        count = _by_fact(results["count"])[BOX_S1]
        total = _by_fact(results["total"])[BOX_S1]
        self.assertIn(BOX_S1_FINDING, _inputs(amount))
        for calculation in (count, total):
            self.assertIn(BOX_S1_FINDING, _inputs(calculation))
            self.assertNotIn(amount["id"], _inputs(calculation))
        for symbol in RESPONSIBILITIES:
            self.assertIn(amount["id"], _inputs(_by_fact(results[symbol])[BOX_S1]))
        # A synthetic extra consumer can read the amount without declaring any
        # responsibility wording. Pin reach alone would select it too.
        amount_guard = {"op": "compare", "cmp": "gt", "left": {"op": "ref", "name": AMOUNT}, "right": 0}
        with patch.dict(RULES, {"old": {**RULES["old"], "when": amount_guard}}):
            extra = _drive(_base())
        self.assertIn(amount["id"], _inputs(_by_fact(extra["old"])[BOX_S1]))


if __name__ == "__main__":
    unittest.main()
