"""Delta construction, ownership and full-rebuild differential regressions."""
from __future__ import annotations

from collections import Counter
from contextlib import ExitStack, contextmanager, nullcontext
from copy import deepcopy
from dataclasses import asdict, dataclass, replace
import gc
import json
from pathlib import Path
import random
import threading
from typing import Any, Callable, Iterator, Mapping, cast
from unittest.mock import patch
import weakref

import pytest
import jsonschema

from packages.derivation.loader import DerivationSchemas
from packages.kernel import currency, facts, findings
from packages.kernel import schema_registry
from packages.kernel.schema_registry import SchemaRegistry
from packages.tax.loader import (
    install_domain_scoped_supersession, install_domain_companion_presence,
    install_domain_companion_equalities, install_domain_declaration_signal_contradictions,
)
from tests import test_assertion_standing_track0 as standing
from tests.support import act, demo_bundle, demo_entity, demo_finding

ROOT = Path(__file__).resolve().parents[1]
LOGS = sorted((ROOT / "packages/sample_data").glob("**/acts*.jsonl"))


def _canonical(value: Any) -> bytes:
    def tree(item: Any) -> Any:
        if isinstance(item, dict):
            return ["mapping", [[tree(k), tree(v)] for k, v in item.items()]]
        if isinstance(item, (tuple, list)):
            return [type(item).__name__, [tree(v) for v in item]]
        if isinstance(item, (set, frozenset)):
            return [type(item).__name__, sorted((tree(v) for v in item), key=lambda v: json.dumps(v, sort_keys=True))]
        return item
    return json.dumps(tree(value), separators=(",", ":"), allow_nan=False).encode()


def _ordered(lattice: Mapping[str, facts.Fact]) -> bytes:
    return _canonical([(key, asdict(row)) for key, row in lattice.items()])


# Only the loader's unextended validator class/default instance configuration
# is a reusable phase. This is a bounded library configuration assumption, not
# a fingerprint for arbitrary executable validator policies.
_STANDARD_VALIDATOR = jsonschema.Draft202012Validator
_STANDARD_CLASS_STATE = dict(vars(_STANDARD_VALIDATOR))
_STANDARD_HANDLERS = dict(_STANDARD_VALIDATOR.VALIDATORS)
_STANDARD_META_SCHEMA = _canonical(_STANDARD_VALIDATOR.META_SCHEMA)
_STANDARD_FORMATS = dict(_STANDARD_VALIDATOR.FORMAT_CHECKER.checkers)


def _supported_validator(value: Any) -> bool:
    if type(value) is not _STANDARD_VALIDATOR:
        return False
    names = ("_ref_resolver","_registry","_resolver","_validators")
    if not all(hasattr(value,name) for name in names):
        return False
    if value.format_checker is not None or getattr(value,"_ref_resolver") is not None:
        return False
    try:
        default = _STANDARD_VALIDATOR(value.schema)
    except (TypeError, ValueError, AttributeError):
        return False
    if not all(hasattr(default,name) for name in names):
        return False
    if getattr(value,"_registry") is not getattr(default,"_registry"):
        return False
    resolver, default_resolver = getattr(value,"_resolver"),getattr(default,"_resolver")
    if type(resolver) is not type(default_resolver) or resolver != default_resolver:
        return False
    actual_handlers, expected_handlers = getattr(value,"_validators"),getattr(default,"_validators")
    if type(actual_handlers) is not list or len(actual_handlers) != len(expected_handlers):
        return False
    try:
        return all(type(actual) is tuple and len(actual) == 3
            and actual[0] is expected[0]
            and _canonical(actual[1:]) == _canonical(expected[1:])
            for actual,expected in zip(actual_handlers,expected_handlers))
    except (TypeError, ValueError):
        return False


def _state_bytes(state: findings.FindingState, lattice_bytes: tuple[bytes, bytes] | None = None) -> tuple[bytes, ...]:
    if lattice_bytes is None:
        lattice_bytes = (_ordered(facts.facts_of(state.fact_state)),
            _ordered(facts.facts_of(state.fact_state, include_displaced=True)))
    return (_canonical(asdict(state)), *lattice_bytes,
            _canonical(asdict(currency.compute_currency(state))))


def _outcome(call: Callable[[], findings.FindingState], *,
             lattice_bytes: Callable[[], tuple[bytes, bytes]] | None = None,
             full_rows: bool = False) -> tuple[Any, findings.FindingState | None]:
    try:
        state = call()
    except Exception as error:
        return ("refused", type(error).__module__, type(error).__name__, str(error)), None
    # A broken comparison/serializer must fail, not masquerade as a refusal.
    rows = None if lattice_bytes is None else lattice_bytes()
    if full_rows:
        assert lattice_bytes is None
        rows = (_ordered(facts._project_fact_lattice(state.fact_state)),
                _ordered(facts._project_fact_lattice(state.fact_state,include_displaced=True)))
    return ("accepted", _state_bytes(state, rows)), state


