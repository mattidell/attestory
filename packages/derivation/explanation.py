"""Explanation walker: 'explain this number' as rendering, not research.

A derived finding carries its full lineage as role-bearing pins (ADR-0007/0009).
This walker turns those pins into an explanation tree: the value, the rule that
produced it, the input findings it consumed (recursing into any that are
themselves derived), and the parameters, operation-semantics, adoption, and
governance it stood on. Because the pins are on the finding, explanation is a
traversal of committed data — never a re-evaluation, and never a guess.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from packages.derivation.authorization import AuthorizationResolution, authorization_provenance
from packages.derivation.explanation_graph import GraphBuilder, render_graph, validate_graph, validate_output_schema

_RULE_ROLES = frozenset({"computation", "applicability", "field-mapping", "cross-form-bridge"})
_DEPENDENCY_ROLES = frozenset({"input", "choice"})


@dataclass(frozen=True)
class ExplanationNode:
    finding_id: str
    role: str                       # how this node was pinned by its parent ("output" at the root)
    kind: str                       # derived | input | parameter | operation-semantics | adoption | governance | ...
    symbol: str | None
    value: str | None
    version: str
    produced_by: dict[str, Any] | None
    children: tuple["ExplanationNode", ...]

    def to_dict(self) -> dict[str, Any]:
        node: dict[str, Any] = {
            "finding_id": self.finding_id,
            "role": self.role,
            "kind": self.kind,
            "symbol": self.symbol,
            "value": self.value,
            "version": self.version,
            "produced_by": self.produced_by,
            "children": [child.to_dict() for child in self.children],
        }
        return node


def index_derived(findings: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for finding in findings:
        identifier = finding["id"]
        if identifier in indexed and indexed[identifier] != finding:
            raise ValueError("conflicting finding identity")
        indexed[identifier] = finding
    return indexed


def explain_legacy(
    finding_id: str,
    *,
    role: str,
    derived: dict[str, dict[str, Any]],
    inputs: dict[str, dict[str, Any]] | None = None,
    authorization: AuthorizationResolution | None = None,
    _seen: frozenset[str] = frozenset(),
    _memo: dict[str, ExplanationNode] | None = None,
) -> ExplanationNode:
    """Explain one finding by walking its pins. `role` is how the parent cited it.

    ``authorization`` is attached only at the walk's root as a provenance
    sibling. Recursion does not re-attach it (the grant is run-scoped, not
    per-pin). Published pin-role enums do not yet name this kind; see
    ``authorization_provenance`` for the deferred schema-successor follow-on.
    """
    inputs = inputs or {}
    is_root = not _seen
    if finding_id in _seen:
        raise ValueError("CYCLIC_DEPENDENCY_ERROR")

    if _memo is not None and finding_id in _memo:
        return _attach_root_authorization(_memo[finding_id], authorization, is_root)

    if finding_id in derived:
        finding = derived[finding_id]
        produced_by: dict[str, Any] | None = None
        children: list[ExplanationNode] = []
        seen = _seen | {finding_id}
        for pin in finding["pins"]:
            pin_role = pin["role"]
            if pin_role in _RULE_ROLES:
                produced_by = pin
            elif pin_role in _DEPENDENCY_ROLES:
                children.append(explain_legacy(
                    pin["id"],
                    role=pin_role,
                    derived=derived,
                    inputs=inputs,
                    _seen=seen,
                    _memo=_memo,
                ))
            else:
                children.append(_leaf(pin["id"], pin_role, pin_role, pin["version"]))
        children.sort(key=lambda c: (c.role, c.finding_id))
        node = ExplanationNode(
            finding_id=finding_id,
            role=role,
            kind="derived",
            symbol=finding["symbol"],
            value=finding["value"],
            version=finding["version"],
            produced_by=produced_by,
            children=tuple(children),
        )
        if _memo is not None:
            _memo[finding_id] = node
        return _attach_root_authorization(node, authorization, is_root)

    # A leaf: a human input finding (if we know it) or a bare pinned reference.
    meta = inputs.get(finding_id)
    if meta is not None:
        node = ExplanationNode(
            finding_id=finding_id,
            role=role,
            kind=meta.get("role", "input"),
            symbol=meta.get("symbol"),
            value=meta.get("value"),
            version="v1",
            produced_by=None,
            children=(),
        )
        if _memo is not None:
            _memo[finding_id] = node
        return _attach_root_authorization(node, authorization, is_root)
    node = _leaf(finding_id, role, role, "v1")
    if _memo is not None:
        _memo[finding_id] = node
    return _attach_root_authorization(node, authorization, is_root)


class ExplanationGraph:
    """Shared output for a single root, with explicit compatibility conversion."""

    def __init__(self, builder: GraphBuilder) -> None:
        self.builder = builder

    def to_dict(self) -> dict[str, Any]:
        return self.builder.to_dict()


def explain(
    finding_id: str, *, role: str, derived: dict[str, dict[str, Any]],
    inputs: dict[str, dict[str, Any]] | None = None,
    authorization: AuthorizationResolution | None = None,
) -> ExplanationGraph:
    builder = GraphBuilder(derived, inputs)
    builder.add_root(finding_id, role=role,
                     authorization=authorization_provenance(authorization) if authorization is not None else None)
    return ExplanationGraph(builder)


def _attach_root_authorization(
    node: ExplanationNode,
    authorization: AuthorizationResolution | None,
    is_root: bool,
) -> ExplanationNode:
    if authorization is None or not is_root:
        return node
    extra = ExplanationNode(
        finding_id=authorization.grant_id or "authorization.none",
        role="authorization",
        kind="authorization",
        symbol=None,
        value=authorization.status,
        version="v1",
        produced_by=None,
        children=(),
    )
    children = tuple(sorted(node.children + (extra,), key=lambda c: (c.role, c.finding_id)))
    return replace(node, children=children)


def _leaf(finding_id: str, role: str, kind: str, version: str) -> ExplanationNode:
    return ExplanationNode(
        finding_id=finding_id,
        role=role,
        kind=kind,
        symbol=None,
        value=None,
        version=version,
        produced_by=None,
        children=(),
    )


def render_text(node: ExplanationNode | ExplanationGraph, indent: int = 0) -> str:
    """Render graphs with references; trees are the explicit legacy input."""
    if isinstance(node, ExplanationGraph):
        return "\n".join("  " * indent + line for line in render_graph(node.to_dict()).splitlines())
    pad = "  " * indent
    head = node.symbol if node.symbol is not None else node.finding_id
    value = f" = {node.value}" if node.value is not None else ""
    rule = f"  <- {node.produced_by['id']}" if node.produced_by else ""
    lines = [f"{pad}[{node.role}] {head}{value}{rule}"]
    for child in node.children:
        lines.append(render_text(child, indent + 1))
    return "\n".join(lines)


class CyclicDependencyError(ValueError):
    """CYCLIC_DEPENDENCY_ERROR"""


def walk_npe(
    *,
    run_id: str,
    symbol: str,
    rules: list[dict[str, Any]],
    records: list[dict[str, Any]],
    act_log: list[dict[str, Any]] | None = None,
    derived: dict[str, dict[str, Any]] | None = None,
    inputs: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Project a run to shared npe-walk.v4 (ADR-0020/ADR-0055)."""
    # 1. Locate start/completion records
    start_rec = next((r for r in records if r["run_id"] == run_id and r["phase"] == "started"), None)
    closing_rec = next((r for r in records if r["run_id"] == run_id and r["phase"] in ("completed", "interrupted", "failed")), None)

    if start_rec is None:
        raise ValueError(f"Run {run_id} not found in records")

    closing_phase = closing_rec["phase"] if closing_rec else "started"
    workspace_revision = closing_rec["workspace_revision"] if closing_rec else start_rec["workspace_revision"]

    ledger = closing_rec.get("dispositions", []) if closing_rec else []
    record_blocked = closing_rec.get("blocked", []) if closing_rec else []

    derived_findings = derived or {}
    inputs_findings = inputs or {}

    memo: dict[str, dict[str, Any]] = {}
    graph_builder = GraphBuilder(derived_findings, inputs_findings, run_id=run_id)

    rules_by_symbol: dict[str, list[dict[str, Any]]] = {}
    for rule in rules:
        rules_by_symbol.setdefault(rule["publishes"], []).append(rule)
    derived_symbols = set(rules_by_symbol)
    symbols_by_rule: dict[str, set[str]] = {}
    for rule in rules:
        symbols_by_rule.setdefault(rule["id"], set()).add(rule["publishes"])
    ledger_by_symbol: dict[str, list[dict[str, Any]]] = {}
    for row in ledger:
        for produced_symbol in symbols_by_rule.get(row["artifact_id"], set()):
            ledger_by_symbol.setdefault(produced_symbol, []).append(row)
    log_by_symbol: dict[str, str] = {}
    for act in act_log or []:
        finding = act.get("payload", {}).get("finding", {})
        if act.get("kind") == "derived-publication" and act.get("payload", {}).get("run_id") == run_id and finding.get("symbol") is not None:
            log_by_symbol.setdefault(finding["symbol"], finding["id"])

    def walk_symbol(s: str, path: frozenset[str]) -> str:
        if s in path:
            raise CyclicDependencyError("CYCLIC_DEPENDENCY_ERROR")
        if s in memo:
            return s

        producers = rules_by_symbol.get(s, [])
        producer_rows = ledger_by_symbol.get(s, [])

        # 1. Search ledger for published row
        pub_row = next((row for row in producer_rows if row["disposition"] == "published"), None)
        finding_id = pub_row.get("finding_id") if pub_row else None

        # 2. Search act log for run-scoped derived-publication
        if finding_id is None:
            finding_id = log_by_symbol.get(s)

        node_id = s
        rule_refs = [{"id": r["id"], "version": r["version"]} for r in producers]
        rule_refs.sort(key=lambda r: r["id"])

        if finding_id is not None:
            # Expand the selected publication once into the shared pin graph.
            try:
                explanation_root = graph_builder.add_root(finding_id, role="input")
            except ValueError as exc:
                if str(exc) == "CYCLIC_DEPENDENCY_ERROR":
                    raise CyclicDependencyError(str(exc)) from exc
                raise
            children_nodes: list[str] = []
            new_path = path | {s}
            selected = derived_findings.get(finding_id, {})
            for pin in selected.get("pins", []):
                if pin.get("role") not in _DEPENDENCY_ROLES:
                    continue
                child = derived_findings.get(pin.get("id"), {})
                child_symbol = child.get("symbol")
                if child_symbol is not None and child_symbol in derived_symbols:
                    children_nodes.append(walk_symbol(child_symbol, new_path))

            node = {
                "node_id": node_id,
                "node_kind": "published",
                "symbol": s,
                "rule_references": rule_refs,
                "finding_id": finding_id,
                "explanation_root": explanation_root,
            }
            if children_nodes:
                node["children"] = children_nodes
            memo[s] = node
            return s

        # 3. Search ledger for non-published rows
        non_pub_rows = [row for row in producer_rows if row["disposition"] in ("blocked", "inapplicable")]
        if non_pub_rows:
            blocked_rows = [row for row in non_pub_rows if row["disposition"] == "blocked"]
            if blocked_rows:
                # Blocked node
                unmet: list[str] = []
                for r in blocked_rows:
                    missing_deps = r.get("missing", [])
                    if not missing_deps:
                        blocked_entry = next((b for b in record_blocked if b["artifact_id"] == r["artifact_id"]), None)
                        if blocked_entry:
                            missing_deps = blocked_entry.get("missing", [])
                    for dependency in missing_deps:
                        if dependency not in unmet:
                            unmet.append(dependency)

                code = "DEPENDENCY_ABSENT"
                for r in blocked_rows:
                    row_code = r.get("code")
                    if not row_code:
                        blocked_entry = next((b for b in record_blocked if b["artifact_id"] == r["artifact_id"]), None)
                        if blocked_entry:
                            row_code = blocked_entry.get("code")
                    if row_code:
                        code = row_code
                        break

                children_nodes = []
                new_path = path | {s}
                deps = set()
                for r in producers:
                    if r["id"] in {row["artifact_id"] for row in blocked_rows}:
                        deps.update(r["requires"])

                for dep in sorted(list(deps)):
                    if dep in derived_symbols:
                        children_nodes.append(walk_symbol(dep, new_path))

                node = {
                    "node_id": node_id,
                    "node_kind": "blocked",
                    "symbol": s,
                    "rule_references": rule_refs,
                    "code": code,
                    "unmet_references": unmet,
                }
                if children_nodes:
                    node["children"] = children_nodes
                memo[s] = node
                return s
            else:
                # Inapplicable (guard_inapplicable) node
                children_nodes = []
                new_path = path | {s}
                deps = set()
                for r in producers:
                    deps.update(r["requires"])

                for dep in sorted(list(deps)):
                    if dep in derived_symbols:
                        children_nodes.append(walk_symbol(dep, new_path))

                node = {
                    "node_id": node_id,
                    "node_kind": "guard_inapplicable",
                    "symbol": s,
                    "rule_references": rule_refs,
                }
                if children_nodes:
                    node["children"] = children_nodes
                memo[s] = node
                return s

        # 4. Else, no disposition recorded
        node = {
            "node_id": node_id,
            "node_kind": "no_disposition_recorded",
            "symbol": s,
            "rule_references": rule_refs,
            "closing_phase": closing_phase,
        }
        memo[s] = node
        return s

    root_node = walk_symbol(symbol, frozenset())
    result = {
        "schema": "npe-walk.v4",
        "id": f"walk:{run_id}:{symbol}",
        "run_id": run_id,
        "workspace_revision": workspace_revision,
        "root": root_node,
        "nodes": memo,
        "explanation_graph": graph_builder.to_dict(),
    }
    validate_npe(result)
    return result


