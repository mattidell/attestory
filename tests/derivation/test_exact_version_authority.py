"""Track 5d: the version a rule or binding names is the version that is used.

Every behaviour test goes through ``validate_package`` →
``live._resolved_run_material`` → ``marshal_run_context`` → ``run`` and
``run_reference``. Packages resolve two versions of one id together.
Declaration order is a parameter of each case, not something the answer
may depend on. A hand-built ``RunContext`` is not used.
"""

from __future__ import annotations

import unittest
from typing import Any, Callable

from packages.derivation.live import _resolved_run_material
from packages.derivation.marshal import marshal_run_context
from packages.derivation.package_validation import (
    FIELD_REF_NOT_OBJECT,
)
from tests.derivation.test_subject_declaration_live_path import (
    ADOPTION_PIN,
    GOVERNANCE_PINS,
    _Graph,
    _State,
    _both_runners,
    _currency,
    _finding,
    _lattice_type,
    _ordinary_rule,
    _package_fact_type,
    _publications,
    _resolve,
    _v11_rule,
)

SCOPE_FAMILY = "demo-student-loan"


def _entries(parts: list[tuple[dict[str, Any], str]]) -> list[dict[str, str]]:
    return [{"id": citizen["id"], "version": citizen["version"]} for citizen, _role in parts]


def _parameter(param_id: str, version: str, values: str) -> dict[str, Any]:
    return {
        "schema": "parameter-declaration.v1",
        "id": param_id,
        "version": version,
        "scope": {"tax_year": 2025, "jurisdiction": "us", "family": SCOPE_FAMILY},
        "values": values,
    }


def _with_schema(fact_id: str, version: str, value_schema: dict[str, Any]) -> dict[str, Any]:
    fact = _package_fact_type(fact_id, ["period"], version=version)
    fact["value_schema"] = value_schema
    return fact


def _order(v1: dict[str, Any], v2: dict[str, Any], *, v1_first: bool) -> list[dict[str, Any]]:
    return [v1, v2] if v1_first else [v2, v1]


def _run(
    parts: list[tuple[dict[str, Any], str]],
    findings: dict[str, dict[str, Any]] | None = None,
    lattice: dict[str, dict[str, Any]] | None = None,
    bindings: list[dict[str, Any]] | None = None,
) -> tuple[Any, Any]:
    """validate_package -> _resolved_run_material -> marshal, passing the exact index."""
    findings = findings or {}
    validation, package = _resolve(
        parts, entrypoints=_entries(parts), bindings=bindings or [],
    )
    if not validation.ok:
        raise AssertionError(f"package did not validate: {validation.issues}")
    material = _resolved_run_material(_Graph(list(validation.resolved_members), package))
    rules, parameters, families, mappings, fact_types, bound, collect_names = material
    ctx = marshal_run_context(
        run_id="demo.run.live-path",
        state=_State(findings, lattice or {}),  # type: ignore[arg-type]
        currency=_currency(list(findings)),
        rules=rules,
        parameters=parameters,
        canon={},
        adoption_pin=ADOPTION_PIN,
        governance_pins=GOVERNANCE_PINS,
        family_declarations=families,
        closure_mappings=mappings,
        fact_types=fact_types,
        input_bindings=bound,
        collect_source_names=collect_names,
        emission_only_source_names=list(material.emission_only_names),
        parameter_index=material.parameter_index,
    )
    return _both_runners(ctx)


def _codes(validation: Any) -> list[str]:
    return [issue.code for issue in validation.issues]


def _parameter_pins(finding: dict[str, Any]) -> set[tuple[str, str]]:
    return {
        (str(pin["id"]), str(pin["version"]))
        for pin in finding["pins"]
        if pin.get("role") == "parameter"
    }


def _for_both(results: tuple[Any, Any], check: Callable[[Any], None]) -> None:
    forward, backward = results
    check(forward)
    check(backward)


def _blocked(result: Any, artifact_id: str) -> list[dict[str, Any]]:
    return [
        row for row in result.dispositions
        if row.get("artifact_id") == artifact_id and row.get("disposition") == "blocked"
    ]


