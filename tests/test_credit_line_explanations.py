"""Track 1: each credit line explains itself, on core v64 (runs go through
``live_coordinate_run``).

On core v63 seven form fields carry Form 1040 line 27a's disposition texts, so a saved
return tells the reader that the child tax credit (line 19) is "the earned income credit".
Core v64 publishes a successor of each of the seven with its own line's texts. Only the
``version`` and the disposition ``explain`` texts change: every published value is the one
v63 publishes. Synthetic ``demo.*`` data only.
"""

from __future__ import annotations

import copy
import functools
import hashlib
import importlib.util
import json
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

import pytest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.package_validation import citizen_checksum
from packages.derivation.production_resolver import PublicationSurface
from packages.tax.loader import domain_package_companion_declarations
from tests.test_form_1099_k_income import _handover
from tests.test_form_1099_withholding import (
    CONTENT,
    RELEASE_DIR,
    _social_security_withholding,
    _unemployment_withholding,
)
from tests.test_other_dependents_credit_track1 import _complete, build, ctc_child
from tests.test_refund_or_amount_owed_track1 import ROOT, USER, _act, _attested, _finish, _load

PACKAGE_V63 = CONTENT / "package.core-calculations.v63.json"
PACKAGE_V64 = CONTENT / "package.core-calculations.v64.json"
REGISTRY_V61 = CONTENT / "published-packages.v61.json"
REGISTRY_V62 = CONTENT / "published-packages.v62.json"
RELEASE_V61 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v61.json"
RELEASE_V62 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v62.json"
SURFACE_V63 = PublicationSurface(RELEASE_DIR, REGISTRY_V61, CONTENT)
SURFACE_V64 = PublicationSurface(RELEASE_DIR, REGISTRY_V62, CONTENT)
CORES = {
    "v63": (PACKAGE_V63, RELEASE_V61, "v61", SURFACE_V63),
    "v64": (PACKAGE_V64, RELEASE_V62, "v62", SURFACE_V64),
}
SURVEY = ROOT / "docs/phases/engine-breadth/milestones/credit-line-explanations-evidence/survey.py"
P = "tax.us.2025."
OD = "tax.us.2025.ctc.no-other-dependent"
DTB_PREFIX = "tax.us.2025.dtb.child."

# form-field id -> (own line named in its texts, filename stem)
FIELDS: dict[str, tuple[str, str]] = {
    P + "form1040.line-19": ("Form 1040 line 19", "form1040.line-19"),
    P + "form1040.line-28": ("Form 1040 line 28", "form1040.line-28"),
    P + "form.sch8812.line-4": ("Schedule 8812 line 4", "form.sch8812.line-4"),
    P + "form.sch8812.line-14": ("Schedule 8812 line 14", "form.sch8812.line-14"),
    P + "form.sch8812.line-17": ("Schedule 8812 line 17", "form.sch8812.line-17"),
    P + "form.sch8812.line-20": ("Schedule 8812 line 20", "form.sch8812.line-20"),
    P + "form.sch8812.worksheet-a.line-5": ("Credit Limit Worksheet A line 5", "form.sch8812.worksheet-a.line-5"),
}
# Descriptions that were incomplete and are corrected in the successor (the review's R1 and N2).
DESCRIPTION_REWRITTEN = {P + "form1040.line-19", P + "form.sch8812.line-14", P + "form1040.line-28"}
LINE27A_TEXTS = json.loads((CONTENT / "form1040.line-27a.form-field.json").read_text(encoding="utf-8"))["dispositions"]
SYMBOL_19 = P + "ctc.form1040-line19"
SYMBOL_28 = P + "ctc.form1040-line28"


def _read(stem: str, version: str) -> dict[str, Any]:
    name = f"{stem}.form-field.json" if version == "v1" else f"{stem}.form-field.{version}.json"
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text(encoding="utf-8")))


def _survey() -> Any:
    spec = importlib.util.spec_from_file_location("credit_line_survey", SURVEY)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- running -----------------------------------------------------------------------------


