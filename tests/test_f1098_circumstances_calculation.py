"""Track 2 mortgage circumstance calculation on the production v44 surface.

Cases use the established synthetic return corpus and add production
circumstance answers directly. Each result is obtained through
``live_coordinate_run``; dispositions are checked in the durable report,
while published values are checked on the coordinator result and presentation.
"""
from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.derivation.production_resolver import PublicationSurface
from packages.tax.loader import TAX_CONTENT_DIR
from tests.test_f1098_v43_debt_limit_fix import (
    RELEASE_DIR,
    _case_acts as _v43_case_acts,
    _current_adoption,
    _selected_current_dependency_acts,
    _read_json,
)
from tests.test_f1098e_student_loan_interest_agi_track6 import (
    CLOSURE_TYPE as F1098E_CLOSURE_TYPE,
    FAMILY_ID as F1098E_FAMILY_ID,
    Statement as F1098EStatement,
    _f1098e_acts,
)
from tests.test_f1098_mortgage_interest_line12e_track2 import (  # type: ignore[attr-defined]
    ATTACHMENT_ID,
    SCOPE,
    USER,
    _attested,
    _member_fact_id,
    _f1098_acts,
    _load_fixture_adoption,
    _schedule_a_tie_out_value,
)
from tests.test_form1099g_box1_schedule1_line7 import _published_numeric

ROOT = Path(__file__).resolve().parents[1]
CONTENT = TAX_CONTENT_DIR
PACKAGE_PATH = CONTENT / "package.core-calculations.v44.json"
REGISTRY_PATH = CONTENT / "published-packages.v42.json"
RELEASE_PATH = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v42.json"

LINE8A = "tax.us.2025.schedule-a.line8a"
LINE8A_RULE = "tax.us.2025.rule.f1098-line8a"
REASON = "tax.us.2025.f1098.residence-interest-reason"
REASON_RULE = "tax.us.2025.rule.f1098-residence-interest-reason"
UNRESOLVED_RULE = "tax.us.2025.rule.f1098-residence-interest-unresolved"
UNRESOLVED_FIELD = "tax.us.2025.form.f1098.residence-interest-unresolved"
UNRESOLVED_LINE = "f1098-unresolved"
STANDARD = 15000.0
FACT = "tax.us.2025.f1098."
DEFAULT_ANSWERS = {
    "owns-the-home": "yes",
    "lives-there-most-of-the-time": "yes",
    "home-is-collateral": "yes",
    "owes-the-loan": "yes",
    "paid-the-interest": "yes",
    "no-one-else-owes-it": "yes",
    "this-is-the-original-loan": "yes",
    "what-the-money-paid-for": "bought-the-home",
    "mortgage-credit-certificate-received": "not-received",
}


def _statement_rows(interest: float | None, second_interest: float | None) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    if interest is not None:
        rows.append(("demo.f1098.lender.a", "demo.f1098.stmt.a"))
    if second_interest is not None:
        rows.append(("demo.f1098.lender.b", "demo.f1098.stmt.b"))
    return rows


def _selected_dependency_acts(*, student_interest: float | None = None) -> list[dict[str, object]]:
    if student_interest is None:
        return _selected_current_dependency_acts()
    statements = [F1098EStatement(lender="demo.f1098e.lender.v44", stmt="demo.f1098e.stmt.v44", box1=student_interest)]
    rows = _f1098e_acts(statements=statements, close=True, wages=90000)
    selected: list[dict[str, object]] = []
    for row in rows:
        payload = row.get("payload", {})
        if not isinstance(payload, dict):
            continue
        bundle = payload.get("bundle")
        if isinstance(bundle, dict) and bundle.get("id") in {
            "tax.us.2025.f1098e.vocabulary", "tax.us.2025.sli-scope.vocabulary"
        }:
            selected.append(copy.deepcopy(row))
            continue
        family = payload.get("family")
        if row.get("kind") == "horizon-genesis" and isinstance(family, dict) and family.get("id") == F1098E_FAMILY_ID:
            selected.append(copy.deepcopy(row))
            continue
        finding = payload.get("finding")
        if row.get("kind") == "member-transition" and isinstance(payload.get("member"), dict):
            finding = payload["member"].get("finding")
        fact_id = finding.get("fact_id") if isinstance(finding, dict) else None
        if row.get("kind") in {"assertion", "member-transition"} and isinstance(fact_id, str):
            if fact_id.startswith(F1098E_CLOSURE_TYPE + "|") or fact_id.startswith("tax.us.2025.f1098e."):
                selected.append(copy.deepcopy(row))
            elif fact_id.startswith("tax.us.2025.sli-scope."):
                selected.append(copy.deepcopy(row))
        entity = payload.get("entity")
        if row.get("kind") == "entity-introduced" and isinstance(entity, dict) and str(entity.get("id", "")).startswith("demo.f1098e."):
            selected.append(copy.deepcopy(row))
    return selected


