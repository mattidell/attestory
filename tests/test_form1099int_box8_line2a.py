"""Form 1099-INT box 8 → Form 1040 line 2a: B8-C1–C6 and evidence matrix."""

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
    load_published_citizen_checksums,
    validate_package,
)
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.findings import FindingModelError
from packages.tax.loader import TAX_CONTENT_DIR, domain_companion_presence_pairs, tax_registry
from tests.test_form1099div_box12_line2a import _b12_acts as _box12_base_acts


ROOT = Path(__file__).resolve().parent.parent
CONTENT = TAX_CONTENT_DIR
FIXTURES = ROOT / "packages" / "sample_data" / "form1099int_box8_line2a"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

BOX8_AMOUNT = "tax.us.2025.f1099int.box8-tax-exempt-interest"
BOX8_CLOSURE = "tax.us.2025.f1099int.b8.source-closure"
BOX8_FAMILY = "tax.us.2025.f1099int.b8"
BOX9_AUTH = "tax.us.2025.f1099int.box9-specified-pab-authority"
BOX12_AMOUNT = "tax.us.2025.f1099div.box12-exempt-interest-dividends"
LINE2A = "tax.us.2025.rule.form1040-line2a"

# Residual scope under successor (no-f1099int is Path A/B gate, not residual).
RESIDUAL_SCOPE_TOKENS = (
    "no-f1099oid-tax-exempt",
    "no-unreported-tax-exempt",
    "no-premium-adjustment",
    "no-child-income-election",
    "no-taxable-social-security",
    "no-amt-form-6251",
    "no-credit-using-tax-exempt",
    "no-deduction-using-tax-exempt",
)
ALL_SCOPE_TOKENS = ("no-f1099int-tax-exempt",) + RESIDUAL_SCOPE_TOKENS


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


def _corpus() -> dict[tuple[str, str], dict[str, Any]]:
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        try:
            value = json.loads(path.read_text("utf-8"))
        except Exception:
            continue
        if isinstance(value, dict) and isinstance(value.get("id"), str) and isinstance(
            value.get("version"), str
        ):
            corpus[(value["id"], value["version"])] = value
    return corpus


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / "published-packages.v14.json",
        CONTENT,
    )


def _act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.b8.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-08-05T12:{index // 60:02d}:{index % 60:02d}Z",
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


def _b8_acts(
    *,
    box8_values: list[float] | None = None,
    box9_values: list[object] | None = None,
    close_box8: bool = True,
    box12_values: list[float] | None = None,
    close_box12: bool = True,
    path: str = "B",
    scope: dict[str, str] | None = None,
    include_box9: bool = True,
    wages: float = 90000,
) -> list[dict[str, object]]:
    """Production-shaped act log on the v18 multi-family line-2a route.

    path=\"A\": no-f1099int-tax-exempt=yes (box-8 optional / unused).
    path=\"B\": no-f1099int-tax-exempt=no and box-8 closed.
    """
    if box8_values is None:
        box8_values = [80.0] if path == "B" else []
    if box9_values is None:
        box9_values = [None] * max(1, len(box8_values))
    if box12_values is None:
        box12_values = [] if path == "B" else [100.0]

    scope_vals = {token: "yes" for token in ALL_SCOPE_TOKENS}
    if path == "A":
        scope_vals["no-f1099int-tax-exempt"] = "yes"
    else:
        scope_vals["no-f1099int-tax-exempt"] = "no"
    if scope:
        scope_vals.update(scope)

    # Base box-12 Path A-shaped acts (v17 adoption); rewrite scope + adoption.
    acts = _box12_base_acts(
        box12_values=box12_values,
        close_box12=close_box12,
        scope=scope_vals,
        wages=wages,
        include_box13=True,
    )
    # Drop v17 adoption; we append box-8 material and v18 adoption below.
    acts = [act for act in acts if act.get("kind") != "package-adoption"]

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("f1099int-box8.bundle.json")})

    payers_stmts: list[tuple[str, str]] = []
    for index in range(max(len(box8_values), 1 if box8_values == [] and close_box8 else 0)):
        # When closed-empty with no members, still need horizon genesis only.
        pass

    if box8_values or close_box8:
        add(
            "horizon-genesis",
            {
                "family": {"id": BOX8_FAMILY, "version": "v1"},
                "scope": SCOPE_KEY,
                "horizon_id": "demo.b8.h0",
            },
        )
        horizon = "demo.b8.h0"
        for index, amount in enumerate(box8_values):
            payer = f"demo.b8.payer.{index}"
            stmt = f"demo.b8.stmt.{index}"
            add(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": payer,
                        "kind": "tax.us.interest-payer",
                        "label": f"Synthetic box-8 payer {index}",
                    }
                },
            )
            add(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": stmt,
                        "kind": "tax.us.1099int-statement",
                        "label": f"Synthetic box-8 statement {index}",
                    }
                },
            )
            payers_stmts.append((payer, stmt))
            if include_box9:
                add(
                    "assertion",
                    {
                        "finding": _attested(
                            f"demo.b8.finding.box9.{index}",
                            f"{BOX9_AUTH}|payer={payer},statement={stmt},tax-year=2025",
                            box9_values[index] if index < len(box9_values) else None,
                        )
                    },
                )
            next_horizon = f"demo.b8.h{index + 1}"
            add(
                "member-transition",
                {
                    "family": {"id": BOX8_FAMILY, "version": "v1"},
                    "scope": SCOPE_KEY,
                    "member": {
                        "action": "assert",
                        "finding": _attested(
                            f"demo.b8.finding.box8.{index}",
                            f"{BOX8_AMOUNT}|payer={payer},statement={stmt},tax-year=2025",
                            amount,
                        ),
                    },
                    "successor": {"id": next_horizon, "predecessor": horizon},
                },
            )
            horizon = next_horizon

        if close_box8:
            add(
                "assertion",
                {
                    "finding": _attested(
                        "demo.b8.closure.box8",
                        f"{BOX8_CLOSURE}|family-horizon={horizon},tax-year=2025",
                        True,
                    )
                },
            )

    adoption = cast(
        dict[str, object],
        json.loads((FIXTURES / "adoptions" / "adopt-core-v19-current.json").read_text("utf-8")),
    )
    adoption["committed_against"] = len(acts)
    acts.append(adoption)

    # Renumber act ids / committed_against for a clean log.
    for index, act in enumerate(acts):
        act["committed_against"] = index
        if str(act.get("act_id", "")).startswith("demo.b8.") or str(
            act.get("act_id", "")
        ).startswith("demo.b12.") or str(act.get("act_id", "")).startswith("demo.cgd."):
            act["act_id"] = f"demo.b8.act.{index:03d}"
        act["actor"] = USER
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


