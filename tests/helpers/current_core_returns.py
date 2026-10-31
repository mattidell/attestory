"""Complete returns on the latest core (v66), and the runner that drives them.

Why this exists: lines 2a (Form 1099-INT box 8, Form 1099-DIV box 12), Schedule 8812
line 21 (W-2 boxes 4 and 6) and Schedule 1 line 21 (Form 1098-E) had no committed return
that reaches them on a current core. The old harnesses sit on pre-v59 bases that stop at
the Social Security chain, and a box 8 / box 12 / Form 1098-E member needs companion facts
the current-core base does not record. Each adder here takes a complete, unblocked
current-core return and records one family the way a filer does: the statement entities
are introduced, the same-statement companions are asserted, each amount is a
member-transition advancing the family horizon, and the family closure is attested at the
horizon that results.

Every adder documents what it asserts. Synthetic ``demo.*`` data only; test code only.
"""

from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping, Sequence

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.facts import fact_id_for
from packages.kernel.findings import FindingModelError
from tests import test_collect_closure as cc
from tests import test_other_dependents_credit_track1 as odc
from tests import test_w2g_gambling as w2g
from tests.test_w2g_gambling import _set_answer
from tests.test_form_1099_withholding import (
    YEAR,
    _add,
    _assert,
    _close,
    _introduce,
    _social_security_withholding,
    _unemployment_withholding,
)
from tests.test_form_1099_k_income import _handover
from tests.test_refund_or_amount_owed_track1 import _act, _attested, _elective, _finish, _load
from tests.test_withholding_closure import _horizons, _strip_closure

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "packages/content/tax/2025"
RELEASE_DIR = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"

# The latest core: package v66 / release v64 / registry v64.
PACKAGE = CONTENT / "package.core-calculations.v66.json"
PACKAGE_VERSION = "v66"
RELEASE = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v64.json"
RELEASE_VERSION = "v64"
SURFACE = PublicationSurface(RELEASE_DIR, CONTENT / "published-packages.v64.json", CONTENT)

P = "tax.us.2025."
USER = "demo.user.filer-1"

LINE2A = P + "tax-exempt-interest.line2a-total"
SCH8812_LINE21 = P + "ctc.sch8812.line-21"
SCH1_LINE21 = P + "schedule1.line21-sli-deduction"
BOX8_SUBTOTAL = P + "interest.b8-tax-exempt-subtotal"
BOX12_SUBTOTAL = P + "dividends.12-subtotal"

LINE2A_NO_INT_SCOPE = P + "line2a-scope.no-f1099int-tax-exempt"
BOX9_COMPANION = P + "f1099int.box9-specified-pab-authority"
BOX13_COMPANION = P + "f1099div.box13-specified-pab-authority"
BOX2_COMPANION = P + "f1098e.box2-checked-authority"
BOX7_COUNTRY_COMPANION = P + "f1099div.box8-country-companion"
BOX7_ORDINARY_COMPANION = P + "f1099div.box1a-ordinary"
DIRECT_FTC_ELECTION = P + "direct-ftc.election"
SCH3_LINE1 = P + "schedule3.line1-direct-ftc"
SLI_WITNESSES = tuple(
    P + "f1098e." + token for token in (
        "no-related-person-interest",
        "no-qualified-employer-plan-interest",
        "no-non-qualified-loan-component",
        "no-employer-educational-assistance-interest",
        "no-qtp-earnings-used",
    )
)

# The dependent tie-breaker answers each child needs: another person could claim the child
# (the child also lived with a grandparent), no multiple other claimants, the filer is the parent.
_TIE_BREAKER_ANSWERS = {
    "another-could-claim": "yes", "multiple-other-claimants": "no",
    "filer-is-parent": "yes", "other-is-parent": "no",
}

W2_EMPLOYER = "demo.cgd.t2.employer"
W2_SLIP = "demo.cgd.t2.w2"


# --- running ---------------------------------------------------------------------------


