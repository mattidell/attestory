"""Track 2 production evidence for nominee lifecycle and identity boundaries.

The cases in this module reuse the Track 1 synthetic workspace builders and
enter through the checksum-verified v38 package and ``live_coordinate_run``.
They close the retained lifecycle, missing-report, identity, and bounded-line
2b observations without widening the tax model.
"""

from __future__ import annotations

import copy
import json
import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.tax.nominee_allocation_recording import derive_nominee_allocation_fact_id
from packages.tax.loader import TAX_CONTENT_DIR
from packages.tax.nominee_consequences import (
    PUBLISHES as NOMINEE_PUBLISHES,
    RULE_ID as NOMINEE_RULE_ID,
)
from packages.tax.report_statement_identity import derive_1099int_box1_fact_id
from tests.test_form1099g_box1_schedule1_line7 import _act
from tests.test_nominee_consequences_live import (
    _alloc,
    _c1_workspace,
    _report,
    _workspace_acts,
)
from tests.test_nominee_interest_return_integration_track1 import (
    DERIVED_SUBTOTAL,
    LINE2B_SYMBOL,
    SCHEDULE_B_RULE_ID,
    SCHEDULE_B_SYMBOL,
    _publication,
    _run,
    _surface_v38,
    _v38_acts,
)
from tests.test_package_membership_wiring import ROOT, SCOPE, USER


CONTENT = TAX_CONTENT_DIR


def _allocation_assertion(
    *, finding_id: str, fact_id: str, value: float, evidence_id: str
) -> dict[str, object]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [evidence_id],
    }


def _append_allocation_correction(
    acts: list[dict[str, object]],
    *,
    finding_id: str,
    value: float,
    payer: str = "demo.payer.a",
    stmt: str = "demo.stmt.a",
    recipient: str = "demo.recipient.pat",
    evidence_id: str = "demo.evidence.alloc.pat",
) -> list[dict[str, object]]:
    result = [copy.deepcopy(dict(act)) for act in acts]
    fact_id = derive_nominee_allocation_fact_id(
        payer_name=payer,
        statement_reference=stmt,
        tax_year=2025,
        recipient_id=recipient,
    )
    result.append(
        _act(
            len(result),
            "assertion",
            {
                "finding": _allocation_assertion(
                    finding_id=finding_id,
                    fact_id=fact_id,
                    value=value,
                    evidence_id=evidence_id,
                )
            },
        )
    )
    return result


def _finish_v38(acts: list[dict[str, object]], run_id: str) -> tuple[Any, dict[str, Any], dict[str, Any]]:
    return _run(_v38_acts(acts, prefix=f"demo.track2.{run_id}.act"), run_id)


def _row(report: Mapping[str, Any], artifact_id: str, *, symbol: str | None = None) -> dict[str, Any]:
    rows = [
        cast(dict[str, Any], row)
        for row in report.get("dispositions", [])
        if row.get("artifact_id") == artifact_id
        and (symbol is None or row.get("symbol") == symbol)
    ]
    if len(rows) != 1:
        raise AssertionError(f"expected one {artifact_id!r}/{symbol!r} row, got {rows!r}")
    return rows[0]


def _publication_value(result: Any, symbol: str) -> Decimal:
    finding = _publication(result, symbol)
    if finding is None:
        raise AssertionError(f"missing publication {symbol!r}")
    return Decimal(str(finding["value"]))


def _schedule_b_value(result: Any) -> dict[str, Any] | None:
    finding = _publication(result, SCHEDULE_B_SYMBOL)
    if finding is None:
        return None
    return cast(dict[str, Any], finding["value"])


