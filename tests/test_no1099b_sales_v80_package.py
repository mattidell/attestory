"""Core v80 is the scratch v80 Track 0 proved, published as successors only.

Static checks on the published package, registry and loader entries for
sales with no Form 1099-B (Form 8949 boxes C and F). The cases run through
the coordinator in tests/test_no1099b_sales_v80.py.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from packages.tax.loader import (
    COVERED_FLAG_REFUSAL_OBJECTS,
    covered_flag_refusal_map,
    domain_package_companion_declarations,
    no1099b_scalar_presence_pairs,
    noncovered_scalar_presence_pairs,
)

REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "packages/content/tax/2025"
RULES = REPO / "docs/phases/engine-breadth/milestones/f8949-boxes-cf-evidence/cf-prototype-rules"
CORE = "tax.us.2025.package.core-calculations"
P = "tax.us.2025."


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _prototype_files() -> list[Path]:
    return sorted(p for p in RULES.glob("*.json") if p.name != "_members.json")


def test_every_successor_is_the_prototype_byte_for_byte() -> None:
    files = _prototype_files()
    assert len(files) == 61
    for path in files:
        assert (CONTENT / path.name).read_bytes() == path.read_bytes(), path.name


def test_core_v80_is_v79_with_exactly_the_prototype_member_edits() -> None:
    v79 = _load(CONTENT / "package.core-calculations.v79.json")
    v80 = _load(CONTENT / "package.core-calculations.v80.json")
    edits = _load(RULES / "_members.json")
    assert (v80["id"], v80["version"]) == (CORE, "v80")
    members = {(m["id"], m["version"]): m for m in v79["members"]}
    for edit in edits:
        if edit["op"] == "replace":
            old = edit["old"]
            assert members.pop((old["id"], old["version"])) == old
        else:
            assert edit["op"] == "add"
        new = edit["new"]
        assert (new["id"], new["version"]) not in members
        members[(new["id"], new["version"])] = new
    assert sorted(members) == sorted((m["id"], m["version"]) for m in v80["members"])
    assert sum(e["op"] == "add" for e in edits) == 43
    assert sum(e["op"] == "replace" for e in edits) == 18


def test_registry_v78_only_adds_to_v77() -> None:
    v77 = _load(CONTENT / "published-packages.v77.json")
    v78 = _load(CONTENT / "published-packages.v78.json")
    for key in ("citizens", "packages"):
        before = {(e["id"], e["version"]): e for e in v77[key]}
        after = {(e["id"], e["version"]): e for e in v78[key]}
        for identity, entry in before.items():
            assert after[identity] == entry, identity
    added_packages = {(e["id"], e["version"]) for e in v78["packages"]} - {
        (e["id"], e["version"]) for e in v77["packages"]
    }
    assert added_packages == {(CORE, "v80")}


def test_core_v80_declares_each_box_c_and_f_amount_beside_its_sale() -> None:
    declarations = domain_package_companion_declarations()
    v79, v80 = declarations[(CORE, "v79")], declarations[(CORE, "v80")]
    pairs = no1099b_scalar_presence_pairs()
    assert len(pairs) == 6
    assert v80["presence_pairs"] == {**v79["presence_pairs"], **pairs}
    assert v80["value_domains"] == v79["value_domains"]
    for scalar, sale in pairs.items():
        assert scalar.startswith(sale + ".")
        assert scalar not in v79["presence_pairs"]
    assert set(noncovered_scalar_presence_pairs()) <= set(v80["presence_pairs"])
    assert covered_flag_refusal_map(CORE, "v80") == COVERED_FLAG_REFUSAL_OBJECTS


@pytest.mark.parametrize("line", ["3", "10"])
def test_lines_3_and_10_explain_every_disposition(line: str) -> None:
    field = _load(CONTENT / f"schedule-d.line-{line}.form-field.json")
    assert field["binds_symbol"] == P + f"schedule-d.line-{line}"
    for disposition in ("published_value", "computed_zero", "closure_backed_zero", "blocked"):
        explain = field["dispositions"][disposition]["explain"]
        assert explain.startswith(f"Schedule D line {line}, column (h),"), (disposition, explain)
    box = "C" if line == "3" else "F"
    assert f"box {box}" in field["dispositions"]["published_value"]["explain"]
    citation = _load(CONTENT / f"citation.schedule-d.line-{line}.json")
    assert citation["id"] == P + f"citation.schedule-d.line-{line}"


def test_the_in_class_answer_says_entered_only_once() -> None:
    question = _load(CONTENT / "input-question.schedule-d-boundary-form8949-in-class.json")
    assert "entered only once" in question["question"]
    mapping = _load(CONTENT / "closure-mapping.f8949-no1099b.json")
    assert mapping["closure_question"] == (
        "Did you sell any stocks or other securities for which you did not receive a Form 1099-B "
        "or substitute statement?"
    )
    assert len(mapping["families"]) == 8
