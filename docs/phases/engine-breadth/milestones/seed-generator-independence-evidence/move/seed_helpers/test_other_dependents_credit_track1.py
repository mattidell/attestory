"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""

from __future__ import annotations

from typing import Any
from typing import Mapping
from typing import cast
from seed_helpers.test_child_tax_credit_track1 import CHILD_TYPES
from seed_helpers.test_child_tax_credit_track1 import OD
from seed_helpers.test_child_tax_credit_track1 import build_acts as ctc_build_acts
from seed_helpers.test_refund_or_amount_owed_track1 import _act
from seed_helpers.test_refund_or_amount_owed_track1 import _attested
from seed_helpers.test_refund_or_amount_owed_track1 import _close_empty
from seed_helpers.test_refund_or_amount_owed_track1 import _close_other_box4_families
from seed_helpers.test_refund_or_amount_owed_track1 import _load
from seed_helpers.test_refund_or_amount_owed_track2 import _add_bottom_line_answers
from seed_helpers.test_refund_or_amount_owed_track2 import _add_box2_only

YEAR = "2025"

JOINT_STATUS = "married_filing_jointly"

C_BOX = "tax.us.2025.odc.child.other-dependent-box"

C_TIN = "tax.us.2025.odc.child.tin"

C_CLOSE = "tax.us.2025.odc.child-roster.source-closure"

R_BOX = "tax.us.2025.odc.dependent.other-dependent-box"

R_REL = "tax.us.2025.odc.dependent.relationship"

R_NQC = "tax.us.2025.odc.dependent.not-qualifying-child"

R_GI = "tax.us.2025.odc.dependent.gross-income-under-limit"

R_SUP = "tax.us.2025.odc.dependent.over-half-support"

R_TIN = "tax.us.2025.odc.dependent.tin"

R_CIT = "tax.us.2025.odc.dependent.citizen-or-resident"

R_NM = "tax.us.2025.odc.dependent.not-joint-return"

R_CLOSE = "tax.us.2025.odc.relative-roster.source-closure"

REL_KIND = "tax.us.odc-dependent"

TP = "tax.us.2025.odc.taxpayer-tin"

SP = "tax.us.2025.odc.spouse-tin"

F2555 = "tax.us.2025.odc.no-form-2555"

NEW_ANSWERS_RELATIVE = (R_BOX, R_REL, R_NQC, R_GI, R_SUP, R_TIN, R_CIT, R_NM)

BUNDLES = ("odc-child-roster.bundle.json", "odc-relative-roster.bundle.json",
           "odc-return-questions.bundle.json")

