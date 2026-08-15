"""Track 1: Schedule 1 absence succession — admission, worksheet, live evidence."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import validate_package
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.kernel.schema_registry import SchemaRegistry
from packages.tax.loader import TAX_CONTENT_DIR
from packages.tax.schedule1_adjustments_succession import (
    LINE21_STANDIN_ID,
    MIGRATION_ID,
    NO_RRB_ID,
    NON_SCHEDULE1_SCOPE_IDS,
    PAIRS,
    PREDECESSOR_IDS,
    SUCCESSOR_BUNDLE_ID,
    SUCCESSOR_IDS,
)
from tests.support import act
from tests.test_form1099g_box1_schedule1_line7 import _act, _disposition, _published_numeric
from tests.test_ssa1099_benefits_line6_track2 import (
    SCOPE_TOKENS,
    _renumber,
    _ssa_acts,
)
from tests.test_ssa_no_activity_line6b_track1 import (
    LINE6B,
    USER,
    SCOPE,
    WORKSHEET_ONLY_TOKENS,
    line6b_rows,
    worksheet_rows,
)

ROOT = Path(__file__).resolve().parent.parent
CONTENT = TAX_CONTENT_DIR
FIXTURES = ROOT / "packages" / "sample_data" / "ssa1099_benefits_line6"
PACKAGE_FILE = "package.core-calculations.v31.json"
REGISTRY_FILE = "published-packages.v26.json"
RELEASE_FILE = "demo.release.2025.v24.json"
ADOPTION_FILE = "adopt-core-v31-current.json"
WORKSHEET_V2 = "rule.ss-benefits-worksheet.v2.json"
WORKSHEET_V3 = "rule.ss-benefits-worksheet.v3.json"
PRED_TOKENS = tuple(token for _prefix, token in (id.rsplit(".", 1) for id in PREDECESSOR_IDS))


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


def _corpus() -> dict[tuple[str, str], dict[str, Any]]:
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        if path.name.startswith("package.") or path.name.startswith("published-packages"):
            continue
        try:
            citizen = json.loads(path.read_text("utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(citizen, dict) and "id" in citizen and "version" in citizen:
            corpus[(citizen["id"], citizen["version"])] = citizen
    return corpus


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / REGISTRY_FILE,
        CONTENT,
    )


def _migration_act(index: int) -> dict[str, Any]:
    return _act(index, "migration-adoption", {"migration": _load("schedule1-adjustments-scope.succession.json")})


def _successor_bundle_act(index: int) -> dict[str, Any]:
    return _act(index, "bundle-adoption", {"bundle": _load("schedule1-adjustments-scope.bundle.json")})


def build_successor_acts(
    *,
    drop_tokens: tuple[str, ...] = (),
    extra: list[dict[str, object]] | None = None,
    **kwargs: Any,
) -> list[dict[str, object]]:
    """Old-package SSA acts, then successor bundle, migration, v31 adoption."""
    acts = _ssa_acts(**kwargs)
    acts.pop()  # historical package adoption from the SSA helper
    drop_ids = {f"tax.us.2025.ss-benefits-scope.{token}" for token in drop_tokens}
    if drop_ids:
        filtered: list[dict[str, object]] = []
        for item in acts:
            payload = cast(dict[str, Any], item.get("payload", {}))
            finding = cast(dict[str, Any], payload.get("finding", {}))
            fact_id = str(finding.get("fact_id", ""))
            if any(fact_id.startswith(f"{type_id}|") for type_id in drop_ids):
                continue
            filtered.append(item)
        acts = filtered
    acts.append(_successor_bundle_act(len(acts)))
    acts.append(_migration_act(len(acts)))
    for item in extra or []:
        acts.append(item)
    adoption = json.loads((FIXTURES / "adoptions" / ADOPTION_FILE).read_text("utf-8"))
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return _renumber(acts)


def execute(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, Any], dict[str, Any] | None, str | None]:
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
        if result.refusal is not None:
            return {}, None, str(result.refusal)
        assert result.output_path is not None and result.presentation_path is not None
        return (
            json.loads(result.output_path.read_text("utf-8")),
            json.loads(result.presentation_path.read_text("utf-8")),
            None,
        )


class TestPublishedCitizens(unittest.TestCase):
    def test_successor_bundle_has_exactly_the_thirteen_and_no_predecessors(self) -> None:
        bundle = _load("schedule1-adjustments-scope.bundle.json")
        self.assertEqual(bundle["id"], SUCCESSOR_BUNDLE_ID)
        self.assertEqual(bundle["schema"], "bundle.v2")
        ids = [ft["id"] for ft in bundle["fact_types"]]
        self.assertEqual(tuple(ids), SUCCESSOR_IDS)
        for predecessor in PREDECESSOR_IDS:
            self.assertNotIn(predecessor, ids)
        self.assertNotIn(NO_RRB_ID, ids)
        for other in NON_SCHEDULE1_SCOPE_IDS:
            self.assertNotIn(other, ids)
        for fact_type in bundle["fact_types"]:
            self.assertEqual(fact_type["schema"], "fact-type.v2")
            self.assertEqual(fact_type["value_schema"]["enum"], ["yes", "no"])
            self.assertEqual(fact_type["identity_keys"], [{"kind": "literal", "name": "tax-year", "values": ["2025"]}])
            self.assertNotIn("Social Security Benefits Worksheet", fact_type["title"])

    def test_migration_names_exactly_the_thirteen_pairs(self) -> None:
        migration = _load("schedule1-adjustments-scope.succession.json")
        self.assertEqual(migration["id"], MIGRATION_ID)
        self.assertEqual(migration["finding_mapping"], {"policy": "presented-claim"})
        pairs = [(p["predecessor"], p["successor"]) for p in migration["pairs"]]
        self.assertEqual(tuple(pairs), PAIRS)
        named = {p["predecessor"] for p in migration["pairs"]}
        self.assertNotIn(NO_RRB_ID, named)
        self.assertTrue(set(NON_SCHEDULE1_SCOPE_IDS).isdisjoint(named))

    def test_empty_route_contract_is_byte_identical_except_the_retarget(self) -> None:
        v2 = _load(WORKSHEET_V2)
        v3 = _load(WORKSHEET_V3)
        self.assertEqual(v3["version"], "v3")
        self.assertEqual(v2["requires"], v3["requires"])
        self.assertIn(NO_RRB_ID, v3["requires"])
        self.assertEqual(len(v3["requires"]), 11)
        self.assertEqual(v2["when"]["args"][0], v3["when"]["args"][0])
        self.assertEqual(v2["when"]["args"][2], v3["when"]["args"][2])
        self.assertEqual(v2["value"]["when"], v3["value"]["when"])
        self.assertEqual(v2["value"]["then"], v3["value"]["then"])
        cds_v2 = v2["when"]["args"][1]
        cds_v3 = v3["when"]["args"][1]
        self.assertEqual(cds_v2["op"], "conditional_dependency_set")
        self.assertEqual(cds_v3["op"], "conditional_dependency_set")
        self.assertEqual(cds_v2["condition"], cds_v3["condition"])
        names_v3 = [member["name"] for member in cds_v3["members"]]
        for successor in SUCCESSOR_IDS:
            self.assertIn(successor, names_v3)
        for predecessor in PREDECESSOR_IDS:
            self.assertNotIn(predecessor, names_v3)
        for other in NON_SCHEDULE1_SCOPE_IDS:
            if other == NO_RRB_ID:
                self.assertNotIn(other, names_v3)
            else:
                self.assertIn(other, names_v3)


class TestPackageAdmission(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.corpus = _corpus()
        self.package = _load(PACKAGE_FILE)

    def test_published_v31_package_validates(self) -> None:
        result = validate_package(self.package, self.corpus, self.schemas)
        self.assertTrue(result.ok, result.issues)

    def test_rejects_migration_that_names_no_rrb(self) -> None:
        mutant = copy.deepcopy(self.package)
        migration = copy.deepcopy(self.corpus[(MIGRATION_ID, "v1")])
        migration["pairs"][0]["predecessor"] = NO_RRB_ID
        self.corpus[(MIGRATION_ID, "v1")] = migration
        result = validate_package(mutant, self.corpus, self.schemas)
        codes = {issue.code for issue in result.issues}
        self.assertNotIn("PACKAGE_SCHEMA_INVALID", codes, result.issues)
        self.assertIn("MIGRATION_PREDECESSOR_SET_INVALID", codes, result.issues)
        self.assertIn("MIGRATION_FORBIDDEN_PREDECESSOR", codes, result.issues)

    def test_rejects_package_that_claims_succession_without_the_migration(self) -> None:
        mutant = copy.deepcopy(self.package)
        mutant["members"] = [m for m in mutant["members"] if m["id"] != MIGRATION_ID]
        mutant["entrypoints"] = [e for e in mutant["entrypoints"] if e["id"] != MIGRATION_ID]
        result = validate_package(mutant, self.corpus, self.schemas)
        self.assertIn("SUCCESSION_PACKAGE_INCOMPLETE", {issue.code for issue in result.issues})

    def test_rejects_worksheet_still_bound_to_predecessor_ids(self) -> None:
        mutant_package = copy.deepcopy(self.package)
        for member in mutant_package["members"]:
            if member["id"] == "tax.us.2025.rule.ss-benefits-worksheet":
                member["version"] = "v2"
                member["schema"] = "rule-artifact.v4"
        for entry in mutant_package["entrypoints"]:
            if entry["id"] == "tax.us.2025.rule.ss-benefits-worksheet":
                entry["version"] = "v2"
        result = validate_package(mutant_package, self.corpus, self.schemas)
        codes = {issue.code for issue in result.issues}
        self.assertNotIn("PACKAGE_SCHEMA_INVALID", codes, result.issues)
        self.assertIn("SUCCESSION_PACKAGE_INCOMPLETE", codes, result.issues)
        self.assertTrue(
            {
                "CONDITIONAL_DEPENDENCY_MEMBER_FACT_TYPE_ABSENT",
                "CATEGORY_LITERAL_PIN_STALE",
            } & codes,
            result.issues,
        )


class TestLiveEvidence(unittest.TestCase):
    def test_fresh_successor_package_empty_route_still_publishes_zero(self) -> None:
        acts = build_successor_acts(drop_tokens=WORKSHEET_ONLY_TOKENS, benefits=[], close=True)
        report, model, refusal = execute(acts, "succession.fresh-empty")
        self.assertIsNone(refusal, refusal)
        assert model is not None
        rows = line6b_rows(report)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].get("disposition"), "published")
        self.assertEqual(_published_numeric(model, "line-6b"), 0)
        self.assertEqual(_disposition(model, "line-6b"), "computed_zero")

    def test_no_schedule1_return_is_not_asked_the_successors(self) -> None:
        v3 = _load(WORKSHEET_V3)
        self.assertTrue(set(SUCCESSOR_IDS).isdisjoint(set(v3["requires"])))
        acts = build_successor_acts(drop_tokens=WORKSHEET_ONLY_TOKENS, benefits=[], close=True)
        report, _model, refusal = execute(acts, "succession.no-extra-ask")
        self.assertIsNone(refusal, refusal)
        rows = worksheet_rows(report)
        self.assertEqual(rows[0].get("disposition"), "published")
        pin_ids = {pin["id"] for pin in rows[0].get("pins", [])}
        for successor in SUCCESSOR_IDS:
            self.assertNotIn(successor, pin_ids)

    def test_upgrade_displaces_predecessor_yes_and_leaves_no_rrb(self) -> None:
        acts = build_successor_acts(benefits=[], close=True)
        state = project(tuple(cast(dict[str, Any], a) for a in acts), SchemaRegistry())
        lattice = facts_of(state.fact_state)
        for predecessor in PREDECESSOR_IDS:
            self.assertNotIn(predecessor, state.fact_state.fact_types)
            self.assertFalse(any(fact.fact_type_id == predecessor for fact in lattice.values()))
        self.assertIn(NO_RRB_ID, state.fact_state.fact_types)
        for other in NON_SCHEDULE1_SCOPE_IDS:
            self.assertIn(other, state.fact_state.fact_types)
        view = compute_currency(state)
        for finding in state.findings.values():
            type_id = finding["fact_id"].split("|", 1)[0]
            if type_id in PREDECESSOR_IDS:
                self.assertIn(finding["id"], view.displaced_finding_ids)
        presented_preds = {c["predecessor_fact_id"].split("|", 1)[0] for c in state.presented_successor_claims}
        self.assertTrue(presented_preds <= set(PREDECESSOR_IDS))
        self.assertNotIn(NO_RRB_ID, presented_preds)

    def test_package_omission_without_migration_act_leaves_findings_current(self) -> None:
        """Negatives: F(P) / package-dictionary omission is not retirement."""
        acts = _ssa_acts(benefits=[], close=True)
        acts.pop()
        state = project(tuple(cast(dict[str, Any], a) for a in acts), SchemaRegistry())
        view = compute_currency(state)
        predecessor_findings = [
            finding["id"]
            for finding in state.findings.values()
            if finding["fact_id"].split("|", 1)[0] in PREDECESSOR_IDS
        ]
        self.assertTrue(predecessor_findings)
        for finding_id in predecessor_findings:
            self.assertIn(finding_id, view.current_finding_ids)

    def test_line21_standin_does_not_revive_predecessors_or_touch_no_rrb(self) -> None:
        standin_type = {
            "schema": "fact-type.v2",
            "id": LINE21_STANDIN_ID,
            "version": "v1",
            "title": "Synthetic Schedule 1 line 21 stand-in; not Form 1098-E.",
            "nature": "determinable",
            "identity_keys": [{"kind": "literal", "name": "tax-year", "values": ["2025"]}],
            "value_schema": {"type": "string", "enum": ["yes", "no"]},
            "supersession": {"policy": "free"},
        }
        standin_bundle = {
            "schema": "bundle.v2",
            "id": "demo.schedule1-adjustments-scope.line21-standin.vocabulary",
            "version": "v1",
            "label": "Synthetic line-21 stand-in vocabulary",
            "fact_types": [standin_type],
        }
        extra = [
            _act(0, "bundle-adoption", {"bundle": standin_bundle}),
            _act(
                0,
                "assertion",
                {
                    "finding": {
                        "schema": "finding.v1",
                        "id": "demo.standin.line21.yes",
                        "fact_id": f"{LINE21_STANDIN_ID}|tax-year=2025",
                        "value": "yes",
                        "basis": "attested",
                        "evidence_ids": [],
                    }
                },
            ),
        ]
        acts = build_successor_acts(
            drop_tokens=WORKSHEET_ONLY_TOKENS,
            benefits=[],
            close=True,
            extra=extra,
        )
        state = project(tuple(cast(dict[str, Any], a) for a in acts), SchemaRegistry())
        for predecessor in PREDECESSOR_IDS:
            self.assertNotIn(predecessor, state.fact_state.fact_types)
        self.assertIn(NO_RRB_ID, state.fact_state.fact_types)
        self.assertIn(LINE21_STANDIN_ID, state.fact_state.fact_types)
        for successor in SUCCESSOR_IDS:
            self.assertIn(successor, state.fact_state.fact_types)
        report, model, refusal = execute(acts, "succession.line21-standin")
        self.assertIsNone(refusal, refusal)
        assert model is not None
        rows = line6b_rows(report)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].get("disposition"), "published")
        self.assertEqual(_published_numeric(model, "line-6b"), 0)
        self.assertEqual(_disposition(model, "line-6b"), "computed_zero")
