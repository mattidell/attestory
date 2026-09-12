"""Durable contract-unit evidence for attachment-rule.v11.

All values and identifiers are synthetic.  These tests exercise the repaired
runner and standalone presentation contract directly; the prototype overlay is
deliberately not involved.
"""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable, cast

import jsonschema

from packages.derivation.authorization_closure import build_dependency_edges, rule_scoped_closure
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import _families_reached, package_instance_checksum
from packages.derivation.marshal import _rule_required_symbols
from packages.derivation.presentation_projection import (
    PresentationModelError,
    _resolve_attachment,
    build_presentation_model,
    validate_presentation_model,
)
from packages.derivation.runner import Publication, _Run
from packages.kernel.findings import FindingState


ROOT = Path(__file__).resolve().parents[2]
V11_SCHEMA = ROOT / "packages/schemas/tax/attachment-rule.v11.schema.json"
V11_EXAMPLE = ROOT / "packages/schemas/tax/examples/attachment-rule.v11.schedule-b-exclusive-presence.positive.json"
PRESENTATION_SAMPLE = ROOT / "packages/sample_data/nominee_return_integration_contract/presentation/provenance-groups.presentation-model.v1.json"
V29_PACKAGE = ROOT / "packages/sample_data/derivation/examples/artifact-package.v29.nominee-interest.positive.json"


class _Schemas:
    def validate_declared(self, _finding: dict[str, Any]) -> None:
        return None


def _rule() -> dict[str, Any]:
    return {
        "schema": "attachment-rule.v11",
        "id": "demo.rule.attachment.schedule-b",
        "version": "v1",
        "title": "Demo Schedule B",
        "scope": {"family": "demo", "jurisdiction": "demo", "tax_year": 2025},
        "attachment": {"authority": "demo", "form_id": "demo", "tax_year": 2025, "jurisdiction": "demo"},
        "publishes": "demo.schedule-b",
        "requirement": {
            "kind": "any_trigger",
            "triggers": [
                {
                    "subtotals": ["demo.interest.positive"],
                    "threshold_parameter": {"id": "demo.parameter.threshold", "version": "v1"},
                    "comparison": "strictly_greater_than",
                    "citation": {"id": "demo.citation.schedule-b", "version": "v1"},
                },
                {
                    "kind": "derived_activity",
                    "fact_type": {"id": "demo.interest.nominee-reduction", "version": "v1"},
                    "citation": {"id": "demo.citation.nominee", "version": "v1"},
                },
            ],
        },
        "completeness": {"required_answers": [{"check": "presence", "fact_type": {"id": "demo.answer", "version": "v1"}, "symbol": "demo.answer"}]},
        "itemizations": [
            {
                "part_id": "part-i",
                "label": "Demo Interest",
                "authority": {"kind": "single_family", "source_family": {"id": "demo.family.interest", "version": "v1"}},
                "row_sets": [{"rows": {"op": "collect_members", "member_fact_type": {"id": "demo.interest.amount", "version": "v1"}, "source_family": {"id": "demo.family.interest", "version": "v1"}}, "subtotal_symbol": "demo.interest.positive"}],
                "adjustment_rows": [
                    {
                        "kind": "nominee_distribution",
                        "label": "Nominee Distribution",
                        "sign": "negative",
                        "selection": {
                            "mode": "exclusive_presence",
                            "conflict": "refuse",
                            "paths": [
                                {"id": "legacy", "rows": {"op": "collect_members", "member_fact_type": {"id": "demo.legacy.nominee.amount", "version": "v1"}, "source_family": {"id": "demo.family.legacy-nominee", "version": "v1"}}, "subtotal_symbol": "demo.legacy.nominee"},
                                {"id": "derived", "rows": {"op": "enumerate_published", "fact_type": {"id": "demo.interest.nominee-reduction", "version": "v1"}}, "subtotal_symbol": "demo.derived.nominee"},
                            ],
                        },
                    }
                ],
                "tie_out": {"line_symbol": "demo.interest.taxable", "operation": "subtract", "positive_subtotals": ["demo.interest.positive"], "adjustment_subtotals": ["demo.legacy.nominee", "demo.derived.nominee"]},
            }
        ],
    }