@contextmanager
def _full_rebuild(memo: facts._HistoricalLatticeMemo | None = None) -> Iterator[None]:
    """No candidate context or memo; oracle cannot supply candidate rows."""
    memo = facts._HistoricalLatticeMemo() if memo is None else memo
    token = facts._REPLAY_LATTICES.set(None)
    try:
        with patch.object(facts, "_replay_lattices", side_effect=nullcontext), \
                patch.object(facts, "_HISTORICAL_LATTICES", memo), \
                patch.object(findings._CurrentLatticeHolder, "for_state",
                             lambda self, state: facts._project_fact_lattice(state)), \
                patch.object(currency, "_historical_lattice_for_currency",
                             lambda state: facts._project_fact_lattice(state,include_displaced=True)):
            yield
    finally:
        facts._REPLAY_LATTICES.reset(token)


def _assert_private(state: findings.FindingState) -> None:
    replay = facts._active_lattices()
    assert replay is not None
    for index, mode in ((replay.current, False), (replay.historical, True)):
        view = index.view(state.fact_state)
        full = facts._project_fact_lattice(state.fact_state, include_displaced=mode)
        assert _ordered(view) == _ordered(full)
        assert len(view) == len(full) == len(view.materialize())
        assert all(view.get(key) == row for key, row in full.items())


@dataclass
class _ObservedReplay:
    accepted_steps: int = 0
    rows: tuple[bytes, bytes] | None = None

    def serialized(self) -> tuple[bytes, bytes]:
        if self.rows is None:
            assert self.accepted_steps == 0
            return _ordered({}), _ordered({})
        return self.rows


@contextmanager
def _observe_private(check_at: int) -> Iterator[_ObservedReplay]:
    original = findings._apply_project_act
    observed = _ObservedReplay()
    def apply(state: findings.FindingState, entry: dict[str, Any], registry: SchemaRegistry,
              holder: findings._CurrentLatticeHolder) -> findings.FindingState:
        result = original(state, entry, registry, holder)
        observed.accepted_steps += 1
        if observed.accepted_steps == check_at:
            replay = facts._active_lattices()
            assert replay is not None
            # Compare these bytes directly with the isolated oracle's rows.
            # No duplicate candidate-side full rebuild, public fallback or
            # mock call records retaining every intermediate FindingState.
            observed.rows = (_ordered(replay.current.view(result.fact_state)),
                             _ordered(replay.historical.view(result.fact_state)))
        return result
    with patch.object(findings, "_apply_project_act", apply):
        yield observed


def _registry(current: bool = False) -> SchemaRegistry:
    registry = install_domain_scoped_supersession(DerivationSchemas().registry)
    if current:
        install_domain_companion_presence(registry)
        install_domain_companion_equalities(registry)
        install_domain_declaration_signal_contradictions(registry)
    return registry


def _private_rows(state: findings.FindingState) -> tuple[bytes, bytes]:
    replay = facts._active_lattices()
    assert replay is not None
    return (_ordered(replay.current.view(state.fact_state)),
            _ordered(replay.historical.view(state.fact_state)))


def _cold_pair(prefix: tuple[dict[str, Any], ...], registry: SchemaRegistry) -> tuple[Any, findings.FindingState | None, findings.FindingState | None]:
    """Actual public entrypoints, fresh contexts and isolated states/memos."""
    with _full_rebuild():
        expected, oracle = _outcome(lambda: findings.project(deepcopy(prefix), registry),full_rows=True)
    with patch.object(facts,"_HISTORICAL_LATTICES",facts._HistoricalLatticeMemo()), _observe_private(len(prefix)) as observed:
        actual, candidate = _outcome(lambda: findings.project(deepcopy(prefix), registry), lattice_bytes=observed.serialized)
    assert actual == expected
    if actual[0] == "accepted":
        assert observed.accepted_steps == len(prefix)
    return actual, oracle, candidate


def _registry_phase(prefix: tuple[dict[str, Any], ...], registry: SchemaRegistry) -> tuple[Any, bytes] | None:
    """Reusable only for the loader's supported class/default validator state.

    Unknown registry/validator classes or nondefault runtime policy take the
    cold path. Supported schemas and registry data are then snapshotted; this
    is not a guarantee for arbitrary validator code or external global policy.
    """
    if type(registry) is not SchemaRegistry:
        return None
    try:
        standard_policy = (dict(vars(_STANDARD_VALIDATOR)) == _STANDARD_CLASS_STATE
            and dict(_STANDARD_VALIDATOR.VALIDATORS) == _STANDARD_HANDLERS
            and _canonical(_STANDARD_VALIDATOR.META_SCHEMA) == _STANDARD_META_SCHEMA
            and dict(_STANDARD_VALIDATOR.FORMAT_CHECKER.checkers) == _STANDARD_FORMATS)
    except (TypeError, ValueError, AttributeError):
        return None
    if not standard_policy or type(registry._validators) is not dict:
        return None
    if not all(_supported_validator(value) for value in registry._validators.values()):
        return None
    config = dict(vars(registry))
    config["_dirs"] = [str(path) for path in registry._dirs]
    config["_validators"] = {key:(type(value).__module__,type(value).__qualname__,value.schema)
                             for key,value in registry._validators.items()}
    try:
        return findings.package_in_force(prefix), _canonical(config)
    except (TypeError, ValueError):
        return None


