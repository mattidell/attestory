"""Track 1: the collect guards on core v62, on the real coordinator.

Runs go through ``live_coordinate_run`` on the committed packages (core v61 and
v62). On v61 a recorded member of a source set counts on its bound lines whether
or not the family closure is answered; v62 blocks the guarded rule
``SOURCE_SET_UNCLOSED`` instead, and the lines behind it wait. Answering the
closure gives v62 exactly v61's values.

Seven gaps are closed by five successor rules: Form 1099-DIV box 2a, the Form
1099-R line 4b subtotal, Form SSA-1099 line 6a, and the four non-wash Form
1099-B basis and proceeds sets (Schedule D lines 1a and 8a). The nine interest
sets behind line 2b are a known gap that v62 does not close (line 2b v8 validator
restriction, owner-held): their cases pin that the partial sum still publishes,
so a later fix flips those tests deliberately. Synthetic ``demo.*`` data only.
"""

from __future__ import annotations

import copy
import functools
import glob
import json
import re
from pathlib import Path
from typing import Any

import pytest

from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.facts import fact_id_for
from packages.tax.loader import domain_package_companion_declarations
from tests.test_form_1099_k_income import _handover, _run_finished, _values
from tests.test_form_1099_withholding import (
    CONTENT,
    RELEASE_DIR,
    YEAR,
    _add,
    _assert,
    _base,
    _close,
    _introduce,
    _retirements,
    _social_security,
    _social_security_withholding,
    _unemployment_withholding,
)
from tests.test_refund_or_amount_owed_track1 import _attested, _finish
from tests.test_withholding_closure import (
    PACKAGE_V61,
    RELEASE_V59,
    SURFACE_V61,
    _horizons,
    _strip_closure,
)

PACKAGE_V62 = CONTENT / "package.core-calculations.v62.json"
RELEASE_V60 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v60.json"
SURFACE_V62 = PublicationSurface(RELEASE_DIR, CONTENT / "published-packages.v60.json", CONTENT)
PACKAGE_V63 = CONTENT / "package.core-calculations.v63.json"
RELEASE_V61 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v61.json"
SURFACE_V63 = PublicationSurface(RELEASE_DIR, CONTENT / "published-packages.v61.json", CONTENT)
P = "tax.us.2025."

CORES = {
    "v61": (PACKAGE_V61, RELEASE_V59, "v59", SURFACE_V61),
    "v62": (PACKAGE_V62, RELEASE_V60, "v60", SURFACE_V62),
    "v63": (PACKAGE_V63, RELEASE_V61, "v61", SURFACE_V63),
}

SUCCESSORS = {
    "tax.us.2025.rule.f1099div-2a-subtotal": ("v1", "v2"),
    "tax.us.2025.rule.f1099r-ira-fully-taxable-subtotal": ("v3", "v4"),
    "tax.us.2025.rule.form1040-line6a": ("v1", "v2"),
    "tax.us.2025.rule.schedule-d-line8a-gain": ("v2", "v3"),
    "tax.us.2025.rule.schedule-d-line1a-gain": ("v1", "v2"),
}


# --- running -------------------------------------------------------------------


def _run_on(acts: list[dict[str, object]], run_id: str, core: str, *, reconfirm: bool = True) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    package, release, rel_version, surface = CORES[core]
    finished = _finish(
        copy.deepcopy(acts), package_path=package, package_version=core,
        release_path=release, release_version=rel_version, note=run_id,
    )
    finished = _handover(finished, surface=surface, reconfirm=reconfirm)
    return _run_finished(finished, run_id, surface)


class Result:
    def __init__(self, pubs: dict[str, Any], blocked: list[dict[str, Any]]) -> None:
        self.pubs, self.blocked = pubs, blocked
        self.values = _values(pubs)

    def has(self, line: str) -> bool:
        return P + line in self.pubs

    def value(self, line: str) -> float:
        return float(self.values[P + line])

    def unclosed(self) -> list[tuple[str, tuple[str, ...]]]:
        return sorted(
            (str(r["artifact_id"]).split("rule.")[-1], tuple(str(m) for m in r["missing"]))
            for r in self.blocked if r["code"] == "SOURCE_SET_UNCLOSED"
        )


# --- the committed package, as the P0 probe read it ----------------------------


