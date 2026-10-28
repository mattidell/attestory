"""ADR-0082: companion admission belongs to the package being run.

A synthetic surface (``demo.*`` ids) with three published packages that share
every citizen and differ only in version, so the only thing that varies between
runs is which package is in force:

* ``v1`` -- the earlier package. No declaration: the global maps apply (the
  companion is an absent-or-zero witness).
* ``v2`` -- declares that the same companion may carry any value its
  ``value_schema`` allows.
* ``v3`` -- declares a different companion fact for the same amount.

Every run goes through ``live_coordinate_run``.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.act_log import ActLog
from packages.kernel.facts import fact_id_for
from packages.kernel.findings import FindingModelError, project
from packages.tax.loader import tax_registry

ROOT = Path(__file__).resolve().parent.parent
BASE_PACKAGE = ROOT / "packages/content/tax/2025/package.core-calculations.v53.json"

USER = "demo.user.filer-1"
YEAR = "2025"
RUN_SCOPE = {"jurisdiction": "us", "year": YEAR}
RULE_SCOPE = {"family": "individual-income-tax", "jurisdiction": "US-federal", "tax_year": 2025}
SCOPE_KEY = {"tax-year": YEAR, "subject": "demo.primary"}

P = "demo.cmp."
STATEMENT_KIND = P + "statement"
SRC = P + "amount"
COMP = P + "companion"
COMP_ALT = P + "companion-alt"
CLOSURE_A = P + "amount.source-closure"
CLOSURE_B = P + "companion.source-closure"
FAMILY_A = P + "family-amount"
FAMILY_B = P + "family-companion"
RULE_A = P + "rule.amount-total"
RULE_B = P + "rule.companion-total"
PUB_A = P + "amount-subtotal"
PUB_B = P + "companion-subtotal"
PACKAGE_ID = "demo.package.cmp"
V1, V2, V3 = ("v1", "v2", "v3")


def _pin(item_id: str) -> dict[str, str]:
    return {"id": item_id, "version": "v1"}


def _fact_type(fact_id: str, schema: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": "v1",
        "title": f"Synthetic {fact_id}",
        "nature": "determinable",
        "identity_keys": [
            {"name": "statement", "kind": "entity", "entity_kind": STATEMENT_KIND},
            {"name": "tax-year", "kind": "literal", "values": [YEAR]},
        ],
        "value_schema": schema,
        "supersession": {"policy": "free"},
    }


def _closure_type(fact_id: str) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": "v1",
        "title": f"Synthetic closure {fact_id}",
        "nature": "determinable",
        "identity_keys": [
            {"name": "family-horizon", "kind": "entity", "entity_kind": "kernel.family-horizon"},
            {"name": "tax-year", "kind": "literal", "values": [YEAR]},
        ],
        "value_schema": {"type": "boolean"},
        "supersession": {"policy": "free"},
    }


def _bundle() -> dict[str, Any]:
    nonneg = {"type": "number", "minimum": 0}
    return {
        "schema": "bundle.v2",
        "id": P + "vocabulary",
        "version": "v1",
        "label": "Synthetic companion vocabulary",
        "fact_types": [
            _fact_type(SRC, nonneg),
            _fact_type(COMP, nonneg),
            _fact_type(COMP_ALT, nonneg),
            _closure_type(CLOSURE_A),
            _closure_type(CLOSURE_B),
        ],
    }


def _family(family_id: str, member: str, subtotal: str) -> dict[str, Any]:
    return {
        "schema": "source-family.v1",
        "id": family_id,
        "version": "v1",
        "scope": dict(RULE_SCOPE),
        "title": f"Synthetic family {family_id}",
        "member_predicate": {"fact_type": member},
        "authorizes_subtotal": subtotal,
        "closure_claim": "Every synthetic statement is recorded.",
    }


def _mapping(mapping_id: str, family_id: str, member: str, closure: str, subtotal: str) -> dict[str, Any]:
    return {
        "schema": "source-closure-mapping.v2",
        "id": mapping_id,
        "version": "v1",
        "admission": {"condition": "current-literal-true"},
        "admits_symbol": subtotal,
        "closure_fact_type": _pin(closure),
        "closure_horizon_key": "family-horizon",
        "family": _pin(family_id),
        "member_fact_type": _pin(member),
    }


def _rule(rule_id: str, family_id: str, member: str, publishes: str) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v14",
        "id": rule_id,
        "version": "v1",
        "scope": dict(RULE_SCOPE),
        "role": "computation",
        "requires": [],
        "pins": [],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "when": {"op": "require_closed", "source_set": family_id},
        "value": {
            "op": "add",
            "args": [{"op": "collect", "name": member, "source_set": family_id}],
        },
        "publishes": publishes,
    }


def _citizens() -> list[tuple[dict[str, Any], str]]:
    return [
        (_bundle(), "fact-type-bundle"),
        (_family(FAMILY_A, SRC, P + "amount-subtotal"), "source-family"),
        (_family(FAMILY_B, COMP, P + "companion-subtotal"), "source-family"),
        (_mapping(P + "closure-mapping.a", FAMILY_A, SRC, CLOSURE_A, P + "amount-subtotal"), "source-closure-mapping"),
        (_mapping(P + "closure-mapping.b", FAMILY_B, COMP, CLOSURE_B, P + "companion-subtotal"), "source-closure-mapping"),
        (_rule(RULE_A, FAMILY_A, SRC, PUB_A), "computation"),
        (_rule(RULE_B, FAMILY_B, COMP, PUB_B), "computation"),
    ]


def _build_surface(root: Path) -> tuple[PublicationSurface, dict[str, dict[str, Any]], dict[str, Any]]:
    base = json.loads(BASE_PACKAGE.read_text("utf-8"))
    member_dir = root / "members"
    member_dir.mkdir(parents=True)
    members: list[dict[str, str]] = []
    registry_citizens: list[dict[str, str]] = []
    for body, role in _citizens():
        (member_dir / f"{body['id']}.{body['version']}.json").write_text(
            json.dumps(body, sort_keys=True), encoding="utf-8"
        )
        registry_citizens.append(
            {"id": body["id"], "version": body["version"], "checksum": citizen_checksum(body)}
        )
        members.append(
            {"id": body["id"], "version": body["version"], "schema": body["schema"], "role": role}
        )
    packages: dict[str, dict[str, Any]] = {}
    for version in (V1, V2, V3):
        package = {
            "schema": base["schema"],
            "id": PACKAGE_ID,
            "version": version,
            "scope": dict(base["scope"]),
            "admitted_schemas": list(base["admitted_schemas"]),
            "composition_obligations": [],
            "conflict_semantics": [],
            "entrypoints": [{"id": m["id"], "version": m["version"]} for m in members],
            "input_bindings": [],
            "members": members,
        }
        package["package_checksum"] = package_instance_checksum(package)
        (member_dir / f"{PACKAGE_ID}.{version}.json").write_text(
            json.dumps(package, sort_keys=True), encoding="utf-8"
        )
        packages[version] = package
    registry = {
        "citizens": registry_citizens,
        "packages": [
            {"id": PACKAGE_ID, "version": v, "checksum": packages[v]["package_checksum"]}
            for v in (V1, V2, V3)
        ],
    }
    registry_path = root / "registry.json"
    registry_path.write_text(json.dumps(registry, sort_keys=True), encoding="utf-8")
    release = {
        "id": "demo.release.cmp",
        "version": "v1",
        "schema": "release-registry.v1",
        "package_registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest(),
    }
    release_dir = root / "releases"
    release_dir.mkdir(parents=True)
    release_path = release_dir / "demo.release.cmp.v1.json"
    release_path.write_text(json.dumps(release, sort_keys=True), encoding="utf-8")
    release["checksum"] = hashlib.sha256(release_path.read_bytes()).hexdigest()
    return PublicationSurface(release_dir, registry_path, member_dir), packages, release


def _schemas(*, global_pair: bool = True, declare: bool = True) -> DerivationSchemas:
    """A registry with the synthetic global pair and, optionally, package overlays."""
    schemas = DerivationSchemas()
    reg = schemas.registry
    if global_pair:
        reg.companion_presence_pairs[SRC] = COMP
        reg.companion_value_domains[COMP] = frozenset({None, 0, 0.0})
    if declare:
        # v2: the same companion, any value its value_schema admits.
        reg.package_companion_declarations[(PACKAGE_ID, V2)] = {"value_domains": {COMP: None}}
        # v3: a different companion fact altogether; the old one is not required.
        reg.package_companion_declarations[(PACKAGE_ID, V3)] = {
            "presence_pairs": {SRC: COMP_ALT},
            "value_domains": {COMP: None},
        }
    return schemas


class _Log:
    """Builds one synthetic act log."""

    def __init__(self) -> None:
        self.acts: list[dict[str, Any]] = []

    def add(self, kind: str, payload: dict[str, Any]) -> None:
        index = len(self.acts)
        self.acts.append(
            {
                "schema": "act.v1",
                "act_id": f"demo.cmp.act.{index:03d}",
                "kind": kind,
                "actor": USER,
                "at": "2026-10-27T00:00:00Z",
                "committed_against": index,
                "payload": payload,
            }
        )

    def finding(self, finding_id: str, fact_type: str, value: Any, statement: str = "demo-stmt-1") -> dict[str, Any]:
        return {
            "schema": "finding.v2",
            "id": finding_id,
            "fact_id": fact_id_for(fact_type, (("statement", statement), ("tax-year", YEAR))),
            "value": value,
            "basis": "attested",
            "evidence_ids": [],
        }

    def assertion(self, finding_id: str, fact_type: str, value: Any) -> None:
        self.add("assertion", {"finding": self.finding(finding_id, fact_type, value)})

    def member(self, family: str, finding: dict[str, Any], horizon: str, successor: str) -> None:
        self.add(
            "member-transition",
            {
                "family": _pin(family),
                "scope": SCOPE_KEY,
                "member": {"action": "assert", "finding": finding},
                "successor": {"id": successor, "predecessor": horizon},
            },
        )

    def closure(self, finding_id: str, closure_type: str, horizon: str) -> None:
        self.add(
            "assertion",
            {
                "finding": {
                    "schema": "finding.v2",
                    "id": finding_id,
                    "fact_id": f"{closure_type}|family-horizon={horizon},tax-year={YEAR}",
                    "value": True,
                    "basis": "attested",
                    "evidence_ids": [],
                }
            },
        )

    def adopt(self, package: dict[str, Any], release: dict[str, Any], revision: int, supersedes: str | None = None) -> str:
        payload: dict[str, Any] = {
            "package": {
                "id": package["id"],
                "version": package["version"],
                "checksum": package["package_checksum"],
            },
            "release": {"id": release["id"], "version": release["version"], "checksum": release["checksum"]},
            "revision": revision,
            "scope": dict(RUN_SCOPE),
            "audit": {"note": "synthetic adoption"},
        }
        if supersedes is not None:
            payload["supersedes"] = supersedes
        self.add("package-adoption", payload)
        return str(self.acts[-1]["act_id"])


def _statement_acts(
    *,
    amount: float = 7,
    companion: Any = 0,
    alt: Any = None,
    log: _Log | None = None,
) -> _Log:
    """One statement: companion(s) first (presence), then the amount member."""
    log = log if log is not None else _Log()
    log.add("bundle-adoption", {"bundle": _bundle()})
    log.add(
        "entity-introduced",
        {"entity": {"schema": "entity.v1", "id": "demo-stmt-1", "kind": STATEMENT_KIND, "label": "Synthetic statement"}},
    )
    log.add("horizon-genesis", {"family": _pin(FAMILY_A), "scope": SCOPE_KEY, "horizon_id": "demo.cmp.a0"})
    log.add("horizon-genesis", {"family": _pin(FAMILY_B), "scope": SCOPE_KEY, "horizon_id": "demo.cmp.b0"})
    if companion is not None:
        log.member(FAMILY_B, log.finding("demo.cmp.f.companion", COMP, companion), "demo.cmp.b0", "demo.cmp.b1")
        log.closure("demo.cmp.f.closure-b", CLOSURE_B, "demo.cmp.b1")
    if alt is not None:
        log.assertion("demo.cmp.f.alt", COMP_ALT, alt)
    log.member(FAMILY_A, log.finding("demo.cmp.f.amount", SRC, amount), "demo.cmp.a0", "demo.cmp.a1")
    log.closure("demo.cmp.f.closure-a", CLOSURE_A, "demo.cmp.a1")
    return log


def _coordinate(
    acts: list[dict[str, Any]],
    surface: PublicationSurface,
    schemas: DerivationSchemas,
    workspace: Path,
    run_id: str,
) -> tuple[Any, dict[str, Any]]:
    outcome = live_coordinate_run(
        WorkspaceCapability(workspace),
        repo_root=ROOT,
        authoritative_acts=acts,
        workspace_revision=len(acts),
        run_scope=RUN_SCOPE,
        scope_user=USER,
        request={"schema": "run-request.v1"},
        run_id=run_id,
        governance_pins=[],
        surface=surface,
        output_name=f"{run_id}.json",
        schemas=schemas,
    )
    report: dict[str, Any] = {}
    if outcome.output_path is not None and outcome.output_path.exists():
        report = json.loads(outcome.output_path.read_text("utf-8"))
    return outcome, report


def _disposition(report: dict[str, Any], rule_id: str) -> dict[str, Any]:
    return next(d for d in report["dispositions"] if d.get("artifact_id") == rule_id)


def _published(outcome: Any, symbol_prefix: str) -> list[Any]:
    return [
        float(pub.finding.get("value"))
        for pub in (outcome.publications or ())
        if str(pub.finding.get("symbol", "")).startswith(symbol_prefix)
    ]


def _input_pin_ids(disposition: dict[str, Any]) -> list[str]:
    return [p["id"] for p in disposition.get("pins", []) if p.get("role") == "input"]


class _Surface(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.surface, self.packages, self.release = _build_surface(self.root / "surface")

    def run_under(
        self,
        version: str,
        log: _Log,
        run_id: str,
        *,
        schemas: DerivationSchemas | None = None,
    ) -> tuple[Any, dict[str, Any]]:
        acts = list(log.acts)
        adopting = _Log()
        adopting.acts = acts
        adopting.adopt(self.packages[version], self.release, revision=len(acts) + 1)
        return _coordinate(acts, self.surface, schemas or _schemas(), self.root / run_id, run_id)

    def refusal_message(self, version: str, log: _Log, schemas: DerivationSchemas) -> str:
        with self.assertRaises(FindingModelError) as ctx:
            self.run_under(version, log, "demo-refused", schemas=schemas)
        return str(ctx.exception)


class TestEarlierPackageUnchanged(_Surface):
    def test_nonzero_companion_refused_with_todays_text(self) -> None:
        log = _statement_acts(companion=50)
        with_overlays = self.refusal_message(V1, log, _schemas())
        # Today's behavior: the same registry with no overlay mechanism in use.
        without_overlays = self.refusal_message(V1, _statement_acts(companion=50), _schemas(declare=False))
        self.assertEqual(with_overlays, without_overlays)
        self.assertIn("companion presence violated", with_overlays)
        self.assertIn(COMP, with_overlays)

    def test_zero_companion_publishes_under_earlier_package(self) -> None:
        outcome, _ = self.run_under(V1, _statement_acts(companion=0), "demo-v1-zero")
        self.assertIsNone(outcome.refusal)
        self.assertEqual(_published(outcome, PUB_A), [7])

    def test_missing_companion_still_refused_naming_it(self) -> None:
        log = _Log()
        log.add("bundle-adoption", {"bundle": _bundle()})
        log.add(
            "entity-introduced",
            {"entity": {"schema": "entity.v1", "id": "demo-stmt-1", "kind": STATEMENT_KIND, "label": "s"}},
        )
        log.add("horizon-genesis", {"family": _pin(FAMILY_A), "scope": SCOPE_KEY, "horizon_id": "demo.cmp.a0"})
        log.member(FAMILY_A, log.finding("demo.cmp.f.amount", SRC, 7), "demo.cmp.a0", "demo.cmp.a1")
        for version in (V1, V2):
            message = self.refusal_message(version, log, _schemas())
            self.assertIn("companion presence violated", message)
            self.assertIn(COMP, message)


class TestSuccessorPackageDeclares(_Surface):
    def test_wider_domain_admitted_and_amount_reaches_reading_rule(self) -> None:
        outcome, report = self.run_under(V2, _statement_acts(companion=50), "demo-v2-wide")
        self.assertIsNone(outcome.refusal)
        self.assertEqual(_published(outcome, PUB_A), [7])
        self.assertEqual(_published(outcome, PUB_B), [50])
        self.assertEqual(_disposition(report, RULE_B)["disposition"], "published")

    def test_different_companion_enforced_for_new_fact_not_old(self) -> None:
        # v3 requires COMP_ALT. COMP is absent entirely: not required.
        outcome, _ = self.run_under(V3, _statement_acts(companion=None, alt=3), "demo-v3-alt")
        self.assertIsNone(outcome.refusal)
        self.assertEqual(_published(outcome, PUB_A), [7])
        # COMP_ALT absent: refused naming COMP_ALT, even though COMP is present.
        message = self.refusal_message(V3, _statement_acts(companion=0, alt=None), _schemas())
        self.assertIn("companion presence violated", message)
        self.assertIn(COMP_ALT, message)
        self.assertNotIn(f"{COMP}|", message)

    def test_declaration_keyed_to_other_package_does_not_apply(self) -> None:
        schemas = _schemas()
        schemas.registry.package_companion_declarations.pop((PACKAGE_ID, V2))
        message = self.refusal_message(V2, _statement_acts(companion=50), schemas)
        self.assertIn(COMP, message)


class TestNeverSilent(_Surface):
    def test_log_recorded_under_successor_refuses_under_earlier_package(self) -> None:
        log = _statement_acts(companion=50)
        # Same log: admitted while v2 is in force...
        adopt_v2 = log.adopt(self.packages[V2], self.release, revision=len(log.acts) + 1)
        outcome, _ = _coordinate(list(log.acts), self.surface, _schemas(), self.root / "w2", "demo-rec-v2")
        self.assertEqual(_published(outcome, PUB_B), [50])
        # ...then the person re-adopts the earlier package: the run refuses.
        log.adopt(self.packages[V1], self.release, revision=len(log.acts) + 2, supersedes=adopt_v2)
        with self.assertRaises(FindingModelError) as ctx:
            _coordinate(list(log.acts), self.surface, _schemas(), self.root / "w1", "demo-rec-v1")
        self.assertIn("companion presence violated", str(ctx.exception))
        self.assertIn(COMP, str(ctx.exception))
        # Nothing was computed over the statement: no output was produced.
        self.assertFalse(list((self.root / "w1").rglob("demo-rec-v1.json")))

    def test_adoption_that_would_strand_the_log_is_refused_at_append(self) -> None:
        schemas = _schemas()
        registry = tax_registry()
        registry.companion_presence_pairs[SRC] = COMP
        registry.companion_value_domains[COMP] = frozenset({None, 0, 0.0})
        registry.package_companion_declarations.update(schemas.registry.package_companion_declarations)
        log = _Log()
        adopt_v2 = log.adopt(self.packages[V2], self.release, revision=1)
        _statement_acts(companion=50, log=log)
        with TemporaryDirectory() as tmp:
            actlog = ActLog(Path(tmp), registry)
            revision = 0
            for act in log.acts:
                revision = actlog.append(act, revision)
            self.assertEqual(revision, len(log.acts))
            earlier = _Log()
            earlier.acts = list(log.acts)
            earlier.adopt(self.packages[V1], self.release, revision=2, supersedes=adopt_v2)
            with self.assertRaises(FindingModelError) as ctx:
                actlog.append(earlier.acts[-1], revision)
            self.assertIn(COMP, str(ctx.exception))
            self.assertEqual(actlog.read().revision, revision)
            # Re-adopting the successor is written.
            again = _Log()
            again.acts = list(log.acts)
            again.adopt(self.packages[V2], self.release, revision=3, supersedes=adopt_v2)
            self.assertEqual(actlog.append(again.acts[-1], revision), revision + 1)

    def test_batch_fold_follows_the_package_in_force(self) -> None:
        # One save: v1 adopted, then superseded by v2, then a statement only v2
        # admits. The save's incremental fold must apply the members under v2's
        # maps, as ``project`` of the same prefix does.
        schemas = _schemas()
        registry = tax_registry()
        registry.companion_presence_pairs[SRC] = COMP
        registry.companion_value_domains[COMP] = frozenset({None, 0, 0.0})
        registry.package_companion_declarations.update(schemas.registry.package_companion_declarations)
        log = _Log()
        adopt_v1 = log.adopt(self.packages[V1], self.release, revision=1)
        adopt_v2 = log.adopt(self.packages[V2], self.release, revision=2, supersedes=adopt_v1)
        _statement_acts(companion=50, log=log)
        with TemporaryDirectory() as tmp:
            actlog = ActLog(Path(tmp), registry)
            self.assertEqual(actlog.append_batch(log.acts, 0), len(log.acts))
            project(actlog.read().acts, registry)
            # A later save that re-adopts v1 is refused and writes nothing.
            earlier = _Log()
            earlier.acts = list(log.acts)
            earlier.adopt(self.packages[V1], self.release, revision=3, supersedes=adopt_v2)
            with self.assertRaises(FindingModelError) as ctx:
                actlog.append_batch(earlier.acts[-1:], len(log.acts))
            self.assertIn(COMP, str(ctx.exception))
            self.assertEqual(actlog.read().revision, len(log.acts))

    def test_member_written_under_earlier_package_is_refused_at_append(self) -> None:
        schemas = _schemas()
        registry = tax_registry()
        registry.companion_presence_pairs[SRC] = COMP
        registry.companion_value_domains[COMP] = frozenset({None, 0, 0.0})
        registry.package_companion_declarations.update(schemas.registry.package_companion_declarations)
        log = _Log()
        log.adopt(self.packages[V1], self.release, revision=1)
        with self.assertRaises(FindingModelError) as ctx:
            _statement_acts(companion=50, log=log)
            with TemporaryDirectory() as tmp:
                actlog = ActLog(Path(tmp), registry)
                revision = 0
                for act in log.acts:
                    revision = actlog.append(act, revision)
        self.assertIn(COMP, str(ctx.exception))


class TestProvenanceFollowsPackage(_Surface):
    def _corrected(self, base: _Log, fact_type: str, finding_id: str, value: Any) -> _Log:
        base.assertion(finding_id, fact_type, value)
        return base

    def test_correcting_companion_rederives_under_earlier_package(self) -> None:
        # Companion 0 -> corrected to 0.0 (a plain assertion on the same fact).
        before_log = _statement_acts(companion=0)
        _, before = self.run_under(V1, before_log, "demo-p1-b")
        pins_before = _input_pin_ids(_disposition(before, RULE_A))
        self.assertIn("demo.cmp.f.companion", pins_before)
        corrected = self._corrected(_statement_acts(companion=0), COMP, "demo.cmp.f.companion-corrected", 0.0)
        _, after = self.run_under(V1, corrected, "demo-p1-c")
        pins_after = _input_pin_ids(_disposition(after, RULE_A))
        self.assertIn("demo.cmp.f.companion-corrected", pins_after)
        self.assertNotIn("demo.cmp.f.companion", pins_after)

    def test_correcting_companion_rederives_under_successor_package(self) -> None:
        _, before = self.run_under(V2, _statement_acts(companion=50), "demo-p2-a")
        self.assertIn("demo.cmp.f.companion", _input_pin_ids(_disposition(before, RULE_A)))
        corrected = self._corrected(_statement_acts(companion=50), COMP, "demo.cmp.f.companion-corrected", 80)
        outcome, after = self.run_under(V2, corrected, "demo-p2-b")
        pins_after = _input_pin_ids(_disposition(after, RULE_A))
        self.assertIn("demo.cmp.f.companion-corrected", pins_after)
        self.assertNotIn("demo.cmp.f.companion", pins_after)
        self.assertEqual(_published(outcome, PUB_B), [80])

    def test_successor_companion_pinned_for_its_own_pair(self) -> None:
        _, report = self.run_under(V3, _statement_acts(companion=None, alt=3), "demo-p3-a")
        self.assertIn("demo.cmp.f.alt", _input_pin_ids(_disposition(report, RULE_A)))
        corrected = self._corrected(_statement_acts(companion=None, alt=3), COMP_ALT, "demo.cmp.f.alt-corrected", 4)
        _, after = self.run_under(V3, corrected, "demo-p3-b")
        pins_after = _input_pin_ids(_disposition(after, RULE_A))
        self.assertIn("demo.cmp.f.alt-corrected", pins_after)
        self.assertNotIn("demo.cmp.f.alt", pins_after)


class TestNoAdoptionAct(unittest.TestCase):
    """A log with no adoption act has no package in force: the global maps apply."""

    def test_projection_without_adoption_uses_global_maps(self) -> None:
        schemas = _schemas()
        log = _statement_acts(companion=50)
        with self.assertRaises(FindingModelError) as ctx:
            project(tuple(log.acts), schemas.registry)
        self.assertIn(COMP, str(ctx.exception))
        # The same log projects once a package that declares the wider domain
        # is adopted, and the shared registry is not changed by either call.
        surface_root = TemporaryDirectory()
        self.addCleanup(surface_root.cleanup)
        _, packages, release = _build_surface(Path(surface_root.name) / "s")
        log.adopt(packages[V2], release, revision=len(log.acts) + 1)
        project(tuple(log.acts), schemas.registry)
        self.assertEqual(schemas.registry.companion_value_domains[COMP], frozenset({None, 0, 0.0}))
        with self.assertRaises(FindingModelError):
            project(tuple(log.acts[:-1]), schemas.registry)

    def test_registry_without_declarations_ignores_adoption(self) -> None:
        schemas = _schemas(declare=False)
        surface_root = TemporaryDirectory()
        self.addCleanup(surface_root.cleanup)
        _, packages, release = _build_surface(Path(surface_root.name) / "s")
        log = _statement_acts(companion=50)
        log.adopt(packages[V2], release, revision=len(log.acts) + 1)
        with self.assertRaises(FindingModelError):
            project(tuple(log.acts), schemas.registry)

    def test_malformed_declaration_fails_closed(self) -> None:
        schemas = _schemas(declare=False)
        schemas.registry.package_companion_declarations[(PACKAGE_ID, V2)] = {"presence_pair": {}}
        surface_root = TemporaryDirectory()
        self.addCleanup(surface_root.cleanup)
        _, packages, release = _build_surface(Path(surface_root.name) / "s")
        log = _statement_acts(companion=0)
        log.adopt(packages[V2], release, revision=len(log.acts) + 1)
        with self.assertRaises(FindingModelError) as ctx:
            project(tuple(log.acts), schemas.registry)
        self.assertIn("malformed", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