def _fake_run(*, legacy: bool = False, derived: bool = False, accrued: bool = False, threshold: str = "0", positive: str = "100") -> _Run:
    run: Any = object.__new__(_Run)
    run.ctx = SimpleNamespace(
        run_id="demo.run.v11",
        adoption_pin={"role": "adoption", "id": "demo.package", "version": "v1"},
        governance_pins=[],
        parameters={"demo.parameter.threshold": {"values": threshold}},
    )
    run.schemas = _Schemas()
    run.use_v2 = True
    run.symbols = {"demo.interest.positive": positive, "demo.interest.taxable": positive, "demo.answer": "yes"}
    run.symbol_pin = {name: (f"finding:{name}", "v1", "input", "assertion") for name in run.symbols}
    run.sources = {"demo.interest.amount": [positive]}
    run.source_fids = {"demo.interest.amount": ["demo.interest.finding"]}
    if legacy:
        run.sources["demo.legacy.nominee.amount"] = ["100"]
        run.source_fids["demo.legacy.nominee.amount"] = ["demo.legacy.finding"]
        run.symbols["demo.legacy.nominee"] = "100"
        run.symbols["demo.interest.taxable"] = "0"
        run.symbol_pin["demo.legacy.nominee"] = ("demo.legacy.subtotal", "v1", "input", "assertion")
    run.publications = []
    if derived:
        finding = {"schema": "derived-finding.v2", "id": "finding:derived:nominee", "symbol": "demo.interest.nominee-reduction|report=demo", "value": "100", "version": "v2", "pins": []}
        run.publications = [Publication(act={"run_id": run.ctx.run_id, "finding": finding}, finding=finding)]
        run.symbols["demo.derived.nominee"] = "100"
        run.symbols["demo.interest.taxable"] = "0"
        run.symbol_pin["demo.derived.nominee"] = (finding["id"], "v2", "input", "assertion")
    if accrued:
        finding = {"schema": "derived-finding.v2", "id": "finding:derived:accrued", "symbol": "demo.interest.current-year-adjustment.pairing-scoped|report=demo", "value": "100", "version": "v2", "pins": []}
        run.publications.append(Publication(act={"run_id": run.ctx.run_id, "finding": finding}, finding=finding))
    run.dispositions = []
    run.blocked = []
    run.resolved = set()
    run.symbol_publisher = {}
    run.live_sources = []
    return cast(_Run, run)


def _presentation_attachment(
    schema: str,
    declared_adjustments: list[dict[str, Any]],
    serialized_adjustments: list[dict[str, Any]],
    *,
    part_sum: str = "0",
    legacy_active: bool = False,
    derived_active: bool = False,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], FindingState]:
    rule = {
        "schema": schema,
        "id": "demo.rule.presentation-attachment",
        "version": "v1",
        "title": "Demo Schedule B",
        "publishes": "demo.schedule-b",
        "itemizations": [{
            "part_id": "part-i",
            "label": "Demo Interest",
            "authority": {"kind": "single_family", "source_family": {"id": "demo.family.interest", "version": "v1"}},
            "row_sets": [{
                "rows": {
                    "op": "collect_members",
                    "member_fact_type": {"id": "demo.interest.amount", "version": "v1"},
                    "source_family": {"id": "demo.family.interest", "version": "v1"},
                },
                "subtotal_symbol": "demo.interest.positive",
            }],
            "adjustment_rows": declared_adjustments,
            "tie_out": {
                "line_symbol": "demo.interest.taxable",
                "operation": "subtract",
                "positive_subtotals": ["demo.interest.positive"],
                "adjustment_subtotals": [
                    adjustment.get("subtotal_symbol", "demo.derived.nominee")
                    for adjustment in declared_adjustments
                    for _ in (adjustment.get("selection", {}).get("paths", []) or [None])
                ],
            },
        }],
    }
    derived_finding = {
        "schema": "derived-finding.v2",
        "id": "finding:derived:nominee",
        "fact_id": "demo.derived.nominee|report=demo",
        "symbol": (
            "demo.interest.nominee-reduction|report=demo"
            if derived_active else "demo.unrelated|report=demo"
        ),
        "value": "10",
        "version": "v2",
        "pins": [{"role": "input", "id": "demo.raw.nominee", "version": "v1"}],
    }
    attachment_finding = {
        "schema": "derived-finding.v2",
        "id": "demo.attachment.finding",
        "symbol": "demo.schedule-b",
        "value": {"itemizations": [{
            "part_id": "part-i",
            "row_sets": [{"rows": []}],
            "adjustment_rows": serialized_adjustments,
            "part_sum": part_sum,
        }]},
        "version": "v2",
        "pins": [],
    }
    tie_finding = {
        "schema": "derived-finding.v2",
        "id": "demo.tie.finding",
        "symbol": "demo.interest.taxable",
        "value": part_sum,
        "version": "v2",
        "pins": [],
    }
    publications: dict[str, dict[str, Any]] = {
        "demo.attachment.finding": attachment_finding,
        "demo.tie.finding": tie_finding,
        "finding:derived:nominee": derived_finding,
    }
    state = FindingState(findings={
        "demo.raw.nominee": {
            "schema": "finding.v1",
            "id": "demo.raw.nominee",
            "fact_id": "demo.legacy.nominee|report=demo" if legacy_active else "demo.raw.nominee",
            "value": "0",
            "basis": "attested",
            "evidence_ids": [],
        },
        "finding:derived:nominee": {**derived_finding, "pins": {}},
    }, evidence={})
    return rule, publications, state


