"""Track 1: federal tax withheld on Forms 1099-G and SSA-1099 reaches line 25b on core v59.

Every run goes through ``live_coordinate_run`` on the committed packages (core v58 /
registry v56 / release v56 and the successor core v59 / registry v57 / release v57),
on a complete return (the dependent tie-breaker Track 1 base: income, credits and the
bottom-line answers all answered). Statements are recorded the way a filer does:
the statement entities are introduced, the same-statement companions asserted, and
each family member recorded by a member-transition that advances the family horizon,
with the family closure attested at the horizon that results.

The figures asserted are the ones the coordinator produces. Each case also checks the
one thing that must hold whatever the figures are: the withholding moves line 25b,
line 33 and the bottom line by exactly the amount withheld and nothing else.
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping, cast
import unittest

from packages.derivation.explanation import explain_legacy as explain, index_derived
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.facts import fact_id_for
from packages.kernel.findings import FindingModelError
from tests.test_other_dependents_credit_track1 import JOINT_STATUS, build, _complete
from tests.test_refund_or_amount_owed_track1 import _act, _attested, _finish, _load

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages/content/tax/2025"
RELEASE_DIR = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"

PACKAGE_V58 = CONTENT / "package.core-calculations.v58.json"
RELEASE_V56 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v56.json"
SURFACE_V58 = PublicationSurface(RELEASE_DIR, CONTENT / "published-packages.v56.json", CONTENT)
PACKAGE_V59 = CONTENT / "package.core-calculations.v59.json"
RELEASE_V57 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v57.json"
SURFACE_V59 = PublicationSurface(RELEASE_DIR, CONTENT / "published-packages.v57.json", CONTENT)

USER = "demo.user.filer-1"
YEAR = "2025"
SCOPE_KEY = {"tax-year": YEAR, "subject": "demo.primary"}
NO_OTHER_DEPENDENT = "tax.us.2025.ctc.no-other-dependent"

LINE24 = "tax.us.2025.tax.line24-total-tax"
LINE25A = "tax.us.2025.payments.line25a"
LINE25B = "tax.us.2025.payments.line25b"
LINE25D = "tax.us.2025.payments.line25d"
LINE33 = "tax.us.2025.payments.line33"
LINE35A = "tax.us.2025.payments.line35a-refunded"
LINE37 = "tax.us.2025.payments.line37-amount-owed"
TOTAL_INCOME = "tax.us.2025.income.total-income"
LINES = (LINE24, LINE25A, LINE25B, LINE25D, LINE33, LINE35A, LINE37)

G_SUBTOTAL = "tax.us.2025.unemployment.b4-withholding-subtotal"
SSA_SUBTOTAL = "tax.us.2025.ssa1099.b6-withholding-subtotal"
INT_SUBTOTAL = "tax.us.2025.interest.b4-withholding-subtotal"
IRA_SUBTOTAL = "tax.us.2025.ira.box4-withholding-subtotal"
DIV_SUBTOTAL = "tax.us.2025.dividends.b4-withholding-subtotal"

G_FAMILY = "tax.us.2025.f1099g.1"
G_BOX1 = "tax.us.2025.f1099g.box1-unemployment"
G_AUTHORITY = "tax.us.2025.f1099g.box4-federal-withholding-authority"
G_B4_FAMILY = "tax.us.2025.f1099g.b4"
G_B4 = "tax.us.2025.f1099g.box4-withholding"
G_B4_CLOSURE = "tax.us.2025.f1099g.b4.source-closure"

SSA_FAMILY = "tax.us.2025.ssa1099.benefits"
SSA_B3 = "tax.us.2025.ssa1099.box3-benefits-paid"
SSA_B4 = "tax.us.2025.ssa1099.box4-repayment"
SSA_B5 = "tax.us.2025.ssa1099.box5-net-benefits"
SSA_B6_WITNESS = "tax.us.2025.ssa1099.box6-withholding"
SSA_RECIPIENT = "tax.us.2025.ssa1099.recipient"
SSA_KIND = "tax.us.2025.ssa1099.statement-kind"
SSA_LUMP = "tax.us.2025.ssa1099.lump-sum-election"
SSA_B6_FAMILY = "tax.us.2025.ssa1099.b6"
SSA_B6 = "tax.us.2025.ssa1099.box6-voluntary-withholding"
SSA_B6_CLOSURE = "tax.us.2025.ssa1099.b6.source-closure"

IRA_FAMILY = "tax.us.2025.f1099r.ira-fully-taxable"
IRA_B4_FAMILY = "tax.us.2025.f1099r.box4"
INT_B1_FAMILY = "tax.us.2025.f1099int.b1"
INT_B4_FAMILY = "tax.us.2025.f1099int.b4"
DIV_1A_FAMILY = "tax.us.2025.f1099div.1a"
DIV_B4_FAMILY = "tax.us.2025.f1099div.b4"


# --- recording ---------------------------------------------------------------


def _add(acts: list[dict[str, object]], kind: str, payload: dict[str, object]) -> None:
    acts.append(_act(len(acts), kind, payload))


def _introduce(acts: list[dict[str, object]], entity_id: str, kind: str) -> None:
    _add(acts, "entity-introduced", {"entity": {"schema": "entity.v1", "id": entity_id, "kind": kind, "label": "Synthetic"}})


def _assert(acts: list[dict[str, object]], finding_id: str, fact_type: str, keys: tuple[tuple[str, str], ...], value: object) -> None:
    fact_id = fact_id_for(fact_type, keys + (("tax-year", YEAR),))
    _add(acts, "assertion", {"finding": _attested(finding_id, fact_id, value)})


def _head(acts: list[dict[str, object]], family_id: str) -> str:
    """The family's current horizon in the base: its genesis (no transition yet)."""
    for act in acts:
        payload = cast(dict[str, Any], act["payload"])
        if act["kind"] == "horizon-genesis" and payload["family"]["id"] == family_id:
            return str(payload["horizon_id"])
    raise AssertionError(f"no horizon genesis for {family_id}")


