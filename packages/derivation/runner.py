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
    BLOCK_INVALID,
    AccessLog,
    Environment,
    EvalBlocked,
    evaluate,
)
from packages.kernel.act_log import ActLog
from packages.derivation.loader import DerivationSchemas, PUBLICATION_ACT_SCHEMA
from packages.derivation.package_validation import find_covered_w_identity_key_collisions
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
    # ADR-0061 Decision 2 amended / Track 1 repair round 3: the raw
    # ADR-0011 identity-bearing fact id (`type|broker=...,statement=...,
    # transaction=...,tax-year=...`), distinct from `finding_id` (the
    # human/system-authored finding label used for pins). Optional and
    # defaulted so every existing fixture scenario JSON that omits it keeps
    # working unchanged; the identity-key collision guard is the only
    # consumer and treats an unset value as carrying no identity (never a
    # false collision).
    fact_id: str | None = None


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
    fact_types: list[dict[str, Any]] = field(default_factory=list)
    input_bindings: list[dict[str, Any]] = field(default_factory=list)


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


_LEDGER_EXCLUDED_PIN_ROLES = frozenset(
    {"computation", "applicability", "field-mapping", "cross-form-bridge"}
)

# ADR-0036: the schema tag identifying an attachment citizen. Attachment
# rules carry no `when`/`value` expression tree - they are interpreted
# directly from their declarative requirement/itemizations/completeness
# structure by `_Run.attempt_attachment`, not by `evaluate()`.
ATTACHMENT_SCHEMAS = frozenset(
    {"attachment-rule.v1", "attachment-rule.v2", "attachment-rule.v3", "attachment-rule.v4", "attachment-rule.v5", "attachment-rule.v6"}
)
ITEMIZATION_TIE_OUT_VIOLATION = "ITEMIZATION_TIE_OUT_VIOLATION"
# ADR-0055 Decision 2: a required answer present as a current finding but
# valued other than its declared required value - distinct from absence
# (DEPENDENCY_ABSENT), never folded into it, never silence.
COMPLETENESS_VALUE_VIOLATION = "COMPLETENESS_VALUE_VIOLATION"

# ADR-0062 Decision 2 / Track 1 repair (Finding 1, CRITICAL): the two Form
# 8949 validation guards - code W applied to an individually non-loss
# transaction, and a disallowed-adjustment amount exceeding that one
# transaction's own otherwise-deductible loss - must each be evaluated per
# contributing transaction, before any amount is trusted downstream. A box
# subtotal already nets every member's proceeds/basis/adjustment together;
# testing the guard against that subtotal (the original defect) lets one
# individually-invalid member hide behind another member's valid loss.
# Scoped to the exact whole-transaction families ADR-0061 Decision 2
# introduces - there is exactly one consumer of this shape today, so this is
# a targeted repair rather than a generic per-attachment mechanism. Each of
# the three consuming rules (the attachment itself, and each of lines
# 1b/8b) independently checks its own relevant box(es) the moment it is
# attempted, so the fix holds regardless of saturation order - no rule
# trusts another rule's disposition to have already screened this.
_F8949_ROW_GUARD_BOXES: dict[str, tuple[str, str]] = {
    "st": ("tax.us.2025.f1099b.covered-w-st", "tax.us.2025.f1099b.covered-w-st-txn"),
    "lt": ("tax.us.2025.f1099b.covered-w-lt", "tax.us.2025.f1099b.covered-w-lt-txn"),
}
GUARD_NONLOSS_ADJUSTMENT = "tax.us.2025.block.f8949.code-w-on-gain"
GUARD_ADJUSTMENT_EXCEEDS_LOSS = "tax.us.2025.block.f8949.adjustment-exceeds-loss"
# ADR-0061 Decision 1 / Finding 3 repair: "flag yes, no amount" and "amount
# present, flag not yes" are each independently representable (the two
# fields are independently contributable) and must each be independently
# blockable with a named code - neither combination silently passes through
# as if it were the other.
GUARD_FLAG_WITHOUT_AMOUNT = "tax.us.2025.block.f8949.box-1g-flag-without-amount"
GUARD_AMOUNT_WITHOUT_FLAG = "tax.us.2025.block.f8949.box-1g-amount-without-flag"
_LINE_GUARD_BOX_KEYS: dict[str, tuple[str, ...]] = {
    "tax.us.2025.rule.schedule-d-line1b": ("st",),
    "tax.us.2025.rule.schedule-d-line8b": ("lt",),
}

# ADR-0061 Decision 2 amended (Track 1 repair round 3): the identity-key
# collision kill-test (`find_covered_w_identity_key_collisions`) is correct
# in isolation but was never supplied a run's actually-asserted fact ids -
# `resolve_production_package` validates the package/citizen graph once,
# independent of any run, and structurally cannot see per-run collisions.
# This wires the same, already-tested comparison into the live run path,
# reusing `_LINE_GUARD_BOX_KEYS`'s box-scoping so each of the three
# `_f8949_row_guard_violations` call sites (attempt, attempt_attachment,
# finalize_unreached) checks it too, and no rule trusts another's
# disposition to have already screened it.
_COVERED_W_IDENTITY_COLLISION_BOX_TYPES: dict[str, tuple[str, str]] = {
    "st": ("tax.us.2025.f1099b.covered-st-txn", "tax.us.2025.f1099b.covered-w-st-txn"),
    "lt": ("tax.us.2025.f1099b.covered-lt-txn", "tax.us.2025.f1099b.covered-w-lt-txn"),
}
GUARD_IDENTITY_KEY_COLLISION = "tax.us.2025.block.covered-w.identity-key-collision"