@functools.lru_cache(maxsize=1)
def _package_index() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    pkg = json.loads(PACKAGE_V61.read_text())
    idx: dict[tuple[str, str], dict[str, Any]] = {}
    for name in glob.glob(str(CONTENT / "*.json")):
        try:
            body = json.loads(Path(name).read_text())
        except ValueError:
            continue
        if isinstance(body, dict) and "id" in body and "version" in body:
            idx[(body["id"], body["version"])] = body
    members = [idx[(m["id"], m["version"])] for m in pkg["members"]]
    families = {m["id"]: m for m in members if str(m.get("schema", "")).startswith("source-family")}
    mappings = {m["family"]["id"]: m for m in members if str(m.get("schema", "")).startswith("source-closure-mapping")}
    fact_types: dict[str, Any] = {}
    bundles: dict[str, Any] = {}
    for m in pkg["members"]:
        if m["role"] == "fact-type-bundle":
            bundle = idx[(m["id"], m["version"])]
            for ft in bundle["fact_types"]:
                fact_types[ft["id"]] = ft
                bundles[ft["id"]] = bundle
    return families, mappings, fact_types, bundles


def _base_return() -> list[dict[str, object]]:
    acts = _base(wages=50000.0, w2_withheld=4500.0)
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])
    return acts


def _adopt(acts: list[dict[str, object]], type_id: str) -> None:
    _, _, _, bundles = _package_index()
    adopted = {t["id"] for a in acts if a["kind"] == "bundle-adoption" for t in a["payload"]["bundle"]["fact_types"]}  # type: ignore[index]
    if type_id not in adopted and type_id in bundles:
        _add(acts, "bundle-adoption", {"bundle": bundles[type_id]})


def _add_member(acts: list[dict[str, object]], family: str, value: float, *, close: bool, tag: str) -> list[dict[str, object]]:
    """One member of ``family`` by member-transition; the family closure attested true at the
    resulting horizon when ``close``, otherwise left unanswered."""
    families, mappings, fact_types, _ = _package_index()
    fam, mapping = families[family], mappings[family]
    ftype = fact_types[fam["member_predicate"]["fact_type"]]
    out = _strip_closure(acts, mapping["closure_fact_type"]["id"])
    _adopt(out, ftype["id"])
    _adopt(out, mapping["closure_fact_type"]["id"])
    horizons = _horizons(out, family)
    if not horizons:
        genesis = f"demo.cc.{tag}.g0"
        _add(out, "horizon-genesis", {"family": {"id": family, "version": fam["version"]},
                                      "scope": {"tax-year": YEAR, "subject": "demo.primary"}, "horizon_id": genesis})
        horizons = [genesis]
    declared: list[tuple[str, str]] = []
    for key in ftype["identity_keys"]:
        if key["kind"] == "entity":
            eid = f"demo.cc.{tag}.{key['name']}"
            _introduce(out, eid, key["entity_kind"])
            declared.append((key["name"], eid))
        else:
            declared.append((key["name"], key["values"][0]))
    new = f"demo.cc.{tag}.h1"
    _add(out, "member-transition", {
        "family": {"id": family, "version": fam["version"]},
        "scope": {"tax-year": YEAR, "subject": "demo.primary"},
        "member": {"action": "assert", "finding": _attested(f"demo.cc.{tag}.member", fact_id_for(ftype["id"], tuple(declared)), value)},
        "successor": {"id": new, "predecessor": horizons[-1]},
    })
    if close:
        _close(out, mapping["closure_fact_type"]["id"], new, f"demo.cc.{tag}.closure")
    return out


def _gap_return(family: str, *, close: bool) -> list[dict[str, object]]:
    """The withholding-closure base return plus one 1,000 member of ``family`` (10,000 for the
    1099-R line 4b family and 12,000 for the SSA-1099 benefits family)."""
    _, mappings, _, _ = _package_index()
    acts = _base_return()
    if family == P + "f1099r.ira-fully-taxable":
        acts = _strip_closure(_strip_closure(acts, mappings[family]["closure_fact_type"]["id"]),
                              mappings[P + "f1099r.box4"]["closure_fact_type"]["id"])
        _retirements(acts, [(10000.0, None)])
    elif family == P + "ssa1099.benefits":
        _social_security(acts, [12000.0], witness=None)
    else:
        return _add_member(acts, family, 1000.0, close=close, tag=family.split(".")[-1])
    return acts if close else _strip_closure(acts, mappings[family]["closure_fact_type"]["id"])


def _run(acts: list[dict[str, object]], run_id: str, core: str, *, reconfirm: bool = True) -> Result:
    """A member refused for contradicting a base "none" declaration has that declaration
    removed and is rerun (both cores alike)."""
    for _ in range(5):
        try:
            return Result(*_run_on(acts, run_id, core, reconfirm=reconfirm))
        except Exception as exc:
            match = re.search(r"contradiction: (\S+) is currently", str(exc))
            if not match:
                raise
            acts = _strip_closure(acts, match.group(1))
    raise AssertionError("too many declaration removals")


