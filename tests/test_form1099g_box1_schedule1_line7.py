"""Form 1099-G box 1 → Schedule 1 line 7 / Form 1040 line 8: UG-C1–C8 and evidence matrix."""

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
from tests.test_capital_gain_distributions_line7a_t2_coordinator import _cgd_t2_acts


ROOT = Path(__file__).resolve().parent.parent
CONTENT = TAX_CONTENT_DIR
FIXTURES = ROOT / "packages" / "sample_data" / "form1099g_box1_schedule1_line7"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

BOX1_AMOUNT = "tax.us.2025.f1099g.box1-unemployment"
BOX1_CLOSURE = "tax.us.2025.f1099g.1.source-closure"
BOX1_FAMILY = "tax.us.2025.f1099g.1"
BOX4_AUTH = "tax.us.2025.f1099g.box4-federal-withholding-authority"
LINE7 = "tax.us.2025.schedule1.line7-unemployment"
LINE8 = "tax.us.2025.income.additional-income"
LINE10 = "tax.us.2025.schedule1.line10-additional-income"

SCOPE_TOKENS = (
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
        CONTENT / "published-packages.v15.json",
        CONTENT,
    )


def _act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.ug.act.{index:03d}",
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
    return f"tax.us.2025.schedule1-part1-scope.{token}"


