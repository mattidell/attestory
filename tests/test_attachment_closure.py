"""Track 1: attachments wait for their statements, on core v63 (runs go through
``live_coordinate_run``).

On core v62 an attachment publishes the amount of a recorded member whether or not the family
closure is answered: ``attempt_attachment`` reads rows straight from the members and waits only
for an absent subtotal symbol. Core v63 guards the 13 subtotal rules the attachments read (the
four non-wash Form 1099-B sets on Schedule D, the six wash-sale sets on Form 8949, Form 1099-G
box 1 on Schedule 1, and the nominee and ABP adjustments on Schedule B) and the seven positive
interest subtotals, so the subtotal blocks ``SOURCE_SET_UNCLOSED`` and every reader waits:
the attachment and line 2b. Answering the closure gives v63 exactly v62's values. Synthetic
``demo.*`` data only.
"""

from __future__ import annotations

import functools
import json
from typing import Any

import pytest

from packages.kernel.facts import fact_id_for
from packages.tax.loader import domain_package_companion_declarations
from tests.test_collect_closure import (
    INTEREST_GAPS,
    PACKAGE_V62,
    PACKAGE_V63,
    P,
    Result,
    _adopt,
    _add_member,
    _base_result,
    _base_return,
    _case,
    _package_index,
    _run,
)
from tests.test_form_1099_withholding import CONTENT, YEAR, _add, _assert, _close, _introduce
from tests.test_refund_or_amount_owed_track1 import _attested
from tests.test_withholding_closure import _horizons, _strip_closure

# --- the 20 successors ------------------------------------------------------------------

SUCCESSORS: dict[str, tuple[str, str]] = {
    P + "rule." + name: pins for name, pins in {
        "f1099b-covered-lt-basis-subtotal": ("v1", "v2"),
        "f1099b-covered-lt-proceeds-subtotal": ("v1", "v2"),
        "f1099b-covered-st-basis-subtotal": ("v1", "v2"),
        "f1099b-covered-st-proceeds-subtotal": ("v1", "v2"),
        "f1099b-covered-w-lt-adjustment-subtotal": ("v2", "v3"),
        "f1099b-covered-w-lt-basis-subtotal": ("v2", "v3"),
        "f1099b-covered-w-lt-proceeds-subtotal": ("v2", "v3"),
        "f1099b-covered-w-st-adjustment-subtotal": ("v2", "v3"),
        "f1099b-covered-w-st-basis-subtotal": ("v2", "v3"),
        "f1099b-covered-w-st-proceeds-subtotal": ("v2", "v3"),
        "f1099g-1-subtotal": ("v1", "v2"),
        "scheduleb-adjustment.nominee-subtotal": ("v1", "v2"),
        "scheduleb-adjustment.abp-adjustment-subtotal": ("v1", "v2"),
        "f1099int-b1-subtotal": ("v1", "v2"),
        "f1099int-b3-subtotal": ("v1", "v2"),
        "f1099int-b10-subtotal": ("v1", "v2"),
        "f1099oid-subtotal": ("v1", "v2"),
        "f1099oid-b5-subtotal": ("v1", "v2"),
        "form1065-k1-box5-subtotal": ("v1", "v2"),
        "non-form-interest-subtotal": ("v1", "v2"),
    }.items()
}
ENTRYPOINTS = {
    P + "rule." + n for n in (
        "f1099b-covered-w-lt-adjustment-subtotal", "f1099b-covered-w-lt-basis-subtotal",
        "f1099b-covered-w-lt-proceeds-subtotal", "f1099b-covered-w-st-adjustment-subtotal",
        "f1099b-covered-w-st-basis-subtotal", "f1099b-covered-w-st-proceeds-subtotal", "f1099g-1-subtotal",
    )
}

# --- the 13 attachment gaps --------------------------------------------------------------

