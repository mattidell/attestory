"""Bounded v12 link-count declaration on the validated live path."""

from __future__ import annotations

import copy
import unittest
from dataclasses import replace
from typing import Any

from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import package_instance_checksum, validate_package
from packages.derivation.runner import RunContext
from packages.kernel.schema_registry import SchemaValidationError
from tests.derivation.test_subject_declaration_live_path import (
    ADOPTION_PIN,
    GOVERNANCE_PINS,
    SCOPE,
    _Graph,
    _State,
    _both_runners,
    _currency,
    _finding,
    _input_ids,
    _lattice_type,
    _package_fact_type,
    _publications,
)

STATEMENT = "demo.tax.link-count.statement"
LINKS = "demo.tax.link-count.link"
COUNT = "demo.tax.link-count.result"
AMOUNT = "demo.tax.link-count.amount"
CLAIMS = "demo.tax.link-count.scope-claim"
CLASSIFIER = "demo.tax.link-count.classifier"
DISQUALIFIER_COUNT = "demo.tax.link-count.disqualifier-count"
CONCLUSION = "demo.tax.link-count.conclusion"
RESPONSIBILITY = "demo.tax.link-count.responsibility"
EMPTY_PARAMETER = "demo.param.no-scope-claim"


def _rule(*, value: Any | None = None) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v12",
        "id": "demo.rule.statement-link-count",
        "version": "v1",
        "scope": dict(SCOPE),
        "subject": {"id": STATEMENT, "version": "v1"},
        "joined": {"id": LINKS, "version": "v1"},
        "direction": "joined_contains_subject",
        "role": "computation",
        "reader_role": "link-count",
        "wording": "No borrowing is currently linked to {statement}.",
        "requires": [],
        "pins": [],
        "when": True,
        "value": value or {"op": "link_count", "links": LINKS},
        "publishes": COUNT,
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
    }