def _transition(
    acts: list[dict[str, object]],
    family: tuple[str, str],
    predecessor: str,
    successor: str,
    finding_id: str,
    fact_type: str,
    keys: tuple[tuple[str, str], ...],
    value: object,
) -> str:
    fact_id = fact_id_for(fact_type, keys + (("tax-year", YEAR),))
    _add(
        acts,
        "member-transition",
        {
            "family": {"id": family[0], "version": family[1]},
            "scope": dict(SCOPE_KEY),
            "member": {"action": "assert", "finding": _attested(finding_id, fact_id, value)},
            "successor": {"id": successor, "predecessor": predecessor},
        },
    )
    return successor


def _close(acts: list[dict[str, object]], closure_fact: str, horizon: str, finding_id: str) -> None:
    _add(acts, "assertion", {"finding": _attested(finding_id, f"{closure_fact}|family-horizon={horizon},tax-year={YEAR}", True)})


def _unemployment(acts: list[dict[str, object]], amounts: list[float], *, authority: object = 0.0) -> None:
    """Form 1099-G box 1 statements. ``authority`` is the box-4 absent-or-zero companion
    that core v58 and earlier require beside each box-1 amount (None records none)."""
    head = _head(acts, G_FAMILY)
    for i, amount in enumerate(amounts):
        payer, stmt = f"demo.fw.g.payer.{i}", f"demo.fw.g.stmt.{i}"
        keys = (("payer", payer), ("statement", stmt))
        _introduce(acts, payer, "tax.us.unemployment-payer")
        _introduce(acts, stmt, "tax.us.1099g-statement")
        if authority is not None:
            _assert(acts, f"demo.fw.g.authority.{i}", G_AUTHORITY, keys, authority)
        head = _transition(acts, (G_FAMILY, "v1"), head, f"demo.fw.g1.h{i + 1}", f"demo.fw.g.box1.{i}", G_BOX1, keys, amount)
    _close(acts, "tax.us.2025.f1099g.1.source-closure", head, "demo.fw.g.closure.box1")


def _unemployment_withholding(acts: list[dict[str, object]], amounts: list[float | None], *, close: bool = True) -> None:
    """Form 1099-G box 4 (core v59): one entry per recorded statement; None records no amount."""
    _add(acts, "bundle-adoption", {"bundle": _load("f1099g-box4.bundle.json")})
    head = "demo.fw.g4.h0"
    _add(acts, "horizon-genesis", {"family": {"id": G_B4_FAMILY, "version": "v1"}, "scope": dict(SCOPE_KEY), "horizon_id": head})
    for i, amount in enumerate(amounts):
        if amount is None:
            continue
        keys = (("payer", f"demo.fw.g.payer.{i}"), ("statement", f"demo.fw.g.stmt.{i}"))
        head = _transition(acts, (G_B4_FAMILY, "v1"), head, f"demo.fw.g4.h{i + 1}", f"demo.fw.g.box4.{i}", G_B4, keys, amount)
    if close:
        _close(acts, G_B4_CLOSURE, head, "demo.fw.g.closure.box4")


def _social_security(acts: list[dict[str, object]], benefits: list[float], *, witness: object = 0.0) -> None:
    """Form SSA-1099 box 3/4/5 statements. ``witness`` is the box-6 absent-or-zero companion
    core v58 and earlier require beside each box-5 amount (None records none)."""
    # The Social Security Benefits Worksheet reads this residual scope answer; the base leaves it
    # unanswered because no base statement needed it.
    scope_fact = "tax.us.2025.schedule1-adjustments-scope.no-line24z-writein"
    if not any(str(cast(dict[str, Any], a["payload"]).get("finding", {}).get("fact_id", "")).startswith(scope_fact + "|") for a in acts):
        _add(acts, "assertion", {"finding": _attested("demo.fw.ssa.scope.no-line24z-writein", f"{scope_fact}|tax-year={YEAR}", "yes")})
    head = _head(acts, SSA_FAMILY)
    for i, amount in enumerate(benefits):
        stmt = f"demo.fw.ssa.stmt.{i}"
        keys = (("statement", stmt),)
        _introduce(acts, stmt, "tax.us.ssa1099-statement")
        _assert(acts, f"demo.fw.ssa.b3.{i}", SSA_B3, keys, amount)
        _assert(acts, f"demo.fw.ssa.b4.{i}", SSA_B4, keys, 0.0)
        if witness is not None:
            _assert(acts, f"demo.fw.ssa.witness.{i}", SSA_B6_WITNESS, keys, witness)
        _assert(acts, f"demo.fw.ssa.recipient.{i}", SSA_RECIPIENT, keys, "taxpayer")
        _assert(acts, f"demo.fw.ssa.kind.{i}", SSA_KIND, keys, "ssa-1099")
        _assert(acts, f"demo.fw.ssa.lump.{i}", SSA_LUMP, keys, False)
        head = _transition(acts, (SSA_FAMILY, "v1"), head, f"demo.fw.ssa.h{i + 1}", f"demo.fw.ssa.b5.{i}", SSA_B5, keys, amount)
    _close(acts, "tax.us.2025.ssa1099.source-closure", head, "demo.fw.ssa.closure.benefits")


def _social_security_withholding(acts: list[dict[str, object]], amounts: list[float | None], *, close: bool = True) -> None:
    """Form SSA-1099 box 6 (core v59): one entry per recorded statement; None records no amount."""
    _add(acts, "bundle-adoption", {"bundle": _load("ssa1099-box6.bundle.json")})
    head = "demo.fw.ssa6.h0"
    _add(acts, "horizon-genesis", {"family": {"id": SSA_B6_FAMILY, "version": "v1"}, "scope": dict(SCOPE_KEY), "horizon_id": head})
    for i, amount in enumerate(amounts):
        if amount is None:
            continue
        keys = (("statement", f"demo.fw.ssa.stmt.{i}"),)
        head = _transition(acts, (SSA_B6_FAMILY, "v1"), head, f"demo.fw.ssa6.h{i + 1}", f"demo.fw.ssa.box6.{i}", SSA_B6, keys, amount)
    if close:
        _close(acts, SSA_B6_CLOSURE, head, "demo.fw.ssa.closure.box6")


