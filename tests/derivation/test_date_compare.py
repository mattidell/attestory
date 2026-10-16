"""ADR 0078: the ``date_compare`` operator on ``rule-artifact.v14``.

``date_compare`` compares one date-valued expression against one fixed ISO
date literal carried in the rule. It is the narrowest capability the
mortgage grandfathering condition needs (P3/P4's October 13, 1987 test on
box 3, the Form 1098 origination date) and nothing more: no date
arithmetic, no date-to-date comparison, and no parameterized threshold.

Three layers are exercised, each against the real artifact rather than a
hand-built stand-in:

- the evaluator, directly, for every comparison outcome and every failure
  mode (missing, malformed, non-date);
- schema admission, through ``DerivationSchemas`` against the published
  ``rule-artifact.v14``/``rule-artifact.v13``/``artifact-package.v36``/
  ``artifact-package.v35`` bytes;
- the real production path, through ``live_coordinate_run`` on a temporary
  publication surface with a test-only v14 rule reading a synthetic box-3
  date, never adopted into any shipped tax package.
"""

from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from packages.derivation.evaluator import (
    BLOCK_ABSENT,
    BLOCK_INVALID,
    AccessLog,
    Environment,
    EvalBlocked,
    _is_leap_year,
    _parse_iso_date,
    evaluate,
)
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum, validate_package
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.schema_registry import SchemaValidationError

SCOPE = {"tax_year": 2025, "jurisdiction": "us", "family": "demo"}
THRESHOLD = "1987-10-13"
BOX3_SYMBOL = "demo.tax.adr0078.box3"
PUBLISHES = "demo.tax.adr0078.grandfathered"


def _env(symbols: dict[str, Any]) -> Environment:
    return Environment(
        symbols=symbols,
        symbol_fact_types={},
        symbol_fact_versions={},
        symbol_result_fact_types={},
        categorical_domains={},
        fact_type_versions={},
        sources={},
        closed_sets=frozenset(),
        canon={},
        parameters={},
        parameter_index={},
    )


def _node(left_name: str = "box3", date: str = THRESHOLD, cmp: str = "lt") -> dict[str, Any]:
    return {"op": "date_compare", "left": {"op": "ref", "name": left_name}, "date": date, "cmp": cmp}


