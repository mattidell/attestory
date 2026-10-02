"""Track 3 stage B2: link_coverage runtime.

The node tests hand-assemble an Environment. Dispatch tests hand-assemble
a run and call evaluate_subject_scoped_rule; they do not establish a
durable reader. Rules that the obligations execute are the validated v10
worked example unless a test says otherwise.
"""

from __future__ import annotations

import unittest
from decimal import Decimal
from types import SimpleNamespace
from typing import Any, cast

from packages.derivation.authorization_closure import rule_scoped_closure
from packages.derivation.evaluator import (
    KEYS_UNAVAILABLE,
    LINK_COVERAGE_KEYS_UNAVAILABLE,
    LINK_COVERAGE_SCOPE_UNBOUND,
    AccessLog,
    Environment,
    EvalBlocked,
    evaluate,
)
from packages.derivation.loader import DerivationSchemas
from packages.derivation.marshal import marshal_run_context
from packages.derivation.runner import SourceFact, _Run
from packages.kernel.currency import CurrencyView
from tests.derivation.test_link_coverage_contract import (
    LINKS,
    PARAM_ID,
    REDUCTIONS,
    _base_parts,
    _citation,
    _coverage,
    _fact_type,
    _parameter,
    _reduction,
    _validate,
)

BOX1 = "demo.tax.f1098e.box1-student-loan-interest"
ADOPTION = {"role": "adoption", "id": "demo.package.link-coverage", "version": "v2"}
GOVERNANCE = [{"role": "governance", "id": "demo.governance.probe", "version": "v1"}]


def _node() -> dict[str, Any]:
    return cast(dict[str, Any], _coverage()["value"]["right"])


def _env(
    *,
    keyed: dict[str, Any] | None = None,
    sources: dict[str, list[str]] | None = None,
    parameters: dict[str, dict[str, Any]] | None = None,
) -> Environment:
    return Environment(
        {},
        sources or {},
        frozenset(),
        parameters if parameters is not None else {_parameter()["id"]: _parameter()},
        {},
        keyed_sources={} if keyed is None else keyed,
    )


def _row(
    name: str,
    finding_id: str,
    keys: tuple[tuple[str, str], ...] | None,
    value: Any,
    *,
    fact_id: str = "demo.fact.not-a-match-key",
) -> SourceFact:
    rendered = value if isinstance(value, str) else str(value)
    return SourceFact(
        name=name,
        value=rendered,
        finding_id=finding_id,
        fact_id=fact_id,
        keys=keys,
    )


def _pair(borrowing: str) -> tuple[tuple[str, str], ...]:
    return (
        ("lender", "demo-lender"),
        ("statement", "demo-statement"),
        ("tax-year", "2025"),
        ("borrowing", borrowing),
    )


class _State:
    def __init__(self, findings: dict[str, dict[str, Any]]) -> None:
        self.findings = findings
        self.horizon_state = type("Horizon", (), {"current_by_chain": {}})()


def _currency(finding_ids: list[str]) -> CurrencyView:
    return CurrencyView(
        current_finding_ids=frozenset(finding_ids),
        displaced_finding_ids=frozenset(),
        current_evidence_ids=frozenset(),
        displaced_evidence_ids=frozenset(),
    )


def _run(rules: list[dict[str, Any]]) -> _Run:
    ctx = marshal_run_context(
        run_id="demo.run.link-coverage-runtime",
        state=_State({}),  # type: ignore[arg-type]
        currency=_currency([]),
        rules=rules,
        parameters={PARAM_ID: _parameter()},
        canon={},
        adoption_pin=ADOPTION,
        governance_pins=GOVERNANCE,
        collect_source_names=[BOX1, LINKS, REDUCTIONS],
    )
    return _Run(ctx, DerivationSchemas())


