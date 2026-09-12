"""Track 2: C0–C13 and cross-year through live_coordinate_run on package v36.

Kill 6 (C1 publishes $450) and the identity-boundary regressions remain; this
module extends them with the rest of the fixed cases on the same real path.
"""

from __future__ import annotations

import json
import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping, Sequence, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    load_published_citizen_checksums,
    validate_package,
)
from packages.derivation.production_resolver import PublicationSurface
from packages.tax.loader import TAX_CONTENT_DIR
from packages.tax.nominee_allocation_recording import derive_nominee_allocation_fact_id
from packages.tax.nominee_consequences import (
    CITATION_ID,
    DEPENDENCY_ABSENT,
    NOMINEE_ALLOCATIONS_EXCEED_REPORT,
    PUBLISHES,
    RULE_ID,
)
from packages.tax.report_statement_identity import (
    derive_1099int_box1_fact_id,
    derive_reported_payer_entity_id,
    derive_reported_statement_entity_id,
)
from tests.support import demo_evidence
from tests.test_f1098e_student_loan_interest_agi_track6 import _f1098e_acts
from tests.test_form1099g_box1_schedule1_line7 import _act, _attested
from tests.test_package_membership_wiring import ROOT, SCOPE, USER
from tests.test_ssa1099_benefits_line6_track2 import SCOPE_KEY

CONTENT = TAX_CONTENT_DIR
FIXTURES = ROOT / "packages" / "sample_data" / "package_membership_wiring"
REGISTRY_FILE = "published-packages.v31.json"
RELEASE_FILE = "demo.release.2025.v29.json"
ADOPTION_FILE = "adopt-core-v36-current.json"

PAYER = "demo.payer.a"
STMT = "demo.stmt.a"
YEAR = 2025
RECIPIENT = "demo.recipient.pat"
PAYER_C = "demo.payer.c"
STMT_C = "demo.stmt.c"
PAYER_SHARED = "demo.payer.shared"
STMT_B = "demo.stmt.b"
BOX1_FAMILY = "tax.us.2025.f1099int.b1"
BOX1_CLOSURE_TYPE = "tax.us.2025.f1099int.b1.source-closure"
CGD_BOX1_HORIZON = "demo.cgd.t2.int-b1.h0"
B1_SUBTOTAL = "tax.us.2025.interest.b1-subtotal"
LINE2B_SYMBOL = "tax.us.2025.interest.taxable-total"
LEGACY_NOMINEE_SUBTOTAL = "tax.us.2025.interest.scheduleb-nominee-subtotal"
LEGACY_NOMINEE_AMOUNT = "tax.us.2025.scheduleb.adjustment.nominee.amount"
LEGACY_NOMINEE_FAMILY = "tax.us.2025.scheduleb.adjustment.nominee"
UG_NOMINEE_HORIZON = "demo.ug.sb-nom.h0"
FORBIDDEN_PAYMENT_NAMES = (
    "accrued_interest_paid_to_seller",
    "tax.us.2025.f1099div.box7-foreign-tax-paid",
    "tax.us.2025.quantity.foreign-tax-paid",
    LEGACY_NOMINEE_AMOUNT,
)


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


def _two_report_acts() -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    """One live run holding TWO punctuation-bearing reports and their allocations.

    Returns the acts plus, per report, the ids a caller needs to assert
    isolation: payer, statement reference, report finding id, allocation
    finding id, and the recipient entity id.
    """
    specs = [
        {
            "payer": "Demo Bank, N.A.",
            "stmt": "acct 12,345",
            "recipient": "demo.recipient.pat",
            "report_finding": "demo.f.box1.a1",
            "alloc_finding": "demo.f.pat.1",
            "report_value": 1200.0,
            "alloc_value": 450.0,
            "evidence": "demo.evidence.alloc.pat",
            "horizon": "demo.nominee.two.int-b1.h1",
            "predecessor": "demo.cgd.t2.int-b1.h0",
        },
        {
            "payer": "Demo Trust, Ltd.",
            "stmt": "ref 67,890",
            "recipient": "demo.recipient.kim",
            "report_finding": "demo.f.box1.b1",
            "alloc_finding": "demo.f.kim.1",
            "report_value": 900.0,
            "alloc_value": 300.0,
            "evidence": "demo.evidence.alloc.kim",
            "horizon": "demo.nominee.two.int-b1.h2",
            "predecessor": "demo.nominee.two.int-b1.h1",
        },
    ]
    acts = _f1098e_acts(statements=[], close=True, wages=90000)
    acts.pop()

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("nominee-allocation.bundle.json")})
    for spec in specs:
        payer = str(spec["payer"])
        stmt = str(spec["stmt"])
        recipient = str(spec["recipient"])
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": derive_reported_payer_entity_id(payer),
                    "kind": "tax.us.interest-payer",
                    "label": "Synthetic interest payer",
                }
            },
        )
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": derive_reported_statement_entity_id(
                        payer_name=payer, statement_reference=stmt
                    ),
                    "kind": "tax.us.1099int-statement",
                    "label": "Synthetic Form 1099-INT",
                }
            },
        )
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": recipient,
                    "kind": "tax.us.interest-allocation-recipient",
                    "label": "Synthetic allocation recipient",
                }
            },
        )
        add(
            "member-transition",
            {
                "family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(
                        str(spec["report_finding"]),
                        derive_1099int_box1_fact_id(
                            payer_name=payer, statement_reference=stmt, tax_year=YEAR
                        ),
                        float(spec["report_value"]),  # type: ignore[arg-type]
                    ),
                },
                "successor": {
                    "id": str(spec["horizon"]),
                    "predecessor": str(spec["predecessor"]),
                },
            },
        )
        add(
            "evidence-submitted",
            {
                "evidence": demo_evidence(
                    str(spec["evidence"]),
                    "Synthetic ordinary-language allocation interview",
                    {"mode": "ordinary-language-entry", "synthetic": True},
                )
            },
        )
        add(
            "assertion",
            {
                "finding": {
                    "schema": "finding.v2",
                    "id": str(spec["alloc_finding"]),
                    "fact_id": derive_nominee_allocation_fact_id(
                        payer_name=payer,
                        statement_reference=stmt,
                        tax_year=YEAR,
                        recipient_id=recipient,
                    ),
                    "value": float(spec["alloc_value"]),  # type: ignore[arg-type]
                    "basis": "attested",
                    "evidence_ids": [str(spec["evidence"])],
                }
            },
        )

    adoption = _load_adoption()
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    for index, act in enumerate(acts):
        act["committed_against"] = index
        act["act_id"] = f"demo.nominee-two.act.{index:03d}"
        act["actor"] = USER
    return acts, [{k: str(v) for k, v in spec.items()} for spec in specs]


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


