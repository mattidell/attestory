#!/usr/bin/env python3
"""Render and validate the artifact graph documents.

The canonical artifact graph lives in
docs/product/artifact-graph/artifact-graph.json. The markdown documents in
that directory are generated projections of the JSON and must not be edited
by hand.

Usage:
    python3 tools/render_artifact_graph.py            # validate and write docs
    python3 tools/render_artifact_graph.py --check    # validate and verify docs are fresh

Validation covers:
- JSON Schema conformance (artifact-graph.schema.json).
- Node ids are unique and layer membership is consistent.
- Edge endpoints reference defined nodes and no edge is duplicated.
- Self-referencing edges are audit-only and explicitly allowed.
- The production-edge graph is acyclic.
- The durability rule: definition inputs are canonical, run outputs are
  run snapshots, and run-selected inputs are canonical unless the node is
  explicitly frozen by the run (ProductRunPayload).
- manifest_index edges target RunManifest.
"""

from __future__ import annotations

import argparse
import json
import sys
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
GRAPH_DIR = ROOT / "docs" / "product" / "artifact-graph"
GRAPH_PATH = GRAPH_DIR / "artifact-graph.json"
SCHEMA_PATH = GRAPH_DIR / "artifact-graph.schema.json"

GENERATED_HEADER = (
    "<!-- Generated from artifact-graph.json by tools/render_artifact_graph.py. "
    "Do not edit by hand; edit the JSON and re-run the renderer. -->"
)

LAYERS_DOC = "artifact-graph-layers.md"
CORE_EDGES_DOC = "artifact-graph-core-edges.md"


def load_graph() -> dict:
    graph = json.loads(GRAPH_PATH.read_text())
    schema = json.loads(SCHEMA_PATH.read_text())
    jsonschema.validate(graph, schema)
    return graph


def validate_graph(graph: dict) -> list[str]:
    errors: list[str] = []
    nodes = graph["nodes"]
    layers = graph["layers"]
    node_by_id = {node["id"]: node for node in nodes}
    layer_ids = {layer["id"] for layer in layers}

    if len(node_by_id) != len(nodes):
        errors.append("Node ids are not unique.")

    for node in nodes:
        if node["layer"] not in layer_ids:
            errors.append(f"Node {node['id']} references unknown layer {node['layer']}.")

    for layer in layers:
        for node_id in layer["nodes"]:
            node = node_by_id.get(node_id)
            if node is None:
                errors.append(f"Layer {layer['id']} lists unknown node {node_id}.")
            elif node["layer"] != layer["id"]:
                errors.append(
                    f"Node {node_id} is listed in layer {layer['id']} but declares layer {node['layer']}."
                )
    listed = [node_id for layer in layers for node_id in layer["nodes"]]
    if sorted(listed) != sorted(node_by_id):
        errors.append("Layer node lists and node declarations do not cover the same node set.")

    seen_pairs: set[tuple[str, str]] = set()
    for edge in graph["edges"]:
        pair = (edge["from"], edge["to"])
        if pair in seen_pairs:
            errors.append(f"Duplicate edge {edge['from']} -> {edge['to']}.")
        seen_pairs.add(pair)
        for endpoint in pair:
            if endpoint not in node_by_id:
                errors.append(f"Edge {edge['from']} -> {edge['to']} references unknown node {endpoint}.")
        if edge["from"] == edge["to"]:
            if not edge.get("allow_self_reference"):
                errors.append(f"Self edge on {edge['from']} lacks allow_self_reference.")
            if edge["types"] != ["audit"]:
                errors.append(f"Self edge on {edge['from']} must be audit-only.")
        doc_layer = edge.get("doc_layer")
        if doc_layer is not None and doc_layer not in layer_ids:
            errors.append(f"Edge {edge['from']} -> {edge['to']} has unknown doc_layer {doc_layer}.")
        if edge.get("manifest_index") and edge["to"] != "RunManifest":
            errors.append(f"manifest_index edge {edge['from']} -> {edge['to']} must target RunManifest.")

    production_deps: dict[str, set[str]] = {node_id: set() for node_id in node_by_id}
    for edge in graph["edges"]:
        if "production" in edge["types"] and edge["from"] != edge["to"]:
            if edge["to"] in production_deps and edge["from"] in node_by_id:
                production_deps[edge["to"]].add(edge["from"])
    try:
        TopologicalSorter(production_deps).prepare()
    except CycleError as exc:
        errors.append(f"Production edges contain a cycle: {exc.args[1]}")

    for node in nodes:
        role = node["manifest_role"]
        durability = node["durability"]
        if role == "definition_input" and durability != "canonical":
            errors.append(f"Durability rule: definition input {node['id']} must be canonical.")
        if role == "run_output" and durability != "run_snapshot":
            errors.append(f"Durability rule: run output {node['id']} must be run_snapshot.")
        if role == "run_input" and durability != "canonical" and not node.get("frozen_by_run"):
            errors.append(
                f"Durability rule: run-selected input {node['id']} must be canonical unless frozen_by_run."
            )

    return errors