def _serialized_row(*, source: str, subtotal: str, derived: bool = False) -> dict[str, Any]:
    row: dict[str, Any] = {
        "kind": "nominee_distribution",
        "label": "Nominee Distribution",
        "sign": "negative",
        "rows": [],
        "row_sum": "0",
        "signed_sum": "0",
        "subtotal": {"symbol": subtotal, "value": "0"},
    }
    if derived:
        row["fact_type"] = {"id": "demo.interest.nominee-reduction", "version": "v1"}
        row["rows"] = [{"finding_id": "finding:derived:nominee", "value": "10"}]
        row["row_sum"] = "10"
        row["signed_sum"] = "-10"
    else:
        row["source_family"] = {"id": source, "version": "v1"}
    return row


class AttachmentRuleV11Schema(unittest.TestCase):
    def test_positive_payload_instantiates_and_registry_bytes_are_immutable(self) -> None:
        schema = json.loads(V11_SCHEMA.read_text())
        instance = json.loads(V11_EXAMPLE.read_text())
        jsonschema.Draft202012Validator(schema).validate({k: v for k, v in instance.items() if not k.startswith("_")})
        self.assertEqual(instance["schema"], "attachment-rule.v11")
        self.assertEqual(instance["itemizations"][0]["adjustment_rows"][0]["selection"]["paths"][1]["rows"]["fact_type"]["id"], "tax.us.2025.interest.nominee-reduction")

    def test_runner_selection_paths_are_runtime_distinct(self) -> None:
        rule = _rule()
        no_activity_run = _fake_run()
        result = no_activity_run.attempt_attachment(rule)
        self.assertEqual(result, "published")
        no_activity_value = next(
            p for p in no_activity_run.publications if p.finding["symbol"] == "demo.schedule-b"
        ).finding["value"]
        self.assertEqual(no_activity_value["itemizations"][0]["adjustment_rows"], [])

        legacy_run = _fake_run(legacy=True)
        self.assertEqual(legacy_run.attempt_attachment(rule), "published")
        legacy_value = next(p for p in legacy_run.publications if p.finding["symbol"] == "demo.schedule-b").finding["value"]
        self.assertEqual(legacy_value["itemizations"][0]["adjustment_rows"][0]["source_family"]["id"], "demo.family.legacy-nominee")

        derived_run = _fake_run(derived=True)
        self.assertEqual(derived_run.attempt_attachment(rule), "published")
        derived_value = next(p for p in derived_run.publications if p.finding["symbol"] == "demo.schedule-b").finding["value"]
        self.assertEqual(derived_value["itemizations"][0]["adjustment_rows"][0]["fact_type"]["id"], "demo.interest.nominee-reduction")

        both_run = _fake_run(legacy=True, derived=True)
        self.assertEqual(both_run.attempt_attachment(rule), "blocked")
        self.assertEqual(both_run.dispositions[-1]["code"], "EXCLUSIVE_PRESENCE_CONFLICT")

    def test_unrelated_threshold_trigger_does_not_require_nominee_subtotal(self) -> None:
        run = _fake_run(threshold="1500", positive="2000")
        self.assertEqual(run.attempt_attachment(_rule()), "published")
        self.assertEqual(run.dispositions[-1]["disposition"], "published")

    def test_nominee_activity_requires_attachment_below_threshold(self) -> None:
        run = _fake_run(derived=True, threshold="1500", positive="100")
        self.assertEqual(run.attempt_attachment(_rule()), "published")

    def test_pairing_scoped_accrued_activity_is_not_nominee_trigger(self) -> None:
        run = _fake_run(accrued=True, threshold="1500", positive="100")
        self.assertEqual(run.attempt_attachment(_rule()), "inapplicable")


