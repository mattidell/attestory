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
) -> ExplanationNode:
    """Explain one finding by walking its pins. `role` is how the parent cited it."""
    inputs = inputs or {}
    if finding_id in derived and finding_id not in _seen:
        finding = derived[finding_id]
        produced_by: dict[str, Any] | None = None
        children: list[ExplanationNode] = []
        seen = _seen | {finding_id}
        for pin in finding["pins"]:
            pin_role = pin["role"]
            if pin_role in _RULE_ROLES:
                produced_by = pin
            elif pin_role in _DEPENDENCY_ROLES:
                children.append(explain(pin["id"], role=pin_role, derived=derived, inputs=inputs, _seen=seen))
            else:
                children.append(_leaf(pin["id"], pin_role, pin_role, pin["version"]))
        children.sort(key=lambda c: (c.role, c.finding_id))
        return ExplanationNode(
            finding_id=finding_id,
            role=role,
            kind="derived",
            symbol=finding["symbol"],
            value=finding["value"],
            version=finding["version"],
            produced_by=produced_by,
            children=tuple(children),
        )

    # A leaf: a human input finding (if we know it) or a bare pinned reference.
    meta = inputs.get(finding_id)
    if meta is not None:
        return ExplanationNode(
            finding_id=finding_id,
            role=role,
            kind=meta.get("role", "input"),
            symbol=meta.get("symbol"),
            value=meta.get("value"),
            version="v1",
            produced_by=None,
            children=(),
        )
    return _leaf(finding_id, role, role, "v1")


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
