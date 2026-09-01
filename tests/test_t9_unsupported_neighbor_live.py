"""T9 (unsupported neighbor): the plan requires "a source or circumstance
outside the bounded
treatment" for which the product "describes the translation it cannot
perform and does not silently claim coverage" -- not a fact that is merely
routed elsewhere.

A T9 fixture must not use Form 1099-INT box 8 (tax-exempt
interest). Box 8 is a real neighbor of the accrued-interest-at-purchase
bounded treatment, but it is itself a fully supported, separately-routed
product concept (``rule.f1099int-b8-subtotal.json`` feeds Form 1040 line
2a): proving it stays out of *this* milestone's machinery is an isolation
control, not proof of unsupported-translation behavior. The same is true of
Form 1099-INT box 10 (market discount): it too already has a subtotal rule
and its own current-inclusion route. Both are rejected as T9
candidates for that reason (see ``packages/content/tax/2025/rule.f1099int-
b8-subtotal.json`` and ``rule.f1099int-b10-subtotal.json``).

This file uses Form 1099-INT box 11 (bond premium on a taxable bond)
instead -- a real, recognizable IRS box the domain model already names as a
non-goal ("It does not implement bond premium...",
``docs/domain-models/taxable-interest-translation.md``). No source-family,
closure mapping, or computation rule anywhere in the adopted production
package reads ``tax.us.2025.f1099int.box11-bond-premium``
(``packages/content/tax/2025/f1099int-box11.bundle.json`` declares the fact
type and nothing else). Contributing it is not rejected as unrecognized
input, because a real ``bundle-adoption`` act -- the same production
mechanism ``obligation-acquisition.bundle.json`` already uses in this
same fixture -- names it before it is asserted; the fact type is simply
never a member of, or referenced by, the package the run adopts.

The two things a silence-only check cannot prove: (1) alongside a normal,
otherwise-supported accrued-interest circumstance (T2's own box-1 report
plus ordinary acquisition), the bond-premium neighbor changes nothing about
any published total -- it is never silently absorbed and never silently
dropped in a way that would change a number a reader is already trusting;
and (2) a real, already-wired read model
(``packages.tax.coverage.untranslated_source_findings``, the same coverage
module ADR-0016 decision 3 built for "never let a rollup silently report a
broader universe complete", extended past closed families to fact types
that have no family at all) names the exact fact, its value, and its
provenance, and distinguishes it from a fact type the package *does*
consume -- so a fresh reader can recover what remains unsupported (exit
criterion 9) without the presentation layer inventing a bespoke notice.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.kernel.findings import project
from packages.derivation.loader import DerivationSchemas
from packages.tax.coverage import _referenced_fact_type_ids, untranslated_source_findings
from packages.tax.identity_association import ASSOCIATION_SYMBOL
from packages.tax.pairing_consequences import CURRENT_YEAR_SYMBOL_PREFIX
from tests.test_form1099g_box1_schedule1_line7 import _act, _attested
from tests.test_package_membership_wiring import (
    CONTENT,
    ROOT,
    SCOPE,
    USER,
    _content_corpus,
    _load,
    _surface,
    _t2_acts,
)

BOX11_FACT_TYPE = "tax.us.2025.f1099int.box11-bond-premium"
BOX11_AMOUNT = 30.0
TAXABLE_TOTAL_SYMBOL = "tax.us.2025.interest.taxable-total"
PACKAGE_FILE = "package.core-calculations.v34.json"


def _bond_premium_neighbor_acts(*, amount: float = BOX11_AMOUNT) -> list[dict[str, object]]:
    """The real bundle-adoption + entity + assertion acts that contribute
    one Form 1099-INT box-11 bond-premium finding, spliced in immediately
    before the base fixture's final package-adoption act -- the same
    insertion point ``test_t9_unsupported_neighbor_live``'s prior box-8
    attempt used, and the box-9 companion the base fixture's own box-8
    route already established the pattern for."""
    acts = _t2_acts()
    adoption = acts.pop()
    insert_at = len(acts)
    payer_id = "demo.payer.t9-box11"
    statement_id = "demo.1099int-statement.t9-box11"
    acts.append(_act(insert_at, "bundle-adoption", {"bundle": _load("f1099int-box11.bundle.json")}))
    acts.append(
        _act(
            insert_at + 1,
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": payer_id,
                    "kind": "tax.us.interest-payer",
                    "label": "Synthetic interest payer for the T9 box-11 neighbor",
                }
            },
        )
    )
    acts.append(
        _act(
            insert_at + 2,
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": statement_id,
                    "kind": "tax.us.1099int-statement",
                    "label": "Synthetic Form 1099-INT T9 (box 11 neighbor)",
                }
            },
        )
    )
    acts.append(
        _act(
            insert_at + 3,
            "assertion",
            {
                "finding": _attested(
                    "demo.t9.finding.box11",
                    f"{BOX11_FACT_TYPE}|payer={payer_id},statement={statement_id},tax-year=2025",
                    amount,
                )
            },
        )
    )
    acts.append(adoption)
    return acts


def _renumber(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    for index, act in enumerate(acts):
        act["committed_against"] = index
        act["act_id"] = f"demo.t9.act.{index:03d}"
        act["actor"] = USER
    return acts


def _t9_acts(*, amount: float = BOX11_AMOUNT) -> list[dict[str, object]]:
    return _renumber(_bond_premium_neighbor_acts(amount=amount))


def _run(acts: list[dict[str, object]], run_id: str) -> tuple[Any, dict[str, Any], dict[str, Any]]:
    with TemporaryDirectory() as tmp:
        result = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=_surface(),
            output_name="out.json",
        )
        assert result.refusal is None, result.refusal
        assert result.output_path is not None and result.presentation_path is not None
        report = json.loads(result.output_path.read_text("utf-8"))
        presentation = json.loads(result.presentation_path.read_text("utf-8"))
        return result, report, presentation


def _package_members() -> list[dict[str, Any]]:
    """The exact resolved members of the currently adopted production
    package (v35) -- the same corpus ``test_package_membership_wiring``
    validates the package's exclusive graph against."""
    package = _load(PACKAGE_FILE)
    corpus = _content_corpus()
    return [corpus[(member["id"], member["version"])] for member in package["members"]]


