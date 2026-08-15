"""Track 2 Form 1098-E family and the twelve T0-2 eligibility components.

Facts-only track (no consuming rule yet): the member statement family
(box 1 + box 2 companion), the eleven newly-minted eligibility components,
and the one reused component (filing status). Fixtures prove VOID exclusion
at admission and multi-statement/multi-lender cardinality directly at the
kernel finding/horizon projection layer -- there is no worksheet rule yet
to drive through `live_coordinate_run`.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any, cast

import jsonschema

from packages.kernel.findings import FindingModelError, apply_act, initial_state
from packages.tax.loader import (
    TAX_CONTENT_DIR,
    domain_companion_presence_pairs,
    domain_companion_value_domains,
    tax_registry,
)


ROOT = Path(__file__).resolve().parent.parent
CONTENT = TAX_CONTENT_DIR

BOX1 = "tax.us.2025.f1098e.box1-student-loan-interest"
BOX2 = "tax.us.2025.f1098e.box2-checked-authority"
FAMILY_ID = "tax.us.2025.f1098e.1"
CLOSURE_TYPE = "tax.us.2025.f1098e.1.source-closure"

PER_STATEMENT_COMPONENTS = (
    "tax.us.2025.f1098e.no-related-person-interest",
    "tax.us.2025.f1098e.no-qualified-employer-plan-interest",
    "tax.us.2025.f1098e.no-non-qualified-loan-component",
    "tax.us.2025.f1098e.no-employer-educational-assistance-interest",
    "tax.us.2025.f1098e.no-qtp-earnings-used",
)

FILER_LEVEL_UNIVERSAL_COMPONENTS = (
    "tax.us.2025.sli-scope.no-form-2555",
    "tax.us.2025.sli-scope.no-form-4563",
    "tax.us.2025.sli-scope.no-puerto-rico-or-samoa-income",
)

LEGAL_ZERO_COMPONENTS = (
    "tax.us.2025.sli-scope.not-claimed-as-dependent",
    "tax.us.2025.sli-scope.legally-obligated-for-interest",
)

REUSED_FILING_STATUS = "tax.us.2025.filing-status"


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


def _act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.sli.act.{index:03d}",
        "kind": kind,
        "actor": "demo.user.filer-1",
        "at": f"2026-08-15T12:{index // 60:02d}:{index % 60:02d}Z",
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


def _entity(entity_id: str, kind: str, label: str) -> dict[str, object]:
    return {
        "schema": "entity.v1",
        "id": entity_id,
        "kind": kind,
        "label": label,
    }


def _project(acts: list[dict[str, object]]) -> Any:
    registry = tax_registry()
    state = initial_state()
    for act in acts:
        state = apply_act(state, act, registry)
    return state


def _statement_acts(
    *,
    index: int,
    act_offset: int,
    lender_id: str,
    statement_id: str,
    amount: float,
    box2: object = None,
) -> tuple[list[dict[str, object]], int]:
    """Introduce a lender/statement pair (idempotent per lender) and assert box 1/2."""
    acts: list[dict[str, object]] = []
    n = act_offset
    acts.append(_act(n, "entity-introduced", {
        "entity": _entity(statement_id, "tax.us.1098e-statement", f"Synthetic 1098-E statement {index}"),
    }))
    n += 1
    acts.append(_act(n, "assertion", {
        "finding": _attested(
            f"demo.sli.finding.box2.{index}",
            f"{BOX2}|lender={lender_id},statement={statement_id},tax-year=2025",
            box2,
        )
    }))
    n += 1
    return acts, n


class ContractCases(unittest.TestCase):
    """T0-1 identity/VOID-disposition and T0-2 component-classification shape."""

    def test_box1_identity_and_nonnegative(self) -> None:
        bundle = _load("f1098e.bundle.json")
        amount = next(ft for ft in bundle["fact_types"] if ft["id"] == BOX1)
        self.assertEqual(
            [key["name"] for key in amount["identity_keys"]],
            ["lender", "statement", "tax-year"],
        )
        self.assertEqual(amount["value_schema"], {"type": "number", "minimum": 0})
        identity_text = json.dumps(amount["identity_keys"])
        for forbidden in ("evidence", "file", "upload", "document", "scan"):
            self.assertNotIn(forbidden, identity_text)
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(-1, amount["value_schema"])

    def test_no_void_field_exists_on_the_member_fact_type(self) -> None:
        """A VOID-checked copy has no schema field to be represented by at all
        (the identity keys and value_schema are the only structurally
        admissible surface; "VOID" appears only in explanatory prose)."""
        bundle = _load("f1098e.bundle.json")
        for fact_type in bundle["fact_types"]:
            structural = json.dumps(
                {"identity_keys": fact_type["identity_keys"], "value_schema": fact_type["value_schema"]}
            ).lower()
            self.assertNotIn("void", structural, fact_type["id"])

    def test_box2_admits_only_absent_or_false(self) -> None:
        bundle = _load("f1098e.bundle.json")
        auth = next(ft for ft in bundle["fact_types"] if ft["id"] == BOX2)
        jsonschema.validate(None, auth["value_schema"])
        jsonschema.validate(False, auth["value_schema"])
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(True, auth["value_schema"])

    def test_account_number_is_never_an_identity_key(self) -> None:
        bundle = _load("f1098e.bundle.json")
        blob = json.dumps(bundle)
        self.assertNotIn("account-number", blob)
        self.assertNotIn("account_number", blob)

    def test_family_declares_box1_as_sole_member_predicate(self) -> None:
        family = _load("family.f1098e-1.json")
        self.assertEqual(family["id"], FAMILY_ID)
        self.assertEqual(family["member_predicate"]["fact_type"], BOX1)
        self.assertEqual(
            family["scope"],
            {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        )
        self.assertTrue(family["authorizes_subtotal"])
        self.assertIn("VOID", family["closure_claim"])

    def test_twelve_components_accounted_for_exactly_once(self) -> None:
        """Ten universal + two legal-zero; component 1 reused, component 8 embedded."""
        f1098e = {ft["id"] for ft in _load("f1098e.bundle.json")["fact_types"]}
        sli_scope = {ft["id"] for ft in _load("sli-scope.bundle.json")["fact_types"]}

        # Component 1: filing status != MFS -- reused, never minted.
        self.assertIn(REUSED_FILING_STATUS, self._core_vocabulary_ids())

        # Components 2-4: minted new, SLI-scoped (never reusing ss-benefits-scope).
        for component in FILER_LEVEL_UNIVERSAL_COMPONENTS:
            self.assertIn(component, sli_scope)

        # Components 5-7, 9-10: per-statement universal witnesses.
        for component in PER_STATEMENT_COMPONENTS:
            self.assertIn(component, f1098e)

        # Component 8: box-2 checked authority, embedded in the statement
        # bundle itself, not a separate scope declaration.
        self.assertIn(BOX2, f1098e)

        # Components 11-12: legal zero, filer-level.
        for component in LEGAL_ZERO_COMPONENTS:
            self.assertIn(component, sli_scope)

        total_new = len(FILER_LEVEL_UNIVERSAL_COMPONENTS) + len(PER_STATEMENT_COMPONENTS) + len(LEGAL_ZERO_COMPONENTS) + 1  # +1 for box2
        self.assertEqual(total_new, 11)

    def test_sli_scope_components_not_reused_from_ss_benefits_scope(self) -> None:
        ss_benefits = {ft["id"] for ft in _load("ss-benefits-scope.bundle.json")["fact_types"]}
        sli_scope = {ft["id"] for ft in _load("sli-scope.bundle.json")["fact_types"]}
        for component in FILER_LEVEL_UNIVERSAL_COMPONENTS:
            counterpart = component.replace("sli-scope", "ss-benefits-scope")
            self.assertIn(counterpart, ss_benefits, "expected an ss-benefits-scope counterpart to exist")
            self.assertNotIn(component, ss_benefits)
            self.assertNotEqual(component, counterpart)

    def test_legal_zero_components_are_yes_no_domain_like_universal_ones(self) -> None:
        """Shape is identical to universal components; polarity/consumption differs at Track 3."""
        sli_scope = {ft["id"]: ft for ft in _load("sli-scope.bundle.json")["fact_types"]}
        for component in LEGAL_ZERO_COMPONENTS:
            self.assertEqual(
                sli_scope[component]["value_schema"],
                {"type": "string", "enum": ["yes", "no"]},
            )
            self.assertIn("legal zero", sli_scope[component]["title"].lower())
        for component in FILER_LEVEL_UNIVERSAL_COMPONENTS:
            self.assertNotIn("legal zero", sli_scope[component]["title"].lower())

    def test_companion_presence_pair_registered(self) -> None:
        reg = tax_registry()
        self.assertIn(BOX1, reg.companion_presence_pairs)
        self.assertEqual(reg.companion_presence_pairs[BOX1], BOX2)
        self.assertEqual(domain_companion_presence_pairs()[BOX1], BOX2)
        self.assertEqual(domain_companion_value_domains()[BOX2], frozenset({None, False}))

    def _core_vocabulary_ids(self) -> set[str]:
        blob = _load("core_calculations.bundle.json")
        return {ft["id"] for ft in blob["fact_types"]}


class KernelProjectionCases(unittest.TestCase):
    """VOID exclusion at admission and multi-statement/multi-lender cardinality."""

    def _base_acts(self) -> tuple[list[dict[str, object]], int]:
        acts: list[dict[str, object]] = []
        acts.append(_act(0, "bundle-adoption", {"bundle": _load("f1098e.bundle.json")}))
        return acts, 1

    def test_p1_two_lenders_two_statements_both_admitted(self) -> None:
        """A return with 1098-E statements from two different lenders admits both."""
        acts, n = self._base_acts()
        for index, (lender_suffix, amount) in enumerate([("a", 500.0), ("b", 250.0)]):
            lender_id = f"demo.sli.lender.{lender_suffix}"
            statement_id = f"demo.sli.stmt.{lender_suffix}"
            acts.append(_act(n, "entity-introduced", {
                "entity": _entity(lender_id, "tax.us.student-loan-lender", f"Synthetic lender {lender_suffix}"),
            }))
            n += 1
            stmt_acts, n = _statement_acts(
                index=index, act_offset=n, lender_id=lender_id, statement_id=statement_id, amount=amount,
            )
            acts.extend(stmt_acts)

        acts.append(_act(n, "horizon-genesis", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "horizon_id": "demo.sli.h0",
        }))
        n += 1
        horizon = "demo.sli.h0"
        for index, (lender_suffix, amount) in enumerate([("a", 500.0), ("b", 250.0)]):
            lender_id = f"demo.sli.lender.{lender_suffix}"
            statement_id = f"demo.sli.stmt.{lender_suffix}"
            next_horizon = f"demo.sli.h{index + 1}"
            acts.append(_act(n, "member-transition", {
                "family": {"id": FAMILY_ID, "version": "v1"},
                "scope": {"tax-year": "2025", "subject": "demo.primary"},
                "member": {
                    "action": "assert",
                    "finding": _attested(
                        f"demo.sli.finding.box1.{index}",
                        f"{BOX1}|lender={lender_id},statement={statement_id},tax-year=2025",
                        amount,
                    ),
                },
                "successor": {"id": next_horizon, "predecessor": horizon},
            }))
            n += 1
            horizon = next_horizon

        state = _project(acts)
        box1_findings = [f for f in state.findings.values() if f["fact_id"].startswith(BOX1 + "|")]
        self.assertEqual(len(box1_findings), 2)
        fact_ids = {f["fact_id"] for f in box1_findings}
        self.assertIn(f"{BOX1}|lender=demo.sli.lender.a,statement=demo.sli.stmt.a,tax-year=2025", fact_ids)
        self.assertIn(f"{BOX1}|lender=demo.sli.lender.b,statement=demo.sli.stmt.b,tax-year=2025", fact_ids)
        self.assertEqual({f["value"] for f in box1_findings}, {500.0, 250.0})

    def test_p2_same_lender_two_statements_both_admitted(self) -> None:
        """One lender furnishing two statements (e.g. two loans) admits both."""
        acts, n = self._base_acts()
        lender_id = "demo.sli.lender.shared"
        acts.append(_act(n, "entity-introduced", {
            "entity": _entity(lender_id, "tax.us.student-loan-lender", "Synthetic shared lender"),
        }))
        n += 1
        for index, amount in enumerate([700.0, 300.0]):
            statement_id = f"demo.sli.stmt.shared.{index}"
            stmt_acts, n = _statement_acts(
                index=index, act_offset=n, lender_id=lender_id, statement_id=statement_id, amount=amount,
            )
            acts.extend(stmt_acts)

        acts.append(_act(n, "horizon-genesis", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "horizon_id": "demo.sli.h0",
        }))
        n += 1
        horizon = "demo.sli.h0"
        for index, amount in enumerate([700.0, 300.0]):
            statement_id = f"demo.sli.stmt.shared.{index}"
            next_horizon = f"demo.sli.h{index + 1}"
            acts.append(_act(n, "member-transition", {
                "family": {"id": FAMILY_ID, "version": "v1"},
                "scope": {"tax-year": "2025", "subject": "demo.primary"},
                "member": {
                    "action": "assert",
                    "finding": _attested(
                        f"demo.sli.finding.box1.shared.{index}",
                        f"{BOX1}|lender={lender_id},statement={statement_id},tax-year=2025",
                        amount,
                    ),
                },
                "successor": {"id": next_horizon, "predecessor": horizon},
            }))
            n += 1
            horizon = next_horizon

        state = _project(acts)
        box1_findings = [f for f in state.findings.values() if f["fact_id"].startswith(BOX1 + "|")]
        self.assertEqual(len(box1_findings), 2)
        self.assertEqual({f["value"] for f in box1_findings}, {700.0, 300.0})

    def test_n1_void_statement_never_becomes_a_member(self) -> None:
        """A filer who received one VOID copy and one valid original submits only
        the valid one; the VOID copy leaves no trace because there is nothing
        for it to be admitted as -- proving exclusion at admission, not a
        post-hoc filter over a member that was never created."""
        acts, n = self._base_acts()
        lender_id = "demo.sli.lender.void-case"
        # Only the valid statement is ever introduced; the VOID copy's
        # underlying loan is real, but the VOID'd document itself never
        # produces an entity, a box-1 finding, or any other trace.
        statement_id = "demo.sli.stmt.valid-only"
        acts.append(_act(n, "entity-introduced", {
            "entity": _entity(lender_id, "tax.us.student-loan-lender", "Synthetic lender, VOID scenario"),
        }))
        n += 1
        stmt_acts, n = _statement_acts(
            index=0, act_offset=n, lender_id=lender_id, statement_id=statement_id, amount=150.0,
        )
        acts.extend(stmt_acts)
        acts.append(_act(n, "horizon-genesis", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "horizon_id": "demo.sli.h0",
        }))
        n += 1
        acts.append(_act(n, "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {
                "action": "assert",
                "finding": _attested(
                    "demo.sli.finding.box1.valid",
                    f"{BOX1}|lender={lender_id},statement={statement_id},tax-year=2025",
                    150.0,
                ),
            },
            "successor": {"id": "demo.sli.h1", "predecessor": "demo.sli.h0"},
        }))

        state = _project(acts)
        box1_findings = [f for f in state.findings.values() if f["fact_id"].startswith(BOX1 + "|")]
        self.assertEqual(len(box1_findings), 1)
        self.assertEqual(box1_findings[0]["value"], 150.0)

    def test_n2_box1_via_plain_assertion_rejected(self) -> None:
        """The kernel-level member-only-through-transition invariant applies here."""
        acts, n = self._base_acts()
        lender_id = "demo.sli.lender.bad"
        statement_id = "demo.sli.stmt.bad"
        acts.append(_act(n, "entity-introduced", {
            "entity": _entity(lender_id, "tax.us.student-loan-lender", "Synthetic lender"),
        }))
        n += 1
        acts.append(_act(n, "entity-introduced", {
            "entity": _entity(statement_id, "tax.us.1098e-statement", "Synthetic statement"),
        }))
        n += 1
        acts.append(_act(n, "assertion", {
            "finding": _attested(
                "demo.sli.finding.box1.bad",
                f"{BOX1}|lender={lender_id},statement={statement_id},tax-year=2025",
                100.0,
            )
        }))
        registry = tax_registry()
        state = initial_state()
        for act in acts[:-1]:
            state = apply_act(state, act, registry)
        with self.assertRaises(FindingModelError) as ctx:
            apply_act(state, acts[-1], registry)
        self.assertIn("member-transition", str(ctx.exception))

    def test_n3_box2_checked_true_rejected(self) -> None:
        acts, n = self._base_acts()
        lender_id = "demo.sli.lender.checked"
        statement_id = "demo.sli.stmt.checked"
        acts.append(_act(n, "entity-introduced", {
            "entity": _entity(lender_id, "tax.us.student-loan-lender", "Synthetic lender"),
        }))
        n += 1
        acts.append(_act(n, "entity-introduced", {
            "entity": _entity(statement_id, "tax.us.1098e-statement", "Synthetic statement"),
        }))
        n += 1
        acts.append(_act(n, "assertion", {
            "finding": _attested(
                "demo.sli.finding.box2.checked",
                f"{BOX2}|lender={lender_id},statement={statement_id},tax-year=2025",
                True,
            )
        }))
        registry = tax_registry()
        state = initial_state()
        for act in acts[:-1]:
            state = apply_act(state, act, registry)
        with self.assertRaises(FindingModelError):
            apply_act(state, acts[-1], registry)

    def test_n4_missing_box2_companion_rejected(self) -> None:
        acts, n = self._base_acts()
        lender_id = "demo.sli.lender.nocompanion"
        statement_id = "demo.sli.stmt.nocompanion"
        acts.append(_act(n, "entity-introduced", {
            "entity": _entity(lender_id, "tax.us.student-loan-lender", "Synthetic lender"),
        }))
        n += 1
        acts.append(_act(n, "entity-introduced", {
            "entity": _entity(statement_id, "tax.us.1098e-statement", "Synthetic statement"),
        }))
        n += 1
        # No box-2 assertion at all before the member-transition.
        acts.append(_act(n, "horizon-genesis", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "horizon_id": "demo.sli.h0",
        }))
        n += 1
        acts.append(_act(n, "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {
                "action": "assert",
                "finding": _attested(
                    "demo.sli.finding.box1.nocompanion",
                    f"{BOX1}|lender={lender_id},statement={statement_id},tax-year=2025",
                    100.0,
                ),
            },
            "successor": {"id": "demo.sli.h1", "predecessor": "demo.sli.h0"},
        }))
        registry = tax_registry()
        state = initial_state()
        for act in acts[:-1]:
            state = apply_act(state, act, registry)
        with self.assertRaises(FindingModelError) as ctx:
            apply_act(state, acts[-1], registry)
        self.assertIn("companion presence violated", str(ctx.exception))

    def test_p3_closed_empty_family_is_lawful(self) -> None:
        """A filer with no Form 1098-E statements at all: genesis + closure, no members."""
        acts, n = self._base_acts()
        acts.append(_act(n, "horizon-genesis", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "horizon_id": "demo.sli.h0",
        }))
        n += 1
        acts.append(_act(n, "assertion", {
            "finding": _attested(
                "demo.sli.closure.empty",
                f"{CLOSURE_TYPE}|family-horizon=demo.sli.h0,tax-year=2025",
                True,
            )
        }))
        state = _project(acts)
        box1_findings = [f for f in state.findings.values() if f["fact_id"].startswith(BOX1 + "|")]
        self.assertEqual(box1_findings, [])
        closure_findings = [f for f in state.findings.values() if f["fact_id"].startswith(CLOSURE_TYPE + "|")]
        self.assertEqual(len(closure_findings), 1)
        self.assertTrue(closure_findings[0]["value"])


if __name__ == "__main__":
    unittest.main()
