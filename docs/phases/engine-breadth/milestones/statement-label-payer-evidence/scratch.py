"""P0 projection overlay. Loaded in memory from the ratified source."""

from __future__ import annotations

from collections import defaultdict
from functools import cache
import subprocess
import sys
from types import ModuleType

BASE = "f56d45ad450cc56f7d7559dbeed300ea27b3430e"
PROJECTION = "packages/derivation/presentation_projection.py"
PAGE = "packages/presentation/pages/citation-walk.v1.html"
TAX = "tax.us.2025."
B = TAX + "f1099b."
BOX4 = B + "statement-box4-withholding"
BOX7 = B + "statement-box7-loss-not-allowed"
SALE_TYPES = frozenset(B + term + "-txn" for term in (
    "covered-st", "covered-lt", "covered-w-st", "covered-w-lt",
    "noncovered-st", "noncovered-lt", "code-b-st", "code-b-lt",
))
BROKER = "tax.us.f1099b-broker"
# answer type -> (statement kind, party kind, current peer source types)
WITHHOLDING = {
    TAX + "f1099int.box4-withholding": (
        "tax.us.1099int-statement", "tax.us.interest-payer",
        tuple(TAX + "f1099int." + box for box in (
            "box1-interest", "box3-interest", "box8-tax-exempt-interest", "box10-market-discount",
        )),
    ),
    TAX + "f1099div.box4-withholding": (
        "tax.us.1099div-statement", "tax.us.dividend-payer",
        tuple(TAX + "f1099div." + box for box in (
            "box1a-ordinary", "box2a-capital-gain-distribution", "box12-exempt-interest-dividends",
        )),
    ),
    TAX + "f1099r.ira-box4-withholding": (
        "tax.us.1099r-statement", "tax.us.ira-payer", (TAX + "f1099r.ira-box1-taxable-distribution",),
    ),
    TAX + "f1099g.box4-withholding": (
        "tax.us.1099g-statement", "tax.us.unemployment-payer", (TAX + "f1099g.box1-unemployment",),
    ),
}
SSA = TAX + "ssa1099.box6-voluntary-withholding"
B_SPEC = ("tax.us.f1099b-statement", BROKER, SALE_TYPES | {B + "statement-anchor"})


def git(*args):
    return subprocess.check_output(["git", *args], text=True, timeout=20).strip()


def check_baseline():
    git("merge-base", "--is-ancestor", BASE, "HEAD")


def replace_once(source, anchor, replacement):
    if source.count(anchor) != 1:
        raise ValueError(f"expected one scratch anchor {anchor!r}")
    return source.replace(anchor, replacement, 1)


def sources():
    projection = git("show", f"{BASE}:{PROJECTION}") + "\n"
    page = git("show", f"{BASE}:{PAGE}") + "\n"
    return projection, page


def scratch_page(page):
    return replace_once(page, "[label.statement, label.lender]", "[label.statement, reason.statementPayerLabel, label.lender]")


def scratch_projection(source):
    source = replace_once(
        source,
        "    answer_explanations = _answer_explanation_sentences(",
        '    if statement_questions is not None:\n'
        '        statement_questions._p0_enabled = adopted_package == ("tax.us.2025.package.core-calculations", "v109")\n'
        '    answer_explanations = _answer_explanation_sentences(',
    )
    source = replace_once(
        source,
        "        targets: dict[str, dict[str, str]] = {}\n        for row in rows:",
        "        targets: dict[str, dict[str, str]] = {}\n"
        "        sources: dict[str, list[Mapping[str, Any]]] = {}\n        for row in rows:",
    )
    source = replace_once(source, "            targets.update(found)",
                          "            targets.update(found)\n"
                          "            for fact_id, _identity in found:\n"
                          "                sources.setdefault(fact_id, []).append(row)")
    source = replace_once(
        source,
        '            entries.append((label, fact_id, {"sentence": sentence, "statementLabel": statement_label}))',
        '            entry = {"sentence": sentence, "statementLabel": statement_label}\n'
        '            party = p0_party_label(statement_questions, fact_type, identity, sources[fact_id])\n'
        '            if party is not None:\n'
        '                entry["statementPayerLabel"] = party\n'
        '            entries.append((label, fact_id, entry))',
    )
    source = replace_once(
        source, '"statementLabel", "memberLabel", "memberOrdinal"}), rp)',
        '"statementLabel", "memberLabel", "memberOrdinal", "statementPayerLabel"}), rp)',
    )
    source = replace_once(
        source,
        '                label = reason.get("statementLabel", {})',
        '                label = reason.get("statementLabel", {})\n'
        '                if "statementPayerLabel" in reason:\n'
        '                    party = reason["statementPayerLabel"]\n'
        '                    if (not isinstance(party, str) or not party.strip()\n'
        '                            or not isinstance(label, dict) or not label.get("statement")\n'
        '                            or not label.get("taxYear") or "factId" in reason or "memberLabel" in reason):\n'
        '                        raise PresentationModelError(f"{rp}.statementPayerLabel: expected a recorded name beside a statement")',
    )
    return source