def _retirement(acts: list[dict[str, object]], distribution: float, withheld: float) -> None:
    """One IRA-family Form 1099-R: box 1 (= box 2a) and its box 4 amount."""
    payer, stmt = "demo.fw.r.payer", "demo.fw.r.stmt"
    keys = (("payer", payer), ("statement", stmt))
    _introduce(acts, payer, "tax.us.ira-payer")
    _introduce(acts, stmt, "tax.us.1099r-statement")
    _assert(acts, "demo.fw.r.box2a", "tax.us.2025.f1099r.ira-box2a-taxable-amount", keys, distribution)
    _assert(acts, "demo.fw.r.checkbox", "tax.us.2025.f1099r.ira-sep-simple-checkbox", keys, True)
    _assert(acts, "demo.fw.r.code", "tax.us.2025.f1099r.distribution-code", keys, "7")
    _assert(acts, "demo.fw.r.box2b", "tax.us.2025.f1099r.box2b-not-determined", keys, False)
    head = _transition(
        acts, (IRA_FAMILY, "v2"), _head(acts, IRA_FAMILY), "demo.fw.r.h1", "demo.fw.r.box1",
        "tax.us.2025.f1099r.ira-box1-taxable-distribution", keys, distribution,
    )
    _close(acts, "tax.us.2025.f1099r.ira-fully-taxable.source-closure", head, "demo.fw.r.closure.box1")
    b4_head = _transition(
        acts, (IRA_B4_FAMILY, "v1"), _head(acts, IRA_B4_FAMILY), "demo.fw.r.b4.h1", "demo.fw.r.box4",
        "tax.us.2025.f1099r.ira-box4-withholding", keys, withheld,
    )
    _close(acts, "tax.us.2025.f1099r.box4.source-closure", b4_head, "demo.fw.r.closure.box4")


def _interest(acts: list[dict[str, object]], statements: list[tuple[float, float | None]]) -> None:
    """Form 1099-INT statements: box 1 interest, and the box 4 answer when there is one."""
    b1_head = _head(acts, INT_B1_FAMILY)
    b4_head = _head(acts, INT_B4_FAMILY)
    for i, (box1, box4) in enumerate(statements):
        payer, stmt = f"demo.fw.int.payer.{i}", f"demo.fw.int.stmt.{i}"
        keys = (("payer", payer), ("statement", stmt))
        _introduce(acts, payer, "tax.us.interest-payer")
        _introduce(acts, stmt, "tax.us.1099int-statement")
        b1_head = _transition(
            acts, (INT_B1_FAMILY, "v1"), b1_head, f"demo.fw.int.b1.h{i + 1}", f"demo.fw.int.box1.{i}",
            "tax.us.2025.f1099int.box1-interest", keys, box1,
        )
        if box4 is not None:
            b4_head = _transition(
                acts, (INT_B4_FAMILY, "v1"), b4_head, f"demo.fw.int.b4.h{i + 1}", f"demo.fw.int.box4.{i}",
                "tax.us.2025.f1099int.box4-withholding", keys, box4,
            )
    _close(acts, "tax.us.2025.f1099int.b1.source-closure", b1_head, "demo.fw.int.closure.box1")
    _close(acts, "tax.us.2025.f1099int.b4.source-closure", b4_head, "demo.fw.int.closure.box4")


def _dividends(acts: list[dict[str, object]], statements: list[tuple[float, float | None]]) -> None:
    """Form 1099-DIV statements: box 1a dividends, and the box 4 answer when there is one."""
    a_head = _head(acts, DIV_1A_FAMILY)
    b4_head = _head(acts, DIV_B4_FAMILY)
    for i, (box1a, box4) in enumerate(statements):
        payer, stmt = f"demo.fw.div.payer.{i}", f"demo.fw.div.stmt.{i}"
        keys = (("payer", payer), ("statement", stmt))
        _introduce(acts, payer, "tax.us.dividend-payer")
        _introduce(acts, stmt, "tax.us.1099div-statement")
        a_head = _transition(
            acts, (DIV_1A_FAMILY, "v1"), a_head, f"demo.fw.div.1a.h{i + 1}", f"demo.fw.div.box1a.{i}",
            "tax.us.2025.f1099div.box1a-ordinary", keys, box1a,
        )
        if box4 is not None:
            b4_head = _transition(
                acts, (DIV_B4_FAMILY, "v1"), b4_head, f"demo.fw.div.b4.h{i + 1}", f"demo.fw.div.box4.{i}",
                "tax.us.2025.f1099div.box4-withholding", keys, box4,
            )
    _close(acts, "tax.us.2025.f1099div.1a.source-closure", a_head, "demo.fw.div.closure.box1a")
    _close(acts, "tax.us.2025.f1099div.b4.source-closure", b4_head, "demo.fw.div.closure.box4")


def _retirements(acts: list[dict[str, object]], statements: list[tuple[float, float | None]]) -> None:
    """IRA-family Forms 1099-R: box 1 (= box 2a), and the box 4 answer when there is one."""
    head = _head(acts, IRA_FAMILY)
    b4_head = _head(acts, IRA_B4_FAMILY)
    for i, (distribution, withheld) in enumerate(statements):
        payer, stmt = f"demo.fw.r.payer.{i}", f"demo.fw.r.stmt.{i}"
        keys = (("payer", payer), ("statement", stmt))
        _introduce(acts, payer, "tax.us.ira-payer")
        _introduce(acts, stmt, "tax.us.1099r-statement")
        _assert(acts, f"demo.fw.r.box2a.{i}", "tax.us.2025.f1099r.ira-box2a-taxable-amount", keys, distribution)
        _assert(acts, f"demo.fw.r.checkbox.{i}", "tax.us.2025.f1099r.ira-sep-simple-checkbox", keys, True)
        _assert(acts, f"demo.fw.r.code.{i}", "tax.us.2025.f1099r.distribution-code", keys, "7")
        _assert(acts, f"demo.fw.r.box2b.{i}", "tax.us.2025.f1099r.box2b-not-determined", keys, False)
        head = _transition(
            acts, (IRA_FAMILY, "v2"), head, f"demo.fw.r.h{i + 1}", f"demo.fw.r.box1.{i}",
            "tax.us.2025.f1099r.ira-box1-taxable-distribution", keys, distribution,
        )
        if withheld is not None:
            b4_head = _transition(
                acts, (IRA_B4_FAMILY, "v1"), b4_head, f"demo.fw.r.b4.h{i + 1}", f"demo.fw.r.box4.{i}",
                "tax.us.2025.f1099r.ira-box4-withholding", keys, withheld,
            )
    _close(acts, "tax.us.2025.f1099r.ira-fully-taxable.source-closure", head, "demo.fw.r.closure.box1")
    _close(acts, "tax.us.2025.f1099r.box4.source-closure", b4_head, "demo.fw.r.closure.box4")


