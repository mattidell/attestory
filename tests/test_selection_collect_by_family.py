"""Family-collect selection: the v86 switch, own-family vs foreign collect, v16 vs v15."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, cast

import pytest

from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import MemberIssue, _v13_selection_issues
from packages.kernel.schema_registry import SchemaValidationError
from packages.tax.loader import selection_collect_satisfied_by_family

REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "packages/content/tax/2025"
CORE = "tax.us.2025.package.core-calculations"
P = "tax.us.2025."
BOX4 = P + "f1099b.statement-box4-withholding"
FAMILY = P + "f1099b.b4"
INT_MEMBER = P + "f1099int.box4-withholding"
INT_FAMILY = P + "f1099int.b4"
SUBTOTAL = P + "rule.f1099b-b4-withholding-subtotal"
FOREIGN = P + "rule.skc-t1-foreign-collect"


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text(encoding="utf-8")))


def _resolved(*bodies: dict[str, Any]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    return [({"id": body["id"], "version": body["version"]}, body) for body in bodies]


def _surface(*extra: dict[str, Any]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    return _resolved(
        _load("family.f1099b-b4.json"),
        _load("f1099b-box4.bundle.json"),
        _load("family.f1099int-b4.json"),
        _load("f1099int-box4.bundle.json"),
        *extra,
    )


def _issues(version: str, *extra: dict[str, Any]) -> list[MemberIssue]:
    return _v13_selection_issues({"id": CORE, "version": version}, _surface(*extra))


def _dep_invalid(issues: list[MemberIssue], member_id: str) -> list[MemberIssue]:
    return [item for item in issues if item.member_id == member_id and item.code == "RULE_SELECTION_DEPENDENCIES_INVALID"]


def _foreign(*, requires: list[str]) -> dict[str, Any]:
    body = copy.deepcopy(_load("rule.f1099b-b4-withholding-subtotal.v2.json"))
    body["id"] = FOREIGN
    path = body["selection"]["paths"][0]
    path["value"]["args"][0]["name"] = INT_MEMBER
    path["value"]["args"][0]["source_set"] = INT_FAMILY
    path["requires"] = list(requires)
    path["pins"] = [
        {"id": name, "origin": "assertion", "role": "input", "version": "v1"} for name in requires
    ]
    return body


def test_switch_on_from_core_calculations_v86() -> None:
    assert selection_collect_satisfied_by_family(CORE, "v86") is True
    assert selection_collect_satisfied_by_family(CORE, "v87") is True
    assert selection_collect_satisfied_by_family(CORE, "v85") is False
    assert selection_collect_satisfied_by_family(CORE, "v84") is False
    assert selection_collect_satisfied_by_family(CORE, "v1") is False
    assert selection_collect_satisfied_by_family(P + "package.interest-slice", "v86") is False
    assert selection_collect_satisfied_by_family(CORE, "86") is False
    assert selection_collect_satisfied_by_family(CORE, "latest") is False


def test_v86_own_family_collect_needs_no_requires() -> None:
    v2 = _load("rule.f1099b-b4-withholding-subtotal.v2.json")
    assert v2["selection"]["paths"][0]["requires"] == []
    assert _dep_invalid(_issues("v86", v2), SUBTOTAL) == []


def test_v86_foreign_collect_still_must_be_listed() -> None:
    missing = _foreign(requires=[])
    listed = _foreign(requires=[INT_MEMBER])
    assert _dep_invalid(_issues("v86", missing), FOREIGN)
    assert _dep_invalid(_issues("v86", listed), FOREIGN) == []


def test_v86_own_family_categorical_read_is_not_exempt() -> None:
    # ADR 0085 exempts the member collect only; a categorical read of the
    # activity family is still a dependency.
    body = copy.deepcopy(_load("rule.f1099b-b4-withholding-subtotal.v2.json"))
    body["selection"]["paths"][0]["value"]["args"][0]["op"] = "collect_categorical_all_equal"
    assert _dep_invalid(_issues("v86", body), SUBTOTAL)


def test_v85_and_earlier_keep_the_requires_equality() -> None:
    v1 = _load("rule.f1099b-b4-withholding-subtotal.json")
    v2 = _load("rule.f1099b-b4-withholding-subtotal.v2.json")
    assert v1["selection"]["paths"][0]["requires"] == [BOX4]
    for version in ("v85", "v84"):
        assert _dep_invalid(_issues(version, v1), SUBTOTAL) == []
        assert _dep_invalid(_issues(version, v2), SUBTOTAL)
    assert _dep_invalid(_issues("v86", v1), SUBTOTAL)


def test_v16_one_path_validates_and_v15_one_path_does_not() -> None:
    schemas = DerivationSchemas()
    v16 = _load("rule.f1099b-b4-withholding-subtotal.v2.json")
    assert len(v16["selection"]["paths"]) == 1
    assert schemas.validate_declared(v16) == "rule-artifact.v16"
    v15 = copy.deepcopy(v16)
    v15["schema"] = "rule-artifact.v15"
    with pytest.raises(SchemaValidationError) as raised:
        schemas.validate_declared(v15)
    assert raised.value.schema_id == "rule-artifact.v15"
    assert any("minItems" in error or "too short" in error for error in raised.value.errors)
