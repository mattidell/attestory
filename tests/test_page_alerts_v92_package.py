"""Core v92 publishes the line 6c words and the Schedule 1 top-entry citation.

Static checks: byte identity with the prototype except the named differences,
the six member additions or successors, registry v90 add-only, release v90,
and the loader entries. v91 and earlier stay as they were. The coordinate
runs live in tests/test_page_alerts_v92.py.

The named differences from the prototype and the Track 0 sibling are the
line 6c inapplicable sentence, the top-entry zero sentence, and the two
line 6c labels. The prototype is loaded under a name no other module uses,
and no attribute of it is assigned.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from types import ModuleType
from typing import Any, cast

from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.tax.loader import (
    COVERED_FLAG_REFUSAL_OBJECTS,
    covered_flag_refusal_map,
    domain_package_companion_declarations,
    selection_collect_satisfied_by_family,
)
from tests import evidence_loader


REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/page-alerts-evidence"
L12D = REPO / "docs/phases/engine-breadth/milestones/line12d-boxes-evidence"
CORE = "tax.us.2025.package.core-calculations"
P = "tax.us.2025."
RELEASE_STEM = "demo.release.sli-worksheet-integration.2025"
INAPPLICABLE = (
    "This line 6c box does not apply to this return, or the box is the "
    "other checked/not-checked state."
)
ZERO = (
    "No gross payment amount in box 1a of a Form 1099-K for personal items "
    "you sold was recorded for 2025."
)
PROTOTYPE_ZERO = "No Form 1099-K statements were received for 2025."
LABEL_NOT_CHECKED = "Lump-sum election (not checked)"
LABEL_CHECKED = "Lump-sum election"
PROTOTYPE_LABEL = "Lump-sum election"
PROTOTYPE_CHECKED_LABEL = "Lump-sum election checked"
EARLIER = ("v91", "v90", "v89", "v88", "v87", "v86", "v85", "v84")
REPLACED = (
    P + "rule.form1040-line6c",
    P + "form1040.line-6c",
    P + "schedule1.top-entry.form-field",
)
ADDED = (
    P + "citation.schedule1.top-entry",
    P + "rule.form1040-line6c-checked",
    P + "form1040.line-6c-checked",
)


def _load(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _bytes(body: Any) -> bytes:
    return (json.dumps(body, indent=2) + "\n").encode("utf-8")


def _kept(body: dict[str, Any]) -> dict[str, Any]:
    skip = ("version", "members", "entrypoints", "package_checksum")
    return {key: value for key, value in body.items() if key not in skip}


def _prototype() -> ModuleType:
    return evidence_loader.load(EVIDENCE / "prototype.py", "pa_t1_v92_package_prototype")


def _line12d_names() -> None:
    # The line 12d harness is imported by bare name. Bind those names to this
    # owner's copies by path, so another evidence directory earlier on
    # sys.path cannot supply a different ``probe``.
    evidence_loader.load(L12D / "prototype.py", "prototype")
    evidence_loader.load(L12D / "probe.py", "probe")


def _sibling() -> ModuleType:
    _line12d_names()
    return evidence_loader.load(EVIDENCE / "track0.py", "pa_t1_v92_package_track0")


def test_citizens_match_the_prototype_except_the_named_differences() -> None:
    """Inapplicable sentence, zero sentence, and both labels are the differences."""
    prototype = _prototype()
    sibling = _sibling()
    written = cast(list[tuple[str, dict[str, Any]]], prototype.artifacts())
    assert [name for name, _body in written] == [
        "rule.form1040-line6c.v2.json",
        "form1040.line-6c.form-field.v2.json",
        "citation.schedule1.top-entry.json",
        "schedule1.top-entry.form-field.v2.json",
    ]
    for name, source in written:
        if name == "form1040.line-6c.form-field.v2.json":
            assert source["dispositions"]["guard_inapplicable"]["explain"] == (
                "line 6c disposition is inapplicable for the current class"
            )
            assert source["label"] == PROTOTYPE_LABEL
            source = copy.deepcopy(source)
            source["dispositions"]["guard_inapplicable"]["explain"] = INAPPLICABLE
            source["label"] = LABEL_NOT_CHECKED
        elif name == "schedule1.top-entry.form-field.v2.json":
            assert source["dispositions"]["closure_backed_zero"]["explain"] == PROTOTYPE_ZERO
            source = copy.deepcopy(source)
            source["dispositions"]["closure_backed_zero"]["explain"] = ZERO
        assert (CONTENT / name).read_bytes() == _bytes(source)

    rule = cast(dict[str, Any], sibling._checked_rule())
    field = cast(dict[str, Any], sibling._checked_field())
    assert field["dispositions"]["guard_inapplicable"]["explain"] == (
        "The checked lump-sum election disposition does not apply."
    )
    assert field["label"] == PROTOTYPE_CHECKED_LABEL
    revised = copy.deepcopy(field)
    revised["dispositions"]["guard_inapplicable"]["explain"] = INAPPLICABLE
    revised["label"] = LABEL_CHECKED
    assert (CONTENT / "rule.form1040-line6c-checked.json").read_bytes() == _bytes(rule)
    assert (CONTENT / "form1040.line-6c-checked.form-field.json").read_bytes() == _bytes(revised)


def test_core_v92_moves_exactly_the_six_members() -> None:
    before = _load(CONTENT / "package.core-calculations.v91.json")
    after = _load(CONTENT / "package.core-calculations.v92.json")
    assert (after["id"], after["version"], after["schema"]) == (CORE, "v92", before["schema"])
    assert _kept(after) == _kept(before)

    old_members = {row["id"]: row for row in cast(list[dict[str, Any]], before["members"])}
    new_members = {row["id"]: row for row in cast(list[dict[str, Any]], after["members"])}
    assert set(new_members) - set(old_members) == set(ADDED)
    assert set(old_members) - set(new_members) == set()
    changed = sorted(member_id for member_id, row in new_members.items() if old_members.get(member_id) != row)
    assert changed == sorted((*REPLACED, *ADDED))
    assert new_members[P + "rule.form1040-line6c"]["version"] == "v2"
    assert new_members[P + "form1040.line-6c"]["version"] == "v2"
    assert new_members[P + "schedule1.top-entry.form-field"]["version"] == "v2"
    assert new_members[P + "rule.schedule1-top-entry"] == old_members[P + "rule.schedule1-top-entry"]
    assert all(new_members[member_id]["role"] == old_members[member_id]["role"] for member_id in REPLACED)
    assert new_members[P + "citation.schedule1.top-entry"]["role"] == "citation"
    assert new_members[P + "rule.form1040-line6c-checked"]["role"] == "computation"
    assert new_members[P + "form1040.line-6c-checked"]["role"] == "form-field"

    old_entrypoints = {(row["id"], row["version"]) for row in cast(list[dict[str, Any]], before["entrypoints"])}
    new_entrypoints = {(row["id"], row["version"]) for row in cast(list[dict[str, Any]], after["entrypoints"])}
    assert old_entrypoints - new_entrypoints == {
        (P + "rule.form1040-line6c", "v1"),
        (P + "schedule1.top-entry.form-field", "v1"),
    }
    assert new_entrypoints - old_entrypoints == {
        (P + "rule.form1040-line6c", "v2"),
        (P + "schedule1.top-entry.form-field", "v2"),
        (P + "rule.form1040-line6c-checked", "v1"),
    }
    assert (P + "form1040.line-6c", "v2") not in new_entrypoints
    assert (P + "form1040.line-6c-checked", "v1") not in new_entrypoints
    assert after["package_checksum"] == package_instance_checksum(after)


def test_registry_v90_is_add_only() -> None:
    before = _load(CONTENT / "published-packages.v89.json")
    after = _load(CONTENT / "published-packages.v90.json")
    for key in ("citizens", "packages"):
        old = {(row["id"], row["version"]): row for row in cast(list[dict[str, Any]], before[key])}
        new = {(row["id"], row["version"]): row for row in cast(list[dict[str, Any]], after[key])}
        assert all(new[identity] == row for identity, row in old.items())
    added_citizens = {
        (row["id"], row["version"]): row["checksum"]
        for row in cast(list[dict[str, Any]], after["citizens"])
        if (row["id"], row["version"]) not in {
            (old["id"], old["version"]) for old in cast(list[dict[str, Any]], before["citizens"])
        }
    }
    names = {
        (P + "rule.form1040-line6c", "v2"): "rule.form1040-line6c.v2.json",
        (P + "form1040.line-6c", "v2"): "form1040.line-6c.form-field.v2.json",
        (P + "citation.schedule1.top-entry", "v1"): "citation.schedule1.top-entry.json",
        (P + "schedule1.top-entry.form-field", "v2"): "schedule1.top-entry.form-field.v2.json",
        (P + "rule.form1040-line6c-checked", "v1"): "rule.form1040-line6c-checked.json",
        (P + "form1040.line-6c-checked", "v1"): "form1040.line-6c-checked.form-field.json",
    }
    assert set(added_citizens) == set(names)
    for identity, name in names.items():
        assert added_citizens[identity] == citizen_checksum(_load(CONTENT / name))
    added_packages = [
        row for row in cast(list[dict[str, Any]], after["packages"])
        if (row["id"], row["version"]) not in {
            (old["id"], old["version"]) for old in cast(list[dict[str, Any]], before["packages"])
        }
    ]
    package = _load(CONTENT / "package.core-calculations.v92.json")
    assert added_packages == [{"checksum": package["package_checksum"], "id": CORE, "version": "v92"}]


def test_release_v90_and_loader_entries_carry_v91() -> None:
    release = _load(RELEASES / f"{RELEASE_STEM}.v90.json")
    previous = _load(RELEASES / f"{RELEASE_STEM}.v89.json")
    assert release["version"] == "v90"
    assert release["package_registry_sha256"] == hashlib.sha256(
        (CONTENT / "published-packages.v90.json").read_bytes()
    ).hexdigest()
    assert {key: value for key, value in release.items() if key not in ("version", "package_registry_sha256")} == {
        key: value for key, value in previous.items() if key not in ("version", "package_registry_sha256")
    }

    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v92")] == declarations[(CORE, "v91")]
    assert covered_flag_refusal_map(CORE, "v92") == COVERED_FLAG_REFUSAL_OBJECTS
    assert covered_flag_refusal_map(CORE, "v92") == covered_flag_refusal_map(CORE, "v91")
    assert selection_collect_satisfied_by_family(CORE, "v92") is True
    assert selection_collect_satisfied_by_family(CORE, "v91") is True


def test_v91_and_earlier_are_unchanged() -> None:
    before = _load(CONTENT / "published-packages.v89.json")
    after = _load(CONTENT / "published-packages.v90.json")
    old_packages = {(row["id"], row["version"]): row for row in cast(list[dict[str, Any]], before["packages"])}
    new_packages = {(row["id"], row["version"]): row for row in cast(list[dict[str, Any]], after["packages"])}
    assert all(new_packages[key] == value for key, value in old_packages.items())
    for version in EARLIER:
        package = _load(CONTENT / f"package.core-calculations.{version}.json")
        assert package["package_checksum"] == package_instance_checksum(package)
        assert old_packages[(CORE, version)]["checksum"] == package["package_checksum"]
        assert new_packages[(CORE, version)]["checksum"] == package["package_checksum"]
