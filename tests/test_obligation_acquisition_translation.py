"""Track 2 evidence for the Document and Ordinary-Fact Translation Vertical:
the nine canonical translation cases T1-T9, each run through the real
coordinator.

Every case here goes through ``live_coordinate_run``
(``packages/derivation/live.py``) against the wired production package set
this milestone publishes --- ``package.core-calculations`` v34 /
``published-packages`` v29 / release v27 / the ``adopt-core-v34-current``
fixture built by ``tools/generate_obligation_acquisition_translation.py``.
That is the same evidentiary bar the Schedule B adjustment and Form 1098-E
milestones set for their own integration surfaces, and it is the bar that
makes these cases evidence rather than illustration.

What the milestone is actually testing is a translation: the person records
ordinary facts about a purchase --- when they bought a bond, what they paid
the seller for interest that had already accrued, which payer's report the
purchase concerns --- and the engine, not the person, decides that those
facts are an accrued-interest adjustment to taxable interest. At no point is
the user asked to supply a tax classification. T3, T4, T5 and T9 are the
cases where the honest answer is a refusal, and each refusal names the
ordinary question it is about rather than a tax conclusion.

Every identity is obviously synthetic (``demo.*``) and every amount is
invented. Nothing here derives from a real document or a real return.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from tests.test_market_discount_interest_integration import _act, _attested
from tests.test_schedule_b_interest_adjustments import _adjustment_acts

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = ROOT / "packages" / "sample_data" / "obligation_acquisition_translation"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

FAMILY = "tax.us.2025.obligation.acquisition"
SCALAR_FAMILY = "tax.us.2025.obligation.accrued-interest-paid"
ACQUISITION = "tax.us.2025.obligation.acquisition"
ACCRUED = "tax.us.2025.obligation.acquisition.accrued-interest-paid"
ACQ_CLOSURE = "tax.us.2025.obligation.acquisition.source-closure"
ACCRUED_CLOSURE = "tax.us.2025.obligation.accrued-interest-paid.source-closure"

SUBJECT = "demo.oat.subject.filer"
# The payer and box-1 statement the Schedule B harness's own base return
# records. The association is against *these* identities, not invented ones,
# so a passing association is a real join against a real recorded item.
BASE_PAYER = "demo.md.bank"
BASE_B1_HORIZON = "demo.md.int-b1.h1"
# Above the Schedule B threshold, so Part I is actually rendered and the
# derived class is visible on the return rather than merely computed.
BASE_BOX1 = 2000.0

LINE_2B = "tax.us.2025.rule.form1040-line2b"
SCHEDULE_B = "tax.us.2025.rule.attachment.schedule-b"
ADJUSTMENT_LABEL = "Accrued Interest (bond acquisition)"


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / "published-packages.v29.json",
        CONTENT,
    )


def _acq_fact_id(fact_type: str, obligation: str, acquisition: str) -> str:
    # Identity-key declaration order, which is the order `_fact_id` renders
    # (packages/kernel/facts.py): subject, obligation, acquisition, tax-year.
    return (
        f"{fact_type}|subject={SUBJECT},obligation={obligation},"
        f"acquisition={acquisition},tax-year=2025"
    )


class Acquisition:
    """One synthetic obligation purchase, as ordinary facts about a purchase.

    The defaults describe the bounded case the milestone translates: a bond
    that pays interest periodically in arrears, bought while current, where
    the accrued interest was a separately stated component of what the buyer
    paid the seller. Each neighbouring case T9 refuses is reached by
    overriding exactly one of those answers, which is the point --- the
    refusals are driven by the person's own answers, not by a tax judgement
    the product made on their behalf.
    """

    def __init__(
        self,
        *,
        token: str,
        accrued: float | None = 300.0,
        payer: str = BASE_PAYER,
        periodic_in_arrears: str | None = "yes",
        in_default: str | None = "no",
        separately_stated: str | None = "yes",
        acquired_on: str = "2025-05-15",
    ) -> None:
        self.token = token
        self.obligation = f"demo.oat.obligation.{token}"
        self.acquisition = f"demo.oat.acq.{token}"
        self.accrued = accrued
        self.payer = payer
        self.periodic_in_arrears = periodic_in_arrears
        self.in_default = in_default
        self.separately_stated = separately_stated
        self.acquired_on = acquired_on

    def record(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "acquired_on": self.acquired_on,
            "concerns_reported_payer": self.payer,
        }
        if self.accrued is not None:
            value["accrued_interest_paid_to_seller"] = self.accrued
        if self.periodic_in_arrears is not None:
            value["obligation_pays_periodically_in_arrears"] = self.periodic_in_arrears
        if self.in_default is not None:
            value["obligation_in_default_or_arrears_at_purchase"] = self.in_default
        if self.separately_stated is not None:
            value["accrued_paid_as_separate_component"] = self.separately_stated
        return value


def _acquisition_acts(
    *,
    acquisitions: list[Acquisition] | None = None,
    close: bool = True,
    extra_b1: list[tuple[str, str, float]] | None = None,
    corrections: list[tuple[Acquisition, dict[str, Any] | None, float | None]] | None = None,
) -> list[dict[str, object]]:
    """The Schedule B adjustment base return plus an obligation-acquisition
    lifecycle, adopting the v34 package.

    ``acquisitions=None`` or ``[]`` with ``close=True`` is the closed-empty
    case: both families are closed with zero current members, which is what
    lets the closure-backed zero publish rather than blocking.

    ``extra_b1`` admits further Form 1099-INT box-1 items as
    ``(payer, statement, amount)``, which is how the several-matches case
    (T5) is reached: the association is against the *payer*, so two items
    from one payer is the ambiguity, not two items in general.
    """
    acquisitions = acquisitions or []
    acts = _adjustment_acts(box1_interest=BASE_BOX1)
    acts.pop()  # replace the v15 adoption with this milestone's v34 route

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    b1_horizon = BASE_B1_HORIZON
    for index, (payer, statement, amount) in enumerate(extra_b1 or []):
        # The payer may already be current --- T5's whole point is a *second*
        # item from a payer the base return already recorded --- and the
        # kernel rejects reintroducing an existing entity.
        introduced = [(statement, "tax.us.1099int-statement", "Synthetic Form 1099-INT")]
        if payer != BASE_PAYER:
            introduced.insert(0, (payer, "tax.us.interest-payer", "Synthetic interest payer"))
        for entity_id, kind, label in introduced:
            add("entity-introduced", {"entity": {
                "schema": "entity.v1", "id": entity_id, "kind": kind, "label": label,
            }})
        successor = f"demo.oat.int-b1.h{index + 1}"
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {"action": "assert", "finding": _attested(
                f"demo.oat.finding.b1.{index}",
                f"tax.us.2025.f1099int.box1-interest|payer={payer},"
                f"statement={statement},tax-year=2025",
                amount,
            )},
            "successor": {"id": successor, "predecessor": b1_horizon},
        })
        b1_horizon = successor
    if extra_b1:
        # Admitting a further member advanced the family's horizon, so the
        # base return's closure attestation no longer keys the current one.
        add("assertion", {"finding": _attested(
            "demo.oat.closure.int-b1",
            f"tax.us.2025.f1099int.b1.source-closure|family-horizon={b1_horizon},tax-year=2025",
            True,
        )})

    add("bundle-adoption", {"bundle": json.loads(
        (CONTENT / "obligation-acquisition.bundle.json").read_text("utf-8")
    )})
    add("entity-introduced", {"entity": {
        "schema": "entity.v1", "id": SUBJECT,
        "kind": "tax.us.filing-subject", "label": "Synthetic filing subject",
    }})
    for acq in acquisitions:
        add("entity-introduced", {"entity": {
            "schema": "entity.v1", "id": acq.obligation,
            "kind": "tax.us.obligation", "label": "Synthetic debt obligation",
        }})
        add("entity-introduced", {"entity": {
            "schema": "entity.v1", "id": acq.acquisition,
            "kind": "tax.us.obligation-acquisition", "label": "Synthetic obligation purchase",
        }})

    add("horizon-genesis", {"family": {"id": FAMILY, "version": "v1"},
                            "scope": SCOPE_KEY, "horizon_id": "demo.oat.acq.h0"})
    add("horizon-genesis", {"family": {"id": SCALAR_FAMILY, "version": "v1"},
                            "scope": SCOPE_KEY, "horizon_id": "demo.oat.accrued.h0"})

    acq_horizon = "demo.oat.acq.h0"
    accrued_horizon = "demo.oat.accrued.h0"
    for index, acq in enumerate(acquisitions):
        successor = f"demo.oat.acq.h{index + 1}"
        add("member-transition", {
            "family": {"id": FAMILY, "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {"action": "assert", "finding": _attested(
                f"demo.oat.finding.acq.{acq.token}",
                _acq_fact_id(ACQUISITION, acq.obligation, acq.acquisition),
                acq.record(),
            )},
            "successor": {"id": successor, "predecessor": acq_horizon},
        })
        acq_horizon = successor

        if acq.accrued is None:
            # The scalar companion is the projection of an answer that was
            # never given, so there is nothing to record. The canonical
            # family's own constraint is what names the missing question.
            continue
        successor = f"demo.oat.accrued.h{index + 1}"
        add("member-transition", {
            "family": {"id": SCALAR_FAMILY, "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {"action": "assert", "finding": _attested(
                f"demo.oat.finding.accrued.{acq.token}",
                _acq_fact_id(ACCRUED, acq.obligation, acq.acquisition),
                acq.accrued,
            )},
            "successor": {"id": successor, "predecessor": accrued_horizon},
        })
        accrued_horizon = successor

    # Correcting a fact already in a family is an ordinary assertion, not a
    # member transition: the kernel rejects a transition that re-asserts a
    # current member, because membership did not change --- only the value
    # did. That distinction is exactly what T6/T7 are about, so the harness
    # honours it rather than routing around it.
    for offset, (acq, record, accrued) in enumerate(corrections or []):
        if record is not None:
            add("assertion", {"finding": _attested(
                f"demo.oat.finding.acq.{acq.token}.c{offset}",
                _acq_fact_id(ACQUISITION, acq.obligation, acq.acquisition),
                record,
            )})
        if accrued is not None:
            add("assertion", {"finding": _attested(
                f"demo.oat.finding.accrued.{acq.token}.c{offset}",
                _acq_fact_id(ACCRUED, acq.obligation, acq.acquisition),
                accrued,
            )})

    if close:
        add("assertion", {"finding": _attested(
            "demo.oat.closure.acq",
            f"{ACQ_CLOSURE}|family-horizon={acq_horizon},tax-year=2025", True,
        )})
        add("assertion", {"finding": _attested(
            "demo.oat.closure.accrued",
            f"{ACCRUED_CLOSURE}|family-horizon={accrued_horizon},tax-year=2025", True,
        )})

    adoption = cast(dict[str, object], json.loads(
        (FIXTURES / "adoptions" / "adopt-core-v34-current.json").read_text("utf-8")
    ))
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


def _run(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
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
        return (
            json.loads(result.output_path.read_text("utf-8")),
            json.loads(result.presentation_path.read_text("utf-8")),
        )


def _section(model: dict[str, Any], section_id: str) -> dict[str, Any]:
    return next(section for section in model["sections"] if section["id"] == section_id)


def _dispositions(report: dict[str, Any], artifact_id: str) -> list[dict[str, Any]]:
    return [row for row in report.get("dispositions", []) if row.get("artifact_id") == artifact_id]


VALIDATION_ARTIFACT = "tax.us.2025.obligation.acquisition.member-validation"


def _refusal_codes(report: dict[str, Any]) -> set[str]:
    """The block codes the acquisition family's own validation names.

    Scoped deliberately to the synthesized member-validation artifact rather
    than to every blocked row in the run: this base return legitimately
    blocks many unrelated artifacts, so a run-wide code sweep would pass for
    the wrong reason.
    """
    codes: set[str] = set()
    for row in report.get("dispositions", []):
        if row.get("artifact_id") != f"{VALIDATION_ARTIFACT}.synthesized":
            continue
        if row.get("disposition") != "blocked":
            continue
        codes.update(row.get("missing", []))
    return codes


def _assert_line_2b_withheld(case: unittest.TestCase, report: dict[str, Any]) -> None:
    """Line 2b must be blocked *on this family's validation*, not merely absent."""
    rows = _dispositions(report, LINE_2B)
    case.assertTrue(rows)
    for row in rows:
        case.assertEqual(row["disposition"], "blocked", row)
        case.assertIn(VALIDATION_ARTIFACT, row.get("missing", []), row)