class LinkCoverageArm(unittest.TestCase):
    """Section 3 checks and the three outcomes, on the node alone."""

    def test_unbound_slot_fail_closes_and_does_not_read_sources(self) -> None:
        access = AccessLog()
        env = _env(sources={LINKS: ["100"], REDUCTIONS: ["40"]})
        with self.assertRaises(EvalBlocked) as caught:
            evaluate(_node(), env, access)
        self.assertEqual(caught.exception.category, "DEPENDENCY_INVALID")
        self.assertEqual(caught.exception.missing, [LINK_COVERAGE_SCOPE_UNBOUND])
        self.assertEqual(access.collects, set())
        self.assertEqual(access.closure_reads, set())
        self.assertEqual(access.link_coverage_findings, set())
        self.assertEqual(access.parameters, set())

    def test_sentinel_on_either_name_is_not_the_default(self) -> None:
        for keyed in (
            {LINKS: KEYS_UNAVAILABLE, REDUCTIONS: []},
            {LINKS: [], REDUCTIONS: KEYS_UNAVAILABLE},
        ):
            with self.subTest(keyed=sorted(keyed)):
                with self.assertRaises(EvalBlocked) as caught:
                    evaluate(_node(), _env(keyed=keyed), AccessLog())
                self.assertEqual(caught.exception.category, "DEPENDENCY_INVALID")
                self.assertEqual(caught.exception.missing, [LINK_COVERAGE_KEYS_UNAVAILABLE])

    def test_unbound_is_reported_before_the_sentinel(self) -> None:
        keyed = {REDUCTIONS: KEYS_UNAVAILABLE}
        with self.assertRaises(EvalBlocked) as caught:
            evaluate(_node(), _env(keyed=keyed), AccessLog())
        self.assertEqual(caught.exception.missing, [LINK_COVERAGE_SCOPE_UNBOUND])

    def test_no_link_returns_the_parameter_and_pins_only_that(self) -> None:
        access = AccessLog()
        result = evaluate(
            _node(),
            _env(keyed={LINKS: [], REDUCTIONS: []}),
            access,
        )
        self.assertEqual(result, Decimal("0"))
        self.assertEqual(access.parameters, {PARAM_ID})
        self.assertEqual(access.link_coverage_findings, set())
        self.assertEqual(access.closure_reads, set())
        self.assertEqual(access.collects, set())

    def test_missing_parameter_is_absent_and_a_version_mismatch_is_invalid(self) -> None:
        keyed: dict[str, Any] = {LINKS: [], REDUCTIONS: []}
        with self.assertRaises(EvalBlocked) as missing:
            evaluate(_node(), _env(keyed=keyed, parameters={}), AccessLog())
        self.assertEqual(missing.exception.category, "DEPENDENCY_ABSENT")
        self.assertEqual(missing.exception.missing, [PARAM_ID])
        wrong = _parameter()
        wrong["version"] = "v2"
        with self.assertRaises(EvalBlocked) as mismatch:
            evaluate(_node(), _env(keyed=keyed, parameters={PARAM_ID: wrong}), AccessLog())
        self.assertEqual(mismatch.exception.category, "DEPENDENCY_INVALID")
        self.assertEqual(mismatch.exception.missing, [PARAM_ID])

    def test_covered_sum_pins_every_link_and_reduction_not_the_parameter(self) -> None:
        link_a = _row(LINKS, "demo.finding.link.a", _pair("a"), "200", fact_id="demo.fact.crossed.b")
        link_b = _row(LINKS, "demo.finding.link.b", _pair("b"), "900", fact_id="demo.fact.crossed.a")
        red_a = _row(REDUCTIONS, "demo.finding.reduction.a", _pair("a"), "200", fact_id="demo.fact.crossed.a")
        red_b = _row(REDUCTIONS, "demo.finding.reduction.b", _pair("b"), "300", fact_id="demo.fact.crossed.b")
        access = AccessLog()
        result = evaluate(
            _node(),
            _env(keyed={LINKS: [link_a, link_b], REDUCTIONS: [red_b, red_a]}),
            access,
        )
        self.assertEqual(result, Decimal("500"))
        self.assertEqual(
            access.link_coverage_findings,
            {
                "demo.finding.link.a",
                "demo.finding.link.b",
                "demo.finding.reduction.a",
                "demo.finding.reduction.b",
            },
        )
        self.assertEqual(access.parameters, set())

    def test_key_order_does_not_matter_and_a_narrower_map_is_an_orphan(self) -> None:
        forward = _pair("a")
        backward = tuple(reversed(forward))
        link = _row(LINKS, "demo.finding.link.a", forward, "1000")
        reduction = _row(REDUCTIONS, "demo.finding.reduction.a", backward, "40")
        result = evaluate(
            _node(),
            _env(keyed={LINKS: [link], REDUCTIONS: [reduction]}),
            AccessLog(),
        )
        self.assertEqual(result, Decimal("40"))

        narrow = _row(
            REDUCTIONS,
            "demo.finding.reduction.narrow",
            tuple(pair for pair in forward if pair[0] != "borrowing"),
            "40",
            fact_id=link.fact_id or "",
        )
        with self.assertRaises(EvalBlocked) as caught:
            evaluate(_node(), _env(keyed={LINKS: [link], REDUCTIONS: [narrow]}), AccessLog())
        self.assertEqual(caught.exception.missing, ["demo.finding.reduction.narrow"])
        self.assertNotIn("demo.finding.link.a", caught.exception.missing)

    def test_orphan_is_reported_before_an_uncovered_link(self) -> None:
        link = _row(LINKS, "demo.finding.link.a", _pair("a"), "1000")
        stale = _row(REDUCTIONS, "demo.finding.reduction.stale", _pair("z"), "40")
        with self.assertRaises(EvalBlocked) as caught:
            evaluate(_node(), _env(keyed={LINKS: [link], REDUCTIONS: [stale]}), AccessLog())
        self.assertEqual(caught.exception.missing, ["demo.finding.reduction.stale"])

    def test_duplicate_link_maps_name_both_links(self) -> None:
        first = _row(LINKS, "demo.finding.link.b", _pair("a"), "1")
        second = _row(LINKS, "demo.finding.link.a", _pair("a"), "1")
        with self.assertRaises(EvalBlocked) as caught:
            evaluate(_node(), _env(keyed={LINKS: [first, second], REDUCTIONS: []}), AccessLog())
        self.assertEqual(
            caught.exception.missing,
            ["demo.finding.link.a", "demo.finding.link.b"],
        )

    def test_two_reductions_for_one_link_name_the_link(self) -> None:
        link = _row(LINKS, "demo.finding.link.a", _pair("a"), "1000")
        one = _row(REDUCTIONS, "demo.finding.reduction.1", _pair("a"), "1")
        two = _row(REDUCTIONS, "demo.finding.reduction.2", _pair("a"), "2")
        with self.assertRaises(EvalBlocked) as caught:
            evaluate(_node(), _env(keyed={LINKS: [link], REDUCTIONS: [one, two]}), AccessLog())
        self.assertEqual(caught.exception.missing, ["demo.finding.link.a"])

    def test_non_numeric_names_the_link_and_does_not_coerce(self) -> None:
        for value in (True, "included", "true"):
            with self.subTest(value=value):
                link = _row(LINKS, "demo.finding.link.a", _pair("a"), "1000")
                reduction = SimpleNamespace(
                    name=REDUCTIONS,
                    value=value,
                    finding_id="demo.finding.reduction.a",
                    fact_id="demo.fact.not-a-match-key",
                    keys=_pair("a"),
                )
                access = AccessLog()
                with self.assertRaises(EvalBlocked) as caught:
                    evaluate(_node(), _env(keyed={LINKS: [link], REDUCTIONS: [reduction]}), access)
                self.assertEqual(caught.exception.category, "DEPENDENCY_INVALID")
                self.assertEqual(caught.exception.missing, ["demo.finding.link.a"])
                self.assertNotIn("0", caught.exception.missing)
                self.assertEqual(access.link_coverage_findings, set())

    def test_published_zero_covers(self) -> None:
        link = _row(LINKS, "demo.finding.link.a", _pair("a"), "1000")
        reduction = _row(REDUCTIONS, "demo.finding.reduction.a", _pair("a"), "0")
        access = AccessLog()
        result = evaluate(_node(), _env(keyed={LINKS: [link], REDUCTIONS: [reduction]}), access)
        self.assertEqual(result, Decimal("0"))
        self.assertEqual(
            access.link_coverage_findings,
            {"demo.finding.link.a", "demo.finding.reduction.a"},
        )

    def test_uncovered_link_pins_that_finding_and_not_the_parameter(self) -> None:
        covered = _row(LINKS, "demo.finding.link.covered", _pair("a"), "1000")
        uncovered = _row(LINKS, "demo.finding.link.uncovered", _pair("b"), "500")
        reduction = _row(REDUCTIONS, "demo.finding.reduction.covered", _pair("a"), "10")
        access = AccessLog()
        with self.assertRaises(EvalBlocked) as caught:
            evaluate(
                _node(),
                _env(keyed={LINKS: [uncovered, covered], REDUCTIONS: [reduction]}),
                access,
            )
        self.assertEqual(caught.exception.missing, ["demo.finding.link.uncovered"])
        self.assertEqual(access.link_coverage_findings, {"demo.finding.link.uncovered"})
        self.assertEqual(access.parameters, set())

    def test_ordinary_collect_and_count_are_unchanged(self) -> None:
        empty = Environment({}, {"demo.tax.link-reduction": []}, frozenset(), {}, {})
        with self.assertRaises(EvalBlocked) as collect_blocked:
            evaluate(
                {"op": "collect", "name": "demo.tax.link-reduction", "source_set": "demo.family.reductions"},
                empty,
                AccessLog(),
            )
        self.assertEqual(collect_blocked.exception.category, "SOURCE_SET_UNCLOSED")
        self.assertEqual(collect_blocked.exception.missing, ["demo.family.reductions"])
        with self.assertRaises(EvalBlocked) as count_blocked:
            evaluate(
                {"op": "count", "name": LINKS, "source_set": "demo.family.links"},
                Environment({}, {LINKS: ["1000", "500"]}, frozenset(), {}, {}),
                AccessLog(),
            )
        self.assertEqual(count_blocked.exception.category, "SOURCE_SET_UNCLOSED")
        self.assertEqual(count_blocked.exception.missing, ["demo.family.links"])
        present = evaluate(
            {"op": "collect", "name": REDUCTIONS},
            Environment({}, {REDUCTIONS: ["0"]}, frozenset({"demo.family.unused"}), {}, {}),
            AccessLog(),
        )
        self.assertEqual(present, [Decimal("0")])


