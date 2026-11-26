"""Fast publication and wording-bar tests for core v107 (sale-explanation-wording).

Core v107 replaces the 30 family-block-explanation citizens and the 8 sale
wash-sale adjustment input questions with v2 successors whose sentences read
plainly. Nothing else in the package moves.
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
WORDING = ROOT / "docs" / "phases" / "engine-breadth" / "milestones" / "sale-explanation-wording-evidence" / "wording.json"
CORE = "tax.us.2025.package.core-calculations"
STEM = "demo.release.sli-worksheet-integration.2025"
P = "tax.us.2025."

ENGINE_WORDS = ("family", "member", "block", "floor", "fact", "code", "constraint", "subtotal", "null")
COLUMN_LABEL = re.compile(r"\((?:[a-h])\)")


def _read(path: Path) -> dict[str, Any]:
    return dict(json.loads(path.read_text(encoding="utf-8")))


def _wording() -> list[dict[str, Any]]:
    return list(_read(WORDING)["replacements"])


def _pins(package: dict[str, Any]) -> set[tuple[str, str, str, str]]:
    return {(m["id"], m["version"], m["schema"], m["role"]) for m in package["members"]}


def _successor_path(row: dict[str, Any]) -> Path:
    return ROOT / re.sub(r"(?:\.v\d+)?\.json$", ".v2.json", row["file"])


def test_core_v107_replaces_exactly_the_38_sentence_citizens() -> None:
    v106 = _read(CONTENT / "package.core-calculations.v106.json")
    v107 = _read(CONTENT / "package.core-calculations.v107.json")
    assert (v107["id"], v107["version"], v107["schema"]) == (CORE, "v107", v106["schema"])
    assert v107["package_checksum"] == package_instance_checksum(v107)
    assert v107["admitted_schemas"] == v106["admitted_schemas"]
    assert v107["input_bindings"] == v106["input_bindings"]
    assert v107["composition_obligations"] == v106["composition_obligations"]
    assert v107["scope"] == v106["scope"]

    rows = _wording()
    assert len(rows) == 38
    moved = {r["id"] for r in rows}
    removed = _pins(v106) - _pins(v107)
    added = _pins(v107) - _pins(v106)
    assert {pin[0] for pin in removed} == moved == {pin[0] for pin in added}
    assert {(pin[0], pin[2], pin[3]) for pin in removed} == {(pin[0], pin[2], pin[3]) for pin in added}
    assert {pin[1] for pin in removed} == {"v1"} and {pin[1] for pin in added} == {"v2"}
    assert sum(1 for pin in added if pin[2] == "family-block-explanation.v1") == 30
    assert sum(1 for pin in added if pin[2] == "input-question.v1") == 8

    bump = {(i, "v1"): (i, "v2") for i in moved}
    old_entries = [bump.get((e["id"], e["version"]), (e["id"], e["version"])) for e in v106["entrypoints"]]
    assert old_entries == [(e["id"], e["version"]) for e in v107["entrypoints"]]
    # Same order: each replacement sits where its predecessor sat.
    assert [bump.get((m["id"], m["version"]), (m["id"], m["version"])) for m in v106["members"]] == [
        (m["id"], m["version"]) for m in v107["members"]
    ]


@pytest.mark.parametrize("row", _wording(), ids=lambda r: r["id"][len(P):])
def test_each_successor_is_its_predecessor_with_only_the_sentence_and_version(row: dict[str, Any]) -> None:
    old = _read(ROOT / row["file"])
    new = _read(_successor_path(row))
    prop = row["property"]
    assert old[prop] == row["old"]
    assert new[prop] == row["new"]
    assert {**old, "version": "v2", prop: row["new"]} == new
    assert list(new) == list(old)


def test_registry_v105_is_add_only_and_release_v105_moves_only_the_registry() -> None:
    reg104 = _read(CONTENT / "published-packages.v104.json")
    reg105 = _read(CONTENT / "published-packages.v105.json")
    assert reg105["citizens"][: len(reg104["citizens"])] == reg104["citizens"]
    assert reg105["packages"][: len(reg104["packages"])] == reg104["packages"]
    added = reg105["citizens"][len(reg104["citizens"]):]
    assert {(e["id"], e["version"]) for e in added} == {(r["id"], "v2") for r in _wording()}
    for row in _wording():
        entry = next(e for e in added if e["id"] == row["id"])
        assert entry["checksum"] == citizen_checksum(_read(_successor_path(row)))
    v107 = _read(CONTENT / "package.core-calculations.v107.json")
    assert reg105["packages"][len(reg104["packages"]):] == [
        {"id": CORE, "version": "v107", "checksum": v107["package_checksum"]}
    ]
    rel104 = _read(RELEASES / f"{STEM}.v104.json")
    rel105 = _read(RELEASES / f"{STEM}.v105.json")
    digest = hashlib.sha256((CONTENT / "published-packages.v105.json").read_bytes()).hexdigest()
    assert rel105 == {**rel104, "version": "v105", "package_registry_sha256": digest}


def test_v107_loader_entries_carry_v106() -> None:
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v107")] == declarations[(CORE, "v106")]
    assert covered_flag_refusal_map(CORE, "v107") == covered_flag_refusal_map(CORE, "v106")
    for switch in (
        selection_collect_satisfied_by_family,
        later_any_arm_refs_while_count_blocked,
        unconfirmed_family_names_closure_question,
        explains_identity_exclusivity_collision,
    ):
        assert switch(CORE, "v107") == switch(CORE, "v106") is True


def test_every_v107_member_constraint_has_its_plain_explanation() -> None:
    """ADR 0088 Decision 5 on the current core: each sale rule has an adopted explanation."""
    v107 = _read(CONTENT / "package.core-calculations.v107.json")
    by_key = {(r["family_id"], r["block_code"]): r for r in _wording() if r["property"] == "explanation"}
    adopted = {(m["id"], m["version"]) for m in v107["members"]}
    families: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("family.*.json"):
        doc = _read(path)
        families[(doc["id"], doc["version"])] = doc
    explanations: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("family-block-explanation.*.v2.json"):
        doc = _read(path)
        explanations[(doc["family_id"], doc["block_code"])] = doc
    checked = 0
    for pin in v107["members"]:
        if not pin["schema"].startswith("source-family."):
            continue
        family = families[(pin["id"], pin["version"])]
        for constraint in family.get("member_constraints", []):
            key = (family["id"], constraint["block_code"])
            doc = explanations[key]
            assert (doc["id"], doc["version"]) in adopted
            assert doc["explanation"] == by_key[key]["new"]
            checked += 1
    assert checked == 30


def _sentences(text: str) -> list[str]:
    return [part for part in re.split(r"(?<=[.?!])\s+", text.strip()) if part]


@pytest.mark.parametrize("row", _wording(), ids=lambda r: r["id"][len(P):])
def test_each_sentence_meets_the_mechanical_wording_bar(row: dict[str, Any]) -> None:
    text = row["new"]
    lowered = text.lower()
    assert not [word for word in ENGINE_WORDS if re.search(r"\b" + word, lowered)], text
    assert not re.search(r"[A-Z]{2,}_[A-Z_]+", text), text
    assert ";" not in text, text
    assert "(" not in COLUMN_LABEL.sub("", text) and ")" not in COLUMN_LABEL.sub("", text), text
    assert len(_sentences(text)) <= 2, text
    assert "1099-B" in text or "8949" in text, text
    if row["property"] == "explanation":
        assert lowered.count("proceeds") <= 1 and lowered.count("basis") <= 1, text
        assert text.startswith(("You ", "This ", "The ", "Box ")), text
    else:
        assert _sentences(text)[0].endswith("?"), text
        assert "enter 0" in lowered or "if there is one" in lowered, text


def test_short_and_long_term_read_the_same_where_the_rule_is_the_same() -> None:
    by_pair: dict[tuple[str, str], dict[str, str]] = {}
    for row in _wording():
        if row["property"] == "explanation":
            stem, term = row["family_id"].rsplit("-", 1)
            by_pair.setdefault((stem, row["block_code"]), {})[term] = row["new"]
        else:
            stem, term = row["id"].rsplit("-adjustment", 1)[0].rsplit("-", 1)
            word = {"st": "short-term", "lt": "long-term"}[term]
            by_pair.setdefault((stem, "question"), {})[term] = row["new"].replace(word, "TERM")
    assert len(by_pair) == 19
    for key, texts in by_pair.items():
        assert set(texts) == {"st", "lt"}, key
        assert texts["st"] == texts["lt"], key


def test_one_rule_reads_the_same_across_sale_kinds_except_where_the_form_differs() -> None:
    rows = [r for r in _wording() if r["property"] == "explanation"]
    holding = {r["family_id"]: r["new"] for r in rows if r["block_code"] == "HOLDING_PERIOD_MISMATCH"}
    with_1099b = {text for fam, text in holding.items() if ".f1099b." in fam}
    without = {text for fam, text in holding.items() if ".f8949.no1099b" in fam}
    assert len(with_1099b) == 1 and len(without) == 1
    assert "box 2 of your Form 1099-B" in next(iter(with_1099b))
    assert "1099-B" not in next(iter(without))
    for code in ("CODE_W_ON_GAIN", "ADJUSTMENT_EXCEEDS_LOSS"):
        texts = {r["family_id"]: r["new"] for r in rows if r["block_code"] == code}
        assert "box 1g" in texts[P + "f1099b.covered-w-st"]
        assert "column (g)" in texts[P + "f1099b.noncovered-st"]
        assert "net proceeds" in texts[P + "f8949.no1099b-st"]
        assert "correct basis" in texts[P + "f1099b.code-b-st"]
