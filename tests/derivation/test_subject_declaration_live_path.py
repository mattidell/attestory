"""Track 5c: the declaration-to-execution path, not just the dispatcher.

Track 5a/5b's own test files (``test_subject_relationship_declarations.py``,
``test_per_subject_scheduling.py``, ``test_relationship_presence.py``) prove
the dispatcher is correct once a caller hands it ``RunContext.sources`` and
``fact_types`` directly. They never prove a declared subject/relationship
*reaches* that dispatcher through the real live path. This file tests that
seam: every scenario here goes through ``validate_package`` (a real
``artifact-package.v32`` package), ``live._resolved_run_material`` on the
validated members, and ``marshal_run_context`` over a kernel state that
carries a real fact lattice (``packages.kernel.facts.KernelState`` /
``facts_of``, the same shape ``tests/derivation/test_subject_dispatch.py``
uses) -- never a hand-populated ``RunContext.sources`` or ``fact_types``.
``run`` and ``run_reference`` are both exercised and must agree.

Three defects an independent review reproduced at ``6ca54a8d``:

1. ``_resolved_run_material`` did not load standalone ``fact-type.v2``
   members, and did not add a v11 rule's ``subject``/``joined`` types to the
   emission-only names -- a validated subject-only rule reached both
   schedulers with zero sources.
2. ``_identity_names`` matched a reference fact type by id only, ignoring
   the exact pinned version -- a stale, weaker declaration of the same id
   silently governed the presence check.
3. A declared ``joined`` type with zero source rows fell through to
   ``run.symbol_pin``/``run.symbols`` -- an unrelated run-wide scalar
   published under the same symbol name was read as if it were the joined
   row's own value.

Each defect's test is written to fail against the pre-fix code; the build
report records that confirmation.
"""

from __future__ import annotations

import unittest
from typing import Any

from packages.derivation.live import _resolved_run_material
from packages.derivation.loader import DerivationSchemas
from packages.derivation.marshal import marshal_run_context
from packages.derivation.package_validation import (
    package_instance_checksum,
    validate_package,
)
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import RunContext, run
from packages.kernel.currency import CurrencyView
from packages.kernel.facts import KernelState

SCOPE = {"tax_year": 2025, "jurisdiction": "us", "family": "demo-student-loan"}
ADOPTION_PIN = {"role": "adoption", "id": "demo.package.live-path", "version": "v1"}
GOVERNANCE_PINS = [{"role": "governance", "id": "demo.governance.live-path", "version": "v1"}]


# ---------------------------------------------------------------------------
# Kernel-state fixtures (the fact lattice), same shape as
# tests/derivation/test_subject_dispatch.py.
# ---------------------------------------------------------------------------


class _HorizonState:
    def __init__(self) -> None:
        self.current_by_chain: dict[tuple[str, str, str], str] = {}


class _State:
    def __init__(
        self, findings: dict[str, dict[str, Any]], lattice: dict[str, dict[str, Any]]
    ) -> None:
        self.findings = findings
        self.horizon_state = _HorizonState()
        self.fact_state = KernelState(fact_types=lattice)


def _finding(fid: str, fact_id: str, value: Any) -> dict[str, Any]:
    return {"id": fid, "fact_id": fact_id, "value": value, "basis": "attested"}


def _currency(finding_ids: list[str]) -> CurrencyView:
    ids = frozenset(finding_ids)
    return CurrencyView(
        current_finding_ids=ids,
        displaced_finding_ids=frozenset(),
        current_evidence_ids=frozenset(),
        displaced_evidence_ids=frozenset(),
    )


def _lattice_type(
    type_id: str, keys: tuple[tuple[str, tuple[str, ...]], ...]
) -> dict[str, Any]:
    """A ``KernelState.fact_types`` entry: real identity for ``facts_of``.

    Independent of the *package-declared* ``fact-type.v2`` citizen below --
    exactly as production separates the kernel's own bundle-adopted lattice
    from a package's declared identity metadata. Each key's ``values`` tuple
    is the cartesian factor ``facts_of`` multiplies out; a single-value tuple
    holds a key fixed while another key with several values produces one
    fact per value.
    """
    return {
        "id": type_id,
        "nature": "record",
        "identity_keys": [
            {"name": name, "kind": "literal", "values": list(values)}
            for name, values in keys
        ],
    }


# ---------------------------------------------------------------------------
# Package-level fixtures: the real validate_package -> _resolved_run_material
# -> marshal_run_context chain.
# ---------------------------------------------------------------------------


