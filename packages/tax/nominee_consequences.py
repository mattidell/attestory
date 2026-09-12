"""Report-local nominee-interest reduction consequences (ADR-0074).

The binding-path registry is the single nominee-rule-id constant that
package validation, live source registration, and the ``_Run.attempt``
intercept share. A schema-valid ``bound_sources`` rule whose id is absent
from this set is refused (``MEMBER_NO_BINDING_PATH``).

The coordinator owns identity filtering, year-scoping, outer-join
scheduling, C13 diagnosis, pin assembly, and mixed per-report outcomes.
Tax arithmetic stays in the adopted rule's declared ``value``.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field, replace
from decimal import Decimal
from typing import Any, Mapping, Sequence

from packages.derivation.evaluator import AccessLog, EvalBlocked, evaluate
from packages.derivation.runner import SourceFact, _sorted_pins
from packages.kernel.facts import fact_id_for
from packages.tax.report_statement_identity import REPORT_FACT_TYPE

RULE_ID = "tax.us.2025.rule.interest.nominee-reduction"
PUBLISHES = "tax.us.2025.interest.nominee-reduction"
ALLOCATION_FACT_TYPE = "tax.us.nominee-allocation.amount"
DERIVED_NOMINEE_SYMBOL = "tax.us.2025.interest.derived-nominee-subtotal"
LEGACY_NOMINEE_AMOUNT = "tax.us.2025.scheduleb.adjustment.nominee.amount"
LEGACY_NOMINEE_SUBTOTAL = "tax.us.2025.interest.scheduleb-nominee-subtotal"
LEGACY_NOMINEE_FAMILY = "tax.us.2025.scheduleb.adjustment.nominee"
LINE2B_RULE_ID = "tax.us.2025.rule.form1040-line2b"
LINE2B_SUCCESSOR_VERSION = "v7"
DECLARED_LINE2B_SCHEMA = "rule-artifact.v9"
DECLARED_LINE2B_VERSION = "v8"
NOMINEE_AGGREGATE_RULE_ID = "tax.us.2025.rule.interest.derived-nominee-subtotal"
NOMINEE_AGGREGATE_VERSION = "v1"
BOTH_PRESENT_MISSING = "legacy-and-derived-nominee-both-present"
NOMINEE_ALLOCATIONS_EXCEED_REPORT = "NOMINEE_ALLOCATIONS_EXCEED_REPORT"
DEPENDENCY_ABSENT = "DEPENDENCY_ABSENT"
DEPENDENCY_INVALID = "DEPENDENCY_INVALID"
DECLARATIVE_TOP_LEVEL_INVALID = "declarative-top-level-contract-invalid"
SELECTION_PATH_ID_DUPLICATE = "selection-path-id-duplicate"
CITATION_ID = "tax.us.2025.citation.interest.nominee-reduction"

BOUND_SOURCE_RULE_IDS = frozenset({RULE_ID})

COLLECT_SOURCE_NAMES: tuple[str, ...] = (
    ALLOCATION_FACT_TYPE,
    REPORT_FACT_TYPE,
)


def is_nominee_reduction_rule(rule: Mapping[str, Any]) -> bool:
    return rule.get("id") == RULE_ID


def is_line2b_nominee_successor(rule: Mapping[str, Any]) -> bool:
    """Return whether this is the bounded line-2b nominee-path successor.

    The successor keeps both the legacy and derived nominee symbols in its
    declared slot surface.  Their presence is a runtime policy choice: one
    path may be current, neither may be current, and both current is a
    refusal.  Keeping that union in the citizen lets package validation prove
    the same adjustment vocabulary is shared by line 2b and Schedule B while
    this helper preserves the absence semantics of the two paths.
    """
    return (
        rule.get("id") == LINE2B_RULE_ID
        and rule.get("version") == LINE2B_SUCCESSOR_VERSION
    )


def is_line2b_declared_selection_rule(rule: Mapping[str, Any]) -> bool:
    """Return the exact owner-authorized v9 line-2b selection citizen."""
    return (
        rule.get("schema") == DECLARED_LINE2B_SCHEMA
        and rule.get("id") == LINE2B_RULE_ID
        and rule.get("version") == DECLARED_LINE2B_VERSION
        and isinstance(rule.get("selection"), Mapping)
    )


def is_nominee_aggregate_rule(rule: Mapping[str, Any]) -> bool:
    """Return the distinct adopted v9 nominee aggregate producer."""
    return (
        rule.get("schema") == DECLARED_LINE2B_SCHEMA
        and rule.get("id") == NOMINEE_AGGREGATE_RULE_ID
        and rule.get("version") == NOMINEE_AGGREGATE_VERSION
        and isinstance(rule.get("aggregation"), Mapping)
    )


def declarative_top_level_is_neutral(rule: Mapping[str, Any]) -> bool:
    """Whether a v9 declarative variant has no ignored top-level state.

    The bounded contract keeps the ordinary rule fields present for schema
    compatibility, but their only admissible values are semantic no-ops.
    Runtime dispatch therefore cannot silently ignore a mutated guard,
    requirement, or pin declaration.
    """
    return (
        rule.get("when") is True
        and rule.get("requires") == []
        and rule.get("pins") == []
    )


def selection_path_ids_are_unique(rule: Mapping[str, Any]) -> bool:
    """Return whether every declared selection path has a unique id."""
    selection = rule.get("selection")
    if not isinstance(selection, Mapping):
        return False
    paths = selection.get("paths")
    if not isinstance(paths, list):
        return False
    path_ids: list[str] = []
    for path in paths:
        if not isinstance(path, Mapping) or not isinstance(path.get("id"), str):
            return False
        path_ids.append(path["id"])
    return len(path_ids) == len(set(path_ids))


def declared_path_pin_contract_is_truthful(
    declaration: Mapping[str, Any],
) -> bool:
    """Validate the bounded path/default input-pin metadata.

    Findings consumed by the selected expression are ordinary asserted inputs
    at v1.  The declaration may not relabel one as a default, point at a
    different version, duplicate it, or omit it.  Runtime pins still come
    from the evaluator access log; this predicate protects the declared
    contract before a path can execute.
    """
    requires = declaration.get("requires")
    pins = declaration.get("pins")
    if not isinstance(requires, list) or not isinstance(pins, list):
        return False
    if any(not isinstance(symbol, str) or not symbol for symbol in requires):
        return False
    if len(pins) != len(requires):
        return False
    pin_ids: list[str] = []
    for pin in pins:
        if not isinstance(pin, Mapping):
            return False
        if (
            pin.get("role") != "input"
            or pin.get("version") != "v1"
            or pin.get("origin") != "assertion"
            or not isinstance(pin.get("id"), str)
        ):
            return False
        pin_ids.append(pin["id"])
    return len(pin_ids) == len(set(pin_ids)) and set(pin_ids) == set(requires)


def _declared_selection_active_paths(
    run: Any, rule: Mapping[str, Any]
) -> list[Mapping[str, Any]]:
    """Evaluate only the v9 activity declarations, never inactive expressions."""
    selection = rule.get("selection")
    if not isinstance(selection, Mapping):
        return []
    active: list[Mapping[str, Any]] = []
    for path in selection.get("paths", []):
        if not isinstance(path, Mapping):
            continue
        activity = path.get("activity")
        if not isinstance(activity, Mapping):
            continue
        kind = activity.get("kind")
        if kind == "source_nonempty":
            member_pin = activity.get("member_fact_type")
            member_id = member_pin.get("id") if isinstance(member_pin, Mapping) else None
            if isinstance(member_id, str) and getattr(run, "sources", {}).get(member_id):
                active.append(path)
        elif kind == "derived_activity":
            fact_pin = activity.get("fact_type")
            fact_type_id = fact_pin.get("id") if isinstance(fact_pin, Mapping) else None
            if isinstance(fact_type_id, str):
                from packages.derivation.derived_enumeration import derived_activity_present

                if derived_activity_present(
                    publications=getattr(run, "publications", ()),
                    dispositions=getattr(run, "dispositions", ()),
                    fact_type_id=fact_type_id,
                ):
                    active.append(path)
    return active


def declared_selection_activity_pins(
    run: Any, rule: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """Pin the current evidence that makes each active path true.

    This intentionally repeats the same activity predicates as
    ``_declared_selection_active_paths``.  Legacy activity pins the current
    member findings; derived activity pins current report-scoped reduction
    findings or the input causes on a current blocked group.  No static path
    pin is treated as evidence, so displacement/retraction in the marshalled
    run cannot leave stale conflict provenance behind.
    """
    pins: list[dict[str, Any]] = []
    active_paths = _declared_selection_active_paths(run, rule)
    for path in active_paths:
        activity = path.get("activity")
        if not isinstance(activity, Mapping):
            continue
        kind = activity.get("kind")
        if kind == "source_nonempty":
            member_pin = activity.get("member_fact_type")
            member_id = member_pin.get("id") if isinstance(member_pin, Mapping) else None
            if not isinstance(member_id, str):
                continue
            for finding_id in getattr(run, "source_fids", {}).get(member_id, ()):
                if isinstance(finding_id, str):
                    pins.append(_input_pin(finding_id))
        elif kind == "derived_activity":
            fact_pin = activity.get("fact_type")
            fact_type_id = fact_pin.get("id") if isinstance(fact_pin, Mapping) else None
            if not isinstance(fact_type_id, str):
                continue
            from packages.derivation.derived_enumeration import enumerate_published_findings

            for finding in enumerate_published_findings(
                publications=getattr(run, "publications", ()),
                fact_type_id=fact_type_id,
            ):
                finding_id = finding.get("id")
                symbol = finding.get("symbol")
                if (
                    isinstance(finding_id, str)
                    and isinstance(symbol, str)
                    and (
                        symbol == fact_type_id
                        or symbol.startswith(fact_type_id + "|")
                    )
                ):
                    pins.append(_input_pin(finding_id))
            for row in getattr(run, "dispositions", ()):
                symbol = row.get("symbol") if isinstance(row, Mapping) else None
                if not (
                    isinstance(row, Mapping)
                    and row.get("disposition") == "blocked"
                    and isinstance(symbol, str)
                    and symbol.startswith(fact_type_id + "|")
                ):
                    continue
                pins.extend(
                    dict(pin)
                    for pin in row.get("pins", [])
                    if isinstance(pin, Mapping) and pin.get("role") == "input"
                )
    return _sorted_pins(pins)


def declared_line2b_selection_plan(
    run: Any, rule: Mapping[str, Any]
) -> tuple[str, Mapping[str, Any]]:
    """Return ``conflict``, ``path``, or ``default`` and its declaration."""
    selection = rule.get("selection")
    if not isinstance(selection, Mapping):
        return "default", {}
    active = _declared_selection_active_paths(run, rule)
    if len(active) > 1:
        refusal = selection.get("refusal", {})
        return "conflict", refusal if isinstance(refusal, Mapping) else {}
    if active:
        return "path", active[0]
    default = selection.get("default", {})
    return "default", default if isinstance(default, Mapping) else {}


def declared_line2b_selection_requires(
    run: Any, rule: Mapping[str, Any]
) -> list[str]:
    """Return top-level plus selected-path dependencies for eligibility."""
    plan, declaration = declared_line2b_selection_plan(run, rule)
    if plan == "conflict":
        return list(rule.get("requires", []))
    return list(rule.get("requires", [])) + list(declaration.get("requires", []))


@dataclass
class _ReportGroup:
    report: SourceFact | None = None
    allocations: list[SourceFact] = field(default_factory=list)


class NomineeIdentityError(ValueError):
    """A nominee-relevant source carries unusable or inconsistent identity.

    This is a loud stop -- never a filter. A report or
    allocation that this run is supposed to consider must not disappear because
    its identity metadata is missing or disagrees with itself: silently dropping
    it would turn a real allocation into C0, a cross-year exclusion, or a
    smaller successful total -- all of which are wrong *tax* answers presented
    as ordinary ones. On the production path, the same check runs as a bounded
    preflight and is converted to the live coordinator's typed
    ``NOMINEE_IDENTITY`` refusal before output reservation or a start record.
    The exception remains available as an in-run defense for fixture and
    lower-level coordinator callers.
    """


# The declared identity keys of each fact type this coordinator consumes, in
# the order ``fact_id_for`` renders them.
_EXPECTED_KEYS: dict[str, tuple[str, ...]] = {
    REPORT_FACT_TYPE: ("payer", "statement", "tax-year"),
    ALLOCATION_FACT_TYPE: ("payer", "statement", "tax-year", "recipient"),
}


def _ambiguous_rendering(keys: tuple[tuple[str, str], ...]) -> str | None:
    """The rendered id is non-injective for these bindings, if it is.

    ``facts._fact_id`` joins ``name=value`` pairs on "," without escaping. A
    value that itself contains ``,<keyname>=`` therefore renders
    indistinguishably from a different tuple of bindings -- two genuinely
    distinct reports can produce byte-identical fact ids, and the kernel
    lattice (a dict keyed on that rendering) collapses them before this
    coordinator sees either. Structured keys do **not** repair that: they
    avoid *re-parsing*, not the collision in the rendering itself.

    Detecting the hazard is possible from the bindings alone and costs
    nothing, so this coordinator stops rather than computing a tax result on
    an identity it cannot know is unique. The check is deliberately
    conservative -- it rejects a superset of the genuinely colliding cases --
    and it **protects nominee calculation only**; it does not repair the
    kernel's non-injective representation. Ordinary punctuation, including
    ordinary commas in payer names and statement references, is supported and
    is not what this rejects: only a delimiter-shaped ``,<key-name>=``
    sequence is. Repairing the rendering would mean changing the general
    fact-identity contract, which is an owner decision outside this milestone.
    """
    names = {name for name, _value in keys}
    for _name, value in keys:
        for other in names:
            if f",{other}=" in value:
                return other
    return None


def _validated_keys(source: SourceFact, expected: tuple[str, ...]) -> dict[str, str]:
    """Structured bindings for one relevant source, or a loud refusal."""
    what = f"{source.name} finding {source.finding_id!r}"
    if source.keys is None:
        raise NomineeIdentityError(
            f"{what} carries no structured identity keys; the nominee "
            "consequence cannot establish its report or year, and dropping it "
            "would silently change the tax result"
        )
    keys = dict(source.keys)
    missing = [name for name in expected if not keys.get(name)]
    if missing:
        raise NomineeIdentityError(f"{what} is missing identity component(s) {missing}")
    unexpected = sorted(set(keys) - set(expected))
    if unexpected:
        raise NomineeIdentityError(
            f"{what} carries unexpected identity component(s) {unexpected}"
        )
    if not source.fact_id:
        raise NomineeIdentityError(f"{what} has no fact_id to agree with its bindings")
    rendered = fact_id_for(source.name, tuple((name, keys[name]) for name in expected))
    if rendered != source.fact_id:
        raise NomineeIdentityError(
            f"{what} structured bindings disagree with its fact_id: "
            f"bindings render {rendered!r}, fact_id is {source.fact_id!r}"
        )
    collided = _ambiguous_rendering(source.keys)
    if collided is not None:
        raise NomineeIdentityError(
            f"{what} has an ambiguously rendered identity: a component value "
            f"contains ',{collided}=', so its fact_id does not uniquely "
            "identify these bindings. Track 1 is limited to uniquely rendered "
            "identities; repairing the rendering is an owner decision on the "
            "general fact-identity contract."
        )
    return keys


def _relevant(source: SourceFact) -> bool:
    return source.name in _EXPECTED_KEYS


def _validate_relevant_sources(sources: Sequence[SourceFact]) -> dict[str, dict[str, str]]:
    """Validate every relevant source *before* any filtering or grouping.

    Ordering matters: validating after the year filter would let an
    unestablished year hide the very defect this guards.
    """
    validated: dict[str, dict[str, str]] = {}
    for source in sources:
        if not _relevant(source):
            continue
        keys = _validated_keys(source, _EXPECTED_KEYS[source.name])
        validated[id(source)] = keys  # type: ignore[index]
    return validated


def _report_fact_id_from_allocation_keys(keys: Mapping[str, str]) -> str:
    return fact_id_for(
        REPORT_FACT_TYPE,
        (
            ("payer", keys["payer"]),
            ("statement", keys["statement"]),
            ("tax-year", keys["tax-year"]),
        ),
    )


def _group_symbol(report_fact_id: str) -> str:
    return f"{PUBLISHES}|{report_fact_id}"


def _input_pin(finding_id: str) -> dict[str, Any]:
    return {"role": "input", "id": finding_id, "version": "v1", "origin": "assertion"}


class NomineeCitationError(ValueError):
    """The adopted nominee rule does not declare a usable citation."""


def _citation_pin(rule: Mapping[str, Any]) -> dict[str, Any]:
    """The rule's own declared citation. No manufactured fallback.

    A pin is a provenance claim: inventing ``CITATION_ID`` when the adopted
    citizen declares nothing would assert an authority the run never read.
    Fail loudly instead -- a missing or malformed declaration is a content
    defect, not a condition to paper over.
    """
    citations = rule.get("citations") or []
    citation = citations[0] if citations else None
    if not isinstance(citation, Mapping):
        raise NomineeCitationError(
            f"rule {rule.get('id')!r} declares no citation; the nominee reduction "
            "cannot pin an authority it did not read"
        )
    cid = citation.get("id")
    version = citation.get("version")
    if not isinstance(cid, str) or not cid or not isinstance(version, str) or not version:
        raise NomineeCitationError(
            f"rule {rule.get('id')!r} declares a malformed citation {citation!r}; "
            "both id and version are required"
        )
    return {"role": "citation", "id": cid, "version": version}


def _build_universe(
    sources: Sequence[SourceFact], *, reporting_year: int | None
) -> dict[str, _ReportGroup]:
    """Outer-join universe over validated relevant sources.

    Every relevant source is validated **first**. Nothing relevant is ever
    dropped for want of identity: a source that cannot be established raises
    (``NomineeIdentityError``) rather than quietly becoming C0, a cross-year
    exclusion, or a smaller successful total. Only the *year* legitimately
    excludes a source from this execution, and it is read from bindings this
    function has already proved present and consistent.
    """
    relevant = [source for source in sources if _relevant(source)]
    keys_by_source = {
        id(source): _validated_keys(source, _EXPECTED_KEYS[source.name])
        for source in relevant
    }
    if reporting_year is None and relevant:
        raise NomineeIdentityError(
            "the run declares no reporting year, so no nominee source can be "
            "scoped to this execution; refusing rather than silently treating "
            "every report as out of scope"
        )
    universe: dict[str, _ReportGroup] = {}
    for source in relevant:
        keys = keys_by_source[id(source)]
        if keys["tax-year"] != str(reporting_year):
            continue  # a different tax year: an honest, established exclusion
        if source.name == REPORT_FACT_TYPE:
            assert source.fact_id is not None  # established by _validated_keys
            universe.setdefault(source.fact_id, _ReportGroup()).report = source
        else:
            report_fact_id = _report_fact_id_from_allocation_keys(keys)
            universe.setdefault(report_fact_id, _ReportGroup()).allocations.append(source)
    return universe


def validate_nominee_identity_sources(
    sources: Sequence[SourceFact], *, reporting_year: int | None
) -> None:
    """Validate the current nominee sources before a production run starts.

    The production marshaller supplies the exact current report and allocation
    sources that the v38 nominee rule can consume.  Reusing the same universe
    builder here keeps the pre-run boundary identical to the in-run guard:
    every relevant source is checked before year filtering, while unrelated
    return facts remain outside this bounded identity policy.  The builder's
    return value is intentionally discarded; this is an identity check, not a
    second calculation or a source-selection path.
    """
    _build_universe(sources, reporting_year=reporting_year)


def _shared_pins(run: Any, rule: Mapping[str, Any]) -> list[dict[str, Any]]:
    rule_pin = {
        "role": rule.get("role", "computation"),
        "id": rule["id"],
        "version": rule["version"],
    }
    return [
        dict(rule_pin),
        _citation_pin(rule),
        dict(run.ctx.adoption_pin),
        *(dict(p) for p in run.ctx.governance_pins),
    ]


def _present_pins(
    run: Any,
    rule: Mapping[str, Any],
    *,
    report: SourceFact | None,
    allocations: Sequence[SourceFact],
    access: AccessLog,
) -> list[dict[str, Any]]:
    pins = list(_shared_pins(run, rule))
    if report is not None:
        pins.append(_input_pin(report.finding_id))
    for allocation in allocations:
        pins.append(_input_pin(allocation.finding_id))
    pins.extend(run.dependency_pins_for_access(access))
    return _sorted_pins(pins)


def _record_no_groups_selected(run: Any, rule: Mapping[str, Any]) -> None:
    pins = _sorted_pins(
        [
            _citation_pin(rule),
            dict(run.ctx.adoption_pin),
            *(dict(p) for p in run.ctx.governance_pins),
        ]
    )
    run.dispositions.append(
        {
            "artifact_id": rule["id"],
            "disposition": "inapplicable",
            "no_groups_selected": True,
            "symbol": PUBLISHES,
            "pins": pins,
        }
    )


def _reduction_publications(run: Any) -> list[dict[str, Any]]:
    """Return current, published report-scoped nominee reductions only."""
    prefix = PUBLISHES + "|"
    return [
        pub.finding
        for pub in getattr(run, "publications", ())
        if isinstance(pub.finding.get("symbol"), str)
        and pub.finding["symbol"].startswith(prefix)
    ]


def _reduction_blocks(run: Any) -> list[dict[str, Any]]:
    """Return current report-scoped nominee blocks from the run ledger."""
    prefix = PUBLISHES + "|"
    return [
        row
        for row in getattr(run, "dispositions", ())
        if row.get("disposition") == "blocked"
        and isinstance(row.get("symbol"), str)
        and row["symbol"].startswith(prefix)
    ]


def _aggregate_block_details(
    blocked: Sequence[Mapping[str, Any]],
) -> tuple[str, list[str]]:
    """Propagate the truthful cause when a nominee group blocks aggregation.

    ``NOMINEE_ALLOCATIONS_EXCEED_REPORT`` is specific to an over-allocation
    group.  An absent current report is a different failure and must not be
    relabeled as an over-allocation merely because it prevents the same
    aggregate.  Preserve the strongest dependency cause and its missing ids;
    retain the established over-allocation code when every blocked group has
    that cause (and no missing dependency).
    """
    rows = list(blocked)
    absent_missing = sorted(
        {
            str(missing)
            for row in rows
            if row.get("code") == DEPENDENCY_ABSENT
            for missing in row.get("missing", [])
            if isinstance(missing, str)
        }
    )
    if absent_missing or any(row.get("code") == DEPENDENCY_ABSENT for row in rows):
        return DEPENDENCY_ABSENT, absent_missing

    invalid_missing = sorted(
        {
            str(missing)
            for row in rows
            if row.get("code") == DEPENDENCY_INVALID
            for missing in row.get("missing", [])
            if isinstance(missing, str)
        }
    )
    if invalid_missing or any(row.get("code") == DEPENDENCY_INVALID for row in rows):
        return DEPENDENCY_INVALID, invalid_missing

    if rows and all(
        row.get("code") in {None, NOMINEE_ALLOCATIONS_EXCEED_REPORT}
        for row in rows
    ):
        return NOMINEE_ALLOCATIONS_EXCEED_REPORT, []

    # This is a defensive fallback for a future nominee-group block code.  A
    # generic invalid dependency is safer than naming a cause the row did not
    # establish, while preserving any explicit missing identifiers.
    missing = sorted(
        {
            str(item)
            for row in rows
            for item in row.get("missing", [])
            if isinstance(item, str)
        }
    )
    return DEPENDENCY_INVALID, missing


def nominee_activity_present(run: Any) -> bool:
    """Whether the current run has supported nominee activity.

    A raw current allocation is enough to establish activity before the
    report-group dispatcher runs.  Once it has run, the suffixed publication
    or blocked disposition is the current consequence evidence.  No negative
    or zero-valued finding is manufactured for the absent case.
    """
    sources = getattr(run, "live_sources", getattr(run.ctx, "sources", ()))
    reporting_year = getattr(getattr(run, "ctx", None), "reporting_year", None)
    current_allocations: list[SourceFact] = []
    for source in sources:
        if source.name != ALLOCATION_FACT_TYPE:
            continue
        # ``_build_universe`` has already validated these structured keys on
        # the normal production path.  Reuse the bound year here instead of
        # treating an out-of-year allocation as current activity merely
        # because it is present in the projected source list.
        if reporting_year is None or source.keys is None:
            current_allocations.append(source)
            continue
        if dict(source.keys).get("tax-year") == str(reporting_year):
            current_allocations.append(source)
    return bool(
        current_allocations
        or _reduction_publications(run)
        or _reduction_blocks(run)
    )


def legacy_nominee_activity_present(run: Any) -> bool:
    """Whether a current legacy Schedule B nominee member is present."""
    return bool(getattr(run, "sources", {}).get(LEGACY_NOMINEE_AMOUNT, ()))


def nominee_aggregate_blocked(run: Any) -> bool:
    """Whether dispatcher B recorded a dependent aggregate block."""
    return any(
        row.get("disposition") == "blocked"
        and row.get("symbol") == DERIVED_NOMINEE_SYMBOL
        for row in getattr(run, "dispositions", ())
    )


def nominee_aggregation_enabled(run: Any) -> bool:
    """Whether the adopted graph contains the successor form consumers."""
    for candidate in getattr(getattr(run, "ctx", None), "rules", ()):
        # v9 gives the aggregate an adopted computation identity of its own.
        # Consumer presence must not activate the older report-rule-owned
        # aggregate once that producer is present.
        if is_nominee_aggregate_rule(candidate):
            return False
        if is_line2b_nominee_successor(candidate):
            return True
        if candidate.get("schema") == "attachment-rule.v11":
            return True
    return False


def dispatch_nominee_aggregate_producer_on_run(
    run: Any, rule: Mapping[str, Any]
) -> str:
    """Publish the v9 nominee aggregate under its own computation identity."""
    if not declarative_top_level_is_neutral(rule):
        run.record_named_block(
            rule_id=rule["id"],
            code=DEPENDENCY_INVALID,
            missing=[DECLARATIVE_TOP_LEVEL_INVALID],
            pins=_sorted_pins(_shared_pins(run, rule)),
            symbol=DERIVED_NOMINEE_SYMBOL,
        )
        run.resolved.add(rule["id"])
        setattr(run, "_declared_nominee_aggregate_status", "blocked")
        return "blocked"

    status = getattr(run, "_declared_nominee_aggregate_status", None)
    if status is not None:
        return str(status)

    aggregation = rule.get("aggregation")
    expected = {
        "mode": "sum",
        "source_fact_type": {"id": PUBLISHES, "version": "v1"},
        "source_symbol_prefix": PUBLISHES + "|",
        "source_rule": {"id": RULE_ID, "version": "v1"},
        "absence": "inapplicable",
        "blocked": "propagate",
    }
    malformed = not isinstance(aggregation, Mapping) or any(
        aggregation.get(key) != value for key, value in expected.items()
    )
    if malformed:
        pins = _shared_pins(run, rule)
        run.record_named_block(
            rule_id=rule["id"],
            code=DEPENDENCY_INVALID,
            missing=["nominee-aggregate-contract-invalid"],
            pins=_sorted_pins(pins),
            symbol=DERIVED_NOMINEE_SYMBOL,
        )
        run.resolved.add(rule["id"])
        setattr(run, "_declared_nominee_aggregate_status", "blocked")
        return "blocked"

    blocked = _reduction_blocks(run)
    published = _reduction_publications(run)
    if blocked:
        pins = list(_shared_pins(run, rule))
        for row in blocked:
            pins.extend(
                dict(pin) for pin in row.get("pins", []) if isinstance(pin, Mapping)
            )
        block_code, block_missing = _aggregate_block_details(blocked)
        run.record_named_block(
            rule_id=rule["id"],
            code=block_code,
            missing=block_missing,
            pins=_sorted_pins(pins),
            symbol=DERIVED_NOMINEE_SYMBOL,
        )
        run.resolved.add(rule["id"])
        setattr(run, "_declared_nominee_aggregate_status", "blocked")
        return "blocked"

    if not published:
        run.dispositions.append({
            "artifact_id": rule["id"],
            "disposition": "inapplicable",
            "no_source_activity": True,
            "pins": _sorted_pins(_shared_pins(run, rule)),
        })
        run.resolved.add(rule["id"])
        setattr(run, "_declared_nominee_aggregate_status", "inapplicable")
        return "inapplicable"

    total = sum(
        (Decimal(str(finding["value"])) for finding in published), Decimal("0")
    )
    pins = list(_shared_pins(run, rule))
    pins.extend(_input_pin(str(finding["id"])) for finding in published)
    run.publish_symbol_finding(
        rule_id=rule["id"],
        symbol=DERIVED_NOMINEE_SYMBOL,
        value=format(total, "f"),
        pins=_sorted_pins(pins),
        source_name=DERIVED_NOMINEE_SYMBOL,
        source_fact_id=DERIVED_NOMINEE_SYMBOL,
    )
    setattr(run, "_declared_nominee_aggregate_status", "published")
    return "published"


def dispatch_nominee_aggregate_on_run(run: Any, rule: Mapping[str, Any]) -> str:
    """Dispatch the selected Candidate-B form-facing nominee aggregate.

    The aggregate enumerates only suffixed, current report-scoped nominee
    reductions.  A blocked report group blocks the aggregate, while a
    published sibling remains available in the run ledger.  With no current
    group outcome this function is intentionally silent: I0 has no derived
    nominee subtotal and no invented zero.
    """
    status = getattr(run, "_nominee_aggregate_status", None)
    if status is not None:
        return str(status)

    blocked = _reduction_blocks(run)
    published = _reduction_publications(run)
    if blocked:
        pins = list(_shared_pins(run, rule))
        for row in blocked:
            pins.extend(dict(pin) for pin in row.get("pins", []) if isinstance(pin, Mapping))
        block_code, block_missing = _aggregate_block_details(blocked)
        run.record_named_block(
            rule_id=rule["id"],
            # The report-scoped rows retain their own symbols/pins; the
            # aggregate is a single dependent block, not a second synthetic
            # group outcome.  Preserve an absent-report cause instead of
            # relabeling it as over-allocation.
            code=block_code,
            missing=block_missing,
            pins=_sorted_pins(pins),
            symbol=DERIVED_NOMINEE_SYMBOL,
        )
        run.resolved.add(rule["id"])
        setattr(run, "_nominee_aggregate_status", "blocked")
        return "blocked"

    if not published:
        setattr(run, "_nominee_aggregate_status", "inapplicable")
        return "inapplicable"

    total = sum(
        (Decimal(str(finding["value"])) for finding in published), Decimal("0")
    )
    pins = list(_shared_pins(run, rule))
    pins.extend(_input_pin(str(finding["id"])) for finding in published)
    run.publish_symbol_finding(
        rule_id=rule["id"],
        symbol=DERIVED_NOMINEE_SYMBOL,
        value=format(total, "f"),
        pins=_sorted_pins(pins),
        source_name=DERIVED_NOMINEE_SYMBOL,
        source_fact_id=DERIVED_NOMINEE_SYMBOL,
    )
    setattr(run, "_nominee_aggregate_status", "published")
    return "published"


def _without_nominee_refs(node: Any, removed: frozenset[str]) -> Any:
    """Remove optional nominee refs from the known rule expression grammar."""
    if isinstance(node, dict):
        if node.get("op") == "ref" and node.get("name") in removed:
            return None
        if node.get("op") == "require_closed" and node.get("source_set") in removed:
            return None
        out: dict[str, Any] = {}
        for key, value in node.items():
            if key == "args" and isinstance(value, list):
                out[key] = [
                    child
                    for item in value
                    if (child := _without_nominee_refs(item, removed)) is not None
                ]
                continue
            child = _without_nominee_refs(value, removed)
            if child is not None:
                out[key] = child
        return out
    if isinstance(node, list):
        return [
            child
            for item in node
            if (child := _without_nominee_refs(item, removed)) is not None
        ]
    return node


def line2b_effective_requires(run: Any, rule: Mapping[str, Any]) -> list[str]:
    """Return line-2b dependencies after selecting the current nominee path."""
    if not is_line2b_nominee_successor(rule):
        return list(rule.get("requires", []))
    legacy = legacy_nominee_activity_present(run)
    derived = nominee_activity_present(run) or DERIVED_NOMINEE_SYMBOL in getattr(run, "symbols", {})
    removed: set[str] = set()
    # Keep the policy check reachable even when one path has not produced a
    # subtotal (for example, a malformed legacy closure).  Both-present is a
    # bounded refusal, not a numeric/dependency comparison, so it must not be
    # masked by requiring both optional symbols first.
    if legacy and derived:
        removed.update({LEGACY_NOMINEE_SUBTOTAL, DERIVED_NOMINEE_SYMBOL})
    elif not legacy:
        removed.add(LEGACY_NOMINEE_SUBTOTAL)
    if not derived or nominee_aggregate_blocked(run):
        removed.add(DERIVED_NOMINEE_SYMBOL)
    return [req for req in rule.get("requires", []) if req not in removed]


def prepare_line2b_nominee_successor(
    run: Any, rule: Mapping[str, Any]
) -> tuple[str, dict[str, Any] | None]:
    """Select or refuse the successor's legacy/new nominee adjustment paths."""
    if not is_line2b_nominee_successor(rule):
        return "ordinary", dict(rule)

    legacy = legacy_nominee_activity_present(run)
    derived = nominee_activity_present(run) or DERIVED_NOMINEE_SYMBOL in getattr(run, "symbols", {})
    if legacy and derived:
        return "refuse", None
    if derived and nominee_aggregate_blocked(run):
        return "blocked", None

    removed: set[str] = set()
    if not legacy:
        removed.update({LEGACY_NOMINEE_SUBTOTAL, LEGACY_NOMINEE_FAMILY})
    if not derived:
        removed.add(DERIVED_NOMINEE_SYMBOL)
    prepared = copy.deepcopy(dict(rule))
    prepared["_runtime_nominee_paths"] = True
    prepared["requires"] = [
        req for req in prepared.get("requires", []) if req not in removed
    ]
    for key in ("when", "value"):
        prepared[key] = _without_nominee_refs(prepared.get(key), frozenset(removed))
    return "ready", prepared


