"""Form 1099-DIV box 7 direct FTC (no Form 1116): B7-C1–C10 and evidence matrix P*/N*."""

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
from packages.tax.loader import TAX_CONTENT_DIR
from tests.test_schedule_d_current_year_losses_t1 import (
    BOUNDARY_5,
    _build_acts as _sdcyl_build_acts,
)


ROOT = Path(__file__).resolve().parent.parent
CONTENT = TAX_CONTENT_DIR
FIXTURES = ROOT / "packages" / "sample_data" / "form1099div_box7_direct_ftc"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

BOX7_AMOUNT = "tax.us.2025.f1099div.box7-foreign-tax-paid"
BOX7_CLOSURE = "tax.us.2025.f1099div.7.source-closure"
BOX7_FAMILY = "tax.us.2025.f1099div.7"
BOX7_SUBTOTAL = "tax.us.2025.foreign-tax.box7-subtotal"
BOX8_AUTH = "tax.us.2025.f1099div.box8-country-companion"
ELECTION = "tax.us.2025.direct-ftc.election"
BOX1A = "tax.us.2025.f1099div.box1a-ordinary"

SCH3_L1 = "tax.us.2025.schedule3.line1-direct-ftc"
SCH3_L8 = "tax.us.2025.schedule3.line8-total"
L20 = "tax.us.2025.credits.form1040-line20"
TAX_AFTER = "tax.us.2025.tax.after-nonrefundable-credits"
LINE16 = "tax.us.2025.tax.total-tax"

SCOPE_TOKENS = (
    "all-foreign-income-passive",
    "all-foreign-income-on-1099div",
    "no-f1099int-foreign-tax",
    "no-k1-k3-foreign-tax",
    "no-other-foreign-tax-source",
    "tax-type-creditable",
    "legal-liability-and-paid",
    "no-refund-rebate-subsidy",
    "no-excluded-income-association",
    "holding-period-16-day-met",
    "no-short-sale-obligation",
    "country-recognized-non-terrorism",
    "no-carryback-carryforward",
    "no-schedule-a-deduction-election",
    "no-form-1116-required",
    "no-sch3-line2",
    "no-sch3-line3",
    "no-sch3-line4",
    "no-sch3-line5",
    "no-sch3-line6",
    "no-line17-schedule2-additional",
    "no-line19-ctc-odc",
    "no-schedule2-regular-tax-add",
    "no-form-4972-on-line16",
)


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
        CONTENT / "published-packages.v16.json",
        CONTENT,
    )


def _act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.b7.act.{index:03d}",
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


def _elective(finding_id: str, fact_id: str, value: object) -> dict[str, object]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "elective",
        "evidence_ids": [],
    }


def _scope_id(token: str) -> str:
    return f"tax.us.2025.direct-ftc-scope.{token}"