def _forward_prefixes(entries: list[dict[str, Any]], registry: SchemaRegistry) -> Iterator[tuple[int, Any]]:
    """Every prefix, full-rebuild oracle; cold restart on exact registry change."""
    oracle_memo = facts._HistoricalLatticeMemo()
    candidate_memo = facts._HistoricalLatticeMemo()
    oracle = candidate = None
    previous_phase = None
    holder = findings._CurrentLatticeHolder()
    with patch.object(facts,"_HISTORICAL_LATTICES",candidate_memo), ExitStack() as contexts:
        for length in range(len(entries)+1):
            prefix = tuple(entries[:length])
            effective = findings.companion_registry_in_force(prefix,registry)
            phase = _registry_phase(prefix,effective)
            if length == 0 or phase is None or phase != previous_phase:
                contexts.close()
                contexts.enter_context(facts._replay_lattices())
                actual, oracle, candidate = _cold_pair(prefix,registry)
                oracle_memo = facts._HistoricalLatticeMemo()
                holder = findings._CurrentLatticeHolder()
                if candidate is None or oracle is None:
                    yield length, actual
                    return
                assert _private_rows(candidate) == actual[1][1:3]
            else:
                assert oracle is not None and candidate is not None
                def advance_oracle() -> findings.FindingState:
                    assert oracle is not None
                    return findings._apply_project_act(oracle,deepcopy(entries[length-1]),effective,findings._CurrentLatticeHolder())
                with _full_rebuild(oracle_memo):
                    expected, next_oracle = _outcome(advance_oracle,full_rows=True)
                # Capture the actual successor inside the context, without a
                # public facts_of fallback or retained intermediate-state list.
                def advance() -> findings.FindingState:
                    assert candidate is not None
                    return findings._apply_project_act(candidate,deepcopy(entries[length-1]),effective,holder)
                try:
                    next_candidate = advance()
                except Exception as error:
                    actual = ("refused",type(error).__module__,type(error).__name__,str(error))
                    next_candidate = None
                else:
                    assert next_candidate is not None
                    actual = ("accepted",_state_bytes(next_candidate,_private_rows(next_candidate)))
                assert actual == expected, length
                if next_oracle is None or next_candidate is None:
                    yield length,actual
                    return
                oracle,candidate = next_oracle,next_candidate
            previous_phase = phase
            yield length,actual
        assert candidate is not None
        final = actual
        cold,_,_ = _cold_pair(tuple(entries),registry)
        assert cold == final
        unknown = act(len(entries),"assertion",{"finding":demo_finding(
            finding_id="demo.delta.refused",fact_id="demo.absent|period=2025",basis="attested",evidence_ids=[])})
        refused,_,_ = _cold_pair(tuple(entries+[unknown]),registry)
        actual,_ = _outcome(lambda: findings._apply_project_act(candidate,deepcopy(unknown),effective,holder))
        assert actual == refused and actual[0] == "refused"
        assert _state_bytes(candidate,_private_rows(candidate)) == final[1]
        retried,_,_ = _cold_pair(tuple(entries),registry)
        assert retried == final


# Every-prefix state/currency serialization plus cold entrypoint checkpoints is
# an integration workload, not a fast unit test or a timing assertion.
@pytest.mark.live
@pytest.mark.parametrize("current", [False, True], ids=["historical", "current"])
@pytest.mark.parametrize("path", LOGS, ids=[str(p.relative_to(ROOT)) for p in LOGS])
def test_every_fixture_prefix_matches_isolated_full_rebuild(path: Path, current: bool) -> None:
    entries = [json.loads(line) for line in path.read_text().splitlines() if line]
    registry = _registry(current)
    previous = None
    count = 0
    for length,actual in _forward_prefixes(entries,registry):
        assert actual[0] == "accepted"
        count += 1
        if length and length % 19 == 0:
            cold,_,_ = _cold_pair(tuple(entries[:length-1]),registry)
            assert cold == previous
        previous = actual
    assert count == len(entries)+1


def _demo_state() -> facts.KernelState:
    return facts.project((act(0,"bundle-adoption",{"bundle":demo_bundle()}),
        act(1,"entity-introduced",{"entity":demo_entity("demo-corp-a","Demo")})), _registry())


