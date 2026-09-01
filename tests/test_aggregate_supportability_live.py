"""Aggregate supportability, through real package resolution.

The rule citizen
``rule.interest.current-year-adjustment.aggregate-supportability`` must be a
real member of an adopted production package, reachable through
``live_coordinate_run`` — not only exercised by
``tests.test_pairing_consequences`` manually constructing a ``RunContext``
and injecting the rule directly. This reproduces the exact masked-overclaim scenario ADR-0070 names (report
``500``, two genuinely-associated ``300`` acquisitions, one unrelated
``200`` report) through ``live_coordinate_run`` against the real,
checksum-published ``package.core-calculations.v34`` — proving the
aggregate check actually fires and blocks through production package
resolution, not only the isolated ``_execute``-level harness.
"""

from __future__ import annotations

import json
import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    load_published_citizen_checksums,
    package_instance_checksum,
    validate_package,
)
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.findings import project
from packages.tax.identity_association import ASSOCIATION_SYMBOL, REPORT_FACT_TYPE
from packages.tax.loader import TAX_CONTENT_DIR
from packages.tax.obligation_acquisition_mapping import (
    build_ordinary_acquisition_contribution,
    contribute_ordinary_acquisition,
    derive_obligation_entity_id,
    derive_reported_statement_entity_id,
)
from packages.tax.pairing_consequences import (
    AGGREGATE_ACCRUED_EXCEEDS_REPORT,
    AGGREGATE_SUPPORTABILITY_RULE_ID,
    AGGREGATE_SUPPORTABILITY_SYMBOL_PREFIX,
    CURRENT_YEAR_RULE_ID,
    CURRENT_YEAR_SUBTOTAL_RULE_ID,
    CURRENT_YEAR_SUBTOTAL_SYMBOL,
    CURRENT_YEAR_SYMBOL_PREFIX,
)
from tests.support import demo_evidence
from tests.test_f1098e_student_loan_interest_agi_track6 import _f1098e_acts
from tests.test_form1099g_box1_schedule1_line7 import _act, _attested
from tests.test_package_membership_wiring import ROOT, SCOPE, USER, _load
from tests.test_ssa1099_benefits_line6_track2 import SCOPE_KEY

CONTENT = TAX_CONTENT_DIR
FIXTURES = ROOT / "packages" / "sample_data" / "package_membership_wiring"

PACKAGE_FILE = "package.core-calculations.v34.json"
REGISTRY_FILE = "published-packages.v29.json"
RELEASE_FILE = "demo.release.2025.v27.json"
ADOPTION_FILE = "adopt-core-v34-current.json"

PAYER_MAIN = "demo.payer.agg-live-main"
STATEMENT_REFERENCE_MAIN = "ACCOUNT-REF-AGG-LIVE-MAIN"
PAYER_UNRELATED = "demo.payer.agg-live-unrelated"
STATEMENT_UNRELATED_ID = "demo.1099int-statement.agg-live-unrelated"


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / REGISTRY_FILE,
        CONTENT,
    )


def _load_adoption() -> dict[str, Any]:
    return cast(
        dict[str, Any],
        json.loads((FIXTURES / "adoptions" / ADOPTION_FILE).read_text("utf-8")),
    )


def _answers(
    *, obligation_reference: str, reported_statement_reference: str | None,
    accrued: float, payer: str = PAYER_MAIN, confirmed_report_match: bool = False,
) -> dict[str, Any]:
    return {
        "payer_name": payer,
        "obligation_description": f"synthetic municipal bond series demo-2025 ({obligation_reference})",
        "obligation_reference": obligation_reference,
        "acquisition_date": "2025-03-14",
        "accrued_interest_paid_to_seller": accrued,
        "currency": "USD",
        "reported_statement_reference": reported_statement_reference,
        "confirmed_report_match": confirmed_report_match,
    }