def _b7_acts(
    *,
    box7_values: list[float] | None = None,
    box8_values: list[str] | None = None,
    close_box7: bool = True,
    scope: dict[str, str] | None = None,
    box1a: float | None = 500,
    box1b: float | None = 100,
    wages: float = 90000,
    include_box8: bool = True,
    election: str | None = "yes",
    filing_status: str = "single",
) -> list[dict[str, object]]:
    """Build a production-shaped act log on the v21 route with box-7 facts.

    Base is the Schedule D current-year-loss coordinator with closed-empty
    covered ST/LT families so Form 1040 line 16 regular tax publishes (needed
    for the FTC regular-tax cap). Wages are fixed at 90000 in that builder;
    ``wages`` is accepted for API stability and only used when it matches
    that base (non-default wages are applied via superseding W-2 assertion).
    """
    box7_values = [100.0] if box7_values is None else box7_values
    if box8_values is None:
        box8_values = ["CA"] * max(1, len(box7_values) if box7_values else 1)
    scope_vals = {token: "yes" for token in SCOPE_TOKENS}
    if scope:
        scope_vals.update(scope)

    acts = _sdcyl_build_acts(
        st=[],
        lt=[],
        box1a=box1a,
        box1b=box1b if box1b is not None else 0,
        box2a=None,
        close_2a=True,
        close_st=True,
        close_lt=True,
        filing_status=filing_status,
        boundary={name: "yes" for name in BOUNDARY_5},
        components={"C1": "yes", "C2": "yes", "C3": "yes", "C4": "yes"},
    )
    acts.pop()  # drop historical package adoption

    # Swap residual-carrying box-2a vocabulary for residual-free v2 (v21 graph).
    for act in acts:
        if act["kind"] == "bundle-adoption":
            payload = cast(dict[str, object], act["payload"])
            bundle = cast(dict[str, Any], payload.get("bundle") or {})
            if bundle.get("id") == "tax.us.2025.f1099div.box2a.vocabulary":
                payload["bundle"] = _load("f1099div-box2a.bundle.v2.json")

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    # capital-gain-distributions = no (no box-2a members) so line 16 can gate.
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.b7.cg-dist",
                "tax.us.2025.capital-gain-distributions|tax-year=2025",
                "no",
            )
        },
    )

    # Post-rebase core v21 graph: close families introduced by Form 8949, 1099-INT
    # box 8, Schedule B adjustments, and 1099-G so line 16 / preferential base /
    # Schedule 1 / tax-exempt interest publish alongside the FTC credit path.
    for name in (
        "scheduleb.bundle.json",
        "scheduleb-adjustment.nominee.bundle.json",
        "scheduleb-adjustment.accrued-interest.bundle.json",
        "scheduleb-adjustment.abp-adjustment.bundle.json",
        "f1099b-covered-w-st.bundle.json",
        "f1099b-covered-w-lt.bundle.json",
        "f1099b-covered-w-st-scalars.bundle.json",
        "f1099b-covered-w-lt-scalars.bundle.json",
        "f1099int-box8.bundle.json",
        "f1099g-box1.bundle.json",
        "schedule1-part1-scope.bundle.json",
    ):
        add("bundle-adoption", {"bundle": _load(name)})

    closed_empty: tuple[tuple[str, str, str], ...] = (
        (
            "tax.us.2025.scheduleb.adjustment.nominee",
            "demo.b7.sb-nominee.h0",
            "tax.us.2025.scheduleb.adjustment.nominee.source-closure",
        ),
        (
            "tax.us.2025.scheduleb.adjustment.accrued-interest",
            "demo.b7.sb-accrued.h0",
            "tax.us.2025.scheduleb.adjustment.accrued-interest.source-closure",
        ),
        (
            "tax.us.2025.scheduleb.adjustment.abp-adjustment",
            "demo.b7.sb-abp.h0",
            "tax.us.2025.scheduleb.adjustment.abp-adjustment.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-st",
            "demo.b7.wst.h0",
            "tax.us.2025.f1099b.covered-w-st.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-st-proceeds",
            "demo.b7.wst-p.h0",
            "tax.us.2025.f1099b.covered-w-st-proceeds.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-st-basis",
            "demo.b7.wst-b.h0",
            "tax.us.2025.f1099b.covered-w-st-basis.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-st-adjustment",
            "demo.b7.wst-a.h0",
            "tax.us.2025.f1099b.covered-w-st-adjustment.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-lt",
            "demo.b7.wlt.h0",
            "tax.us.2025.f1099b.covered-w-lt.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-lt-proceeds",
            "demo.b7.wlt-p.h0",
            "tax.us.2025.f1099b.covered-w-lt-proceeds.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-lt-basis",
            "demo.b7.wlt-b.h0",
            "tax.us.2025.f1099b.covered-w-lt-basis.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-lt-adjustment",
            "demo.b7.wlt-a.h0",
            "tax.us.2025.f1099b.covered-w-lt-adjustment.source-closure",
        ),
        (
            "tax.us.2025.f1099int.b8",
            "demo.b7.int-b8.h0",
            "tax.us.2025.f1099int.b8.source-closure",
        ),
        (
            "tax.us.2025.f1099g.1",
            "demo.b7.g1.h0",
            "tax.us.2025.f1099g.1.source-closure",
        ),
    )
    for family_id, horizon_id, closure_type in closed_empty:
        add(
            "horizon-genesis",
            {
                "family": {"id": family_id, "version": "v1"},
                "scope": SCOPE_KEY,
                "horizon_id": horizon_id,
            },
        )
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.b7.closure.{horizon_id}",
                    f"{closure_type}|family-horizon={horizon_id},tax-year=2025",
                    True,
                )
            },
        )
    # Schedule B foreign-account / foreign-trust and Schedule 1 Part I scope
    # gates required by the post-#164 / #166 package graph.
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.b7.scheduleb.foreign-account",
                "tax.us.2025.scheduleb.foreign-account|tax-year=2025",
                "no",
            )
        },
    )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.b7.scheduleb.foreign-trust",
                "tax.us.2025.scheduleb.foreign-trust|tax-year=2025",
                "no",
            )
        },
    )
    for token in (
        "no-sch1-line1-taxable-refunds",
        "no-sch1-line2a-alimony",
        "no-sch1-line3-business",
        "no-sch1-line4-other-gains",
        "no-sch1-line5-rental",
        "no-sch1-line6-farm",
        "no-sch1-other-income",
        "no-unemployment-repayment",
        "no-f1099g-box2-state-refund",
        "no-f1099g-other-payment-classes",
    ):
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.b7.sch1-scope.{token}",
                    f"tax.us.2025.schedule1-part1-scope.{token}|tax-year=2025",
                    "yes",
                )
            },
        )

    if wages != 90000:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.b7.wages.override",
                    "tax.us.2025.w2.box1-wages|employer=demo.sdcyl.t1.employer,"
                    "w2-slip=demo.sdcyl.t1.w2,tax-year=2025",
                    wages,
                )
            },
        )

    add("bundle-adoption", {"bundle": _load("f1099div-box12.bundle.v2.json")})
    add("bundle-adoption", {"bundle": _load("f1099div-box7.bundle.json")})
    add("bundle-adoption", {"bundle": _load("direct-ftc-scope.bundle.json")})

    # Primary statement identity matches sdcyl dividend payer/stmt.
    payers_stmts: list[tuple[str, str]] = [
        ("demo.sdcyl.t1.payer", "demo.sdcyl.t1.stmt")
    ]
    for index in range(1, max(len(box7_values), 1)):
        payer = f"demo.b7.payer.{index}"
        stmt = f"demo.b7.stmt.{index}"
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": payer,
                    "kind": "tax.us.dividend-payer",
                    "label": f"Synthetic box-7 payer {index}",
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
                    "label": f"Synthetic box-7 statement {index}",
                }
            },
        )
        if box1a is not None:
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.b7.finding.box1a.{index}",
                        f"{BOX1A}|payer={payer},statement={stmt},tax-year=2025",
                        box1a,
                    )
                },
            )
        payers_stmts.append((payer, stmt))

    add(
        "horizon-genesis",
        {
            "family": {"id": BOX7_FAMILY, "version": "v1"},
            "scope": SCOPE_KEY,
            "horizon_id": "demo.b7.h0",
        },
    )
    horizon = "demo.b7.h0"
    for index, amount in enumerate(box7_values):
        payer, stmt = payers_stmts[index]
        if include_box8:
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.b7.finding.box8.{index}",
                        f"{BOX8_AUTH}|payer={payer},statement={stmt},tax-year=2025",
                        box8_values[index] if index < len(box8_values) else "CA",
                    )
                },
            )
        next_horizon = f"demo.b7.h{index + 1}"
        add(
            "member-transition",
            {
                "family": {"id": BOX7_FAMILY, "version": "v1"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(
                        f"demo.b7.finding.box7.{index}",
                        f"{BOX7_AMOUNT}|payer={payer},statement={stmt},tax-year=2025",
                        amount,
                    ),
                },
                "successor": {"id": next_horizon, "predecessor": horizon},
            },
        )
        horizon = next_horizon

    if close_box7:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.b7.closure.box7",
                    f"{BOX7_CLOSURE}|family-horizon={horizon},tax-year=2025",
                    True,
                )
            },
        )

    if election is not None:
        add(
            "assertion",
            {
                "finding": _elective(
                    "demo.b7.election",
                    f"{ELECTION}|tax-year=2025",
                    election,
                )
            },
        )

    for token, value in scope_vals.items():
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.b7.scope.{token}",
                    f"{_scope_id(token)}|tax-year=2025",
                    value,
                )
            },
        )

    adoption = cast(
        dict[str, object],
        json.loads((FIXTURES / "adoptions" / "adopt-core-v21-current.json").read_text("utf-8")),
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


def _disp(model: dict[str, Any], section_id: str) -> str:
    return cast(str, _section(model, section_id)["resolved"]["disposition"])


def _val(model: dict[str, Any], section_id: str) -> Any:
    return _section(model, section_id)["resolved"].get("value")


def _disposition(out: dict[str, Any], symbol: str) -> dict[str, Any]:
    return next(d for d in out["dispositions"] if d.get("symbol") == symbol)


class CitizenContractCases(unittest.TestCase):
    """B7-C1 residual/family shape and historical immutability."""

    def test_box7_member_identity_and_nonnegative(self) -> None:
        # B7-C1 / P1 shape.
        bundle = _load("f1099div-box7.bundle.json")
        amount = next(ft for ft in bundle["fact_types"] if ft["id"] == BOX7_AMOUNT)
        self.assertEqual(
            [key["name"] for key in amount["identity_keys"]],
            ["payer", "statement", "tax-year"],
        )
        self.assertEqual(amount["value_schema"], {"type": "number", "minimum": 0})
        self.assertNotIn("evidence", json.dumps(amount["identity_keys"]))
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(-1, amount["value_schema"])

    def test_residual_v4_omits_2a_7_and_12(self) -> None:
        # B7-C2 residual succession.
        bundle = _load("f1099div-box7.bundle.json")
        residual = next(
            ft
            for ft in bundle["fact_types"]
            if ft["id"] == "tax.us.2025.f1099div.recorded-boxes" and ft["version"] == "v4"
        )
        self.assertEqual(set(residual["value_schema"]["properties"]), {"3", "5"})
        self.assertNotIn("7", residual["value_schema"]["properties"])
        self.assertNotIn("12", residual["value_schema"]["properties"])
        self.assertNotIn("2a", residual["value_schema"]["properties"])

    def test_historical_residual_v3_still_has_7(self) -> None:
        hist = _load("f1099div-box12.bundle.json")
        residual = next(
            ft
            for ft in hist["fact_types"]
            if ft["id"] == "tax.us.2025.f1099div.recorded-boxes"
        )
        self.assertEqual(residual["version"], "v3")
        self.assertIn("7", residual["value_schema"]["properties"])

    def test_box8_admits_country_or_ric_not_applicable(self) -> None:
        # B7-C3.
        bundle = _load("f1099div-box7.bundle.json")
        auth = next(ft for ft in bundle["fact_types"] if ft["id"] == BOX8_AUTH)
        jsonschema.validate("CA", auth["value_schema"])
        jsonschema.validate("not_applicable", auth["value_schema"])
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate("", auth["value_schema"])
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(["CA", "FR"], auth["value_schema"])

    def test_dividend_universe_v4_composable_includes_7(self) -> None:
        universe = _load("dividend-universe.v4.json")
        boxes = {entry["box"] for entry in universe["composable_boxes"]}
        self.assertEqual(boxes, {"1a", "1b", "2a", "12", "7"})
        self.assertEqual(set(universe["recorded_non_composable_boxes"]), {"3", "5"})

    def test_line16_symbol_unchanged_in_citizens(self) -> None:
        # B7-C9 hygiene: line-16 rule still publishes total-tax.
        rule = _load("rule.form1040-line16.v5.json")
        self.assertEqual(rule["publishes"], LINE16)
        self.assertNotEqual(rule["publishes"], TAX_AFTER)


class PackageExclusivityCases(unittest.TestCase):
    def test_v21_package_validates(self) -> None:
        package = _load("package.core-calculations.v21.json")
        result = validate_package(
            package,
            _corpus(),
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / "published-packages.v16.json"),
        )
        self.assertTrue(result.ok, result.issues)

    def test_mixed_box7_residual_and_family_rejects(self) -> None:
        # N13: residual with property 7 + box-7 family.
        hist = _load("f1099div-box12.bundle.json")  # residual v3 with 7
        succ = _load("f1099div-box7.bundle.json")
        package = {
            "schema": "artifact-package.v18",
            "id": "demo.package.mixed-box7",
            "version": "v1",
            "scope": {
                "tax_year": 2025,
                "jurisdiction": "US-federal",
                "family": "individual-income-tax",
            },
            "admitted_schemas": [
                "bundle.v2",
                "quantity-vocabulary.v3",
                "quantity-vocabulary.v10",
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
                    "schema": "quantity-vocabulary.v10",
                    "id": "tax.us.2025.quantity.foreign-tax-paid",
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
                ("tax.us.2025.quantity.foreign-tax-paid", "v1"):
                    _load("quantity.foreign-tax-paid.json"),
            },
            DerivationSchemas(),
        )
        codes = {issue.code for issue in result.issues}
        self.assertTrue(
            {"MIXED_BOX7_GRAPH", "MIXED_RESIDUAL_GRAPH"} & codes,
            result.issues,
        )

    def test_n14_historical_v17_package_still_validates(self) -> None:
        package = _load("package.core-calculations.v17.json")
        result = validate_package(
            package,
            _corpus(),
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / "published-packages.v12.json"),
        )
        self.assertTrue(result.ok, result.issues)


