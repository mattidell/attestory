"""Static survey of unguarded ``collect`` sites in a core package.

Lifted from the milestone's P0 survey (collect-closure-survey-evidence/survey.py) so the
regression test can run it on any core package. Reads the package and its members from
``packages/content``; never runs a return. The symbol graph is a deliberate
over-approximation (it follows refs in branches that may not run), so an ``unguarded``
entry is a candidate that the live cases in tests/test_collect_closure.py confirm or
refute.
"""

from __future__ import annotations

import glob
import json
import sys
from collections import defaultdict, deque
from collections.abc import Iterator
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "packages" / "content" / "tax" / "2025"


def walk(node: Any) -> Iterator[dict[str, Any]]:
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)


def conjunct_closed(when: Any) -> set[str]:
    """Source sets a ``when`` requires closed on every evaluation (single
    ``require_closed`` or a conjunction (``all``) of them, nested)."""
    if not isinstance(when, dict):
        return set()
    if when.get("op") == "require_closed":
        return {when["source_set"]}
    if when.get("op") == "all":
        out: set[str] = set()
        for arg in when.get("args", []):
            out |= conjunct_closed(arg)
        return out
    return set()


def collect_sites(node: Any, inherited: frozenset[str]) -> Iterator[tuple[dict[str, Any], frozenset[str]]]:
    """Yield ``(collect node, source sets closed by every enclosing rule or selection-path
    ``when``)``. A dict with a ``when`` and no ``op`` is a rule or a selection path; a dict
    with an ``op`` (``choose``, ``all``...) is an expression, whose ``when`` is a condition
    and guards nothing."""
    if isinstance(node, dict):
        guards = inherited
        if "op" not in node and "when" in node:
            guards = inherited | frozenset(conjunct_closed(node["when"]))
        if node.get("op") == "collect":
            yield node, guards
        for k, v in node.items():
            if k == "when" and "op" not in node:
                continue
            yield from collect_sites(v, guards)
    elif isinstance(node, list):
        for v in node:
            yield from collect_sites(v, inherited)


def any_closed(when: Any) -> set[str]:
    return {n["source_set"] for n in walk(when) if n.get("op") == "require_closed"}


_NON_READS = ("id", "publishes", "pins", "blocked", "citations", "notes", "scope", "role", "schema", "version")


def strings(node: Any) -> Iterator[str]:
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from strings(v)


def reads_of(member: dict[str, Any], published: set[str], composition_of: dict[str, str]) -> set[str]:
    """Every published symbol a node can read: its ``requires``, every ``ref`` (value and
    when), and any published-symbol string anywhere else in the body (selection tables,
    attachment itemizations, and so on), plus the symbol of a composition it names.
    Deliberately an over-approximation; the live probe is what confirms or refutes."""
    out = set(member.get("requires") or [])
    body = {k: v for k, v in member.items() if k not in _NON_READS}
    out |= {s for s in strings(body) if s in published}
    comp = member.get("composition")
    if isinstance(comp, dict) and comp.get("id") in composition_of:
        out.add(composition_of[comp["id"]])
    out.discard(member.get("publishes"))
    return out