def _return(*, answered: bool = True) -> list[dict[str, object]]:
    """Single parent, wages $30,000, one qualifying child who also lived with a grandparent:
    the child tax credit (line 19), the earned income credit (line 27a) and the additional
    child tax credit (line 28) all publish. With ``answered`` false the dependent tie-breaker
    questions for the child are left unanswered, so the credit lines are blocked."""
    ret_answers = {
        OD: "yes",
        "tax.us.2025.eic.age-25-under-65": "yes",
        "tax.us.2025.eic.main-home-in-us": "yes",
    }
    acts = build(wages=30000.0, filing_status="single", children={"demo-child-1": ctc_child()},
                 return_answers=ret_answers)
    acts.append(_act(len(acts), "bundle-adoption", {"bundle": _load("dtb-questions.bundle.json")}))
    if answered:
        for k, v in {"another-could-claim": "yes", "multiple-other-claimants": "no",
                     "filer-is-parent": "yes", "other-is-parent": "no"}.items():
            fid = f"{DTB_PREFIX}{k}|child=demo-child-1,tax-year=2025"
            acts.append(_act(len(acts), "assertion", {"finding": _attested(f"demo.dtb.{k}", fid, v)}))
    acts = _complete(acts)
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])
    return acts


@functools.lru_cache(maxsize=None)
def _present(core: str, closed: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    package, release, rel_version, surface = CORES[core]
    run_id = f"demo.cle.{core}.{'closed' if closed else 'open'}"
    finished = _finish(
        copy.deepcopy(_return(answered=closed)), package_path=package, package_version=core,
        release_path=release, release_version=rel_version, note=run_id,
    )
    finished = _handover(finished, surface=surface, reconfirm=True)
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        assert outcome.refusal is None, f"{run_id} refused: {outcome.refusal}"
        assert outcome.presentation_path is not None
        model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
        assert outcome.output_path is not None
        report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
    pubs = {str(item.finding["symbol"]): item.finding for item in outcome.publications or ()}
    rows = [r for r in report.get("dispositions", []) if r.get("disposition") == "blocked"]
    blocked = {str(r["artifact_id"]) for r in rows}
    return model, {"pubs": pubs, "blocked": blocked, "rows": rows}


def _embedded_fields(node: Any, found: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    """Every form field the saved presentation embeds, by id."""
    if isinstance(node, dict):
        if isinstance(node.get("dispositions"), dict) and isinstance(node.get("id"), str) and "line" in node:
            found.setdefault(node["id"], []).append(node)
        for value in node.values():
            _embedded_fields(value, found)
    elif isinstance(node, list):
        for value in node:
            _embedded_fields(value, found)
    return found


def _texts(field: dict[str, Any]) -> dict[str, str]:
    return {code: row["explain"] for code, row in field["dispositions"].items()}


# --- the successors ----------------------------------------------------------------------


@pytest.mark.parametrize("field_id", sorted(FIELDS))
def test_successor_texts_name_their_own_line(field_id: str) -> None:
    line, stem = FIELDS[field_id]
    old, new = _read(stem, "v1"), _read(stem, "v2")
    assert new["id"] == field_id and new["version"] == "v2"
    for code, text in _texts(new).items():
        assert line in text, (code, text)
        assert "earned income credit" not in text.lower(), (code, text)
    assert _texts(new)["published_value"] == new["description"]
    # nothing but the version and the explain texts changed
    for key in ("binds_symbol", "citation", "form", "id", "line", "schema"):
        assert new[key] == old[key], key
    # Schedule 8812 line 14 is both credits; only its label was too narrow.
    assert (new["label"] != old["label"]) == (field_id == "tax.us.2025.form.sch8812.line-14")
    # the description is rewritten only where the old one under-described the line
    assert (new["description"] != old["description"]) == (field_id in DESCRIPTION_REWRITTEN)
    for code, row in new["dispositions"].items():
        assert {k: v for k, v in row.items() if k != "explain"} == {
            k: v for k, v in old["dispositions"][code].items() if k != "explain"}, code
    assert set(new["dispositions"]) == set(old["dispositions"])


@pytest.mark.parametrize("field_id", sorted(FIELDS))
def test_v63_fields_keep_the_old_text(field_id: str) -> None:
    _, stem = FIELDS[field_id]
    old = _read(stem, "v1")
    assert _texts(old) == _texts({"dispositions": LINE27A_TEXTS})
    assert old["version"] == "v1"
    package = json.loads(PACKAGE_V63.read_text(encoding="utf-8"))
    assert {"id": field_id, "role": "form-field", "schema": "form-field.v3", "version": "v1"} in package["members"]


# --- the package chain -------------------------------------------------------------------


def test_v64_swaps_exactly_the_seven_form_fields() -> None:
    v63 = json.loads(PACKAGE_V63.read_text(encoding="utf-8"))
    v64 = json.loads(PACKAGE_V64.read_text(encoding="utf-8"))
    assert (v64["id"], v64["version"]) == (v63["id"], "v64")

    def pins(package: dict[str, Any], key: str) -> set[tuple[str, str]]:
        return {(m["id"], m["version"]) for m in package[key]}

    for key in ("members", "entrypoints"):
        gone, added = pins(v63, key) - pins(v64, key), pins(v64, key) - pins(v63, key)
        assert gone == {(fid, "v1") for fid in FIELDS}, key
        assert added == {(fid, "v2") for fid in FIELDS}, key
    for key in ("input_bindings", "admitted_schemas", "composition_obligations", "conflict_semantics", "scope"):
        assert v64[key] == v63[key], key
    assert len(v64["members"]) == len(v63["members"])


def test_registry_v62_only_adds_and_names_the_package_checksum() -> None:
    v61 = json.loads(REGISTRY_V61.read_text(encoding="utf-8"))
    v62 = json.loads(REGISTRY_V62.read_text(encoding="utf-8"))
    for key, added in (
        ("citizens", {(fid, "v2") for fid in FIELDS}),
        ("packages", {(P + "package.core-calculations", "v64")}),
    ):
        old = {(r["id"], r["version"]): r["checksum"] for r in v61[key]}
        new = {(r["id"], r["version"]): r["checksum"] for r in v62[key]}
        assert {k: v for k, v in new.items() if k in old} == old, key
        assert set(new) - set(old) == added, key
    package = json.loads(PACKAGE_V64.read_text(encoding="utf-8"))
    packages = {(r["id"], r["version"]): r["checksum"] for r in v62["packages"]}
    assert packages[(package["id"], "v64")] == package["package_checksum"]
    citizens = {(r["id"], r["version"]): r["checksum"] for r in v62["citizens"]}
    for fid, (_, stem) in FIELDS.items():
        body = json.loads((CONTENT / f"{stem}.form-field.v2.json").read_text(encoding="utf-8"))
        assert citizens[(fid, "v2")] == citizen_checksum(body)


def test_release_v62_names_registry_v62() -> None:
    release = json.loads(RELEASE_V62.read_text(encoding="utf-8"))
    assert release["version"] == "v62"
    assert release["package_registry_sha256"] == hashlib.sha256(REGISTRY_V62.read_bytes()).hexdigest()
    earlier = json.loads(RELEASE_V61.read_text(encoding="utf-8"))
    assert release["package_registry_sha256"] != earlier["package_registry_sha256"]


def test_v64_shares_v63_companion_declaration() -> None:
    declarations = domain_package_companion_declarations()
    pkg = P + "package.core-calculations"
    assert declarations[(pkg, "v64")] == declarations[(pkg, "v63")]


# --- the copy-check as a regression test ------------------------------------------------


def test_copy_check_is_clean_on_the_latest_core_package() -> None:
    survey = _survey()
    assert survey.survey(PACKAGE_V64) == []


def test_corrected_descriptions_cover_both_credits_the_gates_and_part_ii_b() -> None:
    line19 = _read("form1040.line-19", "v2")["description"]
    assert "child tax credit and the credit for other dependents" in line19
    line14 = _read("form.sch8812.line-14", "v2")["description"]
    assert "never below zero" in line14 and "filer and spouse gates" in line14
    line28 = _read("form1040.line-28", "v2")["description"]
    assert "three or more children" in line28 and "line 20 is below line 17" in line28


def test_copy_check_flags_a_whole_text_copy_that_names_no_line() -> None:
    """Line 14's non-published texts planted on line 19 name line 14, a line line 19's
    description also names, so the name-based check alone accepts them. The shared-text check
    catches them; a generic allowlisted phrase shared by two fields is not flagged."""
    survey = _survey()
    package = json.loads(PACKAGE_V64.read_text(encoding="utf-8"))
    fields = survey.form_fields(package)
    assert survey.shared_texts(fields) == []
    line14, line19 = (fields[(fid, "v2")] for fid in (P + "form.sch8812.line-14", P + "form1040.line-19"))
    planted = copy.deepcopy(line19)
    for code in ("blocked", "closure_backed_zero", "computed_zero", "guard_inapplicable"):
        planted["dispositions"][code]["explain"] = line14["dispositions"][code]["explain"]
    swapped = dict(fields)
    swapped[(P + "form1040.line-19", "v2")] = planted
    flagged = survey.shared_texts(swapped)
    assert {tuple(row["fields"]) for row in flagged} == {(P + "form.sch8812.line-14", P + "form1040.line-19")}
    assert len(flagged) == 4
    # a text that names no line and is shared by two fields is flagged unless it is allowlisted
    generic = copy.deepcopy(line19)
    generic["dispositions"]["blocked"]["explain"] = "Something went wrong."
    other = copy.deepcopy(line14)
    other["dispositions"]["blocked"]["explain"] = "Something went wrong."
    assert len(survey.shared_texts({("a", "v1"): generic, ("b", "v1"): other})) == 1
    other["dispositions"]["blocked"]["explain"] = generic["dispositions"]["blocked"]["explain"] = "Blocked."
    assert survey.shared_texts({("a", "v1"): generic, ("b", "v1"): other}) == []


def test_copy_check_finds_the_seven_on_v63() -> None:
    survey = _survey()
    assert {row["id"] for row in survey.survey(PACKAGE_V63)} - {"(shared text)"} == set(FIELDS)


# --- a saved presentation ----------------------------------------------------------------


@pytest.mark.parametrize("closed", [True, False], ids=["published", "blocked"])
def test_saved_presentation_shows_the_corrected_text_on_v64_and_the_old_on_v63(closed: bool) -> None:
    for core, expected_version in (("v64", "v2"), ("v63", "v1")):
        model, run = _present(core, closed)
        fields = _embedded_fields(model, {})
        for fid in (P + "form1040.line-19", P + "form1040.line-28"):
            assert fields[fid], (core, fid)
            line, _ = FIELDS[fid]
            for field in fields[fid]:
                assert field["version"] == expected_version
                texts = _texts(field)
                if core == "v64":
                    assert all(line in t for t in texts.values()), texts
                    assert not any("earned income credit" in t.lower() for t in texts.values())
                else:
                    assert texts["blocked"] == "Earned income credit is blocked because an input it needs is missing or invalid."
        if closed:
            assert SYMBOL_19 in run["pubs"] and SYMBOL_28 in run["pubs"]
        else:
            assert SYMBOL_19 not in run["pubs"] and SYMBOL_28 not in run["pubs"]
            assert P + "rule.ctc-form1040-line19" in run["blocked"]


def test_every_published_value_is_identical_on_v63_and_v64() -> None:
    _, v63 = _present("v63", True)
    _, v64 = _present("v64", True)
    assert set(v63["pubs"]) == set(v64["pubs"])
    for symbol, finding in v63["pubs"].items():
        assert finding["value"] == v64["pubs"][symbol]["value"], symbol
    assert [Decimal(str(v64["pubs"][s]["value"])) for s in (SYMBOL_19, P + "payments.line27a", SYMBOL_28)] == [
        Decimal(1475), Decimal(3261), Decimal(725)]
    assert v63["blocked"] == v64["blocked"]