class ExactDefaultParameter(unittest.TestCase):
    """``optional_default`` pins parameter v1. The package also resolves v2.

    The manufactured finding's value is v1's value, and its parameter pin
    is v1 — in both declaration orders, for an ordinary rule and a
    declared-subject rule. v2's value is never published under that pin.
    """

    FACT = "demo.tax.exact.default"
    PARAM = "demo.param.exact.default"
    ECHO = "demo.tax.exact.default-echo"

    def _fact(self) -> dict[str, Any]:
        fact = _package_fact_type(self.FACT, ["period"], version="v1")
        fact["optional_default"] = {"parameter": {"id": self.PARAM, "version": "v1"}}
        return fact

    def _binding(self) -> dict[str, Any]:
        return {
            "symbol": self.FACT,
            "fact_type": {"id": self.FACT, "version": "v1"},
            "mode": "optional_default",
        }

    def _parts(self, rule: dict[str, Any], *, v1_first: bool, extra: list[tuple[dict[str, Any], str]] | None = None) -> list[tuple[dict[str, Any], str]]:
        parameters = _order(
            _parameter(self.PARAM, "v1", "from-v1"),
            _parameter(self.PARAM, "v2", "from-v2"),
            v1_first=v1_first,
        )
        parts = [(rule, "computation"), (self._fact(), "fact-type")]
        parts.extend(extra or [])
        parts.extend((parameter, "parameter") for parameter in parameters)
        return parts

    def _assert_pinned_v1(self, symbol: str, result: Any) -> None:
        published = _publications(result)
        self.assertIn(symbol, published, result.dispositions)
        self.assertEqual(published[symbol]["value"], "from-v1")
        self.assertNotEqual(published[symbol]["value"], "from-v2")
        input_pins = [
            pin for pin in published[symbol]["pins"]
            if pin.get("role") == "input" and pin.get("origin") == "declared_default"
        ]
        self.assertEqual(len(input_pins), 1, published[symbol]["pins"])
        default_finding = next(
            item.finding for item in result.publications if item.finding["id"] == input_pins[0]["id"]
        )
        self.assertEqual(default_finding["value"], "from-v1")
        self.assertEqual(_parameter_pins(default_finding), {(self.PARAM, "v1")})
        self.assertNotIn((self.PARAM, "v2"), _parameter_pins(default_finding))

    def test_ordinary_rule_both_orders(self) -> None:
        rule = _ordinary_rule(
            rule_id="demo.rule.exact.default-echo",
            publishes=self.ECHO,
            value={"op": "ref", "name": self.FACT},
            requires=[self.FACT],
        )
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                results = _run(self._parts(rule, v1_first=v1_first), bindings=[self._binding()])
                _for_both(results, lambda result: self._assert_pinned_v1(self.ECHO, result))

    def test_declared_subject_rule_both_orders(self) -> None:
        subject = "demo.tax.exact.default-subject"
        rule = _v11_rule(
            rule_id="demo.rule.exact.default-subject",
            subject={"id": subject, "version": "v1"},
            requires=[self.FACT],
            value={"op": "ref", "name": self.FACT},
            publishes="demo.tax.exact.default-subject-result",
        )
        subject_fact = f"{subject}|who=demo-who"
        findings = {"demo.finding.exact.default-subject": _finding("demo.finding.exact.default-subject", subject_fact, "x")}
        lattice = {subject: _lattice_type(subject, (("who", ("demo-who",)),))}
        symbol = f"demo.tax.exact.default-subject-result|{subject_fact}"
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                parts = self._parts(
                    rule, v1_first=v1_first,
                    extra=[(_package_fact_type(subject, ["who"]), "fact-type")],
                )
                results = _run(parts, findings, lattice, bindings=[self._binding()])
                _for_both(results, lambda result: self._assert_pinned_v1(symbol, result))