@dataclass
class CurrentRun:
    """One run on the latest core: every published finding by symbol, and the blocked rows."""

    pubs: dict[str, dict[str, Any]]
    blocked: list[dict[str, Any]]

    def value(self, symbol: str) -> Decimal | None:
        return Decimal(str(self.pubs[symbol]["value"])) if symbol in self.pubs else None

    def blocked_names(self) -> set[tuple[str, str]]:
        """(rule name without the tax prefix, code) for every blocked row."""
        return {(str(r.get("artifact_id", "")).replace(P, ""), str(r.get("code"))) for r in self.blocked}


def run_current_core(acts: list[dict[str, object]], run_id: str) -> CurrentRun:
    """Adopts the latest core on ``acts`` and runs them through ``live_coordinate_run``.

    Does not change ``acts``. A recorded member that contradicts a base declaration is a
    defect in the return, not something to repair here: it raises ``AssertionError`` naming the
    declaration, and the adder that records the member should have changed that answer.
    """
    try:
        return _run_once(acts, run_id)
    except FindingModelError as exc:
        found = re.search(r"contradiction: (\S+) is currently", str(exc))
        if not found:
            raise
        raise AssertionError(
            f"{run_id}: a recorded member contradicts the base declaration {found.group(1)}; "
            "the adder that records the member must change that answer (as add_tax_exempt_interest_1099int "
            "does for the line 2a scope answer)"
        ) from exc


def finished_acts(acts: list[dict[str, object]], note: str) -> list[dict[str, object]]:
    """``acts`` with the latest-core adoption and the hand-over appended, ready for a run or a session."""
    finished = _finish(
        copy.deepcopy(acts), package_path=PACKAGE, package_version=PACKAGE_VERSION,
        release_path=RELEASE, release_version=RELEASE_VERSION, note=note,
    )
    return _handover(finished, surface=SURFACE, reconfirm=True)


def _run_once(acts: list[dict[str, object]], run_id: str) -> CurrentRun:
    finished = finished_acts(acts, run_id)
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=SURFACE,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            raise AssertionError(f"{run_id} refused: {outcome.refusal.reason} {outcome.refusal.detail}")
        pubs = {str(p.finding["symbol"]): p.finding for p in outcome.publications or ()}
        blocked: list[dict[str, Any]] = []
        if outcome.output_path is not None:
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            blocked = [r for r in report.get("dispositions", []) if r.get("disposition") == "blocked"]
    return CurrentRun(pubs, blocked)


# --- recording -------------------------------------------------------------------------


def _record_members(
    acts: list[dict[str, object]],
    family: str,
    amounts: Sequence[float],
    *,
    tag: str,
    companions: Sequence[tuple[str, object]] = (),
    entities: Mapping[str, str] | None = None,
) -> list[dict[str, object]]:
    """One member per amount of ``family`` by member-transition, the family closed after the last.

    Before each member, ``companions`` ((fact type, value) pairs) are asserted on the member's
    own entities (the kernel checks a companion's presence before the member touches). When
    ``entities`` names an entity per identity key, those existing entities are used instead of
    introducing new ones (a W-2 slip already in the base). Any closure the base holds for the
    family is withdrawn first and re-attested at the final horizon.
    """
    families, mappings, fact_types, _ = cc._package_index()
    fam, mapping = families[family], mappings[family]
    ftype = fact_types[fam["member_predicate"]["fact_type"]]
    closure_type = mapping["closure_fact_type"]["id"]
    if any(f'"demo.ccr.{tag}0.' in json.dumps(a["payload"]) for a in acts):
        raise AssertionError(
            f"{family} was already recorded by this helper (tag {tag!r}): give all amounts in one call")
    out = _strip_closure(copy.deepcopy(acts), closure_type)
    cc._adopt(out, ftype["id"])
    cc._adopt(out, closure_type)
    for companion, _ in companions:
        cc._adopt(out, companion)
    horizons = _horizons(out, family)
    if not horizons:
        genesis = f"demo.ccr.{tag}.g0"
        _add(out, "horizon-genesis", {"family": {"id": family, "version": fam["version"]},
                                      "scope": {"tax-year": YEAR, "subject": "demo.primary"}, "horizon_id": genesis})
        horizons = [genesis]
    head = horizons[-1]
    for i, amount in enumerate(amounts):
        declared: list[tuple[str, str]] = []
        for key in ftype["identity_keys"]:
            if key["kind"] == "entity":
                if entities is not None and key["name"] in entities:
                    declared.append((key["name"], entities[key["name"]]))
                else:
                    eid = f"demo.ccr.{tag}{i}.{key['name']}"
                    _introduce(out, eid, key["entity_kind"])
                    declared.append((key["name"], eid))
            else:
                declared.append((key["name"], key["values"][0]))
        keys = tuple(d for d in declared if d[0] != "tax-year")
        for j, (companion, value) in enumerate(companions):
            _assert(out, f"demo.ccr.{tag}{i}.companion{j}", companion, keys, value)
        successor = f"demo.ccr.{tag}{i}.h1"
        _add(out, "member-transition", {
            "family": {"id": family, "version": fam["version"]},
            "scope": {"tax-year": YEAR, "subject": "demo.primary"},
            "member": {"action": "assert",
                       "finding": _attested(f"demo.ccr.{tag}{i}.member", fact_id_for(ftype["id"], tuple(declared)), amount)},
            "successor": {"id": successor, "predecessor": head},
        })
        head = successor
    _close(out, closure_type, head, f"demo.ccr.{tag}.closure")
    return _renumbered(out)


