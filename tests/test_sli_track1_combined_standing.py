"""Track 1: line 21 reads each form's combined standing.

The successor worksheet (``tax.us.2025.rule.sli-worksheet`` v5, core
calculations v42) publishes from the current answers on each Form 1098-E.
Favorable combined standing is only ``none``. These cases are the charter
table. Each one is recorded through the real recorder, or through the
source-append helper named below for the late member, recovered fresh, and
run through ``live_coordinate_run`` on both runners. The line 21 section is
read back from the coordinator's saved presentation.

The "changes" cases are also run on the adopted v41 package. That base
blocks because the older answer and the loan detail are both present.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from unittest import mock

import pytest

import packages.derivation.live as live_module
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.marshal import marshal_live_run_context
from packages.derivation.loader import DerivationSchemas
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import RunResult, run
from packages.kernel.facts import fact_id_for
from packages.kernel.findings import project
from packages.kernel.horizons import current_horizon_id
import tests.test_sli_relationship_recording as track14
import tests.test_sli_track4_support_chain as track4
import tests.test_sli_track5_worksheet_integration as track5
from tests.support import act
from tests.test_form1099g_box1_schedule1_line7 import _attested

pytestmark = pytest.mark.live

ROOT = track5.ROOT
CONTENT = track5.CONTENT
USER = track5.USER
SCOPE = track5.SCOPE
RELEASE_DIR = track5.RELEASE_DIR
V40_RELEASE = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v40.json"
V40_REGISTRY = CONTENT / "published-packages.v40.json"
V42_PACKAGE = CONTENT / "package.core-calculations.v42.json"

COMBINED = "tax.us.2025.sli.statement-combined-standing"
OLDER = "tax.us.2025.sli.older-answer"
LINE26 = "tax.us.2025.schedule1.line26-total-adjustments"
LINE1 = "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal"
LINE10_FIELD = "tax.us.2025.form1040.line-10"
LINE1A_FIELD = "tax.us.2025.form1040.line-1a"
SUM_LOAN_NO = "tax.us.2025.sli.sum.inclusion-loan-cost-no"
FLAG_LOAN_NO = "tax.us.2025.sli.flag.inclusion-loan-cost-no"
COUNT_DENIED = "tax.us.2025.sli.count.statement-inclusion-denied"
FAMILY = {"id": "tax.us.2025.f1098e.1", "version": "v1"}
CLOSURE = "tax.us.2025.f1098e.1.source-closure"
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}
BOTH_TOKEN = track5.BOTH_TOKEN
REPLACED = track5.REPLACED
RESULT_DIR = Path("/tmp/track1-results")

STANDARD = {"cedar": 3000.0, "birch": 1800.0}
Populate = Callable[[track5.Return], None]


@dataclass(frozen=True)
class Spec:
    """One charter case: how to record it, and what v42 must publish."""

    wages: float
    amounts: dict[str, float]
    populate: Populate
    disposition: str
    value: int | None
    code: str | None
    combined: dict[str, str | None]
    missing: str | None = None
    neighbors: bool = False
    line1: int | None = None
    older: dict[str, str] | None = None


def _link_complete(
    ws: track5.Return,
    borrowing: str,
    school: str,
    statement: str,
    *,
    loan: str | None = "yes",
    enroll: str | None = "yes",
    financing: bool = True,
) -> None:
    if financing:
        ws.link("financing", borrowing, school)
    ws.link("statement-inclusion", borrowing, statement)
    if loan is not None:
        ws.answer("loan", borrowing, loan)
    if enroll is not None:
        ws.answer("enroll", borrowing, enroll)


def _birch_old(ws: track5.Return) -> None:
    ws.old_answers("birch")


def _k0a(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    ws.old_answers("birch")


def _k0b(ws: track5.Return) -> None:
    _link_complete(ws, "autumn", "autumn", "cedar")
    ws.common_answers("cedar")
    _link_complete(ws, "spring", "spring", "birch")
    ws.common_answers("birch")


def _k1(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar")
    _birch_old(ws)


def _k7(ws: track5.Return) -> None:
    _link_complete(ws, "autumn", "autumn", "cedar")
    ws.common_answers("cedar")
    _link_complete(ws, "spring", "spring", "birch")
    ws.common_answers("birch")


def _k8_before(ws: track5.Return) -> None:
    ws.link("financing", "autumn", "autumn")
    ws.link("statement-inclusion", "autumn", "cedar")
    ws.link("statement-inclusion", "autumn", "birch")
    ws.answer("loan", "autumn", "yes")
    ws.answer("enroll", "autumn", "yes")
    ws.common_answers("cedar")
    ws.common_answers("birch")


def _correct_enrollment(ws: track5.Return) -> None:
    """The product review corrects the shared enrollment answer to no."""
    from packages.tax import sli_relationship_review as review_mod

    finding_id = ws.current_finding(
        "tax.us.2025.sli.enrolled-at-least-half-time",
        (("borrowing", ws.borrowing["autumn"]),),
    )
    name = ws._name("track1-correct-enroll")
    review = review_mod.prepare_borrowing_answer_review(
        ws.log, ws.registry, review_id=f"demo.track1.review.{name}",
        shown_at="2026-10-08T09:00:00Z", borrowing_refs=tuple(ws.borrowing.values()),
    )
    review_mod.correct_borrowing_answer_review(
        ws.log, ws.registry, review, finding_id=finding_id, borrowing_ref=ws.borrowing["autumn"],
        question=track4.QUESTIONS["enroll"], response="no", actor=USER, at="2026-10-08T09:00:00Z",
        submission_id=f"demo.track1.submission.{name}", evidence_id=f"demo.evidence.track1.{name}",
    )


def _k8_after(ws: track5.Return) -> None:
    _k8_before(ws)
    _correct_enrollment(ws)


def _append(ws: track5.Return, kind: str, payload: dict[str, Any]) -> None:
    revision = ws.log.read().revision
    item = act(revision, kind, payload)
    item["actor"] = USER
    item["act_id"] = f"demo.track1.{kind}.{ws._name('act')}"
    ws.log.append(item, expected_revision=revision)


def add_cedar_member(ws: track5.Return, *, reclose: bool) -> None:
    """Admit Cedar's box 1 on the next horizon, through the source-append helper.

    Box 2 is attested first. The box 1 member advances the Form 1098-E
    horizon. ``reclose`` writes a closure on that new horizon; leaving it
    false is the late-unclosed case.
    """
    keys = track5.Return.STATEMENT_KEYS["cedar"]
    track14._append_source(ws.log, ws.registry, track5.BOX2, keys, False, ws._name("track1-cedar-box2"))
    box1 = fact_id_for(track4.BOX1, keys)
    state = project(ws.acts(), ws.registry)
    predecessor = current_horizon_id(state.horizon_state, FAMILY, SCOPE_KEY)
    if not isinstance(predecessor, str) or not predecessor:
        raise AssertionError("Form 1098-E has no current horizon to succeed")
    _append(ws, "member-transition", {
        "family": FAMILY,
        "scope": SCOPE_KEY,
        "member": {
            "action": "assert",
            "finding": _attested("demo.track1.finding.cedar-box1", box1, 3000.0),
        },
        "successor": {"id": "demo.track1.horizon.1", "predecessor": predecessor},
    })
    ws.statement_keys["cedar"] = keys
    ws.statement["cedar"] = box1
    ws.old_answers("cedar")
    if reclose:
        _append(ws, "assertion", {
            "finding": _attested(
                "demo.track1.finding.closure",
                f"{CLOSURE}|family-horizon=demo.track1.horizon.1,tax-year=2025",
                True,
            ),
        })


def _mfs(ws: track5.Return) -> None:
    _k0a(ws)
    track14._append_source(
        ws.log, ws.registry, "tax.us.2025.filing-status", (("tax-year", "2025"),),
        "married_filing_separately", ws._name("track1-mfs"),
    )


def _late_unclosed(ws: track5.Return) -> None:
    ws.old_answers("birch")
    add_cedar_member(ws, reclose=False)


def _two_form(ws: track5.Return) -> None:
    """Cedar's loan-cost no stays on Cedar. Birch's own inclusion answered yes."""
    ws.link("statement-inclusion", "autumn", "cedar")
    ws.answer("loan", "autumn", "no")
    ws.answer("enroll", "autumn", "yes")
    _link_complete(ws, "spring", "spring", "birch")


def _k2(ws: track5.Return) -> None:
    ws.old_answers("cedar", values={REPLACED: "no"})
    _link_complete(ws, "autumn", "autumn", "cedar")
    _birch_old(ws)


def _k3(ws: track5.Return) -> None:
    ws.old_answers("cedar", skip=(REPLACED,))
    _link_complete(ws, "autumn", "autumn", "cedar")
    _birch_old(ws)


def _k5(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    ws.link("statement-inclusion", "autumn", "cedar")
    ws.outcome("statement-inclusion", "autumn", "cedar", "no")
    _birch_old(ws)


def _k6(ws: track5.Return) -> None:
    ws.old_answers("cedar", values={"no-related-person-interest": "no"})
    _link_complete(ws, "autumn", "autumn", "cedar")
    _birch_old(ws)


def _k9_after(ws: track5.Return) -> None:
    _k1(ws)
    ws.outcome("statement-inclusion", "autumn", "cedar", "withdrawn")


def _k10(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", loan="no")
    _birch_old(ws)


def _k11(ws: track5.Return) -> None:
    _link_complete(ws, "spring", "spring", "birch")
    ws.common_answers("birch")


def _k12(ws: track5.Return) -> None:
    ws.plain("autumn", "autumn", "cedar")
    ws.plain("spring", "spring", "birch")
    ws.retract_source(ws.statement["cedar"])


def _k13(ws: track5.Return) -> None:
    _link_complete(ws, "autumn", "autumn", "cedar")
    ws.common_answers("cedar")
    ws.old_answers("birch")
    _link_complete(ws, "spring", "spring", "birch")
    ws.unscoped_rewrite("birch", 1800.0)


def _m1(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", loan="no", financing=False)
    _birch_old(ws)


def _m2(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", loan="cannot-tell", enroll="no")
    _birch_old(ws)


def _m3(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", loan="no", enroll="no")
    ws.outcome("financing", "autumn", "autumn", "cannot-tell")
    _birch_old(ws)


def _m5(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar")
    _link_complete(ws, "spring", "spring", "cedar", enroll="no")
    _birch_old(ws)


def _shared(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    ws.old_answers("birch")
    ws.link("financing", "autumn", "autumn")
    ws.link("statement-inclusion", "autumn", "cedar")
    ws.link("statement-inclusion", "autumn", "birch")
    ws.answer("loan", "autumn", "no")
    ws.answer("enroll", "autumn", "yes")


def _open_loan(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", loan="no")
    ws.outcome("statement-inclusion", "autumn", "cedar", "cannot-tell")
    _birch_old(ws)


def _open_enroll(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", enroll="no")
    ws.outcome("statement-inclusion", "autumn", "cedar", "cannot-tell")
    _birch_old(ws)


def _withdrawn_loan(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", loan="no")
    ws.outcome("statement-inclusion", "autumn", "cedar", "withdrawn")
    _birch_old(ws)


def _withdrawn_enroll(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", enroll="no")
    ws.outcome("statement-inclusion", "autumn", "cedar", "withdrawn")
    _birch_old(ws)


def _both_contrary(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", loan="no")
    ws.outcome("statement-inclusion", "autumn", "cedar", "withdrawn")
    _link_complete(ws, "spring", "spring", "cedar", enroll="no")
    ws.outcome("statement-inclusion", "spring", "cedar", "cannot-tell")
    _birch_old(ws)


def _u3(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    ws.doubt("cedar")
    _birch_old(ws)


def _u4(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar")
    ws.outcome("statement-inclusion", "autumn", "cedar", "cannot-tell")
    _birch_old(ws)


def _u8a(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar")
    ws.outcome("financing", "autumn", "autumn", "cannot-tell")
    _birch_old(ws)


def _u9b(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", loan="cannot-tell")
    _birch_old(ws)


def _u10b(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", enroll="cannot-tell")
    _birch_old(ws)


def _l7(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar")
    _link_complete(ws, "spring", "spring", "cedar")
    _birch_old(ws)


def _l8b(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar")
    ws.outcome("financing", "autumn", "autumn", "withdrawn")
    _birch_old(ws)


def _l8c(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", financing=False)
    _birch_old(ws)


def _l8d(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    ws.link("financing", "autumn", "autumn")
    ws.link("financing", "autumn", "spring")
    ws.link("statement-inclusion", "autumn", "cedar")
    ws.answer("loan", "autumn", "yes")
    ws.answer("enroll", "autumn", "yes")
    _birch_old(ws)


def _l9a(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", loan=None)
    _birch_old(ws)


def _l10a(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", enroll=None)
    _birch_old(ws)


def _u8e(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar")
    ws.outcome("financing", "autumn", "autumn", "no")
    _birch_old(ws)


def _mix(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", loan=None, enroll="cannot-tell")
    _birch_old(ws)


def _denied_loan_no(ws: track5.Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", loan="no")
    ws.outcome("statement-inclusion", "autumn", "cedar", "no")
    _birch_old(ws)


def _empty(ws: track5.Return) -> None:
    del ws


def _form(value: str, *, birch: str | None = "none") -> dict[str, str | None]:
    return {"cedar": value, "birch": birch}


def _specs() -> dict[str, Spec]:
    both_none: dict[str, str | None] = {"cedar": "none", "birch": "none"}
    published = "published_value"
    blocked = "blocked"
    invalid = "DEPENDENCY_INVALID"

    def spec(
        wages: float,
        amounts: dict[str, float],
        populate: Populate,
        disposition: str,
        value: int | None,
        code: str | None,
        combined: dict[str, str | None],
        **rest: Any,
    ) -> Spec:
        return Spec(wages, amounts, populate, disposition, value, code, combined, **rest)

    rows: dict[str, Spec] = {
        "K0a": spec(50000, STANDARD, _k0a, published, 2500, None, both_none, neighbors=True, line1=4800),
        "K0b": spec(50000, STANDARD, _k0b, published, 2500, None, both_none),
        "K1": spec(50000, STANDARD, _k1, published, 2500, None, both_none, neighbors=True, line1=4800),
        "K2": spec(50000, STANDARD, _k2, blocked, None, invalid, _form("older-no"), neighbors=True, line1=4800),
        "K3": spec(50000, STANDARD, _k3, published, 2500, None, both_none),
        "K5": spec(50000, STANDARD, _k5, published, 2500, None, both_none),
        "K6": spec(50000, STANDARD, _k6, blocked, None, "SLI_UNIVERSAL_COMPONENT_VIOLATION", both_none),
        "K7-below": spec(50000, {"cedar": 2000.0, "birch": 1000.0}, _k7, published, 2500, None, both_none),
        "K7-phaseout": spec(90000, {"cedar": 2000.0, "birch": 1000.0}, _k7, published, 1668, None, both_none),
        "K8-before": spec(50000, {"cedar": 1500.0, "birch": 800.0}, _k8_before, published, 2300, None, both_none),
        "K8-after": spec(50000, {"cedar": 1500.0, "birch": 800.0}, _k8_after, blocked, None, invalid,
                         {"cedar": "enrollment-no", "birch": "enrollment-no"}),
        "K9-before": spec(50000, STANDARD, _k1, published, 2500, None, both_none),
        "K9-after": spec(50000, STANDARD, _k9_after, published, 2500, None, both_none,
                         older={"cedar": "yes", "birch": "yes"}),
        "K10": spec(50000, STANDARD, _k10, blocked, None, invalid, _form("contradicts-loan-cost-no")),
        "K11": spec(50000, STANDARD, _k11, blocked, None, invalid, {"cedar": None, "birch": "none"},
                    missing="cedar-box1"),
        "K12": spec(50000, STANDARD, _k12, blocked, None, invalid, {"cedar": None, "birch": "none"},
                    missing="cedar-marker-autumn"),
        "K13": spec(50000, STANDARD, _k13, blocked, None, invalid,
                    {"cedar": "none", "birch": "applicability-unestablished"}, missing="birch-marker-spring"),
        "M1": spec(50000, STANDARD, _m1, blocked, None, invalid, _form("contradicts-loan-cost-no")),
        "M2": spec(50000, STANDARD, _m2, blocked, None, invalid, _form("contradicts-enrollment-no")),
        "M3": spec(50000, STANDARD, _m3, blocked, None, invalid, _form("contradicts-loan-cost-no")),
        "M5": spec(50000, STANDARD, _m5, blocked, None, invalid, _form("contradicts-enrollment-no")),
        "shared-borrowing": spec(50000, STANDARD, _shared, blocked, None, invalid,
                                 {"cedar": "contradicts-loan-cost-no", "birch": "contradicts-loan-cost-no"}),
        "open-loan-no": spec(50000, STANDARD, _open_loan, blocked, None, invalid, _form("open-inclusion-loan-cost-no")),
        "open-enroll-no": spec(50000, STANDARD, _open_enroll, blocked, None, invalid,
                               _form("open-inclusion-enrollment-no")),
        "withdrawn-loan-no": spec(50000, STANDARD, _withdrawn_loan, blocked, None, invalid,
                                  _form("withdrawn-inclusion-loan-cost-no")),
        "withdrawn-enroll-no": spec(50000, STANDARD, _withdrawn_enroll, blocked, None, invalid,
                                    _form("withdrawn-inclusion-enrollment-no")),
        "both-contrary": spec(50000, STANDARD, _both_contrary, blocked, None, invalid,
                              _form("contrary-on-unsettled-inclusion")),
        "U3": spec(50000, STANDARD, _u3, blocked, None, invalid, _form("statement-loan-cannot-tell")),
        "U4": spec(50000, STANDARD, _u4, blocked, None, invalid, _form("inclusion-cannot-tell")),
        "U8a": spec(50000, STANDARD, _u8a, blocked, None, invalid, _form("mixed-unresolved-and-lacks")),
        "U9b": spec(50000, STANDARD, _u9b, blocked, None, invalid, _form("loan-cost-cannot-tell")),
        "U10b": spec(50000, STANDARD, _u10b, blocked, None, invalid, _form("enrollment-cannot-tell")),
        "L7": spec(50000, STANDARD, _l7, published, 2500, None, both_none),
        "L8b": spec(50000, STANDARD, _l8b, published, 2500, None, both_none),
        "L8c": spec(50000, STANDARD, _l8c, published, 2500, None, both_none),
        "L8d": spec(50000, STANDARD, _l8d, published, 2500, None, both_none),
        "L9a": spec(50000, STANDARD, _l9a, published, 2500, None, both_none),
        "L10a": spec(50000, STANDARD, _l10a, published, 2500, None, both_none),
        "U8e": spec(50000, STANDARD, _u8e, blocked, None, invalid, _form("financing-denied-unsettled")),
        "mix-loan-missing-enroll-cannot-tell": spec(50000, STANDARD, _mix, blocked, None, invalid,
                                                     _form("mixed-unresolved-and-lacks")),
        "denied-loan-no": spec(50000, STANDARD, _denied_loan_no, published, 2500, None, both_none),
        "two-form": spec(50000, STANDARD, _two_form, blocked, None, invalid, _form("no-schooling-link")),
        "empty": spec(50000, {}, _empty, "closure_backed_zero", 0, None, {}, neighbors=True),
        "mfs": spec(50000, STANDARD, _mfs, blocked, None, "SLI_MFS_INELIGIBLE", both_none,
                    neighbors=True, line1=4800),
        "late-unclosed": spec(50000, {"birch": 1800.0}, _late_unclosed, blocked, None, "SOURCE_SET_UNCLOSED",
                              both_none, neighbors=True, line1=4800),
    }
    return rows


SPECS = _specs()
CHANGES = (
    "K1", "K3", "K5", "K9-before", "K9-after",
    "L7", "L8b", "L8c", "L8d", "L9a", "L10a", "denied-loan-no",
)


def adopt_v42(ws: track5.Return) -> None:
    """A second adoption. Revision 2 is the current package; v41 stays in the log."""
    package = json.loads(V42_PACKAGE.read_text("utf-8"))
    release = json.loads(V40_RELEASE.read_text("utf-8"))
    revision = ws.log.read().revision
    item = act(revision, "package-adoption", {
        "package": {"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]},
        "release": {
            "id": release["id"], "version": release["version"],
            "checksum": hashlib.sha256(V40_RELEASE.read_bytes()).hexdigest(),
        },
        "scope": SCOPE, "revision": 2,
    })
    item["actor"] = USER
    item["act_id"] = "demo.track1.adoption.v42"
    ws.log.append(item, expected_revision=revision)


def _section(model: dict[str, Any], field_id: str) -> dict[str, Any]:
    [section] = [row for row in model["sections"] if row["field"]["id"] == field_id]
    resolved: dict[str, Any] = section["resolved"]
    return resolved


def _number(value: Any) -> int | float:
    number = float(value)
    if number.is_integer():
        return int(number)
    return number


def _sole(result: RunResult, symbol: str) -> int | float:
    found = []
    for pub in result.publications:
        name = str(pub.finding["symbol"]).split("|", 1)[0]
        if name == symbol:
            found.append(pub.finding["value"])
    if len(found) != 1:
        raise AssertionError(f"{symbol} published {len(found)} times")
    return _number(found[0])


def _absent(result: RunResult, symbol: str) -> bool:
    return all(str(pub.finding["symbol"]).split("|", 1)[0] != symbol for pub in result.publications)


def _by_subject(result: RunResult, symbol: str) -> dict[str, Any]:
    prefix = symbol + "|"
    rows: dict[str, Any] = {}
    for pub in result.publications:
        name = str(pub.finding["symbol"])
        if name.startswith(prefix):
            rows[name[len(prefix):]] = pub.finding["value"]
    return rows


def _classes(result: RunResult, symbol: str, statements: dict[str, str]) -> dict[str, str | None]:
    published = track5.published(result, symbol)
    return {label: published.get(fact_id) for label, fact_id in statements.items()}


def _missing_id(ws: track5.Return, kind: str | None) -> str | None:
    if kind == "cedar-box1":
        return ws.statement["cedar"]
    if kind == "cedar-marker-autumn":
        return track5._marker(ws, "cedar", "autumn")
    if kind == "birch-marker-spring":
        return track5._marker(ws, "birch", "spring")
    return None


class _Ran(track5.Outcome):
    def __init__(self, outcome: track5.Outcome, *, reloaded: bool, runners_agreed: bool) -> None:
        super().__init__(outcome.forward, outcome.reference, outcome.model, outcome.page_html)
        self.reloaded = reloaded
        self.runners_agreed = runners_agreed


def run_v42(acts: tuple[dict[str, Any], ...], run_id: str) -> _Ran:
    """Release resolution on published-packages v40, both runners, saved output reloaded."""
    captured: list[Any] = []

    def spy(**kwargs: Any) -> Any:
        marshalled = marshal_live_run_context(**kwargs)
        captured.append(marshalled._context)
        return marshalled

    with mock.patch.object(live_module, "marshal_live_run_context", side_effect=spy), \
            tempfile.TemporaryDirectory(prefix="sli-track1-live-") as work:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(work) / "workspace"), repo_root=ROOT, authoritative_acts=acts,
            workspace_revision=len(acts), run_scope=SCOPE, scope_user=USER,
            request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
            surface=PublicationSurface(RELEASE_DIR, V40_REGISTRY, CONTENT), output_name="track1.json",
        )
        if outcome.refusal is not None or outcome.presentation_path is None:
            raise AssertionError(f"core calculations v42 refused: {outcome.refusal!r}")
        model = json.loads(outcome.presentation_path.read_text("utf-8"))
    [context] = captured
    schemas = DerivationSchemas()
    forward, reference = run(context, schemas), run_reference(context, schemas)
    agreed = track4.surface(forward) == track4.surface(reference)
    if not agreed:
        raise AssertionError("forward and reference runners disagree")
    assert outcome.publications is not None
    if sorted(json.dumps(p.finding, sort_keys=True) for p in outcome.publications) != sorted(
            json.dumps(p.finding, sort_keys=True) for p in forward.publications):
        raise AssertionError("the coordinator's publications differ from the reloaded forward runner")
    return _Ran(track5.Outcome(forward, reference, model), reloaded=True, runners_agreed=agreed)


def _record(lane: str, name: str, payload: dict[str, Any]) -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    (RESULT_DIR / f"{lane}-{name}.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")


def _summary(outcome: _Ran | track5.Outcome, statements: dict[str, str]) -> dict[str, Any]:
    line21 = outcome.line21
    row = outcome.worksheet_row()
    return {
        "disposition": line21.get("disposition"),
        "value": line21.get("value"),
        "activeCodes": line21.get("activeCodes"),
        "worksheet_code": row.get("code"),
        "worksheet_missing": row.get("missing"),
        "combined": _classes(outcome.forward, COMBINED, statements),
        "older": _classes(outcome.forward, OLDER, statements),
        "reasons": line21.get("reasons"),
        "runners_agreed": getattr(outcome, "runners_agreed", True),
        "presentation_reloaded": getattr(outcome, "reloaded", True),
        "line21_explanation": "line21Explanation" in outcome.model,
    }


def _expect_line(spec: Spec, actual: dict[str, Any]) -> str:
    got_value = actual["value"] if spec.disposition != "blocked" else actual["worksheet_code"]
    want_value = spec.value if spec.disposition != "blocked" else spec.code
    return (
        f"expected {spec.disposition} {want_value} combined {spec.combined}; "
        f"actual {actual['disposition']} {got_value} combined {actual['combined']}"
    )


def _check(case: unittest.TestCase, spec: Spec, ws: track5.Return, outcome: _Ran) -> None:
    case.assertTrue(outcome.runners_agreed)
    case.assertTrue(outcome.reloaded)
    case.assertIn("sections", outcome.model)
    line21 = outcome.line21
    case.assertEqual(line21["disposition"], spec.disposition, _expect_line(spec, _summary(outcome, ws.statement)))
    if spec.value is not None:
        case.assertEqual(line21["value"], spec.value)
    if spec.code is not None:
        case.assertEqual(line21["activeCodes"], [spec.code])
        case.assertEqual(outcome.worksheet_row()["code"], spec.code)
    missing_id = _missing_id(ws, spec.missing)
    if missing_id is not None:
        case.assertEqual(outcome.worksheet_row()["missing"], [missing_id])
    case.assertEqual(_classes(outcome.forward, COMBINED, ws.statement), spec.combined)
    if spec.older is not None:
        case.assertEqual(_classes(outcome.forward, OLDER, ws.statement), spec.older)
    if spec.disposition == "blocked" and spec.code == "DEPENDENCY_INVALID":
        case.assertTrue(line21.get("reasons"), "the blocking class is named on the line")
    if spec.neighbors:
        _check_neighbors(case, outcome, wages=spec.wages, line21_value=spec.value, line1=spec.line1)


def _check_neighbors(
    case: unittest.TestCase,
    outcome: track5.Outcome,
    *,
    wages: float,
    line21_value: int | None,
    line1: int | None,
) -> None:
    wages_line = _section(outcome.model, LINE1A_FIELD)
    case.assertEqual(wages_line["disposition"], "published_value")
    case.assertEqual(wages_line["value"], wages)
    line10 = _section(outcome.model, LINE10_FIELD)
    if line21_value is None:
        case.assertTrue(_absent(outcome.forward, LINE26))
        case.assertEqual(line10["disposition"], "blocked")
        case.assertIn("DEPENDENCY_ABSENT", line10["activeCodes"])
    elif line21_value == 0:
        case.assertEqual(_sole(outcome.forward, LINE26), 0)
        case.assertEqual(line10["disposition"], "computed_zero")
        case.assertEqual(line10["value"], 0)
    else:
        case.assertEqual(_sole(outcome.forward, LINE26), line21_value)
        case.assertEqual(line10["disposition"], "published_value")
        case.assertEqual(line10["value"], line21_value)
    if line1 is not None:
        case.assertEqual(_sole(outcome.forward, LINE1), line1)


def _check_locality(case: unittest.TestCase, name: str, ws: track5.Return, outcome: track5.Outcome) -> None:
    """An inclusion-subject read stays on the form that inclusion belongs to."""
    sums = _by_subject(outcome.forward, SUM_LOAN_NO)
    flags = _by_subject(outcome.forward, FLAG_LOAN_NO)
    denied = _by_subject(outcome.forward, COUNT_DENIED)
    def number_at(rows: dict[str, Any], fact_id: str) -> int | float:
        return _number(rows[fact_id])

    if name == "two-form":
        cedar_inclusion = ws.inclusion_fact_id("autumn", "cedar")
        birch_inclusion = ws.inclusion_fact_id("spring", "birch")
        case.assertEqual(number_at(sums, ws.statement["cedar"]), 1)
        case.assertEqual(number_at(sums, ws.statement["birch"]), 0)
        case.assertEqual(number_at(flags, cedar_inclusion), 1)
        case.assertEqual(number_at(flags, birch_inclusion), 0)
        case.assertEqual(set(flags), {cedar_inclusion, birch_inclusion})
    if name == "denied-loan-no":
        denied_pair = ws.inclusion_fact_id("autumn", "cedar")
        case.assertEqual(number_at(denied, ws.statement["cedar"]), 1)
        case.assertEqual(number_at(denied, ws.statement["birch"]), 0)
        case.assertEqual(number_at(sums, ws.statement["cedar"]), 0)
        case.assertEqual(number_at(sums, ws.statement["birch"]), 0)
        flagged = flags.get(denied_pair)
        case.assertFalse(flagged is not None and _number(flagged) == 1)
    if name == "shared-borrowing":
        cedar_inclusion = ws.inclusion_fact_id("autumn", "cedar")
        birch_inclusion = ws.inclusion_fact_id("autumn", "birch")
        case.assertEqual(number_at(sums, ws.statement["cedar"]), 1)
        case.assertEqual(number_at(sums, ws.statement["birch"]), 1)
        case.assertEqual(number_at(flags, cedar_inclusion), 1)
        case.assertEqual(number_at(flags, birch_inclusion), 1)
        case.assertEqual(set(flags), {cedar_inclusion, birch_inclusion})


def _run_v42(case: unittest.TestCase, name: str) -> None:
    spec = SPECS[name]
    ws = track5.Return(wages=spec.wages, amounts=spec.amounts)
    with ws.raw:
        spec.populate(ws)
        adopt_v42(ws)
        outcome = run_v42(ws.acts(), f"demo.run.track1.{name}")
        _record("v42", name, _summary(outcome, dict(ws.statement)))
        _check(case, spec, ws, outcome)
        _check_locality(case, name, ws, outcome)
        if name == "K1":
            case.assertIn("line21Explanation", outcome.model)


def _run_base(case: unittest.TestCase, name: str) -> None:
    spec = SPECS[name]
    ws = track5.Return(wages=spec.wages, amounts=spec.amounts)
    with ws.raw:
        spec.populate(ws)
        outcome = track5.run_live(ws.acts(), f"demo.run.track1.base.{name}")
        row = outcome.worksheet_row()
        text = json.dumps(outcome.line21.get("reasons"))
        _record("v41", name, {
            "disposition": outcome.line21.get("disposition"),
            "value": outcome.line21.get("value"),
            "activeCodes": outcome.line21.get("activeCodes"),
            "worksheet_code": row.get("code"),
            "worksheet_missing": row.get("missing"),
            "reason_names_both_present": "cannot be used together" in text,
        })
        case.assertEqual(outcome.line21["disposition"], "blocked")
        case.assertEqual(row["code"], "DEPENDENCY_INVALID")
        case.assertIn(BOTH_TOKEN, row["missing"])
        case.assertIn("cannot be used together", text)


class CoverDetail(unittest.TestCase):
    """One method per charter case, so a single case can be run on its own."""


class V41Base(unittest.TestCase):
    """The changes cases still fail on the adopted v41 worksheet."""


def _attach(owner: type[unittest.TestCase], prefix: str, names: tuple[str, ...] | dict[str, Spec],
            runner: Callable[[unittest.TestCase, str], None]) -> None:
    for name in names:
        def test(self: unittest.TestCase, name: str = name) -> None:
            runner(self, name)
        test.__name__ = prefix + name.replace("-", "_")
        setattr(owner, test.__name__, test)


_attach(CoverDetail, "test_case_", SPECS, _run_v42)
_attach(V41Base, "test_base_", CHANGES, _run_base)