def dispatch_nominee_consequences_on_run(run: Any, rule: Mapping[str, Any]) -> str:
    """Classify every report-group key once and evaluate selected groups.

    C0 option 1: report-only keys are not invoked. Zero selected groups
    records the rule-level ``no_groups_selected`` inapplicable row.
    """
    sources = getattr(run, "live_sources", run.ctx.sources)
    universe = _build_universe(
        sources, reporting_year=getattr(run.ctx, "reporting_year", None)
    )
    published_any = False
    blocked_any = False
    selected_any = False

    for report_fact_id in sorted(universe):
        group = universe[report_fact_id]
        allocations = sorted(
            group.allocations, key=lambda source: source.fact_id or ""
        )
        if not allocations:
            continue
        selected_any = True
        symbol = _group_symbol(report_fact_id)
        if group.report is None:
            blocked_any = True
            run.record_named_block(
                rule_id=rule["id"],
                code=DEPENDENCY_ABSENT,
                missing=[report_fact_id],
                pins=_present_pins(
                    run, rule, report=None, allocations=allocations, access=AccessLog()
                ),
                symbol=symbol,
            )
            continue

        access = AccessLog()
        local_env = replace(
            run.env(),
            symbols={REPORT_FACT_TYPE: group.report.value},
            sources={},
            bound_sources={
                ALLOCATION_FACT_TYPE: [source.value for source in allocations]
            },
        )
        try:
            value = evaluate(rule["value"], local_env, access)
        except EvalBlocked as exc:
            blocked_any = True
            code = exc.category
            missing = list(exc.missing)
            if code == NOMINEE_ALLOCATIONS_EXCEED_REPORT:
                missing = []
            run.record_named_block(
                rule_id=rule["id"],
                code=code,
                missing=missing,
                pins=_present_pins(
                    run,
                    rule,
                    report=group.report,
                    allocations=allocations,
                    access=access,
                ),
                symbol=symbol,
            )
            continue

        published_any = True
        amount = value if isinstance(value, Decimal) else Decimal(str(value))
        run.publish_symbol_finding(
            rule_id=rule["id"],
            symbol=symbol,
            value=format(amount, "f"),
            pins=_present_pins(
                run,
                rule,
                report=group.report,
                allocations=allocations,
                access=access,
            ),
            source_name=PUBLISHES,
            source_fact_id=report_fact_id,
        )

    run.resolved.add(rule["id"])
    # The v9 production graph has a distinct aggregate producer.  Once the
    # declared line-2b selection is present, report-rule dispatch must not
    # activate the historical consumer-owned aggregate as a side effect.  The
    # exact identity guard remains active even for a malformed/missing
    # aggregate citizen so an invalid successor cannot silently fall back to
    # the old hidden path.
    declared_selection_present = any(
        is_line2b_declared_selection_rule(candidate)
        for candidate in getattr(getattr(run, "ctx", None), "rules", ())
    )
    if not declared_selection_present and nominee_aggregation_enabled(run):
        dispatch_nominee_aggregate_on_run(run, rule)
    if not selected_any:
        _record_no_groups_selected(run, rule)
        return "inapplicable"
    if blocked_any and not published_any:
        return "blocked"
    return "published"