def test_forward_harness_cold_restarts_for_retroactive_registry_change() -> None:
    base = _registry()
    changed = _registry()
    changed.companion_presence_pairs["demo.counterparty-payment"] = "demo.required-companion"
    entries = [act(0,"bundle-adoption",{"bundle":demo_bundle()}),
        act(1,"entity-introduced",{"entity":demo_entity("demo-corp-a","Demo")}),
        act(2,"assertion",{"finding":demo_finding(basis="attested",evidence_ids=[])}),
        act(3,"entity-introduced",{"entity":demo_entity("demo-late","Demo")})]
    # Model a prefix-selected map that retroactively refuses the earlier
    # assertion. Merely applying the last entity act would wrongly accept it.
    def select(prefix: Any, registry: SchemaRegistry) -> SchemaRegistry:
        return changed if len(prefix) >= 4 else base
    cold_lengths = []
    original = _cold_pair
    def cold(prefix: tuple[dict[str, Any], ...], registry: SchemaRegistry) -> tuple[Any, findings.FindingState | None, findings.FindingState | None]:
        cold_lengths.append(len(prefix))
        return original(prefix,registry)
    with patch.object(findings,"companion_registry_in_force",select), \
            patch(__name__+"._cold_pair",cold):
        outcomes = list(_forward_prefixes(entries,base))
        expected,_,_ = original(tuple(entries),base)
    assert [length for length,_ in outcomes] == list(range(5))
    assert all(outcome[0] == "accepted" for _,outcome in outcomes[:-1])
    assert outcomes[-1][1] == expected and expected[0] == "refused"
    assert cold_lengths == [0,4]
    assert facts._active_lattices() is None


def test_forward_harness_unknown_configuration_forces_cold_prefixes() -> None:
    registry = _registry()
    assert _registry_phase((),registry) is not None
    setattr(registry,"demo_unknown_configuration",object())
    assert _registry_phase((),registry) is None
    entries = [act(0,"bundle-adoption",{"bundle":demo_bundle()})]
    lengths = []
    original = _cold_pair
    def cold(prefix: tuple[dict[str, Any], ...], schemas: SchemaRegistry) -> tuple[Any, findings.FindingState | None, findings.FindingState | None]:
        lengths.append(len(prefix))
        return original(prefix,schemas)
    with patch(__name__+"._cold_pair",cold):
        outcomes = list(_forward_prefixes(entries,registry))
    assert all(outcome[0] == "accepted" for _,outcome in outcomes)
    assert lengths[:2] == [0,1]
    assert facts._active_lattices() is None


def test_forward_harness_transient_unknown_validator_policy_matches_cold_refusal() -> None:
    class DemoValidator:
        def __init__(self, original: Any) -> None:
            self.schema = original.schema
            self.original = original
            self.refuse = False

        def iter_errors(self, instance: Any) -> Iterator[jsonschema.ValidationError]:
            if self.refuse:
                yield jsonschema.ValidationError("demo changed validator policy")
            else:
                yield from self.original.iter_errors(instance)

    registry = _registry()
    validator = DemoValidator(registry._validators["bundle.v1"])
    registry._validators["bundle.v1"] = cast(Any,validator)
    assert _registry_phase((),registry) is None
    entries = [act(0,"bundle-adoption",{"bundle":demo_bundle()})] + [
        act(i,"entity-introduced",{"entity":demo_entity(f"demo-{i}","Demo")})
        for i in range(1,5)]

    def select(prefix: Any, unused: SchemaRegistry) -> SchemaRegistry:
        next_mode = len(prefix) == 4
        if next_mode != validator.refuse:
            schema_registry.clear_caches()
            validator.refuse = next_mode
        return registry

    try:
        with patch.object(findings,"companion_registry_in_force",select):
            observed = list(_forward_prefixes(entries,registry))
            cold,_,_ = _cold_pair(tuple(entries[:4]),registry)
            later,_,_ = _cold_pair(tuple(entries),registry)
        assert len(observed) == 5
        assert all(outcome[0] == "accepted" for _,outcome in observed[:4])
        assert observed[4][0] == 4 and observed[4][1] == cold
        assert cold[0] == "refused" and "demo changed validator policy" in cold[-1]
        assert later[0] == "accepted" and not validator.refuse
        assert facts._active_lattices() is None
    finally:
        schema_registry.clear_caches()


def test_registry_phase_rejects_nondefault_standard_validator_runtime_policy() -> None:
    # Runtime-policy mutations target the real kernel bundle validator. Loading
    # every unrelated derivation/tax schema adds cold meta-validation work but
    # no additional validator-policy kind. Keep the actual domain installers
    # and both policy snapshots; full-catalog positives remain in fixture folds.
    registry = install_domain_scoped_supersession(SchemaRegistry())
    for current in (False,True):
        if current:
            install_domain_companion_presence(registry)
            install_domain_companion_equalities(registry)
            install_domain_declaration_signal_contradictions(registry)
        assert _registry_phase((),registry) is not None
        validator = registry._validators["bundle.v1"]
        for name,value in (("format_checker",jsonschema.FormatChecker()),
                           ("_registry",object()), ("_resolver",object()),
                           ("_validators",[])):
            with patch.object(validator,name,value):
                assert _registry_phase((),registry) is None, name
        assert _registry_phase((),registry) is not None
    with patch.object(_STANDARD_VALIDATOR,"VALIDATORS",{}):
        assert _registry_phase((),registry) is None