# set under test -> (closed trigger family or None, trigger amount, attachment symbol,
#                    part id of the amount, subtotal rule that blocks on v63)
ATTACHMENT_GAPS: dict[str, tuple[str | None, float, str, str, str]] = {
    "f1099b.covered-lt-proceeds": (None, 0.0, "schedule-d.disposition", "line-8a-proceeds", "f1099b-covered-lt-proceeds-subtotal"),
    "f1099b.covered-st-proceeds": (None, 0.0, "schedule-d.disposition", "line-1a-proceeds", "f1099b-covered-st-proceeds-subtotal"),
    "f1099b.covered-lt-basis": ("f1099b.covered-lt-proceeds", 1000.0, "schedule-d.disposition", "line-8a-basis", "f1099b-covered-lt-basis-subtotal"),
    "f1099b.covered-st-basis": ("f1099b.covered-st-proceeds", 1000.0, "schedule-d.disposition", "line-1a-basis", "f1099b-covered-st-basis-subtotal"),
    "f1099b.covered-w-lt-proceeds": (None, 0.0, "form8949.disposition", "box-d-proceeds", "f1099b-covered-w-lt-proceeds-subtotal"),
    "f1099b.covered-w-st-proceeds": (None, 0.0, "form8949.disposition", "box-a-proceeds", "f1099b-covered-w-st-proceeds-subtotal"),
    "f1099b.covered-w-lt-basis": ("f1099b.covered-w-lt-proceeds", 1000.0, "form8949.disposition", "box-d-basis", "f1099b-covered-w-lt-basis-subtotal"),
    "f1099b.covered-w-lt-adjustment": ("f1099b.covered-w-lt-proceeds", 1000.0, "form8949.disposition", "box-d-adjustment", "f1099b-covered-w-lt-adjustment-subtotal"),
    "f1099b.covered-w-st-basis": ("f1099b.covered-w-st-proceeds", 1000.0, "form8949.disposition", "box-a-basis", "f1099b-covered-w-st-basis-subtotal"),
    "f1099b.covered-w-st-adjustment": ("f1099b.covered-w-st-proceeds", 1000.0, "form8949.disposition", "box-a-adjustment", "f1099b-covered-w-st-adjustment-subtotal"),
    "f1099g.1": (None, 0.0, "schedule1.disposition", "line-7-unemployment", "f1099g-1-subtotal"),
    "scheduleb.adjustment.nominee": ("f1099int.b1", 2000.0, "scheduleb.disposition", "nominee_distribution", "scheduleb-adjustment.nominee-subtotal"),
    "scheduleb.adjustment.abp-adjustment": ("f1099int.b1", 2000.0, "scheduleb.disposition", "abp_adjustment", "scheduleb-adjustment.abp-adjustment-subtotal"),
}


def _boundary_form8949(acts: list[dict[str, object]]) -> None:
    """The Form 8949 Part III answer a wash-sale return needs for Form 8949 to publish."""
    ftid = P + "schedule-d-boundary.no-other-form8949-adjustments"
    _adopt(acts, ftid)
    _assert(acts, "demo.ac.boundary.8949", ftid, (), "yes")


def _gap_acts(suffix: str, *, close: bool) -> list[dict[str, object]]:
    trigger, amount, _, _, _ = ATTACHMENT_GAPS[suffix]
    tag = suffix.replace(".", "-")
    acts = _base_return()
    if suffix.startswith("f1099b.covered-w-"):
        _boundary_form8949(acts)
    if trigger is not None:
        acts = _add_member(acts, P + trigger, amount, close=True, tag="t" + trigger.replace(".", "-"))
    return _add_member(acts, P + suffix, 1000.0, close=close, tag=tag)


@functools.lru_cache(maxsize=None)
def _attachment_case(suffix: str, answered: bool, core: str) -> Result:
    tag = suffix.replace(".", "-")
    return _run(_gap_acts(suffix, close=answered), f"demo.ac.{tag}.{'a' if answered else 'u'}.{core}", core)


def _parts(result: Result, symbol: str) -> dict[str, float]:
    """part id (or adjustment kind) -> the row sum an attachment itemizes, summed over the
    part's row sets; empty when the attachment is not published."""
    pub = result.pubs.get(P + symbol)
    if pub is None:
        return {}
    out: dict[str, float] = {}
    for part in pub["value"]["itemizations"]:
        for rs in part["row_sets"]:
            out[part["part_id"]] = out.get(part["part_id"], 0.0) + float(rs["row_sum"])
        for adj in part.get("adjustment_rows", []):
            out[adj["kind"]] = out.get(adj["kind"], 0.0) + float(adj["row_sum"])
    return out


@pytest.mark.parametrize("suffix", sorted(ATTACHMENT_GAPS))
def test_v62_publishes_the_partial_amount_on_the_attachment(suffix: str) -> None:
    _, _, symbol, part, _ = ATTACHMENT_GAPS[suffix]
    assert _parts(_attachment_case(suffix, False, "v62"), symbol).get(part) == 1000.0


@pytest.mark.parametrize("suffix", sorted(ATTACHMENT_GAPS))
def test_v63_does_not_publish_it_and_the_subtotal_blocks_unclosed(suffix: str) -> None:
    _, _, symbol, part, rule = ATTACHMENT_GAPS[suffix]
    result = _attachment_case(suffix, False, "v63")
    assert part not in _parts(result, symbol), (suffix, _parts(result, symbol))
    assert any(r == rule and P + suffix in missing for r, missing in result.unclosed()), result.unclosed()


