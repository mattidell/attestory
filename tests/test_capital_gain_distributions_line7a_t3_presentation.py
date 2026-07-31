"""Track 3 synthetic presentation evidence for line 7a / line 7b."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.presentation_projection import PresentationModelError, build_presentation_model, validate_presentation_model
from packages.derivation.runner import Publication
from packages.kernel.findings import FindingState
from tools import generate_capital_gain_distributions_line7a_t3_presentation_goldens as goldens

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"


def _field() -> dict[str, Any]:
    return json.loads((CONTENT / "form1040.line-7b.form-field.v2.json").read_text("utf-8"))


def _citation() -> dict[str, Any]:
    return json.loads((CONTENT / "citation.form1040.line-7b.json").read_text("utf-8"))


def _categorical_model(*, field: dict[str, Any] | None = None, value: Any = "checked", include_citation: bool = True) -> dict[str, Any]:
    field = field or _field()
    raw = {"schema": "finding.v1", "id": "demo.raw", "fact_id": "demo.checked", "value": "no", "basis": "attested", "evidence_ids": []}
    finding = {"schema": "derived-finding.v2", "id": "demo.derived", "symbol": field["binds_symbol"], "value": value, "version": "v2", "pins": [{"role": "input", "id": "demo.raw", "version": "v1"}]}
    rule = {"schema": "rule-artifact.v2", "id": "demo.rule", "publishes": field["binds_symbol"]}
    row = {"artifact_id": "demo.rule", "symbol": field["binds_symbol"], "disposition": "published", "finding_id": "demo.derived", "pins": finding["pins"]}
    members = [field, rule] + ([_citation()] if include_citation else [])
    return build_presentation_model(run_id="demo.t3", resolved_members=members, state=FindingState(findings={"demo.raw": raw}, evidence={}), publications=[Publication(act={}, finding=finding)], dispositions=[row])


class CategoricalProjection(unittest.TestCase):
    def test_checked_is_a_fixed_categorical_disposition_without_a_value_key(self) -> None:
        model = _categorical_model()
        resolved = model["sections"][0]["resolved"]
        self.assertEqual(resolved["disposition"], "published_categorical")
        self.assertNotIn("value", resolved)
        self.assertEqual(model["sections"][0]["field"]["citation"], _field()["citation"])
        validate_presentation_model(model)

    def test_malformed_categorical_value_and_missing_or_wrong_citation_fail_closed(self) -> None:
        with self.assertRaises(PresentationModelError):
            _categorical_model(value=1)
        with self.assertRaises(PresentationModelError):
            _categorical_model(include_citation=False)
        bad_field = _field()
        bad_field["citation"] = {"id": "demo.wrong.citation", "version": "v1"}
        with self.assertRaises(PresentationModelError):
            _categorical_model(field=bad_field)


class ProductionShapedGoldens(unittest.TestCase):
    def test_regeneration_is_deterministic_and_matches_committed_goldens(self) -> None:
        first = goldens.regenerate()
        second = goldens.regenerate()
        self.assertEqual(first, second)
        for name, model in first.items():
            committed = json.loads((goldens.GOLDEN_DIR / f"{name}.presentation-model.v1.json").read_text("utf-8"))
            self.assertEqual(committed, model)
            validate_presentation_model(committed)

    def test_three_dispositions_are_honest(self) -> None:
        models = goldens.regenerate()
        eligible = {section["id"]: section for section in models["eligible"]["sections"]}
        missing = {section["id"]: section for section in models["missing-authority"]["sections"]}
        required = {section["id"]: section for section in models["schedule-d-required"]["sections"]}
        self.assertEqual(eligible["line-7a"]["resolved"]["value"], 1500)
        self.assertEqual(eligible["line-7b"]["resolved"]["disposition"], "published_categorical")
        self.assertEqual(eligible["line-7b"]["field"]["citation"]["id"], "tax.us.2025.citation.form1040.line-7b")
        self.assertEqual(missing["line-7a"]["resolved"]["disposition"], "blocked")
        self.assertEqual(missing["line-7b"]["resolved"]["disposition"], "blocked")
        self.assertEqual(required["line-7a"]["resolved"]["disposition"], "guard_inapplicable")
        self.assertEqual(required["line-7b"]["resolved"]["disposition"], "guard_inapplicable")


if __name__ == "__main__":
    unittest.main()
