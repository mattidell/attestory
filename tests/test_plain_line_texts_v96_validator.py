"""Decision 5: the v96 nominee-return successor graph, with its controls.

Measured reason for the live marker: loading the 1,800-citizen corpus took
15 s and each full package validation 2.3 s on an idle machine, above the
3.0 s fast-lane budget.
"""
from __future__ import annotations

import copy
import json
from functools import lru_cache
from pathlib import Path
from typing import Any, cast

import pytest

from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    load_published_citizen_checksums,
    package_instance_checksum,
    validate_package,
)
from tools.package_successor import load_corpus

pytestmark = pytest.mark.live

CONTENT = Path(__file__).resolve().parents[1] / "packages/content/tax/2025"
FIELD = "tax.us.2025.form1040.line-2b"
MIXED = "NOMINEE_RETURN_SUCCESSOR_GRAPH_MIXED"


@lru_cache(maxsize=1)
def _corpus() -> Any:
    return load_corpus(CONTENT)[0]


def _package(version: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / f"package.core-calculations.{version}.json").read_text(encoding="utf-8")))


def _codes(package: dict[str, Any], registry: str, field_version: str | None = None) -> list[str]:
    body = copy.deepcopy(package)
    if field_version is not None:
        next(p for p in body["members"] if p["id"] == FIELD)["version"] = field_version
        body["package_checksum"] = package_instance_checksum(body)
    checks = load_published_citizen_checksums(CONTENT / f"published-packages.{registry}.json")
    return [i.code for i in validate_package(body, _corpus(), DerivationSchemas(), checks).issues]


def test_published_v96_with_line_2b_field_v7_is_accepted() -> None:
    package = _package("v96")
    assert next(p for p in package["members"] if p["id"] == FIELD)["version"] == "v7"
    assert _codes(package, "v94") == []


def test_v96_with_line_2b_field_v6_is_rejected() -> None:
    assert _codes(_package("v96"), "v94", "v6") == [MIXED]


def test_v95_with_line_2b_field_v7_is_rejected() -> None:
    assert _codes(_package("v95"), "v94", "v7") == [MIXED]


def test_published_v95_is_still_accepted() -> None:
    package = _package("v95")
    assert next(p for p in package["members"] if p["id"] == FIELD)["version"] == "v6"
    assert _codes(package, "v93") == []
