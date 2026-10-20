"""Exact source-family version authority tests.

ADR-0014, ADR-0016, ADR-0017: A closure recorded for one family version
must not authorize a different version's claim.

This suite exercises:
1. Exact v2 mapping with only v1 chain gets no closure admission.
2. Dual-version independence: both v1 and v2 chains in workspace select their
   exact matching version without false multiple-scope collisions.
3. Multiple scopes for the SAME selected version raise SourceAuthorityError.
4. Unadopted versions/families do not interfere.
5. Coverage parity: coverage_report reflects exact-version closure and succession.
6. Live coordinator integration: original v1-only setup does not authorize v2
   empty subtotal; explicit v2 setup restores the expected subtotal.
"""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from packages.derivation.live import live_coordinate_run
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.marshal import marshal_closure_authority
from packages.derivation.source_authority import (
    SourceAuthorityError,
    resolve_closure_admissions,
)
from packages.kernel import findings
from packages.kernel.currency import compute_currency
from packages.tax.coverage import CLOSED, OPEN, coverage_report
from packages.tax.loader import (
    TAX_CONTENT_DIR,
    load_closure_mappings,
    load_source_families,
    tax_registry,
)
from packages.derivation.live_workspace import WorkspaceCapability

ROOT = Path(__file__).resolve().parent.parent.parent
SCOPE = {"tax-year": "2025", "subject": "demo.primary"}
SURFACE = {"surface": "synthetic-test"}
USER = "demo-user"


def _act(index: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"act-{index:04d}",
        "kind": kind,
        "actor": "user",
        "at": f"2026-10-18T20:{index % 60:02d}:00Z",
        "committed_against": index,
        "payload": payload,
    }