def _acts(
    interest: float | None,
    *,
    answers: dict[str, str | None] | None = None,
    answer_history: dict[str, list[str]] | None = None,
    retract_answer: str | None = None,
    box2: float = 200000.0,
    box3: str = "2020-06-01",
    box9: float = 1.0,
    filing_status: str | None = None,
    omit_box2: bool = False,
    second_interest: float | None = None,
    student_interest: float | None = None,
    legacy_authority_overrides: dict[str, str] | None = None,
    unclosed_family: bool = False,
) -> list[dict[str, object]]:
    """Extend the proven v43 return acts with direct Track 1 answers."""
    if second_interest is None:
        acts = _v43_case_acts(
            interest,
            box2=box2,
            filing_status=filing_status,
            omit_box2=omit_box2,
            authority_overrides=legacy_authority_overrides,
        )
    else:
        if interest is None:
            raise ValueError("multiple statements require a first statement")
        acts = _f1098_acts(
            interest=interest,
            box2=box2,
            box3=box3,
            box9=box9,
            second_statement_interest=second_interest,
            authority_overrides=legacy_authority_overrides,
            wages=90000,
        )
        acts.pop()  # replace the v29 adoption with the current package adoption
        acts.extend(_selected_dependency_acts(student_interest=student_interest))
        acts.append(_current_adoption(_load_fixture_adoption(), len(acts)))
    for row in acts:
        payload = row.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        fact_id = finding.get("fact_id") if isinstance(finding, dict) else None
        if not isinstance(fact_id, str):
            continue
        finding_map = cast(dict[str, Any], finding)
        if fact_id.startswith(FACT + "box3-origination-date|"):
            finding_map["value"] = box3
        elif fact_id.startswith(FACT + "box9-number-of-properties|"):
            finding_map["value"] = box9
    adoption = acts.pop()
    # Replace the proven closed-empty Form 1098-E dependency setup when this
    # case exercises an existing nonempty student-loan statement on v44.
    if student_interest is not None and second_interest is None:
        acts = [
            row for row in acts
            if not (
                (row.get("kind") in {"assertion", "horizon-genesis", "bundle-adoption"})
                and isinstance(row.get("payload"), dict)
                and (
                    row.get("kind") == "bundle-adoption"
                    and isinstance(cast(dict[str, Any], row["payload"]).get("bundle"), dict)
                    and cast(dict[str, Any], cast(dict[str, Any], row["payload"]).get("bundle")).get("id") == "tax.us.2025.f1098e.vocabulary"
                    or
                    row.get("kind") == "horizon-genesis"
                    and isinstance(cast(dict[str, Any], row["payload"]).get("family"), dict)
                    and cast(dict[str, Any], cast(dict[str, Any], row["payload"]).get("family")).get("id") == F1098E_FAMILY_ID
                    or isinstance(cast(dict[str, Any], row["payload"]).get("finding"), dict)
                    and str(cast(dict[str, Any], cast(dict[str, Any], row["payload"]).get("finding")).get("fact_id", "")).startswith(("tax.us.2025.f1098e.", F1098E_CLOSURE_TYPE + "|"))
                )
            )
        ]
        acts.extend(_selected_dependency_acts(student_interest=student_interest))
    if omit_box2:
        acts = [
            row for row in acts
            if not (
                row.get("kind") == "assertion"
                and isinstance(row.get("payload"), dict)
                and isinstance(cast(dict[str, Any], row["payload"]).get("finding"), dict)
                and str(cast(dict[str, Any], cast(dict[str, Any], row["payload"]).get("finding")).get("fact_id", "")).startswith(
                    FACT + "box2-outstanding-principal|"
                )
            )
        ]
    acts.append({
        "schema": "act.v1",
        "act_id": "demo.f1098.t2.circumstances.bundle",
        "kind": "bundle-adoption",
        "actor": USER,
        "at": "2026-10-14T20:30:00Z",
        "committed_against": len(acts),
        "payload": {"bundle": _read_json(CONTENT / "f1098-circumstances.bundle.json")},
    })
    answers = {**DEFAULT_ANSWERS, **(answers or {})}
    answer_history = answer_history or {}
    retracted_finding_id: str | None = None
    serial = 0
    for payer, statement in _statement_rows(interest, second_interest):
        for suffix in (*DEFAULT_ANSWERS, "loan-timing-relative-to-purchase", "loan-timing-relative-to-building-or-improving"):
            history = answer_history.get(suffix)
            values = history if history is not None else [answers.get(suffix)]
            for value in values:
                if value is None:
                    continue
                fact_id = _member_fact_id(FACT + suffix, payer, statement)
                finding_id = f"demo.f1098.t2.circumstance.{serial}"
                finding = _attested(finding_id, fact_id, value)
                acts.append({
                    "schema": "act.v1",
                    "act_id": f"demo.f1098.t2.answer-act.{serial}",
                    "kind": "assertion",
                    "actor": USER,
                    "at": "2026-10-14T20:30:00Z",
                    "committed_against": len(acts),
                    "payload": {"finding": finding},
                })
                if suffix == retract_answer:
                    retracted_finding_id = finding_id
                serial += 1
    if unclosed_family:
        acts = [
            row for row in acts
            if not (
                row.get("kind") == "assertion"
                and isinstance(row.get("payload"), dict)
                and isinstance(cast(dict[str, Any], row["payload"]).get("finding"), dict)
                and str(cast(dict[str, Any], cast(dict[str, Any], row["payload"]).get("finding")).get("fact_id", "")).startswith(
                    FACT + "source-closure|"
                )
            )
        ]
    if retracted_finding_id is not None:
        acts.append({
            "schema": "act.v1",
            "act_id": "demo.f1098.t2.withdraw-answer",
            "kind": "finding-retracted",
            "actor": USER,
            "at": "2026-10-14T20:31:00Z",
            "committed_against": len(acts),
            "payload": {"finding_id": retracted_finding_id},
        })
    pkg = _read_json(PACKAGE_PATH)
    release = _read_json(RELEASE_PATH)
    adoption = copy.deepcopy(adoption)
    adoption["act_id"] = "demo.f1098.v44.adopt-current"
    adoption["committed_against"] = len(acts)
    payload = cast(dict[str, Any], adoption["payload"])
    payload["package"] = {"id": pkg["id"], "version": pkg["version"], "checksum": pkg["package_checksum"]}
    payload["release"] = {
        "id": release["id"],
        "version": release["version"],
        "checksum": hashlib.sha256(RELEASE_PATH.read_bytes()).hexdigest(),
    }
    payload["revision"] = len(acts)
    payload["audit"] = {"note": "synthetic mortgage circumstance calculation"}
    acts.append(adoption)
    for index, row in enumerate(acts):
        row["committed_against"] = index
    return acts


