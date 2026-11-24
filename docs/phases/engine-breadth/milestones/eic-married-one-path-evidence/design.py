"""v2 of the two married-taxpayer selection rules, with one path each.

rule-artifact.v14 requires two selection paths, so the published v1 rules
carry an inert second path. These successors keep the separated-recorded
path and the v1 default, drop that inert path, and move to
rule-artifact.v17. Every other field stays as published.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

P = "tax.us.2025."
RECORDED = P + "rule.eic-married-taxpayer-recorded"
FROM_SEPARATED = P + "rule.eic-married-taxpayer-from-separated"
RECORDED_V1 = "rule.eic-married-taxpayer-recorded.v1.json"
FROM_V1 = "rule.eic-married-taxpayer-from-separated.v1.json"
RECORDED_FILE = "rule.eic-married-taxpayer-recorded.v2.json"
FROM_FILE = "rule.eic-married-taxpayer-from-separated.v2.json"
PATH_ID = "separated-recorded"
INERT = P + "eic.married-taxpayer-inert"


def successor(v1: dict[str, Any]) -> dict[str, Any]:
    """v1 on rule-artifact.v17, with only the separated-recorded path."""
    out = copy.deepcopy(v1)
    out["schema"] = "rule-artifact.v17"
    out["version"] = "v2"
    paths = out["selection"]["paths"]
    kept = [path for path in paths if path["id"] == PATH_ID]
    if len(paths) != 2 or len(kept) != 1:
        raise ValueError("v1 selection is not one separated-recorded path plus one other path")
    out["selection"]["paths"] = kept
    return out


def written(source: Path) -> dict[str, dict[str, Any]]:
    return {
        RECORDED_FILE: successor(json.loads((source / RECORDED_V1).read_text(encoding="utf-8"))),
        FROM_FILE: successor(json.loads((source / FROM_V1).read_text(encoding="utf-8"))),
    }


def dump(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"