class UnavailableExactParameterDoesNotBorrow(unittest.TestCase):
    """The fact type's ``optional_default`` pins parameter v1.

    Resolving only v2 of that id is not that parameter. Admission rejects
    it, in either declaration order, for an ordinary rule and a
    declared-subject rule. Resolving v1 admits the package, and both
    runners use v1's value and pin v1.
    """

    FACT = "demo.tax.exact.missing-param"
    PARAM = "demo.param.exact.missing-param"
    SUBJECT = "demo.tax.exact.missing-param-subject"

    def _fact(self) -> dict[str, Any]:
        fact = _package_fact_type(self.FACT, ["period"], version="v1")
        fact["optional_default"] = {"parameter": {"id": self.PARAM, "version": "v1"}}
        return fact

    def _binding(self) -> dict[str, Any]:
        return {
            "symbol": self.FACT,
            "fact_type": {"id": self.FACT, "version": "v1"},
            "mode": "optional_default",
        }

    def _parts(
        self,
        parameters: list[dict[str, Any]],
        *,
        fact_first: bool,
        declared_subject: bool,
    ) -> tuple[list[tuple[dict[str, Any], str]], str]:
        fact = (self._fact(), "fact-type")
        param_parts = [(parameter, "parameter") for parameter in parameters]
        pair = [fact, *param_parts] if fact_first else [*param_parts, fact]
        if not declared_subject:
            echo = "demo.tax.exact.missing-param-echo"
            rule = _ordinary_rule(
                rule_id="demo.rule.exact.missing-param",
                publishes=echo,
                value={"op": "ref", "name": self.FACT},
                requires=[self.FACT],
            )
            return [(rule, "computation"), *pair], echo
        publishes = "demo.tax.exact.missing-param-result"
        rule = _v11_rule(
            rule_id="demo.rule.exact.missing-param-subject",
            subject={"id": self.SUBJECT, "version": "v1"},
            requires=[self.FACT],
            value={"op": "ref", "name": self.FACT},
            publishes=publishes,
        )
        symbol = f"{publishes}|{self.SUBJECT}|who=demo-who"
        return [
            (rule, "computation"),
            (_package_fact_type(self.SUBJECT, ["who"]), "fact-type"),
            *pair,
        ], symbol

    def _assert_rejected(self, parts: list[tuple[dict[str, Any], str]]) -> None:
        validation, _package = _resolve(parts, bindings=[self._binding()], entrypoints=_entries(parts))
        self.assertFalse(
            validation.ok,
            "validate_package accepted a package whose optional_default pins "
            f"parameter v1 while only a sibling version is resolved: {validation.issues}",
        )
        absent = [issue for issue in validation.issues if issue.code == "BINDING_DEFAULT_ABSENT"]
        self.assertTrue(absent, validation.issues)
        self.assertTrue(
            any(self.PARAM in issue.detail and "v1" in issue.detail for issue in absent),
            absent,
        )

    def _assert_used_v1(self, symbol: str, result: Any) -> None:
        published = _publications(result)
        self.assertIn(symbol, published, result.dispositions)
        self.assertEqual(published[symbol]["value"], "from-v1")
        self.assertNotEqual(published[symbol]["value"], "from-v2")
        input_pins = [
            pin for pin in published[symbol]["pins"]
            if pin.get("role") == "input" and pin.get("origin") == "declared_default"
        ]
        self.assertEqual(len(input_pins), 1, published[symbol]["pins"])
        default_finding = next(
            item.finding for item in result.publications if item.finding["id"] == input_pins[0]["id"]
        )
        self.assertEqual(default_finding["value"], "from-v1")
        self.assertEqual(_parameter_pins(default_finding), {(self.PARAM, "v1")})
        self.assertNotIn((self.PARAM, "v2"), _parameter_pins(default_finding))

    def _accept(self, parts: list[tuple[dict[str, Any], str]], symbol: str, *, declared_subject: bool) -> None:
        validation, _package = _resolve(parts, bindings=[self._binding()], entrypoints=_entries(parts))
        self.assertTrue(validation.ok, validation.issues)
        self.assertNotIn("BINDING_DEFAULT_ABSENT", _codes(validation))
        findings: dict[str, dict[str, Any]] = {}
        lattice: dict[str, dict[str, Any]] = {}
        if declared_subject:
            subject_fact = f"{self.SUBJECT}|who=demo-who"
            findings = {
                "demo.finding.exact.missing-subject": _finding(
                    "demo.finding.exact.missing-subject", subject_fact, "x",
                ),
            }
            lattice = {self.SUBJECT: _lattice_type(self.SUBJECT, (("who", ("demo-who",)),))}
        _for_both(
            _run(parts, findings, lattice, bindings=[self._binding()]),
            lambda result: self._assert_used_v1(symbol, result),
        )

    def test_sibling_only_rejected_ordinary_both_orders(self) -> None:
        for fact_first in (True, False):
            with self.subTest(fact_first=fact_first):
                parts, _symbol = self._parts(
                    [_parameter(self.PARAM, "v2", "from-v2")],
                    fact_first=fact_first,
                    declared_subject=False,
                )
                self._assert_rejected(parts)

    def test_sibling_only_rejected_declared_subject_both_orders(self) -> None:
        for fact_first in (True, False):
            with self.subTest(fact_first=fact_first):
                parts, _symbol = self._parts(
                    [_parameter(self.PARAM, "v2", "from-v2")],
                    fact_first=fact_first,
                    declared_subject=True,
                )
                self._assert_rejected(parts)

    def test_pinned_version_only_accepted_both_orders(self) -> None:
        parameter = [_parameter(self.PARAM, "v1", "from-v1")]
        for declared_subject in (False, True):
            for fact_first in (True, False):
                with self.subTest(declared_subject=declared_subject, fact_first=fact_first):
                    parts, symbol = self._parts(
                        parameter, fact_first=fact_first, declared_subject=declared_subject,
                    )
                    self._accept(parts, symbol, declared_subject=declared_subject)

    def test_pinned_version_beside_sibling_accepted_both_orders(self) -> None:
        for declared_subject in (False, True):
            for v1_first in (True, False):
                with self.subTest(declared_subject=declared_subject, v1_first=v1_first):
                    parameters = _order(
                        _parameter(self.PARAM, "v1", "from-v1"),
                        _parameter(self.PARAM, "v2", "from-v2"),
                        v1_first=v1_first,
                    )
                    parts, symbol = self._parts(
                        parameters, fact_first=True, declared_subject=declared_subject,
                    )
                    self._accept(parts, symbol, declared_subject=declared_subject)


class EmptyCoverageUsesThePinnedParameter(unittest.TestCase):
    """No links. ``link_coverage``'s empty parameter pins v1; v2 is also resolved.

    Both orders publish v1's value and pin v1. The pinned version is not
    blocked merely because the other declaration would have won an id map.
    """

    PARAM = "demo.param.exact.coverage"
    LINKS = "demo.tax.exact.coverage-link"
    REDUCTIONS = "demo.tax.exact.coverage-reduction"
    SUBJECT = "demo.tax.exact.coverage-subject"
    PUBLISHES = "demo.tax.exact.coverage-result"

    def _parts(self, *, v1_first: bool) -> tuple[list[tuple[dict[str, Any], str]], str]:
        subject_fact = f"{self.SUBJECT}|who=demo-who"
        rule = _v11_rule(
            rule_id="demo.rule.exact.coverage",
            subject={"id": self.SUBJECT, "version": "v1"},
            joined={"id": self.LINKS, "version": "v1"},
            direction="joined_contains_subject",
            value={
                "op": "link_coverage",
                "links": self.LINKS,
                "reductions": self.REDUCTIONS,
                "empty": {"parameter": {"id": self.PARAM, "version": "v1"}},
            },
            publishes=self.PUBLISHES,
        )
        reduction = _ordinary_rule(
            rule_id="demo.rule.exact.coverage-reduction",
            publishes=self.REDUCTIONS,
            value=0,
        )
        parameters = _order(
            _parameter(self.PARAM, "v1", "10"),
            _parameter(self.PARAM, "v2", "99"),
            v1_first=v1_first,
        )
        parts = [
            (rule, "computation"),
            (reduction, "computation"),
            (_package_fact_type(self.SUBJECT, ["who"]), "fact-type"),
            (_package_fact_type(self.LINKS, ["who"]), "fact-type"),
        ]
        parts.extend((parameter, "parameter") for parameter in parameters)
        return parts, f"{self.PUBLISHES}|{subject_fact}"

    def test_both_orders_publish_v1_and_pin_v1(self) -> None:
        subject_fact = f"{self.SUBJECT}|who=demo-who"
        findings = {
            "demo.finding.exact.coverage-subject": _finding(
                "demo.finding.exact.coverage-subject", subject_fact, "x",
            ),
        }
        lattice = {self.SUBJECT: _lattice_type(self.SUBJECT, (("who", ("demo-who",)),))}
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                parts, symbol = self._parts(v1_first=v1_first)

                def check(result: Any) -> None:
                    published = _publications(result)
                    self.assertIn(symbol, published, result.dispositions)
                    self.assertEqual(published[symbol]["value"], "10")
                    self.assertNotEqual(published[symbol]["value"], "99")
                    self.assertIn((self.PARAM, "v1"), _parameter_pins(published[symbol]))
                    self.assertNotIn((self.PARAM, "v2"), _parameter_pins(published[symbol]))

                _for_both(_run(parts, findings, lattice), check)