def _finding(finding_id: str, fact_id: str, value: Any) -> dict[str, Any]:
    return {
        "schema": "finding.v1",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


class ExactFamilyVersionAuthorityTests(unittest.TestCase):
    registry: Any
    schemas: DerivationSchemas
    canon: dict[str, dict[str, Any]]
    families: dict[str, dict[str, Any]]
    mappings: dict[str, dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = tax_registry()
        cls.schemas = DerivationSchemas()
        cls.canon = load_canon(cls.schemas)
        cls.families = load_source_families(cls.registry)
        cls.mappings = load_closure_mappings(cls.registry)

    def _sample_family_pair(self) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
        """Return (fam_v1, fam_v2, map_v1, map_v2) for covered-w-st."""
        fam_v1 = json.loads(
            (TAX_CONTENT_DIR / "family.f1099b-covered-w-st.json").read_text("utf-8")
        )
        fam_v2 = json.loads(
            (TAX_CONTENT_DIR / "family.f1099b-covered-w-st.v2.json").read_text("utf-8")
        )
        map_v1 = json.loads(
            (TAX_CONTENT_DIR / "closure-mapping.f1099b-covered-w-st.json").read_text("utf-8")
        )
        map_v2 = json.loads(
            (TAX_CONTENT_DIR / "closure-mapping.f1099b-covered-w-st.v2.json").read_text("utf-8")
        )
        return fam_v1, fam_v2, map_v1, map_v2

    def _bundle_act(self) -> dict[str, Any]:
        bundle = json.loads(
            (TAX_CONTENT_DIR / "f1099b-covered-w-st.bundle.json").read_text("utf-8")
        )
        return _act(0, "bundle-adoption", {"bundle": bundle})

    def test_v2_mapping_with_only_v1_chain_gets_no_v2_closure_admission(self) -> None:
        """A workspace with only a v1 horizon chain must NOT authorize a v2 mapping."""
        fam_v1, fam_v2, map_v1, map_v2 = self._sample_family_pair()
        fid = fam_v2["id"]

        acts = [
            self._bundle_act(),
            _act(1, "horizon-genesis", {
                "family": {"id": fid, "version": "v1"},
                "scope": {"tax-year": "2025", "subject": "demo.primary"},
                "horizon_id": "demo.wst.v1.h0",
            }),
            _act(2, "assertion", {
                "finding": _finding(
                    "demo.closure.wst.v1",
                    f"{fid}.source-closure|family-horizon=demo.wst.v1.h0,tax-year=2025",
                    True,
                )
            }),
        ]
        state = findings.project(tuple(acts), self.registry)
        currency = compute_currency(state)

        # Marshal with v2 mapping
        records, current_horizons = marshal_closure_authority(state, currency, [map_v2])

        # Under the exact-version guard:
        # current_horizons must NOT map fid to demo.wst.v1.h0
        self.assertNotIn(fid, current_horizons)

        # resolve_closure_admissions must admit nothing for fid
        admissions = resolve_closure_admissions([map_v2], [fam_v2], records, current_horizons)
        self.assertNotIn(fid, admissions)

    def test_dual_version_chains_containment_refusal(self) -> None:
        """Workspace with both v1 and v2 chains in same scope refuses authority (Finding 1 containment)."""
        fam_v1, fam_v2, map_v1, map_v2 = self._sample_family_pair()
        fid = fam_v1["id"]

        acts = [
            self._bundle_act(),
            # v1 chain and closure
            _act(1, "horizon-genesis", {
                "family": {"id": fid, "version": "v1"},
                "scope": {"tax-year": "2025", "subject": "demo.primary"},
                "horizon_id": "demo.wst.v1.h0",
            }),
            _act(2, "assertion", {
                "finding": _finding(
                    "demo.closure.wst.v1",
                    f"{fid}.source-closure|family-horizon=demo.wst.v1.h0,tax-year=2025",
                    True,
                )
            }),
            # v2 chain and closure (same scope, separate horizon: both-current log defect)
            _act(3, "horizon-genesis", {
                "family": {"id": fid, "version": "v2"},
                "scope": {"tax-year": "2025", "subject": "demo.primary"},
                "horizon_id": "demo.wst.v2.h0",
            }),
            _act(4, "assertion", {
                "finding": _finding(
                    "demo.closure.wst.v2",
                    f"{fid}.source-closure|family-horizon=demo.wst.v2.h0,tax-year=2025",
                    True,
                )
            }),
        ]
        state = findings.project(tuple(acts), self.registry)
        currency = compute_currency(state)

        # Containment rule: marshal refuses authority when multiple version chains are current in one scope
        with self.assertRaises(SourceAuthorityError) as ctx_v2:
            marshal_closure_authority(state, currency, [map_v2])
        self.assertIn("has multiple active version chains", str(ctx_v2.exception))

        with self.assertRaises(SourceAuthorityError) as ctx_v1:
            marshal_closure_authority(state, currency, [map_v1])
        self.assertIn("has multiple active version chains", str(ctx_v1.exception))

    def test_multiple_scopes_for_same_version_refuses(self) -> None:
        """Two horizon chains for the SAME family version across multiple scopes raises error."""
        fam_v1, fam_v2, map_v1, map_v2 = self._sample_family_pair()
        fid = fam_v2["id"]

        acts = [
            _act(0, "horizon-genesis", {
                "family": {"id": fid, "version": "v2"},
                "scope": {"tax-year": "2025", "subject": "demo.primary"},
                "horizon_id": "demo.wst.v2.h0.primary",
            }),
            _act(1, "horizon-genesis", {
                "family": {"id": fid, "version": "v2"},
                "scope": {"tax-year": "2025", "subject": "demo.secondary"},
                "horizon_id": "demo.wst.v2.h0.secondary",
            }),
        ]
        state = findings.project(tuple(acts), self.registry)
        currency = compute_currency(state)

        with self.assertRaises(SourceAuthorityError) as ctx:
            marshal_closure_authority(state, currency, [map_v2])
        self.assertIn("multiple scopes", str(ctx.exception))

    def test_coverage_parity_and_succession(self) -> None:
        """Coverage report honors exact version and reflects succession on that version."""
        fam_v1, fam_v2, map_v1, map_v2 = self._sample_family_pair()
        fid = fam_v2["id"]
        families_dict = {fid: fam_v2}
        mappings_dict = {map_v2["id"]: map_v2}

        # Case A: only v1 chain present -> coverage reports OPEN for v2
        acts_v1 = [
            self._bundle_act(),
            _act(1, "horizon-genesis", {
                "family": {"id": fid, "version": "v1"},
                "scope": {"tax-year": "2025", "subject": "demo.primary"},
                "horizon_id": "demo.wst.v1.h0",
            }),
            _act(2, "assertion", {
                "finding": _finding(
                    "demo.closure.wst.v1",
                    f"{fid}.source-closure|family-horizon=demo.wst.v1.h0,tax-year=2025",
                    True,
                )
            }),
        ]
        state_v1 = findings.project(tuple(acts_v1), self.registry)
        currency_v1 = compute_currency(state_v1)
        cov_v1 = coverage_report(state_v1, currency_v1, families_dict, mappings_dict)
        self.assertEqual(len(cov_v1), 1)
        self.assertEqual(cov_v1[0].status, OPEN)

        # Case B: clean v2 base present and closed -> coverage reports CLOSED
        acts_v2 = [
            self._bundle_act(),
            _act(1, "horizon-genesis", {
                "family": {"id": fid, "version": "v2"},
                "scope": {"tax-year": "2025", "subject": "demo.primary"},
                "horizon_id": "demo.wst.v2.h0",
            }),
            _act(2, "assertion", {
                "finding": _finding(
                    "demo.closure.wst.v2",
                    f"{fid}.source-closure|family-horizon=demo.wst.v2.h0,tax-year=2025",
                    True,
                )
            }),
        ]
        state_v2 = findings.project(tuple(acts_v2), self.registry)
        currency_v2 = compute_currency(state_v2)
        cov_v2 = coverage_report(state_v2, currency_v2, families_dict, mappings_dict)
        self.assertEqual(len(cov_v2), 1)
        self.assertEqual(cov_v2[0].status, CLOSED)
        self.assertEqual(cov_v2[0].current_horizon, "demo.wst.v2.h0")

        _TXN_BASE = {
            "covered_security": "yes",
            "basis_reported_to_irs": "yes",
            "box_1f_market_discount": "no",
            "ordinary_indicated": "no",
            "qof_indicated": "no",
            "taxpayer_side_adjustment": "no",
            "collectibles_or_special_rate": "no",
        }
        val = {
            **_TXN_BASE,
            "proceeds": 1000.0,
            "basis": 800.0,
            "long_term": "no",
            "box_1g_wash_sale_adjustment": "yes",
            "box_1g_wash_sale_disallowed_amount": 50.0,
        }

        # Case C: Member transition on v2 chain advances horizon to h1 -> coverage reopens to OPEN
        acts_v3 = list(acts_v2) + [
            _act(3, "entity-introduced", {
                "entity": {"schema": "entity.v1", "id": "demo.broker", "kind": "tax.us.f1099b-broker", "label": "Broker"}
            }),
            _act(4, "entity-introduced", {
                "entity": {"schema": "entity.v1", "id": "demo.b-stmt", "kind": "tax.us.f1099b-statement", "label": "Statement"}
            }),
            _act(5, "entity-introduced", {
                "entity": {"schema": "entity.v1", "id": "demo.txn.1", "kind": "tax.us.f1099b-transaction", "label": "Txn 1"}
            }),
            _act(6, "member-transition", {
                "family": {"id": fid, "version": "v2"},
                "scope": {"tax-year": "2025", "subject": "demo.primary"},
                "member": {
                    "action": "assert",
                    "finding": _finding(
                        "f.txn.1",
                        f"{fid}-txn|broker=demo.broker,statement=demo.b-stmt,transaction=demo.txn.1,tax-year=2025",
                        val,
                    ),
                },
                "successor": {"id": "demo.wst.v2.h1", "predecessor": "demo.wst.v2.h0"},
            }),
        ]
        state_v3 = findings.project(tuple(acts_v3), self.registry)
        currency_v3 = compute_currency(state_v3)
        cov_v3 = coverage_report(state_v3, currency_v3, families_dict, mappings_dict)
        self.assertEqual(len(cov_v3), 1)
        self.assertEqual(cov_v3[0].status, OPEN)
        self.assertEqual(cov_v3[0].current_horizon, "demo.wst.v2.h1")

        # Case D: Re-attesting closure on successor horizon h1 restores CLOSED
        acts_v4 = list(acts_v3) + [
            _act(7, "assertion", {
                "finding": _finding(
                    "demo.closure.wst.v2.h1",
                    f"{fid}.source-closure|family-horizon=demo.wst.v2.h1,tax-year=2025",
                    True,
                )
            }),
        ]
        state_v4 = findings.project(tuple(acts_v4), self.registry)
        currency_v4 = compute_currency(state_v4)
        cov_v4 = coverage_report(state_v4, currency_v4, families_dict, mappings_dict)
        self.assertEqual(len(cov_v4), 1)
        self.assertEqual(cov_v4[0].status, CLOSED)
        self.assertEqual(cov_v4[0].current_horizon, "demo.wst.v2.h1")

    def test_unadopted_version_and_scope_isolation(self) -> None:
        """Chains for unadopted versions or scopes do not bleed into current_horizons."""
        fam_v1, fam_v2, map_v1, map_v2 = self._sample_family_pair()
        fid = fam_v2["id"]
        other_fid = "tax.us.2025.f1099b.covered-w-lt"

        acts = [
            self._bundle_act(),
            # Target family v1 chain retired via handover to v2
            _act(1, "horizon-genesis", {
                "family": {"id": fid, "version": "v1"},
                "scope": {"tax-year": "2025", "subject": "demo.primary"},
                "horizon_id": "demo.wst.v1.h0",
            }),
            _act(2, "family-handover", {
                "predecessor": {
                    "family": {"id": fid, "version": "v1"},
                    "scope": {"tax-year": "2025", "subject": "demo.primary"},
                    "horizon_id": "demo.wst.v1.h0",
                },
                "successor": {
                    "family": {"id": fid, "version": "v2"},
                    "scope": {"tax-year": "2025", "subject": "demo.primary"},
                    "horizon_id": "demo.wst.v2.h0",
                },
            }),
            # Other family chain (unadopted family in another scope)
            _act(3, "horizon-genesis", {
                "family": {"id": other_fid, "version": "v2"},
                "scope": {"tax-year": "2025", "subject": "demo.other"},
                "horizon_id": "demo.wlt.v2.h0",
            }),
        ]
        state = findings.project(tuple(acts), self.registry)
        currency = compute_currency(state)

        records, current_horizons = marshal_closure_authority(state, currency, [map_v2])
        self.assertEqual(current_horizons, {fid: "demo.wst.v2.h0"})

    def test_malformed_and_duplicate_mapping_refusal(self) -> None:
        """Conflicting or duplicate mapping versions for the same family raise SourceAuthorityError."""
        fam_v1, fam_v2, map_v1, map_v2 = self._sample_family_pair()
        state = findings.project(tuple([self._bundle_act()]), self.registry)
        currency = compute_currency(state)

        # Passing both v1 and v2 mappings for the same family must refuse
        with self.assertRaises(SourceAuthorityError) as ctx:
            marshal_closure_authority(state, currency, [map_v1, map_v2])
        self.assertIn("ambiguous mapping versions", str(ctx.exception))

    def test_real_coordinator_v1_only_vs_fresh_v2_empty_authority(self) -> None:
        """Synthetic acts + real coordinator integration: v1-only blocks on absent parent; v2 restores subtotal."""
        from tests.test_f1099k_personal_item_sale_track1 import (
            _finish_acts,
            _make_base_acts,
            SCOPE as LIVE_SCOPE,
            SURFACE as LIVE_SURFACE,
            USER as LIVE_USER,
        )

        w_subtotal_symbol = "tax.us.2025.f1099b.covered-w-st-proceeds-subtotal"
        w_rule_id = "tax.us.2025.rule.f1099b-covered-w-st-proceeds-subtotal"
        parent_val_rule = "tax.us.2025.f1099b.covered-w-st.member-validation.synthesized"

        # 1. Run with honest v1-only base acts (no v2 wash-sale authority recorded)
        v1_only_acts = _make_base_acts(wages=90000.0, include_v2_empty_authority=False)
        finished_v1 = _finish_acts(v1_only_acts)

        with TemporaryDirectory() as tmp1:
            res_v1 = live_coordinate_run(
                WorkspaceCapability(Path(tmp1) / "workspace"),
                repo_root=ROOT,
                authoritative_acts=finished_v1,
                workspace_revision=len(finished_v1),
                run_scope=LIVE_SCOPE,
                scope_user=LIVE_USER,
                request={"schema": "run-request.v1"},
                run_id="demo.exact_ver.v1_only",
                governance_pins=[],
                surface=LIVE_SURFACE,
                output_name="out_v1.json",
            )
            self.assertIsNone(res_v1.refusal)
            assert res_v1.output_path is not None
            report_v1 = json.loads(res_v1.output_path.read_text("utf-8"))

            # In v1-only: W subtotal is NOT published because v2 mapping is unclosed
            pubs_v1 = [p.finding for p in (res_v1.publications or ())]
            w_pubs_v1 = [p for p in pubs_v1 if p.get("symbol") == w_subtotal_symbol]
            self.assertEqual(len(w_pubs_v1), 0, "v1-only setup must not publish v2 W subtotal")

            # 1a. Trace parent synthesized validation rule: blocks because v2 parent family is unclosed
            parent_disps = [d for d in report_v1.get("dispositions", []) if d.get("artifact_id") == parent_val_rule]
            self.assertTrue(parent_disps, f"Expected {parent_val_rule} in report dispositions")
            self.assertEqual(parent_disps[0].get("disposition"), "blocked")
            self.assertEqual(parent_disps[0].get("missing"), ["tax.us.2025.f1099b.covered-w-st"])

            # 1b. Trace downstream W scalar subtotal: blocks with DEPENDENCY_ABSENT on parent validation
            disps_v1 = [d for d in report_v1.get("dispositions", []) if d.get("artifact_id") == w_rule_id]
            self.assertTrue(disps_v1, f"Expected {w_rule_id} in report dispositions")
            self.assertEqual(disps_v1[0].get("disposition"), "blocked")
            self.assertEqual(disps_v1[0].get("code"), "DEPENDENCY_ABSENT")
            self.assertEqual(disps_v1[0].get("missing"), ["tax.us.2025.f1099b.covered-w-st.member-validation"])

        # 2. Run with explicit fresh v2 wash-sale empty authority
        v2_acts = _make_base_acts(wages=90000.0, include_v2_empty_authority=True)
        finished_v2 = _finish_acts(v2_acts)

        with TemporaryDirectory() as tmp2:
            res_v2 = live_coordinate_run(
                WorkspaceCapability(Path(tmp2) / "workspace"),
                repo_root=ROOT,
                authoritative_acts=finished_v2,
                workspace_revision=len(finished_v2),
                run_scope=LIVE_SCOPE,
                scope_user=LIVE_USER,
                request={"schema": "run-request.v1"},
                run_id="demo.exact_ver.v2_clean",
                governance_pins=[],
                surface=LIVE_SURFACE,
                output_name="out_v2.json",
            )
            self.assertIsNone(res_v2.refusal)
            assert res_v2.output_path is not None
            report_v2 = json.loads(res_v2.output_path.read_text("utf-8"))

            # In v2: Check durable report disposition published
            disps_v2 = [d for d in report_v2.get("dispositions", []) if d.get("artifact_id") == w_rule_id]
            self.assertTrue(disps_v2, f"Expected {w_rule_id} in report dispositions")
            self.assertEqual(disps_v2[0].get("disposition"), "published")

            # Check saved ledger pins for exact mapping, declaration, and closure finding
            pins_v2 = disps_v2[0].get("pins", [])
            pin_tuples = {(p.get("role"), p.get("id"), p.get("version")) for p in pins_v2}
            self.assertIn(("package", "tax.us.2025.closure-mapping.f1099b-covered-w-st-proceeds", "v2"), pin_tuples)
            self.assertIn(("package", "tax.us.2025.f1099b.covered-w-st-proceeds", "v2"), pin_tuples)
            self.assertIn(("input", "f.closure.demo.synthetic.wst-p.v2.h0", "v1"), pin_tuples)

            # In-memory numeric / publication assertions (separately labeled):
            pubs_v2 = [p.finding for p in (res_v2.publications or ())]
            w_pubs_v2 = [p for p in pubs_v2 if p.get("symbol") == w_subtotal_symbol]
            self.assertEqual(len(w_pubs_v2), 1, "v2 setup must publish v2 W subtotal")
            val = w_pubs_v2[0].get("value")
            self.assertIsNotNone(val)
            assert val is not None
            self.assertEqual(float(val), 0.0)


if __name__ == "__main__":
    unittest.main()