def _w2_withholding(acts: list[dict[str, object]], amount: float) -> None:
    """Sets the base's one W-2 box 2 amount (the base records zero)."""
    hits = 0
    for act in acts:
        finding = cast(dict[str, Any], act["payload"]).get("finding")
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith("tax.us.2025.w2.box2-withholding|"):
            finding["value"] = amount
            hits += 1
    assert hits == 1, hits


def _base(*, wages: float, w2_withheld: float = 0.0, joint: bool = False) -> list[dict[str, object]]:
    status: dict[str, Any] = {"filing_status": JOINT_STATUS} if joint else {}
    acts = _complete(build(wages=wages, children={}, return_answers={NO_OTHER_DEPENDENT: "yes"}, **status))
    _w2_withholding(acts, w2_withheld)
    return acts


def _close_new_families_empty(acts: list[dict[str, object]]) -> None:
    """The two closures a v58 answer set is asked on v59: no box-4 / box-6 amount recorded."""
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])


# --- running -----------------------------------------------------------------


@dataclass
class Run:
    pubs: dict[str, dict[str, Any]]
    blocked: list[dict[str, Any]]

    def value(self, symbol: str) -> Decimal:
        return Decimal(str(self.pubs[symbol]["value"]))

    def lines(self) -> dict[str, Decimal | None]:
        return {s: (Decimal(str(self.pubs[s]["value"])) if s in self.pubs else None) for s in LINES}

    def net(self) -> Decimal:
        """Refund minus amount owed: the bottom line as one signed figure."""
        return self.value(LINE35A) - self.value(LINE37)

    def blocked_on(self, artifact_token: str) -> dict[str, Any]:
        for row in self.blocked:
            if str(row.get("artifact_id", "")).endswith(artifact_token):
                return row
        raise AssertionError(f"{artifact_token} is not blocked")


def _finished(acts: list[dict[str, object]], run_id: str, *, core: str) -> list[dict[str, object]]:
    if core == "v59":
        package, version, release, rel_version = PACKAGE_V59, "v59", RELEASE_V57, "v57"
    else:
        package, version, release, rel_version = PACKAGE_V58, "v58", RELEASE_V56, "v56"
    return _finish(
        copy.deepcopy(acts), package_path=package, package_version=version,
        release_path=release, release_version=rel_version, note=run_id,
    )


def _recorded_handover(finished: list[dict[str, object]], *, reconfirm: bool) -> list[dict[str, object]]:
    """Hands the Social Security chain of ``finished`` over with the recorder's own staging (the
    version comes from the adopted package) and, when ``reconfirm``, attests the closure on the
    successor horizon."""
    from packages.derivation.loader import DerivationSchemas
    from packages.tax.loader import (
        install_domain_companion_equalities,
        install_domain_companion_presence,
        install_domain_declaration_signal_contradictions,
    )
    from packages.tax.ssa_family_handover import ssa_family_version_for_acts, stage_ssa_family_handover

    # The registry a live run projects with (live.py installs the same domain maps), so the log
    # is folded exactly as the run folds it.
    registry = DerivationSchemas().registry
    install_domain_companion_presence(registry)
    install_domain_companion_equalities(registry)
    install_domain_declaration_signal_contradictions(registry)
    version = ssa_family_version_for_acts(finished, actor=USER, surface=SURFACE_V59)
    act, _ = stage_ssa_family_handover(
        finished, registry, actor=USER, at="2026-10-28T12:00:00Z", family_version=version
    )
    out = copy.deepcopy(finished) + [cast(dict[str, object], act)]
    if reconfirm:
        horizon = act["payload"]["successor"]["horizon_id"]
        closure = _act(
            len(out), "assertion",
            {"finding": _attested(
                "demo.fw.ssa.reconfirm",
                f"tax.us.2025.ssa1099.source-closure|family-horizon={horizon},tax-year={YEAR}",
                True,
            )},
        )
        closure["actor"] = USER
        out.append(closure)
    return out


def _run(acts: list[dict[str, object]], run_id: str, *, core: str, ssa: str = "reconfirmed") -> Run:
    """Runs ``acts`` on core v58, or on core v59 with the Social Security chain ``ssa``:
    ``"v1"`` (not handed over), ``"handed"`` (handed over, not re-confirmed) or ``"reconfirmed"``."""
    finished = _finished(acts, run_id, core=core)
    if core == "v59" and ssa != "v1":
        finished = _recorded_handover(finished, reconfirm=ssa == "reconfirmed")
    surface = SURFACE_V59 if core == "v59" else SURFACE_V58
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
            surface=surface,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            raise AssertionError(f"{run_id} refused: {outcome.refusal.reason} {outcome.refusal.detail}")
        pubs = {str(p.finding["symbol"]): p.finding for p in outcome.publications or ()}
        blocked: list[dict[str, Any]] = []
        if outcome.output_path is not None:
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            blocked = [r for r in report.get("dispositions", []) if r.get("disposition") == "blocked"]
    return Run(pubs, blocked)


def _roots(run: Run) -> dict[str, tuple[Any, list[str]]]:
    """Blocked rows that are not merely waiting on another blocked line: artifact -> (code, missing)."""
    return {
        str(r["artifact_id"]): (r["code"], list(r["missing"]))
        for r in run.blocked
        if r["code"] != "DEPENDENCY_ABSENT"
    }


def _walk_ids(run: Run, symbol: str) -> tuple[set[str], set[str]]:
    """Finding ids and symbols reached by the explanation walk from a published line."""
    tree = explain(str(run.pubs[symbol]["id"]), role="output", derived=index_derived(list(run.pubs.values())))
    finding_ids: set[str] = set()
    symbols: set[str] = set()

    def walk(node: Any) -> None:
        if node.finding_id:
            finding_ids.add(node.finding_id)
        if node.symbol:
            symbols.add(node.symbol)
        for child in node.children:
            walk(child)

    walk(tree)
    return finding_ids, symbols


