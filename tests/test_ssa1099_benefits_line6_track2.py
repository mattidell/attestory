"""Track 2: SSA-1099 Social Security Benefits Worksheet through line 6a/6b and line 9."""

from __future__ import annotations

import hashlib
import json
import shutil
import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.package_validation import package_instance_checksum
from packages.derivation.production_resolver import (
    PublicationSurface,
    Refusal,
    resolve_production_package,
)
from packages.tax.loader import TAX_CONTENT_DIR
from packages.tax.ssa_benefits import SsaBenefitsError
from tests.test_form1099r_ira_line4b_track2 import _ira_acts
from tests.test_form1099g_box1_schedule1_line7 import (
    _act,
    _attested,
    _disposition,
    _published_numeric,
)


ROOT = Path(__file__).resolve().parent.parent
CONTENT = TAX_CONTENT_DIR
FIXTURES = ROOT / "packages" / "sample_data" / "ssa1099_benefits_line6"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

FAMILY = "tax.us.2025.ssa1099.benefits"
BOX3 = "tax.us.2025.ssa1099.box3-benefits-paid"
BOX4 = "tax.us.2025.ssa1099.box4-repayment"
BOX5 = "tax.us.2025.ssa1099.box5-net-benefits"
BOX6 = "tax.us.2025.ssa1099.box6-withholding"
RECIPIENT = "tax.us.2025.ssa1099.recipient"
KIND = "tax.us.2025.ssa1099.statement-kind"
LUMP = "tax.us.2025.ssa1099.lump-sum-election"
CLOSURE = "tax.us.2025.ssa1099.source-closure"
MFS = "tax.us.2025.mfs-lived-apart-all-year"
LINE6A = "tax.us.2025.social-security.line6a"
LINE6B = "tax.us.2025.social-security.line6b"
LINE6C = "tax.us.2025.social-security.line6c-indicator"
LINE6D = "tax.us.2025.social-security.line6d-indicator"
TOTAL_INCOME = "tax.us.2025.income.total-income"
LINE2A = "tax.us.2025.tax-exempt-interest.line2a-total"

SCOPE_TOKENS = (
    "no-unsupported-line1-entries",
    "no-pension-annuity-line5b",
    "no-traditional-ira-deduction",
    "no-form-2555",
    "no-form-4563",
    "no-form-8815",
    "no-excluded-adoption-benefits",
    "no-puerto-rico-or-samoa-income",
    "no-schedule1-line24z-writein",
    "no-sch1-line11-educator",
    "no-sch1-line12-business-expenses",
    "no-sch1-line13-hsa",
    "no-sch1-line14-moving",
    "no-sch1-line15-deductible-se",
    "no-sch1-line16-se-retirement",
    "no-sch1-line17-se-health",
    "no-sch1-line18-penalty",
    "no-sch1-line19-alimony-paid",
    "no-sch1-line20-ira-deduction",
    "no-sch1-line23-archer-msa",
    "no-sch1-line25-other-adjustments",
    "no-lump-sum-election",
    "no-rrb-or-foreign-social-benefit",
)


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


def _scope_id(token: str) -> str:
    return f"tax.us.2025.ss-benefits-scope.{token}"


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / "published-packages.v23.json",
        CONTENT,
    )


def _ssa_acts(
    *,
    benefits: list[tuple[float, float, float]] | None = None,
    close: bool = True,
    wages: float = 15000,
    interest: float | None = None,
    ordinary_dividends: float | None = None,
    qualified_dividends: float | None = None,
    capital_gains: float | None = None,
    unemployment: float | None = None,
    filing_status: str = "single",
    mfs_lived_apart: str | None = None,
    tax_exempt: float | None = None,
    ira_amounts: list[float] | None = None,
    scope: dict[str, str] | None = None,
    recipient: str = "taxpayer",
    statement_overrides: list[dict[str, object]] | None = None,
) -> list[dict[str, object]]:
    """Production-shaped acts with controlled ordinary-income components + SSA."""
    from tests import test_form1099r_ira_line4b_track2 as ira_mod

    original_ug = cast(Any, getattr(ira_mod, "_ug_acts"))

    def _ug_with_components(**kwargs: Any) -> list[dict[str, object]]:
        kwargs["wages"] = wages
        # Unemployment → Schedule 1 / Form 1040 line 8 via 1099-G box 1.
        if unemployment is not None and unemployment > 0:
            kwargs["box1_values"] = [unemployment]
            kwargs["close_box1"] = True
        else:
            kwargs["box1_values"] = []
            kwargs["close_box1"] = True
        # Ordinary / qualified dividends and capital-gain distributions.
        if ordinary_dividends is not None:
            kwargs["box1a"] = ordinary_dividends
        if qualified_dividends is not None:
            kwargs["box1b"] = qualified_dividends
        if capital_gains is not None:
            kwargs["box2a"] = capital_gains
        return cast(list[dict[str, object]], original_ug(**kwargs))

    setattr(ira_mod, "_ug_acts", _ug_with_components)
    try:
        acts = _ira_acts(
            amounts=[] if ira_amounts is None else ira_amounts,
            close=True,
            qualified_dividends=False,
        )
    finally:
        setattr(ira_mod, "_ug_acts", original_ug)
    acts.pop()  # drop historical package adoption

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    # Ensure wages / filing status from base corpus; override wages via W-2 if needed
    # is already set by upstream helpers. Adopt SSA vocabulary + scope + successor packages.
    add("bundle-adoption", {"bundle": _load("ssa1099.bundle.v2.json")})
    add("bundle-adoption", {"bundle": _load("ss-benefits-scope.bundle.json")})
    # Line 2a residual scopes + closed-empty box-12 so tax-exempt line 2a
    # publishes zero for the worksheet W4 pin without Path B INT box-8.
    if not any(
        act.get("kind") == "bundle-adoption"
        and cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("bundle", {})).get("id")
        == "tax.us.2025.line2a-scope.vocabulary"
        for act in acts
    ):
        add("bundle-adoption", {"bundle": _load("line2a-scope.bundle.json")})
    line2a_scope_tokens = (
        "no-f1099int-tax-exempt",
        "no-f1099oid-tax-exempt",
        "no-unreported-tax-exempt",
        "no-premium-adjustment",
        "no-child-income-election",
        "no-amt-form-6251",
        "no-credit-using-tax-exempt",
        "no-deduction-using-tax-exempt",
    )
    for token in line2a_scope_tokens:
        fid = f"tax.us.2025.line2a-scope.{token}"
        # skip if already asserted by upstream corpus
        already = any(
            str(cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("finding", {})).get("fact_id", "")).startswith(fid + "|")
            for act in acts
        )
        if not already:
            add(
                "assertion",
                {"finding": _attested(f"demo.ssa.line2a.{token}", f"{fid}|tax-year=2025", "yes")},
            )
    div12_family = "tax.us.2025.f1099div.12"
    if not any(
        act.get("kind") == "bundle-adoption"
        and cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("bundle", {})).get("id")
        == "tax.us.2025.f1099div.box12.vocabulary"
        for act in acts
    ):
        add("bundle-adoption", {"bundle": _load("f1099div-box12.bundle.v2.json")})

    scope_vals = {token: "yes" for token in SCOPE_TOKENS}
    if scope:
        scope_vals.update(scope)
    for token, value in scope_vals.items():
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.ssa.scope.{token}",
                    f"{_scope_id(token)}|tax-year=2025",
                    value,
                )
            },
        )

    if mfs_lived_apart is not None:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.mfs-lived-apart",
                    f"{MFS}|tax-year=2025",
                    mfs_lived_apart,
                )
            },
        )

    # Override corpus filing status when a non-default status is requested.
    if filing_status != "single":
        replaced = False
        for act in acts:
            finding = cast(
                dict[str, Any],
                cast(dict[str, Any], act.get("payload", {})).get("finding", {}),
            )
            fact_id = str(finding.get("fact_id", ""))
            if fact_id.startswith("tax.us.2025.filing-status|"):
                finding["value"] = filing_status
                replaced = True
                break
        if not replaced:
            add(
                "assertion",
                {
                    "finding": _attested(
                        "demo.ssa.filing-status",
                        "tax.us.2025.filing-status|tax-year=2025",
                        filing_status,
                    )
                },
            )

    # Taxable interest (Form 1099-INT box 1): advance the CGD closed-empty
    # int-b1 horizon so line 2b includes the amount exactly once.
    if interest is not None and interest > 0:
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": "demo.ssa.int.payer",
                    "kind": "tax.us.interest-payer",
                    "label": "Synthetic interest payer",
                }
            },
        )
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": "demo.ssa.int.stmt",
                    "kind": "tax.us.1099int-statement",
                    "label": "Synthetic Form 1099-INT",
                }
            },
        )
        add(
            "member-transition",
            {
                "family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(
                        "demo.ssa.finding.int-b1",
                        "tax.us.2025.f1099int.box1-interest|"
                        "payer=demo.ssa.int.payer,statement=demo.ssa.int.stmt,tax-year=2025",
                        interest,
                    ),
                },
                "successor": {
                    "id": "demo.ssa.int-b1.h1",
                    "predecessor": "demo.cgd.t2.int-b1.h0",
                },
            },
        )
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.closure.int-b1",
                    "tax.us.2025.f1099int.b1.source-closure|"
                    "family-horizon=demo.ssa.int-b1.h1,tax-year=2025",
                    True,
                )
            },
        )

    benefits = [(12000.0, 0.0, 12000.0)] if benefits is None else benefits
    horizon = "demo.ssa.h0"
    add(
        "horizon-genesis",
        {"family": {"id": FAMILY, "version": "v1"}, "scope": SCOPE_KEY, "horizon_id": horizon},
    )
    for index, (b3, b4, b5) in enumerate(benefits):
        statement = f"demo.ssa.statement.{index}"
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": statement,
                    "kind": "tax.us.ssa1099-statement",
                    "label": "Synthetic Form SSA-1099",
                }
            },
        )
        # box5 is the collected member: assert companions first so presence
        # admission sees a complete same-statement witness set.
        ov = {}
        if statement_overrides and index < len(statement_overrides):
            ov = statement_overrides[index]
        kind_val = cast(str, ov.get("kind", "ssa-1099"))
        lump_val = cast(bool, ov.get("lump_sum_election", False))
        recip_val = cast(str, ov.get("recipient", recipient))
        box6_val = cast(float | None, ov.get("box6", 0))
        members: tuple[tuple[str, object, str], ...] = (
            (BOX3, b3, "box3"),
            (BOX4, b4, "box4"),
            (BOX6, box6_val, "box6"),
            (RECIPIENT, recip_val, "recipient"),
            (KIND, kind_val, "kind"),
            (LUMP, lump_val, "lump"),
            (BOX5, b5, "box5"),
        )
        for member_fact_type, member_value, member_suffix in members:
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.ssa.finding.{member_suffix}.{index}",
                        f"{member_fact_type}|statement={statement},tax-year=2025",
                        member_value,
                    )
                },
            )

    if close:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.closure",
                    f"{CLOSURE}|family-horizon={horizon},tax-year=2025",
                    True,
                )
            },
        )

    # Line-2a residual scopes still required by line2a v3 (except removed SS residual)
    # Already present via IRA/UG helpers for many paths; tax-exempt optional Path A/B.

    # Line 2a / box-12: present tax-exempt dividends or closed-empty zero.
    div12_family = "tax.us.2025.f1099div.12"
    horizon = "demo.ssa.div12.h0"
    add(
        "horizon-genesis",
        {
            "family": {"id": div12_family, "version": "v1"},
            "scope": SCOPE_KEY,
            "horizon_id": horizon,
        },
    )
    if tax_exempt is not None and tax_exempt > 0:
        payer = "demo.ssa.div12.payer"
        statement = "demo.ssa.div12.statement.0"
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": payer,
                    "kind": "tax.us.dividend-payer",
                    "label": "Synthetic dividend payer",
                }
            },
        )
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": statement,
                    "kind": "tax.us.1099div-statement",
                    "label": "Synthetic Form 1099-DIV",
                }
            },
        )
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.div12.box13",
                    "tax.us.2025.f1099div.box13-specified-pab-authority|"
                    f"payer={payer},statement={statement},tax-year=2025",
                    None,
                )
            },
        )
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.div12.box12",
                    "tax.us.2025.f1099div.box12-exempt-interest-dividends|"
                    f"payer={payer},statement={statement},tax-year=2025",
                    tax_exempt,
                )
            },
        )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.ssa.div12.closure",
                f"tax.us.2025.f1099div.12.source-closure|family-horizon={horizon},tax-year=2025",
                True,
            )
        },
    )


    adoption = _load_fixture_adoption()
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


