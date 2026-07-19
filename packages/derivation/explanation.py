"""Explanation walker: 'explain this number' as rendering, not research.

A derived finding carries its full lineage as role-bearing pins (ADR-0007/0009).
This walker turns those pins into an explanation tree: the value, the rule that
produced it, the input findings it consumed (recursing into any that are
themselves derived), and the parameters, operation-semantics, adoption, and
governance it stood on. Because the pins are on the finding, explanation is a
traversal of committed data — never a re-evaluation, and never a guess.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

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
    return {finding["id"]: finding for finding in findings}


def explain(
    finding_id: str,
    *,
    role: str,
    derived: dict[str, dict[str, Any]],
    inputs: dict[str, dict[str, Any]] | None = None,
    _seen: frozenset[str] = frozenset(),
    _memo: dict[str, ExplanationNode] | None = None,
) -> ExplanationNode:
    """Explain one finding by walking its pins. `role` is how the parent cited it."""
    inputs = inputs or {}
    if finding_id in _seen:
        raise ValueError("CYCLIC_DEPENDENCY_ERROR")

    if _memo is not None and finding_id in _memo:
        return _memo[finding_id]

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
                children.append(explain(
                    pin["id"],
                    role=pin_role,
                    derived=derived,
                    inputs=inputs,
                    _seen=seen,
                    _memo=_memo
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
        return node

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
        return node
    node = _leaf(finding_id, role, role, "v1")
    if _memo is not None:
        _memo[finding_id] = node
    return node


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


def render_text(node: ExplanationNode, indent: int = 0) -> str:
    """A compact human rendering of an explanation tree."""
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
    """Pure project walker returning an npe-walk.v1 payload (ADR-0020)."""
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
    explain_memo: dict[str, ExplanationNode] = {}

    derived_symbols = {r["publishes"] for r in rules}

    def walk_symbol(s: str, path: frozenset[str]) -> dict[str, Any]:
        if s in path:
            raise CyclicDependencyError("CYCLIC_DEPENDENCY_ERROR")
        if s in memo:
            return memo[s]

        producers = [r for r in rules if r["publishes"] == s]
        producer_ids = {r["id"] for r in producers}

        # 1. Search ledger for published row
        pub_row = next((row for row in ledger if row["artifact_id"] in producer_ids and row["disposition"] == "published"), None)
        finding_id = pub_row.get("finding_id") if pub_row else None

        # 2. Search act log for run-scoped derived-publication
        if finding_id is None and act_log:
            for act in act_log:
                if (
                    act.get("kind") == "derived-publication"
                    and act.get("payload", {}).get("run_id") == run_id
                    and act.get("payload", {}).get("finding", {}).get("symbol") == s
                ):
                    finding_id = act["payload"]["finding"]["id"]
                    break

        node_id = s
        rule_refs = [{"id": r["id"], "version": r["version"]} for r in producers]
        rule_refs.sort(key=lambda r: r["id"])

        if finding_id is not None:
            # Delegate to explain
            exp_node = explain(
                finding_id,
                role="input",
                derived=derived_findings,
                inputs=inputs_findings,
                _memo=explain_memo,
            )

            children_nodes = []
            new_path = path | {s}

            for child in exp_node.children:
                child_symbol = child.symbol
                if child_symbol is None and child.finding_id in derived_findings:
                    child_symbol = derived_findings[child.finding_id].get("symbol")

                if child_symbol is not None and child_symbol in derived_symbols:
                    children_nodes.append(walk_symbol(child_symbol, new_path))

            node = {
                "node_id": node_id,
                "node_kind": "published",
                "symbol": s,
                "rule_references": rule_refs,
                "finding_id": finding_id,
            }
            if children_nodes:
                node["children"] = children_nodes
            memo[s] = node
            return node

        # 3. Search ledger for non-published rows
        non_pub_rows = [row for row in ledger if row["artifact_id"] in producer_ids and row["disposition"] in ("blocked", "inapplicable")]
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
                return node
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
                return node

        # 4. Else, no disposition recorded
        node = {
            "node_id": node_id,
            "node_kind": "no_disposition_recorded",
            "symbol": s,
            "rule_references": rule_refs,
            "closing_phase": closing_phase,
        }
        memo[s] = node
        return node

    root_node = walk_symbol(symbol, frozenset())
    return {
        "schema": "npe-walk.v1",
        "id": f"walk:{run_id}:{symbol}",
        "run_id": run_id,
        "workspace_revision": workspace_revision,
        "root": root_node,
    }
