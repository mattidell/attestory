"""T8 (identity discriminator), through the real published package.

**A genuine rework of both sides' identity derivation, not a wording
pass.** Manufacturing the report's own statement entity id with
``obligation_acquisition_mapping.derive_reported_statement_entity_id`` —
the *acquisition-side* helper — and then proving that an
acquisition using that same helper joins it, would only prove two fixtures
built by the same function agree with each other; it would not prove that an
independent document-side path and the ordinary-language path resolve to
shared identity. The real-world case the milestone plan
requires is one statement/account that legitimately aggregates interest
from *several* obligations, with obligation correspondence resolved only by
the person's own attestation, never by the statement match alone — not two
distinct statements under one payer, which exercises the wrong ambiguity.

This test:

- Derives the report's own payer and statement entity ids through
  ``packages.tax.report_statement_identity`` — a module that does not
  import or call anything in ``obligation_acquisition_mapping`` — and
  contributes the report through a real, minimal "contribute a documentary
  Form 1099-INT report" path
  (``report_statement_identity.contribute_1099int_report``) that goes
  through the same ``apply_contribution_batch`` admission boundary
  ``contribute_ordinary_acquisition`` already uses on the acquisition side.
  Both modules independently implement the *same documented* payer/
  statement canonicalization convention (see both modules' docstrings) —
  neither calls the other.
- Builds one report/statement that aggregates interest from two genuinely
  distinct obligations, and proves: (a) an acquisition for obligation A,
  attested (``confirmed_report_match: True``) against that report,
  associates and computes its own adjustment; (b) a second acquisition for
  obligation B, also attested against the same report, associates
  independently (both sharing one report is a legitimate real-world shape,
  bounded by ADR-0070's aggregate-supportability check, not something this
  seam needs to prevent); (c) a third acquisition for a different
  obligation, naming the same payer but supplying no statement reference
  and never confirming, does not silently join the coarse payer+year
  candidate; (d) a fourth acquisition names the *correct* statement
  reference — the statement-narrowed tier resolves it to exactly this one
  report — but withholds confirmation, and still refuses
  ``ASSOCIATION_UNCONFIRMED`` rather than associating. (c) and (d) together
  are the direct proof that a payer/statement/year match, even the exactly
  right one, is never by itself sufficient — only the person's own
  attestation associates.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.kernel.findings import project
from packages.tax.identity_association import (
    ASSOCIATION_AMBIGUOUS,
    ASSOCIATION_SYMBOL,
    ASSOCIATION_UNCONFIRMED,
    REPORT_FACT_TYPE,
)
from packages.tax.obligation_acquisition_mapping import (
    build_ordinary_acquisition_contribution,
    contribute_ordinary_acquisition,
    derive_obligation_entity_id,
)
from packages.tax.pairing_consequences import BASIS_SYMBOL_PREFIX, CURRENT_YEAR_SYMBOL_PREFIX
from packages.tax.report_statement_identity import (
    build_1099int_report_contribution,
    build_1099int_report_entity_acts,
    contribute_1099int_report,
    derive_1099int_box1_fact_id,
    derive_reported_payer_entity_id,
    derive_reported_statement_entity_id,
)
from tests.support import demo_evidence
from tests.test_f1098e_student_loan_interest_agi_track6 import _f1098e_acts
from tests.test_form1099g_box1_schedule1_line7 import _act, _attested
from tests.test_package_membership_wiring import ROOT, SCOPE, USER, _load, _surface

# The document side (Form 1099-INT) and the ordinary-language side name this
# payer and statement/account by the *same raw string* a real payer name and
# a real account reference would be — never a pre-built entity id. Each side
# canonicalizes these strings independently (see
# ``packages.tax.report_statement_identity`` and
# ``packages.tax.obligation_acquisition_mapping``'s docstrings for the
# shared, documented convention both sides follow without one calling the
# other).
PAYER_NAME = "Demo T8-Live Aggregating Bank"
STATEMENT_REFERENCE = "ACCOUNT-REF-T8-LIVE-SHARED"
REPORT_AMOUNT = 1150.0

OBLIGATION_REFERENCE_A = "DEMO-BOND-T8-LIVE-A"
OBLIGATION_REFERENCE_B = "DEMO-BOND-T8-LIVE-B"
OBLIGATION_REFERENCE_C = "DEMO-BOND-T8-LIVE-C-UNATTESTED"
OBLIGATION_REFERENCE_D = "DEMO-BOND-T8-LIVE-D-STATEMENT-NO-CONFIRM"
ACCRUED_A = 300.0
ACCRUED_B = 200.0
ACCRUED_C = 50.0
ACCRUED_D = 75.0

FAMILY_PREDECESSOR = "demo.cgd.t2.int-b1.h0"
FAMILY_SUCCESSOR = "demo.t8-live.int-b1.h1"


def _acquisition_answers(
    *,
    obligation_reference: str,
    accrued: float,
    statement_reference: str | None,
    confirmed: bool,
) -> dict[str, object]:
    return {
        "payer_name": PAYER_NAME,
        "obligation_description": f"synthetic obligation ({obligation_reference})",
        "obligation_reference": obligation_reference,
        "acquisition_date": "2025-03-14",
        "accrued_interest_paid_to_seller": accrued,
        "currency": "USD",
        "reported_statement_reference": statement_reference,
        "confirmed_report_match": confirmed,
    }


def _t8_acts() -> list[dict[str, object]]:
    """One report aggregating two obligations' interest; a third,
    unattested, obligation from the same payer that must not silently join
    it. Built from the same complete-production-shaped-return base
    ``_t2_acts`` uses, but with its own payer/statement/obligations (never
    T2's), so the live fixtures do not share mutable entity state."""
    acts = _f1098e_acts(statements=[], close=True, wages=90000)
    acts.pop()  # drop the v33 Track-6 adoption

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("obligation-acquisition.bundle.json")})

    # --- Document side: the payer and statement entities are introduced,
    # and their ids derived, entirely through report_statement_identity --
    # a module that never imports or calls obligation_acquisition_mapping.
    for entity_act in build_1099int_report_entity_acts(
        payer_name=PAYER_NAME,
        statement_reference=STATEMENT_REFERENCE,
        act_index=len(acts),
    ):
        acts.append(entity_act)

    # --- Ordinary side: three genuinely distinct obligations from this
    # same payer (A and B will both be attested against the one report
    # below; C never is).
    for obligation_reference in (
        OBLIGATION_REFERENCE_A,
        OBLIGATION_REFERENCE_B,
        OBLIGATION_REFERENCE_C,
        OBLIGATION_REFERENCE_D,
    ):
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": derive_obligation_entity_id(
                        payer_name=PAYER_NAME,
                        obligation_reference=obligation_reference,
                        obligation_description=f"synthetic obligation ({obligation_reference})",
                    ),
                    "kind": "tax.us.interest-obligation",
                    "label": f"Synthetic obligation {obligation_reference}",
                }
            },
        )

    add(
        "evidence-submitted",
        {
            "evidence": demo_evidence(
                "demo.evidence.report.t8-live",
                "Synthetic Form 1099-INT (T8 live, aggregating two obligations)",
                {"mode": "document-report-entry", "synthetic": True},
            )
        },
    )

    schemas = DerivationSchemas()
    for index, act in enumerate(acts):
        act["committed_against"] = index
        act["act_id"] = f"demo.t8-live.act.{index:03d}"
        act["actor"] = USER
    state = project(tuple(dict(act) for act in acts), schemas.registry)

    # --- Contribute the documentary report through the real, independent,
    # minimal report-contribution path.
    report_admitted = contribute_1099int_report(
        state,
        payer_name=PAYER_NAME,
        statement_reference=STATEMENT_REFERENCE,
        tax_year=2025,
        amount=REPORT_AMOUNT,
        scope={"tax-year": "2025", "subject": "demo.primary"},
        family_predecessor_id=FAMILY_PREDECESSOR,
        family_successor_id=FAMILY_SUCCESSOR,
        registry=schemas.registry,
        record_id="demo.crec.report.t8-live",
        act_index=len(acts),
        contribution_id="demo.contribution.report.t8-live",
        evidence_id="demo.evidence.report.t8-live",
        finding_id="demo.finding.box1.t8-live",
        committed_against=len(acts),
    )
    if report_admitted.terminal_record.get("phase") != "completed":
        raise AssertionError(f"1099-INT report was not admitted: {report_admitted.terminal_record}")
    state = report_admitted.state

    report_built = build_1099int_report_contribution(
        payer_name=PAYER_NAME,
        statement_reference=STATEMENT_REFERENCE,
        tax_year=2025,
        amount=REPORT_AMOUNT,
        scope={"tax-year": "2025", "subject": "demo.primary"},
        family_predecessor_id=FAMILY_PREDECESSOR,
        family_successor_id=FAMILY_SUCCESSOR,
        act_index=len(acts),
        contribution_id="demo.contribution.report.t8-live",
        evidence_id="demo.evidence.report.t8-live",
        finding_id="demo.finding.box1.t8-live",
        committed_against=len(acts),
    )
    for extra in (report_built.contribution_act, report_built.member_transition_act):
        extra["actor"] = USER
        acts.append(extra)

    add(
        "assertion",
        {
            "finding": _attested(
                "demo.t8-live.closure.int-b1",
                f"tax.us.2025.f1099int.b1.source-closure|family-horizon={FAMILY_SUCCESSOR},tax-year=2025",
                True,
            )
        },
    )

    for index, act in enumerate(acts):
        act["committed_against"] = index
        act["act_id"] = f"demo.t8-live.act.{index:03d}"
        act["actor"] = USER
    state = project(tuple(dict(act) for act in acts), schemas.registry)

    # --- Ordinary side: acquisitions A and B, both attested against the
    # one shared report (proving the statement-narrowed tier's mandatory
    # confirmation, which now also names its target -- the same shared
    # report's own fact id, uniformly required at both tiers); acquisition
    # C never attested to it, on the coarse (no statement reference) tier;
    # acquisition D names the correct statement reference but withholds
    # confirmation, on the statement-narrowed tier -- proving that a
    # statement match alone, even naming the right report, is not
    # sufficient without the person's own attestation.
    shared_report_fact_id = derive_1099int_box1_fact_id(
        payer_name=PAYER_NAME, statement_reference=STATEMENT_REFERENCE, tax_year=2025
    )
    for obligation_reference, accrued, statement_reference, confirmed, confirmed_target, tag in (
        (OBLIGATION_REFERENCE_A, ACCRUED_A, STATEMENT_REFERENCE, True, shared_report_fact_id, "a"),
        (OBLIGATION_REFERENCE_B, ACCRUED_B, STATEMENT_REFERENCE, True, shared_report_fact_id, "b"),
        (OBLIGATION_REFERENCE_C, ACCRUED_C, None, False, None, "c"),
        (OBLIGATION_REFERENCE_D, ACCRUED_D, STATEMENT_REFERENCE, False, None, "d"),
    ):
        answers = _acquisition_answers(
            obligation_reference=obligation_reference,
            accrued=accrued,
            statement_reference=statement_reference,
            confirmed=confirmed,
        )
        evidence_id = f"demo.evidence.acq.t8-live.{tag}"
        add(
            "evidence-submitted",
            {
                "evidence": demo_evidence(
                    evidence_id,
                    f"Synthetic ordinary-language acquisition interview ({tag})",
                    {"mode": "ordinary-language-entry", "synthetic": True},
                )
            },
        )
        for index, act in enumerate(acts):
            act["committed_against"] = index
            act["act_id"] = f"demo.t8-live.act.{index:03d}"
            act["actor"] = USER
        state = project(tuple(dict(act) for act in acts), schemas.registry)

        admitted = contribute_ordinary_acquisition(
            state,
            answers,
            registry=schemas.registry,
            record_id=f"demo.crec.acq.t8-live.{tag}",
            act_index=len(acts),
            contribution_id=f"demo.contribution.acq.t8-live.{tag}",
            evidence_id=evidence_id,
            finding_id=f"demo.finding.acq.t8-live.{tag}",
            committed_against=len(acts),
            confirmed_report_fact_id=confirmed_target,
        )
        if admitted.terminal_record.get("phase") != "completed":
            raise AssertionError(f"ordinary acquisition {tag!r} was not admitted: {admitted.terminal_record}")
        state = admitted.state

        built = build_ordinary_acquisition_contribution(
            answers,
            act_index=len(acts),
            contribution_id=f"demo.contribution.acq.t8-live.{tag}",
            evidence_id=evidence_id,
            finding_id=f"demo.finding.acq.t8-live.{tag}",
            committed_against=len(acts),
            confirmed_report_fact_id=confirmed_target,
        )
        for extra in (built.contribution_act, built.assertion_act):
            extra["actor"] = USER
            acts.append(extra)

    adoption = cast(
        dict[str, Any],
        json.loads(
            (ROOT / "packages" / "sample_data" / "package_membership_wiring" / "adoptions" / "adopt-core-v34-current.json").read_text(
                "utf-8"
            )
        ),
    )
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    for index, act in enumerate(acts):
        act["committed_against"] = index
        act["act_id"] = f"demo.t8-live.act.{index:03d}"
        act["actor"] = USER
    return acts