def _package_fact_type(fact_id: str, key_names: list[str], *, version: str = "v1") -> dict[str, Any]:
    """A ``fact-type.v2`` package citizen whose identity is exactly ``key_names``.

    Only the names matter to containment/presence; values are placeholders,
    the same shape ``test_subject_relationship_declarations._fact_type`` and
    ``test_relationship_presence._fact_type`` use.
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
    requires: list[str] | None = None,
    value: Any,
    publishes: str,
    when: Any = True,
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
        "when": when,
        "value": value,
        "publishes": publishes,
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
    }
    if joined is not None:
        rule["joined"] = dict(joined)
    if direction is not None:
        rule["direction"] = direction
    return rule


def _ordinary_rule(
    *, rule_id: str, publishes: str, value: Any, requires: list[str] | None = None, version: str = "v1"
) -> dict[str, Any]:
    """A v1-v10-shaped predecessor: no ``subject``, evaluated once, unsuffixed."""
    return {
        "schema": "rule-artifact.v6",
        "id": rule_id,
        "version": version,
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": list(requires or []),
        "pins": [],
        "when": True,
        "value": value,
        "publishes": publishes,
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
    }


def _package(
    parts: list[tuple[dict[str, Any], str]],
    *,
    bindings: list[dict[str, Any]] | None = None,
    entrypoints: list[dict[str, str]] | None = None,
    schema: str = "artifact-package.v32",
    package_id: str = "demo.package.live-path",
    version: str = "v1",
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema": schema,
        "id": package_id,
        "version": version,
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


class _Graph:
    """The two fields ``_resolved_run_material`` reads off a resolved graph.

    Same shape as ``production_resolver.ResolvedGraph`` and the ``_Graph``
    test shim ``test_link_coverage_contract.py``/``test_subject_relationship_
    declarations.py`` already use -- built here from ``validate_package``'s
    own ``resolved_members``, not a hand-assembled member list.
    """

    def __init__(self, resolved_members: Any, package: dict[str, Any]) -> None:
        self.resolved_members = resolved_members
        self.package = package


def _resolve(
    parts: list[tuple[dict[str, Any], str]], **kwargs: Any
) -> tuple[Any, dict[str, Any]]:
    package = _package(parts, **kwargs)
    corpus = {(citizen["id"], citizen["version"]): citizen for citizen, _role in parts}
    validation = validate_package(package, corpus, DerivationSchemas())
    return validation, package


def _live_context(
    parts: list[tuple[dict[str, Any], str]],
    findings: dict[str, dict[str, Any]],
    lattice: dict[str, dict[str, Any]],
    **kwargs: Any,
) -> tuple[Any, RunContext]:
    """The real chain: validate_package -> _resolved_run_material -> marshal.

    Returns the resolved-material tuple (so a test can assert on
    ``emission_only_names``/``fact_types`` directly) and the marshalled
    ``RunContext`` ``run``/``run_reference`` execute.
    """
    validation, package = _resolve(parts, **kwargs)
    if not validation.ok:
        raise AssertionError(f"package did not validate: {validation.issues}")
    graph = _Graph(list(validation.resolved_members), package)
    material = _resolved_run_material(graph)
    rules, parameters, families, mappings, fact_types, bindings, collect_names = material
    ctx = marshal_run_context(
        run_id="demo.run.live-path",
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
    return material, ctx


def _both_runners(ctx: RunContext) -> tuple[Any, Any]:
    schemas = DerivationSchemas()
    return run(ctx, schemas), run_reference(ctx, schemas)


def _publications(result: Any) -> dict[str, dict[str, Any]]:
    return {p.finding["symbol"]: p.finding for p in result.publications}


def _blocked_rows(result: Any, symbol: str) -> list[dict[str, Any]]:
    return [row for row in result.dispositions if row.get("symbol") == symbol]


def _input_ids(pins: list[dict[str, Any]]) -> set[str]:
    return {str(pin["id"]) for pin in pins if pin.get("role") == "input"}


# ---------------------------------------------------------------------------
# Defect 1: declared subjects/relationships do not reach live execution.
# ---------------------------------------------------------------------------


STATEMENT = "demo.tax.livepath.statement"
CONFIRMED = "demo.tax.livepath.confirmed"


class SubjectOnlyRuleStandaloneFactTypes(unittest.TestCase):
    """A subject-only v11 rule over a standalone ``fact-type.v2`` (no bundle)."""

    def _fixture(self) -> tuple[list[tuple[dict[str, Any], str]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
        lattice = {
            STATEMENT: _lattice_type(STATEMENT, (
                ("lender", ("demo-lender",)),
                ("statement", ("demo-statement-1", "demo-statement-2")),
                ("tax-year", ("2025",)),
            )),
        }
        s1 = f"{STATEMENT}|lender=demo-lender,statement=demo-statement-1,tax-year=2025"
        s2 = f"{STATEMENT}|lender=demo-lender,statement=demo-statement-2,tax-year=2025"
        findings = {
            "demo.finding.s1": _finding("demo.finding.s1", s1, "current"),
            "demo.finding.s2": _finding("demo.finding.s2", s2, "current"),
        }
        rule = _v11_rule(
            rule_id="demo.rule.livepath.subject-only",
            subject={"id": STATEMENT, "version": "v1"},
            requires=[],
            value={"op": "ref", "name": STATEMENT},
            publishes=CONFIRMED,
        )
        parts = [
            (rule, "computation"),
            (_package_fact_type(STATEMENT, ["lender", "statement", "tax-year"]), "fact-type"),
        ]
        return parts, findings, lattice

    def test_one_keyed_publication_per_statement_both_runners(self) -> None:
        parts, findings, lattice = self._fixture()
        rule = parts[0][0]
        entrypoints = [
            {"id": rule["id"], "version": rule["version"]},
            {"id": STATEMENT, "version": "v1"},
        ]
        material, ctx = _live_context(parts, findings, lattice, entrypoints=entrypoints)
        self.assertIn(STATEMENT, material.emission_only_names)
        forward, backward = _both_runners(ctx)
        for result in (forward, backward):
            published = _publications(result)
            s1_symbol = f"{CONFIRMED}|{STATEMENT}|lender=demo-lender,statement=demo-statement-1,tax-year=2025"
            s2_symbol = f"{CONFIRMED}|{STATEMENT}|lender=demo-lender,statement=demo-statement-2,tax-year=2025"
            self.assertIn(s1_symbol, published, result.dispositions)
            self.assertIn(s2_symbol, published, result.dispositions)
            self.assertEqual(published[s1_symbol]["value"], "current")
            self.assertEqual(published[s2_symbol]["value"], "current")
            self.assertEqual(_input_ids(published[s1_symbol]["pins"]), {"demo.finding.s1"})
            self.assertEqual(_input_ids(published[s2_symbol]["pins"]), {"demo.finding.s2"})


FINANCING = "demo.tax.livepath.financing"
ENROLMENT = "demo.tax.livepath.enrolment"
STATUS = "demo.tax.livepath.status"


class JoinedRowsAreEmittedAndPresenceRuns(unittest.TestCase):
    """A v11 rule declaring ``joined``/``direction`` over standalone fact
    types: the joined rows are emitted with keys, and the presence check
    runs -- one joining case, one malformed-row block."""

    def _fact_types(self) -> list[tuple[dict[str, Any], str]]:
        return [
            (_package_fact_type(FINANCING, ["borrowing", "period", "institution", "programme"]), "fact-type"),
            (_package_fact_type(ENROLMENT, ["period", "institution", "programme"]), "fact-type"),
        ]

    def _rule(self) -> dict[str, Any]:
        return _v11_rule(
            rule_id="demo.rule.livepath.status",
            subject={"id": FINANCING, "version": "v1"},
            joined={"id": ENROLMENT, "version": "v1"},
            direction="subject_contains_joined",
            requires=[ENROLMENT],
            value={"op": "ref", "name": ENROLMENT},
            publishes=STATUS,
        )

    def _entrypoints(self, rule: dict[str, Any]) -> list[dict[str, str]]:
        return [
            {"id": rule["id"], "version": rule["version"]},
            {"id": FINANCING, "version": "v1"},
            {"id": ENROLMENT, "version": "v1"},
        ]

    def test_joining_case_publishes_pinning_the_joined_row(self) -> None:
        rule = self._rule()
        parts = [(rule, "computation")] + self._fact_types()
        lattice = {
            FINANCING: _lattice_type(FINANCING, (
                ("borrowing", ("demo-borrowing-1",)),
                ("period", ("2024-autumn",)),
                ("institution", ("demo-institution",)),
                ("programme", ("demo-programme",)),
            )),
            ENROLMENT: _lattice_type(ENROLMENT, (
                ("period", ("2024-autumn",)),
                ("institution", ("demo-institution",)),
                ("programme", ("demo-programme",)),
            )),
        }
        financing_fact = f"{FINANCING}|borrowing=demo-borrowing-1,period=2024-autumn,institution=demo-institution,programme=demo-programme"
        enrolment_fact = f"{ENROLMENT}|period=2024-autumn,institution=demo-institution,programme=demo-programme"
        findings = {
            "demo.finding.financing": _finding("demo.finding.financing", financing_fact, "tuition"),
            "demo.finding.enrolment": _finding("demo.finding.enrolment", enrolment_fact, "not-adverse"),
        }
        material, ctx = _live_context(parts, findings, lattice, entrypoints=self._entrypoints(rule))
        self.assertIn(FINANCING, material.emission_only_names)
        self.assertIn(ENROLMENT, material.emission_only_names)
        forward, backward = _both_runners(ctx)
        for result in (forward, backward):
            published = _publications(result)
            symbol = f"{STATUS}|{financing_fact}"
            self.assertIn(symbol, published, result.dispositions)
            self.assertEqual(published[symbol]["value"], "not-adverse")
            # The subject's own finding is always pinned as an input
            # alongside whichever joined row it read.
            self.assertEqual(
                _input_ids(published[symbol]["pins"]),
                {"demo.finding.financing", "demo.finding.enrolment"},
            )

    def test_malformed_enrolment_row_blocks_the_subject(self) -> None:
        rule = self._rule()
        parts = [(rule, "computation")] + self._fact_types()
        lattice = {
            FINANCING: _lattice_type(FINANCING, (
                ("borrowing", ("demo-borrowing-1",)),
                ("period", ("2024-autumn",)),
                ("institution", ("demo-institution",)),
                ("programme", ("demo-programme",)),
            )),
            ENROLMENT: _lattice_type(ENROLMENT, (
                ("period", ("2024-autumn",)),
                ("institution", ("demo-institution",)),
                ("programme", ("demo-programme",)),
            )),
        }
        financing_fact = f"{FINANCING}|borrowing=demo-borrowing-1,period=2024-autumn,institution=demo-institution,programme=demo-programme"
        enrolment_fact = f"{ENROLMENT}|period=2024-autumn,institution=demo-institution,programme=demo-programme"
        # Present, current, but not a lattice fact -- its fact_id carries
        # only one of the three declared identity names, so the kernel
        # lattice has no matching entry and marshal renders it keys=None
        # (ADR 0076 Part 2: "it lacks a required name" / "no keys at all").
        malformed_fact = f"{ENROLMENT}|programme=demo-programme"
        findings = {
            "demo.finding.financing": _finding("demo.finding.financing", financing_fact, "tuition"),
            "demo.finding.enrolment": _finding("demo.finding.enrolment", enrolment_fact, "not-adverse"),
            "demo.finding.enrolment.malformed": _finding(
                "demo.finding.enrolment.malformed", malformed_fact, "adverse"
            ),
        }
        material, ctx = _live_context(parts, findings, lattice, entrypoints=self._entrypoints(rule))
        forward, backward = _both_runners(ctx)
        for result in (forward, backward):
            published = _publications(result)
            symbol = f"{STATUS}|{financing_fact}"
            self.assertNotIn(symbol, published)
            rows = _blocked_rows(result, symbol)
            self.assertEqual(len(rows), 1, result.dispositions)
            self.assertEqual(rows[0]["code"], "DEPENDENCY_INVALID")
            self.assertEqual(rows[0]["missing"], ["demo.finding.enrolment.malformed"])


WITNESS = "demo.tax.livepath.witness"
WITNESS_ECHO = "demo.tax.livepath.witness-echo"


class EmissionIsNotScalarBinding(unittest.TestCase):
    """An ordinary rule elsewhere in the package keeps the same scalar
    binding with and without the v11 rule present (Track 4's rule: an
    emission-only finding is not marked used)."""

    def _witness_parts(self) -> list[tuple[dict[str, Any], str]]:
        ordinary = _ordinary_rule(
            rule_id="demo.rule.livepath.witness-echo",
            publishes=WITNESS_ECHO,
            value={"op": "ref", "name": WITNESS},
            requires=[WITNESS],
        )
        return [(ordinary, "computation")]

    def _findings(self) -> dict[str, dict[str, Any]]:
        return {
            "demo.finding.witness": _finding("demo.finding.witness", WITNESS, "witness-value"),
        }

    def test_ordinary_scalar_binding_unaffected_by_the_v11_rule(self) -> None:
        without_v11 = self._witness_parts()
        entrypoints_without = [{"id": without_v11[0][0]["id"], "version": without_v11[0][0]["version"]}]
        _material_a, ctx_a = _live_context(
            without_v11, self._findings(), {}, entrypoints=entrypoints_without
        )

        v11_rule = _v11_rule(
            rule_id="demo.rule.livepath.subject-only-sibling",
            subject={"id": STATEMENT, "version": "v1"},
            requires=[],
            value={"op": "ref", "name": STATEMENT},
            publishes=CONFIRMED,
        )
        lattice_b = {
            STATEMENT: _lattice_type(STATEMENT, (
                ("lender", ("demo-lender",)),
                ("statement", ("demo-statement-1",)),
                ("tax-year", ("2025",)),
            )),
        }
        statement_fact = f"{STATEMENT}|lender=demo-lender,statement=demo-statement-1,tax-year=2025"
        findings_b = dict(self._findings())
        findings_b["demo.finding.s1"] = _finding("demo.finding.s1", statement_fact, "current")
        with_v11 = self._witness_parts() + [
            (v11_rule, "computation"),
            (_package_fact_type(STATEMENT, ["lender", "statement", "tax-year"]), "fact-type"),
        ]
        entrypoints_with = entrypoints_without + [
            {"id": v11_rule["id"], "version": v11_rule["version"]},
            {"id": STATEMENT, "version": "v1"},
        ]
        _material_b, ctx_b = _live_context(
            with_v11, findings_b, lattice_b, entrypoints=entrypoints_with
        )

        forward_a, backward_a = _both_runners(ctx_a)
        forward_b, backward_b = _both_runners(ctx_b)
        for a, b in ((forward_a, forward_b), (backward_a, backward_b)):
            pub_a = _publications(a)[WITNESS_ECHO]
            pub_b = _publications(b)[WITNESS_ECHO]
            self.assertEqual(pub_a["value"], pub_b["value"])
            self.assertEqual(pub_a["value"], "witness-value")
            self.assertEqual(_input_ids(pub_a["pins"]), _input_ids(pub_b["pins"]))


# ---------------------------------------------------------------------------
# Defect 2: runtime does not honour the pinned fact-type version.
# ---------------------------------------------------------------------------


V2STATEMENT = "demo.tax.livepath.v2case.statement"
V2LINKS = "demo.tax.livepath.v2case.links"
V2ECHO = "demo.tax.livepath.v2case.link-echo"


class RuntimeHonoursThePinnedFactTypeVersion(unittest.TestCase):
    """A weaker v1 identity declared alongside a stronger v2 identity of the
    same id; the rule pins v2. Runtime must resolve exactly that pin, in
    either declaration order."""

    def _fixture(self, *, weak_first: bool) -> tuple[list[tuple[dict[str, Any], str]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
        rule = _v11_rule(
            rule_id="demo.rule.livepath.v2case",
            subject={"id": V2STATEMENT, "version": "v2"},
            joined={"id": V2LINKS, "version": "v1"},
            direction="joined_contains_subject",
            requires=[V2LINKS],
            value={"op": "ref", "name": V2LINKS},
            publishes=V2ECHO,
        )
        weak = _package_fact_type(V2STATEMENT, ["tax-year"], version="v1")
        strong = _package_fact_type(V2STATEMENT, ["lender", "statement", "tax-year"], version="v2")
        # The joined type's own declared identity is a superset of the
        # *strong* subject identity, so static containment (Track 5a) holds
        # regardless of which subject version this runtime defect confuses.
        links_type = _package_fact_type(V2LINKS, ["lender", "statement", "tax-year", "borrowing"])
        fact_type_parts = [weak, strong] if weak_first else [strong, weak]
        parts = [(rule, "computation")] + [(ft, "fact-type") for ft in fact_type_parts] + [
            (links_type, "fact-type"),
        ]

        lattice = {
            V2STATEMENT: _lattice_type(V2STATEMENT, (
                ("lender", ("demo-lender",)),
                ("statement", ("demo-statement-1", "demo-statement-2")),
                ("tax-year", ("2025",)),
            )),
            # The real link row carries only tax-year -- complete under the
            # weak v1 declaration (whose only required name is tax-year),
            # malformed under the pinned, stronger v2 declaration (missing
            # lender and statement). The row's actual keys are independent
            # of what either package-declared fact-type citizen promises.
            V2LINKS: _lattice_type(V2LINKS, (("tax-year", ("2025",)),)),
        }
        s1 = f"{V2STATEMENT}|lender=demo-lender,statement=demo-statement-1,tax-year=2025"
        s2 = f"{V2STATEMENT}|lender=demo-lender,statement=demo-statement-2,tax-year=2025"
        link = f"{V2LINKS}|tax-year=2025"
        findings = {
            "demo.finding.s1": _finding("demo.finding.s1", s1, "current"),
            "demo.finding.s2": _finding("demo.finding.s2", s2, "current"),
            "demo.finding.link": _finding("demo.finding.link", link, "42"),
        }
        return parts, findings, lattice

    def _entrypoints(self, rule: dict[str, Any]) -> list[dict[str, str]]:
        return [
            {"id": rule["id"], "version": rule["version"]},
            {"id": V2STATEMENT, "version": "v1"},
            {"id": V2STATEMENT, "version": "v2"},
            {"id": V2LINKS, "version": "v1"},
        ]

    def _assert_blocks_both_statements(self, weak_first: bool) -> None:
        parts, findings, lattice = self._fixture(weak_first=weak_first)
        rule = parts[0][0]
        material, ctx = _live_context(parts, findings, lattice, entrypoints=self._entrypoints(rule))
        # Both declared (id, "v1") and (id, "v2") versions of V2STATEMENT
        # must be present in the resolved material -- Defect 1's
        # "keeping every declared version of an id."
        self.assertEqual(
            {(ft.get("id"), ft.get("version")) for ft in material[4] if ft.get("id") == V2STATEMENT},
            {(V2STATEMENT, "v1"), (V2STATEMENT, "v2")},
        )
        forward, backward = _both_runners(ctx)
        s1_fact = f"{V2STATEMENT}|lender=demo-lender,statement=demo-statement-1,tax-year=2025"
        s2_fact = f"{V2STATEMENT}|lender=demo-lender,statement=demo-statement-2,tax-year=2025"
        for result in (forward, backward):
            published = _publications(result)
            for fact_id in (s1_fact, s2_fact):
                symbol = f"{V2ECHO}|{fact_id}"
                self.assertNotIn(symbol, published, f"{fact_id} published {published.get(symbol)!r}")
                rows = _blocked_rows(result, symbol)
                self.assertEqual(len(rows), 1, result.dispositions)
                self.assertEqual(rows[0]["code"], "DEPENDENCY_INVALID")
                self.assertEqual(rows[0]["missing"], ["demo.finding.link"])

    def test_weak_declared_first_still_blocks_both(self) -> None:
        self._assert_blocks_both_statements(weak_first=True)

    def test_strong_declared_first_still_blocks_both(self) -> None:
        self._assert_blocks_both_statements(weak_first=False)


# ---------------------------------------------------------------------------
# Defect 3: a run-wide scalar bypasses a declared relationship.
# ---------------------------------------------------------------------------


BYPASS_FINANCING = "demo.tax.livepath.bypass.financing"
BYPASS_ENROLMENT = "demo.tax.livepath.bypass.enrolment"
BYPASS_STATUS = "demo.tax.livepath.bypass.status"


class RunWideScalarDoesNotBypassADeclaredRelationship(unittest.TestCase):
    """The joined type's value is available inside dispatch only from a row
    that joined this subject -- never the run-wide scalar, and not readable
    from the run-wide environment during that subject's evaluation."""

    def _financing_fact_type(self) -> dict[str, Any]:
        return _package_fact_type(
            BYPASS_FINANCING, ["borrowing", "period", "institution", "programme"]
        )

    def _enrolment_fact_type(self) -> dict[str, Any]:
        return _package_fact_type(BYPASS_ENROLMENT, ["period", "institution", "programme"])

    def _financing_lattice_and_fact(self) -> tuple[dict[str, dict[str, Any]], str]:
        lattice = {
            BYPASS_FINANCING: _lattice_type(BYPASS_FINANCING, (
                ("borrowing", ("demo-borrowing-1",)),
                ("period", ("2024-autumn",)),
                ("institution", ("demo-institution",)),
                ("programme", ("demo-programme",)),
            )),
        }
        fact_id = (
            f"{BYPASS_FINANCING}|borrowing=demo-borrowing-1,period=2024-autumn,"
            "institution=demo-institution,programme=demo-programme"
        )
        return lattice, fact_id

    def _status_rule(self) -> dict[str, Any]:
        return _v11_rule(
            rule_id="demo.rule.livepath.bypass-status",
            subject={"id": BYPASS_FINANCING, "version": "v1"},
            joined={"id": BYPASS_ENROLMENT, "version": "v1"},
            direction="subject_contains_joined",
            requires=[BYPASS_ENROLMENT],
            value={"op": "ref", "name": BYPASS_ENROLMENT},
            publishes=BYPASS_STATUS,
        )

    def test_no_rows_and_a_run_wide_scalar_blocks_absent_not_the_scalar(self) -> None:
        """Reproduces the bypass: an ordinary rule elsewhere in the package
        publishes a scalar under the exact same symbol name as the declared
        joined type. Zero rows of that type exist anywhere. The declared
        relationship must not let the subject read that unrelated scalar."""
        status_rule = self._status_rule()
        ambient_rule = _ordinary_rule(
            rule_id="demo.rule.livepath.ambient-enrolment",
            publishes=BYPASS_ENROLMENT,
            value="run-wide-value",
        )
        parts = [
            (status_rule, "computation"),
            (ambient_rule, "computation"),
            (self._financing_fact_type(), "fact-type"),
            (self._enrolment_fact_type(), "fact-type"),
        ]
        lattice, financing_fact = self._financing_lattice_and_fact()
        findings = {
            "demo.finding.financing": _finding("demo.finding.financing", financing_fact, "tuition"),
        }
        entrypoints = [
            {"id": status_rule["id"], "version": status_rule["version"]},
            {"id": ambient_rule["id"], "version": ambient_rule["version"]},
            {"id": BYPASS_FINANCING, "version": "v1"},
            {"id": BYPASS_ENROLMENT, "version": "v1"},
        ]
        material, ctx = _live_context(parts, findings, lattice, entrypoints=entrypoints)
        forward, backward = _both_runners(ctx)
        symbol = f"{BYPASS_STATUS}|{financing_fact}"
        for result in (forward, backward):
            published = _publications(result)
            self.assertNotIn(symbol, published, f"published using the run-wide scalar: {published.get(symbol)!r}")
            rows = _blocked_rows(result, symbol)
            self.assertEqual(len(rows), 1, result.dispositions)
            self.assertEqual(rows[0]["code"], "DEPENDENCY_ABSENT")
            self.assertEqual(rows[0]["missing"], [BYPASS_ENROLMENT])
            # The ambient rule's own ordinary, unsuffixed publication still
            # exists in the run -- this is not a claim that it never ran.
            self.assertIn(BYPASS_ENROLMENT, {p.finding["symbol"] for p in result.publications})

    def test_ordinary_valid_joined_case_publishes_pinning_the_row(self) -> None:
        status_rule = self._status_rule()
        parts = [
            (status_rule, "computation"),
            (self._financing_fact_type(), "fact-type"),
            (self._enrolment_fact_type(), "fact-type"),
        ]
        lattice, financing_fact = self._financing_lattice_and_fact()
        lattice[BYPASS_ENROLMENT] = _lattice_type(BYPASS_ENROLMENT, (
            ("period", ("2024-autumn",)),
            ("institution", ("demo-institution",)),
            ("programme", ("demo-programme",)),
        ))
        enrolment_fact = (
            f"{BYPASS_ENROLMENT}|period=2024-autumn,institution=demo-institution,programme=demo-programme"
        )
        findings = {
            "demo.finding.financing": _finding("demo.finding.financing", financing_fact, "tuition"),
            "demo.finding.enrolment": _finding("demo.finding.enrolment", enrolment_fact, "not-adverse"),
        }
        entrypoints = [
            {"id": status_rule["id"], "version": status_rule["version"]},
            {"id": BYPASS_FINANCING, "version": "v1"},
            {"id": BYPASS_ENROLMENT, "version": "v1"},
        ]
        material, ctx = _live_context(parts, findings, lattice, entrypoints=entrypoints)
        forward, backward = _both_runners(ctx)
        symbol = f"{BYPASS_STATUS}|{financing_fact}"
        for result in (forward, backward):
            published = _publications(result)
            self.assertIn(symbol, published, result.dispositions)
            self.assertEqual(published[symbol]["value"], "not-adverse")
            self.assertEqual(
                _input_ids(published[symbol]["pins"]),
                {"demo.finding.financing", "demo.finding.enrolment"},
            )

    def test_declared_default_still_takes_its_own_pinned_path(self) -> None:
        """No joined row anywhere, no run-wide same-named scalar -- but the
        joined type declares an ``optional_default``. That symbol still
        takes the declared-default path, distinct from both the bypass
        (blocked) and the ordinary joined (real row) cases."""
        param_id = "demo.parameter.livepath.bypass-default"
        parameter = {
            "schema": "parameter-declaration.v1",
            "id": param_id,
            "version": "v1",
            "scope": dict(SCOPE),
            "values": "not-adverse",
        }
        enrolment_type = dict(self._enrolment_fact_type())
        enrolment_type["optional_default"] = {"parameter": {"id": param_id, "version": "v1"}}
        status_rule = self._status_rule()
        parts = [
            (status_rule, "computation"),
            (self._financing_fact_type(), "fact-type"),
            (enrolment_type, "fact-type"),
            (parameter, "parameter"),
        ]
        lattice, financing_fact = self._financing_lattice_and_fact()
        findings = {
            "demo.finding.financing": _finding("demo.finding.financing", financing_fact, "tuition"),
        }
        entrypoints = [
            {"id": status_rule["id"], "version": status_rule["version"]},
            {"id": BYPASS_FINANCING, "version": "v1"},
            {"id": BYPASS_ENROLMENT, "version": "v1"},
            {"id": param_id, "version": "v1"},
        ]
        # ``optional_default`` on the fact type alone is not enough --
        # ``subject_dispatch._optional_default`` also requires an ordinary
        # package ``input_bindings`` entry naming the symbol and fact type
        # with ``mode: optional_default`` (the same shape
        # ``test_subject_dispatch.py``'s ``CIRCUMSTANCE`` binding uses).
        bindings = [{
            "symbol": BYPASS_ENROLMENT,
            "fact_type": {"id": BYPASS_ENROLMENT, "version": "v1"},
            "mode": "optional_default",
        }]
        material, ctx = _live_context(
            parts, findings, lattice, entrypoints=entrypoints, bindings=bindings
        )
        forward, backward = _both_runners(ctx)
        symbol = f"{BYPASS_STATUS}|{financing_fact}"
        for result in (forward, backward):
            published = _publications(result)
            self.assertIn(symbol, published, result.dispositions)
            self.assertEqual(published[symbol]["value"], "not-adverse")
            pins = published[symbol]["pins"]
            input_pins = [pin for pin in pins if pin["role"] == "input"]
            origins = {pin["id"]: pin.get("origin") for pin in input_pins}
            # The subject's own finding is an ordinary asserted input; the
            # joined symbol itself is not a source-pinned finding at all --
            # it is a separate, visibly-pinned ``declared_default`` finding
            # (Track 5b's own default machinery), never the bypass's
            # unscoped run-wide value and never absent.
            self.assertEqual(origins.get("demo.finding.financing"), "assertion")
            default_ids = [fid for fid, origin in origins.items() if origin == "declared_default"]
            self.assertEqual(len(default_ids), 1, origins)
            default_finding = next(
                p.finding for p in result.publications if p.finding["id"] == default_ids[0]
            )
            self.assertEqual(default_finding["value"], "not-adverse")
            default_parameter_ids = {
                pin["id"] for pin in default_finding["pins"] if pin["role"] == "parameter"
            }
            self.assertEqual(default_parameter_ids, {param_id})