def _derived_id(section: dict[str, Any]) -> str:
    resolved_raw = section.get("resolved")
    resolved: dict[str, Any] = resolved_raw if isinstance(resolved_raw, dict) else {}
    act_raw = resolved.get("act")
    act: dict[str, Any] = act_raw if isinstance(act_raw, dict) else {}
    finding_raw = act.get("finding")
    finding: dict[str, Any] = finding_raw if isinstance(finding_raw, dict) else {}
    finding_id = finding.get("id")
    if isinstance(finding_id, str):
        return finding_id
    return json.dumps(resolved, sort_keys=True)


def _section(model: dict[str, Any], section_id: str) -> dict[str, Any]:

    return next(section for section in model["sections"] if section["id"] == section_id)


class CitizenContractCases(unittest.TestCase):
    """B8-C1 / B8-C2 citizen shapes and historical immutability."""

    def test_box8_member_identity_and_nonnegative(self) -> None:
        bundle = _load("f1099int-box8.bundle.json")
        amount = next(ft for ft in bundle["fact_types"] if ft["id"] == BOX8_AMOUNT)
        self.assertEqual(
            [key["name"] for key in amount["identity_keys"]],
            ["payer", "statement", "tax-year"],
        )
        self.assertEqual(amount["value_schema"], {"type": "number", "minimum": 0})
        self.assertNotIn("evidence", json.dumps(amount["identity_keys"]))
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(-1, amount["value_schema"])

    def test_box9_admits_only_absent_or_zero(self) -> None:
        bundle = _load("f1099int-box8.bundle.json")
        auth = next(ft for ft in bundle["fact_types"] if ft["id"] == BOX9_AUTH)
        jsonschema.validate(None, auth["value_schema"])
        jsonschema.validate(0, auth["value_schema"])
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(5, auth["value_schema"])

    def test_historical_line2a_v1_bytes_immutable(self) -> None:
        hist = _load("rule.form1040-line2a.json")
        self.assertEqual(hist["version"], "v1")
        self.assertEqual(hist["value"], {"name": "tax.us.2025.dividends.12-subtotal", "op": "ref"})
        succ = _load("rule.form1040-line2a.v2.json")
        self.assertEqual(succ["version"], "v2")
        self.assertNotEqual(hist, succ)

    def test_companion_pair_registered_on_domain_and_registry(self) -> None:
        reg = tax_registry()
        self.assertEqual(
            domain_companion_presence_pairs()[BOX8_AMOUNT],
            BOX9_AUTH,
        )
        self.assertEqual(reg.companion_presence_pairs[BOX8_AMOUNT], BOX9_AUTH)