def _renumbered(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    """``acts`` with unique act ids and ``committed_against`` equal to each act's position.

    Withdrawing a closure removes an act, so the next appended act would reuse an id the log
    still holds (a workspace log refuses a duplicate). The first holder keeps its id.
    """
    seen: set[str] = set()
    for index, act in enumerate(acts):
        act_id = str(act["act_id"])
        if act_id in seen:
            act_id = f"{act_id}.ccr{index}"
            act["act_id"] = act_id
        seen.add(act_id)
        act["committed_against"] = index
    return acts


# --- the returns -----------------------------------------------------------------------


def base_return() -> list[dict[str, object]]:
    """A complete return on the latest core with no statement of any family.

    Single filer, wages 50,000 and 4,500 withheld on one W-2, standard deduction, no
    dependents; every closure and absence answer the latest core asks is given, so a run
    publishes the bottom line (Form 1040 line 34) with no blocked rule.
    Asserts: ``test_base_return_publishes_with_nothing_blocked``.
    """
    return w2g._w2g_return([])


def add_tax_exempt_interest_1099int(acts: list[dict[str, object]], amounts: Sequence[float]) -> list[dict[str, object]]:
    """Form 1099-INT box 8 statements, one per amount, each with its box 9 companion.

    Box 9 (specified private activity bond interest) is recorded as absent (null) on each
    statement, the only values the fact type admits besides zero. The box 8 family is closed
    after the last statement. The base's line 2a scope answer "no Form 1099-INT tax-exempt
    interest" is changed to "no" (it is the filer's own answer, contradicted by the statements),
    which selects the route that reads the box 8 subtotal. Reaches Form 1040 line 2a.

    All amounts go in one call: a second call on the same return raises ``AssertionError``.
    Does not change ``acts``; returns a new act list.
    """
    acts = copy.deepcopy(acts)
    _set_answer(acts, LINE2A_NO_INT_SCOPE, "no")
    return _record_members(acts, P + "f1099int.b8", amounts, tag="b8", companions=[(BOX9_COMPANION, None)])


def add_exempt_interest_dividends_1099div(acts: list[dict[str, object]], amounts: Sequence[float]) -> list[dict[str, object]]:
    """Form 1099-DIV box 12 statements, one per amount, each with its box 13 companion.

    Box 13 is recorded as absent (null) on each statement. The box 12 family is closed after
    the last statement. Reaches Form 1040 line 2a through the box 12 subtotal.

    All amounts go in one call: a second call on the same return raises ``AssertionError``.
    Does not change ``acts``; returns a new act list.
    """
    return _record_members(acts, P + "f1099div.12", amounts, tag="b12", companions=[(BOX13_COMPANION, None)])


def add_foreign_tax_1099div(acts: list[dict[str, object]], amounts: Sequence[float]) -> list[dict[str, object]]:
    """Form 1099-DIV box 7 statements, one per amount of foreign tax paid.

    Each statement carries its box 8 country companion ("FR") and a box 1a ordinary dividend
    of 100.00, both asserted on the statement's own entities. The base's direct foreign tax
    credit election is set to "yes" (a foreign-tax return must elect to be complete; the
    scope answers the base already gives are kept). The box 7 family is closed after the
    last statement. Reaches Schedule 3 line 1 through the box 7 subtotal.

    All amounts go in one call: a second call on the same return raises ``AssertionError``.
    Does not change ``acts``; returns a new act list.
    """
    acts = copy.deepcopy(acts)
    prefix = DIRECT_FTC_ELECTION + "|"
    acts = [a for a in acts if not str(_finding_of(a).get("fact_id", "")).startswith(prefix)]
    acts.append(_act(len(acts), "assertion", {
        "finding": _elective("demo.ccr.b7.election", f"{DIRECT_FTC_ELECTION}|tax-year={YEAR}", "yes")}))
    return _record_members(
        acts, P + "f1099div.7", amounts, tag="b7",
        companions=[(BOX7_COUNTRY_COMPANION, "FR"), (BOX7_ORDINARY_COMPANION, 100.0)])


def _finding_of(act: Mapping[str, Any]) -> Mapping[str, Any]:
    finding = act.get("payload", {}).get("finding")
    return finding if isinstance(finding, dict) else {}


def add_student_loan_interest_1098e(acts: list[dict[str, object]], amounts: Sequence[float]) -> list[dict[str, object]]:
    """Form 1098-E statements, one per amount of box 1 interest.

    Each statement carries its box 2 companion (the checked-box authority, False) and the
    five per-statement universal answers (no related-person interest, no qualified employer
    plan interest, no non-qualified loan component, no employer educational assistance, no
    qualified tuition program earnings used), all "yes". The family is closed after the last
    statement. Reaches Schedule 1 line 21 through the student loan interest worksheet.

    All amounts go in one call: a second call on the same return raises ``AssertionError``.
    Does not change ``acts``; returns a new act list.
    """
    companions: list[tuple[str, object]] = [(BOX2_COMPANION, False)] + [(w, "yes") for w in SLI_WITNESSES]
    return _record_members(acts, P + "f1098e.1", amounts, tag="sli", companions=companions)


def part_ii_b_return(*, box4: float, box6: float, wages: float = 15000.0, children: int = 3) -> list[dict[str, object]]:
    """A complete return on the latest core that reads Schedule 8812 Part II-B.

    Single filer with ``children`` qualifying children (three by default, the least that
    triggers Part II-B), wages low enough that line 20 stays below line 17, and the base W-2
    slip carrying ``box4`` and ``box6``. Reaches Schedule 8812 line 21 through the box 4 and
    box 6 totals.

    Builds its own return (takes no act list) and returns the new act list. The box 4 and
    box 6 amounts are recorded here once; the list is not meant for a second call of this kind.
    """
    kids = {f"demo-child-{i}": odc.ctc_child() for i in range(1, children + 1)}
    answers = {
        "tax.us.2025.ctc.no-other-dependent": "yes",
        "tax.us.2025.eic.age-25-under-65": "yes",
        "tax.us.2025.eic.main-home-in-us": "yes",
    }
    acts = odc.build(wages=wages, children=kids, return_answers=answers)
    acts.append(_act(len(acts), "bundle-adoption", {"bundle": _load("dtb-questions.bundle.json")}))
    for name in kids:
        for question, answer in _TIE_BREAKER_ANSWERS.items():
            fid = f"{P}dtb.child.{question}|child={name},tax-year={YEAR}"
            acts.append(_act(len(acts), "assertion", {"finding": _attested(f"demo.ccr.dtb.{question}.{name}", fid, answer)}))
    acts = odc._complete(acts)
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])
    w2g._w2g(acts, [])
    slip = {"employer": W2_EMPLOYER, "w2-slip": W2_SLIP}
    acts = _record_members(acts, P + "w2-box4", [box4], tag="w4", entities=slip)
    return _record_members(acts, P + "w2-box6", [box6], tag="w6", entities=slip)
