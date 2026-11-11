"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""

from __future__ import annotations

from typing import Mapping
from typing import cast
from seed_helpers.test_refund_or_amount_owed_track1 import _act
from seed_helpers.test_refund_or_amount_owed_track1 import _attested
from seed_helpers.test_refund_or_amount_owed_track1 import _load
from seed_helpers.test_refund_or_amount_owed_track1 import _sdd

EIC_CHILD_KIND = "tax.us.eic-child"

YEAR = "2025"

EIC_FAMILY = "tax.us.2025.eic.child-roster"

EIC_CLOSURE = "tax.us.2025.eic.child-roster.source-closure"

EIC_AGE = "tax.us.2025.eic.child.age"

EIC_RES = "tax.us.2025.eic.child.residency"

EIC_NOT_QC = "tax.us.2025.eic.not-qualifying-child-of-another"

EIC_SP_SSN = "tax.us.2025.eic.spouse-valid-ssn"

EIC_SEP = "tax.us.2025.eic.separated-spouse"

CHILD_KIND = EIC_CHILD_KIND

FAMILY = "tax.us.2025.ctc.child-roster"

CLOSURE = "tax.us.2025.ctc.child-roster.source-closure"

REL = "tax.us.2025.eic.child.relationship"

JOINT = "tax.us.2025.eic.child.joint-return"

SSN = "tax.us.2025.eic.child.ssn"

OTHER = "tax.us.2025.eic.child.another-may-claim"

U17 = "tax.us.2025.ctc.child.under-17"

RES = "tax.us.2025.ctc.child.lived-with-you"

SUP = "tax.us.2025.ctc.child.no-over-half-support"

CIT = "tax.us.2025.ctc.child.citizen-or-resident"

CLAIM = "tax.us.2025.ctc.child.claimed-as-dependent"

CHILD_TYPES = (REL, JOINT, SSN, OTHER, U17, RES, SUP, CIT, CLAIM)

TP_SSN = "tax.us.2025.eic.taxpayer-valid-ssn"

NRA = "tax.us.2025.eic.not-nonresident-alien"

NOT_DEP = "tax.us.2025.eic.not-claimable-as-dependent"

UNSUP = "tax.us.2025.eic.no-unsupported-situations"

OD = "tax.us.2025.ctc.no-other-dependent"

SPOUSE = "tax.us.2025.ctc.spouse-ssn-or-itin"

PR = "tax.us.2025.ctc.no-puerto-rico-or-4563-exclusion"

L2931 = "tax.us.2025.lines29-31-scope.no-other-refundable-credits"

FILER_ANSWERS = (TP_SSN, NRA, NOT_DEP, UNSUP, OD, PR, L2931)