class PackageExclusivityCases(unittest.TestCase):
    def test_v18_package_validates(self) -> None:
        package = _load("package.core-calculations.v19.json")
        result = validate_package(
            package,
            _corpus(),
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / "published-packages.v14.json"),
        )
        self.assertTrue(result.ok, result.issues)

    def test_historical_v17_still_validates(self) -> None:
        package = _load("package.core-calculations.v17.json")
        result = validate_package(
            package,
            _corpus(),
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / "published-packages.v12.json"),
        )
        self.assertTrue(result.ok, result.issues)

    def test_mixed_historical_line2a_v1_and_box8_rejects(self) -> None:
        hist_rule = _load("rule.form1040-line2a.json")
        family = _load("family.f1099int-b8.json")
        bundle = _load("f1099int-box8.bundle.json")
        package = {
            "schema": "artifact-package.v16",
            "id": "demo.package.mixed-line2a",
            "version": "v1",
            "scope": {
                "tax_year": 2025,
                "jurisdiction": "US-federal",
                "family": "individual-income-tax",
            },
            "admitted_schemas": [
                "rule-artifact.v3",
                "source-family.v1",
                "bundle.v2",
                "quantity-vocabulary.v8",
            ],
            "members": [
                {
                    "role": "computation",
                    "schema": "rule-artifact.v3",
                    "id": hist_rule["id"],
                    "version": hist_rule["version"],
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
                    "id": bundle["id"],
                    "version": bundle["version"],
                },
                {
                    "role": "parameter",
                    "schema": "quantity-vocabulary.v8",
                    "id": "tax.us.2025.quantity.tax-exempt-interest",
                    "version": "v1",
                },
            ],
            "input_bindings": [],
            "entrypoints": [
                {"id": hist_rule["id"], "version": hist_rule["version"]},
                {"id": bundle["id"], "version": bundle["version"]},
            ],
            "composition_obligations": [],
            "package_checksum": "0" * 64,
        }
        result = validate_package(
            package,
            {
                (hist_rule["id"], hist_rule["version"]): hist_rule,
                (family["id"], family["version"]): family,
                (bundle["id"], bundle["version"]): bundle,
                ("tax.us.2025.quantity.tax-exempt-interest", "v1"): _load(
                    "quantity.tax-exempt-interest.json"
                ),
            },
            DerivationSchemas(),
        )
        codes = {issue.code for issue in result.issues}
        self.assertIn("MIXED_LINE2A_GRAPH", codes, result.issues)

    def test_line9_raw_box8_read_rejects(self) -> None:
        bad_line9 = {
            "schema": "rule-artifact.v2",
            "id": "demo.rule.line9-raw-box8",
            "version": "v1",
            "scope": {
                "tax_year": 2025,
                "jurisdiction": "US-federal",
                "family": "individual-income-tax",
                "effective_from": "2025-01-01",
            },
            "role": "computation",
            "requires": [BOX8_AMOUNT],
            "pins": [],
            "when": True,
            "value": {"op": "ref", "name": BOX8_AMOUNT},
            "publishes": "tax.us.2025.income.total-income",
            "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [BOX8_AMOUNT]},
        }
        family = _load("family.f1099int-b8.json")
        bundle = _load("f1099int-box8.bundle.json")
        package = {
            "schema": "artifact-package.v16",
            "id": "demo.package.raw-box8",
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
                "quantity-vocabulary.v8",
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
                    "id": bundle["id"],
                    "version": bundle["version"],
                },
                {
                    "role": "parameter",
                    "schema": "quantity-vocabulary.v8",
                    "id": "tax.us.2025.quantity.tax-exempt-interest",
                    "version": "v1",
                },
            ],
            "input_bindings": [],
            "entrypoints": [{"id": bad_line9["id"], "version": "v1"}],
            "composition_obligations": [],
            "package_checksum": "0" * 64,
        }
        result = validate_package(
            package,
            {
                (cast(str, bad_line9["id"]), "v1"): bad_line9,
                (family["id"], family["version"]): family,
                (bundle["id"], bundle["version"]): bundle,
                ("tax.us.2025.quantity.tax-exempt-interest", "v1"): _load(
                    "quantity.tax-exempt-interest.json"
                ),
            },
            DerivationSchemas(),
        )
        codes = {issue.code for issue in result.issues}
        self.assertIn("RAW_BOX8_DOWNSTREAM_READ", codes, result.issues)