class CategoricalDomainsAreExactVersions(unittest.TestCase):
    """Two versions of one fact type are two domains.

    A binding pins v1. A ``category_literal`` pins its own version. Comparing
    v1 with v2 is a domain mismatch, not an equality. A value valid only at
    the pinned version is not rejected because the other version was declared
    last, and a literal whose version has no enum does not borrow the sibling.
    """

    FACT = "demo.tax.exact.domain"
    ECHO = "demo.tax.exact.domain-echo"

    def _facts(self, *, v1_first: bool, v2_enum: list[str] | None) -> list[dict[str, Any]]:
        v1 = _with_schema(self.FACT, "v1", {"type": "string", "enum": ["a", "b"]})
        if v2_enum is None:
            v2 = _with_schema(self.FACT, "v2", {"type": "string"})
        else:
            v2 = _with_schema(self.FACT, "v2", {"type": "string", "enum": v2_enum})
        return _order(v1, v2, v1_first=v1_first)

    def _rule(self, value: Any, *, when: Any = True) -> dict[str, Any]:
        rule = _ordinary_rule(
            rule_id="demo.rule.exact.domain",
            publishes=self.ECHO,
            value=value,
            requires=[self.FACT],
        )
        rule["when"] = when
        return rule

    def _binding(self, version: str = "v1") -> dict[str, Any]:
        return {
            "symbol": self.FACT,
            "fact_type": {"id": self.FACT, "version": version},
            "mode": "required",
        }

    def _finding(self, value: str) -> dict[str, dict[str, Any]]:
        return {
            "demo.finding.exact.domain": _finding(
                "demo.finding.exact.domain", f"{self.FACT}|period=demo", value,
            ),
        }

    def test_pinned_input_matches_its_own_literal_both_orders(self) -> None:
        compare = {
            "op": "categorical_compare",
            "cmp": "eq",
            "left": {"op": "ref", "name": self.FACT},
            "right": {
                "op": "category_literal",
                "fact_type": {"id": self.FACT, "version": "v1"},
                "value": "a",
            },
        }
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                parts = [(self._rule(compare), "computation")]
                parts.extend((fact, "fact-type") for fact in self._facts(v1_first=v1_first, v2_enum=["x", "y"]))

                def check(result: Any) -> None:
                    published = _publications(result)
                    self.assertIn(self.ECHO, published, result.dispositions)
                    self.assertEqual(published[self.ECHO]["value"], "true")
                    input_ids = {pin["id"] for pin in published[self.ECHO]["pins"] if pin.get("role") == "input"}
                    self.assertEqual(input_ids, {"demo.finding.exact.domain"})

                _for_both(_run(parts, self._finding("a"), bindings=[self._binding()]), check)

    def test_two_versions_of_one_id_do_not_compare_equal(self) -> None:
        compare = {
            "op": "categorical_compare",
            "cmp": "eq",
            "left": {
                "op": "category_literal",
                "fact_type": {"id": self.FACT, "version": "v1"},
                "value": "yes",
            },
            "right": {
                "op": "category_literal",
                "fact_type": {"id": self.FACT, "version": "v2"},
                "value": "yes",
            },
        }
        rule = _ordinary_rule(
            rule_id="demo.rule.exact.domain-mismatch",
            publishes=self.ECHO,
            value=compare,
        )
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                v1 = _with_schema(self.FACT, "v1", {"type": "string", "enum": ["yes", "no"]})
                v2 = _with_schema(self.FACT, "v2", {"type": "string", "enum": ["yes", "x"]})
                parts = [(rule, "computation")] + [(fact, "fact-type") for fact in _order(v1, v2, v1_first=v1_first)]

                def check(result: Any) -> None:
                    self.assertNotIn(self.ECHO, _publications(result))
                    blocked = _blocked(result, rule["id"])
                    self.assertTrue(blocked, result.dispositions)
                    self.assertTrue(
                        all(row.get("code") == "CATEGORICAL_DOMAIN_MISMATCH" for row in blocked),
                        blocked,
                    )

                _for_both(_run(parts), check)

    def test_literal_does_not_borrow_a_sibling_enum(self) -> None:
        compare = {
            "op": "categorical_compare",
            "cmp": "eq",
            "left": {
                "op": "category_literal",
                "fact_type": {"id": self.FACT, "version": "v2"},
                "value": "a",
            },
            "right": {
                "op": "category_literal",
                "fact_type": {"id": self.FACT, "version": "v2"},
                "value": "a",
            },
        }
        rule = _ordinary_rule(
            rule_id="demo.rule.exact.domain-sibling",
            publishes=self.ECHO,
            value=compare,
        )
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                parts = [(rule, "computation")]
                parts.extend((fact, "fact-type") for fact in self._facts(v1_first=v1_first, v2_enum=None))

                def check(result: Any) -> None:
                    self.assertNotIn(self.ECHO, _publications(result))
                    self.assertNotIn("true", [item.finding["value"] for item in result.publications])
                    blocked = _blocked(result, rule["id"])
                    self.assertTrue(blocked, result.dispositions)

                _for_both(_run(parts), check)

    def test_collect_rows_use_the_literal_version(self) -> None:
        value = {
            "op": "collect_categorical_all_equal",
            "name": self.FACT,
            "value": {
                "op": "category_literal",
                "fact_type": {"id": self.FACT, "version": "v1"},
                "value": "a",
            },
        }
        rule = _ordinary_rule(
            rule_id="demo.rule.exact.domain-collect",
            publishes=self.ECHO,
            value=value,
        )
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                parts = [(rule, "computation")]
                parts.extend((fact, "fact-type") for fact in self._facts(v1_first=v1_first, v2_enum=["x", "y"]))

                def check(result: Any) -> None:
                    published = _publications(result)
                    self.assertEqual(published[self.ECHO]["value"], "true", result.dispositions)

                _for_both(_run(parts, self._finding("a")), check)

    def test_optional_default_symbol_carries_the_binding_version(self) -> None:
        fact_v1 = _with_schema(self.FACT, "v1", {"type": "string", "enum": ["a", "b"]})
        fact_v1["optional_default"] = {"parameter": {"id": "demo.param.exact.domain-default", "version": "v1"}}
        fact_v2 = _with_schema(self.FACT, "v2", {"type": "string", "enum": ["x", "y"]})
        compare = {
            "op": "categorical_compare",
            "cmp": "eq",
            "left": {"op": "ref", "name": self.FACT},
            "right": {
                "op": "category_literal",
                "fact_type": {"id": self.FACT, "version": "v1"},
                "value": "a",
            },
        }
        rule = self._rule(compare)
        binding = {
            "symbol": self.FACT,
            "fact_type": {"id": self.FACT, "version": "v1"},
            "mode": "optional_default",
        }
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                parts = [(rule, "computation")]
                parts.extend((fact, "fact-type") for fact in _order(fact_v1, fact_v2, v1_first=v1_first))
                parts.append((_parameter("demo.param.exact.domain-default", "v1", "a"), "parameter"))

                def check(result: Any) -> None:
                    published = _publications(result)
                    self.assertEqual(published[self.ECHO]["value"], "true", result.dispositions)

                _for_both(_run(parts, bindings=[binding]), check)


