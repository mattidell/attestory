"""Loader for the tax content family (First Tax Slice, Track 1).

ADR-0011: the W-2 vocabulary is ordinary kernel ``fact-type.v1`` content
carried in a ``bundle.v1`` — no specialized tax-fact-type schema exists.
ADR-0012: an official form field is a first-class versioned content citizen
validated against the published tax schema directory, distinct from the
derivation output symbol it presents.

Like the derivation loader, every citizen is validated against the
*published* schema files via the kernel SchemaRegistry; a schema mutated out
from under its checksum is a registry defect, never a silent pass. This
module loads declared content only — it contains no runner, no workspace,
and no form-identifier-aware scheduling (E11.3 posture).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from packages.derivation.loader import DERIVATION_SCHEMA_DIR
from packages.derivation.source_authority import validate_mapping_against_family
from packages.kernel.schema_registry import (
    KERNEL_SCHEMA_DIR,
    SchemaRegistry,
    SchemaValidationError,
)

_PACKAGES_DIR = Path(__file__).resolve().parent.parent
TAX_SCHEMA_DIR = _PACKAGES_DIR / "schemas" / "tax"
TAX_CONTENT_DIR = _PACKAGES_DIR / "content" / "tax" / "2025"

FORM_FIELD_SCHEMA = "form-field.v1"
SOURCE_FAMILY_SCHEMA = "source-family.v1"
SOURCE_FAMILY_SCHEMAS = {"source-family.v1", "source-family.v2"}
CLOSURE_MAPPING_SCHEMA = "source-closure-mapping.v1"
W2_BUNDLE_FILE = "w2.bundle.json"
F1099INT_BUNDLE_FILE = "f1099int.bundle.json"


def _version_rank(version: str) -> int:
    """Return the numeric rank of a schema-validated ``v<N>`` citizen version."""
    return int(version.removeprefix("v"))


def domain_companion_presence_pairs() -> dict[str, str | list[str]]:
    """Domain companion-presence pairs enforced at finding admission.

    Production projection (``live_coordinate_run`` → ``project``) must install
    these on its registry. ``tax_registry()`` installs the same map for domain
    loaders and direct registry-path tests.

    Values may be one companion fact-type id or a list of required same-statement
    companions. Presence is always required; optional value-domain restrictions
    live in ``domain_companion_value_domains``.
    """
    return {
        # Form 1099-DIV box-12 route (B12-C3): each box-12 statement member
        # requires an explicit same-statement box-13 absence/zero companion.
        # Kernel enforces presence generically; value domain rejects nonzero
        # without creating Form 6251.
        "tax.us.2025.f1099div.box12-exempt-interest-dividends": (
            "tax.us.2025.f1099div.box13-specified-pab-authority"
        ),
        # Form 1099-G box-1 route (UG-C2): each box-1 statement member requires
        # an explicit same-statement box-4 absence/zero companion. Nonzero is
        # rejected without creating Form 1040 line 25b.
        "tax.us.2025.f1099g.box1-unemployment": (
            "tax.us.2025.f1099g.box4-federal-withholding-authority"
        ),
        # Form 1099-INT box-8 route (B8-C2): each box-8 statement member
        # requires an explicit same-statement box-9 absence/zero companion.
        # Live production projection must install this pair (box-12 review
        # lesson). Nonzero is rejected without creating Form 6251.
        "tax.us.2025.f1099int.box8-tax-exempt-interest": (
            "tax.us.2025.f1099int.box9-specified-pab-authority"
        ),
        # Form 1099-DIV box-7 direct FTC route (B7-C3/C4): each box-7 member
        # requires an explicit same-statement box-8 companion (country string or
        # RIC not_applicable) and associated same-statement box-1a ordinary
        # dividends (presence only; never invent foreign-income amount from tax).
        "tax.us.2025.f1099div.box7-foreign-tax-paid": [
            "tax.us.2025.f1099div.box8-country-companion",
            "tax.us.2025.f1099div.box1a-ordinary",
        ],
        # Form 1099-R IRA-family route: each collected box-1 member requires
        # an explicit false box-2b-not-determined witness on the same logical
        # statement. The combined IRA/SEP/SIMPLE checkbox and code-7 values
        # are restricted below; box-1/box-2a equality is installed separately
        # as an admission invariant.
        "tax.us.2025.f1099r.ira-box1-taxable-distribution": [
            "tax.us.2025.f1099r.ira-box2a-taxable-amount",
            "tax.us.2025.f1099r.ira-sep-simple-checkbox",
            "tax.us.2025.f1099r.distribution-code",
            "tax.us.2025.f1099r.box2b-not-determined",
        ],
        # Form SSA-1099 ordinary benefits route: each box-5 member requires
        # same-statement box-3, box-4, box-6, recipient, statement-kind, and
        # lump-sum-election companions. Box 3/4/5 equality is enforced in
        # domain equality admission separately from presence.
        "tax.us.2025.ssa1099.box5-net-benefits": [
            "tax.us.2025.ssa1099.box3-benefits-paid",
            "tax.us.2025.ssa1099.box4-repayment",
            "tax.us.2025.ssa1099.box6-withholding",
            "tax.us.2025.ssa1099.recipient",
            "tax.us.2025.ssa1099.statement-kind",
            "tax.us.2025.ssa1099.lump-sum-election",
        ],
        # Form 1098-E box-1 route (T0-2 component 8 / T0-3): each box-1
        # statement member requires an explicit same-statement box-2
        # checked/unchecked companion. A checked box 2 is rejected without
        # silently narrowing or overstating the worksheet's total-interest
        # figure (mirrors the f1099g box-1/box-4 pattern).
        "tax.us.2025.f1098e.box1-student-loan-interest": (
            "tax.us.2025.f1098e.box2-checked-authority"
        ),
    }


def domain_companion_value_domains() -> dict[str, frozenset[object]]:
    """Optional admitted companion value domains beyond fact-type value_schema.

    Absence/zero companions for tax-exempt and withholding authority witnesses
    remain restricted after multi-companion generalization. Box-7 country and
    box-1a companions rely on their fact-type value_schema alone.
    """
    return {
        "tax.us.2025.f1099div.box13-specified-pab-authority": frozenset({None, 0, 0.0}),
        "tax.us.2025.f1099g.box4-federal-withholding-authority": frozenset({None, 0, 0.0}),
        "tax.us.2025.f1098e.box2-checked-authority": frozenset({None, False}),
        "tax.us.2025.f1099int.box9-specified-pab-authority": frozenset({None, 0, 0.0}),
        "tax.us.2025.f1099r.box2b-not-determined": frozenset({False}),
        "tax.us.2025.f1099r.ira-sep-simple-checkbox": frozenset({True}),
        "tax.us.2025.f1099r.distribution-code": frozenset({"7"}),
        "tax.us.2025.ssa1099.box6-withholding": frozenset({None, 0, 0.0}),
        "tax.us.2025.ssa1099.statement-kind": frozenset({"ssa-1099"}),
        "tax.us.2025.ssa1099.lump-sum-election": frozenset({False}),
        "tax.us.2025.ssa1099.recipient": frozenset({"taxpayer", "spouse"}),
    }


def domain_companion_equality_pairs() -> dict[str, str]:
    """Same-statement numeric equality witnesses for bounded tax families."""
    return {
        "tax.us.2025.f1099r.ira-box1-taxable-distribution": (
            "tax.us.2025.f1099r.ira-box2a-taxable-amount"
        ),
    }


def install_domain_companion_equalities(registry: SchemaRegistry) -> SchemaRegistry:
    """Install same-statement equality admission invariants."""
    registry.companion_equality_pairs.update(domain_companion_equality_pairs())
    return registry


def domain_migration_resolution_policies() -> dict[str, str]:
    """Migration id -> opt-in resolution policy, enforced generically by
    ``packages.kernel.findings.apply_migration_adoption`` (ADR-0072
    Decision 4).

    ``tax.us.2025.scheduleb-accrued-interest.succession``'s v1 artifact
    presents a claim for any then-current legacy finding; without this
    policy, adoption would immediately retire the predecessor type
    regardless of that finding's value, silently discarding a live legacy
    claim genuinely unrelated to any new pairing, with no refusal and no
    trace. "resolved-required" refuses adoption outright while any
    predecessor fact this migration would retire -- live or withdrawn --
    last recorded a nonzero value.

    A nonzero legacy claim blocks migration. The only currently accepted
    resolution is a same-identity correction to a genuinely zero value
    (the same free same-identity correction ADR-0072's amount-collision
    case already uses), never by asserting zero for a claim that is still
    true. Withdrawing a nonzero claim (an ordinary member-transition
    removal, ADR-0017) does **not** resolve it, with or without naming
    ``corresponds_to_fact_id`` (``act-member-transition.v3``): no accepted
    mechanism can check a claimed representation transfer against
    anything, since the predecessor fact type carries no obligation,
    payer, or report identity -- a real, current, but domain-wrong
    correspondence would otherwise let a genuinely distinct nonzero claim
    be discarded. Withdrawal only matters for a claim whose value was
    already genuinely zero, where it migrates without naming any
    replacement. Whether to build a genuine representation-transfer
    adjudication act that could let a nonzero claim resolve honestly
    remains an explicit, undecided owner question (see ADR-0072 and
    ``docs/phase-state.md``'s "Open and owner-held"); this policy does not
    approximate that decision with a structural proxy.
    """
    return {
        "tax.us.2025.scheduleb-accrued-interest.succession": "resolved-required",
    }


def install_domain_migration_resolution_policies(registry: SchemaRegistry) -> SchemaRegistry:
    """Install domain migration-resolution policies on a published registry."""
    registry.migration_resolution_policies.update(domain_migration_resolution_policies())
    return registry


def install_domain_companion_presence(registry: SchemaRegistry) -> SchemaRegistry:
    """Install domain companion-presence pairs on an existing published registry.

    Idempotent: re-applying the same pairs is a no-op for equal keys.

    Also installs migration-resolution policies (``install_domain_
    migration_resolution_policies``): this function's exact call sites
    (``tax_registry()`` below and ``packages.derivation.live.live_
    coordinate_run``) are the two places every registry a workspace fold
    or production run actually uses gets domain maps layered onto it, so
    folding the migration-resolution install in here -- rather than adding
    a third call site to each -- reaches the live path without touching
    ``packages/derivation/live.py``.
    """
    registry.companion_presence_pairs.update(domain_companion_presence_pairs())
    domains = getattr(registry, "companion_value_domains", None)
    if domains is None:
        registry.companion_value_domains = {}
        domains = registry.companion_value_domains
    domains.update(domain_companion_value_domains())
    install_domain_migration_resolution_policies(registry)
    return registry


def domain_declaration_signal_contradictions() -> list[dict[str, str]]:
    """Domain declaration/signal contradictions enforced at finding admission.

    Production projection (``live_coordinate_run`` → ``project``) must install
    these on its registry. ``tax_registry()`` installs the same list for domain
    loaders and direct registry-path tests.
    """
    return [
        # ADR-0038 decision 5 / ADR-0050 decisions 2 and 4: a current "no"
        # capital-gain-distributions declaration and the
        # CAPITAL_GAIN_DISTRIBUTION_RECORDED signal may never both be current.
        {
            "declaration_fact_type": "tax.us.2025.capital-gain-distributions",
            "declaration_value": "no",
            "signal_fact_type": "tax.us.2025.f1099div.box2a-capital-gain-distribution",
        },
        # Path A (no-f1099int-tax-exempt = yes) contradicts any current non-null
        # box-8 tax-exempt interest member. Path B uses declaration = no with a
        # closed box-8 family instead of silently ignoring box-8 amounts.
        {
            "declaration_fact_type": "tax.us.2025.line2a-scope.no-f1099int-tax-exempt",
            "declaration_value": "yes",
            "signal_fact_type": "tax.us.2025.f1099int.box8-tax-exempt-interest",
        },
    ]


def install_domain_declaration_signal_contradictions(
    registry: SchemaRegistry,
) -> SchemaRegistry:
    """Install domain declaration/signal contradictions on a published registry.

    Idempotent for equal rule dicts: skips rules already present.
    """
    existing = {
        (
            rule.get("declaration_fact_type"),
            rule.get("declaration_value"),
            rule.get("signal_fact_type"),
            rule.get("signal_field"),
        )
        for rule in registry.declaration_signal_contradictions
    }
    for rule in domain_declaration_signal_contradictions():
        key = (
            rule.get("declaration_fact_type"),
            rule.get("declaration_value"),
            rule.get("signal_fact_type"),
            rule.get("signal_field"),
        )
        if key not in existing:
            registry.declaration_signal_contradictions.append(dict(rule))
            existing.add(key)
    return registry


def tax_registry() -> SchemaRegistry:
    """A registry spanning the kernel, tax, and derivation schema families.

    Bundle and fact-type content validate against the kernel family;
    form-field content validates against the tax family; source-family
    declarations and closure mappings validate against the derivation
    family. Schema ids are unique across the directories (enforced on
    load).
    """
    reg = SchemaRegistry([KERNEL_SCHEMA_DIR, TAX_SCHEMA_DIR, DERIVATION_SCHEMA_DIR])
    families = load_source_families(reg)
    for family in families.values():
        reg.family_member_predicates.add(family["member_predicate"]["fact_type"])
    # ADR-0035 decision 4: 1099-DIV box 1b (qualified) is a per-statement
    # subset of box 1a (ordinary) - enforced generically by the kernel via
    # the declared pair, at admission, before state mutation is observed.
    reg.subset_invariant_pairs["tax.us.2025.f1099div.box1b-qualified"] = (
        "tax.us.2025.f1099div.box1a-ordinary"
    )
    install_domain_declaration_signal_contradictions(reg)
    install_domain_companion_presence(reg)
    install_domain_companion_equalities(reg)
    return reg


def _load_bundle(filename: str, reg: SchemaRegistry) -> dict[str, Any]:
    bundle: dict[str, Any] = json.loads(
        (TAX_CONTENT_DIR / filename).read_text("utf-8")
    )
    reg.validate_declared(bundle)
    seen: set[str] = set()
    for fact_type in bundle["fact_types"]:
        reg.validate_declared(fact_type)
        if fact_type["id"] in seen:
            raise SchemaValidationError(
                "bundle.v1", [f"duplicate fact-type id in bundle: {fact_type['id']}"]
            )
        seen.add(fact_type["id"])
    return bundle


def load_w2_bundle(registry: SchemaRegistry | None = None) -> dict[str, Any]:
    """Load and strictly validate the 2025 W-2 vocabulary bundle.

    The bundle envelope and every nested fact type validate against their
    declared schema versions. Nested fact-type ids must be unique.
    """
    reg = registry if registry is not None else tax_registry()
    return _load_bundle(W2_BUNDLE_FILE, reg)


def load_f1099int_bundle(registry: SchemaRegistry | None = None) -> dict[str, Any]:
    """Load and strictly validate the 2025 Form 1099-INT box-1 bundle."""
    reg = registry if registry is not None else tax_registry()
    return _load_bundle(F1099INT_BUNDLE_FILE, reg)


def load_source_families(
    registry: SchemaRegistry | None = None,
) -> dict[str, dict[str, Any]]:
    """Load every committed source-family declaration, mapped id -> citizen."""
    reg = registry if registry is not None else tax_registry()
    by_id: dict[str, dict[str, Any]] = {}
    for path in sorted(TAX_CONTENT_DIR.glob("family.*.json")):
        citizen: dict[str, Any] = json.loads(path.read_text("utf-8"))
        declared = reg.validate_declared(citizen)
        if declared not in SOURCE_FAMILY_SCHEMAS:
            raise SchemaValidationError(
                SOURCE_FAMILY_SCHEMA,
                [f"{path.name} declares {declared}, not one of {sorted(SOURCE_FAMILY_SCHEMAS)}"],
            )
        existing = by_id.get(citizen["id"])
        if existing is None:
            by_id[citizen["id"]] = citizen
            continue
        if existing["version"] == citizen["version"]:
            raise SchemaValidationError(
                SOURCE_FAMILY_SCHEMA,
                [f"duplicate source-family id/version: {citizen['id']}@{citizen['version']}"],
            )
        if _version_rank(citizen["version"]) > _version_rank(existing["version"]):
            by_id[citizen["id"]] = citizen
    return by_id


def load_closure_mappings(
    registry: SchemaRegistry | None = None,
) -> dict[str, dict[str, Any]]:
    """Load every committed closure mapping, validated against its family.

    Each mapping validates against the published schema *and* against the
    declaration it pins (ADR-0014/0016): a mapping whose family is not
    committed, whose member fact type diverges from the canonical
    predicate, or whose admitted symbol is not the declaration's
    authorized subtotal is a content defect, never a silent pass.
    """
    reg = registry if registry is not None else tax_registry()
    families = load_source_families(reg)
    by_id: dict[str, dict[str, Any]] = {}
    for path in sorted(TAX_CONTENT_DIR.glob("closure-mapping.*.json")):
        citizen: dict[str, Any] = json.loads(path.read_text("utf-8"))
        declared = reg.validate_declared(citizen)
        if declared not in {"source-closure-mapping.v1", "source-closure-mapping.v2"}:
            raise SchemaValidationError(
                "source-closure-mapping.v2",
                [f"{path.name} declares {declared}, not source-closure-mapping.v1 or source-closure-mapping.v2"],
            )
        family = families.get(citizen["family"]["id"])
        if family is not None and family["version"] != citizen["family"]["version"]:
            # Validate historical mappings against their exact family
            # successor, while the domain registry exposes the highest
            # version as the current declaration.
            family = None
            for family_path in sorted(TAX_CONTENT_DIR.glob("family.*.json")):
                candidate = json.loads(family_path.read_text("utf-8"))
                if candidate.get("id") == citizen["family"]["id"] and candidate.get("version") == citizen["family"]["version"]:
                    family = candidate
                    reg.validate_declared(candidate)
                    break
        if family is None:
            raise SchemaValidationError(
                "source-closure-mapping.v2",
                [f"{path.name} pins family {citizen['family']['id']}, "
                 "which no committed declaration provides"],
            )
        validate_mapping_against_family(citizen, family)
        existing = by_id.get(citizen["id"])
        if existing is None:
            by_id[citizen["id"]] = citizen
            continue
        if existing["version"] == citizen["version"]:
            raise SchemaValidationError(
                "source-closure-mapping.v2",
                [f"duplicate mapping id/version: {citizen['id']}@{citizen['version']}"],
            )
        if _version_rank(citizen["version"]) > _version_rank(existing["version"]):
            by_id[citizen["id"]] = citizen
    return by_id


def load_form_fields(registry: SchemaRegistry | None = None) -> dict[str, dict[str, Any]]:
    """Load every committed form-field citizen, mapped id -> citizen.

    Each citizen validates against a published ``form-field`` schema version.
    A duplicate id/version pair is a content defect: two published fields with
    one identity would make the printed-locator identity ambiguous. Distinct
    versions of one id follow the closure-mapping convention: the highest
    published version is the current citizen.
    """
    reg = registry if registry is not None else tax_registry()
    by_id: dict[str, dict[str, Any]] = {}
    for path in sorted(TAX_CONTENT_DIR.glob("*.form-field*.json")):
        citizen: dict[str, Any] = json.loads(path.read_text("utf-8"))
        declared = reg.validate_declared(citizen)
        if declared not in {"form-field.v1", "form-field.v2", "form-field.v3"}:
            raise SchemaValidationError(
                "form-field.v3",
                [f"{path.name} declares {declared}, not a published form-field schema"],
            )
        existing = by_id.get(citizen["id"])
        if existing is None:
            by_id[citizen["id"]] = citizen
            continue
        if existing["version"] == citizen["version"]:
            raise SchemaValidationError(
                "form-field.v3", [f"duplicate form-field id: {citizen['id']}"]
            )
        if _version_rank(citizen["version"]) > _version_rank(existing["version"]):
            by_id[citizen["id"]] = citizen
    return by_id