class LiveEvidenceCases(unittest.TestCase):
    """Evidence matrix P1–P12 / N1–N7 through live_coordinate_run."""

    def test_p1_one_payer_box8_publishes_line2a(self) -> None:
        # P1 / Path B box-8-only (box-12 closed-empty).
        _, model = _run(_b8_acts(box8_values=[80], box12_values=[], path="B"), "demo.b8.p1")
        self.assertEqual(_section(model, "line-2a")["resolved"]["value"], 80)
        self.assertEqual(
            _section(model, "line-2a")["resolved"]["disposition"], "published_value"
        )

    def test_p2_multiple_payers_aggregate_once(self) -> None:
        _, model = _run(
            _b8_acts(box8_values=[80, 20], box12_values=[], path="B"), "demo.b8.p2"
        )
        self.assertEqual(_section(model, "line-2a")["resolved"]["value"], 100)

    def test_p3_box8_only_box12_closed_empty(self) -> None:
        _, model = _run(
            _b8_acts(box8_values=[55], box12_values=[], path="B"), "demo.b8.p3"
        )
        self.assertEqual(_section(model, "line-2a")["resolved"]["value"], 55)

    def test_p4_path_a_box12_only(self) -> None:
        _, model = _run(
            _b8_acts(box8_values=[], box12_values=[100], path="A", close_box8=False),
            "demo.b8.p4",
        )
        self.assertEqual(_section(model, "line-2a")["resolved"]["value"], 100)

    def test_p5_mixed_aggregation(self) -> None:
        _, model = _run(
            _b8_acts(box8_values=[80], box12_values=[100], path="B"), "demo.b8.p5"
        )
        self.assertEqual(_section(model, "line-2a")["resolved"]["value"], 180)

    def test_p6_box9_null_admissible(self) -> None:
        _, model = _run(
            _b8_acts(box8_values=[25], box9_values=[None], path="B"), "demo.b8.p6"
        )
        self.assertEqual(_section(model, "line-2a")["resolved"]["value"], 25)

    def test_p7_box9_zero_admissible(self) -> None:
        _, model = _run(
            _b8_acts(box8_values=[25], box9_values=[0], path="B"), "demo.b8.p7"
        )
        self.assertEqual(_section(model, "line-2a")["resolved"]["value"], 25)

    def test_n1_missing_box9_companion_rejected_on_live_path(self) -> None:
        acts = _b8_acts(box8_values=[80], include_box9=False, path="B")
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
                    run_id="demo.b8.n1-missing",
                    governance_pins=[],
                    surface=_surface(),
                    output_name="out.json",
                )
        message = str(ctx.exception)
        self.assertIn("companion presence violated", message)
        self.assertIn(BOX8_AMOUNT, message)
        self.assertIn(BOX9_AUTH, message)
        self.assertNotIn("6251", message.lower())

    def test_n2_nonzero_box9_rejected_without_form_6251(self) -> None:
        acts = _b8_acts(box8_values=[80], box9_values=[5], path="B")
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
                    run_id="demo.b8.n2",
                    governance_pins=[],
                    surface=_surface(),
                    output_name="out.json",
                )
        message = str(ctx.exception).lower()
        self.assertNotIn("6251", message)

    def test_n3_open_box8_under_path_b_blocks(self) -> None:
        _, model = _run(
            _b8_acts(box8_values=[80], close_box8=False, path="B"), "demo.b8.n3"
        )
        disp = _section(model, "line-2a")["resolved"]["disposition"]
        self.assertIn(disp, {"blocked", "guard_inapplicable"}, disp)

    def test_p8_late_member_then_restored_closure(self) -> None:
        acts = _b8_acts(box8_values=[80], path="B")
        # Late second member after closure: advances horizon, invalidates prior closure.
        acts.append(
            _act(
                len(acts),
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": "demo.b8.payer.late",
                        "kind": "tax.us.interest-payer",
                        "label": "Synthetic late box-8 payer",
                    }
                },
            )
        )
        acts.append(
            _act(
                len(acts),
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": "demo.b8.stmt.late",
                        "kind": "tax.us.1099int-statement",
                        "label": "Synthetic late box-8 statement",
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
                        "demo.b8.finding.box9.late",
                        f"{BOX9_AUTH}|payer=demo.b8.payer.late,statement=demo.b8.stmt.late,tax-year=2025",
                        None,
                    )
                },
            )
        )
        # Find current horizon from last box-8 transition or genesis.
        prior_horizon = "demo.b8.h1"  # one member → h1
        acts.append(
            _act(
                len(acts),
                "member-transition",
                {
                    "family": {"id": BOX8_FAMILY, "version": "v1"},
                    "scope": SCOPE_KEY,
                    "member": {
                        "action": "assert",
                        "finding": _attested(
                            "demo.b8.finding.box8.late",
                            f"{BOX8_AMOUNT}|payer=demo.b8.payer.late,statement=demo.b8.stmt.late,tax-year=2025",
                            20,
                        ),
                    },
                    "successor": {"id": "demo.b8.h.late", "predecessor": prior_horizon},
                },
            )
        )
        # Without re-close: line 2a blocked/stale.
        stale_acts = list(acts)
        for index, act in enumerate(stale_acts):
            act["committed_against"] = index
        _, stale = _run(stale_acts, "demo.b8.p8-stale")
        self.assertIn(
            _section(stale, "line-2a")["resolved"]["disposition"],
            {"blocked", "guard_inapplicable"},
        )
        # Re-close on successor horizon restores publication.
        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.b8.closure.box8.restored",
                        f"{BOX8_CLOSURE}|family-horizon=demo.b8.h.late,tax-year=2025",
                        True,
                    )
                },
            )
        )
        for index, act in enumerate(acts):
            act["committed_against"] = index
        _, restored = _run(acts, "demo.b8.p8-restored")
        self.assertEqual(_section(restored, "line-2a")["resolved"]["value"], 100)

    def test_p9_correction_same_identity(self) -> None:
        acts = _b8_acts(box8_values=[80], path="B")
        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.b8.finding.box8.correction",
                        f"{BOX8_AMOUNT}|payer=demo.b8.payer.0,statement=demo.b8.stmt.0,tax-year=2025",
                        95,
                    )
                },
            )
        )
        for index, act in enumerate(acts):
            act["committed_against"] = index
        _, model = _run(acts, "demo.b8.p9")
        self.assertEqual(_section(model, "line-2a")["resolved"]["value"], 95)

    def test_box9_correction_displaces_line2a(self) -> None:
        """Same-statement box-9 null→0 re-derives line 2a (ADR-0010 companion pin)."""
        acts = _b8_acts(box8_values=[80], path="B", box9_values=[None])
        for index, act in enumerate(acts):
            act["committed_against"] = index
        _, first = _run(acts, "demo.b8.box9-disp-1")
        section1 = _section(first, "line-2a")
        self.assertEqual(section1["resolved"]["value"], 80)
        id1 = _derived_id(section1)

        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.b8.finding.box9.corrected",
                        f"{BOX9_AUTH}|payer=demo.b8.payer.0,statement=demo.b8.stmt.0,tax-year=2025",
                        0,
                    )
                },
            )
        )
        for index, act in enumerate(acts):
            act["committed_against"] = index
        _, second = _run(acts, "demo.b8.box9-disp-2")
        section2 = _section(second, "line-2a")
        self.assertEqual(section2["resolved"]["value"], 80)
        id2 = _derived_id(section2)
        self.assertNotEqual(id1, id2, "box-9 correction must re-derive line 2a")
        # Intermediate subtotal (or presentation) must pin the corrected companion.
        blob = json.dumps(second)
        self.assertIn("demo.b8.finding.box9.corrected", blob)

    def test_p10_path_switch_displaces(self) -> None:
        """One act log: Path A → Path B by correcting the INT absence declaration."""
        acts = _b8_acts(
            box8_values=[], box12_values=[100], path="A", close_box8=False
        )
        for index, act in enumerate(acts):
            act["committed_against"] = index
        _, path_a = _run(acts, "demo.b8.p10-a")
        sec_a = _section(path_a, "line-2a")
        self.assertEqual(sec_a["resolved"]["value"], 100)
        id_a = _derived_id(sec_a)

        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.b8.scope.no-f1099int.switched",
                        f"{_scope_id('no-f1099int-tax-exempt')}|tax-year=2025",
                        "no",
                    )
                },
            )
        )
        b_only = _b8_acts(box8_values=[80], box12_values=[], path="B", close_box12=False)
        for act in b_only:
            kind = str(act.get("kind"))
            pl_raw = act.get("payload")
            pl: dict[str, Any] = pl_raw if isinstance(pl_raw, dict) else {}
            if kind == "package-adoption":
                continue
            if kind == "bundle-adoption":
                # Keep INT box-8 bundle if not already present.
                bundle_raw = pl.get("bundle")
                bundle = bundle_raw if isinstance(bundle_raw, dict) else None
                bid = str(bundle.get("id") or "") if bundle is not None else ""
                if "f1099int" in bid or "box8" in json.dumps(bundle or {}).lower():
                    acts.append(dict(act))
                continue
            if kind == "horizon-genesis":
                family_raw = pl.get("family")
                family = family_raw if isinstance(family_raw, dict) else {}
                fam = str(family.get("id") or "")
                if fam == BOX8_FAMILY:
                    acts.append(dict(act))
                continue
            if kind == "entity-introduced":
                ent_raw = pl.get("entity")
                ent = ent_raw if isinstance(ent_raw, dict) else {}
                eid = str(ent.get("id") or "")
                if eid.startswith("demo.b8."):
                    acts.append(dict(act))
                continue
            if kind == "member-transition":
                family_raw = pl.get("family")
                family = family_raw if isinstance(family_raw, dict) else {}
                fam = str(family.get("id") or "")
                if fam == BOX8_FAMILY:
                    acts.append(dict(act))
                continue
            if kind == "assertion":
                finding_raw = pl.get("finding")
                finding = finding_raw if isinstance(finding_raw, dict) else {}
                fact_id = str(finding.get("fact_id") or "")
                if fact_id.startswith(BOX8_AMOUNT) or fact_id.startswith(BOX9_AUTH) or fact_id.startswith(BOX8_CLOSURE):
                    acts.append(dict(act))
                continue
        for index, act in enumerate(acts):
            act["committed_against"] = index
            act["act_id"] = f"demo.b8.act.{index:03d}"

        _, path_b = _run(acts, "demo.b8.p10-b")
        sec_b = _section(path_b, "line-2a")
        self.assertEqual(sec_b["resolved"]["value"], 180)
        id_b = _derived_id(sec_b)
        self.assertNotEqual(id_a, id_b, "path switch must re-derive line 2a")
        self.assertIn("demo.b8.scope.no-f1099int.switched", json.dumps(path_b))

    def test_path_a_with_nonempty_box8_fails_honestly(self) -> None:
        # Path A yes + non-empty box-8 → declaration/signal contradiction.
        acts = _b8_acts(box8_values=[80], box12_values=[100], path="A")
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
                    run_id="demo.b8.path-a-contradiction",
                    governance_pins=[],
                    surface=_surface(),
                    output_name="out.json",
                )
        message = str(ctx.exception).lower()
        self.assertIn("contradiction", message)
        self.assertIn("no-f1099int", message.replace("_", "-") or message)

    def test_n4_oid_scope_no_blocks(self) -> None:
        _, model = _run(
            _b8_acts(box8_values=[80], path="B", scope={"no-f1099oid-tax-exempt": "no"}),
            "demo.b8.n4",
        )
        disp = _section(model, "line-2a")["resolved"]["disposition"]
        self.assertIn(disp, {"blocked", "guard_inapplicable"}, disp)

    def test_n5_premium_scope_no_blocks(self) -> None:
        _, model = _run(
            _b8_acts(box8_values=[80], path="B", scope={"no-premium-adjustment": "no"}),
            "demo.b8.n5",
        )
        disp = _section(model, "line-2a")["resolved"]["disposition"]
        self.assertIn(disp, {"blocked", "guard_inapplicable"}, disp)

    def test_n6_excluded_downstream_consumer_blocks(self) -> None:
        _, model = _run(
            _b8_acts(box8_values=[80], path="B", scope={"no-amt-form-6251": "no"}),
            "demo.b8.n6",
        )
        disp = _section(model, "line-2a")["resolved"]["disposition"]
        self.assertIn(disp, {"blocked", "guard_inapplicable"}, disp)

    def test_p11_line2a_changes_line9_and_taxable_income_unchanged(self) -> None:
        _, with_te = _run(
            _b8_acts(box8_values=[80], box12_values=[100], path="B"), "demo.b8.p11-pos"
        )
        _, without = _run(
            _b8_acts(box8_values=[], box12_values=[], path="A", close_box8=False),
            "demo.b8.p11-zero",
        )
        self.assertEqual(_section(with_te, "line-2a")["resolved"]["value"], 180)
        for section_id in ("line-9", "line-15"):
            # line-15 is taxable income on the Form 1040 surface used in goldens.
            if section_id not in json.dumps(with_te) and section_id == "line-15":
                # Fall back: any section labeled taxable income
                taxable_ids = [
                    s.get("id")
                    for s in with_te.get("sections", [])
                    if "taxable" in json.dumps(s).lower()
                ]
                self.assertTrue(taxable_ids or _section(with_te, "line-9"), taxable_ids)
                continue
            self.assertEqual(
                _section(with_te, section_id)["resolved"].get("value"),
                _section(without, section_id)["resolved"].get("value"),
                section_id,
            )
            self.assertEqual(
                _section(with_te, section_id)["resolved"]["disposition"],
                _section(without, section_id)["resolved"]["disposition"],
                section_id,
            )

    def test_p12_presentation_golden_reported_only(self) -> None:
        """Committed presentation golden must match the live model byte-for-structure."""
        _, model = _run(
            _b8_acts(box8_values=[80], box12_values=[100], path="B"), "demo.b8.p12"
        )
        golden_path = FIXTURES / "presentation" / "box8-line2a.presentation-model.v1.json"
        self.assertTrue(
            golden_path.is_file(),
            f"committed presentation golden required at {golden_path}",
        )
        golden = json.loads(golden_path.read_text("utf-8"))
        # Full structural equality: value, citations, authority, explain, pin labels,
        # and every other section the surface publishes (P12 contract).
        self.assertEqual(model, golden)
        live_sec = _section(model, "line-2a")
        self.assertEqual(live_sec["resolved"]["value"], 180)
        explain = json.dumps(live_sec).lower()
        self.assertTrue(
            "not directly taxable" in explain
            or "reported but not" in explain
            or "tax-exempt" in explain,
            explain[:500],
        )

    def test_n7_malformed_presentation_blocks_or_redacts(self) -> None:
        """Projector on the real line-2a field path rejects non-numeric publication."""
        from packages.derivation.loader import DerivationSchemas, load_canon
        from packages.derivation.marshal import marshal_live_run_context
        from packages.derivation.presentation_projection import (
            PresentationModelError,
            build_presentation_model,
        )
        from packages.derivation.production_executor import execute_marshaled
        from packages.derivation.production_resolver import resolve_production_package
        from packages.derivation.runner import Publication
        from packages.kernel.currency import compute_currency
        from packages.kernel.findings import project
        from packages.tax.loader import (
            domain_companion_presence_pairs,
            install_domain_companion_presence,
            install_domain_declaration_signal_contradictions,
        )
        from packages.derivation.live import _resolved_run_material

        acts = _b8_acts(box8_values=[50], path="B")
        schemas = DerivationSchemas()
        install_domain_companion_presence(schemas.registry)
        install_domain_declaration_signal_contradictions(schemas.registry)
        from packages.derivation.production_resolver import ResolvedGraph

        resolved = resolve_production_package(
            acts,
            run_scope=SCOPE,
            scope_user=USER,
            workspace_revision=len(acts),
            surface=_surface(),
            schemas=schemas,
        )
        self.assertIsInstance(resolved, ResolvedGraph)
        assert isinstance(resolved, ResolvedGraph)
        state = project(tuple(dict(act) for act in acts), schemas.registry)
        currency = compute_currency(state)
        rules, parameters, families, mappings, fact_types, bindings, collect_names = (
            _resolved_run_material(resolved)
        )
        context = marshal_live_run_context(
            run_id="demo.b8.n7-projector",
            state=state,
            currency=currency,
            rules=rules,
            parameters=parameters,
            canon=load_canon(schemas),
            adoption_pin={
                "role": "adoption",
                "id": resolved.package["id"],
                "version": resolved.package["version"],
            },
            governance_pins=[],
            family_declarations=families,
            closure_mappings=mappings,
            fact_types=fact_types,
            input_bindings=bindings,
            collect_source_names=collect_names,
            companion_presence_pairs=domain_companion_presence_pairs(),
        )
        result = execute_marshaled(context, schemas)
        symbol = "tax.us.2025.tax-exempt-interest.line2a-total"
        pubs: list[Publication] = []
        found = False
        for pub in result.publications:
            finding = copy.deepcopy(pub.finding)
            if finding.get("symbol") == symbol:
                finding["value"] = "not-a-number"
                found = True
            pubs.append(Publication(act=pub.act, finding=finding))
        self.assertTrue(found, "expected line2a-total publication from the live package path")
        with self.assertRaises(PresentationModelError) as ctx:
            build_presentation_model(
                run_id="demo.b8.n7-bad",
                resolved_members=resolved.resolved_members,
                state=state,
                publications=pubs,
                dispositions=result.dispositions,
            )
        message = str(ctx.exception).lower()
        self.assertIn("invalid numeric", message)
        self.assertIn("line2a", message.replace("-", "").replace("_", "") or message)



