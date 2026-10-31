"""Track 2: federal tax withheld on Forms 1099 in saved presentations on core v59.

The goldens are the presentation models ``live_coordinate_run`` writes for two synthetic
returns, through the real coordinator on core v59 / registry v57 / release v57, built from
the Track 1 return builders (``tests/test_form_1099_withholding.py``):

1. Unemployment: wages $50,000 with $4,500 withheld, a Form 1099-G with $6,000 in box 1 and
   $600 withheld in box 4.
2. Social Security: wages $40,000 with $2,500 withheld, a Form SSA-1099 with $12,000 in
   box 3 and $800 withheld in box 6, and a Form 1099-R with $10,000 distributed and $1,200
   withheld in box 4.

Line 25b is the sum of the five withholding subtotals, and its form-field text is the
successor ``form1040.line-25b.form-field`` v2, which names Forms 1099-INT, 1099-DIV and
1099-R box 4, Form 1099-G box 4 and Form SSA-1099 box 6, and not Form 1099-K.
"""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast
import unittest

from packages.derivation.presentation_projection import project_presentation_v1
from packages.derivation.explanation import explain_legacy as explain, index_derived
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from tests.test_form_1099_withholding import (
    CONTENT,
    LINE25B,
    ROOT,
    SURFACE_V59,
    USER,
    YEAR,
    G_SUBTOTAL,
    IRA_SUBTOTAL,
    SSA_SUBTOTAL,
    _finished,
    _recorded_handover,
    _social_security_return,
    _unemployment_return,
)

PRESENTATION = ROOT / "packages" / "sample_data" / "form_1099_withholding" / "presentation"
UNEMPLOYMENT_GOLDEN = PRESENTATION / "unemployment-600-withheld.presentation-model.v1.json"
SOCIAL_SECURITY_GOLDEN = PRESENTATION / "social-security-800-and-retirement-1200-withheld.presentation-model.v1.json"
RUN_UNEMPLOYMENT = "demo.fw.presentation.unemployment-600-withheld"
RUN_SOCIAL_SECURITY = "demo.fw.presentation.social-security-800-and-retirement-1200-withheld"