def _load_fixture_adoption() -> dict[str, object]:
    return cast(
        dict[str, object],
        json.loads((FIXTURES / "adoptions" / "adopt-core-v28-current.json").read_text("utf-8")),
    )


def _run(acts: list[dict[str, object]], run_id: str = "demo.ssa.run") -> tuple[dict[str, Any], dict[str, Any]]:
    surface = _surface()
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
        return (
            json.loads(result.output_path.read_text("utf-8")),
            json.loads(result.presentation_path.read_text("utf-8")),
        )


def _authenticated_v28_mutation_surface(
    temporary_root: Path, package: dict[str, Any], mutation: str
) -> tuple[PublicationSurface, list[dict[str, object]]]:
    """Build an authenticated temporary v28 chain for resolver kill tests."""
    member_dir = temporary_root / "members"
    release_dir = temporary_root / "releases"
    member_dir.mkdir()
    release_dir.mkdir()
    for source in CONTENT.glob("*.json"):
        shutil.copyfile(source, member_dir / source.name)

    mutated = json.loads(json.dumps(package))
    if mutation == "stale":
        for entry in cast(list[dict[str, Any]], mutated["entrypoints"]):
            if entry["id"] == "tax.us.2025.rule.form1040-line9":
                entry["version"] = "v1"
                break
        else:
            raise AssertionError("line-9 entrypoint not found")
    elif mutation == "dangling":
        cast(list[dict[str, Any]], mutated["entrypoints"]).append(
            {"id": "tax.us.2025.rule.nonexistent-entrypoint", "version": "v1"}
        )
    else:
        raise AssertionError(f"unknown mutation: {mutation}")
    mutated["package_checksum"] = package_instance_checksum(mutated)
    (member_dir / "package.core-calculations.v28.json").write_text(
        json.dumps(mutated, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    registry = _load("published-packages.v23.json")
    package_entry = next(
        entry
        for entry in cast(list[dict[str, Any]], registry["packages"])
        if entry["id"] == mutated["id"] and entry["version"] == mutated["version"]
    )
    package_entry["checksum"] = mutated["package_checksum"]
    registry_path = temporary_root / "published-packages.v23.json"
    registry_bytes = (json.dumps(registry, indent=2, sort_keys=True) + "\n").encode("utf-8")
    registry_path.write_bytes(registry_bytes)

    release_source = FIXTURES / "publication_surface" / "releases" / "demo.release.2025.v21.json"
    release = cast(dict[str, Any], json.loads(release_source.read_text("utf-8")))
    release["package_registry_sha256"] = hashlib.sha256(registry_bytes).hexdigest()
    release_bytes = (json.dumps(release, indent=2, sort_keys=True) + "\n").encode("utf-8")
    (release_dir / release_source.name).write_bytes(release_bytes)

    adoption = _load_fixture_adoption()
    payload = cast(dict[str, Any], adoption["payload"])
    payload["package"]["checksum"] = mutated["package_checksum"]
    payload["release"]["checksum"] = hashlib.sha256(release_bytes).hexdigest()
    adoption["committed_against"] = 0
    return PublicationSurface(release_dir, registry_path, member_dir), [adoption]


def _pub(payload: dict[str, Any], symbol: str) -> float:
    return cast(float, _published_numeric(payload, symbol))




def _expected_taxable_ss(
    benefits: float,
    ordinary: float,
    tax_exempt: float = 0.0,
    *,
    base: float = 25000.0,
    tier2: float = 9000.0,
) -> float:
    """Paper Social Security Benefits Worksheet W1–W18 for nonnegative inputs."""
    from decimal import Decimal, ROUND_HALF_UP

    def D(x: float | int | Decimal | str) -> Decimal:
        return Decimal(str(x))

    w1 = D(benefits)
    w2 = (w1 * D("0.5"))
    w5 = w2 + D(ordinary) + D(tax_exempt)
    w7 = max(w5, D(0))
    w9 = max(w7 - D(base), D(0))
    if w9 == 0:
        return float(0)
    w11 = max(w9 - D(tier2), D(0))
    w12 = min(w9, D(tier2))
    w13 = w12 * D("0.5")
    w14 = min(w2, w13)
    w15 = w11 * D("0.85")
    w16 = w14 + w15
    w17 = w1 * D("0.85")
    w18 = min(w16, w17)
    # Project rounding: nearest dollar half-up, matching common IRS money rounding
    # used by the live round mode on demo fixtures.
    return float(w18.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _report_item(report: dict[str, Any], symbol: str) -> dict[str, Any]:
    for item in report.get("dispositions", []):
        if item.get("symbol") == symbol:
            return cast(dict[str, Any], item)
    raise AssertionError(f"missing disposition for {symbol}")


def _renumber(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    for index, act in enumerate(acts):
        act["committed_against"] = index
    return acts


class TestSsaWorksheetLive(unittest.TestCase):
    def test_production_rejects_unreconciled_boxes(self) -> None:
        acts = _renumber(
            _ssa_acts(
                benefits=[(1000.0, 200.0, 700.0)],
                ira_amounts=[],
                wages=90000,
            )
        )
        with self.assertRaisesRegex(SsaBenefitsError, "box 5 to equal box 3 minus box 4"):
            _run(acts, run_id="demo.ssa.production.bad-reconciliation")

    def test_production_rejects_spouse_on_single_return(self) -> None:
        acts = _renumber(
            _ssa_acts(
                benefits=[(12000.0, 0.0, 12000.0)],
                ira_amounts=[],
                wages=90000,
                recipient="spouse",
            )
        )
        with self.assertRaisesRegex(SsaBenefitsError, "spouse recipient only"):
            _run(acts, run_id="demo.ssa.production.spouse-single")

    def test_production_rejects_spouse_after_filing_status_correction(self) -> None:
        acts = _ssa_acts(
            benefits=[(12000.0, 0.0, 12000.0)],
            ira_amounts=[],
            wages=90000,
            filing_status="married_filing_jointly",
            recipient="spouse",
        )
        adoption = acts.pop()
        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.ssa.filing-status.correction",
                        "tax.us.2025.filing-status|tax-year=2025",
                        "single",
                    )
                },
            )
        )
        adoption["committed_against"] = len(acts)
        acts.append(adoption)
        with self.assertRaisesRegex(SsaBenefitsError, "spouse recipient only"):
            _run(_renumber(acts), run_id="demo.ssa.production.spouse-correction")

    def test_production_recipient_correction_displaces_both_directions(self) -> None:
        """A recipient correction alone (filing status held fixed) displaces
        the SSA admission decision correctly in both directions."""
        recipient_fact_id = (
            f"{RECIPIENT}|statement=demo.ssa.statement.0,tax-year=2025"
        )

        def _correct_recipient(
            acts: list[dict[str, object]], value: str
        ) -> list[dict[str, object]]:
            acts = list(acts)
            adoption = acts.pop()
            acts.append(
                _act(
                    len(acts),
                    "assertion",
                    {
                        "finding": _attested(
                            "demo.ssa.finding.recipient.0.correction",
                            recipient_fact_id,
                            value,
                        )
                    },
                )
            )
            adoption["committed_against"] = len(acts)
            acts.append(adoption)
            return _renumber(acts)

        original_recipient_finding_id = "demo.ssa.finding.recipient.0"
        correction_finding_id = "demo.ssa.finding.recipient.0.correction"

        def _currency_for(acts: list[dict[str, object]]) -> Any:
            from packages.derivation.loader import DerivationSchemas
            from packages.kernel.currency import compute_currency
            from packages.kernel.findings import project

            # Currency is a projection over the kernel act log alone; drop
            # the trailing package-adoption (a different family's act) so
            # only findings/entities feed the fact/finding projection.
            kernel_acts = [a for a in acts if a.get("kind") != "package-adoption"]
            return compute_currency(project(tuple(kernel_acts), DerivationSchemas().registry))

        # Direction 1: admissible (taxpayer, single) -> inadmissible (spouse
        # correction on a single return).
        base_acts = _ssa_acts(
            benefits=[(12000.0, 0.0, 12000.0)],
            ira_amounts=[],
            wages=90000,
            filing_status="single",
            recipient="taxpayer",
        )
        _, admissible_model = _run(
            _renumber(list(base_acts)), run_id="demo.ssa.repair.recipient.before"
        )
        self.assertEqual(
            float(_published_numeric(admissible_model, "line-6a")), 12000.0
        )
        to_inadmissible = _correct_recipient(base_acts, "spouse")
        currency_to_inadmissible = _currency_for(to_inadmissible)
        self.assertIn(
            original_recipient_finding_id,
            currency_to_inadmissible.displaced_finding_ids,
        )
        self.assertIn(
            correction_finding_id, currency_to_inadmissible.current_finding_ids
        )
        with self.assertRaisesRegex(SsaBenefitsError, "spouse recipient only"):
            _run(
                to_inadmissible,
                run_id="demo.ssa.repair.recipient.to-inadmissible",
            )

        # Direction 2: inadmissible (spouse, single) -> admissible (corrected
        # to taxpayer, still single, no filing-status change involved).
        blocked_acts = _ssa_acts(
            benefits=[(8000.0, 0.0, 8000.0)],
            ira_amounts=[],
            wages=40000,
            filing_status="single",
            recipient="spouse",
        )
        restored = _correct_recipient(blocked_acts, "taxpayer")
        currency_to_admissible = _currency_for(restored)
        self.assertIn(
            original_recipient_finding_id,
            currency_to_admissible.displaced_finding_ids,
        )
        self.assertIn(
            correction_finding_id, currency_to_admissible.current_finding_ids
        )
        _, restored_model = _run(
            restored, run_id="demo.ssa.repair.recipient.to-admissible"
        )
        self.assertEqual(float(_published_numeric(restored_model, "line-6a")), 8000.0)

    def test_package_resolves_v28(self) -> None:
        adoption = _load_fixture_adoption()
        adoption["committed_against"] = 0
        result = resolve_production_package(
            [adoption],
            run_scope=SCOPE,
            scope_user=USER,
            workspace_revision=0,
            surface=_surface(),
        )
        self.assertNotIsInstance(result, Refusal)
        assert not isinstance(result, Refusal)
        self.assertEqual(result.package["version"], "v28")
        members = {(m["id"], m["version"]) for m in result.package["members"]}
        self.assertIn(("tax.us.2025.rule.form1040-line9", "v7"), members)
        self.assertIn(("tax.us.2025.rule.ss-benefits-worksheet", "v1"), members)
        self.assertIn(("tax.us.2025.rule.form1040-line2a", "v3"), members)

    def test_v21_exact_entrypoints_hard_refuse_authenticated_mutations(self) -> None:
        package = _load("package.core-calculations.v28.json")
        self.assertEqual(package["schema"], "artifact-package.v21")
        for mutation in ("stale", "dangling"):
            with self.subTest(mutation=mutation), TemporaryDirectory() as directory:
                surface, acts = _authenticated_v28_mutation_surface(
                    Path(directory), package, mutation
                )
                result = resolve_production_package(
                    acts,
                    run_scope=SCOPE,
                    scope_user=USER,
                    workspace_revision=0,
                    surface=surface,
                )
                self.assertIsInstance(result, Refusal)
                assert isinstance(result, Refusal)
                self.assertEqual(result.reason, "HARD_GATE_REFUSED")
                expected = (
                    "ENTRYPOINT_VERSION_MISMATCH" if mutation == "stale" else "ENTRYPOINT_DANGLING"
                )
                self.assertIn(expected, {issue["code"] for issue in result.issues})

    def test_below_threshold_zero_taxable(self) -> None:
        # Low wages keep W7 under the $25,000 single base → taxable SS = 0.
        acts = _ssa_acts(benefits=[(10000.0, 0.0, 10000.0)], ira_amounts=[], wages=10000)
        for index, act in enumerate(acts):
            act["committed_against"] = index
        report, model = _run(acts, run_id="demo.ssa.below-threshold")
        self.assertEqual(_disposition(model, "line-6a"), "published_value")
        self.assertEqual(_published_numeric(model, "line-6a"), 10000)
        self.assertIn(
            _disposition(model, "line-6b"),
            {"published_value", "computed_zero", "closure_backed_zero"},
        )
        self.assertEqual(_published_numeric(model, "line-6b"), 0)
        self.assertEqual(_disposition(model, "line-6c"), "published_categorical")
        self.assertEqual(_disposition(model, "line-9"), "published_value")
        self.assertGreaterEqual(_published_numeric(model, "line-9"), 0)
        # report symbols published
        symbols = {item.get("symbol") for item in report.get("dispositions", [])}
        self.assertIn(LINE6A, symbols)
        self.assertIn(LINE6B, symbols)
        self.assertIn(TOTAL_INCOME, symbols)

    def test_closed_empty_family_publishes_zero(self) -> None:
        """A closed family with no SSA-1099 members publishes line 6a/6b zero
        under current closure — the affirmative half of the closed-empty /
        open-empty pair (milestone Required evidence: closed-empty family)."""
        acts = _renumber(
            _ssa_acts(benefits=[], ira_amounts=[], wages=15000, close=True)
        )
        _, model = _run(acts, run_id="demo.ssa.repair.closed-empty")
        self.assertEqual(_disposition(model, "line-6a"), "computed_zero")
        self.assertEqual(_published_numeric(model, "line-6a"), 0)
        self.assertEqual(_disposition(model, "line-6b"), "computed_zero")
        self.assertEqual(_published_numeric(model, "line-6b"), 0)

    def test_open_empty_family_blocks(self) -> None:
        """The same empty family with no current closure blocks rather than
        zeroing — the negative half of the pair. Nothing else committed
        distinguishes 'an affirmative closure authorized this zero' from
        'the runner zeroes empty sets'; this pair is what does."""
        acts = _renumber(
            _ssa_acts(benefits=[], ira_amounts=[], wages=15000, close=False)
        )
        _, model = _run(acts, run_id="demo.ssa.repair.open-empty")
        self.assertEqual(_disposition(model, "line-6a"), "blocked")
        self.assertEqual(_disposition(model, "line-6b"), "blocked")
        line6a = _published_numeric(model, "line-6a")
        self.assertIn("DEPENDENCY_ABSENT", line6a.get("activeCodes", []))

    def test_zero_benefits_statement_publishes_zero(self) -> None:
        """A present, reconciled statement whose box 3/4/5 are all zero
        publishes computed zero (a real member, not a closure-backed zero)."""
        acts = _renumber(
            _ssa_acts(benefits=[(0.0, 0.0, 0.0)], ira_amounts=[], wages=15000)
        )
        _, model = _run(acts, run_id="demo.ssa.repair.zero-benefits")
        self.assertEqual(_disposition(model, "line-6a"), "computed_zero")
        self.assertEqual(_published_numeric(model, "line-6a"), 0)
        self.assertEqual(_disposition(model, "line-6b"), "computed_zero")
        self.assertEqual(_published_numeric(model, "line-6b"), 0)

    def test_repayment_equal_to_benefits_publishes_zero(self) -> None:
        """Box 4 repayment exactly equal to box 3 benefits reconciles to a
        zero box 5 and publishes zero, distinct from the excess-repayment
        block case already covered elsewhere."""
        acts = _renumber(
            _ssa_acts(benefits=[(1000.0, 1000.0, 0.0)], ira_amounts=[], wages=15000)
        )
        _, model = _run(acts, run_id="demo.ssa.repair.repayment-equals-benefits")
        self.assertEqual(_disposition(model, "line-6a"), "computed_zero")
        self.assertEqual(_published_numeric(model, "line-6a"), 0)
        self.assertEqual(_disposition(model, "line-6b"), "computed_zero")
        self.assertEqual(_published_numeric(model, "line-6b"), 0)

    def test_member_present_no_closure_publishes(self) -> None:
        """A nonempty family publishes on present-source aggregation without
        any closure at all — closure only ever gates the empty case."""
        acts = _renumber(
            _ssa_acts(
                benefits=[(12000.0, 0.0, 12000.0)],
                ira_amounts=[],
                wages=90000,
                close=False,
            )
        )
        _, model = _run(acts, run_id="demo.ssa.repair.member-no-closure")
        self.assertEqual(_disposition(model, "line-6a"), "published_value")
        self.assertEqual(_published_numeric(model, "line-6a"), 12000.0)
        self.assertEqual(_disposition(model, "line-6b"), "published_value")
        self.assertEqual(_published_numeric(model, "line-6b"), 10200.0)

    def test_taxable_region_publishes_line6b_into_line9(self) -> None:
        # High ordinary income forces inclusion into the 50%/85% region.
        acts = _ssa_acts(benefits=[(12000.0, 0.0, 12000.0)], ira_amounts=[], wages=90000)
        for index, act in enumerate(acts):
            act["committed_against"] = index
        report, model = _run(acts, run_id="demo.ssa.taxable-region")
        self.assertEqual(_disposition(model, "line-6a"), "published_value")
        self.assertEqual(_published_numeric(model, "line-6a"), 12000)
        self.assertEqual(_disposition(model, "line-6b"), "published_value")
        taxable = _published_numeric(model, "line-6b")
        self.assertGreater(taxable, 0)
        self.assertLessEqual(taxable, 12000 * 0.85 + 1e-6)
        self.assertEqual(_disposition(model, "line-9"), "published_value")
        total = _published_numeric(model, "line-9")
        self.assertGreaterEqual(total, taxable)

    def test_worksheet_pin_table_excludes_line9_cycle(self) -> None:
        rule = _load("rule.ss-benefits-worksheet.json")
        pin_ids = {p["id"] for p in rule["pins"]}
        self.assertNotIn("tax.us.2025.income.total-income", pin_ids)
        self.assertNotIn(LINE6B, pin_ids)
        self.assertNotIn("tax.us.2025.agi", pin_ids)
        # required components present once
        for symbol in (
            "tax.us.2025.wages.total-w2-box1",
            "tax.us.2025.interest.taxable-total",
            "tax.us.2025.dividends.ordinary-total",
            "tax.us.2025.ira.distributions.line4b",
            "tax.us.2025.capital-gains.line7a-total",
            "tax.us.2025.income.additional-income",
            "tax.us.2025.tax-exempt-interest.line2a-total",
            LINE6A,
        ):
            self.assertIn(symbol, pin_ids)
            self.assertEqual(sum(1 for p in rule["pins"] if p["id"] == symbol), 1)

    def test_line9_v7_includes_line6b_once(self) -> None:
        rule = _load("rule.form1040-line9.v7.json")
        refs = [a["name"] for a in rule["value"]["args"]]
        self.assertEqual(refs.count(LINE6B), 1)
        self.assertNotIn(LINE2A, refs)
        self.assertIn("tax.us.2025.ira.distributions.line4b", refs)

    def test_line2a_v3_drops_ss_residual(self) -> None:
        rule = _load("rule.form1040-line2a.v3.json")
        self.assertNotIn(
            "tax.us.2025.line2a-scope.no-taxable-social-security", rule["requires"]
        )
        pin_ids = {p["id"] for p in rule["pins"]}
        self.assertNotIn(
            "tax.us.2025.line2a-scope.no-taxable-social-security", pin_ids
        )

    def test_package_additive_only(self) -> None:
        v26 = _load("package.core-calculations.v26.json")
        v27 = _load("package.core-calculations.v27.json")
        v28 = _load("package.core-calculations.v28.json")
        for earlier, later in ((v26, v27), (v27, v28)):
            old_ids = {m["id"] for m in earlier["members"]}
            new_ids = {m["id"] for m in later["members"]}
            self.assertEqual(old_ids - new_ids, set())
            self.assertEqual(
                earlier["composition_obligations"], later["composition_obligations"]
            )
        self.assertIn(
            "tax.us.2025.rule.ss-benefits-worksheet",
            {m["id"] for m in v28["members"]},
        )
        self.assertEqual(
            next(
                m["version"]
                for m in v28["members"]
                if m["id"] == "tax.us.2025.rule.form1040-line9"
            ),
            "v7",
        )
        self.assertEqual(
            next(
                m["version"]
                for m in v28["members"]
                if m["id"] == "demo.parameter.tax-brackets.2025"
            ),
            "v2",
        )
        self.assertEqual(v27["package_checksum"], package_instance_checksum(v27))
        self.assertEqual(v28["package_checksum"], package_instance_checksum(v28))
        brackets = _load("parameter.tax-brackets.v2.json")
        self.assertEqual(
            set(brackets["values"]),
            {
                "single",
                "married_filing_jointly",
                "married_filing_separately",
                "head_of_household",
                "qualifying_surviving_spouse",
            },
        )

    def test_manifest_only_adds(self) -> None:
        v21 = _load("published-packages.v21.json")
        v22 = _load("published-packages.v22.json")
        v23 = _load("published-packages.v23.json")
        for earlier, later in ((v21, v22), (v22, v23)):
            old_c = {(c["id"], c["version"]) for c in earlier["citizens"]}
            new_c = {(c["id"], c["version"]) for c in later["citizens"]}
            self.assertTrue(old_c.issubset(new_c))
            old_p = {(p["id"], p["version"]) for p in earlier["packages"]}
            new_p = {(p["id"], p["version"]) for p in later["packages"]}
            self.assertTrue(old_p.issubset(new_p))
        new_p = {(p["id"], p["version"]) for p in v23["packages"]}
        self.assertIn(("tax.us.2025.package.core-calculations", "v27"), new_p)
        self.assertIn(("tax.us.2025.package.core-calculations", "v28"), new_p)



    def test_all_filing_statuses_close_line16(self) -> None:
        """Every plan-supported filing status reaches line 16 without LOOKUP_MISS."""
        statuses = (
            ("single", None),
            ("married_filing_jointly", None),
            ("head_of_household", None),
            ("qualifying_surviving_spouse", None),
            ("married_filing_separately", "yes"),
            ("married_filing_separately", "no"),
        )
        for status, lived in statuses:
            with self.subTest(status=status, lived=lived):
                acts = _ssa_acts(
                    benefits=[(12000.0, 0.0, 12000.0)],
                    ira_amounts=[],
                    wages=90000,
                    filing_status=status,
                    mfs_lived_apart=lived,
                )
                for index, act in enumerate(acts):
                    act["committed_against"] = index
                report, model = _run(acts, run_id=f"demo.ssa.status.{status}.{lived}")
                self.assertEqual(_disposition(model, "line-6a"), "published_value")
                self.assertEqual(_disposition(model, "line-6b"), "published_value")
                self.assertEqual(_disposition(model, "line-9"), "published_value")
                self.assertEqual(_disposition(model, "line-16"), "published_value")
                self.assertGreaterEqual(_published_numeric(model, "line-16"), 0)

    def test_mfs_lived_apart_checks_line6d(self) -> None:
        acts = _ssa_acts(
            benefits=[(12000.0, 0.0, 12000.0)],
            ira_amounts=[],
            wages=90000,
            filing_status="married_filing_separately",
            mfs_lived_apart="yes",
        )
        for index, act in enumerate(acts):
            act["committed_against"] = index
        _, model = _run(acts, run_id="demo.ssa.mfs.apart")
        self.assertEqual(_disposition(model, "line-6d"), "published_categorical")
        self.assertEqual(
            _disposition(model, "line-6d-not-checked"), "guard_inapplicable"
        )

    def test_mfs_lived_with_not_checked_line6d(self) -> None:
        acts = _ssa_acts(
            benefits=[(12000.0, 0.0, 12000.0)],
            ira_amounts=[],
            wages=90000,
            filing_status="married_filing_separately",
            mfs_lived_apart="no",
        )
        for index, act in enumerate(acts):
            act["committed_against"] = index
        _, model = _run(acts, run_id="demo.ssa.mfs.with")
        self.assertEqual(
            _disposition(model, "line-6d-not-checked"), "published_categorical"
        )
        self.assertEqual(_disposition(model, "line-6d"), "guard_inapplicable")

    def test_mfs_missing_living_arrangement_blocks(self) -> None:
        acts = _ssa_acts(
            benefits=[(12000.0, 0.0, 12000.0)],
            ira_amounts=[],
            wages=90000,
            filing_status="married_filing_separately",
            mfs_lived_apart=None,
        )
        for index, act in enumerate(acts):
            act["committed_against"] = index
        report, model = _run(acts, run_id="demo.ssa.mfs.missing")
        # Worksheet requires living arrangement under MFS → line 6b blocked.
        self.assertEqual(_disposition(model, "line-6b"), "blocked")
        symbols = {
            item.get("symbol"): item
            for item in report.get("dispositions", [])
            if item.get("artifact_id") == "tax.us.2025.rule.ss-benefits-worksheet"
        }
        self.assertTrue(symbols or _disposition(model, "line-6b") == "blocked")

    def test_joint_taxpayer_and_spouse_aggregate_once(self) -> None:
        acts = _ssa_acts(
            benefits=[
                (8000.0, 0.0, 8000.0),
                (4000.0, 0.0, 4000.0),
            ],
            ira_amounts=[],
            wages=20000,
            filing_status="married_filing_jointly",
        )
        # Second statement recipient spouse
        # Patch second statement recipient to spouse after build
        for act in acts:
            finding = cast(
                dict[str, Any],
                cast(dict[str, Any], act.get("payload", {})).get("finding", {}),
            )
            fact_id = str(finding.get("fact_id", ""))
            if (
                fact_id.startswith(RECIPIENT + "|")
                and "demo.ssa.statement.1" in fact_id
            ):
                finding["value"] = "spouse"
        for index, act in enumerate(acts):
            act["committed_against"] = index
        _, model = _run(acts, run_id="demo.ssa.joint.aggregate")
        self.assertEqual(_published_numeric(model, "line-6a"), 12000)

    def test_tax_exempt_interest_raises_6b_not_line9(self) -> None:
        base_acts = _ssa_acts(
            benefits=[(10000.0, 0.0, 10000.0)],
            ira_amounts=[],
            wages=20000,
            tax_exempt=None,
        )
        te_acts = _ssa_acts(
            benefits=[(10000.0, 0.0, 10000.0)],
            ira_amounts=[],
            wages=20000,
            tax_exempt=15000.0,
        )
        for acts in (base_acts, te_acts):
            for index, act in enumerate(acts):
                act["committed_against"] = index
        base_report, base_model = _run(base_acts, run_id="demo.ssa.te.base")
        te_report, te_model = _run(te_acts, run_id="demo.ssa.te.positive")
        base_6b = _published_numeric(base_model, "line-6b")
        te_6b = _published_numeric(te_model, "line-6b")
        self.assertGreater(te_6b, base_6b)
        base_9 = _published_numeric(base_model, "line-9")
        te_9 = _published_numeric(te_model, "line-9")
        # Line 9 rises only by the taxable-SS delta, never by tax-exempt interest.
        self.assertEqual(te_9 - base_9, te_6b - base_6b)
        # Preferential / tax-exempt path: line 2a must not enter line 9 args
        line9 = _load("rule.form1040-line9.v7.json")
        self.assertNotIn(LINE2A, [a["name"] for a in line9["value"]["args"]])

    def test_downstream_agi_ti_line16_recompute(self) -> None:
        acts = _ssa_acts(
            benefits=[(12000.0, 0.0, 12000.0)],
            ira_amounts=[],
            wages=90000,
        )
        for index, act in enumerate(acts):
            act["committed_against"] = index
        _, model = _run(acts, run_id="demo.ssa.downstream")
        line9 = _published_numeric(model, "line-9")
        line6b = _published_numeric(model, "line-6b")
        line6a = _published_numeric(model, "line-6a")
        self.assertEqual(line6a, 12000)
        self.assertGreater(line6b, 0)
        self.assertGreaterEqual(line9, line6b)
        self.assertEqual(_disposition(model, "line-11"), "published_value")
        self.assertEqual(_disposition(model, "line-15"), "published_value")
        self.assertEqual(_disposition(model, "line-16"), "published_value")
        # AGI equals total income when no above-the-line adjustments are present.
        self.assertEqual(
            _published_numeric(model, "line-11"), _published_numeric(model, "line-9")
        )

    def test_line6d_not_checked_field_binds_symbol(self) -> None:
        field = _load("form1040.line-6d-not-checked.form-field.json")
        self.assertEqual(
            field["binds_symbol"], "tax.us.2025.social-security.line6d-not-checked"
        )
        self.assertEqual(field["dispositions"]["published_value"]["render"], "not_checked")
        pkg = _load("package.core-calculations.v28.json")
        self.assertIn(
            {
                "id": "tax.us.2025.form1040.line-6d-not-checked",
                "role": "form-field",
                "schema": "form-field.v3",
                "version": "v1",
            },
            pkg["members"],
        )