def _run(name: str, interest: float | None, **kwargs: Any) -> tuple[dict[str, Any], dict[str, Any], Any]:
    acts = _acts(interest, **kwargs)
    with TemporaryDirectory(prefix="f1098-circumstance-calculation-") as tmp:
        result = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "workspace"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=f"demo.f1098.v44.{name}",
            governance_pins=[],
            surface=PublicationSurface(RELEASE_DIR, REGISTRY_PATH, CONTENT),
            output_name="out.json",
        )
        if result.refusal is not None:
            raise AssertionError(f"v44 published package refused: {result.refusal!r}")
        assert result.output_path is not None and result.presentation_path is not None
        return (
            cast(dict[str, Any], json.loads(result.output_path.read_text("utf-8"))),
            cast(dict[str, Any], json.loads(result.presentation_path.read_text("utf-8"))),
            result,
        )


def _rows(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["artifact_id"]: row for row in report.get("dispositions", [])}


def _published(result: Any, symbol: str) -> list[Any]:
    return [
        pub.finding.get("value")
        for pub in result.publications or ()
        if pub.finding.get("symbol") == symbol or str(pub.finding.get("symbol", "")).startswith(symbol + "|")
    ]


def _input_pins(result: Any, symbol: str) -> set[str]:
    findings = [
        pub.finding for pub in result.publications or ()
        if pub.finding.get("symbol") == symbol or str(pub.finding.get("symbol", "")).startswith(symbol + "|")
    ]
    if len(findings) != 1:
        raise AssertionError(f"expected one publication for {symbol}; got {len(findings)}")
    return {pin["id"] for pin in findings[0].get("pins", []) if pin.get("role") == "input"}