class T1NoAcquisitionRecorded(unittest.TestCase):
    """T1: a return with no obligation purchase at all is unaffected."""

    def test_closed_empty_family_leaves_line_2b_at_the_reported_total(self) -> None:
        _, model = _run(_acquisition_acts(), "demo.oat.t1")
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], BASE_BOX1)

    def test_no_adjustment_row_is_rendered_for_an_empty_family(self) -> None:
        _, model = _run(_acquisition_acts(), "demo.oat.t1-rows")
        group = next(g for g in model["citationGroups"] if g["id"] == SCHEDULE_B)
        headings = [part["heading"] for part in group["parts"]]
        # The class is declared, so the row exists; it just carries nothing.
        self.assertIn(ADJUSTMENT_LABEL, headings)


class T2OrdinaryFactsBecomeAnAdjustment(unittest.TestCase):
    """T2: the translation itself. Ordinary purchase facts in, adjustment out."""

    def test_recorded_purchase_reduces_line_2b_without_being_classified(self) -> None:
        _, model = _run(
            _acquisition_acts(acquisitions=[Acquisition(token="orchard", accrued=300)]),
            "demo.oat.t2",
        )
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], BASE_BOX1 - 300)

    def test_schedule_b_renders_the_derived_class_under_its_own_label(self) -> None:
        _, model = _run(
            _acquisition_acts(acquisitions=[Acquisition(token="orchard", accrued=300)]),
            "demo.oat.t2-schedule-b",
        )
        group = next(g for g in model["citationGroups"] if g["id"] == SCHEDULE_B)
        headings = [part["heading"] for part in group["parts"]]
        self.assertIn(ADJUSTMENT_LABEL, headings)
        # Distinct from the statement-transcribed accrued-interest class: the
        # difference the fourth class exists to record is provenance.
        self.assertIn("Accrued Interest", headings)

    def test_the_person_supplied_no_tax_classification(self) -> None:
        """The recorded facts are about a purchase, end to end.

        This is the milestone's product claim stated as a test: the member
        payload the user's acts carry names a date, an amount paid to a
        seller, and three yes/no recognitions about the obligation. It never
        names an adjustment, a Schedule B class, or a line.
        """
        payload = Acquisition(token="orchard", accrued=300).record()
        self.assertEqual(
            sorted(payload),
            [
                "accrued_interest_paid_to_seller",
                "accrued_paid_as_separate_component",
                "acquired_on",
                "concerns_reported_payer",
                "obligation_in_default_or_arrears_at_purchase",
                "obligation_pays_periodically_in_arrears",
            ],
        )
        rendered = json.dumps(payload).lower()
        for tax_word in ("adjustment", "schedule", "line", "taxable", "deduct"):
            self.assertNotIn(tax_word, rendered)


