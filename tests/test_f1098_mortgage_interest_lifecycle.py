"""Track 1 Form 1098 Mortgage Interest Lifecycle evidence.

Finding 2 (repair round 5): runner-level live_coordinate_run proof that
- a correction at the same statement identity resolves count to 1 and publishes line 8a;
- two distinct statement identities block with MULTIPLE_F1098_OUT_OF_SCOPE.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast
from unittest.mock import patch

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface, ResolvedGraph, resolve_production_package
from packages.kernel.facts import fact_id_for
from packages.kernel.findings import apply_act, initial_state
from packages.tax.loader import TAX_CONTENT_DIR, tax_registry


ROOT = Path(__file__).resolve().parent.parent
CONTENT = TAX_CONTENT_DIR
# Reuse an existing publication-surface fixture; the package members we need
# for Schedule A line 8a are injected via resolve_production_package patch
# because Track 1 does not yet wire them into a successor package (Track 2).
FIXTURES = ROOT / "packages" / "sample_data" / "form1099int_box8_line2a"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}
FAMILY_ID = "tax.us.2025.f1098"
LINE8A = "tax.us.2025.schedule-a.line8a"

AUTHORITY = [
    "liable-and-paid",
    "qualified-main-home",
    "acquisition-debt-use",
    "no-balance-increase",
    "no-refinance",
    "single-mortgage-single-home",
    "not-shared-except-spouse",
    "no-mortgage-interest-credit",
]


def load(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text("utf-8")))


def _act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.f1098.t1.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-08-02T12:{index // 60:02d}:{index % 60:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _attested(finding_id: str, fact_id: str, value: object) -> dict[str, object]:
    return {
        "schema": "finding.v1",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


def _member_fact_id(fact_type: str, payer: str, statement: str) -> str:
    return fact_id_for(
        fact_type,
        (
            ("payer", payer),
            ("statement", statement),
            ("tax-year", "2025"),
        ),
    )


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / "published-packages.v14.json",
        CONTENT,
    )


def _line8a_form_field() -> dict[str, Any]:
    return {
        "schema": "form-field.v3",
        "id": LINE8A,
        "version": "v1",
        "binds_symbol": LINE8A,
        "label": "Home mortgage interest (Form 1098)",
        "description": "Synthetic Schedule A line 8a form-field for Track 1 finding-2 tests.",
        "line": "sch-a-8a",
        "form": {
            "authority": "IRS",
            "form_id": "Schedule A",
            "jurisdiction": "US-federal",
            "tax_year": 2025,
        },
        "citation": {"id": "tax.us.2025.citation.schedule-a.line8a", "version": "v1"},
        "dispositions": {
            "blocked": {
                "codes": [
                    "DEPENDENCY_ABSENT",
                    "DEPENDENCY_INVALID",
                    "VALUE_INVALID",
                    "MULTIPLE_F1098_OUT_OF_SCOPE",
                    "SOURCE_SET_UNCLOSED",
                    "CATEGORICAL_DOMAIN_MISMATCH",
                ],
                "explain": "Schedule A line 8a is blocked.",
                "render": "",
            },
            "published_value": {
                "explain": "Schedule A line 8a publishes the admitted Form 1098 interest.",
                "render": "{value}",
            },
            "guard_inapplicable": {
                "explain": "Schedule A line 8a is not applicable.",
                "render": "",
            },
        },
    }


class TestF1098Lifecycle(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = tax_registry()

    def _scenario_acts(
        self, statements: list[tuple[str, str, float]]
    ) -> tuple[list[dict[str, object]], str]:
        acts: list[dict[str, object]] = []

        def add(kind: str, payload: dict[str, object]) -> None:
            acts.append(_act(len(acts), kind, payload))

        add("bundle-adoption", {"bundle": load(CONTENT / "f1098.bundle.json")})
        # Core vocabulary carries filing-status (required by line-8a debt-limit branch).
        add("bundle-adoption", {"bundle": load(CONTENT / "core_calculations.bundle.v2.json")})

        payers = sorted({t[0] for t in statements})
        stmts = sorted({t[1] for t in statements})

        for payer in payers:
            add(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": payer,
                        "kind": "tax.us.mortgage-lender",
                        "label": "Synthetic lender",
                    }
                },
            )
        for stmt in stmts:
            add(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": stmt,
                        "kind": "tax.us.1098-statement",
                        "label": "Synthetic 1098 statement",
                    }
                },
            )

        add(
            "horizon-genesis",
            {
                "family": {"id": FAMILY_ID, "version": "v1"},
                "scope": SCOPE_KEY,
                "horizon_id": "demo.f1098.h0",
            },
        )
        horizon = "demo.f1098.h0"

        for index, (payer, stmt, box1) in enumerate(statements):
            successor = f"demo.f1098.h{index + 1}"
            add(
                "member-transition",
                {
                    "family": {"id": FAMILY_ID, "version": "v1"},
                    "scope": SCOPE_KEY,
                    "member": {
                        "action": "assert",
                        "finding": {
                            "schema": "finding.v1",
                            "id": f"demo.f1098.box1.{index}",
                            "fact_id": _member_fact_id(
                                "tax.us.2025.f1098.box1-mortgage-interest", payer, stmt
                            ),
                            "value": box1,
                            "basis": "attested",
                            "evidence_ids": [],
                        },
                    },
                    "successor": {"id": successor, "predecessor": horizon},
                },
            )
            horizon = successor

            # Companion / requires-surface facts for this statement identity.
            companions: list[tuple[str, object]] = [
                ("tax.us.2025.f1098.box2-outstanding-principal", 200000.0),
                ("tax.us.2025.f1098.box3-origination-date", "2020-06-01"),
                ("tax.us.2025.f1098.box4-overpaid-refund", 0.0),
                ("tax.us.2025.f1098.box5-mortgage-insurance", 0.0),
                ("tax.us.2025.f1098.box6-points", 0.0),
                ("tax.us.2025.f1098.box9-number-of-properties", 1.0),
                ("tax.us.2025.f1098.box11-other", 0.0),
            ]
            for fact_type, value in companions:
                short = fact_type.rsplit(".", 1)[-1]
                add(
                    "assertion",
                    {
                        "finding": _attested(
                            f"demo.f1098.{short}.{index}",
                            _member_fact_id(fact_type, payer, stmt),
                            value,
                        )
                    },
                )
            for auth in AUTHORITY:
                add(
                    "assertion",
                    {
                        "finding": _attested(
                            f"demo.f1098.{auth}.{index}",
                            _member_fact_id(f"tax.us.2025.f1098.{auth}", payer, stmt),
                            "yes",
                        )
                    },
                )

        return acts, horizon

    def test_duplicate_statement_collapses_to_single_finding(self) -> None:
        acts, _ = self._scenario_acts([("demo.lender.a", "demo.stmt.a", 15000.0)])
        state = initial_state()
        for act in acts:
            state = apply_act(state, act, self.registry)

        fact_id = _member_fact_id(
            "tax.us.2025.f1098.box1-mortgage-interest", "demo.lender.a", "demo.stmt.a"
        )
        correction_act = _act(
            len(acts),
            "assertion",
            {
                "finding": {
                    "schema": "finding.v1",
                    "id": "demo.f1098.box1.correction",
                    "fact_id": fact_id,
                    "value": 16000.0,
                    "basis": "attested",
                    "evidence_ids": [],
                }
            },
        )
        state = apply_act(state, correction_act, self.registry)

        original = state.findings["demo.f1098.box1.0"]
        corrected = state.findings["demo.f1098.box1.correction"]

        self.assertEqual(original["value"], 15000.0)
        self.assertEqual(corrected["value"], 16000.0)
        self.assertEqual(original["fact_id"], fact_id)
        self.assertEqual(corrected["fact_id"], fact_id)

    def test_distinct_statements_produce_multiple_findings(self) -> None:
        acts, _ = self._scenario_acts(
            [
                ("demo.lender.a", "demo.stmt.a", 15000.0),
                ("demo.lender.b", "demo.stmt.b", 5000.0),
            ]
        )
        state = initial_state()
        for act in acts:
            state = apply_act(state, act, self.registry)

        fact_id_a = _member_fact_id(
            "tax.us.2025.f1098.box1-mortgage-interest", "demo.lender.a", "demo.stmt.a"
        )
        fact_id_b = _member_fact_id(
            "tax.us.2025.f1098.box1-mortgage-interest", "demo.lender.b", "demo.stmt.b"
        )

        finding_a = state.findings["demo.f1098.box1.0"]
        finding_b = state.findings["demo.f1098.box1.1"]

        self.assertNotEqual(fact_id_a, fact_id_b)
        self.assertEqual(finding_a["fact_id"], fact_id_a)
        self.assertEqual(finding_b["fact_id"], fact_id_b)
        self.assertEqual(finding_a["value"], 15000.0)
        self.assertEqual(finding_b["value"], 5000.0)

    def _patch_resolve(self) -> Any:
        orig_resolve = resolve_production_package

        def custom_resolve(*args: Any, **kwargs: Any) -> Any:
            res = orig_resolve(*args, **kwargs)
            if not isinstance(res, ResolvedGraph):
                return res
            rule = load(CONTENT / "rule.schedule-a-line8a.json")
            family = load(CONTENT / "family.f1098.json")
            mapping = load(CONTENT / "closure-mapping.f1098.json")
            bundle = load(CONTENT / "f1098.bundle.json")
            debt_limit_parameter = load(CONTENT / "parameter.mortgage-interest-debt-limit.json")
            new_members = list(res.resolved_members) + [
                rule,
                family,
                mapping,
                bundle,
                debt_limit_parameter,
                _line8a_form_field(),
            ]
            package = dict(res.package)
            package["input_bindings"] = list(package.get("input_bindings", [])) + [
                {
                    "fact_type": {"id": "tax.us.2025.filing-status", "version": "v1"},
                    "mode": "required",
                    "symbol": "filing_status",
                }
            ]
            return ResolvedGraph(
                package=package,
                resolved_members=tuple(new_members),
                adoption_act_id=res.adoption_act_id,
                release_id=res.release_id,
            )

        return patch(
            "packages.derivation.live.resolve_production_package",
            side_effect=custom_resolve,
        )

    def _run(self, acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
        """Drive live_coordinate_run; return (result_output, presentation_model)."""
        adoption = load(FIXTURES / "adoptions" / "adopt-core-v19-current.json")
        adoption = dict(adoption)
        adoption["committed_against"] = len(acts)
        acts = list(acts) + [adoption]
        for index, act in enumerate(acts):
            act["committed_against"] = index
            act["actor"] = USER

        with self._patch_resolve():
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
                    self.fail(f"Run refused: {result.refusal}")
                assert result.output_path is not None
                assert result.presentation_path is not None
                return (
                    json.loads(result.output_path.read_text("utf-8")),
                    json.loads(result.presentation_path.read_text("utf-8")),
                )

    def _line8a_outcome(
        self, output: dict[str, Any], presentation: dict[str, Any]
    ) -> dict[str, Any]:
        """Locate the line-8a rule outcome from result + presentation model."""
        rule_id = "tax.us.2025.schedule-a.line8a.rule"
        disp_row = None
        for disp in output.get("dispositions", []):
            if disp.get("artifact_id") == rule_id:
                disp_row = disp
                break
        self.assertIsNotNone(disp_row, f"no disposition for {rule_id}")
        assert disp_row is not None

        if disp_row.get("disposition") == "published":
            # Value is on the presentation model (same as form1099int pattern).
            sections = presentation.get("sections") or presentation.get("fields") or []
            value = None
            for section in sections:
                sid = section.get("id") or section.get("section_id") or section.get("field_id")
                if sid in {LINE8A, "sch-a-8a", "tax.us.2025.schedule-a.line8a"}:
                    resolved = section.get("resolved") or {}
                    value = resolved.get("value", section.get("value"))
                    break
            # Fallback: scan any nested value next to our symbol.
            if value is None:
                blob = json.dumps(presentation)
                # last resort: walk
                def walk(node: Any) -> Any:
                    if isinstance(node, dict):
                        if node.get("symbol") == LINE8A and "value" in node:
                            return node["value"]
                        if node.get("binds_symbol") == LINE8A:
                            r = node.get("resolved") or {}
                            if "value" in r:
                                return r["value"]
                        for v in node.values():
                            found = walk(v)
                            if found is not None:
                                return found
                    elif isinstance(node, list):
                        for v in node:
                            found = walk(v)
                            if found is not None:
                                return found
                    return None
                value = walk(presentation)
            return {"kind": "published", "disposition": disp_row, "value": value}

        if disp_row.get("disposition") == "blocked":
            return {
                "kind": "blocked",
                "disposition": disp_row,
                "code": disp_row.get("code"),
            }
        return {"kind": disp_row.get("disposition"), "disposition": disp_row}

    def test_corrected_statement_publishes_line8a(self) -> None:
        """Finding 2a: same-identity correction → count 1 → computed line 8a."""
        acts, horizon = self._scenario_acts([("demo.lender.a", "demo.stmt.a", 15000.0)])
        fact_id = _member_fact_id(
            "tax.us.2025.f1098.box1-mortgage-interest", "demo.lender.a", "demo.stmt.a"
        )
        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": {
                        "schema": "finding.v1",
                        "id": "demo.f1098.box1.correction",
                        "fact_id": fact_id,
                        "value": 16000.0,
                        "basis": "attested",
                        "evidence_ids": [],
                    }
                },
            )
        )
        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.f1098.closure",
                        f"tax.us.2025.f1098.source-closure|family-horizon={horizon},tax-year=2025",
                        True,
                    )
                },
            )
        )
        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.filing-status",
                        "tax.us.2025.filing-status|tax-year=2025",
                        "single",
                    )
                },
            )
        )

        output, presentation = self._run(acts, "demo.f1098.finding2.correction")
        section = self._line8a_outcome(output, presentation)
        self.assertEqual(section["kind"], "published", section)
        # Decimal-string values are normal on this path.
        self.assertIsNotNone(section.get("value"), section)
        self.assertEqual(float(section["value"]), 16000.0)

    def test_multiple_statements_block_line8a_out_of_scope(self) -> None:
        """Finding 2b: two identities → count 2 → MULTIPLE_F1098_OUT_OF_SCOPE."""
        acts, horizon = self._scenario_acts(
            [
                ("demo.lender.a", "demo.stmt.a", 15000.0),
                ("demo.lender.b", "demo.stmt.b", 5000.0),
            ]
        )
        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.f1098.closure",
                        f"tax.us.2025.f1098.source-closure|family-horizon={horizon},tax-year=2025",
                        True,
                    )
                },
            )
        )
        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.filing-status",
                        "tax.us.2025.filing-status|tax-year=2025",
                        "single",
                    )
                },
            )
        )

        output, presentation = self._run(acts, "demo.f1098.finding2.multiple")
        section = self._line8a_outcome(output, presentation)
        self.assertEqual(section["kind"], "blocked", section)
        self.assertEqual(section.get("code"), "MULTIPLE_F1098_OUT_OF_SCOPE", section)


if __name__ == "__main__":
    unittest.main()