@functools.lru_cache(maxsize=None)
def _case(family: str, answered: bool, core: str) -> Result:
    # Only the SSA-1099 benefits family's unanswered closure needs the harness's automatic
    # reconfirmation after the handover switched off.
    reconfirm = answered or family != P + "ssa1099.benefits"
    tag = family.replace(P, "").replace(".", "-")
    return _run(_gap_return(family, close=answered), f"demo.cc.{tag}.{'a' if answered else 'u'}.{core}", core, reconfirm=reconfirm)


@functools.lru_cache(maxsize=None)
def _base_result(core: str) -> Result:
    return _run(_base_return(), f"demo.cc.base.{core}", core)


# --- the seven gaps v62 closes --------------------------------------------------

# family -> (rule that blocks on v62, {bound line: value v61 publishes unanswered})
GAPS: dict[str, tuple[str, dict[str, float]]] = {
    P + "f1099div.2a": ("f1099div-2a-subtotal", {
        "dividends.2a-subtotal": 1000.0, "income.agi": 51000.0, "schedule-d.line-15": 1000.0}),
    P + "f1099r.ira-fully-taxable": ("f1099r-ira-fully-taxable-subtotal", {
        "ira.distributions.line4b": 10000.0, "income.agi": 60000.0}),
    P + "ssa1099.benefits": ("form1040-line6a", {"social-security.line6a": 12000.0}),
    P + "f1099b.covered-lt-basis": ("schedule-d-line8a-gain", {
        "schedule-d.line-8a-gain": -1000.0, "schedule-d.line-15": -1000.0, "schedule-d.line-21": 1000.0}),
    P + "f1099b.covered-lt-proceeds": ("schedule-d-line8a-gain", {
        "schedule-d.line-8a-gain": 1000.0, "income.agi": 51000.0, "capital-gains.line7a-total": 1000.0}),
    P + "f1099b.covered-st-basis": ("schedule-d-line1a-gain", {
        "schedule-d.line-1a-gain": -1000.0, "schedule-d.line-7": -1000.0, "schedule-d.line-21": 1000.0}),
    P + "f1099b.covered-st-proceeds": ("schedule-d-line1a-gain", {
        "schedule-d.line-1a-gain": 1000.0, "income.agi": 51000.0, "capital-gains.line7a-total": 1000.0}),
}


@pytest.mark.parametrize("family", sorted(GAPS))
def test_v61_publishes_the_partial_sum(family: str) -> None:
    _, lines = GAPS[family]
    result = _case(family, False, "v61")
    for line, expected in lines.items():
        assert result.has(line), (family, line)
        assert result.value(line) == expected, (family, line)


@pytest.mark.parametrize("family", sorted(GAPS))
def test_v62_blocks_unclosed_and_the_lines_behind_wait(family: str) -> None:
    rule, lines = GAPS[family]
    result = _case(family, False, "v62")
    assert any(r == rule and family in missing for r, missing in result.unclosed()), result.unclosed()
    for line in lines:
        assert not result.has(line), (family, line)


@pytest.mark.parametrize("family", sorted(GAPS))
def test_answering_the_closure_gives_v61_values_on_v62(family: str) -> None:
    v61, v62 = _case(family, True, "v61"), _case(family, True, "v62")
    assert v61.blocked == [] and v62.blocked == []
    assert v62.values == v61.values
    base = _base_result("v61")
    _, lines = GAPS[family]
    assert any(v62.value(line) != float(base.values.get(P + line, 0)) for line in lines)


# --- the nine interest gaps: known, parked ---------------------------------------

# Known gap on v62, closed on v63. Line 2b v8 has when=true and cannot be given a guard, so
# core v63 guards the subtotal rules it reads instead (tests/test_attachment_closure.py pins
# line 2b blocking on v63). These nine still publish a partial taxable-interest total on v62,
# which stays pinned here as history.
INTEREST_GAPS = {
    "f1099int.b1": 1000.0, "f1099int.b3": 1000.0, "f1099oid.b1": 1000.0, "non-form-interest": 1000.0,
    "form1065-k1.box5": 1000.0, "f1099int.b10": 1000.0, "f1099oid.b5": 1000.0,
    "scheduleb.adjustment.nominee": -1000.0, "scheduleb.adjustment.abp-adjustment": -1000.0,
}


@pytest.mark.parametrize("suffix", sorted(INTEREST_GAPS))
def test_known_gap_interest_set_still_publishes_a_partial_sum_on_v62(suffix: str) -> None:
    family = P + suffix
    result = _case(family, False, "v62")
    assert result.has("interest.taxable-total"), suffix
    base = _base_result("v62")
    assert result.value("interest.taxable-total") == float(base.values[P + "interest.taxable-total"]) + INTEREST_GAPS[suffix], suffix
    assert result.has("income.agi"), suffix