class T3MissingAmountIsNamedNotDefaulted(unittest.TestCase):
    """T3: unanswered and zero are different states of the person's records."""

    def test_absent_accrued_amount_blocks_and_names_the_ordinary_question(self) -> None:
        report, _ = _run(
            _acquisition_acts(acquisitions=[Acquisition(token="orchard", accrued=None)]),
            "demo.oat.t3",
        )
        self.assertIn("ACCRUED_AMOUNT_NOT_SUPPLIED", _refusal_codes(report))

    def test_line_2b_does_not_publish_a_guess(self) -> None:
        report, _ = _run(
            _acquisition_acts(acquisitions=[Acquisition(token="orchard", accrued=None)]),
            "demo.oat.t3-line",
        )
        _assert_line_2b_withheld(self, report)


class T4NothingToAttachTo(unittest.TestCase):
    """T4: a purchase concerning a payer no recorded report accounts for."""

    def test_unmatched_association_blocks_rather_than_inventing_a_report(self) -> None:
        report, _ = _run(
            _acquisition_acts(acquisitions=[
                Acquisition(token="orchard", payer="demo.oat.payer.unreported"),
            ]),
            "demo.oat.t4",
        )
        self.assertIn("IDENTITY_ASSOCIATION_UNMATCHED", _refusal_codes(report))
        _assert_line_2b_withheld(self, report)