class AdmissionAndPresentation(unittest.TestCase):
    def _direct_declared(self, schema: str) -> dict[str, Any]:
        rows: dict[str, Any] = {
            "op": "collect_members",
            "member_fact_type": {"id": "demo.interest.nominee", "version": "v1"},
            "source_family": {"id": "demo.family.nominee", "version": "v1"},
        }
        return {
            "kind": "nominee_distribution",
            "label": "Nominee Distribution",
            "sign": "negative",
            "rows": rows,
            "subtotal_symbol": "demo.nominee.subtotal",
        }

    def _project(
        self,
        schema: str,
        declared: list[dict[str, Any]],
        serialized: list[dict[str, Any]],
        *,
        part_sum: str = "0",
        legacy_active: bool = False,
        derived_active: bool = False,
        extra_dispositions: list[dict[str, Any]] | None = None,
    ) -> None:
        rule, publications, state = _presentation_attachment(
            schema,
            declared,
            serialized,
            part_sum=part_sum,
            legacy_active=legacy_active,
            derived_active=derived_active,
        )
        _resolve_attachment(
            rule,
            dispositions_by_symbol={
                "demo.schedule-b": [{"disposition": "published", "finding_id": "demo.attachment.finding"}],
                "demo.interest.taxable": [{"disposition": "published", "finding_id": "demo.tie.finding"}],
            },
            publications_by_id=publications,
            state=state,
            pin_labels={},
            dispositions=[
                *(extra_dispositions or []),
            ],
        )

    def test_inherited_v6_v8_and_v10_rows_must_match_declared_adjustments(self) -> None:
        declared = [self._direct_declared("attachment-rule.v6")]
        matching = _serialized_row(source="demo.family.nominee", subtotal="demo.nominee.subtotal")
        for schema in ("attachment-rule.v6", "attachment-rule.v8"):
            with self.subTest(schema=schema, mutation="matching"):
                self._project(schema, declared, [matching])
            with self.subTest(schema=schema, mutation="missing"):
                with self.assertRaises(PresentationModelError):
                    self._project(schema, declared, [])
            with self.subTest(schema=schema, mutation="extra"):
                with self.assertRaises(PresentationModelError):
                    self._project(schema, [], [matching])

        v10_declared = [self._direct_declared("attachment-rule.v10")]
        with self.subTest(schema="attachment-rule.v10", mutation="matching"):
            self._project("attachment-rule.v10", v10_declared, [matching])
        with self.subTest(schema="attachment-rule.v10", mutation="missing"):
            with self.assertRaises(PresentationModelError):
                self._project("attachment-rule.v10", v10_declared, [])

        ambiguous = self._direct_declared("attachment-rule.v8")
        ambiguous["rows"] = {**ambiguous["rows"], "member_fact_type": {"id": "demo.other.member", "version": "v1"}}
        with self.assertRaises(PresentationModelError):
            self._project("attachment-rule.v8", [declared[0], ambiguous], [matching])

    def test_v11_presentation_rows_follow_one_exclusive_selection_path(self) -> None:
        declared = [{
            "kind": "nominee_distribution",
            "label": "Nominee Distribution",
            "sign": "negative",
            "selection": {
                "mode": "exclusive_presence",
                "conflict": "refuse",
                "paths": [
                    {
                        "id": "legacy",
                        "rows": {
                            "op": "collect_members",
                            "member_fact_type": {"id": "demo.legacy.nominee", "version": "v1"},
                            "source_family": {"id": "demo.family.legacy-nominee", "version": "v1"},
                        },
                        "subtotal_symbol": "demo.legacy.subtotal",
                    },
                    {
                        "id": "derived",
                        "rows": {"op": "enumerate_published", "fact_type": {"id": "demo.interest.nominee-reduction", "version": "v1"}},
                        "subtotal_symbol": "demo.derived.subtotal",
                    },
                ],
            },
        }]
        legacy = _serialized_row(source="demo.family.legacy-nominee", subtotal="demo.legacy.subtotal")
        derived = _serialized_row(source="", subtotal="demo.derived.subtotal", derived=True)
        derived_zero = _serialized_row(source="", subtotal="demo.derived.subtotal", derived=True)
        derived_zero["rows"] = [{"finding_id": "finding:derived:nominee", "value": "0"}]
        derived_zero["row_sum"] = "0"
        derived_zero["signed_sum"] = "0"
        legacy["rows"] = [{"finding_id": "demo.raw.nominee", "value": "0"}]
        self._project("attachment-rule.v11", declared, [legacy], legacy_active=True)
        self._project("attachment-rule.v11", declared, [derived], derived_active=True)
        self._project("attachment-rule.v11", declared, [derived_zero], derived_active=True)
        self._project("attachment-rule.v11", declared, [])
        with self.assertRaises(PresentationModelError):
            self._project("attachment-rule.v11", declared, [], part_sum="10", legacy_active=True)
        with self.assertRaises(PresentationModelError):
            self._project("attachment-rule.v11", declared, [legacy, derived])
        with self.assertRaises(PresentationModelError):
            self._project("attachment-rule.v11", declared, [legacy, legacy], legacy_active=True)
        omitted_zero_derived = dict(derived_zero, rows=[])
        with self.assertRaises(PresentationModelError):
            self._project("attachment-rule.v11", declared, [omitted_zero_derived], derived_active=True)
        duplicate_zero_derived = dict(derived_zero, rows=[*derived_zero["rows"], {"finding_id": "finding:derived:nominee", "value": "0"}])
        with self.assertRaises(PresentationModelError):
            self._project("attachment-rule.v11", declared, [duplicate_zero_derived], derived_active=True)
        extra_zero_derived = dict(derived_zero, rows=[*derived_zero["rows"], {"finding_id": "finding:derived:extra", "value": "0"}])
        with self.assertRaises(PresentationModelError):
            self._project("attachment-rule.v11", declared, [extra_zero_derived], derived_active=True)
        omitted_zero_legacy = dict(legacy, rows=[])
        with self.assertRaises(PresentationModelError):
            self._project("attachment-rule.v11", declared, [omitted_zero_legacy], legacy_active=True)
        duplicate_zero_legacy = dict(legacy, rows=[*legacy["rows"], {"finding_id": "demo.raw.nominee", "value": "0"}])
        with self.assertRaises(PresentationModelError):
            self._project("attachment-rule.v11", declared, [duplicate_zero_legacy], legacy_active=True)
        extra_zero_legacy = dict(legacy, rows=[*legacy["rows"], {"finding_id": "demo.raw.extra", "value": "0"}])
        with self.assertRaises(PresentationModelError):
            self._project("attachment-rule.v11", declared, [extra_zero_legacy], legacy_active=True)
        blocked_derived = {
            "disposition": "blocked",
            "symbol": "demo.interest.nominee-reduction|report=blocked",
        }
        with self.assertRaises(PresentationModelError):
            self._project("attachment-rule.v11", declared, [], extra_dispositions=[blocked_derived])
        extra = _serialized_row(source="demo.family.unlisted", subtotal="demo.unlisted.subtotal")
        with self.assertRaises(PresentationModelError):
            self._project("attachment-rule.v11", declared, [extra])

    def test_direct_v11_rows_require_exact_current_contributors(self) -> None:
        legacy_declared = self._direct_declared("attachment-rule.v11")
        legacy_declared["rows"] = {
            "op": "collect_members",
            "member_fact_type": {"id": "demo.legacy.nominee", "version": "v1"},
            "source_family": {"id": "demo.family.legacy-nominee", "version": "v1"},
        }
        legacy_declared["subtotal_symbol"] = "demo.legacy.subtotal"
        legacy = _serialized_row(source="demo.family.legacy-nominee", subtotal="demo.legacy.subtotal")
        legacy["rows"] = [{"finding_id": "demo.raw.nominee", "value": "0"}]
        self._project("attachment-rule.v11", [legacy_declared], [legacy], legacy_active=True)
        for mutation, rows in (
            ("omitted", []),
            ("duplicate", [*legacy["rows"], {"finding_id": "demo.raw.nominee", "value": "0"}]),
            ("extra", [*legacy["rows"], {"finding_id": "demo.raw.extra", "value": "0"}]),
        ):
            with self.subTest(kind="collect_members", mutation=mutation):
                with self.assertRaises(PresentationModelError):
                    self._project(
                        "attachment-rule.v11",
                        [legacy_declared],
                        [dict(legacy, rows=rows)],
                        legacy_active=True,
                    )

        derived_declared = self._direct_declared("attachment-rule.v11")
        derived_declared["rows"] = {
            "op": "enumerate_published",
            "fact_type": {"id": "demo.interest.nominee-reduction", "version": "v1"},
        }
        derived_declared["subtotal_symbol"] = "demo.derived.subtotal"
        derived = _serialized_row(source="", subtotal="demo.derived.subtotal", derived=True)
        derived["rows"] = [{"finding_id": "finding:derived:nominee", "value": "0"}]
        self._project("attachment-rule.v11", [derived_declared], [derived], derived_active=True)
        for mutation, rows in (
            ("omitted", []),
            ("duplicate", [*derived["rows"], {"finding_id": "finding:derived:nominee", "value": "0"}]),
            ("extra", [*derived["rows"], {"finding_id": "finding:derived:extra", "value": "0"}]),
        ):
            with self.subTest(kind="enumerate_published", mutation=mutation):
                with self.assertRaises(PresentationModelError):
                    self._project(
                        "attachment-rule.v11",
                        [derived_declared],
                        [dict(derived, rows=rows)],
                        derived_active=True,
                    )

        selected = {
            "kind": "nominee_distribution",
            "label": "Nominee Distribution",
            "sign": "negative",
            "selection": {
                "mode": "exclusive_presence",
                "conflict": "refuse",
                "paths": [{
                    "id": "derived",
                    "rows": {
                        "op": "enumerate_published",
                        "fact_type": {"id": "demo.interest.nominee-reduction", "version": "v1"},
                    },
                    "subtotal_symbol": "demo.derived.subtotal",
                }],
            },
        }
        with self.assertRaises(PresentationModelError):
            self._project(
                "attachment-rule.v11",
                [derived_declared, selected],
                [derived],
                derived_active=True,
            )

    def _v29_corpus(self) -> tuple[dict[str, Any], dict[tuple[str, str], dict[str, Any]]]:
        """Build the synthetic citizens pinned by the committed v29 instance."""
        content = ROOT / "packages/content/tax/2025"

        def load(name: str) -> dict[str, Any]:
            return cast(dict[str, Any], json.loads((content / name).read_text()))

        rule = _rule()
        rule.update({"id": "demo.rule.attachment.schedule-b", "version": "v1"})
        rule["scope"] = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}
        part = rule["itemizations"][0]
        part["tie_out"]["line_symbol"] = "demo.interest.positive"
        part["adjustment_rows"][0]["selection"]["paths"][0]["rows"]["source_family"]["id"] = "demo.family.nominee"

        families: list[dict[str, Any]] = []
        for family_id, fact_type, subtotal in (
            ("demo.family.interest", "demo.interest.amount", "demo.interest.positive"),
            ("demo.family.nominee", "demo.legacy.nominee.amount", "demo.legacy.nominee"),
        ):
            family = load("family.f1099int-b1.json")
            family["id"] = family_id
            family["member_predicate"]["fact_type"] = fact_type
            family["authorizes_subtotal"] = subtotal
            families.append(family)

        bundle = load("nominee-reduction.bundle.json")
        bundle["id"] = "demo.bundle.v11"
        bundle["label"] = "Demo v11 fact vocabulary"
        nominee_fact = copy.deepcopy(bundle["fact_types"][0])
        nominee_fact["id"] = "demo.interest.nominee-reduction"
        bundle["fact_types"] = [nominee_fact]
        answer_fact = copy.deepcopy(nominee_fact)
        answer_fact["id"] = "demo.answer"
        answer_fact["title"] = "Demo categorical answer"
        answer_fact["value_schema"] = {"enum": ["yes", "no"]}
        bundle["fact_types"].append(answer_fact)

        parameter = load("parameter.schedule-b-threshold.json")
        parameter["id"] = "demo.parameter.threshold"
        citation_schedule = load("citation.schedule-b.json")
        citation_schedule["id"] = "demo.citation.schedule-b"
        citation_nominee = load("citation.interest.nominee-reduction.json")
        citation_nominee["id"] = "demo.citation.nominee"
        citizens = [*families, bundle, parameter, citation_schedule, citation_nominee, rule]
        return json.loads(V29_PACKAGE.read_text()), {
            (citizen["id"], citizen["version"]): citizen for citizen in citizens
        }

    def test_v29_package_is_schema_validated_and_admits_v11(self) -> None:
        package, corpus = self._v29_corpus()
        schemas = DerivationSchemas()
        schemas.validate_declared(package)
        self.assertEqual(package_instance_checksum(package), package["package_checksum"])
        from packages.derivation.package_validation import validate_package

        result = validate_package(package, corpus, schemas)
        self.assertTrue(result.ok, msg=str(result.issues))

    def test_production_v11_projection_preserves_i3_and_i6_groups(self) -> None:
        rule = _rule()
        rule["itemizations"][0]["adjustment_rows"].append({
            "kind": "accrued_interest",
            "label": "Accrued Interest",
            "sign": "negative",
            "subtotal_symbol": "demo.accrued_interest.subtotal",
            "rows": {
                "op": "enumerate_published",
                "fact_type": {"id": "demo.interest.current-year-adjustment.pairing-scoped", "version": "v1"},
            },
        })
        attachment_id = "demo.attachment.schedule-b"
        raw_ids = ["demo.raw.report-a", "demo.raw.report-b"]
        derived = [
            ("finding:derived:nominee.a", "Nominee Distribution", "nominee_distribution", "demo.citation.nominee"),
            ("finding:derived:nominee.b", "Nominee Distribution", "nominee_distribution", "demo.citation.nominee"),
            ("finding:derived:accrued", "Accrued Interest", "accrued_interest", "demo.citation.accrued"),
        ]
        findings: dict[str, dict[str, Any]] = {
            raw_id: {
                "schema": "finding.v1", "id": raw_id, "fact_id": f"demo.fact.{raw_id[-1]}",
                "value": "100", "basis": "attested", "evidence_ids": [],
            }
            for raw_id in raw_ids
        }
        publications: list[Publication] = []
        finding_rows: list[dict[str, Any]] = []
        for index, (finding_id, label, kind, citation_id) in enumerate(derived):
            source_id = raw_ids[min(index, len(raw_ids) - 1)]
            finding = {
                "schema": "derived-finding.v2", "id": finding_id,
                "fact_id": f"demo.fact.derived.{index}",
                "symbol": (
                    "demo.interest.nominee-reduction"
                    if kind == "nominee_distribution"
                    else "demo.interest.current-year-adjustment.pairing-scoped"
                ) + f"|report={index}",
                "value": "100", "version": "v2",
                "pins": [
                    {"role": "input", "id": source_id, "version": "v1"},
                    {"role": "computation", "id": f"demo.rule.{kind}", "version": "v1"},
                    {"role": "citation", "id": citation_id, "version": "v1"},
                ],
            }
            findings[finding_id] = finding
            publications.append(Publication(act={"run_id": "demo.run.v11", "finding": finding}, finding=finding))
            finding_rows.append({"finding_id": finding_id, "value": "100"})
        adjustment_rows = [
            {
                "kind": "nominee_distribution",
                "label": "Nominee Distribution",
                "sign": "negative",
                "fact_type": {"id": "demo.interest.nominee-reduction", "version": "v1"},
                "subtotal": {"symbol": "demo.derived.nominee", "value": "200"},
                "row_sum": "200",
                "rows": finding_rows[:2],
            },
            {
                "kind": "accrued_interest",
                "label": "Accrued Interest",
                "sign": "negative",
                "fact_type": {"id": "demo.interest.current-year-adjustment.pairing-scoped", "version": "v1"},
                "subtotal": {"symbol": "demo.accrued_interest.subtotal", "value": "100"},
                "row_sum": "100",
                "rows": finding_rows[2:],
            },
        ]
        attachment_finding = {
            "schema": "derived-finding.v2", "id": attachment_id,
            "fact_id": "demo.fact.attachment", "symbol": rule["publishes"], "value": {"itemizations": [{
                "part_id": "part-i",
                "row_sets": [{"rows": [{"finding_id": raw_ids[0], "value": "100"}]}],
                "adjustment_rows": adjustment_rows,
            }]},
            "version": "v2", "pins": [],
        }
        tie_finding = {
            "schema": "derived-finding.v2", "id": "demo.tie",
            "fact_id": "demo.fact.tie", "symbol": "demo.interest.taxable", "value": "100", "version": "v2", "pins": [],
        }
        publications.extend([
            Publication(act={"run_id": "demo.run.v11", "finding": attachment_finding}, finding=attachment_finding),
            Publication(act={"run_id": "demo.run.v11", "finding": tie_finding}, finding=tie_finding),
        ])
        findings.update({attachment_id: attachment_finding, "demo.tie": tie_finding})
        dispositions = [
            {"artifact_id": rule["id"], "symbol": rule["publishes"], "disposition": "published", "finding_id": attachment_id},
            {"artifact_id": "demo.rule.tie", "symbol": "demo.interest.taxable", "disposition": "published", "finding_id": "demo.tie"},
        ]
        model = build_presentation_model(
            run_id="demo.run.v11",
            resolved_members=[rule],
            # The production state stores currency edges in its pins mapping;
            # publication payloads carry the projection pin list separately.
            # Keep those two real representations distinct in this seam test.
            state=FindingState(
                findings={
                    finding_id: {**finding, "pins": {}}
                    if finding.get("schema") == "derived-finding.v2" else finding
                    for finding_id, finding in findings.items()
                },
                evidence={},
            ),
            publications=publications,
            dispositions=dispositions,
        )
        groups = model["provenanceGroups"]
        self.assertEqual({group["id"] for group in groups}, {finding_id for finding_id, *_ in derived})
        self.assertEqual(
            {(group["adjustmentLabel"], group["adjustmentKind"]) for group in groups},
            {("Nominee Distribution", "nominee_distribution"), ("Accrued Interest", "accrued_interest")},
        )
        self.assertEqual(
            [part["heading"] for part in model["citationGroups"][0]["parts"]],
            ["Demo Interest", "Nominee Distribution", "Accrued Interest"],
        )

    def _package_result(self, *, stale_fact: bool = False, stale_citation: bool = False) -> Any:
        from packages.derivation.loader import DerivationSchemas
        from packages.derivation.package_validation import validate_package

        package, corpus = self._v29_corpus()
        rule = corpus[("demo.rule.attachment.schedule-b", "v1")]
        if stale_fact:
            rule["requirement"]["triggers"][1]["fact_type"]["id"] = "demo.missing.fact"
        if stale_citation:
            rule["requirement"]["triggers"][1]["citation"]["id"] = "demo.missing.citation"
        return validate_package(package, corpus, DerivationSchemas())

    def test_package_admission_rejects_absent_derived_trigger_fact_type(self) -> None:
        result = self._package_result(stale_fact=True)
        self.assertIn("ATTACHMENT_TRIGGER_FACT_TYPE_ABSENT", {issue.code for issue in result.issues})

    def test_package_admission_rejects_stale_derived_trigger_citation(self) -> None:
        result = self._package_result(stale_citation=True)
        self.assertIn("ATTACHMENT_TRIGGER_CITATION_ABSENT", {issue.code for issue in result.issues})

    def test_v11_edges_include_nested_paths_and_any_trigger_dependencies(self) -> None:
        rule = _rule()
        corpus = {rule["id"]: rule}
        for citizen_id, schema in (("demo.family.legacy-nominee", "source-family.v1"), ("demo.interest.nominee-reduction", "fact-type.v2"), ("demo.parameter.threshold", "parameter-declaration.v1"), ("demo.citation.schedule-b", "citation.v1"), ("demo.citation.nominee", "citation.v1")):
            corpus[citizen_id] = {"id": citizen_id, "version": "v1", "schema": schema}
        edges = build_dependency_edges(corpus)
        self.assertEqual(edges[rule["id"]], {"demo.family.legacy-nominee", "demo.interest.nominee-reduction", "demo.parameter.threshold", "demo.citation.schedule-b", "demo.citation.nominee"})
        closure = rule_scoped_closure({rule["id"]}, corpus)
        self.assertEqual(
            {citizen_id for citizen_id, _version in closure},
            set(corpus),
        )

    def test_nested_threshold_subtotal_reaches_its_producer_in_each_consumer(self) -> None:
        rule = _rule()
        rule["requirement"]["triggers"][0]["subtotals"] = ["demo.threshold.total"]
        producer = {
            "schema": "rule-artifact.v3",
            "id": "demo.producer.threshold",
            "version": "v1",
            "role": "computation",
            "scope": rule["scope"],
            "requires": [],
            "when": True,
            "value": {"op": "add", "args": []},
            "publishes": "demo.threshold.total",
        }
        corpus = {rule["id"]: rule, producer["id"]: producer}
        edges = build_dependency_edges(corpus)
        self.assertIn(producer["id"], edges[rule["id"]])
        reached = _families_reached(rule, {"demo.threshold.total": "demo.family.threshold"})
        self.assertIn(("demo.family.threshold", "reads_subtotal"), reached)
        self.assertIn("demo.threshold.total", _rule_required_symbols(rule))

    def test_sample_is_durable_and_valid(self) -> None:
        validate_presentation_model(json.loads(PRESENTATION_SAMPLE.read_text()))

    def test_provenance_relationship_mutations_fail_closed(self) -> None:
        model = json.loads(PRESENTATION_SAMPLE.read_text())
        cases: dict[str, Callable[[dict[str, Any]], None]] = {
            "unknown attachment": lambda m: m["provenanceGroups"][0].__setitem__("attachmentId", "demo.unknown"),
            "label mismatch": lambda m: m["provenanceGroups"][0].__setitem__("adjustmentLabel", "Other"),
            "kind mismatch": lambda m: m["provenanceGroups"][0].__setitem__("adjustmentKind", "accrued_interest"),
            "unrelated group id": lambda m: m["provenanceGroups"][0].__setitem__("id", "finding:derived:unrelated"),
            "altered lineage": lambda m: m["citationGroups"][0]["parts"][0]["citationSites"][0].__setitem__("pinId", "finding:derived:tampered"),
            "empty lineage": lambda m: m["provenanceGroups"][0].__setitem__("citationSites", []),
            "duplicate group": lambda m: m["provenanceGroups"].append(copy.deepcopy(m["provenanceGroups"][0])),
            "missing group": lambda m: m["provenanceGroups"].clear(),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                mutated = copy.deepcopy(model)
                mutate(mutated)
                with self.assertRaises(PresentationModelError):
                    validate_presentation_model(mutated)


if __name__ == "__main__":
    unittest.main()