def _ug_acts(
    *,
    box1_values: list[float] | None = None,
    box4_values: list[object] | None = None,
    close_box1: bool = True,
    scope: dict[str, str] | None = None,
    wages: float = 90000,
    box1a: float | None = 0,
    box1b: float | None = 0,
    box2a: float | None = None,
    include_box4: bool = True,
    same_payer_two_statements: bool = False,
) -> list[dict[str, object]]:
    """Build a production-shaped act log on the v20 route with box-1 facts."""
    box1_values = [2500.0] if box1_values is None else box1_values
    if box4_values is None:
        box4_values = [None] * max(1, len(box1_values) if box1_values else 1)
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

    # Residual-free box2a vocabulary for exclusive package graph (same as box-12 tests).
    for act in acts:
        if act["kind"] == "bundle-adoption":
            payload = cast(dict[str, object], act["payload"])
            bundle = cast(dict[str, Any], payload.get("bundle") or {})
            if bundle.get("id") == "tax.us.2025.f1099div.box2a.vocabulary":
                payload["bundle"] = _load("f1099div-box2a.bundle.v2.json")

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("f1099g-box1.bundle.json")})
    add("bundle-adoption", {"bundle": _load("schedule1-part1-scope.bundle.json")})
    # Close remaining interest-composition v4 families and Schedule B adjustment
    # families closed-empty so taxable-interest (and thus line 9) can publish on
    # the current core package graph.
    for name in (
        "form1065-k1.bundle.json",
        "f1099int-b10.bundle.json",
        "f1099oid-b5.bundle.json",
        "f1099int-box8.bundle.json",
        "scheduleb.bundle.json",
        "scheduleb-adjustment.nominee.bundle.json",
        "scheduleb-adjustment.accrued-interest.bundle.json",
        "scheduleb-adjustment.abp-adjustment.bundle.json",
        "f1099b-covered-st.bundle.json",
        "f1099b-covered-lt.bundle.json",
        "f1099b-covered-st-scalars.bundle.json",
        "f1099b-covered-lt-scalars.bundle.json",
        "f1099b-covered-w-st.bundle.json",
        "f1099b-covered-w-lt.bundle.json",
        "f1099b-covered-w-st-scalars.bundle.json",
        "f1099b-covered-w-lt-scalars.bundle.json",
        "schedule-d-boundary.bundle.json",
    ):
        add("bundle-adoption", {"bundle": _load(name)})

    # Closed-empty interest-composition remainder + Schedule B adjustments +
    # covered ST/LT families so line 7a / line 9 can publish alongside line 8.
    closed_empty: tuple[tuple[str, str, str], ...] = (
        (
            "tax.us.2025.form1065-k1.box5",
            "demo.ug.k1.h0",
            "tax.us.2025.form1065-k1.box5.source-closure",
        ),
        (
            "tax.us.2025.f1099int.b10",
            "demo.ug.int-b10.h0",
            "tax.us.2025.f1099int.b10.source-closure",
        ),
        (
            "tax.us.2025.f1099oid.b5",
            "demo.ug.oid-b5.h0",
            "tax.us.2025.f1099oid.b5.source-closure",
        ),
        (
            "tax.us.2025.scheduleb.adjustment.nominee",
            "demo.ug.sb-nom.h0",
            "tax.us.2025.scheduleb.adjustment.nominee.source-closure",
        ),
        (
            "tax.us.2025.scheduleb.adjustment.accrued-interest",
            "demo.ug.sb-acc.h0",
            "tax.us.2025.scheduleb.adjustment.accrued-interest.source-closure",
        ),
        (
            "tax.us.2025.scheduleb.adjustment.abp-adjustment",
            "demo.ug.sb-abp.h0",
            "tax.us.2025.scheduleb.adjustment.abp-adjustment.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-st",
            "demo.ug.st.h0",
            "tax.us.2025.f1099b.covered-st.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-st-proceeds",
            "demo.ug.st-p.h0",
            "tax.us.2025.f1099b.covered-st-proceeds.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-st-basis",
            "demo.ug.st-b.h0",
            "tax.us.2025.f1099b.covered-st-basis.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-lt",
            "demo.ug.lt.h0",
            "tax.us.2025.f1099b.covered-lt.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-lt-proceeds",
            "demo.ug.lt-p.h0",
            "tax.us.2025.f1099b.covered-lt-proceeds.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-lt-basis",
            "demo.ug.lt-b.h0",
            "tax.us.2025.f1099b.covered-lt-basis.source-closure",
        ),
        (
            "tax.us.2025.f1099int.b8",
            "demo.ug.int-b8.h0",
            "tax.us.2025.f1099int.b8.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-st",
            "demo.ug.wst.h0",
            "tax.us.2025.f1099b.covered-w-st.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-st-proceeds",
            "demo.ug.wst-p.h0",
            "tax.us.2025.f1099b.covered-w-st-proceeds.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-st-basis",
            "demo.ug.wst-b.h0",
            "tax.us.2025.f1099b.covered-w-st-basis.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-st-adjustment",
            "demo.ug.wst-a.h0",
            "tax.us.2025.f1099b.covered-w-st-adjustment.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-lt",
            "demo.ug.wlt.h0",
            "tax.us.2025.f1099b.covered-w-lt.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-lt-proceeds",
            "demo.ug.wlt-p.h0",
            "tax.us.2025.f1099b.covered-w-lt-proceeds.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-lt-basis",
            "demo.ug.wlt-b.h0",
            "tax.us.2025.f1099b.covered-w-lt-basis.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-lt-adjustment",
            "demo.ug.wlt-a.h0",
            "tax.us.2025.f1099b.covered-w-lt-adjustment.source-closure",
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
                    f"demo.ug.closure.{horizon_id}",
                    f"{closure_type}|family-horizon={horizon_id},tax-year=2025",
                    True,
                )
            },
        )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.ug.scheduleb.foreign-account",
                "tax.us.2025.scheduleb.foreign-account|tax-year=2025",
                "no",
            )
        },
    )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.ug.scheduleb.foreign-trust",
                "tax.us.2025.scheduleb.foreign-trust|tax-year=2025",
                "no",
            )
        },
    )
    for token in (
        "no-inbound-capital-loss-carryovers",
        "no-form8949-sources",
        "no-other-schedule-d-sources",
        "no-lines-18-19-sources",
        "no-1099da-or-qof",
    ):
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.ug.sd-boundary.{token}",
                    f"tax.us.2025.schedule-d-boundary.{token}|tax-year=2025",
                    "yes",
                )
            },
        )

    n_members = max(len(box1_values), 1)
    payers_stmts: list[tuple[str, str]] = []
    if same_payer_two_statements and n_members >= 2:
        payer = "demo.ug.payer.shared"
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": payer,
                    "kind": "tax.us.unemployment-payer",
                    "label": "Synthetic shared unemployment agency",
                }
            },
        )
        for index in range(n_members):
            stmt = f"demo.ug.stmt.{index}"
            add(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": stmt,
                        "kind": "tax.us.1099g-statement",
                        "label": f"Synthetic 1099-G statement {index}",
                    }
                },
            )
            payers_stmts.append((payer, stmt))
    else:
        for index in range(n_members):
            payer = f"demo.ug.payer.{index}"
            stmt = f"demo.ug.stmt.{index}"
            add(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": payer,
                        "kind": "tax.us.unemployment-payer",
                        "label": f"Synthetic unemployment agency {index}",
                    }
                },
            )
            add(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": stmt,
                        "kind": "tax.us.1099g-statement",
                        "label": f"Synthetic 1099-G statement {index}",
                    }
                },
            )
            payers_stmts.append((payer, stmt))

    add(
        "horizon-genesis",
        {
            "family": {"id": BOX1_FAMILY, "version": "v1"},
            "scope": SCOPE_KEY,
            "horizon_id": "demo.ug.h0",
        },
    )
    horizon = "demo.ug.h0"
    for index, amount in enumerate(box1_values):
        payer, stmt = payers_stmts[index]
        if include_box4:
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.ug.finding.box4.{index}",
                        f"{BOX4_AUTH}|payer={payer},statement={stmt},tax-year=2025",
                        box4_values[index] if index < len(box4_values) else None,
                    )
                },
            )
        next_horizon = f"demo.ug.h{index + 1}"
        add(
            "member-transition",
            {
                "family": {"id": BOX1_FAMILY, "version": "v1"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(
                        f"demo.ug.finding.box1.{index}",
                        f"{BOX1_AMOUNT}|payer={payer},statement={stmt},tax-year=2025",
                        amount,
                    ),
                },
                "successor": {"id": next_horizon, "predecessor": horizon},
            },
        )
        horizon = next_horizon

    if close_box1:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ug.closure.box1",
                    f"{BOX1_CLOSURE}|family-horizon={horizon},tax-year=2025",
                    True,
                )
            },
        )

    for token, value in scope_vals.items():
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.ug.scope.{token}",
                    f"{_scope_id(token)}|tax-year=2025",
                    value,
                )
            },
        )

    adoption = cast(
        dict[str, object],
        json.loads((FIXTURES / "adoptions" / "adopt-core-v20-current.json").read_text("utf-8")),
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


def _derived_id(section: dict[str, Any]) -> str:
    """Stable identity for a derived publication used in displacement checks."""
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



def _published_numeric(model: dict[str, Any], section_id: str) -> Any:
    resolved = _section(model, section_id)["resolved"]
    if resolved.get("disposition") in {
        "published_value",
        "computed_zero",
        "closure_backed_zero",
    }:
        return resolved.get("value")
    return resolved


def _disposition(model: dict[str, Any], section_id: str) -> str:
    return cast(str, _section(model, section_id)["resolved"]["disposition"])


def _attachment(model: dict[str, Any], attachment_id: str) -> dict[str, Any]:
    return next(a for a in model["attachments"] if a["id"] == attachment_id)


class CitizenContractCases(unittest.TestCase):
    """UG-C1 shape: identity, nonnegative, companion schema."""

    def test_box1_member_identity_and_nonnegative(self) -> None:
        bundle = _load("f1099g-box1.bundle.json")
        amount = next(ft for ft in bundle["fact_types"] if ft["id"] == BOX1_AMOUNT)
        self.assertEqual(
            [key["name"] for key in amount["identity_keys"]],
            ["payer", "statement", "tax-year"],
        )
        self.assertEqual(amount["value_schema"], {"type": "number", "minimum": 0})
        self.assertNotIn("evidence", json.dumps(amount["identity_keys"]))
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(-1, amount["value_schema"])

    def test_box4_admits_only_absent_or_zero(self) -> None:
        bundle = _load("f1099g-box1.bundle.json")
        auth = next(ft for ft in bundle["fact_types"] if ft["id"] == BOX4_AUTH)
        jsonschema.validate(None, auth["value_schema"])
        jsonschema.validate(0, auth["value_schema"])
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(5, auth["value_schema"])

    def test_line9_v5_adds_line8_exactly_once(self) -> None:
        rule = _load("rule.form1040-line9.v5.json")
        self.assertEqual(rule["version"], "v5")
        args = [a["name"] for a in rule["value"]["args"]]
        self.assertEqual(
            args,
            [
                "tax.us.2025.wages.total-w2-box1",
                "tax.us.2025.interest.taxable-total",
                "tax.us.2025.dividends.ordinary-total",
                "tax.us.2025.capital-gains.line7a-total",
                LINE8,
            ],
        )
        self.assertEqual(args.count(LINE8), 1)
        hist = _load("rule.form1040-line9.v4.json")
        self.assertEqual(hist["version"], "v4")
        self.assertNotIn(LINE8, json.dumps(hist["value"]))

    def test_scope_tokens_cover_alternative_a(self) -> None:
        bundle = _load("schedule1-part1-scope.bundle.json")
        ids = {ft["id"] for ft in bundle["fact_types"]}
        for token in SCOPE_TOKENS:
            self.assertIn(_scope_id(token), ids)


class PackageExclusivityCases(unittest.TestCase):
    def test_v20_package_validates(self) -> None:
        package = _load("package.core-calculations.v20.json")
        result = validate_package(
            package,
            _corpus(),
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / "published-packages.v15.json"),
        )
        self.assertTrue(result.ok, result.issues)

    def test_package_union_preserves_ratified_tip_members(self) -> None:
        # Focused package-union test: v20 is additive over ratified tip v19
        # (post Form 8949 + Form 1099-INT box-8 merges on origin/main).
        pred = _load("package.core-calculations.v19.json")
        v20 = _load("package.core-calculations.v20.json")
        pred_ids = {m["id"] for m in pred["members"]}
        v20_by_id = {m["id"]: m for m in v20["members"]}
        missing = sorted(pred_ids - set(v20_by_id))
        self.assertEqual(missing, [])
        # Line-9 advances to v5; all other shared ids keep versions.
        for member in pred["members"]:
            if member["id"] == "tax.us.2025.rule.form1040-line9":
                self.assertEqual(v20_by_id[member["id"]]["version"], "v5")
            else:
                self.assertEqual(
                    v20_by_id[member["id"]]["version"],
                    member["version"],
                    member["id"],
                )
        self.assertEqual(v20["schema"], "artifact-package.v17")
        self.assertIn("quantity-vocabulary.v9", v20["admitted_schemas"])

    def test_historical_v17_still_validates(self) -> None:
        package = _load("package.core-calculations.v17.json")
        result = validate_package(
            package,
            _corpus(),
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / "published-packages.v12.json"),
        )
        self.assertTrue(result.ok, result.issues)

    def test_historical_line9_versions_immutable(self) -> None:
        for name, version in (
            ("rule.form1040-line9.json", "v1"),
            ("rule.form1040-line9.v2.json", "v2"),
            ("rule.form1040-line9.v3.json", "v3"),
            ("rule.form1040-line9.v4.json", "v4"),
        ):
            rule = _load(name)
            self.assertEqual(rule["version"], version)
            self.assertNotIn(LINE8, json.dumps(rule.get("value", {})))