def build_acts(
    *,
    wages: float,
    filing_status: str = "single",
    children: Mapping[str, Mapping[str, str]] | None = None,
    return_answers: Mapping[str, str | None] | None = None,
    closed_roster: bool = True,
    eic_roster: bool = True,
    eic_spouse_ssn: str | None = "yes",
    interest: float | None = None,
    can_be_claimed: str = "no",
) -> list[dict[str, object]]:
    raw = cast(list[dict[str, object]], _sdd()._senior_acts(
        wages=wages, filing_status=filing_status, can_be_claimed=can_be_claimed))
    if interest is not None:
        raw = _with_taxable_interest(raw, interest)
    raw.append(_act(len(raw), "bundle-adoption", {"bundle": _load("eic-questions.bundle.json")}))
    raw.append(_act(len(raw), "bundle-adoption", {"bundle": _load("eic-child-roster.bundle.json")}))
    raw.append(_act(len(raw), "bundle-adoption", {"bundle": _load("ctc-child-roster.bundle.json")}))
    raw.append(_act(len(raw), "bundle-adoption", {"bundle": _load("ctc-return-questions.bundle.json")}))

    answers: dict[str, str | None] = {fid: "yes" for fid in FILER_ANSWERS}
    if filing_status == "married_filing_jointly":
        # The earned income credit's dependent answer is not asked on a joint return, and
        # the credit's filer gate reads the standard-deduction answer instead.
        answers.pop(NOT_DEP, None)
        answers[SPOUSE] = "yes"
    if return_answers:
        answers.update(return_answers)
    for fid, val in answers.items():
        if val is None:
            continue
        raw.append(_act(len(raw), "assertion", {"finding": _attested(
            f"demo.{fid.split('.')[-1]}", f"{fid}|tax-year={YEAR}", val)}))

    scope_key = {"tax-year": YEAR, "subject": "demo.primary"}
    kids = dict(children or {})
    for child in kids:
        raw.append(_act(len(raw), "entity-introduced", {"entity": {
            "schema": "entity.v1", "id": child, "kind": CHILD_KIND, "label": f"Synthetic {child}"}}))
    if eic_roster:
        _add_eic_roster(raw, kids, filing_status, spouse_ssn=eic_spouse_ssn)
    raw.append(_act(len(raw), "horizon-genesis", {
        "family": {"id": FAMILY, "version": "v1"}, "scope": scope_key, "horizon_id": "demo.ctc.h0"}))
    horizon = "demo.ctc.h0"
    for idx, (child, c_answers) in enumerate(kids.items()):
        successor = f"demo.ctc.h{idx + 1}"
        if c_answers.get(CLAIM) is not None:
            raw.append(_act(len(raw), "member-transition", {
                "family": {"id": FAMILY, "version": "v1"},
                "scope": scope_key,
                "member": {"action": "assert", "finding": _attested(
                    f"demo.claim.{child}", child_fid(CLAIM, child), c_answers[CLAIM])},
                "successor": {"id": successor, "predecessor": horizon},
            }))
            horizon = successor
        for fid in CHILD_TYPES:
            if fid in (REL, CLAIM) or fid not in c_answers or c_answers[fid] is None:
                continue
            raw.append(_act(len(raw), "assertion", {"finding": _attested(
                f"demo.{fid.split('.')[-1]}.{child}", child_fid(fid, child), c_answers[fid])}))
    if closed_roster:
        raw.append(_act(len(raw), "assertion", {"finding": _attested(
            "demo.ctc.closure", f"{CLOSURE}|family-horizon={horizon},tax-year={YEAR}", True)}))
    return raw

def _add_eic_roster(acts: list[dict[str, object]], kids: Mapping[str, Mapping[str, str]], filing_status: str, *, spouse_ssn: str | None = "yes") -> None:
    """The earned income roster for the same children. Each relationship fact is a member
    of this family only: the kernel allows one membership per fact, so the credit family's
    member is the claimed-as-dependent fact instead."""

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("assertion", {"finding": _attested("demo.eic.not-qc", f"{EIC_NOT_QC}|tax-year={YEAR}", "yes")})
    if filing_status == "married_filing_jointly" and spouse_ssn is not None:
        add("assertion", {"finding": _attested("demo.eic.sp-ssn", f"{EIC_SP_SSN}|tax-year={YEAR}", spouse_ssn)})
    if filing_status in ("married_filing_separately", "head_of_household"):
        add("assertion", {"finding": _attested("demo.eic.sep", f"{EIC_SEP}|tax-year={YEAR}", "yes")})
    scope_key = {"tax-year": YEAR, "subject": "demo.primary"}
    add("horizon-genesis", {"family": {"id": EIC_FAMILY, "version": "v1"}, "scope": scope_key, "horizon_id": "demo.eic.h0"})
    horizon = "demo.eic.h0"
    for idx, child in enumerate(kids):
        successor = f"demo.eic.h{idx + 1}"
        add("member-transition", {
            "family": {"id": EIC_FAMILY, "version": "v1"}, "scope": scope_key,
            "member": {"action": "assert", "finding": _attested(
                f"demo.eic.rel.{child}", child_fid(REL, child), "yes")},
            "successor": {"id": successor, "predecessor": horizon}})
        horizon = successor
        add("assertion", {"finding": _attested(f"demo.eic.age.{child}", child_fid(EIC_AGE, child), "yes")})
        add("assertion", {"finding": _attested(f"demo.eic.res.{child}", child_fid(EIC_RES, child), "yes")})
    add("assertion", {"finding": _attested(
        "demo.eic.closure", f"{EIC_CLOSURE}|family-horizon={horizon},tax-year={YEAR}", True)})