def _unemployment_return(*, withheld: float | None, wages: float = 50000.0, w2: float = 4500.0) -> list[dict[str, object]]:
    acts = _base(wages=wages, w2_withheld=w2)
    _unemployment(acts, [6000.0], authority=None)
    _unemployment_withholding(acts, [withheld])
    _social_security_withholding(acts, [])
    return acts


def _figures(run: Run) -> dict[str, str | None]:
    """Line 24, 25a, 25b, 25d, 33, 35a and 37, in that order, as the coordinator published them."""
    return {s.rsplit(".", 1)[-1]: (None if v is None else str(v)) for s, v in run.lines().items()}


def _expect(run: Run, tax: str, l25a: str, l25b: str, l25d: str, l33: str, refund: str, owed: str) -> None:
    assert _figures(run) == {
        "line24-total-tax": tax, "line25a": l25a, "line25b": l25b, "line25d": l25d,
        "line33": l33, "line35a-refunded": refund, "line37-amount-owed": owed,
    }, _figures(run)


class UnemploymentWithholding(unittest.TestCase):
    def test_600_withheld_on_6000_moves_25b_payments_and_bottom_line_by_exactly_600(self) -> None:
        without = _run(_unemployment_return(withheld=None), "demo.fw.g0", core="v59")
        withheld = _run(_unemployment_return(withheld=600.0), "demo.fw.g600", core="v59")
        # Without any box 4 amount: tax 4595 against 4500 withheld on the W-2 leaves 95 owed.
        _expect(without, "4595", "4500", "0", "4500", "4500", "0", "95")
        # With 600 withheld: line 25b, 25d and 33 each rise by 600 and the 95 owed becomes a 505 refund.
        _expect(withheld, "4595", "4500", "600", "5100", "5100", "505", "0")
        self.assertEqual(withheld.value(LINE25B) - without.value(LINE25B), 600)
        self.assertEqual(withheld.value(LINE33) - without.value(LINE33), 600)
        self.assertEqual(withheld.net() - without.net(), 600)
        self.assertEqual(withheld.value(LINE24), without.value(LINE24))
        self.assertEqual(withheld.value(G_SUBTOTAL), 600)

    def test_the_explanation_walks_from_line_25b_to_the_1099g_statement(self) -> None:
        run = _run(_unemployment_return(withheld=600.0), "demo.fw.g.walk", core="v59")
        finding_ids, symbols = _walk_ids(run, LINE25B)
        self.assertIn(G_SUBTOTAL, symbols)
        self.assertIn("demo.fw.g.box4.0", finding_ids)
        # The box-1 income finding is not what line 25b read; only the box-4 amount is.
        self.assertNotIn("demo.fw.g.box1.0", finding_ids)

    def test_a_joint_return_with_a_1099g_for_each_spouse_adds_both(self) -> None:
        acts = _base(wages=80000.0, w2_withheld=7000.0, joint=True)
        _unemployment(acts, [5000.0, 4000.0], authority=None)
        _unemployment_withholding(acts, [500.0, 400.0])
        _social_security_withholding(acts, [])
        run = _run(acts, "demo.fw.joint", core="v59")
        _expect(run, "6426", "7000", "900", "7900", "7900", "1474", "0")
        self.assertEqual(run.value(G_SUBTOTAL), 900)
        finding_ids, _ = _walk_ids(run, LINE25B)
        self.assertTrue({"demo.fw.g.box4.0", "demo.fw.g.box4.1"} <= finding_ids)

    def test_a_statement_with_no_box_4_amount_adds_nothing(self) -> None:
        acts = _base(wages=80000.0, w2_withheld=7000.0, joint=True)
        _unemployment(acts, [5000.0, 4000.0], authority=None)
        _unemployment_withholding(acts, [500.0, None])
        _social_security_withholding(acts, [])
        run = _run(acts, "demo.fw.joint.one", core="v59")
        self.assertEqual(run.value(G_SUBTOTAL), 500)
        self.assertEqual(run.value(LINE25B), 500)


def _social_security_return(*, withheld: float | None, retirement: tuple[float, float] | None = None) -> list[dict[str, object]]:
    acts = _base(wages=40000.0, w2_withheld=2500.0)
    _social_security(acts, [12000.0], witness=None)
    if retirement is not None:
        _retirement(acts, *retirement)
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [withheld])
    return acts


class SocialSecurityWithholding(unittest.TestCase):
    def test_box_6_withholding_alone_reaches_25b_payments_and_the_bottom_line(self) -> None:
        without = _run(_social_security_return(withheld=None), "demo.fw.ssa0", core="v59")
        withheld = _run(_social_security_return(withheld=800.0), "demo.fw.ssa800", core="v59")
        _expect(without, "3899", "2500", "0", "2500", "2500", "0", "1399")
        _expect(withheld, "3899", "2500", "800", "3300", "3300", "0", "599")
        self.assertEqual(withheld.value(LINE25B) - without.value(LINE25B), 800)
        self.assertEqual(withheld.net() - without.net(), 800)
        self.assertEqual(withheld.value(LINE24), without.value(LINE24))
        self.assertEqual(withheld.value(SSA_SUBTOTAL), 800)
        finding_ids, symbols = _walk_ids(withheld, LINE25B)
        self.assertIn(SSA_SUBTOTAL, symbols)
        self.assertIn("demo.fw.ssa.box6.0", finding_ids)

    def test_box_6_withholding_with_a_1099r_box_4_amount_adds_both(self) -> None:
        alone = _run(_social_security_return(withheld=800.0), "demo.fw.ssa.alone", core="v59")
        both = _run(_social_security_return(withheld=800.0, retirement=(10000.0, 1200.0)), "demo.fw.ssa.r", core="v59")
        # The 10,000 distribution is taxed at 12 percent here (1200 more tax) and 1200 is withheld on
        # it, so the amount owed does not move.
        _expect(both, "5099", "2500", "2000", "4500", "4500", "0", "599")
        self.assertEqual(both.value(SSA_SUBTOTAL), 800)
        self.assertEqual(both.value(IRA_SUBTOTAL), 1200)
        self.assertEqual(both.value(LINE25B) - alone.value(LINE25B), 1200)
        self.assertEqual(both.value(LINE24) - alone.value(LINE24), 1200)
        self.assertEqual(both.net(), alone.net())
        finding_ids, _ = _walk_ids(both, LINE25B)
        self.assertTrue({"demo.fw.ssa.box6.0", "demo.fw.r.box4"} <= finding_ids)