def bullets(lines: list[str]) -> list[str]:
    return [f"- {line}" for line in lines]


def code_bullets(ids: list[str]) -> list[str]:
    return [f"- `{node_id}`" for node_id in ids]


def grouped_arrow_block(edges: list[dict]) -> list[str]:
    """Render edges as a text block grouped by source in first-appearance order."""
    order: list[str] = []
    targets: dict[str, list[str]] = {}
    for edge in edges:
        source = edge["from"]
        if source not in targets:
            targets[source] = []
            order.append(source)
        targets[source].append(edge["to"])
    lines: list[str] = ["```text"]
    for index, source in enumerate(order):
        if index:
            lines.append("")
        lines.append(source)
        lines.extend(f"  -> {target}" for target in targets[source])
    lines.append("```")
    return lines


def edge_section(edge: dict) -> list[str]:
    lines = [f"### {edge['from']} -> {edge['to']}", "", "Edge type:"]
    lines.extend(f"- {edge_type}" for edge_type in edge["types"])
    if edge.get("meaning"):
        lines.extend(["", "Meaning:"])
        lines.extend(bullets(edge["meaning"]))
    if edge.get("audit_value"):
        lines.extend(["", "Audit value:"])
        lines.extend(bullets(edge["audit_value"]))
    if edge.get("notes"):
        lines.extend(["", "Notes:"])
        lines.extend(bullets(edge["notes"]))
    return lines


def node_section(node: dict, graph: dict) -> list[str]:
    production_in: list[str] = []
    audit_in: list[str] = []
    production_out: list[str] = []
    audit_out: list[str] = []
    for edge in graph["edges"]:
        if edge["from"] == edge["to"]:
            continue
        is_production = "production" in edge["types"]
        if edge["to"] == node["id"]:
            (production_in if is_production else audit_in).append(edge["from"])
        if edge["from"] == node["id"]:
            if edge.get("manifest_index") and node["id"] != "RunManifest":
                continue
            (production_out if is_production else audit_out).append(edge["to"])

    lines = [f"## {node['id']}", "", "Durability:", f"- `{node['durability']}`", ""]
    lines.extend(["Category:", f"- `{node['category']}`", ""])
    lines.append("Purpose:")
    lines.extend(bullets(node["purpose"]))
    lines.append("")
    lines.append("Consumes:")
    lines.extend(code_bullets(production_in) if production_in else ["- None."])
    lines.append("")
    if audit_in:
        lines.append("Audit context:")
        lines.extend(code_bullets(audit_in))
        lines.append("")
    lines.append("Feeds:")
    lines.extend(code_bullets(production_out) if production_out else ["- None."])
    lines.append("")
    if audit_out:
        lines.append("Explains:")
        lines.extend(code_bullets(audit_out))
        lines.append("")
    lines.append("Boundary owner:")
    lines.extend(f"- `{owner}`" for owner in node["boundary_owner"])
    lines.extend(["", "Schema status:", f"- `{node['schema_status']}`"])
    lines.extend(["", "Manifest role:", f"- `{node['manifest_role']}`"])
    lines.extend(["", "Personal data risk:", f"- `{node['personal_data_risk']}`"])
    lines.extend(["", "Commit policy:"])
    lines.extend(f"- `{policy}`" for policy in node["commit_policy"])
    for section in node.get("sections", []):
        lines.extend(["", f"### {section['title']}", ""])
        lines.extend(section["body"])
    return lines


