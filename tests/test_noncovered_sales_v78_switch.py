"""Core v78 stays off the noncovered-sales package switch.

The grouped closure answer and the covered-flag refusal run only when a
successor package names them. v78's artifact package does not admit
source-closure-mapping.v4, and its companion declaration does not name
the refusal map.
"""

from __future__ import annotations

import json

from packages.derivation.source_authority import covered_flag_block
from packages.tax.loader import (
    COVERED_FLAG_REFUSAL_OBJECTS,
    TAX_CONTENT_DIR,
    covered_flag_refusal_map,
    domain_package_companion_declarations,
    named_covered_flag_refusal_maps,
    noncovered_scalar_presence_pairs,
)

CORE = "tax.us.2025.package.core-calculations"


def test_only_cores_v79_through_v84_name_the_covered_flag_refusal() -> None:
    assert named_covered_flag_refusal_maps() == {
        (CORE, version): COVERED_FLAG_REFUSAL_OBJECTS for version in ("v79", "v80", "v81", "v82", "v83", "v84")
    }
    for version in ("v79", "v80", "v81", "v82", "v83", "v84"):
        assert covered_flag_refusal_map(CORE, version) == COVERED_FLAG_REFUSAL_OBJECTS


def test_core_v79_requires_each_noncovered_scalar_beside_its_sale() -> None:
    declaration = domain_package_companion_declarations()[(CORE, "v79")]
    pairs = noncovered_scalar_presence_pairs()
    for scalar, sale in pairs.items():
        assert declaration["presence_pairs"][scalar] == sale
    earlier = domain_package_companion_declarations()[(CORE, "v78")]
    for scalar in pairs:
        assert scalar not in earlier["presence_pairs"]


def test_core_through_v78_does_not_name_the_refusal() -> None:
    for (package_id, version) in domain_package_companion_declarations():
        if package_id != CORE:
            continue
        rank = int(version.removeprefix("v"))
        if rank <= 78:
            assert covered_flag_refusal_map(package_id, version) is None


def test_core_v78_package_does_not_admit_grouped_closure() -> None:
    citizen = json.loads((TAX_CONTENT_DIR / "package.core-calculations.v78.json").read_text())
    assert citizen["schema"] == "artifact-package.v40"
    assert citizen["version"] == "v78"
    assert "source-closure-mapping.v4" not in citizen["admitted_schemas"]
    assert all(member.get("schema") != "source-closure-mapping.v4" for member in citizen["members"])


def test_empty_refusal_leaves_the_recorded_block_unchanged() -> None:
    code, missing = covered_flag_block(
        "SOURCE_SET_UNCLOSED",
        ["tax.us.2025.f1099b.covered-lt"],
        frozenset(),
        "BASIS_NOT_REPORTED_ON_COVERED",
    )
    assert code == "SOURCE_SET_UNCLOSED"
    assert missing == ["tax.us.2025.f1099b.covered-lt"]
