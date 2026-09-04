"""Track 0 — reproduced behavior and the A/B comparison (later-year-basis-reuse).

Milestone: ``later-year-basis-reuse``. Plan:
``docs/phases/tax-concept-derivation/milestones/later-year-basis-reuse.md``.
Findings: ``docs/prototypes/later-year-basis-reuse/track-0-findings.md``.

This module holds all of Track 0's executed evidence:

- C7, the one authorized persisted-boundary experiment, on **one** temporary
  ``ActLog``, and its manual-injection negative control;
- AS-1 (C14) and AS-2 (C15), bounded continuations of that **same** log,
  reached because C7 is negative (see the findings document for the exact
  executed result) — including AS-2's later-reporting-year negative control;
- a small number of other executable claims (C3's own ``$150`` case, C4, C5,
  C6, C8a, C13b), plus bounded absence searches with a negative probe
  (C9, C11);
- S1-S7, and the A/B representation comparison (C12), under held-constant
  conditions.

Every fact used is synthetic (``demo.*``); no personal data. The temporary
``ActLog`` this module builds exists only at test runtime and is never
committed.
"""

from __future__ import annotations

import json
import re
import tempfile
import unittest
from collections.abc import Iterator, Mapping
from decimal import Decimal
from pathlib import Path
from typing import Any

from packages.derivation.loader import DerivationSchemas, load_canon, workspace_registry
from packages.derivation.marshal import marshal_run_context
from packages.derivation.package_validation import package_instance_checksum, validate_package
from packages.derivation.projection import derived_findings_from_acts, workspace_currency
from packages.derivation.runner import (
    InputFinding,
    RunContext,
    SourceFact,
    append_publications,
    run,
)
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.findings import project
from packages.kernel.schema_registry import SchemaValidationError
from packages.tax.identity_association import (
    ACQUISITION_FACT_TYPE,
    ASSOCIATION_SYMBOL,
    REPORT_FACT_TYPE,
    collect_source_names as association_collect_source_names,
)
from packages.tax.obligation_acquisition_mapping import (
    OBLIGATION_ENTITY_KIND,
    PAYER_ENTITY_KIND,
    build_obligation_acquisition_bundle,
    build_ordinary_acquisition_contribution,
    build_ordinary_acquisition_entity_acts,
    derive_obligation_acquisition_fact_id,
    derive_obligation_entity_id,
    derive_payer_entity_id,
)
from packages.tax.pairing_consequences import (
    BASIS_RULE_ID,
    BASIS_SYMBOL_PREFIX,
    CURRENT_YEAR_SYMBOL_PREFIX,
    SUPPORTABILITY_TYPE,
    pairing_scoped_collect_source_names,
)
from packages.tax.report_statement_identity import (
    STATEMENT_ENTITY_KIND,
    derive_1099int_box1_fact_id,
    derive_reported_statement_entity_id,
)
from packages.tax.supportability import SUPPORTABILITY_SYMBOL, load_rule as load_supportability_rule
from tests.support import demo_evidence
from tests.test_integration_checkpoint import (
    _answers as _t2_answers,
    _currency as _t2_currency,
    _findings_for as _t2_findings_for,
    _pairing_values as _t2_pairing_values,
    _pubs_by_prefix as _t2_pubs_by_prefix,
    _report as _t2_report,
    _run as _t2_run,
)

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
EXAMPLES = ROOT / "packages" / "sample_data" / "derivation" / "examples"