# ---------------------------------------------------------------------------
# Round 2 -- Defect 4 (same class as Defect 2): ``optional_default`` resolved
# by fact-type id alone, in three places -- package_validation.py's binding
# check, runner.py's ordinary optional_default machinery, and
# subject_dispatch._optional_default. Each let one version of an id silently
# answer for another: a binding pinning a version with no default validated
# anyway (last-declared-wins), and at runtime the wrong version's parameter
# could be read.
# ---------------------------------------------------------------------------


VALIDATION_FT = "demo.tax.optdefault.validation"
VALIDATION_PARAM = "demo.parameter.optdefault.v2-only"


class ValidationRejectsABindingPinningANoDefaultVersion(unittest.TestCase):
    """A fact type declared at v1 (no ``optional_default``) and v2 (with
    one); the binding pins v1. ``validate_package`` must reject this --
    the pinned version declares no default -- in either declaration order."""

    def _fixture(self, *, v1_first: bool) -> list[tuple[dict[str, Any], str]]:
        ft_v1 = _package_fact_type(VALIDATION_FT, ["period"], version="v1")
        ft_v2 = dict(_package_fact_type(VALIDATION_FT, ["period"], version="v2"))
        ft_v2["optional_default"] = {"parameter": {"id": VALIDATION_PARAM, "version": "v1"}}
        parameter = {
            "schema": "parameter-declaration.v1",
            "id": VALIDATION_PARAM,
            "version": "v1",
            "scope": dict(SCOPE),
            "values": "not-adverse",
        }
        rule = _ordinary_rule(
            rule_id="demo.rule.optdefault.validation-echo",
            publishes="demo.tax.optdefault.validation-echo",
            value={"op": "ref", "name": VALIDATION_FT},
            requires=[VALIDATION_FT],
        )
        fact_type_parts = [ft_v1, ft_v2] if v1_first else [ft_v2, ft_v1]
        return [(rule, "computation")] + [(ft, "fact-type") for ft in fact_type_parts] + [
            (parameter, "parameter"),
        ]

    def _validate(self, *, v1_first: bool) -> Any:
        parts = self._fixture(v1_first=v1_first)
        binding = {
            "symbol": VALIDATION_FT,
            "fact_type": {"id": VALIDATION_FT, "version": "v1"},
            "mode": "optional_default",
        }
        entrypoints = [
            {"id": parts[0][0]["id"], "version": parts[0][0]["version"]},
            {"id": VALIDATION_FT, "version": "v1"},
            {"id": VALIDATION_FT, "version": "v2"},
            {"id": VALIDATION_PARAM, "version": "v1"},
        ]
        validation, _package = _resolve(parts, bindings=[binding], entrypoints=entrypoints)
        return validation

    def test_v1_declared_first_is_rejected(self) -> None:
        validation = self._validate(v1_first=True)
        self.assertFalse(validation.ok, validation.issues)
        self.assertIn("BINDING_DEFAULT_MISSING", [issue.code for issue in validation.issues])

    def test_v2_declared_first_is_rejected(self) -> None:
        validation = self._validate(v1_first=False)
        self.assertFalse(validation.ok, validation.issues)
        self.assertIn("BINDING_DEFAULT_MISSING", [issue.code for issue in validation.issues])


