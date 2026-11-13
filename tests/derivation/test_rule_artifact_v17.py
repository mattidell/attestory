"""ADR 0086: expression blocks may declare explanation-routing names."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from packages.derivation.evaluator import AccessLog, Environment, EvalBlocked, evaluate
from packages.derivation.loader import DerivationSchemas
from packages.kernel.schema_registry import SchemaValidationError


REPO = Path(__file__).resolve().parents[2]
CONTENT = REPO / "packages/content/tax/2025"
SCHEMAS = REPO / "packages/schemas/derivation"


def _first_block(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        if value.get("op") == "block":
            return value
        for child in value.values():
            try:
                return _first_block(child)
            except LookupError:
                pass
    elif isinstance(value, list):
        for child in value:
            try:
                return _first_block(child)
            except LookupError:
                pass
    raise LookupError("no expression block")


def _environment() -> Environment:
    return Environment({}, {}, frozenset(), {}, {})


def test_declared_block_names_are_carried_exactly() -> None:
    names = ["demo.question.alpha", "demo.question.beta"]
    with pytest.raises(EvalBlocked) as raised:
        evaluate(
            {"op": "block", "code": "DEPENDENCY_ABSENT", "missing": names},
            _environment(),
            AccessLog(),
        )
    assert raised.value.category == "DEPENDENCY_ABSENT"
    assert raised.value.missing == names


def test_block_without_declared_names_is_unchanged() -> None:
    with pytest.raises(EvalBlocked) as raised:
        evaluate(
            {"op": "block", "code": "DEPENDENCY_ABSENT"},
            _environment(),
            AccessLog(),
        )
    assert raised.value.category == "DEPENDENCY_ABSENT"
    assert raised.value.missing == []


def test_v17_accepts_only_nonempty_unique_declared_names() -> None:
    schemas = DerivationSchemas()
    rule = json.loads((CONTENT / "rule.schedule-d-line3.v2.json").read_text(encoding="utf-8"))
    rule["schema"] = "rule-artifact.v17"
    block = _first_block(rule)
    block["missing"] = ["demo.question.alpha", "demo.question.beta"]
    assert schemas.validate_declared(rule) == "rule-artifact.v17"

    for invalid in ([], [""], ["demo.question.alpha", "demo.question.alpha"]):
        bad = copy.deepcopy(rule)
        _first_block(bad)["missing"] = invalid
        with pytest.raises(SchemaValidationError):
            schemas.validate_declared(bad)


def test_v16_schema_bytes_and_expression_behavior_are_stable() -> None:
    schema_path = SCHEMAS / "rule-artifact.v16.schema.json"
    manifest = json.loads((SCHEMAS / "published.json").read_text(encoding="utf-8"))
    assert hashlib.sha256(schema_path.read_bytes()).hexdigest() == manifest[schema_path.name]

    rule = json.loads((CONTENT / "rule.f1099b-b4-withholding-subtotal.v2.json").read_text(encoding="utf-8"))
    assert DerivationSchemas().validate_declared(rule) == "rule-artifact.v16"
    with pytest.raises(EvalBlocked) as raised:
        evaluate({"op": "block", "code": "DEPENDENCY_ABSENT"}, _environment(), AccessLog())
    assert raised.value.missing == []


def test_v16_rejects_the_v17_property() -> None:
    schemas = DerivationSchemas()
    rule = json.loads((CONTENT / "rule.schedule-d-line3.v2.json").read_text(encoding="utf-8"))
    rule["schema"] = "rule-artifact.v16"
    _first_block(rule)["missing"] = ["demo.question.alpha"]
    with pytest.raises(SchemaValidationError) as raised:
        schemas.validate_declared(rule)
    assert raised.value.schema_id == "rule-artifact.v16"
