"""Fast publication and wording-bar tests for core v108 (code-b-basis-sentence).

Core v108 replaces the four code B wash-sale explanations
(ADJUSTMENT_EXCEEDS_LOSS and CODE_W_ON_GAIN, short-term and long-term) with v3
successors whose second sentence names the correct basis the filer entered.
Nothing else in the package moves.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import pytest

from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.tax.loader import (
    covered_flag_refusal_map,
    domain_package_companion_declarations,
    explains_identity_exclusivity_collision,
    later_any_arm_refs_while_count_blocked,
    selection_collect_satisfied_by_family,
    unconfirmed_family_names_closure_question,
)

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
RELEASES = ROOT / "packages" / "sample_data" / "student_loan_worksheet_integration" / "publication_surface" / "releases"
MILESTONES = ROOT / "docs" / "phases" / "engine-breadth" / "milestones"
WORDING = MILESTONES / "code-b-basis-sentence-evidence" / "wording.json"
V107_WORDING = MILESTONES / "sale-explanation-wording-evidence" / "wording.json"
CORE = "tax.us.2025.package.core-calculations"
STEM = "demo.release.sli-worksheet-integration.2025"
P = "tax.us.2025."

ENGINE_WORDS = ("family", "member", "block", "floor", "fact", "code", "constraint", "subtotal", "null")
COLUMN_LABEL = re.compile(r"\((?:[a-h])\)")
SECOND = ("Check the proceeds and wash-sale loss you entered against box 1d and box 1g of your Form 1099-B, "
          "and the correct basis you entered against your own records, then fix whichever amount is wrong.")
FOUR = {
    f"{P}family-block-explanation.f1099b-code-b-{term}.{code}"
    for term in ("st", "lt")
    for code in ("adjustment-exceeds-loss", "code-w-on-gain")
}


def _read(path: Path) -> dict[str, Any]:
    return dict(json.loads(path.read_text(encoding="utf-8")))


def _wording() -> list[dict[str, Any]]:
    return list(_read(WORDING)["replacements"])


def _pins(package: dict[str, Any]) -> set[tuple[str, str, str, str]]:
    return {(m["id"], m["version"], m["schema"], m["role"]) for m in package["members"]}


def _successor_path(row: dict[str, Any]) -> Path:
    return ROOT / re.sub(r"\.v2\.json$", ".v3.json", row["file"])


def _sentences(text: str) -> list[str]:
    return [part for part in re.split(r"(?<=[.?!])\s+", text.strip()) if part]


def test_the_wording_record_is_the_four_code_b_wash_sale_explanations_with_the_decision_1_sentence() -> None:
    rows = _wording()
    assert {r["id"] for r in rows} == FOUR and len(rows) == 4
    for row in rows:
        assert row["version"] == "v2" and row["property"] == "explanation"
        old, new = _sentences(row["old"]), _sentences(row["new"])
        assert len(old) == len(new) == 2
        assert new[0] == old[0]
        assert new[1] == SECOND


def test_core_v108_replaces_exactly_the_four_explanations_in_place() -> None:
    v107 = _read(CONTENT / "package.core-calculations.v107.json")
    v108 = _read(CONTENT / "package.core-calculations.v108.json")
    assert (v108["id"], v108["version"], v108["schema"]) == (CORE, "v108", v107["schema"])
    assert v108["package_checksum"] == package_instance_checksum(v108)
    for key in ("admitted_schemas", "input_bindings", "composition_obligations", "scope"):
        assert v108[key] == v107[key], key
    removed = _pins(v107) - _pins(v108)
    added = _pins(v108) - _pins(v107)
    assert {pin[0] for pin in removed} == FOUR == {pin[0] for pin in added}
    assert {(pin[0], pin[2], pin[3]) for pin in removed} == {(pin[0], pin[2], pin[3]) for pin in added}
    assert {pin[1] for pin in removed} == {"v2"} and {pin[1] for pin in added} == {"v3"}
    assert {pin[2] for pin in added} == {"family-block-explanation.v1"}
    bump = {(i, "v2"): (i, "v3") for i in FOUR}
    assert [bump.get((e["id"], e["version"]), (e["id"], e["version"])) for e in v107["entrypoints"]] == [
        (e["id"], e["version"]) for e in v108["entrypoints"]
    ]
    assert [bump.get((m["id"], m["version"]), (m["id"], m["version"])) for m in v107["members"]] == [
        (m["id"], m["version"]) for m in v108["members"]
    ]
    assert {k for k in v108 if v108[k] != v107[k]} <= {"version", "members", "entrypoints", "package_checksum"}


@pytest.mark.parametrize("row", _wording(), ids=lambda r: r["id"][len(P):])
def test_each_successor_is_its_predecessor_with_only_the_sentence_and_version(row: dict[str, Any]) -> None:
    old = _read(ROOT / row["file"])
    new = _read(_successor_path(row))
    assert old["explanation"] == row["old"]
    assert new["explanation"] == row["new"]
    assert {**old, "version": "v3", "explanation": row["new"]} == new
    assert list(new) == list(old)


def test_registry_v106_is_add_only_and_release_v106_moves_only_the_registry() -> None:
    reg105 = _read(CONTENT / "published-packages.v105.json")
    reg106 = _read(CONTENT / "published-packages.v106.json")
    assert {k for k in reg106 if reg106[k] != reg105[k]} <= {"citizens", "packages"}
    assert reg106["citizens"][: len(reg105["citizens"])] == reg105["citizens"]
    assert reg106["packages"][: len(reg105["packages"])] == reg105["packages"]
    added = reg106["citizens"][len(reg105["citizens"]):]
    assert sorted((e["id"], e["version"]) for e in added) == sorted((i, "v3") for i in FOUR)
    for row in _wording():
        entry = next(e for e in added if e["id"] == row["id"])
        assert entry["checksum"] == citizen_checksum(_read(_successor_path(row)))
    v108 = _read(CONTENT / "package.core-calculations.v108.json")
    assert reg106["packages"][len(reg105["packages"]):] == [
        {"id": CORE, "version": "v108", "checksum": v108["package_checksum"]}
    ]
    rel105 = _read(RELEASES / f"{STEM}.v105.json")
    rel106 = _read(RELEASES / f"{STEM}.v106.json")
    digest = hashlib.sha256((CONTENT / "published-packages.v106.json").read_bytes()).hexdigest()
    assert rel106 == {**rel105, "version": "v106", "package_registry_sha256": digest}


def test_v108_loader_entries_carry_v107() -> None:
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v108")] == declarations[(CORE, "v107")]
    assert covered_flag_refusal_map(CORE, "v108") == covered_flag_refusal_map(CORE, "v107")
    for switch in (
        selection_collect_satisfied_by_family,
        later_any_arm_refs_while_count_blocked,
        unconfirmed_family_names_closure_question,
        explains_identity_exclusivity_collision,
    ):
        assert switch(CORE, "v108") == switch(CORE, "v107") is True


def test_every_v108_explanation_is_the_v107_wording_except_the_four() -> None:
    """The other 26 sale explanations and 8 questions stay on their v107 words."""
    v107 = _read(CONTENT / "package.core-calculations.v107.json")
    v108 = _read(CONTENT / "package.core-calculations.v108.json")
    others = {(m["id"], m["version"]) for m in v107["members"]
              if m["schema"] in ("family-block-explanation.v1", "input-question.v1") and m["id"] not in FOUR}
    assert others <= {(m["id"], m["version"]) for m in v108["members"]}
    assert sum(1 for m in v108["members"] if m["schema"] == "family-block-explanation.v1") == 30


def _v108_sentences() -> list[tuple[str, str]]:
    """Every v107-bar sentence as v108 adopts it: v107 wording, with the four replaced."""
    four = {r["id"]: r["new"] for r in _wording()}
    return [(r["id"], four.get(r["id"], r["new"])) for r in _read(V107_WORDING)["replacements"]]


@pytest.mark.parametrize("item", _v108_sentences(), ids=lambda item: item[0][len(P):])
def test_the_v107_wording_bar_holds_with_the_decision_2_exception(item: tuple[str, str]) -> None:
    cid, text = item
    lowered = text.lower()
    assert not [word for word in ENGINE_WORDS if re.search(r"\b" + word, lowered)], text
    assert not re.search(r"[A-Z]{2,}_[A-Z_]+", text), text
    assert ";" not in text, text
    assert "(" not in COLUMN_LABEL.sub("", text) and ")" not in COLUMN_LABEL.sub("", text), text
    assert "1099-B" in text or "8949" in text, text
    for match in re.finditer(r"basis|proceeds", lowered):
        window = lowered[max(0, match.start() - 60): match.end() + 60]
        assert re.search(r"\bbox \w+|\bcolumns? \(|you entered|you said", window), (match.group(), text)
    if ".family-block-explanation." in cid:
        assert len(_sentences(text)) <= 2, text
        assert lowered.count("proceeds") <= 1, text
        assert text.startswith(("You ", "This ", "The ")), text
        if cid in FOUR:
            # Decision 2: the four read the filer's correct basis, so "basis" appears twice,
            # each time as "the correct basis you entered".
            assert lowered.count("basis") == 2, text
            assert lowered.count("correct basis you entered") == 2, text
        else:
            assert lowered.count("basis") <= 1, text
