"""Track 5a: ADR 0076 Parts 1 and 2, the declarative half.

``rule-artifact.v11`` adds ``subject`` (required) and ``joined``/``direction``
(optional, present together) to v10's grammar. ``artifact-package.v32``
admits it. This file exercises only the new declarations and the static
package-validation checks they add: schema shape, pin resolution, and
identity-key containment. **No runtime behaviour** — scheduling and the
runtime presence check are Track 5b. Every behaviour test here uses a v11
rule on a v32 package (ADR 0076's acceptance condition); the existing
``tests/test_sli_g2_binding_probe.py`` probes are not touched and remain
evidence of today's undeclared behaviour on v1-v10/v31.
"""

from __future__ import annotations

import copy
import unittest
from typing import Any

from packages.derivation.authorization_closure import build_dependency_edges
from packages.derivation.live import _resolved_run_material
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    package_instance_checksum,
    validate_package,
)
from packages.kernel.schema_registry import SchemaValidationError
from tests.derivation.test_link_coverage_contract import (
    BOX1,
    LINKS,
    PARAM_ID,
    REDUCTIONS,
    SCOPE,
    _Graph,
    _citation,
    _coverage,
    _fact_type as _statement_fact_type,
    _parameter,
    _reduction,
)

RULE_SUBJECT_UNRESOLVED = "RULE_SUBJECT_UNRESOLVED"
RULE_JOINED_UNRESOLVED = "RULE_JOINED_UNRESOLVED"
RULE_RELATIONSHIP_NOT_CONTAINED = "RULE_RELATIONSHIP_NOT_CONTAINED"
LINK_COVERAGE_RELATIONSHIP_INVALID = "LINK_COVERAGE_RELATIONSHIP_INVALID"
PACKAGE_SCHEMA_INVALID = "PACKAGE_SCHEMA_INVALID"

STATEMENT = "demo.tax.f1098e.statement"
ENROLMENT = "demo.tax.enrolment-circumstance"
FINANCING = "demo.tax.financing-claim"

STATEMENT_IDENTITY = ["lender", "statement", "tax-year"]
FULL_LINK_IDENTITY = STATEMENT_IDENTITY + ["borrowing"]
ENROLMENT_IDENTITY = ["period", "institution", "programme"]
FINANCING_IDENTITY = ["borrowing", "period", "institution", "programme"]


def _fact_type(fact_id: str, key_names: list[str], *, version: str = "v1") -> dict[str, Any]:
    """A ``fact-type.v2`` citizen whose identity is exactly ``key_names``.

    Only the names matter to the containment check under test; each key is
    declared ``literal`` with a placeholder domain, the same shape
    ``test_link_coverage_contract._fact_type`` already uses.
    """
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": version,
        "title": fact_id,
        "nature": "determinable",
        "identity_keys": [
            {"name": name, "kind": "literal", "values": ["placeholder"]}
            for name in key_names
        ],
        "value_schema": {"type": "object"},
        "supersession": {"policy": "free"},
    }


def _v11_rule(
    *,
    rule_id: str,
    subject: dict[str, str],
    joined: dict[str, str] | None = None,
    direction: str | None = None,
    value: Any = True,
    publishes: str | None = None,
    requires: list[str] | None = None,
    version: str = "v1",
) -> dict[str, Any]:
    rule: dict[str, Any] = {
        "schema": "rule-artifact.v11",
        "id": rule_id,
        "version": version,
        "scope": dict(SCOPE),
        "subject": dict(subject),
        "role": "computation",
        "requires": list(requires or []),
        "pins": [],
        "when": True,
        "value": value,
        "publishes": publishes or f"{rule_id}.output",
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
    }
    if joined is not None:
        rule["joined"] = dict(joined)
    if direction is not None:
        rule["direction"] = direction
    return rule