def _aggregate_overclaim_acts() -> list[dict[str, object]]:
    """One report of 500 (two genuinely-associated 300 acquisitions sharing
    a reported statement reference) and one unrelated report of 200 (one
    50 acquisition), all under the real ``obligation-acquisition.bundle``
    entity-kind identity — ADR-0070's exact masked-overclaim scenario.

    Every acquisition below must name the report its
    ``confirmed_report_match: true`` confirms, uniformly at both tiers. The
    vocabulary a workspace adopts (this ``bundle-adoption``
    act) and the rule package it separately adopts (still v34, below) are
    independent axes — bumping the former does not change which rule
    package this reproduction dispatches through."""
    acts = _f1098e_acts(statements=[], close=True, wages=90000)
    acts.pop()  # drop the v33 Track-6 adoption

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("obligation-acquisition.bundle.json")})

    statement_main = derive_reported_statement_entity_id(
        payer_name=PAYER_MAIN, reported_statement_reference=STATEMENT_REFERENCE_MAIN
    )
    assert statement_main is not None

    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": PAYER_MAIN,
                "kind": "tax.us.interest-payer",
                "label": "Synthetic aggregate-live main payer",
            }
        },
    )
    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": statement_main,
                "kind": "tax.us.1099int-statement",
                "label": "Synthetic aggregate-live shared statement",
            }
        },
    )
    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": derive_obligation_entity_id(
                    payer_name=PAYER_MAIN,
                    obligation_reference="DEMO-BOND-AGG-LIVE-A",
                    obligation_description="synthetic municipal bond series demo-2025 (DEMO-BOND-AGG-LIVE-A)",
                ),
                "kind": "tax.us.interest-obligation",
                "label": "Synthetic obligation A",
            }
        },
    )
    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": derive_obligation_entity_id(
                    payer_name=PAYER_MAIN,
                    obligation_reference="DEMO-BOND-AGG-LIVE-B",
                    obligation_description="synthetic municipal bond series demo-2025 (DEMO-BOND-AGG-LIVE-B)",
                ),
                "kind": "tax.us.interest-obligation",
                "label": "Synthetic obligation B",
            }
        },
    )
    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": PAYER_UNRELATED,
                "kind": "tax.us.interest-payer",
                "label": "Synthetic aggregate-live unrelated payer",
            }
        },
    )
    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": STATEMENT_UNRELATED_ID,
                "kind": "tax.us.1099int-statement",
                "label": "Synthetic aggregate-live unrelated statement",
            }
        },
    )
    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": derive_obligation_entity_id(
                    payer_name=PAYER_UNRELATED,
                    obligation_reference="DEMO-BOND-AGG-LIVE-U",
                    obligation_description="synthetic municipal bond series demo-2025 (DEMO-BOND-AGG-LIVE-U)",
                ),
                "kind": "tax.us.interest-obligation",
                "label": "Synthetic unrelated obligation",
            }
        },
    )

    main_fact_id = f"{REPORT_FACT_TYPE}|payer={PAYER_MAIN},statement={statement_main},tax-year=2025"
    unrelated_fact_id = (
        f"{REPORT_FACT_TYPE}|payer={PAYER_UNRELATED},statement={STATEMENT_UNRELATED_ID},tax-year=2025"
    )
    add(
        "member-transition",
        {
            "family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {
                "action": "assert",
                "finding": _attested("demo.agg-live.finding.box1.main", main_fact_id, 500.0),
            },
            "successor": {"id": "demo.agg-live.int-b1.h1", "predecessor": "demo.cgd.t2.int-b1.h0"},
        },
    )
    add(
        "member-transition",
        {
            "family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {
                "action": "assert",
                "finding": _attested("demo.agg-live.finding.box1.unrelated", unrelated_fact_id, 200.0),
            },
            "successor": {"id": "demo.agg-live.int-b1.h2", "predecessor": "demo.agg-live.int-b1.h1"},
        },
    )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.agg-live.closure.int-b1",
                "tax.us.2025.f1099int.b1.source-closure|family-horizon=demo.agg-live.int-b1.h2,tax-year=2025",
                True,
            )
        },
    )

    evidence = demo_evidence(
        "demo.evidence.acq.agg-live",
        "Synthetic ordinary-language acquisition interview (aggregate-live)",
        {"mode": "ordinary-language-entry", "synthetic": True},
    )
    add("evidence-submitted", {"evidence": evidence})

    schemas = DerivationSchemas()
    answers_by_id = {
        "a": _answers(
            obligation_reference="DEMO-BOND-AGG-LIVE-A",
            reported_statement_reference=STATEMENT_REFERENCE_MAIN,
            accrued=300.0,
            confirmed_report_match=True,
        ),
        "b": _answers(
            obligation_reference="DEMO-BOND-AGG-LIVE-B",
            reported_statement_reference=STATEMENT_REFERENCE_MAIN,
            accrued=300.0,
            confirmed_report_match=True,
        ),
        "u": _answers(
            obligation_reference="DEMO-BOND-AGG-LIVE-U",
            reported_statement_reference=None,
            accrued=50.0,
            payer=PAYER_UNRELATED,
            confirmed_report_match=True,
        ),
    }
    # A confirmation must name the report it confirms uniformly at both
    # tiers: "u" confirms on the coarse tier (no statement reference); "a"
    # and "b" confirm on the statement-narrowed tier -- both name their own
    # target explicitly.
    targets_by_id = {"a": main_fact_id, "b": main_fact_id, "u": unrelated_fact_id}

    for tag, answers in answers_by_id.items():
        for index, act in enumerate(acts):
            act["committed_against"] = index
            act["act_id"] = f"demo.agg-live.act.{index:03d}"
            act["actor"] = USER
        base = project(tuple(dict(act) for act in acts), schemas.registry)
        admitted = contribute_ordinary_acquisition(
            base,
            answers,
            registry=schemas.registry,
            record_id=f"demo.crec.acq.agg-live.{tag}",
            act_index=len(acts),
            contribution_id=f"demo.contribution.acq.agg-live.{tag}",
            evidence_id="demo.evidence.acq.agg-live",
            finding_id=f"demo.finding.acq.agg-live.{tag}",
            committed_against=len(acts),
            confirmed_report_fact_id=targets_by_id.get(tag),
        )
        if admitted.terminal_record.get("phase") != "completed":
            raise AssertionError(f"ordinary acquisition {tag} was not admitted: {admitted.terminal_record}")
        built = build_ordinary_acquisition_contribution(
            answers,
            act_index=len(acts),
            contribution_id=f"demo.contribution.acq.agg-live.{tag}",
            evidence_id="demo.evidence.acq.agg-live",
            finding_id=f"demo.finding.acq.agg-live.{tag}",
            committed_against=len(acts),
            confirmed_report_fact_id=targets_by_id.get(tag),
        )
        for extra in (built.contribution_act, built.assertion_act):
            extra["actor"] = USER
            acts.append(extra)

    adoption = _load_adoption()
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    for index, act in enumerate(acts):
        act["committed_against"] = index
        act["act_id"] = f"demo.agg-live.act.{index:03d}"
        act["actor"] = USER
    return acts