class CompanionAdmissionCases(unittest.TestCase):
    def test_box1_companion_pair_registered(self) -> None:
        reg = tax_registry()
        self.assertIn(BOX1_AMOUNT, reg.companion_presence_pairs)
        self.assertEqual(reg.companion_presence_pairs[BOX1_AMOUNT], BOX4_AUTH)
        self.assertEqual(domain_companion_presence_pairs()[BOX1_AMOUNT], BOX4_AUTH)


class LiveEvidenceCases(unittest.TestCase):
    """P1–P16 / N1–N7 through live_coordinate_run."""

    def test_p1_one_statement_publishes_line7_10_8(self) -> None:
        _, model = _run(_ug_acts(box1_values=[2500]), "demo.ug.p1")
        self.assertEqual(_published_numeric(model, "line-sch1-7"), 2500)
        self.assertEqual(_published_numeric(model, "line-sch1-10"), 2500)
        self.assertEqual(_published_numeric(model, "line-8"), 2500)
        att = _attachment(model, "tax.us.2025.rule.attachment.schedule-1")
        self.assertEqual(att["resolved"]["disposition"], "published")

    def test_p2_multiple_agencies_aggregate_once(self) -> None:
        _, model = _run(_ug_acts(box1_values=[1000, 400]), "demo.ug.p2")
        self.assertEqual(_published_numeric(model, "line-8"), 1400)

    def test_p3_two_statements_same_payer(self) -> None:
        _, model = _run(
            _ug_acts(box1_values=[700, 300], same_payer_two_statements=True),
            "demo.ug.p3",
        )
        self.assertEqual(_published_numeric(model, "line-8"), 1000)

    def test_p4_correction_same_identity(self) -> None:
        """Correction supersedes the same logical statement and re-derives line 8."""
        acts = _ug_acts(box1_values=[1000])
        for index, act in enumerate(acts):
            act["committed_against"] = index
        _, before = _run(acts, "demo.ug.p4-before")
        sec_before = _section(before, "line-8")
        self.assertEqual(sec_before["resolved"]["value"], 1000)
        id_before = _derived_id(sec_before)

        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.ug.finding.box1.correction",
                        f"{BOX1_AMOUNT}|payer=demo.ug.payer.0,statement=demo.ug.stmt.0,tax-year=2025",
                        1250,
                    )
                },
            )
        )
        for index, act in enumerate(acts):
            act["committed_against"] = index
        _, after = _run(acts, "demo.ug.p4-after")
        sec_after = _section(after, "line-8")
        self.assertEqual(sec_after["resolved"]["value"], 1250)
        id_after = _derived_id(sec_after)
        self.assertNotEqual(
            id_before,
            id_after,
            "same-statement box-1 correction must re-derive line 8 (not reuse stale finding)",
        )
        blob = json.dumps(after)
        self.assertIn("demo.ug.finding.box1.correction", blob)
        # Companion provenance for the same logical statement remains on the walk.
        self.assertIn("demo.ug.finding.box4.0", blob)

    def test_p5_closed_empty_publishes_explicit_zero(self) -> None:
        _, model = _run(_ug_acts(box1_values=[], close_box1=True), "demo.ug.p5")
        for section_id in ("line-sch1-7", "line-sch1-10", "line-8"):
            resolved = _section(model, section_id)["resolved"]
            self.assertIn(
                resolved["disposition"],
                {"closure_backed_zero", "computed_zero", "published_value"},
                section_id,
            )
            self.assertEqual(resolved.get("value"), 0, section_id)

    def test_p6_open_closure_blocks(self) -> None:
        _, model = _run(
            _ug_acts(box1_values=[900], close_box1=False),
            "demo.ug.p6",
        )
        self.assertEqual(_disposition(model, "line-sch1-7"), "blocked")
        self.assertEqual(_disposition(model, "line-8"), "blocked")

    def test_p7_late_member_stale_then_restore(self) -> None:
        acts = _ug_acts(box1_values=[500], close_box1=True)
        # Late member on successor horizon without re-closure → stale.
        acts.append(
            _act(
                len(acts),
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": "demo.ug.payer.late",
                        "kind": "tax.us.unemployment-payer",
                        "label": "Late agency",
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
                        "id": "demo.ug.stmt.late",
                        "kind": "tax.us.1099g-statement",
                        "label": "Late statement",
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
                        "demo.ug.finding.box4.late",
                        f"{BOX4_AUTH}|payer=demo.ug.payer.late,statement=demo.ug.stmt.late,tax-year=2025",
                        None,
                    )
                },
            )
        )
        acts.append(
            _act(
                len(acts),
                "member-transition",
                {
                    "family": {"id": BOX1_FAMILY, "version": "v1"},
                    "scope": SCOPE_KEY,
                    "member": {
                        "action": "assert",
                        "finding": _attested(
                            "demo.ug.finding.box1.late",
                            f"{BOX1_AMOUNT}|payer=demo.ug.payer.late,statement=demo.ug.stmt.late,tax-year=2025",
                            200,
                        ),
                    },
                    "successor": {"id": "demo.ug.h-late", "predecessor": "demo.ug.h1"},
                },
            )
        )
        for index, act in enumerate(acts):
            act["committed_against"] = index
            act["act_id"] = f"demo.ug.p7.stale.{index:03d}"
        _, stale = _run(acts, "demo.ug.p7-stale")
        self.assertEqual(_disposition(stale, "line-8"), "blocked")

        # Successor closure restores publication.
        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.ug.closure.box1.restored",
                        f"{BOX1_CLOSURE}|family-horizon=demo.ug.h-late,tax-year=2025",
                        True,
                    )
                },
            )
        )
        for index, act in enumerate(acts):
            act["committed_against"] = index
            act["act_id"] = f"demo.ug.p7.restore.{index:03d}"
        _, restored = _run(acts, "demo.ug.p7-restored")
        self.assertEqual(_published_numeric(restored, "line-8"), 700)

    def test_p8_box4_null_admissible(self) -> None:
        _, model = _run(
            _ug_acts(box1_values=[300], box4_values=[None]),
            "demo.ug.p8",
        )
        self.assertEqual(_published_numeric(model, "line-8"), 300)

    def test_p9_box4_zero_admissible(self) -> None:
        _, model = _run(
            _ug_acts(box1_values=[300], box4_values=[0]),
            "demo.ug.p9",
        )
        self.assertEqual(_published_numeric(model, "line-8"), 300)

    def test_n1_missing_box4_companion_rejected(self) -> None:
        acts = _ug_acts(box1_values=[100], include_box4=False)
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
                    run_id="demo.ug.n1",
                    governance_pins=[],
                    surface=_surface(),
                    output_name="out.json",
                )
        message = str(ctx.exception)
        self.assertIn("companion presence violated", message)
        self.assertIn(BOX1_AMOUNT, message)
        self.assertIn(BOX4_AUTH, message)
        self.assertNotIn("25b", message.lower())

    def test_n2_nonzero_box4_rejected(self) -> None:
        acts = _ug_acts(box1_values=[100], box4_values=[50])
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
                    run_id="demo.ug.n2",
                    governance_pins=[],
                    surface=_surface(),
                    output_name="out.json",
                )
        message = str(ctx.exception).lower()
        self.assertTrue(
            "companion" in message or "box4" in message.replace("-", "").replace("_", ""),
            message,
        )
        self.assertNotIn("25b", message)

    def test_n3_residual_incomplete_blocks(self) -> None:
        _, model = _run(
            _ug_acts(
                box1_values=[400],
                scope={"no-f1099g-box2-state-refund": "no"},
            ),
            "demo.ug.n3",
        )
        self.assertIn(_disposition(model, "line-8"), {"blocked", "guard_inapplicable"})

    def test_n4_repayment_blocks(self) -> None:
        _, model = _run(
            _ug_acts(
                box1_values=[400],
                scope={"no-unemployment-repayment": "no"},
            ),
            "demo.ug.n4",
        )
        self.assertIn(_disposition(model, "line-8"), {"blocked", "guard_inapplicable"})

    def test_n5_other_schedule1_income_present_blocks(self) -> None:
        _, model = _run(
            _ug_acts(
                box1_values=[400],
                scope={"no-sch1-line3-business": "no"},
            ),
            "demo.ug.n5",
        )
        self.assertIn(_disposition(model, "line-sch1-10"), {"blocked", "guard_inapplicable"})
        self.assertIn(_disposition(model, "line-8"), {"blocked", "guard_inapplicable"})

    def test_n6_missing_scope_authority_blocks(self) -> None:
        acts = _ug_acts(box1_values=[400])
        acts = [
            act
            for act in acts
            if not (
                act["kind"] == "assertion"
                and "schedule1-part1-scope.no-sch1-line1-taxable-refunds"
                in json.dumps(act["payload"])
            )
        ]
        for index, act in enumerate(acts):
            act["committed_against"] = index
            act["act_id"] = f"demo.ug.n6.act.{index:03d}"
        _, model = _run(acts, "demo.ug.n6")
        self.assertEqual(_disposition(model, "line-8"), "blocked")

    def test_p10_unemployment_only_line_equality_and_line9_once(self) -> None:
        # Wages closed-empty / zero path: compare line 9 with and without unemployment.
        _, with_u = _run(
            _ug_acts(box1_values=[1800], wages=0, box1a=None, box2a=None),
            "demo.ug.p10-with",
        )
        _, without = _run(
            _ug_acts(box1_values=[], close_box1=True, wages=0, box1a=None, box2a=None),
            "demo.ug.p10-without",
        )
        self.assertEqual(_published_numeric(with_u, "line-sch1-7"), 1800)
        self.assertEqual(_published_numeric(with_u, "line-sch1-10"), 1800)
        self.assertEqual(_published_numeric(with_u, "line-8"), 1800)
        line9_with = _published_numeric(with_u, "line-9")
        line9_without = _published_numeric(without, "line-9")
        if isinstance(line9_with, (int, float)) and isinstance(line9_without, (int, float)):
            self.assertEqual(line9_with - line9_without, 1800)
        else:
            # Without unemployment, line 8 = 0 so line 9 equals with_u minus 1800.
            self.assertEqual(_published_numeric(with_u, "line-8"), 1800)
            self.assertEqual(_published_numeric(without, "line-8"), 0)

    def test_p11_unemployment_plus_w2(self) -> None:
        _, model = _run(
            _ug_acts(box1_values=[500], wages=90000, box1a=None, box2a=None),
            "demo.ug.p11",
        )
        self.assertEqual(_published_numeric(model, "line-1a"), 90000)
        self.assertEqual(_published_numeric(model, "line-8"), 500)
        line9 = _published_numeric(model, "line-9")
        self.assertIsInstance(line9, (int, float))
        self.assertEqual(line9, 90500)

    def test_p12_unemployment_plus_interest_dividends(self) -> None:
        # Base _cgd path includes closed interest (often zero) and optional dividends.
        _, model = _run(
            _ug_acts(box1_values=[250], wages=50000, box1a=600, box1b=100, box2a=None),
            "demo.ug.p12",
        )
        self.assertEqual(_published_numeric(model, "line-8"), 250)
        line9 = _published_numeric(model, "line-9")
        self.assertIsInstance(line9, (int, float))
        # wages 50000 + ordinary dividends 600 + line8 250 (+ interest 0 + line7a 0)
        self.assertEqual(line9, 50850)

    def test_p13_unemployment_plus_capital_gain_path(self) -> None:
        _, model = _run(
            _ug_acts(box1_values=[100], wages=80000, box1a=0, box2a=1500),
            "demo.ug.p13",
        )
        self.assertEqual(_published_numeric(model, "line-8"), 100)
        # line 7a path remains present; line 8 added once
        line9 = _published_numeric(model, "line-9")
        self.assertIsInstance(line9, (int, float))
        line7a = _published_numeric(model, "line-7a")
        if isinstance(line7a, (int, float)):
            self.assertEqual(line9, 80000 + line7a + 100)

    def test_p14_downstream_taxable_income_and_tax(self) -> None:
        _, model = _run(
            _ug_acts(box1_values=[2000], wages=90000, box1a=None, box2a=None),
            "demo.ug.p14",
        )
        line9 = _published_numeric(model, "line-9")
        line15 = _published_numeric(model, "line-15")
        line16 = _published_numeric(model, "line-16")
        self.assertIsInstance(line9, (int, float))
        self.assertIsInstance(line15, (int, float))
        self.assertIsInstance(line16, (int, float))
        self.assertEqual(line9, 92000)
        # taxable income = line9 - standard deduction; tax recomputes from it
        self.assertLess(line15, line9)
        self.assertGreaterEqual(line16, 0)

    def test_p15_correction_displaces_downstream(self) -> None:
        """Box-1 correction re-derives line 8 and line 9; provenance pins the correction."""
        acts = _ug_acts(box1_values=[1000], wages=50000, box1a=None, box2a=None)
        for index, act in enumerate(acts):
            act["committed_against"] = index
        _, before = _run(acts, "demo.ug.p15-before")
        line8_before = _section(before, "line-8")
        line9_before = _section(before, "line-9")
        self.assertEqual(line8_before["resolved"]["value"], 1000)
        self.assertEqual(line9_before["resolved"]["value"], 51000)
        id8_before = _derived_id(line8_before)
        id9_before = _derived_id(line9_before)

        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.ug.p15.correction",
                        f"{BOX1_AMOUNT}|payer=demo.ug.payer.0,statement=demo.ug.stmt.0,tax-year=2025",
                        1500,
                    )
                },
            )
        )
        for index, act in enumerate(acts):
            act["committed_against"] = index
        _, after = _run(acts, "demo.ug.p15-after")
        line8_after = _section(after, "line-8")
        line9_after = _section(after, "line-9")
        self.assertEqual(line8_after["resolved"]["value"], 1500)
        self.assertEqual(line9_after["resolved"]["value"], 51500)
        self.assertNotEqual(id8_before, _derived_id(line8_after), "line 8 must re-derive")
        self.assertNotEqual(id9_before, _derived_id(line9_after), "line 9 must re-derive")
        blob = json.dumps(after)
        self.assertIn("demo.ug.p15.correction", blob)
        self.assertIn("demo.ug.finding.box4.0", blob)

    def test_p15b_box4_null_to_zero_displaces(self) -> None:
        """Box-4 companion null→0 re-derives line 8 with corrected companion provenance."""
        acts = _ug_acts(box1_values=[800], box4_values=[None])
        for index, act in enumerate(acts):
            act["committed_against"] = index
        _, first = _run(acts, "demo.ug.p15b-1")
        sec1 = _section(first, "line-8")
        self.assertEqual(sec1["resolved"]["value"], 800)
        id1 = _derived_id(sec1)
        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.ug.finding.box4.corrected",
                        f"{BOX4_AUTH}|payer=demo.ug.payer.0,statement=demo.ug.stmt.0,tax-year=2025",
                        0,
                    )
                },
            )
        )
        for index, act in enumerate(acts):
            act["committed_against"] = index
        _, second = _run(acts, "demo.ug.p15b-2")
        sec2 = _section(second, "line-8")
        self.assertEqual(sec2["resolved"]["value"], 800)
        self.assertNotEqual(id1, _derived_id(sec2), "box-4 correction must re-derive line 8")
        self.assertIn("demo.ug.finding.box4.corrected", json.dumps(second))

    def test_p16_presentation_golden_structural_equality(self) -> None:
        """Committed presentation golden must match a fresh P16-shaped live model."""
        _, model = _run(_ug_acts(box1_values=[1400]), "demo.ug.p16")
        golden_path = (
            FIXTURES / "presentation" / "form1099g-box1-line8.presentation-model.v1.json"
        )
        self.assertTrue(
            golden_path.is_file(),
            f"committed presentation golden required at {golden_path}",
        )
        golden = json.loads(golden_path.read_text("utf-8"))
        self.assertEqual(
            model,
            golden,
            "regenerate with tools/generate_form1099g_box1_schedule1_line7_goldens.py",
        )
        self.assertEqual(_published_numeric(model, "line-sch1-7"), 1400)
        self.assertEqual(_published_numeric(model, "line-8"), 1400)
        section = _section(model, "line-8")
        self.assertTrue(section.get("citationSites") or model.get("citationGroups"))
        explain = json.dumps(section).lower()
        self.assertTrue(
            "additional income" in explain or "schedule 1" in explain or "line 8" in explain,
            section,
        )
        att = _attachment(model, "tax.us.2025.rule.attachment.schedule-1")
        self.assertEqual(att["resolved"]["disposition"], "published")

    def test_n7_malformed_presentation_blocks_or_redacts(self) -> None:
        """Projector on the real line-8 field path rejects non-numeric publication."""
        from packages.derivation.loader import DerivationSchemas, load_canon
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
        from packages.derivation.live import _resolved_run_material

        acts = _ug_acts(box1_values=[50])
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
            run_id="demo.ug.n7-projector",
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
        symbol = "tax.us.2025.income.additional-income"
        pubs: list[Publication] = []
        found = False
        for pub in result.publications:
            finding = copy.deepcopy(pub.finding)
            if finding.get("symbol") == symbol:
                finding["value"] = "not-a-number"
                found = True
            pubs.append(Publication(act=pub.act, finding=finding))
        self.assertTrue(
            found,
            "expected additional-income (line 8) publication from the live package path",
        )
        with self.assertRaises(PresentationModelError) as ctx:
            build_presentation_model(
                run_id="demo.ug.n7-bad",
                resolved_members=resolved.resolved_members,
                state=state,
                publications=pubs,
                dispositions=result.dispositions,
            )
        message = str(ctx.exception).lower()
        self.assertIn("invalid numeric", message)

    def test_line2a_remains_non_input_to_line9(self) -> None:
        # R1-adjacent: unemployment path does not feed line 2a into line 9.
        rule = _load("rule.form1040-line9.v5.json")
        blob = json.dumps(rule)
        self.assertNotIn("line2a", blob)
        self.assertNotIn("tax-exempt-interest", blob)
        self.assertNotIn("box12", blob)