def normalized(label):
    return " ".join(label.split()).casefold()


def entity_label(walker, entity_id, kind):
    entity = walker._state.fact_state.entities.get(entity_id)
    if entity is not None and entity.status == "current" and entity.entity.get("kind") == kind:
        label = entity.entity.get("label")
        if isinstance(label, str) and label.strip():
            return label
    return None


def current_sources(walker, source_types):
    facts = walker._facts()
    return [
        fact for finding_id in walker._current_ids()
        if (finding := walker._state.findings.get(finding_id))
        and (fact := facts.get(finding.get("fact_id"))) is not None
        and fact.fact_type_id in source_types
    ]


def cohort(walker, spec, year, label, party_key):
    statement_kind, party_kind, source_types = spec
    peers = defaultdict(set)
    for fact in current_sources(walker, source_types):
        keys = dict(fact.keys)
        statement = keys.get("statement")
        if keys.get("tax-year") == year and entity_label(walker, statement, statement_kind) == label:
            peers[statement].add(keys.get(party_key))
    names = {}
    for statement, party_ids in peers.items():
        if len(party_ids) != 1:
            return {}
        party_id, = party_ids
        name = entity_label(walker, party_id, party_kind)
        if name is None:
            return {}
        names[statement] = (party_id, name)
    if len(names) < 2 or len({normalized(name) for _, name in names.values()}) != len(names):
        return {}
    return names


def pinned_brokers(walker, fact_type, statement, year, rows):
    """Require a single current broker on matching input findings for every attribution row."""
    current_ids = walker._current_ids()
    brokers = set()
    for row in rows:
        rule = walker._rules.get(str(row.get("artifact_id")))
        pairing, = walker._paired_nodes(rule, fact_type)
        matches = set()
        for pin in row.get("pins") or ():
            if pin.get("role") != "input":
                continue
            finding = walker._state.findings.get(pin["id"], {})
            fact = walker._facts().get(finding.get("fact_id"))
            if fact is None:
                if pin["id"] in walker._publications:
                    continue
                return set()
            if fact.fact_type_id not in pairing["income"]:
                continue
            keys = dict(fact.keys)
            if keys.get("statement") != statement:
                continue
            if (pin["id"] not in current_ids or keys.get("tax-year") != year
                    or not keys.get("broker")):
                return set()
            matches.add(keys["broker"])
        if len(matches) != 1:
            return set()
        brokers.update(matches)
    return brokers


def party_label(walker, fact_type, identity, rows):
    if not walker._p0_enabled:
        return None
    is_broker = fact_type in {BOX4, BOX7}
    spec = B_SPEC if is_broker else WITHHOLDING.get(fact_type)
    if spec is None:
        return None
    statement, year = identity.get("statement"), identity.get("tax-year")
    label = entity_label(walker, statement, spec[0])
    if label is None or not year:
        return None
    party_key = "broker" if is_broker else "payer"
    # Memoize per workspace and cohort. The coordinator state is fixed during projection.
    memo = vars(walker).setdefault("_p0_cohorts", {})
    key = (spec[0], year, label)
    if key not in memo:
        same_label = sum(
            entity_label(walker, entity_id, spec[0]) == label
            for entity_id in walker._state.fact_state.entities
        )
        memo[key] = cohort(walker, spec, year, label, party_key) if same_label > 1 else {}
    pair = memo[key].get(statement)
    if pair is None:
        return None
    party_id, name = pair
    ids = pinned_brokers(walker, fact_type, statement, year, rows) if is_broker else {identity.get("payer")}
    return name if ids == {party_id} else None


@cache
def projectors():
    baseline, _ = sources()
    builds = []
    for version, source in (("baseline", baseline), ("scratch", scratch_projection(baseline))):
        module = ModuleType(f"packages.derivation._statement_payer_{version}")
        sys.modules[module.__name__] = module
        module.p0_party_label = party_label
        exec(compile(source, PROJECTION, "exec"), vars(module))
        from packages.derivation import live

        module.PresentationModelError = live.PresentationModelError
        builds.append(module.build_presentation_model)
    return tuple(builds)