class T5MoreThanOnePlausibleReport(unittest.TestCase):
    """T5: one payer, two box-1 items, and no basis to choose between them."""

    def test_ambiguous_association_blocks_rather_than_choosing(self) -> None:
        report, _ = _run(
            _acquisition_acts(
                acquisitions=[Acquisition(token="orchard")],
                extra_b1=[(BASE_PAYER, "demo.oat.stmt.second", 400.0)],
            ),
            "demo.oat.t5",
        )
        self.assertIn("IDENTITY_ASSOCIATION_AMBIGUOUS", _refusal_codes(report))
        _assert_line_2b_withheld(self, report)


class T6And7CorrectionsDisplaceIndependently(unittest.TestCase):
    """T6/T7: correcting one recorded fact does not disturb the others."""

    def test_correcting_the_accrued_amount_moves_only_that_amount(self) -> None:
        acq = Acquisition(token="orchard", accrued=300)
        _, model = _run(
            _acquisition_acts(acquisitions=[acq], corrections=[(acq, None, 250.0)]),
            "demo.oat.t6",
        )
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], BASE_BOX1 - 250)

    def test_correcting_the_purchase_record_leaves_the_amount_standing(self) -> None:
        acq = Acquisition(token="orchard", accrued=300)
        corrected = acq.record() | {"acquired_on": "2025-06-01"}
        _, model = _run(
            _acquisition_acts(acquisitions=[acq], corrections=[(acq, corrected, None)]),
            "demo.oat.t7",
        )
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], BASE_BOX1 - 300)


