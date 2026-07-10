"""Shared test fixtures: a demo schema set and act builders.

The demo vocabulary is deliberately synthetic (milestone plan, ratified
decision 3): tests prove the machinery obeys the Constitution without
entangling tax content.
"""

import json
import shutil
from pathlib import Path
from typing import Any

from packages.kernel.schema_registry import (
    KERNEL_SCHEMA_DIR,
    SchemaRegistry,
    write_manifest,
)

DEMO_NOTE_PAYLOAD_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {"text": {"type": "string", "minLength": 1}},
    "required": ["text"],
    "additionalProperties": False,
}


def registry_with_demo_kinds(schema_dir: Path) -> SchemaRegistry:
    """A registry over the published kernel schemas plus a demo act kind.

    Kernel schema files are copied byte-for-byte so tests exercise the
    real published versions; the synthetic ``demo-note`` act kind exists
    only to give envelope-level tests a payload with no kernel meaning.
    """
    for path in sorted(KERNEL_SCHEMA_DIR.glob("*.schema.json")):
        shutil.copy(path, schema_dir / path.name)
    (schema_dir / "act-demo-note.v1.schema.json").write_text(
        json.dumps(DEMO_NOTE_PAYLOAD_SCHEMA, indent=2), "utf-8"
    )
    write_manifest(schema_dir)
    return SchemaRegistry(schema_dir)


def demo_note_act(index: int, text: str | None = None) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"demo-act-{index:03d}",
        "kind": "demo-note",
        "actor": "user",
        "at": f"2026-01-01T00:00:{index % 60:02d}Z",
        "committed_against": index,
        "payload": {"text": text if text is not None else f"note {index}"},
    }
