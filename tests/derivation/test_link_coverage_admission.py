"""Track 4: reusable link admission and present-row joinability.

Option B (ADR 0075). The link type is emitted and is not a collect name.
Findings emitted only for that set are not marked used. The reduction name
is on neither list. Present link rows that share no key name with the
subject block before the no-link default. Zero rows still take it.
"""

from __future__ import annotations

import unittest
from decimal import Decimal
from typing import Any

from packages.derivation.evaluator import AccessLog, Environment, EvalBlocked, evaluate
from packages.derivation.live import _resolved_run_material
from tests.derivation.test_link_coverage_contract import (
    BOX1,
    LINKS,
    REDUCTIONS,
    SCOPE,
    SIBLING,
    _Graph,
    _base_parts,
    _coverage,
    _finding,
    _marshal,
    _reduction,
    _sibling_value,
    _validate,
)
from tests.derivation.test_link_coverage_runtime import _row, _run

FAMILY_ID = "demo.family.statement-links"


def _family() -> dict[str, Any]:
    return {
        "schema": "source-family.v1",
        "id": FAMILY_ID,
        "version": "v1",
        "title": "Demo statement links",
        "scope": dict(SCOPE),
        "closure_claim": "Every demo statement-to-borrowing link is recorded.",
        "member_predicate": {"fact_type": LINKS},
        "authorizes_subtotal": "demo.tax.statement-link-subtotal",
    }


def _box(value: str = "1500", statement: str = "demo-statement") -> Any:
    return _row(
        BOX1,
        f"demo.finding.box1.{statement}",
        (("lender", "demo-lender"), ("statement", statement), ("tax-year", "2025")),
        value,
        fact_id=f"demo.fact.box1.{statement}",
    )


def _dispatch(sources: list[Any]) -> Any:
    result, _package = _validate(_base_parts())
    if not result.ok:
        raise AssertionError(result.issues)
    rule = _coverage()
    prepared = _run([rule, _reduction()])
    prepared.live_sources = sources
    return prepared.evaluate_subject_scoped_rule(subject_type=BOX1, rule=rule)