def _reason(result: Any) -> Any:
    values = _published(result, REASON)
    return values[0] if values else None


def _field(model: dict[str, Any]) -> dict[str, Any]:
    return next(section for section in model["sections"] if section["field"]["id"] == UNRESOLVED_FIELD)


class MortgageCircumstanceCalculation(unittest.TestCase):
    def test_supported_purchase_and_schedule_a_tie_out(self) -> None:
        report, model, result = _run("supported-purchase", 20000.0)
        rows = _rows(report)
        self.assertEqual(rows[LINE8A_RULE]["disposition"], "published")
        self.assertEqual(rows[REASON_RULE]["disposition"], "published")
        self.assertEqual(rows[UNRESOLVED_RULE]["disposition"], "inapplicable")
        self.assertEqual(_published(result, LINE8A), ["20000.0"])
        self.assertEqual(_reason(result), "qualified")
        self.assertEqual(_published_numeric(model, "line-12e"), 20000.0)
        self.assertEqual(_published_numeric(model, "line-15"), 70000.0)
        attachment = next(item for item in model["attachments"] if item["id"] == ATTACHMENT_ID)
        self.assertEqual(attachment["resolved"]["disposition"], "published")
        self.assertEqual(_schedule_a_tie_out_value(model), 20000.0)
        self.assertEqual(_field(model)["resolved"]["disposition"], "guard_inapplicable")

    def test_supported_below_standard_and_zero_interest_stay_qualified(self) -> None:
        for label, interest in (("below-standard", 5000.0), ("zero-interest", 0.0)):
            report, model, result = _run(label, interest)
            rows = _rows(report)
            self.assertEqual(rows[LINE8A_RULE]["disposition"], "published")
            self.assertEqual(_reason(result), "qualified")
            self.assertEqual(_published(result, LINE8A), [f"{interest:.1f}"])
            self.assertEqual(_published_numeric(model, "line-12e"), STANDARD)

    def test_determined_zeros_and_decisive_precedence(self) -> None:
        cases: tuple[tuple[str, dict[str, str], str], ...] = (
            ("personal-zero", {"what-the-money-paid-for": "unrelated-personal-expense", "loan-timing-relative-to-purchase": "no", "loan-timing-relative-to-building-or-improving": "no"}, "use-unrelated-personal-expense"),
            ("collateral-priority", {"home-is-collateral": "no", "what-the-money-paid-for": "unrelated-personal-expense"}, "not-collateral"),
            ("payment-priority", {"paid-the-interest": "no", "what-the-money-paid-for": "unrelated-personal-expense"}, "not-paid"),
        )
        for name, answers, expected_reason in cases:
            report, model, result = _run(name, 20000.0, answers=answers)
            rows = _rows(report)
            self.assertEqual(rows[LINE8A_RULE]["disposition"], "published")
            self.assertEqual(_published(result, LINE8A), ["0"])
            self.assertEqual(_reason(result), expected_reason)
            self.assertEqual(_published_numeric(model, "line-12e"), STANDARD)
            self.assertEqual(rows[UNRESOLVED_RULE]["disposition"], "inapplicable")
            self.assertEqual(_field(model)["resolved"]["disposition"], "guard_inapplicable")

    def test_partial_payment_and_payment_uncertainty_never_publish_amount(self) -> None:
        for name, value, expected in (
            ("partial-payment", "paid-by-others-or-partial", "payment-outside-coverage"),
            ("uncertain-payment", "cannot-tell", "cannot-tell-payment"),
        ):
            report, model, result = _run(name, 20000.0, answers={"paid-the-interest": value})
            rows = _rows(report)
            self.assertEqual(rows[LINE8A_RULE]["disposition"], "blocked")
            self.assertNotIn(LINE8A, [pub.finding.get("symbol") for pub in result.publications or ()])
            self.assertEqual(_reason(result), expected)
            self.assertEqual(rows[UNRESOLVED_RULE]["disposition"], "blocked")
            field = _field(model)
            self.assertEqual(field["resolved"]["disposition"], "blocked")
            self.assertTrue(field["resolved"]["reasons"])

    def test_personal_expense_timing_defaults_exceptions_and_grandfather_boundary(self) -> None:
        cases: tuple[tuple[str, dict[str, str], str, str], ...] = (
            ("purchase-yes-over-missing", {"what-the-money-paid-for": "unrelated-personal-expense", "loan-timing-relative-to-purchase": "yes"}, "timing-exception-possible", "blocked"),
            ("missing-over-building-cleared", {"what-the-money-paid-for": "unrelated-personal-expense", "loan-timing-relative-to-building-or-improving": "no"}, "timing-not-established", "blocked"),
            ("timing-cannot-tell", {"what-the-money-paid-for": "unrelated-personal-expense", "loan-timing-relative-to-purchase": "cannot-tell", "loan-timing-relative-to-building-or-improving": "no"}, "cannot-tell-timing", "blocked"),
            ("grandfather-before", {"what-the-money-paid-for": "unrelated-personal-expense", "loan-timing-relative-to-purchase": "no", "loan-timing-relative-to-building-or-improving": "no"}, "possible-grandfathered-debt", "blocked"),
            ("grandfather-on-cutoff", {"what-the-money-paid-for": "unrelated-personal-expense", "loan-timing-relative-to-purchase": "no", "loan-timing-relative-to-building-or-improving": "no"}, "possible-grandfathered-debt", "blocked"),
            ("grandfather-after", {"what-the-money-paid-for": "unrelated-personal-expense", "loan-timing-relative-to-purchase": "no", "loan-timing-relative-to-building-or-improving": "no"}, "use-unrelated-personal-expense", "published"),
        )
        dates = {"grandfather-before": "1987-10-12", "grandfather-on-cutoff": "1987-10-13", "grandfather-after": "1987-10-14"}
        for name, answers, expected, amount_disposition in cases:
            report, _model, result = _run(name, 20000.0, answers=answers, box3=dates.get(name, "2020-06-01"))
            rows = _rows(report)
            self.assertEqual(rows[LINE8A_RULE]["disposition"], amount_disposition)
            self.assertEqual(_reason(result), expected)
            if amount_disposition == "published":
                self.assertEqual(_published(result, LINE8A), ["0"])
            else:
                self.assertEqual(_published(result, LINE8A), [])

    def test_box2_limit_filing_status_and_missing_principal(self) -> None:
        cases: tuple[tuple[str, dict[str, str], float, str | None, bool, str, str | None], ...] = (
            ("at-limit", {}, 750000.0, None, False, "published", "qualified"),
            ("over-limit", {}, 800000.0, None, False, "blocked", "debt-limit-over"),
            ("mfs-under-limit", {}, 300000.0, "married_filing_separately", False, "published", "qualified"),
            ("mfs-over-limit", {}, 500000.0, "married_filing_separately", False, "blocked", "debt-limit-over"),
            ("missing-box2", {}, 200000.0, None, True, "blocked", None),
        )
        for name, answers, box2, filing_status, omit_box2, disposition, expected_reason in cases:
            report, _model, result = _run(name, 20000.0, answers=answers, box2=box2, filing_status=filing_status, omit_box2=omit_box2)
            rows = _rows(report)
            self.assertEqual(rows[LINE8A_RULE]["disposition"], disposition)
            self.assertEqual(_reason(result), expected_reason)
            self.assertEqual(_published(result, LINE8A), ["20000.0"] if disposition == "published" else [])
        report, model, result = _run("mfj-spouse-answers", 20000.0, filing_status="married_filing_jointly")
        self.assertEqual(_reason(result), "qualified")
        self.assertEqual(_published_numeric(model, "line-12e"), 30000.0)

    def test_uncertain_and_outside_coverage_reasons(self) -> None:
        cases: tuple[tuple[str, dict[str, str], str], ...] = (
            ("ownership-uncertain", {"owns-the-home": "cannot-tell"}, "cannot-tell-ownership"),
            ("residence-uncertain", {"lives-there-most-of-the-time": "cannot-tell"}, "cannot-tell-residence"),
            ("share-uncertain", {"no-one-else-owes-it": "cannot-tell"}, "cannot-tell-share"),
            ("collateral-uncertain", {"home-is-collateral": "cannot-tell"}, "cannot-tell-collateral"),
            ("use-uncertain", {"what-the-money-paid-for": "cannot-tell"}, "cannot-tell-use"),
            ("owner-not-on-note", {"owes-the-loan": "no"}, "owner-not-on-note"),
            ("certificate-received", {"mortgage-credit-certificate-received": "received"}, "certificate-received"),
            ("refinance-outside", {"this-is-the-original-loan": "no"}, "outside-coverage"),
            ("other-use-outside", {"what-the-money-paid-for": "other"}, "outside-coverage"),
            ("multi-property-outside", {}, "outside-coverage"),
        )
        for name, answers, expected_reason in cases:
            kwargs = {"box9": 2.0} if name == "multi-property-outside" else {}
            report, model, result = _run(name, 20000.0, answers=answers, **kwargs)
            rows = _rows(report)
            self.assertEqual(_reason(result), expected_reason)
            self.assertEqual(rows[LINE8A_RULE]["disposition"], "blocked")
            self.assertEqual(_published(result, LINE8A), [])
            self.assertEqual(_published_numeric(model, "line-12e")["disposition"], "blocked")
            self.assertEqual(rows[UNRESOLVED_RULE]["disposition"], "blocked")

    def test_missing_new_answer_does_not_borrow_legacy_confirmation(self) -> None:
        report, model, result = _run("missing-new-payment", 20000.0, answers={"paid-the-interest": None})
        rows = _rows(report)
        self.assertEqual(rows[LINE8A_RULE]["disposition"], "blocked")
        self.assertEqual(rows[REASON_RULE]["disposition"], "blocked")
        self.assertEqual(_published(result, LINE8A), [])
        self.assertEqual(_published_numeric(model, "line-12e")["disposition"], "blocked")
        self.assertEqual(rows[UNRESOLVED_RULE]["disposition"], "blocked")
        fallback = _field(model)["resolved"].get("reasons", [])
        self.assertTrue(fallback)
        self.assertIn("available information", fallback[0]["sentence"])

    def test_opposite_legacy_confirmation_does_not_override_current_answer(self) -> None:
        report, _model, result = _run(
            "legacy-no-current-yes", 20000.0,
            answers={"what-the-money-paid-for": "bought-the-home"},
            legacy_authority_overrides={"acquisition-debt-use": "no"},
        )
        self.assertEqual(_rows(report)[LINE8A_RULE]["disposition"], "published")
        self.assertEqual(_reason(result), "qualified")
        report, _model, result = _run(
            "legacy-yes-current-no", 20000.0,
            answers={"what-the-money-paid-for": "unrelated-personal-expense", "loan-timing-relative-to-purchase": "no", "loan-timing-relative-to-building-or-improving": "no"},
            legacy_authority_overrides={"acquisition-debt-use": "yes"},
        )
        self.assertEqual(_rows(report)[LINE8A_RULE]["disposition"], "published")
        self.assertEqual(_reason(result), "use-unrelated-personal-expense")
        self.assertEqual(_published(result, LINE8A), ["0"])

    def test_correction_and_withdrawal_use_only_current_or_reserved_default(self) -> None:
        report, _model, result = _run(
            "payment-corrected-to-no",
            20000.0,
            answer_history={"paid-the-interest": ["yes", "no"]},
        )
        self.assertEqual(_reason(result), "not-paid")
        self.assertEqual(_published(result, LINE8A), ["0"])
        for symbol in (LINE8A, REASON):
            pins = _input_pins(result, symbol)
            self.assertIn("demo.f1098.t2.circumstance.5", pins)
            self.assertNotIn("demo.f1098.t2.circumstance.4", pins)
        report, _model, result = _run(
            "payment-correction-withdrawn",
            20000.0,
            answer_history={"paid-the-interest": ["yes", "no"]},
            retract_answer="paid-the-interest",
        )
        self.assertEqual(_rows(report)[LINE8A_RULE]["disposition"], "blocked")
        self.assertIsNone(_reason(result))
        self.assertEqual(_rows(report)[REASON_RULE]["disposition"], "blocked")
        self.assertIn("tax.us.2025.f1098.paid-the-interest", _rows(report)[REASON_RULE]["missing"])
        self.assertEqual(_published(result, LINE8A), [])
        report, _model, result = _run(
            "timing-withdrawn",
            20000.0,
            answers={"what-the-money-paid-for": "unrelated-personal-expense", "loan-timing-relative-to-purchase": None, "loan-timing-relative-to-building-or-improving": "no"},
            answer_history={"loan-timing-relative-to-purchase": ["no"]},
            retract_answer="loan-timing-relative-to-purchase",
        )
        self.assertEqual(_reason(result), "timing-not-established")
        self.assertEqual(_published(result, LINE8A), [])

    def test_multiple_statement_and_unclosed_family_do_not_publish_single_amount(self) -> None:
        report, _model, result = _run("multiple-statements", 20000.0, second_interest=1000.0)
        self.assertEqual(_rows(report)[LINE8A_RULE]["disposition"], "blocked")
        self.assertEqual(_rows(report)[LINE8A_RULE]["code"], "MULTIPLE_F1098_OUT_OF_SCOPE")
        self.assertEqual(_published(result, LINE8A), [])
        report, _model, result = _run("unclosed-family", 20000.0, unclosed_family=True)
        self.assertEqual(_rows(report)[LINE8A_RULE]["disposition"], "blocked")
        self.assertEqual(_rows(report)[LINE8A_RULE]["code"], "SOURCE_SET_UNCLOSED")
        self.assertEqual(_published(result, LINE8A), [])

    def test_closed_empty_path_and_old_publication_bytes_remain_available(self) -> None:
        report, model, result = _run("no-statement", None)
        self.assertEqual(_rows(report)[LINE8A_RULE]["disposition"], "inapplicable")
        self.assertEqual(_published_numeric(model, "line-12e"), STANDARD)
        self.assertEqual(_field(model)["resolved"]["disposition"], "guard_inapplicable")

    def test_nonempty_student_loan_case_remains_available_on_v44(self) -> None:
        report, model, result = _run("student-loan-compatibility", 20000.0, student_interest=3000.0)
        rows = _rows(report)
        self.assertEqual(rows[LINE8A_RULE]["disposition"], "published")
        self.assertEqual(_published(result, LINE8A), ["20000.0"])
        self.assertEqual(_published_numeric(model, "line-12e"), 20000.0)
        self.assertEqual(rows["tax.us.2025.rule.sli-worksheet"]["disposition"], "published")
        self.assertEqual(
            _published(result, "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal"),
            ["3000"],
        )
        self.assertEqual(
            _published(result, "tax.us.2025.schedule1.line21-sli-deduction"),
            ["1668"],
        )
        old_package = _read_json(CONTENT / "package.core-calculations.v43.json")
        new_package = _read_json(PACKAGE_PATH)
        self.assertEqual(old_package["version"], "v43")
        self.assertEqual(old_package["package_checksum"], package_instance_checksum(old_package))
        self.assertEqual(new_package["schema"], "artifact-package.v36")
        self.assertEqual(new_package["version"], "v44")
        self.assertEqual(new_package["package_checksum"], package_instance_checksum(new_package))
        members = {(m["id"], m["version"]) for m in new_package["members"]}
        self.assertNotIn(("tax.us.2025.schedule-a.line8a.rule", "v2"), members)
        registry = _read_json(REGISTRY_PATH)
        indexed = {(x["id"], x["version"]): x["checksum"] for x in registry["citizens"]}
        for filename in (
            "f1098-circumstances.bundle.json",
            "parameter.f1098-timing-building-structural-default.json",
            "parameter.f1098-timing-purchase-structural-default.json",
            "parameter.f1098-box9-default-single-property.json",
            "rule.f1098-line8a.json",
            "rule.f1098-residence-interest-reason.json",
            "rule.f1098-residence-interest-unresolved.json",
            "f1098.residence-interest-unresolved.form-field.json",
        ):
            citizen = _read_json(CONTENT / filename)
            self.assertEqual(indexed[(citizen["id"], citizen["version"])], citizen_checksum(citizen))


if __name__ == "__main__":
    unittest.main()
