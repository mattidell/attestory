"""MD-C3 structural and two-layer Schedule-B tie-out evidence for the
seven-family market-discount Schedule B content successor."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.package_validation import PackageValidation, validate_package
from packages.derivation.runner import (
    ITEMIZATION_TIE_OUT_VIOLATION,
    InputFinding,
    RunContext,
    RunResult,
    SourceFact,
    run,
)


ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


def _corpus() -> dict[tuple[str, str], dict[str, Any]]:
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        value = json.loads(path.read_text("utf-8"))
        if isinstance(value.get("id"), str) and isinstance(value.get("version"), str):
            corpus[(value["id"], value["version"])] = value
    return corpus


def _package_result(attachment: dict[str, Any]) -> PackageValidation:
    corpus = _corpus()
    corpus[(attachment["id"], attachment["version"])] = attachment
    package = _load("package.core-calculations.v10.json")
    return validate_package(package, corpus, DerivationSchemas())


class StructuralAdmission(unittest.TestCase):
    def setUp(self) -> None:
        self.attachment = _load("rule.attachment.schedule-b.v3.json")

    def assert_code(self, attachment: dict[str, Any], code: str) -> None:
        result = _package_result(attachment)
        self.assertFalse(result.ok)
        self.assertIn(code, {issue.code for issue in result.issues})

    def test_md_p10_seven_row_sets_are_present(self) -> None:
        """MD-P10 groundwork: Part I carries exactly seven row sets."""
        self.assertEqual(len(self.attachment["itemizations"][0]["row_sets"]), 7)
        subtotals = {row["subtotal_symbol"] for row in self.attachment["itemizations"][0]["row_sets"]}
        self.assertIn("tax.us.2025.interest.b10-market-discount-subtotal", subtotals)
        self.assertIn("tax.us.2025.interest.oid-b5-market-discount-subtotal", subtotals)

    def test_md_n7_omitted_market_discount_slot_rejects(self) -> None:
        """MD-N7: a composition-backed part cannot omit a market-discount family."""
        malformed = copy.deepcopy(self.attachment)
        malformed["itemizations"][0]["row_sets"].pop()
        self.assert_code(malformed, "ATTACHMENT_COMPOSITION_BIJECTION_MISMATCH")

    def test_md_n7_wrong_member_or_subtotal_rejects(self) -> None:
        """MD-N7: family predicate and authorized subtotal are exact joins."""
        for key, value, code in (
            ("member_fact_type", {"id": "tax.us.2025.non-form-interest.amount", "version": "v1"}, "ATTACHMENT_ROW_MEMBER_MISMATCH"),
            ("subtotal_symbol", "tax.us.2025.interest.non-form-subtotal", "ATTACHMENT_ROW_SUBTOTAL_MISMATCH"),
        ):
            with self.subTest(key=key):
                malformed = copy.deepcopy(self.attachment)
                row_set = malformed["itemizations"][0]["row_sets"][-1]
                if key == "member_fact_type":
                    row_set["rows"][key] = value
                else:
                    row_set[key] = value
                self.assert_code(malformed, code)

    def test_md_n7_duplicate_market_discount_row_set_rejects(self) -> None:
        """MD-N7: duplicating a market-discount family fails structural admission."""
        malformed = copy.deepcopy(self.attachment)
        duplicate = copy.deepcopy(malformed["itemizations"][0]["row_sets"][-1])
        duplicate["subtotal_symbol"] = "demo.extra.subtotal"
        malformed["itemizations"][0]["row_sets"].append(duplicate)
        self.assert_code(malformed, "ATTACHMENT_COMPOSITION_BIJECTION_MISMATCH")


def _input(symbol: str, value: object) -> InputFinding:
    return InputFinding(symbol=symbol, value=value, finding_id=f"demo.finding.{symbol}", role="input")


def _run_attachment(*, b10_rows: list[str], b10_subtotal: str, line2b: str) -> RunResult:
    attachment = _load("rule.attachment.schedule-b.v3.json")
    subtotals = {
        "tax.us.2025.interest.b1-subtotal": "0",
        "tax.us.2025.interest.b3-subtotal": "0",
        "tax.us.2025.interest.oid-subtotal": "0",
        "tax.us.2025.interest.non-form-subtotal": "0",
        "tax.us.2025.interest.form1065-k1-box5-subtotal": "0",
        "tax.us.2025.interest.b10-market-discount-subtotal": b10_subtotal,
        "tax.us.2025.interest.oid-b5-market-discount-subtotal": "0",
        "tax.us.2025.interest.taxable-total": line2b,
        "tax.us.2025.dividends.1a-subtotal": "0",
        "tax.us.2025.dividends.ordinary-total": "0",
    }
    inputs = [_input(symbol, value) for symbol, value in subtotals.items()]
    inputs += [
        _input("tax.us.2025.scheduleb.foreign-account", "no"),
        _input("tax.us.2025.scheduleb.foreign-trust", "no"),
    ]
    sources = [
        SourceFact("tax.us.2025.f1099int.box10-market-discount", value, f"demo.md.row.{index}")
        for index, value in enumerate(b10_rows)
    ]
    return run(
        RunContext(
            run_id="demo.md.tieout",
            rules=[attachment],
            parameters={"tax.us.2025.parameter.schedule-b-threshold": _load("parameter.schedule-b-threshold.json")},
            canon=load_canon(DerivationSchemas()),
            inputs=inputs,
            sources=sources,
            adoption_pin={"role": "adoption", "id": "demo.adoption", "version": "v1"},
            governance_pins=[],
        ),
        DerivationSchemas(),
    )


class RuntimeTieOutContainment(unittest.TestCase):
    def test_md_n8_family_row_set_mismatch_blocks_attachment(self) -> None:
        """MD-N8: stale market-discount rows fail before whole-part publication."""
        result = _run_attachment(b10_rows=["1599"], b10_subtotal="1600", line2b="1600")
        row = result.dispositions[0]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], ITEMIZATION_TIE_OUT_VIOLATION)
        self.assertIn("demo.md.row.0", {pin["id"] for pin in row["pins"]})

    def test_md_n9_whole_part_mismatch_blocks_attachment(self) -> None:
        """MD-N9: tied market-discount rows still cannot diverge from line 2b."""
        result = _run_attachment(b10_rows=["1600"], b10_subtotal="1600", line2b="1601")
        row = result.dispositions[0]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], ITEMIZATION_TIE_OUT_VIOLATION)
        self.assertIn("part-i-interest:tax.us.2025.interest.taxable-total", row["missing"])


if __name__ == "__main__":
    unittest.main()