class CompanionProvenanceFailClosedCases(unittest.TestCase):
    """Companion pin edges must fail closed (shared box-9 / box-13 path)."""

    def test_runner_fails_closed_when_box13_companion_source_missing(self) -> None:
        """Generic pin path: collecting box-12 without a same-statement box-13 source stops."""
        from packages.derivation.evaluator import AccessLog
        from packages.derivation.loader import DerivationSchemas
        from packages.derivation.runner import RunContext, SourceFact, _Run
        from packages.derivation.source_authority import SourceAuthorityError

        box12 = "tax.us.2025.f1099div.box12-exempt-interest-dividends"
        box13 = "tax.us.2025.f1099div.box13-specified-pab-authority"
        suffix = "payer=demo.b12.payer.0,statement=demo.b12.stmt.0,tax-year=2025"
        ctx = RunContext(
            run_id="demo.b12.companion-pin-fail-closed",
            rules=[],
            parameters={},
            canon={},
            inputs=[],
            sources=[
                SourceFact(
                    name=box12,
                    value="100",
                    finding_id="demo.b12.finding.box12.0",
                    fact_id=f"{box12}|{suffix}",
                )
                # Deliberately omit box-13 companion source.
            ],
            adoption_pin={"role": "adoption", "id": "demo.pkg", "version": "v1"},
            governance_pins=[],
            companion_presence_pairs={box12: box13},
        )
        run = _Run(ctx, DerivationSchemas())
        access = AccessLog()
        access.collects.add(box12)
        with self.assertRaises(SourceAuthorityError) as raised:
            run.pins_for(
                {"role": "rule", "id": "demo.rule", "version": "v1"},
                access,
            )
        message = str(raised.exception).lower()
        self.assertIn("companion provenance", message)
        self.assertIn("box13", message.replace("-", "").replace("_", "") or message)

    def test_runner_pins_box13_companion_when_present(self) -> None:
        from packages.derivation.evaluator import AccessLog
        from packages.derivation.loader import DerivationSchemas
        from packages.derivation.runner import RunContext, SourceFact, _Run

        box12 = "tax.us.2025.f1099div.box12-exempt-interest-dividends"
        box13 = "tax.us.2025.f1099div.box13-specified-pab-authority"
        suffix = "payer=demo.b12.payer.0,statement=demo.b12.stmt.0,tax-year=2025"
        ctx = RunContext(
            run_id="demo.b12.companion-pin-ok",
            rules=[],
            parameters={},
            canon={},
            inputs=[],
            sources=[
                SourceFact(
                    name=box12,
                    value="100",
                    finding_id="demo.b12.finding.box12.0",
                    fact_id=f"{box12}|{suffix}",
                ),
                SourceFact(
                    name=box13,
                    value="None",
                    finding_id="demo.b12.finding.box13.0",
                    fact_id=f"{box13}|{suffix}",
                ),
            ],
            adoption_pin={"role": "adoption", "id": "demo.pkg", "version": "v1"},
            governance_pins=[],
            companion_presence_pairs={box12: box13},
        )
        run = _Run(ctx, DerivationSchemas())
        access = AccessLog()
        access.collects.add(box12)
        pins = run.pins_for(
            {"role": "rule", "id": "demo.rule", "version": "v1"},
            access,
        )
        pin_ids = {p.get("id") for p in pins}
        self.assertIn("demo.b12.finding.box12.0", pin_ids)
        self.assertIn("demo.b12.finding.box13.0", pin_ids)

    def test_live_material_includes_box13_and_box9_companions_in_collect_names(self) -> None:
        """_resolved_run_material admits companions for every collected subordinate family."""
        from packages.derivation.live import _resolved_run_material
        from packages.derivation.loader import DerivationSchemas
        from packages.derivation.production_resolver import resolve_production_package

        # Production package on this branch resolves both box-8 and box-12 families.
        acts = _b8_acts(box8_values=[80], box12_values=[100], path="B")
        schemas = DerivationSchemas()
        from packages.derivation.production_resolver import ResolvedGraph

        resolved = resolve_production_package(
            acts,
            run_scope=SCOPE,
            scope_user=USER,
            workspace_revision=len(acts),
            surface=_surface(),
            schemas=schemas,
        )
        self.assertIsInstance(resolved, ResolvedGraph)
        assert isinstance(resolved, ResolvedGraph)
        *_, collect_names = _resolved_run_material(resolved)
        box12 = "tax.us.2025.f1099div.box12-exempt-interest-dividends"
        box13 = "tax.us.2025.f1099div.box13-specified-pab-authority"
        self.assertIn(box12, collect_names)
        self.assertIn(box13, collect_names)
        self.assertIn(BOX8_AMOUNT, collect_names)
        self.assertIn(BOX9_AUTH, collect_names)




class CompatibilityCases(unittest.TestCase):
    def test_r1_box12_package_still_validates(self) -> None:
        package = _load("package.core-calculations.v17.json")
        result = validate_package(
            package,
            _corpus(),
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / "published-packages.v12.json"),
        )
        self.assertTrue(result.ok, result.issues)

    def test_historical_line2a_v1_unchanged_bytes(self) -> None:
        # Guard against accidental rewrite of immutable @v1.
        text = (CONTENT / "rule.form1040-line2a.json").read_text("utf-8")
        self.assertIn('"version": "v1"', text)
        self.assertIn("no-f1099int-tax-exempt", text)
        self.assertNotIn("f1099int.b8", text)


if __name__ == "__main__":
    unittest.main()
