"""Synthetic consumer for the production Form 1098 circumstance defaults.

This named test-only consumer observes package validation, resolved run
material, marshalling and both runners. Its synthetic outputs are not a
mortgage calculation or a live coordinator result.
"""
from __future__ import annotations

import json
import unittest
from unittest import mock
from pathlib import Path
from typing import Any, cast

from packages.derivation.package_validation import validate_package
from packages.derivation.loader import DerivationSchemas
from packages.derivation.live import _resolved_run_material
from packages.derivation.marshal import marshal_run_context
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for
from packages.kernel.findings import project
from packages.tax.loader import load_f1098_circumstances_bundle
from tests.derivation.test_subject_declaration_live_path import (
    _both_runners,
    _lattice_type,
    _live_context,
    _ordinary_rule,
    _package,
    _resolve,
    _Graph,
    ADOPTION_PIN,
    GOVERNANCE_PINS,
)
import tests.derivation.test_subject_declaration_live_path as live_path
from tests.test_f1098_circumstances_vocabulary import _record_answer, _workspace
from tests.support import act

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "packages/content/tax/2025"
SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}
OUTPUTS = {
    "box9-number-of-properties": "demo.tax.f1098.defaults.box9",
    "loan-timing-relative-to-purchase": "demo.tax.f1098.defaults.purchase-timing",
    "loan-timing-relative-to-building-or-improving": "demo.tax.f1098.defaults.building-timing",
}
DEFAULT_PARAMETERS = {
    OUTPUTS["box9-number-of-properties"]: (
        "tax.us.2025.parameter.f1098-box9-default-single-property", "v1",
    ),
    OUTPUTS["loan-timing-relative-to-purchase"]: (
        "tax.us.2025.parameter.f1098-timing-purchase-structural-default", "v1",
    ),
    OUTPUTS["loan-timing-relative-to-building-or-improving"]: (
        "tax.us.2025.parameter.f1098-timing-building-structural-default", "v1",
    ),
}


def _parameter(filename: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / filename).read_text("utf-8")))


def _context_from_admitted_state(
    parts: list[tuple[dict[str, Any], str]], bindings: list[dict[str, Any]], state: Any
) -> Any:
    entries = [{"id": citizen["id"], "version": citizen["version"]} for citizen, _ in parts]
    validation, package = _resolve(parts, bindings=bindings, entrypoints=entries)
    if not validation.ok:
        raise AssertionError(validation.issues)
    material = _resolved_run_material(_Graph(list(validation.resolved_members), package))
    rules, parameters, families, mappings, fact_types, resolved_bindings, collect_names = material
    return marshal_run_context(
        run_id="demo.run.f1098.admitted-state",
        state=state,
        currency=compute_currency(state),
        rules=rules,
        parameters=parameters,
        canon={},
        adoption_pin=ADOPTION_PIN,
        governance_pins=GOVERNANCE_PINS,
        family_declarations=families,
        closure_mappings=mappings,
        fact_types=fact_types,
        input_bindings=resolved_bindings,
        collect_source_names=collect_names,
        emission_only_source_names=list(material.emission_only_names),
    )