@pytest.mark.parametrize("suffix", sorted(ATTACHMENT_GAPS))
def test_answered_closure_gives_v63_the_v62_values(suffix: str) -> None:
    _, _, symbol, part, _ = ATTACHMENT_GAPS[suffix]
    v62, v63 = _attachment_case(suffix, True, "v62"), _attachment_case(suffix, True, "v63")
    assert v62.blocked == [] and v63.blocked == []
    assert v63.values == v62.values
    assert _parts(v63, symbol).get(part) == 1000.0


# --- the nine interest sets behind line 2b -------------------------------------------------


@pytest.mark.parametrize("suffix", sorted(INTEREST_GAPS))
def test_v62_publishes_a_partial_line_2b_and_v63_blocks_it(suffix: str) -> None:
    family = P + suffix
    v62, v63 = _case(family, False, "v62"), _case(family, False, "v63")
    base = _base_result("v62")
    assert v62.value("interest.taxable-total") == float(base.values[P + "interest.taxable-total"]) + INTEREST_GAPS[suffix]
    assert not v63.has("interest.taxable-total"), suffix
    assert any(family in missing for _, missing in v63.unclosed()), v63.unclosed()


@pytest.mark.parametrize("suffix", sorted(INTEREST_GAPS))
def test_answered_interest_closure_gives_v63_the_v62_values(suffix: str) -> None:
    family = P + suffix
    v62, v63 = _case(family, True, "v62"), _case(family, True, "v63")
    assert v62.blocked == [] and v63.blocked == []
    assert v63.values == v62.values
    assert v63.has("interest.taxable-total")


# --- a stale closure and a closure attested false ----------------------------------------------


def _later_member(acts: list[dict[str, object]], family: str, value: float, tag: str) -> list[dict[str, object]]:
    """One more member after the family's current horizon, leaving any closure attested at the
    earlier horizon where it is (so that closure is stale)."""
    families, _, fact_types, _ = _package_index()
    fam = families[family]
    ftype = fact_types[fam["member_predicate"]["fact_type"]]
    out = list(acts)
    declared: list[tuple[str, str]] = []
    for key in ftype["identity_keys"]:
        if key["kind"] == "entity":
            eid = f"demo.ac.{tag}.{key['name']}"
            _introduce(out, eid, key["entity_kind"])
            declared.append((key["name"], eid))
        else:
            declared.append((key["name"], key["values"][0]))
    _add(out, "member-transition", {
        "family": {"id": family, "version": fam["version"]},
        "scope": {"tax-year": YEAR, "subject": "demo.primary"},
        "member": {"action": "assert", "finding": _attested(f"demo.ac.{tag}.member", fact_id_for(ftype["id"], tuple(declared)), value)},
        "successor": {"id": f"demo.ac.{tag}.h2", "predecessor": _horizons(out, family)[-1]},
    })
    return out


def _closure_variant(suffix: str, kind: str) -> list[dict[str, object]]:
    family = P + suffix
    _, mappings, _, _ = _package_index()
    closure = mappings[family]["closure_fact_type"]["id"]
    tag = "v" + suffix.replace(".", "-")
    if kind == "stale":
        acts = _add_member(_base_return(), family, 1000.0, close=True, tag=tag)
        return _later_member(acts, family, 1000.0, tag + "-2")
    acts = _add_member(_base_return(), family, 1000.0, close=False, tag=tag)
    horizon = _horizons(acts, family)[-1]
    _add(acts, "assertion", {"finding": _attested(f"demo.ac.{tag}.closure-false", f"{closure}|family-horizon={horizon},tax-year={YEAR}", False)})
    return acts


@pytest.mark.parametrize("kind", ["stale", "false"])
@pytest.mark.parametrize("suffix", ["f1099b.covered-lt-proceeds", "f1099g.1"])
def test_stale_or_false_closure_keeps_the_attachment_waiting_on_v63(suffix: str, kind: str) -> None:
    _, _, symbol, part, rule = ATTACHMENT_GAPS[suffix]
    v62 = _run(_closure_variant(suffix, kind), f"demo.ac.{kind}.{suffix}.v62", "v62")
    v63 = _run(_closure_variant(suffix, kind), f"demo.ac.{kind}.{suffix}.v63", "v63")
    assert _parts(v62, symbol).get(part, 0.0) >= 1000.0, (suffix, kind)
    assert part not in _parts(v63, symbol), (suffix, kind)
    assert any(r == rule and P + suffix in missing for r, missing in v63.unclosed()), v63.unclosed()


