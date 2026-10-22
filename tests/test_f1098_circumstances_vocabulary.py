"""Production mortgage circumstance vocabulary and ordinary finding lifecycle."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

import pytest

from packages.derivation.loader import DerivationSchemas
from packages.kernel.act_log import ActLog
from packages.kernel.contribution import ContributionError, apply_contribution_batch
from packages.kernel.facts import fact_id_for
from packages.kernel.currency import compute_currency
from packages.kernel.findings import project
from packages.tax.loader import install_domain_scoped_supersession, load_f1098_circumstances_bundle
from tests.support import act, demo_entity, demo_evidence


PAYER = "demo.f1098.lender"
STATEMENT_A = "demo.f1098.statement.a"
STATEMENT_B = "demo.f1098.statement.b"
FACT = "tax.us.2025.f1098.paid-the-interest"
def _record_answer(log: ActLog, registry: Any, fact_type: str, statement: str, value: Any, label: str) -> str:
    """Admit a synthetic witness through contribution and ActLog paths."""
    is_internal = fact_type.endswith((
        ".residence-interest-reason", ".inert-path-unwritten",
    ))
    before = log.read()
    evidence_id = f"demo.evidence.f1098.{label}"
    contribution_id = f"demo.contribution.f1098.{label}"
    finding_id = f"demo.finding.f1098.{label}"
    identity_keys = (
        (("marker", "unused"),) if fact_type.endswith(".inert-path-unwritten") else
        (("payer", PAYER), ("statement", statement), ("tax-year", "2025"))
    )
    finding = {
        "schema": "finding.v2", "id": finding_id,
        "fact_id": fact_id_for(fact_type, identity_keys),
        "value": value, "basis": "attested", "evidence_ids": [evidence_id],
        "contribution_id": contribution_id,
    }
    staged = list(before.acts)
    evidence_title = (
        "Synthetic content-admission witness; not a user answer"
        if is_internal else "Synthetic Form 1098 circumstance answer"
    )
    evidence = act(len(staged), "evidence-submitted", {"evidence": demo_evidence(
        evidence_id, evidence_title, {"label": label},
    )})
    staged.append(evidence)
    contribution = act(len(staged), "contribution", {"contribution": {
        "schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id,
        "content": {
            "mode": "content-admission-witness" if is_internal else "manual-entry",
            "synthetic": True,
        },
    }})
    assertion = act(len(staged) + 1, "assertion", {"finding": finding})
    base = project(tuple(staged), registry)
    admitted = apply_contribution_batch(
        base, contribution_act=contribution, successor_acts=[assertion],
        registry=registry, record_id=f"demo.contribution-record.f1098.{label}",
    )
    if admitted.terminal_record["phase"] != "completed":
        raise AssertionError(admitted.terminal_record)
    for item in (evidence, contribution, assertion):
        log.append(item, expected_revision=log.read().revision)
    return finding_id


def _workspace() -> tuple[tempfile.TemporaryDirectory[str], ActLog, Any]:
    raw = tempfile.TemporaryDirectory(prefix="f1098-circumstances-")
    registry = DerivationSchemas().registry
    install_domain_scoped_supersession(registry)
    log = ActLog(Path(raw.name) / "workspace", registry)
    old_bundle = json.loads((Path(__file__).resolve().parents[1]
                             / "packages/content/tax/2025/f1098.bundle.json").read_text("utf-8"))
    circumstance_bundle = load_f1098_circumstances_bundle(registry)
    log.append(act(0, "bundle-adoption", {"bundle": old_bundle}), expected_revision=0)
    log.append(act(1, "bundle-adoption", {"bundle": circumstance_bundle}), expected_revision=1)
    log.append(act(2, "entity-introduced", {"entity": demo_entity(
        PAYER, "Synthetic mortgage lender", "tax.us.mortgage-lender",
    )}), expected_revision=2)
    for index, statement in enumerate((STATEMENT_A, STATEMENT_B), start=3):
        log.append(act(index, "entity-introduced", {"entity": demo_entity(
            statement, f"Synthetic statement {statement.rsplit('.', 1)[-1]}",
            "tax.us.1098-statement",
        )}), expected_revision=index)
    return raw, log, registry


class CircumstanceVocabulary(unittest.TestCase):
    def test_bundle_loads_all_selected_types_and_exact_parameter_pins(self) -> None:
        bundle = load_f1098_circumstances_bundle()
        by_id = {item["id"]: item for item in bundle["fact_types"]}
        expected_ids = {
            "owns-the-home", "lives-there-most-of-the-time", "home-is-collateral",
            "owes-the-loan", "paid-the-interest", "no-one-else-owes-it",
            "what-the-money-paid-for", "this-is-the-original-loan",
            "mortgage-credit-certificate-received", "loan-timing-relative-to-purchase",
            "loan-timing-relative-to-building-or-improving", "box9-number-of-properties",
            "residence-interest-reason", "inert-path-unwritten",
        }
        self.assertEqual(bundle["version"], "v1")
        self.assertEqual(
            {citizen_id.removeprefix("tax.us.2025.f1098.") for citizen_id in by_id},
            expected_ids,
        )
        self.assertEqual(len(by_id), 14)
        self.assertEqual(
            by_id[FACT]["value_schema"]["enum"],
            ["yes", "paid-by-others-or-partial", "no", "cannot-tell"],
        )
        for suffix, parameter in (
            ("loan-timing-relative-to-purchase", "timing-purchase-structural-default"),
            ("loan-timing-relative-to-building-or-improving", "timing-building-structural-default"),
        ):
            item = by_id[f"tax.us.2025.f1098.{suffix}"]
            self.assertEqual(item["value_schema"]["enum"], ["yes", "no", "cannot-tell", "not-asked"])
            self.assertEqual(
                item["optional_default"]["parameter"],
                {"id": f"tax.us.2025.parameter.f1098-{parameter}", "version": "v1"},
            )
        self.assertEqual(by_id["tax.us.2025.f1098.box9-number-of-properties"]["version"], "v2")
        self.assertEqual(
            by_id["tax.us.2025.f1098.box9-number-of-properties"]["optional_default"]["parameter"],
            {"id": "tax.us.2025.parameter.f1098-box9-default-single-property", "version": "v1"},
        )
        self.assertEqual(
            len(by_id["tax.us.2025.f1098.residence-interest-reason"]["value_schema"]["oneOf"]),
            19,
        )
        self.assertEqual(
            by_id["tax.us.2025.f1098.inert-path-unwritten"]["identity_keys"],
            [{"name": "marker", "kind": "literal", "values": ["unused"]}],
        )
        for citizen_id, citizen in by_id.items():
            if citizen["id"].endswith(".inert-path-unwritten"):
                continue
            self.assertEqual(
                citizen["identity_keys"],
                [
                    {"name": "payer", "kind": "entity", "entity_kind": "tax.us.mortgage-lender"},
                    {"name": "statement", "kind": "entity", "entity_kind": "tax.us.1098-statement"},
                    {"name": "tax-year", "kind": "literal", "values": ["2025"]},
                ],
            )

    def test_payment_values_are_admitted_as_distinct_answers(self) -> None:
        raw, log, registry = _workspace()
        with raw:
            for index, value in enumerate(("yes", "paid-by-others-or-partial", "no", "cannot-tell")):
                statement = f"demo.f1098.statement.payment.{index}"
                revision = log.read().revision
                log.append(act(revision, "entity-introduced", {"entity": demo_entity(
                    statement, f"Synthetic payment statement {index}", "tax.us.1098-statement",
                )}), expected_revision=revision)
                _record_answer(log, registry, FACT, statement, value, f"payment.{index}")
            state = project(log.read().acts, registry)
            self.assertEqual(len(state.findings), 4)
            invalid_statement = "demo.f1098.statement.payment.invalid"
            revision = log.read().revision
            log.append(act(revision, "entity-introduced", {"entity": demo_entity(
                invalid_statement, "Synthetic invalid payment statement", "tax.us.1098-statement",
            )}), expected_revision=revision)
            with self.assertRaises(ContributionError):
                _record_answer(log, registry, FACT, invalid_statement, "partly-paid", "payment.invalid")

    @pytest.mark.live  # Durably admits every Form 1098 circumstance type and value, then projects the log.
    def test_every_bundle_type_and_selected_value_is_durably_admitted(self) -> None:
        raw, log, registry = _workspace()
        with raw:
            bundle = load_f1098_circumstances_bundle(registry)
            cursor = 0
            for fact_type in bundle["fact_types"]:
                schema = fact_type["value_schema"]
                values = schema.get("enum")
                if values is None and "oneOf" in schema:
                    values = [item["const"] for item in schema["oneOf"]]
                if values is None:
                    values = [1]
                for value in values:
                    statement = f"demo.f1098.statement.inventory.{cursor}"
                    if not fact_type["id"].endswith(".inert-path-unwritten"):
                        revision = log.read().revision
                        log.append(act(revision, "entity-introduced", {"entity": demo_entity(
                            statement, f"Synthetic inventory statement {cursor}",
                            "tax.us.1098-statement",
                        )}), expected_revision=revision)
                    _record_answer(log, registry, fact_type["id"], statement, value,
                                   f"inventory.{cursor}")
                    cursor += 1
            self.assertEqual(len(project(log.read().acts, registry).findings), cursor)

    def test_statement_identity_is_separate_and_correction_displaces_only_one(self) -> None:
        raw, log, registry = _workspace()
        with raw:
            initial = _record_answer(log, registry, FACT, STATEMENT_A, "yes", "lifecycle.a.initial")
            neighbor = _record_answer(log, registry, FACT, STATEMENT_B, "no", "lifecycle.b.current")
            corrected = _record_answer(
                log, registry, FACT, STATEMENT_A, "paid-by-others-or-partial", "lifecycle.a.corrected",
            )
            before = project(log.read().acts, registry)
            before_current = compute_currency(before).current_finding_ids
            self.assertIn(corrected, before_current)
            self.assertIn(neighbor, before_current)
            self.assertNotIn(initial, before_current)
            revision = log.read().revision
            log.append(act(revision, "finding-retracted", {"finding_id": corrected}), expected_revision=revision)
            after = project(log.read().acts, registry)
            current = compute_currency(after).current_finding_ids
            self.assertNotIn(initial, current)
            self.assertNotIn(corrected, current)
            self.assertIn(neighbor, current)
            self.assertEqual(after.retracted_finding_ids, frozenset({corrected}))