class ValidationUsesThePinnedFactTypeVersion(unittest.TestCase):
    """Reviewer's case: v1 is a scalar, v2 is an object with ``amount``.

    A binding that pins v2 is accepted in both declaration orders, and the
    live path reads ``amount``. A binding that pins v1 is rejected in both
    orders. The yes/no check uses the same pin, not the collapsed id.
    """

    FACT = "demo.tax.exact.field"
    ECHO = "demo.tax.exact.field-echo"

    def _facts(self, *, v1_first: bool) -> list[dict[str, Any]]:
        scalar = _with_schema(self.FACT, "v1", {"type": "number"})
        object_type = _with_schema(
            self.FACT, "v2",
            {"type": "object", "properties": {"amount": {"type": "string"}}},
        )
        return _order(scalar, object_type, v1_first=v1_first)

    def _field_rule(self) -> dict[str, Any]:
        rule = _ordinary_rule(
            rule_id="demo.rule.exact.field",
            publishes=self.ECHO,
            value={"op": "ref", "name": self.FACT, "field": "amount"},
            requires=[self.FACT],
        )
        rule["schema"] = "rule-artifact.v7"
        return rule

    def _binding(self, version: str) -> dict[str, Any]:
        return {
            "symbol": self.FACT,
            "fact_type": {"id": self.FACT, "version": version},
            "mode": "required",
        }

    def test_binding_pinned_to_v2_is_accepted_and_reads_amount(self) -> None:
        rule = self._field_rule()
        findings = {
            "demo.finding.exact.field": _finding(
                "demo.finding.exact.field", f"{self.FACT}|period=demo", {"amount": "10"},
            ),
        }
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                parts = [(rule, "computation")] + [(fact, "fact-type") for fact in self._facts(v1_first=v1_first)]

                def check(result: Any) -> None:
                    published = _publications(result)
                    self.assertEqual(published[self.ECHO]["value"], "10", result.dispositions)
                    input_ids = {pin["id"] for pin in published[self.ECHO]["pins"] if pin.get("role") == "input"}
                    self.assertEqual(input_ids, {"demo.finding.exact.field"})

                _for_both(_run(parts, findings, bindings=[self._binding("v2")]), check)

    def test_binding_pinned_to_v1_scalar_is_rejected_both_orders(self) -> None:
        rule = self._field_rule()
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                parts = [(rule, "computation")] + [(fact, "fact-type") for fact in self._facts(v1_first=v1_first)]
                validation, _package = _resolve(
                    parts, bindings=[self._binding("v1")], entrypoints=_entries(parts),
                )
                self.assertFalse(validation.ok, validation.issues)
                self.assertIn(FIELD_REF_NOT_OBJECT, _codes(validation))

    def test_yes_no_check_uses_the_binding_version(self) -> None:
        member = "demo.tax.exact.yesno"
        rule = _ordinary_rule(
            rule_id="demo.rule.exact.yesno",
            publishes="demo.tax.exact.yesno-echo",
            requires=[member],
            value={"op": "ref", "name": member},
        )
        rule["when"] = {
            "op": "conditional_dependency_set",
            "condition": {
                "op": "categorical_compare",
                "cmp": "eq",
                "left": {"op": "ref", "name": member},
                "right": {
                    "op": "category_literal",
                    "fact_type": {"id": member, "version": "v2"},
                    "value": "yes",
                },
            },
            "members": [{"op": "ref", "name": member}],
        }
        open_string = _with_schema(member, "v1", {"type": "string"})
        yes_no = _with_schema(member, "v2", {"type": "string", "enum": ["yes", "no"]})
        findings = {
            "demo.finding.exact.yesno": _finding(
                "demo.finding.exact.yesno", f"{member}|period=demo", "yes",
            ),
        }
        for v1_first in (True, False):
            with self.subTest(pinned="v2", v1_first=v1_first):
                parts = [(rule, "computation")] + [
                    (fact, "fact-type") for fact in _order(open_string, yes_no, v1_first=v1_first)
                ]
                binding = {
                    "symbol": member,
                    "fact_type": {"id": member, "version": "v2"},
                    "mode": "required",
                }

                def check(result: Any) -> None:
                    published = _publications(result)
                    self.assertEqual(published[rule["publishes"]]["value"], "yes", result.dispositions)

                _for_both(_run(parts, findings, bindings=[binding]), check)
        for v1_first in (True, False):
            with self.subTest(pinned="v1", v1_first=v1_first):
                parts = [(rule, "computation")] + [
                    (fact, "fact-type") for fact in _order(open_string, yes_no, v1_first=v1_first)
                ]
                validation, _package = _resolve(
                    parts,
                    bindings=[{
                        "symbol": member,
                        "fact_type": {"id": member, "version": "v1"},
                        "mode": "required",
                    }],
                    entrypoints=_entries(parts),
                )
                self.assertFalse(validation.ok, validation.issues)
                self.assertIn("CONDITIONAL_DEPENDENCY_MEMBER_NOT_YES_NO", _codes(validation))