@pytest.mark.parametrize("kind", ["stale", "false"])
def test_stale_or_false_interest_closure_blocks_line_2b_on_v63(kind: str) -> None:
    v62 = _run(_closure_variant("f1099int.b1", kind), f"demo.ac.{kind}.int.v62", "v62")
    v63 = _run(_closure_variant("f1099int.b1", kind), f"demo.ac.{kind}.int.v63", "v63")
    assert v62.has("interest.taxable-total") and v62.has("income.agi")
    assert not v63.has("interest.taxable-total") and not v63.has("income.agi")


# --- a complete return ----------------------------------------------------------------------


def _complete_return() -> list[dict[str, object]]:
    """Schedule B, Schedule D, Form 8949 and Schedule 1 all required, every family closed."""
    acts = _base_return()
    _boundary_form8949(acts)
    for suffix, amount in (
        ("f1099int.b1", 2000.0), ("scheduleb.adjustment.nominee", 1000.0),
        ("scheduleb.adjustment.abp-adjustment", 1000.0), ("f1099g.1", 1000.0),
        ("f1099b.covered-lt-proceeds", 1000.0), ("f1099b.covered-lt-basis", 1000.0),
        ("f1099b.covered-st-proceeds", 1000.0), ("f1099b.covered-st-basis", 1000.0),
        ("f1099b.covered-w-lt-proceeds", 1000.0), ("f1099b.covered-w-lt-basis", 1000.0),
        ("f1099b.covered-w-lt-adjustment", 1000.0), ("f1099b.covered-w-st-proceeds", 1000.0),
        ("f1099b.covered-w-st-basis", 1000.0), ("f1099b.covered-w-st-adjustment", 1000.0),
    ):
        acts = _add_member(acts, P + suffix, amount, close=True, tag="cr" + suffix.replace(".", "-"))
    return acts


def test_complete_return_publishes_every_value_identically_on_v62_and_v63() -> None:
    v62 = _run(_complete_return(), "demo.ac.complete.v62", "v62")
    v63 = _run(_complete_return(), "demo.ac.complete.v63", "v63")
    assert v62.blocked == v63.blocked == []
    assert v63.values == v62.values
    assert set(v63.pubs) == set(v62.pubs)
    for symbol in ("schedule-d.disposition", "form8949.disposition", "schedule1.disposition", "scheduleb.disposition"):
        assert v63.has(symbol), symbol
        assert v63.pubs[P + symbol]["value"] == v62.pubs[P + symbol]["value"], symbol


# --- the sets a guarded requirement read already holds: pinned live ---------------------------------


def _add_member_with_companion(acts: list[dict[str, object]], family: str, value: float, *, tag: str,
                               companion: str) -> list[dict[str, object]]:
    """``_add_member`` (closure left unanswered) plus a same-statement ``False`` companion asserted
    on the member's own entities, for a family whose member validation requires one."""
    families, mappings, fact_types, _ = _package_index()
    fam, mapping = families[family], mappings[family]
    ftype = fact_types[fam["member_predicate"]["fact_type"]]
    out = _strip_closure(acts, mapping["closure_fact_type"]["id"])
    for type_id in (ftype["id"], mapping["closure_fact_type"]["id"], companion):
        _adopt(out, type_id)
    horizons = _horizons(out, family)
    if not horizons:
        genesis = f"demo.ac.{tag}.g0"
        _add(out, "horizon-genesis", {"family": {"id": family, "version": fam["version"]},
                                      "scope": {"tax-year": YEAR, "subject": "demo.primary"}, "horizon_id": genesis})
        horizons = [genesis]
    declared: list[tuple[str, str]] = []
    for key in ftype["identity_keys"]:
        if key["kind"] == "entity":
            eid = f"demo.ac.{tag}.{key['name']}"
            _introduce(out, eid, key["entity_kind"])
            declared.append((key["name"], eid))
        else:
            declared.append((key["name"], key["values"][0]))
    _assert(out, f"demo.ac.{tag}.companion", companion, tuple(d for d in declared if d[0] != "tax-year"), False)
    _add(out, "member-transition", {
        "family": {"id": family, "version": fam["version"]},
        "scope": {"tax-year": YEAR, "subject": "demo.primary"},
        "member": {"action": "assert", "finding": _attested(f"demo.ac.{tag}.member", fact_id_for(ftype["id"], tuple(declared)), value)},
        "successor": {"id": f"demo.ac.{tag}.h1", "predecessor": horizons[-1]},
    })
    return out