class TestSsaArithmeticReference(unittest.TestCase):
    """Paper arithmetic reference for W1–W18 without live graph."""

    def _taxable(
        self,
        w1: Decimal,
        ordinary: Decimal,
        tax_exempt: Decimal,
        base: Decimal,
        tier2: Decimal,
    ) -> Decimal:
        w2 = w1 * Decimal("0.5")
        w5 = w2 + ordinary + tax_exempt
        w7 = max(w5 - Decimal(0), Decimal(0))
        w9 = max(w7 - base, Decimal(0))
        if w9 == 0:
            return Decimal(0)
        w11 = max(w9 - tier2, Decimal(0))
        w12 = min(w9, tier2)
        w13 = w12 * Decimal("0.5")
        w14 = min(w2, w13)
        w15 = w11 * Decimal("0.85")
        w16 = w14 + w15
        w17 = w1 * Decimal("0.85")
        return min(w16, w17)

    def test_regions(self) -> None:
        # below threshold
        self.assertEqual(
            self._taxable(Decimal(5000), Decimal(10000), Decimal(0), Decimal(25000), Decimal(9000)),
            Decimal(0),
        )
        # 50% region
        t = self._taxable(Decimal(12000), Decimal(30000), Decimal(0), Decimal(25000), Decimal(9000))
        # w2=6000, w5=36000, w7=36000, w9=11000, w11=2000, w12=9000, w13=4500, w14=4500, w15=1700, w16=6200, w17=10200 -> 6200
        self.assertEqual(t, Decimal("6200"))
        # 85% cap
        t2 = self._taxable(Decimal(30000), Decimal(100000), Decimal(0), Decimal(25000), Decimal(9000))
        self.assertEqual(t2, Decimal("25500"))  # 0.85 * 30000




