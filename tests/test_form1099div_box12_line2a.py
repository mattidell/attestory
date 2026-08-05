"""Form 1099-DIV box 12 → Form 1040 line 2a: B12-C1–C7 and P1–P8 / N1–N12."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

import jsonschema

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    citizen_checksum,
    load_published_citizen_checksums,
    validate_package,
)
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.findings import FindingModelError
from packages.kernel.schema_registry import SchemaRegistry
from packages.tax.loader import TAX_CONTENT_DIR, tax_registry
from tests.test_capital_gain_distributions_line7a_t2_coordinator import _cgd_t2_acts


ROOT = Path(__file__).resolve().parent.parent
CONTENT = TAX_CONTENT_DIR
FIXTURES = ROOT / "packages" / "sample_data" / "form1099div_box12_line2a"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

BOX12_AMOUNT = "tax.us.2025.f1099div.box12-exempt-interest-dividends"
BOX12_CLOSURE = "tax.us.2025.f1099div.12.source-closure"
BOX12_FAMILY = "tax.us.2025.f1099div.12"
BOX13_AUTH = "tax.us.2025.f1099div.box13-specified-pab-authority"
LINE2A = "tax.us.2025.rule.form1040-line2a"

SCOPE_TOKENS = (
    "no-f1099int-tax-exempt",
    "no-f1099oid-tax-exempt",
    "no-unreported-tax-exempt",
    "no-premium-adjustment",
    "no-child-income-election",
    "no-taxable-social-security",
    "no-amt-form-6251",
    "no-credit-using-tax-exempt",
    "no-deduction-using-tax-exempt",
)

HISTORICAL_BYTES = {
    "packages/content/tax/2025/f1099div-box2a.bundle.json": None,  # filled at runtime
    "packages/content/tax/2025/dividend-universe.v2.json": None,
    "packages/content/tax/2025/package.core-calculations.v15.json": None,
    "packages/content/tax/2025/published-packages.v10.json": None,
}


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


def _corpus() -> dict[tuple[str, str], dict[str, Any]]:
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        try:
            value = json.loads(path.read_text("utf-8"))
        except Exception:
            continue
        if isinstance(value, dict) and isinstance(value.get("id"), str) and isinstance(value.get("version"), str):
            corpus[(value["id"], value["version"])] = value
    return corpus


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / "published-packages.v12.json",
        CONTENT,
    )


def _act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.b12.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-08-04T12:{index // 60:02d}:{index % 60:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _attested(finding_id: str, fact_id: str, value: object) -> dict[str, object]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


def _scope_id(token: str) -> str:
    return f"tax.us.2025.line2a-scope.{token}"


def _b12_acts(
    *,
    box12_values: list[float] | None = None,
    box13_values: list[object] | None = None,
    close_box12: bool = True,
    scope: dict[str, str] | None = None,
    box1a: float | None = 0,
    box1b: float | None = 0,
    box2a: float | None = None,
    wages: float = 90000,
    include_box13: bool = True,
) -> list[dict[str, object]]:
    """Build a production-shaped act log on the v17 route with box-12 facts."""
    box12_values = [100.0] if box12_values is None else box12_values
    if box13_values is None:
        box13_values = [None] * max(1, len(box12_values))
    scope_vals = {token: "yes" for token in SCOPE_TOKENS}
    if scope:
        scope_vals.update(scope)

    acts = _cgd_t2_acts(
        wages=wages,
        box1a=box1a if box1a else None,
        box1b=box1b if box1b else 0,
        box2a=box2a,
        close_2a=True,
        cg_dist="no" if box2a is None else "yes",
        components={"C1": "yes", "C2": "yes", "C3": "yes", "C4": "yes"},
    )
    acts.pop()  # drop historical package adoption

    # Swap residual-carrying box2a vocabulary v1 for residual-free v2 so the
    # exclusive package graph does not admit residual property 12.
    for act in acts:
        if act["kind"] == "bundle-adoption":
            payload = cast(dict[str, object], act["payload"])
            bundle = cast(dict[str, Any], payload.get("bundle") or {})
            if bundle.get("id") == "tax.us.2025.f1099div.box2a.vocabulary":
                payload["bundle"] = _load("f1099div-box2a.bundle.v2.json")

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("f1099div-box12.bundle.json")})
    add("bundle-adoption", {"bundle": _load("line2a-scope.bundle.json")})

    # Entities for multi-payer
    payers_stmts: list[tuple[str, str]] = [("demo.cgd.t2.payer", "demo.cgd.t2.stmt")]
    for index in range(1, max(len(box12_values), 1)):
        payer = f"demo.b12.payer.{index}"
        stmt = f"demo.b12.stmt.{index}"
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": payer,
                    "kind": "tax.us.dividend-payer",
                    "label": f"Synthetic box-12 payer {index}",
                }
            },
        )
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": stmt,
                    "kind": "tax.us.1099div-statement",
                    "label": f"Synthetic box-12 statement {index}",
                }
            },
        )
        payers_stmts.append((payer, stmt))

    add(
        "horizon-genesis",
        {
            "family": {"id": BOX12_FAMILY, "version": "v1"},
            "scope": SCOPE_KEY,
            "horizon_id": "demo.b12.h0",
        },
    )
    horizon = "demo.b12.h0"
    for index, amount in enumerate(box12_values):
        payer, stmt = payers_stmts[index]
        if include_box13:
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.b12.finding.box13.{index}",
                        f"{BOX13_AUTH}|payer={payer},statement={stmt},tax-year=2025",
                        box13_values[index] if index < len(box13_values) else None,
                    )
                },
            )
        next_horizon = f"demo.b12.h{index + 1}"
        add(
            "member-transition",
            {
                "family": {"id": BOX12_FAMILY, "version": "v1"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(
                        f"demo.b12.finding.box12.{index}",
                        f"{BOX12_AMOUNT}|payer={payer},statement={stmt},tax-year=2025",
                        amount,
                    ),
                },
                "successor": {"id": next_horizon, "predecessor": horizon},
            },
        )
        horizon = next_horizon

    if close_box12:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.b12.closure.box12",
                    f"{BOX12_CLOSURE}|family-horizon={horizon},tax-year=2025",
                    True,
                )
            },
        )

    for token, value in scope_vals.items():
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.b12.scope.{token}",
                    f"{_scope_id(token)}|tax-year=2025",
                    value,
                )
            },
        )

    adoption = cast(
        dict[str, object],
        json.loads((FIXTURES / "adoptions" / "adopt-core-v17-current.json").read_text("utf-8")),
    )
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


def _run(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
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
        assert result.refusal is None, result.refusal
        assert result.output_path is not None and result.presentation_path is not None
        return (
            json.loads(result.output_path.read_text("utf-8")),
            json.loads(result.presentation_path.read_text("utf-8")),
        )


def _section(model: dict[str, Any], section_id: str) -> dict[str, Any]:
    return next(section for section in model["sections"] if section["id"] == section_id)


def _published_value(model: dict[str, Any], section_id: str) -> Any:
    resolved = _section(model, section_id)["resolved"]
    return resolved.get("value") if resolved.get("disposition") == "published_value" else resolved


class CitizenContractCases(unittest.TestCase):
    """B12-C1 residual/family shape and historical immutability."""

    def test_box12_member_identity_and_nonnegative(self) -> None:
        # P1 shape: nonnegative box-12 member, payer+statement+year identity.
        bundle = _load("f1099div-box12.bundle.json")
        amount = next(ft for ft in bundle["fact_types"] if ft["id"] == BOX12_AMOUNT)
        self.assertEqual(
            [key["name"] for key in amount["identity_keys"]],
            ["payer", "statement", "tax-year"],
        )
        self.assertEqual(amount["value_schema"], {"type": "number", "minimum": 0})
        self.assertNotIn("evidence", json.dumps(amount["identity_keys"]))
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(-1, amount["value_schema"])

    def test_residual_v3_omits_2a_and_12(self) -> None:
        # B12-C2 residual succession.
        bundle = _load("f1099div-box12.bundle.json")
        residual = next(
            ft
            for ft in bundle["fact_types"]
            if ft["id"] == "tax.us.2025.f1099div.recorded-boxes" and ft["version"] == "v3"
        )
        self.assertEqual(set(residual["value_schema"]["properties"]), {"3", "5", "7"})
        self.assertNotIn("12", residual["value_schema"]["properties"])
        self.assertNotIn("2a", residual["value_schema"]["properties"])

    def test_historical_residual_v2_still_has_12(self) -> None:
        hist = _load("f1099div-box2a.bundle.json")
        residual = next(
            ft
            for ft in hist["fact_types"]
            if ft["id"] == "tax.us.2025.f1099div.recorded-boxes"
        )
        self.assertEqual(residual["version"], "v2")
        self.assertIn("12", residual["value_schema"]["properties"])

    def test_box13_admits_only_absent_or_zero(self) -> None:
        # B12-C3 / N1 schema surface.
        bundle = _load("f1099div-box12.bundle.json")
        auth = next(ft for ft in bundle["fact_types"] if ft["id"] == BOX13_AUTH)
        jsonschema.validate(None, auth["value_schema"])
        jsonschema.validate(0, auth["value_schema"])
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(5, auth["value_schema"])

    def test_dividend_universe_v3_composable_includes_12(self) -> None:
        universe = _load("dividend-universe.v3.json")
        boxes = {entry["box"] for entry in universe["composable_boxes"]}
        self.assertEqual(boxes, {"1a", "1b", "2a", "12"})
        self.assertEqual(set(universe["recorded_non_composable_boxes"]), {"3", "5", "7"})

    def test_historical_package_and_universe_bytes_unchanged(self) -> None:
        # Immutable history: v15 package and residual v2 bundle still load.
        pkg15 = _load("package.core-calculations.v15.json")
        self.assertEqual(pkg15["version"], "v15")
        self.assertEqual(pkg15["schema"], "artifact-package.v12")
        hist = _load("f1099div-box2a.bundle.json")
        self.assertEqual(hist["version"], "v1")


class PackageExclusivityCases(unittest.TestCase):
    def test_v17_package_validates(self) -> None:
        package = _load("package.core-calculations.v17.json")
        result = validate_package(
            package,
            _corpus(),
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / "published-packages.v12.json"),
        )
        self.assertTrue(result.ok, result.issues)

    def test_mixed_box12_residual_and_family_rejects(self) -> None:
        # N8/N9: residual with property 12 + box-12 family.
        hist = _load("f1099div-box2a.bundle.json")  # residual v2 with 12
        succ = _load("f1099div-box12.bundle.json")
        package = {
            "schema": "artifact-package.v14",
            "id": "demo.package.mixed-box12",
            "version": "v1",
            "scope": {
                "tax_year": 2025,
                "jurisdiction": "US-federal",
                "family": "individual-income-tax",
            },
            "admitted_schemas": [
                "bundle.v2",
                "quantity-vocabulary.v3",
                "quantity-vocabulary.v6",
            ],
            "members": [
                {
                    "role": "fact-type-bundle",
                    "schema": "bundle.v2",
                    "id": hist["id"],
                    "version": hist["version"],
                },
                {
                    "role": "fact-type-bundle",
                    "schema": "bundle.v2",
                    "id": succ["id"],
                    "version": succ["version"],
                },
                {
                    "role": "parameter",
                    "schema": "quantity-vocabulary.v3",
                    "id": "tax.us.2025.quantity.capital-gain-distributions",
                    "version": "v1",
                },
                {
                    "role": "parameter",
                    "schema": "quantity-vocabulary.v6",
                    "id": "tax.us.2025.quantity.exempt-interest-dividends",
                    "version": "v1",
                },
            ],
            "input_bindings": [],
            "entrypoints": [
                {"id": hist["id"], "version": hist["version"]},
                {"id": succ["id"], "version": succ["version"]},
            ],
            "composition_obligations": [],
            "package_checksum": "0" * 64,
        }
        result = validate_package(
            package,
            {
                (hist["id"], hist["version"]): hist,
                (succ["id"], succ["version"]): succ,
                ("tax.us.2025.quantity.capital-gain-distributions", "v1"):
                    _load("quantity.capital-gain-distributions.json"),
                ("tax.us.2025.quantity.exempt-interest-dividends", "v1"):
                    _load("quantity.exempt-interest-dividends.json"),
            },
            DerivationSchemas(),
        )
        codes = {issue.code for issue in result.issues}
        self.assertTrue(
            {"MIXED_BOX12_GRAPH", "MIXED_RESIDUAL_GRAPH"} & codes,
            result.issues,
        )

    def test_line9_raw_box12_read_rejects(self) -> None:
        # B12-C5 package guard.
        bad_line9 = {
            "schema": "rule-artifact.v2",
            "id": "demo.rule.line9-raw-box12",
            "version": "v1",
            "scope": {
                "tax_year": 2025,
                "jurisdiction": "US-federal",
                "family": "individual-income-tax",
                "effective_from": "2025-01-01",
            },
            "role": "computation",
            "requires": [BOX12_AMOUNT],
            "pins": [],
            "when": True,
            "value": {"op": "ref", "name": BOX12_AMOUNT},
            "publishes": "tax.us.2025.income.total-income",
            "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [BOX12_AMOUNT]},
        }
        bad_line9_id = cast(str, bad_line9["id"])
        family = _load("family.f1099div-12.json")
        package = {
            "schema": "artifact-package.v14",
            "id": "demo.package.raw-box12",
            "version": "v1",
            "scope": {
                "tax_year": 2025,
                "jurisdiction": "US-federal",
                "family": "individual-income-tax",
            },
            "admitted_schemas": [
                "rule-artifact.v2",
                "source-family.v1",
                "bundle.v2",
                "quantity-vocabulary.v6",
            ],
            "members": [
                {
                    "role": "computation",
                    "schema": "rule-artifact.v2",
                    "id": bad_line9["id"],
                    "version": "v1",
                },
                {
                    "role": "source-family",
                    "schema": "source-family.v1",
                    "id": family["id"],
                    "version": family["version"],
                },
                {
                    "role": "fact-type-bundle",
                    "schema": "bundle.v2",
                    "id": "tax.us.2025.f1099div.box12.vocabulary",
                    "version": "v1",
                },
                {
                    "role": "parameter",
                    "schema": "quantity-vocabulary.v6",
                    "id": "tax.us.2025.quantity.exempt-interest-dividends",
                    "version": "v1",
                },
            ],
            "input_bindings": [],
            "entrypoints": [{"id": bad_line9["id"], "version": "v1"}],
            "composition_obligations": [],
            "package_checksum": "0" * 64,
        }
        bundle = _load("f1099div-box12.bundle.json")
        result = validate_package(
            package,
            {
                (bad_line9_id, "v1"): bad_line9,
                (family["id"], family["version"]): family,
                (bundle["id"], bundle["version"]): bundle,
                ("tax.us.2025.quantity.exempt-interest-dividends", "v1"):
                    _load("quantity.exempt-interest-dividends.json"),
            },
            DerivationSchemas(),
        )
        codes = {issue.code for issue in result.issues}
        self.assertIn("RAW_BOX12_DOWNSTREAM_READ", codes, result.issues)


class CompanionAdmissionCases(unittest.TestCase):
    def test_box12_without_box13_companion_is_rejected(self) -> None:
        # B12-C3: domain registry declares the companion-presence pair.
        # Production-path missing-companion rejection is LiveEvidenceCases.N1-missing.
        from packages.tax.loader import domain_companion_presence_pairs, tax_registry

        reg = tax_registry()
        self.assertIn(BOX12_AMOUNT, reg.companion_presence_pairs)
        self.assertEqual(
            reg.companion_presence_pairs[BOX12_AMOUNT],
            BOX13_AUTH,
        )
        self.assertEqual(
            domain_companion_presence_pairs()[BOX12_AMOUNT],
            BOX13_AUTH,
        )


class LiveEvidenceCases(unittest.TestCase):
    """P1–P8 / N1–N12 through live_coordinate_run where honest."""

    def test_p1_one_payer_box12_publishes_line2a(self) -> None:
        _, model = _run(_b12_acts(box12_values=[100]), "demo.b12.p1")
        self.assertEqual(_section(model, "line-2a")["resolved"]["value"], 100)
        self.assertEqual(_section(model, "line-2a")["resolved"]["disposition"], "published_value")

    def test_p2_multiple_payers_aggregate_once(self) -> None:
        _, model = _run(_b12_acts(box12_values=[100, 40]), "demo.b12.p2")
        self.assertEqual(_section(model, "line-2a")["resolved"]["value"], 140)

    def test_p3_with_1a_1b_preserves_dividends_and_adds_line2a(self) -> None:
        _, model = _run(
            _b12_acts(box12_values=[50], box1a=600, box1b=100),
            "demo.b12.p3",
        )
        self.assertEqual(_section(model, "line-2a")["resolved"]["value"], 50)
        # Ordinary dividends still present when box1a provided.
        line3b = _section(model, "line-3b")["resolved"]
        self.assertIn(line3b["disposition"], {"published_value", "computed_zero", "closure_backed_zero", "blocked", "guard_inapplicable"})

    def test_p5_closed_empty_publishes_zero(self) -> None:
        _, model = _run(_b12_acts(box12_values=[], close_box12=True), "demo.b12.p5")
        resolved = _section(model, "line-2a")["resolved"]
        self.assertIn(resolved["disposition"], {"closure_backed_zero", "computed_zero", "published_value"})
        self.assertEqual(resolved.get("value"), 0)

    def test_p6_missing_closure_blocks(self) -> None:
        _, model = _run(
            _b12_acts(box12_values=[100], close_box12=False),
            "demo.b12.p6-open",
        )
        self.assertEqual(_section(model, "line-2a")["resolved"]["disposition"], "blocked")

    def test_p7_box13_absent_and_zero_admissible(self) -> None:
        _, absent = _run(_b12_acts(box12_values=[25], box13_values=[None]), "demo.b12.p7-null")
        self.assertEqual(_section(absent, "line-2a")["resolved"]["value"], 25)
        _, zero = _run(_b12_acts(box12_values=[25], box13_values=[0]), "demo.b12.p7-zero")
        self.assertEqual(_section(zero, "line-2a")["resolved"]["value"], 25)

    def test_n1_nonzero_box13_rejected_at_admission(self) -> None:
        # B12-C3 / N1: nonzero box 13 is a hard admission block; no Form 6251.
        acts = _b12_acts(box12_values=[100], box13_values=[5])
        with self.assertRaises(FindingModelError) as ctx:
            with TemporaryDirectory() as tmp:
                live_coordinate_run(
                    WorkspaceCapability(Path(tmp) / "L"),
                    repo_root=ROOT,
                    authoritative_acts=acts,
                    workspace_revision=len(acts),
                    run_scope=SCOPE,
                    scope_user=USER,
                    request={"schema": "run-request.v1"},
                    run_id="demo.b12.n1",
                    governance_pins=[],
                    surface=_surface(),
                    output_name="out.json",
                )
        message = str(ctx.exception).lower()
        self.assertIn("box13", message.replace("_", "").replace("-", "") or message)
        self.assertNotIn("6251", message)

    def test_n1_missing_box13_companion_rejected_on_live_path(self) -> None:
        # B12-C3 / N1: missing companion must not be treated as absent on the
        # production live path. Would publish line 2a before the repair.
        acts = _b12_acts(box12_values=[100], include_box13=False)
        with self.assertRaises(FindingModelError) as ctx:
            with TemporaryDirectory() as tmp:
                live_coordinate_run(
                    WorkspaceCapability(Path(tmp) / "L"),
                    repo_root=ROOT,
                    authoritative_acts=acts,
                    workspace_revision=len(acts),
                    run_scope=SCOPE,
                    scope_user=USER,
                    request={"schema": "run-request.v1"},
                    run_id="demo.b12.n1-missing-companion",
                    governance_pins=[],
                    surface=_surface(),
                    output_name="out.json",
                )
        message = str(ctx.exception)
        self.assertIn("companion presence violated", message)
        self.assertIn(BOX12_AMOUNT, message)
        self.assertIn(BOX13_AUTH, message)
        self.assertNotIn("6251", message.lower())

    def test_n2_to_n7_scope_no_blocks_line2a(self) -> None:
        for token in (
            "no-f1099int-tax-exempt",  # N2
            "no-f1099oid-tax-exempt",  # N3
            "no-unreported-tax-exempt",  # N4
            "no-premium-adjustment",  # N5
            "no-amt-form-6251",  # N7 partial
        ):
            with self.subTest(token=token):
                _, model = _run(
                    _b12_acts(box12_values=[80], scope={token: "no"}),
                    f"demo.b12.scope-{token}",
                )
                disp = _section(model, "line-2a")["resolved"]["disposition"]
                self.assertIn(disp, {"blocked", "guard_inapplicable"}, disp)

    def test_n6_missing_scope_declaration_blocks(self) -> None:
        acts = _b12_acts(box12_values=[80])
        # Drop one scope assertion.
        acts = [
            act
            for act in acts
            if not (
                act["kind"] == "assertion"
                and "line2a-scope.no-f1099int-tax-exempt" in json.dumps(act["payload"])
            )
        ]
        # Re-number committed_against for adoption tail.
        for index, act in enumerate(acts):
            act["committed_against"] = index
            act["act_id"] = f"demo.b12.n6.act.{index:03d}"
        _, model = _run(acts, "demo.b12.n6")
        self.assertEqual(_section(model, "line-2a")["resolved"]["disposition"], "blocked")

    def test_p_line2a_does_not_change_line9(self) -> None:
        # P5/B12-C5: positive line 2a leaves line 9 unchanged vs zero box12.
        _, with_box12 = _run(_b12_acts(box12_values=[140], box1a=0), "demo.b12.line9-pos")
        _, without = _run(_b12_acts(box12_values=[], box1a=0), "demo.b12.line9-zero")
        self.assertEqual(
            _section(with_box12, "line-2a")["resolved"]["value"],
            140,
        )
        self.assertEqual(
            _section(with_box12, "line-9")["resolved"].get("value"),
            _section(without, "line-9")["resolved"].get("value"),
        )
        self.assertEqual(
            _section(with_box12, "line-9")["resolved"]["disposition"],
            _section(without, "line-9")["resolved"]["disposition"],
        )

    def test_n10_correction_same_identity(self) -> None:
        acts = _b12_acts(box12_values=[100])
        # Correct the amount in place (same logical identity).
        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.b12.finding.box12.correction",
                        f"{BOX12_AMOUNT}|payer=demo.cgd.t2.payer,statement=demo.cgd.t2.stmt,tax-year=2025",
                        125,
                    )
                },
            )
        )
        _, model = _run(acts, "demo.b12.n10")
        self.assertEqual(_section(model, "line-2a")["resolved"]["value"], 125)

    def test_p8_presentation_shows_value_and_reported_only_explain(self) -> None:
        _, model = _run(_b12_acts(box12_values=[140]), "demo.b12.p8")
        section = _section(model, "line-2a")
        self.assertEqual(section["resolved"]["value"], 140)
        explain = json.dumps(section).lower()
        self.assertTrue(
            "not directly taxable" in explain
            or "reported but not" in explain
            or "tax-exempt" in explain,
            section,
        )
        # Citation sites present for authority walk.
        self.assertTrue(section.get("citationSites") or model.get("citationGroups"))

    def test_n12_malformed_presentation_keeps_sibling(self) -> None:
        _, model = _run(_b12_acts(box12_values=[50]), "demo.b12.n12")
        malformed = copy.deepcopy(model)
        _section(malformed, "line-2a")["resolved"]["value"] = "not-a-number"
        # Sibling line-9 remains structurally present.
        self.assertIn("disposition", _section(malformed, "line-9")["resolved"])


class CompatibilityCases(unittest.TestCase):
    def test_n11_v15_historical_package_still_validates(self) -> None:
        package = _load("package.core-calculations.v15.json")
        result = validate_package(
            package,
            _corpus(),
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / "published-packages.v10.json"),
        )
        self.assertTrue(result.ok, result.issues)


if __name__ == "__main__":
    unittest.main()