def validate_npe(walk: dict[str, Any]) -> None:
    """Reject broken NPE references and run-context mismatches."""
    validate_output_schema("npe-walk.v4", walk)
    graph = walk["explanation_graph"]
    validate_graph(graph)
    if walk.get("schema") != "npe-walk.v4" or graph["run_id"] != walk.get("run_id"):
        raise ValueError("invalid NPE context")
    nodes = walk["nodes"]
    if not isinstance(nodes, dict) or walk["root"] not in nodes:
        raise ValueError("invalid NPE root")
    active: set[str] = set()
    done: set[str] = set()
    def visit(key: str) -> None:
        if key in active:
            raise CyclicDependencyError("CYCLIC_DEPENDENCY_ERROR")
        if key in done:
            return
        node = nodes[key]
        if node.get("node_id") != key or not isinstance(node.get("children", []), list):
            raise ValueError("invalid NPE node")
        if node.get("node_kind") == "published":
            target = node.get("explanation_root")
            if target not in graph["nodes"] or graph["nodes"][target]["id"] != node.get("finding_id"):
                raise ValueError("invalid NPE finding reference")
        active.add(key)
        for child in node.get("children", []):
            if not isinstance(child, str) or child not in nodes:
                raise ValueError("invalid NPE child reference")
            visit(child)
        active.remove(key)
        done.add(key)
    for key in nodes:
        visit(key)


def walk_npe_legacy(**kwargs: Any) -> dict[str, Any]:
    """Explicit adapter for historical npe-walk.v3 recursive consumers."""
    graph = walk_npe(**kwargs)
    memo: dict[str, dict[str, Any]] = {}
    def expand(key: str) -> dict[str, Any]:
        if key in memo:
            return memo[key]
        source = graph['nodes'][key]
        node = {name: value for name, value in source.items() if name not in ('children', 'explanation_root')}
        memo[key] = node
        if 'children' in source:
            node['children'] = [expand(child) for child in source['children']]
        return node
    return {'schema': 'npe-walk.v3', 'id': graph['id'], 'run_id': graph['run_id'],
            'workspace_revision': graph['workspace_revision'], 'root': expand(graph['root'])}