def _v58_answer_set() -> list[dict[str, object]]:
    """Unemployment and Social Security with no withholding, recorded the way core v58 asks."""
    acts = _base(wages=50000.0, w2_withheld=4500.0)
    _unemployment(acts, [6000.0])
    _social_security(acts, [12000.0])
    return acts


class SuccessionFromV58(unittest.TestCase):
    def test_before_the_social_security_handover_a_v58_answer_set_blocks_on_three_families(self) -> None:
        acts = _v58_answer_set()
        _expect(_run(acts, "demo.fw.succ.v58", core="v58"), "6019", "4500", "0", "4500", "4500", "0", "1519")
        v59 = _run(acts, "demo.fw.succ.v59.open", core="v59", ssa="v1")
        self.assertEqual(
            _roots(v59),
            {
                "tax.us.2025.rule.f1099g-b4-subtotal": ("SOURCE_SET_UNCLOSED", [G_B4_FAMILY]),
                "tax.us.2025.rule.ssa1099-b6-subtotal": ("SOURCE_SET_UNCLOSED", [SSA_B6_FAMILY]),
                "tax.us.2025.rule.ss-benefits-worksheet": ("SOURCE_SET_UNCLOSED", [SSA_FAMILY]),
            },
        )
        # Everything else blocked is a consequence of these three.
        self.assertTrue(all(r["code"] in {"SOURCE_SET_UNCLOSED", "DEPENDENCY_ABSENT"} for r in v59.blocked))
        self.assertEqual(list(v59.blocked_on("form1040-line25b")["missing"]), [G_SUBTOTAL, SSA_SUBTOTAL])
        self.assertNotIn(LINE25B, v59.pubs)

    def test_after_the_handover_and_before_the_reconfirmation_only_the_closure_blocks(self) -> None:
        closed = _v58_answer_set()
        _close_new_families_empty(closed)
        run = _run(closed, "demo.fw.succ.handed", core="v59", ssa="handed")
        self.assertEqual(_roots(run), {"tax.us.2025.rule.ss-benefits-worksheet": ("SOURCE_SET_UNCLOSED", [SSA_FAMILY])})
        self.assertIn(LINE25B, run.pubs)
        self.assertNotIn("tax.us.2025.social-security.line6b", run.pubs)
        self.assertNotIn(LINE37, run.pubs)

    def test_after_the_reconfirmation_and_both_closures_every_published_symbol_equals_its_v58_value(self) -> None:
        acts = _v58_answer_set()
        v58 = _run(acts, "demo.fw.succ.v58b", core="v58")
        closed = copy.deepcopy(acts)
        _close_new_families_empty(closed)
        v59 = _run(closed, "demo.fw.succ.v59.closed", core="v59")
        self.assertEqual(v59.blocked, [])
        self.assertEqual({s: f["value"] for s, f in v58.pubs.items()}, {s: v59.pubs[s]["value"] for s in v58.pubs})
        self.assertEqual(set(v59.pubs) - set(v58.pubs), {G_SUBTOTAL, SSA_SUBTOTAL})
        self.assertEqual(v59.value(G_SUBTOTAL), 0)
        self.assertEqual(v59.value(SSA_SUBTOTAL), 0)
        self.assertEqual(v59.lines(), v58.lines())

    def test_a_v58_answer_set_with_no_ssa_1099_goes_through_the_same_path(self) -> None:
        acts = _base(wages=50000.0, w2_withheld=4500.0)
        _unemployment(acts, [6000.0])
        v58 = _run(acts, "demo.fw.succ.empty.v58", core="v58")
        closed = copy.deepcopy(acts)
        _close_new_families_empty(closed)
        before = _run(closed, "demo.fw.succ.empty.v1", core="v59", ssa="v1")
        self.assertEqual(_roots(before), {"tax.us.2025.rule.ssa1099-benefits-subtotal": ("SOURCE_SET_UNCLOSED", [SSA_FAMILY])})
        handed = _run(closed, "demo.fw.succ.empty.handed", core="v59", ssa="handed")
        self.assertEqual(_roots(handed), {"tax.us.2025.rule.ssa1099-benefits-subtotal": ("SOURCE_SET_UNCLOSED", [SSA_FAMILY])})
        done = _run(closed, "demo.fw.succ.empty.done", core="v59")
        self.assertEqual(done.blocked, [])
        _expect(done, "4595", "4500", "0", "4500", "4500", "0", "95")
        self.assertEqual(done.lines(), v58.lines())
        self.assertEqual(done.value("tax.us.2025.social-security.line6b"), 0)

    def test_an_unclosed_new_family_blocks_naming_the_family(self) -> None:
        acts = _base(wages=50000.0, w2_withheld=4500.0)
        _unemployment(acts, [6000.0], authority=None)
        _unemployment_withholding(acts, [], close=False)
        _social_security_withholding(acts, [])
        run = _run(acts, "demo.fw.unclosed.g", core="v59")
        row = run.blocked_on("rule.f1099g-b4-subtotal")
        self.assertEqual((row["code"], list(row["missing"])), ("SOURCE_SET_UNCLOSED", [G_B4_FAMILY]))
        self.assertEqual(list(run.blocked_on("rule.form1040-line25b")["missing"]), [G_SUBTOTAL])
        self.assertNotIn(LINE25B, run.pubs)
        self.assertNotIn(G_SUBTOTAL, run.pubs)

        ssa = _base(wages=40000.0, w2_withheld=2500.0)
        _social_security(ssa, [12000.0], witness=None)
        _unemployment_withholding(ssa, [])
        _social_security_withholding(ssa, [], close=False)
        run = _run(ssa, "demo.fw.unclosed.ssa", core="v59")
        row = run.blocked_on("rule.ssa1099-b6-subtotal")
        self.assertEqual((row["code"], list(row["missing"])), ("SOURCE_SET_UNCLOSED", [SSA_B6_FAMILY]))
        self.assertNotIn(LINE25B, run.pubs)


    def test_a_recorded_amount_counts_before_its_closure_exactly_as_1099int_box_4_does(self) -> None:
        """The standing posture of the box-4 families: closure is read only when no amount is recorded."""
        g = _base(wages=50000.0, w2_withheld=4500.0)
        _unemployment(g, [6000.0], authority=None)
        _unemployment_withholding(g, [600.0], close=False)
        _social_security_withholding(g, [])
        g59 = _run(g, "demo.fw.member.noclosure.g", core="v59")
        self.assertEqual(g59.value(LINE25B), 600)
        self.assertEqual(g59.blocked, [])

        i = _base(wages=50000.0, w2_withheld=4500.0)
        _interest(i, [(500.0, 50.0)])
        i.pop()  # the box-4 closure attested last by the recorder
        i58 = _run(i, "demo.fw.member.noclosure.int", core="v58")
        self.assertEqual(i58.value(LINE25B), 50)
        self.assertEqual(i58.blocked, [])


