"""The saturation runner: derivation becomes executable.

Eligibility is read from declared state (a rule fires when its `requires` are
all present); the runner saturates to a fixpoint, publishing each derived
value as a `derived-finding.v1` through a `derived-publication-act`
(ADR-0007/0009). Pins are built from what evaluation actually read (the
AccessLog) plus the run's adoption and governance identity — and those
identities are *passed in* as versioned inputs, never minted as constants
here (ADR-0007 decision 4; the pins audit test enforces it). Ids are
content-addressed over canonical payloads (decision 5) so a re-run or a
shuffled evaluation order yields byte-identical findings.

Blocking is contained and categorized (ADR-0006 decision 8): a rule whose
dependency never arrives, whose value is present-but-invalid, or whose empty
source set is unclosed is recorded — the run still saturates the rest. The
completion record distinguishes published, inapplicable (false guard), and
blocked dispositions (ADR-0008 decision 4).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

from packages.derivation.evaluator import (
    BLOCK_ABSENT,
    AccessLog,
    Environment,
    EvalBlocked,
    evaluate,
)
from packages.kernel.act_log import ActLog
from packages.derivation.loader import DerivationSchemas, PUBLICATION_ACT_SCHEMA
from packages.derivation.records import (
    RecordStream,
    closing_record,
    start_run,
)
from packages.derivation.source_authority import (
    ClosureFindingRecord,
    audit_collect_authority,
    resolve_closure_admissions,
)


@dataclass(frozen=True)
class InputFinding:
    """A workspace finding feeding the run: a human answer or a prior value."""

    symbol: str
    value: Any
    finding_id: str
    role: str  # "input" or "choice"


@dataclass(frozen=True)
class SourceFact:
    """One collectable raw fact instance (e.g. one W-2's box 1)."""

    name: str
    value: str
    finding_id: str


@dataclass(frozen=True)
class RunContext:
    """Everything one run reads. There is no closed-set input.

    Closure authority arrives only as adopted declaration/mapping citizens
    plus closure findings and current horizons marshalled from record
    state; the runner resolves admission internally (ADR-0014 decision 4).
    A caller cannot name a set closed — it can only present the record.
    """

    run_id: str
    rules: list[dict[str, Any]]
    parameters: dict[str, dict[str, Any]]
    canon: dict[str, dict[str, Any]]
    inputs: list[InputFinding]
    sources: list[SourceFact]
    adoption_pin: dict[str, Any]
    governance_pins: list[dict[str, Any]]
    family_declarations: list[dict[str, Any]] = field(default_factory=list)
    closure_mappings: list[dict[str, Any]] = field(default_factory=list)
    closure_findings: list[ClosureFindingRecord] = field(default_factory=list)
    current_horizons: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Publication:
    act: dict[str, Any]       # act-derived-publication payload {run_id, finding}
    finding: dict[str, Any]   # derived-finding.v1


@dataclass(frozen=True)
class RunResult:
    run_id: str
    publications: list[Publication]
    dispositions: list[dict[str, Any]]
    blocked: list[dict[str, Any]]
    stop_reason: str
    symbols: dict[str, Any] = field(default_factory=dict)


def _value_str(value: Any) -> str:
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _canonical(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _content_id(prefix: str, payload: Any) -> str:
    return prefix + hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()[:24]


def _sorted_pins(pins: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique = {(p["role"], p["id"], p["version"]): p for p in pins}
    return [unique[key] for key in sorted(unique)]


class _Run:
    """Mutable per-run state, kept off the frozen public surface."""

    def __init__(self, ctx: RunContext, schemas: DerivationSchemas) -> None:
        self.ctx = ctx
        self.schemas = schemas
        # Single dispatch: the admitted family set is computed here from
        # adopted mappings and record state; both runners share it, and no
        # other constructor path exists (ADR-0014 decision 4).
        audit_collect_authority(
            ctx.rules, ctx.closure_mappings, ctx.family_declarations
        )
        self.admissions = resolve_closure_admissions(
            ctx.closure_mappings,
            ctx.family_declarations,
            ctx.closure_findings,
            ctx.current_horizons,
        )
        self.symbols: dict[str, Any] = {i.symbol: i.value for i in ctx.inputs}
        # symbol -> (finding_id, version, pin-role) for building dependency pins
        self.symbol_pin: dict[str, tuple[str, str, str]] = {
            i.symbol: (i.finding_id, "v1", i.role) for i in ctx.inputs
        }
        self.sources: dict[str, list[str]] = {}
        self.source_fids: dict[str, list[str]] = {}
        for fact in ctx.sources:
            self.sources.setdefault(fact.name, []).append(fact.value)
            self.source_fids.setdefault(fact.name, []).append(fact.finding_id)
        self.resolved: set[str] = set()
        self.publications: list[Publication] = []
        self.dispositions: list[dict[str, Any]] = []
        self.blocked: list[dict[str, Any]] = []

    def env(self) -> Environment:
        return Environment(
            symbols=self.symbols,
            sources=self.sources,
            closed_sets=frozenset(self.admissions),
            parameters=self.ctx.parameters,
            canon=self.ctx.canon,
        )

    def pins_for(self, rule: dict[str, Any], access: AccessLog) -> list[dict[str, Any]]:
        pins: list[dict[str, Any]] = [
            {"role": rule["role"], "id": rule["id"], "version": rule["version"]}
        ]
        for name in access.refs:
            fid, ver, role = self.symbol_pin[name]
            pins.append({"role": role, "id": fid, "version": ver})
        for name in access.collects:
            for fid in self.source_fids.get(name, []):
                pins.append({"role": "input", "id": fid, "version": "v1"})
        for pid in access.parameters | access.tables:
            pins.append({"role": "parameter", "id": pid, "version": self.ctx.parameters[pid]["version"]})
        # A closure-backed zero pins the exact adopted mapping and
        # declaration versions plus the exact current closure finding it
        # stood on; the horizon identity travels in that finding's fact key
        # (ADR-0014 decision 5). Present-source paths never reach here.
        for family_id in access.closure_reads:
            admission = self.admissions[family_id]
            pins.append({"role": "package", "id": admission.mapping_id,
                         "version": admission.mapping_version})
            pins.append({"role": "package", "id": admission.declaration_id,
                         "version": admission.declaration_version})
            pins.append({"role": "input", "id": admission.closure_finding_id,
                         "version": "v1"})
        for op in access.operations:
            pins.append({"role": "operation-semantics", "id": op, "version": self.ctx.canon[op]["version"]})
        # Adoption and governance identity come from the run context — versioned
        # inputs, never constants invented here (ADR-0007 decision 4).
        pins.append(self.ctx.adoption_pin)
        pins.extend(self.ctx.governance_pins)
        return _sorted_pins(pins)

    def is_eligible(self, rule: dict[str, Any]) -> bool:
        return all(req in self.symbols for req in rule["requires"])

    def attempt(self, rule: dict[str, Any]) -> str:
        """Fire one eligible rule, recording its outcome. Returns the outcome.

        This is the single per-rule step both schedulers share: eligibility is
        the caller's precondition, everything downstream (guard, value, publish,
        pins, finding assembly) is identical regardless of traversal order — so
        two schedulers reaching a rule with the same state produce byte-identical
        findings.
        """
        rule_id = rule["id"]
        access = AccessLog()
        try:
            guard = evaluate(rule["when"], self.env(), access)
        except EvalBlocked as exc:
            self._record_blocked(rule, access, exc.category, exc.missing)
            return "blocked"
        if not guard:
            self.dispositions.append({"artifact_id": rule_id, "disposition": "inapplicable",
                                      "guard_result": False, "pins": self.pins_for(rule, access)})
            self.resolved.add(rule_id)
            return "inapplicable"
        try:
            value = evaluate(rule["value"], self.env(), access)
        except EvalBlocked as exc:
            self._record_blocked(rule, access, exc.category, exc.missing)
            return "blocked"

        symbol = rule["publishes"]
        pins = self.pins_for(rule, access)
        body = {"symbol": symbol, "value": _value_str(value), "pins": pins}
        finding = {
            "schema": "derived-finding.v1",
            "id": _content_id("finding:derived:", body),
            "symbol": symbol,
            "value": body["value"],
            "version": "v1",
            "pins": pins,
        }
        act = {"run_id": self.ctx.run_id, "finding": finding}
        self.schemas.validate(PUBLICATION_ACT_SCHEMA, act)
        self.schemas.validate_declared(finding)
        self.publications.append(Publication(act=act, finding=finding))
        self.dispositions.append({"artifact_id": rule_id, "disposition": "published", "pins": pins})
        self.symbols[symbol] = value
        # Downstream refs to this symbol pin THIS derived finding, as an input.
        self.symbol_pin[symbol] = (finding["id"], "v1", "input")
        self.resolved.add(rule_id)
        return "published"

    def _record_blocked(self, rule: dict[str, Any], access: AccessLog, code: str, missing: list[str]) -> None:
        rule_id = rule["id"]
        self.blocked.append({"artifact_id": rule_id, "code": code, "missing": missing})
        self.dispositions.append({"artifact_id": rule_id, "disposition": "blocked",
                                  "pins": self.pins_for(rule, access)})
        self.resolved.add(rule_id)

    def finalize_unreached(self) -> None:
        """Rules that never became eligible saturate blocked on their gap."""
        for rule in self.ctx.rules:
            if rule["id"] in self.resolved:
                continue
            missing = [req for req in rule["requires"] if req not in self.symbols]
            self.blocked.append({"artifact_id": rule["id"], "code": BLOCK_ABSENT, "missing": missing})
            self.dispositions.append({"artifact_id": rule["id"], "disposition": "blocked", "pins": []})

    def result(self) -> RunResult:
        return RunResult(
            run_id=self.ctx.run_id,
            publications=self.publications,
            dispositions=self.dispositions,
            blocked=self.blocked,
            stop_reason="saturated",
            symbols=self.symbols,
        )


def run(ctx: RunContext, schemas: DerivationSchemas) -> RunResult:
    """Forward, data-driven saturation: fire every eligible rule until fixpoint."""
    state = _Run(ctx, schemas)
    progress = True
    while progress:
        progress = False
        for rule in ctx.rules:
            if rule["id"] in state.resolved or not state.is_eligible(rule):
                continue
            state.attempt(rule)
            progress = True
    state.finalize_unreached()
    return state.result()


def append_publications(act_log: ActLog, result: RunResult, *, actor: str, at: str) -> int:
    """Append each publication as a `derived-publication` act-log envelope.

    ADR-0010: publication acts land in the workspace act log (ADR-0008), so
    derived findings enter the projection from the record. The envelope's actor
    and timestamp come from the persistence boundary — not the sealed runner —
    while the act_id is content-addressed over the payload, so it is stable
    across runs. Returns the new revision.
    """
    revision = act_log.read().revision
    for pub in result.publications:
        envelope = {
            "schema": "act.v1",
            "act_id": _content_id("act:publication:", pub.act),
            "kind": "derived-publication",
            "actor": actor,
            "at": at,
            "committed_against": revision,
            "payload": pub.act,
        }
        revision = act_log.append(envelope, expected_revision=revision)
    return revision


def run_and_record(
    ctx: RunContext,
    schemas: DerivationSchemas,
    stream: RecordStream,
    *,
    workspace_revision: int,
    adopted_packages: set[str],
    start_record_id: str,
    completion_record_id: str,
) -> RunResult:
    """Gate on adoption, bound the run with a started/completed record pair.

    The started record is written before any evaluation (so a crash mid-run is
    a detectable open run, ADR-0008); the completion record carries the run's
    published/blocked surface and per-rule dispositions.
    """
    start_run(
        stream,
        record_id=start_record_id,
        run_id=ctx.run_id,
        workspace_revision=workspace_revision,
        governance_pins=ctx.governance_pins,
        adoption_pin=ctx.adoption_pin,
        adopted_packages=adopted_packages,
    )
    result = run(ctx, schemas)
    published = [
        {"symbol": pub.finding["symbol"], "finding_id": pub.finding["id"],
         "act_id": _content_id("act:publication:", pub.act)}
        for pub in result.publications
    ]
    stream.append(
        closing_record(
            record_id=completion_record_id,
            run_id=ctx.run_id,
            phase="completed",
            workspace_revision=workspace_revision,
            governance_pins=ctx.governance_pins,
            adoption_pin=ctx.adoption_pin,
            stop_reason=result.stop_reason,
            published=published,
            blocked=result.blocked,
            dispositions=result.dispositions,
        )
    )
    return result