class SyntheticF1098DefaultConsumer(unittest.TestCase):
    def _parts(self) -> tuple[list[tuple[dict[str, Any], str]], list[dict[str, Any]]]:
        bundle = load_f1098_circumstances_bundle()
        by_id = {ft["id"]: ft for ft in bundle["fact_types"]}
        parameters = [
            _parameter("parameter.f1098-box9-default-single-property.json"),
            _parameter("parameter.f1098-timing-purchase-structural-default.json"),
            _parameter("parameter.f1098-timing-building-structural-default.json"),
        ]
        parts: list[tuple[dict[str, Any], str]] = []
        bindings: list[dict[str, Any]] = []
        for i, (suffix, output) in enumerate(OUTPUTS.items()):
            fact_type = by_id[f"tax.us.2025.f1098.{suffix}"]
            parameter = fact_type["optional_default"]["parameter"]
            parts.append((fact_type, "fact-type"))
            parts.append((parameters[i], "parameter"))
            rule = _ordinary_rule(
                rule_id=f"demo.rule.f1098.default.{i}",
                publishes=output,
                value={"op": "ref", "name": fact_type["id"]},
                requires=[fact_type["id"]],
            )
            parts.append((rule, "computation"))
            bindings.append({
                "symbol": fact_type["id"],
                "fact_type": {"id": fact_type["id"], "version": fact_type["version"]},
                "mode": "optional_default",
            })
            self.assertEqual(parameter, {"id": parameters[i]["id"], "version": parameters[i]["version"]})
        return parts, bindings

    def test_absent_values_resolve_from_exact_declarations_through_both_runners(self) -> None:
        with mock.patch.object(live_path, "SCOPE", SCOPE):
            parts, bindings = self._parts()
            entries = [{"id": citizen["id"], "version": citizen["version"]} for citizen, _ in parts]
            _material, context = _live_context(parts, {}, {}, bindings=bindings, entrypoints=entries)
        forward, reference = _both_runners(context)
        expected = {
            OUTPUTS["box9-number-of-properties"]: "1",
            OUTPUTS["loan-timing-relative-to-purchase"]: "not-asked",
            OUTPUTS["loan-timing-relative-to-building-or-improving"]: "not-asked",
        }
        for result in (forward, reference):
            publications = {item.finding["symbol"]: item.finding for item in result.publications}
            findings = {item.finding["id"]: item.finding for item in result.publications}
            for symbol, value in expected.items():
                self.assertEqual(publications[symbol]["value"], value, result.dispositions)
                defaults = [
                    pin for pin in publications[symbol]["pins"]
                    if pin.get("origin") == "declared_default"
                ]
                self.assertEqual(len(defaults), 1)
                default_finding = findings[defaults[0]["id"]]
                parameter_pins = {
                    (pin["id"], pin["version"])
                    for pin in default_finding["pins"] if pin.get("role") == "parameter"
                }
                self.assertEqual(parameter_pins, {DEFAULT_PARAMETERS[symbol]})

    def test_preexisting_box9_v1_finding_remains_usable_under_v2_binding(self) -> None:
        with mock.patch.object(live_path, "SCOPE", SCOPE):
            parts, bindings = self._parts()
            original = json.loads((CONTENT / "f1098.bundle.json").read_text("utf-8"))
            box9_v1 = next(
                item for item in original["fact_types"]
                if item["id"] == "tax.us.2025.f1098.box9-number-of-properties"
            )
            parts.append((box9_v1, "fact-type"))
            entries = [{"id": citizen["id"], "version": citizen["version"]} for citizen, _ in parts]
            keys = (
                ("payer", "demo.f1098.lender.old"),
                ("statement", "demo.f1098.statement.old"),
                ("tax-year", "2025"),
            )
            fact_id = fact_id_for(box9_v1["id"], keys)
            lattice = {
                box9_v1["id"]: _lattice_type(box9_v1["id"], tuple((name, (value,)) for name, value in keys))
            }
            findings: dict[str, dict[str, Any]] = {
                "demo.finding.f1098.old-box9": {
                    "id": "demo.finding.f1098.old-box9", "fact_id": fact_id,
                    "value": 2, "basis": "attested",
                }
            }
            _material, context = _live_context(
                parts, findings, lattice, bindings=bindings, entrypoints=entries
            )
        forward, reference = _both_runners(context)
        for result in (forward, reference):
            publications = {item.finding["symbol"]: item.finding for item in result.publications}
            self.assertEqual(
                publications[OUTPUTS["box9-number-of-properties"]]["value"], "2",
                result.dispositions,
            )
            pins = publications[OUTPUTS["box9-number-of-properties"]]["pins"]
            self.assertFalse(any(pin.get("origin") == "declared_default" for pin in pins))

    def test_timing_answer_overrides_not_asked_default(self) -> None:
        timing_facts = (
            ("loan-timing-relative-to-purchase", "demo.f1098.lender.answer"),
            ("loan-timing-relative-to-building-or-improving", "demo.f1098.lender.building-answer"),
        )
        for timing_suffix, payer in timing_facts:
            for answer in ("yes", "no", "cannot-tell"):
                with self.subTest(timing_fact=timing_suffix, answer=answer):
                    with mock.patch.object(live_path, "SCOPE", SCOPE):
                        parts, bindings = self._parts()
                        entries = [{"id": citizen["id"], "version": citizen["version"]} for citizen, _ in parts]
                        timing_type = f"tax.us.2025.f1098.{timing_suffix}"
                        keys = (
                            ("payer", payer),
                            ("statement", f"demo.f1098.statement.{timing_suffix}.{answer}"),
                            ("tax-year", "2025"),
                        )
                        fact_id = fact_id_for(timing_type, keys)
                        box9_type = "tax.us.2025.f1098.box9-number-of-properties"
                        box9_keys = (
                            ("payer", "demo.f1098.lender.box9-answer"),
                            ("statement", f"demo.f1098.statement.box9-answer.{timing_suffix}.{answer}"),
                            ("tax-year", "2025"),
                        )
                        box9_fact_id = fact_id_for(box9_type, box9_keys)
                        lattice = {
                            timing_type: _lattice_type(
                                timing_type, tuple((name, (value,)) for name, value in keys)
                            ),
                            box9_type: _lattice_type(
                                box9_type, tuple((name, (value,)) for name, value in box9_keys)
                            ),
                        }
                        findings: dict[str, dict[str, Any]] = {
                            f"demo.finding.f1098.timing-answer.{timing_suffix}.{answer}": {
                                "id": f"demo.finding.f1098.timing-answer.{timing_suffix}.{answer}",
                                "fact_id": fact_id, "value": answer, "basis": "attested",
                            },
                            f"demo.finding.f1098.box9-answer.{timing_suffix}.{answer}": {
                                "id": f"demo.finding.f1098.box9-answer.{timing_suffix}.{answer}",
                                "fact_id": box9_fact_id, "value": 2, "basis": "attested",
                            },
                        }
                        _material, context = _live_context(
                            parts, findings, lattice, bindings=bindings, entrypoints=entries
                        )
                    forward, reference = _both_runners(context)
                    symbol = OUTPUTS[timing_suffix]
                    box9_symbol = OUTPUTS["box9-number-of-properties"]
                    for result in (forward, reference):
                        publications = {item.finding["symbol"]: item.finding for item in result.publications}
                        self.assertEqual(publications[symbol]["value"], answer, result.dispositions)
                        self.assertEqual(publications[box9_symbol]["value"], "2", result.dispositions)
                        self.assertFalse(
                            any(pin.get("origin") == "declared_default" for pin in publications[symbol]["pins"])
                        )
                        self.assertFalse(
                            any(pin.get("origin") == "declared_default" for pin in publications[box9_symbol]["pins"])
                        )

    def test_retracting_timing_answer_restores_reserved_default(self) -> None:
        for timing_suffix, statement, answer_id in (
            ("loan-timing-relative-to-purchase", "demo.f1098.statement.a", "purchase"),
            ("loan-timing-relative-to-building-or-improving", "demo.f1098.statement.a", "building"),
        ):
            with self.subTest(timing_fact=timing_suffix):
                with mock.patch.object(live_path, "SCOPE", SCOPE):
                    raw, log, registry = _workspace()
                    with raw:
                        timing_type = f"tax.us.2025.f1098.{timing_suffix}"
                        finding_id = _record_answer(
                            log, registry, timing_type, statement, "yes",
                            f"withdrawal.timing-answer.{answer_id}",
                        )
                        parts, bindings = self._parts()
                        before = project(log.read().acts, registry)
                        self.assertIn(finding_id, compute_currency(before).current_finding_ids)
                        context_before = _context_from_admitted_state(parts, bindings, before)
                        revision = log.read().revision
                        log.append(
                            act(revision, "finding-retracted", {"finding_id": finding_id}),
                            expected_revision=revision,
                        )
                        after = project(log.read().acts, registry)
                        self.assertNotIn(finding_id, compute_currency(after).current_finding_ids)
                        context_after = _context_from_admitted_state(parts, bindings, after)
                    before_results = _both_runners(context_before)
                    after_results = _both_runners(context_after)
                symbol = OUTPUTS[timing_suffix]
                for result in before_results:
                    published = next(item.finding for item in result.publications if item.finding["symbol"] == symbol)
                    self.assertEqual(published["value"], "yes")
                for result in after_results:
                    publications = {item.finding["symbol"]: item.finding for item in result.publications}
                    self.assertEqual(publications[symbol]["value"], "not-asked", result.dispositions)
                    defaults = [
                        pin for pin in publications[symbol]["pins"]
                        if pin.get("origin") == "declared_default"
                    ]
                    self.assertEqual(len(defaults), 1)
                    findings = {item.finding["id"]: item.finding for item in result.publications}
                    parameter_pins = {
                        (pin["id"], pin["version"])
                        for pin in findings[defaults[0]["id"]]["pins"]
                        if pin.get("role") == "parameter"
                    }
                    self.assertEqual(parameter_pins, {DEFAULT_PARAMETERS[symbol]})

    def test_missing_pinned_parameter_is_a_validation_failure(self) -> None:
        with mock.patch.object(live_path, "SCOPE", SCOPE):
            parts, bindings = self._parts()
            parts = [(citizen, role) for citizen, role in parts
                     if citizen.get("id") != "tax.us.2025.parameter.f1098-timing-building-structural-default"]
            entries = [{"id": citizen["id"], "version": citizen["version"]} for citizen, _ in parts]
            package_parts = [(citizen, role) for citizen, role in parts]
            package = _package(package_parts, bindings=bindings, entrypoints=entries)
            corpus = {(citizen["id"], citizen["version"]): citizen for citizen, _ in package_parts}
            validation = validate_package(package, corpus, DerivationSchemas())
        self.assertFalse(validation.ok)
        self.assertIn("BINDING_DEFAULT_ABSENT", {issue.code for issue in validation.issues}, validation.issues)


if __name__ == "__main__":
    unittest.main()