class Track2LifecycleAndBoundary(unittest.TestCase):
    def test_i9_correction_retraction_and_reassertion_use_only_current_support(self) -> None:
        corrected_base = _c1_workspace(finalize=False)
        corrected_acts = _append_allocation_correction(
            corrected_base, finding_id="demo.track2.alloc.corrected", value=400.0
        )
        corrected, corrected_report, _corrected_presentation = _finish_v38(
            corrected_acts, "i9-correction"
        )
        self.assertEqual(_publication_value(corrected, DERIVED_SUBTOTAL), Decimal("400"))
        self.assertEqual(_publication_value(corrected, LINE2B_SYMBOL), Decimal("800"))
        corrected_schedule_b = _schedule_b_value(corrected)
        self.assertIsNotNone(corrected_schedule_b)
        assert corrected_schedule_b is not None
        self.assertEqual(
            corrected_schedule_b["itemizations"][0]["adjustment_rows"][0]["subtotal"]["value"],
            "400.0",
        )
        self.assertEqual(
            _row(corrected_report, NOMINEE_RULE_ID)["disposition"], "published"
        )
        self.assertNotIn("demo.f.pat.1", json.dumps(corrected_report))

        retracted_acts = list(corrected_acts)
        retracted_acts.append(
            _act(
                len(retracted_acts),
                "finding-retracted",
                {"finding_id": "demo.track2.alloc.corrected"},
            )
        )
        retracted, retracted_report, retracted_presentation = _finish_v38(
            retracted_acts, "i9-retraction"
        )
        self.assertIsNone(_publication(retracted, DERIVED_SUBTOTAL))
        self.assertIsNone(_publication(retracted, NOMINEE_PUBLISHES))
        self.assertEqual(_publication_value(retracted, LINE2B_SYMBOL), Decimal("1200"))
        nominee_rows = [
            cast(dict[str, Any], row)
            for row in retracted_report.get("dispositions", [])
            if row.get("artifact_id") == NOMINEE_RULE_ID
        ]
        self.assertEqual(len(nominee_rows), 1)
        self.assertEqual(nominee_rows[0]["disposition"], "inapplicable")
        self.assertTrue(nominee_rows[0]["no_groups_selected"])
        self.assertIsNone(_publication(retracted, SCHEDULE_B_SYMBOL))
        schedule_b = next(
            attachment
            for attachment in retracted_presentation["attachments"]
            if attachment["id"] == SCHEDULE_B_RULE_ID
        )
        self.assertEqual(schedule_b["resolved"]["disposition"], "guard_inapplicable")
        self.assertNotIn("demo.track2.alloc.corrected", json.dumps(retracted_report))

        reasserted_acts = _append_allocation_correction(
            retracted_acts,
            finding_id="demo.track2.alloc.reasserted",
            value=250.0,
        )
        reasserted, reasserted_report, _reasserted_presentation = _finish_v38(
            reasserted_acts, "i9-reassertion"
        )
        self.assertEqual(_publication_value(reasserted, DERIVED_SUBTOTAL), Decimal("250"))
        self.assertEqual(_publication_value(reasserted, LINE2B_SYMBOL), Decimal("950"))
        self.assertEqual(
            _row(reasserted_report, NOMINEE_RULE_ID)["disposition"], "published"
        )
        self.assertNotIn("demo.track2.alloc.corrected", json.dumps(reasserted_report))
        self.assertNotIn("demo.f.pat.1", json.dumps(reasserted_report))

    def test_i10_retracted_report_blocks_its_group_and_dependents_only(self) -> None:
        report_a = _report(
            payer="demo.payer.track2.i10.a",
            stmt="demo.stmt.track2.i10.a",
            finding="demo.track2.i10.report.a",
            value=1200.0,
        )
        report_b = _report(
            payer="demo.payer.track2.i10.b",
            stmt="demo.stmt.track2.i10.b",
            finding="demo.track2.i10.report.b",
            value=900.0,
        )
        base = _workspace_acts(
            reports=[report_a, report_b],
            allocations=[
                {
                    "payer": report_a["payer"],
                    "stmt": report_a["stmt"],
                    "recipient": "demo.recipient.track2.i10.a",
                    "alloc_finding": "demo.track2.i10.alloc.a",
                    "alloc_value": 450.0,
                    "evidence": "demo.track2.i10.evidence.a",
                    "tax_year": 2025,
                },
                {
                    "payer": report_b["payer"],
                    "stmt": report_b["stmt"],
                    "recipient": "demo.recipient.track2.i10.b",
                    "alloc_finding": "demo.track2.i10.alloc.b",
                    "alloc_value": 300.0,
                    "evidence": "demo.track2.i10.evidence.b",
                    "tax_year": 2025,
                },
            ],
            close_box1=True,
            finalize=False,
        )
        report_a_fact_id = derive_1099int_box1_fact_id(
            payer_name=str(report_a["payer"]),
            statement_reference=str(report_a["stmt"]),
            tax_year=2025,
        )
        base.append(
            _act(
                len(base),
                "finding-retracted",
                {"finding_id": str(report_a["report_finding"])},
            )
        )
        result, report, presentation = _finish_v38(base, "i10-missing-current-report")

        suffix_a = f"{NOMINEE_PUBLISHES}|{report_a_fact_id}"
        report_b_fact_id = derive_1099int_box1_fact_id(
            payer_name=str(report_b["payer"]),
            statement_reference=str(report_b["stmt"]),
            tax_year=2025,
        )
        suffix_b = f"{NOMINEE_PUBLISHES}|{report_b_fact_id}"
        self.assertIsNone(_publication(result, suffix_a))
        self.assertEqual(_publication_value(result, suffix_b), Decimal("300"))
        blocked_group = _row(report, NOMINEE_RULE_ID, symbol=suffix_a)
        self.assertEqual(blocked_group["disposition"], "blocked")
        self.assertEqual(blocked_group["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(blocked_group["missing"], [report_a_fact_id])
        self.assertEqual(_row(report, NOMINEE_RULE_ID, symbol=suffix_b)["disposition"], "published")
        self.assertIsNone(_publication(result, DERIVED_SUBTOTAL))
        aggregate = _row(
            report,
            "tax.us.2025.rule.interest.derived-nominee-subtotal",
        )
        self.assertEqual(aggregate["disposition"], "blocked")
        self.assertEqual(aggregate["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(aggregate["missing"], [report_a_fact_id])
        line2b = _row(report, "tax.us.2025.rule.form1040-line2b")
        self.assertEqual(line2b["disposition"], "blocked")
        schedule_b = _row(report, SCHEDULE_B_RULE_ID)
        self.assertEqual(schedule_b["disposition"], "blocked")
        self.assertEqual(
            next(
                attachment
                for attachment in presentation["attachments"]
                if attachment["id"] == SCHEDULE_B_RULE_ID
            )["resolved"]["disposition"],
            "blocked",
        )
        surviving = _publication(result, suffix_b)
        self.assertIsNotNone(surviving)
        assert surviving is not None
        self.assertIn("demo.track2.i10.alloc.b", json.dumps(surviving))
        self.assertNotIn("demo.track2.i10.alloc.a", json.dumps(surviving))

    def test_i11_delimiter_identity_refuses_before_any_run_effect(self) -> None:
        recipient = "demo.recipient.pat,tax-year=1999"
        acts = _v38_acts(_workspace_acts(
            reports=[_report(payer="demo.payer.a", stmt="demo.stmt.a", finding="demo.f.i11.report", value=1200.0)],
            allocations=[
                _alloc(
                    payer="demo.payer.a",
                    stmt="demo.stmt.a",
                    recipient=recipient,
                    finding="demo.f.i11.alloc",
                    value=450.0,
                    evidence="demo.evidence.i11.alloc",
                )
            ],
            close_box1=True,
        ), prefix="demo.track2.i11.act")

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
                run_id="demo.track2.i11-delimiter",
                governance_pins=[],
                surface=_surface_v38(),
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

    def test_i11_normal_comma_identity_remains_usable_on_v38(self) -> None:
        acts = _v38_acts(
            _workspace_acts(
                reports=[
                    _report(
                        payer="Demo Bank, N.A.",
                        stmt="acct 12,345 / copy B",
                        finding="demo.track2.i11.comma.report",
                        value=1200.0,
                    )
                ],
                allocations=[
                    _alloc(
                        payer="Demo Bank, N.A.",
                        stmt="acct 12,345 / copy B",
                        recipient="demo.recipient.track2.i11.comma",
                        finding="demo.track2.i11.comma.alloc",
                        value=450.0,
                        evidence="demo.track2.i11.comma.evidence",
                    )
                ],
                close_box1=True,
            ),
            prefix="demo.track2.i11.comma.act",
        )
        result, _normal_report, _presentation = _run(acts, "demo.track2.i11-comma")
        self.assertIsNone(result.refusal)
        report_fact_id = derive_1099int_box1_fact_id(
            payer_name="Demo Bank, N.A.",
            statement_reference="acct 12,345 / copy B",
            tax_year=2025,
        )
        self.assertEqual(
            _publication_value(
                result,
                f"{NOMINEE_PUBLISHES}|{report_fact_id}",
            ),
            Decimal("450"),
        )

    def test_i12_taxable_total_remains_a_bounded_line2b_standin(self) -> None:
        result, _report, _presentation = _run(
            _v38_acts(_c1_workspace(), prefix="demo.track2.i12.act"),
            "demo.track2.i12",
        )
        self.assertEqual(_publication_value(result, LINE2B_SYMBOL), Decimal("750"))
        package = json.loads(
            (CONTENT / "package.core-calculations.v38.json").read_text("utf-8")
        )
        self.assertEqual(package["version"], "v38")
        line2b_members = [
            member
            for member in package["members"]
            if member.get("id") == "tax.us.2025.form1040.line-2b"
        ]
        self.assertEqual(len(line2b_members), 1)
        self.assertEqual(line2b_members[0]["role"], "form-field")
        self.assertEqual(line2b_members[0]["schema"], "form-field.v3")
        self.assertEqual(line2b_members[0]["version"], "v5")

        form_field = json.loads(
            (CONTENT / "form1040.line-2b.form-field.v5.json").read_text("utf-8")
        )
        self.assertEqual(form_field["id"], "tax.us.2025.form1040.line-2b")
        self.assertEqual(form_field["schema"], "form-field.v3")
        self.assertEqual(form_field["version"], "v5")
        self.assertEqual(form_field["binds_symbol"], LINE2B_SYMBOL)
        self.assertNotEqual(
            form_field["binds_symbol"], "tax.us.2025.form1040.line-2b"
        )

        description = form_field["description"]
        self.assertIn("exact seven-family positive taxable interest", description)
        for adjustment in ("Nominee Distribution", "Accrued Interest", "ABP Adjustment"):
            self.assertIn(adjustment, description)
        self.assertNotIn("complete 2025 taxable-interest", description.lower())
        self.assertNotIn("filing support", description.lower())

        published_explain = form_field["dispositions"]["published_value"]["explain"]
        self.assertIn("seven-family positive interest total", published_explain)
        self.assertIn("exact contributed and closed Schedule B adjustment classes", published_explain)
        self.assertNotIn("complete 2025 taxable-interest", published_explain.lower())
        self.assertNotIn("filing support", published_explain.lower())


if __name__ == "__main__":
    unittest.main()