class ZeroSubjectRecordsNothing(unittest.TestCase):
    """A declared-subject rule with no current subject finding records nothing.

    No publication and no disposition. A downstream rule that requires the
    published symbol blocks ``DEPENDENCY_ABSENT`` rather than treating the
    silence as a value. The same package with subject findings executes once
    per finding. No new disposition is introduced.
    """

    SUBJECT = "demo.tax.exact.zero-subject"
    PUBLISHES = "demo.tax.exact.zero-result"
    DOWNSTREAM = "demo.tax.exact.zero-downstream"

    def _parts(self) -> list[tuple[dict[str, Any], str]]:
        subject_rule = _v11_rule(
            rule_id="demo.rule.exact.zero-subject",
            subject={"id": self.SUBJECT, "version": "v1"},
            value="executed",
            publishes=self.PUBLISHES,
        )
        downstream = _ordinary_rule(
            rule_id="demo.rule.exact.zero-downstream",
            publishes=self.DOWNSTREAM,
            value={"op": "ref", "name": self.PUBLISHES},
            requires=[self.PUBLISHES],
        )
        return [
            (subject_rule, "computation"),
            (downstream, "computation"),
            (_package_fact_type(self.SUBJECT, ["who"]), "fact-type"),
        ]

    def test_no_finding_publishes_nothing_and_the_consumer_blocks(self) -> None:
        def check(result: Any) -> None:
            self.assertEqual(result.publications, [])
            subject_rows = [
                row for row in result.dispositions
                if row.get("artifact_id") == "demo.rule.exact.zero-subject"
            ]
            self.assertEqual(subject_rows, [])
            blocked = _blocked(result, "demo.rule.exact.zero-downstream")
            self.assertTrue(blocked, result.dispositions)
            self.assertTrue(all(row.get("code") == "DEPENDENCY_ABSENT" for row in blocked), blocked)
            self.assertTrue(
                all(self.PUBLISHES in row.get("missing", []) for row in blocked),
                blocked,
            )

        _for_both(_run(self._parts()), check)

    def test_each_current_subject_reaches_execution(self) -> None:
        lattice = {self.SUBJECT: _lattice_type(self.SUBJECT, (("who", ("a", "b")),))}
        fact_a = f"{self.SUBJECT}|who=a"
        fact_b = f"{self.SUBJECT}|who=b"
        findings = {
            "demo.finding.exact.zero.a": _finding("demo.finding.exact.zero.a", fact_a, "a"),
            "demo.finding.exact.zero.b": _finding("demo.finding.exact.zero.b", fact_b, "b"),
        }

        def check(result: Any) -> None:
            published = _publications(result)
            self.assertEqual(published[f"{self.PUBLISHES}|{fact_a}"]["value"], "executed")
            self.assertEqual(published[f"{self.PUBLISHES}|{fact_b}"]["value"], "executed")
            published_rows = [
                row for row in result.dispositions
                if row.get("artifact_id") == "demo.rule.exact.zero-subject"
                and row.get("disposition") == "published"
            ]
            self.assertEqual(len(published_rows), 2, result.dispositions)

        _for_both(_run(self._parts(), findings, lattice), check)