class DateCompareEvaluation(unittest.TestCase):
    """Every comparison outcome and failure mode, directly on the evaluator."""

    def test_every_comparison_against_the_threshold(self) -> None:
        cases: tuple[tuple[str, str, bool], ...] = (
            ("eq", "1987-10-13", True),
            ("eq", "1986-01-01", False),
            ("ne", "1986-01-01", True),
            ("ne", "1987-10-13", False),
            ("gt", "1990-01-01", True),
            ("gt", "1987-10-13", False),
            ("gte", "1987-10-13", True),
            ("gte", "1986-01-01", False),
            ("lt", "1986-01-01", True),
            ("lt", "1987-10-13", False),
            ("lte", "1987-10-13", True),
            ("lte", "1990-01-01", False),
        )
        for cmp, box3, expected in cases:
            with self.subTest(cmp=cmp, box3=box3):
                result = evaluate(_node(cmp=cmp), _env({"box3": box3}), AccessLog())
                self.assertEqual(result, expected)

    def test_equality_at_the_threshold_is_exact(self) -> None:
        result = evaluate(_node(date=THRESHOLD, cmp="eq"), _env({"box3": THRESHOLD}), AccessLog())
        self.assertTrue(result)

    def test_missing_left_value_blocks_dependency_absent(self) -> None:
        with self.assertRaises(EvalBlocked) as caught:
            evaluate(_node(), _env({}), AccessLog())
        self.assertEqual(caught.exception.category, BLOCK_ABSENT)
        self.assertEqual(caught.exception.missing, ["box3"])

    def test_malformed_left_value_blocks_dependency_invalid(self) -> None:
        for bad in (
            "not-a-date", "1987/10/13", "19871013", "2025-13-40", "2025-02-30", "",
            # Year 0000 (owner finding 2): the repository's calendar domain
            # (RFC 3339 full-date / Python's own ``date``, MINYEAR=1) has no
            # year 0000, in a leap-shaped day or otherwise.
            "0000-01-01", "0000-02-29",
        ):
            with self.subTest(bad=bad):
                with self.assertRaises(EvalBlocked) as caught:
                    evaluate(_node(), _env({"box3": bad}), AccessLog())
                self.assertEqual(caught.exception.category, BLOCK_INVALID)
                self.assertEqual(caught.exception.missing, [bad])

    def test_non_date_valued_left_blocks_dependency_invalid(self) -> None:
        for bad in (19871013, True, None, ["1987-10-13"]):
            with self.subTest(bad=bad):
                with self.assertRaises(EvalBlocked) as caught:
                    evaluate(_node(), _env({"box3": bad}), AccessLog())
                self.assertEqual(caught.exception.category, BLOCK_INVALID)

    def test_malformed_literal_date_in_the_rule_blocks_dependency_invalid(self) -> None:
        with self.assertRaises(EvalBlocked) as caught:
            evaluate(_node(date="not-a-date"), _env({"box3": "1986-01-01"}), AccessLog())
        self.assertEqual(caught.exception.category, BLOCK_INVALID)
        self.assertEqual(caught.exception.missing, ["not-a-date"])

    def test_year_0000_literal_date_blocks_dependency_invalid(self) -> None:
        # Owner finding 2 applies to the rule's own literal, not only the
        # operand: a hand-authored or mutated rule byte naming year 0000
        # must fail closed the same way.
        with self.assertRaises(EvalBlocked) as caught:
            evaluate(_node(date="0000-01-01"), _env({"box3": "1986-01-01"}), AccessLog())
        self.assertEqual(caught.exception.category, BLOCK_INVALID)
        self.assertEqual(caught.exception.missing, ["0000-01-01"])

    def test_leap_year_february_29_parses_correctly(self) -> None:
        # The hand-rolled parser (no ``datetime`` import; the evaluator is
        # sealed against ambient-state imports) must still get leap years
        # right: 2024 and 2000 are leap; 2023 and 1900 (divisible by 100,
        # not 400) are not.
        self.assertEqual(_parse_iso_date("2024-02-29"), (2024, 2, 29))
        self.assertEqual(_parse_iso_date("2000-02-29"), (2000, 2, 29))
        self.assertIsNone(_parse_iso_date("2023-02-29"))
        self.assertIsNone(_parse_iso_date("1900-02-29"))

    def test_year_0000_is_outside_the_calendar_domain(self) -> None:
        # Owner finding 2: year 0000 is rejected whether or not the
        # month/day happen to look leap-shaped (0000 would itself be a
        # leap year under the 4/100/400 rule, so this is not caught by the
        # ordinary leap-year check alone — it needs its own, explicit year
        # floor).
        self.assertTrue(_is_leap_year(0))
        self.assertIsNone(_parse_iso_date("0000-01-01"))
        self.assertIsNone(_parse_iso_date("0000-02-29"))
        self.assertEqual(_parse_iso_date("0001-01-01"), (1, 1, 1))

    def test_leap_year_february_29_blocks_through_the_operator_when_invalid(self) -> None:
        with self.assertRaises(EvalBlocked) as caught:
            evaluate(_node(), _env({"box3": "1900-02-29"}), AccessLog())
        self.assertEqual(caught.exception.category, BLOCK_INVALID)
        self.assertEqual(caught.exception.missing, ["1900-02-29"])


def _rule(**overrides: Any) -> dict[str, Any]:
    rule: dict[str, Any] = {
        "schema": "rule-artifact.v14",
        "id": "demo.rule.adr0078.grandfathered",
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [],
        "pins": [],
        "when": True,
        "value": _node(left_name=BOX3_SYMBOL),
        "publishes": PUBLISHES,
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
    }
    rule.update(overrides)
    return rule