def _content_corpus() -> dict[tuple[str, str], dict[str, Any]]:
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        try:
            value = json.loads(path.read_text("utf-8"))
        except Exception:
            continue
        if (
            isinstance(value, dict)
            and isinstance(value.get("id"), str)
            and isinstance(value.get("version"), str)
            and not ("citizens" in value and "packages" in value)
        ):
            corpus[(value["id"], value["version"])] = value
    return corpus


def _c1_acts(
    *, payer: str = PAYER, stmt: str = STMT, recipient: str = RECIPIENT
) -> list[dict[str, object]]:
    acts = _f1098e_acts(statements=[], close=True, wages=90000)
    acts.pop()  # drop the Track-6 v33 adoption

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("nominee-allocation.bundle.json")})
    payer_id = derive_reported_payer_entity_id(payer)
    statement_id = derive_reported_statement_entity_id(
        payer_name=payer, statement_reference=stmt
    )
    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": payer_id,
                "kind": "tax.us.interest-payer",
                "label": "Synthetic interest payer A",
            }
        },
    )
    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": statement_id,
                "kind": "tax.us.1099int-statement",
                "label": "Synthetic Form 1099-INT A",
            }
        },
    )
    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": recipient,
                "kind": "tax.us.interest-allocation-recipient",
                "label": "Synthetic allocation recipient Pat",
            }
        },
    )
    report_fact_id = derive_1099int_box1_fact_id(
        payer_name=payer, statement_reference=stmt, tax_year=YEAR
    )
    add(
        "member-transition",
        {
            "family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {
                "action": "assert",
                "finding": _attested("demo.f.box1.a1", report_fact_id, 1200.0),
            },
            "successor": {
                "id": "demo.nominee.c1.int-b1.h1",
                "predecessor": "demo.cgd.t2.int-b1.h0",
            },
        },
    )
    alloc_fact_id = derive_nominee_allocation_fact_id(
        payer_name=payer,
        statement_reference=stmt,
        tax_year=YEAR,
        recipient_id=recipient,
    )
    evidence = demo_evidence(
        "demo.evidence.alloc.pat",
        "Synthetic ordinary-language allocation interview",
        {"mode": "ordinary-language-entry", "synthetic": True},
    )
    add("evidence-submitted", {"evidence": evidence})
    add(
        "assertion",
        {
            "finding": {
                "schema": "finding.v2",
                "id": "demo.f.pat.1",
                "fact_id": alloc_fact_id,
                "value": 450.0,
                "basis": "attested",
                "evidence_ids": ["demo.evidence.alloc.pat"],
            }
        },
    )

    adoption = _load_adoption()
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    for index, act in enumerate(acts):
        act["committed_against"] = index
        act["act_id"] = f"demo.nominee-live.act.{index:03d}"
        act["actor"] = USER
    return acts


def _suffix(payer: str, stmt: str, *, tax_year: int = YEAR) -> str:
    return f"{PUBLISHES}|{derive_1099int_box1_fact_id(payer_name=payer, statement_reference=stmt, tax_year=tax_year)}"


def _box1_horizon(index: int) -> str:
    return f"demo.nominee.box1.h{index}"


def _finalize_acts(
    acts: list[dict[str, object]], *, prefix: str = "demo.nominee-live.act"
) -> list[dict[str, object]]:
    finalized = [dict(act) for act in acts]
    if finalized and finalized[-1].get("kind") == "package-adoption":
        finalized.pop()
    adoption = _load_adoption()
    adoption["committed_against"] = len(finalized)
    finalized.append(adoption)
    for index, act in enumerate(finalized):
        act["committed_against"] = index
        act["act_id"] = f"{prefix}.{index:03d}"
        act["actor"] = USER
    return finalized


def _workspace_acts(
    *,
    reports: Sequence[Mapping[str, Any]],
    allocations: Sequence[Mapping[str, Any]] = (),
    close_box1: bool = False,
    extra: Sequence[tuple[str, dict[str, object]]] = (),
    finalize: bool = True,
    act_prefix: str = "demo.nominee-live.act",
) -> list[dict[str, object]]:
    """One live workspace: reports, current allocations, optional box-1 close.

    Report-only groups (no current allocation) are C0 option 1 and are not
    invoked. ``close_box1`` re-closes the box-1 family on the last advanced
    horizon so the b1-subtotal is actually calculated — required for C0's
    'box-1 still calculated' assertion, not for the nominee publication itself.
    """
    acts = _f1098e_acts(statements=[], close=True, wages=90000)
    acts.pop()

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("nominee-allocation.bundle.json")})
    introduced: set[str] = set()

    def introduce(entity_id: str, kind: str, label: str) -> None:
        if entity_id in introduced:
            return
        introduced.add(entity_id)
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": entity_id,
                    "kind": kind,
                    "label": label,
                }
            },
        )

    for spec in reports:
        payer = str(spec["payer"])
        stmt = str(spec["stmt"])
        introduce(
            derive_reported_payer_entity_id(payer),
            "tax.us.interest-payer",
            "Synthetic interest payer",
        )
        introduce(
            derive_reported_statement_entity_id(payer_name=payer, statement_reference=stmt),
            "tax.us.1099int-statement",
            "Synthetic Form 1099-INT",
        )
    for spec in allocations:
        introduce(
            str(spec["recipient"]),
            "tax.us.interest-allocation-recipient",
            "Synthetic allocation recipient",
        )
        payer = str(spec["payer"])
        stmt = str(spec["stmt"])
        introduce(
            derive_reported_payer_entity_id(payer),
            "tax.us.interest-payer",
            "Synthetic interest payer",
        )
        introduce(
            derive_reported_statement_entity_id(payer_name=payer, statement_reference=stmt),
            "tax.us.1099int-statement",
            "Synthetic Form 1099-INT",
        )

    horizon = CGD_BOX1_HORIZON
    advanced = 0
    for spec in reports:
        if spec.get("report_value") is None:
            continue
        advanced += 1
        successor = str(spec.get("horizon") or _box1_horizon(advanced))
        payer = str(spec["payer"])
        stmt = str(spec["stmt"])
        add(
            "member-transition",
            {
                "family": {"id": BOX1_FAMILY, "version": "v1"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(
                        str(spec["report_finding"]),
                        derive_1099int_box1_fact_id(
                            payer_name=payer, statement_reference=stmt, tax_year=YEAR
                        ),
                        float(spec["report_value"]),
                    ),
                },
                "successor": {"id": successor, "predecessor": horizon},
            },
        )
        horizon = successor
    if close_box1 and advanced:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.nominee.box1.closure",
                    f"{BOX1_CLOSURE_TYPE}|family-horizon={horizon},tax-year=2025",
                    True,
                )
            },
        )

    for spec in allocations:
        payer = str(spec["payer"])
        stmt = str(spec["stmt"])
        recipient = str(spec["recipient"])
        tax_year = int(spec.get("tax_year", YEAR))
        evidence_id = str(spec["evidence"])
        add(
            "evidence-submitted",
            {
                "evidence": demo_evidence(
                    evidence_id,
                    "Synthetic ordinary-language allocation interview",
                    {"mode": "ordinary-language-entry", "synthetic": True},
                )
            },
        )
        add(
            "assertion",
            {
                "finding": {
                    "schema": "finding.v2",
                    "id": str(spec["alloc_finding"]),
                    "fact_id": derive_nominee_allocation_fact_id(
                        payer_name=payer,
                        statement_reference=stmt,
                        tax_year=tax_year,
                        recipient_id=recipient,
                    ),
                    "value": float(spec["alloc_value"]),
                    "basis": "attested",
                    "evidence_ids": [evidence_id],
                }
            },
        )

    for kind, payload in extra:
        add(kind, payload)

    if finalize:
        return _finalize_acts(acts, prefix=act_prefix)
    return acts