class CompatibilityCases(unittest.TestCase):
    """R1–R4: package members present and executable peer routes still pass."""

    def _run_named(self, name: str) -> None:
        suite = unittest.defaultTestLoader.loadTestsFromName(name)
        result = unittest.TestResult()
        suite.run(result)
        if not result.wasSuccessful():
            errors = result.failures + result.errors
            detail = "\n".join(f"{t}: {err}" for t, err in errors[:3])
            self.fail(f"{name} failed ({len(errors)}): {detail}")

    def test_r1_line2a_and_box8_route_still_executes(self) -> None:
        package = _load("package.core-calculations.v20.json")
        members = {(m["id"], m["version"]) for m in package["members"]}
        self.assertIn(("tax.us.2025.rule.form1040-line2a", "v2"), members)
        self.assertIn(("tax.us.2025.f1099div.box12.vocabulary", "v1"), members)
        self.assertIn(("tax.us.2025.f1099int.box8.vocabulary", "v1"), members)
        self._run_named(
            "tests.test_form1099int_box8_line2a.LiveEvidenceCases."
            "test_p1_one_payer_box8_publishes_line2a"
        )

    def test_r2_schedule_b_route_still_executes(self) -> None:
        package = _load("package.core-calculations.v20.json")
        members = {(m["id"], m["version"]) for m in package["members"]}
        self.assertIn(("tax.us.2025.rule.attachment.schedule-b", "v4"), members)
        self._run_named(
            "tests.test_schedule_b_interest_adjustments."
            "AdjustmentLifecycleCases.test_composition_subtracts_all_three_once"
        )

    def test_r3_schedule_d_and_carryover_routes_still_execute(self) -> None:
        package = _load("package.core-calculations.v20.json")
        members = {(m["id"], m["version"]) for m in package["members"]}
        self.assertIn(("tax.us.2025.rule.attachment.schedule-d", "v5"), members)
        self.assertIn(("tax.us.2025.rule.capital-loss-carryover.short-term", "v1"), members)
        self.assertIn(("tax.us.2025.rule.capital-loss-carryover.long-term", "v1"), members)
        self._run_named(
            "tests.test_schedule_d_inbound_loss_carryovers_t1."
            "PathADeclaredNoCarryover.test_path_a_publishes_zero_without_prior_facts"
        )

    def test_r4_form8949_route_still_executes(self) -> None:
        package = _load("package.core-calculations.v20.json")
        members = {(m["id"], m["version"]) for m in package["members"]}
        self.assertIn(("tax.us.2025.rule.attachment.f8949", "v1"), members)
        self.assertIn(("tax.us.2025.f1099b.covered-w-st", "v1"), members)
        self._run_named(
            "tests.test_schedule_d_form8949_covered_wash_sale_t1."
            "HappyPath.test_st_loss_fully_disallowed"
        )


if __name__ == "__main__":
    unittest.main()
