"""Track 2: the dependent tie-breaker in saved presentations on core v58.

The goldens are the presentation models ``live_coordinate_run`` writes for two
synthetic returns, through the real coordinator on v58 / release v56:

1. Single parent winning a contested child:
   Single, wages $30,000, one child under 17 with a valid SSN who also lived with
   a grandparent; the filer is the parent, the grandparent is not (row 4 of the
   resolution table). The child counts for the EIC and the child tax credit; lines 19,
   27a and 28 publish.

2. Single grandparent losing child to claiming parent:
   Single, wages $18,000, a grandparent filer against a parent who will claim (row 5).
   The child counts for none of the three credits; the EIC is the credit without a
   qualifying child; lines 19, 27a and 28 publish.

Hand-checked against Schedule 8812 (2025), the Form 1040 Tax Table (2025, ``i1040gi-2025.txt``),
and the 2025 EIC parameters and table. Sources cited by line of the pdftotext text in
``temp/tax-on-taxable-income/sources/``:
- Standard deduction: Single $15,750 (``i1040gi-2025.txt:228``);
- Tax Table:
  - row 14,250-14,300, single column 1,475 (``i1040gi-2025.txt:4948``);
  - row 2,250-2,275, single column 226 (``i1040gi-2025.txt:4751``);
- Schedule 8812 ``f1040s8.txt`` and instructions ``i1040s8.txt``:
  - CTC $2,200 per qualifying child under 17 with valid SSN;
  - ACTC maximum $1,700 per child, 15% of earned income over $2,500;
- EIC parameters (``packages/content/tax/2025/parameter.eic-2025.json``) and table:
  - row 30,000-30,050, Single, 1 child: 3,261 (``i1040gi-2025.txt:3605``);
  - row 18,000-18,050, Single, 0 children: 83 (``i1040gi-2025.txt:3449``; completed limit 19,104).
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
from packages.derivation.production_resolver import PublicationSurface
from tests.test_other_dependents_credit_track1 import (
    LINE19,
    build,
    ctc_child,
)
from tests.test_refund_or_amount_owed_track1 import (
    CONTENT,
    RELEASE_DIR,
    ROOT,
    USER,
    _act,
    _attested,
    _close_empty,
    _close_other_box4_families,
    _finish,
    _load,
)
from tests.test_refund_or_amount_owed_track2 import _add_bottom_line_answers, _add_box2_only
from tests.test_other_dependents_credit_presentation import (
    MFJ_GOLDEN as ODC_V56_MFJ_GOLDEN,
    RUN_MFJ as ODC_V56_RUN_MFJ,
    _acts_mfj as _odc_v56_acts_mfj,
    _present as _odc_v56_present,
)

PRESENTATION = ROOT / "packages" / "sample_data" / "dependent_tie_breaker" / "presentation"
PARENT_WINS_GOLDEN = PRESENTATION / "single-parent-wins-contested-child.presentation-model.v1.json"
GRANDPARENT_LOSES_GOLDEN = PRESENTATION / "single-grandparent-loses-child-to-parent.presentation-model.v1.json"
RUN_PARENT_WINS = "demo.dtb.presentation.single-parent-wins-contested-child"
RUN_GRANDPARENT_LOSES = "demo.dtb.presentation.single-grandparent-loses-child-to-parent"

PACKAGE_V58 = CONTENT / "package.core-calculations.v58.json"
REGISTRY_V56 = CONTENT / "published-packages.v56.json"
RELEASE_V56 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v56.json"
SURFACE_V58 = PublicationSurface(RELEASE_DIR, REGISTRY_V56, CONTENT)

OD = "tax.us.2025.ctc.no-other-dependent"
LINE27A = "tax.us.2025.payments.line27a"
LINE28 = "tax.us.2025.ctc.form1040-line28"
DTB_PREFIX = "tax.us.2025.dtb.child."
DTB_CLEAR_PREFIX = "tax.us.2025.dtb.child.tie-breaker-clear"


def _finish_presentation(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    """Adds the W-2 box 2 family (no withholding), closes the other box 4 families, and
    adds the bottom-line answers, as earlier presentation tests do."""
    acts = _add_box2_only(acts, employer="demo.cgd.t2.employer", slip="demo.cgd.t2.w2", amount=0.0)
    _close_empty(
        acts,
        family="tax.us.2025.w2-box2",
        version="v1",
        closure_fact="tax.us.2025.w2-box2.source-closure",
        horizon="demo.dtb.t2.w2box2",
    )
    _close_other_box4_families(acts, skip={"w2-box2"})
    acts = _add_bottom_line_answers(acts, estimated=0.0, applied_2026=0.0)
    return _finish(
        acts,
        package_path=PACKAGE_V58,
        package_version="v58",
        release_path=RELEASE_V56,
        release_version="v56",
        note="dependent tie breaker presentation golden",
    )


def _acts_single_parent_wins() -> list[dict[str, object]]:
    kids = {"demo-child-1": ctc_child()}
    ret_answers = {
        OD: "yes",
        "tax.us.2025.eic.age-25-under-65": "yes",
        "tax.us.2025.eic.main-home-in-us": "yes",
    }
    acts = build(wages=30000.0, filing_status="single", children=kids, return_answers=ret_answers)
    acts.append(_act(len(acts), "bundle-adoption", {"bundle": _load("dtb-questions.bundle.json")}))
    dtb_answers = {
        "another-could-claim": "yes",
        "multiple-other-claimants": "no",
        "filer-is-parent": "yes",
        "other-is-parent": "no",
    }
    for k, v in dtb_answers.items():
        fid = f"{DTB_PREFIX}{k}|child=demo-child-1,tax-year=2025"
        acts.append(_act(len(acts), "assertion", {"finding": _attested(f"demo.dtb.{k}", fid, v)}))
    return _finish_presentation(acts)


def _acts_single_grandparent_loses() -> list[dict[str, object]]:
    kids = {"demo-child-1": ctc_child()}
    ret_answers = {
        OD: "yes",
        "tax.us.2025.eic.age-25-under-65": "yes",
        "tax.us.2025.eic.main-home-in-us": "yes",
    }
    acts = build(wages=18000.0, filing_status="single", children=kids, return_answers=ret_answers)
    acts.append(_act(len(acts), "bundle-adoption", {"bundle": _load("dtb-questions.bundle.json")}))
    dtb_answers = {
        "another-could-claim": "yes",
        "multiple-other-claimants": "no",
        "filer-is-parent": "no",
        "other-is-parent": "yes",
        "other-will-claim": "yes",
    }
    for k, v in dtb_answers.items():
        fid = f"{DTB_PREFIX}{k}|child=demo-child-1,tax-year=2025"
        acts.append(_act(len(acts), "assertion", {"finding": _attested(f"demo.dtb.{k}", fid, v)}))
    return _finish_presentation(acts)


def _present(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=SURFACE_V58,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            raise AssertionError(f"{run_id} refused: {outcome.refusal.reason} {outcome.refusal.detail}")
        if outcome.presentation_path is None or outcome.publications is None:
            raise AssertionError(f"{run_id} saved no presentation")
        model = cast(dict[str, Any], json.loads(outcome.presentation_path.read_text(encoding="utf-8")))
        pubs = {str(pub.finding["symbol"]): pub.finding for pub in outcome.publications}
        return model, pubs


def _load_golden(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise AssertionError(f"committed presentation golden required at {path}")
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _numeric(model: dict[str, Any], section_id: str) -> Any:
    section = next(s for s in model["sections"] if s["id"] == section_id)
    resolved = section["resolved"]
    if resolved.get("disposition") in {"published_value", "computed_zero", "closure_backed_zero"}:
        return resolved.get("value")
    return resolved


class DependentTieBreakerPresentationTests(unittest.TestCase):
    def test_single_parent_wins_golden_regenerates_and_matches(self) -> None:
        model, _ = _present(_acts_single_parent_wins(), RUN_PARENT_WINS)
        self.assertEqual(project_presentation_v1(model), _load_golden(PARENT_WINS_GOLDEN))

    def test_single_parent_wins_walk_from_line_28_and_pins(self) -> None:
        model, pubs = _present(_acts_single_parent_wins(), RUN_PARENT_WINS)
        self.assertEqual(_numeric(model, "line-19"), 1475)
        self.assertEqual(_numeric(model, "line-27a"), 3261)
        self.assertEqual(_numeric(model, "line-28"), 725)

        derived = index_derived(list(pubs.values()))
        tree = explain(str(pubs[LINE28]["id"]), role="output", derived=derived)

        dtb_clear_nodes: list[Any] = []
        all_dtb_pins: set[str] = set()

        def walk(node: Any) -> None:
            if node.symbol and node.symbol.startswith(DTB_CLEAR_PREFIX):
                dtb_clear_nodes.append(node)
            if node.finding_id and "demo.dtb." in node.finding_id:
                all_dtb_pins.add(node.finding_id)
            for c in node.children:
                walk(c)

        walk(tree)
        self.assertTrue(len(dtb_clear_nodes) > 0, "Walk from line 28 reached dtb clear node")

        expected_dtb_pins = {
            "demo.dtb.another-could-claim",
            "demo.dtb.multiple-other-claimants",
            "demo.dtb.filer-is-parent",
            "demo.dtb.other-is-parent",
        }
        self.assertEqual(all_dtb_pins, expected_dtb_pins)

        dtb_node = dtb_clear_nodes[0]
        dtb_node_pins = {
            c.finding_id for c in dtb_node.children if c.finding_id and "demo.dtb." in c.finding_id
        }
        self.assertEqual(dtb_node_pins, expected_dtb_pins)

        s28 = next(s for s in model["sections"] if s["id"] == "line-28")
        site_dtb_pins = {
            site["pinId"] for site in s28.get("citationSites", []) if "demo.dtb." in site["pinId"]
        }
        self.assertEqual(site_dtb_pins, expected_dtb_pins)

    def test_single_grandparent_loses_golden_regenerates_and_matches(self) -> None:
        model, _ = _present(_acts_single_grandparent_loses(), RUN_GRANDPARENT_LOSES)
        self.assertEqual(project_presentation_v1(model), _load_golden(GRANDPARENT_LOSES_GOLDEN))

    def test_single_grandparent_loses_walk_names_other_will_claim_not_filer_agi_higher(self) -> None:
        model, pubs = _present(_acts_single_grandparent_loses(), RUN_GRANDPARENT_LOSES)
        self.assertEqual(_numeric(model, "line-19"), 0)
        self.assertEqual(_numeric(model, "line-27a"), 83)
        self.assertEqual(_numeric(model, "line-28"), 0)

        derived = index_derived(list(pubs.values()))

        # Walk from lines 19, 27a, 28
        for sym in (LINE19, LINE27A, LINE28):
            tree = explain(str(pubs[sym]["id"]), role="output", derived=derived)
            all_pins: set[str] = set()
            all_symbols: set[str] = set()

            def walk(node: Any) -> None:
                if node.finding_id:
                    all_pins.add(node.finding_id)
                if node.symbol:
                    all_symbols.add(node.symbol)
                for c in node.children:
                    walk(c)

            walk(tree)
            self.assertIn("demo.dtb.other-will-claim", all_pins)
            self.assertNotIn("demo.dtb.filer-agi-higher", all_pins)
            self.assertFalse(any("filer-agi-higher" in s for s in all_symbols))

        # Also verify in presentation model sections citationSites
        for sid in ("line-19", "line-27a", "line-28"):
            section = next(s for s in model["sections"] if s["id"] == sid)
            sites = {site["pinId"] for site in section.get("citationSites", [])}
            self.assertIn("demo.dtb.other-will-claim", sites)
            self.assertNotIn("demo.dtb.filer-agi-higher", sites)

    def test_single_parent_wins_hand_check(self) -> None:
        model, _ = _present(_acts_single_parent_wins(), RUN_PARENT_WINS)
        # Wages $30,000 = line 1a = line 11 (no adjustments). Standard deduction $15,750
        # (i1040gi-2025.txt:228): taxable income $14,250. Tax Table row 14,250-14,300,
        # single column 1,475 (i1040gi-2025.txt:4948).
        self.assertEqual(_numeric(model, "line-16"), 1475)
        self.assertEqual(_numeric(model, "line-8812-wa-5"), 1475)

        # Schedule 8812: line 4 = 1 (demo-child-1 under 17 with a valid SSN); line 5 = 1 x 2,200
        # = 2,200; line 6 = 0; line 7 = 0; line 8 = 2,200; line 9 = 200,000; line 10 = 0;
        # line 11 = 0; line 12 = 2,200; line 13 = Worksheet A = tax 1,475;
        # line 14 = min(2,200, 1,475) = 1,475.
        self.assertEqual(_numeric(model, "line-8812-4"), 1)
        self.assertEqual(_numeric(model, "line-8812-14"), 1475)

        # Form 1040 line 19 = 1,475.
        self.assertEqual(_numeric(model, "line-19"), 1475)

        # Line 24 = line 16 - line 19 = 1,475 - 1,475 = 0 (no other taxes).
        self.assertEqual(_numeric(model, "line-24"), 0)

        # Schedule 8812 Part II-A (ACTC): line 16a = line 12 - line 14 = 2,200 - 1,475 = 725;
        # line 16b = 1 x 1,700 = 1,700; line 17 = min(725, 1,700) = 725;
        # line 18a = 30,000; line 18b = 2,500; line 19 = 27,500; line 20 = 27,500 x 0.15 = 4,125;
        # line 27 = min(line 17, line 20) = min(725, 4,125) = 725.
        self.assertEqual(_numeric(model, "line-8812-17"), 725)
        self.assertEqual(_numeric(model, "line-8812-20"), 4125)

        # Form 1040 line 28 = 725.
        self.assertEqual(_numeric(model, "line-28"), 725)

        # EIC: Single, 1 qualifying child, completed amount 50,434 (parameter.eic-2025.json, other.1.completed);
        # EIC Table row 30,000-30,050, Single 1 child column: 3,261 (i1040gi-2025.txt:3605).
        self.assertEqual(_numeric(model, "line-27a"), 3261)

        # Line 33 = line 27a + line 28 = 3,261 + 725 = 3,986 (withholding box 2 is 0);
        # Line 34 = 3,986 - line 24 (0) = 3,986 (refund); line 37 = 0.
        self.assertEqual(_numeric(model, "line-33"), 3986)
        self.assertEqual(_numeric(model, "line-34"), 3986)
        self.assertEqual(_numeric(model, "line-37"), 0)

    def test_single_grandparent_loses_hand_check(self) -> None:
        model, _ = _present(_acts_single_grandparent_loses(), RUN_GRANDPARENT_LOSES)
        # Wages $18,000 = line 1a = line 11 (no adjustments). Standard deduction $15,750
        # (i1040gi-2025.txt:228): taxable income $2,250. Tax Table row 2,250-2,275,
        # single column 226 (i1040gi-2025.txt:4751).
        self.assertEqual(_numeric(model, "line-16"), 226)
        self.assertEqual(_numeric(model, "line-8812-wa-5"), 226)

        # Schedule 8812: child lost in tie-breaker does not count for CTC or ODC;
        # line 4 = 0; line 6 = 0; line 14 = 0.
        self.assertEqual(_numeric(model, "line-8812-4"), 0)
        self.assertEqual(_numeric(model, "line-8812-14"), 0)

        # Form 1040 line 19 = 0.
        self.assertEqual(_numeric(model, "line-19"), 0)

        # Line 24 = line 16 - line 19 = 226 - 0 = 226.
        self.assertEqual(_numeric(model, "line-24"), 226)

        # Form 1040 line 28 = 0 (no ACTC without qualifying child).
        self.assertEqual(_numeric(model, "line-28"), 0)

        # EIC: Single, 0 qualifying children (statutory childless credit);
        # wages $18,000 is below completed amount 19,104 (parameter.eic-2025.json, other.0.completed);
        # EIC Table row 18,000-18,050, Single 0 children column: 83 (i1040gi-2025.txt:3449).
        self.assertEqual(_numeric(model, "line-27a"), 83)

        # Line 33 = line 27a + line 28 = 83; line 34 = 0; line 37 = line 24 (226) - line 33 (83) = 143 (amount owed).
        self.assertEqual(_numeric(model, "line-33"), 83)
        self.assertEqual(_numeric(model, "line-34"), 0)
        self.assertEqual(_numeric(model, "line-37"), 143)

    def test_v56_other_dependents_credit_presentation_reads_as_before(self) -> None:
        model, _ = _odc_v56_present(_odc_v56_acts_mfj(), ODC_V56_RUN_MFJ)
        self.assertEqual(project_presentation_v1(model), _load_golden(ODC_V56_MFJ_GOLDEN))


if __name__ == "__main__":
    unittest.main()


def test_v58_graph_preserves_every_recorded_pin_and_producer() -> None:
    model, pubs = _present(_acts_single_parent_wins(), RUN_PARENT_WINS)
    assert project_presentation_v1(model) == _load_golden(PARENT_WINS_GOLDEN)
    nodes = model['explanationGraph']['nodes']
    by_id = {str(f['id']): f for f in pubs.values()}
    root = model['sectionRoots']['line-27a']
    key = model['explanationGraph']['roots'][root['root']]['target']
    reached = set()
    pending = [key]
    while pending:
        key = pending.pop()
        if key in reached:
            continue
        reached.add(key)
        node = nodes[key]
        if node['kind'] == 'derived':
            finding = by_id[node['id']]
            assert node['value'] == finding['value']
            assert node['symbol'] == finding['symbol']
            assert node['version'] == finding['version']
            pins = sorted(finding['pins'], key=lambda pin: (pin['role'], pin['id']))
            assert [edge['pin'] for edge in node['edges']] == pins
            producers = [pin for pin in finding['pins'] if pin['role'] in {'computation','applicability','field-mapping','cross-form-bridge'}]
            assert node['produced_by'] == (producers[-1] if producers else None)
        for edge in node['edges']:
            assert nodes[edge['target']]['id'] == edge['pin']['id']
            pending.append(edge['target'])
    assert len(reached) < 8608
    assert sum(len(nodes[key]['edges']) for key in reached) < 8607