def render_layer_doc(layer: dict, graph: dict) -> str:
    node_by_id = {node["id"]: node for node in graph["nodes"]}
    doc_edges = [
        edge
        for edge in graph["edges"]
        if not edge.get("manifest_index")
        and (edge.get("doc_layer") or node_by_id[edge["to"]]["layer"]) == layer["id"]
    ]
    lines = [GENERATED_HEADER, "", f"# Artifact Graph {layer['name']}", ""]
    for paragraph in layer["description"]:
        lines.extend([paragraph, ""])
    lines.extend(["## Layer Graph", ""])
    lines.extend(grouped_arrow_block(doc_edges))
    lines.append("")
    documented = [
        edge for edge in doc_edges if edge.get("meaning") or edge.get("audit_value") or edge.get("notes")
    ]
    if documented:
        lines.extend(["## Core Edges", ""])
        for edge in documented:
            lines.extend(edge_section(edge))
            lines.append("")
    for node_id in layer["nodes"]:
        lines.extend(node_section(node_by_id[node_id], graph))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_layers_doc(graph: dict) -> str:
    node_by_id = {node["id"]: node for node in graph["nodes"]}
    lines = [GENERATED_HEADER, "", f"# Artifact Graph Layers", ""]
    for paragraph in graph["intro"]:
        lines.extend([paragraph, ""])
    lines.extend(["The graph uses only two durability classes:", ""])
    for durability in graph["durability_classes"]:
        lines.append(f"- `{durability['id']}`: {durability['description']}")
    lines.append("")
    for paragraph in graph["scope_note"]:
        lines.extend([paragraph, ""])
    lines.extend(["## Durability Rule", ""])
    for paragraph in graph["durability_rule"]:
        lines.extend([paragraph, ""])
    lines.extend(["## Layer Summary", "", "```text"])
    for index, layer in enumerate(graph["layers"]):
        if index:
            lines.append("")
        lines.append(layer["name"])
        lines.extend(f"  {node_id}" for node_id in layer["nodes"])
    lines.extend(["```", "", "## Layer Documents", ""])
    for layer in graph["layers"]:
        lines.append(f"- [{layer['name']}]({layer['doc_file']})")
    lines.extend(["", "## Cross-Layer Flow", ""])
    cross_layer = [
        edge
        for edge in graph["edges"]
        if not edge.get("manifest_index")
        and "production" in edge["types"]
        and edge["from"] != edge["to"]
        and node_by_id[edge["from"]]["layer"] != node_by_id[edge["to"]]["layer"]
    ]
    lines.extend(grouped_arrow_block(cross_layer))
    lines.append("")
    for paragraph in graph["cross_flow_note"]:
        lines.extend([paragraph, ""])
    return "\n".join(lines).rstrip() + "\n"


def render_core_edges_doc(graph: dict) -> str:
    lines = [GENERATED_HEADER, "", "# Artifact Graph Edge Types", ""]
    lines.extend(
        [
            "This document defines the edge types used by the artifact graph. Concrete edge instances live in the layer documents:",
            "",
        ]
    )
    for layer in graph["layers"]:
        lines.append(f"- [{layer['name']}]({layer['doc_file']})")
    lines.append("")
    for paragraph in graph["scope_note"]:
        lines.extend([paragraph, ""])
    for edge_type in graph["edge_types"]:
        lines.extend([f"## {edge_type['heading']}", ""])
        for paragraph in edge_type["description"]:
            lines.extend([paragraph, ""])
        example = edge_type.get("example")
        if example:
            lines.extend(["Example:", "", "```text", example["edge"], "```", ""])
            for paragraph in example["explanation"]:
                lines.extend([paragraph, ""])
        if edge_type.get("questions"):
            lines.extend([edge_type["questions_intro"], ""])
            lines.extend(bullets(edge_type["questions"]))
            lines.append("")
        for paragraph in edge_type.get("closing_note", []):
            lines.extend([paragraph, ""])
    lines.extend(["## Reproducibility Edges", ""])
    for paragraph in graph["reproducibility_note"]:
        lines.extend([paragraph, ""])
    roles = [
        ("Definition inputs:", "definition_input"),
        ("Run-selected inputs:", "run_input"),
        ("Run outputs:", "run_output"),
    ]
    for label, role in roles:
        members = [
            node_id
            for layer in graph["layers"]
            for node_id in layer["nodes"]
            if next(node for node in graph["nodes"] if node["id"] == node_id)["manifest_role"] == role
        ]
        lines.append(label)
        lines.extend(code_bullets(members))
        lines.append("")
    for paragraph in graph["run_manifest_note"]:
        lines.extend([paragraph, ""])
    return "\n".join(lines).rstrip() + "\n"


def render_all(graph: dict) -> dict[str, str]:
    documents = {
        LAYERS_DOC: render_layers_doc(graph),
        CORE_EDGES_DOC: render_core_edges_doc(graph),
    }
    for layer in graph["layers"]:
        documents[layer["doc_file"]] = render_layer_doc(layer, graph)
    return documents


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the graph and verify the rendered documents match the committed files.",
    )
    args = parser.parse_args()

    try:
        graph = load_graph()
    except jsonschema.ValidationError as exc:
        print(f"Schema validation failed: {exc.message}")
        return 2

    errors = validate_graph(graph)
    if errors:
        print("Artifact graph validation failed:")
        for error in errors:
            print(f"- {error}")
        return 2

    documents = render_all(graph)
    if args.check:
        stale = []
        for filename, content in documents.items():
            path = GRAPH_DIR / filename
            if not path.exists() or path.read_text() != content:
                stale.append(filename)
        if stale:
            print("Rendered documents are stale. Run python3 tools/render_artifact_graph.py:")
            for filename in stale:
                print(f"- {filename}")
            return 1
        print(f"Artifact graph is valid and {len(documents)} documents are fresh.")
        return 0

    for filename, content in documents.items():
        (GRAPH_DIR / filename).write_text(content)
        print(f"Wrote {GRAPH_DIR / filename}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
