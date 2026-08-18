"""Track 3 bounded 2025 covered-W migration acceptance (ADR-0066 Decision 8).

Generic machinery does not know that these families must declare C1-C4.
This module is the migration-owned completeness check: both whole families
must carry the four constraints and their identity-exclusivity declaration,
and each one-at-a-time removal mutant must fail with exactly one missing
declaration. Package closure over declarations that are present remains
Track 2's generic vocabulary.
"""

from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    check_validation_graph,
    compile_validation_graph,
    package_instance_checksum,
    validate_package,
)

REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
T3 = REPO / "packages" / "sample_data" / "declarative_validation_substrate_t3"

ST = "tax.us.2025.f1099b.covered-w-st"
LT = "tax.us.2025.f1099b.covered-w-lt"
REQUIRED_FAMILIES = (ST, LT)
REQUIRED_CONSTRAINT_IDS = (
    "tax.us.2025.constraint.f8949.box-1g-flag-without-amount",
    "tax.us.2025.constraint.f8949.box-1g-amount-without-flag",
    "tax.us.2025.constraint.f8949.code-w-on-gain",
    "tax.us.2025.constraint.f8949.adjustment-exceeds-loss",
)
REQUIRED_EXCLUSIVITY = {
    ST: "tax.us.2025.f1099b.covered-st",
    LT: "tax.us.2025.f1099b.covered-lt",
}
IDENTITY_COMPONENTS = ("broker", "statement", "transaction", "tax-year")
SCALAR_PINS = {
    "tax.us.2025.f1099b.covered-w-st-proceeds": ST,
    "tax.us.2025.f1099b.covered-w-st-basis": ST,
    "tax.us.2025.f1099b.covered-w-st-adjustment": ST,
    "tax.us.2025.f1099b.covered-w-lt-proceeds": LT,
    "tax.us.2025.f1099b.covered-w-lt-basis": LT,
    "tax.us.2025.f1099b.covered-w-lt-adjustment": LT,
}
CONSUMER_CLASSES = (
    "tax.us.2025.rule.f1099b-covered-w-st-proceeds-subtotal",
    "tax.us.2025.rule.f1099b-covered-w-st-basis-subtotal",
    "tax.us.2025.rule.f1099b-covered-w-st-adjustment-subtotal",
    "tax.us.2025.rule.f1099b-covered-w-lt-proceeds-subtotal",
    "tax.us.2025.rule.f1099b-covered-w-lt-basis-subtotal",
    "tax.us.2025.rule.f1099b-covered-w-lt-adjustment-subtotal",
    "tax.us.2025.rule.schedule-d-line1b",
    "tax.us.2025.rule.schedule-d-line8b",
    "tax.us.2025.rule.attachment.f8949",
    "tax.us.2025.rule.attachment.schedule-d",
)
V31_CHECKSUM = "58962a776cd1ce980b84d00be3503cd331f46c7ce8652ab0616383a9ac8d709c"
V26_REGISTRY_SHA = "0fd7433e0b8e31d9ea6b3f1ca2f121a173e7a216e1dbd9f9a6013daace5615ce"