def _odc_extras(
    raw: list[dict[str, object]],
    children: Mapping[str, Mapping[str, str]],
    relatives: Mapping[str, Mapping[str, str]],
    *,
    child_closed: bool,
    relative_closed: bool,
    return_answers: Mapping[str, str | None],
) -> None:
    def add(kind: str, payload: dict[str, object]) -> None:
        raw.append(_act(len(raw), kind, payload))

    for name in BUNDLES:
        add("bundle-adoption", {"bundle": _load(name)})
    scope = {"tax-year": YEAR, "subject": "demo.primary"}
    head = "demo.odc.child.h0"
    family = {"id": "tax.us.2025.odc.child-roster", "version": "v1"}
    add("horizon-genesis", {"family": family, "scope": scope, "horizon_id": head})
    # A roster row exists only for a child marked yes; a child marked no (or not marked) is not a row.
    marked = [(c, a) for c, a in children.items() if a.get(C_BOX) == "yes"]
    for idx, (child, answers) in enumerate(marked):
        successor = f"demo.odc.child.h{idx + 1}"
        add("member-transition", {"family": family, "scope": scope, "member": {
            "action": "assert", "finding": _attested(
                f"demo.odc.box.{child}", child_fid(C_BOX, child), answers[C_BOX])},
            "successor": {"id": successor, "predecessor": head}})
        head = successor
        if answers.get(C_TIN) is not None:
            add("assertion", {"finding": _attested(
                f"demo.odc.tin.{child}", child_fid(C_TIN, child), answers[C_TIN])})
    if child_closed:
        add("assertion", {"finding": _attested(
            "demo.odc.child.closure", f"{C_CLOSE}|family-horizon={head},tax-year={YEAR}", True)})

    rel_scope = {"tax-year": YEAR, "subject": "demo.primary"}
    rel_head = "demo.odc.rel.h0"
    rel_family = {"id": "tax.us.2025.odc.relative-roster", "version": "v1"}
    for name, answers in relatives.items():
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": name, "kind": REL_KIND,
                                             "label": "Synthetic other dependent"}})
    add("horizon-genesis", {"family": rel_family, "scope": rel_scope, "horizon_id": rel_head})
    rel_marked = [(n, a) for n, a in relatives.items() if a.get(R_BOX) == "yes"]
    for idx, (name, answers) in enumerate(rel_marked):
        successor = f"demo.odc.rel.h{idx + 1}"
        add("member-transition", {"family": rel_family, "scope": rel_scope, "member": {
            "action": "assert", "finding": _attested(
                f"demo.odc.rel.box.{name}", _rel_fid(R_BOX, name), answers[R_BOX])},
            "successor": {"id": successor, "predecessor": rel_head}})
        rel_head = successor
        for fact in NEW_ANSWERS_RELATIVE:
            if fact == R_BOX or answers.get(fact) is None:
                continue
            add("assertion", {"finding": _attested(
                f"demo.odc.rel.{fact.rsplit('.', 1)[-1]}.{name}", _rel_fid(fact, name), answers[fact])})
    if relative_closed:
        add("assertion", {"finding": _attested(
            "demo.odc.rel.closure", f"{R_CLOSE}|family-horizon={rel_head},tax-year={YEAR}", True)})

    for fact, answer in return_answers.items():
        if answer is None:
            continue
        add("assertion", {"finding": _attested(
            f"demo.odc.ret.{fact.rsplit('.', 1)[-1]}", f"{fact}|tax-year={YEAR}", answer)})

def _complete(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    """Adds the W-2 box 2 family, closes the other box 4 families and the bottom-line answers, as the
    child tax credit presentation does, so the return is complete on v55 and on v56."""
    acts = _add_box2_only(acts, employer="demo.cgd.t2.employer", slip="demo.cgd.t2.w2", amount=0.0)
    _close_empty(acts, family="tax.us.2025.w2-box2", version="v1",
                 closure_fact="tax.us.2025.w2-box2.source-closure", horizon="demo.odc.complete.w2box2")
    _close_other_box4_families(acts, skip={"w2-box2"})
    return _add_bottom_line_answers(acts, estimated=0.0, applied_2026=0.0)

def build(
    *,
    wages: float,
    filing_status: str = "single",
    children: Mapping[str, Mapping[str, str]] | None = None,
    relatives: Mapping[str, Mapping[str, str]] | None = None,
    return_answers: Mapping[str, str | None] | None = None,
    child_closed: bool = True,
    relative_closed: bool = True,
    can_be_claimed: str | None = "no",
    ctc_closed: bool = True,
) -> list[dict[str, object]]:
    kids = dict(children or {})
    ctc_kids = {name: {k: v for k, v in answers.items() if k in CHILD_TYPES}
                for name, answers in kids.items()}
    ret: dict[str, str | None] = {TP: "yes", F2555: "yes"}
    if filing_status == JOINT_STATUS:
        ret[SP] = "yes"
    if children or relatives:
        # An other dependent is present: the return answer says the rosters are read.
        ret[OD] = "no"
    ret.update(return_answers or {})
    odc_side = {k: ret[k] for k in (TP, SP, F2555) if k in ret}
    ctc_side = {k: v for k, v in ret.items() if k not in (TP, SP, F2555)}
    raw = ctc_build_acts(wages=wages, filing_status=filing_status, children=ctc_kids,
                         closed_roster=ctc_closed, can_be_claimed=cast(Any, can_be_claimed),
                         return_answers=ctc_side)
    _odc_extras(raw, kids, relatives or {}, child_closed=child_closed,
                relative_closed=relative_closed, return_answers=odc_side)
    return raw