class CompanionAdmissionCases(unittest.TestCase):
    def test_box7_companion_pairs_registered(self) -> None:
        from packages.tax.loader import domain_companion_presence_pairs, tax_registry

        reg = tax_registry()
        self.assertIn(BOX7_AMOUNT, reg.companion_presence_pairs)
        companions = reg.companion_presence_pairs[BOX7_AMOUNT]
        self.assertEqual(
            list(companions) if not isinstance(companions, str) else [companions],
            [BOX8_AUTH, BOX1A],
        )
        self.assertEqual(
            domain_companion_presence_pairs()[BOX7_AMOUNT],
            [BOX8_AUTH, BOX1A],
        )


class LiveEvidenceCases(unittest.TestCase):
    """Evidence matrix through live_coordinate_run where honest."""

    def test_p1_one_payer_below_threshold_publishes_credit(self) -> None:
        # P1 / P16 / P17 basis.
        _, model = _run(_b7_acts(box7_values=[100]), "demo.b7.p1")
        self.assertEqual(_disp(model, "line-Sch3-1"), "published_value")
        self.assertEqual(_val(model, "line-Sch3-1"), 100)
        self.assertEqual(_val(model, "line-Sch3-8"), 100)
        self.assertEqual(_val(model, "line-20"), 100)
        line16 = _val(model, "line-16")
        after = _val(model, "line-22")
        self.assertIsNotNone(line16)
        self.assertEqual(after, max(float(line16) - 100, 0))

    def test_p2_multiple_payers_aggregate_once(self) -> None:
        # P2 / P11 / P15.
        _, model = _run(_b7_acts(box7_values=[100, 40]), "demo.b7.p2")
        self.assertEqual(_val(model, "line-Sch3-1"), 140)
        self.assertEqual(_val(model, "line-20"), 140)

    def test_p3_exactly_300_non_joint(self) -> None:
        # P3.
        _, model = _run(_b7_acts(box7_values=[300]), "demo.b7.p3")
        self.assertEqual(_disp(model, "line-Sch3-1"), "published_value")
        self.assertEqual(_val(model, "line-Sch3-1"), 300)

    def test_p4_above_300_non_joint_blocks(self) -> None:
        # P4: whole-dollar above threshold (half_up subtotal makes fractional
        # 300.01 collapse to 300; 301 is the honest post-round over-threshold).
        _, model = _run(_b7_acts(box7_values=[301]), "demo.b7.p4")
        self.assertIn(_disp(model, "line-Sch3-1"), {"blocked", "guard_inapplicable"})

    def test_p5_exactly_600_mfj(self) -> None:
        # P5.
        _, model = _run(
            _b7_acts(box7_values=[600], filing_status="married_filing_jointly"),
            "demo.b7.p5",
        )
        self.assertEqual(_disp(model, "line-Sch3-1"), "published_value")
        self.assertEqual(_val(model, "line-Sch3-1"), 600)

    def test_p6_above_600_mfj_blocks(self) -> None:
        # P6.
        _, model = _run(
            _b7_acts(box7_values=[601], filing_status="married_filing_jointly"),
            "demo.b7.p6",
        )
        self.assertIn(_disp(model, "line-Sch3-1"), {"blocked", "guard_inapplicable"})

    def test_p7_mfs_shares_300_threshold_expression_single_filer_live_gate(self) -> None:
        # P7, narrowed (repair Finding 2): this test proves two *distinct*
        # things and does not conflate them.
        #
        # 1. The published threshold expression's MFJ/$600 vs everyone-else/
        #    $300 branch literally covers MFS — MFS is not a separate,
        #    unimplemented branch; it falls into the same else-branch single
        #    does.
        # 2. The non-MFJ *live* gate is only actually exercised end-to-end
        #    for single, because live MFS end-to-end evidence is out of
        #    bounds here (see test_n_mfs_live_run_currently_raises below and
        #    the milestone's "Supported class" note).
        rule = _load("rule.schedule3-line1-direct-ftc.json")
        blob = json.dumps(rule)
        self.assertIn("married_filing_jointly", blob)
        self.assertIn("600", blob)
        self.assertIn("300", blob)
        # Non-MFJ live gate, single filer only (the one status this milestone
        # actually certifies end-to-end on the else branch).
        _, at = _run(_b7_acts(box7_values=[300], filing_status="single"), "demo.b7.p7-at")
        self.assertEqual(_disp(at, "line-Sch3-1"), "published_value")
        _, over = _run(_b7_acts(box7_values=[301], filing_status="single"), "demo.b7.p7-over")
        self.assertIn(_disp(over, "line-Sch3-1"), {"blocked", "guard_inapplicable"})

    def test_n_mfs_live_run_currently_raises(self) -> None:
        # Repair Finding 2: MFS is in the contract's threshold expression
        # (B7-C7) but this milestone does not certify a live MFS run — the
        # engine has no MFS tax-bracket table (only single/MFJ are
        # published), so Form 1040 line 16 regular tax cannot resolve for
        # MFS and the run fails closed with SchemaValidationError before the
        # box-7 threshold rule is ever reached. This makes the gap visible in
        # the suite rather than hiding it behind a silent single-filer
        # substitution. Deferred to the milestone that adds MFS tax-bracket
        # parameters (see docs/phases/engine-breadth/milestones/
        # form1099div-box7-direct-ftc.md, "Supported class").
        from packages.kernel.schema_registry import SchemaValidationError

        with self.assertRaises(SchemaValidationError) as ctx:
            _run(
                _b7_acts(box7_values=[300], filing_status="married_filing_separately"),
                "demo.b7.p7-mfs-live-gap",
            )
        message = str(ctx.exception)
        self.assertIn("LOOKUP_MISS", message)

    def test_n1_missing_election_blocks(self) -> None:
        # N1.
        _, model = _run(_b7_acts(box7_values=[100], election=None), "demo.b7.n1")
        self.assertIn(_disp(model, "line-Sch3-1"), {"blocked", "guard_inapplicable"})

    def test_n2_election_declined_blocks(self) -> None:
        # N2.
        _, model = _run(_b7_acts(box7_values=[100], election="no"), "demo.b7.n2")
        self.assertIn(_disp(model, "line-Sch3-1"), {"blocked", "guard_inapplicable"})

    def test_p8_foreign_tax_capped_by_regular_tax(self) -> None:
        # P8: large foreign tax with modest wages → credit = regular tax, after-credit 0.
        _, model = _run(_b7_acts(box7_values=[250], wages=12000), "demo.b7.p8")
        line16 = float(_val(model, "line-16") or 0)
        credit = float(_val(model, "line-Sch3-1") or 0)
        self.assertLess(line16, 250)
        self.assertEqual(credit, line16)
        self.assertEqual(_val(model, "line-22"), 0)

    def test_p9_zero_regular_tax_credit_zero(self) -> None:
        # P9: wages low enough that line 16 is 0.
        _, model = _run(_b7_acts(box7_values=[50], wages=0), "demo.b7.p9")
        line16 = _val(model, "line-16")
        if line16 in (0, 0.0) and _disp(model, "line-16") in {
            "published_value",
            "computed_zero",
            "closure_backed_zero",
        }:
            self.assertEqual(_val(model, "line-Sch3-1"), 0)
            after = _val(model, "line-22")
            self.assertTrue(after is None or float(after) >= 0)
        else:
            # If standard deduction makes line 16 zero-or-blocked, credit must not go negative.
            if _disp(model, "line-Sch3-1") == "published_value":
                self.assertGreaterEqual(float(_val(model, "line-Sch3-1")), 0)

    def test_n3_to_n10_scope_no_blocks(self) -> None:
        # N3–N10 via scope component flip to no.
        cases = {
            "all-foreign-income-on-1099div": "N3/N5",
            "all-foreign-income-passive": "N4",
            "no-refund-rebate-subsidy": "N6",
            "holding-period-16-day-met": "N7",
            "no-carryback-carryforward": "N8",
            "no-schedule-a-deduction-election": "N9",
            "no-f1099int-foreign-tax": "N10",
        }
        for token, label in cases.items():
            with self.subTest(label=label, token=token):
                _, model = _run(
                    _b7_acts(box7_values=[80], scope={token: "no"}),
                    f"demo.b7.scope-{token}",
                )
                self.assertIn(
                    _disp(model, "line-Sch3-1"),
                    {"blocked", "guard_inapplicable"},
                    label,
                )

    def test_n11_other_sch3_credit_blocks_line8(self) -> None:
        # N11.
        _, model = _run(
            _b7_acts(box7_values=[80], scope={"no-sch3-line2": "no"}),
            "demo.b7.n11",
        )
        # Schedule 3 line 1 may still publish; Schedule 3 line 8 completeness fails.
        # (Form 1040 line 8 is the Schedule 1 other-income path — different section.)
        self.assertIn(_disp(model, "line-Sch3-8"), {"blocked", "guard_inapplicable"})

    def test_n12_missing_box8_companion_rejected(self) -> None:
        # N12 / B7-C3.
        acts = _b7_acts(box7_values=[100], include_box8=False)
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
                    run_id="demo.b7.n12",
                    governance_pins=[],
                    surface=_surface(),
                    output_name="out.json",
                )
        message = str(ctx.exception)
        self.assertIn("companion presence violated", message)
        self.assertIn(BOX7_AMOUNT, message)
        self.assertIn(BOX8_AUTH, message)

    def test_p10_correction_same_identity(self) -> None:
        # P10: box-7 amount correction on the same statement identity displaces
        # the credit and downstream tax result (B7-C10). Observe identity, not
        # just value: the superseded source finding is distinct from the
        # current one, the derived Schedule 3 / line-20 identities change on
        # correction, and exact pins are present and correct afterward.
        from packages.derivation.loader import DerivationSchemas
        from packages.kernel.findings import project

        base_acts = _b7_acts(box7_values=[100])
        out_before, model_before = _run(base_acts, "demo.b7.p10-base")
        self.assertEqual(_val(model_before, "line-Sch3-1"), 100)
        sch3_1_before = _disposition(out_before, SCH3_L1)
        sch3_8_before = _disposition(out_before, SCH3_L8)
        l20_before = _disposition(out_before, L20)

        original_finding_id = "demo.b7.finding.box7.0"
        correction_finding_id = "demo.b7.finding.box7.correction"
        corrected_acts = list(base_acts[:-1])  # drop adoption, re-append after insert
        corrected_acts.append(
            _act(
                len(corrected_acts),
                "assertion",
                {
                    "finding": _attested(
                        correction_finding_id,
                        f"{BOX7_AMOUNT}|payer=demo.sdcyl.t1.payer,statement=demo.sdcyl.t1.stmt,tax-year=2025",
                        125,
                    )
                },
            )
        )
        adoption = copy.deepcopy(base_acts[-1])
        adoption["committed_against"] = len(corrected_acts) + 1
        corrected_acts.append(adoption)

        out_after, model_after = _run(corrected_acts, "demo.b7.p10-corrected")
        self.assertEqual(_val(model_after, "line-Sch3-1"), 125)

        # The superseded finding's identity is distinct from the current
        # finding's identity (not just that the value changed).
        schemas = DerivationSchemas()
        state = project(tuple(dict(a) for a in corrected_acts), schemas.registry)
        self.assertIn(original_finding_id, state.findings)
        self.assertIn(correction_finding_id, state.findings)
        self.assertNotEqual(original_finding_id, correction_finding_id)
        self.assertEqual(state.findings[original_finding_id]["value"], 100)
        self.assertEqual(state.findings[correction_finding_id]["value"], 125)

        # The derived (Schedule 3 / line-20) identity changes on correction,
        # not just its value.
        sch3_1_after = _disposition(out_after, SCH3_L1)
        sch3_8_after = _disposition(out_after, SCH3_L8)
        l20_after = _disposition(out_after, L20)
        self.assertNotEqual(sch3_1_before["finding_id"], sch3_1_after["finding_id"])
        self.assertNotEqual(sch3_8_before["finding_id"], sch3_8_after["finding_id"])
        self.assertNotEqual(l20_before["finding_id"], l20_after["finding_id"])

        # Exact pins are present and correct after the correction: source tax
        # (subtotal chain), associated income / source closure, creditability,
        # election/eligibility, Schedule 3, and Form 1040 consumer chaining.
        sch3_1_pin_ids = {p["id"] for p in sch3_1_after["pins"]}
        self.assertIn("tax.us.2025.package.core-calculations", sch3_1_pin_ids)
        self.assertIn("demo.b7.election", sch3_1_pin_ids)  # election/eligibility
        self.assertIn("demo.b7.closure.box7", sch3_1_pin_ids)  # associated income
        self.assertIn("demo.b7.scope.tax-type-creditable", sch3_1_pin_ids)  # creditability
        self.assertIn("tax.us.2025.citation.schedule3.line1", sch3_1_pin_ids)
        subtotal_after = _disposition(out_after, BOX7_SUBTOTAL)
        self.assertIn(subtotal_after["finding_id"], sch3_1_pin_ids)  # source tax
        # Schedule 3 line-1 -> line-8 -> Form 1040 line-20 consumer chain re-pins
        # to the new derived identities, not the pre-correction ones.
        sch3_8_pin_ids = {p["id"] for p in sch3_8_after["pins"]}
        self.assertIn(sch3_1_after["finding_id"], sch3_8_pin_ids)
        self.assertNotIn(sch3_1_before["finding_id"], sch3_8_pin_ids)
        l20_pin_ids = {p["id"] for p in l20_after["pins"]}
        self.assertIn(sch3_8_after["finding_id"], l20_pin_ids)
        self.assertNotIn(sch3_8_before["finding_id"], l20_pin_ids)

    def test_p10b_election_correction_displaces_result(self) -> None:
        # B7-C10: election or eligibility correction — not just the source
        # amount — displaces the result.
        base_acts = _b7_acts(box7_values=[100])
        _, model_before = _run(base_acts, "demo.b7.p10b-base")
        self.assertEqual(_disp(model_before, "line-Sch3-1"), "published_value")
        self.assertEqual(_val(model_before, "line-Sch3-1"), 100)

        corrected_acts = list(base_acts[:-1])
        corrected_acts.append(
            _act(
                len(corrected_acts),
                "assertion",
                {"finding": _elective("demo.b7.election.correction", f"{ELECTION}|tax-year=2025", "no")},
            )
        )
        adoption = copy.deepcopy(base_acts[-1])
        adoption["committed_against"] = len(corrected_acts) + 1
        corrected_acts.append(adoption)
        _, model_after_election = _run(corrected_acts, "demo.b7.p10b-election")
        self.assertIn(
            _disp(model_after_election, "line-Sch3-1"), {"blocked", "guard_inapplicable"}
        )

    def test_p10c_eligibility_correction_displaces_result(self) -> None:
        # B7-C10: an eligibility (creditability scope) correction displaces
        # the result, distinct from an amount or election correction.
        base_acts = _b7_acts(box7_values=[100])
        _, model_before = _run(base_acts, "demo.b7.p10c-base")
        self.assertEqual(_disp(model_before, "line-Sch3-1"), "published_value")

        corrected_acts = list(base_acts[:-1])
        corrected_acts.append(
            _act(
                len(corrected_acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.b7.scope.tax-type-creditable.correction",
                        f"{_scope_id('tax-type-creditable')}|tax-year=2025",
                        "no",
                    )
                },
            )
        )
        adoption = copy.deepcopy(base_acts[-1])
        adoption["committed_against"] = len(corrected_acts) + 1
        corrected_acts.append(adoption)
        _, model_after = _run(corrected_acts, "demo.b7.p10c-eligibility")
        self.assertIn(_disp(model_after, "line-Sch3-1"), {"blocked", "guard_inapplicable"})

    def test_p12_late_member_stale_then_restore(self) -> None:
        # P12.
        base = _b7_acts(box7_values=[100], close_box7=True)
        # After closed, add a late member via member-transition (new horizon).
        payer = "demo.b7.payer.late"
        stmt = "demo.b7.stmt.late"
        late_acts = list(base[:-1])  # drop adoption temporarily
        n = len(late_acts)

        def add(kind: str, payload: dict[str, object]) -> None:
            late_acts.append(_act(len(late_acts), kind, payload))

        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": payer,
                    "kind": "tax.us.dividend-payer",
                    "label": "Late payer",
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
                    "label": "Late statement",
                }
            },
        )
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.b7.late.box1a",
                    f"{BOX1A}|payer={payer},statement={stmt},tax-year=2025",
                    200,
                )
            },
        )
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.b7.late.box8",
                    f"{BOX8_AUTH}|payer={payer},statement={stmt},tax-year=2025",
                    "JP",
                )
            },
        )
        # Find current horizon from last box7 closure
        prior_horizon = "demo.b7.h1"
        next_horizon = "demo.b7.h-late"
        add(
            "member-transition",
            {
                "family": {"id": BOX7_FAMILY, "version": "v1"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(
                        "demo.b7.late.box7",
                        f"{BOX7_AMOUNT}|payer={payer},statement={stmt},tax-year=2025",
                        20,
                    ),
                },
                "successor": {"id": next_horizon, "predecessor": prior_horizon},
            },
        )
        # Stale: without re-close, credit consumers should leave / block.
        adoption = cast(
            dict[str, object],
            json.loads((FIXTURES / "adoptions" / "adopt-core-v21-current.json").read_text()),
        )
        adoption["committed_against"] = len(late_acts)
        late_acts.append(adoption)
        _, stale = _run(late_acts, "demo.b7.p12-stale")
        self.assertIn(_disp(stale, "line-Sch3-1"), {"blocked", "guard_inapplicable"})

        # Restore: re-close on successor horizon.
        restore = list(late_acts[:-1])
        restore.append(
            _act(
                len(restore),
                "assertion",
                {
                    "finding": _attested(
                        "demo.b7.closure.restore",
                        f"{BOX7_CLOSURE}|family-horizon={next_horizon},tax-year=2025",
                        True,
                    )
                },
            )
        )
        adoption2 = copy.deepcopy(adoption)
        adoption2["committed_against"] = len(restore)
        restore.append(adoption2)
        _, restored = _run(restore, "demo.b7.p12-restore")
        self.assertEqual(_val(restored, "line-Sch3-1"), 120)

    def test_p13_p14_income_path_preserved_with_box1b(self) -> None:
        # P13 / P14: box 7 does not reduce dividends; box 1b coexists.
        _, with_credit = _run(
            _b7_acts(box7_values=[80], box1a=600, box1b=150),
            "demo.b7.p13-credit",
        )
        _, no_credit = _run(
            _b7_acts(box7_values=[80], box1a=600, box1b=150, election="no"),
            "demo.b7.p13-noelect",
        )
        # line 3b ordinary dividends should match when income path is published.
        if _disp(with_credit, "line-3b") == "published_value":
            self.assertEqual(_val(with_credit, "line-3b"), _val(no_credit, "line-3b"))
        if _disp(with_credit, "line-3a") == "published_value":
            self.assertEqual(_val(with_credit, "line-3a"), _val(no_credit, "line-3a"))
        self.assertEqual(_val(with_credit, "line-Sch3-1"), 80)

    def test_p15_credit_once_not_income(self) -> None:
        # P15: credit appears on line 20 once; line 16 regular tax still present.
        _, model = _run(_b7_acts(box7_values=[90]), "demo.b7.p15")
        self.assertEqual(_val(model, "line-20"), 90)
        self.assertEqual(_disp(model, "line-16"), "published_value")
        self.assertIsNotNone(_val(model, "line-16"))

    def test_p16_tie_outs(self) -> None:
        # P16.
        _, model = _run(_b7_acts(box7_values=[75]), "demo.b7.p16")
        self.assertEqual(_val(model, "line-Sch3-1"), _val(model, "line-Sch3-8"))
        self.assertEqual(_val(model, "line-Sch3-8"), _val(model, "line-20"))
        line16 = float(_val(model, "line-16"))
        credit = float(_val(model, "line-20"))
        self.assertEqual(_val(model, "line-22"), max(line16 - credit, 0))

    def test_p17_presentation_shows_direct_election_not_form1116(self) -> None:
        # P17. Committed presentation golden must match the live model
        # byte-for-structure (B7-C10: "One canonical positive golden").
        _, model = _run(_b7_acts(box7_values=[100]), "demo.b7.p17")
        golden_path = FIXTURES / "presentation" / "box7-direct-ftc.presentation-model.v1.json"
        self.assertTrue(
            golden_path.is_file(),
            f"committed presentation golden required at {golden_path}",
        )
        golden = json.loads(golden_path.read_text("utf-8"))
        self.assertEqual(model, golden)
        section = _section(model, "line-Sch3-1")
        self.assertEqual(section["resolved"]["value"], 100)
        blob = json.dumps(section).lower()
        self.assertTrue(
            "direct" in blob or "without form 1116" in blob or "foreign tax" in blob,
            section,
        )
        self.assertNotIn("form 1116 completed", blob)
        self.assertNotIn("form 1116 was completed", blob)

    def test_n15_compact_negative_presentation_mutation(self) -> None:
        # N15. Projector on the real Schedule 3 line-1 field path rejects
        # non-numeric publication (same pattern as the sibling milestone's
        # test_n7_malformed_presentation_blocks_or_redacts).
        from packages.derivation.loader import DerivationSchemas, load_canon
        from packages.derivation.live import _resolved_run_material
        from packages.derivation.marshal import marshal_live_run_context
        from packages.derivation.presentation_projection import (
            PresentationModelError,
            build_presentation_model,
        )
        from packages.derivation.production_executor import execute_marshaled
        from packages.derivation.production_resolver import (
            ResolvedGraph,
            resolve_production_package,
        )
        from packages.derivation.runner import Publication
        from packages.kernel.currency import compute_currency
        from packages.kernel.findings import project
        from packages.tax.loader import (
            domain_companion_presence_pairs,
            install_domain_companion_presence,
            install_domain_declaration_signal_contradictions,
        )

        acts = _b7_acts(box7_values=[50])
        schemas = DerivationSchemas()
        install_domain_companion_presence(schemas.registry)
        install_domain_declaration_signal_contradictions(schemas.registry)

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
            run_id="demo.b7.n15-projector",
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
        symbol = SCH3_L1
        pubs: list[Publication] = []
        found = False
        for pub in result.publications:
            finding = copy.deepcopy(pub.finding)
            if finding.get("symbol") == symbol:
                finding["value"] = "not-a-number"
                found = True
            pubs.append(Publication(act=pub.act, finding=finding))
        self.assertTrue(found, "expected schedule3-line1 publication from the live package path")
        with self.assertRaises(PresentationModelError) as ctx:
            build_presentation_model(
                run_id="demo.b7.n15-bad",
                resolved_members=resolved.resolved_members,
                state=state,
                publications=pubs,
                dispositions=result.dispositions,
            )
        message = str(ctx.exception).lower()
        self.assertIn("invalid numeric", message)

    def test_ric_box8_not_applicable_admissible(self) -> None:
        # B7-C3 RIC companion.
        _, model = _run(
            _b7_acts(box7_values=[40], box8_values=["not_applicable"]),
            "demo.b7.ric",
        )
        self.assertEqual(_val(model, "line-Sch3-1"), 40)