class DerivedCategoricalFallback(unittest.TestCase):
    """Stage 2 choice C1, with the stage-1 block when several versions exist.

    A derived finding carries no fact type. One resolved version of an id
    equal to the symbol name keeps today's symbol-name fallback. Several
    versions block rather than taking whichever declaration was last.
    """

    FACT = "demo.tax.exact.derived"
    PRODUCER = "demo.rule.exact.derived-producer"
    CONSUMER = "demo.rule.exact.derived-consumer"

    def _parts(self, enums: list[tuple[str, list[str]]], *, v1_first: bool) -> list[tuple[dict[str, Any], str]]:
        producer = _ordinary_rule(
            rule_id=self.PRODUCER,
            publishes=self.FACT,
            value={
                "op": "category_literal",
                "fact_type": {"id": self.FACT, "version": "v1"},
                "value": "yes",
            },
        )
        consumer = _ordinary_rule(
            rule_id=self.CONSUMER,
            publishes="demo.tax.exact.derived-echo",
            requires=[self.FACT],
            value={
                "op": "categorical_compare",
                "cmp": "eq",
                "left": {"op": "ref", "name": self.FACT},
                "right": {
                    "op": "category_literal",
                    "fact_type": {"id": self.FACT, "version": "v1"},
                    "value": "yes",
                },
            },
        )
        facts = [
            _with_schema(self.FACT, version, {"type": "string", "enum": enum})
            for version, enum in enums
        ]
        if not v1_first:
            facts.reverse()
        return [(producer, "computation"), (consumer, "computation")] + [
            (fact, "fact-type") for fact in facts
        ]

    def test_one_version_keeps_the_symbol_name_fallback(self) -> None:
        parts = self._parts([("v1", ["yes", "no"])], v1_first=True)

        def check(result: Any) -> None:
            published = _publications(result)
            producer = published[self.FACT]
            self.assertEqual(producer["value"], "yes")
            self.assertNotIn("fact_type", producer)
            consumer = published["demo.tax.exact.derived-echo"]
            self.assertEqual(consumer["value"], "true")
            input_ids = {pin["id"] for pin in consumer["pins"] if pin.get("role") == "input"}
            self.assertEqual(input_ids, {producer["id"]})

        _for_both(_run(parts), check)

    def test_several_versions_block_instead_of_taking_the_last(self) -> None:
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                parts = self._parts(
                    [("v1", ["yes", "no"]), ("v2", ["yes", "x"])],
                    v1_first=v1_first,
                )

                def check(result: Any) -> None:
                    published = _publications(result)
                    self.assertIn(self.FACT, published, result.dispositions)
                    self.assertNotIn("fact_type", published[self.FACT])
                    self.assertNotIn("demo.tax.exact.derived-echo", published)
                    blocked = _blocked(result, self.CONSUMER)
                    self.assertTrue(blocked, result.dispositions)
                    self.assertTrue(
                        all(row.get("code") == "CATEGORICAL_DOMAIN_MISMATCH" for row in blocked),
                        blocked,
                    )

                _for_both(_run(parts), check)


class UnversionedParameterReference(unittest.TestCase):
    """Stage 2 choice C2. The ``parameter`` op names no version.

    One resolved version is still that version's value and pin. Two versions
    block at runtime. The run does not select one.
    """

    PARAM = "demo.param.exact.unversioned"
    ECHO = "demo.tax.exact.unversioned-echo"

    def _rule(self) -> dict[str, Any]:
        return _ordinary_rule(
            rule_id="demo.rule.exact.unversioned",
            publishes=self.ECHO,
            value={"op": "parameter", "parameter_id": self.PARAM},
        )

    def test_one_version_is_used_and_pinned(self) -> None:
        parts = [
            (self._rule(), "computation"),
            (_parameter(self.PARAM, "v1", "1"), "parameter"),
        ]

        def check(result: Any) -> None:
            published = _publications(result)
            self.assertEqual(published[self.ECHO]["value"], "1", result.dispositions)
            self.assertEqual(_parameter_pins(published[self.ECHO]), {(self.PARAM, "v1")})

        _for_both(_run(parts), check)

    def test_two_versions_block_rather_than_select(self) -> None:
        rule = self._rule()
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                parameters = _order(
                    _parameter(self.PARAM, "v1", "1"),
                    _parameter(self.PARAM, "v2", "2"),
                    v1_first=v1_first,
                )
                parts = [(rule, "computation")] + [(parameter, "parameter") for parameter in parameters]

                def check(result: Any) -> None:
                    published = _publications(result)
                    self.assertNotIn(self.ECHO, published)
                    values = [item.finding["value"] for item in result.publications]
                    self.assertNotIn("1", values)
                    self.assertNotIn("2", values)
                    blocked = _blocked(result, rule["id"])
                    self.assertTrue(blocked, result.dispositions)
                    self.assertTrue(
                        all(row.get("code") == "DEPENDENCY_INVALID" for row in blocked),
                        blocked,
                    )
                    self.assertTrue(all(self.PARAM in row.get("missing", []) for row in blocked), blocked)

                _for_both(_run(parts), check)