class T9UnsupportedNeighborDescribedNotSilent(unittest.TestCase):
    """Real production package, real bundle-adoption contribution, real
    presentation and coverage-read-model paths: the box-11 bond-premium
    neighbor is recognized, never conflated with the accrued-interest
    translation, and legibly named as unsupported."""

    def test_bond_premium_is_recognized_input_not_a_rejected_unknown(self) -> None:
        """The whole point of T9: this is not merely an unrecognized input
        that admission rejects outright -- it is a real, declared fact type
        (via a real ``bundle-adoption`` act) that is admitted and recorded."""
        acts = _t9_acts()
        state = project(tuple(dict(act) for act in acts), DerivationSchemas().registry)
        self.assertIn(BOX11_FACT_TYPE, state.fact_state.fact_types)
        matches = [
            finding
            for finding in state.findings.values()
            if finding["fact_id"].startswith(BOX11_FACT_TYPE + "|")
        ]
        self.assertEqual(len(matches), 1, matches)
        self.assertEqual(matches[0]["value"], BOX11_AMOUNT)

    def test_bond_premium_never_enters_the_pairing_or_current_year_machinery(self) -> None:
        acts = _t9_acts()
        result, _report, _presentation = _run(acts, "demo.run.t9.neighbor.isolation")
        publications = tuple(result.publications or ())
        pairings = [
            pub.finding
            for pub in publications
            if str(pub.finding.get("symbol", "")).startswith(ASSOCIATION_SYMBOL)
        ]
        current_year = [
            pub.finding
            for pub in publications
            if str(pub.finding.get("symbol", "")).startswith(CURRENT_YEAR_SYMBOL_PREFIX + "|")
        ]
        self.assertEqual(len(pairings), 1, pairings)  # T2's own real acquisition/report pairing
        for pub in publications:
            self.assertNotIn(str(BOX11_AMOUNT), json.dumps(pub.finding.get("value")))

    def test_bond_premium_changes_no_published_total_next_to_a_supported_circumstance(self) -> None:
        """The isolation-control half of the proof: run the exact same T2
        accrued-interest circumstance with and without the box-11 neighbor
        present, and confirm every published total is byte-identical. The
        neighbor is neither silently absorbed into a total nor silently
        dropped in a way a reader could mistake for "nothing was reported."
        """
        baseline_acts = _renumber(_t2_acts())
        neighbor_acts = _t9_acts()
        baseline_result, _br, _bp = _run(baseline_acts, "demo.run.t9.baseline")
        neighbor_result, _nr, _np = _run(neighbor_acts, "demo.run.t9.neighbor.totals")

        def _publication_values(result: Any) -> dict[str, Any]:
            return {
                pub.finding["symbol"]: pub.finding["value"]
                for pub in (result.publications or ())
            }

        baseline_values = _publication_values(baseline_result)
        neighbor_values = _publication_values(neighbor_result)
        self.assertIn(TAXABLE_TOTAL_SYMBOL, baseline_values)
        self.assertEqual(baseline_values, neighbor_values)

    def test_untranslated_source_findings_names_the_recognized_but_untranslated_fact(self) -> None:
        """The real coverage read model: it names the exact fact, its exact
        value, and its provenance -- and correctly does *not* flag a fact
        type the package actually does consume (box 1), proving this is a
        structural finding, not a hand-authored list that happens to
        contain box 11."""
        acts = _t9_acts()
        state = project(tuple(dict(act) for act in acts), DerivationSchemas().registry)
        members = _package_members()
        untranslated = untranslated_source_findings(state, members)

        matching = [item for item in untranslated if item.fact_type_id == BOX11_FACT_TYPE]
        self.assertEqual(len(matching), 1, untranslated)
        finding = matching[0]
        self.assertEqual(finding.value, BOX11_AMOUNT)
        self.assertEqual(finding.finding_id, "demo.t9.finding.box11")
        self.assertIn("does not", finding.fact_type_title.lower())
        self.assertIn("bond premium", finding.fact_type_title.lower())

        untranslated_ids = {item.fact_type_id for item in untranslated}
        self.assertNotIn("tax.us.2025.f1099int.box1-interest", untranslated_ids)

    def test_metadata_only_member_cannot_manufacture_false_coverage(self) -> None:
        """Negative control: a metadata-only package member -- a citation whose
        non-semantic ``subject`` field happens to name the box-11 fact-type
        id -- must never make box 11 look consumed. Consumption is decided
        from exact semantic reference fields (a family's member predicate,
        a closure mapping's member fact type, a rule's collect/count/
        categorical-witness operand, a rule's own input pin, an
        attachment's itemization row or completeness answer, a checked-
        conclusion-binding component), never from an incidental string
        match anywhere in a member's content."""
        acts = _t9_acts()
        state = project(tuple(dict(act) for act in acts), DerivationSchemas().registry)
        members = _package_members()
        decoy = {
            "schema": "citation.v1",
            "id": "demo.citation.metadata-only-decoy",
            "version": "v1",
            "subject": BOX11_FACT_TYPE,
            "notes": f"Mentions {BOX11_FACT_TYPE} in free text, not a real reference.",
        }

        untranslated = untranslated_source_findings(state, list(members) + [decoy])

        untranslated_ids = {item.fact_type_id for item in untranslated}
        self.assertIn(
            BOX11_FACT_TYPE, untranslated_ids,
            "a metadata-only member's incidental subject/notes field must not "
            "manufacture a false consumption claim",
        )

    def test_a_genuine_non_collect_input_pin_is_recognized_as_consumption(self) -> None:
        """Positive control: a genuine consumer that is not a family/closure
        ``collect`` at all -- a field-mapping rule that pins a fact type
        directly as an ``input`` (e.g. ``rule.form1040-line12e.json`` pins
        ``tax.us.2025.f1098-scope.no-mortgage-statement`` this way, and
        several ``line2a``/``schedule1-line10``/``sli-worksheet`` rules pin
        their own scope-answer fact types the same way) is still recognized
        as consumption, not just a rule's ``value``/``when`` expression
        operand. This proves the traversal accounts for the genuine
        non-family-collect consumer path, not only the aggregation path box
        1 and box 11 exercise."""
        members = _package_members()
        pin_input_fact_type_ids = {
            pin["id"]
            for member in members
            if isinstance(member.get("pins"), list)
            for pin in member["pins"]
            if isinstance(pin, dict) and pin.get("role") == "input"
        }
        rule_publishes = {
            member["publishes"] for member in members if "publishes" in member
        }
        # A pin id that is not itself another rule's published symbol is a
        # genuine fact-type input pin, not a rule-to-rule subtotal wire --
        # the same distinction the fix's traversal itself makes.
        candidates = pin_input_fact_type_ids - rule_publishes
        self.assertTrue(candidates, "expected at least one genuine input-pinned fact type")

        referenced = _referenced_fact_type_ids(members)
        self.assertTrue(
            candidates <= referenced,
            f"input-pinned fact types not recognized as consumed: {candidates - referenced}",
        )

    def test_no_bundle_adoption_means_the_finding_would_be_rejected_not_silent(self) -> None:
        """Negative control: without the real ``bundle-adoption`` act, the
        same raw assertion is rejected as unrecognized input, confirming
        that T9's admission above is real recognition, not a validation gap
        that would admit any string as a fact id."""
        from packages.kernel.findings import FindingModelError

        acts = _renumber(_t2_acts())
        adoption = acts.pop()
        payer_id = "demo.payer.t9-box11-no-bundle"
        statement_id = "demo.1099int-statement.t9-box11-no-bundle"
        acts.append(
            _act(
                len(acts),
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": payer_id,
                        "kind": "tax.us.interest-payer",
                        "label": "Synthetic interest payer (no bundle adoption)",
                    }
                },
            )
        )
        acts.append(
            _act(
                len(acts),
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": statement_id,
                        "kind": "tax.us.1099int-statement",
                        "label": "Synthetic Form 1099-INT (no bundle adoption)",
                    }
                },
            )
        )
        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.t9.finding.box11-no-bundle",
                        f"{BOX11_FACT_TYPE}|payer={payer_id},statement={statement_id},tax-year=2025",
                        BOX11_AMOUNT,
                    )
                },
            )
        )
        acts.append(adoption)
        acts = _renumber(acts)
        with self.assertRaises(FindingModelError):
            project(tuple(dict(act) for act in acts), DerivationSchemas().registry)


if __name__ == "__main__":
    unittest.main()