def _package(
    parts: list[tuple[dict[str, Any], str]],
    *,
    bindings: list[dict[str, Any]] | None = None,
    entrypoints: list[dict[str, str]] | None = None,
    schema: str = "artifact-package.v32",
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema": schema,
        "id": "demo.package.subject-relationship",
        "version": "v1",
        "scope": dict(SCOPE),
        "admitted_schemas": sorted({citizen["schema"] for citizen, _role in parts}),
        "members": [
            {
                "role": role,
                "schema": citizen["schema"],
                "id": citizen["id"],
                "version": citizen["version"],
            }
            for citizen, role in parts
        ],
        "input_bindings": list(bindings or []),
        "entrypoints": entrypoints or [{"id": parts[0][0]["id"], "version": parts[0][0]["version"]}],
        "composition_obligations": [],
    }
    body["package_checksum"] = package_instance_checksum(body)
    return body


def _validate(parts: list[tuple[dict[str, Any], str]], **kwargs: Any) -> tuple[Any, dict[str, Any]]:
    package = _package(parts, **kwargs)
    corpus = {(citizen["id"], citizen["version"]): citizen for citizen, _role in parts}
    return validate_package(package, corpus, DerivationSchemas()), package


def _codes(result: Any) -> list[str]:
    return [issue.code for issue in result.issues]


class RuleArtifactV11Schema(unittest.TestCase):
    """Schema-level shape: subject required; joined/direction paired; direction closed."""

    def _base(self) -> dict[str, Any]:
        return _v11_rule(
            rule_id="demo.rule.v11-schema-shape",
            subject={"id": STATEMENT, "version": "v1"},
        )

    def test_worked_shape_validates(self) -> None:
        DerivationSchemas().validate_declared(self._base())

    def test_missing_subject_is_rejected(self) -> None:
        rule = self._base()
        del rule["subject"]
        with self.assertRaises(SchemaValidationError):
            DerivationSchemas().validate_declared(rule)

    def test_joined_without_direction_is_rejected(self) -> None:
        rule = self._base()
        rule["joined"] = {"id": LINKS, "version": "v1"}
        with self.assertRaises(SchemaValidationError):
            DerivationSchemas().validate_declared(rule)

    def test_direction_without_joined_is_rejected(self) -> None:
        rule = self._base()
        rule["direction"] = "joined_contains_subject"
        with self.assertRaises(SchemaValidationError):
            DerivationSchemas().validate_declared(rule)

    def test_unknown_direction_is_rejected(self) -> None:
        rule = self._base()
        rule["joined"] = {"id": LINKS, "version": "v1"}
        rule["direction"] = "sideways"
        with self.assertRaises(SchemaValidationError):
            DerivationSchemas().validate_declared(rule)

    def test_v11_rejected_as_member_of_v31_accepted_on_v32(self) -> None:
        rule = self._base()
        parts = [
            (rule, "computation"),
            (_statement_fact_type(STATEMENT, "Demo statement"), "fact-type"),
        ]
        entrypoints = [
            {"id": rule["id"], "version": rule["version"]},
            {"id": STATEMENT, "version": "v1"},
        ]
        v31_result, _pkg = _validate(parts, schema="artifact-package.v31", entrypoints=entrypoints)
        self.assertFalse(v31_result.ok)
        self.assertIn(PACKAGE_SCHEMA_INVALID, _codes(v31_result))

        v32_result, _pkg = _validate(parts, schema="artifact-package.v32", entrypoints=entrypoints)
        self.assertTrue(v32_result.ok, v32_result.issues)