class AggregateSupportabilityPackageV34(unittest.TestCase):
    def test_v34_admits_the_rule_and_validates(self) -> None:
        pkg = _load(PACKAGE_FILE)
        self.assertEqual(pkg["version"], "v34")
        self.assertEqual(pkg["package_checksum"], package_instance_checksum(pkg))
        members = {(m["id"], m["version"]) for m in pkg["members"]}
        self.assertIn((AGGREGATE_SUPPORTABILITY_RULE_ID, "v1"), members)
        entrypoints = {(e["id"], e["version"]) for e in pkg["entrypoints"]}
        self.assertIn((AGGREGATE_SUPPORTABILITY_RULE_ID, "v1"), entrypoints)

        corpus: dict[tuple[str, str], dict[str, Any]] = {}
        for path in CONTENT.glob("*.json"):
            try:
                value = json.loads(path.read_text("utf-8"))
            except Exception:
                continue
            if isinstance(value, dict) and isinstance(value.get("id"), str) and isinstance(
                value.get("version"), str
            ):
                corpus[(value["id"], value["version"])] = value
        loaded_members = {
            (m["id"], m["version"]): corpus[(m["id"], m["version"])] for m in pkg["members"]
        }
        result = validate_package(
            pkg,
            loaded_members,
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / REGISTRY_FILE),
        )
        self.assertTrue(result.ok, result.issues)

    def test_v33_still_does_not_admit_it(self) -> None:
        """v34 is additive, not a rewrite of v33's own bytes."""
        pkg = _load("package.core-calculations.v33.json")
        members = {(m["id"], m["version"]) for m in pkg["members"]}
        self.assertNotIn((AGGREGATE_SUPPORTABILITY_RULE_ID, "v1"), members)