def _uses_attachment_machinery(rules: list[dict[str, Any]]) -> bool:
    return any(rule.get("schema") in ATTACHMENT_SCHEMAS for rule in rules)


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
        
        self.use_v2 = any(
            rule.get("schema") in {"rule-artifact.v2", "rule-artifact.v3"}
            for rule in ctx.rules
        ) or _uses_attachment_machinery(ctx.rules)
        self.symbol_fact_types: dict[str, str] = {}
        self.categorical_domains: dict[str, list[str]] = {}
        
        fact_types_by_id = {ft["id"]: ft for ft in ctx.fact_types}
        for ft in ctx.fact_types:
            val_schema = ft.get("value_schema", {})
            if isinstance(val_schema, dict) and "enum" in val_schema:
                self.categorical_domains[ft["id"]] = val_schema["enum"]

        self.symbols: dict[str, Any] = {}
        # symbol -> (finding_id, version, pin-role, provenance)
        self.symbol_pin: dict[str, tuple[str, str, str, str | None]] = {}
        
        for i in ctx.inputs:
            self.symbols[i.symbol] = i.value
            fact_type_id = i.symbol
            for binding in ctx.input_bindings:
                if binding["symbol"] == i.symbol:
                    fact_type_id = binding["fact_type"]["id"]
                    break
            self.symbol_fact_types[i.symbol] = fact_type_id
            provenance = "assertion" if self.use_v2 else None
            self.symbol_pin[i.symbol] = (i.finding_id, "v1", i.role, provenance)

        self.publications: list[Publication] = []
        
        if self.use_v2:
            for binding in ctx.input_bindings:
                symbol = binding["symbol"]
                if symbol in self.symbols:
                    continue
                if binding["mode"] == "optional_default":
                    fact_type_id = binding["fact_type"]["id"]
                    self.symbol_fact_types[symbol] = fact_type_id
                    ft_def: dict[str, Any] | None = fact_types_by_id.get(fact_type_id)
                    if ft_def is not None and "optional_default" in ft_def:
                        opt_def = ft_def["optional_default"]
                        param_id = opt_def["parameter"]["id"]
                        param_version = opt_def["parameter"]["version"]
                        param_val = ctx.parameters.get(param_id, {}).get("values")
                        if param_val is not None:
                            pins = [self.ctx.adoption_pin] + self.ctx.governance_pins
                            pins.append({
                                "role": "parameter",
                                "id": param_id,
                                "version": param_version
                            })
                            pins = _sorted_pins(pins)

                            body = {
                                "symbol": symbol,
                                "value": _value_str(param_val),
                                "pins": pins,
                                "resolved_input": {
                                    "fact_id": fact_type_id,
                                    "origin": "declared_default"
                                }
                            }
                            finding_id = _content_id("finding:derived:", body)
                            finding = {
                                "schema": "derived-finding.v2",
                                "id": finding_id,
                                "symbol": symbol,
                                "value": body["value"],
                                "version": "v2",
                                "pins": pins,
                                "resolved_input": body["resolved_input"]
                            }
                            self.schemas.validate_declared(finding)
                            act = {"run_id": self.ctx.run_id, "finding": finding}
                            self.publications.append(Publication(act=act, finding=finding))
                            self.symbols[symbol] = param_val
                            self.symbol_pin[symbol] = (finding_id, "v2", "input", "declared_default")

        self.sources: dict[str, list[str]] = {}
        self.source_fids: dict[str, list[str]] = {}
        # ADR-0061 Decision 2 amended / Track 1 repair round 3: the raw
        # ADR-0011 fact ids actually asserted this run, keyed the same way
        # as `self.sources`/`self.source_fids` - the identity-key collision
        # guard's only consumer. Falls back to `finding_id` (never a real
        # identity string) when a source carries no `fact_id`, so an absent
        # value can never manufacture a false collision.
        self.source_fact_ids: dict[str, list[str]] = {}
        for fact in ctx.sources:
            self.sources.setdefault(fact.name, []).append(fact.value)
            self.source_fids.setdefault(fact.name, []).append(fact.finding_id)
            self.source_fact_ids.setdefault(fact.name, []).append(
                fact.fact_id if fact.fact_id is not None else fact.finding_id
            )
        self.resolved: set[str] = set()
        self.dispositions: list[dict[str, Any]] = []
        self.blocked: list[dict[str, Any]] = []
        self.symbol_publisher: dict[str, dict[str, Any]] = {}

    def env(self) -> Environment:
        return Environment(
            symbols=self.symbols,
            sources=self.sources,
            closed_sets=frozenset(self.admissions),
            parameters=self.ctx.parameters,
            canon=self.ctx.canon,
            symbol_fact_types=self.symbol_fact_types,
            categorical_domains=self.categorical_domains,
        )

    def pins_for(self, rule: dict[str, Any], access: AccessLog) -> list[dict[str, Any]]:
        pins: list[dict[str, Any]] = [
            {"role": rule["role"], "id": rule["id"], "version": rule["version"]}
        ]
        for name in access.refs:
            # A blocked evaluation can have read a declared ref only far
            # enough to establish that no current finding exists.  Absence is
            # recorded in the disposition's missing list; it has no finding
            # identity to pin.  Present refs retain their ordinary pins.
            source = self.symbol_pin.get(name)
            if source is None:
                continue
            fid, ver, role, provenance = source
            pin = {"role": role, "id": fid, "version": ver}
            if self.use_v2 and role == "input":
                pin["origin"] = provenance if provenance is not None else "assertion"
            pins.append(pin)
        for name in access.collects:
            for fid in self.source_fids.get(name, []):
                pin = {"role": "input", "id": fid, "version": "v1"}
                if self.use_v2:
                    pin["origin"] = "assertion"
                pins.append(pin)
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
            pin = {"role": "input", "id": admission.closure_finding_id,
                   "version": "v1"}
            if self.use_v2:
                pin["origin"] = "assertion"
            pins.append(pin)
        for op in access.operations:
            pins.append({"role": "operation-semantics", "id": op, "version": self.ctx.canon[op]["version"]})
        # Declared rule citations (ADR-0029 / ADR-0050 line-7b exact citation pin).
        for citation in rule.get("citations", []):
            pins.append({
                "role": "citation",
                "id": citation["id"],
                "version": citation["version"],
            })
        # Adoption and governance identity come from the run context — versioned
        # inputs, never constants invented here (ADR-0007 decision 4).
        pins.append(self.ctx.adoption_pin)
        pins.extend(self.ctx.governance_pins)
        return _sorted_pins(pins)

    def ledger_pins_for(self, rule: dict[str, Any], access: AccessLog) -> list[dict[str, Any]]:
        """Return v2 disposition evidence in the record schema's pin vocabulary."""
        pins = self.pins_for(rule, access)
        if not self.use_v2:
            return pins
        return [pin for pin in pins if pin["role"] not in _LEDGER_EXCLUDED_PIN_ROLES]

    def _requires(self, rule: dict[str, Any]) -> list[str]:
        """Ordinary rules declare `requires` directly; an attachment rule has
        no such field - its eligibility gate is exactly the requirement
        conditional's subtotal symbols (ADR-0036 decision 2), which are also
        every itemization's tie-out line symbol in this milestone's content."""
        if rule.get("schema") in ATTACHMENT_SCHEMAS:
            requirement = rule["requirement"]
            # Threshold requirement: eligibility gates on its subtotal
            # symbols. Categorical family_nonempty requirement (ADR-0053
            # Decision 1) gates on nothing upfront - attempt_attachment
            # reads closure/membership state directly and blocks honestly
            # if the pinned family is unclosed.
            symbols = list(requirement.get("subtotals", []))
            if rule.get("schema") in ("attachment-rule.v2", "attachment-rule.v3", "attachment-rule.v4", "attachment-rule.v5", "attachment-rule.v6"):
                for part in rule["itemizations"]:
                    symbols.append(part["tie_out"]["line_symbol"])
                    symbols.extend(row_set["subtotal_symbol"] for row_set in part["row_sets"])
                    if rule.get("schema") == "attachment-rule.v6":
                        symbols.extend(
                            row["subtotal_symbol"] for row in part["adjustment_rows"]
                        )
                        symbols.extend(part["tie_out"]["positive_subtotals"])
                        symbols.extend(part["tie_out"]["adjustment_subtotals"])
            return sorted(set(symbols))
        return list(rule["requires"])

    def is_eligible(self, rule: dict[str, Any]) -> bool:
        return all(req in self.symbols for req in self._requires(rule))

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

        # Finding 1 repair (ADR-0062 Decision 2): lines 1b/8b each screen
        # their own box's contributing transactions independently, the
        # moment they are attempted - never by trusting the Form 8949
        # attachment's disposition to have already run first (saturation
        # order is not guaranteed), and never against the already-netted
        # subtotal a masking scenario could exploit.
        line_guard_boxes = _LINE_GUARD_BOX_KEYS.get(rule_id)
        if line_guard_boxes is not None:
            violated_codes, violation_pins = self._f8949_row_guard_violations(line_guard_boxes)
            if violated_codes:
                self._record_blocked(rule, access, BLOCK_INVALID, violated_codes)
                return "blocked"
            collision_codes, collision_pins = self._covered_w_identity_key_collision_violations(
                line_guard_boxes
            )
            if collision_codes:
                self._record_blocked(rule, access, BLOCK_INVALID, collision_codes)
                return "blocked"

        # 1. If any declared dependency is absent -> blocked
        missing = [req for req in rule["requires"] if req not in self.symbols]
        if missing:
            self._record_blocked(rule, access, "DEPENDENCY_ABSENT", missing)
            return "blocked"

        # 2. Else, if the output symbol is already published by another producer under conflict semantics
        symbol = rule["publishes"]
        if symbol in self.symbols:
            winner = self.symbol_publisher.get(symbol)
            disposition_row = {
                "artifact_id": rule_id,
                "disposition": "inapplicable",
                "pins": []
            }
            if self.use_v2:
                if winner:
                    disposition_row["superseded_by"] = {"role": "package", "id": winner["id"], "version": winner["version"]}
            self.dispositions.append(disposition_row)
            self.resolved.add(rule_id)
            return "inapplicable"

        # 3. Evaluate guard
        try:
            guard = evaluate(rule["when"], self.env(), access)
        except EvalBlocked as exc:
            self._record_blocked(rule, access, exc.category, exc.missing)
            return "blocked"
        if not guard:
            disposition_row = {
                "artifact_id": rule_id,
                "disposition": "inapplicable",
                "guard_result": False,
                "pins": self.ledger_pins_for(rule, access)
            }
            self.dispositions.append(disposition_row)
            self.resolved.add(rule_id)
            return "inapplicable"

        # 4. Evaluate value
        try:
            value = evaluate(rule["value"], self.env(), access)
        except EvalBlocked as exc:
            self._record_blocked(rule, access, exc.category, exc.missing)
            return "blocked"

        pins = self.pins_for(rule, access)
        
        provenance = "assertion"
        if self.use_v2:
            for pin in pins:
                if pin.get("role") == "input" and pin.get("origin") == "declared_default":
                    provenance = "declared_default"
                    break

        schema_ver = "v2" if self.use_v2 else "v1"
        body = {"symbol": symbol, "value": _value_str(value), "pins": pins}
        finding = {
            "schema": f"derived-finding.{schema_ver}",
            "id": _content_id("finding:derived:", body),
            "symbol": symbol,
            "value": body["value"],
            "version": schema_ver,
            "pins": pins,
        }
        act = {"run_id": self.ctx.run_id, "finding": finding}
        if self.use_v2:
            self.schemas.validate_declared(finding)
        else:
            self.schemas.validate(PUBLICATION_ACT_SCHEMA, act)
            self.schemas.validate_declared(finding)
        self.publications.append(Publication(act=act, finding=finding))

        self.symbol_publisher[symbol] = rule

        disposition_row = {
            "artifact_id": rule_id,
            "disposition": "published",
            "pins": self.ledger_pins_for(rule, access)
        }
        if self.use_v2:
            disposition_row["finding_id"] = finding["id"]
            disposition_row["act_id"] = _content_id("act:publication:", act)
            disposition_row["symbol"] = symbol
        self.dispositions.append(disposition_row)

        self.symbols[symbol] = value
        # Downstream refs to this symbol pin THIS derived finding, as an input.
        self.symbol_pin[symbol] = (finding["id"], schema_ver, "input", provenance if self.use_v2 else None)
        self.resolved.add(rule_id)
        return "published"

    def _symbol_pin_entry(self, symbol: str) -> dict[str, Any]:
        fid, ver, role, provenance = self.symbol_pin[symbol]
        pin: dict[str, Any] = {"role": role, "id": fid, "version": ver}
        if self.use_v2 and role == "input":
            pin["origin"] = provenance if provenance is not None else "assertion"
        return pin

    def _attachment_block(self, rule_id: str, code: str, missing: list[str], pins: list[dict[str, Any]]) -> None:
        self.blocked.append({"artifact_id": rule_id, "code": code, "missing": missing})
        self.dispositions.append({
            "artifact_id": rule_id,
            "disposition": "blocked",
            "code": code,
            "missing": missing,
            "pins": _sorted_pins(pins),
        })
        self.resolved.add(rule_id)

    def _attachment_family_nonempty_trigger(
        self,
        rule_id: str,
        requirement: dict[str, Any],
        governance_pins: list[dict[str, Any]],
    ) -> tuple[bool, list[dict[str, Any]], list[dict[str, Any]], str | None]:
        """ADR-0053 Decision 1: categorical `family_nonempty` requirement.

        Required when the pinned source family is current and closed with
        at least one member; not required when current and closed-empty;
        blocked (never a silent default) when unclosed. Reuses the same
        generic closure-admission and collectible-source state `collect`
        and `require_closed` already read - no new evaluator operation or
        generic substrate.

        Returns ``(required, base_pins, triggers, outcome)``. When
        ``outcome`` is not ``None`` the blocked/inapplicable disposition has
        already been recorded and the caller must return that outcome
        immediately.
        """
        family_id = requirement["source_family"]["id"]
        citation = requirement["citation"]

        if family_id not in self.admissions:
            self._attachment_block(rule_id, BLOCK_ABSENT, [family_id], governance_pins)
            return False, [], [], "blocked"

        admission = self.admissions[family_id]
        declaration = next(
            d for d in self.ctx.family_declarations if d["id"] == family_id
        )
        member_fact_type_id = declaration["member_predicate"]["fact_type"]
        member_values = self.sources.get(member_fact_type_id, [])
        required = len(member_values) > 0

        base_pins: list[dict[str, Any]] = [
            {"role": "package", "id": admission.mapping_id, "version": admission.mapping_version},
            {"role": "package", "id": admission.declaration_id, "version": admission.declaration_version},
        ]
        closure_pin = {"role": "input", "id": admission.closure_finding_id, "version": "v1"}
        if self.use_v2:
            closure_pin["origin"] = "assertion"
        base_pins.append(closure_pin)
        base_pins.append({"role": "citation", "id": citation["id"], "version": citation["version"]})
        base_pins.append(self.ctx.adoption_pin)
        base_pins.extend(self.ctx.governance_pins)

        triggers = [{
            "source_family": family_id,
            "member_count": len(member_values),
            "over": required,
        }]
        return required, base_pins, triggers, None

    def _f8949_row_guard_violations(
        self, box_keys: tuple[str, ...] = ("st", "lt")
    ) -> tuple[list[str], list[dict[str, Any]]]:
        """Per-transaction ADR-0062 Decision 2 guard evaluation (Finding 1
        repair): each ``covered-w-st``/``covered-w-lt`` member is read from
        its own single whole-transaction finding (proceeds/basis/adjustment
        co-located there), never from a box's already-netted subtotal, so an
        individually-invalid member can never hide behind another member's
        valid loss. Returns the sorted, deduplicated violated block codes
        and the input pins of every transaction actually read.
        """
        violated: set[str] = set()
        pins: list[dict[str, Any]] = []
        for box_key in box_keys:
            _family_id, member_fact_type = _F8949_ROW_GUARD_BOXES[box_key]
            raw_values = self.sources.get(member_fact_type, [])
            fids = self.source_fids.get(member_fact_type, [])
            for raw, fid in zip(raw_values, fids):
                member = json.loads(raw)
                d = Decimal(str(member["proceeds"]))
                e = Decimal(str(member["basis"]))
                flag = member.get("box_1g_wash_sale_adjustment")
                has_amount = "box_1g_wash_sale_disallowed_amount" in member
                g = Decimal(str(member.get("box_1g_wash_sale_disallowed_amount", 0)))
                row_violated = False
                # Flag/amount independence (Finding 3): each asymmetric
                # combination is its own named, structurally blockable
                # state - never folded into the other, never silently
                # treated as the well-formed case.
                if flag == "yes" and not has_amount:
                    violated.add(GUARD_FLAG_WITHOUT_AMOUNT)
                    row_violated = True
                if has_amount and flag != "yes":
                    violated.add(GUARD_AMOUNT_WITHOUT_FLAG)
                    row_violated = True
                if g > 0 and d >= e:
                    violated.add(GUARD_NONLOSS_ADJUSTMENT)
                    row_violated = True
                if g > max(e - d, Decimal(0)):
                    violated.add(GUARD_ADJUSTMENT_EXCEEDS_LOSS)
                    row_violated = True
                if row_violated:
                    pin = {"role": "input", "id": fid, "version": "v1"}
                    if self.use_v2:
                        pin["origin"] = "assertion"
                    pins.append(pin)
        return sorted(violated), pins

    def _covered_w_identity_key_collision_violations(
        self, box_keys: tuple[str, ...] = ("st", "lt")
    ) -> tuple[list[str], list[dict[str, Any]]]:
        """Per-run ADR-0061 Decision 2 amended identity-key collision guard
        (Track 1 repair round 3): reuses
        ``package_validation.find_covered_w_identity_key_collisions`` -
        never reimplements the identity-key comparison - against this run's
        own asserted fact ids for the direct-reporting and wash-sale
        transaction fact types. A collision means the same real transaction
        (broker/statement/transaction/tax-year) was asserted into both a
        direct-reporting family and its wash-sale counterpart; that can
        never be inferred from version supersession, only from contributed
        identity, so this must read the raw fact ids actually asserted this
        run - `self.source_fact_ids`, not `self.source_fids` (which holds
        finding ids, used only for pins, and carries no identity keys).
        """
        fact_types: set[str] = set()
        for box_key in box_keys:
            direct_type, w_type = _COVERED_W_IDENTITY_COLLISION_BOX_TYPES[box_key]
            fact_types.add(direct_type)
            fact_types.add(w_type)
        asserted_fact_ids = {ft: self.source_fact_ids.get(ft, []) for ft in fact_types}
        issues = find_covered_w_identity_key_collisions(asserted_fact_ids)
        if not issues:
            return [], []
        pins: list[dict[str, Any]] = []
        seen_fids: set[str] = set()
        for ft in sorted(fact_types):
            for fid in self.source_fids.get(ft, []):
                if fid in seen_fids:
                    continue
                seen_fids.add(fid)
                pin = {"role": "input", "id": fid, "version": "v1"}
                if self.use_v2:
                    pin["origin"] = "assertion"
                pins.append(pin)
        return [GUARD_IDENTITY_KEY_COLLISION], pins

    def attempt_attachment(self, rule: dict[str, Any]) -> str:
        """Interpret one ADR-0036 attachment citizen directly from its
        declarative requirement/itemizations/completeness structure.

        Three atomic outcomes on the ratified triad, never an embedded state
        field: not-required is `inapplicable` (the ordinary guard_inapplicable
        family every other rule already uses when its guard evaluates false);
        required-and-incomplete is `blocked`, naming exactly the missing
        required answers (reusing DEPENDENCY_ABSENT - no new vocabulary);
        required-and-complete is `published`, pinned to every subtotal,
        itemization row, and Part III answer consumed. A tie-out mismatch
        hard-fails the attachment only (ITEMIZATION_TIE_OUT_VIOLATION),
        checked only once completeness already holds.
        """
        rule_id = rule["id"]
        requirement = rule["requirement"]

        governance_pins = [self.ctx.adoption_pin] + list(self.ctx.governance_pins)

        if requirement.get("kind") == "family_nonempty":
            required, base_pins, triggers, outcome = self._attachment_family_nonempty_trigger(
                rule_id, requirement, governance_pins
            )
            if outcome is not None:
                return outcome
        else:
            subtotal_symbols: list[str] = requirement["subtotals"]

            missing_subtotals = [s for s in subtotal_symbols if s not in self.symbols]
            if missing_subtotals:
                self._attachment_block(rule_id, BLOCK_ABSENT, missing_subtotals, governance_pins)
                return "blocked"

            threshold_pin = requirement["threshold_parameter"]
            threshold_param = self.ctx.parameters.get(threshold_pin["id"])
            if threshold_param is None:
                self._attachment_block(rule_id, BLOCK_ABSENT, [threshold_pin["id"]], governance_pins)
                return "blocked"
            threshold = Decimal(str(threshold_param["values"]))

            base_pins = [self._symbol_pin_entry(s) for s in subtotal_symbols]
            base_pins.append({"role": "parameter", "id": threshold_pin["id"], "version": threshold_pin["version"]})
            citation = requirement["citation"]
            base_pins.append({"role": "citation", "id": citation["id"], "version": citation["version"]})
            base_pins.append(self.ctx.adoption_pin)
            base_pins.extend(self.ctx.governance_pins)

            # The requirement conditional is an "any subtotal over threshold"
            # test with a per-trigger outcome recorded, never silence about
            # which subtotal(s) crossed it (deliverable 5).
            triggers = [
                {"subtotal": s, "value": _value_str(self.symbols[s]),
                 "over": Decimal(str(self.symbols[s])) > threshold}
                for s in subtotal_symbols
            ]
            required = any(t["over"] for t in triggers)

        if not required:
            self.dispositions.append({
                "artifact_id": rule_id,
                "disposition": "inapplicable",
                "guard_result": False,
                "pins": _sorted_pins(base_pins),
            })
            self.resolved.add(rule_id)
            return "inapplicable"

        itemization_pins: list[dict[str, Any]] = []
        if rule["schema"] in ("attachment-rule.v2", "attachment-rule.v3", "attachment-rule.v4", "attachment-rule.v5", "attachment-rule.v6"):
            itemization_symbols = sorted({
                symbol
                for part in rule["itemizations"]
                for symbol in (
                    part["tie_out"]["line_symbol"],
                    *(row_set["subtotal_symbol"] for row_set in part["row_sets"]),
                )
            })
            if rule["schema"] == "attachment-rule.v6":
                itemization_symbols = sorted(set(itemization_symbols) | {
                    symbol
                    for part in rule["itemizations"]
                    for symbol in (
                        *(row["subtotal_symbol"] for row in part["adjustment_rows"]),
                        *part["tie_out"]["positive_subtotals"],
                        *part["tie_out"]["adjustment_subtotals"],
                    )
                })
            missing_itemization = [symbol for symbol in itemization_symbols if symbol not in self.symbols]
            if missing_itemization:
                self._attachment_block(rule_id, BLOCK_ABSENT, missing_itemization, base_pins)
                return "blocked"
            itemization_pins = [self._symbol_pin_entry(symbol) for symbol in itemization_symbols]

        # Finding 1 repair (ADR-0062 Decision 2): per-transaction guards,
        # checked before completeness/tie-out, on the exact whole-transaction
        # members this rule's boxes admit - never on the aggregated subtotal
        # already folded above, which a masking scenario could otherwise net
        # past undetected.
        if rule_id == "tax.us.2025.rule.attachment.f8949":
            violated_codes, violation_pins = self._f8949_row_guard_violations()
            if violated_codes:
                self._attachment_block(
                    rule_id, BLOCK_INVALID, violated_codes,
                    base_pins + itemization_pins + violation_pins,
                )
                return "blocked"
            collision_codes, collision_pins = self._covered_w_identity_key_collision_violations()
            if collision_codes:
                self._attachment_block(
                    rule_id, BLOCK_INVALID, collision_codes,
                    base_pins + itemization_pins + collision_pins,
                )
                return "blocked"

        # Completeness: every required answer's presence is checked
        # independently before any value is read (ADR-0036 decision 4) - a
        # missing answer never masks, nor is masked by, another's presence.
        completeness = rule["completeness"]
        answer_specs: dict[str, dict[str, Any]] = {a["symbol"]: a for a in completeness["required_answers"]}
        required_answers: list[str] = list(answer_specs)
        branch_requirements = completeness.get("branch_requirements", [])

        missing_answers: list[str] = [s for s in required_answers if s not in self.symbols]
        triggered_extra_symbols: list[str] = []
        named_obligations: list[dict[str, str]] = []
        for branch in branch_requirements:
            when = branch["when_answer"]
            trigger_symbol = when["symbol"]
            if trigger_symbol not in self.symbols:
                # The trigger answer is itself required and already counted
                # in missing_answers; its branch cannot be evaluated without
                # reading a value ahead of presence, so it is skipped, not
                # guessed at (presence-before-value, never the reverse).
                continue
            if str(self.symbols[trigger_symbol]) != when["equals"]:
                continue
            for extra in branch.get("adds_required", []):
                extra_symbol = extra["symbol"]
                triggered_extra_symbols.append(extra_symbol)
                answer_specs[extra_symbol] = extra
                if extra_symbol not in self.symbols:
                    missing_answers.append(extra_symbol)
            for obligation in branch.get("names_obligations", []):
                named_obligations.append(dict(obligation))

        missing_answers = sorted(set(missing_answers))
        if missing_answers:
            answer_pins = list(base_pins)
            for s in required_answers + triggered_extra_symbols:
                if s in self.symbols:
                    answer_pins.append(self._symbol_pin_entry(s))
            self._attachment_block(rule_id, BLOCK_ABSENT, missing_answers, answer_pins)
            return "blocked"

        used_answer_symbols = sorted(set(required_answers) | set(triggered_extra_symbols))

        # ADR-0055 Decision 2/3: presence is checked first, independently
        # per answer, above; a "value"-checked answer already found present
        # is now compared to its declared required value. A mismatch is a
        # completeness violation distinct from absence - the current
        # finding read here is the exact one the presence check already
        # confirmed exists, never a new lookup. One pass names every
        # currently violated answer, never only the first.
        violated_answers = sorted(
            f"{s}={_value_str(self.symbols[s])}"
            for s in used_answer_symbols
            if answer_specs[s].get("check") == "value"
            and _value_str(self.symbols[s]) != answer_specs[s]["equals"]
        )
        if violated_answers:
            answer_pins = [self._symbol_pin_entry(s) for s in used_answer_symbols]
            self._attachment_block(
                rule_id, COMPLETENESS_VALUE_VIOLATION, violated_answers, base_pins + answer_pins
            )
            return "blocked"

        answers_value = {s: _value_str(self.symbols[s]) for s in used_answer_symbols}
        answer_pins = [self._symbol_pin_entry(s) for s in used_answer_symbols]

        # Itemization: rows pin the member findings collect_members gathers
        # from the same closed family, at the same horizon, lines 2b/3b
        # already collected; each part's row-sum ties out to its named line.
        itemizations_value: list[dict[str, Any]] = []
        row_pins: list[dict[str, Any]] = []
        tie_out_violations: list[str] = []
        for part in rule["itemizations"]:
            if rule["schema"] == "attachment-rule.v1":
                row_sets = [{"rows": part["rows"], "subtotal_symbol": part["tie_out"]["line_symbol"]}]
            else:
                row_sets = part["row_sets"]
            row_sets_value: list[dict[str, Any]] = []
            part_sum = Decimal(0)
            for row_set in row_sets:
                rows_spec = row_set["rows"]
                fact_name = rows_spec["member_fact_type"]["id"]
                values = self.sources.get(fact_name, [])
                fids = self.source_fids.get(fact_name, [])
                rows = [{"finding_id": fid, "value": val} for val, fid in zip(values, fids)]
                row_sum = sum((Decimal(v) for v in values), Decimal(0))
                subtotal_symbol = row_set["subtotal_symbol"]
                subtotal_value = Decimal(str(self.symbols[subtotal_symbol]))
                row_sets_value.append({
                    "source_family": rows_spec["source_family"],
                    "rows": rows,
                    "row_sum": _value_str(row_sum),
                    "subtotal": {"symbol": subtotal_symbol, "value": _value_str(subtotal_value)},
                })
                if row_sum != subtotal_value:
                    tie_out_violations.append(
                        f"{part['part_id']}:{rows_spec['source_family']['id']}:{subtotal_symbol}"
                    )
                part_sum += row_sum
                row_pins.extend({"role": "input", "id": fid, "version": "v1",
                                  **({"origin": "assertion"} if self.use_v2 else {})}
                                 for fid in fids)
            adjustment_rows_value: list[dict[str, Any]] = []
            if rule["schema"] == "attachment-rule.v6":
                positive_subtotals = [
                    row_set["subtotal_symbol"] for row_set in part["row_sets"]
                ]
                adjustment_subtotals = [
                    row["subtotal_symbol"] for row in part["adjustment_rows"]
                ]
                tie_out = part["tie_out"]
                if (
                    tie_out["positive_subtotals"] != positive_subtotals
                    or tie_out["adjustment_subtotals"] != adjustment_subtotals
                ):
                    tie_out_violations.append(f"{part['part_id']}:tie_out_declaration")
                for adjustment in part["adjustment_rows"]:
                    rows_spec = adjustment["rows"]
                    fact_name = rows_spec["member_fact_type"]["id"]
                    values = self.sources.get(fact_name, [])
                    fids = self.source_fids.get(fact_name, [])
                    rows = [{"finding_id": fid, "value": val} for val, fid in zip(values, fids)]
                    row_sum = sum((Decimal(v) for v in values), Decimal(0))
                    subtotal_symbol = adjustment["subtotal_symbol"]
                    subtotal_value = Decimal(str(self.symbols[subtotal_symbol]))
                    adjustment_rows_value.append({
                        "kind": adjustment["kind"],
                        "label": adjustment["label"],
                        "sign": adjustment["sign"],
                        "source_family": rows_spec["source_family"],
                        "rows": rows,
                        "row_sum": _value_str(row_sum),
                        "signed_sum": _value_str(-row_sum),
                        "subtotal": {"symbol": subtotal_symbol, "value": _value_str(subtotal_value)},
                    })
                    if any(Decimal(v) < 0 for v in values) or row_sum != subtotal_value:
                        tie_out_violations.append(
                            f"{part['part_id']}:{rows_spec['source_family']['id']}:{subtotal_symbol}"
                        )
                    part_sum -= row_sum
                    row_pins.extend({"role": "input", "id": fid, "version": "v1",
                                      **({"origin": "assertion"} if self.use_v2 else {})}
                                     for fid in fids)
            tie_symbol = part["tie_out"]["line_symbol"]
            line_value = Decimal(str(self.symbols[tie_symbol]))
            if rule["schema"] == "attachment-rule.v1":
                legacy = row_sets_value[0]
                itemizations_value.append({
                    "part_id": part["part_id"],
                    "rows": legacy["rows"],
                    "row_sum": legacy["row_sum"],
                    "tie_out": {"line_symbol": tie_symbol, "line_value": _value_str(line_value)},
                })
            else:
                itemizations_value.append({
                    "part_id": part["part_id"],
                    "row_sets": row_sets_value,
                    **({"adjustment_rows": adjustment_rows_value} if rule["schema"] == "attachment-rule.v6" else {}),
                    "part_sum": _value_str(part_sum),
                    "tie_out": {"line_symbol": tie_symbol, "line_value": _value_str(line_value)},
                })
            if part_sum != line_value:
                tie_out_violations.append(f"{part['part_id']}:{tie_symbol}")

        if tie_out_violations:
            self._attachment_block(
                rule_id, ITEMIZATION_TIE_OUT_VIOLATION, sorted(set(tie_out_violations)),
                base_pins + itemization_pins + answer_pins + (row_pins if rule["schema"] in ("attachment-rule.v2", "attachment-rule.v3", "attachment-rule.v4", "attachment-rule.v5", "attachment-rule.v6") else []),
            )
            return "blocked"

        value = {
            "required": True,
            "triggers": triggers,
            "itemizations": itemizations_value,
            "answers": answers_value,
            "named_obligations": named_obligations,
        }
        symbol = rule["publishes"]
        pins = _sorted_pins(base_pins + itemization_pins + answer_pins + row_pins)
        body = {"symbol": symbol, "value": value, "pins": pins}
        finding = {
            "schema": "derived-finding.v2",
            "id": _content_id("finding:derived:", body),
            "symbol": symbol,
            "value": value,
            "version": "v2",
            "pins": pins,
        }
        act = {"run_id": self.ctx.run_id, "finding": finding}
        self.schemas.validate_declared(finding)
        self.publications.append(Publication(act=act, finding=finding))
        self.symbol_publisher[symbol] = rule
        self.dispositions.append({
            "artifact_id": rule_id,
            "disposition": "published",
            "pins": pins,
            "finding_id": finding["id"],
            "act_id": _content_id("act:publication:", act),
            "symbol": symbol,
        })
        self.symbols[symbol] = value
        self.symbol_pin[symbol] = (finding["id"], "v2", "input", "assertion")
        self.resolved.add(rule_id)
        return "published"

    def _record_blocked(self, rule: dict[str, Any], access: AccessLog, code: str, missing: list[str]) -> None:
        rule_id = rule["id"]
        self.blocked.append({"artifact_id": rule_id, "code": code, "missing": missing})
        disposition_row = {
            "artifact_id": rule_id,
            "disposition": "blocked",
            "pins": self.ledger_pins_for(rule, access)
        }
        if self.use_v2:
            disposition_row["code"] = code
            disposition_row["missing"] = missing
        self.dispositions.append(disposition_row)
        self.resolved.add(rule_id)

    def finalize_unreached(self) -> None:
        """Rules that never became eligible saturate blocked on their gap."""
        for rule in self.ctx.rules:
            if rule["id"] in self.resolved:
                continue

            if rule.get("schema") in ATTACHMENT_SCHEMAS:
                self.attempt_attachment(rule)
                continue

            # Finding 1/3 repair: lines 1b/8b screen their own box's
            # per-transaction guards here too - a rule that never became
            # eligible (e.g. its adjustment subtotal is blocked on an
            # unrelated closure gap) must still surface the more specific,
            # named guard violation when one exists, the same as the main
            # saturation path already does in `attempt`.
            line_guard_boxes = _LINE_GUARD_BOX_KEYS.get(rule["id"])
            if line_guard_boxes is not None:
                violated_codes, _violation_pins = self._f8949_row_guard_violations(line_guard_boxes)
                if violated_codes:
                    self._record_blocked(rule, AccessLog(), BLOCK_INVALID, violated_codes)
                    continue
                collision_codes, _collision_pins = self._covered_w_identity_key_collision_violations(
                    line_guard_boxes
                )
                if collision_codes:
                    self._record_blocked(rule, AccessLog(), BLOCK_INVALID, collision_codes)
                    continue

            # A false guard is an atomic inapplicable disposition even when
            # later numeric dependencies are absent.  Preflight only far
            # enough to prove false: a true or blocked preflight retains the
            # established missing-dependency/conflict/fallback precedence
            # below.  This lets declared guards classify their branch before
            # numeric work without turning missing inputs into assumed values.
            guard_access = AccessLog()
            try:
                guard_preflight = evaluate(rule["when"], self.env(), guard_access)
            except EvalBlocked:
                guard_preflight = None
            if guard_preflight is False:
                self.dispositions.append({
                    "artifact_id": rule["id"],
                    "disposition": "inapplicable",
                    "guard_result": False,
                    "pins": self.ledger_pins_for(rule, guard_access),
                })
                self.resolved.add(rule["id"])
                continue

            # 1. If any dependency is absent -> blocked
            missing = [req for req in rule["requires"] if req not in self.symbols]
            if missing:
                self.blocked.append({"artifact_id": rule["id"], "code": BLOCK_ABSENT, "missing": missing})
                disposition_row = {
                    "artifact_id": rule["id"],
                    "disposition": "blocked",
                    "pins": []
                }
                if self.use_v2:
                    disposition_row["code"] = "DEPENDENCY_ABSENT"
                    disposition_row["missing"] = missing
                self.dispositions.append(disposition_row)
                self.resolved.add(rule["id"])
                continue

            # 2. Else if output symbol already published by another producer under conflict semantics -> inapplicable conflict-loser
            symbol = rule["publishes"]
            if symbol in self.symbols:
                winner = self.symbol_publisher.get(symbol)
                disposition_row = {
                    "artifact_id": rule["id"],
                    "disposition": "inapplicable",
                    "pins": []
                }
                if self.use_v2:
                    if winner:
                        disposition_row["superseded_by"] = {"role": "package", "id": winner["id"], "version": winner["version"]}
                self.dispositions.append(disposition_row)
                self.resolved.add(rule["id"])
                continue

            # 3. Else evaluate (fallback)
            access = AccessLog()
            try:
                guard = evaluate(rule["when"], self.env(), access)
            except EvalBlocked as exc:
                self._record_blocked(rule, access, exc.category, exc.missing)
                continue
            if not guard:
                disposition_row = {
                    "artifact_id": rule["id"],
                    "disposition": "inapplicable",
                    "guard_result": False,
                    "pins": self.ledger_pins_for(rule, access)
                }
                self.dispositions.append(disposition_row)
                self.resolved.add(rule["id"])
                continue

            try:
                value = evaluate(rule["value"], self.env(), access)
            except EvalBlocked as exc:
                self._record_blocked(rule, access, exc.category, exc.missing)
                continue

            pins = self.pins_for(rule, access)
            provenance = "assertion"
            if self.use_v2:
                for pin in pins:
                    if pin.get("role") == "input" and pin.get("origin") == "declared_default":
                        provenance = "declared_default"
                        break
            schema_ver = "v2" if self.use_v2 else "v1"
            body = {"symbol": symbol, "value": _value_str(value), "pins": pins}
            finding = {
                "schema": f"derived-finding.{schema_ver}",
                "id": _content_id("finding:derived:", body),
                "symbol": symbol,
                "value": body["value"],
                "version": schema_ver,
                "pins": pins,
            }
            act = {"run_id": self.ctx.run_id, "finding": finding}
            if self.use_v2:
                self.schemas.validate_declared(finding)
            else:
                self.schemas.validate(PUBLICATION_ACT_SCHEMA, act)
                self.schemas.validate_declared(finding)
            self.publications.append(Publication(act=act, finding=finding))

            self.symbol_publisher[symbol] = rule

            disposition_row = {
                "artifact_id": rule["id"],
                "disposition": "published",
                "pins": self.ledger_pins_for(rule, access)
            }
            if self.use_v2:
                disposition_row["finding_id"] = finding["id"]
                disposition_row["act_id"] = _content_id("act:publication:", act)
                disposition_row["symbol"] = symbol
            self.dispositions.append(disposition_row)

            self.symbols[symbol] = value
            # Downstream refs to this symbol pin THIS derived finding, as an input.
            self.symbol_pin[symbol] = (finding["id"], schema_ver, "input", provenance if self.use_v2 else None)
            self.resolved.add(rule["id"])

    def result(self) -> RunResult:
        return RunResult(
            run_id=self.ctx.run_id,
            publications=self.publications,
            dispositions=self.dispositions,
            blocked=self.blocked,
            stop_reason="saturated",
            symbols=self.symbols,
        )