def test_known_gap_schedule_d_attachment_still_publishes_the_partial_amount_on_v62() -> None:
    """Known gap: attachment.schedule-d reads the covered subtotals directly, so with one
    long-term proceeds member and the closure unanswered, line 8a blocks while
    schedule-d.disposition (the attachment's itemization) still publishes the partial
    1,000. Core v63 guards the subtotal rule so the attachment waits too
    (tests/test_attachment_closure.py); v62 stays pinned here as history."""
    result = _case(P + "f1099b.covered-lt-proceeds", False, "v62")
    assert not result.has("schedule-d.line-8a-gain")
    assert result.has("schedule-d.disposition")
    disposition = result.pubs[P + "schedule-d.disposition"]["value"]
    assert disposition["required"] is True
    sets = {rs["source_family"]["id"]: rs["subtotal"]["value"]
            for part in disposition["itemizations"] for rs in part["row_sets"]}
    assert float(sets[P + "f1099b.covered-lt-proceeds"]) == 1000.0


# --- a complete return ------------------------------------------------------------


def _complete_return() -> list[dict[str, object]]:
    """Interest, dividends, a 1099-R, an SSA-1099 and 1099-B sales, every family closed."""
    families, mappings, _, _ = _package_index()
    acts = _base_return()
    acts = _strip_closure(acts, mappings[P + "f1099r.ira-fully-taxable"]["closure_fact_type"]["id"])
    acts = _strip_closure(acts, mappings[P + "f1099r.box4"]["closure_fact_type"]["id"])
    _retirements(acts, [(10000.0, None)])
    _social_security(acts, [12000.0], witness=None)
    for suffix in ("f1099int.b1", "f1099div.2a", "f1099b.covered-lt-basis", "f1099b.covered-lt-proceeds",
                   "f1099b.covered-st-basis", "f1099b.covered-st-proceeds"):
        acts = _add_member(acts, P + suffix, 1000.0, close=True, tag="cr" + suffix.replace(".", "-"))
    return acts


def test_complete_return_publishes_identically_on_v61_and_v62() -> None:
    v61 = _run(_complete_return(), "demo.cc.complete.v61", "v61")
    v62 = _run(_complete_return(), "demo.cc.complete.v62", "v62")
    assert v61.blocked == [] and v62.blocked == []
    assert v62.values == v61.values
    for line in ("interest.taxable-total", "dividends.2a-subtotal", "ira.distributions.line4b",
                 "social-security.line6a", "schedule-d.line-1a-gain", "schedule-d.line-8a-gain", "income.agi"):
        assert v62.has(line), line


# --- the package chain --------------------------------------------------------------


def _citizens(name: str) -> dict[tuple[str, str], str]:
    body = json.loads((CONTENT / name).read_text())
    return {(c["id"], c["version"]): c["checksum"] for c in body["citizens"]}


def test_registry_v60_only_adds_the_five_successors() -> None:
    old, new = _citizens("published-packages.v59.json"), _citizens("published-packages.v60.json")
    assert set(old) <= set(new)
    assert all(new[key] == old[key] for key in old)
    assert set(new) - set(old) == {(rid, to) for rid, (_, to) in SUCCESSORS.items()}


def test_core_v62_differs_from_v61_only_in_the_five_members() -> None:
    v61, v62 = json.loads(PACKAGE_V61.read_text()), json.loads(PACKAGE_V62.read_text())
    assert v62["version"] == "v62"
    old = {(m["id"], m["version"]) for m in v61["members"]}
    new = {(m["id"], m["version"]) for m in v62["members"]}
    assert old - new == {(rid, frm) for rid, (frm, _) in SUCCESSORS.items()}
    assert new - old == {(rid, to) for rid, (_, to) in SUCCESSORS.items()}
    assert v62["input_bindings"] == v61["input_bindings"]
    assert v62["admitted_schemas"] == v61["admitted_schemas"]
    entry_old = {(e["id"], e["version"]) for e in v61["entrypoints"]}
    entry_new = {(e["id"], e["version"]) for e in v62["entrypoints"]}
    assert entry_new - entry_old <= {(rid, to) for rid, (_, to) in SUCCESSORS.items()}
    assert len(entry_old - entry_new) == len(entry_new - entry_old) == 4
    line2b = [m for m in v62["members"] if m["id"] == P + "rule.form1040-line2b"]
    assert line2b == [m for m in v61["members"] if m["id"] == P + "rule.form1040-line2b"]


def test_v62_shares_the_v61_companion_declaration() -> None:
    declarations = domain_package_companion_declarations()
    core = P + "package.core-calculations"
    assert declarations[(core, "v62")] == declarations[(core, "v61")]