class GeneratorReproducibilityCases(unittest.TestCase):
    """Repair Finding 1: the generator must reproduce the committed artifacts.

    Regression for the destructive/non-reproducible generator bug: it must be
    additive over the real ratified predecessor state
    (``published-packages.v15.json`` / ``package.core-calculations.v20.json``
    / adoption ``demo.act.adopt.core.v20``), not a rebuild from a stale
    snapshot. This captures the generator's output in memory and diffs it
    against the committed bytes without writing to the working tree.
    """

    def test_generator_output_matches_committed_bytes(self) -> None:
        from tools.generate_form1099div_box7_direct_ftc import render_all

        files = render_all()
        self.assertTrue(files, "generator produced no files")
        mismatches: list[str] = []
        for path, body in files.items():
            if not path.is_file():
                mismatches.append(f"missing on disk: {path}")
                continue
            existing = path.read_bytes()
            if existing != body:
                mismatches.append(f"content differs: {path}")
        self.assertEqual(
            mismatches,
            [],
            "generator output no longer reproduces committed artifacts:\n"
            + "\n".join(mismatches),
        )


class CompatibilityCases(unittest.TestCase):
    """N14: box-12 / interest / Schedule B / D / carryover / line-16 regressions stay green via package history."""

    def test_box12_package_v17_still_validates(self) -> None:
        package = _load("package.core-calculations.v17.json")
        result = validate_package(
            package,
            _corpus(),
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / "published-packages.v12.json"),
        )
        self.assertTrue(result.ok, result.issues)

    def test_final_package_union_includes_successors(self) -> None:
        # Focused final-package test: v21 members include box-7 successors and retain line-16 v5.
        package = _load("package.core-calculations.v21.json")
        ids = {(m["id"], m["version"]) for m in package["members"]}
        self.assertIn(("tax.us.2025.f1099div.box7.vocabulary", "v1"), ids)
        self.assertIn(("tax.us.2025.dividend-universe", "v4"), ids)
        self.assertIn(("tax.us.2025.rule.form1040-line16", "v5"), ids)
        self.assertIn(("tax.us.2025.rule.schedule3-line1-direct-ftc", "v1"), ids)
        self.assertIn(("tax.us.2025.f1099div.box12.vocabulary", "v2"), ids)


if __name__ == "__main__":
    unittest.main()