class LinkCoverageDispatch(unittest.TestCase):
    """Per-subject slot installation. The run is hand-assembled."""

    def setUp(self) -> None:
        result, _package = _validate(_base_parts())
        self.assertTrue(result.ok, result.issues)
        self.rule = _coverage()
        self.prepared = _run([self.rule, _reduction()])

    def _dispatch(self, sources: list[SourceFact]) -> Any:
        self.prepared.live_sources = sources
        return self.prepared.evaluate_subject_scoped_rule(subject_type=BOX1, rule=self.rule)

    def _box(self) -> SourceFact:
        return _row(
            BOX1,
            "demo.finding.box1.runtime",
            (("lender", "demo-lender"), ("statement", "demo-statement"), ("tax-year", "2025")),
            "1500",
            fact_id="demo.fact.box1.runtime",
        )

    def test_no_link_source_installs_an_empty_slot_and_publishes_the_default(self) -> None:
        result = self._dispatch([self._box()])
        self.assertEqual(len(result.publications), 1)
        self.assertEqual(result.blocked, ())
        finding = result.publications[0]
        self.assertEqual(finding["value"], "1500")
        self.assertNotIn("resolved_input", finding)
        roles = {pin["role"] for pin in finding["pins"]}
        self.assertNotIn("package", roles)
        self.assertEqual(
            {pin["id"] for pin in finding["pins"] if pin["role"] == "parameter"},
            {PARAM_ID},
        )
        self.assertEqual(
            {pin["id"] for pin in finding["pins"] if pin["role"] == "input"},
            {"demo.finding.box1.runtime"},
        )

    def test_missing_keys_on_either_name_block_and_do_not_publish_the_default(self) -> None:
        box = self._box()
        keyed_link = _row(LINKS, "demo.finding.link.keyed", _pair("a"), "1000")
        unkeyed_link = _row(LINKS, "demo.finding.link.unkeyed", None, "1000")
        unkeyed_reduction = _row(REDUCTIONS, "demo.finding.reduction.unkeyed", None, "10")
        cases = (
            [box, unkeyed_link],
            [box, keyed_link, unkeyed_reduction],
        )
        for sources in cases:
            with self.subTest(sources=[source.finding_id for source in sources]):
                result = self._dispatch(sources)
                self.assertEqual(result.publications, ())
                self.assertEqual(len(result.blocked), 1)
                self.assertEqual(result.blocked[0].code, "DEPENDENCY_INVALID")
                self.assertEqual(result.blocked[0].missing, (LINK_COVERAGE_KEYS_UNAVAILABLE,))

    def test_covered_dispatch_pins_each_link_and_reduction(self) -> None:
        box = self._box()
        link_a = _row(LINKS, "demo.finding.link.a", _pair("a"), "1000", fact_id="demo.fact.crossed.b")
        link_b = _row(LINKS, "demo.finding.link.b", _pair("b"), "500", fact_id="demo.fact.crossed.a")
        red_a = _row(REDUCTIONS, "demo.finding.reduction.a", _pair("a"), "200", fact_id="demo.fact.crossed.a")
        red_b = _row(REDUCTIONS, "demo.finding.reduction.b", _pair("b"), "300", fact_id="demo.fact.crossed.b")
        result = self._dispatch([box, link_b, link_a, red_a, red_b])
        self.assertEqual(result.blocked, ())
        self.assertEqual(result.publications[0]["value"], "1000")
        inputs = [pin for pin in result.publications[0]["pins"] if pin["role"] == "input"]
        self.assertEqual(
            {pin["id"] for pin in inputs},
            {
                "demo.finding.box1.runtime",
                "demo.finding.link.a",
                "demo.finding.link.b",
                "demo.finding.reduction.a",
                "demo.finding.reduction.b",
            },
        )
        self.assertTrue(all(pin["origin"] == "assertion" and pin["version"] == "v1" for pin in inputs))
        self.assertFalse(any(pin["role"] == "parameter" for pin in result.publications[0]["pins"]))

    def test_uncovered_dispatch_names_and_pins_the_link(self) -> None:
        box = self._box()
        link = _row(LINKS, "demo.finding.link.only", _pair("a"), "1000")
        result = self._dispatch([box, link])
        self.assertEqual(result.publications, ())
        self.assertEqual(result.blocked[0].missing, ("demo.finding.link.only",))
        inputs = {pin["id"] for pin in result.blocked[0].pins if pin["role"] == "input"}
        self.assertIn("demo.finding.link.only", inputs)
        self.assertNotIn(PARAM_ID, {pin["id"] for pin in result.blocked[0].pins})

    def test_attempt_outside_dispatch_fail_closes_scope_unbound(self) -> None:
        self.prepared.symbols[BOX1] = 1500
        self.prepared.symbol_pin[BOX1] = ("demo.finding.box1.runtime", "v1", "input", "assertion")
        self.prepared.sources.setdefault(LINKS, []).append("100")
        self.prepared.sources.setdefault(REDUCTIONS, []).append("40")
        self.assertEqual(self.prepared.attempt(self.rule), "blocked")
        self.assertEqual(self.prepared.publications, [])
        row = self.prepared.dispositions[-1]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(row["missing"], [LINK_COVERAGE_SCOPE_UNBOUND])