class PinResolution(unittest.TestCase):
    """An unresolvable subject or joined pin is rejected."""

    def test_unresolvable_subject_is_rejected(self) -> None:
        rule = _v11_rule(
            rule_id="demo.rule.unresolved-subject",
            subject={"id": "demo.tax.no-such-type", "version": "v1"},
        )
        result, _pkg = _validate([(rule, "computation")])
        self.assertFalse(result.ok)
        self.assertIn(RULE_SUBJECT_UNRESOLVED, _codes(result))

    def test_unresolvable_joined_is_rejected(self) -> None:
        rule = _v11_rule(
            rule_id="demo.rule.unresolved-joined",
            subject={"id": STATEMENT, "version": "v1"},
            joined={"id": "demo.tax.no-such-joined-type", "version": "v1"},
            direction="joined_contains_subject",
        )
        parts = [
            (rule, "computation"),
            (_statement_fact_type(STATEMENT, "Demo statement"), "fact-type"),
        ]
        result, _pkg = _validate(parts)
        self.assertFalse(result.ok)
        self.assertIn(RULE_JOINED_UNRESOLVED, _codes(result))

    def test_stale_version_does_not_resolve(self) -> None:
        rule = _v11_rule(
            rule_id="demo.rule.stale-version-subject",
            subject={"id": STATEMENT, "version": "v2"},
        )
        parts = [
            (rule, "computation"),
            (_fact_type(STATEMENT, ["statement"]), "fact-type"),
        ]
        result, _pkg = _validate(parts)
        self.assertFalse(result.ok)
        self.assertIn(RULE_SUBJECT_UNRESOLVED, _codes(result))


class RelationshipKeyNameTable(unittest.TestCase):
    """ADR 0076 Part 2's key-name table, as declared fact types.

    Each case declares a subject and a joined fact type with the ADR's
    exact identity-key names (see ``tests/test_sli_g2_binding_probe.py``'s
    ``STATEMENT_IDENTITY``/``FINANCING_IDENTITY``/``ENROLMENT_IDENTITY``,
    which this test does not import or edit) and checks both directions.
    """

    def _rule(self, *, direction: str, subject_id: str, joined_id: str) -> dict[str, Any]:
        return _v11_rule(
            rule_id=f"demo.rule.relationship-{direction}-{subject_id}-{joined_id}",
            subject={"id": subject_id, "version": "v1"},
            joined={"id": joined_id, "version": "v1"},
            direction=direction,
        )

    def _check(
        self, *, subject_id: str, subject_keys: list[str], joined_id: str, joined_keys: list[str]
    ) -> dict[str, bool]:
        subject_type = _fact_type(subject_id, subject_keys)
        joined_type = _fact_type(joined_id, joined_keys)
        outcome: dict[str, bool] = {}
        for direction in ("joined_contains_subject", "subject_contains_joined"):
            rule = self._rule(direction=direction, subject_id=subject_id, joined_id=joined_id)
            result, _pkg = _validate(
                [
                    (rule, "computation"),
                    (subject_type, "fact-type"),
                    (joined_type, "fact-type"),
                ],
                entrypoints=[
                    {"id": rule["id"], "version": rule["version"]},
                    {"id": subject_id, "version": "v1"},
                    {"id": joined_id, "version": "v1"},
                ],
            )
            outcome[direction] = RULE_RELATIONSHIP_NOT_CONTAINED not in _codes(result)
            if outcome[direction]:
                self.assertTrue(result.ok, result.issues)
        return outcome

    def test_tax_year_and_borrowing_vs_statement_identity_both_reject(self) -> None:
        outcome = self._check(
            subject_id="demo.tax.statement.a",
            subject_keys=STATEMENT_IDENTITY,
            joined_id="demo.tax.link.tax-year-and-borrowing",
            joined_keys=["tax-year", "borrowing"],
        )
        self.assertEqual(outcome, {"joined_contains_subject": False, "subject_contains_joined": False})

    def test_shared_statement_id_only_both_reject(self) -> None:
        """No lender, no tax-year on the link: statement + borrowing only."""
        outcome = self._check(
            subject_id="demo.tax.statement.b",
            subject_keys=STATEMENT_IDENTITY,
            joined_id="demo.tax.link.statement-and-borrowing-only",
            joined_keys=["statement", "borrowing"],
        )
        self.assertEqual(outcome, {"joined_contains_subject": False, "subject_contains_joined": False})

    def test_lender_tax_year_and_borrowing_both_reject(self) -> None:
        outcome = self._check(
            subject_id="demo.tax.statement.c",
            subject_keys=STATEMENT_IDENTITY,
            joined_id="demo.tax.link.lender-tax-year-borrowing",
            joined_keys=["lender", "tax-year", "borrowing"],
        )
        self.assertEqual(outcome, {"joined_contains_subject": False, "subject_contains_joined": False})

    def test_full_statement_identity_plus_borrowing_only_joined_contains_subject(self) -> None:
        outcome = self._check(
            subject_id="demo.tax.statement.d",
            subject_keys=STATEMENT_IDENTITY,
            joined_id="demo.tax.link.full-statement-plus-borrowing",
            joined_keys=FULL_LINK_IDENTITY,
        )
        self.assertEqual(outcome, {"joined_contains_subject": True, "subject_contains_joined": False})

    def test_full_enrolment_vs_financing_only_subject_contains_joined(self) -> None:
        outcome = self._check(
            subject_id="demo.tax.financing.e",
            subject_keys=FINANCING_IDENTITY,
            joined_id="demo.tax.enrolment.full",
            joined_keys=ENROLMENT_IDENTITY,
        )
        self.assertEqual(outcome, {"joined_contains_subject": False, "subject_contains_joined": True})

    def test_period_only_enrolment_subject_contains_joined_accepts_this_is_adr_residual_1(self) -> None:
        """ADR 0076 residual 1: a weaker declaration passes at validation.

        This is not a fix. The check enforces containment over whatever the
        fact type declares; a period-only enrolment declaration is a content
        decision the check cannot see is too weak.
        """
        outcome = self._check(
            subject_id="demo.tax.financing.f",
            subject_keys=FINANCING_IDENTITY,
            joined_id="demo.tax.enrolment.period-only",
            joined_keys=["period"],
        )
        self.assertEqual(outcome, {"joined_contains_subject": False, "subject_contains_joined": True})


