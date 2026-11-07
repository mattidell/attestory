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


IN_CLASS = P + "schedule-d-boundary.form8949-in-class"
PROPOSITION = (
    "Whether this return's Form 8949 work beyond covered sales and code W is only boxes B, C, E and F: "
    "sales of stocks or other securities, each recorded once under the one box its statement gives it, "
    "with a basis you supply (and, on boxes C and F, net proceeds you supply) and an optional wash-sale "
    "adjustment. yes or no."
)
QUESTION = (
    "Is every sale on your Form 8949 either a sale your broker reported with its basis and no adjustment "
    "other than a wash-sale loss, or a sale of stocks or other securities, entered only once, with a "
    "basis you supply (and net proceeds you supply when you got no Form 1099-B) and no adjustment other "
    "than a wash-sale loss?"
)


def test_the_in_class_question_asks_exactly_the_proposition() -> None:
    """Review B1: the question is true of the proposition it is answered for.

    The proposition leaves out only covered sales with no adjustment or code W.
    So the question exempts a covered sale only with no adjustment other than
    a wash-sale loss, and every other sale must be a box B, C, E or F sale of
    securities, entered once, with a basis the filer supplies. A covered sale
    with any other code makes the truthful answer no.
    """
    question = _load(CONTENT / "input-question.schedule-d-boundary-form8949-in-class.json")
    bundle = _load(CONTENT / "schedule-d-boundary-form8949-in-class.bundle.json")
    (fact,) = [f for f in bundle["fact_types"] if f["id"] == IN_CLASS]
    assert question["fact_type"] == {"id": IN_CLASS, "version": fact["version"]}
    assert fact["title"] == PROPOSITION
    assert bundle["label"] == "Whether Form 8949 work beyond covered sales and code W is only boxes B, C, E and F"
    text = question["question"]
    assert text == QUESTION
    covered, other = text.removeprefix("Is every sale on your Form 8949 either ").split(", or ")
    # Each arm of the question carries the proposition's adjustment limit: code W only.
    for arm in (covered, other):
        assert arm.count("no adjustment other than a wash-sale loss") == 1, arm
    assert covered.startswith("a sale your broker reported with its basis")
    # The other arm is the proposition's boxes B, C, E and F: securities, once, basis supplied.
    for phrase in ("stocks or other securities", "entered only once", "a basis you supply",
                   "net proceeds you supply when you got no Form 1099-B"):
        assert phrase in other, phrase
    assert not text.startswith("Apart from")
    mapping = _load(CONTENT / "closure-mapping.f8949-no1099b.json")
    assert mapping["closure_question"] == (
        "Did you sell any stocks or other securities for which you did not receive a Form 1099-B "
        "or substitute statement?"
    )
    assert len(mapping["families"]) == 8


@pytest.mark.parametrize("name, version", [
    ("attachment.f8949.v4.json", "v4"),
    ("attachment.schedule-d.v8.json", "v8"),
])
def test_the_attachment_successors_name_boxes_c_and_f_and_lines_3_and_10(name: str, version: str) -> None:
    """Review N1: the title the page lists is the successor's own."""
    body = _load(CONTENT / name)
    title = body["title"]
    assert body["version"] == version
    assert f"attachment {version}:" in title
    assert "box C and box F" in title or "box C and F" in title
    assert "lines 3 and 10" in title or "lines 2, 3, 9 and 10" in title