def test_current_ownership_and_retained_views_survive_nested_mutation() -> None:
    # Same real two-act demo projection; unrelated derivation/tax schemas do
    # not participate in these kernel-state ownership and nested-mutation reads.
    registry = install_domain_scoped_supersession(SchemaRegistry())
    state = facts.project((act(0,"bundle-adoption",{"bundle":demo_bundle()}),
        act(1,"entity-introduced",{"entity":demo_entity("demo-corp-a","Demo")})), registry)
    index = facts._LatticeIndex()
    old = index.view(state)
    expected = _ordered(old)
    exposed = old.materialize()
    exposed.clear()
    # This assertion fails for the P0 retained-public-dictionary shortcut.
    assert _ordered(index.view(state)) == expected
    public = facts.facts_of(state)
    public.clear()
    assert _ordered(facts.facts_of(state)) == expected
    state.fact_types["demo.rate-choice"]["identity_keys"][0]["values"].append("2026")
    state.fact_types["demo.counterparty-payment"]["nature"] = "elective"
    state.entities["demo-corp-a"].entity["kind"] = "demo.account"
    assert _ordered(index.view(state)) == _ordered(facts._project_fact_lattice(state))
    assert _ordered(old) == expected
    state.fact_types["demo.rate-choice"]["id"] = "demo.changed-id"
    changed = index.view(state)
    full = facts._project_fact_lattice(state)
    assert _ordered(changed) == _ordered(full)
    assert all(changed.get(key) == row for key, row in full.items())


def test_historical_first_read_snapshot_identity_mutation_and_weak_cleanup() -> None:
    # This actual demo replay consumes kernel citizens only. Keep its real
    # validation/policy without compiling unrelated derivation/tax schemas.
    registry = install_domain_scoped_supersession(SchemaRegistry())
    registry.companion_presence_pairs["demo.unused"] = "demo.other"
    entries = (act(0,"bundle-adoption",{"bundle":demo_bundle()}),
        act(1,"entity-introduced",{"entity":demo_entity("demo-corp-a","Demo")}),
        act(2,"assertion",{"finding":demo_finding(basis="attested",evidence_ids=[])}))
    with _full_rebuild():
        oracle = findings.project(deepcopy(entries), registry)
        expected = _ordered(facts.facts_of(oracle.fact_state, include_displaced=True))
    memo = facts._HistoricalLatticeMemo()
    with patch.object(facts, "_HISTORICAL_LATTICES", memo):
        state = findings.project(deepcopy(entries), registry)
        assert memo._snapshot(state.fact_state) is not None
        # No public read before mutation: this fails for the initial Track 1
        # shortcut that skipped currency's first-read historical side effect.
        state.fact_state.fact_types["demo.counterparty-payment"]["nature"] = "elective"
        state.fact_state.entities["demo-corp-a"].entity["kind"] = "demo.account"
        historical = facts.facts_of(state.fact_state, include_displaced=True)
        assert _ordered(historical) == expected
        historical.pop(next(iter(historical)))
        assert facts.facts_of(state.fact_state, include_displaced=True) is historical
        with facts._replay_lattices():
            assert facts._historical_lattice_for_currency(state.fact_state) is historical
        fresh = replace(state.fact_state)
        assert _ordered(memo.for_state(fresh)) == _ordered(facts._project_fact_lattice(fresh, include_displaced=True))
        temporary = findings.project(deepcopy(entries), registry)
        ident, ref = id(temporary.fact_state), weakref.ref(temporary.fact_state)
        assert ident in memo._pending
        del temporary
        gc.collect()
        assert ref() is None and ident not in memo._pending
        ident, ref = id(fresh), weakref.ref(fresh)
        del fresh
        gc.collect()
        assert ref() is None and ident not in memo._entries


# Three full projections and a foreign-thread replay take about 1.8s locally
# and 4.9s on a loaded CI runner, past the fast-lane budget.
@pytest.mark.live
def test_nested_exception_and_thread_context_cleanup() -> None:
    state = _demo_state()
    memo = facts._HistoricalLatticeMemo()
    with patch.object(facts, "_HISTORICAL_LATTICES", memo), facts._replay_lattices():
        outer = facts._active_lattices()
        assert outer is not None
        view = facts._current_lattice_for_replay(state)
        assert isinstance(view, facts._LatticeView)
        with facts._replay_lattices():
            assert facts._active_lattices() is not outer
        assert facts._active_lattices() is outer
        findings.project((act(0,"bundle-adoption",{"bundle":demo_bundle()}),), _registry())
        assert facts._active_lattices() is outer
        with pytest.raises(facts.FactModelError):
            findings.project((act(0,"entity-superseded",{"entity_id":"demo.absent"}),), _registry())
        assert facts._active_lattices() is outer
        facts._historical_lattice_for_currency(state)
        expected = _ordered(facts._project_fact_lattice(state, include_displaced=True))
        results: list[tuple[Any, bytes]] = []
        # Copying a ContextVar does not make a foreign thread its index owner.
        from contextvars import copy_context
        context = copy_context()
        def worker() -> None:
            results.append((facts._current_lattice_for_replay(state),
                _ordered(facts.facts_of(state, include_displaced=True))))
        thread = threading.Thread(target=lambda: context.run(worker))
        thread.start()
        thread.join()
        assert results == [(None, expected)]
        assert facts._active_lattices() is outer
    assert facts._active_lattices() is None