RUNTIME_FT = "demo.tax.optdefault.runtime"
RUNTIME_PARAM_A = "demo.parameter.optdefault.pinned"
RUNTIME_PARAM_B = "demo.parameter.optdefault.sibling"
RUNTIME_ECHO = "demo.tax.optdefault.runtime-echo"


class RuntimeResolvesTheExactPinnedDefault(unittest.TestCase):
    """Both versions of the same id declare a default, with *different*
    parameters -- this validates under either the old or the new logic (some
    version has a default), isolating the runtime lookup. The binding pins
    v1 (parameter A, "not-adverse"); v2's parameter (B, "adverse") must never
    be read, in either declaration order -- the positive case (the pinned
    version does declare a default) still works correctly."""

    def _fact_types(self, *, v1_first: bool) -> list[dict[str, Any]]:
        ft_v1 = dict(_package_fact_type(RUNTIME_FT, ["period"], version="v1"))
        ft_v1["optional_default"] = {"parameter": {"id": RUNTIME_PARAM_A, "version": "v1"}}
        ft_v2 = dict(_package_fact_type(RUNTIME_FT, ["period"], version="v2"))
        ft_v2["optional_default"] = {"parameter": {"id": RUNTIME_PARAM_B, "version": "v1"}}
        return [ft_v1, ft_v2] if v1_first else [ft_v2, ft_v1]

    def _parameters(self) -> list[dict[str, Any]]:
        return [
            {
                "schema": "parameter-declaration.v1", "id": RUNTIME_PARAM_A, "version": "v1",
                "scope": dict(SCOPE), "values": "not-adverse",
            },
            {
                "schema": "parameter-declaration.v1", "id": RUNTIME_PARAM_B, "version": "v1",
                "scope": dict(SCOPE), "values": "adverse",
            },
        ]

    def _binding(self) -> dict[str, Any]:
        return {
            "symbol": RUNTIME_FT,
            "fact_type": {"id": RUNTIME_FT, "version": "v1"},
            "mode": "optional_default",
        }

    def _assert_default_from_pinned_version(self, symbol: str, result: Any) -> None:
        published = _publications(result)
        self.assertIn(symbol, published, result.dispositions)
        self.assertEqual(published[symbol]["value"], "not-adverse")
        # The manufactured ``declared_default`` finding is a separate
        # publication (both the ordinary and the subject-scoped machinery
        # record it as its own derived-finding.v2); the outer symbol's own
        # pins reference it as an ordinary input, and that finding's own
        # pins carry the parameter -- never the sibling version's.
        input_pins = [pin for pin in published[symbol]["pins"] if pin["role"] == "input"]
        default_pins = [pin for pin in input_pins if pin.get("origin") == "declared_default"]
        self.assertEqual(len(default_pins), 1, published[symbol]["pins"])
        default_finding = next(
            p.finding for p in result.publications if p.finding["id"] == default_pins[0]["id"]
        )
        self.assertEqual(default_finding["value"], "not-adverse")
        parameter_ids = {pin["id"] for pin in default_finding["pins"] if pin["role"] == "parameter"}
        self.assertEqual(parameter_ids, {RUNTIME_PARAM_A})
        self.assertNotIn(RUNTIME_PARAM_B, parameter_ids)

    def _run_ordinary(self, *, v1_first: bool) -> tuple[Any, Any]:
        rule = _ordinary_rule(
            rule_id="demo.rule.optdefault.runtime-echo",
            publishes=RUNTIME_ECHO,
            value={"op": "ref", "name": RUNTIME_FT},
            requires=[RUNTIME_FT],
        )
        parts = [(rule, "computation")] + [
            (ft, "fact-type") for ft in self._fact_types(v1_first=v1_first)
        ] + [(p, "parameter") for p in self._parameters()]
        entrypoints = [
            {"id": rule["id"], "version": rule["version"]},
            {"id": RUNTIME_FT, "version": "v1"},
            {"id": RUNTIME_FT, "version": "v2"},
            {"id": RUNTIME_PARAM_A, "version": "v1"},
            {"id": RUNTIME_PARAM_B, "version": "v1"},
        ]
        _material, ctx = _live_context(
            parts, {}, {}, entrypoints=entrypoints, bindings=[self._binding()]
        )
        return _both_runners(ctx)

    def test_ordinary_rule_v1_declared_first(self) -> None:
        forward, backward = self._run_ordinary(v1_first=True)
        for result in (forward, backward):
            self._assert_default_from_pinned_version(RUNTIME_ECHO, result)

    def test_ordinary_rule_v2_declared_first(self) -> None:
        forward, backward = self._run_ordinary(v1_first=False)
        for result in (forward, backward):
            self._assert_default_from_pinned_version(RUNTIME_ECHO, result)

    def _run_subject(self, *, v1_first: bool) -> tuple[Any, Any, str]:
        subject_type = "demo.tax.optdefault.subject"
        v11_rule = _v11_rule(
            rule_id="demo.rule.optdefault.subject-echo",
            subject={"id": subject_type, "version": "v1"},
            requires=[RUNTIME_FT],
            value={"op": "ref", "name": RUNTIME_FT},
            publishes="demo.tax.optdefault.subject-result",
        )
        parts = [
            (v11_rule, "computation"),
            (_package_fact_type(subject_type, ["who"]), "fact-type"),
        ] + [
            (ft, "fact-type") for ft in self._fact_types(v1_first=v1_first)
        ] + [(p, "parameter") for p in self._parameters()]
        entrypoints = [
            {"id": v11_rule["id"], "version": v11_rule["version"]},
            {"id": subject_type, "version": "v1"},
            {"id": RUNTIME_FT, "version": "v1"},
            {"id": RUNTIME_FT, "version": "v2"},
            {"id": RUNTIME_PARAM_A, "version": "v1"},
            {"id": RUNTIME_PARAM_B, "version": "v1"},
        ]
        lattice = {
            subject_type: _lattice_type(subject_type, (("who", ("demo-who",)),)),
        }
        subject_fact = f"{subject_type}|who=demo-who"
        findings = {
            "demo.finding.subject": _finding("demo.finding.subject", subject_fact, "x"),
        }
        _material, ctx = _live_context(
            parts, findings, lattice, entrypoints=entrypoints, bindings=[self._binding()]
        )
        symbol = f"demo.tax.optdefault.subject-result|{subject_fact}"
        return _both_runners(ctx) + (symbol,)

    def test_declared_subject_rule_v1_declared_first(self) -> None:
        forward, backward, symbol = self._run_subject(v1_first=True)
        for result in (forward, backward):
            self._assert_default_from_pinned_version(symbol, result)

    def test_declared_subject_rule_v2_declared_first(self) -> None:
        forward, backward, symbol = self._run_subject(v1_first=False)
        for result in (forward, backward):
            self._assert_default_from_pinned_version(symbol, result)


if __name__ == "__main__":
    unittest.main()
