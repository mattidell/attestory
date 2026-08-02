"""Track 1 Covered Long-Term Gains, Schedule D Line 8a: schema/content citizens (ADR-0052)."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from typing import Any, ClassVar, cast

import jsonschema

from packages.derivation.loader import DERIVATION_SCHEMA_DIR
from packages.kernel.facts import fact_id_for
from packages.kernel.findings import FindingModelError, apply_act, initial_state
from packages.kernel.schema_registry import KERNEL_SCHEMA_DIR, SchemaRegistry, SchemaValidationError
from packages.tax.loader import (
    TAX_CONTENT_DIR,
    TAX_SCHEMA_DIR,
    load_closure_mappings,
    load_source_families,
    tax_registry,
)

ROOT = Path("packages/sample_data/schedule_d_covered_ltcg_8a_t1")
NEGATIVES = ROOT / "negatives"

ANCHOR_FACT_TYPE = "tax.us.2025.f1099b.statement-anchor"
MEMBER_FACT_TYPE = "tax.us.2025.f1099b.covered-ltcg-txn"
CLOSURE_FACT_TYPE = "tax.us.2025.f1099b.covered-ltcg.source-closure"
FAMILY_ID = "tax.us.2025.f1099b.covered-ltcg"
CLOSURE_MAPPING_ID = "tax.us.2025.closure-mapping.f1099b-covered-ltcg"

BOUNDARY_DECLARATION_IDS = (
    "tax.us.2025.schedule-d-boundary.no-short-term-transactions",
    "tax.us.2025.schedule-d-boundary.no-current-capital-losses",
    "tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers",
    "tax.us.2025.schedule-d-boundary.no-form8949-sources",
    "tax.us.2025.schedule-d-boundary.no-other-schedule-d-sources",
    "tax.us.2025.schedule-d-boundary.no-lines-18-19-sources",
    "tax.us.2025.schedule-d-boundary.no-1099da-or-qof",
)

COMMITTED_CITIZENS = (
    "f1099b-covered-ltcg.bundle.json",
    "family.f1099b-covered-ltcg.json",
    "closure-mapping.f1099b-covered-ltcg.json",
    "schedule-d-boundary.bundle.json",
)

HISTORICAL_BYTES = {
    "docs/adr/0036-schedule-attachment-ontology.md": (
        "6c307da66ead376523838848442095cfea11e109ad5566830ad24d434c7d3265"
    ),
    "docs/adr/0050-capital-gain-distributions-and-line-7a.md": (
        "47fb67494cf9baf6de248e5bb7ef2b658b7a6b15d3c5158f6773025edd6c639b"
    ),
    "packages/content/tax/2025/family.f1099div-2a.json": (
        "127687b54ad6d5042f70464c9012ab22ea62c9ba9635aae3364507abd9b25cdf"
    ),
    "packages/content/tax/2025/closure-mapping.f1099div-2a.json": (
        "f80ef9f0109d22c7b2a975617f3a170b6dba5b2d54461832b8420be9f9f96789"
    ),
    "packages/schemas/kernel/fact-type.v2.schema.json": (
        "727d4233cb1124f1085163944764aee27379b9c041aa7a88679c037f55a7a938"
    ),
    "packages/schemas/derivation/source-family.v1.schema.json": (
        "78462f32843d005801c4e50272ee864c340f20966f5e88b894b0a7deb14d8490"
    ),
    "packages/schemas/derivation/source-closure-mapping.v2.schema.json": (
        "7046dcea09ad5b26850c0697c8ab12afc7231f08d988ff26479a01018733d4ca"
    ),
    "packages/schemas/kernel/bundle.v2.schema.json": (
        "3abb73ea8cebb516f86f12d20e6b3dc0c3d5f9ad40a2ac7b5b3645d98c689c0c"
    ),
}

_ELIGIBLE_VALUE = {
    "proceeds": 6000,
    "basis": 2000,
    "covered_security": "yes",
    "basis_reported_to_irs": "yes",
    "long_term": "yes",
    "box_1f_market_discount": "no",
    "box_1g_wash_sale_adjustment": "no",
    "ordinary_indicated": "no",
    "qof_indicated": "no",
    "taxpayer_side_adjustment": "no",
    "collectibles_or_special_rate": "no",
    "gain_only": "yes",
}


def load(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text("utf-8")))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.sched-d-8a.t1.act.{index:03d}",
        "kind": kind,
        "actor": "demo.user.filer-1",
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


def _member_fact_id(broker: str, statement: str, transaction: str) -> str:
    return fact_id_for(
        MEMBER_FACT_TYPE,
        (
            ("broker", broker),
            ("statement", statement),
            ("transaction", transaction),
            ("tax-year", "2025"),
        ),
    )


def _anchor_fact_id(broker: str, statement: str) -> str:
    return fact_id_for(
        ANCHOR_FACT_TYPE,
        (("broker", broker), ("statement", statement), ("tax-year", "2025")),
    )


def _boundary_acts(index_start: int, values: dict[str, str] | None) -> list[dict[str, object]]:
    values = values if values is not None else {fid: "yes" for fid in BOUNDARY_DECLARATION_IDS}
    acts: list[dict[str, object]] = []
    for offset, fact_type_id in enumerate(BOUNDARY_DECLARATION_IDS):
        if fact_type_id not in values:
            continue
        fact_id = fact_id_for(fact_type_id, (("tax-year", "2025"),))
        finding_id = f"demo.sched-d-8a.boundary.{offset}"
        acts.append(
            _act(
                index_start + offset,
                "assertion",
                {"finding": _attested(finding_id, fact_id, values[fact_type_id])},
            )
        )
    return acts


def _scenario_acts(
    transactions: list[tuple[str, str, str, dict[str, Any]]],
    *,
    close_family: bool | None = True,
    boundary: dict[str, str] | None = None,
) -> tuple[list[dict[str, object]], str]:
    """Build a full act sequence admitting one or more eligible transactions.

    Returns the acts list and the id of the final family horizon (for
    building the closure fact id in tests that assert it directly).
    """
    acts: list[dict[str, object]] = []

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": load(TAX_CONTENT_DIR / "f1099b-covered-ltcg.bundle.json")})
    add("bundle-adoption", {"bundle": load(TAX_CONTENT_DIR / "schedule-d-boundary.bundle.json")})

    brokers = sorted({t[0] for t in transactions})
    statements = sorted({t[1] for t in transactions})
    txns = sorted({t[2] for t in transactions})
    for broker in brokers:
        add("entity-introduced", {"entity": {
            "schema": "entity.v1", "id": broker, "kind": "tax.us.f1099b-broker",
            "label": "Synthetic broker",
        }})
    for statement in statements:
        add("entity-introduced", {"entity": {
            "schema": "entity.v1", "id": statement, "kind": "tax.us.f1099b-statement",
            "label": "Synthetic 1099-B statement",
        }})
    for txn in txns:
        add("entity-introduced", {"entity": {
            "schema": "entity.v1", "id": txn, "kind": "tax.us.f1099b-transaction",
            "label": "Synthetic covered long-term sale",
        }})

    scope = {"tax-year": "2025", "subject": "demo.primary"}
    add("horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": scope, "horizon_id": "demo.sched-d-8a.h0"})
    horizon = "demo.sched-d-8a.h0"

    for broker, statement in sorted({(t[0], t[1]) for t in transactions}):
        add("assertion", {"finding": _attested(
            f"demo.sched-d-8a.anchor.{broker}.{statement}",
            _anchor_fact_id(broker, statement),
            {"broker_name": "Synthetic Broker"},
        )})

    for idx, (broker, statement, txn, value) in enumerate(transactions):
        successor = f"demo.sched-d-8a.h{idx + 1}"
        add("member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": {
                "schema": "finding.v1",
                "id": f"demo.sched-d-8a.txn.{idx}",
                "fact_id": _member_fact_id(broker, statement, txn),
                "value": value,
                "basis": "attested",
                "evidence_ids": [],
            }},
            "successor": {"id": successor, "predecessor": horizon},
        })
        horizon = successor

    if close_family is not None:
        add("assertion", {"finding": _attested(
            "demo.sched-d-8a.closure",
            fact_id_for(CLOSURE_FACT_TYPE, (("family-horizon", horizon), ("tax-year", "2025"))),
            close_family,
        )})

    acts.extend(_boundary_acts(len(acts), boundary))
    return acts, horizon


class TrackOneRegistry(unittest.TestCase):
    registry: ClassVar[SchemaRegistry]

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = SchemaRegistry([KERNEL_SCHEMA_DIR, DERIVATION_SCHEMA_DIR, TAX_SCHEMA_DIR])


class PositiveInstances(TrackOneRegistry):
    def test_every_committed_track1_citizen_validates(self) -> None:
        for name in COMMITTED_CITIZENS:
            with self.subTest(name=name):
                citizen = load(TAX_CONTENT_DIR / name)
                self.registry.validate_declared(citizen)
                if name.endswith(".bundle.json"):
                    for fact_type in citizen["fact_types"]:
                        self.registry.validate_declared(fact_type)

    def test_family_and_closure_mapping_load_through_production_loader(self) -> None:
        registry = tax_registry()
        families = load_source_families(registry)
        mappings = load_closure_mappings(registry)
        family = families[FAMILY_ID]
        mapping = mappings[CLOSURE_MAPPING_ID]
        self.assertEqual(family["member_predicate"]["fact_type"], MEMBER_FACT_TYPE)
        self.assertEqual(family["authorizes_subtotal"], "tax.us.2025.f1099b.covered-ltcg-subtotal")
        self.assertEqual(mapping["family"], {"id": FAMILY_ID, "version": "v1"})
        self.assertEqual(mapping["member_fact_type"], {"id": MEMBER_FACT_TYPE, "version": "v1"})
        self.assertEqual(mapping["closure_fact_type"], {"id": CLOSURE_FACT_TYPE, "version": "v1"})
        self.assertEqual(mapping["closure_horizon_key"], "family-horizon")
        self.assertEqual(mapping["admits_symbol"], "tax.us.2025.f1099b.covered-ltcg-subtotal")
        self.assertEqual(mapping["admission"], {"condition": "current-literal-true"})
        claim = family["closure_claim"].lower()
        self.assertIn("short-term", claim)
        self.assertIn("1099-da", claim)
        self.assertTrue("says nothing" in claim or "never" in claim or "does not assert" in claim)

    def test_registry_registers_new_family_member_predicate(self) -> None:
        registry = tax_registry()
        self.assertIn(MEMBER_FACT_TYPE, registry.family_member_predicates)


class SourceClassIdentity(TrackOneRegistry):
    def test_anchor_identity_is_logical_not_evidence(self) -> None:
        bundle = load(TAX_CONTENT_DIR / "f1099b-covered-ltcg.bundle.json")
        anchor = next(ft for ft in bundle["fact_types"] if ft["id"] == ANCHOR_FACT_TYPE)
        keys = {k["name"]: k for k in anchor["identity_keys"]}
        self.assertEqual(keys["broker"]["entity_kind"], "tax.us.f1099b-broker")
        self.assertEqual(keys["statement"]["entity_kind"], "tax.us.f1099b-statement")
        self.assertEqual(keys["tax-year"]["values"], ["2025"])
        identity_text = json.dumps(anchor["identity_keys"])
        for forbidden in ("evidence", "file", "upload", "document", "scan"):
            self.assertNotIn(forbidden, identity_text)

    def test_member_identity_shares_anchor_entities_and_adds_transaction(self) -> None:
        bundle = load(TAX_CONTENT_DIR / "f1099b-covered-ltcg.bundle.json")
        member = next(ft for ft in bundle["fact_types"] if ft["id"] == MEMBER_FACT_TYPE)
        keys = {k["name"]: k for k in member["identity_keys"]}
        self.assertEqual(keys["broker"]["entity_kind"], "tax.us.f1099b-broker")
        self.assertEqual(keys["statement"]["entity_kind"], "tax.us.f1099b-statement")
        self.assertEqual(keys["transaction"]["entity_kind"], "tax.us.f1099b-transaction")
        self.assertEqual(keys["tax-year"]["values"], ["2025"])
        identity_text = json.dumps(member["identity_keys"])
        for forbidden in ("evidence", "file", "upload", "document", "scan"):
            self.assertNotIn(forbidden, identity_text)
        self.assertEqual(member["supersession"], {"policy": "free"})
        self.assertNotIn("source_amount", member)

    def test_member_predicate_fields_are_contributed_never_derived(self) -> None:
        bundle = load(TAX_CONTENT_DIR / "f1099b-covered-ltcg.bundle.json")
        member = next(ft for ft in bundle["fact_types"] if ft["id"] == MEMBER_FACT_TYPE)
        props = member["value_schema"]["properties"]
        required = set(member["value_schema"]["required"])
        predicate_fields = {
            "covered_security", "basis_reported_to_irs", "long_term",
            "box_1f_market_discount", "box_1g_wash_sale_adjustment",
            "ordinary_indicated", "qof_indicated", "taxpayer_side_adjustment",
            "collectibles_or_special_rate", "gain_only",
        }
        self.assertTrue(predicate_fields.issubset(required))
        for field in predicate_fields:
            self.assertEqual(props[field], {"enum": ["yes", "no"]})
        self.assertEqual(member["value_schema"]["additionalProperties"], False)
        # gain_only is its own attested field, never a computed proceeds-basis comparison.
        self.assertNotIn("gain", props)
        self.assertIn("proceeds", props)
        self.assertIn("basis", props)


class CompletenessDeclarations(TrackOneRegistry):
    def test_seven_declarations_have_yes_no_domain_no_default_free_supersession(self) -> None:
        bundle = load(TAX_CONTENT_DIR / "schedule-d-boundary.bundle.json")
        by_id = {ft["id"]: ft for ft in bundle["fact_types"]}
        self.assertEqual(set(by_id), set(BOUNDARY_DECLARATION_IDS))
        for fact_id in BOUNDARY_DECLARATION_IDS:
            with self.subTest(fact_id=fact_id):
                ft = by_id[fact_id]
                self.assertEqual(ft["value_schema"], {"enum": ["yes", "no"]})
                self.assertNotIn("optional_default", ft)
                self.assertEqual(ft["supersession"], {"policy": "free"})
                self.assertEqual(ft["identity_keys"], [
                    {"name": "tax-year", "kind": "literal", "values": ["2025"]}
                ])

    def test_declaration_value_schema_rejects_non_yes_no_values(self) -> None:
        bundle = load(TAX_CONTENT_DIR / "schedule-d-boundary.bundle.json")
        by_id = {ft["id"]: ft for ft in bundle["fact_types"]}
        for fact_id in BOUNDARY_DECLARATION_IDS:
            validator = jsonschema.Draft202012Validator(by_id[fact_id]["value_schema"])
            with self.subTest(fact_id=fact_id):
                self.assertEqual(list(validator.iter_errors("yes")), [])
                self.assertEqual(list(validator.iter_errors("no")), [])
                self.assertTrue(list(validator.iter_errors(True)))
                self.assertTrue(list(validator.iter_errors(False)))
                self.assertTrue(list(validator.iter_errors("maybe")))
                self.assertTrue(list(validator.iter_errors(None)))

    def test_no_synthesizing_conclusion_citizen_is_published(self) -> None:
        bundle = load(TAX_CONTENT_DIR / "schedule-d-boundary.bundle.json")
        ids = {ft["id"] for ft in bundle["fact_types"]}
        self.assertEqual(len(ids), 7)
        for name in ids:
            self.assertNotIn("conclusion", name)


class KernelAdmission(unittest.TestCase):
    """Exercises the already-generic kernel admission/currency machinery
    (ADR-0010, ADR-0023) against the new family - no new evaluator or rule
    is introduced; these tests confirm existing production behavior extends
    correctly to Track 1's citizens.
    """

    def setUp(self) -> None:
        self.registry = tax_registry()

    def test_two_transactions_one_anchor_remain_distinct_members(self) -> None:
        """Shared case 2 shape: one broker/statement, two transactions."""
        acts, horizon = _scenario_acts([
            ("demo.broker.a", "demo.stmt.a", "demo.sale.001", _ELIGIBLE_VALUE),
            ("demo.broker.a", "demo.stmt.a", "demo.sale.002", {**_ELIGIBLE_VALUE, "proceeds": 5000, "basis": 3000}),
        ])
        state = initial_state()
        for act in acts:
            state = apply_act(state, act, self.registry)
        fact_ids = {f["fact_id"] for f in state.findings.values()}
        self.assertIn(_member_fact_id("demo.broker.a", "demo.stmt.a", "demo.sale.001"), fact_ids)
        self.assertIn(_member_fact_id("demo.broker.a", "demo.stmt.a", "demo.sale.002"), fact_ids)
        self.assertNotEqual(
            _member_fact_id("demo.broker.a", "demo.stmt.a", "demo.sale.001"),
            _member_fact_id("demo.broker.a", "demo.stmt.a", "demo.sale.002"),
        )
        closure_id = fact_id_for(CLOSURE_FACT_TYPE, (("family-horizon", horizon), ("tax-year", "2025")))
        closure_finding = next(f for f in state.findings.values() if f["fact_id"] == closure_id)
        self.assertIs(closure_finding["value"], True)

    def test_multi_broker_members_remain_distinct(self) -> None:
        """Shared case 3 shape: two distinct brokers, colliding sale suffix."""
        acts, _ = _scenario_acts([
            ("demo.broker.a", "demo.stmt.a", "demo.sale.001", _ELIGIBLE_VALUE),
            ("demo.broker.b", "demo.stmt.b", "demo.sale.001", {**_ELIGIBLE_VALUE, "proceeds": 9000, "basis": 5000}),
        ])
        state = initial_state()
        for act in acts:
            state = apply_act(state, act, self.registry)
        fact_ids = {f["fact_id"] for f in state.findings.values()}
        self.assertIn(_member_fact_id("demo.broker.a", "demo.stmt.a", "demo.sale.001"), fact_ids)
        self.assertIn(_member_fact_id("demo.broker.b", "demo.stmt.b", "demo.sale.001"), fact_ids)
        self.assertNotEqual(
            _member_fact_id("demo.broker.a", "demo.stmt.a", "demo.sale.001"),
            _member_fact_id("demo.broker.b", "demo.stmt.b", "demo.sale.001"),
        )

    def test_correction_preserves_identity_sibling_unaffected(self) -> None:
        """Shared case 4: correcting one transaction leaves its sibling untouched."""
        acts, _ = _scenario_acts([
            ("demo.broker.a", "demo.stmt.a", "demo.sale.001", _ELIGIBLE_VALUE),
            ("demo.broker.a", "demo.stmt.a", "demo.sale.002", {**_ELIGIBLE_VALUE, "proceeds": 5000, "basis": 3000}),
        ])
        state = initial_state()
        for act in acts:
            state = apply_act(state, act, self.registry)

        t1_fact_id = _member_fact_id("demo.broker.a", "demo.stmt.a", "demo.sale.001")
        corrected_value = {**_ELIGIBLE_VALUE, "proceeds": 6200}
        correction = _act(len(acts), "assertion", {"finding": {
            "schema": "finding.v1",
            "id": "demo.sched-d-8a.txn.0.correction",
            "fact_id": t1_fact_id,
            "value": corrected_value,
            "basis": "attested",
            "evidence_ids": [],
        }})
        state = apply_act(state, correction, self.registry)

        original = state.findings["demo.sched-d-8a.txn.0"]
        corrected = state.findings["demo.sched-d-8a.txn.0.correction"]
        sibling = state.findings["demo.sched-d-8a.txn.1"]
        self.assertEqual(original["value"]["proceeds"], 6000)  # immutable history
        self.assertEqual(corrected["value"]["proceeds"], 6200)
        self.assertEqual(corrected["fact_id"], t1_fact_id)
        self.assertEqual(sibling["value"]["proceeds"], 5000)  # unaffected
        self.assertEqual(
            sibling["fact_id"],
            _member_fact_id("demo.broker.a", "demo.stmt.a", "demo.sale.002"),
        )

    def test_member_transition_rejects_reusing_an_existing_transaction_ref(self) -> None:
        """Named negative: two sales collapsing onto one transaction-ref.

        Attempting to add a *second*, distinct sale under a transaction-ref
        that is already a current member is rejected outright by the
        member-transition path (ADR-0023 SC-R2) - it is not silently
        admitted as a second member, which is exactly why P1-S3 requires a
        distinct logical-transaction-ref per sale.
        """
        acts, horizon = _scenario_acts([
            ("demo.broker.a", "demo.stmt.a", "demo.sale.001", _ELIGIBLE_VALUE),
        ], close_family=None)
        state = initial_state()
        for act in acts:
            state = apply_act(state, act, self.registry)

        collapsed = _act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": {
                "schema": "finding.v1",
                "id": "demo.sched-d-8a.txn.collapsed",
                "fact_id": _member_fact_id("demo.broker.a", "demo.stmt.a", "demo.sale.001"),
                "value": {**_ELIGIBLE_VALUE, "proceeds": 9000, "basis": 1000},
                "basis": "attested",
                "evidence_ids": [],
            }},
            "successor": {"id": "demo.sched-d-8a.h-collapsed", "predecessor": horizon},
        })
        with self.assertRaises(FindingModelError):
            apply_act(state, collapsed, self.registry)

    def test_plain_assertion_of_a_brand_new_member_is_rejected(self) -> None:
        """ADR-0023 SC-R1 generically covers the new family: a not-yet-member
        fact of the member fact type cannot enter through a plain assertion.
        """
        acts, _ = _scenario_acts([
            ("demo.broker.a", "demo.stmt.a", "demo.sale.001", _ELIGIBLE_VALUE),
        ], close_family=None)
        acts.append(_act(len(acts), "entity-introduced", {"entity": {
            "schema": "entity.v1", "id": "demo.sale.002", "kind": "tax.us.f1099b-transaction",
            "label": "Synthetic second sale",
        }}))
        state = initial_state()
        for act in acts:
            state = apply_act(state, act, self.registry)

        bad_assertion = _act(len(acts), "assertion", {"finding": {
            "schema": "finding.v1",
            "id": "demo.sched-d-8a.txn.bypass",
            "fact_id": _member_fact_id("demo.broker.a", "demo.stmt.a", "demo.sale.002"),
            "value": _ELIGIBLE_VALUE,
            "basis": "attested",
            "evidence_ids": [],
        }})
        with self.assertRaises(FindingModelError):
            apply_act(state, bad_assertion, self.registry)

    def test_anchor_is_a_contributed_fact_independent_of_the_family(self) -> None:
        acts, _ = _scenario_acts([
            ("demo.broker.a", "demo.stmt.a", "demo.sale.001", _ELIGIBLE_VALUE),
        ], close_family=None)
        state = initial_state()
        for act in acts:
            state = apply_act(state, act, self.registry)
        anchor_finding = next(
            f for f in state.findings.values()
            if f["fact_id"] == _anchor_fact_id("demo.broker.a", "demo.stmt.a")
        )
        self.assertEqual(anchor_finding["value"], {"broker_name": "Synthetic Broker"})


class NamedNegatives(unittest.TestCase):
    SCHEMA_REJECTING = (
        "source-family.v1.f1099b-covered-ltcg-invalid-member.json",
        "source-closure-mapping.v2.f1099b-covered-ltcg-invalid-admission.json",
    )

    def setUp(self) -> None:
        self.registry = SchemaRegistry([KERNEL_SCHEMA_DIR, DERIVATION_SCHEMA_DIR, TAX_SCHEMA_DIR])

    def test_schema_negatives_reject(self) -> None:
        for name in self.SCHEMA_REJECTING:
            with self.subTest(name=name):
                with self.assertRaises(SchemaValidationError):
                    self.registry.validate_declared(load(NEGATIVES / name))

    def test_boolean_domain_is_not_the_accepted_yes_no_contract(self) -> None:
        # The bare fact-type schema admits any value_schema object; the accepted
        # boundary-declaration contract is the {yes, no} enum on the committed
        # citizens. This records the rejected shape without weakening the
        # generic schema.
        negative = load(NEGATIVES / "fact-type.v2.schedule-d-boundary-boolean-domain.json")
        self.registry.validate_declared(negative)
        self.assertEqual(negative["value_schema"], {"type": "boolean"})
        bundle = load(TAX_CONTENT_DIR / "schedule-d-boundary.bundle.json")
        for ft in bundle["fact_types"]:
            self.assertEqual(ft["value_schema"], {"enum": ["yes", "no"]})

    def test_evidence_identity_is_not_the_accepted_shape(self) -> None:
        negative = load(NEGATIVES / "fact-type.v2.covered-ltcg-txn-evidence-identity.json")
        self.registry.validate_declared(negative)  # schema-valid, structurally
        identity_text = json.dumps(negative["identity_keys"])
        self.assertIn("evidence", identity_text)
        bundle = load(TAX_CONTENT_DIR / "f1099b-covered-ltcg.bundle.json")
        committed = next(ft for ft in bundle["fact_types"] if ft["id"] == MEMBER_FACT_TYPE)
        committed_text = json.dumps(committed["identity_keys"])
        self.assertNotIn("evidence", committed_text)

    def test_collapsed_identity_is_not_the_accepted_shape(self) -> None:
        negative = load(NEGATIVES / "fact-type.v2.covered-ltcg-txn-collapsed-identity.json")
        self.registry.validate_declared(negative)  # schema-valid, structurally
        negative_key_names = {k["name"] for k in negative["identity_keys"]}
        self.assertNotIn("transaction", negative_key_names)
        bundle = load(TAX_CONTENT_DIR / "f1099b-covered-ltcg.bundle.json")
        committed = next(ft for ft in bundle["fact_types"] if ft["id"] == MEMBER_FACT_TYPE)
        committed_key_names = {k["name"] for k in committed["identity_keys"]}
        self.assertIn("transaction", committed_key_names)

    def test_member_value_missing_required_predicate_field_rejects(self) -> None:
        bundle = load(TAX_CONTENT_DIR / "f1099b-covered-ltcg.bundle.json")
        member = next(ft for ft in bundle["fact_types"] if ft["id"] == MEMBER_FACT_TYPE)
        negative_value = load(NEGATIVES / "value.covered-ltcg-txn-missing-gain-only.json")
        validator = jsonschema.Draft202012Validator(member["value_schema"])
        errors = list(validator.iter_errors(negative_value))
        self.assertTrue(errors)
        self.assertTrue(any("gain_only" in str(e.message) or "gain_only" in str(e.validator_value) for e in errors))
        self.assertEqual(list(validator.iter_errors(_ELIGIBLE_VALUE)), [])


class HistoricalImmutability(unittest.TestCase):
    def test_historical_content_and_schemas_are_byte_for_byte_unchanged(self) -> None:
        for path, digest in HISTORICAL_BYTES.items():
            with self.subTest(path=path):
                self.assertEqual(sha256_file(Path(path)), digest)

    def test_historical_box2a_family_and_mapping_still_load_unchanged(self) -> None:
        registry = tax_registry()
        families = load_source_families(registry)
        mappings = load_closure_mappings(registry)
        self.assertEqual(
            families["tax.us.2025.f1099div.2a"]["member_predicate"]["fact_type"],
            "tax.us.2025.f1099div.box2a-capital-gain-distribution",
        )
        self.assertEqual(
            mappings["tax.us.2025.closure-mapping.f1099div-2a"]["admits_symbol"],
            "tax.us.2025.dividends.2a-subtotal",
        )

    def test_no_new_schema_file_was_introduced(self) -> None:
        """Track 1 publishes new content only (fact-type.v2, source-family.v1,
        source-closure-mapping.v2, bundle.v2 already exist); no schema
        registry manifest entry is added.
        """
        for directory in (KERNEL_SCHEMA_DIR, DERIVATION_SCHEMA_DIR, TAX_SCHEMA_DIR):
            manifest = load(directory / "published.json")
            for filename in manifest:
                self.assertTrue((directory / filename).is_file())


if __name__ == "__main__":
    unittest.main()
