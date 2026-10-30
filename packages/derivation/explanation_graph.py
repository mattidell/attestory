"""Build and validate run-local, role-bearing explanation graphs."""
from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

from packages.kernel.schema_registry import SchemaRegistry, SchemaValidationError

DEPENDENCIES = frozenset({'input', 'choice'})
RULES = frozenset({'computation', 'applicability', 'field-mapping', 'cross-form-bridge'})


@lru_cache(maxsize=1)
def _output_registry() -> SchemaRegistry:
    return SchemaRegistry(Path(__file__).resolve().parent.parent / "schemas" / "derivation")


def validate_output_schema(name: str, value: object) -> None:
    """Validate only the three published shared-output boundaries."""
    if name not in {"explanation-graph.v1", "npe-walk.v4", "presentation-model.v2"}:
        raise ValueError("unknown shared output schema")
    try:
        _output_registry().validate(name, value)
    except SchemaValidationError as exc:
        raise ValueError("invalid shared output shape") from exc


def _key(kind: str, identifier: str, version: str) -> str:
    # Length prefixes prevent ambiguities when identifiers themselves contain colons.
    return f'{kind}:{len(identifier)}:{identifier}:{version}'


class GraphBuilder:
    """One builder per immutable snapshot, with one expansion per finding."""

    def __init__(self, derived: Mapping[str, Mapping[str, Any]], inputs: Mapping[str, Mapping[str, Any]] | None = None, *, run_id: str | None = None) -> None:
        self.run_id = run_id
        self.derived = deepcopy(derived)
        self.inputs = deepcopy(inputs or {})
        self.nodes: dict[str, dict[str, Any]] = {}
        self.roots: list[dict[str, Any]] = []
        self.active: set[str] = set()

    def _walk(self, identifier: str, version: str, dependency: bool) -> str:
        finding = self.derived.get(identifier) if dependency else None
        meta = self.inputs.get(identifier) if dependency and finding is None else None
        kind = 'derived' if finding is not None else 'input' if meta is not None else 'reference'
        actual_version = str(finding.get('version', version)) if finding is not None else version
        key = _key(kind, identifier, actual_version)
        if key in self.active:
            raise ValueError('CYCLIC_DEPENDENCY_ERROR')
        if key in self.nodes:
            return key
        self.active.add(key)
        try:
            edges = []
            produced_by = None
            if finding is not None:
                for pin in finding['pins']:
                    pin_copy = deepcopy(pin)
                    role = str(pin['role'])
                    target = self._walk(str(pin['id']), str(pin['version']), role in DEPENDENCIES)
                    edges.append({'target': target, 'pin': pin_copy})
                    if role in RULES:
                        produced_by = pin_copy
                edges.sort(key=lambda edge: (edge['pin']['role'], edge['pin']['id']))
            payload: Mapping[str, Any] = finding if finding is not None else meta if meta is not None else {}
            self.nodes[key] = {'id': identifier, 'version': actual_version, 'kind': kind,
                               'symbol': payload.get('symbol'), 'value': payload.get('value'),
                               'produced_by': produced_by, 'edges': edges}
        finally:
            self.active.remove(key)
        return key

    def add_root(self, identifier: str, *, role: str, authorization: Any = None) -> str:
        finding = self.derived.get(identifier)
        version = str(finding.get('version', 'v1')) if finding is not None else 'v1'
        target = self._walk(identifier, version, True)
        root: dict[str, Any] = {'target': target, 'role': role}
        if authorization is not None:
            root['authorization'] = deepcopy(authorization)
        self.roots.append(root)
        return target

    def to_dict(self) -> dict[str, Any]:
        graph = {'schema': 'explanation-graph.v1', 'run_id': self.run_id, 'roots': deepcopy(self.roots), 'nodes': deepcopy(self.nodes)}
        validate_graph(graph)
        return graph