class DateCompareSchemaAdmission(unittest.TestCase):
    """``rule-artifact.v14`` admits the node; its predecessors still reject it."""

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    def test_v14_rule_with_date_compare_validates(self) -> None:
        self.schemas.validate_declared(_rule())

    def test_v13_rejects_the_same_rule_body(self) -> None:
        rule = _rule(schema="rule-artifact.v13")
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(rule)

    def test_v13_content_is_unaffected_shared_key_count_still_validates(self) -> None:
        # Regression guard for "v14 is v13 plus one operator, nothing removed":
        # an existing v13 shape (shared_key_count, ADR 0077 Part 1) still
        # validates on v13 exactly as before this change.
        rule = {
            "schema": "rule-artifact.v13",
            "id": "demo.rule.adr0077.count",
            "version": "v1",
            "scope": dict(SCOPE),
            "subject": {"id": "demo.tax.adr0077.inclusion", "version": "v1"},
            "role": "computation",
            "requires": [],
            "pins": [],
            "when": True,
            "value": {"op": "shared_key_count", "fact_type": "demo.tax.adr0077.financing", "key": "borrowing"},
            "publishes": "demo.tax.adr0077.count",
            "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
        }
        self.schemas.validate_declared(rule)

    def test_malformed_date_compare_shapes_are_rejected(self) -> None:
        malformed_variants = (
            {"op": "date_compare", "left": {"op": "ref", "name": "box3"}, "date": "1987-10-13"},  # missing cmp
            {"op": "date_compare", "left": {"op": "ref", "name": "box3"}, "cmp": "lt"},  # missing date
            {"op": "date_compare", "date": "1987-10-13", "cmp": "lt"},  # missing left
            {"op": "date_compare", "left": {"op": "ref", "name": "box3"}, "date": "1987-10-13", "cmp": "between"},  # bad cmp
            {"op": "date_compare", "left": {"op": "ref", "name": "box3"}, "date": "19871013", "cmp": "lt"},  # not ISO
            {"op": "date_compare", "left": {"op": "ref", "name": "box3"}, "date": "1987-10-13", "cmp": "lt", "extra": 1},
        )
        for value in malformed_variants:
            with self.subTest(value=value):
                rule = _rule(value=value)
                with self.assertRaises(SchemaValidationError):
                    self.schemas.validate_declared(rule)

    def test_artifact_package_v36_admits_rule_artifact_v14(self) -> None:
        package = {
            "schema": "artifact-package.v36",
            "id": "demo.package.adr0078",
            "version": "v1",
            "scope": dict(SCOPE),
            "admitted_schemas": ["rule-artifact.v14"],
            "members": [{"role": "computation", "schema": "rule-artifact.v14", "id": "demo.rule", "version": "v1"}],
            "input_bindings": [],
            "entrypoints": [{"id": "demo.rule", "version": "v1"}],
            "composition_obligations": [],
        }
        package["package_checksum"] = package_instance_checksum(package)
        self.schemas.validate_declared(package)

    def test_artifact_package_v35_still_rejects_rule_artifact_v14(self) -> None:
        # The predecessor publication surface never admits the new version
        # (boundary: "do not adopt the operator into any published tax
        # package"); only the new v36 schema successor admits v14.
        package = {
            "schema": "artifact-package.v35",
            "id": "demo.package.adr0078.rejected",
            "version": "v1",
            "scope": dict(SCOPE),
            "admitted_schemas": ["rule-artifact.v14"],
            "members": [{"role": "computation", "schema": "rule-artifact.v14", "id": "demo.rule", "version": "v1"}],
            "input_bindings": [],
            "entrypoints": [{"id": "demo.rule", "version": "v1"}],
            "composition_obligations": [],
        }
        package["package_checksum"] = package_instance_checksum(package)
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(package)