def _load_example(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((EXAMPLES / name).read_text(encoding="utf-8"))
    return loaded

ADOPTION_PIN = {
    "role": "adoption",
    "id": "demo.package.later-year-basis-reuse-track0",
    "version": "v1",
}
GOVERNANCE = [{"role": "governance", "id": "governance.constitution", "version": "v1"}]

# This milestone's own worked figures (findings §1.2-1.3), with the
# reading that makes them cohere stated explicitly:
#
#   $10,000  purchase price paid to the seller at settlement, which
#            ALREADY INCLUDES the $150 accrued-interest component
#   +   $40  commission
#   = $10,040 cost origin
#   -   $150 accrued-interest basis reduction (Treas. Reg. § 1.61-7(c))
#   =  $9,890 adjusted basis
#   $10,200 proceeds - $9,890 = $310 gain, versus an understated $160 if
#            the reduction is never reached.
#
# The $150 is therefore subtracted once and added once, never both
# counted into and added on top of the $10,040.
DISPOSITION_PROCEEDS = 10200.0
COST_ORIGIN = 10040.0
ACCRUED_INTEREST_PAID = 150.0
EXPECTED_GAIN_WITH_BASIS = Decimal("310")
EXPECTED_GAIN_WITHOUT_BASIS = Decimal("160")

PAYER_NAME = "demo.payer.bank-c"
OBLIGATION_REFERENCE = "DEMO-BOND-C"
OBLIGATION_DESCRIPTION = "synthetic interest-bearing obligation demo-bond-c"
ACQUISITION_DATE = "2025-03-14"
REPORT_STATEMENT_REFERENCE = "demo-account-c"
REPORT_AMOUNT = 500.0
REPORT_TAX_YEAR = 2025


def _content(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((CONTENT / name).read_text(encoding="utf-8"))
    return loaded


def _acquisition_answers(*, accrued: float = ACCRUED_INTEREST_PAID) -> dict[str, Any]:
    return {
        "payer_name": PAYER_NAME,
        "obligation_description": OBLIGATION_DESCRIPTION,
        "obligation_reference": OBLIGATION_REFERENCE,
        "acquisition_date": ACQUISITION_DATE,
        "accrued_interest_paid_to_seller": accrued,
        "currency": "USD",
        "confirmed_report_match": True,
    }


def _report_fact_id() -> str:
    return derive_1099int_box1_fact_id(
        payer_name=PAYER_NAME,
        statement_reference=REPORT_STATEMENT_REFERENCE,
        tax_year=REPORT_TAX_YEAR,
    )


def _report_finding(finding_id: str = "demo.finding.box1.laterbasis") -> dict[str, Any]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": _report_fact_id(),
        "value": REPORT_AMOUNT,
        "basis": "documentary",
        "evidence_ids": ["demo.evidence.report.laterbasis"],
    }


def _collect_names() -> list[str]:
    return sorted(set(association_collect_source_names()) | set(pairing_scoped_collect_source_names()))


def _seam_rules() -> list[dict[str, Any]]:
    return [
        load_supportability_rule(),
        _content("rule.interest.current-year-adjustment.pairing-scoped.json"),
        _content("rule.basis.item-level-consequence.pairing-scoped.json"),
    ]


def _seam_rules_with_basis_version(version: str) -> list[dict[str, Any]]:
    """The same seam rule set with the ADR-0071 basis rule at a later version.

    Used for S5 (stale history). The pairing-scoped dispatch selects by rule
    id and pins ``rule["version"]``, so this changes the governing version
    without changing which rule governs.
    """
    rules = _seam_rules()
    return [
        {**rule, "version": version} if rule.get("id") == BASIS_RULE_ID else rule
        for rule in rules
    ]


_DISPOSITION_SYMBOL = "test.later.disposition-gain"


def _disposition_rule(basis_symbol: str, *, rule_id: str = "test.later.rule.disposition-gain") -> dict[str, Any]:
    """A disposable, test-local later-year consumer (S-a1 vocabulary, S-a2 wiring).

    Publishes proceeds-minus-cost-plus-the-earlier-basis-reduction, so a
    resolved value of 310 means the earlier $150 consequence reached this
    rule; an unresolved (blocked) rule means it did not.
    """
    return {
        "schema": "rule-artifact.v7",
        "id": rule_id,
        "version": "v1",
        "scope": {"tax_year": 2029, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation",
        "requires": [basis_symbol],
        "pins": [],
        "citations": [],
        "when": True,
        "value": {
            "op": "add",
            "args": [
                {"op": "subtract", "left": DISPOSITION_PROCEEDS, "right": COST_ORIGIN},
                {"op": "ref", "name": basis_symbol},
            ],
        },
        "publishes": _DISPOSITION_SYMBOL,
        "blocked": {"code": "OPEN_DEPENDENCY", "missing": [basis_symbol]},
    }


# --------------------------------------------------------------------------
# The A/B representation comparison (C12).
#
# Shape A (aggregate): ONE published adjusted-basis value at a symbol the
# consumer can name in advance; the consumer reads that one symbol.
# Shape B (durable components): the components stay separately published and
# the CONSUMER composes them.
#
# Only the composition each shape inherently needs is added. No shared
# adapter is imposed, because imposing one would erase the very difference
# under test (milestone plan, "The A/B comparison (C12)").
#
# Held constant across both shapes: the access strategy (AS-2 re-execution
# over the real projection/marshalling boundary), the projected source facts
# and currentness state (the same ``state``/``currency`` objects), the
# scenario, and the consumer purpose and output contract (proceeds minus
# adjusted basis, published as a single disposition-gain symbol).
#
# The cost origin is a test-local rule because composition gap 1 (no
# ``purchase_price``/``acquisition_costs`` vocabulary) means no committed
# content can produce it. It is identical for both shapes, so it cannot
# favour either.
# --------------------------------------------------------------------------

COST_ORIGIN_SYMBOL = "test.later.cost-origin"
AGGREGATE_BASIS_SYMBOL = "test.later.adjusted-basis"
GAIN_A_SYMBOL = "test.later.disposition-gain.aggregate"
GAIN_B_SYMBOL = "test.later.disposition-gain.components"
BROKER_BASIS_SYMBOL = "test.later.broker-reported-basis"

EXPECTED_GAIN_AFTER_CORRECTION = Decimal("360")


def _test_local_rule(
    rule_id: str, *, requires: list[str], value: Any, publishes: str
) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v7",
        "id": rule_id,
        "version": "v1",
        "scope": {"tax_year": 2029, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation",
        "requires": list(requires),
        "pins": [],
        "citations": [],
        "when": True,
        "value": value,
        "publishes": publishes,
        "blocked": {"code": "OPEN_DEPENDENCY", "missing": list(requires)},
    }


def _cost_origin_rule() -> dict[str, Any]:
    return _test_local_rule(
        "test.later.rule.cost-origin", requires=[], value=COST_ORIGIN, publishes=COST_ORIGIN_SYMBOL
    )


def _broker_reported_basis_rule(amount: float) -> dict[str, Any]:
    """A documentary broker-reported basis figure, published as a plain value.

    S3 (disagrees) / S6 (agrees) supply this; S7 omits it entirely.
    """
    return _test_local_rule(
        "test.later.rule.broker-reported-basis",
        requires=[],
        value=amount,
        publishes=BROKER_BASIS_SYMBOL,
    )


def _aggregate_basis_rule(basis_symbol: str) -> dict[str, Any]:
    """Shape A's inherent composition: publish ONE adjusted basis."""
    return _test_local_rule(
        "test.later.rule.adjusted-basis-aggregate",
        requires=[COST_ORIGIN_SYMBOL, basis_symbol],
        value={
            "op": "subtract",
            "left": {"op": "ref", "name": COST_ORIGIN_SYMBOL},
            "right": {"op": "ref", "name": basis_symbol},
        },
        publishes=AGGREGATE_BASIS_SYMBOL,
    )


def _gain_from_aggregate_rule() -> dict[str, Any]:
    """Shape A's consumer.

    Note what this rule does NOT contain: any runtime-keyed symbol. Every
    name in it is a fixed string authorable with no knowledge of any run.
    That is the executed asymmetry C12 turns on.
    """
    return _test_local_rule(
        "test.later.rule.gain-from-aggregate",
        requires=[AGGREGATE_BASIS_SYMBOL],
        value={
            "op": "subtract",
            "left": DISPOSITION_PROCEEDS,
            "right": {"op": "ref", "name": AGGREGATE_BASIS_SYMBOL},
        },
        publishes=GAIN_A_SYMBOL,
    )


def _gain_from_components_rule(basis_symbol: str) -> dict[str, Any]:
    """Shape B's consumer: it composes the components itself, and therefore
    must name the runtime-keyed pairing-scoped consequence symbol directly."""
    return _test_local_rule(
        "test.later.rule.gain-from-components",
        requires=[COST_ORIGIN_SYMBOL, basis_symbol],
        value={
            "op": "subtract",
            "left": DISPOSITION_PROCEEDS,
            "right": {
                "op": "subtract",
                "left": {"op": "ref", "name": COST_ORIGIN_SYMBOL},
                "right": {"op": "ref", "name": basis_symbol},
            },
        },
        publishes=GAIN_B_SYMBOL,
    )


def _publication(result: Any, symbol: str) -> dict[str, Any] | None:
    for pub in result.publications:
        if pub.finding.get("symbol") == symbol:
            found: dict[str, Any] = pub.finding
            return found
    return None


def _blocked_row(result: Any, rule_id: str) -> dict[str, Any] | None:
    for row in result.blocked:
        if row["artifact_id"] == rule_id:
            found: dict[str, Any] = row
            return found
    return None


class _SequentialActLog:
    """Thin ordering helper over a real ``ActLog``: no second log is created.

    Every act appended through this helper lands in the one temporary
    ``ActLog`` passed to ``__init__``. It only manages ``committed_against``
    / ``act_id`` bookkeeping so pre-built act dicts (from the ordinary-
    acquisition and 1099-INT-report contribution builders) and hand-built
    envelopes can interleave without a revision or id collision.
    """

    def __init__(self, log: ActLog) -> None:
        self.log = log

    @property
    def revision(self) -> int:
        return self.log.read().revision

    def append_envelope(self, kind: str, payload: dict[str, Any]) -> int:
        rev = self.revision
        envelope = {
            "schema": "act.v1",
            "act_id": f"demo.track0.act.{rev:04d}",
            "kind": kind,
            "actor": "user",
            "at": f"2026-01-01T00:{rev // 60:02d}:{rev % 60:02d}Z",
            "committed_against": rev,
            "payload": payload,
        }
        return self.log.append(envelope, expected_revision=rev)

    def append_built(self, built_act: dict[str, Any]) -> int:
        """Append a pre-built act dict whose ``committed_against`` already
        names the expected revision (the ordinary-acquisition contribution
        builders compute this themselves from the ``act_index``/
        ``committed_against`` the caller supplies)."""
        rev = self.revision
        if built_act["committed_against"] != rev:
            raise AssertionError(
                f"pre-built act commits against {built_act['committed_against']}, log is at {rev}"
            )
        return self.log.append(built_act, expected_revision=rev)


class Track0PersistedBoundaryExperiment(unittest.TestCase):
    """C7 + its manual-injection control, then AS-1 and AS-2 on the same log.

    One temporary ``ActLog`` for the entire method — no second log, restart,
    or cross-process step (Track 0 evidence-rung ceiling).
    """

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.registry = workspace_registry()
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.log = ActLog(Path(self._tmp.name) / "ws", self.registry)
        self.seq = _SequentialActLog(self.log)

    # -- act-log construction -------------------------------------------------

    def _commit_earlier_case(self) -> tuple[str, str]:
        """Commit the acquisition and the report as real, admitted acts.

        Returns (acquisition_fact_id, acquisition_finding_id). Everything
        here is a genuinely committed act on the one temporary log — no
        hand-built ``FindingState``. This is what makes AS-2's later
        "obtain from the real projection boundary" step honest: there is a
        real boundary to obtain them from.
        """
        answers = _acquisition_answers()
        report_fact_id = _report_fact_id()

        # 0: acquisition-side vocabulary.
        self.seq.append_envelope(
            "bundle-adoption", {"bundle": build_obligation_acquisition_bundle(answers)}
        )
        # 1: report-side vocabulary (production content, unmodified).
        self.seq.append_envelope("bundle-adoption", {"bundle": _content("f1099int.bundle.json")})

        # 2, 3: payer + obligation entities (acquisition side).
        for entity_act in build_ordinary_acquisition_entity_acts(answers, act_index=self.seq.revision):
            self.seq.append_built(entity_act)

        # 4: the report's own statement entity. The payer entity kind and
        # derivation are shared with the report side (both sides document
        # this convention independently; see report_statement_identity.py
        # and obligation_acquisition_mapping.py module docstrings) — the
        # payer entity above is reused, never re-introduced.
        statement_entity_id = derive_reported_statement_entity_id(
            payer_name=PAYER_NAME, statement_reference=REPORT_STATEMENT_REFERENCE
        )
        self.seq.append_envelope(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": statement_entity_id,
                    "kind": STATEMENT_ENTITY_KIND,
                    "label": "Synthetic 1099-INT statement (Track 0)",
                }
            },
        )

        # 5: acquisition evidence.
        self.seq.append_envelope(
            "evidence-submitted",
            {
                "evidence": demo_evidence(
                    "demo.evidence.acq.laterbasis",
                    "Synthetic ordinary-language acquisition interview (Track 0)",
                    {"mode": "ordinary-language-entry", "synthetic": True},
                )
            },
        )

        # 6, 7: acquisition contribution + assertion, confirmed against the
        # report above.
        acq_index = self.seq.revision
        built = build_ordinary_acquisition_contribution(
            answers,
            act_index=acq_index,
            contribution_id="demo.contribution.acq.laterbasis",
            evidence_id="demo.evidence.acq.laterbasis",
            finding_id="demo.finding.acq.laterbasis",
            committed_against=acq_index,
            confirmed_report_fact_id=report_fact_id,
        )
        self.seq.append_built(built.contribution_act)
        self.seq.append_built(built.assertion_act)

        # 8: report evidence.
        self.seq.append_envelope(
            "evidence-submitted",
            {
                "evidence": demo_evidence(
                    "demo.evidence.report.laterbasis",
                    "Synthetic Form 1099-INT (Track 0)",
                    {"mode": "document-report-entry", "synthetic": True},
                )
            },
        )
        # 9: the report itself, a plain documentary assertion — no source-
        # family/closure machinery is adopted, so
        # ``registry.family_member_predicates`` never names this fact type
        # and the SC-R1 member-transition requirement in
        # ``packages.kernel.findings.apply_assertion`` never triggers.
        self.seq.append_envelope("assertion", {"finding": _report_finding()})

        acquisition_fact_id = derive_obligation_acquisition_fact_id(
            payer_name=PAYER_NAME,
            obligation_reference=OBLIGATION_REFERENCE,
            obligation_description=OBLIGATION_DESCRIPTION,
            acquisition_date=ACQUISITION_DATE,
        )
        return acquisition_fact_id, built.finding["id"]

    def _correct_acquisition(self, *, new_accrued: float) -> str:
        """S4: correct the earlier acquisition's accrued amount, same fact id.

        The obligation-acquisition fact type's ``supersession.policy`` is
        ``"free"``, so a same-fact-id assertion is a correction, not a
        rejected duplicate.
        """
        answers = _acquisition_answers(accrued=new_accrued)
        self.seq.append_envelope(
            "evidence-submitted",
            {
                "evidence": demo_evidence(
                    "demo.evidence.acq.laterbasis.correction",
                    "Synthetic correction to the acquisition interview (Track 0, S4)",
                    {"mode": "ordinary-language-entry", "synthetic": True},
                )
            },
        )
        idx = self.seq.revision
        built = build_ordinary_acquisition_contribution(
            answers,
            act_index=idx,
            contribution_id="demo.contribution.acq.laterbasis.correction",
            evidence_id="demo.evidence.acq.laterbasis.correction",
            finding_id="demo.finding.acq.laterbasis.corrected",
            committed_against=idx,
            confirmed_report_fact_id=_report_fact_id(),
        )
        self.seq.append_built(built.contribution_act)
        self.seq.append_built(built.assertion_act)
        return str(built.finding["id"])

    # -- The A/B comparison, on this same log ----------------------------------

    def _run_shape(
        self,
        *,
        run_id: str,
        state: Any,
        currency: Any,
        rules: list[dict[str, Any]],
        reporting_year: int | None,
    ) -> Any:
        ctx = marshal_run_context(
            run_id=run_id,
            state=state,
            currency=currency,
            rules=rules,
            parameters={},
            canon={},
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOVERNANCE,
            collect_source_names=_collect_names(),
            reporting_year=reporting_year,
        )
        # Both shapes run with NO injection at all: the same held-constant
        # access strategy (AS-2 in-run re-execution over the real boundary).
        self.assertEqual(ctx.inputs, [])
        return run(ctx, self.schemas)

    def _ab_shapes(
        self,
        *,
        label: str,
        state: Any,
        currency: Any,
        basis_symbol: str,
        reporting_year: int | None,
        broker_amount: float | None = None,
        seam: list[dict[str, Any]] | None = None,
    ) -> tuple[Any, Any]:
        """Run shape A and shape B under identical held-constant conditions."""
        shared = (seam if seam is not None else _seam_rules()) + [_cost_origin_rule()]
        if broker_amount is not None:
            shared = shared + [_broker_reported_basis_rule(broker_amount)]
        result_a = self._run_shape(
            run_id=f"demo.run.track0.c12.{label}.aggregate",
            state=state,
            currency=currency,
            rules=shared + [_aggregate_basis_rule(basis_symbol), _gain_from_aggregate_rule()],
            reporting_year=reporting_year,
        )
        result_b = self._run_shape(
            run_id=f"demo.run.track0.c12.{label}.components",
            state=state,
            currency=currency,
            rules=shared + [_gain_from_components_rule(basis_symbol)],
            reporting_year=reporting_year,
        )
        return result_a, result_b

    def _ab_comparison(
        self,
        *,
        state: Any,
        currency: Any,
        basis_symbol: str,
        basis_finding_id: str,
    ) -> None:
        """C12: A versus B, held constant, under AS-2 (the reachable experiment).

        AS-1 is unreachable as an experiment (blocked twice, independently —
        see the findings document §7.1/§7.2), so this comparison runs under
        AS-2 alone. That is experimental unreachability, not a product
        architecture selection, and not observational equivalence.
        """
        # --- S1: positive ---------------------------------------------------
        a1, b1 = self._ab_shapes(
            label="s1",
            state=state,
            currency=currency,
            basis_symbol=basis_symbol,
            reporting_year=REPORT_TAX_YEAR,
        )
        gain_a = _publication(a1, GAIN_A_SYMBOL)
        gain_b = _publication(b1, GAIN_B_SYMBOL)
        assert gain_a is not None and gain_b is not None
        # NUMERIC RESULT: identical. No difference.
        self.assertEqual(Decimal(str(a1.symbols[GAIN_A_SYMBOL])), EXPECTED_GAIN_WITH_BASIS)
        self.assertEqual(Decimal(str(b1.symbols[GAIN_B_SYMBOL])), EXPECTED_GAIN_WITH_BASIS)
        # DISPOSITION: identical. Neither shape blocks.
        self.assertIsNone(_blocked_row(a1, "test.later.rule.gain-from-aggregate"))
        self.assertIsNone(_blocked_row(b1, "test.later.rule.gain-from-components"))
        # The NEIGHBORING result in the eligible state (closure gate,
        # artifact 2): the current-year consequence and the supportability
        # verdict publish alongside, identically under both shapes.
        for result in (a1, b1):
            self.assertEqual(len(_by_prefix(result, CURRENT_YEAR_SYMBOL_PREFIX + "|")), 1)
            self.assertEqual(len(_by_prefix(result, SUPPORTABILITY_SYMBOL + "|")), 1)

        # PROVENANCE / COMPONENT ADDRESSABILITY: a real, executed difference.
        # Shape B's own consumer publication pins the pairing-scoped basis
        # consequence finding directly, so a reader walks gain -> consequence
        # -> association -> acquisition/report fact ids in one hop. Shape A's
        # consumer publication does NOT pin it; it pins only the aggregate,
        # and the same walk needs an extra hop through the aggregate's own
        # publication (which is present here only because A's aggregate is
        # recomputed in this same run).
        a_pin_ids = {pin["id"] for pin in gain_a["pins"]}
        b_pin_ids = {pin["id"] for pin in gain_b["pins"]}
        aggregate = _publication(a1, AGGREGATE_BASIS_SYMBOL)
        assert aggregate is not None
        self.assertIn(basis_finding_id, b_pin_ids)
        self.assertNotIn(basis_finding_id, a_pin_ids)
        self.assertIn(aggregate["id"], a_pin_ids)
        self.assertIn(basis_finding_id, {pin["id"] for pin in aggregate["pins"]})

        # DECLARATIVE ADDRESSABILITY: the difference that is NOT an artifact
        # of the access strategy. Shape A's consumer rule contains no
        # runtime-keyed name at all; shape B's consumer rule must name the
        # pairing-scoped symbol, whose suffix is a derived pairing finding id
        # discoverable only from a completed run (composition gap 4).
        self.assertNotIn(basis_symbol, json.dumps(_gain_from_aggregate_rule()))
        self.assertIn(basis_symbol, json.dumps(_gain_from_components_rule(basis_symbol)))
        # Gap 4 is not closed by shape A; it is relocated into A's one
        # aggregating rule, which still names the runtime-keyed symbol.
        self.assertIn(basis_symbol, json.dumps(_aggregate_basis_rule(basis_symbol)))

        # --- S2: the earlier consequence is not available to the later run --
        # Same acts, same shapes; only the run's own reporting year differs,
        # so the association never forms and the consequence is never
        # published. Neither shape may present an unadjusted $160 gain.
        a2, b2 = self._ab_shapes(
            label="s2",
            state=state,
            currency=currency,
            basis_symbol=basis_symbol,
            reporting_year=2029,
        )
        self.assertNotIn(GAIN_A_SYMBOL, a2.symbols)
        self.assertNotIn(GAIN_B_SYMBOL, b2.symbols)
        for result in (a2, b2):
            self.assertNotIn(
                str(EXPECTED_GAIN_WITHOUT_BASIS),
                json.dumps([p.finding for p in result.publications]),
            )
        # The difference is in WHICH symbol the consumer's own blocked row
        # names. B names the missing authority; A names the aggregate, and
        # the missing authority appears one row away, on the aggregating
        # rule's own blocked row.
        a2_consumer = _blocked_row(a2, "test.later.rule.gain-from-aggregate")
        a2_aggregate = _blocked_row(a2, "test.later.rule.adjusted-basis-aggregate")
        b2_consumer = _blocked_row(b2, "test.later.rule.gain-from-components")
        assert a2_consumer is not None and a2_aggregate is not None and b2_consumer is not None
        self.assertEqual(a2_consumer["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(a2_consumer["missing"], [AGGREGATE_BASIS_SYMBOL])
        self.assertEqual(a2_aggregate["missing"], [basis_symbol])
        self.assertEqual(b2_consumer["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(b2_consumer["missing"], [basis_symbol])
        # The NEIGHBORING result in the ineligible state (closure gate,
        # artifact 2): the current-year consequence and the supportability
        # verdict are absent too, and the association simply does not form --
        # no ASSOCIATION_UNCONFIRMED disposition is raised.
        for result in (a2, b2):
            self.assertEqual(_by_prefix(result, CURRENT_YEAR_SYMBOL_PREFIX + "|"), [])
            self.assertEqual(_by_prefix(result, SUPPORTABILITY_SYMBOL + "|"), [])
            self.assertFalse(
                any(row.get("code") == "ASSOCIATION_UNCONFIRMED" for row in result.blocked)
            )

        # --- S3 (broker disagrees) / S6 (broker agrees) ----------------------
        # C11: no mechanism compares a broker figure against a named
        # product-derived adjustment. Executed at the consumer: supplying a
        # documentary figure changes NOTHING under either shape — no
        # reconciliation, no refusal, no flag, in either direction. The two
        # shapes are indistinguishable here because neither has anything to
        # be distinguishable with.
        for label, amount in (("s3-disagrees", COST_ORIGIN), ("s6-agrees", 9890.0)):
            a3, b3 = self._ab_shapes(
                label=label,
                state=state,
                currency=currency,
                basis_symbol=basis_symbol,
                reporting_year=REPORT_TAX_YEAR,
                broker_amount=amount,
            )
            self.assertEqual(Decimal(str(a3.symbols[GAIN_A_SYMBOL])), EXPECTED_GAIN_WITH_BASIS)
            self.assertEqual(Decimal(str(b3.symbols[GAIN_B_SYMBOL])), EXPECTED_GAIN_WITH_BASIS)
            self.assertEqual(Decimal(str(a3.symbols[BROKER_BASIS_SYMBOL])), Decimal(str(amount)))
            # Nothing pins or reads the broker figure in either shape.
            broker_pub = _publication(a3, BROKER_BASIS_SYMBOL)
            assert broker_pub is not None
            for gain_symbol, result in ((GAIN_A_SYMBOL, a3), (GAIN_B_SYMBOL, b3)):
                pub = _publication(result, gain_symbol)
                assert pub is not None
                self.assertNotIn(broker_pub["id"], {pin["id"] for pin in pub["pins"]})

        # --- S7: no broker-reported basis exists at all ----------------------
        # S1 already is this case: no broker figure is supplied there. Both
        # shapes state an adjusted basis from canonical derived history
        # alone, at the same value. Documentary absence is not treated as
        # absence of a canonical adjusted basis under either shape.
        self.assertIsNone(_publication(a1, BROKER_BASIS_SYMBOL))
        self.assertIsNone(_publication(b1, BROKER_BASIS_SYMBOL))
        self.assertEqual(
            Decimal(str(a1.symbols[AGGREGATE_BASIS_SYMBOL])), Decimal("9890")
        )

    # -- the one test method ---------------------------------------------------

    def test_persisted_boundary_c7_then_as1_as2_on_one_temporary_act_log(self) -> None:
        acquisition_fact_id, original_acquisition_finding_id = self._commit_earlier_case()

        # === Step 1-2 (plan): execute the earlier case for real, over the
        # committed acts, through the real kernel projection/marshalling
        # boundary -- the same construction ``live.py`` uses (project +
        # compute_currency + marshal_run_context) -- then append its
        # publications to the SAME temporary act log.
        acts_before = self.log.read().acts
        state_earlier = project(acts_before, self.registry)
        currency_earlier = compute_currency(state_earlier)
        self.assertIn(original_acquisition_finding_id, state_earlier.findings)
        ctx_earlier = marshal_run_context(
            run_id="demo.run.track0.earlier",
            state=state_earlier,
            currency=currency_earlier,
            rules=_seam_rules(),
            parameters={},
            canon={},
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOVERNANCE,
            collect_source_names=_collect_names(),
            reporting_year=REPORT_TAX_YEAR,
        )
        result_earlier = run(ctx_earlier, self.schemas)

        pairings = _t2_pairing_values_from(result_earlier)
        self.assertEqual(len(pairings), 1, result_earlier.blocked)
        self.assertEqual(pairings[0]["left_fact_id"], acquisition_fact_id)
        self.assertEqual(pairings[0]["right_fact_id"], _report_fact_id())
        support = _by_prefix(result_earlier, SUPPORTABILITY_SYMBOL + "|")
        self.assertEqual(len(support), 1)
        self.assertIs(support[0]["value"], True)
        basis_pubs = _by_prefix(result_earlier, BASIS_SYMBOL_PREFIX + "|")
        self.assertEqual(len(basis_pubs), 1)
        basis_finding = basis_pubs[0]
        self.assertEqual(basis_finding["value"], "150.0")
        basis_symbol = basis_finding["symbol"]
        basis_finding_id = basis_finding["id"]
        basis_value = basis_finding["value"]

        # Step 2 (plan): attempt to append the earlier run's publications to
        # the temporary act log.
        #
        # EXECUTED, UNANTICIPATED RESULT: this fails before the intended
        # projection-boundary question is even reached. Every seam rule here
        # is `rule-artifact.v6`/`v7` (the real ADR-0068/0070/0071 content),
        # so the runner's own `use_v2` flag is True and every publication is
        # a `derived-finding.v2`. The one committed persistence primitive's
        # payload schema (`act-derived-publication.v1`) hard-codes
        # `finding.schema == "derived-finding.v1"` as a JSON Schema `const`,
        # with no v2 counterpart wired to the act-log path -- so a v2
        # finding is rejected by schema validation, one step earlier than
        # the ADR-0010 compose-over/projection mechanism this experiment set
        # out to measure. Both committed exercises of `append_publications`
        # (tests/derivation/test_cascade.py,
        # tests/derivation/test_act_log_admission.py) use only
        # `rule-artifact.v1`-shaped demo rules, which is why this gap was
        # never exercised before this milestone.
        with self.assertRaises(SchemaValidationError) as caught:
            append_publications(self.log, result_earlier, actor="user", at="2026-06-01T00:00:00Z")
        self.assertIn("derived-finding.v1", str(caught.exception))

        # Because the real basis-consequence publication can never enter the
        # log, the log still carries no `derived-publication` act naming it.
        # To still answer Track 0 success condition 4 (whether the real
        # projection/marshalling boundary supplies or omits a derived
        # finding) by execution, a schema-compatible (v1) derived
        # publication is committed instead, following the exact committed
        # pattern in tests/derivation/test_cascade.py. This exercises the
        # SAME kernel code path (`packages.kernel.findings.apply_act`'s
        # `KERNEL_ACT_KINDS` exclusion of `derived-publication`, which does
        # not branch on the finding's own schema version) -- legitimate,
        # if generic, corroborating evidence, not a substitute for the
        # (blocked) real-value exercise above.
        demo_ctx = RunContext(
            run_id="demo.run.track0.generic-v1-demo",
            rules=[_load_example("rule-artifact.wages-line1a.json")],
            parameters={},
            canon=load_canon(self.schemas),
            inputs=[InputFinding("rounding.convention", "half_up", "demo.finding.rounding", "input")],
            sources=[SourceFact("demo.w2.box1", "42000", "demo.finding.w2.laterbasis")],
            adoption_pin={"role": "adoption", "id": "demo.package.first-slice.2025", "version": "v1"},
            governance_pins=GOVERNANCE,
        )
        demo_result = run(demo_ctx, self.schemas)
        demo_line1a = next(
            p.finding for p in demo_result.publications if p.finding["symbol"] == "demo.form1040.line1a"
        )
        append_publications(self.log, demo_result, actor="user", at="2026-06-01T00:05:00Z")

        # === C7 (generic mechanism): attempt to expose that demo derived
        # finding to a later run through the real projection/marshalling
        # boundary -- the same construction ``live.py`` uses.
        acts_after = self.log.read().acts
        state_later = project(acts_after, self.registry)
        currency_later = compute_currency(state_later)
        self.assertNotIn(demo_line1a["id"], state_later.findings)

        demo_consumer_rule = _disposition_rule(
            demo_line1a["symbol"], rule_id="test.later.rule.demo-consumer"
        )
        ctx_later_real = marshal_run_context(
            run_id="demo.run.track0.later.real-boundary",
            state=state_later,
            currency=currency_later,
            rules=[demo_consumer_rule],
            parameters={},
            canon={},
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOVERNANCE,
            collect_source_names=[],
            reporting_year=2029,
        )
        result_later_real = run(ctx_later_real, self.schemas)

        # The disconfirmation check runs FIRST, so that on the most likely
        # C7-positive path this diagnostic is what prints -- not a bare list
        # diff from the corroborating assertions below.
        self.assertNotIn(
            _DISPOSITION_SYMBOL,
            result_later_real.symbols,
            "C7 unexpectedly POSITIVE: the real boundary resolved the later "
            "disposition rule without manual injection -- Rival A is "
            "falsified; AS-1/AS-2 would not be reached. Marshaled inputs: "
            f"{ctx_later_real.inputs!r}; sources: {ctx_later_real.sources!r}",
        )
        # Corroborating detail, in the same direction: the real boundary
        # never surfaces the earlier consequence as an input or a source --
        # neither collect_source_names (nothing declares it) nor the
        # fallback "symbol == fact type id" path (derived findings carry a
        # symbol, never a fact_id) can reach it.
        self.assertEqual(
            ctx_later_real.inputs, [], "C7 positive via marshaled inputs"
        )
        self.assertEqual(
            ctx_later_real.sources, [], "C7 positive via marshaled sources"
        )
        blocked_rows = [
            row for row in result_later_real.blocked if row["artifact_id"] == demo_consumer_rule["id"]
        ]
        self.assertEqual(len(blocked_rows), 1, result_later_real.blocked)
        self.assertEqual(blocked_rows[0]["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(blocked_rows[0]["missing"], [demo_line1a["symbol"]])

        # Executed rather than merely asserted in prose: the demo
        # publication above IS a `derived-finding.v1`, so it already
        # satisfies `act-derived-publication.v1`'s schema `const` -- the
        # precondition §7.1 leg (1) names. It nevertheless does not reach
        # `state.findings` (asserted above) and does not reach
        # `ctx.inputs`/`ctx.sources` (asserted just above). That is a
        # direct demonstration that the schema `const` and the projection
        # exclusion are TWO INDEPENDENT blockers: relaxing the schema alone
        # would not surface a derived finding to a later run, because
        # `packages.kernel.findings.apply_act` excludes `derived-publication`
        # from `KERNEL_ACT_KINDS` unconditionally (no schema-version
        # branch), and `marshal_run_context` reads only `state.findings`.
        self.assertEqual(demo_line1a["schema"], "derived-finding.v1")

        # --- Manual-injection negative control, over the REAL $150 value ----
        # (never committed to the log -- it could never be, so it is taken
        # directly from `result_earlier`, in memory). The disposition rule,
        # handed the earlier value directly, resolves to $310 -- isolating
        # persistence/the boundary as the cause of non-exposure, not the
        # rule vocabulary's inability to express the calculation.
        disposition_rule = _disposition_rule(basis_symbol)
        ctx_injected = RunContext(
            run_id="demo.run.track0.later.manual-injection-control",
            rules=[disposition_rule],
            parameters={},
            canon={},
            inputs=[
                InputFinding(
                    symbol=basis_symbol, value=basis_value, finding_id=basis_finding_id, role="input"
                )
            ],
            sources=[],
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOVERNANCE,
        )
        result_control = run(ctx_injected, self.schemas)
        self.assertIn(_DISPOSITION_SYMBOL, result_control.symbols)
        self.assertEqual(
            Decimal(str(result_control.symbols[_DISPOSITION_SYMBOL])), EXPECTED_GAIN_WITH_BASIS
        )

        # === AS-1 (C14): retrieval, continuing this same log. -----------------
        # For the REAL basis consequence: BLOCKED at the persistence step
        # above, before retrieval is reachable at all. The exact failure
        # point is the `act-derived-publication.v1` schema rejecting a
        # `derived-finding.v2` payload -- not the retrieval/currentness
        # machinery, which is never reached for this value. Recorded here,
        # not routed around.
        #
        # The retrieval/currentness/hand-off MECHANISM is demonstrated
        # generically against the demo finding that did commit -- proof the
        # machinery itself works once its schema precondition holds.
        derived = derived_findings_from_acts(acts_after)
        self.assertIn(demo_line1a["id"], derived)
        retrieved = derived[demo_line1a["id"]]
        kernel_currency, derivation_currency = workspace_currency(acts_after, self.registry)
        self.assertIn(demo_line1a["id"], derivation_currency.current_derived_ids)

        ctx_as1 = RunContext(
            run_id="demo.run.track0.later.as1-retrieval",
            rules=[demo_consumer_rule],
            parameters={},
            canon={},
            inputs=[
                InputFinding(
                    symbol=retrieved["symbol"],
                    value=retrieved["value"],
                    finding_id=retrieved["id"],
                    role="input",
                )
            ],
            sources=[],
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOVERNANCE,
        )
        result_as1 = run(ctx_as1, self.schemas)
        self.assertIn(_DISPOSITION_SYMBOL, result_as1.symbols)
        # AS-1's demonstrated result is the historical execution's own value
        # and finding id -- unchanged from `demo_result`, never re-derived.
        self.assertEqual(retrieved["id"], demo_line1a["id"])
        self.assertEqual(retrieved["value"], demo_line1a["value"])

        # === AS-2 (C15): re-execution, same log, explicit 2025 context. ------
        # Obtain the acquisition and report findings from the real
        # projection/marshalling boundary over the SAME authoritative acts
        # (not the hand-assembled findings a rung-3 fixture would use), and
        # re-execute association/supportability/consequence production --
        # never retrieving or injecting them.
        state_as2 = project(acts_after, self.registry)
        currency_as2 = compute_currency(state_as2)
        ctx_as2 = marshal_run_context(
            run_id="demo.run.track0.later.as2-re-execution",
            state=state_as2,
            currency=currency_as2,
            rules=_seam_rules(),
            parameters={},
            canon={},
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOVERNANCE,
            collect_source_names=_collect_names(),
            reporting_year=REPORT_TAX_YEAR,
        )
        # The canonical inputs AS-2 re-derives from: the projected
        # acquisition and report findings, obtained from the real boundary,
        # confirmation fields intact.
        acquisition_source = next(
            s for s in ctx_as2.sources if s.name == ACQUISITION_FACT_TYPE
        )
        report_source = next(s for s in ctx_as2.sources if s.name == REPORT_FACT_TYPE)
        self.assertEqual(acquisition_source.finding_id, original_acquisition_finding_id)
        self.assertIsNotNone(report_source.fact_id)
        self.assertTrue(str(report_source.fact_id).startswith(REPORT_FACT_TYPE))

        result_as2 = run(ctx_as2, self.schemas)
        as2_pairings = _t2_pairing_values_from(result_as2)
        self.assertEqual(len(as2_pairings), 1, result_as2.blocked)
        as2_basis = _by_prefix(result_as2, BASIS_SYMBOL_PREFIX + "|")
        self.assertEqual(len(as2_basis), 1)
        self.assertEqual(as2_basis[0]["value"], "150.0")
        # Re-derived, not retrieved: AS-2 never reads `retrieved` or
        # `result_earlier` to produce this value -- it re-executes the
        # rules over freshly projected source findings.
        as2_basis_symbol = as2_basis[0]["symbol"]
        as2_basis_finding_id = as2_basis[0]["id"]

        ctx_as2_consumer = RunContext(
            run_id="demo.run.track0.later.as2-consumer",
            rules=[_disposition_rule(as2_basis_symbol)],
            parameters={},
            canon={},
            inputs=[
                InputFinding(
                    symbol=as2_basis_symbol,
                    value=as2_basis[0]["value"],
                    finding_id=as2_basis_finding_id,
                    role="input",
                )
            ],
            sources=[],
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOVERNANCE,
        )
        result_as2_consumer = run(ctx_as2_consumer, self.schemas)
        self.assertEqual(
            Decimal(str(result_as2_consumer.symbols[_DISPOSITION_SYMBOL])), EXPECTED_GAIN_WITH_BASIS
        )

        # --- Same-run, mixed-scope composition, and exactly what it
        # establishes ------------------------------------------------------
        # Run the seam rules AND the disposition rule together in ONE run
        # over the real boundary, with NO `RunContext.inputs` injection at
        # all. The pairing-scoped basis rule publishes its runtime-keyed
        # symbol into the runner's own symbol table, and the disposition
        # rule's `{"op": "ref", "name": <that symbol>}` resolves it natively
        # inside the same saturation loop.
        #
        # WHAT THIS ESTABLISHES, AND ONLY THIS: SAME-RUN, MIXED-SCOPE RULE
        # EXPRESSIVENESS. The disposition rule declares `scope.tax_year ==
        # 2029`; the run below carries `reporting_year=REPORT_TAX_YEAR`
        # (2025) -- the report filter that governs which 1099-INT reports
        # may associate, not the year the disposition consumer's own rule is
        # scoped to (see `docs/domain-models/taxable-interest-translation.md`
        # "Cross-year handling"). NOTHING IN THE EVALUATED PATH COMPARES
        # `reporting_year` TO A RULE'S DECLARED `scope.tax_year`; the raw
        # runner does not check or enforce a match between them at all. This
        # is a general fact about the raw runner, not a defect unique to
        # this experiment -- `reporting_year=2025` alongside
        # `scope.tax_year=2029` is not "incoherent" in any sense the domain
        # model or the runner enforces. This proves that TEST-LOCAL
        # MIXED-SCOPE SAME-RUN COMPUTATION IS EXPRESSIBLE. It does NOT prove
        # that an authorized production route exists for that composition --
        # package validation is the separate mechanism that enforces or
        # refuses scope coherence for adopted content (`SCOPE_MISMATCH`,
        # C5), and it is not exercised by this run. The separate later
        # consumer above receives the value by INJECTION through a
        # test-local `InputFinding`.
        #
        # The narrower question -- can the value reach a consumer without
        # injection when the report filter is ITSELF set to the later year?
        # -- is asked and answered NEGATIVELY further below (the
        # `reporting_year=2029` negative control), and that negative control
        # tests one specific configuration, not the space of possible
        # authorized compositions.
        #
        # The naming question: `C8bDeclaredTraversalConstructionAttempt`
        # shows a RAW same-run evaluator CAN aggregate the nonempty
        # pairing-consequence live sources by the symbol's fixed prefix,
        # with no runtime-keyed name. It does NOT show an authorized
        # traversal: the rule's `source_set` is invented and undeclared, and
        # the evaluator never consults it on the nonempty path. Current
        # package validation ACCEPTS this invented rule (zero issues,
        # confirmed by direct execution against the real `artifact-package
        # .v26` package) -- but that acceptance happened because the
        # enforcing `COLLECT_TARGET_NOT_FAMILY` check is inactive at this
        # package generation, not because the traversal is authorized in the
        # sense the check exists to establish. What no declared construct
        # can do is select the consequence OF A NAMED ACQUISITION.
        # Composition gap 4 therefore survives on both the selection half
        # and the authorization half.
        ctx_in_run = marshal_run_context(
            run_id="demo.run.track0.in-run-composition",
            state=state_as2,
            currency=currency_as2,
            rules=_seam_rules()
            + [_disposition_rule(as2_basis_symbol, rule_id="test.later.rule.in-run-disposition")],
            parameters={},
            canon={},
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOVERNANCE,
            collect_source_names=_collect_names(),
            reporting_year=REPORT_TAX_YEAR,
        )
        # No injection whatsoever: the marshaller supplies no inputs.
        self.assertEqual(ctx_in_run.inputs, [])
        result_in_run = run(ctx_in_run, self.schemas)
        self.assertEqual(result_in_run.symbols.get(as2_basis_symbol), "150.0")
        self.assertEqual(
            Decimal(str(result_in_run.symbols[_DISPOSITION_SYMBOL])), EXPECTED_GAIN_WITH_BASIS
        )
        self.assertEqual(result_in_run.blocked, [])

        # --- AS-2's mandatory later-reporting-year negative control ----------
        # Re-attempt association directly under a LATER reporting year, over
        # the identical authoritative acts. The 2025 report must not
        # silently associate; a pass here would mean AS-2's earlier success
        # reflected cross-year leakage, not genuine re-derivation.
        ctx_as2_later_year = marshal_run_context(
            run_id="demo.run.track0.later.as2-negative-control",
            state=state_as2,
            currency=currency_as2,
            rules=_seam_rules(),
            parameters={},
            canon={},
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOVERNANCE,
            collect_source_names=_collect_names(),
            reporting_year=2029,
        )
        result_as2_control = run(ctx_as2_later_year, self.schemas)
        self.assertEqual(_t2_pairing_values_from(result_as2_control), [])
        self.assertEqual(_by_prefix(result_as2_control, BASIS_SYMBOL_PREFIX + "|"), [])

        # --- The `reporting_year=2029` negative-control configuration ------
        # The in-run composition above establishes SAME-RUN, MIXED-SCOPE
        # RULE EXPRESSIVENESS ONLY: the disposition rule declares
        # `scope.tax_year == 2029` while the run it executes in carries
        # `reporting_year=2025`, and nothing in the evaluated path compares
        # the two. That is a general fact about the raw runner, not a defect
        # unique to that experiment.
        #
        # This block tests ONE SPECIFIC CONFIGURATION: a run whose report
        # filter (`reporting_year`) is itself set to 2029, alongside
        # consumer rules that also declare `scope.tax_year=2029`. It does
        # NOT test, and is not offered as testing, every possible AS-2
        # cross-year contract -- only this one. Both authorable consumer
        # forms are tried, both declaring `scope.tax_year=2029`
        # (`_c8b_rule`'s `scope.tax_year` parameter is passed `2029` here,
        # since a collect consumer hardcoded to 2025 would not test what
        # this experiment claims).
        #
        # Result: with the report filter itself set to 2029, the association
        # does not form (the negative control immediately above), so no
        # consequence is produced for any consumer to read; and the only
        # other committed way to carry a determination from the
        # 2025-report-filtered run into a separate run is the act log,
        # which is blocked twice independently (findings §6.1/§6.2). This
        # proves this one configuration is negative -- it does NOT prove no
        # composition is possible. What is actually missing is an
        # AUTHORIZED PACKAGE/SCOPE CONTRACT for composing the 2025
        # determination into a later disposition calculation: no adopted
        # 2029 package exists, and no cross-scope composition contract
        # exists in committed content; `package_validation.py` independently
        # refuses scope-mismatched package members (`SCOPE_MISMATCH`, C5).
        # That is the real ground for the production-blocked conclusion --
        # not package validation being an obstacle, and not an exhaustive
        # demonstration that every 2029/2029 run fails. Recorded as a
        # limitation, not routed around: establishing such a contract would
        # require product machinery the Track 0 boundary does not authorize.
        ctx_filter2029 = marshal_run_context(
            run_id="demo.run.track0.later-report-filter",
            state=state_as2,
            currency=currency_as2,
            rules=_seam_rules()
            + [
                _disposition_rule(
                    as2_basis_symbol, rule_id="test.later.rule.filter2029-disposition"
                ),
                _c8b_rule(
                    {
                        "op": "add",
                        "args": [
                            {
                                "op": "collect",
                                "name": BASIS_SYMBOL_PREFIX,
                                "source_set": C8B_SOURCE_SET,
                            }
                        ],
                    },
                    rule_id="test.later.rule.filter2029-collect",
                    tax_year=2029,
                ),
            ],
            parameters={},
            canon={},
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOVERNANCE,
            collect_source_names=_collect_names(),
            reporting_year=2029,
        )
        self.assertEqual(ctx_filter2029.inputs, [])
        result_filter2029 = run(ctx_filter2029, self.schemas)
        self.assertEqual(_by_prefix(result_filter2029, BASIS_SYMBOL_PREFIX + "|"), [])
        self.assertNotIn(_DISPOSITION_SYMBOL, result_filter2029.symbols)
        self.assertNotIn(C8B_SYMBOL, result_filter2029.symbols)
        row_ref = _blocked_row(result_filter2029, "test.later.rule.filter2029-disposition")
        assert row_ref is not None
        self.assertEqual(row_ref["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(row_ref["missing"], [as2_basis_symbol])
        row_collect = _blocked_row(result_filter2029, "test.later.rule.filter2029-collect")
        assert row_collect is not None
        self.assertEqual(row_collect["code"], "SOURCE_SET_UNCLOSED")
        self.assertEqual(row_collect["missing"], [C8B_SOURCE_SET])
        # The collect consumer really was scoped to the later year this time.
        collect_consumer = _c8b_rule(
            {"op": "add", "args": []}, rule_id="test.later.rule.filter2029-collect",
            tax_year=2029,
        )
        self.assertEqual(collect_consumer["scope"]["tax_year"], 2029)
        # Neither shape of consumer produced an unadjusted $160 gain either:
        # the reporting_year=2029 configuration refuses rather than under-reports.
        self.assertNotEqual(
            result_filter2029.symbols.get(_DISPOSITION_SYMBOL), EXPECTED_GAIN_WITHOUT_BASIS
        )

        # === The A/B comparison (C12), under AS-2, on the same projected
        # state and currentness this AS-2 re-execution just used. S1, S2,
        # S3, S6, S7 here; S4 below, after the correction lands.
        self._ab_comparison(
            state=state_as2,
            currency=currency_as2,
            basis_symbol=as2_basis_symbol,
            basis_finding_id=as2_basis_finding_id,
        )

        # === S4 (plan step 6): correction/displacement over this same log. --
        # Kernel-level displacement is real and unaffected by the schema gap
        # above (it never touches `derived-publication` acts at all).
        corrected_finding_id = self._correct_acquisition(new_accrued=200.0)
        acts_final = self.log.read().acts
        kernel_currency_final, _derivation_currency_final = workspace_currency(acts_final, self.registry)
        self.assertIn(original_acquisition_finding_id, kernel_currency_final.displaced_finding_ids)
        self.assertIn(corrected_finding_id, kernel_currency_final.current_finding_ids)

        # Neither `basis_finding_id` nor `as2_basis_finding_id` was ever
        # committed as a `derived-publication` act (the schema gap above),
        # so displacement over the act log cannot be exercised for either --
        # naming that gap plainly rather than asserting something the log
        # never held. What CAN be shown, honestly: AS-2's re-execution
        # strategy absorbs the correction for free, because it re-derives
        # from current projected state on every call rather than reading a
        # stored value. Re-running the SAME AS-2 re-execution over the
        # now-corrected acts reproduces the corrected $200 consequence, not
        # the original $150 -- with no retrieval, no injection, and no
        # awareness of the prior value.
        state_as2_corrected = project(acts_final, self.registry)
        currency_as2_corrected = compute_currency(state_as2_corrected)
        ctx_as2_corrected = marshal_run_context(
            run_id="demo.run.track0.later.as2-re-execution-post-correction",
            state=state_as2_corrected,
            currency=currency_as2_corrected,
            rules=_seam_rules(),
            parameters={},
            canon={},
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOVERNANCE,
            collect_source_names=_collect_names(),
            reporting_year=REPORT_TAX_YEAR,
        )
        result_as2_corrected = run(ctx_as2_corrected, self.schemas)
        as2_basis_corrected = _by_prefix(result_as2_corrected, BASIS_SYMBOL_PREFIX + "|")
        self.assertEqual(len(as2_basis_corrected), 1, result_as2_corrected.blocked)
        self.assertEqual(as2_basis_corrected[0]["value"], "200.0")
        # AS-1, by contrast, cannot be re-exercised at all here: the value
        # it would retrieve was never persisted in the first place.

        # --- C12 / S4: the same A/B comparison, post-correction -------------
        # Under AS-2 both shapes re-derive the whole determination, so both
        # absorb the correction identically and NEITHER exposes a
        # component-level displacement edge to displace. This is the
        # structural neutralisation the findings document records: two of
        # the three surviving durable-component differences (displacement
        # granularity, independent supersession) cannot be exercised at all
        # under re-execution, because there is no persisted component to
        # displace.
        corrected_basis_symbol = as2_basis_corrected[0]["symbol"]
        a4, b4 = self._ab_shapes(
            label="s4",
            state=state_as2_corrected,
            currency=currency_as2_corrected,
            basis_symbol=corrected_basis_symbol,
            reporting_year=REPORT_TAX_YEAR,
        )
        self.assertEqual(
            Decimal(str(a4.symbols[GAIN_A_SYMBOL])), EXPECTED_GAIN_AFTER_CORRECTION
        )
        self.assertEqual(
            Decimal(str(b4.symbols[GAIN_B_SYMBOL])), EXPECTED_GAIN_AFTER_CORRECTION
        )
        # The aggregate declaration does NOT survive the change to the
        # authority it summarizes (closure gate, artifact 3): it is
        # regenerated at $9,840 and pins the corrected consequence's own new
        # finding id.
        aggregate_after = _publication(a4, AGGREGATE_BASIS_SYMBOL)
        assert aggregate_after is not None
        self.assertEqual(Decimal(str(a4.symbols[AGGREGATE_BASIS_SYMBOL])), Decimal("9840"))
        self.assertIn(
            as2_basis_corrected[0]["id"], {pin["id"] for pin in aggregate_after["pins"]}
        )
        # Neither shape published anything before the correction that the
        # correction could displace: nothing from either shape's earlier run
        # was ever committed to the log (C7's schema gap forbids it), so
        # "displacement granularity" has no observable under AS-2 at all.
        self.assertEqual(
            [
                act
                for act in acts_final
                if act.get("kind") == "derived-publication"
                and GAIN_A_SYMBOL in json.dumps(act)
            ],
            [],
        )

        # --- C12 / S5: stale history (a later rule VERSION governs) ---------
        # Executed, not argued. Re-run both shapes with the ADR-0071 basis
        # rule at a bumped version. Under AS-2 the governing version is
        # simply whichever rule set the current run is given: both shapes
        # take the new determination identically, both record the new
        # version on the consequence's own rule pin, and NEITHER shape can
        # name, prefer, or reject the superseded determination — there is no
        # superseded artifact anywhere to address. "Independent
        # supersession", B's third recorded difference, therefore has no
        # observable under AS-2 either.
        bumped_seam = _seam_rules_with_basis_version("v2")
        ctx_bumped = marshal_run_context(
            run_id="demo.run.track0.c12.s5.bumped-basis-rule-version",
            state=state_as2_corrected,
            currency=currency_as2_corrected,
            rules=bumped_seam,
            parameters={},
            canon={},
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOVERNANCE,
            collect_source_names=_collect_names(),
            reporting_year=REPORT_TAX_YEAR,
        )
        result_bumped = run(ctx_bumped, self.schemas)
        bumped_basis = _by_prefix(result_bumped, BASIS_SYMBOL_PREFIX + "|")
        self.assertEqual(len(bumped_basis), 1, result_bumped.blocked)
        self.assertEqual(bumped_basis[0]["value"], "200.0")
        self.assertIn(
            {"role": "computation", "id": BASIS_RULE_ID, "version": "v2"},
            bumped_basis[0]["pins"],
        )
        self.assertIn(
            {"role": "computation", "id": BASIS_RULE_ID, "version": "v1"},
            as2_basis_corrected[0]["pins"],
        )
        a5, b5 = self._ab_shapes(
            label="s5",
            state=state_as2_corrected,
            currency=currency_as2_corrected,
            basis_symbol=bumped_basis[0]["symbol"],
            reporting_year=REPORT_TAX_YEAR,
            seam=bumped_seam,
        )
        self.assertEqual(
            Decimal(str(a5.symbols[GAIN_A_SYMBOL])), EXPECTED_GAIN_AFTER_CORRECTION
        )
        self.assertEqual(
            Decimal(str(b5.symbols[GAIN_B_SYMBOL])), EXPECTED_GAIN_AFTER_CORRECTION
        )


def _by_prefix(result: Any, prefix: str) -> list[dict[str, Any]]:
    return [
        pub.finding
        for pub in result.publications
        if str(pub.finding.get("symbol", "")).startswith(prefix)
    ]


def _t2_pairing_values_from(result: Any) -> list[dict[str, Any]]:
    return [finding["value"] for finding in _by_prefix(result, ASSOCIATION_SYMBOL)]


class C3TheMilestonesOwnHundredFiftyDollarCase(unittest.TestCase):
    """C3: the committed rule republishes the *supplied* amount, not a fixed
    figure. The committed T2 test demonstrates this at ``42.0``; this
    milestone supplies and executes its own ``$150`` case by overriding
    ``_answers()``, per the milestone plan's explicit correction."""

    def test_committed_t2_case_still_publishes_42(self) -> None:
        result = _t2_run(_t2_findings_for(answers=_t2_answers(), reports=[_t2_report()]))
        cy = _t2_pubs_by_prefix(result, CURRENT_YEAR_SYMBOL_PREFIX + "|")
        basis = _t2_pubs_by_prefix(result, BASIS_SYMBOL_PREFIX + "|")
        self.assertEqual(cy[0]["value"], "42.0")
        self.assertEqual(basis[0]["value"], "42.0")

    def test_this_milestones_own_150_case(self) -> None:
        report = _t2_report(amount=REPORT_AMOUNT)
        result = _t2_run(
            _t2_findings_for(
                answers=_t2_answers(accrued_interest_paid_to_seller=ACCRUED_INTEREST_PAID),
                reports=[report],
            )
        )
        pairings = _t2_pairing_values(result)
        self.assertEqual(len(pairings), 1)
        cy = _t2_pubs_by_prefix(result, CURRENT_YEAR_SYMBOL_PREFIX + "|")
        basis = _t2_pubs_by_prefix(result, BASIS_SYMBOL_PREFIX + "|")
        self.assertEqual(cy[0]["value"], "150.0")
        self.assertEqual(basis[0]["value"], "150.0")
        # Keyed by the derived pairing finding id, not a fixed suffix.
        self.assertTrue(basis[0]["symbol"].startswith(BASIS_SYMBOL_PREFIX + "|"))
        pairing_pub = _t2_pubs_by_prefix(result, ASSOCIATION_SYMBOL + "|")[0]
        self.assertTrue(basis[0]["symbol"].endswith(pairing_pub["id"]))


class C4ReportingYearGatesAssociation(unittest.TestCase):
    """C4: a run carries exactly one ``reporting_year``, gating which reports
    associate; ``None`` means no report is ever in scope."""

    def test_report_outside_run_reporting_year_does_not_associate(self) -> None:
        result = _t2_run(
            _t2_findings_for(answers=_t2_answers(), reports=[_t2_report()]),
            reporting_year=2029,
        )
        self.assertEqual(_t2_pairing_values(result), [])

    def test_none_reporting_year_means_no_report_in_scope(self) -> None:
        result = _t2_run(
            _t2_findings_for(answers=_t2_answers(), reports=[_t2_report()]),
            reporting_year=None,
        )
        self.assertEqual(_t2_pairing_values(result), [])

    def test_matching_reporting_year_associates(self) -> None:
        result = _t2_run(
            _t2_findings_for(answers=_t2_answers(), reports=[_t2_report()]),
            reporting_year=2025,
        )
        self.assertEqual(len(_t2_pairing_values(result)), 1)


class C13bConfirmationNeverRetargetsAcrossReportingYears(unittest.TestCase):
    """C13b: a confirmation recorded against one report's fact id never
    authorizes association against a different report or reporting year."""

    def test_confirmation_naming_a_report_outside_scope_does_not_associate(self) -> None:
        report = _t2_report()
        findings = _t2_findings_for(
            answers=_t2_answers(),
            reports=[report],
            confirmed_report_fact_id=report["fact_id"],
        )
        # The confirmation still names the same fact id; only the run's own
        # reporting-year context changed.
        result = _t2_run(findings, reporting_year=2029)
        self.assertEqual(_t2_pairing_values(result), [])
        self.assertFalse(
            any(row.get("code") == "ASSOCIATION_UNCONFIRMED" for row in result.blocked),
        )


class C8aCommittedCorrelationStructure(unittest.TestCase):
    """C8a: the association's recorded fields and the consequence symbol's
    suffix, read directly off the executed T2 fixture's own artifacts."""

    def test_association_pins_and_consequence_suffix(self) -> None:
        result = _t2_run(_t2_findings_for(answers=_t2_answers(), reports=[_t2_report()]))
        association = _t2_pubs_by_prefix(result, ASSOCIATION_SYMBOL + "|")[0]
        self.assertIn("left_fact_id", association["value"])
        self.assertIn("right_fact_id", association["value"])
        basis = _t2_pubs_by_prefix(result, BASIS_SYMBOL_PREFIX + "|")[0]
        current_year = _t2_pubs_by_prefix(result, CURRENT_YEAR_SYMBOL_PREFIX + "|")[0]
        self.assertTrue(basis["symbol"].endswith(association["id"]))
        self.assertTrue(current_year["symbol"].endswith(association["id"]))
        self.assertIn(association["id"], {pin["id"] for pin in basis["pins"]})
        self.assertIn(association["id"], {pin["id"] for pin in current_year["pins"]})


def _c8b_rule(
    value: Any,
    *,
    rule_id: str = "test.c8b.traversal-attempt",
    tax_year: int = 2025,
) -> dict[str, Any]:
    """A candidate declared traversal, shaped as a real ``rule-artifact.v7``.

    Given no ``requires``: the C8b construction question is purely whether a
    *declared expression* can reach the pairing-scoped consequence, not
    whether the runner can be coaxed into delivering it.

    ``tax_year`` defaults to 2025 -- the event year, correct for the
    construction attempts, which run in a 2025-reporting-year context. The
    ``reporting_year=2029`` negative-control test passes ``tax_year=2029`` so
    that the collect consumer declares the same scope as the report filter
    it runs under; a consumer left at 2025 would not test what that
    experiment claims.
    """
    return {
        "schema": "rule-artifact.v7",
        "id": rule_id,
        "version": "v1",
        "scope": {
            "tax_year": tax_year,
            "jurisdiction": "US-federal",
            "family": "individual-income-tax",
        },
        "role": "computation",
        "requires": [],
        "pins": [],
        "citations": [],
        "when": True,
        "value": value,
        "publishes": C8B_SYMBOL,
        "blocked": {"code": "OPEN_DEPENDENCY", "missing": []},
    }


C8B_SYMBOL = "test.c8b.reached-basis-consequence"
C8B_SOURCE_SET = "demo.set.pairing-scoped-basis"


class C8bDeclaredTraversalConstructionAttempt(unittest.TestCase):
    """C8b, performed as the plan specifies: a bounded declared-expression
    construction attempt, a bounded corpus search for any other committed
    traversal, and a negative probe showing the search could find a positive.

    C8b's falsifier is explicit: exhibiting a working declared join falsifies
    the no-traversal prediction, and failure to author one is not proof none
    exists. **The result splits into three parts**, and they must not be
    read as one another:

    (a) **Falsified, executed, and narrow.** A raw same-run evaluator run
        *can* aggregate the nonempty pairing-consequence live sources by
        their fixed **prefix**, with no runtime-keyed name in the rule text,
        because the runner registers every pairing-scoped publication as a
        live source under the symbol's fixed prefix
        (``runner._append_live_source_from_finding``, which splits the symbol
        at ``"|"``). This is raw fixed-prefix aggregation of live sources.
    (b) **Not falsified.** Nothing reaches *the consequence of a named
        acquisition*. ``collect`` takes ``{op, name, source_set}`` and nothing
        else (``rule-artifact.v7``, ``additionalProperties: false``), so it
        aggregates every row under the prefix with no key, filter, or join;
        ``ref`` needs a literal symbol name, and the per-pairing symbol's
        suffix is a runtime-derived pairing finding id.
    (c) **Not established.** No source-family-authorized traversal is
        established by (a). The positive rule names an INVENTED
        ``source_set`` (``demo.set.pairing-scoped-basis``) with no
        source-family declaration, no closure mapping, and no admission
        anywhere in the repository; and the evaluator's ``collect`` returns
        on the nonempty path BEFORE the ``source_set`` / closure check runs,
        so the invented set was never consulted in the passing run.
        ``C8bCandidateAgainstCurrentPackageValidation`` below puts the same
        rule through the current production package validation path: current
        package validation mechanically ACCEPTS it with zero issues, because
        ``COLLECT_TARGET_NOT_FAMILY`` is inactive for
        ``artifact-package.v26``. That acceptance does not supply the missing
        source-family declaration, closure mapping, or semantic authority.
    """

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    def test_construction_attempt_a_collect_without_a_source_set_is_not_schema_valid(
        self,
    ) -> None:
        """The first thing a declared traversal would try is not authorable."""
        candidate = _c8b_rule(
            {"op": "add", "args": [{"op": "collect", "name": BASIS_SYMBOL_PREFIX}]}
        )
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(candidate)

    def test_construction_attempt_b_a_schema_valid_collect_on_the_prefix_reaches_it(
        self,
    ) -> None:
        """**The positive.** A committed-shape rule naming only fixed strings
        resolves to the pairing-scoped basis consequence's own value."""
        candidate = _c8b_rule(
            {
                "op": "add",
                "args": [
                    {
                        "op": "collect",
                        "name": BASIS_SYMBOL_PREFIX,
                        "source_set": C8B_SOURCE_SET,
                    }
                ],
            }
        )
        self.schemas.validate_declared(candidate)
        # No runtime-derived name anywhere in the rule text.
        self.assertNotIn("|", json.dumps(candidate))

        result = _t2_run(
            _t2_findings_for(answers=_t2_answers(), reports=[_t2_report()]),
            rules=_seam_rules() + [candidate],
        )
        basis = _t2_pubs_by_prefix(result, BASIS_SYMBOL_PREFIX + "|")[0]
        self.assertEqual(str(result.symbols[C8B_SYMBOL]), str(basis["value"]))
        self.assertEqual(result.blocked, [])

    def test_construction_attempt_c_it_fails_closed_when_no_consequence_exists(
        self,
    ) -> None:
        """It does not silently read zero: with no pairing (``reporting_year``
        2029) the declared source set is unclosed and the rule blocks."""
        candidate = _c8b_rule(
            {
                "op": "add",
                "args": [
                    {
                        "op": "collect",
                        "name": BASIS_SYMBOL_PREFIX,
                        "source_set": C8B_SOURCE_SET,
                    }
                ],
            }
        )
        result = _t2_run(
            _t2_findings_for(answers=_t2_answers(), reports=[_t2_report()]),
            rules=_seam_rules() + [candidate],
            reporting_year=2029,
        )
        self.assertNotIn(C8B_SYMBOL, result.symbols)
        row = _blocked_row(result, "test.c8b.traversal-attempt")
        assert row is not None
        self.assertEqual(row["code"], "SOURCE_SET_UNCLOSED")
        self.assertEqual(row["missing"], [C8B_SOURCE_SET])

    def test_construction_attempt_d_no_declared_construct_selects_by_acquisition(
        self,
    ) -> None:
        """**The half that is not falsified**, read off the committed schema
        rather than argued: the ``collect`` node admits exactly ``op``,
        ``name``, ``source_set`` -- no key, filter, join, or identity operand
        -- and every pairing-scoped publication in a run is registered under
        the same prefix name. So the positive above reaches *all* such
        consequences in the run, never a named acquisition's own."""
        schema = json.loads(
            (
                ROOT / "packages" / "schemas" / "derivation" / "rule-artifact.v7.schema.json"
            ).read_text(encoding="utf-8")
        )
        collect_nodes = [
            node
            for node in schema["$defs"]["expr"]["oneOf"]
            if isinstance(node, dict)
            and node.get("properties", {}).get("op", {}).get("const") == "collect"
        ]
        self.assertEqual(len(collect_nodes), 1)
        node = collect_nodes[0]
        self.assertEqual(set(node["properties"]), {"op", "name", "source_set"})
        self.assertIs(node["additionalProperties"], False)
        # And the source name a pairing-scoped consequence is registered
        # under is the symbol's prefix, shared by every pairing in the run.
        result = _t2_run(_t2_findings_for(answers=_t2_answers(), reports=[_t2_report()]))
        basis = _t2_pubs_by_prefix(result, BASIS_SYMBOL_PREFIX + "|")[0]
        prefix, separator, suffix = str(basis["symbol"]).partition("|")
        self.assertEqual(prefix, BASIS_SYMBOL_PREFIX)
        self.assertTrue(separator and suffix)

    def test_bounded_corpus_search_finds_no_other_committed_traversal(self) -> None:
        """Search the committed content corpus for any declared traversal to a
        pairing-scoped consequence, plus the negative probe."""
        content_files = sorted((ROOT / "packages" / "content").rglob("*.json"))
        self.assertGreater(len(content_files), 100)

        naming_a_runtime_key: list[str] = []
        naming_the_pairing_prefix: list[str] = []
        using_collect_at_all: list[str] = []
        for path in content_files:
            text = path.read_text(encoding="utf-8")
            if re.search(r'"name"\s*:\s*"[^"]*\|', text):
                naming_a_runtime_key.append(str(path))
            if "pairing-scoped" in text and '"collect"' in text:
                naming_the_pairing_prefix.append(str(path))
            if re.search(r'"op"\s*:\s*"collect"', text):
                using_collect_at_all.append(str(path))

        self.assertEqual(naming_a_runtime_key, [])
        self.assertEqual(naming_the_pairing_prefix, [])
        # Negative probe: the same file selector and the same `collect`
        # pattern do find committed positives, so the two zero results are
        # genuine absences rather than a search that could never match.
        self.assertGreater(len(using_collect_at_all), 10)


PRODUCTION_PACKAGE_FILE = "package.core-calculations.v35.json"
CONTENT_2025 = ROOT / "packages" / "content" / "tax" / "2025"


def _content_corpus_2025() -> dict[tuple[str, str], dict[str, Any]]:
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT_2025.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if {"id", "version", "schema"} <= data.keys() and not (
            "citizens" in data and "packages" in data
        ):
            corpus[(data["id"], str(data["version"]))] = data
    return corpus


class C8bCandidateAgainstCurrentPackageValidation(unittest.TestCase):
    """C8b's "positive" was graded against schema validation of a single
    rule and a same-run evaluator execution. Neither consults authority.
    This class puts the candidate rule through the **current production
    package validation path** and records what it actually does.

    Two facts make the earlier grading unsafe, and both are re-established
    here by execution rather than asserted:

    1. ``packages/derivation/evaluator.py`` ``collect`` fetches rows and, if
       they are nonempty, RETURNS AT ONCE; the ``source_set`` / closure check
       runs only on the empty path. So the C8b nonempty run succeeded without
       the invented ``demo.set.pairing-scoped-basis`` ever being consulted.
    2. ``package_validation``'s ``COLLECT_TARGET_NOT_FAMILY`` -- the check
       that WOULD notice an undeclared ``source_set`` -- is gated behind a
       literal allowlist of package schema versions that ends at
       ``artifact-package.v17``, while the current production package is
       ``artifact-package.v26``.

    **Finding, recorded and deliberately NOT fixed here** (product code,
    outside this milestone's boundary; escalated to the owner): the
    collect-target universe guard documents itself as binding
    "artifact-package.v3 onward" but has not bound since v17.
    ``collect`` is expressible under ``rule-artifact.v2`` through ``v7``;
    what is special is admission: ``rule-artifact.v7`` is admitted ONLY by
    ``artifact-package.v26``, and the guard has therefore never bound a
    ``rule-artifact.v7`` collect.
    """

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    def _candidate(self) -> dict[str, Any]:
        return _c8b_rule(
            {
                "op": "add",
                "args": [
                    {
                        "op": "collect",
                        "name": BASIS_SYMBOL_PREFIX,
                        "source_set": C8B_SOURCE_SET,
                    }
                ],
            }
        )

    def test_the_invented_source_set_is_declared_by_nothing_committed(self) -> None:
        """No source-family, no closure mapping, no admission names it."""
        hits = [
            str(path.relative_to(ROOT))
            for path in sorted((ROOT / "packages").rglob("*.json"))
            if C8B_SOURCE_SET in path.read_text(encoding="utf-8", errors="ignore")
        ]
        self.assertEqual(hits, [])

    def test_current_production_package_validation_accepts_the_invented_source_set(
        self,
    ) -> None:
        """**The experiment the Track 0 boundary asked for, and its actual result.**

        Add the candidate to the real ``package.core-calculations.v35``
        (``artifact-package.v26``) with the real 2025 content corpus and run
        ``validate_package``. Result: **mechanically ACCEPTS, ``ok is True``,
        zero issues** -- the undeclared ``source_set`` raises nothing,
        because ``COLLECT_TARGET_NOT_FAMILY`` is inactive for
        ``artifact-package.v26``.

        This does NOT establish a source-family-authorized traversal. That
        acceptance does not supply the missing source-family declaration,
        closure mapping, or semantic authority.
        """
        package = json.loads((CONTENT_2025 / PRODUCTION_PACKAGE_FILE).read_text("utf-8"))
        self.assertEqual(package["schema"], "artifact-package.v26")
        corpus = _content_corpus_2025()
        members = {
            (m["id"], m["version"]): corpus[(m["id"], m["version"])]
            for m in package["members"]
        }
        # The unmodified package validates, so any issue below is ours.
        self.assertTrue(validate_package(package, members, self.schemas).ok)

        candidate = self._candidate()
        mutated = json.loads(json.dumps(package))
        mutated["members"].append(
            {
                "id": candidate["id"],
                "role": "computation",
                "schema": "rule-artifact.v7",
                "version": candidate["version"],
            }
        )
        # Reachability is a separate check; make the candidate an entrypoint
        # so the only thing under test is the undeclared source set.
        mutated["entrypoints"].append(
            {"id": candidate["id"], "version": candidate["version"]}
        )
        mutated["package_checksum"] = package_instance_checksum(mutated)
        members[(candidate["id"], candidate["version"])] = candidate

        result = validate_package(mutated, members, self.schemas)
        self.assertEqual([issue.code for issue in result.issues], [])
        self.assertTrue(result.ok)

        # And nothing in the package declares the set it names.
        families = [
            citizen
            for citizen in result.resolved_members
            if citizen.get("schema", "").startswith("source-family.")
        ]
        self.assertGreater(len(families), 5)
        self.assertNotIn(C8B_SOURCE_SET, {family["id"] for family in families})

    def test_the_collect_target_guard_allowlist_stops_at_v17(self) -> None:
        """The gap, read off committed product source. Recorded, not fixed."""
        source = (
            ROOT / "packages" / "derivation" / "package_validation.py"
        ).read_text(encoding="utf-8")
        head, _, tail = source.partition("universe_guard_active = package.get(\"schema\") in {")
        allowlist_text, _, _ = tail.partition("}")
        allowed = set(re.findall(r'"(artifact-package\.v\d+)"', allowlist_text))
        self.assertTrue(allowed)
        highest = max(int(name.rsplit(".v", 1)[1]) for name in allowed)
        self.assertEqual(highest, 17)
        self.assertNotIn("artifact-package.v26", allowed)
        # The adjacent comment claims a strictly wider binding than the code.
        self.assertIn("artifact-package.v3", head[-800:])
        self.assertIn("onward", head[-800:])

    def test_rule_artifact_v7_exists_only_in_the_unguarded_generation(self) -> None:
        """So the guard has never bound a ``rule-artifact.v7`` collect."""
        admitting = []
        for path in sorted(
            (ROOT / "packages" / "schemas" / "derivation").glob("artifact-package.v*.schema.json")
        ):
            if "rule-artifact.v7" in path.read_text(encoding="utf-8"):
                admitting.append(path.name)
        self.assertEqual(admitting, ["artifact-package.v26.schema.json"])

    def test_negative_probe_the_guard_does_fire_at_a_guarded_generation(self) -> None:
        """The guard is real: the SAME invented ``source_set``, in a minimal
        package at ``artifact-package.v4``, is rejected
        ``COLLECT_TARGET_NOT_FAMILY``. So the acceptance above is a gating
        gap, not a check that never worked."""
        fact_type = {
            "schema": "fact-type.v2",
            "id": "demo.fact.alpha-item",
            "version": "v1",
            "title": "Demo alpha item",
            "nature": "determinable",
            "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
            "value_schema": {"type": "number"},
            "supersession": {"policy": "free"},
        }
        rule = {
            "schema": "rule-artifact.v2",
            "id": "demo.rule.alpha-subtotal",
            "version": "v1",
            "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"},
            "role": "computation",
            "requires": [],
            "pins": [],
            "when": True,
            "value": {
                "op": "add",
                "args": [
                    {
                        "op": "collect",
                        "name": "demo.fact.alpha-item",
                        "source_set": C8B_SOURCE_SET,
                    }
                ],
            },
            "publishes": "demo.alpha.subtotal",
            "blocked": {"code": "OPEN_DEPENDENCY", "missing": []},
        }
        members: list[dict[str, Any]] = [fact_type, rule]
        roles = {"fact-type.v2": "fact-type", "rule-artifact.v2": "computation"}
        package: dict[str, Any] = {
            "schema": "artifact-package.v4",
            "id": "demo.package.track0-guard-probe",
            "version": "v1",
            "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"},
            "admitted_schemas": sorted({m["schema"] for m in members}),
            "members": [
                {
                    "role": roles[str(m["schema"])],
                    "schema": m["schema"],
                    "id": m["id"],
                    "version": m["version"],
                }
                for m in members
            ],
            "input_bindings": [],
            "entrypoints": [{"id": m["id"], "version": m["version"]} for m in members],
            "composition_obligations": [],
            "package_checksum": "0" * 64,
        }
        corpus: dict[tuple[str, str], dict[str, Any]] = {
            (str(m["id"]), str(m["version"])): m for m in members
        }
        guarded = validate_package(package, corpus, self.schemas)
        self.assertIn("COLLECT_TARGET_NOT_FAMILY", {i.code for i in guarded.issues})
        # And at the documented v1/v2 history exemption it does not fire --
        # the allowlist behaves exactly as its comment describes at its
        # lower edge, and silently not at all at its upper edge.
        unguarded_history = dict(package, schema="artifact-package.v2")
        history = validate_package(unguarded_history, corpus, self.schemas)
        self.assertNotIn("COLLECT_TARGET_NOT_FAMILY", {i.code for i in history.issues})

    def test_the_nonempty_collect_path_never_consults_the_source_set(self) -> None:
        """Why the C8b run "passed": the evaluator's nonempty branch returns
        before the closure check. Executed both ways on the same rule."""
        source = (ROOT / "packages" / "derivation" / "evaluator.py").read_text("utf-8")
        _, _, after = source.partition('    if op == "collect":')
        body, _, _ = after.partition('    if op == "count":')
        self.assertLess(body.index("if not rows:"), body.index("source_set"))

        candidate = self._candidate()
        nonempty = _t2_run(
            _t2_findings_for(answers=_t2_answers(), reports=[_t2_report()]),
            rules=_seam_rules() + [candidate],
        )
        self.assertIn(C8B_SYMBOL, nonempty.symbols)
        empty = _t2_run(
            _t2_findings_for(answers=_t2_answers(), reports=[_t2_report()]),
            rules=_seam_rules() + [candidate],
            reporting_year=2029,
        )
        row = _blocked_row(empty, candidate["id"])
        assert row is not None
        self.assertEqual(row["code"], "SOURCE_SET_UNCLOSED")


class C5PackageValidationScopeCheckIsMemberScoped(unittest.TestCase):
    """C5: only a member *carrying a ``scope`` key* is checked against the
    package's own scope; a member with no ``scope`` key is not reached by
    this check at all -- not generalized to every citizen."""

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    def _rule(self, *, scope: dict[str, Any] | None) -> dict[str, Any]:
        rule: dict[str, Any] = {
            "schema": "rule-artifact.v7",
            "id": "demo.track0.rule.c5",
            "version": "v1",
            "role": "computation",
            "requires": [],
            "pins": [],
            "when": True,
            "value": 1,
            "publishes": "demo.track0.c5.symbol",
            "blocked": {"code": "OPEN_DEPENDENCY", "missing": []},
        }
        if scope is not None:
            rule["scope"] = scope
        return rule

    def _package(self, rule: dict[str, Any]) -> dict[str, Any]:
        return {
            "schema": "artifact-package.v1",
            "id": "demo.track0.package.c5",
            "version": "v1",
            "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
            "members": [
                {"role": "computation", "id": rule["id"], "version": rule["version"]}
            ],
        }

    def test_mismatched_scope_on_a_scoped_member_is_rejected(self) -> None:
        rule = self._rule(scope={"tax_year": 2026, "jurisdiction": "US-federal", "family": "individual-income-tax"})
        corpus = {(rule["id"], rule["version"]): rule}
        result = validate_package(self._package(rule), corpus, self.schemas)
        codes = {issue.code for issue in result.issues}
        self.assertIn("SCOPE_MISMATCH", codes)

    def test_member_with_no_scope_key_is_not_reached_by_the_scope_check(self) -> None:
        rule = self._rule(scope=None)
        corpus = {(rule["id"], rule["version"]): rule}
        result = validate_package(self._package(rule), corpus, self.schemas)
        codes = {issue.code for issue in result.issues}
        self.assertNotIn("SCOPE_MISMATCH", codes)


class C6AcceptancePredictsNothingAboutResolution(unittest.TestCase):
    """C6, two parts kept separate: (a) the validator accepts a rule whose
    ``requires``/``ref`` names a symbol no package member produces; (b)
    runtime execution of that same rule is a *separate* question, answered
    only by actually running it."""

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    def _rule(self) -> dict[str, Any]:
        return {
            "schema": "rule-artifact.v7",
            "id": "demo.track0.rule.c6",
            "version": "v1",
            "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
            "role": "computation",
            "requires": ["demo.track0.c6.unproduced-symbol"],
            "pins": [],
            "when": True,
            "value": {"op": "ref", "name": "demo.track0.c6.unproduced-symbol"},
            "publishes": "demo.track0.c6.result",
            "blocked": {"code": "OPEN_DEPENDENCY", "missing": ["demo.track0.c6.unproduced-symbol"]},
        }

    def test_a_validator_accepts_the_unresolved_requires(self) -> None:
        rule = self._rule()
        package = {
            "schema": "artifact-package.v1",
            "id": "demo.track0.package.c6",
            "version": "v1",
            "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
            "members": [{"role": "computation", "id": rule["id"], "version": rule["version"]}],
        }
        corpus = {(rule["id"], rule["version"]): rule}
        result = validate_package(package, corpus, self.schemas)
        codes = {issue.code for issue in result.issues}
        self.assertNotIn("CLOSURE_MISSING_PARAMETER", codes)
        self.assertFalse(any("unproduced-symbol" in issue.detail for issue in result.issues))

    def test_b_runtime_execution_blocks_it_a_separate_question(self) -> None:
        rule = self._rule()
        ctx = RunContext(
            run_id="demo.run.track0.c6",
            rules=[rule],
            parameters={},
            canon={},
            inputs=[],
            sources=[],
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOVERNANCE,
        )
        result = run(ctx, self.schemas)
        self.assertNotIn(rule["publishes"], result.symbols)
        blocked = [row for row in result.blocked if row["artifact_id"] == rule["id"]]
        self.assertEqual(len(blocked), 1)
        self.assertEqual(blocked[0]["code"], "DEPENDENCY_ABSENT")


class C10CorrectionDisplacesBothPublishedConsequences(unittest.TestCase):
    """C10: correcting the earlier acquisition displaces BOTH published
    consequences. It grounds S4 and the "correct" requirement of §2.5 item 3
    in the findings, which the A/B comparison depends on, so it is executed
    into this module's own record rather than cited from another file."""

    def test_named_committed_displacement_test_passes(self) -> None:
        from tests.test_pairing_consequences import TestCorrectionDisplacement

        case = TestCorrectionDisplacement(
            "test_shared_pins_displace_both_consequences_via_real_machinery"
        )
        outcome = case.run()
        assert outcome is not None
        self.assertTrue(outcome.wasSuccessful(), outcome.errors + outcome.failures)
        self.assertEqual(outcome.testsRun, 1)

    def test_correcting_the_acquisition_displaces_both_consequences_here(self) -> None:
        """The same claim, exercised directly on this milestone's own $150
        figures rather than only by delegation: correcting the acquisition
        changes both the current-year and the basis consequence, and both
        carry the correction's own new finding ids."""
        report = _t2_report(amount=REPORT_AMOUNT)
        before = _t2_run(
            _t2_findings_for(
                answers=_t2_answers(accrued_interest_paid_to_seller=ACCRUED_INTEREST_PAID),
                reports=[report],
            )
        )
        after = _t2_run(
            _t2_findings_for(
                answers=_t2_answers(accrued_interest_paid_to_seller=200.0),
                reports=[report],
            )
        )
        cy_before = _t2_pubs_by_prefix(before, CURRENT_YEAR_SYMBOL_PREFIX + "|")[0]
        cy_after = _t2_pubs_by_prefix(after, CURRENT_YEAR_SYMBOL_PREFIX + "|")[0]
        basis_before = _t2_pubs_by_prefix(before, BASIS_SYMBOL_PREFIX + "|")[0]
        basis_after = _t2_pubs_by_prefix(after, BASIS_SYMBOL_PREFIX + "|")[0]
        self.assertEqual(cy_before["value"], "150.0")
        self.assertEqual(basis_before["value"], "150.0")
        self.assertEqual(cy_after["value"], "200.0")
        self.assertEqual(basis_after["value"], "200.0")
        # Both consequences are genuinely new findings, not rewrites.
        self.assertNotEqual(cy_before["id"], cy_after["id"])
        self.assertNotEqual(basis_before["id"], basis_after["id"])


class C9NoProductionCallerOfAppendPublications(unittest.TestCase):
    """C9: ``append_publications`` (durable cross-run retrieval's primitive)
    has no caller under ``packages/`` -- a bounded search, plus a negative
    probe confirming the search method itself can find a positive."""

    def test_no_caller_under_packages(self) -> None:
        pattern = re.compile(r"\bappend_publications\s*\(")
        packages_dir = ROOT / "packages"
        hits: list[str] = []
        for path in packages_dir.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            if pattern.search(text):
                hits.append(str(path.relative_to(ROOT)))
        # The definition itself lives under packages/derivation/runner.py;
        # a bare `def append_publications(` is not a call.
        call_hits = [
            h
            for h in hits
            if not any(
                "def append_publications" in line
                for line in (ROOT / h).read_text(encoding="utf-8").splitlines()
                if pattern.search(line)
            )
        ]
        self.assertEqual(call_hits, [], call_hits)

    def test_negative_probe_the_search_finds_known_test_callers(self) -> None:
        pattern = re.compile(r"\bappend_publications\s*\(")
        tests_dir = ROOT / "tests"
        hits = [
            str(path.relative_to(ROOT))
            for path in tests_dir.rglob("*.py")
            if pattern.search(path.read_text(encoding="utf-8"))
        ]
        self.assertIn("tests/derivation/test_cascade.py", hits)
        self.assertIn("tests/derivation/test_act_log_admission.py", hits)
        # This module itself is now a fourth, disposable caller.
        self.assertIn("tests/test_later_year_basis_reuse_track0.py", hits)


def _walk_nodes(node: Any) -> Iterator[dict[str, Any]]:
    """Every mapping reachable inside a declared citizen."""
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from _walk_nodes(value)
    elif isinstance(node, list):
        for value in node:
            yield from _walk_nodes(value)


def _consumed_names(citizen: Mapping[str, Any]) -> set[str]:
    """The names a declared rule actually READS: ``requires`` plus every
    ``ref`` / ``collect`` / ``count`` name in its ``when`` and ``value``.

    This is a consumption trace, not a text search: a name that appears in a
    citizen's ``publishes``, ``notes``, ``id``, or citation list is not
    counted, and a package manifest that merely *enumerates* the rule
    contributes nothing at all.
    """
    consumed: set[str] = set(citizen.get("requires") or [])
    for node in _walk_nodes({"when": citizen.get("when"), "value": citizen.get("value")}):
        if node.get("op") in {"ref", "collect", "count"} and isinstance(node.get("name"), str):
            consumed.add(node["name"])
    return consumed


class C11NoBrokerBasisComparisonMechanism(unittest.TestCase):
    """C11: no mechanism compares a broker-reported basis against a named
    product-derived adjustment.

    A file-level regex co-occurrence test -- artifacts that merely *name*
    two strings -- is not a consumer trace, and a repository-wide absence
    claim cannot rest on string non-intersection: a manifest naming both
    sides reads neither, and a rule reading both could name them through
    ``requires`` without the words ever co-occurring in the pattern's own
    form.

    So this builds the real trace instead. ``test_two_sided_consumer_trace_
    ...`` below enumerates the concrete broker-reported-basis fact types,
    resolves the declared rules that actually consume them through
    ``requires`` / ``collect`` / ``ref`` / ``count``, separately resolves
    every consumer of the pairing-scoped basis consequence's published
    symbol and declared fact type on both the declared and the Python side,
    and intersects the two **consumer sets**.

    The trace's result is stronger and simpler than a co-occurrence test
    could show: the derived side has **no declared consumer at all**. Two
    categories, not ten inputs. Five declared rule IDs (across seven rule
    documents -- two IDs are each committed at two document versions)
    consume the five transaction-basis VALUE fact types
    (``tax.us.2025.f1099b.covered-{st,lt,ltcg,w-st,w-lt}-txn.basis``) --
    these, and ONLY these, feed those subtotal rule IDs; zero committed
    rules consume the pairing-scoped basis consequence; no Python module
    under ``packages/`` names any broker-reported-basis fact type, and the
    only Python module naming the derived consequence is its own producer.
    The five corresponding CLOSURE-AUTHORITY fact types (the
    ``.source-closure`` ones) establish source-set completeness and are NOT
    direct expression inputs to the subtotal rules; they are not counted
    among the five VALUE fact types above. The intersection is empty
    because one side is empty -- which is exactly what the committed rule's
    own note records ("A later-year disposition consumer of this finding is
    still open").
    """

    BASIS_COMPARISON = re.compile(r"basis.*(compare|reconcil)|reconcil.*basis", re.IGNORECASE)

    #: The published symbol of the committed pairing-scoped basis rule, the
    #: declared fact type it instantiates, and the runtime symbol prefix.
    DERIVED_BASIS_NAMES = frozenset(
        {
            "tax.us.2025.basis.item-level-consequence",
            "tax.us.2025.basis.item-level-consequence.pairing-scoped",
        }
    )

    def _declared_rules(self) -> list[tuple[str, str, dict[str, Any]]]:
        """Every declared rule/attachment citizen under ``packages/content``."""
        found: list[tuple[str, str, dict[str, Any]]] = []
        for path in sorted((ROOT / "packages" / "content").rglob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (ValueError, UnicodeDecodeError):
                continue
            for node in _walk_nodes(data):
                schema = node.get("schema")
                if (
                    isinstance(schema, str)
                    and re.fullmatch(r"(rule-artifact|attachment-rule)\.v\d+", schema)
                    and "value" in node
                    and isinstance(node.get("id"), str)
                ):
                    found.append((node["id"], str(path.relative_to(ROOT)), node))
        return found

    def _broker_basis_fact_types(self) -> set[str]:
        """Committed ``f1099b`` ``*basis*`` fact-type ids, resolved from
        ``fact-type.v2`` citizens rather than guessed. The set contains two
        categories: five transaction-basis VALUE types (the only inputs to
        the five subtotal rules) and five corresponding CLOSURE-AUTHORITY
        ``.source-closure`` types (source-set completeness, not expression
        inputs). The consumer-trace test enumerates both; they must not be
        read as ten inputs of one kind."""
        fact_types: set[str] = set()
        for path in sorted((ROOT / "packages" / "content").rglob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (ValueError, UnicodeDecodeError):
                continue
            for node in _walk_nodes(data):
                if node.get("schema") == "fact-type.v2" and isinstance(node.get("id"), str):
                    fact_id = node["id"]
                    if "f1099b" in fact_id and "basis" in fact_id:
                        fact_types.add(fact_id)
        return fact_types

    def _reads_derived(self, consumed: set[str]) -> bool:
        prefix = "tax.us.2025.basis.item-level-consequence.pairing-scoped|"
        return any(
            name in self.DERIVED_BASIS_NAMES or name.startswith(prefix) for name in consumed
        )

    def test_two_sided_consumer_trace_no_artifact_reads_both(self) -> None:
        """Trace consumers, not co-occurring strings."""
        broker_fact_types = self._broker_basis_fact_types()
        # Non-vacuous, and stated exactly so the trace is auditable.
        self.assertEqual(
            sorted(broker_fact_types),
            [
                "tax.us.2025.f1099b.covered-lt-basis.source-closure",
                "tax.us.2025.f1099b.covered-lt-txn.basis",
                "tax.us.2025.f1099b.covered-ltcg-basis.source-closure",
                "tax.us.2025.f1099b.covered-ltcg-txn.basis",
                "tax.us.2025.f1099b.covered-st-basis.source-closure",
                "tax.us.2025.f1099b.covered-st-txn.basis",
                "tax.us.2025.f1099b.covered-w-lt-basis.source-closure",
                "tax.us.2025.f1099b.covered-w-lt-txn.basis",
                "tax.us.2025.f1099b.covered-w-st-basis.source-closure",
                "tax.us.2025.f1099b.covered-w-st-txn.basis",
            ],
        )

        broker_consumers: set[str] = set()
        derived_consumers: set[str] = set()
        both: set[str] = set()
        rules = self._declared_rules()
        self.assertGreater(len(rules), 50, "the declared-rule selector found almost nothing")
        for rule_id, _rel, citizen in rules:
            consumed = _consumed_names(citizen)
            is_broker = bool(consumed & broker_fact_types)
            is_derived = self._reads_derived(consumed)
            if is_broker:
                broker_consumers.add(rule_id)
            if is_derived:
                derived_consumers.add(rule_id)
            if is_broker and is_derived:
                both.add(rule_id)

        # Broker side, resolved by consumption: non-vacuous and exact.
        self.assertEqual(
            sorted(broker_consumers),
            [
                "tax.us.2025.rule.f1099b-covered-lt-basis-subtotal",
                "tax.us.2025.rule.f1099b-covered-ltcg-basis-subtotal",
                "tax.us.2025.rule.f1099b-covered-st-basis-subtotal",
                "tax.us.2025.rule.f1099b-covered-w-lt-basis-subtotal",
                "tax.us.2025.rule.f1099b-covered-w-st-basis-subtotal",
            ],
        )
        # Derived side: NO committed declared rule consumes it at all.
        self.assertEqual(sorted(derived_consumers), [])
        self.assertEqual(sorted(both), [])

    def test_the_derived_side_has_no_declared_consumer_by_the_rules_own_admission(self) -> None:
        """The trace's zero is corroborated by the committed rule's own note,
        so the empty derived-consumer set is not an artefact of the selector."""
        rule = json.loads(
            (
                ROOT
                / "packages"
                / "content"
                / "tax"
                / "2025"
                / "rule.basis.item-level-consequence.pairing-scoped.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(rule["publishes"], "tax.us.2025.basis.item-level-consequence")
        self.assertIn("later-year disposition consumer", rule["notes"])
        self.assertIn("still open", rule["notes"])

    def test_python_consumer_trace_across_packages(self) -> None:
        """The Python half of the same trace, by module rather than by file
        text co-occurrence: which modules under ``packages/`` name each side."""
        broker_fact_types = self._broker_basis_fact_types()
        broker_modules: list[str] = []
        derived_modules: list[str] = []
        for path in sorted((ROOT / "packages").rglob("*.py")):
            text = path.read_text(encoding="utf-8", errors="ignore")
            rel = str(path.relative_to(ROOT))
            if any(fact_id in text for fact_id in broker_fact_types):
                broker_modules.append(rel)
            if any(name in text for name in self.DERIVED_BASIS_NAMES):
                derived_modules.append(rel)
        # No product module names a broker-reported-basis fact type at all --
        # those subtotals are declared content, not Python.
        self.assertEqual(broker_modules, [])
        # The only module naming the derived consequence is its PRODUCER.
        self.assertEqual(derived_modules, ["packages/tax/pairing_consequences.py"])
        self.assertEqual(sorted(set(broker_modules) & set(derived_modules)), [])

    def _matching_paths(self) -> list[Path]:
        pattern = re.compile(r"taxpayer_side_adjustment")
        paths: list[Path] = []
        for glob in ("*.py", "*.json"):
            for path in (ROOT / "packages").rglob(glob):
                if pattern.search(path.read_text(encoding="utf-8")):
                    paths.append(path)
        return paths

    def test_no_comparison_of_taxpayer_side_adjustment_against_a_derived_basis(self) -> None:
        """Narrow by construction: this supports a conclusion about the
        inspected ``taxpayer_side_adjustment`` / Schedule D paths only. The
        repository-wide claim rests on the two-sided trace above."""
        offending: dict[str, list[str]] = {}
        for path in self._matching_paths():
            lines = [
                line
                for line in path.read_text(encoding="utf-8").splitlines()
                if self.BASIS_COMPARISON.search(line)
            ]
            if lines:
                offending[str(path.relative_to(ROOT))] = lines
        self.assertEqual(offending, {})

    def test_negative_probe_a_the_file_selector_finds_the_uses_that_do_exist(self) -> None:
        """Probes the FILE SELECTOR only: `taxpayer_side_adjustment` really
        does occur under packages/, so the selector is not vacuous."""
        hits = sorted(str(path.relative_to(ROOT)) for path in self._matching_paths())
        self.assertTrue(hits, "the selector found no files at all -- it cannot be trusted")
        # Exactly what the search returns, stated precisely:
        # five f1099b-covered-* bundle files, two occurrences each, plus one
        # sample-data negative fixture that is NOT a bundle declaration.
        bundles = [h for h in hits if h.startswith("packages/content/tax/2025/")]
        others = [h for h in hits if not h.startswith("packages/content/tax/2025/")]
        self.assertEqual(len(bundles), 5, bundles)
        self.assertTrue(all("f1099b-covered-" in h for h in bundles), bundles)
        self.assertEqual(
            others, ["packages/sample_data/schedule_d_covered_ltcg_8a_t1/negatives/"
                     "value.covered-ltcg-txn-missing-gain-only.json"], others
        )

    def test_negative_probe_b_the_basis_comparison_pattern_can_find_a_positive(self) -> None:
        """Probes the PATTERN the absence claim actually rests on.

        The file selector being non-vacuous says nothing about whether
        ``BASIS_COMPARISON`` could ever match. Run that exact pattern over a
        committed file known to discuss reconciling broker-reported basis --
        ``docs/domain-models/investment-basis.md``, whose "Reconciliation
        with institutionally reported basis" section is precisely the
        subject matter C11 claims no *mechanism* implements. The pattern
        matches there, so its zero result over the ``taxpayer_side_adjustment``
        files is a genuine absence of a comparison mechanism, not a pattern
        that could never match anything.
        """
        prose = (ROOT / "docs" / "domain-models" / "investment-basis.md").read_text(encoding="utf-8")
        matches = [line for line in prose.splitlines() if self.BASIS_COMPARISON.search(line)]
        self.assertTrue(
            matches,
            "the basis-comparison pattern matched nothing even in prose that "
            "explicitly discusses reconciling broker-reported basis -- the "
            "pattern cannot be trusted as an absence probe",
        )


if __name__ == "__main__":
    unittest.main()