# set -> (closed trigger or None, attachment symbol, symbol its requirement reads that is held)
HELD_BY_REQUIREMENT = {
    "f1099div.1a": (None, "scheduleb.disposition", "dividends.ordinary-total"),
    "f1099k": ("f1099g.1", "schedule1.disposition", "schedule1.top-entry"),
    "f1098e.1": ("f1099g.1", "schedule1.disposition", "schedule1.line21-sli-deduction"),
}


@functools.lru_cache(maxsize=None)
def _held_case(suffix: str, core: str) -> Result:
    trigger, _, _ = HELD_BY_REQUIREMENT[suffix]
    acts = _base_return()
    if trigger is not None:
        acts = _add_member(acts, P + trigger, 1000.0, close=True, tag="t" + trigger.replace(".", "-"))
    tag = suffix.replace(".", "-")
    if suffix == "f1098e.1":
        acts = _add_member_with_companion(acts, P + suffix, 1000.0, tag=tag, companion=P + "f1098e.box2-checked-authority")
    else:
        acts = _add_member(acts, P + suffix, 1000.0, close=False, tag=tag)
    return _run(acts, f"demo.ac.held.{tag}.{core}", core)


@pytest.mark.parametrize("suffix", sorted(HELD_BY_REQUIREMENT))
def test_held_set_publishes_no_attachment_amount_on_v63(suffix: str) -> None:
    """The attachment waits on a symbol a guarded rule holds. That is a live fact of today's
    package, not a property of the attachment: if it stops holding, this fails."""
    _, symbol, held = HELD_BY_REQUIREMENT[suffix]
    result = _held_case(suffix, "v63")
    assert not result.has(symbol), suffix
    absent = {str(m) for r in result.blocked if r["code"] == "DEPENDENCY_ABSENT" for m in r["missing"]}
    assert P + held in absent, (suffix, sorted(absent))


# --- the package chain ----------------------------------------------------------------------


def _citizens(name: str) -> dict[tuple[str, str], str]:
    body = json.loads((CONTENT / name).read_text())
    return {(c["id"], c["version"]): c["checksum"] for c in body["citizens"]}


def test_registry_v61_only_adds_the_twenty_successors() -> None:
    old, new = _citizens("published-packages.v60.json"), _citizens("published-packages.v61.json")
    assert set(old) <= set(new)
    assert all(new[key] == old[key] for key in old)
    assert set(new) - set(old) == {(rid, to) for rid, (_, to) in SUCCESSORS.items()}


def test_core_v63_differs_from_v62_only_in_the_twenty_members() -> None:
    v62: dict[str, Any] = json.loads(PACKAGE_V62.read_text())
    v63: dict[str, Any] = json.loads(PACKAGE_V63.read_text())
    assert v63["version"] == "v63"
    old = {(m["id"], m["version"]) for m in v62["members"]}
    new = {(m["id"], m["version"]) for m in v63["members"]}
    assert old - new == {(rid, frm) for rid, (frm, _) in SUCCESSORS.items()}
    assert new - old == {(rid, to) for rid, (_, to) in SUCCESSORS.items()}
    assert v63["input_bindings"] == v62["input_bindings"]
    assert v63["admitted_schemas"] == v62["admitted_schemas"]
    entry_old = {(e["id"], e["version"]) for e in v62["entrypoints"]}
    entry_new = {(e["id"], e["version"]) for e in v63["entrypoints"]}
    assert entry_old - entry_new == {(rid, SUCCESSORS[rid][0]) for rid in ENTRYPOINTS}
    assert entry_new - entry_old == {(rid, SUCCESSORS[rid][1]) for rid in ENTRYPOINTS}
    for rid in (P + "rule.form1040-line2b", P + "rule.attachment.schedule-d", P + "rule.attachment.f8949"):
        assert [m for m in v63["members"] if m["id"] == rid] == [m for m in v62["members"] if m["id"] == rid]


def test_v63_shares_the_v62_companion_declaration() -> None:
    declarations = domain_package_companion_declarations()
    core = P + "package.core-calculations"
    assert declarations[(core, "v63")] == declarations[(core, "v62")]


def test_each_successor_is_its_predecessor_with_the_guard() -> None:
    for rid, (frm, to) in SUCCESSORS.items():
        name = rid.split("rule.")[1]
        old = json.loads((CONTENT / (f"rule.{name}.json" if frm == "v1" else f"rule.{name}.{frm}.json")).read_text())
        new = json.loads((CONTENT / f"rule.{name}.{to}.json").read_text())
        assert new["version"] == to and new["when"]["op"] == "require_closed"
        changed = {k for k in set(old) | set(new) if old.get(k) != new.get(k)}
        assert changed <= {"version", "when", "notes"}, (rid, changed)