class DateComparePackageSchemaInheritance(unittest.TestCase):
    """Owner finding 1: ``artifact-package.v36`` must keep every check
    ``artifact-package.v35`` makes, not only admit ``rule-artifact.v14``.

    A passing date rule does not show that v35's contract survived; these
    tests reproduce, on v36, two checks that v35 already enforces
    (``_reader_role_issues``'s ``READER_ROLE_TEXT_INVALID`` and the exact-
    entrypoint-pin ``ENTRYPOINT_VERSION_MISMATCH``) and confirm v36 still
    rejects what v35 rejects.
    """

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    @staticmethod
    def _base_package(schema: str, members: list[dict[str, Any]], entrypoints: list[dict[str, Any]]) -> dict[str, Any]:
        package: dict[str, Any] = {
            "schema": schema,
            "id": "demo.package.adr0078.inheritance",
            "version": "v2",
            "scope": dict(SCOPE),
            "admitted_schemas": sorted({m["schema"] for m in members}),
            "members": members,
            "input_bindings": [],
            "entrypoints": entrypoints,
            "composition_obligations": [],
        }
        package["package_checksum"] = package_instance_checksum(package)
        return package

    def test_v36_rejects_a_dangling_entrypoint_version_the_same_as_v35(self) -> None:
        # v35 only admits rule-artifact.v13 (not the new v14), so each
        # package surface is paired with the rule schema it actually
        # admits; the semantic check under test — exact-entrypoint-pin
        # ``ENTRYPOINT_VERSION_MISMATCH`` — is schema-generation-scoped, not
        # rule-schema-scoped, and must fire on both pairings alike.
        for package_schema, rule_schema in (
            ("artifact-package.v35", "rule-artifact.v13"),
            ("artifact-package.v36", "rule-artifact.v14"),
        ):
            with self.subTest(package_schema=package_schema):
                rule = _rule(schema=rule_schema)
                members = [{"role": "computation", "schema": rule_schema, "id": rule["id"], "version": "v1"}]
                corpus = {(rule["id"], rule["version"]): rule}
                package = self._base_package(
                    package_schema, members, entrypoints=[{"id": rule["id"], "version": "v999"}],
                )
                result = validate_package(package, corpus, self.schemas)
                self.assertIn("ENTRYPOINT_VERSION_MISMATCH", [issue.code for issue in result.issues])
                self.assertFalse(result.ok)

    def test_v36_rejects_a_misplaced_linenote_the_same_as_v35(self) -> None:
        for package_schema, rule_schema in (
            ("artifact-package.v35", "rule-artifact.v13"),
            ("artifact-package.v36", "rule-artifact.v14"),
        ):
            with self.subTest(package_schema=package_schema):
                # v13 does not admit date_compare; give each generation an
                # ordinary, schema-valid value expression of its own — the
                # check under test is reader-role text placement, not the
                # date operator.
                value = _node(left_name=BOX3_SYMBOL) if rule_schema == "rule-artifact.v14" else {
                    "op": "compare", "left": {"op": "ref", "name": "demo.other"}, "right": 0, "cmp": "gt",
                }
                rule = _rule(
                    schema=rule_schema,
                    id="demo.rule.adr0078.misplaced-line-note",
                    reader_role="statement-amount",
                    lineNote="this belongs only on a bare-statement-conclusion rule",
                    value=value,
                )
                members = [{"role": "computation", "schema": rule_schema, "id": rule["id"], "version": "v1"}]
                corpus = {(rule["id"], rule["version"]): rule}
                package = self._base_package(
                    package_schema, members, entrypoints=[{"id": rule["id"], "version": "v1"}],
                )
                result = validate_package(package, corpus, self.schemas)
                self.assertIn("READER_ROLE_TEXT_INVALID", [issue.code for issue in result.issues])
                self.assertFalse(result.ok)


