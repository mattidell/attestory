"""Is ``count == 0`` an executable bare-statement selection?

HAND-DISPATCHED. Nothing in this module is a production schedule. Each case
calls ``_Run.evaluate_subject_scoped_rule`` in order: the presence marker
(subject: the link type), the count (subject: box 1), then the bare-statement
rule (subject: box 1). Synthetic ``demo.*`` identities only. No production
citizen is imported from content.

The count rule is ``rule-artifact.v10``. Its value is one ``link_coverage``.
The bare rule ``requires`` the count symbol, guards ``count == 0``, and
publishes a categorical token. Packages are accepted by ``validate_package``
before any dispatch. The bare rule declares no ``optional_default``.
"""

from __future__ import annotations

import unittest
from typing import Any

from packages.derivation.evaluator import LINK_COVERAGE_KEYS_UNAVAILABLE
from packages.derivation.loader import DerivationSchemas
from packages.derivation.marshal import marshal_run_context
from packages.derivation.runner import SourceFact, _Run
from packages.derivation.subject_dispatch import (
    DEPENDENCY_ABSENT,
    DEPENDENCY_INVALID,
    LINK_COVERAGE_UNJOINABLE,
    SubjectScopedResult,
)
from packages.kernel.currency import CurrencyView
from tests.derivation.test_link_coverage_contract import (
    LINKS,
    PARAM_ID,
    SCOPE,
    _citation,
    _fact_type,
    _parameter,
    _validate,
)

BOX1 = "demo.tax.f1098e.box1-student-loan-interest"
MARKER = "demo.tax.link-presence-marker"
COUNT = "demo.tax.link-presence-count"
BARE = "demo.tax.bare-statement"
TOKEN_TYPE = "demo.tax.bare-statement-token"
TOKEN = "demo-bare-statement"
MARKER_RULE = "demo.rule.link-presence-marker"
COUNT_RULE = "demo.rule.link-presence-count"
BARE_RULE = "demo.rule.bare-statement"
PREREQ = "demo.tax.marker-prerequisite"
BOX_FINDING = "demo.finding.box1.probe"
BOX_FACT = "demo.fact.box1.probe"
LINK_FINDING = "demo.finding.link.probe"
LINK_FACT = "demo.fact.link.probe"
ADOPTION = {"role": "adoption", "id": "demo.package.link-coverage", "version": "v2"}
GOVERNANCE = [{"role": "governance", "id": "demo.governance.probe", "version": "v1"}]

# HAND-DISPATCHED. The guard is the count's value. No node reads a pin.
_GUARD: dict[str, Any] = {
    "op": "compare",
    "cmp": "eq",
    "left": {"op": "ref", "name": COUNT},
    "right": 0,
}
_TOKEN: dict[str, Any] = {
    "op": "category_literal",
    "fact_type": {"id": TOKEN_TYPE, "version": "v1"},
    "value": TOKEN,
}


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


def _rule(
    *,
    rule_id: str,
    publishes: str,
    value: Any,
    when: Any = True,
    requires: list[str] | None = None,
    role: str = "computation",
) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v10",
        "id": rule_id,
        "version": "v1",
        "scope": dict(SCOPE),
        "role": role,
        "requires": [] if requires is None else list(requires),
        "pins": [],
        "when": when,
        "value": value,
        "publishes": publishes,
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
        "citations": [{"id": _citation()["id"], "version": "v1"}],
    }


def _marker(
    *,
    value: Any = 1,
    when: Any = True,
    requires: list[str] | None = None,
) -> dict[str, Any]:
    return _rule(
        rule_id=MARKER_RULE,
        publishes=MARKER,
        value=value,
        when=when,
        requires=requires,
    )


def _count() -> dict[str, Any]:
    return _rule(
        rule_id=COUNT_RULE,
        publishes=COUNT,
        value={
            "op": "link_coverage",
            "links": LINKS,
            "reductions": MARKER,
            "empty": {"parameter": {"id": PARAM_ID, "version": "v1"}},
        },
    )


def _bare() -> dict[str, Any]:
    """Requires the count symbol. No optional default. Guard is the value."""
    return _rule(
        rule_id=BARE_RULE,
        publishes=BARE,
        role="applicability",
        requires=[COUNT],
        when=_GUARD,
        value=_TOKEN,
    )


def _token_type() -> dict[str, Any]:
    fact = _fact_type(TOKEN_TYPE, "Demo bare statement token")
    fact["value_schema"] = {"enum": [TOKEN]}
    return fact