class LinkCoverageRelationshipRequirement(unittest.TestCase):
    """A v11 link_coverage rule must declare joined == links, direction joined_contains_subject."""

    def _coverage_v11(
        self,
        *,
        joined: dict[str, str] | None,
        direction: str | None,
    ) -> dict[str, Any]:
        rule = copy.deepcopy(_coverage())
        rule["schema"] = "rule-artifact.v11"
        rule["subject"] = {"id": BOX1, "version": "v1"}
        if joined is not None:
            rule["joined"] = joined
        if direction is not None:
            rule["direction"] = direction
        return rule

    def _parts(self, rule: dict[str, Any]) -> list[tuple[dict[str, Any], str]]:
        return [
            (rule, "computation"),
            (_reduction(), "computation"),
            (_parameter(), "parameter"),
            (_statement_fact_type(LINKS, "Demo statement to borrowing link"), "fact-type"),
            (_statement_fact_type(BOX1, "Demo box 1"), "fact-type"),
            (_citation(), "citation"),
        ]

    def _entrypoints(self, rule: dict[str, Any]) -> list[dict[str, str]]:
        return [
            {"id": rule["id"], "version": rule["version"]},
            {"id": BOX1, "version": "v1"},
            {"id": LINKS, "version": "v1"},
        ]

    def test_wrong_direction_is_rejected(self) -> None:
        rule = self._coverage_v11(
            joined={"id": LINKS, "version": "v1"}, direction="subject_contains_joined"
        )
        result, _pkg = _validate(self._parts(rule), entrypoints=self._entrypoints(rule))
        self.assertFalse(result.ok)
        self.assertIn(LINK_COVERAGE_RELATIONSHIP_INVALID, _codes(result))

    def test_wrong_joined_type_is_rejected(self) -> None:
        rule = self._coverage_v11(
            joined={"id": BOX1, "version": "v1"}, direction="joined_contains_subject"
        )
        result, _pkg = _validate(self._parts(rule), entrypoints=self._entrypoints(rule))
        self.assertFalse(result.ok)
        self.assertIn(LINK_COVERAGE_RELATIONSHIP_INVALID, _codes(result))

    def test_no_joined_is_rejected(self) -> None:
        rule = self._coverage_v11(joined=None, direction=None)
        result, _pkg = _validate(self._parts(rule), entrypoints=self._entrypoints(rule))
        self.assertFalse(result.ok)
        self.assertIn(LINK_COVERAGE_RELATIONSHIP_INVALID, _codes(result))

    def test_right_pair_is_accepted(self) -> None:
        rule = self._coverage_v11(
            joined={"id": LINKS, "version": "v1"}, direction="joined_contains_subject"
        )
        result, _pkg = _validate(self._parts(rule), entrypoints=self._entrypoints(rule))
        self.assertTrue(result.ok, result.issues)
        self.assertNotIn(LINK_COVERAGE_RELATIONSHIP_INVALID, _codes(result))