class LinkCoverageAdmission(unittest.TestCase):
    """The names are usable. No other symbol's scalar binding moves."""

    def test_resolved_material_emits_the_link_type_and_registers_neither_name(self) -> None:
        result, package = _validate(_base_parts())
        self.assertTrue(result.ok, result.issues)
        material = _resolved_run_material(_Graph(result.resolved_members, package))
        collect_names = material[6]
        self.assertNotIn(LINKS, collect_names)
        self.assertNotIn(REDUCTIONS, collect_names)
        self.assertEqual(material.emission_only_names, (LINKS,))

    def test_sibling_may_name_the_link_type_and_the_package_validates(self) -> None:
        requires = _sibling_value({"op": "ref", "name": BOX1})
        requires["requires"] = [LINKS]
        requires["value"] = 0
        ref = _sibling_value({"op": "ref", "name": LINKS})
        ref["id"] = "demo.rule.sibling-ref"
        counted = _sibling_value({
            "op": "count",
            "name": LINKS,
            "source_set": "demo.family.unused",
        })
        counted["id"] = "demo.rule.sibling-count"
        collected = _sibling_value({
            "op": "collect",
            "name": LINKS,
            "source_set": FAMILY_ID,
        })
        collected["id"] = "demo.rule.sibling-collect"
        for rule, extra in (
            (requires, []),
            (ref, []),
            (counted, []),
            (collected, [(_family(), "source-family")]),
        ):
            with self.subTest(rule=rule["id"]):
                result, _package = _validate(
                    _base_parts() + extra + [(rule, "computation")],
                    entrypoints=[
                        {"id": "demo.rule.statement-box-minus-reductions", "version": "v2"},
                        {"id": rule["id"], "version": "v1"},
                    ],
                )
                self.assertTrue(result.ok, result.issues)
                self.assertNotIn("LINK_COVERAGE_NAME_REUSED", [issue.code for issue in result.issues])

    def test_link_type_binding_matches_an_uncollected_symbol(self) -> None:
        binding = [{
            "symbol": LINKS,
            "fact_type": {"id": LINKS, "version": "v1"},
            "mode": "required",
        }]
        one = _marshal([], binding, {
            "demo.finding.link.a": _finding("demo.finding.link.a", f"{LINKS}|statement=a", "10"),
        }, emission_only=[LINKS])
        bound = [item for item in one.inputs if item.symbol == LINKS]
        self.assertEqual([(item.finding_id, item.value) for item in bound], [("demo.finding.link.a", "10")])
        self.assertEqual([source.finding_id for source in one.sources if source.name == LINKS], ["demo.finding.link.a"])

        agreeing = _marshal([], binding, {
            "demo.finding.link.b": _finding("demo.finding.link.b", f"{LINKS}|statement=b", "10"),
            "demo.finding.link.a": _finding("demo.finding.link.a", f"{LINKS}|statement=a", "10"),
        }, emission_only=[LINKS])
        agreed = [item for item in agreeing.inputs if item.symbol == LINKS]
        self.assertEqual([(item.finding_id, item.value) for item in agreed], [("demo.finding.link.a", "10")])

        disagreeing = _marshal([], binding, {
            "demo.finding.link.b": _finding("demo.finding.link.b", f"{LINKS}|statement=b", "20"),
            "demo.finding.link.a": _finding("demo.finding.link.a", f"{LINKS}|statement=a", "10"),
        }, emission_only=[LINKS])
        self.assertEqual([item for item in disagreeing.inputs if item.symbol == LINKS], [])
        self.assertEqual(
            sorted(source.finding_id for source in disagreeing.sources if source.name == LINKS),
            ["demo.finding.link.a", "demo.finding.link.b"],
        )

    def test_sibling_scalar_is_unchanged(self) -> None:
        bindings = [{
            "symbol": SIBLING,
            "fact_type": {"id": SIBLING, "version": "v1"},
            "mode": "required",
        }]
        one = _marshal([], bindings, {
            "demo.finding.sibling.1": _finding("demo.finding.sibling.1", f"{SIBLING}|statement=a", "demo-one"),
            "demo.finding.link.1": _finding("demo.finding.link.1", f"{LINKS}|statement=a", "10"),
        }, emission_only=[LINKS])
        sibling = [item for item in one.inputs if item.symbol == SIBLING]
        self.assertEqual([(item.finding_id, item.value) for item in sibling], [("demo.finding.sibling.1", "demo-one")])
        self.assertEqual([item.symbol for item in one.inputs if item.symbol == LINKS], [])

        several = _marshal([], bindings, {
            "demo.finding.sibling.2": _finding("demo.finding.sibling.2", f"{SIBLING}|statement=b", "demo-agree"),
            "demo.finding.sibling.1": _finding("demo.finding.sibling.1", f"{SIBLING}|statement=a", "demo-agree"),
        }, emission_only=[LINKS])
        agreed = [item for item in several.inputs if item.symbol == SIBLING]
        self.assertEqual([(item.finding_id, item.value) for item in agreed], [("demo.finding.sibling.1", "demo-agree")])

    def test_ref_outside_dispatch_binds_when_values_agree_only(self) -> None:
        """Emission must not mark the link findings used, or this scalar is lost."""
        rule = _sibling_value({"op": "ref", "name": LINKS})
        agree = _marshal([], [], {
            "demo.finding.link.b": _finding("demo.finding.link.b", f"{LINKS}|statement=b", "10"),
            "demo.finding.link.a": _finding("demo.finding.link.a", f"{LINKS}|statement=a", "10"),
        }, emission_only=[LINKS], rules=[rule])
        bound = [item for item in agree.inputs if item.symbol == LINKS]
        self.assertEqual([(item.finding_id, item.value) for item in bound], [("demo.finding.link.a", "10")])

        one = _marshal([], [], {
            "demo.finding.link.a": _finding("demo.finding.link.a", f"{LINKS}|statement=a", "10"),
        }, emission_only=[LINKS], rules=[rule])
        self.assertEqual(
            [(item.finding_id, item.value) for item in one.inputs if item.symbol == LINKS],
            [("demo.finding.link.a", "10")],
        )

        disagree = _marshal([], [], {
            "demo.finding.link.b": _finding("demo.finding.link.b", f"{LINKS}|statement=b", "20"),
            "demo.finding.link.a": _finding("demo.finding.link.a", f"{LINKS}|statement=a", "10"),
        }, emission_only=[LINKS], rules=[rule])
        self.assertEqual([item for item in disagree.inputs if item.symbol == LINKS], [])

    def test_sibling_collect_returns_decimals_not_key_maps(self) -> None:
        numeric = _marshal([], [], {
            "demo.finding.link.a": _finding("demo.finding.link.a", f"{LINKS}|statement=a", "10"),
            "demo.finding.link.b": _finding("demo.finding.link.b", f"{LINKS}|statement=b", "20"),
        }, emission_only=[LINKS])
        rows = [source.value for source in numeric.sources if source.name == LINKS]
        self.assertEqual(rows, ["10", "20"])
        self.assertTrue(all(not isinstance(value, dict) for value in rows))
        collected = evaluate(
            {"op": "collect", "name": LINKS, "source_set": FAMILY_ID},
            Environment({}, {LINKS: rows}, frozenset({FAMILY_ID}), {}, {}),
            AccessLog(),
        )
        self.assertEqual(collected, [Decimal("10"), Decimal("20")])
        self.assertTrue(all(isinstance(value, Decimal) for value in collected))

        objected = _marshal([], [], {
            "demo.finding.link.obj": _finding(
                "demo.finding.link.obj", f"{LINKS}|statement=a", {"borrowing": "demo-b"},
            ),
        }, emission_only=[LINKS])
        object_rows = [source.value for source in objected.sources if source.name == LINKS]
        self.assertEqual(len(object_rows), 1)
        self.assertIsInstance(object_rows[0], str)
        self.assertNotIsInstance(object_rows[0], dict)
        with self.assertRaises(EvalBlocked) as caught:
            evaluate(
                {"op": "collect", "name": LINKS, "source_set": FAMILY_ID},
                Environment({}, {LINKS: object_rows}, frozenset({FAMILY_ID}), {}, {}),
                AccessLog(),
            )
        self.assertEqual(caught.exception.category, "DEPENDENCY_INVALID")
        self.assertTrue(any("not a number" in item for item in caught.exception.missing))