def test_exception_after_historical_read_drops_pending_state() -> None:
    # These bundle/entity/assertion acts use real kernel schemas. Unrelated
    # derivation/tax catalog compilation does not exercise exception cleanup.
    registry = install_domain_scoped_supersession(SchemaRegistry())
    registry.companion_presence_pairs["demo.unused"] = "demo.other"
    entries = (act(0,"bundle-adoption",{"bundle":demo_bundle()}),
        act(1,"entity-introduced",{"entity":demo_entity("demo-corp-a","Demo")}),
        act(2,"assertion",{"finding":demo_finding(basis="attested",evidence_ids=[])}))
    memo = facts._HistoricalLatticeMemo()
    original = findings._apply_project_act
    def fail_after_read(state: findings.FindingState, entry: dict[str, Any], schemas: SchemaRegistry,
                        holder: findings._CurrentLatticeHolder) -> findings.FindingState:
        result = original(state,entry,schemas,holder)
        if entry["kind"] == "assertion":
            assert memo._snapshot(result.fact_state) is not None
            raise RuntimeError("demo exception after historical read")
        return result
    with patch.object(facts,"_HISTORICAL_LATTICES",memo), \
            patch.object(findings,"_apply_project_act",fail_after_read):
        with pytest.raises(RuntimeError,match="demo exception"):
            findings.project(deepcopy(entries),registry)
    gc.collect()
    assert not memo._pending
    assert facts._active_lattices() is None


# Eight acts, each state projected twice in both lattice modes, take about 1.8s
# locally and 3.9s on a loaded CI runner (quick job, PR #262), past the
# fast-lane budget.
@pytest.mark.live
def test_collision_order_backtracking_and_duplicate_declared_id_boundary() -> None:
    ft = deepcopy(demo_bundle()["fact_types"][0])
    ft["id"] = "demo.delta.cross"
    ft["identity_keys"] = [dict(name="left",kind="entity",entity_kind="demo.counterparty"),
        dict(name="right",kind="entity",entity_kind="demo.counterparty"),
        dict(name="period",kind="literal",values=["z","a","z"])]
    bundle = dict(schema="bundle.v1",id="demo.delta.bundle",label="Demo",fact_types=[ft])
    registry = _registry()
    state = facts.apply_act(facts.initial_state(), act(0,"bundle-adoption",{"bundle":bundle}), registry)
    states = [state]
    for i, entity_id in enumerate(("demo-c","demo-a,right=demo-b","demo-b,right=demo-c","demo-a|opaque")):
        state = facts.apply_act(state, act(i+1,"entity-introduced",{"entity":demo_entity(entity_id,"Demo")}), registry)
        states.append(state)
    state = facts.apply_act(state,act(5,"entity-superseded",{"entity_id":"demo-c","replacement":demo_entity("demo-new","Demo")}),registry)
    states.append(state)
    state = facts.apply_act(state,act(6,"entity-superseded",{"entity_id":"demo-new"}),registry)
    states.append(state)
    revised = deepcopy(bundle)
    revised["fact_types"][0]["nature"] = "elective"
    revised["fact_types"][0]["identity_keys"][-1]["values"] = ["a","z","a"]
    state = facts.apply_act(state,act(7,"bundle-adoption",{"bundle":revised}),registry)
    states.append(state)
    for mode in (False, True):
        index = facts._LatticeIndex(mode)
        saved = []
        for item in states + [states[2], states[-1]]:
            view = index.view(item)
            full = facts._project_fact_lattice(item, include_displaced=mode)
            assert _ordered(view) == _ordered(full)
            assert len(view) == len(full)
            assert all(view[key] == row for key, row in full.items())
            saved.append((view,_ordered(full)))
        assert all(_ordered(view) == expected for view, expected in saved)
    for schema in ("fact-type.v1","fact-type.v2","fact-type.v3"):
        import re
        assert re.fullmatch(registry.get(schema)["properties"]["id"]["pattern"], "demo.bad|id") is None
    # Defensive malformed nested mutation, not an admitted-state contract.
    state.fact_types["demo.alias"] = deepcopy(state.fact_types[ft["id"]])
    state.fact_types["demo.alias"]["nature"] = "determinable"
    view = facts._LatticeIndex().view(state)
    full = facts._project_fact_lattice(state)
    assert len(view) == len(full) == len(view.materialize())
    assert _ordered(view) == _ordered(full)
    assert all(view[key] == row for key,row in full.items())