def _load(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((CONTENT / name).read_text())
    return loaded


def _family_docs() -> dict[str, dict[str, Any]]:
    return {
        ST: _load("family.f1099b-covered-w-st.v2.json"),
        LT: _load("family.f1099b-covered-w-lt.v2.json"),
    }


def missing_declarations(family_docs: dict[str, dict[str, Any]]) -> list[str]:
    missing: list[str] = []
    for family_id in REQUIRED_FAMILIES:
        family = family_docs.get(family_id)
        if family is None:
            missing.append(f"family {family_id} absent")
            continue
        constraints = {item["id"] for item in family.get("member_constraints") or []}
        for constraint_id in REQUIRED_CONSTRAINT_IDS:
            if constraint_id not in constraints:
                missing.append(f"{family_id} missing constraint {constraint_id}")
        counterparts = {
            rule["incompatible_family"]["id"]
            for rule in family.get("identity_exclusivity") or []
        }
        expected = REQUIRED_EXCLUSIVITY[family_id]
        if expected not in counterparts:
            missing.append(f"{family_id} missing exclusivity vs {expected}")
    return missing


def drop_constraint(
    family_docs: dict[str, dict[str, Any]], family_id: str, constraint_id: str
) -> dict[str, dict[str, Any]]:
    family = dict(family_docs[family_id])
    family["member_constraints"] = [
        item for item in family["member_constraints"] if item["id"] != constraint_id
    ]
    return dict(family_docs, **{family_id: family})


def drop_exclusivity(
    family_docs: dict[str, dict[str, Any]], family_id: str
) -> dict[str, dict[str, Any]]:
    family = dict(family_docs[family_id])
    family["identity_exclusivity"] = []
    return dict(family_docs, **{family_id: family})


def _content_corpus() -> dict[tuple[str, str], dict[str, Any]]:
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        data = json.loads(path.read_text())
        if {"id", "version", "schema"} <= data.keys() and not (
            "citizens" in data and "packages" in data
        ):
            corpus[(data["id"], str(data["version"]))] = data
    return corpus


class MigrationDeclarations(unittest.TestCase):
    def test_complete_selected_content(self) -> None:
        self.assertEqual(missing_declarations(_family_docs()), [])

    def test_ten_one_at_a_time_mutants(self) -> None:
        family_docs = _family_docs()
        observed: list[str] = []
        for family_id in REQUIRED_FAMILIES:
            for constraint_id in REQUIRED_CONSTRAINT_IDS:
                expected = f"{family_id} missing constraint {constraint_id}"
                missing = missing_declarations(
                    drop_constraint(family_docs, family_id, constraint_id)
                )
                self.assertEqual(missing, [expected], missing)
                observed.append(expected)
            expected = (
                f"{family_id} missing exclusivity vs {REQUIRED_EXCLUSIVITY[family_id]}"
            )
            missing = missing_declarations(drop_exclusivity(family_docs, family_id))
            self.assertEqual(missing, [expected], missing)
            observed.append(expected)
        self.assertEqual(len(observed), 10)

    def test_whole_families_carry_c1_c4_and_exclusivity_shape(self) -> None:
        for family_id, family in _family_docs().items():
            self.assertEqual(family["schema"], "source-family.v2")
            self.assertEqual(family["version"], "v2")
            codes = [item["block_code"] for item in family["member_constraints"]]
            self.assertEqual(
                codes,
                [
                    "BOX_1G_FLAG_WITHOUT_AMOUNT",
                    "BOX_1G_AMOUNT_WITHOUT_FLAG",
                    "CODE_W_ON_GAIN",
                    "ADJUSTMENT_EXCEEDS_LOSS",
                ],
            )
            exclusivity = family["identity_exclusivity"]
            self.assertEqual(len(exclusivity), 1)
            rule = exclusivity[0]
            self.assertEqual(rule["id"], "tax.us.2025.block.covered-w.identity-key-collision")
            self.assertEqual(
                rule["incompatible_family"],
                {"id": REQUIRED_EXCLUSIVITY[family_id], "version": "v1"},
            )
            self.assertEqual(
                [component["fact_id_bound_key"] for component in rule["components"]],
                list(IDENTITY_COMPONENTS),
            )

    def test_scalar_projects_from_whole_v2(self) -> None:
        for scalar_id, whole_id in SCALAR_PINS.items():
            suffix = scalar_id.split("f1099b.", 1)[1]  # covered-w-st-proceeds
            family = _load(f"family.f1099b-{suffix}.v2.json")
            self.assertEqual(family["id"], scalar_id)
            self.assertEqual(family["schema"], "source-family.v2")
            self.assertEqual(
                family["projects_from"],
                {"id": whole_id, "version": "v2"},
            )
            self.assertNotIn("family", family["projects_from"])
            self.assertNotIn("field", family["projects_from"])


class PackagePublication(unittest.TestCase):
    def test_v32_validates_and_compiled_graph(self) -> None:
        pkg = _load("package.core-calculations.v32.json")
        self.assertEqual(pkg["schema"], "artifact-package.v24")
        self.assertEqual(pkg["version"], "v32")
        self.assertEqual(pkg["package_checksum"], package_instance_checksum(pkg))
        corpus = _content_corpus()
        result = validate_package(
            pkg,
            {(m["id"], m["version"]): corpus[(m["id"], m["version"])] for m in pkg["members"]},
            DerivationSchemas(),
        )
        self.assertTrue(result.ok, result.issues)
        producers = [
            member
            for member in result.resolved_members
            if str(member.get("id", "")).endswith(".member-validation.synthesized")
        ]
        self.assertEqual(
            sorted(producer["id"] for producer in producers),
            [
                f"{LT}.member-validation.synthesized",
                f"{ST}.member-validation.synthesized",
            ],
        )
        by_id = {member["id"]: member for member in result.resolved_members}
        expected_edges = {
            "tax.us.2025.rule.f1099b-covered-w-st-proceeds-subtotal": [f"{ST}.member-validation"],
            "tax.us.2025.rule.f1099b-covered-w-st-basis-subtotal": [f"{ST}.member-validation"],
            "tax.us.2025.rule.f1099b-covered-w-st-adjustment-subtotal": [f"{ST}.member-validation"],
            "tax.us.2025.rule.f1099b-covered-w-lt-proceeds-subtotal": [f"{LT}.member-validation"],
            "tax.us.2025.rule.f1099b-covered-w-lt-basis-subtotal": [f"{LT}.member-validation"],
            "tax.us.2025.rule.f1099b-covered-w-lt-adjustment-subtotal": [f"{LT}.member-validation"],
            "tax.us.2025.rule.schedule-d-line1b": [f"{ST}.member-validation"],
            "tax.us.2025.rule.schedule-d-line8b": [f"{LT}.member-validation"],
            "tax.us.2025.rule.attachment.f8949": [
                f"{LT}.member-validation",
                f"{ST}.member-validation",
            ],
            "tax.us.2025.rule.attachment.schedule-d": [
                f"{LT}.member-validation",
                f"{ST}.member-validation",
            ],
        }
        for consumer_id, symbols in expected_edges.items():
            requires = [
                req
                for req in by_id[consumer_id].get("requires", [])
                if str(req).endswith(".member-validation")
            ]
            self.assertEqual(requires, symbols, consumer_id)

    def test_v32_publication_and_adoption_checksums(self) -> None:
        pkg = _load("package.core-calculations.v32.json")
        registry = json.loads((CONTENT / "published-packages.v27.json").read_text())
        entry = next(
            item
            for item in registry["packages"]
            if item["id"] == pkg["id"] and item["version"] == "v32"
        )
        self.assertEqual(entry["checksum"], pkg["package_checksum"])
        release = json.loads(
            (T3 / "publication_surface/releases/demo.release.2025.v25.json").read_text()
        )
        self.assertEqual(release["id"], "demo.release.2025")
        self.assertEqual(release["version"], "v25")
        self.assertEqual(
            release["package_registry_sha256"],
            hashlib.sha256((CONTENT / "published-packages.v27.json").read_bytes()).hexdigest(),
        )
        adoption = json.loads((T3 / "adoptions/adopt-core-v32-current.json").read_text())
        self.assertEqual(adoption["payload"]["revision"], 32)
        self.assertEqual(adoption["payload"]["package"]["version"], "v32")
        self.assertEqual(
            adoption["payload"]["package"]["checksum"], pkg["package_checksum"]
        )
        self.assertEqual(adoption["payload"]["release"]["version"], "v25")

    def test_historical_v31_and_v26_byte_identity(self) -> None:
        v31 = _load("package.core-calculations.v31.json")
        self.assertEqual(v31["version"], "v31")
        self.assertEqual(v31["package_checksum"], V31_CHECKSUM)
        self.assertEqual(package_instance_checksum(v31), V31_CHECKSUM)
        v26_bytes = (CONTENT / "published-packages.v26.json").read_bytes()
        self.assertEqual(hashlib.sha256(v26_bytes).hexdigest(), V26_REGISTRY_SHA)
        v31_result = validate_package(
            v31,
            {
                (member["id"], member["version"]): _content_corpus()[(member["id"], member["version"])]
                for member in v31["members"]
            },
            DerivationSchemas(),
        )
        self.assertTrue(v31_result.ok, v31_result.issues)

    def test_consumer_class_accounting_and_compiled_edge_mutants(self) -> None:
        pkg = _load("package.core-calculations.v32.json")
        corpus = _content_corpus()
        members = {
            (member["id"], member["version"]): corpus[(member["id"], member["version"])]
            for member in pkg["members"]
        }
        families_by_id = {
            citizen["id"]: citizen
            for citizen in members.values()
            if citizen["schema"] in {"source-family.v1", "source-family.v2"}
        }
        families_by_subtotal = {
            family["authorizes_subtotal"]: family["id"]
            for family in families_by_id.values()
        }
        compiled = compile_validation_graph(
            list(members.values()), families_by_id, families_by_subtotal, DerivationSchemas()
        )
        issues = check_validation_graph(
            compiled, families_by_id, families_by_subtotal, pkg["id"]
        )
        self.assertEqual(issues, [])

        # Remove one compiled consumer edge.
        omitted = copy.deepcopy(compiled)
        target = next(item for item in omitted if item["id"] == "tax.us.2025.rule.schedule-d-line1b")
        target["requires"] = [
            req for req in target["requires"] if req != f"{ST}.member-validation"
        ]
        omitted_issues = check_validation_graph(
            omitted, families_by_id, families_by_subtotal, pkg["id"]
        )
        self.assertTrue(
            any(
                issue.code == "SYNTHESIZED_PREREQUISITE_OMITTED"
                and issue.member_id == "tax.us.2025.rule.schedule-d-line1b"
                for issue in omitted_issues
            ),
            omitted_issues,
        )

        # Duplicate a validation producer.
        ambiguous = copy.deepcopy(compiled)
        producer = next(
            item for item in ambiguous if item["id"] == f"{ST}.member-validation.synthesized"
        )
        duplicate = dict(producer)
        duplicate["id"] = f"{ST}.member-validation.duplicate"
        ambiguous.append(duplicate)
        ambiguous_issues = check_validation_graph(
            ambiguous, families_by_id, families_by_subtotal, pkg["id"]
        )
        self.assertTrue(
            any(issue.code == "VALIDATION_PRODUCER_AMBIGUOUS" for issue in ambiguous_issues),
            ambiguous_issues,
        )

        # Remove the synthesized producer.
        removed = [
            item
            for item in compiled
            if item["id"] != f"{ST}.member-validation.synthesized"
        ]
        removed_issues = check_validation_graph(
            removed, families_by_id, families_by_subtotal, pkg["id"]
        )
        self.assertTrue(
            any(issue.code == "VALIDATION_PRODUCER_MISSING" for issue in removed_issues),
            removed_issues,
        )

        # Mutate accounts_for on one consumer per class.
        subtotal = copy.deepcopy(members[("tax.us.2025.rule.f1099b-covered-w-st-proceeds-subtotal", "v2")])
        line = copy.deepcopy(members[("tax.us.2025.rule.schedule-d-line1b", "v2")])
        attachment = copy.deepcopy(members[("tax.us.2025.rule.attachment.f8949", "v2")])

        for consumer in (subtotal, line, attachment):
            mutated = copy.deepcopy(consumer)
            mutated["accounts_for"] = []
            mutated_members = dict(members)
            mutated_members[(mutated["id"], mutated["version"])] = mutated
            result = validate_package(pkg, mutated_members, DerivationSchemas())
            self.assertFalse(result.ok)
            self.assertTrue(
                any(
                    issue.code == "FAMILY_ACCOUNTING_NOT_DECLARED"
                    and issue.member_id == mutated["id"]
                    for issue in result.issues
                ),
                result.issues,
            )

        extra = copy.deepcopy(line)
        extra["accounts_for"] = list(extra["accounts_for"]) + [
            {
                "relationship": "composes_line",
                "family": {"id": ST, "version": "v2"},
            }
        ]
        extra_members = dict(members)
        extra_members[(extra["id"], extra["version"])] = extra
        extra_result = validate_package(pkg, extra_members, DerivationSchemas())
        self.assertTrue(
            any(
                issue.code == "FAMILY_ACCOUNTING_UNREACHED" and issue.member_id == extra["id"]
                for issue in extra_result.issues
            ),
            extra_result.issues,
        )

        wrong = copy.deepcopy(line)
        wrong["accounts_for"] = [
            {
                "relationship": entry["relationship"],
                "family": {"id": entry["family"]["id"], "version": "v1"},
            }
            for entry in wrong["accounts_for"]
        ]
        wrong_members = dict(members)
        wrong_members[(wrong["id"], wrong["version"])] = wrong
        wrong_result = validate_package(pkg, wrong_members, DerivationSchemas())
        self.assertTrue(
            any(
                issue.code in {"FAMILY_ACCOUNTING_NOT_DECLARED", "FAMILY_ACCOUNTING_UNREACHED"}
                and issue.member_id == wrong["id"]
                for issue in wrong_result.issues
            ),
            wrong_result.issues,
        )


class DomainCodeInventory(unittest.TestCase):
    def test_deleted_symbols_absent_from_assigned_engine(self) -> None:
        banned = (
            "_F8949_ROW_GUARD_BOXES",
            "_LINE_GUARD_BOX_KEYS",
            "_f8949_row_guard_violations",
            "_COVERED_W_IDENTITY_COLLISION_BOX_TYPES",
            "_COVERED_W_IDENTITY_COLLISION_PAIRS",
            "_COVERED_W_IDENTITY_KEY_NAMES",
            "find_covered_w_identity_key_collisions",
            "GUARD_NONLOSS_ADJUSTMENT",
            "GUARD_ADJUSTMENT_EXCEEDS_LOSS",
            "GUARD_FLAG_WITHOUT_AMOUNT",
            "GUARD_AMOUNT_WITHOUT_FLAG",
            "GUARD_IDENTITY_KEY_COLLISION",
        )
        for rel in (
            "packages/derivation/runner.py",
            "packages/derivation/package_validation.py",
            "packages/derivation/marshal.py",
        ):
            text = (REPO / rel).read_text()
            for symbol in banned:
                self.assertNotIn(symbol, text, rel)
        marshal = (REPO / "packages/derivation/marshal.py").read_text()
        self.assertNotIn("Form 8949 row guards", marshal)
        self.assertIn("LINE_1A_8A_PINS_COVERED_W", (REPO / "packages/derivation/package_validation.py").read_text())


class TaxRegistryMixedFamilyVersions(unittest.TestCase):
    """The shared tax_registry()/load_source_families() boundary must accept
    a mix of source-family.v1 and source-family.v2 declarations: it globs
    every family.*.json under the 2025 content directory, and this
    migration's eight new families are the first source-family.v2 citizens
    to live there.
    """

    def test_tax_registry_loads_with_mixed_v1_and_v2_families(self) -> None:
        from packages.tax.loader import load_source_families, tax_registry

        reg = tax_registry()
        families = load_source_families(reg)
        for family_id in REQUIRED_FAMILIES:
            self.assertEqual(families[family_id]["version"], "v2")
        self.assertTrue(
            any(f["version"] == "v1" for f in families.values()),
            "expected at least one pre-existing v1 family to remain loadable",
        )