class TestSsaVerificationRepair(unittest.TestCase):
    """Required-evidence matrix completion for the verification repair charter."""

    def _ordinary_from_model(self, model: dict[str, Any]) -> float:
        """Sum worksheet ordinary-income components from presentation when present."""
        parts = []
        for section_id in ("line-1a", "line-2b", "line-3b", "line-4b", "line-7a", "line-8"):
            try:
                parts.append(float(_published_numeric(model, section_id) or 0))
            except Exception:
                parts.append(0.0)
        return sum(parts)

    def test_live_worksheet_regions_and_85_cap(self) -> None:
        """Distinct live regions: zero, threshold, 50%, 50→85 boundary, 85% non-cap, cap."""
        cases = [
            # label, wages, benefits, checks
            ("zero_below_threshold", 10000.0, 10000.0, "zero"),
            # Exactly at base threshold: W7 == 25000 → W9 == 0.
            # W1=10000,W2=5000,W3=20000 → W5=25000.
            ("threshold_exact", 20000.0, 10000.0, "zero"),
            # First-tier only: 0 < W9 <= 9000.
            ("fifty_region", 20000.0, 12000.0, "fifty"),
            # Exactly at 50→85 transition: W9 == 9000.
            # W1=12000,W2=6000; need W7=34000 → W3=28000.
            ("transition_boundary", 28000.0, 12000.0, "transition_edge"),
            # 85% inclusion active but below statutory cap.
            ("eighty_five_non_cap", 30000.0, 20000.0, "eighty_five"),
            # Statutory 85% of benefits cap binds.
            ("eighty_five_cap", 40000.0, 12000.0, "cap"),
        ]
        for label, wages, benefits, region in cases:
            with self.subTest(label=label):
                acts = _renumber(
                    _ssa_acts(
                        benefits=[(benefits, 0.0, benefits)],
                        ira_amounts=[],
                        wages=wages,
                    )
                )
                _, model = _run(acts, run_id=f"demo.ssa.region.{label}")
                line6a = float(_published_numeric(model, "line-6a"))
                line6b = float(_published_numeric(model, "line-6b"))
                ordinary = self._ordinary_from_model(model)
                expected = _expected_taxable_ss(line6a, ordinary, 0.0)
                self.assertEqual(line6a, benefits)
                self.assertEqual(line6b, expected)
                w2 = 0.5 * benefits
                w7 = w2 + ordinary
                w9 = max(w7 - 25000.0, 0.0)
                w11 = max(w9 - 9000.0, 0.0)
                w17 = 0.85 * benefits
                if region == "zero":
                    self.assertEqual(line6b, 0)
                    self.assertEqual(w9, 0.0)
                elif region == "fifty":
                    self.assertGreater(line6b, 0)
                    self.assertLessEqual(w9, 9000.0 + 1e-6)
                    self.assertEqual(w11, 0.0)
                    self.assertLessEqual(line6b, benefits * 0.5 + 1e-6)
                elif region == "transition_edge":
                    self.assertAlmostEqual(w9, 9000.0, places=0)
                    self.assertEqual(w11, 0.0)
                    self.assertGreater(line6b, 0)
                elif region == "eighty_five":
                    # 85% slice active (W11>0) but statutory cap W17 does not bind.
                    self.assertGreater(w11, 0.0)
                    self.assertLess(line6b, w17 - 1e-6)
                    self.assertGreater(line6b, 0.0)
                elif region == "cap":
                    self.assertEqual(line6b, round(w17))
                    self.assertGreaterEqual(w11, 0.0)

    def test_exact_once_components_and_tax_exempt_outside_line9(self) -> None:
        worksheet = _load("rule.ss-benefits-worksheet.json")
        pin_ids = [p["id"] for p in worksheet["pins"]]
        required = [
            "tax.us.2025.wages.total-w2-box1",
            "tax.us.2025.interest.taxable-total",
            "tax.us.2025.dividends.ordinary-total",
            "tax.us.2025.ira.distributions.line4b",
            "tax.us.2025.capital-gains.line7a-total",
            "tax.us.2025.income.additional-income",
            "tax.us.2025.tax-exempt-interest.line2a-total",
            LINE6A,
        ]
        for symbol in required:
            self.assertEqual(pin_ids.count(symbol), 1, symbol)
        self.assertEqual(pin_ids.count(LINE6B), 0)
        self.assertEqual(pin_ids.count(TOTAL_INCOME), 0)

        line9 = _load("rule.form1040-line9.v7.json")
        args = [a["name"] for a in line9["value"]["args"]]
        self.assertEqual(args.count(LINE6B), 1)
        self.assertNotIn(LINE2A, args)
        for symbol in (
            "tax.us.2025.wages.total-w2-box1",
            "tax.us.2025.interest.taxable-total",
            "tax.us.2025.dividends.ordinary-total",
            "tax.us.2025.ira.distributions.line4b",
            "tax.us.2025.capital-gains.line7a-total",
            "tax.us.2025.income.additional-income",
        ):
            self.assertEqual(args.count(symbol), 1, symbol)

        pref = _load("rule.selected-preferential-base.v4.json")
        pref_blob = json.dumps(pref)
        self.assertNotIn(LINE6B, pref_blob)
        self.assertNotIn("social-security", pref_blob)

        base_kw: dict[str, Any] = dict(
            benefits=[(12000.0, 0.0, 12000.0)],
            ira_amounts=[],
            wages=20000.0,
        )
        _, base_model = _run(
            _renumber(_ssa_acts(**base_kw)), run_id="demo.ssa.once.base"
        )
        base_6b = float(_published_numeric(base_model, "line-6b"))
        base_9 = float(_published_numeric(base_model, "line-9"))

        def _delta_case(label: str, extra: dict[str, Any], section: str, amount: float) -> None:
            acts = _renumber(_ssa_acts(**{**base_kw, **extra}))
            _, model = _run(acts, run_id=f"demo.ssa.once.{label}")
            self.assertEqual(float(_published_numeric(model, section)), amount, label)
            new_6b = float(_published_numeric(model, "line-6b"))
            new_9 = float(_published_numeric(model, "line-9"))
            self.assertGreaterEqual(new_6b, base_6b, label)
            # Ordinary components enter line 9 once and also feed the worksheet once.
            self.assertEqual(new_9 - base_9, amount + (new_6b - base_6b), label)

        _delta_case("interest", {"interest": 3000.0}, "line-2b", 3000.0)
        _delta_case(
            "ordinary-div",
            {"ordinary_dividends": 2500.0},
            "line-3b",
            2500.0,
        )
        _delta_case("ira", {"ira_amounts": [5000.0]}, "line-4b", 5000.0)
        _delta_case(
            "cap-gains",
            {"capital_gains": 1500.0},
            "line-7a",
            1500.0,
        )
        _delta_case(
            "unemployment",
            {"unemployment": 2000.0},
            "line-8",
            2000.0,
        )

        # Qualified dividends: publish on line 3a; ordinary box-1a on line 3b.
        # Preferential path lowers line 16 vs ordinary-only tax; QD does not add a
        # second ordinary amount into line 6b / line 9 beyond box-1a.
        qd_acts = _renumber(
            _ssa_acts(
                **base_kw,
                ordinary_dividends=1000.0,
                qualified_dividends=400.0,
            )
        )
        _, qd_model = _run(qd_acts, run_id="demo.ssa.once.qd")
        # Committed production-shaped QD evidence (exact values).
        self.assertEqual(_disposition(qd_model, "line-3a"), "published_value")
        self.assertEqual(float(_published_numeric(qd_model, "line-3a")), 400.0)
        self.assertEqual(float(_published_numeric(qd_model, "line-3b")), 1000.0)
        self.assertEqual(float(_published_numeric(qd_model, "line-6b")), 1000.0)
        self.assertEqual(float(_published_numeric(qd_model, "line-9")), 22000.0)
        # Preferential-tax path publishes line 16 for this QD corpus.
        self.assertEqual(_disposition(qd_model, "line-16"), "published_value")
        self.assertEqual(float(_published_numeric(qd_model, "line-16")), 700.0)
        # Ordinary-only control: QD does not change line 6b / line 9 beyond box-1a.
        ord_only_acts = _renumber(
            _ssa_acts(**base_kw, ordinary_dividends=1000.0, qualified_dividends=None)
        )
        _, ord_model = _run(ord_only_acts, run_id="demo.ssa.once.ord-only")
        self.assertEqual(float(_published_numeric(ord_model, "line-6b")), 1000.0)
        self.assertEqual(float(_published_numeric(ord_model, "line-9")), 22000.0)
        # Preferential base must not list taxable Social Security.
        self.assertNotIn(LINE6B, json.dumps(_load("rule.selected-preferential-base.v4.json")))

        # Tax-exempt changes 6b only (not added to line 9 as its own term).
        te_acts = _renumber(_ssa_acts(**base_kw, tax_exempt=10000.0))
        _, te_model = _run(te_acts, run_id="demo.ssa.once.te")
        te_6b = float(_published_numeric(te_model, "line-6b"))
        te_9 = float(_published_numeric(te_model, "line-9"))
        self.assertGreater(te_6b, base_6b)
        self.assertEqual(te_9 - base_9, te_6b - base_6b)
        self.assertEqual(_published_numeric(te_model, "line-2a"), 10000)

    def test_production_distinct_statements_aggregate_as_two_members(self) -> None:
        """Two separately furnished SSA-1099s get distinct statement entities
        and aggregate as two members, not one (production admission boundary,
        not the removed isolated helper)."""
        acts = _renumber(
            _ssa_acts(
                benefits=[(1000.0, 0.0, 1000.0), (2500.0, 0.0, 2500.0)],
                ira_amounts=[],
                wages=10000,
            )
        )
        _, model = _run(acts, run_id="demo.ssa.repair.distinct-members")
        self.assertEqual(float(_published_numeric(model, "line-6a")), 3500.0)

    def test_production_correction_preserves_identity_and_displaces(self) -> None:
        """A same-statement correction supersedes the prior finding at the
        production boundary and carries exact displacement pins (mirrors
        the K-1 ADR-0015-adjacent correction proof pattern)."""
        acts = _ssa_acts(benefits=[(1000.0, 0.0, 1000.0)], ira_amounts=[], wages=10000)
        adoption = acts.pop()
        correction_box3 = _act(
            len(acts),
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.finding.box3.0.correction",
                    f"{BOX3}|statement=demo.ssa.statement.0,tax-year=2025",
                    1500.0,
                )
            },
        )
        correction_box5 = _act(
            len(acts) + 1,
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.finding.box5.0.correction",
                    f"{BOX5}|statement=demo.ssa.statement.0,tax-year=2025",
                    1500.0,
                )
            },
        )
        acts = acts + [correction_box3, correction_box5]

        from packages.derivation.loader import DerivationSchemas
        from packages.kernel.currency import compute_currency
        from packages.kernel.findings import project

        currency = compute_currency(project(tuple(acts), DerivationSchemas().registry))
        self.assertIn("demo.ssa.finding.box5.0", currency.displaced_finding_ids)
        self.assertIn(
            "demo.ssa.finding.box5.0.correction", currency.current_finding_ids
        )
        self.assertIn("demo.ssa.finding.box3.0", currency.displaced_finding_ids)
        self.assertIn(
            "demo.ssa.finding.box3.0.correction", currency.current_finding_ids
        )

        adoption["committed_against"] = len(acts)
        acts.append(adoption)
        _, model = _run(_renumber(acts), run_id="demo.ssa.repair.correction")
        self.assertEqual(float(_published_numeric(model, "line-6a")), 1500.0)

    def test_production_duplicate_identity_blocks(self) -> None:
        """Logical statement identity is the admitted entity itself
        (ratified 2026-08-09): re-introducing the same statement entity id
        blocks rather than silently collapsing."""
        from packages.kernel.facts import FactModelError

        acts = _ssa_acts(benefits=[(1000.0, 0.0, 1000.0)], ira_amounts=[], wages=10000)
        adoption = acts.pop()
        acts.append(
            _act(
                len(acts),
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": "demo.ssa.statement.0",
                        "kind": "tax.us.ssa1099-statement",
                        "label": "Duplicate synthetic Form SSA-1099",
                    }
                },
            )
        )
        adoption["committed_against"] = len(acts)
        acts.append(adoption)
        with self.assertRaisesRegex(
            FactModelError, "entity already exists: demo.ssa.statement.0"
        ):
            _run(_renumber(acts), run_id="demo.ssa.repair.duplicate-entity")

    def test_production_conflicting_correction_blocks(self) -> None:
        """A correction that leaves box 5 no longer reconciled with box 3
        minus box 4 blocks at the production admission boundary."""
        acts = _ssa_acts(benefits=[(1000.0, 0.0, 1000.0)], ira_amounts=[], wages=10000)
        adoption = acts.pop()
        acts.append(
            _act(
                len(acts),
                "assertion",
                {
                    "finding": _attested(
                        "demo.ssa.finding.box5.0.conflicting-correction",
                        f"{BOX5}|statement=demo.ssa.statement.0,tax-year=2025",
                        1600.0,
                    )
                },
            )
        )
        adoption["committed_against"] = len(acts)
        acts.append(adoption)
        with self.assertRaisesRegex(SsaBenefitsError, "box 5 to equal box 3 minus box 4"):
            _run(_renumber(acts), run_id="demo.ssa.repair.conflicting-correction")

    def test_recipient_suffix_missing_tax_year_fails_closed(self) -> None:
        """``validate_projected_source_boundary`` (the exact production
        function called from ``live.py``) must fail closed, not silently
        default to tax year 2025, when a spouse-recipient suffix carries no
        ``tax-year=`` component. Every fact id admitted through the real
        kernel always carries one (the fact type's declared identity keys
        always include it), so this exercises the function directly with a
        hand-built adversarial finding set — the guard's removal (reverting
        to the old ``tax_year or '2025'`` silent default) makes this test
        fail because a differently-keyed filing status would then be read."""
        from packages.tax.ssa_benefits import validate_projected_source_boundary

        findings: list[dict[str, object]] = [
            {
                "fact_id": "tax.us.2025.ssa1099.box5-net-benefits|statement=demo.ssa.statement.0",
                "value": 1000.0,
            },
            {
                "fact_id": "tax.us.2025.ssa1099.box3-benefits-paid|statement=demo.ssa.statement.0",
                "value": 1000.0,
            },
            {
                "fact_id": "tax.us.2025.ssa1099.box4-repayment|statement=demo.ssa.statement.0",
                "value": 0.0,
            },
            {
                "fact_id": "tax.us.2025.ssa1099.recipient|statement=demo.ssa.statement.0",
                "value": "spouse",
            },
            # A filing-status finding that would wrongly appear authoritative
            # under the old silent '2025' default, even though this suffix
            # names no tax year at all.
            {"fact_id": "tax.us.2025.filing-status|tax-year=2025", "value": "married_filing_jointly"},
        ]
        with self.assertRaisesRegex(
            SsaBenefitsError, "requires an explicit tax-year key"
        ):
            validate_projected_source_boundary(findings)

    def test_production_stale_correction_blocks(self) -> None:
        """A membership correction citing a superseded (stale) predecessor
        horizon is rejected atomically before any member mutation."""
        from packages.derivation.loader import DerivationSchemas
        from packages.kernel.findings import project
        from packages.kernel.horizons import HorizonModelError

        acts = _ssa_acts(benefits=[(1000.0, 0.0, 1000.0)], ira_amounts=[], wages=10000)
        adoption = acts.pop()

        statement = "demo.ssa.statement.late"
        acts.append(
            _act(
                len(acts),
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": statement,
                        "kind": "tax.us.ssa1099-statement",
                        "label": "Late synthetic Form SSA-1099",
                    }
                },
            )
        )
        for fact_type, value, suffix in (
            (BOX3, 500.0, "box3"),
            (BOX4, 0, "box4"),
            (BOX6, 0, "box6"),
            (RECIPIENT, "taxpayer", "recipient"),
            (KIND, "ssa-1099", "kind"),
            (LUMP, False, "lump"),
        ):
            acts.append(
                _act(
                    len(acts),
                    "assertion",
                    {
                        "finding": _attested(
                            f"demo.ssa.finding.{suffix}.late",
                            f"{fact_type}|statement={statement},tax-year=2025",
                            value,
                        )
                    },
                )
            )
        # First membership transition genuinely advances the horizon h0 -> h1.
        acts.append(
            _act(
                len(acts),
                "member-transition",
                {
                    "family": {"id": FAMILY, "version": "v1"},
                    "scope": SCOPE_KEY,
                    "member": {
                        "action": "assert",
                        "finding": _attested(
                            "demo.ssa.finding.box5.late",
                            f"{BOX5}|statement={statement},tax-year=2025",
                            500.0,
                        ),
                    },
                    "successor": {
                        "id": "demo.ssa.h.late.repair",
                        "predecessor": "demo.ssa.h0",
                    },
                },
            )
        )
        # Second transition citing the now-superseded original horizon as
        # predecessor is a stale correction: it must block, not silently
        # apply against out-of-date membership state.
        stale_acts = acts + [
            _act(
                len(acts),
                "member-transition",
                {
                    "family": {"id": FAMILY, "version": "v1"},
                    "scope": SCOPE_KEY,
                    "member": {
                        "action": "assert",
                        "finding": _attested(
                            "demo.ssa.finding.box5.late.stale-attempt",
                            f"{BOX5}|statement={statement}-2,tax-year=2025",
                            600.0,
                        ),
                    },
                    "successor": {
                        "id": "demo.ssa.h.late.repair.2",
                        "predecessor": "demo.ssa.h0",
                    },
                },
            )
        ]
        with self.assertRaisesRegex(HorizonModelError, "wrong predecessor"):
            project(tuple(_renumber(stale_acts)), DerivationSchemas().registry)

    def test_production_evidence_replacement_does_not_rekey_fact(self) -> None:
        """Replacing the evidence behind a documentary SSA-1099 finding
        leaves the finding's fact identity and value untouched (ADR-0015
        decision 2/consequence, proved here for the SSA family)."""
        acts = _ssa_acts(benefits=[(1000.0, 0.0, 1000.0)], ira_amounts=[], wages=10000)
        # Rewrite statement 0's box5 finding to a documentary basis citing
        # freshly submitted evidence, inserted just before that assertion.
        evidence_id = "demo.ssa.evidence.0"
        box5_fact_id = f"{BOX5}|statement=demo.ssa.statement.0,tax-year=2025"
        box5_index = next(
            i
            for i, act in enumerate(acts)
            if cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("finding", {})).get("fact_id")
            == box5_fact_id
        )
        acts.insert(
            box5_index,
            _act(
                0,
                "evidence-submitted",
                {
                    "evidence": {
                        "schema": "evidence.v1",
                        "id": evidence_id,
                        "kind": "demo.statement.ssa1099",
                        "label": "Synthetic Form SSA-1099 box 5 evidence",
                        "content": {"value": 1000.0},
                    }
                },
            ),
        )
        box5_finding = cast(
            dict[str, Any],
            cast(dict[str, Any], acts[box5_index + 1].get("payload", {})).get("finding", {}),
        )
        box5_finding["basis"] = "documentary"
        box5_finding["evidence_ids"] = [evidence_id]
        adoption = acts.pop()
        acts.append(
            _act(
                len(acts),
                "evidence-replaced",
                {
                    "evidence_id": evidence_id,
                    "replacement": {
                        "schema": "evidence.v1",
                        "id": "demo.ssa.evidence.0.v2",
                        "kind": "demo.statement.ssa1099",
                        "label": "Synthetic Form SSA-1099 box 5 evidence, rescanned",
                        "content": {"value": 1000.0},
                    },
                },
            )
        )

        from packages.derivation.loader import DerivationSchemas
        from packages.kernel.findings import project

        acts = _renumber(acts)
        state = project(tuple(acts), DerivationSchemas().registry)
        # The finding's fact identity and value are untouched by the evidence
        # lifecycle event: evidence replacement is not a correction.
        finding = state.findings["demo.ssa.finding.box5.0"]
        self.assertEqual(finding["fact_id"], box5_fact_id)
        self.assertEqual(finding["value"], 1000.0)
        self.assertEqual(finding["evidence_ids"], [evidence_id])
        self.assertEqual(state.evidence[evidence_id].status, "replaced")

        adoption["committed_against"] = len(acts)
        acts.append(adoption)
        _, model = _run(_renumber(acts), run_id="demo.ssa.repair.evidence-replace")
        self.assertEqual(float(_published_numeric(model, "line-6a")), 1000.0)

    def test_live_late_member_stale_closure_and_reclosure(self) -> None:
        """Closure freshness (ADR-0017): a closed-empty family's zero cannot
        survive a horizon that has moved past the closure it stood on.

        Closure only ever gates the *empty* collect (``packages/derivation/
        evaluator.py``): a nonempty family aggregates present members and
        never consults closure at all, so a lifecycle built only on a
        nonempty family cannot witness freshness. This test carries the
        family through closed-empty -> late real member (nonempty, no
        closure needed) -> member withdrawn (empty again, but on a horizon
        the h0 closure never attested) -> reclosed, and asserts a different
        disposition at each step. Unlike the test this replaces, the
        assertions here would not all pass unchanged if closure freshness
        were not honoured: with the h0 closure finding still authorizing an
        empty result on a horizon it was never attested against, the third
        run below would wrongly publish a computed/closure zero instead of
        blocking (verified against a build with both freshness paths
        disabled: currency's entity-supersession displacement of the h0
        closure finding, and ``resolve_closure_admissions``'s horizon-match
        check)."""
        # Step 1: closed-empty family — zero authorized only by current
        # closure on h0.
        acts = _ssa_acts(benefits=[], ira_amounts=[], wages=15000, close=True)
        adoption = acts.pop()
        _, model1 = _run(
            _renumber(list(acts) + [adoption]), run_id="demo.ssa.late.closed-empty"
        )
        self.assertEqual(_disposition(model1, "line-6a"), "computed_zero")
        self.assertEqual(_published_numeric(model1, "line-6a"), 0)

        # Step 2: a late member enters through a member-transition on the
        # box 5 member-predicate fact itself (the family's real member
        # predicate, not box 3), with companions asserted first so
        # companion-presence admits it, and a horizon successor h.late
        # recording the membership change (ADR-0017 decision 3).
        statement = "demo.ssa.statement.late"
        acts2 = list(acts)
        acts2.append(
            _act(
                len(acts2),
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": statement,
                        "kind": "tax.us.ssa1099-statement",
                        "label": "Late synthetic Form SSA-1099",
                    }
                },
            )
        )
        for fact_type, value, suffix in (
            (BOX3, 4000.0, "box3"),
            (BOX4, 0.0, "box4"),
            (BOX6, 0, "box6"),
            (RECIPIENT, "taxpayer", "recipient"),
            (KIND, "ssa-1099", "kind"),
            (LUMP, False, "lump"),
        ):
            acts2.append(
                _act(
                    len(acts2),
                    "assertion",
                    {
                        "finding": _attested(
                            f"demo.ssa.finding.{suffix}.late",
                            f"{fact_type}|statement={statement},tax-year=2025",
                            value,
                        )
                    },
                )
            )
        acts2.append(
            _act(
                len(acts2),
                "member-transition",
                {
                    "family": {"id": FAMILY, "version": "v1"},
                    "scope": SCOPE_KEY,
                    "member": {
                        "action": "assert",
                        "finding": _attested(
                            "demo.ssa.finding.box5.late",
                            f"{BOX5}|statement={statement},tax-year=2025",
                            4000.0,
                        ),
                    },
                    "successor": {
                        "id": "demo.ssa.h.late",
                        "predecessor": "demo.ssa.h0",
                    },
                },
            )
        )
        _, model2 = _run(
            _renumber(list(acts2) + [_load_fixture_adoption()]),
            run_id="demo.ssa.late.present-source",
        )
        self.assertEqual(_disposition(model2, "line-6a"), "published_value")
        self.assertEqual(_published_numeric(model2, "line-6a"), 4000.0)

        # State check: horizon succession displaced the h0 closure finding
        # (ADR-0017 decision 5) — the exact mechanism that stops it from
        # re-authorizing an empty zero once the family becomes empty again.
        from packages.derivation.loader import DerivationSchemas
        from packages.kernel.currency import compute_currency
        from packages.kernel.findings import project

        currency = compute_currency(project(tuple(acts2), DerivationSchemas().registry))
        self.assertIn("demo.ssa.closure", currency.displaced_finding_ids)
        self.assertNotIn("demo.ssa.closure", currency.current_finding_ids)

        # Step 3: withdraw the late member (a second membership-changing
        # transition, successor h.late2). The family is empty again, but on
        # a horizon no closure has ever attested — this is the state that
        # actually distinguishes stale from fresh. If freshness were not
        # honoured, this would wrongly publish zero instead of blocking.
        acts3 = list(acts2)
        acts3.append(
            _act(
                len(acts3),
                "member-transition",
                {
                    "family": {"id": FAMILY, "version": "v1"},
                    "scope": SCOPE_KEY,
                    "member": {
                        "action": "remove",
                        "fact_id": f"{BOX5}|statement={statement},tax-year=2025",
                    },
                    "successor": {
                        "id": "demo.ssa.h.late2",
                        "predecessor": "demo.ssa.h.late",
                    },
                },
            )
        )
        _, model3 = _run(
            _renumber(list(acts3) + [_load_fixture_adoption()]),
            run_id="demo.ssa.late.stale-empty",
        )
        self.assertEqual(_disposition(model3, "line-6a"), "blocked")
        line6a_blocked = _published_numeric(model3, "line-6a")
        self.assertIn("DEPENDENCY_ABSENT", line6a_blocked.get("activeCodes", []))

        # Step 4: reclose on the current horizon h.late2 — authority is
        # restored and the zero publishes again.
        acts4 = list(acts3)
        acts4.append(
            _act(
                len(acts4),
                "assertion",
                {
                    "finding": _attested(
                        "demo.ssa.closure.late2",
                        f"{CLOSURE}|family-horizon=demo.ssa.h.late2,tax-year=2025",
                        True,
                    )
                },
            )
        )
        _, model4 = _run(
            _renumber(list(acts4) + [_load_fixture_adoption()]),
            run_id="demo.ssa.late.reclosed",
        )
        self.assertEqual(_disposition(model4, "line-6a"), "computed_zero")
        self.assertEqual(_published_numeric(model4, "line-6a"), 0)
        self.assertEqual(_disposition(model4, "line-6b"), "computed_zero")
        self.assertEqual(_published_numeric(model4, "line-6b"), 0)

    def test_admission_rejects_out_of_class_statements(self) -> None:
        """RRB/foreign, lump-sum, box-6 withholding, and non-taxpayer/spouse
        recipient all hard-reject at the real production admission boundary
        (content vocabulary layer, ``FindingModelError``) — not the removed
        isolated helper. Excess repayment hard-rejects at the
        ``validate_projected_source_boundary`` production boundary
        (``SsaBenefitsError``)."""
        from packages.kernel.findings import FindingModelError

        def _one_statement_acts(**override: object) -> list[dict[str, object]]:
            return _renumber(
                _ssa_acts(
                    benefits=[(100.0, 0.0, 100.0)],
                    ira_amounts=[],
                    wages=10000,
                    statement_overrides=[override],
                )
            )

        with self.assertRaisesRegex(
            FindingModelError, "does not conform to tax.us.2025.ssa1099.statement-kind"
        ):
            _run(_one_statement_acts(kind="rrb-1099"), run_id="demo.ssa.repair.rrb")

        with self.assertRaisesRegex(
            FindingModelError,
            "does not conform to tax.us.2025.ssa1099.lump-sum-election",
        ):
            _run(
                _one_statement_acts(lump_sum_election=True),
                run_id="demo.ssa.repair.lump-sum",
            )

        with self.assertRaisesRegex(
            FindingModelError,
            "does not conform to tax.us.2025.ssa1099.box6-withholding",
        ):
            _run(_one_statement_acts(box6=50), run_id="demo.ssa.repair.box6")

        with self.assertRaisesRegex(
            FindingModelError, "does not conform to tax.us.2025.ssa1099.recipient"
        ):
            _run(
                _one_statement_acts(recipient="dependent"),
                run_id="demo.ssa.repair.dependent-recipient",
            )

        # Excess repayment: box 4 exceeds box 3, box 5 forced to zero by the
        # furnished statement — reconciliation still fails (0 != 100-150).
        excess_acts = _renumber(
            _ssa_acts(benefits=[(100.0, 150.0, 0.0)], ira_amounts=[], wages=10000)
        )
        with self.assertRaisesRegex(SsaBenefitsError, "box 5 to equal box 3 minus box 4"):
            _run(excess_acts, run_id="demo.ssa.repair.excess-repayment")

    def _assert_scope_tokens_block(self, tokens: tuple[str, ...], batch: str) -> None:
        worksheet = json.dumps(_load("rule.ss-benefits-worksheet.json"))
        for token in tokens:
            self.assertIn(_scope_id(token), worksheet, token)
        for token in tokens:
            with self.subTest(token=token):
                acts = _renumber(
                    _ssa_acts(
                        benefits=[(12000.0, 0.0, 12000.0)],
                        ira_amounts=[],
                        wages=40000,
                        scope={token: "no"},
                    )
                )
                _, model = _run(acts, run_id=f"demo.ssa.guard.{batch}.{token}")
                self.assertEqual(
                    _disposition(model, "line-6b"),
                    "guard_inapplicable",
                    token,
                )
                self.assertEqual(_disposition(model, "line-6a"), "published_value")

    def test_live_scope_guards_eligibility_batch(self) -> None:
        self._assert_scope_tokens_block(
            (
                "no-unsupported-line1-entries",
                "no-pension-annuity-line5b",
                "no-traditional-ira-deduction",
                "no-form-2555",
                "no-form-4563",
                "no-form-8815",
            ),
            "elig",
        )

    def test_live_scope_guards_foreign_adoption_batch(self) -> None:
        self._assert_scope_tokens_block(
            (
                "no-excluded-adoption-benefits",
                "no-puerto-rico-or-samoa-income",
                "no-schedule1-line24z-writein",
                "no-lump-sum-election",
                "no-rrb-or-foreign-social-benefit",
            ),
            "foreign",
        )

    def test_live_scope_guards_schedule1_part_a_batch(self) -> None:
        self._assert_scope_tokens_block(
            (
                "no-sch1-line11-educator",
                "no-sch1-line12-business-expenses",
                "no-sch1-line13-hsa",
                "no-sch1-line14-moving",
                "no-sch1-line15-deductible-se",
                "no-sch1-line16-se-retirement",
            ),
            "sch1a",
        )

    def test_live_scope_guards_schedule1_part_b_batch(self) -> None:
        self._assert_scope_tokens_block(
            (
                "no-sch1-line17-se-health",
                "no-sch1-line18-penalty",
                "no-sch1-line19-alimony-paid",
                "no-sch1-line20-ira-deduction",
                "no-sch1-line23-archer-msa",
                "no-sch1-line25-other-adjustments",
            ),
            "sch1b",
        )

    def test_worksheet_when_names_every_scope_token(self) -> None:
        """Every accepted exception token is required yes in the worksheet when-clause."""
        worksheet = _load("rule.ss-benefits-worksheet.json")
        blob = json.dumps(worksheet["when"])
        for token in SCOPE_TOKENS:
            self.assertIn(_scope_id(token), blob, token)
            self.assertEqual(
                sum(1 for pin in worksheet["pins"] if pin["id"] == _scope_id(token)),
                1,
                token,
            )

    def test_joint_aggregation_not_double_counted(self) -> None:
        acts = _renumber(
            _ssa_acts(
                benefits=[(8000.0, 0.0, 8000.0), (4000.0, 0.0, 4000.0)],
                ira_amounts=[],
                wages=20000,
                filing_status="married_filing_jointly",
            )
        )
        for act in acts:
            finding = cast(
                dict[str, Any],
                cast(dict[str, Any], act.get("payload", {})).get("finding", {}),
            )
            fact_id = str(finding.get("fact_id", ""))
            if fact_id.startswith(RECIPIENT + "|") and "demo.ssa.statement.1" in fact_id:
                finding["value"] = "spouse"
        report, model = _run(acts, run_id="demo.ssa.joint.once")
        self.assertEqual(_published_numeric(model, "line-6a"), 12000)
        ordinary = self._ordinary_from_model(model)
        expected = _expected_taxable_ss(12000, ordinary, 0.0, base=32000.0, tier2=12000.0)
        self.assertEqual(float(_published_numeric(model, "line-6b")), expected)
        # Pins name both statement findings once each in the source walk lineage.
        # Aggregate once: two box-5 members → one line 6a total, worksheet uses it once.
        self.assertEqual(float(_published_numeric(model, "line-6a")), 12000.0)
        subtotal = next(
            item
            for item in report.get("dispositions", [])
            if item.get("artifact_id") == "tax.us.2025.rule.ssa1099-benefits-subtotal"
        )
        self.assertEqual(subtotal.get("disposition"), "published")
        # Line 9 includes taxable SS once (not 2× benefits).
        line9 = float(_published_numeric(model, "line-9"))
        line6b = float(_published_numeric(model, "line-6b"))
        self.assertLess(line9, 20000 + line6b + 1)  # wages 20k + components + one 6b

    def test_line6c_not_elected_and_filing_status_dispositions(self) -> None:
        acts = _renumber(
            _ssa_acts(benefits=[(12000.0, 0.0, 12000.0)], ira_amounts=[], wages=40000)
        )
        report, model = _run(acts, run_id="demo.ssa.line6c")
        self.assertEqual(_disposition(model, "line-6c"), "published_categorical")
        item = _report_item(report, LINE6C)
        self.assertEqual(item["disposition"], "published")
        # Non-MFS: checked field inapplicable, not-checked field inapplicable.
        self.assertEqual(_disposition(model, "line-6d"), "guard_inapplicable")
        self.assertEqual(_disposition(model, "line-6d-not-checked"), "guard_inapplicable")

    def test_production_shaped_exact_downstream_values(self) -> None:
        wages = 40000.0
        benefits = 12000.0
        acts = _renumber(
            _ssa_acts(
                benefits=[(benefits, 0.0, benefits)],
                ira_amounts=[],
                wages=wages,
            )
        )
        report, model = _run(acts, run_id="demo.ssa.exact.downstream")
        self.assertEqual(_published_numeric(model, "line-6a"), 12000)
        self.assertEqual(_published_numeric(model, "line-6b"), 10200)
        self.assertEqual(_published_numeric(model, "line-9"), 50200)
        self.assertEqual(_published_numeric(model, "line-11"), 50200)
        self.assertEqual(_published_numeric(model, "line-15"), 35200)
        self.assertEqual(_published_numeric(model, "line-16"), 3992)
        # Preferential base not fed by Social Security.
        pref_rule = _load("rule.selected-preferential-base.v4.json")
        self.assertNotIn(LINE6B, json.dumps(pref_rule))

    def test_citations_explanations_and_presentation(self) -> None:
        acts = _renumber(
            _ssa_acts(benefits=[(12000.0, 0.0, 12000.0)], ira_amounts=[], wages=40000)
        )
        report, model = _run(acts, run_id="demo.ssa.presentation.positive")
        section_ids = {s["id"] for s in model["sections"]}
        for sid in ("line-6a", "line-6b", "line-6c", "line-9", "line-16"):
            self.assertIn(sid, section_ids)
        self.assertEqual(_disposition(model, "line-6a"), "published_value")
        self.assertEqual(_disposition(model, "line-6b"), "published_value")
        self.assertEqual(_disposition(model, "line-6c"), "published_categorical")

        # Citation pins on rules.
        for name, cites in (
            ("rule.form1040-line6a.json", ("tax.us.2025.citation.form1040.line-6a",)),
            (
                "rule.ss-benefits-worksheet.json",
                (
                    "tax.us.2025.citation.form1040.ss-benefits-worksheet",
                    "tax.us.2025.citation.form1040.line-6b",
                ),
            ),
            ("rule.form1040-line9.v7.json", ("tax.us.2025.citation.form1040.line-9",)),
        ):
            blob = json.dumps(_load(name))
            for cite in cites:
                self.assertIn(cite, blob)

        # Walkable explanation pins present on published line 6b disposition.
        line6b = _report_item(report, LINE6B)
        self.assertTrue(line6b.get("pins") or line6b.get("finding_id"))
        self.assertIn("tax.us.2025.rule.ss-benefits-worksheet", json.dumps(line6b))

        # Blocked presentation for incomplete worksheet component.
        blocked_acts = _renumber(
            _ssa_acts(
                benefits=[(12000.0, 0.0, 12000.0)],
                ira_amounts=[],
                wages=40000,
                scope={"no-sch1-line11-educator": "no"},
            )
        )
        blocked_report, blocked_model = _run(
            blocked_acts, run_id="demo.ssa.presentation.blocked"
        )
        self.assertEqual(
            _disposition(blocked_model, "line-6b"), "guard_inapplicable"
        )
        blocked_section = next(
            s for s in blocked_model["sections"] if s["id"] == "line-6b"
        )
        self.assertEqual(
            blocked_section["resolved"]["disposition"], "guard_inapplicable"
        )
        # Healthy siblings still present.
        self.assertEqual(_disposition(blocked_model, "line-6a"), "published_value")
        # Missing living-arrangement remains a true blocked disposition.
        mfs_acts = _renumber(
            _ssa_acts(
                benefits=[(12000.0, 0.0, 12000.0)],
                ira_amounts=[],
                wages=40000,
                filing_status="married_filing_separately",
                mfs_lived_apart=None,
            )
        )
        _, mfs_model = _run(mfs_acts, run_id="demo.ssa.presentation.mfs-block")
        self.assertEqual(_disposition(mfs_model, "line-6b"), "blocked")

    def test_package_and_registry_semantic_integrity(self) -> None:
        v26 = _load("package.core-calculations.v26.json")
        v27 = _load("package.core-calculations.v27.json")
        v28 = _load("package.core-calculations.v28.json")

        def member_set(pkg: dict[str, Any]) -> set[tuple[str, str]]:
            return {(m["id"], m["version"]) for m in pkg["members"]}

        def entry_set(pkg: dict[str, Any]) -> set[tuple[str, str]]:
            return {(e["id"], e["version"]) for e in pkg["entrypoints"]}

        def binding_set(pkg: dict[str, Any]) -> set[tuple[str, str, str]]:
            out: set[tuple[str, str, str]] = set()
            for b in pkg.get("input_bindings", []):
                ft = b.get("fact_type") or {}
                out.add(
                    (
                        str(b.get("symbol")),
                        str(ft.get("id")),
                        str(ft.get("version")),
                    )
                )
            return out

        for earlier, later in ((v26, v27), (v27, v28)):
            # Member IDs never drop (versions may advance).
            self.assertTrue(
                {m["id"] for m in earlier["members"]}.issubset(
                    {m["id"] for m in later["members"]}
                )
            )
            self.assertEqual(
                earlier["composition_obligations"], later["composition_obligations"]
            )
            # Exact input-binding identities are preserved.
            self.assertEqual(binding_set(earlier), binding_set(later))
            # Entrypoint ids never drop; exact pins may advance.
            self.assertTrue(
                {e["id"] for e in earlier["entrypoints"]}.issubset(
                    {e["id"] for e in later["entrypoints"]}
                )
            )
            self.assertTrue(
                set(earlier["admitted_schemas"]).issubset(set(later["admitted_schemas"]))
            )

        def selected(pkg: dict[str, Any], rule_id: str) -> str:
            return cast(str, next(m["version"] for m in pkg["members"] if m["id"] == rule_id))

        self.assertEqual(selected(v28, "tax.us.2025.rule.form1040-line9"), "v7")
        self.assertEqual(selected(v28, "tax.us.2025.rule.form1040-line2a"), "v3")
        self.assertEqual(selected(v28, "demo.parameter.tax-brackets.2025"), "v2")
        self.assertEqual(
            selected(v28, "demo.parameter.qdcg-preferential-brackets.2025"), "v2"
        )
        # Upstream IRA / line-7a / line-8 producers remain the ratified selections.
        self.assertEqual(
            selected(v28, "tax.us.2025.rule.f1099r-ira-fully-taxable-subtotal"), "v3"
        )
        self.assertEqual(selected(v28, "tax.us.2025.rule.form1040-line7a"), "v5")
        self.assertEqual(selected(v28, "tax.us.2025.rule.form1040-line8"), "v1")

        r21 = _load("published-packages.v21.json")
        r22 = _load("published-packages.v22.json")
        r23 = _load("published-packages.v23.json")
        for earlier, later in ((r21, r22), (r22, r23)):
            self.assertTrue(
                {(c["id"], c["version"]) for c in earlier["citizens"]}.issubset(
                    {(c["id"], c["version"]) for c in later["citizens"]}
                )
            )
            self.assertTrue(
                {(p["id"], p["version"]) for p in earlier["packages"]}.issubset(
                    {(p["id"], p["version"]) for p in later["packages"]}
                )
            )

        # Selected adoption artifact pins core v28 + release v21 exactly.
        adoption = _load_fixture_adoption()
        payload = cast(dict[str, Any], adoption["payload"])
        self.assertEqual(payload["package"]["version"], "v28")
        self.assertEqual(payload["package"]["checksum"], v28["package_checksum"])
        self.assertEqual(payload["release"]["version"], "v21")
        self.assertEqual(payload["revision"], 28)
        self.assertEqual(payload["supersedes"], "demo.act.adopt.core.v27")
        release = json.loads(
            (
                FIXTURES
                / "publication_surface"
                / "releases"
                / "demo.release.2025.v21.json"
            ).read_text()
        )
        self.assertEqual(release["version"], "v21")
        self.assertEqual(
            release["package_registry_sha256"],
            __import__("hashlib")
            .sha256((CONTENT / "published-packages.v23.json").read_bytes())
            .hexdigest(),
        )

        self.assertEqual(v28["package_checksum"], package_instance_checksum(v28))
        self.assertEqual(v28["version"], "v28")
        # Historical package member sets remain present as versioned history.
        self.assertIn(("tax.us.2025.package.core-calculations", "v26"), {
            (p["id"], p["version"]) for p in r23["packages"]
        })
        self.assertIn(("tax.us.2025.package.core-calculations", "v27"), {
            (p["id"], p["version"]) for p in r23["packages"]
        })
        self.assertIn(("tax.us.2025.package.core-calculations", "v28"), {
            (p["id"], p["version"]) for p in r23["packages"]
        })


if __name__ == "__main__":
    unittest.main()