# The one-axis case takes about 2.4s locally and 6.5s on a loaded CI runner,
# past the fast-lane budget.
@pytest.mark.live
@pytest.mark.parametrize("axes", [1,2])
def test_construction_count_is_delta_not_repeated_full_product(axes: int) -> None:
    registry = _registry()
    ft = deepcopy(demo_bundle()["fact_types"][0])
    ft["identity_keys"] = [dict(name=f"axis{i}",kind="entity",entity_kind="demo.counterparty") for i in range(axes)]
    ft["identity_keys"].append(dict(name="period",kind="literal",values=["a","z"]))
    state = facts.apply_act(facts.initial_state(),act(0,"bundle-adoption",{"bundle":dict(demo_bundle(),fact_types=[ft])}),registry)
    index = facts._LatticeIndex()
    constructor = facts.Fact
    with patch.object(facts,"Fact",wraps=constructor) as counted:
        for step in range(16):
            state = facts.apply_act(state,act(step+1,"entity-introduced",{"entity":demo_entity(f"demo-{step:04d}","Demo")}),registry)
            index.view(state)
        assert counted.call_count == 2*16**axes
        unchanged = counted.call_count
        index.view(state)
        assert counted.call_count == unchanged
    assert _ordered(index.view(state)) == _ordered(facts._project_fact_lattice(state))


# Measured with -n0 --durations=0: 1.7s call locally and 7.2s on a loaded CI
# runner (PR #264 quick job), past the fast-lane budget. Every other non-live
# test here calls in 0.6s or less; the 2.7s setup on the first test of a worker
# is the session registry warm-up in tests/conftest.py, which is not timed.
@pytest.mark.live
def test_speculative_refusal_then_retry_and_gated_retraction_are_atomic() -> None:
    registry = _registry()
    registry.family_member_predicates.add(standing.MEMBER)
    registry.companion_presence_pairs[standing.MEMBER] = "demo.delta.support"
    buddy = deepcopy(cast(dict[str, Any], standing.BUNDLE_V1["fact_types"][1]))
    buddy["id"] = "demo.delta.support"
    support: dict[str, Any] = dict(schema="bundle.v1",id="demo.delta.support-bundle",label="Demo",fact_types=[buddy])
    accepted = deepcopy(standing.base_acts()) + [act(7,"bundle-adoption",{"bundle":support}),
        act(8,"horizon-genesis",{"family":standing.FAMILY,"scope":standing.FAMILY_SCOPE,"horizon_id":"demo.atomic.h0"})]
    transition = dict(family=standing.FAMILY,scope=standing.FAMILY_SCOPE,
        member=dict(action="assert",finding=standing.fnd("demo.atomic.member",standing.MEMBER_FACT,10)),
        successor=dict(id="demo.atomic.h1",predecessor="demo.atomic.h0"))
    attempts = [act(9,"member-transition",transition),
        act(9,"assertion",{"finding":standing.fnd("demo.atomic.support","demo.delta.support|counterparty=demo-corp-a,period=2025",10)}),
        act(10,"member-transition",transition),
        act(11,"assertion",{"finding":standing.fnd("demo.atomic.gated",standing.GATED_FACT,20)}),
        act(12,"assertion",{"finding":standing.fnd("demo.atomic.closed",standing.GATE_FACT,True)}),
        standing.retraction(13,"demo.atomic.gated"),
        act(13,"entity-superseded",{"entity_id":"demo-corp-a"}),
        act(14,"entity-superseded",{"entity_id":"demo-corp-a"})]
    memo = facts._HistoricalLatticeMemo()
    outcomes = []
    with patch.object(facts,"_HISTORICAL_LATTICES",memo), facts._replay_lattices():
        state = findings.project(deepcopy(tuple(accepted)),registry)
        holder = findings._CurrentLatticeHolder()
        for entry in attempts:
            with _full_rebuild():
                expected,_ = _outcome(lambda: findings.project(deepcopy(tuple(accepted+[entry])),registry))
            before = _state_bytes(state)
            actual, successor = _outcome(lambda: findings._apply_project_act(state,deepcopy(entry),registry,holder))
            assert actual == expected
            outcomes.append(actual[0])
            if successor is not None:
                state = successor
                accepted.append(entry)
            else:
                assert _state_bytes(state) == before
            _assert_private(state)
    assert outcomes == ["refused","accepted","accepted","accepted","accepted","refused","accepted","refused"]


