"""Pairing-scoped current-year adjustment and basis consequence (ADR-0071).

Seam 5 of the Document and Ordinary-Fact Translation Vertical. Two separate
``rule-artifact.v7`` citizens each call ``evaluate_pairing_scoped_rule`` once
per current ADR-0068 pairing — never one rule publishing two findings from a
single loop iteration. Both are gated on an ADR-0070 supportability verdict
of True for the same pairing.

What exists now
---------------
- Two checksum-shaped content citizens under ``packages/content/tax/2025/``,
  with fact types keyed to the ADR-0068 pairing (entity kind
  ``tax.us.acquisition-report-pairing``), never
  ``tax.us.scheduleb-adjustment-instance``.
- Runner intercept: when either rule is in ``RunContext.rules``, ``attempt()``
  dispatches through ``evaluate_pairing_scoped_rule`` rather than ordinary
  once-per-rule-id evaluation. Authorization is copied onto ``Environment``
  the same way as every other rule; evaluation does not consult it
  (ADR-0069). There is no currentness gate in the run loop to bypass.
- ``SUPPORTABILITY_NOT_ESTABLISHED`` already survives ``derivation-record.v8``.

Line-2b successor aggregator
----------------------------
``dispatch_current_year_subtotal_on_run`` sums pairing-scoped current-year
adjustment publications into
``tax.us.2025.interest.current-year-adjustment-subtotal``.
``rule.form1040-line2b`` v5 subtracts that symbol in addition to the
incumbent form-row accrued-interest subtotal (coexistence).

Later-year basis consumer remains a milestone non-goal.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from decimal import Decimal
from typing import Any, Mapping, Sequence, cast

from packages.derivation.evaluator import AccessLog, EvalBlocked, Environment, evaluate
from packages.derivation.loader import DerivationSchemas
from packages.derivation.pairing_dispatch import (
    PairingBinding,
    PairingBlock,
    PairingPublish,
    PairingScopedResult,
    evaluate_pairing_scoped_rule,
)
from packages.derivation.runner import SourceFact
from packages.tax.identity_association import (
    ACQUISITION_FACT_TYPE,
    ASSOCIATION_SYMBOL,
    REPORT_FACT_TYPE,
)

DEPENDENCY_INVALID = "DEPENDENCY_INVALID"
SUPPORTABILITY_NOT_ESTABLISHED = "SUPPORTABILITY_NOT_ESTABLISHED"

ACQUISITION_FIELD = "accrued_interest_paid_to_seller"
PAIRING_TYPE = ASSOCIATION_SYMBOL
SUPPORTABILITY_TYPE = "tax.us.2025.relationship.accrued-supported"

# Both content citizens'
# ``value`` field is this exact expression (see
# ``rule.interest.current-year-adjustment.pairing-scoped.json`` and
# ``rule.basis.item-level-consequence.pairing-scoped.json``). It is kept
# here only as the default for the two standalone helper functions below
# (``evaluate_current_year_adjustment``/``evaluate_basis_consequence``,
# exercised directly by unit tests without a loaded rule citizen) so their
# behavior is unchanged. Production dispatch (``dispatch_consequence_on_run``)
# never uses this constant — it evaluates the adopted rule's own ``value``
# field, whatever it declares, so a genuinely different successor expression
# genuinely changes what gets published.
DEFAULT_CONSEQUENCE_VALUE_EXPR: dict[str, Any] = {
    "op": "ref",
    "name": ACQUISITION_FACT_TYPE,
    "field": ACQUISITION_FIELD,
}

CURRENT_YEAR_RULE_ID = (
    "tax.us.2025.rule.interest.current-year-adjustment.pairing-scoped"
)
BASIS_RULE_ID = "tax.us.2025.rule.basis.item-level-consequence.pairing-scoped"
PAIRING_SCOPED_CONSEQUENCE_RULE_IDS = frozenset(
    {CURRENT_YEAR_RULE_ID, BASIS_RULE_ID}
)

# The declared consequence
# fact-type ids in pairing-scoped-consequences.bundle.json both carry a
# ``.pairing-scoped`` suffix; these runtime symbol prefixes must equal them
# exactly, or a run never instantiates the declared fact type at all. The
# bundle's declared ids are the correct side (they distinguish this vocabulary
# from any future non-pairing-scoped consequence of the same tax concept);
# the runtime prefixes are fixed here to match, not the reverse.
CURRENT_YEAR_SYMBOL_PREFIX = "tax.us.2025.interest.current-year-adjustment.pairing-scoped"
BASIS_SYMBOL_PREFIX = "tax.us.2025.basis.item-level-consequence.pairing-scoped"
CURRENT_YEAR_SUBTOTAL_RULE_ID = (
    "tax.us.2025.rule.interest.current-year-adjustment-subtotal"
)
CURRENT_YEAR_SUBTOTAL_SYMBOL = "tax.us.2025.interest.current-year-adjustment-subtotal"

CURRENT_YEAR_CITATION_ID = (
    "tax.us.2025.citation.scheduleb-adjustment.accrued-interest"
)
BASIS_CITATION_ID = "tax.us.2025.citation.basis-adjustment.accrued-interest"

# Aggregate supportability. ADR-0070
# Decision 4's per-pairing check (each acquisition against its own report's
# full amount) is correct and not reopened; it cannot see a *combined*
# over-claim when several acquisitions genuinely associate (ADR-0068) to the
# same report. This is a separate, additive layer: group every same-run
# current-year-adjustment publication by the exact report fact id its
# pairing names (via the pairing's own pinned right_fact_id — the real pin
# chain ADR-0068/0070 already establish, never a new correlation signal),
# sum the claims per report, and block the report-group whose combined claim
# exceeds that report's own real box-1 amount. Detects and blocks only; it
# does not decide how much of the report each acquisition is "really"
# entitled to (no allocation policy is introduced).
AGGREGATE_SUPPORTABILITY_RULE_ID = (
    "tax.us.2025.rule.interest.current-year-adjustment.aggregate-supportability"
)
AGGREGATE_ACCRUED_EXCEEDS_REPORT = "AGGREGATE_ACCRUED_EXCEEDS_REPORT"
AGGREGATE_SUPPORTABILITY_SYMBOL_PREFIX = (
    "tax.us.2025.interest.current-year-adjustment.aggregate-supported"
)

_RULE_SYMBOL_PREFIX = {
    CURRENT_YEAR_RULE_ID: CURRENT_YEAR_SYMBOL_PREFIX,
    BASIS_RULE_ID: BASIS_SYMBOL_PREFIX,
}
_RULE_CITATION_ID = {
    CURRENT_YEAR_RULE_ID: CURRENT_YEAR_CITATION_ID,
    BASIS_RULE_ID: BASIS_CITATION_ID,
}


def is_pairing_scoped_consequence_rule(rule: Mapping[str, Any]) -> bool:
    return rule.get("id") in PAIRING_SCOPED_CONSEQUENCE_RULE_IDS


def is_current_year_subtotal_rule(rule: Mapping[str, Any]) -> bool:
    return rule.get("id") == CURRENT_YEAR_SUBTOTAL_RULE_ID


def pairing_scoped_collect_source_names() -> tuple[str, ...]:
    """Fact-type names marshal must collect for these rules to see pairings."""
    return (ACQUISITION_FACT_TYPE, REPORT_FACT_TYPE, PAIRING_TYPE, SUPPORTABILITY_TYPE)


def _decode(raw: Any) -> Any:
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw
    return raw


def _verdict_passes(raw: Any) -> bool:
    decoded = _decode(raw)
    if decoded is True:
        return True
    if isinstance(decoded, str) and decoded.strip().lower() == "true":
        return True
    return False


def _input_pin(finding_id: str) -> dict[str, Any]:
    return {"role": "input", "id": finding_id, "version": "v1", "origin": "assertion"}


def _citation_pin(citation_id: str, version: str = "v1") -> dict[str, Any]:
    return {"role": "citation", "id": citation_id, "version": version}


def supportability_by_pairing_fact_id(
    sources: Sequence[SourceFact],
) -> dict[str, SourceFact]:
    """Index ADR-0070 supportability sources by the pairing fact id they name.

    Expected shape (ADR-0070 production; Seam 3 may still be landing the
    producer): ``SourceFact.name == SUPPORTABILITY_TYPE``, ``fact_id`` is
    the pairing's fact id, value is True when the accrued amount does not
    exceed the associated report.
    """
    return {
        s.fact_id: s
        for s in sources
        if s.name == SUPPORTABILITY_TYPE and s.fact_id
    }


def _symbol_for(prefix: str) -> Callable[[PairingBinding], str]:
    def _symbol(binding: PairingBinding) -> str:
        return f"{prefix}|{binding.pairing_fact_id}"

    return _symbol


def _pairing_local_environment(binding: PairingBinding, run: Any | None = None) -> Environment:
    """Build the environment the rule's own declared expression evaluates in.

    A pairing-scoped consequence rule's
    ``value`` expression refs the acquisition/report fact-type ids as symbol
    names (see the content citizens' ``{"op": "ref", "name":
    ACQUISITION_FACT_TYPE, ...}`` shape). The ordinary run-wide ``Environment``
    (``_Run.env()``) resolves a ref by that name to whichever "current"
    global finding of that type exists — exactly the masking hazard
    ``pairing_dispatch.py`` already documents for raw source lookups (two
    current facts of the same type both appear at once when several
    pairings are live in one run). This environment instead binds those two
    names to *this pairing's own* resolved left/right values only, so the
    expression can never read a sibling pairing's fact by accident.

    ``sources``/(the two-layer source-set-closure field, positional below --
    never named here; only ``runner.py`` and ``evaluator.py`` may name it,
    per the source-completeness audit) are intentionally empty/absent: a
    pairing-scoped consequence expression has no legitimate reason to
    ``collect`` a cross-cutting raw source set (that is global, not
    pairing-local, state) or assert any set closed on its own authority.
    ``parameters``/``canon`` are carried over from the run when available so
    an expression may still use ordinary operations (``round``,
    ``range_lookup``, ...) that read declared parameter/canon citizens
    rather than fact state.
    """
    symbols = {
        ACQUISITION_FACT_TYPE: binding.left_value,
        REPORT_FACT_TYPE: binding.right_value,
    }
    parameters = dict(run.ctx.parameters) if run is not None else {}
    canon = dict(run.ctx.canon) if run is not None else {}
    return Environment(symbols, {}, frozenset(), parameters, canon)


def _dependency_pins(run: Any | None, access: AccessLog) -> tuple[dict[str, Any], ...]:
    """Convert a pairing rule's own ``AccessLog`` into truthful dependency pins.

    The pairing-local
    expression evaluator (``_evaluate_one_factory``) records every
    parameter, table, operation-semantics citizen, ref, and closure read the
    adopted rule's declared ``value`` expression actually touched — the same
    ``AccessLog`` ordinary rule evaluation uses. That access log is
    converted into truthful dependency pins so a successor rule that changes
    behavior through a parameter or operation-semantics citizen is reflected
    in the published finding's pins, not only in citation,
    adoption, governance, pairing-side, and supportability pins. This
    reuses ``_Run.dependency_pins_for_access`` — the exact conversion
    ordinary evaluation's ``pins_for`` already performs — so both dispatch
    paths turn the same access classes into the same pin shape. The
    pairing-specific left/right binding is unaffected: those pins are
    assembled separately in ``pairing_dispatch.evaluate_pairing_scoped_rule``
    (``present_pins``) and composed with this function's result via
    ``extra_pins``, never replaced.

    ``run`` is ``None`` only for the two standalone helper functions
    (``evaluate_current_year_adjustment``/``evaluate_basis_consequence``)
    that unit tests call directly without a loaded run context; there is no
    run to resolve a parameter/table/operation citizen's version against, so
    those callers get no dependency pins.
    """
    if run is None:
        return ()
    return tuple(run.dependency_pins_for_access(access))


def _evaluate_one_factory(
    supportability_by_pairing: Mapping[str, SourceFact],
    *,
    value_expr: Mapping[str, Any] = DEFAULT_CONSEQUENCE_VALUE_EXPR,
    run: Any | None = None,
) -> Callable[[PairingBinding], "PairingPublish | PairingBlock"]:
    """Build the per-pairing evaluator for one consequence rule.

    ``value_expr`` is the adopted rule citizen's own declared ``value``
    field (or, for the standalone helper functions with no loaded rule
    citizen, the fixed default expression both current content citizens
    happen to declare). Evaluation runs through the same closed-vocabulary
    expression evaluator (``packages.derivation.evaluator.evaluate``) every
    ordinary rule's ``value``/``when`` already uses — no second evaluator is
    invented — against a pairing-local environment
    (``_pairing_local_environment``), so a genuinely different declared
    expression genuinely changes what this pairing publishes.
    """
    def evaluate_one(binding: PairingBinding) -> PairingPublish | PairingBlock:
        supportability = supportability_by_pairing.get(binding.pairing_fact_id)
        if supportability is None or not _verdict_passes(supportability.value):
            extra: tuple[dict[str, Any], ...] = ()
            if supportability is not None:
                extra = (_input_pin(supportability.finding_id),)
            return PairingBlock(
                code=SUPPORTABILITY_NOT_ESTABLISHED,
                missing=(binding.pairing_fact_id,),
                extra_pins=extra,
            )
        env = _pairing_local_environment(binding, run=run)
        access = AccessLog()
        try:
            raw_value = evaluate(dict(value_expr), env, access)
        except EvalBlocked as exc:
            return PairingBlock(
                code=exc.category,
                missing=tuple(exc.missing) or (binding.left_fact_id,),
                extra_pins=(
                    _input_pin(supportability.finding_id),
                    *_dependency_pins(run, access),
                ),
            )
        if isinstance(raw_value, bool):
            return PairingBlock(
                code=DEPENDENCY_INVALID,
                missing=(binding.left_fact_id,),
                extra_pins=(
                    _input_pin(supportability.finding_id),
                    *_dependency_pins(run, access),
                ),
            )
        try:
            amount = Decimal(str(raw_value))
        except Exception:
            return PairingBlock(
                code=DEPENDENCY_INVALID,
                missing=(binding.left_fact_id,),
                extra_pins=(
                    _input_pin(supportability.finding_id),
                    *_dependency_pins(run, access),
                ),
            )
        return PairingPublish(
            value=format(amount, "f"),
            extra_pins=(
                _input_pin(supportability.finding_id),
                *_dependency_pins(run, access),
            ),
        )

    return evaluate_one


def evaluate_current_year_adjustment(
    *,
    sources: Sequence[SourceFact],
    rule_id: str = CURRENT_YEAR_RULE_ID,
    rule_version: str = "v1",
    citation_id: str = CURRENT_YEAR_CITATION_ID,
    extra_pins: Sequence[Mapping[str, Any]] = (),
    schemas: DerivationSchemas | None = None,
) -> PairingScopedResult:
    """Rule A: current-year interest adjustment, once per pairing."""
    return _dispatch_one_rule(
        sources=sources,
        rule_id=rule_id,
        rule_version=rule_version,
        citation_id=citation_id,
        symbol_prefix=CURRENT_YEAR_SYMBOL_PREFIX,
        extra_pins=extra_pins,
        schemas=schemas,
    )


def evaluate_basis_consequence(
    *,
    sources: Sequence[SourceFact],
    rule_id: str = BASIS_RULE_ID,
    rule_version: str = "v1",
    citation_id: str = BASIS_CITATION_ID,
    extra_pins: Sequence[Mapping[str, Any]] = (),
    schemas: DerivationSchemas | None = None,
) -> PairingScopedResult:
    """Rule B: item-level basis consequence, once per pairing."""
    return _dispatch_one_rule(
        sources=sources,
        rule_id=rule_id,
        rule_version=rule_version,
        citation_id=citation_id,
        symbol_prefix=BASIS_SYMBOL_PREFIX,
        extra_pins=extra_pins,
        schemas=schemas,
    )


def _dispatch_one_rule(
    *,
    sources: Sequence[SourceFact],
    rule_id: str,
    rule_version: str,
    citation_id: str,
    symbol_prefix: str,
    extra_pins: Sequence[Mapping[str, Any]],
    schemas: DerivationSchemas | None,
) -> PairingScopedResult:
    schemas = schemas or DerivationSchemas()
    return evaluate_pairing_scoped_rule(
        sources=sources,
        pairing_type=PAIRING_TYPE,
        left_type=ACQUISITION_FACT_TYPE,
        right_type=REPORT_FACT_TYPE,
        rule_id=rule_id,
        rule_version=rule_version,
        symbol_for=_symbol_for(symbol_prefix),
        evaluate_one=_evaluate_one_factory(supportability_by_pairing_fact_id(sources)),
        extra_pins=[_citation_pin(citation_id), *(dict(p) for p in extra_pins)],
        schemas=schemas,
    )


def dispatch_consequence_on_run(run: Any, rule: Mapping[str, Any]) -> PairingScopedResult:
    """Apply one consequence rule to the run's marshaled pairing sources.

    Called from ``_Run.attempt`` when the rule id is one of the two
    pairing-scoped artifacts. Uses the run's own
    ``evaluate_pairing_scoped_rule`` so publications land on the same
    ledger as ordinary rules.
    """
    rule_id = rule["id"]
    prefix = _RULE_SYMBOL_PREFIX[rule_id]
    citations = rule.get("citations") or []
    citation = citations[0] if citations else {}
    citation_id = citation.get("id") or _RULE_CITATION_ID[rule_id]
    citation_version = citation.get("version") or "v1"
    extra = [
        _citation_pin(citation_id, citation_version),
        dict(run.ctx.adoption_pin),
        *(dict(p) for p in run.ctx.governance_pins),
    ]
    sources = getattr(run, "live_sources", run.ctx.sources)
    return cast(
        PairingScopedResult,
        run.evaluate_pairing_scoped_rule(
            pairing_type=PAIRING_TYPE,
            left_type=ACQUISITION_FACT_TYPE,
            right_type=REPORT_FACT_TYPE,
            rule_id=rule_id,
            rule_version=rule["version"],
            symbol_for=_symbol_for(prefix),
            evaluate_one=_evaluate_one_factory(
                supportability_by_pairing_fact_id(sources),
                value_expr=rule["value"],
                run=run,
            ),
            extra_pins=extra,
        ),
    )


def consequence_eligibility(run: Any) -> bool:
    """Pairing-scoped consequences wait until Seam 3 supportability has run.

    Package membership sorts rules by id, so the two consequence citizens
    precede ``rule.relationship.accrued-supported``. Without this gate they
    would fire, resolve empty, and never see same-run supportability.
    Isolation tests that omit the supportability rule stay immediately
    eligible — the same posture as ``subtotal_eligibility``.
    """
    from packages.tax.supportability import RULE_ID as SUPPORTABILITY_RULE_ID

    rule_ids = {rule["id"] for rule in run.ctx.rules}
    if SUPPORTABILITY_RULE_ID not in rule_ids:
        return True
    return SUPPORTABILITY_RULE_ID in run.resolved


def is_aggregate_supportability_rule(rule: Mapping[str, Any]) -> bool:
    return rule.get("id") == AGGREGATE_SUPPORTABILITY_RULE_ID


def aggregate_supportability_eligibility(run: Any) -> bool:
    """The aggregate check waits until the pairing-scoped current-year rule has run.

    Same posture as ``subtotal_eligibility``: an isolation test that omits
    the per-pairing current-year rule stays immediately eligible.
    """
    rule_ids = {rule["id"] for rule in run.ctx.rules}
    if CURRENT_YEAR_RULE_ID not in rule_ids:
        return True
    return CURRENT_YEAR_RULE_ID in run.resolved


def subtotal_eligibility(run: Any) -> bool:
    """The subtotal waits until the pairing-scoped current-year rule — and,
    when present, the aggregate-supportability check — have both run.

    The aggregate check must resolve first so the subtotal can exclude any
    report group it blocked; without this second gate the
    subtotal could read `run.blocked` before the aggregate check populates it.
    """
    rule_ids = {rule["id"] for rule in run.ctx.rules}
    if CURRENT_YEAR_RULE_ID in rule_ids and CURRENT_YEAR_RULE_ID not in run.resolved:
        return False
    if (
        AGGREGATE_SUPPORTABILITY_RULE_ID in rule_ids
        and AGGREGATE_SUPPORTABILITY_RULE_ID not in run.resolved
    ):
        return False
    return True


def _pairing_right_fact_id_index(sources: Sequence[SourceFact]) -> dict[str, str]:
    """Map each current pairing's own fact id to its pinned right_fact_id.

    The same pin-chain dereference ADR-0068/0070 already establish
    (``PairingBinding.right_fact_id``) — never a new correlation signal.
    """
    index: dict[str, str] = {}
    for source in sources:
        if source.name != PAIRING_TYPE or not source.fact_id:
            continue
        decoded = _decode(source.value)
        if isinstance(decoded, dict) and isinstance(decoded.get("right_fact_id"), str):
            index[source.fact_id] = decoded["right_fact_id"]
    return index


def _report_sources_by_fact_id(sources: Sequence[SourceFact]) -> dict[str, SourceFact]:
    return {
        s.fact_id: s for s in sources if s.name == REPORT_FACT_TYPE and s.fact_id
    }


def _current_year_groups_by_report(
    run: Any,
) -> dict[str, list[dict[str, Any]]]:
    """Group this run's current-year-adjustment publications by report fact id.

    Groups by the specific report fact id each pairing's own pinned
    ``right_fact_id`` names — the exact report the combined claim must
    never exceed.
    """
    sources = getattr(run, "live_sources", run.ctx.sources)
    pairing_right = _pairing_right_fact_id_index(sources)
    prefix = CURRENT_YEAR_SYMBOL_PREFIX + "|"
    groups: dict[str, list[dict[str, Any]]] = {}
    for pub in run.publications:
        symbol = pub.finding.get("symbol")
        if not isinstance(symbol, str) or not symbol.startswith(prefix):
            continue
        pairing_fact_id = symbol[len(prefix):]
        report_fact_id = pairing_right.get(pairing_fact_id)
        if report_fact_id is None:
            continue
        groups.setdefault(report_fact_id, []).append(pub.finding)
    return groups


def _aggregate_blocked_report_fact_ids(run: Any) -> set[str]:
    """Report fact ids the aggregate check already blocked this run.

    Derived from ``run.blocked``, not a new side channel: the aggregate
    check's own recorded refusals are the single source of truth the
    subtotal reads to exclude a report group's contribution.
    """
    return {
        row["missing"][0]
        for row in run.blocked
        if row.get("artifact_id") == AGGREGATE_SUPPORTABILITY_RULE_ID
        and row.get("code") == AGGREGATE_ACCRUED_EXCEEDS_REPORT
        and row.get("missing")
    }


def _retract_pairing_scoped_publications_for_blocked_groups(
    run: Any,
    *,
    blocked_report_fact_ids: set[str],
    pairing_right: Mapping[str, str],
) -> None:
    """Demote a blocked report-group's per-pairing findings to blocked.

    Detecting a combined over-claim
    establishes only that the claimed set is *unresolved* — not that zero
    adjustment applies. Leaving every individual current-year-adjustment
    and basis-consequence finding for the blocked group sitting in
    ``run.publications`` with a plain ``published`` disposition would let
    any consumer other than the subtotal rule (which already excludes them
    from its own sum) mistake a blocked group's per-pairing findings for
    ordinarily-supported ones. This applies the same discipline the
    codebase already uses for a named refusal (e.g.
    ``ASSOCIATION_AMBIGUOUS``/``ASSOCIATION_UNCONFIRMED``): the finding is
    removed from the live publication set and its disposition row is
    rewritten from ``published`` to ``blocked`` with the aggregate check's
    own named code, rather than silently vanishing or staying falsely
    "published". No new disposition shape or schema version is introduced —
    ``AGGREGATE_ACCRUED_EXCEEDS_REPORT`` already survives the
    derivation-record ledger (ADR-0070 / v9, admitted through v10).
    """
    if not blocked_report_fact_ids:
        return
    blocked_pairing_ids = {
        pairing_fact_id
        for pairing_fact_id, report_fact_id in pairing_right.items()
        if report_fact_id in blocked_report_fact_ids
    }
    if not blocked_pairing_ids:
        return

    prefixes = (CURRENT_YEAR_SYMBOL_PREFIX + "|", BASIS_SYMBOL_PREFIX + "|")

    def _pairing_of(symbol: Any) -> str | None:
        if not isinstance(symbol, str):
            return None
        for prefix in prefixes:
            if symbol.startswith(prefix):
                return symbol[len(prefix):]
        return None

    retained: list[Any] = []
    for pub in run.publications:
        symbol = pub.finding.get("symbol")
        pairing_fact_id = _pairing_of(symbol)
        if pairing_fact_id is None or pairing_fact_id not in blocked_pairing_ids:
            retained.append(pub)
            continue
        report_fact_id = pairing_right[pairing_fact_id]
        for row in run.dispositions:
            if row.get("symbol") == symbol and row.get("disposition") == "published":
                row["disposition"] = "blocked"
                row["code"] = AGGREGATE_ACCRUED_EXCEEDS_REPORT
                row["missing"] = [report_fact_id]
        run.symbols.pop(symbol, None)
        run.symbol_pin.pop(symbol, None)
    run.publications = retained

    prefix_names = {CURRENT_YEAR_SYMBOL_PREFIX, BASIS_SYMBOL_PREFIX}
    run.live_sources = [
        s
        for s in getattr(run, "live_sources", run.ctx.sources)
        if not (s.name in prefix_names and s.fact_id in blocked_pairing_ids)
    ]
    for name in prefix_names:
        if name not in run.sources:
            continue
        keep = [
            index
            for index, fid in enumerate(run.source_fact_ids.get(name, []))
            if fid not in blocked_pairing_ids
        ]
        run.sources[name] = [run.sources[name][index] for index in keep]
        run.source_fids[name] = [run.source_fids[name][index] for index in keep]
        run.source_fact_ids[name] = [run.source_fact_ids[name][index] for index in keep]


def dispatch_aggregate_supportability_on_run(run: Any, rule: Mapping[str, Any]) -> str:
    """Block a report group whose combined current-year claim exceeds it.

    ADR-0070 Decision 4's per-pairing supportability check evaluates each
    acquisition independently against its associated report's full amount,
    by design (no cumulative comparison, no allocation decision). That
    leaves a gap this rule closes: when two or more genuinely-associated
    (ADR-0068) acquisitions share one report, their *combined* claim can
    exceed that report even though each individually passed. This rule
    groups same-run current-year-adjustment publications by the exact
    report fact id each pairing names, sums the claims per report, and
    blocks (``AGGREGATE_ACCRUED_EXCEEDS_REPORT``) only the report group that
    exceeds — never the whole run, never a sibling report's unrelated
    claims, and never by adjudicating an allocation between the
    acquisitions.

    A blocked group's individual current-year-adjustment
    and basis-consequence findings are retracted from ordinary
    publication (``_retract_pairing_scoped_publications_for_blocked_groups``)
    — detecting an unresolved combined claim does not establish that no
    adjustment applies, so those findings cannot keep presenting as
    ordinarily-supported to any downstream consumer.
    """
    sources = getattr(run, "live_sources", run.ctx.sources)
    reports = _report_sources_by_fact_id(sources)
    groups = _current_year_groups_by_report(run)
    pairing_right = _pairing_right_fact_id_index(sources)

    rule_pin = {
        "role": rule.get("role", "computation"),
        "id": rule["id"],
        "version": rule["version"],
    }
    citations = rule.get("citations") or []
    citation = citations[0] if citations else {}
    citation_id = citation.get("id") or CURRENT_YEAR_CITATION_ID
    citation_version = citation.get("version") or "v1"
    shared_pins = [
        dict(rule_pin),
        _citation_pin(citation_id, citation_version),
        dict(run.ctx.adoption_pin),
        *(dict(p) for p in run.ctx.governance_pins),
    ]

    published_any = False
    blocked_any = False
    blocked_report_fact_ids: set[str] = set()
    for report_fact_id in sorted(groups):
        findings = groups[report_fact_id]
        report_source = reports.get(report_fact_id)
        if report_source is None:
            # The pairing named a report this run never marshaled as a live
            # source; nothing to compare against. Leave this group alone —
            # DEPENDENCY_ABSENT territory the per-pairing dispatch already
            # covers, not this rule's concern.
            continue
        total = sum(
            (Decimal(str(finding["value"])) for finding in findings), Decimal("0")
        )
        report_amount = Decimal(str(_decode(report_source.value)))
        input_pins = [_input_pin(report_source.finding_id)]
        input_pins.extend(_input_pin(finding["id"]) for finding in findings)
        if total > report_amount:
            blocked_any = True
            blocked_report_fact_ids.add(report_fact_id)
            run.record_named_block(
                rule_id=rule["id"],
                code=AGGREGATE_ACCRUED_EXCEEDS_REPORT,
                missing=[report_fact_id],
                pins=[*shared_pins, *input_pins],
            )
        else:
            published_any = True
            run.publish_symbol_finding(
                rule_id=rule["id"],
                symbol=f"{AGGREGATE_SUPPORTABILITY_SYMBOL_PREFIX}|{report_fact_id}",
                value=True,
                pins=[*shared_pins, *input_pins],
                source_name=AGGREGATE_SUPPORTABILITY_SYMBOL_PREFIX,
                source_fact_id=report_fact_id,
            )
    _retract_pairing_scoped_publications_for_blocked_groups(
        run,
        blocked_report_fact_ids=blocked_report_fact_ids,
        pairing_right=pairing_right,
    )
    run.resolved.add(rule["id"])
    if blocked_any and not published_any:
        return "blocked"
    return "published"


def dispatch_current_year_subtotal_on_run(run: Any, rule: Mapping[str, Any]) -> str:
    """Sum pairing-scoped current-year adjustments into the line-2b subtractand.

    Collects same-run publications whose symbol is the ADR-0071 current-year
    prefix; does not read the incumbent Schedule B form-row family. An empty
    set publishes 0, so T1 (no acquisition) still reaches taxable interest.

    When the aggregate-supportability
    check has blocked any report group this run, this rule does not
    silently publish a plain, ordinarily-supported subtotal that excludes
    the disputed group's contribution — that framing would overstate the
    result as "correct" when detecting a combined over-claim establishes only
    that the claimed set is unresolved. Instead the subtotal itself blocks, named
    with the same ``AGGREGATE_ACCRUED_EXCEEDS_REPORT`` code and the exact
    report fact id(s) still unresolved. ``rule.form1040-line2b`` requires
    this symbol, so the block propagates upward through the same
    missing-dependency mechanism every other blocked prerequisite already
    uses (no new schema or disposition shape) — line-2b itself blocks
    rather than presenting a confident, different taxable-interest number.
    A run with no aggregate block is entirely unaffected: this rule
    publishes its plain sum exactly as before.
    """
    blocked_report_fact_ids = _aggregate_blocked_report_fact_ids(run)
    rule_pin = {"role": rule.get("role", "computation"), "id": rule["id"], "version": rule["version"]}
    shared_pins = [
        dict(rule_pin),
        dict(run.ctx.adoption_pin),
        *(dict(p) for p in run.ctx.governance_pins),
    ]
    if blocked_report_fact_ids:
        run.record_named_block(
            rule_id=rule["id"],
            code=AGGREGATE_ACCRUED_EXCEEDS_REPORT,
            missing=sorted(blocked_report_fact_ids),
            pins=shared_pins,
        )
        run.resolved.add(rule["id"])
        return "blocked"

    total = Decimal("0")
    pins: list[dict[str, Any]] = list(shared_pins)
    prefix = CURRENT_YEAR_SYMBOL_PREFIX + "|"
    for pub in run.publications:
        symbol = pub.finding.get("symbol")
        if not isinstance(symbol, str) or not symbol.startswith(prefix):
            continue
        total += Decimal(str(pub.finding["value"]))
        pins.append(_input_pin(pub.finding["id"]))
    run.publish_symbol_finding(
        rule_id=rule["id"],
        symbol=CURRENT_YEAR_SUBTOTAL_SYMBOL,
        value=format(total, "f"),
        pins=pins,
        source_name=CURRENT_YEAR_SUBTOTAL_SYMBOL,
        source_fact_id=CURRENT_YEAR_SUBTOTAL_SYMBOL,
    )
    return "published"
