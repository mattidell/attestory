"""Published v93 adds ten prototype questions with one named wording repair.

These static checks cover immutable prior publications, additive adoption,
the registry/release integrity chain and production loader declarations.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, cast

from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.tax.loader import (
    covered_flag_refusal_map,
    domain_package_companion_declarations,
    selection_collect_satisfied_by_family,
)
from tests import evidence_loader

REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/line6b-reason-evidence"
CORE = "tax.us.2025.package.core-calculations"
STEM = "demo.release.sli-worksheet-integration.2025"
TERRITORIAL_NAME = "input-question.ss-benefits-scope-no-puerto-rico-or-samoa-income.v1.json"
TERRITORIAL_QUESTION = "For 2025, were you (or your spouse, if filing jointly) a bona fide resident of Puerto Rico or American Samoa who had any income?"


def _read(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text()))


def _artifacts() -> list[tuple[str, dict[str, Any]]]:
    prototype = evidence_loader.load(EVIDENCE / "prototype.py", "l6b_v93_package_prototype")
    artifacts = copy.deepcopy(cast(list[tuple[str, dict[str, Any]]], prototype.artifacts()))
    for name, body in artifacts:
        if name == TERRITORIAL_NAME:
            assert body["question"] == "Were you a bona fide resident of Puerto Rico or American Samoa with income from there in 2025?"
            body["question"] = TERRITORIAL_QUESTION
    return artifacts


def _index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    result = {(row["id"], row["version"]): row for row in rows}
    assert len(result) == len(rows)
    return result


def test_ten_question_files_match_p0_except_named_territorial_repair() -> None:
    artifacts = _artifacts()
    assert len(artifacts) == 10
    assert len({body["fact_type"]["id"] for _, body in artifacts}) == 10
    for name, body in artifacts:
        assert (CONTENT / name).read_bytes() == (json.dumps(body, indent=2) + "\n").encode()


def test_v93_adds_exactly_ten_members_and_entrypoints() -> None:
    before = _read(CONTENT / "package.core-calculations.v92.json")
    after = _read(CONTENT / "package.core-calculations.v93.json")
    assert (after["id"], after["version"]) == (CORE, "v93")
    skip = {"version", "members", "entrypoints", "package_checksum"}
    assert {k: v for k, v in after.items() if k not in skip} == {
        k: v for k, v in before.items() if k not in skip
    }
    expected = {(body["id"], "v1"): body for _, body in _artifacts()}
    for kind in ("members", "entrypoints"):
        old, new = _index(before[kind]), _index(after[kind])
        assert all(new[key] == row for key, row in old.items())
        assert set(new) - set(old) == set(expected)
        for key, body in expected.items():
            wanted = {"id": body["id"], "version": "v1"}
            if kind == "members":
                wanted.update(schema="input-question.v1", role="input-question")
            assert new[key] == wanted
    assert after["package_checksum"] == package_instance_checksum(after)


def test_registry_v91_is_add_only_with_exactly_the_ten_citizens() -> None:
    before = _read(CONTENT / "published-packages.v90.json")
    after = _read(CONTENT / "published-packages.v91.json")
    for kind in ("citizens", "packages"):
        old, new = _index(before[kind]), _index(after[kind])
        assert all(new[key] == row for key, row in old.items())
        added = {key: row for key, row in new.items() if key not in old}
        if kind == "citizens":
            assert added == {
                (body["id"], "v1"): {
                    "id": body["id"], "version": "v1", "checksum": citizen_checksum(body)
                } for _, body in _artifacts()
            }
        else:
            package = _read(CONTENT / "package.core-calculations.v93.json")
            assert added == {(CORE, "v93"): {
                "id": CORE, "version": "v93", "checksum": package["package_checksum"]
            }}


def test_release_and_loader_declarations_carry_v92() -> None:
    before = _read(RELEASES / f"{STEM}.v90.json")
    after = _read(RELEASES / f"{STEM}.v91.json")
    assert after["version"] == "v91"
    assert after["package_registry_sha256"] == hashlib.sha256(
        (CONTENT / "published-packages.v91.json").read_bytes()
    ).hexdigest()
    skip = {"version", "package_registry_sha256"}
    assert {k: v for k, v in after.items() if k not in skip} == {
        k: v for k, v in before.items() if k not in skip
    }
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v93")] == declarations[(CORE, "v92")]
    assert covered_flag_refusal_map(CORE, "v93") == covered_flag_refusal_map(CORE, "v92")
    assert covered_flag_refusal_map(CORE, "v93")
    assert selection_collect_satisfied_by_family(CORE, "v93") is True
    assert selection_collect_satisfied_by_family(CORE, "v92") is True


def test_v92_and_all_earlier_core_checksums_are_unchanged() -> None:
    before = _index(_read(CONTENT / "published-packages.v90.json")["packages"])
    after = _index(_read(CONTENT / "published-packages.v91.json")["packages"])
    for path in CONTENT.glob("package.core-calculations.v*.json"):
        package = _read(path)
        if int(package["version"][1:]) > 92:
            continue
        identity = (CORE, package["version"])
        assert before[identity] == after[identity]
        assert before[identity]["checksum"] == package["package_checksum"]
        assert package["package_checksum"] == package_instance_checksum(package)