def _random_entry(rng: random.Random, seed: int, step: int, index: int,
                  state: findings.FindingState, bundle: dict[str, Any]) -> dict[str, Any]:
    choice = rng.randrange(9)
    live = [key for key,life in state.fact_state.entities.items()
            if life.status == "current" and life.entity["kind"] == "demo.counterparty"]
    family_key,horizon_id = next(iter(state.horizon_state.current_by_chain.items()))
    family = dict(id=family_key[0],version=family_key[1])
    scope = dict(family_key[2])
    if choice == 0 and len(live) < 9:
        return act(index,"entity-introduced",{"entity":demo_entity(f"demo-s{seed}-e{step},right=demo-c","Demo")})
    if choice == 1:
        payload: dict[str, Any] = dict(entity_id=rng.choice(list(state.fact_state.entities)))
        if rng.randrange(2):
            payload["replacement"] = demo_entity(f"demo-s{seed}-replacement{step}","Demo")
        return act(index,"entity-superseded",payload)
    if choice == 2:
        revised = deepcopy(bundle)
        for ft in revised["fact_types"]:
            ft["identity_keys"][-1]["values"] = rng.choice((["z","a","z"],["a","z"],["z"]))
            ft["nature"] = rng.choice(("elective","determinable"))
        if rng.randrange(2):
            revised["fact_types"].reverse()
        return act(index,"bundle-adoption",{"bundle":revised})
    if choice == 3:
        target = rng.choice(list(state.findings)) if state.findings else "demo.absent-finding"
        return standing.retraction(index,target)
    if choice == 4:
        members = [row for row in facts._project_fact_lattice(state.fact_state).values() if row.fact_type_id == standing.MEMBER]
        if members and rng.randrange(3):
            selected = rng.choice(members)
            member = dict(action="assert",finding=standing.fnd(f"demo-s{seed}-member{step}",selected.fact_id,rng.randrange(100)))
        else:
            known = [f["fact_id"] for f in state.findings.values() if f["fact_id"].startswith(standing.MEMBER+"|")]
            member = dict(action="remove",fact_id=rng.choice(known) if known else "demo.absent|period=2025")
        return act(index,"member-transition",dict(family=family,scope=scope,member=member,
            successor=dict(id=f"demo-s{seed}-h{step}",predecessor=horizon_id if rng.randrange(5) else "demo.stale")))
    if choice == 5:
        new_family = dict(id=family["id"],version="v"+str(int(family["version"][1:])+1))
        return act(index,"family-handover",dict(
            predecessor=dict(family=family,scope=scope,horizon_id=horizon_id),
            successor=dict(family=new_family,scope=scope,horizon_id=f"demo-s{seed}-handover{step}")))
    if choice == 6:
        return act(index,"migration-adoption",{"migration":deepcopy(standing.MIGRATION)})
    candidates = [row for row in facts._project_fact_lattice(state.fact_state).values() if row.fact_type_id != standing.MEMBER]
    selected = rng.choice(candidates)
    schema = state.fact_state.fact_types[selected.fact_type_id]["value_schema"]
    value = rng.choice(schema["enum"]) if "enum" in schema else bool(rng.randrange(2)) if schema.get("type") == "boolean" else rng.randrange(100)
    finding_id = rng.choice(list(state.findings)) if state.findings and rng.randrange(8) == 0 else f"demo-s{seed}-finding{step}"
    return act(index,"assertion",{"finding":standing.fnd(finding_id,selected.fact_id,value)})


# Actual appliers and full replay after each attempt form an integration test.
@pytest.mark.live
@pytest.mark.parametrize("seed", [7,103,20261104,93017,414141])
def test_seeded_admitted_and_refused_histories_match_full_rebuild(seed: int) -> None:
    rng = random.Random(seed)
    registry = _registry()
    registry.family_member_predicates.add(standing.MEMBER)
    cross = deepcopy(demo_bundle()["fact_types"][0])
    cross["id"] = "demo.random.cross"
    cross["identity_keys"] = [dict(name="left",kind="entity",entity_kind="demo.counterparty"),
        dict(name="right",kind="entity",entity_kind="demo.counterparty"),
        dict(name="period",kind="literal",values=["z","a","z"])]
    successor_type = dict(deepcopy(cross),id="demo.random.successor")
    bundle = dict(schema="bundle.v1",id="demo.random.bundle",label="Demo",fact_types=[cross,successor_type])
    accepted = deepcopy(standing.base_acts()) + [act(7,"bundle-adoption",{"bundle":bundle}),
        act(8,"horizon-genesis",{"family":standing.FAMILY,"scope":standing.FAMILY_SCOPE,"horizon_id":"demo.random.h0"})]
    admitted: Counter[str] = Counter()
    refused: Counter[str] = Counter()
    with patch.object(facts,"_HISTORICAL_LATTICES",facts._HistoricalLatticeMemo()), facts._replay_lattices():
        state = findings.project(deepcopy(tuple(accepted)),registry)
        holder = findings._CurrentLatticeHolder()
        for step in range(90):
            entry = _random_entry(rng,seed,step,len(accepted),state,bundle)
            with _full_rebuild():
                expected,_ = _outcome(lambda: findings.project(deepcopy(tuple(accepted+[entry])),registry))
            actual,successor = _outcome(lambda: findings._apply_project_act(state,deepcopy(entry),registry,holder))
            assert actual == expected, (seed,step,entry["kind"])
            if successor is not None:
                state = successor
                accepted.append(entry)
                admitted[entry["kind"]] += 1
            else:
                refused[entry["kind"]] += 1
            _assert_private(state)
    assert sum(admitted.values()) + sum(refused.values()) == 90
    assert sum(admitted.values()) > 0 and sum(refused.values()) > 0
    assert admitted["bundle-adoption"] and admitted["family-handover"]
    assert refused["migration-adoption"] and refused["entity-superseded"]
