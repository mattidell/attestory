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
NOMINEE_ALLOCATIONS_EXCEED_REPORT = "NOMINEE_ALLOCATIONS_EXCEED_REPORT"
DEPENDENCY_ABSENT = "DEPENDENCY_ABSENT"
CITATION_ID = "tax.us.2025.citation.interest.nominee-reduction"

BOUND_SOURCE_RULE_IDS = frozenset({RULE_ID})

COLLECT_SOURCE_NAMES: tuple[str, ...] = (
    ALLOCATION_FACT_TYPE,
    REPORT_FACT_TYPE,
)


def is_nominee_reduction_rule(rule: Mapping[str, Any]) -> bool:
    return rule.get("id") == RULE_ID


@dataclass
class _ReportGroup:
    report: SourceFact | None = None
    allocations: list[SourceFact] = field(default_factory=list)


class NomineeIdentityError(ValueError):
    """A nominee-relevant source carries unusable or inconsistent identity.

    This is a loud, **execution-time** stop -- never a filter. A report or
    allocation that this run is supposed to consider must not disappear because
    its identity metadata is missing or disagrees with itself: silently dropping
    it would turn a real allocation into C0, a cross-year exclusion, or a
    smaller successful total -- all of which are wrong *tax* answers presented
    as ordinary ones.

    Scope, stated precisely because it is easy to overstate: this is **not** an
    intake or admission gate and **not** a product ``Refusal``. The recording
    contracts admit these values long before this coordinator sees them, and
    through ``live_coordinate_run`` this exception is raised *after* output
    paths are reserved and the start record is appended, leaving an open run
    and empty reserved outputs. See the milestone plan, "Substrate boundary --
    non-injective fact-id rendering", and the regression that pins that
    measured state.
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
    if not selected_any:
        _record_no_groups_selected(run, rule)
        return "inapplicable"
    if blocked_any and not published_any:
        return "blocked"
    return "published"