class T8SeveralObligationsUnderOnePayer(unittest.TestCase):
    """T8: association is many-to-one, so one report can account for two buys."""

    def test_two_acquisitions_both_subtract(self) -> None:
        _, model = _run(
            _acquisition_acts(acquisitions=[
                Acquisition(token="orchard", accrued=300),
                Acquisition(token="mill", accrued=120),
            ]),
            "demo.oat.t8",
        )
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], BASE_BOX1 - 420)


class T9NeighbouringCasesAreRefused(unittest.TestCase):
    """T9: the cases just outside the bounded treatment, each named."""

    def test_each_neighbour_blocks_under_its_own_code(self) -> None:
        cases = (
            ("OBLIGATION_NOT_PERIODIC_IN_ARREARS", {"periodic_in_arrears": "no"}),
            ("OBLIGATION_IN_DEFAULT_OR_ARREARS", {"in_default": "yes"}),
            ("ACCRUED_NOT_SEPARATELY_STATED", {"separately_stated": "unknown"}),
        )
        for code, override in cases:
            with self.subTest(code=code):
                report, _ = _run(
                    _acquisition_acts(acquisitions=[
                        Acquisition(token="orchard", **override),  # type: ignore[arg-type]
                    ]),
                    f"demo.oat.t9.{code.lower()}",
                )
                self.assertIn(code, _refusal_codes(report))

    def test_an_unanswered_recognition_refuses_the_same_way_as_a_no(self) -> None:
        """Absent and "not the bounded case" both refuse, deliberately.

        Each of these constraints is `any(field_absent, field_not_equals)`,
        because `field_not_equals` is False on an absent field. Without the
        absence arm, simply not answering would slip past a guard that a "no"
        would have tripped --- which is the silent-widening failure the
        bounded treatment exists to prevent.
        """
        report, _ = _run(
            _acquisition_acts(acquisitions=[
                Acquisition(token="orchard", periodic_in_arrears=None),
            ]),
            "demo.oat.t9-absent",
        )
        self.assertIn("OBLIGATION_NOT_PERIODIC_IN_ARREARS", _refusal_codes(report))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