class DateCompareLiveCoordinator(unittest.TestCase):
    """The operator exercised from facts on record, through the real production
    path (``live_coordinate_run``), never a hand-built ``RunContext``.

    Mirrors ``ConditionalDependencyLiveCoordinator``
    (``tests/derivation/test_conditional_multi_dependency.py``): a synthetic
    temporary publication surface, a real act log, and the coordinator's own
    package-adoption/assertion acts. The package and rule here are test-only
    and admitted through ``artifact-package.v36``/``rule-artifact.v14`` on a
    temporary surface; neither is adopted into any shipped tax package.
    """

    @staticmethod
    def _fact_type(identifier: str, value_schema: dict[str, Any]) -> dict[str, Any]:
        return {
            "schema": "fact-type.v2", "id": identifier, "version": "v1",
            "title": f"Synthetic {identifier}", "nature": "determinable",
            "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
            "value_schema": value_schema, "supersession": {"policy": "free"},
        }

    def _surface_and_acts(
        self, root: Path, box3_value: Any | None
    ) -> tuple[PublicationSurface, list[dict[str, Any]]]:
        member_dir = root / "members"
        release_dir = root / "releases"
        member_dir.mkdir()
        release_dir.mkdir()
        rule = _rule()
        bundle = {
            "schema": "bundle.v2", "id": "demo.bundle.adr0078", "version": "v1",
            "label": "ADR 0078 synthetic box-3 date",
            "fact_types": [self._fact_type(BOX3_SYMBOL, {"type": "string", "format": "date"})],
        }
        package: dict[str, Any] = {
            "schema": "artifact-package.v36",
            "id": "demo.package.adr0078",
            "version": "v2",
            "scope": dict(SCOPE),
            "admitted_schemas": ["bundle.v2", "rule-artifact.v14"],
            "members": [
                {"role": "fact-type-bundle", "schema": "bundle.v2", "id": bundle["id"], "version": "v1"},
                {"role": "computation", "schema": "rule-artifact.v14", "id": rule["id"], "version": "v1"},
            ],
            "input_bindings": [
                {"symbol": BOX3_SYMBOL, "fact_type": {"id": BOX3_SYMBOL, "version": "v1"}, "mode": "required"},
            ],
            "entrypoints": [{"id": rule["id"], "version": "v1"}],
            "composition_obligations": [],
        }
        package["package_checksum"] = package_instance_checksum(package)
        for body in (rule, bundle, package):
            (member_dir / f"{body['id']}.{body['version']}.json").write_text(
                json.dumps(body, sort_keys=True, separators=(",", ":")), encoding="utf-8"
            )
        registry = {
            "packages": [{"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]}],
            "citizens": [
                {"id": rule["id"], "version": rule["version"], "checksum": citizen_checksum(rule)},
                {"id": bundle["id"], "version": bundle["version"], "checksum": citizen_checksum(bundle)},
            ],
        }
        registry_path = root / "published-packages.json"
        registry_path.write_text(json.dumps(registry, sort_keys=True, separators=(",", ":")), encoding="utf-8")
        release = {
            "schema": "release-registry.v1", "id": "demo.release.adr0078", "version": "v1",
            "package_registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest(),
        }
        release_bytes = json.dumps(release, sort_keys=True, separators=(",", ":")).encode("utf-8")
        (release_dir / "demo.release.adr0078.v1.json").write_bytes(release_bytes)

        def act(index: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
            return {"schema": "act.v1", "act_id": f"demo.adr0078.act.{index}", "kind": kind, "actor": "demo.user", "at": f"2026-10-13T00:00:{index:02d}Z", "committed_against": index, "payload": payload}

        acts: list[dict[str, Any]] = [act(0, "bundle-adoption", {"bundle": bundle})]
        if box3_value is not None:
            acts.append(act(len(acts), "assertion", {"finding": {
                "schema": "finding.v1", "id": "demo.adr0078.finding.box3",
                "fact_id": f"{BOX3_SYMBOL}|tax-year=2025", "value": box3_value,
                "basis": "attested", "evidence_ids": [],
            }}))
        acts.append(act(len(acts), "package-adoption", {
            "package": {"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]},
            "release": {"id": release["id"], "version": release["version"], "checksum": hashlib.sha256(release_bytes).hexdigest()},
            "scope": {"jurisdiction": "us", "year": "2052"}, "revision": 1,
        }))
        return PublicationSurface(release_dir, registry_path, member_dir), acts

    def _run(self, box3_value: Any | None, run_id: str) -> tuple[Any, dict[str, Any]]:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            surface, acts = self._surface_and_acts(root, box3_value)
            outcome = live_coordinate_run(
                WorkspaceCapability(root / "workspace"), repo_root=Path(__file__).resolve().parents[2],
                authoritative_acts=acts, workspace_revision=len(acts), run_scope={"jurisdiction": "us", "year": "2052"},
                scope_user="demo.user", request={"schema": "run-request.v1"}, run_id=run_id,
                governance_pins=[], surface=surface, output_name=f"{run_id}.json",
            )
            self.assertIsNone(outcome.refusal)
            records = [json.loads(line) for line in (root / "workspace" / "records" / "derivation_records.jsonl").read_text().splitlines()]
            closing = records[-1]
            return outcome, closing["dispositions"][0]

    def test_before_the_threshold_publishes_true_and_pins_box3(self) -> None:
        outcome, row = self._run("1986-05-01", "adr0078-before")
        self.assertEqual(row["disposition"], "published")
        finding = outcome.publications[0].finding
        self.assertEqual(finding["value"], "true")
        input_ids = {pin["id"] for pin in finding["pins"] if pin["role"] == "input"}
        self.assertEqual(input_ids, {"demo.adr0078.finding.box3"})
        row_input_ids = {pin["id"] for pin in row["pins"] if pin["role"] == "input"}
        self.assertEqual(row_input_ids, {"demo.adr0078.finding.box3"})

    def test_after_the_threshold_publishes_false(self) -> None:
        outcome, row = self._run("1990-01-01", "adr0078-after")
        self.assertEqual(row["disposition"], "published")
        self.assertEqual(outcome.publications[0].finding["value"], "false")

    def test_at_the_threshold_publishes_false_for_lt(self) -> None:
        outcome, row = self._run("1987-10-13", "adr0078-at-threshold")
        self.assertEqual(row["disposition"], "published")
        self.assertEqual(outcome.publications[0].finding["value"], "false")

    def test_missing_box3_blocks_dependency_absent(self) -> None:
        _outcome, row = self._run(None, "adr0078-missing")
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(row["missing"], [BOX3_SYMBOL])

    def test_malformed_box3_blocks_dependency_invalid(self) -> None:
        _outcome, row = self._run("not-a-date", "adr0078-malformed")
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(row["missing"], ["not-a-date"])

    def test_v13_rule_body_is_unaffected_on_a_v13_surface(self) -> None:
        # "existing v13 content is unchanged in behaviour": an ordinary
        # v13 numeric `compare` rule, run the same way, through the same
        # coordinator, is untouched by this addition.
        rule = {
            "schema": "rule-artifact.v13",
            "id": "demo.rule.adr0078.v13-control",
            "version": "v1",
            "scope": dict(SCOPE),
            "role": "computation",
            "requires": [],
            "pins": [],
            "when": True,
            "value": {"op": "compare", "left": {"op": "ref", "name": "demo.tax.adr0078.v13control"}, "right": 5, "cmp": "gt"},
            "publishes": "demo.tax.adr0078.v13control-result",
            "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
        }
        DerivationSchemas().validate_declared(rule)
        copy.deepcopy(rule)  # no mutation by validation


if __name__ == "__main__":
    unittest.main()