class LinkCoverageUnjoinable(unittest.TestCase):
    """Present rows that share no key name block. Zero rows take the default."""

    def test_zero_rows_take_the_default(self) -> None:
        result = _dispatch([_box()])
        self.assertEqual(result.blocked, ())
        self.assertEqual(result.publications[0]["value"], "1500")

    def test_present_unjoinable_rows_block_before_the_default(self) -> None:
        link = _row(LINKS, "demo.finding.link.borrow-only", (("borrowing", "demo-b"),), "10")
        result = _dispatch([_box(), link])
        self.assertEqual(result.publications, ())
        self.assertEqual(len(result.blocked), 1)
        self.assertEqual(result.blocked[0].code, "DEPENDENCY_INVALID")
        self.assertEqual(result.blocked[0].missing, ("link-coverage-unjoinable",))
        self.assertNotIn(
            "demo.param.no-link-reduction",
            {pin["id"] for pin in result.blocked[0].pins},
        )

    def test_shared_name_with_disagreeing_value_is_still_the_default(self) -> None:
        link = _row(
            LINKS,
            "demo.finding.link.other-statement",
            (
                ("lender", "demo-lender"),
                ("statement", "other-statement"),
                ("tax-year", "2025"),
                ("borrowing", "demo-b"),
            ),
            "10",
        )
        result = _dispatch([_box(), link])
        self.assertEqual(result.blocked, ())
        self.assertEqual(result.publications[0]["value"], "1500")

    def test_false_guard_stays_inapplicable(self) -> None:
        link = _row(LINKS, "demo.finding.link.borrow-only", (("borrowing", "demo-b"),), "10")
        result = _dispatch([_box("0"), link])
        self.assertEqual(result.blocked, ())
        self.assertEqual(len(result.inapplicable), 1)

    def test_joined_reduction_is_still_the_orphan(self) -> None:
        link = _row(LINKS, "demo.finding.link.borrow-only", (("borrowing", "demo-b"),), "10")
        reduction = _row(
            REDUCTIONS,
            "demo.finding.reduction.joined",
            (("lender", "demo-lender"), ("statement", "demo-statement"), ("tax-year", "2025")),
            "40",
        )
        result = _dispatch([_box(), link, reduction])
        self.assertEqual(result.publications, ())
        self.assertEqual(result.blocked[0].missing, ("demo.finding.reduction.joined",))

    def test_other_statement_with_a_disagreeing_shared_name_is_isolated(self) -> None:
        north = _box(statement="north")
        west = _box(statement="west")
        link = _row(LINKS, "demo.finding.link.north", _pair_for("north"), "10")
        result = _dispatch([west, north, link])
        self.assertEqual(len(result.publications), 1)
        self.assertEqual(result.publications[0]["value"], "1500")
        self.assertTrue(result.publications[0]["symbol"].endswith("|demo.fact.box1.west"))
        self.assertEqual(result.blocked[0].subject_fact_id, "demo.fact.box1.north")
        self.assertEqual(result.blocked[0].missing, ("demo.finding.link.north",))


def _pair_for(statement: str) -> tuple[tuple[str, str], ...]:
    return (
        ("lender", "demo-lender"),
        ("statement", statement),
        ("tax-year", "2025"),
        ("borrowing", "demo-b"),
    )