class EarlierPackagesStillRefuse(unittest.TestCase):
    def test_a_nonzero_1099g_box_4_is_still_refused_on_v58(self) -> None:
        acts = _base(wages=50000.0, w2_withheld=4500.0)
        _unemployment(acts, [6000.0], authority=600.0)
        with self.assertRaises(FindingModelError) as raised:
            _run(acts, "demo.fw.v58.nonzero", core="v58")
        self.assertIn(G_AUTHORITY, str(raised.exception))

    def test_a_nonzero_ssa_box_6_is_still_refused_on_v58(self) -> None:
        acts = _base(wages=40000.0, w2_withheld=2500.0)
        _social_security(acts, [12000.0], witness=800.0)
        with self.assertRaises(FindingModelError) as raised:
            _run(acts, "demo.fw.v58.ssa.nonzero", core="v58")
        self.assertIn(SSA_B6_WITNESS, str(raised.exception))

    def test_a_log_that_adopts_v59_is_refused_on_v58_by_the_registry_check(self) -> None:
        for name, acts in (
            ("g", _unemployment_return(withheld=600.0)),
            ("ssa", _social_security_return(withheld=800.0)),
        ):
            finished = _recorded_handover(_finished(acts, f"demo.fw.adopted.{name}", core="v59"), reconfirm=True)
            adoptions = [a for a in finished if a["kind"] == "package-adoption"]
            self.assertEqual([cast(Mapping[str, Any], cast(Mapping[str, Any], a["payload"])["package"])["version"] for a in adoptions], ["v59"])
            with TemporaryDirectory() as tmp:
                outcome = live_coordinate_run(
                    WorkspaceCapability(Path(tmp) / "L"),
                    repo_root=ROOT,
                    authoritative_acts=finished,
                    workspace_revision=len(finished),
                    run_scope={"jurisdiction": "us", "year": YEAR},
                    scope_user=USER,
                    request={"schema": "run-request.v1"},
                    run_id=f"demo.fw.adopted.{name}.on.v58",
                    governance_pins=[],
                    surface=SURFACE_V58,
                    output_name="out.json",
                )
            self.assertIsNotNone(outcome.refusal)
            assert outcome.refusal is not None
            self.assertEqual(outcome.refusal.reason, "REGISTRY_CHECKSUM_MISMATCH")

    def test_a_log_recorded_on_v59_with_1099g_withholding_is_refused_on_v58_naming_the_companion(self) -> None:
        acts = _unemployment_return(withheld=600.0)
        self.assertEqual(_run(acts, "demo.fw.v59.ok", core="v59").value(LINE25B), 600)
        with self.assertRaises(FindingModelError) as raised:
            _run(acts, "demo.fw.v59.on.v58", core="v58")
        message = str(raised.exception)
        self.assertIn("companion presence violated", message)
        self.assertIn(G_AUTHORITY, message)

    def test_a_log_recorded_on_v59_with_ssa_withholding_is_refused_on_v58_naming_the_companion(self) -> None:
        acts = _social_security_return(withheld=800.0)
        self.assertEqual(_run(acts, "demo.fw.v59.ssa.ok", core="v59").value(LINE25B), 800)
        with self.assertRaises(FindingModelError) as raised:
            _run(acts, "demo.fw.v59.ssa.on.v58", core="v58")
        message = str(raised.exception)
        self.assertIn("companion presence violated", message)
        self.assertIn(SSA_B6_WITNESS, message)