def _present(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    finished = _recorded_handover(_finished(acts, run_id, core="v59"), reconfirm=True)
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=SURFACE_V59,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            raise AssertionError(f"{run_id} refused: {outcome.refusal.reason} {outcome.refusal.detail}")
        if outcome.presentation_path is None or outcome.publications is None:
            raise AssertionError(f"{run_id} saved no presentation")
        model = cast(dict[str, Any], json.loads(outcome.presentation_path.read_text(encoding="utf-8")))
        pubs = {str(pub.finding["symbol"]): pub.finding for pub in outcome.publications}
        return model, pubs


def _unemployment() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    return _present(_unemployment_return(withheld=600.0), RUN_UNEMPLOYMENT)


def _social_security() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    return _present(_social_security_return(withheld=800.0, retirement=(10000.0, 1200.0)), RUN_SOCIAL_SECURITY)


def _load_golden(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise AssertionError(f"committed presentation golden required at {path}")
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _section(model: dict[str, Any], section_id: str) -> dict[str, Any]:
    return cast(dict[str, Any], next(s for s in model["sections"] if s["id"] == section_id))


def _numeric(model: dict[str, Any], section_id: str) -> Any:
    resolved = _section(model, section_id)["resolved"]
    if resolved.get("disposition") in {"published_value", "computed_zero", "closure_backed_zero"}:
        return resolved.get("value")
    return resolved


def _walk(pubs: dict[str, dict[str, Any]], symbol: str) -> tuple[set[str], set[str]]:
    tree = explain(str(pubs[symbol]["id"]), role="output", derived=index_derived(list(pubs.values())))
    finding_ids: set[str] = set()
    symbols: set[str] = set()

    def walk(node: Any) -> None:
        if node.finding_id:
            finding_ids.add(node.finding_id)
        if node.symbol:
            symbols.add(node.symbol)
        for child in node.children:
            walk(child)

    walk(tree)
    return finding_ids, symbols


class WithholdingPresentationTests(unittest.TestCase):
    def test_unemployment_golden_regenerates_and_matches(self) -> None:
        model, _ = _unemployment()
        self.assertEqual(project_presentation_v1(model), _load_golden(UNEMPLOYMENT_GOLDEN))

    def test_social_security_golden_regenerates_and_matches(self) -> None:
        model, _ = _social_security()
        self.assertEqual(project_presentation_v1(model), _load_golden(SOCIAL_SECURITY_GOLDEN))

    def test_unemployment_lines(self) -> None:
        model, _ = _unemployment()
        # Wages 50,000 less the 15,750 standard deduction: tax 4,595 (line 24); 4,500 withheld
        # on the W-2 (25a) and 600 on the 1099-G (25b) make 5,100 (25d, 33): a refund of 505.
        self.assertEqual(_numeric(model, "line-25b"), 600)
        self.assertEqual(_numeric(model, "line-25d"), 5100)
        self.assertEqual(_numeric(model, "line-33"), 5100)
        self.assertEqual(_numeric(model, "line-34"), 505)
        self.assertEqual(_numeric(model, "line-37"), 0)

    def test_social_security_lines(self) -> None:
        model, _ = _social_security()
        # 800 (SSA-1099 box 6) and 1,200 (1099-R box 4) make 2,000 on line 25b; with 2,500 on
        # the W-2 that is 4,500 against total tax of 5,099: 599 owed.
        self.assertEqual(_numeric(model, "line-25b"), 2000)
        self.assertEqual(_numeric(model, "line-25d"), 4500)
        self.assertEqual(_numeric(model, "line-33"), 4500)
        self.assertEqual(_numeric(model, "line-34"), 0)
        self.assertEqual(_numeric(model, "line-37"), 599)

    def test_line_25b_explanation_reaches_each_withholding_finding(self) -> None:
        _, pubs = _unemployment()
        finding_ids, symbols = _walk(pubs, LINE25B)
        self.assertIn(G_SUBTOTAL, symbols)
        self.assertIn("demo.fw.g.box4.0", finding_ids)

        _, pubs = _social_security()
        finding_ids, symbols = _walk(pubs, LINE25B)
        self.assertTrue({SSA_SUBTOTAL, IRA_SUBTOTAL} <= symbols)
        self.assertTrue({"demo.fw.ssa.box6.0", "demo.fw.r.box4"} <= finding_ids)

    def test_line_25b_citation_sites_name_each_withholding_pin(self) -> None:
        model, _ = _unemployment()
        self.assertIn("demo.fw.g.box4.0", {s["pinId"] for s in _section(model, "line-25b").get("citationSites", [])})
        model, _ = _social_security()
        sites = {s["pinId"] for s in _section(model, "line-25b").get("citationSites", [])}
        self.assertTrue({"demo.fw.ssa.box6.0", "demo.fw.r.box4"} <= sites)

    def test_line_25b_form_field_text_is_the_successor(self) -> None:
        v2 = json.loads((CONTENT / "form1040.line-25b.form-field.v2.json").read_text(encoding="utf-8"))
        v1 = json.loads((CONTENT / "form1040.line-25b.form-field.json").read_text(encoding="utf-8"))
        self.assertEqual((v1["version"], v2["version"]), ("v1", "v2"))
        package = json.loads((CONTENT / "package.core-calculations.v59.json").read_text(encoding="utf-8"))
        members = [m for m in package["members"] if m["id"] == v2["id"] and m["role"] == "form-field"]
        self.assertEqual([m["version"] for m in members], ["v2"])
        text = json.dumps(v2)
        for named in ("1099-INT", "1099-DIV", "1099-R box 4", "1099-G box 4", "SSA-1099 box 6", "five"):
            self.assertIn(named, text)
        self.assertNotIn("1099-K", text)
        self.assertIn("1099-K", json.dumps(v1))
        # Both saved presentations carry the successor, not v1.
        for model in (_unemployment()[0], _social_security()[0]):
            self.assertEqual(_section(model, "line-25b")["field"], v2)


if __name__ == "__main__":
    unittest.main()