def validate_graph(graph: Mapping[str, Any]) -> None:
    validate_output_schema("explanation-graph.v1", graph)
    if set(graph) != {'schema', 'run_id', 'roots', 'nodes'} or graph.get('schema') != 'explanation-graph.v1':
        raise ValueError('invalid explanation graph envelope')
    if graph['run_id'] is not None and (not isinstance(graph['run_id'], str) or not graph['run_id']):
        raise ValueError('invalid explanation graph run id')
    roots, nodes = graph['roots'], graph['nodes']
    if not isinstance(roots, list) or not isinstance(nodes, dict):
        raise ValueError('invalid explanation graph collections')
    for root in roots:
        if not isinstance(root, dict) or not {'target', 'role'} <= root.keys() or set(root) - {'target', 'role', 'authorization'} or not isinstance(root['role'], str) or not isinstance(root['target'], str) or root['target'] not in nodes:
            raise ValueError('invalid explanation graph root')
    for key, node in nodes.items():
        if not isinstance(key, str) or not isinstance(node, dict) or set(node) != {'id','version','kind','symbol','value','produced_by','edges'}:
            raise ValueError('invalid explanation graph node')
        if node['kind'] not in ('derived','input','reference') or not isinstance(node['id'], str) or not isinstance(node['version'], str) or key != _key(node['kind'], node['id'], node['version']):
            raise ValueError('invalid explanation graph identity')
        if not isinstance(node['edges'], list) or (node['kind'] != 'derived' and node['edges']):
            raise ValueError('invalid explanation graph edges')
        if node['kind'] == 'reference' and (node['symbol'] is not None or node['value'] is not None or node['produced_by'] is not None):
            raise ValueError('invalid bare reference payload')
        for edge in node['edges']:
            if not isinstance(edge, dict) or set(edge) != {'target','pin'} or not isinstance(edge['target'], str) or edge['target'] not in nodes or not isinstance(edge['pin'], dict) or not {'id','role','version'} <= edge['pin'].keys() or not all(isinstance(edge['pin'][field], str) and edge['pin'][field] for field in ('id','role','version')):
                raise ValueError('invalid explanation graph edge')
            target = nodes[edge['target']]
            if (edge['pin']['role'] not in DEPENDENCIES and target['kind'] != 'reference') or edge['pin']['id'] != target['id'] or (target['kind'] != 'derived' and edge['pin']['version'] != target['version']):
                raise ValueError('explanation graph pin mismatch')
        if node['produced_by'] is not None and not any(edge['pin'] == node['produced_by'] and edge['pin']['role'] in RULES for edge in node['edges']):
            raise ValueError('invalid explanation producer')
    active: set[str] = set()
    visited: set[str] = set()
    def visit(key: str) -> None:
        if key in active:
            raise ValueError('CYCLIC_DEPENDENCY_ERROR')
        if key in visited:
            return
        active.add(key)
        for edge in nodes[key]['edges']:
            visit(edge['target'])
        active.remove(key)
        visited.add(key)
    for key in nodes:
        visit(key)


def render_graph(graph: Mapping[str, Any]) -> str:
    """Render each node once and name every subsequent reference."""
    validate_graph(graph)
    seen: set[str] = set()
    lines: list[str] = []
    nodes = graph['nodes']
    def visit(key: str, role: str, depth: int) -> None:
        node = nodes[key]
        pad = '  ' * depth
        if key in seen:
            lines.append(f'{pad}[{role}] see {key}')
            return
        seen.add(key)
        head = node['symbol'] or node['id']
        value = f" = {node['value']}" if node['value'] is not None else ''
        producer = f"  <- {node['produced_by']['id']}" if node['produced_by'] else ''
        lines.append(f'{pad}[{role}] {head}{value}{producer} ({key})')
        for edge in node['edges']:
            visit(edge['target'], edge['pin']['role'], depth + 1)
    for root in graph['roots']:
        visit(root['target'], root['role'], 0)
    return '\n'.join(lines)