def survey(package_path: Path) -> dict[str, Any]:
    """The P0 survey of one core package: every collect not guarded at its own site, with
    the bound fields it reaches and the rules that cut each path."""
    package = json.loads(package_path.read_text())
    index: dict[tuple[str, str], tuple[str, dict[str, Any]]] = {}
    for f in glob.glob(str(CONTENT / "*.json")):
        try:
            j = json.loads(Path(f).read_text())
        except ValueError:
            continue
        if isinstance(j, dict) and "id" in j and "version" in j:
            index[(j["id"], j["version"])] = (Path(f).name, j)

    members = [(m, index[(m["id"], m["version"])][1]) for m in package["members"]]
    # Every member that publishes a symbol is a graph node: rules, but also the
    # taxable-interest composition, attachment rules, the W-2 field mapping and the
    # checked-conclusion binding.
    rules = {m["id"]: j for m, j in members if "publishes" in j}
    computation = {m["id"] for m, j in members if m["role"] == "computation"}
    # Attachment citizens (Schedule D, Schedule 1, ...) are published outputs like a form
    # field: a path to one counts as reaching a published output.
    attachments = {m["id"] for m, j in members if m["role"] == "attachment-rule"}
    producers: dict[str, list[str]] = defaultdict(list)
    for rid, r in rules.items():
        producers[r["publishes"]].append(rid)
    published = set(producers)
    families = {j["id"]: j for m, j in members if m["role"] == "source-family"}
    # Mirrors packages.derivation.package_validation._is_constrained: a family with
    # member constraints, identity exclusivity, itemizations or completeness gets a
    # synthesized `<family>.member-validation` prerequisite on every rule that reads
    # its subtotal or names its source set; that prerequisite blocks while the family
    # is not closed (runner._evaluate_family_validation).
    constrained = {fid for fid, f in families.items()
                   if f.get("member_constraints") or f.get("identity_exclusivity")
                   or f.get("itemizations") or f.get("completeness")}
    # A family that `projects_from` a constrained family is widened into the constrained
    # set by the compiler (_constrained_closure), so it is forced the same way.
    projected = {fid for fid, f in families.items()
                 if isinstance(f.get("projects_from"), dict) and f["projects_from"].get("id") in constrained}
    constrained |= projected
    fields = {j["binds_symbol"]: j["id"] for m, j in members if m["schema"].startswith("form-field")}

    composition_of = {j["id"]: j["publishes"] for m, j in members if m["role"] == "composition"}
    consumers: dict[str, set[str]] = defaultdict(set)   # symbol -> node ids that read it
    for rid, r in rules.items():
        for sym in reads_of(r, published, composition_of):
            consumers[sym].add(rid)
    other_consumers: dict[str, set[str]] = defaultdict(set)
    for sym, ids in consumers.items():
        other_consumers[sym] = {i for i in ids if i not in computation}

    def downstream_any(start: str | None) -> list[str]:
        """Every bound field downstream of a published symbol, guards ignored."""
        out: set[str] = set()
        seen_all: set[str] = set()
        qa = deque([start] if start else [])
        while qa:
            sym = qa.popleft()
            if sym in seen_all:
                continue
            seen_all.add(sym)
            if sym in fields:
                out.add(sym)
            for cid in consumers.get(sym, ()):
                if rules[cid].get("publishes"):
                    qa.append(rules[cid]["publishes"])
        return sorted(out)

    inventory: list[dict[str, Any]] = []
    guarded_sites: list[dict[str, Any]] = []
    no_source_set: list[dict[str, Any]] = []
    for rid, r in sorted(rules.items()):
        if rid not in computation:
            continue
        sites = [(n, set(g)) for n, g in collect_sites({k: v for k, v in r.items() if k not in ("pins", "blocked")}, frozenset())]
        for n in walk(r.get("when")):
            if n.get("op") == "collect":
                sites.append((n, set()))
        if not sites:
            continue
        own_closed = conjunct_closed(r.get("when"))
        counted = {n["source_set"] for n in walk(r.get("value")) if n.get("op") == "count"}
        collects = [n for n, _ in sites]
        outside: list[dict[str, Any]] = []
        for c, site_guards in sites:
            if c.get("source_set") in site_guards:
                guarded_sites.append({"rule": rid, "version": r["version"], "source_set": c.get("source_set"),
                                      "publishes": r.get("publishes"),
                                      "bound_fields_downstream_any_path": downstream_any(r.get("publishes")),
                                      "guard": "enclosing when" if c.get("source_set") in own_closed else "enclosing selection-path when"})
        sites_by_id = {id(c): g for c, g in sites}
        for c in collects + outside:
            ss = c.get("source_set")
            if ss is None:
                no_source_set.append({"rule": rid, "version": r["version"], "collects": c["name"],
                                      "publishes": r.get("publishes")})
                continue
            if ss in sites_by_id[id(c)]:
                continue
            forced = ss in constrained
            entry: dict[str, Any] = {
                "rule": rid, "version": r["version"], "schema": r["schema"], "source_set": ss,
                "collects": c["name"], "source_set_is_declared_family": ss in families,
                "family_constrained_member_validation_forces_closure": forced,
                "publishes": r.get("publishes"),
                "other_sets_collected_by_rule": sorted({n.get("source_set") for n in collects if n.get("source_set") not in (None, ss)}),
                "own_when_guards": sorted(own_closed),
                "own_when_nested_guards": sorted(any_closed(r.get("when")) - own_closed),
                "same_rule_count_over_set": ss in counted,
                "same_rule_count_in_when": ss in {n["source_set"] for n in walk(r.get("when")) if n.get("op") == "count"},
                "has_subject": "subject" in r,
                "collect_outside_value_or_when": bool(outside),
            }
            # Walk forward from the published symbol, cutting at any rule that
            # conjunctively requires ss closed.
            start = r.get("publishes")
            # A rule is held for this set when its own ``when`` requires the set closed or one
            # of its hard ``requires`` is published by a held rule: it cannot publish while
            # the set is unclosed, whatever else it reads. (The graph above also follows refs
            # in branches that may not run; ``requires`` is the only certain dependency.)
            held = {cid for cid, cr in rules.items() if ss in conjunct_closed(cr.get("when"))}
            grew = True
            while grew:
                grew = False
                held_symbols = {rules[h]["publishes"] for h in held if rules[h].get("publishes")}
                for cid, cr in rules.items():
                    if cid not in held and held_symbols & set(cr.get("requires") or []):
                        held.add(cid)
                        grew = True
            seen_syms: set[str] = set()
            guarded_at: set[str] = set()
            reach_fields: set[str] = set()
            reach_other: set[str] = set()
            reach_rules: set[str] = set()
            q = deque([start] if start else [])
            while q:
                sym = q.popleft()
                if sym in seen_syms:
                    continue
                seen_syms.add(sym)
                if sym in fields:
                    reach_fields.add(sym)
                for cid in sorted(consumers.get(sym, ())):
                    cr = rules[cid]
                    if cid not in computation:
                        reach_other.add(cid)
                    if cid in held:
                        guarded_at.add(cid)
                        continue
                    reach_rules.add(cid)
                    if cr.get("publishes"):
                        q.append(cr["publishes"])
            # Every bound field downstream of the published symbol whether or not a guard sits
            # on the path (what the live probe filters on).
            every: set[str] = set()
            seen_all: set[str] = set()
            qa = deque([start] if start else [])
            while qa:
                sym = qa.popleft()
                if sym in seen_all:
                    continue
                seen_all.add(sym)
                if sym in fields:
                    every.add(sym)
                for cid in consumers.get(sym, ()):
                    if rules[cid].get("publishes"):
                        qa.append(rules[cid]["publishes"])
            entry["bound_fields_downstream_any_path"] = sorted(every)
            entry["reaches_bound_fields_unguarded"] = sorted(reach_fields)
            entry["reaches_other_consumers_unguarded"] = sorted(reach_other)
            entry["reaches_attachments_unguarded"] = sorted(reach_other & attachments)
            entry["guarding_rules_on_paths"] = sorted(guarded_at)
            entry["unguarded_rules_on_paths"] = sorted(reach_rules)
            entry["published_symbol_is_bound_directly"] = start in fields
            if forced:
                entry["auto_class"] = "forced-by-member-validation"
            elif entry["same_rule_count_in_when"]:
                # `count` raises SOURCE_SET_UNCLOSED unless the set is closed, and the
                # rule's own `when` evaluates it first.
                entry["auto_class"] = "guarded-by-own-count-in-when"
            elif reach_fields or reach_other:
                entry["auto_class"] = "unguarded"
            else:
                entry["auto_class"] = "guarded-or-no-bound-line"
            inventory.append(entry)

    counts: dict[str, int] = defaultdict(int)
    for e in inventory:
        counts[e["auto_class"]] += 1
    out = {
        "package": {"id": package["id"], "version": package["version"]},
        "rules_in_package": len(rules),
        "form_fields_in_package": len(fields),
        "graph_nodes": len(rules),
        "source_families_in_package": len(families),
        "constrained_families": sorted(constrained),
        "inventory_count": len(inventory),
        "collect_sites_total": len(inventory) + len(guarded_sites) + len(no_source_set),
        "collect_sites_guarded_at_own_site": len(guarded_sites),
        "auto_class_counts": dict(counts),
        "inventory": inventory,
        "collects_guarded_at_their_own_site": guarded_sites,
        "collects_without_source_set": no_source_set,
    }
    return out