class LiveT8SharedReportSelectsByAttestation(unittest.TestCase):
    def test_two_attested_obligations_associate_two_unconfirmed_do_not(self) -> None:
        acts = _t8_acts()
        with TemporaryDirectory() as tmp:
            result = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"),
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="demo.run.t8-live.selection",
                governance_pins=[],
                surface=_surface(),
                output_name="out.json",
            )
            self.assertIsNone(result.refusal, result.refusal)
            report = json.loads(cast(Path, result.output_path).read_text("utf-8"))
            publications = tuple(result.publications or ())

        def by_prefix(prefix: str) -> list[dict[str, Any]]:
            return [pub.finding for pub in publications if str(pub.finding.get("symbol", "")).startswith(prefix)]

        expected_fact_id = (
            f"{REPORT_FACT_TYPE}|payer={derive_reported_payer_entity_id(PAYER_NAME)},"
            f"statement={derive_reported_statement_entity_id(payer_name=PAYER_NAME, statement_reference=STATEMENT_REFERENCE)},"
            "tax-year=2025"
        )

        # (a) and (b): both attested acquisitions associate with the one
        # shared report -- proving canonical identity (the person's own
        # attestation) selects the specific item, not any automatic signal.
        pairings = by_prefix(ASSOCIATION_SYMBOL)
        self.assertEqual(len(pairings), 2, pairings)
        self.assertTrue(all(p["value"]["right_fact_id"] == expected_fact_id for p in pairings), pairings)

        current_year = by_prefix(CURRENT_YEAR_SYMBOL_PREFIX + "|")
        basis = by_prefix(BASIS_SYMBOL_PREFIX + "|")
        self.assertEqual(len(current_year), 2, current_year)
        self.assertEqual(len(basis), 2, basis)
        self.assertEqual(
            sorted(finding["value"] for finding in current_year),
            sorted([str(ACCRUED_A), str(ACCRUED_B)]),
        )

        # (c): the third acquisition names the same payer and shares the
        # same statement/account (via the coarse payer+year tier -- it
        # supplies no statement reference at all), but was never attested
        # to this report -- it must not silently join it. It refuses
        # ASSOCIATION_UNCONFIRMED, not associate.
        #
        # (d): the fourth acquisition names the *correct* statement
        # reference -- the statement-narrowed tier resolves it to exactly
        # this one report -- but withholds confirmation. A statement match
        # alone, even the right one, is not sufficient. It too refuses
        # ASSOCIATION_UNCONFIRMED rather than silently joining.
        dispositions = report.get("dispositions", [])
        unconfirmed = [row for row in dispositions if row.get("code") == ASSOCIATION_UNCONFIRMED]
        self.assertEqual(len(unconfirmed), 2, dispositions)
        for row in unconfirmed:
            (candidate,) = row["missing"]
            self.assertEqual(candidate, expected_fact_id)

        self.assertFalse(
            any(row.get("code") == ASSOCIATION_AMBIGUOUS for row in dispositions),
            dispositions,
        )
        # Only two pairings ever publish -- neither unconfirmed acquisition
        # contributes a current-year or basis finding of its own.
        published_current_year_values = {finding["value"] for finding in current_year}
        self.assertNotIn(str(ACCRUED_C), published_current_year_values)
        self.assertNotIn(str(ACCRUED_D), published_current_year_values)


if __name__ == "__main__":
    unittest.main()