class LinkCoverageAuthorization(unittest.TestCase):
    def test_closure_reaches_the_reduction_link_fact_type_parameter_and_bundle(self) -> None:
        result, _package = _validate(_base_parts())
        self.assertTrue(result.ok, result.issues)
        coverage = _coverage()
        reduction = _reduction()
        parameter = _parameter()
        fact = _fact_type(LINKS, "Demo statement to borrowing link")
        citation = _citation()
        bundle = {
            "schema": "bundle.v1",
            "id": "demo.bundle.link-facts",
            "version": "v1",
            "fact_types": [{"id": LINKS}],
        }
        other = {
            "schema": "bundle.v1",
            "id": "demo.bundle.other",
            "version": "v1",
            "fact_types": [{"id": "demo.tax.unrelated"}],
        }
        corpus: dict[str, dict[str, Any]] = {
            str(citizen["id"]): citizen
            for citizen in (coverage, reduction, parameter, fact, citation, bundle, other)
        }
        closure = rule_scoped_closure({coverage["id"]}, corpus)
        self.assertIn((coverage["id"], "v2"), closure)
        self.assertIn((reduction["id"], "v1"), closure)
        self.assertIn((fact["id"], "v1"), closure)
        self.assertIn((parameter["id"], "v1"), closure)
        self.assertIn((bundle["id"], "v1"), closure)
        self.assertIn((citation["id"], "v1"), closure)
        self.assertNotIn((other["id"], "v1"), closure)