def _execute(ctx: RunContext, schemas: DerivationSchemas) -> RunResult:
    """Evaluator implementation shared by fixture and marshalled live paths."""
    state = _Run(ctx, schemas)
    progress = True
    while progress:
        progress = False
        for rule in ctx.rules:
            if rule["id"] in state.resolved or not state.is_eligible(rule):
                continue
            if rule.get("schema") in ATTACHMENT_SCHEMAS:
                state.attempt_attachment(rule)
            else:
                state.attempt(rule)
            progress = True
    state.finalize_unreached()
    return state.result()


def run(ctx: RunContext, schemas: DerivationSchemas) -> RunResult:
    """Fixture/test evaluator entrypoint for a deliberately assembled context.

    Production callers use ``production_executor.execute_marshaled`` instead;
    that entrypoint accepts only the opaque result of the record-state
    marshaller.  Keeping the fixture entrypoint preserves the deterministic
    legacy scenario corpus without making it a live-run route.
    """
    return _execute(ctx, schemas)


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
    use_v2 = any(
        rule.get("schema") in {"rule-artifact.v2", "rule-artifact.v3"}
        for rule in ctx.rules
    ) or _uses_attachment_machinery(ctx.rules)
    start_run(
        stream,
        record_id=start_record_id,
        run_id=ctx.run_id,
        workspace_revision=workspace_revision,
        governance_pins=ctx.governance_pins,
        adoption_pin=ctx.adoption_pin,
        adopted_packages=adopted_packages,
        use_v2=use_v2,
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
            use_v2=use_v2,
        )
    )
    return result