def _report(
    *,
    payer: str,
    stmt: str,
    finding: str,
    value: float,
) -> dict[str, Any]:
    return {
        "payer": payer,
        "stmt": stmt,
        "report_finding": finding,
        "report_value": value,
    }


def _alloc(
    *,
    payer: str,
    stmt: str,
    recipient: str,
    finding: str,
    value: float,
    evidence: str,
    tax_year: int = YEAR,
) -> dict[str, Any]:
    return {
        "payer": payer,
        "stmt": stmt,
        "recipient": recipient,
        "alloc_finding": finding,
        "alloc_value": value,
        "evidence": evidence,
        "tax_year": tax_year,
    }


def _c1_workspace(*, close_box1: bool = True, finalize: bool = True) -> list[dict[str, object]]:
    return _workspace_acts(
        reports=[_report(payer=PAYER, stmt=STMT, finding="demo.f.box1.a1", value=1200.0)],
        allocations=[
            _alloc(
                payer=PAYER,
                stmt=STMT,
                recipient=RECIPIENT,
                finding="demo.f.pat.1",
                value=450.0,
                evidence="demo.evidence.alloc.pat",
            )
        ],
        close_box1=close_box1,
        finalize=finalize,
    )


class NomineeConsequencesLive(unittest.TestCase):
    def test_kill_3_v36_has_no_unreachable_members(self) -> None:
        pkg = _load("package.core-calculations.v36.json")
        corpus = _content_corpus()
        members = {(m["id"], m["version"]): corpus[(m["id"], m["version"])] for m in pkg["members"]}
        result = validate_package(
            pkg,
            members,
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / REGISTRY_FILE),
        )
        self.assertTrue(result.ok, result.issues)
        self.assertFalse(any(issue.code == "MEMBER_UNREACHABLE" for issue in result.issues))

    def test_kill_6_c1_publishes_450_through_live_coordinate_run(self) -> None:
        acts = _c1_acts()
        report_fact_id = derive_1099int_box1_fact_id(
            payer_name=PAYER, statement_reference=STMT, tax_year=YEAR
        )
        suffix = f"{PUBLISHES}|{report_fact_id}"
        with TemporaryDirectory() as tmp:
            outcome = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"),
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="demo.run.nominee-c1-live",
                governance_pins=[],
                surface=_surface(),
                output_name="out.json",
            )
            self.assertIsNone(outcome.refusal, outcome.refusal)
            publications = tuple(outcome.publications or ())
        published = [p.finding for p in publications if p.finding.get("symbol") == suffix]
        self.assertEqual(len(published), 1, [p.finding.get("symbol") for p in publications])
        self.assertEqual(Decimal(str(published[0]["value"])), Decimal("450"))

    # --- Lossless report/allocation association -------------------------
    #
    # ``facts._fact_id`` joins ``name=value`` pairs on "," without escaping,
    # and the recording contract permits commas in payer_name,
    # statement_reference, and recipient_id. Re-parsing the rendered fact id
    # therefore truncates those values, which previously produced
    # DEPENDENCY_ABSENT instead of the report-scoped reduction. The
    # coordinator now reads ``SourceFact.keys`` (the kernel lattice's own
    # structured tuples) and never splits the string. These run the real
    # package/live path, not a hand-built RunContext.

    def _live(self, acts: list[dict[str, object]], run_id: str) -> Any:
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "L"
            outcome = live_coordinate_run(
                WorkspaceCapability(root),
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
            self.assertIsNone(outcome.refusal, outcome.refusal)
            self._last_record = (
                json.loads(Path(outcome.output_path).read_text("utf-8"))
                if outcome.output_path
                else {}
            )
            records_path = root / "records" / "derivation_records.jsonl"
            records = [
                json.loads(line)
                for line in records_path.read_text("utf-8").splitlines()
                if line.strip()
            ]
            closing = [row for row in records if row.get("phase") == "completed"]
            self.assertEqual(len(closing), 1, [row.get("phase") for row in records])
            self._last_closing = closing[0]
            return tuple(outcome.publications or ())

    def _assert_reduction(
        self, publications: Any, *, payer: str, stmt: str, recipient: str, amount: str
    ) -> dict[str, Any]:
        report_fact_id = derive_1099int_box1_fact_id(
            payer_name=payer, statement_reference=stmt, tax_year=YEAR
        )
        suffix = f"{PUBLISHES}|{report_fact_id}"
        published = [p.finding for p in publications if p.finding.get("symbol") == suffix]
        self.assertEqual(
            len(published), 1, [p.finding.get("symbol") for p in publications]
        )
        finding = published[0]
        self.assertEqual(Decimal(str(finding["value"])), Decimal(amount))
        # The symbol carries the EXACT current report fact id, commas intact.
        self.assertEqual(finding["symbol"], suffix)
        self.assertIn(report_fact_id, finding["symbol"])
        # Pins name exactly this report and its one allocation.
        input_pins = {p["id"] for p in finding["pins"] if p["role"] == "input"}
        self.assertEqual(input_pins, {"demo.f.box1.a1", "demo.f.pat.1"})
        return cast(dict[str, Any], finding)

    def test_comma_bearing_payer_name_associates_and_publishes(self) -> None:
        payer = "Demo Bank, N.A."
        pubs = self._live(_c1_acts(payer=payer), "demo.run.nominee-comma-payer")
        self._assert_reduction(
            pubs, payer=payer, stmt=STMT, recipient=RECIPIENT, amount="450"
        )

    def test_comma_bearing_statement_reference_associates_and_publishes(self) -> None:
        stmt = "acct 12,345 / copy B"
        pubs = self._live(_c1_acts(stmt=stmt), "demo.run.nominee-comma-stmt")
        self._assert_reduction(
            pubs, payer=PAYER, stmt=stmt, recipient=RECIPIENT, amount="450"
        )

    def test_comma_bearing_recipient_cannot_corrupt_the_year_filter(self) -> None:
        """A recipient id containing ",tax-year=1999" must not re-scope the run.

        Before the structured-identity repair this silently excluded the
        allocation from a 2025 run: the rendered id ends
        ``...,recipient=demo.recipient.pat,tax-year=1999`` and a comma-splitting
        parser takes the LAST pair as the year.

        The honest outcome is now a loud refusal, not a guessed result. The
        coordinator's ambiguity guard is deliberately CONSERVATIVE: it refuses
        any binding whose rendering contains ``,<keyname>=``, which is a
        superset of the genuinely colliding cases (this particular value is in
        fact uniquely rendered, because key order is fixed). Refusing a
        superset is the safe direction -- what must never happen is a wrong
        year scoping presented as an ordinary answer.
        """
        recipient = "demo.recipient.pat,tax-year=1999"
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "L"
            acts = _c1_acts(recipient=recipient)
            outcome = live_coordinate_run(
                WorkspaceCapability(root),
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="demo.run.nominee-comma-recipient",
                governance_pins=[],
                surface=_surface(),
                output_name="out.json",
            )
            self.assertIsNotNone(outcome.refusal)
            assert outcome.refusal is not None
            self.assertEqual(outcome.refusal.reason, "NOMINEE_IDENTITY")
            self.assertIn("ambiguously rendered", outcome.refusal.detail)
            self.assertIsNone(outcome.run_id)
            self.assertIsNone(outcome.output_path)
            self.assertIsNone(outcome.presentation_path)
            self.assertFalse((root / "records" / "derivation_records.jsonl").exists())
            self.assertFalse((root / "outputs").exists())
        # Critically: it did NOT quietly scope the run to 1999.
        self.assertNotIn("1999 is the reporting year", outcome.refusal.detail)

    def test_identity_guard_is_a_clean_pre_run_refusal(self) -> None:
        """The production identity boundary has no durable run effects.

        The bounded nominee identity check runs after package resolution,
        projection, and marshalling, but before output paths are reserved or
        the derivation start record is appended. It returns the live
        coordinator's typed refusal instead of leaking NomineeIdentityError.

        This test pins the selected bounded behavior: no run id, output or
        presentation path, reserved empty output, or started/completed record.
        """
        acts = _c1_acts(recipient="demo.recipient.pat,tax-year=1999")
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "L"
            outcome = live_coordinate_run(
                WorkspaceCapability(root),
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="demo.run.nominee-identity-boundary",
                governance_pins=[],
                surface=_surface(),
                output_name="out.json",
            )
            self.assertIsNotNone(outcome.refusal)
            assert outcome.refusal is not None
            self.assertEqual(outcome.refusal.reason, "NOMINEE_IDENTITY")
            self.assertIn("ambiguously rendered", outcome.refusal.detail)
            self.assertIsNone(outcome.run_id)
            self.assertIsNone(outcome.output_path)
            self.assertIsNone(outcome.presentation_path)

            records_path = root / "records" / "derivation_records.jsonl"
            self.assertFalse(records_path.exists())
            self.assertFalse((root / "outputs").exists())

    def test_two_punctuation_bearing_reports_stay_isolated(self) -> None:
        """One real live run with TWO punctuation-bearing reports.

        The previous version of this test executed only report A and asserted
        that report B's symbol was absent -- which it trivially was, since B
        never entered the run. That proved nothing about isolation. This
        version puts both reports and both allocations in a single
        ``live_coordinate_run`` and asserts they stay apart.
        """
        acts, specs = _two_report_acts()
        pubs = self._live(acts, "demo.run.nominee-two-reports")

        expected = []
        for spec in specs:
            report_fact_id = derive_1099int_box1_fact_id(
                payer_name=spec["payer"],
                statement_reference=spec["stmt"],
                tax_year=YEAR,
            )
            expected.append((spec, report_fact_id, f"{PUBLISHES}|{report_fact_id}"))

        a_spec, a_report, a_suffix = expected[0]
        b_spec, b_report, b_suffix = expected[1]
        self.assertNotEqual(a_report, b_report)

        findings = {
            p.finding["symbol"]: p.finding
            for p in pubs
            if str(p.finding.get("symbol", "")).startswith(f"{PUBLISHES}|")
        }
        # Two distinct suffixed publications.
        self.assertEqual(set(findings), {a_suffix, b_suffix}, sorted(findings))

        # Each exact expected value.
        self.assertEqual(Decimal(str(findings[a_suffix]["value"])), Decimal("450"))
        self.assertEqual(Decimal(str(findings[b_suffix]["value"])), Decimal("300"))

        # Each publication pins only its own report and allocation, and
        # neither report's sources appear in the other result.
        a_pins = {p["id"] for p in findings[a_suffix]["pins"] if p["role"] == "input"}
        b_pins = {p["id"] for p in findings[b_suffix]["pins"] if p["role"] == "input"}
        self.assertEqual(a_pins, {a_spec["report_finding"], a_spec["alloc_finding"]})
        self.assertEqual(b_pins, {b_spec["report_finding"], b_spec["alloc_finding"]})
        self.assertEqual(a_pins & b_pins, set())
        self.assertNotIn(b_spec["report_finding"], a_pins)
        self.assertNotIn(b_spec["alloc_finding"], a_pins)
        self.assertNotIn(a_spec["report_finding"], b_pins)
        self.assertNotIn(a_spec["alloc_finding"], b_pins)

        # The grouped disposition count is exactly two: one identified row per
        # classified disposition-group (ADR-0074 Decision 3c), asserted on the
        # durable ledger before any symbol-keyed collapse could merge them.
        rows = [
            row
            for row in self._last_record.get("dispositions", [])
            if row.get("artifact_id") == RULE_ID
        ]
        self.assertEqual(len(rows), 2, rows)
        self.assertEqual({row.get("symbol") for row in rows}, {a_suffix, b_suffix})

    # --- Track 2: C0–C13 and cross-year through the real boundary ----------

    def _nominee_rows(self, source: Mapping[str, Any]) -> list[dict[str, Any]]:
        return [
            cast(dict[str, Any], row)
            for row in source.get("dispositions", [])
            if row.get("artifact_id") == RULE_ID
        ]

    def _input_pins(self, finding: Mapping[str, Any]) -> set[str]:
        return {str(pin["id"]) for pin in finding.get("pins", []) if pin.get("role") == "input"}

    def _publication(self, publications: Any, symbol: str) -> dict[str, Any]:
        found = [p.finding for p in publications if p.finding.get("symbol") == symbol]
        self.assertEqual(len(found), 1, [p.finding.get("symbol") for p in publications])
        return cast(dict[str, Any], found[0])

    def _publication_value(self, publications: Any, symbol: str) -> Decimal:
        return Decimal(str(self._publication(publications, symbol)["value"]))

    def _assert_no_reduction(self, publications: Any, suffix: str) -> None:
        found = [p.finding for p in publications if p.finding.get("symbol") == suffix]
        self.assertEqual(found, [], [p.finding.get("symbol") for p in publications])

    def _assert_supported(
        self,
        publications: Any,
        *,
        payer: str,
        stmt: str,
        reduction: str,
        remainder: str,
        report_amount: str,
        report_finding: str,
        alloc_findings: Sequence[str],
        excluded_findings: Sequence[str] = (),
    ) -> dict[str, Any]:
        suffix = _suffix(payer, stmt)
        finding = self._publication(publications, suffix)
        self.assertEqual(Decimal(str(finding["value"])), Decimal(reduction))
        observed = Decimal(report_amount) - Decimal(str(finding["value"]))
        self.assertEqual(observed, Decimal(remainder))
        pins = self._input_pins(finding)
        expected = {report_finding, *alloc_findings}
        self.assertEqual(pins, expected)
        for finding_id in excluded_findings:
            self.assertNotIn(finding_id, pins)
        self.assertNotIn(LEGACY_NOMINEE_AMOUNT, json.dumps(finding))
        return finding

    def _assert_blocked_exceed(
        self,
        publications: Any,
        *,
        payer: str,
        stmt: str,
        report_finding: str,
        alloc_findings: Sequence[str],
        excluded_findings: Sequence[str] = (),
    ) -> dict[str, Any]:
        suffix = _suffix(payer, stmt)
        self._assert_no_reduction(publications, suffix)
        rows = self._nominee_rows(self._last_closing)
        matching = [row for row in rows if row.get("symbol") == suffix]
        self.assertEqual(len(matching), 1, rows)
        row = matching[0]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], NOMINEE_ALLOCATIONS_EXCEED_REPORT)
        self.assertEqual(row["missing"], [])
        pins = self._input_pins(row)
        self.assertIn(report_finding, pins)
        for finding_id in alloc_findings:
            self.assertIn(finding_id, pins)
        for finding_id in excluded_findings:
            self.assertNotIn(finding_id, pins)
        return row

    def test_c0_no_groups_selected_and_box1_still_calculated(self) -> None:
        pubs = self._live(
            _workspace_acts(
                reports=[_report(payer=PAYER, stmt=STMT, finding="demo.f.box1.a1", value=1200.0)],
                close_box1=True,
            ),
            "demo.run.nominee-c0",
        )
        suffix = _suffix(PAYER, STMT)
        self._assert_no_reduction(pubs, suffix)
        self.assertEqual(self._publication_value(pubs, B1_SUBTOTAL), Decimal("1200"))
        rows = self._nominee_rows(self._last_closing)
        self.assertEqual(len(rows), 1, rows)
        row = rows[0]
        self.assertEqual(row["disposition"], "inapplicable")
        self.assertTrue(row["no_groups_selected"])
        self.assertEqual(row["symbol"], PUBLISHES)
        self.assertNotIn("|", row["symbol"])
        durable = self._nominee_rows(self._last_record)
        self.assertEqual(len(durable), 1, durable)
        self.assertEqual(durable[0]["symbol"], PUBLISHES)

    def test_c1_publishes_450_with_observed_remainder_and_pins(self) -> None:
        pubs = self._live(_c1_workspace(), "demo.run.nominee-c1-remainder")
        finding = self._assert_supported(
            pubs,
            payer=PAYER,
            stmt=STMT,
            reduction="450",
            remainder="750",
            report_amount="1200",
            report_finding="demo.f.box1.a1",
            alloc_findings=["demo.f.pat.1"],
        )
        self.assertEqual(self._publication_value(pubs, B1_SUBTOTAL), Decimal("1200"))
        pin_blob = json.dumps(finding["pins"])
        self.assertIn(RULE_ID, pin_blob)
        self.assertIn(CITATION_ID, pin_blob)

    def test_c2_full_allocation_remainder_zero(self) -> None:
        pubs = self._live(
            _workspace_acts(
                reports=[_report(payer=PAYER, stmt=STMT, finding="demo.f.box1.a1", value=1200.0)],
                allocations=[
                    _alloc(
                        payer=PAYER,
                        stmt=STMT,
                        recipient=RECIPIENT,
                        finding="demo.f.pat.1",
                        value=1200.0,
                        evidence="demo.evidence.alloc.pat",
                    )
                ],
                close_box1=True,
            ),
            "demo.run.nominee-c2",
        )
        self._assert_supported(
            pubs,
            payer=PAYER,
            stmt=STMT,
            reduction="1200",
            remainder="0",
            report_amount="1200",
            report_finding="demo.f.box1.a1",
            alloc_findings=["demo.f.pat.1"],
        )

    def test_c3_several_recipients_pin_both_allocations(self) -> None:
        pubs = self._live(
            _workspace_acts(
                reports=[_report(payer=PAYER, stmt=STMT, finding="demo.f.box1.a1", value=1200.0)],
                allocations=[
                    _alloc(
                        payer=PAYER,
                        stmt=STMT,
                        recipient=RECIPIENT,
                        finding="demo.f.pat.1",
                        value=300.0,
                        evidence="demo.evidence.alloc.pat",
                    ),
                    _alloc(
                        payer=PAYER,
                        stmt=STMT,
                        recipient="demo.recipient.kim",
                        finding="demo.f.kim.1",
                        value=150.0,
                        evidence="demo.evidence.alloc.kim",
                    ),
                ],
                close_box1=True,
            ),
            "demo.run.nominee-c3",
        )
        self._assert_supported(
            pubs,
            payer=PAYER,
            stmt=STMT,
            reduction="450",
            remainder="750",
            report_amount="1200",
            report_finding="demo.f.box1.a1",
            alloc_findings=["demo.f.pat.1", "demo.f.kim.1"],
        )

    def test_c4_closing_record_carries_exceed_report_code(self) -> None:
        pubs = self._live(
            _workspace_acts(
                reports=[_report(payer=PAYER, stmt=STMT, finding="demo.f.box1.a1", value=1200.0)],
                allocations=[
                    _alloc(
                        payer=PAYER,
                        stmt=STMT,
                        recipient=RECIPIENT,
                        finding="demo.f.pat.1",
                        value=800.0,
                        evidence="demo.evidence.alloc.pat",
                    ),
                    _alloc(
                        payer=PAYER,
                        stmt=STMT,
                        recipient="demo.recipient.kim",
                        finding="demo.f.kim.1",
                        value=450.0,
                        evidence="demo.evidence.alloc.kim",
                    ),
                ],
                close_box1=True,
            ),
            "demo.run.nominee-c4",
        )
        self._assert_blocked_exceed(
            pubs,
            payer=PAYER,
            stmt=STMT,
            report_finding="demo.f.box1.a1",
            alloc_findings=["demo.f.pat.1", "demo.f.kim.1"],
        )
        self.assertEqual(self._publication_value(pubs, B1_SUBTOTAL), Decimal("1200"))
        self.assertNotEqual(
            self._nominee_rows(self._last_closing)[0]["code"], "DEPENDENCY_INVALID"
        )

    def test_c5a_report_correction_yields_corrected_remainder(self) -> None:
        first = self._live(_c1_workspace(), "demo.run.nominee-c5a-before")
        self._assert_supported(
            first,
            payer=PAYER,
            stmt=STMT,
            reduction="450",
            remainder="750",
            report_amount="1200",
            report_finding="demo.f.box1.a1",
            alloc_findings=["demo.f.pat.1"],
        )
        acts = _c1_workspace(finalize=False)
        report_fact_id = derive_1099int_box1_fact_id(
            payer_name=PAYER, statement_reference=STMT, tax_year=YEAR
        )
        acts.append(
            _act(
                len(acts),
                "assertion",
                {"finding": _attested("demo.f.box1.a2", report_fact_id, 1000.0)},
            )
        )
        pubs = self._live(_finalize_acts(acts), "demo.run.nominee-c5a-after")
        finding = self._assert_supported(
            pubs,
            payer=PAYER,
            stmt=STMT,
            reduction="450",
            remainder="550",
            report_amount="1000",
            report_finding="demo.f.box1.a2",
            alloc_findings=["demo.f.pat.1"],
            excluded_findings=["demo.f.box1.a1"],
        )
        self.assertNotIn("750", str(finding["value"]))
        self.assertEqual(self._publication_value(pubs, B1_SUBTOTAL), Decimal("1000"))

    def test_c5b_report_correction_to_over_allocation_blocks(self) -> None:
        acts = _c1_workspace(finalize=False)
        report_fact_id = derive_1099int_box1_fact_id(
            payer_name=PAYER, statement_reference=STMT, tax_year=YEAR
        )
        acts.append(
            _act(
                len(acts),
                "assertion",
                {"finding": _attested("demo.f.box1.a2", report_fact_id, 400.0)},
            )
        )
        pubs = self._live(_finalize_acts(acts), "demo.run.nominee-c5b")
        self._assert_blocked_exceed(
            pubs,
            payer=PAYER,
            stmt=STMT,
            report_finding="demo.f.box1.a2",
            alloc_findings=["demo.f.pat.1"],
            excluded_findings=["demo.f.box1.a1"],
        )

    def test_c6_allocation_correct_retract_reassert_uses_only_current(self) -> None:
        alloc_fact_id = derive_nominee_allocation_fact_id(
            payer_name=PAYER,
            statement_reference=STMT,
            tax_year=YEAR,
            recipient_id=RECIPIENT,
        )
        base = _c1_workspace(finalize=False)

        corrected = list(base)
        corrected.append(
            _act(
                len(corrected),
                "assertion",
                {
                    "finding": {
                        "schema": "finding.v2",
                        "id": "demo.f.pat.2",
                        "fact_id": alloc_fact_id,
                        "value": 400.0,
                        "basis": "attested",
                        "evidence_ids": ["demo.evidence.alloc.pat"],
                    }
                },
            )
        )
        pubs = self._live(_finalize_acts(corrected), "demo.run.nominee-c6-correct")
        self._assert_supported(
            pubs,
            payer=PAYER,
            stmt=STMT,
            reduction="400",
            remainder="800",
            report_amount="1200",
            report_finding="demo.f.box1.a1",
            alloc_findings=["demo.f.pat.2"],
            excluded_findings=["demo.f.pat.1"],
        )

        retracted = list(corrected)
        retracted.append(
            _act(len(retracted), "finding-retracted", {"finding_id": "demo.f.pat.2"})
        )
        pubs = self._live(_finalize_acts(retracted), "demo.run.nominee-c6-retract")
        suffix = _suffix(PAYER, STMT)
        self._assert_no_reduction(pubs, suffix)
        rows = self._nominee_rows(self._last_closing)
        self.assertEqual(len(rows), 1, rows)
        self.assertEqual(rows[0]["disposition"], "inapplicable")
        self.assertTrue(rows[0]["no_groups_selected"])
        self.assertEqual(rows[0]["symbol"], PUBLISHES)
        pin_blob = json.dumps(self._last_closing)
        self.assertNotIn("demo.f.pat.1", pin_blob)
        self.assertNotIn("demo.f.pat.2", pin_blob)
        self.assertEqual(self._publication_value(pubs, B1_SUBTOTAL), Decimal("1200"))

        reasserted = list(retracted)
        reasserted.append(
            _act(
                len(reasserted),
                "assertion",
                {
                    "finding": {
                        "schema": "finding.v2",
                        "id": "demo.f.pat.3",
                        "fact_id": alloc_fact_id,
                        "value": 250.0,
                        "basis": "attested",
                        "evidence_ids": ["demo.evidence.alloc.pat"],
                    }
                },
            )
        )
        pubs = self._live(_finalize_acts(reasserted), "demo.run.nominee-c6-reassert")
        self._assert_supported(
            pubs,
            payer=PAYER,
            stmt=STMT,
            reduction="250",
            remainder="950",
            report_amount="1200",
            report_finding="demo.f.box1.a1",
            alloc_findings=["demo.f.pat.3"],
            excluded_findings=["demo.f.pat.1", "demo.f.pat.2"],
        )

    def test_c7_same_payer_supportable_isolation(self) -> None:
        pubs = self._live(
            _workspace_acts(
                reports=[
                    _report(
                        payer=PAYER_SHARED,
                        stmt=STMT,
                        finding="demo.f.box1.a1",
                        value=1200.0,
                    ),
                    _report(
                        payer=PAYER_SHARED,
                        stmt=STMT_B,
                        finding="demo.f.box1.b1",
                        value=1500.0,
                    ),
                ],
                allocations=[
                    _alloc(
                        payer=PAYER_SHARED,
                        stmt=STMT,
                        recipient=RECIPIENT,
                        finding="demo.f.pat.1",
                        value=450.0,
                        evidence="demo.evidence.alloc.pat",
                    )
                ],
                close_box1=True,
            ),
            "demo.run.nominee-c7",
        )
        self._assert_supported(
            pubs,
            payer=PAYER_SHARED,
            stmt=STMT,
            reduction="450",
            remainder="750",
            report_amount="1200",
            report_finding="demo.f.box1.a1",
            alloc_findings=["demo.f.pat.1"],
            excluded_findings=["demo.f.box1.b1"],
        )
        self._assert_no_reduction(pubs, _suffix(PAYER_SHARED, STMT_B))
        rows = self._nominee_rows(self._last_closing)
        self.assertEqual(len(rows), 1, rows)
        self.assertEqual(rows[0]["symbol"], _suffix(PAYER_SHARED, STMT))
        self.assertEqual(self._publication_value(pubs, B1_SUBTOTAL), Decimal("2700"))

    def test_c8_ownership_without_payment_still_publishes(self) -> None:
        pubs = self._live(_c1_workspace(), "demo.run.nominee-c8")
        finding = self._assert_supported(
            pubs,
            payer=PAYER,
            stmt=STMT,
            reduction="450",
            remainder="750",
            report_amount="1200",
            report_finding="demo.f.box1.a1",
            alloc_findings=["demo.f.pat.1"],
        )
        blob = json.dumps(finding)
        for name in FORBIDDEN_PAYMENT_NAMES:
            self.assertNotIn(name, blob)

    def test_c10_unrelated_group_row_count_before_symbol_collapse(self) -> None:
        pubs = self._live(
            _workspace_acts(
                reports=[
                    _report(payer=PAYER, stmt=STMT, finding="demo.f.box1.a1", value=1200.0),
                    _report(
                        payer=PAYER_C, stmt=STMT_C, finding="demo.f.box1.c1", value=1200.0
                    ),
                ],
                allocations=[
                    _alloc(
                        payer=PAYER,
                        stmt=STMT,
                        recipient=RECIPIENT,
                        finding="demo.f.pat.1",
                        value=800.0,
                        evidence="demo.evidence.alloc.pat",
                    ),
                    _alloc(
                        payer=PAYER,
                        stmt=STMT,
                        recipient="demo.recipient.kim",
                        finding="demo.f.kim.1",
                        value=450.0,
                        evidence="demo.evidence.alloc.kim",
                    ),
                    _alloc(
                        payer=PAYER_C,
                        stmt=STMT_C,
                        recipient="demo.recipient.sam",
                        finding="demo.f.sam.1",
                        value=400.0,
                        evidence="demo.evidence.alloc.sam",
                    ),
                ],
                close_box1=True,
            ),
            "demo.run.nominee-c10",
        )
        # Row COUNT on the durable closing ledger, before any symbol-keyed
        # collapse could merge a duplicate group outcome.
        closing_rows = self._nominee_rows(self._last_closing)
        self.assertEqual(len(closing_rows), 2, closing_rows)
        output_rows = self._nominee_rows(self._last_record)
        self.assertEqual(len(output_rows), 2, output_rows)
        suffix_a = _suffix(PAYER, STMT)
        suffix_c = _suffix(PAYER_C, STMT_C)
        self.assertEqual({row["symbol"] for row in closing_rows}, {suffix_a, suffix_c})
        self._assert_blocked_exceed(
            pubs,
            payer=PAYER,
            stmt=STMT,
            report_finding="demo.f.box1.a1",
            alloc_findings=["demo.f.pat.1", "demo.f.kim.1"],
            excluded_findings=["demo.f.sam.1", "demo.f.box1.c1"],
        )
        self._assert_supported(
            pubs,
            payer=PAYER_C,
            stmt=STMT_C,
            reduction="400",
            remainder="800",
            report_amount="1200",
            report_finding="demo.f.box1.c1",
            alloc_findings=["demo.f.sam.1"],
            excluded_findings=["demo.f.pat.1", "demo.f.kim.1", "demo.f.box1.a1"],
        )

    def test_c11_several_recipients_at_report_ceiling(self) -> None:
        pubs = self._live(
            _workspace_acts(
                reports=[_report(payer=PAYER, stmt=STMT, finding="demo.f.box1.a1", value=1200.0)],
                allocations=[
                    _alloc(
                        payer=PAYER,
                        stmt=STMT,
                        recipient=RECIPIENT,
                        finding="demo.f.pat.1",
                        value=700.0,
                        evidence="demo.evidence.alloc.pat",
                    ),
                    _alloc(
                        payer=PAYER,
                        stmt=STMT,
                        recipient="demo.recipient.kim",
                        finding="demo.f.kim.1",
                        value=500.0,
                        evidence="demo.evidence.alloc.kim",
                    ),
                ],
                close_box1=True,
            ),
            "demo.run.nominee-c11",
        )
        self._assert_supported(
            pubs,
            payer=PAYER,
            stmt=STMT,
            reduction="1200",
            remainder="0",
            report_amount="1200",
            report_finding="demo.f.box1.a1",
            alloc_findings=["demo.f.pat.1", "demo.f.kim.1"],
        )

    def test_c12_same_payer_over_allocation_does_not_absorb(self) -> None:
        pubs = self._live(
            _workspace_acts(
                reports=[
                    _report(
                        payer=PAYER_SHARED,
                        stmt=STMT,
                        finding="demo.f.box1.a1",
                        value=1200.0,
                    ),
                    _report(
                        payer=PAYER_SHARED,
                        stmt=STMT_B,
                        finding="demo.f.box1.b1",
                        value=2000.0,
                    ),
                ],
                allocations=[
                    _alloc(
                        payer=PAYER_SHARED,
                        stmt=STMT,
                        recipient=RECIPIENT,
                        finding="demo.f.pat.1",
                        value=800.0,
                        evidence="demo.evidence.alloc.pat",
                    ),
                    _alloc(
                        payer=PAYER_SHARED,
                        stmt=STMT,
                        recipient="demo.recipient.kim",
                        finding="demo.f.kim.1",
                        value=450.0,
                        evidence="demo.evidence.alloc.kim",
                    ),
                ],
                close_box1=True,
            ),
            "demo.run.nominee-c12",
        )
        self._assert_blocked_exceed(
            pubs,
            payer=PAYER_SHARED,
            stmt=STMT,
            report_finding="demo.f.box1.a1",
            alloc_findings=["demo.f.pat.1", "demo.f.kim.1"],
            excluded_findings=["demo.f.box1.b1"],
        )
        self._assert_no_reduction(pubs, _suffix(PAYER_SHARED, STMT_B))
        rows = self._nominee_rows(self._last_closing)
        self.assertEqual(len(rows), 1, rows)
        self.assertEqual(rows[0]["symbol"], _suffix(PAYER_SHARED, STMT))
        self.assertEqual(self._publication_value(pubs, B1_SUBTOTAL), Decimal("3200"))

    def test_c13_dependency_absent_names_the_composed_report_fact_id(self) -> None:
        pubs = self._live(
            _workspace_acts(
                reports=[],
                allocations=[
                    _alloc(
                        payer=PAYER,
                        stmt=STMT,
                        recipient=RECIPIENT,
                        finding="demo.f.pat.1",
                        value=450.0,
                        evidence="demo.evidence.alloc.pat",
                    )
                ],
            ),
            "demo.run.nominee-c13",
        )
        report_fact_id = derive_1099int_box1_fact_id(
            payer_name=PAYER, statement_reference=STMT, tax_year=YEAR
        )
        suffix = f"{PUBLISHES}|{report_fact_id}"
        self._assert_no_reduction(pubs, suffix)
        rows = self._nominee_rows(self._last_closing)
        self.assertEqual(len(rows), 1, rows)
        row = rows[0]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], DEPENDENCY_ABSENT)
        self.assertEqual(row["missing"], [report_fact_id])
        self.assertEqual(row["symbol"], suffix)
        self.assertEqual(self._input_pins(row), {"demo.f.pat.1"})

    def test_cross_year_2024_allocation_neither_contributes_nor_blocks(self) -> None:
        pubs = self._live(
            _workspace_acts(
                reports=[_report(payer=PAYER, stmt=STMT, finding="demo.f.box1.a1", value=1200.0)],
                allocations=[
                    _alloc(
                        payer=PAYER,
                        stmt=STMT,
                        recipient=RECIPIENT,
                        finding="demo.f.pat.1",
                        value=450.0,
                        evidence="demo.evidence.alloc.pat",
                    ),
                    _alloc(
                        payer=PAYER,
                        stmt=STMT,
                        recipient="demo.recipient.lee",
                        finding="demo.f.lee.1",
                        value=800.0,
                        evidence="demo.evidence.alloc.lee",
                        tax_year=2024,
                    ),
                ],
                close_box1=True,
            ),
            "demo.run.nominee-cross-year",
        )
        self._assert_supported(
            pubs,
            payer=PAYER,
            stmt=STMT,
            reduction="450",
            remainder="750",
            report_amount="1200",
            report_finding="demo.f.box1.a1",
            alloc_findings=["demo.f.pat.1"],
            excluded_findings=["demo.f.lee.1"],
        )
        for row in self._nominee_rows(self._last_closing):
            for missing in row.get("missing") or []:
                self.assertNotIn("tax-year=2024", str(missing))
            self.assertNotEqual(row.get("code"), NOMINEE_ALLOCATIONS_EXCEED_REPORT)

    def test_c1_pin_chain_reaches_report_allocations_rule_and_citation(self) -> None:
        acts = _c1_workspace()
        pubs = self._live(acts, "demo.run.nominee-provenance")
        finding = self._assert_supported(
            pubs,
            payer=PAYER,
            stmt=STMT,
            reduction="450",
            remainder="750",
            report_amount="1200",
            report_finding="demo.f.box1.a1",
            alloc_findings=["demo.f.pat.1"],
        )
        roles = {pin["role"]: pin for pin in finding["pins"]}
        self.assertEqual(roles["computation"]["id"], RULE_ID)
        self.assertEqual(roles["computation"]["version"], "v1")
        self.assertEqual(roles["citation"]["id"], CITATION_ID)
        self.assertEqual(roles["citation"]["version"], "v1")
        self.assertEqual(roles["adoption"]["id"], "tax.us.2025.package.core-calculations")
        self.assertEqual(roles["adoption"]["version"], "v36")
        # Attribution stays on the allocation assertion act; it is not copied
        # into the tax proposition.
        self.assertNotIn("recipient", finding)
        self.assertNotIn("evidence_ids", finding)
        assertion = next(
            act
            for act in acts
            if act.get("kind") == "assertion"
            and cast(dict[str, Any], act.get("payload", {})).get("finding", {}).get("id")
            == "demo.f.pat.1"
        )
        asserted = cast(dict[str, Any], assertion["payload"])["finding"]
        self.assertEqual(asserted["evidence_ids"], ["demo.evidence.alloc.pat"])
        self.assertEqual(assertion["actor"], USER)

    def test_legacy_nominee_subtotal_and_line2b_v6_ignore_the_new_prefix(self) -> None:
        """v36 still publishes the legacy subtotal and line-2b v6 as before.

        A current new-prefix reduction of $450 must not become a line-2b
        subtractand; line-2b keeps subtracting only the legacy nominee
        subtotal (here $100).
        """
        extra: list[tuple[str, dict[str, object]]] = [
            (
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": "demo.sb.nominee.instance.1",
                        "kind": "tax.us.scheduleb-adjustment-instance",
                        "label": "Synthetic legacy nominee instance",
                    }
                },
            ),
            (
                "member-transition",
                {
                    "family": {"id": LEGACY_NOMINEE_FAMILY, "version": "v1"},
                    "scope": SCOPE_KEY,
                    "member": {
                        "action": "assert",
                        "finding": _attested(
                            "demo.f.legacy.nominee.1",
                            f"{LEGACY_NOMINEE_AMOUNT}|tax-year=2025,adjustment-instance=demo.sb.nominee.instance.1",
                            100.0,
                        ),
                    },
                    "successor": {
                        "id": "demo.nominee.sb-nom.h1",
                        "predecessor": UG_NOMINEE_HORIZON,
                    },
                },
            ),
            (
                "assertion",
                {
                    "finding": _attested(
                        "demo.nominee.sb-nom.closure",
                        "tax.us.2025.scheduleb.adjustment.nominee.source-closure|"
                        "family-horizon=demo.nominee.sb-nom.h1,tax-year=2025",
                        True,
                    )
                },
            ),
        ]
        pubs = self._live(
            _workspace_acts(
                reports=[_report(payer=PAYER, stmt=STMT, finding="demo.f.box1.a1", value=1200.0)],
                allocations=[
                    _alloc(
                        payer=PAYER,
                        stmt=STMT,
                        recipient=RECIPIENT,
                        finding="demo.f.pat.1",
                        value=450.0,
                        evidence="demo.evidence.alloc.pat",
                    )
                ],
                close_box1=True,
                extra=extra,
            ),
            "demo.run.nominee-legacy-line2b",
        )
        self._assert_supported(
            pubs,
            payer=PAYER,
            stmt=STMT,
            reduction="450",
            remainder="750",
            report_amount="1200",
            report_finding="demo.f.box1.a1",
            alloc_findings=["demo.f.pat.1"],
        )
        self.assertEqual(self._publication_value(pubs, B1_SUBTOTAL), Decimal("1200"))
        self.assertEqual(self._publication_value(pubs, LEGACY_NOMINEE_SUBTOTAL), Decimal("100"))
        # 1200 box-1 less the $100 legacy nominee row; the new $450 reduction
        # is not a line-2b subtractand.
        self.assertEqual(self._publication_value(pubs, LINE2B_SYMBOL), Decimal("1100"))
        line2b = self._publication(pubs, LINE2B_SYMBOL)
        self.assertNotIn(PUBLISHES, json.dumps(line2b["pins"]))
        self.assertNotIn("demo.f.pat.1", json.dumps(line2b["pins"]))
        nominee = self._publication(pubs, _suffix(PAYER, STMT))
        self.assertNotIn(LEGACY_NOMINEE_AMOUNT, json.dumps(nominee["pins"]))
        self.assertNotIn("demo.f.legacy.nominee.1", json.dumps(nominee["pins"]))


if __name__ == "__main__":
    unittest.main()