class AttachmentThresholdUsesThePinnedParameter(unittest.TestCase):
    """The attachment requirement names ``threshold_parameter`` by version.

    v1 is 10 and v2 is 1000. A subtotal of 50 is over v1 and not over v2, so
    the disposition shows which value was used. The pin on that disposition
    is v1. Resolving only the sibling is rejected at admission. The id-keyed
    parameter map contains only parameter citizens.
    """

    PARAM = "demo.param.exact.attach-threshold"
    SUBTOTAL = "demo.tax.exact.attach-subtotal"
    ANSWER = "demo.tax.exact.attach-answer"
    ANSWER_TYPE = "demo.tax.exact.attach-answer-type"
    RULE = "demo.rule.exact.attach"

    def _attachment(self) -> dict[str, Any]:
        return {
            "schema": "attachment-rule.v1",
            "id": self.RULE,
            "version": "v1",
            "title": "Demo exact threshold attachment",
            "scope": {"tax_year": 2025, "jurisdiction": "us", "family": SCOPE_FAMILY},
            "attachment": {
                "authority": "demo",
                "form_id": "demo-schx",
                "tax_year": 2025,
                "jurisdiction": "us",
            },
            "publishes": "demo.tax.exact.attach-disposition",
            "requirement": {
                "subtotals": [self.SUBTOTAL],
                "threshold_parameter": {"id": self.PARAM, "version": "v1"},
                "comparison": "strictly_greater_than",
                "citation": {"id": "demo.citation.exact.attach", "version": "v1"},
            },
            "itemizations": [],
            "completeness": {
                "required_answers": [{
                    "symbol": self.ANSWER,
                    "fact_type": {"id": self.ANSWER_TYPE, "version": "v1"},
                    "check": "presence",
                }],
            },
        }

    def _citation(self) -> dict[str, Any]:
        return {
            "schema": "citation.v1",
            "id": "demo.citation.exact.attach",
            "version": "v1",
            "authority": {"family": "irs-publication", "publication": "demo-970", "revision": "2025"},
        }

    def _answer_type(self) -> dict[str, Any]:
        return _with_schema(self.ANSWER_TYPE, "v1", {"enum": ["yes", "no"]})

    def _parts(
        self,
        parameters: list[dict[str, Any]],
        *,
        parameter_first: bool = False,
    ) -> list[tuple[dict[str, Any], str]]:
        subtotal = _ordinary_rule(
            rule_id="demo.rule.exact.attach-subtotal",
            publishes=self.SUBTOTAL,
            value="50",
        )
        parts: list[tuple[dict[str, Any], str]] = [
            (subtotal, "computation"),
            (self._attachment(), "attachment-rule"),
            (self._answer_type(), "fact-type"),
            (self._citation(), "citation"),
        ]
        param_parts = [(parameter, "parameter") for parameter in parameters]
        if parameter_first:
            return param_parts + parts
        parts.extend(param_parts)
        return parts

    def _assert_parameters_are_citizens(
        self, parts: list[tuple[dict[str, Any], str]], versions: set[str],
    ) -> None:
        validation, package = _resolve(parts, entrypoints=_entries(parts))
        self.assertTrue(validation.ok, validation.issues)
        material = _resolved_run_material(_Graph(list(validation.resolved_members), package))
        parameters = material[1]
        self.assertNotIn("\x00", parameters)
        for citizen in parameters.values():
            self.assertEqual(citizen.get("schema"), "parameter-declaration.v1")
            self.assertIn("values", citizen)
            self.assertIn("version", citizen)
        self.assertEqual(set(material.parameter_index[self.PARAM]), versions)
        if len(versions) > 1:
            self.assertNotIn(self.PARAM, parameters)
        else:
            self.assertEqual(parameters[self.PARAM]["version"], next(iter(versions)))

    def test_both_orders_use_v1_and_pin_v1(self) -> None:
        for v1_first in (True, False):
            with self.subTest(v1_first=v1_first):
                parameters = _order(
                    _parameter(self.PARAM, "v1", "10"),
                    _parameter(self.PARAM, "v2", "1000"),
                    v1_first=v1_first,
                )
                parts = self._parts(parameters)

                _for_both(_run(parts), self._assert_required_on_v1)
                self._assert_parameters_are_citizens(parts, {"v1", "v2"})

    def _assert_required_on_v1(self, result: Any) -> None:
        rows = [
            row for row in result.dispositions
            if row.get("artifact_id") == self.RULE
        ]
        self.assertEqual(len(rows), 1, result.dispositions)
        row = rows[0]
        # 50 is over v1's 10, so the attachment is required and then
        # blocks on the absent answer. v2's 1000 would have made it
        # inapplicable. The pin is the version that was named.
        self.assertEqual(row.get("disposition"), "blocked", row)
        self.assertEqual(row.get("code"), "DEPENDENCY_ABSENT")
        self.assertEqual(row.get("missing"), [self.ANSWER])
        pins = {
            (pin["id"], pin["version"])
            for pin in row["pins"]
            if pin.get("role") == "parameter"
        }
        self.assertEqual(pins, {(self.PARAM, "v1")})

    def test_sibling_only_is_rejected_in_both_declaration_orders(self) -> None:
        for parameter_first in (True, False):
            with self.subTest(parameter_first=parameter_first):
                parts = self._parts(
                    [_parameter(self.PARAM, "v2", "1000")],
                    parameter_first=parameter_first,
                )
                validation, _package = _resolve(parts, entrypoints=_entries(parts))
                self.assertFalse(
                    validation.ok,
                    "validate_package accepted an attachment whose threshold_parameter "
                    f"pins v1 while only v2 is resolved: {validation.issues}",
                )
                absent = [
                    issue for issue in validation.issues
                    if issue.code == "ATTACHMENT_TRIGGER_PARAMETER_ABSENT"
                ]
                self.assertTrue(absent, validation.issues)
                self.assertTrue(
                    any(self.PARAM in issue.detail and "v1" in issue.detail for issue in absent),
                    absent,
                )

    def test_pinned_version_only_is_used_in_both_declaration_orders(self) -> None:
        for parameter_first in (True, False):
            with self.subTest(parameter_first=parameter_first):
                parts = self._parts(
                    [_parameter(self.PARAM, "v1", "10")],
                    parameter_first=parameter_first,
                )
                validation, _package = _resolve(parts, entrypoints=_entries(parts))
                self.assertTrue(validation.ok, validation.issues)
                self.assertNotIn("ATTACHMENT_TRIGGER_PARAMETER_ABSENT", _codes(validation))
                _for_both(_run(parts), self._assert_required_on_v1)


if __name__ == "__main__":
    unittest.main()
