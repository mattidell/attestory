"""Seam 2 — Acquisition-to-report identity association (ADR-0068).

Synthetic in-repo fixtures only. Proves the production pairing producer:

- one match publishes a ``derived-finding.v2`` with exact provenance pins
  to both source finding ids;
- no match publishes nothing;
- several matches refuse ``ASSOCIATION_AMBIGUOUS``, naming every candidate
  fact id, and never silently associate;
- a correction to either source fact re-evaluates (derive, don't cache);
- adding a second candidate report displaces an existing association into
  ambiguity; removing it republishes the same content-addressed record;
- two acquisitions under the same payer against two reports are not
  greedily paired or collapsed (multi-acquisition scale).

Source findings are marshaled through the real ``marshal_run_context``
collect path. Published records are validated against the real
``derived-finding.v2`` schema. Fact-type ids are the production
vocabulary (box 1 from ``f1099int.bundle.json``; acquisition from
Seam 6), not the spike's unchecked copies.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any

import jsonschema

from packages.derivation.declarative_validation import identity_tuple
from packages.derivation.loader import DerivationSchemas
from packages.derivation.marshal import marshal_run_context
from packages.derivation.runner import RunContext
from packages.derivation.runner import run as runner_run
from packages.kernel.currency import CurrencyView
from packages.kernel.facts import fact_id_for
from packages.kernel.schema_registry import SchemaValidationError
from packages.tax.identity_association import (
    ACQUISITION_FACT_TYPE,
    ASSOCIATION_AMBIGUOUS,
    ASSOCIATION_SYMBOL,
    ASSOCIATION_UNCONFIRMED,
    LEFT_COMPONENTS,
    REPORT_FACT_TYPE,
    RIGHT_COMPONENTS,
    AssocResult,
    associate,
)
from packages.tax.obligation_acquisition_mapping import (
    OBLIGATION_ACQUISITION_FACT_TYPE_ID,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "packages" / "sample_data" / "identity_association"
BOX1_BUNDLE = (
    REPO_ROOT / "packages" / "content" / "tax" / "2025" / "f1099int.bundle.json"
)
ACQUISITION_BUNDLE = (
    REPO_ROOT / "packages" / "content" / "tax" / "2025" / "obligation-acquisition.bundle.json"
)
PUBLISHED_DERIVATION = (
    REPO_ROOT / "packages" / "schemas" / "derivation" / "published.json"
)

ADOPTION_PIN = {
    "role": "adoption",
    "id": "demo.package.identity-association",
    "version": "v1",
}


class _HorizonState:
    def __init__(self) -> None:
        self.current_by_chain: dict[tuple[str, str, str], str] = {}


class _State:
    """Minimal FindingState stand-in; marshal_run_context only reads
    ``.findings`` and ``.horizon_state.current_by_chain``."""

    def __init__(self, findings: dict[str, dict[str, Any]]) -> None:
        self.findings = findings
        self.horizon_state = _HorizonState()


def _load(path: Path) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return loaded


def _currency(finding_ids: list[str]) -> CurrencyView:
    ids = frozenset(finding_ids)
    return CurrencyView(
        current_finding_ids=ids,
        displaced_finding_ids=frozenset(),
        current_evidence_ids=frozenset(),
        displaced_evidence_ids=frozenset(),
    )


def _sources_for(findings: dict[str, dict[str, Any]]) -> list[Any]:
    state = _State(findings)
    currency = _currency(list(findings.keys()))
    ctx = marshal_run_context(
        run_id="demo.run.identity-association",
        state=state,  # type: ignore[arg-type]
        currency=currency,
        rules=[],
        parameters={},
        canon={},
        adoption_pin=ADOPTION_PIN,
        governance_pins=[],
        collect_source_names=[ACQUISITION_FACT_TYPE, REPORT_FACT_TYPE],
    )
    return ctx.sources


# Every fixture in this file's own reports are for tax-year 2025; this
# module's ``reporting_year`` is always sourced from the run's own
# ``run_scope`` in production (never from the acquisition's own answers),
# so most tests here just supply the one reporting-year context the
# fixtures were built under. Tests that specifically exercise
# ``reporting_year``'s own behavior pass it explicitly.
_DEFAULT_REPORTING_YEAR = 2025


def _associate(
    findings: dict[str, dict[str, Any]], *, reporting_year: int | None = _DEFAULT_REPORTING_YEAR
) -> AssocResult:
    return associate(
        sources=_sources_for(findings),
        registry=DerivationSchemas().registry,
        adoption_pin=ADOPTION_PIN,
        reporting_year=reporting_year,
    )


def _example(name: str) -> dict[str, Any]:
    return _load(FIXTURES / "examples" / name)


def _negative(name: str) -> dict[str, Any]:
    return _load(FIXTURES / "negatives" / name)


def _pin_ids(finding: dict[str, Any]) -> set[tuple[str, str]]:
    return {(p["role"], p["id"]) for p in finding["pins"]}


class TestProductionSchemaIds(unittest.TestCase):
    """Spike fixture ids re-validated against committed production content."""

    def test_report_type_is_the_published_box1_fact_type(self) -> None:
        bundle = _load(BOX1_BUNDLE)
        ids = {ft["id"] for ft in bundle["fact_types"]}
        self.assertIn(REPORT_FACT_TYPE, ids)
        box1 = next(ft for ft in bundle["fact_types"] if ft["id"] == REPORT_FACT_TYPE)
        key_names = [k["name"] for k in box1["identity_keys"]]
        self.assertEqual(key_names, ["payer", "statement", "tax-year"])

    def test_acquisition_type_is_seam6_circumstance(self) -> None:
        self.assertEqual(ACQUISITION_FACT_TYPE, OBLIGATION_ACQUISITION_FACT_TYPE_ID)

    def test_derived_finding_v2_is_the_published_finding_schema(self) -> None:
        manifest = _load(PUBLISHED_DERIVATION)
        self.assertIn("derived-finding.v2.schema.json", manifest)

    def test_fixture_fact_ids_compose_from_production_types(self) -> None:
        a1 = _example("finding.v2.acquisition-a1.json")
        r1 = _example("finding.v2.box1-s1.json")
        self.assertEqual(
            a1["fact_id"],
            fact_id_for(
                ACQUISITION_FACT_TYPE,
                (
                    ("payer", "demo.payer.bank-a"),
                    ("reference", "DEMO-BOND-001"),
                    ("acquisition-year", "2025"),
                ),
            ),
        )
        self.assertEqual(
            r1["fact_id"],
            fact_id_for(
                REPORT_FACT_TYPE,
                (
                    ("payer", "demo.payer.bank-a"),
                    ("statement", "demo.1099int-statement.s1"),
                    ("tax-year", "2025"),
                ),
            ),
        )
        self.assertTrue(a1["fact_id"].startswith(ACQUISITION_FACT_TYPE + "|"))
        self.assertTrue(r1["fact_id"].startswith(REPORT_FACT_TYPE + "|"))


class TestPayloadInstantiation(unittest.TestCase):
    """Hand-written positive/negative payloads against production schemas."""

    def setUp(self) -> None:
        self.registry = DerivationSchemas().registry

    def test_positive_source_findings_validate_as_finding_v2(self) -> None:
        for name in (
            "finding.v2.acquisition-a1.json",
            "finding.v2.acquisition-a2.json",
            "finding.v2.box1-s1.json",
            "finding.v2.box1-s2.json",
        ):
            payload = _example(name)
            self.registry.validate("finding.v2", payload)

    def test_positive_acquisition_findings_validate_against_the_real_circumstance_schema(
        self,
    ) -> None:
        """``finding.v2`` alone is only the generic envelope -- it has no
        visibility into a circumstance-specific value shape. The real
        admission boundary (``packages.kernel.findings.apply_act``, via
        ``_validate_finding``) additionally validates a finding's ``value``
        against its own fact type's ``value_schema``
        (``obligation_acquisition_mapping._CIRCUMSTANCE_VALUE_SCHEMA`` for
        this circumstance, including the ``confirmed_report_match: true``
        requires-``confirmed_report_fact_id`` conditional). Every committed
        acquisition fixture must be schema-valid there too, not merely
        against the generic envelope -- this is what would have caught a
        fixture asserting ``confirmed_report_match: true`` with no recorded
        target."""
        from packages.tax.obligation_acquisition_mapping import (
            _CIRCUMSTANCE_VALUE_SCHEMA,
        )

        validator = jsonschema.Draft202012Validator(_CIRCUMSTANCE_VALUE_SCHEMA)
        for name in ("finding.v2.acquisition-a1.json", "finding.v2.acquisition-a2.json"):
            payload = _example(name)
            errors = list(validator.iter_errors(payload["value"]))
            self.assertEqual(errors, [], f"{name}: {[e.message for e in errors]}")

    def test_positive_association_payload_validates_as_derived_finding_v2(self) -> None:
        payload = _example("derived-finding.v2.one-match.json")
        self.registry.validate("derived-finding.v2", payload)
        self.assertEqual(payload["schema"], "derived-finding.v2")
        input_pins = [p for p in payload["pins"] if p["role"] == "input"]
        self.assertEqual(
            {p["id"] for p in input_pins},
            {"demo.finding.acq.a1", "demo.finding.box1.s1"},
        )
        for pin in input_pins:
            self.assertEqual(pin["origin"], "assertion")

    def test_input_pin_without_origin_is_rejected(self) -> None:
        payload = _negative("derived-finding.v2.input-without-origin.json")
        with self.assertRaises(SchemaValidationError):
            self.registry.validate("derived-finding.v2", payload)

    def test_one_sided_pins_are_schema_legal_but_not_a_producer_record(self) -> None:
        """Candidate A's pin gap: schema allows a single input pin; the
        producer must never emit that shape (ADR-0068 Decision 5)."""
        payload = _negative("derived-finding.v2.one-sided-pins.json")
        self.registry.validate("derived-finding.v2", payload)
        a1 = _example("finding.v2.acquisition-a1.json")
        r1 = _example("finding.v2.box1-s1.json")
        result = _associate({a1["id"]: a1, r1["id"]: r1})
        self.assertEqual(len(result.publications), 1)
        input_pins = [
            p for p in result.publications[0]["pins"] if p["role"] == "input"
        ]
        self.assertEqual(
            {p["id"] for p in input_pins},
            {a1["id"], r1["id"]},
        )


class TestOneMatch(unittest.TestCase):
    def test_publishes_pairing_with_exact_provenance(self) -> None:
        a1 = _example("finding.v2.acquisition-a1.json")
        r1 = _example("finding.v2.box1-s1.json")
        result = _associate({a1["id"]: a1, r1["id"]: r1})
        self.assertEqual(result.refusals, ())
        self.assertEqual(len(result.publications), 1)
        assoc = result.publications[0]
        self.assertEqual(assoc["schema"], "derived-finding.v2")
        self.assertEqual(
            assoc["value"],
            {"left_fact_id": a1["fact_id"], "right_fact_id": r1["fact_id"]},
        )
        self.assertEqual(
            assoc["symbol"],
            f"{ASSOCIATION_SYMBOL}|{a1['fact_id']}",
        )
        self.assertIn(("input", a1["id"]), _pin_ids(assoc))
        self.assertIn(("input", r1["id"]), _pin_ids(assoc))
        self.assertIn(("adoption", ADOPTION_PIN["id"]), _pin_ids(assoc))
        for pin in assoc["pins"]:
            self.assertLessEqual(set(pin.keys()), {"role", "id", "version", "origin"})
            if pin["role"] == "input":
                self.assertEqual(pin.get("origin"), "assertion")
            else:
                self.assertNotIn("origin", pin)


class TestNoMatch(unittest.TestCase):
    def test_publishes_nothing_when_no_report_shares_the_tuple(self) -> None:
        a1 = _example("finding.v2.acquisition-a1.json")
        result = _associate({a1["id"]: a1})
        self.assertEqual(result.publications, ())
        self.assertEqual(result.refusals, ())

    def test_publishes_nothing_when_report_is_a_different_payer(self) -> None:
        a1 = _example("finding.v2.acquisition-a1.json")
        other = dict(_example("finding.v2.box1-s1.json"))
        other["id"] = "demo.finding.box1.other-payer"
        other["fact_id"] = fact_id_for(
            REPORT_FACT_TYPE,
            (
                ("payer", "demo.payer.bank-other"),
                ("statement", "demo.1099int-statement.s1"),
                ("tax-year", "2025"),
            ),
        )
        result = _associate({a1["id"]: a1, other["id"]: other})
        self.assertEqual(result.publications, ())
        self.assertEqual(result.refusals, ())


class TestSeveralMatches(unittest.TestCase):
    def test_refuses_naming_every_candidate_and_does_not_guess(self) -> None:
        a1 = _example("finding.v2.acquisition-a1.json")
        r1 = _example("finding.v2.box1-s1.json")
        r2 = _example("finding.v2.box1-s2.json")
        findings = {a1["id"]: a1, r1["id"]: r1, r2["id"]: r2}
        sources = _sources_for(findings)
        box1_sources = [s for s in sources if s.name == REPORT_FACT_TYPE]
        self.assertEqual(len(box1_sources), 2)

        result = associate(
            sources=sources,
            registry=DerivationSchemas().registry,
            adoption_pin=ADOPTION_PIN,
            reporting_year=_DEFAULT_REPORTING_YEAR,
        )
        self.assertEqual(result.publications, ())
        self.assertEqual(len(result.refusals), 1)
        refusal = result.refusals[0]
        self.assertEqual(refusal.code, ASSOCIATION_AMBIGUOUS)
        self.assertEqual(refusal.left_fact_id, a1["fact_id"])
        self.assertEqual(
            set(refusal.candidate_right_fact_ids),
            {r1["fact_id"], r2["fact_id"]},
        )

    def test_set_of_tuples_would_collapse_the_same_inputs(self) -> None:
        """Negative control: Candidate A's ``set`` of identity tuples
        collapses two distinct statement fact ids to one entry."""
        a1 = _example("finding.v2.acquisition-a1.json")
        r1 = _example("finding.v2.box1-s1.json")
        r2 = _example("finding.v2.box1-s2.json")
        sources = _sources_for({a1["id"]: a1, r1["id"]: r1, r2["id"]: r2})
        box1_sources = [s for s in sources if s.name == REPORT_FACT_TYPE]
        own_identities = {
            identity_tuple(
                fact_id=s.fact_id, member_value=None, components=RIGHT_COMPONENTS
            )
            for s in box1_sources
            if s.fact_id is not None
        }
        self.assertEqual(len(box1_sources), 2)
        self.assertEqual(len(own_identities), 1)
        self.assertEqual(
            own_identities,
            {("demo.payer.bank-a",)},
        )


class TestCorrectionReevaluates(unittest.TestCase):
    def test_report_correction_repins_the_new_finding_id(self) -> None:
        a1 = _example("finding.v2.acquisition-a1.json")
        r1 = _example("finding.v2.box1-s1.json")
        before = _associate({a1["id"]: a1, r1["id"]: r1})
        self.assertEqual(len(before.publications), 1)
        before_id = before.publications[0]["id"]
        before_pins = _pin_ids(before.publications[0])

        corrected = dict(r1)
        corrected["id"] = "demo.finding.box1.s1-corrected"
        corrected["value"] = 510.0
        after = _associate({a1["id"]: a1, corrected["id"]: corrected})
        self.assertEqual(len(after.publications), 1)
        assoc = after.publications[0]
        self.assertEqual(
            assoc["value"],
            {"left_fact_id": a1["fact_id"], "right_fact_id": r1["fact_id"]},
        )
        self.assertIn(("input", "demo.finding.box1.s1-corrected"), _pin_ids(assoc))
        self.assertNotIn(("input", r1["id"]), _pin_ids(assoc))
        self.assertNotEqual(assoc["id"], before_id)
        self.assertNotEqual(_pin_ids(assoc), before_pins)

    def test_acquisition_correction_repins_the_new_finding_id(self) -> None:
        a1 = _example("finding.v2.acquisition-a1.json")
        r1 = _example("finding.v2.box1-s1.json")
        before = _associate({a1["id"]: a1, r1["id"]: r1})
        before_id = before.publications[0]["id"]

        corrected = dict(a1)
        corrected["id"] = "demo.finding.acq.a1-corrected"
        value = dict(a1["value"])
        value["accrued_interest_paid_to_seller"] = 45.0
        corrected["value"] = value
        after = _associate({corrected["id"]: corrected, r1["id"]: r1})
        self.assertEqual(len(after.publications), 1)
        assoc = after.publications[0]
        self.assertEqual(assoc["value"]["left_fact_id"], a1["fact_id"])
        self.assertIn(("input", "demo.finding.acq.a1-corrected"), _pin_ids(assoc))
        self.assertNotIn(("input", a1["id"]), _pin_ids(assoc))
        self.assertNotEqual(assoc["id"], before_id)


class TestAddRemoveDisplacement(unittest.TestCase):
    def test_adding_a_second_report_displaces_into_ambiguity(self) -> None:
        a1 = _example("finding.v2.acquisition-a1.json")
        r1 = _example("finding.v2.box1-s1.json")
        r2 = _example("finding.v2.box1-s2.json")
        matched = _associate({a1["id"]: a1, r1["id"]: r1})
        self.assertEqual(len(matched.publications), 1)
        assoc_id = matched.publications[0]["id"]

        displaced = _associate({a1["id"]: a1, r1["id"]: r1, r2["id"]: r2})
        self.assertEqual(displaced.publications, ())
        self.assertEqual(len(displaced.refusals), 1)
        self.assertEqual(displaced.refusals[0].code, ASSOCIATION_AMBIGUOUS)

        restored = _associate({a1["id"]: a1, r1["id"]: r1})
        self.assertEqual(len(restored.publications), 1)
        self.assertEqual(restored.publications[0]["id"], assoc_id)
        self.assertEqual(restored.refusals, ())


class TestConfirmationScopedToNamedReport(unittest.TestCase):
    """A coarse-tier confirmation that names its target report
    (``confirmed_report_fact_id``) must go stale -- refuse
    ``ASSOCIATION_UNCONFIRMED`` -- when the sole coarse-tier candidate
    changes underneath it, rather than silently retargeting onto whatever
    report is sole now. Full lifecycle: S1 confirmed -> S1 removed and
    replaced by S2, same payer/tax-year, acquisition finding unchanged ->
    S2 is the new (and only) sole candidate. Exercised directly against
    ``associate()`` -- an internal unit test of the join/staleness logic,
    not evidence of what real kernel-admitted content can look like.
    """

    def test_confirmed_report_replaced_by_new_sole_candidate_goes_stale(self) -> None:
        a1 = _example("finding.v2.acquisition-a1.json")
        r1 = _example("finding.v2.box1-s1.json")
        r2 = _example("finding.v2.box1-s2.json")

        named = dict(a1)
        value = dict(a1["value"])
        value["confirmed_report_fact_id"] = r1["fact_id"]
        named["value"] = value

        # Stage 1: S1 is the sole coarse-tier candidate and is the report
        # the confirmation actually named. Associates cleanly.
        confirmed = _associate({named["id"]: named, r1["id"]: r1})
        self.assertEqual(confirmed.refusals, ())
        self.assertEqual(len(confirmed.publications), 1)
        self.assertEqual(
            confirmed.publications[0]["value"],
            {"left_fact_id": named["fact_id"], "right_fact_id": r1["fact_id"]},
        )

        # Stage 2: S1 is retired and replaced by S2 (same payer/tax-year,
        # a different statement/report) with no new act on the acquisition
        # side -- the stored confirmation still names S1.
        replaced = _associate({named["id"]: named, r2["id"]: r2})
        self.assertEqual(replaced.publications, ())
        self.assertEqual(len(replaced.refusals), 1)
        refusal = replaced.refusals[0]
        self.assertEqual(refusal.code, ASSOCIATION_UNCONFIRMED)
        self.assertEqual(refusal.left_fact_id, named["fact_id"])
        # Stage 3: S2 is the new, and only, sole candidate -- named as
        # such in the refusal -- but the confirmation naming S1 does not
        # carry over to it.
        self.assertEqual(refusal.candidate_right_fact_ids, (r2["fact_id"],))

    def test_unnamed_confirmation_fails_closed_never_retargets(self) -> None:
        """Negative control, closed. A confirmation that never recorded a
        target at all -- a malformed confirmation, reconstructed here by
        stripping the target from the committed ``acquisition-a1``
        fixture -- must never be honored, at any tier of the coarse-tier
        confirmation lifecycle: it refuses ``ASSOCIATION_UNCONFIRMED`` up
        front, before any report even exists to retarget onto, rather than
        silently retargeting onto whichever report replaces the original."""
        a1 = _example("finding.v2.acquisition-a1.json")
        r1 = _example("finding.v2.box1-s1.json")
        r2 = _example("finding.v2.box1-s2.json")

        unnamed = dict(a1)
        value = dict(a1["value"])
        value.pop("confirmed_report_fact_id", None)
        unnamed["value"] = value
        self.assertNotIn("confirmed_report_fact_id", unnamed["value"])

        # Stage 1: even against the sole candidate it would have matched,
        # an unnamed confirmation no longer associates at all.
        confirmed = _associate({unnamed["id"]: unnamed, r1["id"]: r1})
        self.assertEqual(confirmed.publications, ())
        self.assertEqual(len(confirmed.refusals), 1)
        self.assertEqual(confirmed.refusals[0].code, ASSOCIATION_UNCONFIRMED)
        self.assertEqual(confirmed.refusals[0].left_fact_id, unnamed["fact_id"])
        self.assertEqual(confirmed.refusals[0].candidate_right_fact_ids, (r1["fact_id"],))

        # Stage 2: replacing the sole candidate changes nothing -- there
        # was never a valid association to retarget in the first place.
        replaced = _associate({unnamed["id"]: unnamed, r2["id"]: r2})
        self.assertEqual(replaced.publications, ())
        self.assertEqual(len(replaced.refusals), 1)
        self.assertEqual(replaced.refusals[0].code, ASSOCIATION_UNCONFIRMED)
        self.assertEqual(replaced.refusals[0].candidate_right_fact_ids, (r2["fact_id"],))

    def test_statement_narrowed_confirmation_naming_a_stale_target_refuses(self) -> None:
        """The strict (statement-narrowed) tier enforces the same exact-
        target rule as the coarse tier: a ``confirmed_report_match: true``
        answer alone, without a recorded ``confirmed_report_fact_id``
        naming the current sole candidate, is never sufficient at either
        tier.

        A genuine retire-and-replace lifecycle at a *fixed* reporting-year
        scope cannot change which report is sole under an acquisition's own
        (payer, statement) group key without also changing the acquisition's
        own statement reference (payer/statement/tax-year fully determine a
        report's fact id here), so this constructs the equivalent condition
        directly: the acquisition names a real, currently-sole strict-tier
        candidate via its statement reference, but its own recorded
        ``confirmed_report_fact_id`` names a *different* report entirely
        (as it would after the confirmed report was retired and a
        genuinely different one took its place) -- exactly the shape a
        cross-reporting-year rotation produces at this tier, see
        ``TestReportingYearIsRunScopeNotUserAnswer``."""
        payer = "demo.payer.bank-strict-stale"
        statement_reference = "STMT-STALE"
        statement_entity_id = f"{payer}::statement::{statement_reference}"

        acq_fact_id = fact_id_for(
            ACQUISITION_FACT_TYPE,
            (
                ("payer", payer),
                ("reference", "DEMO-BOND-STALE"),
                ("acquisition-year", "2025"),
            ),
        )
        sole_report_fact_id = fact_id_for(
            REPORT_FACT_TYPE,
            (
                ("payer", payer),
                ("statement", statement_entity_id),
                ("tax-year", "2025"),
            ),
        )
        stale_target_fact_id = fact_id_for(
            REPORT_FACT_TYPE,
            (
                ("payer", payer),
                ("statement", statement_entity_id),
                ("tax-year", "2024"),
            ),
        )
        narrowed: dict[str, Any] = {
            "schema": "finding.v2",
            "id": "demo.finding.acq.strict-stale",
            "fact_id": acq_fact_id,
            "value": {
                "obligation": {
                    "payer_name": payer,
                    "description": "synthetic strict-tier staleness obligation",
                    "reference": "DEMO-BOND-STALE",
                },
                "acquisition_date": "2025-03-14",
                "accrued_interest_paid_to_seller": 42.0,
                "currency": "USD",
                "reported_statement_reference": statement_reference,
                "confirmed_report_match": True,
                # Names a report that is not, and never was, the current
                # strict-tier sole candidate for this acquisition's own
                # statement reference -- exactly what a stale (superseded)
                # target looks like.
                "confirmed_report_fact_id": stale_target_fact_id,
            },
            "basis": "attested",
            "evidence_ids": ["demo.evidence.acq.strict-stale"],
        }
        sole_report: dict[str, Any] = {
            "schema": "finding.v2",
            "id": "demo.finding.box1.strict-stale-sole",
            "fact_id": sole_report_fact_id,
            "value": 500.0,
            "basis": "documentary",
            "evidence_ids": ["demo.evidence.box1.strict-stale-sole"],
        }

        result = _associate({narrowed["id"]: narrowed, sole_report["id"]: sole_report})
        self.assertEqual(result.publications, ())
        self.assertEqual(len(result.refusals), 1)
        refusal = result.refusals[0]
        self.assertEqual(refusal.code, ASSOCIATION_UNCONFIRMED)
        self.assertEqual(refusal.left_fact_id, narrowed["fact_id"])
        self.assertEqual(refusal.candidate_right_fact_ids, (sole_report_fact_id,))


class TestMultiAcquisitionScale(unittest.TestCase):
    def test_same_payer_two_reports_are_not_greedily_paired(self) -> None:
        """Two acquisitions and two reports under the same payer/year.

        The join both sides currently support is (payer, tax-year)
        (ADR-0068 Decision 3), so this is ASSOCIATION_AMBIGUOUS on both
        acquisitions — not a silent 1-1 pairing of A1→R1, A2→R2, and not
        a Candidate-A set-collapse to a false unique match. The two
        report fact ids stay named and distinct.
        """
        a1 = _example("finding.v2.acquisition-a1.json")
        a2 = _example("finding.v2.acquisition-a2.json")
        r1 = _example("finding.v2.box1-s1.json")
        r2 = _example("finding.v2.box1-s2.json")
        result = _associate(
            {a1["id"]: a1, a2["id"]: a2, r1["id"]: r1, r2["id"]: r2}
        )
        self.assertEqual(result.publications, ())
        self.assertEqual(len(result.refusals), 2)
        by_left = {ref.left_fact_id: ref for ref in result.refusals}
        self.assertEqual(set(by_left), {a1["fact_id"], a2["fact_id"]})
        for refusal in result.refusals:
            self.assertEqual(refusal.code, ASSOCIATION_AMBIGUOUS)
            self.assertEqual(
                set(refusal.candidate_right_fact_ids),
                {r1["fact_id"], r2["fact_id"]},
            )

    def test_two_payers_publish_two_independent_associations(self) -> None:
        """Two legitimate unique matches must not overwrite each other."""
        a1 = _example("finding.v2.acquisition-a1.json")
        r1 = _example("finding.v2.box1-s1.json")
        a_b = dict(_example("finding.v2.acquisition-a2.json"))
        a_b["id"] = "demo.finding.acq.bank-b"
        a_b["fact_id"] = fact_id_for(
            ACQUISITION_FACT_TYPE,
            (
                ("payer", "demo.payer.bank-b"),
                ("reference", "DEMO-BOND-101"),
                ("tax-year", "2025"),
            ),
        )
        r_b = dict(_example("finding.v2.box1-s2.json"))
        r_b["id"] = "demo.finding.box1.bank-b"
        r_b["fact_id"] = fact_id_for(
            REPORT_FACT_TYPE,
            (
                ("payer", "demo.payer.bank-b"),
                ("statement", "demo.1099int-statement.t1"),
                ("tax-year", "2025"),
            ),
        )
        # A coarse-tier confirmation must name its target. ``a_b`` is a
        # renamed copy of ``a2`` (a different, unrelated payer, and itself
        # unconfirmed in its committed shape) so this test always sets its
        # own confirmation explicitly, never inherited from ``a2``'s.
        a_b_value = dict(a_b["value"])
        a_b_value["confirmed_report_match"] = True
        a_b_value["confirmed_report_fact_id"] = r_b["fact_id"]
        a_b["value"] = a_b_value
        result = _associate(
            {a1["id"]: a1, r1["id"]: r1, a_b["id"]: a_b, r_b["id"]: r_b}
        )
        self.assertEqual(result.refusals, ())
        self.assertEqual(len(result.publications), 2)
        pairs = {
            (p["value"]["left_fact_id"], p["value"]["right_fact_id"])
            for p in result.publications
        }
        self.assertEqual(
            pairs,
            {
                (a1["fact_id"], r1["fact_id"]),
                (a_b["fact_id"], r_b["fact_id"]),
            },
        )
        symbols = {p["symbol"] for p in result.publications}
        self.assertEqual(len(symbols), 2)


class TestJoinComponents(unittest.TestCase):
    def test_declared_components_are_fact_id_bound_keys_not_amounts(self) -> None:
        """Neither side's declared join components name a year at all any
        more: the coarse join is payer-only, restricted separately to the
        run's own ``reporting_year`` context (never a fact-id-bound
        component on either side) -- see ``_reports_in_reporting_year``."""
        for component in (*LEFT_COMPONENTS, *RIGHT_COMPONENTS):
            self.assertEqual(set(component), {"fact_id_bound_key"})
            self.assertEqual(component["fact_id_bound_key"], "payer")
            self.assertNotIn("amount", component.get("fact_id_bound_key", ""))


class TestRealContributionThroughProductionAssociation(unittest.TestCase):
    """Exercises the required property through the real production path, not
    a hand-built fixture: a genuine ``contribute_ordinary_acquisition``
    coarse-tier confirmation, admitted through the real contribution
    boundary against the current mapper's own bundle, then fed through the
    real ``associate()``/``marshal_run_context`` producer this whole
    module tests."""

    def _admit(self, *, confirmed_report_fact_id: str | None) -> dict[str, Any]:
        import tempfile

        from packages.kernel.findings import project
        from packages.tax.obligation_acquisition_mapping import (
            build_obligation_acquisition_bundle,
            build_ordinary_acquisition_entity_acts,
            contribute_ordinary_acquisition,
        )
        from tests.support import act, demo_evidence, registry_with_demo_kinds

        answers = {
            "payer_name": "demo.payer.bank-a",
            "obligation_description": "synthetic municipal bond series demo-real",
            "obligation_reference": "DEMO-BOND-REAL",
            "acquisition_date": "2025-03-14",
            "accrued_interest_paid_to_seller": 42.0,
            "currency": "USD",
            "confirmed_report_match": True,
        }
        with tempfile.TemporaryDirectory() as tmp:
            registry = registry_with_demo_kinds(Path(tmp))
            bundle = build_obligation_acquisition_bundle(answers)
            opening = [
                act(0, "bundle-adoption", {"bundle": bundle}),
                act(
                    1,
                    "evidence-submitted",
                    {
                        "evidence": demo_evidence(
                            "demo.evidence.acq.real",
                            "Synthetic ordinary-language acquisition interview",
                            {"mode": "ordinary-language-entry", "synthetic": True},
                        )
                    },
                ),
            ]
            opening.extend(build_ordinary_acquisition_entity_acts(answers, act_index=2))
            base = project(tuple(opening), registry)
            result = contribute_ordinary_acquisition(
                base,
                answers,
                registry=registry,
                record_id="demo.crec.acq.real",
                act_index=4,
                contribution_id="demo.contribution.acq.real",
                evidence_id="demo.evidence.acq.real",
                finding_id="demo.finding.acq.real",
                committed_against=4,
                confirmed_report_fact_id=confirmed_report_fact_id,
            )
            self.assertEqual(result.terminal_record["phase"], "completed")
            return result.state.findings["demo.finding.acq.real"]

    def test_real_contribution_with_a_named_target_associates_normally(self) -> None:
        r1 = _example("finding.v2.box1-s1.json")
        acq = self._admit(confirmed_report_fact_id=r1["fact_id"])
        self.assertEqual(acq["value"]["confirmed_report_fact_id"], r1["fact_id"])
        result = _associate({acq["id"]: acq, r1["id"]: r1})
        self.assertEqual(result.refusals, ())
        self.assertEqual(len(result.publications), 1)
        self.assertEqual(
            result.publications[0]["value"],
            {"left_fact_id": acq["fact_id"], "right_fact_id": r1["fact_id"]},
        )

    def test_coarse_tier_true_confirmation_with_no_target_cannot_be_built(self) -> None:
        """The mapper itself now fails closed — this shape can no longer
        even reach the contribution boundary, let alone association."""
        from packages.tax.obligation_acquisition_mapping import OrdinaryInputError

        with self.assertRaises(OrdinaryInputError):
            self._admit(confirmed_report_fact_id=None)


class TestMalformedConfirmationAssertedDirectlyFailsClosed(unittest.TestCase):
    """A malformed acquisition finding -- ``confirmed_report_match: true``
    with no ``confirmed_report_fact_id`` key at all -- is a shape neither
    the real mapper nor the adopted fact type's own ``value_schema`` will
    let into a workspace's content log (see
    ``TestMalformedConfirmationRejectedAtAdmission`` for the kernel-admission
    negative control). This is an internal defense-in-depth unit test: it
    constructs the malformed shape directly and calls ``associate()``
    in-process, bypassing kernel admission entirely, to confirm the
    association path itself also fails closed rather than relying solely on
    the admission boundary to prevent it."""

    def test_malformed_confirmation_refuses_rather_than_associates(self) -> None:
        malformed: dict[str, Any] = {
            "schema": "finding.v2",
            "id": "demo.finding.acq.malformed-shaped",
            "fact_id": fact_id_for(
                ACQUISITION_FACT_TYPE,
                (
                    ("payer", "demo.payer.malformed-shape"),
                    ("reference", "DEMO-BOND-MALFORMED"),
                    ("acquisition-year", "2025"),
                ),
            ),
            "value": {
                "obligation": {
                    "payer_name": "demo.payer.malformed-shape",
                    "description": "synthetic malformed-shaped acquisition",
                    "reference": "DEMO-BOND-MALFORMED",
                },
                "acquisition_date": "2025-03-14",
                "accrued_interest_paid_to_seller": 42.0,
                "currency": "USD",
                "reported_statement_reference": None,
                "confirmed_report_match": True,
                # No ``confirmed_report_fact_id`` key at all — a shape the
                # real mapper refuses to construct.
            },
            "basis": "attested",
            "evidence_ids": ["demo.evidence.acq.malformed-shaped"],
        }
        report: dict[str, Any] = {
            "schema": "finding.v2",
            "id": "demo.finding.box1.malformed-shaped",
            "fact_id": fact_id_for(
                REPORT_FACT_TYPE,
                (
                    ("payer", "demo.payer.malformed-shape"),
                    ("statement", "demo.1099int-statement.malformed-shaped"),
                    ("tax-year", "2025"),
                ),
            ),
            "value": 500.0,
            "basis": "documentary",
            "evidence_ids": ["demo.evidence.box1.malformed-shaped"],
        }
        result = _associate({malformed["id"]: malformed, report["id"]: report})
        self.assertEqual(result.publications, ())
        self.assertEqual(len(result.refusals), 1)
        self.assertEqual(result.refusals[0].code, ASSOCIATION_UNCONFIRMED)
        self.assertEqual(result.refusals[0].left_fact_id, malformed["fact_id"])
        self.assertEqual(
            result.refusals[0].candidate_right_fact_ids, (report["fact_id"],)
        )


class TestMalformedConfirmationRejectedAtAdmission(unittest.TestCase):
    """The kernel-admission negative control for the shape
    ``TestMalformedConfirmationAssertedDirectlyFailsClosed`` exercises
    in-process: ``confirmed_report_match: true`` with no
    ``confirmed_report_fact_id`` is not merely refused by ``associate()``
    when constructed directly -- it cannot enter a workspace's content log
    at all. The adopted ``obligation-acquisition.bundle.json`` fact type
    declares the same ``if``/``then`` on its own ``value_schema`` that the
    real mapper enforces, so ``packages.kernel.findings.apply_act`` --  the
    same admission machinery every real contribution goes through -- rejects
    this shape at assertion time, before any association logic ever runs.
    """

    def test_malformed_confirmation_finding_is_rejected_at_the_real_admission_path(
        self,
    ) -> None:
        import tempfile

        from packages.kernel.findings import FindingModelError, apply_act, project
        from tests.support import act, demo_evidence, registry_with_demo_kinds

        with tempfile.TemporaryDirectory() as tmp:
            registry = registry_with_demo_kinds(Path(tmp))
            bundle = _load(ACQUISITION_BUNDLE)
            opening = [
                act(0, "bundle-adoption", {"bundle": bundle}),
                act(
                    1,
                    "entity-introduced",
                    {
                        "entity": {
                            "schema": "entity.v1",
                            "id": "demo.mcra.payer",
                            "kind": "tax.us.interest-payer",
                            "label": "Synthetic malformed-confirmation payer",
                        }
                    },
                ),
                act(
                    2,
                    "entity-introduced",
                    {
                        "entity": {
                            "schema": "entity.v1",
                            "id": "demo.mcra.obligation",
                            "kind": "tax.us.interest-obligation",
                            "label": "Synthetic malformed-confirmation obligation",
                        }
                    },
                ),
                act(
                    3,
                    "evidence-submitted",
                    {"evidence": demo_evidence("demo.mcra.evidence", "Synthetic acquisition")},
                ),
            ]
            base = project(tuple(opening), registry)

            fact_id = fact_id_for(
                ACQUISITION_FACT_TYPE,
                (
                    ("payer", "demo.mcra.payer"),
                    ("obligation", "demo.mcra.obligation"),
                    ("acquisition-year", "2025"),
                ),
            )
            finding = {
                "schema": "finding.v2",
                "id": "demo.finding.acq.mcra",
                "fact_id": fact_id,
                "value": {
                    "obligation": {
                        "payer_name": "demo.mcra.payer",
                        "description": "synthetic malformed-confirmation obligation",
                        "reference": None,
                    },
                    "acquisition_date": "2025-03-14",
                    "accrued_interest_paid_to_seller": 42.0,
                    "currency": "USD",
                    "reported_statement_reference": None,
                    "confirmed_report_match": True,
                    # No ``confirmed_report_fact_id`` -- the malformed shape.
                },
                "basis": "attested",
                "evidence_ids": ["demo.mcra.evidence"],
            }
            assertion = act(4, "assertion", {"finding": finding})

            with self.assertRaises(FindingModelError) as ctx:
                apply_act(base, assertion, registry)
            self.assertIn("does not conform to", str(ctx.exception))


class TestReportingYearIsRunScopeNotUserAnswer(unittest.TestCase):
    """Structural companion to
    ``test_obligation_acquisition_translation.py::
    test_no_question_asks_for_a_tax_classification`` -- Seam 6's
    ``ORDINARY_ANSWERS_SCHEMA`` has no tax-year-shaped field at all. This
    proves the underlying property directly and structurally: with the
    acquisition's own answers held byte-for-byte identical, changing only
    the run's own ``reporting_year`` context (never anything in the answer
    set) changes which report is even in scope to associate to -- and a
    confirmation's own recorded target, not the run's reporting-year scope
    alone, is what actually authorizes an association against a specific
    report. A future change that reintroduced a user-authored field
    controlling reporting-year assignment would break this test.
    """

    PAYER = "demo.payer.bank-a"
    STATEMENT_REFERENCE = "RY-STMT"

    def _statement_entity_id(self) -> str:
        return f"{self.PAYER}::statement::{self.STATEMENT_REFERENCE}"

    def _acquisition(self) -> dict[str, Any]:
        return {
            "schema": "finding.v2",
            "id": "demo.finding.acq.reporting-year-proof",
            "fact_id": fact_id_for(
                ACQUISITION_FACT_TYPE,
                (
                    ("payer", self.PAYER),
                    ("reference", "DEMO-BOND-RY"),
                    ("acquisition-year", "2025"),
                ),
            ),
            "value": {
                "obligation": {
                    "payer_name": self.PAYER,
                    "description": "synthetic reporting-year proof obligation",
                    "reference": "DEMO-BOND-RY",
                },
                "acquisition_date": "2025-03-14",
                "accrued_interest_paid_to_seller": 42.0,
                "currency": "USD",
                "reported_statement_reference": self.STATEMENT_REFERENCE,
                "confirmed_report_match": True,
            },
            "basis": "attested",
            "evidence_ids": ["demo.evidence.acq.reporting-year-proof"],
        }

    def _report(self, *, tax_year: str) -> dict[str, Any]:
        return {
            "schema": "finding.v2",
            "id": f"demo.finding.box1.reporting-year-proof-{tax_year}",
            "fact_id": fact_id_for(
                REPORT_FACT_TYPE,
                (
                    ("payer", self.PAYER),
                    ("statement", self._statement_entity_id()),
                    ("tax-year", tax_year),
                ),
            ),
            "value": 500.0,
            "basis": "documentary",
            "evidence_ids": [f"demo.evidence.box1.reporting-year-proof-{tax_year}"],
        }

    def test_confirmation_targeted_to_2025_report_associates_in_2025_scoped_run(
        self,
    ) -> None:
        """A confirmation that names the 2025 report as its own recorded
        target associates cleanly in a run scoped to 2025."""
        acq = self._acquisition()
        r_2025 = self._report(tax_year="2025")
        value = dict(acq["value"])
        value["confirmed_report_fact_id"] = r_2025["fact_id"]
        acq["value"] = value

        result = _associate({acq["id"]: acq, r_2025["id"]: r_2025}, reporting_year=2025)
        self.assertEqual(result.refusals, ())
        self.assertEqual(len(result.publications), 1)
        self.assertEqual(
            result.publications[0]["value"]["right_fact_id"], r_2025["fact_id"]
        )

    def test_same_confirmation_refuses_when_a_different_2025_report_becomes_sole(
        self,
    ) -> None:
        """One current confirmation must never authorize the acquisition's
        consequence against more than one report: reporting-year scope
        alone (unchanged here, always 2025) is never what authorizes an
        association -- the recorded target must still match the current
        sole candidate exactly. The acquisition's own recorded target names
        a retired 2025 report's fact id; a different 2025 report (same
        payer, a different statement) is retired-and-replaced into the sole
        candidate with no new act on the acquisition side. The confirmation
        refuses ``ASSOCIATION_UNCONFIRMED`` -- naming the replacement report
        as the (unconfirmed) sole candidate -- never silently retargeting
        onto whichever report is sole now."""
        acq = self._acquisition()
        value = dict(acq["value"])
        value["reported_statement_reference"] = None
        acq["value"] = value
        original = self._report(tax_year="2025")
        replacement_statement_entity_id = f"{self.PAYER}::statement::RY-STMT-REPLACEMENT"
        replacement: dict[str, Any] = {
            "schema": "finding.v2",
            "id": "demo.finding.box1.reporting-year-proof-replacement",
            "fact_id": fact_id_for(
                REPORT_FACT_TYPE,
                (
                    ("payer", self.PAYER),
                    ("statement", replacement_statement_entity_id),
                    ("tax-year", "2025"),
                ),
            ),
            "value": 500.0,
            "basis": "documentary",
            "evidence_ids": ["demo.evidence.box1.reporting-year-proof-replacement"],
        }
        value = dict(acq["value"])
        value["confirmed_report_fact_id"] = original["fact_id"]
        acq["value"] = value
        # ``original`` is retired -- absent from current state -- and
        # ``replacement`` (a different statement, same payer/tax-year) is
        # now the only 2025 report in scope.
        result = _associate({acq["id"]: acq, replacement["id"]: replacement}, reporting_year=2025)
        self.assertEqual(result.publications, ())
        self.assertEqual(len(result.refusals), 1)
        refusal = result.refusals[0]
        self.assertEqual(refusal.code, ASSOCIATION_UNCONFIRMED)
        self.assertEqual(refusal.left_fact_id, acq["fact_id"])
        self.assertEqual(refusal.candidate_right_fact_ids, (replacement["fact_id"],))

    def test_absent_reporting_year_context_is_the_honest_zero_candidate_no_match(
        self,
    ) -> None:
        """``reporting_year=None`` (no run-scope year at all) never guesses
        -- every report is out of scope, the same honest silent no-match
        as any other zero-candidate case, never a new refusal code."""
        acq = self._acquisition()
        r_2025 = self._report(tax_year="2025")
        result = _associate({acq["id"]: acq, r_2025["id"]: r_2025}, reporting_year=None)
        self.assertEqual(result.publications, ())
        self.assertEqual(result.refusals, ())

    # A December acquisition whose relevant report belongs to a later tax
    # year (``reporting_year`` driving the join across acquisition-year and
    # report tax-year, rather than acquisition-year alone) would prove the
    # same point this class's other tests prove for a fixed year -- but no
    # later-year report vocabulary, package member, or consequence path is
    # admitted in this milestone (both the acquisition's ``acquisition-year``
    # and the report's ``tax-year`` are literal identity keys restricted to
    # ``["2025"]`` in the adopted content). That property belongs to the
    # roadmap's "Later-year basis reuse" candidate (see
    # ``docs/phase-state.md``'s "Open and owner-held" section), which
    # exercises cross-year identity and correction directly; it is out of
    # scope here and is not tested with a fabricated 2026 report.


class TestOutOfScopeReportTaxYearIsRejectedAtAdmission(unittest.TestCase):
    """A ``tax-year`` value outside the adopted vocabulary is not merely
    ignored by this module's own producer -- it is rejected at the real
    kernel admission boundary, before any association logic ever runs.
    ``f1099int.bundle.json``'s box-1 fact type declares ``tax-year`` as a
    literal identity key with ``"values": ["2025"]`` (see
    ``TestProductionSchemaIds``); ``packages.kernel.facts.facts_of`` derives
    the fact lattice only from each literal key's declared values, so a
    fact id naming ``tax-year=2026`` is never a member of the lattice at
    all. Asserting a hand-built ``finding.v2`` against that fact id through
    the real ``packages.kernel.findings.apply_act`` path -- the same
    admission machinery every real report ingestion and
    ``contribute_ordinary_acquisition`` call goes through -- fails with
    "finding references unknown fact", not a schema-shape complaint. This
    is the negative control for Seam 2's cross-year mechanism: the
    ``reporting_year`` join itself is real and general (see
    ``TestReportingYearIsRunScopeNotUserAnswer`` /
    ``TestReportingYearThreadedThroughRunContext``), but no report content
    outside 2025 can ever be admitted into a workspace under this
    milestone's adopted vocabulary, so no real run can ever have a 2026
    report to associate against."""

    def test_tax_year_2026_report_finding_is_rejected_at_the_real_admission_path(
        self,
    ) -> None:
        import tempfile

        from packages.kernel.findings import FindingModelError, apply_act, project
        from tests.support import act, demo_evidence, registry_with_demo_kinds

        with tempfile.TemporaryDirectory() as tmp:
            registry = registry_with_demo_kinds(Path(tmp))
            bundle = _load(BOX1_BUNDLE)
            opening = [
                act(0, "bundle-adoption", {"bundle": bundle}),
                act(
                    1,
                    "entity-introduced",
                    {
                        "entity": {
                            "schema": "entity.v1",
                            "id": "demo.oosry.payer",
                            "kind": "tax.us.interest-payer",
                            "label": "Synthetic out-of-scope-year payer",
                        }
                    },
                ),
                act(
                    2,
                    "entity-introduced",
                    {
                        "entity": {
                            "schema": "entity.v1",
                            "id": "demo.oosry.statement",
                            "kind": "tax.us.1099int-statement",
                            "label": "Synthetic out-of-scope-year statement",
                        }
                    },
                ),
                act(
                    3,
                    "evidence-submitted",
                    {"evidence": demo_evidence("demo.oosry.evidence", "Synthetic 1099-INT")},
                ),
            ]
            base = project(tuple(opening), registry)

            out_of_scope_fact_id = fact_id_for(
                REPORT_FACT_TYPE,
                (
                    ("payer", "demo.oosry.payer"),
                    ("statement", "demo.oosry.statement"),
                    ("tax-year", "2026"),
                ),
            )
            self.assertNotIn("tax-year=2025", out_of_scope_fact_id)
            finding = {
                "schema": "finding.v2",
                "id": "demo.finding.box1.oosry",
                "fact_id": out_of_scope_fact_id,
                "value": 500.0,
                "basis": "documentary",
                "evidence_ids": ["demo.oosry.evidence"],
            }
            assertion = act(4, "assertion", {"finding": finding})

            with self.assertRaises(FindingModelError) as ctx:
                apply_act(base, assertion, registry)
            self.assertIn("unknown fact", str(ctx.exception))


class TestReportingYearThreadedThroughRunContext(unittest.TestCase):
    """The real production dispatch path (``packages.derivation.runner.run``
    -> ``_execute`` -> ``try_publish_on_run``) reads
    ``RunContext.reporting_year`` -- never anything acquisition-supplied --
    to decide which reports are in scope. This is the same field
    ``packages.derivation.live.live_coordinate_run`` populates from
    ``run_scope["year"]`` in production; here it is exercised directly,
    one hop closer to the real dispatch than ``associate()`` alone."""

    def _ctx(self, sources: list[Any], *, reporting_year: int | None) -> RunContext:
        return RunContext(
            run_id="demo.run.identity-association.reporting-year-context",
            rules=[],
            parameters={},
            canon={},
            inputs=[],
            sources=sources,
            adoption_pin=ADOPTION_PIN,
            governance_pins=[],
            reporting_year=reporting_year,
        )

    def test_matching_reporting_year_context_associates(self) -> None:
        a1 = _example("finding.v2.acquisition-a1.json")
        r1 = _example("finding.v2.box1-s1.json")
        sources = _sources_for({a1["id"]: a1, r1["id"]: r1})
        result = runner_run(self._ctx(sources, reporting_year=2025), DerivationSchemas())
        pairings = [
            pub.finding
            for pub in result.publications
            if str(pub.finding.get("symbol", "")).startswith(ASSOCIATION_SYMBOL)
        ]
        self.assertEqual(len(pairings), 1)
        self.assertEqual(pairings[0]["value"]["right_fact_id"], r1["fact_id"])

    def test_absent_reporting_year_context_on_the_runcontext_default_is_no_match(
        self,
    ) -> None:
        """A ``RunContext`` that never sets ``reporting_year`` (its own
        default, e.g. most fixture/test paths) makes the association path
        see no report in scope -- honest, silent no-match, never a crash
        and never a guess."""
        a1 = _example("finding.v2.acquisition-a1.json")
        r1 = _example("finding.v2.box1-s1.json")
        sources = _sources_for({a1["id"]: a1, r1["id"]: r1})
        result = runner_run(self._ctx(sources, reporting_year=None), DerivationSchemas())
        pairings = [
            pub.finding
            for pub in result.publications
            if str(pub.finding.get("symbol", "")).startswith(ASSOCIATION_SYMBOL)
        ]
        self.assertEqual(pairings, [])
        self.assertEqual(result.blocked, [])


class TestReportingYearProvenanceIsRunScopeNotAcquisitionValue(unittest.TestCase):
    """The run-scope-supplied reporting year must never be silently
    attributed to the user as part of the acquisition's own attested
    proposition -- it is dispatch-time context, visible only in the
    association's own pins/provenance."""

    def test_acquisition_value_never_carries_a_reporting_or_tax_year_field(self) -> None:
        a1 = _example("finding.v2.acquisition-a1.json")
        self.assertNotIn("tax_year", a1["value"])
        self.assertNotIn("reporting_year", a1["value"])
        self.assertNotIn("tax-year", a1["value"])

    def test_published_pairing_attributes_scope_to_the_adoption_pin_only(self) -> None:
        a1 = _example("finding.v2.acquisition-a1.json")
        r1 = _example("finding.v2.box1-s1.json")
        result = _associate({a1["id"]: a1, r1["id"]: r1})
        self.assertEqual(len(result.publications), 1)
        pairing = result.publications[0]
        self.assertNotIn("reporting_year", pairing["value"])
        self.assertNotIn("tax_year", pairing["value"])
        adoption_pins = [p for p in pairing["pins"] if p["role"] == "adoption"]
        self.assertEqual(len(adoption_pins), 1)
        self.assertEqual(adoption_pins[0]["id"], ADOPTION_PIN["id"])


if __name__ == "__main__":
    unittest.main()
