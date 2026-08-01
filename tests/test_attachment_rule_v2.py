"""K1-C3 structural and two-layer Schedule-B tie-out evidence."""

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
from packages.kernel.schema_registry import SchemaValidationError


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
    package = _load("package.core-calculations.v9.json")
    return validate_package(package, corpus, DerivationSchemas())


class StructuralAdmission(unittest.TestCase):
    def setUp(self) -> None:
        self.attachment = _load("rule.attachment.schedule-b.v2.json")

    def assert_code(self, attachment: dict[str, Any], code: str) -> None:
        result = _package_result(attachment)
        self.assertFalse(result.ok)
        self.assertIn(code, {issue.code for issue in result.issues})

    def test_schema_rejects_empty_row_sets(self) -> None:
        malformed = copy.deepcopy(self.attachment)
        malformed["itemizations"][0]["row_sets"] = []
        with self.assertRaises(SchemaValidationError):
            DerivationSchemas().validate_declared(malformed)

    def test_k1_n7_omitted_composition_slot_rejects(self) -> None:
        """K1-N7: a composition-backed part cannot omit even a zero family."""
        malformed = copy.deepcopy(self.attachment)
        malformed["itemizations"][0]["row_sets"].pop()
        self.assert_code(malformed, "ATTACHMENT_COMPOSITION_BIJECTION_MISMATCH")

    def test_k1_n8_wrong_member_or_subtotal_rejects(self) -> None:
        """K1-N8: family predicate and authorized subtotal are exact joins."""
        for key, value, code in (
            ("member_fact_type", {"id": "tax.us.2025.non-form-interest.amount", "version": "v1"}, "ATTACHMENT_ROW_MEMBER_MISMATCH"),
            ("subtotal_symbol", "tax.us.2025.interest.non-form-subtotal", "ATTACHMENT_ROW_SUBTOTAL_MISMATCH"),
        ):
            with self.subTest(key=key):
                malformed = copy.deepcopy(self.attachment)
                row_set = malformed["itemizations"][0]["row_sets"][0]
                if key == "member_fact_type":
                    row_set["rows"][key] = value
                else:
                    row_set[key] = value
                self.assert_code(malformed, code)

    def test_k1_n9_duplicate_or_extra_family_rejects(self) -> None:
        """K1-N9: duplicate/extra Part-I families fail structural admission."""
        malformed = copy.deepcopy(self.attachment)
        duplicate = copy.deepcopy(malformed["itemizations"][0]["row_sets"][0])
        duplicate["subtotal_symbol"] = "demo.extra.subtotal"
        malformed["itemizations"][0]["row_sets"].append(duplicate)
        self.assert_code(malformed, "ATTACHMENT_COMPOSITION_BIJECTION_MISMATCH")


def _input(symbol: str, value: object) -> InputFinding:
    return InputFinding(symbol=symbol, value=value, finding_id=f"demo.finding.{symbol}", role="input")


def _run_attachment(*, k1_rows: list[str], k1_subtotal: str, line2b: str) -> RunResult:
    attachment = _load("rule.attachment.schedule-b.v2.json")
    subtotals = {
        "tax.us.2025.interest.b1-subtotal": "0",
        "tax.us.2025.interest.b3-subtotal": "0",
        "tax.us.2025.interest.oid-subtotal": "0",
        "tax.us.2025.interest.non-form-subtotal": "0",
        "tax.us.2025.interest.form1065-k1-box5-subtotal": k1_subtotal,
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
        SourceFact("tax.us.2025.form1065-k1.box5-interest", value, f"demo.k1.row.{index}")
        for index, value in enumerate(k1_rows)
    ]
    return run(
        RunContext(
            run_id="demo.k1.tieout",
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
    def test_k1_n10_family_row_set_mismatch_blocks_attachment(self) -> None:
        """K1-N10: stale family rows fail before whole-part publication."""
        result = _run_attachment(k1_rows=["1599"], k1_subtotal="1600", line2b="1600")
        row = result.dispositions[0]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], ITEMIZATION_TIE_OUT_VIOLATION)
        self.assertIn("demo.k1.row.0", {pin["id"] for pin in row["pins"]})

    def test_k1_n11_whole_part_mismatch_blocks_attachment(self) -> None:
        """K1-N11: tied family rows still cannot diverge from line 2b."""
        result = _run_attachment(k1_rows=["1600"], k1_subtotal="1600", line2b="1601")
        row = result.dispositions[0]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], ITEMIZATION_TIE_OUT_VIOLATION)
        self.assertIn("part-i-interest:tax.us.2025.interest.taxable-total", row["missing"])


if __name__ == "__main__":
    unittest.main()