class LiveAggregateOverclaimReproduction(unittest.TestCase):
    """Findings 3 and 6, through real package resolution."""

    def test_published_v34_package_blocks_the_masked_overclaim(self) -> None:
        acts = _aggregate_overclaim_acts()
        with TemporaryDirectory() as tmp:
            result = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"),
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="demo.run.aggregate-live.overclaim",
                governance_pins=[],
                surface=_surface(),
                output_name="out.json",
            )
            self.assertIsNone(result.refusal, result.refusal)
            self.assertIsNotNone(result.output_path)
            report = json.loads(cast(Path, result.output_path).read_text("utf-8"))
            publications = tuple(result.publications or ())

        def by_prefix(prefix: str) -> list[dict[str, Any]]:
            return [
                pub.finding
                for pub in publications
                if str(pub.finding.get("symbol", "")).startswith(prefix)
            ]

        pairings = by_prefix(ASSOCIATION_SYMBOL)
        self.assertEqual(len(pairings), 3, pairings)

        # The aggregate check fires through real package resolution and
        # blocks the shared-report group, named exactly.
        aggregate_blocks = [
            row
            for row in report.get("dispositions", [])
            if row.get("artifact_id") == AGGREGATE_SUPPORTABILITY_RULE_ID
            and row.get("disposition") == "blocked"
        ]
        self.assertEqual(len(aggregate_blocks), 1, aggregate_blocks)
        self.assertEqual(aggregate_blocks[0]["code"], AGGREGATE_ACCRUED_EXCEEDS_REPORT)

        aggregate_publications = by_prefix(AGGREGATE_SUPPORTABILITY_SYMBOL_PREFIX + "|")
        self.assertEqual(len(aggregate_publications), 1, aggregate_publications)
        self.assertIs(aggregate_publications[0]["value"], True)

        # The blocked group's two per-pairing findings are retracted from
        # ordinary publication -- only the unrelated 50 remains presented
        # as ordinarily supported.
        current_year = by_prefix(CURRENT_YEAR_SYMBOL_PREFIX + "|")
        self.assertEqual(len(current_year), 1, current_year)
        self.assertEqual(Decimal(str(current_year[0]["value"])), Decimal("50.0"))
        retracted = [
            row
            for row in report.get("dispositions", [])
            if row.get("artifact_id") == CURRENT_YEAR_RULE_ID
            and row.get("disposition") == "blocked"
            and row.get("code") == AGGREGATE_ACCRUED_EXCEEDS_REPORT
        ]
        self.assertEqual(len(retracted), 2, retracted)

        # The subtotal does not quietly publish a different,
        # confidently-presented number -- it blocks, named the same way.
        self.assertNotIn(
            CURRENT_YEAR_SUBTOTAL_SYMBOL,
            {pub.finding.get("symbol") for pub in publications},
        )
        subtotal_blocks = [
            row
            for row in report.get("dispositions", [])
            if row.get("artifact_id") == CURRENT_YEAR_SUBTOTAL_RULE_ID
            and row.get("disposition") == "blocked"
        ]
        self.assertEqual(len(subtotal_blocks), 1, subtotal_blocks)
        self.assertEqual(subtotal_blocks[0]["code"], AGGREGATE_ACCRUED_EXCEEDS_REPORT)


if __name__ == "__main__":
    unittest.main()