class V10Unaffected(unittest.TestCase):
    """A v10 package that validated before still validates."""

    def test_existing_v10_worked_example_still_validates(self) -> None:
        from tests.derivation.test_link_coverage_contract import _base_parts
        from tests.derivation.test_link_coverage_contract import _validate as _v10_validate

        result, _pkg = _v10_validate(_base_parts())
        self.assertTrue(result.ok, result.issues)


class AdmissionSetsTreatV11LikeV10(unittest.TestCase):
    """live._resolved_run_material and authorization_closure give v11 the
    same link_coverage edges as v10 (admission only)."""

    def _v11_coverage_rule(self) -> dict[str, Any]:
        rule = copy.deepcopy(_coverage())
        rule["schema"] = "rule-artifact.v11"
        rule["id"] = "demo.rule.v11-statement-box-minus-reductions"
        rule["subject"] = {"id": BOX1, "version": "v1"}
        rule["joined"] = {"id": LINKS, "version": "v1"}
        rule["direction"] = "joined_contains_subject"
        return rule

    def test_resolved_run_material_names_the_v11_rule_and_emits_the_link_type(self) -> None:
        rule = self._v11_coverage_rule()
        members = [
            rule,
            _reduction(),
            _parameter(),
            _statement_fact_type(LINKS, "Demo statement to borrowing link"),
            _citation(),
        ]
        material = _resolved_run_material(_Graph(members, {"input_bindings": []}))
        self.assertIn(rule, material[0])
        # Track 5c: a v11 rule's own subject type is emitted too (it was not
        # in 5a, which is why the live path produced no subjects). The joined
        # type is the links type, already emitted for link_coverage.
        self.assertEqual(material.emission_only_names, (LINKS, BOX1))
        self.assertNotIn(LINKS, material[6])
        self.assertNotIn(REDUCTIONS, material[6])

    def test_authorization_closure_gives_v11_the_same_edges_as_v10(self) -> None:
        reduction_rule = _reduction()
        param = _parameter()
        links_fact_type = _statement_fact_type(LINKS, "Demo statement to borrowing link")
        for schema in ("rule-artifact.v10", "rule-artifact.v11"):
            with self.subTest(schema=schema):
                rule = self._v11_coverage_rule()
                rule["schema"] = schema
                if schema == "rule-artifact.v10":
                    del rule["subject"]
                    del rule["joined"]
                    del rule["direction"]
                corpus = {
                    rule["id"]: rule,
                    reduction_rule["id"]: reduction_rule,
                    LINKS: links_fact_type,
                    PARAM_ID: param,
                }
                edges = build_dependency_edges(corpus)
                self.assertEqual(
                    edges[rule["id"]],
                    {reduction_rule["id"], LINKS, PARAM_ID},
                )


if __name__ == "__main__":
    unittest.main()