class SocialSecurityHandover(unittest.TestCase):
    def test_the_handover_is_refused_under_v58_because_v58_declares_the_family_the_chain_is_on(self) -> None:
        from packages.derivation.loader import DerivationSchemas
        from packages.tax.loader import install_domain_companion_presence
        from packages.tax.ssa_family_handover import (
            SsaHandoverRefused,
            ssa_family_version_for_acts,
            stage_ssa_family_handover,
        )

        finished = _finished(_v58_answer_set(), "demo.fw.handover.v58", core="v58")
        version = ssa_family_version_for_acts(finished, actor=USER, surface=SURFACE_V58)
        self.assertEqual(version, "v1")
        registry = DerivationSchemas().registry
        install_domain_companion_presence(registry)
        with self.assertRaises(SsaHandoverRefused) as raised:
            stage_ssa_family_handover(finished, registry, actor=USER, at="2026-10-28T12:00:00Z", family_version=version)
        self.assertIn("nothing to hand over", str(raised.exception))
        # And v59 declares v2, so the same log accepts the handover once v59 is the adopted package.
        v59 = _finished(_v58_answer_set(), "demo.fw.handover.v59", core="v59")
        self.assertEqual(ssa_family_version_for_acts(v59, actor=USER, surface=SURFACE_V59), "v2")

    def test_a_second_handover_is_refused(self) -> None:
        from packages.derivation.loader import DerivationSchemas
        from packages.tax.loader import install_domain_companion_presence
        from packages.tax.ssa_family_handover import SsaHandoverRefused, stage_ssa_family_handover

        handed = _recorded_handover(_finished(_v58_answer_set(), "demo.fw.handover.twice", core="v59"), reconfirm=False)
        registry = DerivationSchemas().registry
        install_domain_companion_presence(registry)
        with self.assertRaises(SsaHandoverRefused) as raised:
            stage_ssa_family_handover(handed, registry, actor=USER, at="2026-10-28T12:05:00Z", family_version="v2")
        self.assertIn("already on v2", str(raised.exception))
        # The kernel refuses it too (ADR-0079): replaying the same handover act cannot be folded.
        from packages.kernel.findings import project

        replay = copy.deepcopy(handed[-1])
        replay["act_id"] = "ssa.handover.replay"
        replay["committed_against"] = len(handed)
        with self.assertRaises(Exception) as kernel:
            project(tuple(copy.deepcopy(handed)) + (replay,), registry)
        self.assertIn("predecessor horizon is not current", str(kernel.exception))

    def test_the_durable_recorder_hands_over_once_on_a_real_log(self) -> None:
        from packages.kernel.act_log import ActLog
        from packages.tax.loader import tax_registry
        from packages.tax.ssa_family_handover import SsaHandoverRefused, hand_over_ssa_family_durably

        registry = tax_registry()
        genesis = _act(0, "horizon-genesis", {
            "family": {"id": SSA_FAMILY, "version": "v1"}, "scope": dict(SCOPE_KEY), "horizon_id": "demo.fw.log.h0",
        })
        genesis["actor"] = USER
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "ws"
            workspace.mkdir()
            log = ActLog(workspace, registry, undeclared_test_log=True)
            log.append_batch([genesis], expected_revision=0)
            # No adoption yet: the chain stays on v1, so there is nothing to hand over.
            with self.assertRaises(SsaHandoverRefused):
                hand_over_ssa_family_durably(
                    log, registry, submission_id="demo.fw.log.0", actor=USER, at="2026-10-28T12:00:00Z",
                    expected_revision=1, surface=SURFACE_V59,
                )
            # A stale reviewed revision is refused before anything is written.
            with self.assertRaises(SsaHandoverRefused):
                hand_over_ssa_family_durably(
                    log, registry, submission_id="demo.fw.log.1", actor=USER, at="2026-10-28T12:00:00Z",
                    expected_revision=0, family_version="v2",
                )
            done = hand_over_ssa_family_durably(
                log, registry, submission_id="demo.fw.log.2", actor=USER, at="2026-10-28T12:00:00Z",
                expected_revision=1, family_version="v2",
            )
            self.assertEqual(done["revision"], 2)
            self.assertEqual(log.read().acts[-1]["kind"], "family-handover")
            with self.assertRaises(SsaHandoverRefused):
                hand_over_ssa_family_durably(
                    log, registry, submission_id="demo.fw.log.3", actor=USER, at="2026-10-28T12:01:00Z",
                    expected_revision=2, family_version="v2",
                )

    def test_the_explanation_of_line_6a_and_6b_cites_the_v2_family(self) -> None:
        run = _run(_social_security_return(withheld=800.0), "demo.fw.explain.6ab", core="v59")
        derived = index_derived(list(run.pubs.values()))
        for symbol in ("tax.us.2025.social-security.line6a", "tax.us.2025.social-security.line6b"):
            cited: set[tuple[str, str]] = set()
            seen: set[str] = set()

            def walk(finding_id: str) -> None:
                if finding_id in seen or finding_id not in derived:
                    return
                seen.add(finding_id)
                for pin in derived[finding_id]["pins"]:
                    cited.add((pin["id"], pin["version"]))
                    walk(pin["id"])

            walk(str(run.pubs[symbol]["id"]))
            self.assertNotIn((SSA_FAMILY, "v1"), cited, symbol)
            # The statement recorded on the retired v1 chain still stands behind both lines.
            self.assertIn(("demo.fw.ssa.b5.0", "v1"), cited, symbol)
            if symbol.endswith("line6b"):
                # Line 6b is where the family's closure is read; it cites the v2 family and mapping.
                self.assertIn((SSA_FAMILY, "v2"), cited, symbol)
                self.assertIn(("tax.us.2025.closure-mapping.ssa1099-benefits", "v2"), cited, symbol)


class InterestWithoutItsBox4Answer(unittest.TestCase):
    def test_a_1099int_statement_with_no_box_4_answer_behaves_as_on_v58(self) -> None:
        acts = _base(wages=50000.0, w2_withheld=4500.0)
        _interest(acts, [(500.0, None), (300.0, 50.0)])
        v58 = _run(acts, "demo.fw.int.v58", core="v58")
        closed = copy.deepcopy(acts)
        _close_new_families_empty(closed)
        v59 = _run(closed, "demo.fw.int.v59", core="v59")
        # The statement with no box 4 answer is left out of the subtotal; the other adds its 50.
        _expect(v58, "3971", "4500", "50", "4550", "4550", "579", "0")
        _expect(v59, "3971", "4500", "50", "4550", "4550", "579", "0")
        self.assertEqual(v58.value(INT_SUBTOTAL), 50)
        self.assertEqual(v59.value(INT_SUBTOTAL), 50)
        self.assertEqual(v59.blocked, [])


class DividendsAndRetirementWithoutTheirBox4Answer(unittest.TestCase):
    """As ``InterestWithoutItsBox4Answer``: the statement with no box 4 answer is
    left out of its subtotal, the answered amount is the whole subtotal and
    reaches line 25b, nothing blocks, and v59 computes what v58 computes."""

    def _check(self, record: Any, subtotal: str, token: str) -> None:
        acts = _base(wages=50000.0, w2_withheld=4500.0)
        record(acts, [(500.0, None), (300.0, 50.0)])
        v58 = _run(acts, f"demo.fw.{token}.v58", core="v58")
        closed = copy.deepcopy(acts)
        _close_new_families_empty(closed)
        v59 = _run(closed, f"demo.fw.{token}.v59", core="v59")
        self.assertEqual(v58.value(subtotal), 50)
        self.assertEqual(v59.value(subtotal), 50)
        self.assertEqual(v59.value(LINE25B), 50)
        self.assertEqual(v59.blocked, [])
        self.assertEqual(_figures(v59), _figures(v58))
        # Both statements' income is counted: 500 and 300 over the same base without them.
        base = _base(wages=50000.0, w2_withheld=4500.0)
        _close_new_families_empty(base)
        without = _run(base, f"demo.fw.{token}.base", core="v59")
        self.assertEqual(v59.value(TOTAL_INCOME) - without.value(TOTAL_INCOME), 800)

    def test_a_1099div_statement_with_no_box_4_answer_behaves_as_on_v58(self) -> None:
        self._check(_dividends, DIV_SUBTOTAL, "div")

    def test_a_1099r_statement_with_no_box_4_answer_behaves_as_on_v58(self) -> None:
        self._check(_retirements, IRA_SUBTOTAL, "ira")


if __name__ == "__main__":
    unittest.main()
