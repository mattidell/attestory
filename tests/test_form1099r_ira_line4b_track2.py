"""Track 2: Form 1099-R IRA line 4b through line 9 and the tax path."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.tax.loader import TAX_CONTENT_DIR
from tests.test_form1099g_box1_schedule1_line7 import (
    _act,
    _attested,
    _disposition,
    _published_numeric,
    _section,
    _ug_acts,
)


ROOT = Path(__file__).resolve().parent.parent
CONTENT = TAX_CONTENT_DIR
FIXTURES = ROOT / "packages" / "sample_data" / "form1099r_ira_line4b"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

IRA_BOX1 = "tax.us.2025.f1099r.ira-box1-taxable-distribution"
IRA_BOX2A = "tax.us.2025.f1099r.ira-box2a-taxable-amount"
IRA_INDICATOR = "tax.us.2025.f1099r.ira-indicator"
IRA_CODE = "tax.us.2025.f1099r.distribution-code"
IRA_BOX2B = "tax.us.2025.f1099r.box2b-not-determined"
IRA_CLOSURE = "tax.us.2025.f1099r.ira-fully-taxable.source-closure"
IRA_FAMILY = "tax.us.2025.f1099r.ira-fully-taxable"
IRA_LINE4B = "tax.us.2025.ira.distributions.line4b"


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


def _ira_acts(
    amounts: list[float] | None = None,
    *,
    close: bool = True,
    qualified_dividends: bool = False,
) -> list[dict[str, object]]:
    """Extend a known production-shaped income corpus with IRA statements."""
    acts = _ug_acts(
        box1_values=[],
        close_box1=True,
        box1a=600 if qualified_dividends else None,
        box1b=150 if qualified_dividends else 0,
        wages=90000,
    )
    acts.pop()  # replace the historical v20 adoption with the Track 2 adoption

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("f1099r-ira.bundle.json")})
    amounts = [1200.0] if amounts is None else amounts
    payer = "demo.ira.payer.alpha"
    add(
        "entity-introduced",
        {"entity": {"schema": "entity.v1", "id": payer, "kind": "tax.us.ira-payer", "label": "Synthetic IRA payer"}},
    )
    horizon = "demo.ira.h0"
    add(
        "horizon-genesis",
        {"family": {"id": IRA_FAMILY, "version": "v1"}, "scope": SCOPE_KEY, "horizon_id": horizon},
    )
    for index, amount in enumerate(amounts):
        statement = f"demo.ira.statement.{index}"
        add(
            "entity-introduced",
            {"entity": {"schema": "entity.v1", "id": statement, "kind": "tax.us.1099r-statement", "label": "Synthetic Form 1099-R"}},
        )
        for fact_type, value, suffix in (
            (IRA_BOX2A, amount, "box2a"),
            (IRA_INDICATOR, "traditional", "indicator"),
            (IRA_CODE, "7", "code"),
            (IRA_BOX2B, False, "box2b"),
        ):
            add(
                "assertion",
                {"finding": _attested(f"demo.ira.finding.{suffix}.{index}", f"{fact_type}|payer={payer},statement={statement},tax-year=2025", value)},
            )
        next_horizon = f"demo.ira.h{index + 1}"
        add(
            "member-transition",
            {
                "family": {"id": IRA_FAMILY, "version": "v1"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(f"demo.ira.finding.box1.{index}", f"{IRA_BOX1}|payer={payer},statement={statement},tax-year=2025", amount),
                },
                "successor": {"id": next_horizon, "predecessor": horizon},
            },
        )
        horizon = next_horizon
    if close:
        add(
            "assertion",
            {"finding": _attested("demo.ira.closure", f"{IRA_CLOSURE}|family-horizon={horizon},tax-year=2025", True)},
        )
    adoption = _load_fixture_adoption()
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


def _load_fixture_adoption() -> dict[str, object]:
    return cast(dict[str, object], json.loads((FIXTURES / "adoptions" / "adopt-core-v22-current.json").read_text("utf-8")))


def _run(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    surface = PublicationSurface(FIXTURES / "publication_surface" / "releases", CONTENT / "published-packages.v17.json", CONTENT)
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
            surface=surface,
            output_name="out.json",
        )
        if result.refusal is not None:
            raise AssertionError(result.refusal)
        assert result.output_path is not None and result.presentation_path is not None
        return json.loads(result.output_path.read_text("utf-8")), json.loads(result.presentation_path.read_text("utf-8"))


class Track2Content(unittest.TestCase):
    def _renumber(self, acts: list[dict[str, object]]) -> list[dict[str, object]]:
        for index, act in enumerate(acts):
            act["committed_against"] = index
        return acts

    def _finding_for(self, acts: list[dict[str, object]], fact_type: str) -> dict[str, Any]:
        for act in acts:
            payload = cast(dict[str, Any], act.get("payload", {}))
            finding = cast(dict[str, Any], payload.get("finding", {}))
            if str(finding.get("fact_id", "")).startswith(fact_type + "|"):
                return finding
        raise AssertionError(f"missing fixture finding for {fact_type}")

    def test_line9_v6_consumes_line4b_once_and_does_not_read_raw_members(self) -> None:
        rule = _load("rule.form1040-line9.v6.json")
        self.assertEqual(rule["version"], "v6")
        self.assertEqual([arg["name"] for arg in rule["value"]["args"]][-1], IRA_LINE4B)
        self.assertNotIn(IRA_BOX1, json.dumps(rule))
        self.assertEqual(rule["value"]["args"].count({"name": IRA_LINE4B, "op": "ref"}), 1)
        self.assertFalse((CONTENT / "form1040.line-4a.form-field.json").exists())

    def test_package_and_registry_are_additive_successors(self) -> None:
        package = _load("package.core-calculations.v22.json")
        registry = _load("published-packages.v17.json")
        self.assertEqual(package["schema"], "artifact-package.v19")
        self.assertEqual(package["version"], "v22")
        self.assertIn("quantity-vocabulary.v11", package["admitted_schemas"])
        self.assertIn({"id": "tax.us.2025.rule.form1040-line9", "version": "v6"}, package["entrypoints"])
        self.assertNotIn({"id": "tax.us.2025.rule.form1040-line9", "version": "v5"}, package["entrypoints"])
        self.assertIn({"id": package["id"], "version": "v22", "checksum": package["package_checksum"]}, registry["packages"])

    def test_positive_path_resolves_4b_9_11_15_16_and_walks_exact_citations(self) -> None:
        report, model = _run(_ira_acts([1200]), "demo.ira.p5")
        for symbol in ("line-4b", "line-9", "line-11", "line-15", "line-16"):
            self.assertEqual(_disposition(model, symbol), "published_value", symbol)
        self.assertEqual(_published_numeric(model, "line-4b"), 1200)
        self.assertEqual(_published_numeric(model, "line-11"), _published_numeric(model, "line-9"))
        self.assertNotIn("line-4a", {section["id"] for section in model["sections"]})
        line4b = next(item for item in report["dispositions"] if item.get("symbol") == IRA_LINE4B)
        line9 = next(item for item in report["dispositions"] if item.get("symbol") == "tax.us.2025.income.total-income")
        self.assertIn("demo.ira.finding.box1.0", json.dumps(line4b))
        self.assertIn("demo.ira.finding.box2b.0", json.dumps(line4b))
        for pin in ("tax.us.2025.citation.f1099r.box1", "tax.us.2025.citation.f1099r.box2a", "tax.us.2025.citation.f1099r.box2b", "tax.us.2025.citation.f1099r.indicator", "tax.us.2025.citation.f1099r.distribution-code", "tax.us.2025.citation.form1040.line-4b"):
            self.assertIn(pin, json.dumps(_load("rule.f1099r-ira-fully-taxable-subtotal.json")))
        self.assertIn("tax.us.2025.citation.form1040.line-9", json.dumps(line9))

    def test_qualified_dividend_compatibility_keeps_regular_tax_published(self) -> None:
        _, model = _run(_ira_acts([1200], qualified_dividends=True), "demo.ira.p6")
        self.assertEqual(_disposition(model, "line-16"), "published_value")
        self.assertGreaterEqual(_published_numeric(model, "line-16"), 0)
        self.assertEqual(_published_numeric(model, "line-4b"), 1200)

    def test_unclosed_family_blocks_downstream_without_redacting_other_lines(self) -> None:
        _, model = _run(_ira_acts([1200], close=False), "demo.ira.n5")
        self.assertEqual(_disposition(model, "line-4b"), "blocked")
        self.assertEqual(_disposition(model, "line-9"), "blocked")
        self.assertEqual(_disposition(model, "line-4b"), "blocked")

    def test_invalid_box2b_is_blocked_by_companion_contract(self) -> None:
        acts = _ira_acts([1200])
        for act in acts:
            finding = cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("finding", {}))
            if finding.get("fact_id", "").startswith(IRA_BOX2B):
                finding["value"] = True
        with self.assertRaisesRegex(Exception, "box2b-not-determined"):
            _run(acts, "demo.ira.n6")

    def test_live_route_rejects_missing_box2a_companion(self) -> None:
        acts = _ira_acts([1200])
        acts = [
            act for act in acts
            if not str(cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("finding", {})).get("fact_id", "")).startswith(IRA_BOX2A + "|")
        ]
        with self.assertRaisesRegex(Exception, "companion presence violated"):
            _run(self._renumber(acts), "demo.ira.repair.missing-box2a")

    def test_live_route_rejects_mismatched_box2a(self) -> None:
        acts = _ira_acts([1200])
        self._finding_for(acts, IRA_BOX2A)["value"] = 1100
        with self.assertRaisesRegex(Exception, "same-statement equality violated"):
            _run(acts, "demo.ira.repair.mismatched-box2a")

    def test_live_route_rejects_missing_ira_indicator_companion(self) -> None:
        acts = _ira_acts([1200])
        acts = [
            act for act in acts
            if not str(cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("finding", {})).get("fact_id", "")).startswith(IRA_INDICATOR + "|")
        ]
        with self.assertRaisesRegex(Exception, "companion presence violated"):
            _run(self._renumber(acts), "demo.ira.repair.missing-indicator")

    def test_live_route_rejects_missing_and_invalid_code7_witness(self) -> None:
        missing = _ira_acts([1200])
        missing = [
            act for act in missing
            if not str(cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("finding", {})).get("fact_id", "")).startswith(IRA_CODE + "|")
        ]
        with self.assertRaisesRegex(Exception, "companion presence violated"):
            _run(self._renumber(missing), "demo.ira.repair.missing-code7")

        invalid = _ira_acts([1200])
        self._finding_for(invalid, IRA_CODE)["value"] = "1"
        with self.assertRaises(Exception):
            _run(invalid, "demo.ira.repair.invalid-code7")

    def test_presentation_model_is_compact_and_redacts_blocked_values(self) -> None:
        _, model = _run(_ira_acts([1200]), "demo.ira.p6-presentation")
        selected = {section["id"]: section for section in model["sections"] if section["id"] in {"line-4b", "line-9", "line-11", "line-15", "line-16"}}
        self.assertEqual(set(selected), {"line-4b", "line-9", "line-11", "line-15", "line-16"})
        self.assertTrue(all(section["resolved"].get("value") is not None for section in selected.values()))
        self.assertNotIn("line-4a", json.dumps(model))


if __name__ == "__main__":
    unittest.main()