def _parts(
    marker: dict[str, Any] | None = None,
) -> list[tuple[dict[str, Any], str]]:
    return [
        (marker if marker is not None else _marker(), "computation"),
        (_count(), "computation"),
        (_bare(), "applicability"),
        (_parameter(), "parameter"),
        (_fact_type(LINKS, "Demo statement to borrowing link"), "fact-type"),
        (_token_type(), "fact-type"),
        (_citation(), "citation"),
    ]


def _ids(pins: list[dict[str, Any]], role: str) -> list[str]:
    return sorted(str(pin["id"]) for pin in pins if pin.get("role") == role)


def _row(
    name: str,
    finding_id: str,
    keys: tuple[tuple[str, str], ...] | None,
    value: str,
    *,
    fact_id: str,
) -> SourceFact:
    return SourceFact(
        name=name,
        value=value,
        finding_id=finding_id,
        fact_id=fact_id,
        keys=keys,
    )


def _box(
    *,
    keys: tuple[tuple[str, str], ...] | None = (
        ("lender", "demo-lender"),
        ("statement", "demo-statement"),
        ("tax-year", "2025"),
    ),
    finding_id: str = BOX_FINDING,
    fact_id: str = BOX_FACT,
) -> SourceFact:
    return _row(BOX1, finding_id, keys, "1500", fact_id=fact_id)


def _link(
    borrowing: str,
    value: str = "1000",
    *,
    finding_id: str = LINK_FINDING,
    fact_id: str = LINK_FACT,
    keys: tuple[tuple[str, str], ...] | None = None,
) -> SourceFact:
    if keys is None:
        keys = (
            ("lender", "demo-lender"),
            ("statement", "demo-statement"),
            ("tax-year", "2025"),
            ("borrowing", borrowing),
        )
    return _row(LINKS, finding_id, keys, value, fact_id=fact_id)


def _drive(
    sources: list[SourceFact],
    *,
    marker: dict[str, Any] | None = None,
    run_marker: bool = True,
    run_count: bool = True,
) -> tuple[SubjectScopedResult | None, SubjectScopedResult | None, SubjectScopedResult]:
    """HAND-DISPATCHED. Marker, then count, then the bare rule. No scheduler."""
    parts = _parts(marker)
    validated, package = _validate(
        parts,
        bindings=[],
        entrypoints=[
            {"id": BARE_RULE, "version": "v1"},
            {"id": TOKEN_TYPE, "version": "v1"},
        ],
    )
    if not validated.ok:
        raise AssertionError(validated.issues)
    if package["input_bindings"] != []:
        raise AssertionError(package["input_bindings"])
    rules = [citizen for citizen, _role in parts if str(citizen.get("schema", "")).startswith("rule-artifact.")]
    fact_types = [citizen for citizen, _role in parts if citizen.get("schema") == "fact-type.v2"]
    ctx = marshal_run_context(
        run_id="demo.run.bare-statement-selection",
        state=_State({}),  # type: ignore[arg-type]
        currency=_currency([]),
        rules=rules,
        parameters={PARAM_ID: _parameter()},
        canon={},
        adoption_pin=ADOPTION,
        governance_pins=GOVERNANCE,
        fact_types=fact_types,
        collect_source_names=[BOX1, LINKS, MARKER, COUNT],
    )
    prepared = _Run(ctx, DerivationSchemas())
    prepared.live_sources = list(sources)
    by_id = {str(rule["id"]): rule for rule in rules}
    marker_result: SubjectScopedResult | None = None
    count_result: SubjectScopedResult | None = None
    if run_marker:
        marker_result = prepared.evaluate_subject_scoped_rule(
            subject_type=LINKS, rule=by_id[MARKER_RULE]
        )
    if run_count:
        count_result = prepared.evaluate_subject_scoped_rule(
            subject_type=BOX1, rule=by_id[COUNT_RULE]
        )
    bare_result: SubjectScopedResult = prepared.evaluate_subject_scoped_rule(
        subject_type=BOX1, rule=by_id[BARE_RULE]
    )
    return marker_result, count_result, bare_result