def _fixture(*, rule: dict[str, Any] | None = None) -> tuple[list[tuple[dict[str, Any], str]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    statement_1 = f"{STATEMENT}|lender=demo-lender,statement=demo-s1,tax-year=2025"
    statement_2 = f"{STATEMENT}|lender=demo-lender,statement=demo-s2,tax-year=2025"
    link_2 = f"{LINKS}|lender=demo-lender,statement=demo-s2,tax-year=2025,borrowing=demo-loan-2"
    findings = {
        "demo.finding.statement-s1": _finding("demo.finding.statement-s1", statement_1, "100"),
        "demo.finding.statement-s2": _finding("demo.finding.statement-s2", statement_2, "200"),
        "demo.finding.link-s2": _finding("demo.finding.link-s2", link_2, "linked"),
    }
    lattice = {
        STATEMENT: _lattice_type(STATEMENT, (
            ("lender", ("demo-lender",)),
            ("statement", ("demo-s1", "demo-s2")),
            ("tax-year", ("2025",)),
        )),
        LINKS: _lattice_type(LINKS, (
            ("lender", ("demo-lender",)),
            ("statement", ("demo-s2",)),
            ("tax-year", ("2025",)),
            ("borrowing", ("demo-loan-2",)),
        )),
    }
    rule_value = rule if rule is not None else _rule()
    return [
        (rule_value, "computation"),
        (_package_fact_type(STATEMENT, ["lender", "statement", "tax-year"]), "fact-type"),
        (_package_fact_type(LINKS, ["lender", "statement", "tax-year", "borrowing"]), "fact-type"),
    ], findings, lattice


def _live(parts: list[tuple[dict[str, Any], str]], findings: dict[str, dict[str, Any]], lattice: dict[str, dict[str, Any]]) -> RunContext:
    package = {
        "schema": "artifact-package.v34",
        "id": "demo.package.link-count",
        "version": "v1",
        "scope": dict(SCOPE),
        "admitted_schemas": sorted({citizen["schema"] for citizen, _ in parts}),
        "members": [
            {"role": role, "schema": citizen["schema"], "id": citizen["id"], "version": citizen["version"]}
            for citizen, role in parts
        ],
        "input_bindings": [],
        "entrypoints": [
            {"id": citizen["id"], "version": citizen["version"]}
            for citizen, _role in parts
        ],
        "composition_obligations": [],
    }
    package["package_checksum"] = package_instance_checksum(package)
    corpus = {(citizen["id"], citizen["version"]): citizen for citizen, _role in parts}
    validation = validate_package(package, corpus, DerivationSchemas())
    if not validation.ok:
        raise AssertionError(validation.issues)
    from packages.derivation.live import _resolved_run_material
    from packages.derivation.marshal import marshal_run_context

    material = _resolved_run_material(_Graph(list(validation.resolved_members), package))
    rules, parameters, families, mappings, fact_types, bindings, collect_names = material
    return marshal_run_context(
        run_id="demo.run.link-count",
        state=_State(findings, lattice),  # type: ignore[arg-type]
        currency=_currency(list(findings)),
        rules=rules,
        parameters=parameters,
        canon={},
        adoption_pin=ADOPTION_PIN,
        governance_pins=GOVERNANCE_PINS,
        family_declarations=families,
        closure_mappings=mappings,
        fact_types=fact_types,
        input_bindings=bindings,
        collect_source_names=collect_names,
        emission_only_source_names=list(material.emission_only_names),
    )


class ExperimentalLinkCount(unittest.TestCase):
    def test_validated_count_is_statement_local_in_both_runners(self) -> None:
        parts, findings, lattice = _fixture()
        ctx = _live(parts, findings, lattice)
        forward, reference = _both_runners(ctx)
        for result in (forward, reference):
            published = _publications(result)
            s1 = f"{COUNT}|{STATEMENT}|lender=demo-lender,statement=demo-s1,tax-year=2025"
            s2 = f"{COUNT}|{STATEMENT}|lender=demo-lender,statement=demo-s2,tax-year=2025"
            self.assertEqual(published[s1]["value"], "0")
            self.assertEqual(published[s2]["value"], "1")
            self.assertEqual(_input_ids(published[s1]["pins"]), {"demo.finding.statement-s1"})
            self.assertEqual(_input_ids(published[s2]["pins"]), {"demo.finding.statement-s2", "demo.finding.link-s2"})
            self.assertNotIn("wording", [pin.get("role") for pin in published[s2]["pins"]])

    def test_zero_marker_and_cancelling_markers_do_not_affect_count(self) -> None:
        parts, findings, lattice = _fixture()
        for index, value in enumerate((0, 1, -1)):
            marker = {
                "schema": "rule-artifact.v6",
                "id": f"demo.rule.marker-{index}",
                "version": "v1",
                "scope": dict(SCOPE),
                "role": "computation",
                "requires": [],
                "pins": [],
                "when": True,
                "value": value,
                "publishes": f"demo.tax.marker-{index}",
                "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
            }
            parts.append((marker, "computation"))
        bare_guard = copy.deepcopy(_rule())
        bare_guard.update(
            id="demo.rule.bare-guard-probe", requires=[COUNT],
            when={"op": "compare", "cmp": "eq", "left": {"op": "ref", "name": COUNT}, "right": 0},
            value=True, publishes="demo.tax.bare-guard-probe",
        )
        bare_guard.pop("reader_role")
        bare_guard.pop("joined")
        bare_guard.pop("direction")
        bare_guard.pop("wording")
        parts.append((bare_guard, "computation"))
        symbol = f"{COUNT}|{STATEMENT}|lender=demo-lender,statement=demo-s2,tax-year=2025"
        bare_s1 = f"demo.tax.bare-guard-probe|{STATEMENT}|lender=demo-lender,statement=demo-s1,tax-year=2025"
        bare_s2 = f"demo.tax.bare-guard-probe|{STATEMENT}|lender=demo-lender,statement=demo-s2,tax-year=2025"
        for ordered_parts in (parts, list(reversed(parts))):
            ctx = _live(ordered_parts, findings, lattice)
            forward, reference = _both_runners(ctx)
            for result in (forward, reference):
                self.assertEqual(_publications(result)[symbol]["value"], "1")
                self.assertIn(bare_s1, _publications(result))
                self.assertNotIn(bare_s2, _publications(result))

    def test_missing_subject_identity_blocks_only_that_statement(self) -> None:
        parts, findings, lattice = _fixture()
        ctx = _live(parts, findings, lattice)
        ctx.sources[:] = [
            replace(source, keys=None)
            if source.name == STATEMENT and source.finding_id == "demo.finding.statement-s1"
            else source
            for source in ctx.sources
        ]
        forward, reference = _both_runners(ctx)
        s1 = f"{COUNT}|{STATEMENT}|lender=demo-lender,statement=demo-s1,tax-year=2025"
        s2 = f"{COUNT}|{STATEMENT}|lender=demo-lender,statement=demo-s2,tax-year=2025"
        for result in (forward, reference):
            blocked = [row for row in result.dispositions if row.get("symbol") == s1]
            self.assertEqual(len(blocked), 1)
            self.assertEqual(blocked[0]["code"], "DEPENDENCY_INVALID")
            self.assertEqual(blocked[0]["missing"], ["link-coverage-keys-unavailable"])
            self.assertNotIn(s1, _publications(result))
            self.assertEqual(_publications(result)[s2]["value"], "1")

    def test_present_link_row_without_identity_keys_blocks(self) -> None:
        parts, findings, lattice = _fixture()
        ctx = _live(parts, findings, lattice)
        ctx.sources[:] = [
            replace(source, keys=None)
            if source.name == LINKS and source.finding_id == "demo.finding.link-s2"
            else source
            for source in ctx.sources
        ]
        forward, reference = _both_runners(ctx)
        symbols = [
            f"{COUNT}|{STATEMENT}|lender=demo-lender,statement={statement},tax-year=2025"
            for statement in ("demo-s1", "demo-s2")
        ]
        for result in (forward, reference):
            for symbol in symbols:
                blocked = [row for row in result.dispositions if row.get("symbol") == symbol]
                self.assertEqual(len(blocked), 1)
                self.assertEqual(blocked[0]["missing"], ["demo.finding.link-s2"])
                self.assertNotIn(symbol, _publications(result))

    def test_v12_rejects_missing_relationship_and_malformed_count(self) -> None:
        parts, _findings, _lattice = _fixture()
        parts[0][0].pop("joined")
        parts[0][0].pop("direction")
        package = {
        "schema": "artifact-package.v34",
            "id": "demo.package.bad-count",
            "version": "v1",
            "scope": dict(SCOPE),
            "admitted_schemas": sorted({c["schema"] for c, _ in parts}),
            "members": [{"role": role, "schema": c["schema"], "id": c["id"], "version": c["version"]} for c, role in parts],
            "input_bindings": [],
            "entrypoints": [{"id": parts[0][0]["id"], "version": "v1"}, {"id": STATEMENT, "version": "v1"}, {"id": LINKS, "version": "v1"}],
            "composition_obligations": [],
        }
        package["package_checksum"] = package_instance_checksum(package)
        corpus = {(c["id"], c["version"]): c for c, _ in parts}
        result = validate_package(package, corpus, DerivationSchemas())
        self.assertFalse(result.ok)
        self.assertIn("LINK_COUNT_RELATIONSHIP_INVALID", [issue.code for issue in result.issues])
        bad = copy.deepcopy(_rule(value={"op": "link_count", "links": LINKS, "empty": {"parameter": {"id": "demo.param.no-link", "version": "v1"}}}))
        with self.assertRaises(SchemaValidationError):
            DerivationSchemas().validate_declared(bad)

    def test_only_six_reader_roles_are_admitted(self) -> None:
        invalid = copy.deepcopy(_rule())
        invalid["reader_role"] = "period-conclusion"
        with self.assertRaises(SchemaValidationError):
            DerivationSchemas().validate_declared(invalid)

    def test_six_role_package_admits_and_enforces_dependencies(self) -> None:
        parts, _, _ = _fixture()
        count = parts[0][0]
        amount = copy.deepcopy(count)
        amount.update(id="demo.rule.amount", reader_role="statement-amount", publishes=AMOUNT, value={"op": "ref", "name": STATEMENT})
        amount.pop("joined")
        amount.pop("direction")
        amount.pop("wording")
        classifier = copy.deepcopy(count)
        classifier.update(
            id="demo.rule.scope-classifier", subject={"id": CLAIMS, "version": "v1"},
            reader_role="statement-scope-classifier", publishes=CLASSIFIER,
            value={"op": "choose", "when": True, "then": 1, "else": {"op": "block", "code": "DEPENDENCY_INVALID"}},
        )
        classifier.pop("joined")
        classifier.pop("direction")
        classifier.pop("wording")
        disqualifier_count = copy.deepcopy(count)
        disqualifier_count.update(
            id="demo.rule.scope-disqualifier-count", joined={"id": CLAIMS, "version": "v1"},
            reader_role="statement-scope-disqualifier-count", publishes=DISQUALIFIER_COUNT,
            value={"op": "link_coverage", "links": CLAIMS, "reductions": CLASSIFIER,
                   "empty": {"parameter": {"id": EMPTY_PARAMETER, "version": "v1"}}},
        )
        disqualifier_count.pop("wording")
        conclusion = copy.deepcopy(count)
        conclusion.update(
            id="demo.rule.bare-conclusion", reader_role="bare-statement-conclusion",
            joined=None, direction=None, requires=[COUNT, DISQUALIFIER_COUNT], publishes=CONCLUSION,
            when={"op": "all", "args": [
                {"op": "compare", "cmp": "eq", "left": {"op": "ref", "name": COUNT}, "right": 0},
                {"op": "compare", "cmp": "eq", "left": {"op": "ref", "name": DISQUALIFIER_COUNT}, "right": 0},
            ]}, value=0,
        )
        conclusion.pop("joined")
        conclusion.pop("direction")
        conclusion.pop("wording")
        responsibilities = []
        for index, wording in enumerate(("borrower", "co-borrower", "guarantor"), 1):
            responsibility = copy.deepcopy(conclusion)
            responsibility.update(
                id=f"demo.rule.responsibility-{index}", reader_role="responsibility",
                requires=[CONCLUSION, AMOUNT], publishes=f"{RESPONSIBILITY}.{index}",
                when=True, value={"op": "ref", "name": AMOUNT}, wording=wording,
            )
            responsibilities.append(responsibility)
        parts.extend([
            (amount, "computation"), (classifier, "computation"),
            (disqualifier_count, "computation"), (conclusion, "computation"),
            *((responsibility, "computation") for responsibility in responsibilities),
            (_package_fact_type(CLAIMS, ["lender", "statement", "tax-year", "claim"]), "fact-type"),
            ({"schema": "parameter-declaration.v1", "id": EMPTY_PARAMETER, "version": "v1", "scope": dict(SCOPE), "values": "0"}, "parameter"),
        ])
        pkg: dict[str, Any] = {
            "schema": "artifact-package.v34", "id": "demo.package.six-roles", "version": "v1",
            "scope": dict(SCOPE), "admitted_schemas": sorted({c["schema"] for c, _ in parts}),
            "members": [{"role": role, "schema": c["schema"], "id": c["id"], "version": c["version"]} for c, role in parts],
            "input_bindings": [], "entrypoints": [{"id": c["id"], "version": c["version"]} for c, _ in parts],
            "composition_obligations": [],
        }
        pkg["package_checksum"] = package_instance_checksum(pkg)
        corpus = {(c["id"], c["version"]): c for c, _ in parts}
        result = validate_package(pkg, corpus, DerivationSchemas())
        self.assertTrue(result.ok, result.issues)

        def rejected_mutation(mutator: Any, code: str) -> None:
            changed = copy.deepcopy(parts)
            mutator(changed)
            changed_corpus = {(c["id"], c["version"]): c for c, _ in changed}
            changed_pkg = copy.deepcopy(pkg)
            changed_pkg["package_checksum"] = package_instance_checksum({k: v for k, v in changed_pkg.items() if k != "package_checksum"})
            changed_result = validate_package(changed_pkg, changed_corpus, DerivationSchemas())
            self.assertIn(code, [issue.code for issue in changed_result.issues])

        rejected_mutation(
            lambda changed: changed[0][0].update(value={"op": "add", "args": [
                {"op": "link_count", "links": LINKS}, 0,
            ]}), "READER_ROLE_INVALID",
        )
        rejected_mutation(
            lambda changed: changed[5][0].update(value={"op": "add", "args": [
                {"op": "link_coverage", "links": CLAIMS, "reductions": CLASSIFIER,
                 "empty": {"parameter": {"id": EMPTY_PARAMETER, "version": "v1"}}}, 0,
            ]}), "READER_ROLE_INVALID",
        )
        rejected_mutation(
            lambda changed: (
                changed[5][0].update(joined={"id": LINKS, "version": "v1"}),
                changed[5][0].update(value={"op": "link_coverage", "links": LINKS, "reductions": CLASSIFIER,
                                        "empty": {"parameter": {"id": EMPTY_PARAMETER, "version": "v1"}}}),
            ), "READER_ROLE_SUBJECT_MISMATCH",
        )
        rejected_mutation(
            lambda changed: changed[6][0].update(subject={"id": CLAIMS, "version": "v1"}),
            "READER_ROLE_SUBJECT_MISMATCH",
        )
        rejected_mutation(
            lambda changed: changed[7][0].update(subject={"id": CLAIMS, "version": "v1"}),
            "READER_ROLE_SUBJECT_MISMATCH",
        )
        rejected_mutation(
            lambda changed: changed[6][0].update(when={"op": "any", "args": [
                {"op": "compare", "cmp": "eq", "left": {"op": "ref", "name": COUNT}, "right": 0}, True,
            ]}), "READER_ROLE_GUARD_INVALID",
        )

        v33_package = copy.deepcopy(pkg)
        v33_package["schema"] = "artifact-package.v33"
        v33_package["package_checksum"] = package_instance_checksum({k: v for k, v in v33_package.items() if k != "package_checksum"})
        v33_result = validate_package(v33_package, corpus, DerivationSchemas())
        self.assertIn("PACKAGE_SCHEMA_INVALID", [issue.code for issue in v33_result.issues])

        classifier["value"] = 2
        pkg["package_checksum"] = package_instance_checksum({k: v for k, v in pkg.items() if k != "package_checksum"})
        bad_classifier = validate_package(pkg, corpus, DerivationSchemas())
        self.assertIn("READER_ROLE_INVALID", [issue.code for issue in bad_classifier.issues])
        classifier["value"] = {"op": "choose", "when": True, "then": 1, "else": {"op": "block", "code": "DEPENDENCY_INVALID"}}
        conclusion["requires"] = [COUNT]
        pkg["package_checksum"] = package_instance_checksum({k: v for k, v in pkg.items() if k != "package_checksum"})
        missing_dependency = validate_package(pkg, corpus, DerivationSchemas())
        self.assertIn("READER_ROLE_DEPENDENCY_MISSING", [issue.code for issue in missing_dependency.issues])
        conclusion["requires"] = [COUNT, DISQUALIFIER_COUNT]
        pkg["package_checksum"] = package_instance_checksum({k: v for k, v in pkg.items() if k != "package_checksum"})

        duplicate = copy.deepcopy(count)
        duplicate.update(id="demo.rule.duplicate-count", publishes="demo.tax.second-count")
        duplicate_parts = parts + [(duplicate, "computation")]
        pkg["members"].append({"role": "computation", "schema": duplicate["schema"], "id": duplicate["id"], "version": duplicate["version"]})
        pkg["entrypoints"].append({"id": duplicate["id"], "version": duplicate["version"]})
        pkg["package_checksum"] = package_instance_checksum({k: v for k, v in pkg.items() if k != "package_checksum"})
        duplicate_result = validate_package(pkg, {(c["id"], c["version"]): c for c, _ in duplicate_parts}, DerivationSchemas())
        self.assertIn("READER_ROLE_DUPLICATE", [issue.code for issue in duplicate_result.issues])