class BareStatementSelectionProbe(unittest.TestCase):
    """Eight hand-dispatched cases. The question is whether the bare rule publishes."""

    def _published(self, result: SubjectScopedResult | None) -> dict[str, Any]:
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.blocked, ())
        self.assertEqual(result.inapplicable, ())
        self.assertEqual(len(result.publications), 1)
        return result.publications[0]

    def test_01_no_link_parameter_zero_publishes(self) -> None:
        """HAND-DISPATCHED. No link. Count is the parameter. Bare rule publishes."""
        marker, count, bare = _drive([_box()])
        assert marker is not None and count is not None
        self.assertEqual(marker.publications, ())
        self.assertEqual(marker.blocked, ())
        finding = self._published(count)
        self.assertEqual(finding["value"], "0")
        self.assertEqual(_ids(finding["pins"], "parameter"), [PARAM_ID])
        self.assertEqual(_ids(finding["pins"], "input"), [BOX_FINDING])
        parameter = next(pin for pin in finding["pins"] if pin["role"] == "parameter")
        self.assertNotIn("origin", parameter)
        published = self._published(bare)
        self.assertEqual(published["value"], TOKEN)
        self.assertIn(finding["id"], _ids(published["pins"], "input"))
        self.assertNotIn(PARAM_ID, _ids(published["pins"], "parameter"))

    def test_02_one_marker_does_not_publish(self) -> None:
        """HAND-DISPATCHED. One link, marker 1. Count is 1. Bare rule does not publish."""
        link = _link("demo-borrowing-a")
        marker, count, bare = _drive([_box(), link])
        assert marker is not None and count is not None
        marked = self._published(marker)
        self.assertEqual(marked["value"], "1")
        finding = self._published(count)
        self.assertEqual(finding["value"], "1")
        self.assertEqual(_ids(finding["pins"], "parameter"), [])
        self.assertEqual(
            _ids(finding["pins"], "input"),
            sorted([BOX_FINDING, link.finding_id, marked["id"]]),
        )
        self.assertEqual(bare.publications, ())
        self.assertEqual(bare.blocked, ())
        self.assertEqual(len(bare.inapplicable), 1)

    def test_03_blocked_marker_does_not_publish(self) -> None:
        """HAND-DISPATCHED. Marker requires an absent symbol. Count blocks. Bare rule does not publish."""
        link = _link("demo-borrowing-a")
        marker, count, bare = _drive(
            [_box(), link],
            marker=_marker(requires=[PREREQ]),
        )
        assert marker is not None and count is not None
        self.assertEqual(marker.publications, ())
        self.assertEqual(len(marker.blocked), 1)
        self.assertEqual(marker.blocked[0].code, DEPENDENCY_ABSENT)
        self.assertEqual(marker.blocked[0].missing, (PREREQ,))
        self.assertEqual(count.publications, ())
        self.assertEqual(count.blocked[0].code, DEPENDENCY_INVALID)
        self.assertEqual(count.blocked[0].missing, (link.finding_id,))
        self.assertEqual(bare.publications, ())
        self.assertEqual(bare.blocked[0].code, DEPENDENCY_ABSENT)
        self.assertEqual(bare.blocked[0].missing, (COUNT,))

    def test_04_missing_marker_does_not_publish(self) -> None:
        """HAND-DISPATCHED. Marker inapplicable, and marker not run. Both block the count."""
        link = _link("demo-borrowing-a")
        sources = [_box(), link]
        held, count, bare = _drive(sources, marker=_marker(when=False))
        assert held is not None and count is not None
        self.assertEqual(held.publications, ())
        self.assertEqual(held.blocked, ())
        self.assertEqual(len(held.inapplicable), 1)
        self.assertEqual(count.publications, ())
        self.assertEqual(count.blocked[0].code, DEPENDENCY_INVALID)
        self.assertEqual(count.blocked[0].missing, (link.finding_id,))
        self.assertEqual(bare.publications, ())
        self.assertEqual(bare.blocked[0].code, DEPENDENCY_ABSENT)
        self.assertEqual(bare.blocked[0].missing, (COUNT,))

        skipped, uncovered, absent = _drive(sources, run_marker=False)
        self.assertIsNone(skipped)
        assert uncovered is not None
        self.assertEqual(uncovered.publications, ())
        self.assertEqual(uncovered.blocked[0].code, DEPENDENCY_INVALID)
        self.assertEqual(uncovered.blocked[0].missing, (link.finding_id,))
        self.assertEqual(absent.publications, ())
        self.assertEqual(absent.blocked[0].code, DEPENDENCY_ABSENT)
        self.assertEqual(absent.blocked[0].missing, (COUNT,))

    def test_05_marker_zero_publishes_on_the_sum(self) -> None:
        """HAND-DISPATCHED. Marker value 0. Count is 0 by the sum. Bare rule publishes."""
        link = _link("demo-borrowing-a")
        marker, count, bare = _drive([_box(), link], marker=_marker(value=0))
        assert marker is not None and count is not None
        marked = self._published(marker)
        self.assertEqual(marked["value"], "0")
        finding = self._published(count)
        self.assertEqual(finding["value"], "0")
        self.assertEqual(_ids(finding["pins"], "parameter"), [])
        self.assertIn(link.finding_id, _ids(finding["pins"], "input"))
        self.assertIn(marked["id"], _ids(finding["pins"], "input"))
        published = self._published(bare)
        self.assertEqual(published["value"], TOKEN)
        self.assertNotIn(PARAM_ID, {pin["id"] for pin in published["pins"]})
        self.assertNotIn(link.finding_id, {pin["id"] for pin in published["pins"]})
        self.assertNotIn(marked["id"], {pin["id"] for pin in published["pins"]})
        self.assertIn(finding["id"], _ids(published["pins"], "input"))

    def test_06_cancelling_markers_publish_on_the_sum(self) -> None:
        """HAND-DISPATCHED. Markers 1 and -1. Count is 0 by the sum. Bare rule publishes.

        The marker value is ``1 - link``. Link values are 0 and 2, so a sum of
        the link rows would be 2. The count is the marker sum.
        """
        first = _link("demo-borrowing-a", "0", finding_id="demo.finding.link.a", fact_id="demo.fact.link.a")
        second = _link("demo-borrowing-b", "2", finding_id="demo.finding.link.b", fact_id="demo.fact.link.b")
        marker_rule = _marker(value={
            "op": "subtract",
            "left": 1,
            "right": {"op": "ref", "name": LINKS},
        })
        marker, count, bare = _drive([_box(), second, first], marker=marker_rule)
        assert marker is not None and count is not None
        self.assertEqual(marker.blocked, ())
        self.assertEqual(sorted(item["value"] for item in marker.publications), ["-1", "1"])
        finding = self._published(count)
        self.assertEqual(finding["value"], "0")
        self.assertEqual(_ids(finding["pins"], "parameter"), [])
        inputs = set(_ids(finding["pins"], "input"))
        self.assertIn(first.finding_id, inputs)
        self.assertIn(second.finding_id, inputs)
        self.assertTrue({item["id"] for item in marker.publications} <= inputs)
        published = self._published(bare)
        self.assertEqual(published["value"], TOKEN)
        bare_ids = {pin["id"] for pin in published["pins"]}
        self.assertNotIn(PARAM_ID, bare_ids)
        self.assertNotIn(first.finding_id, bare_ids)
        self.assertNotIn(second.finding_id, bare_ids)
        self.assertIn(finding["id"], _ids(published["pins"], "input"))

    def test_07_unjoinable_and_keyless_do_not_publish(self) -> None:
        """HAND-DISPATCHED. Unjoinable link, and a subject with no keys. Neither publishes."""
        unjoinable = _link(
            "demo-borrowing-a",
            keys=(("programme", "demo-programme"),),
            finding_id="demo.finding.link.unjoinable",
            fact_id="demo.fact.link.unjoinable",
        )
        _marker_result, count, bare = _drive([_box(), unjoinable])
        assert count is not None
        self.assertEqual(count.publications, ())
        self.assertEqual(count.blocked[0].code, DEPENDENCY_INVALID)
        self.assertEqual(count.blocked[0].missing, (LINK_COVERAGE_UNJOINABLE,))
        self.assertEqual(bare.publications, ())
        self.assertEqual(bare.blocked[0].code, DEPENDENCY_ABSENT)
        self.assertEqual(bare.blocked[0].missing, (COUNT,))

        keyless = _box(keys=None, finding_id="demo.finding.box1.keyless", fact_id="demo.fact.box1.keyless")
        present = _link("demo-borrowing-a")
        _marked, blocked, absent = _drive([keyless, present])
        assert blocked is not None
        self.assertEqual(blocked.publications, ())
        self.assertEqual(blocked.blocked[0].code, DEPENDENCY_INVALID)
        self.assertEqual(blocked.blocked[0].missing, (LINK_COVERAGE_KEYS_UNAVAILABLE,))
        self.assertEqual(absent.publications, ())
        self.assertEqual(absent.blocked[0].code, DEPENDENCY_ABSENT)
        self.assertEqual(absent.blocked[0].missing, (COUNT,))

    def test_08_count_never_run_does_not_publish(self) -> None:
        """HAND-DISPATCHED. The count rule never ran. No optional default. Bare rule does not publish."""
        link = _link("demo-borrowing-a")
        marker, count, bare = _drive([_box(), link], run_count=False)
        assert marker is not None
        self.assertIsNone(count)
        self.assertEqual(self._published(marker)["value"], "1")
        self.assertEqual(bare.publications, ())
        self.assertEqual(len(bare.blocked), 1)
        self.assertEqual(bare.blocked[0].code, DEPENDENCY_ABSENT)
        self.assertEqual(bare.blocked[0].missing, (COUNT,))
        self.assertEqual(bare.inapplicable, ())
