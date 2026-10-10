"""Regenerate the synthetic SLI correction-session workspace and surface
fixtures (``account-review-correction`` milestone, Tracks 1 and 2).

Track 1's seed workspace ("base") is two forms, each supported, on different
borrowings: Cedar (lender "Cedar Servicing") carries the "autumn" borrowing,
Birch (lender "Birch Servicing") carries "spring". Track 2 adds four more
named synthetic states (plan, Track 2 item 1) -- "d1", "shared",
"duplicate-labels" and "blocked" -- each its own committed, sequentially
committed seed act log, selected by the runner's ``--state`` option
(``packages.derivation.runners.sli_correction_evaluation``).

Every state is built only through the real recorder and review flow. The
workspace setup lives in this tool and does not import ``tests``. v42 is
adopted on that workspace. No new package, release, or registry version is
produced here.

The surface publication is its own ADR-0049 container (H4, settled by the
plan's Track 0 review): one manifest entry (the one static page), a no-op
``build_command``, and a ``surface-adoption`` act. It is the same for every
state; only the seed act log differs. All identities are synthetic
``demo.*``.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from collections.abc import Iterable, Mapping
from typing import Any, cast

from packages.derivation.correction_session import CORRECTION_FIXTURE, STATE_SEED_LOGS
from packages.derivation.loader import workspace_registry
from packages.derivation.package_validation import package_instance_checksum
from packages.kernel.act_log import ActLog
from packages.kernel.contribution import apply_contribution_batch
from packages.kernel.facts import fact_id_for
from packages.kernel.findings import project
from packages.tax.loader import install_domain_scoped_supersession, load_sli_relationship_source_bundle
from packages.tax.sli_relationship_recording import introduce_borrowing_reference_durably

ROOT = Path(__file__).resolve().parent.parent
TAX_CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
SAMPLE = ROOT / "packages" / "sample_data"
RELEASE_DIR = SAMPLE / "student_loan_worksheet_integration" / "publication_surface" / "releases"
V41_PACKAGE = TAX_CONTENT / "package.core-calculations.v41.json"
V39_RELEASE = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v39.json"
V42_PACKAGE = TAX_CONTENT / "package.core-calculations.v42.json"
V40_RELEASE = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v40.json"

CGD_ADOPTION = SAMPLE / "frrs_t3" / "adoptions" / "adopt-core-v7-current.json"
UG_FIXTURES = SAMPLE / "form1099g_box1_schedule1_line7"
IRA_ADOPTION = SAMPLE / "form1099r_ira_line4b" / "adoptions" / "adopt-core-v26-current.json"
SSA_ADOPTION = SAMPLE / "ssa1099_benefits_line6" / "adoptions" / "adopt-core-v28-current.json"
F1098E_ADOPTION = SAMPLE / "f1098e_student_loan_interest_track6" / "adoptions" / "adopt-core-v33-current.json"

FILER1 = "demo.user.filer-1"
USER = "demo.user.filer"
SCOPE = {"jurisdiction": "us", "year": "2025"}
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

C1 = "tax.us.2025.exception1.only-box2a-capital-gains"
C2 = "tax.us.2025.exception1.no-capital-losses"
C3 = "tax.us.2025.exception1.no-qof-deferral"
C4 = "tax.us.2025.exception1.no-boxes-2b-2c-2d"
CG_DIST = "tax.us.2025.capital-gain-distributions"

BOX1_AMOUNT = "tax.us.2025.f1099g.box1-unemployment"
BOX1_CLOSURE = "tax.us.2025.f1099g.1.source-closure"
BOX1_FAMILY = "tax.us.2025.f1099g.1"
BOX4_AUTH = "tax.us.2025.f1099g.box4-federal-withholding-authority"
UG_SCOPE_TOKENS = (
    "no-sch1-line1-taxable-refunds",
    "no-sch1-line2a-alimony",
    "no-sch1-line3-business",
    "no-sch1-line4-other-gains",
    "no-sch1-line5-rental",
    "no-sch1-line6-farm",
    "no-sch1-other-income",
    "no-unemployment-repayment",
    "no-f1099g-box2-state-refund",
    "no-f1099g-other-payment-classes",
)

IRA_BOX1 = "tax.us.2025.f1099r.ira-box1-taxable-distribution"
IRA_BOX2A = "tax.us.2025.f1099r.ira-box2a-taxable-amount"
IRA_CHECKBOX = "tax.us.2025.f1099r.ira-sep-simple-checkbox"
IRA_CODE = "tax.us.2025.f1099r.distribution-code"
IRA_BOX2B = "tax.us.2025.f1099r.box2b-not-determined"
IRA_CLOSURE = "tax.us.2025.f1099r.ira-fully-taxable.source-closure"
IRA_FAMILY = "tax.us.2025.f1099r.ira-fully-taxable"

FAMILY = "tax.us.2025.ssa1099.benefits"
BOX3 = "tax.us.2025.ssa1099.box3-benefits-paid"
BOX4 = "tax.us.2025.ssa1099.box4-repayment"
BOX5 = "tax.us.2025.ssa1099.box5-net-benefits"
BOX6 = "tax.us.2025.ssa1099.box6-withholding"
RECIPIENT = "tax.us.2025.ssa1099.recipient"
KIND = "tax.us.2025.ssa1099.statement-kind"
LUMP = "tax.us.2025.ssa1099.lump-sum-election"
CLOSURE = "tax.us.2025.ssa1099.source-closure"
MFS = "tax.us.2025.mfs-lived-apart-all-year"
SSA_SCOPE_TOKENS = (
    "no-unsupported-line1-entries",
    "no-pension-annuity-line5b",
    "no-traditional-ira-deduction",
    "no-form-2555",
    "no-form-4563",
    "no-form-8815",
    "no-excluded-adoption-benefits",
    "no-puerto-rico-or-samoa-income",
    "no-schedule1-line24z-writein",
    "no-sch1-line11-educator",
    "no-sch1-line12-business-expenses",
    "no-sch1-line13-hsa",
    "no-sch1-line14-moving",
    "no-sch1-line15-deductible-se",
    "no-sch1-line16-se-retirement",
    "no-sch1-line17-se-health",
    "no-sch1-line18-penalty",
    "no-sch1-line19-alimony-paid",
    "no-sch1-line20-ira-deduction",
    "no-sch1-line23-archer-msa",
    "no-sch1-line25-other-adjustments",
    "no-lump-sum-election",
    "no-rrb-or-foreign-social-benefit",
)

FAMILY_ID = "tax.us.2025.f1098e.1"
BOX1 = "tax.us.2025.f1098e.box1-student-loan-interest"
BOX2 = "tax.us.2025.f1098e.box2-checked-authority"
CLOSURE_TYPE = "tax.us.2025.f1098e.1.source-closure"
SLI_SCOPE_UNIVERSAL_TOKENS = (
    "no-form-2555",
    "no-form-4563",
    "no-puerto-rico-or-samoa-income",
)
SLI_SCOPE_LEGAL_ZERO_TOKENS = (
    "not-claimed-as-dependent",
    "legally-obligated-for-interest",
)
SCHED1_LINE_TOKENS = (
    "no-line11-educator", "no-line12-business-expenses", "no-line13-hsa",
    "no-line14-moving", "no-line15-deductible-se", "no-line16-se-retirement",
    "no-line17-se-health", "no-line18-penalty", "no-line19-alimony-paid",
    "no-line20-ira-deduction", "no-line23-archer-msa", "no-line25-other-adjustments",
)

SCHOOL = "tax.us.2025.sli.schooling-situation"
QUESTIONS = {"loan": "loan-paid-only-school-costs", "enroll": "enrolled-at-least-half-time"}
ANSWER_TAILS = (
    "no-related-person-interest",
    "no-qualified-employer-plan-interest",
    "no-non-qualified-loan-component",
    "no-employer-educational-assistance-interest",
    "no-qtp-earnings-used",
)
REPLACED = "no-non-qualified-loan-component"
STANDARD = {"cedar": 3000.0, "birch": 1800.0}


def _load_json(path: Path) -> dict[str, object]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise RuntimeError(f"expected an object in {path.name}")
    return loaded


def _load_content(name: str) -> dict[str, Any]:
    loaded = json.loads((TAX_CONTENT / name).read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise RuntimeError(f"expected an object in {name}")
    return loaded


def _attested(finding_id: str, fact_id: str, value: object) -> dict[str, object]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


def _filer1_act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.ug.act.{index:03d}",
        "kind": kind,
        "actor": FILER1,
        "at": f"2026-08-05T12:{index // 60:02d}:{index % 60:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _cgd_live_act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.cgd.t2.act.{index:03d}",
        "kind": kind,
        "actor": FILER1,
        "at": f"2026-07-30T00:00:{index:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _ug_scope_id(token: str) -> str:
    return f"tax.us.2025.schedule1-part1-scope.{token}"


def _ssa_scope_id(token: str) -> str:
    return f"tax.us.2025.ss-benefits-scope.{token}"


def _support_act(index: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"demo-act-{index:03d}",
        "kind": kind,
        "actor": "user",
        "at": f"2026-01-01T00:{index // 60:02d}:{index % 60:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _demo_entity(entity_id: str, label: str, kind: str) -> dict[str, Any]:
    return {"schema": "entity.v1", "id": entity_id, "kind": kind, "label": label}


def _demo_evidence(evidence_id: str, label: str, content: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "evidence.v1",
        "id": evidence_id,
        "kind": "demo.statement",
        "label": label,
        "content": content,
    }


def _append_source(log: ActLog, registry: Any, fact_type: str, keys: tuple[tuple[str, str], ...],
                   value: Any, label: str) -> str:
    before = log.read()
    evidence_id = f"demo.evidence.track14.{label}"
    contribution_id = f"demo.contribution.track14.{label}"
    finding = {"schema": "finding.v2", "id": f"demo.finding.track14.{label}",
               "fact_id": fact_id_for(fact_type, keys), "value": value, "basis": "attested",
               "evidence_ids": [evidence_id], "contribution_id": contribution_id}
    staged = list(before.acts)
    staged.append(_support_act(len(staged), "evidence-submitted", {"evidence": _demo_evidence(
        evidence_id, "Synthetic Track 14 answer", {"label": label})}))
    contribution = _support_act(len(staged), "contribution", {"contribution": {
        "schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id,
        "content": {"mode": "manual-entry", "synthetic": True},
    }})
    assertion = _support_act(len(staged) + 1, "assertion", {"finding": finding})
    base = project(tuple(staged), registry)
    admitted = apply_contribution_batch(base, contribution_act=contribution,
                                        successor_acts=[assertion], registry=registry,
                                        record_id=f"demo.contribution-record.track14.{label}")
    if admitted.terminal_record["phase"] != "completed":
        raise AssertionError(admitted.terminal_record)
    for item in (staged[-1], contribution, assertion):
        log.append(item, expected_revision=log.read().revision)
    return str(finding["fact_id"])

def _cgd_t2_acts(
    *,
    wages: float = 90000,
    box1a: float | None = 600,
    box1b: float | None = 0,
    box2a: float | None = 1500,
    close_2a: bool = True,
    components: dict[str, str | None] | None = None,
    cg_dist: str | None = "yes",
    multi_payer_box2a: list[float] | None = None,
    c4_successor: str | None = None,
) -> list[dict[str, object]]:
    if components is None:
        components = {"C1": "yes", "C2": "yes", "C3": "yes", "C4": "yes"}
    acts: list[dict[str, object]] = []

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_cgd_live_act(len(acts), kind, payload))

    for name in (
        "w2.bundle.v3.json",
        "f1099int.bundle.json",
        "interest_composition.bundle.json",
        "core_calculations.bundle.v2.json",
        "f1099div.bundle.v2.json",
        "f1099div-box2a.bundle.json",
        "exception1.bundle.json",
        "qdcg.bundle.json",
    ):
        add("bundle-adoption", {"bundle": json.loads((TAX_CONTENT / name).read_text())})

    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.cgd.t2.employer", "kind": "tax.us.employer", "label": "Synthetic employer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.cgd.t2.w2", "kind": "tax.us.w2-slip", "label": "Synthetic W-2"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.cgd.t2.payer", "kind": "tax.us.dividend-payer", "label": "Synthetic payer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.cgd.t2.stmt", "kind": "tax.us.1099div-statement", "label": "Synthetic 1099-DIV"}})

    scope = {"tax-year": "2025", "subject": "demo.primary"}
    families = (
        ("tax.us.2025.w2", "v2", "demo.cgd.t2.w2.h0"),
        ("tax.us.2025.f1099int.b1", "v1", "demo.cgd.t2.int-b1.h0"),
        ("tax.us.2025.f1099int.b3", "v1", "demo.cgd.t2.int-b3.h0"),
        ("tax.us.2025.f1099oid.b1", "v1", "demo.cgd.t2.oid-b1.h0"),
        ("tax.us.2025.non-form-interest", "v1", "demo.cgd.t2.nonform.h0"),
        ("tax.us.2025.f1099div.1a", "v1", "demo.cgd.t2.div1a.h0"),
        ("tax.us.2025.f1099div.1b", "v1", "demo.cgd.t2.div1b.h0"),
        ("tax.us.2025.f1099div.2a", "v1", "demo.cgd.t2.div2a.h0"),
    )
    for family_id, version, horizon_id in families:
        add("horizon-genesis", {"family": {"id": family_id, "version": version}, "scope": scope, "horizon_id": horizon_id})

    w2_horizon = "demo.cgd.t2.w2.h0"
    if wages:
        add("member-transition", {
            "family": {"id": "tax.us.2025.w2", "version": "v2"},
            "scope": scope,
            "member": {"action": "assert", "finding": _attested(
                "demo.cgd.t2.finding.wages",
                "tax.us.2025.w2.box1-wages|employer=demo.cgd.t2.employer,w2-slip=demo.cgd.t2.w2,tax-year=2025",
                wages,
            )},
            "successor": {"id": "demo.cgd.t2.w2.h1", "predecessor": w2_horizon},
        })
        w2_horizon = "demo.cgd.t2.w2.h1"

    def _div_member(fact_type: str, family_id: str, predecessor: str, successor: str, value: float, finding_id: str) -> None:
        add("member-transition", {
            "family": {"id": family_id, "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": _attested(
                finding_id,
                f"{fact_type}|payer=demo.cgd.t2.payer,statement=demo.cgd.t2.stmt,tax-year=2025",
                value,
            )},
            "successor": {"id": successor, "predecessor": predecessor},
        })

    div1a_horizon = "demo.cgd.t2.div1a.h0"
    if box1a is not None:
        _div_member(
            "tax.us.2025.f1099div.box1a-ordinary", "tax.us.2025.f1099div.1a",
            div1a_horizon, "demo.cgd.t2.div1a.h1", box1a, "demo.cgd.t2.finding.box1a",
        )
        div1a_horizon = "demo.cgd.t2.div1a.h1"

    div1b_horizon = "demo.cgd.t2.div1b.h0"
    if box1b is not None and box1b != 0:
        _div_member(
            "tax.us.2025.f1099div.box1b-qualified", "tax.us.2025.f1099div.1b",
            div1b_horizon, "demo.cgd.t2.div1b.h1", box1b, "demo.cgd.t2.finding.box1b",
        )
        div1b_horizon = "demo.cgd.t2.div1b.h1"

    div2a_horizon = "demo.cgd.t2.div2a.h0"
    if multi_payer_box2a is not None:
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.cgd.t2.payer-b", "kind": "tax.us.dividend-payer", "label": "Payer B"}})
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.cgd.t2.stmt-b", "kind": "tax.us.1099div-statement", "label": "Stmt B"}})
        pairs = [
            ("demo.cgd.t2.payer", "demo.cgd.t2.stmt"),
            ("demo.cgd.t2.payer-b", "demo.cgd.t2.stmt-b"),
        ]
        for i, amount in enumerate(multi_payer_box2a):
            payer, stmt = pairs[i]
            succ = f"demo.cgd.t2.div2a.h{i + 1}"
            add("member-transition", {
                "family": {"id": "tax.us.2025.f1099div.2a", "version": "v1"},
                "scope": scope,
                "member": {"action": "assert", "finding": _attested(
                    f"demo.cgd.t2.finding.box2a.{i}",
                    f"tax.us.2025.f1099div.box2a-capital-gain-distribution|payer={payer},statement={stmt},tax-year=2025",
                    amount,
                )},
                "successor": {"id": succ, "predecessor": div2a_horizon},
            })
            div2a_horizon = succ
    elif box2a is not None:
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099div.2a", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": _attested(
                "demo.cgd.t2.finding.box2a",
                "tax.us.2025.f1099div.box2a-capital-gain-distribution|payer=demo.cgd.t2.payer,statement=demo.cgd.t2.stmt,tax-year=2025",
                box2a,
            )},
            "successor": {"id": "demo.cgd.t2.div2a.h1", "predecessor": div2a_horizon},
        })
        div2a_horizon = "demo.cgd.t2.div2a.h1"

    add("assertion", {"finding": _attested("demo.cgd.t2.finding.rounding", "rounding.convention|tax-year=2025", "half_up")})
    add("assertion", {"finding": _attested("demo.cgd.t2.finding.status", "tax.us.2025.filing-status|tax-year=2025", "single")})

    component_facts = {
        "C1": (C1, "demo.cgd.t2.finding.c1"),
        "C2": (C2, "demo.cgd.t2.finding.c2"),
        "C3": (C3, "demo.cgd.t2.finding.c3"),
        "C4": (C4, "demo.cgd.t2.finding.c4"),
    }
    for alias, value in components.items():
        if value is None:
            continue
        fact_type, fid = component_facts[alias]
        add("assertion", {"finding": _attested(fid, f"{fact_type}|tax-year=2025", value)})
    if c4_successor is not None:
        add("assertion", {"finding": _attested(
            "demo.cgd.t2.finding.c4.v2", f"{C4}|tax-year=2025", c4_successor,
        )})

    if cg_dist is not None:
        add("assertion", {"finding": _attested("demo.cgd.t2.finding.cg-dist", f"{CG_DIST}|tax-year=2025", cg_dist)})

    closures = [
        ("demo.cgd.t2.closure.w2", "tax.us.2025.w2.source-closure", w2_horizon),
        ("demo.cgd.t2.closure.int-b1", "tax.us.2025.f1099int.b1.source-closure", "demo.cgd.t2.int-b1.h0"),
        ("demo.cgd.t2.closure.int-b3", "tax.us.2025.f1099int.b3.source-closure", "demo.cgd.t2.int-b3.h0"),
        ("demo.cgd.t2.closure.oid-b1", "tax.us.2025.f1099oid.b1.source-closure", "demo.cgd.t2.oid-b1.h0"),
        ("demo.cgd.t2.closure.nonform", "tax.us.2025.non-form-interest.source-closure", "demo.cgd.t2.nonform.h0"),
        ("demo.cgd.t2.closure.div1a", "tax.us.2025.f1099div.1a.source-closure", div1a_horizon),
        ("demo.cgd.t2.closure.div1b", "tax.us.2025.f1099div.1b.source-closure", div1b_horizon),
    ]
    if close_2a:
        closures.append(("demo.cgd.t2.closure.div2a", "tax.us.2025.f1099div.2a.source-closure", div2a_horizon))
    for finding_id, fact_type, horizon_id in closures:
        add("assertion", {"finding": _attested(finding_id, f"{fact_type}|family-horizon={horizon_id},tax-year=2025", True)})

    adoption = _load_json(CGD_ADOPTION)
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts

def _ug_acts(
    *,
    box1_values: list[float] | None = None,
    box4_values: list[object] | None = None,
    close_box1: bool = True,
    scope: dict[str, str] | None = None,
    wages: float = 90000,
    box1a: float | None = 0,
    box1b: float | None = 0,
    box2a: float | None = None,
    include_box4: bool = True,
    same_payer_two_statements: bool = False,
) -> list[dict[str, object]]:
    """Build a production-shaped act log on the v20 route with box-1 facts."""
    box1_values = [2500.0] if box1_values is None else box1_values
    if box4_values is None:
        box4_values = [None] * max(1, len(box1_values) if box1_values else 1)
    scope_vals = {token: "yes" for token in UG_SCOPE_TOKENS}
    if scope:
        scope_vals.update(scope)

    acts = _cgd_t2_acts(
        wages=wages,
        box1a=box1a if box1a else None,
        box1b=box1b if box1b else 0,
        box2a=box2a,
        close_2a=True,
        cg_dist="no" if box2a is None else "yes",
        components={"C1": "yes", "C2": "yes", "C3": "yes", "C4": "yes"},
    )
    acts.pop()  # drop historical package adoption

    # Residual-free box2a vocabulary for exclusive package graph (same as box-12 tests).
    for act in acts:
        if act["kind"] == "bundle-adoption":
            payload = cast(dict[str, object], act["payload"])
            bundle = cast(dict[str, Any], payload.get("bundle") or {})
            if bundle.get("id") == "tax.us.2025.f1099div.box2a.vocabulary":
                payload["bundle"] = _load_content("f1099div-box2a.bundle.v2.json")

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_filer1_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load_content("f1099g-box1.bundle.json")})
    add("bundle-adoption", {"bundle": _load_content("schedule1-part1-scope.bundle.json")})
    # Close remaining interest-composition v4 families and Schedule B adjustment
    # families closed-empty so taxable-interest (and thus line 9) can publish on
    # the current core package graph.
    for name in (
        "form1065-k1.bundle.json",
        "f1099int-b10.bundle.json",
        "f1099oid-b5.bundle.json",
        "f1099int-box8.bundle.json",
        "scheduleb.bundle.json",
        "scheduleb-adjustment.nominee.bundle.json",
        "scheduleb-adjustment.accrued-interest.bundle.json",
        "scheduleb-adjustment.abp-adjustment.bundle.json",
        "f1099b-covered-st.bundle.json",
        "f1099b-covered-lt.bundle.json",
        "f1099b-covered-st-scalars.bundle.json",
        "f1099b-covered-lt-scalars.bundle.json",
        "f1099b-covered-w-st.bundle.json",
        "f1099b-covered-w-lt.bundle.json",
        "f1099b-covered-w-st-scalars.bundle.json",
        "f1099b-covered-w-lt-scalars.bundle.json",
        "schedule-d-boundary.bundle.json",
    ):
        add("bundle-adoption", {"bundle": _load_content(name)})

    # Closed-empty interest-composition remainder + Schedule B adjustments +
    # covered ST/LT families so line 7a / line 9 can publish alongside line 8.
    closed_empty: tuple[tuple[str, str, str], ...] = (
        (
            "tax.us.2025.form1065-k1.box5",
            "demo.ug.k1.h0",
            "tax.us.2025.form1065-k1.box5.source-closure",
        ),
        (
            "tax.us.2025.f1099int.b10",
            "demo.ug.int-b10.h0",
            "tax.us.2025.f1099int.b10.source-closure",
        ),
        (
            "tax.us.2025.f1099oid.b5",
            "demo.ug.oid-b5.h0",
            "tax.us.2025.f1099oid.b5.source-closure",
        ),
        (
            "tax.us.2025.scheduleb.adjustment.nominee",
            "demo.ug.sb-nom.h0",
            "tax.us.2025.scheduleb.adjustment.nominee.source-closure",
        ),
        (
            "tax.us.2025.scheduleb.adjustment.accrued-interest",
            "demo.ug.sb-acc.h0",
            "tax.us.2025.scheduleb.adjustment.accrued-interest.source-closure",
        ),
        (
            "tax.us.2025.scheduleb.adjustment.abp-adjustment",
            "demo.ug.sb-abp.h0",
            "tax.us.2025.scheduleb.adjustment.abp-adjustment.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-st",
            "demo.ug.st.h0",
            "tax.us.2025.f1099b.covered-st.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-st-proceeds",
            "demo.ug.st-p.h0",
            "tax.us.2025.f1099b.covered-st-proceeds.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-st-basis",
            "demo.ug.st-b.h0",
            "tax.us.2025.f1099b.covered-st-basis.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-lt",
            "demo.ug.lt.h0",
            "tax.us.2025.f1099b.covered-lt.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-lt-proceeds",
            "demo.ug.lt-p.h0",
            "tax.us.2025.f1099b.covered-lt-proceeds.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-lt-basis",
            "demo.ug.lt-b.h0",
            "tax.us.2025.f1099b.covered-lt-basis.source-closure",
        ),
        (
            "tax.us.2025.f1099int.b8",
            "demo.ug.int-b8.h0",
            "tax.us.2025.f1099int.b8.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-st",
            "demo.ug.wst.h0",
            "tax.us.2025.f1099b.covered-w-st.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-st-proceeds",
            "demo.ug.wst-p.h0",
            "tax.us.2025.f1099b.covered-w-st-proceeds.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-st-basis",
            "demo.ug.wst-b.h0",
            "tax.us.2025.f1099b.covered-w-st-basis.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-st-adjustment",
            "demo.ug.wst-a.h0",
            "tax.us.2025.f1099b.covered-w-st-adjustment.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-lt",
            "demo.ug.wlt.h0",
            "tax.us.2025.f1099b.covered-w-lt.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-lt-proceeds",
            "demo.ug.wlt-p.h0",
            "tax.us.2025.f1099b.covered-w-lt-proceeds.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-lt-basis",
            "demo.ug.wlt-b.h0",
            "tax.us.2025.f1099b.covered-w-lt-basis.source-closure",
        ),
        (
            "tax.us.2025.f1099b.covered-w-lt-adjustment",
            "demo.ug.wlt-a.h0",
            "tax.us.2025.f1099b.covered-w-lt-adjustment.source-closure",
        ),
    )
    for family_id, horizon_id, closure_type in closed_empty:
        add(
            "horizon-genesis",
            {
                "family": {"id": family_id, "version": "v1"},
                "scope": SCOPE_KEY,
                "horizon_id": horizon_id,
            },
        )
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.ug.closure.{horizon_id}",
                    f"{closure_type}|family-horizon={horizon_id},tax-year=2025",
                    True,
                )
            },
        )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.ug.scheduleb.foreign-account",
                "tax.us.2025.scheduleb.foreign-account|tax-year=2025",
                "no",
            )
        },
    )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.ug.scheduleb.foreign-trust",
                "tax.us.2025.scheduleb.foreign-trust|tax-year=2025",
                "no",
            )
        },
    )
    for token in (
        "no-inbound-capital-loss-carryovers",
        "no-form8949-sources",
        "no-other-schedule-d-sources",
        "no-lines-18-19-sources",
        "no-1099da-or-qof",
    ):
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.ug.sd-boundary.{token}",
                    f"tax.us.2025.schedule-d-boundary.{token}|tax-year=2025",
                    "yes",
                )
            },
        )

    n_members = max(len(box1_values), 1)
    payers_stmts: list[tuple[str, str]] = []
    if same_payer_two_statements and n_members >= 2:
        payer = "demo.ug.payer.shared"
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": payer,
                    "kind": "tax.us.unemployment-payer",
                    "label": "Synthetic shared unemployment agency",
                }
            },
        )
        for index in range(n_members):
            stmt = f"demo.ug.stmt.{index}"
            add(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": stmt,
                        "kind": "tax.us.1099g-statement",
                        "label": f"Synthetic 1099-G statement {index}",
                    }
                },
            )
            payers_stmts.append((payer, stmt))
    else:
        for index in range(n_members):
            payer = f"demo.ug.payer.{index}"
            stmt = f"demo.ug.stmt.{index}"
            add(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": payer,
                        "kind": "tax.us.unemployment-payer",
                        "label": f"Synthetic unemployment agency {index}",
                    }
                },
            )
            add(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": stmt,
                        "kind": "tax.us.1099g-statement",
                        "label": f"Synthetic 1099-G statement {index}",
                    }
                },
            )
            payers_stmts.append((payer, stmt))

    add(
        "horizon-genesis",
        {
            "family": {"id": BOX1_FAMILY, "version": "v1"},
            "scope": SCOPE_KEY,
            "horizon_id": "demo.ug.h0",
        },
    )
    horizon = "demo.ug.h0"
    for index, amount in enumerate(box1_values):
        payer, stmt = payers_stmts[index]
        if include_box4:
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.ug.finding.box4.{index}",
                        f"{BOX4_AUTH}|payer={payer},statement={stmt},tax-year=2025",
                        box4_values[index] if index < len(box4_values) else None,
                    )
                },
            )
        next_horizon = f"demo.ug.h{index + 1}"
        add(
            "member-transition",
            {
                "family": {"id": BOX1_FAMILY, "version": "v1"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(
                        f"demo.ug.finding.box1.{index}",
                        f"{BOX1_AMOUNT}|payer={payer},statement={stmt},tax-year=2025",
                        amount,
                    ),
                },
                "successor": {"id": next_horizon, "predecessor": horizon},
            },
        )
        horizon = next_horizon

    if close_box1:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ug.closure.box1",
                    f"{BOX1_CLOSURE}|family-horizon={horizon},tax-year=2025",
                    True,
                )
            },
        )

    for token, value in scope_vals.items():
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.ug.scope.{token}",
                    f"{_ug_scope_id(token)}|tax-year=2025",
                    value,
                )
            },
        )

    adoption = cast(
        dict[str, object],
        json.loads((UG_FIXTURES / "adoptions" / "adopt-core-v20-current.json").read_text("utf-8")),
    )
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts

def _ira_acts(
    amounts: list[float] | None = None,
    *,
    close: bool = True,
    qualified_dividends: bool = False,
) -> list[dict[str, object]]:
    """Extend a known production-shaped income corpus with IRA statements."""
    acts = _ug_acts(
        box1_values=[],
        close_box1=True,
        box1a=600 if qualified_dividends else None,
        box1b=150 if qualified_dividends else 0,
        wages=90000,
    )
    acts.pop()  # replace the historical v20 adoption with the Track 2 adoption

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_filer1_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load_content("f1099r-ira.bundle.v2.json")})
    amounts = [1200.0] if amounts is None else amounts
    payer = "demo.ira.payer.alpha"
    add(
        "entity-introduced",
        {"entity": {"schema": "entity.v1", "id": payer, "kind": "tax.us.ira-payer", "label": "Synthetic IRA payer"}},
    )
    horizon = "demo.ira.h0"
    add(
        "horizon-genesis",
        {"family": {"id": IRA_FAMILY, "version": "v2"}, "scope": SCOPE_KEY, "horizon_id": horizon},
    )
    for index, amount in enumerate(amounts):
        statement = f"demo.ira.statement.{index}"
        add(
            "entity-introduced",
            {"entity": {"schema": "entity.v1", "id": statement, "kind": "tax.us.1099r-statement", "label": "Synthetic Form 1099-R"}},
        )
        for fact_type, value, suffix in (
            (IRA_BOX2A, amount, "box2a"),
            (IRA_CHECKBOX, True, "checkbox"),
            (IRA_CODE, "7", "code"),
            (IRA_BOX2B, False, "box2b"),
        ):
            add(
                "assertion",
                {"finding": _attested(f"demo.ira.finding.{suffix}.{index}", f"{fact_type}|payer={payer},statement={statement},tax-year=2025", value)},
            )
        next_horizon = f"demo.ira.h{index + 1}"
        add(
            "member-transition",
            {
                "family": {"id": IRA_FAMILY, "version": "v2"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(f"demo.ira.finding.box1.{index}", f"{IRA_BOX1}|payer={payer},statement={statement},tax-year=2025", amount),
                },
                "successor": {"id": next_horizon, "predecessor": horizon},
            },
        )
        horizon = next_horizon
    if close:
        add(
            "assertion",
            {"finding": _attested("demo.ira.closure", f"{IRA_CLOSURE}|family-horizon={horizon},tax-year=2025", True)},
        )
    adoption = _load_json(IRA_ADOPTION)
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts

def _ssa_acts(
    *,
    benefits: list[tuple[float, float, float]] | None = None,
    close: bool = True,
    wages: float = 15000,
    interest: float | None = None,
    ordinary_dividends: float | None = None,
    qualified_dividends: float | None = None,
    capital_gains: float | None = None,
    unemployment: float | None = None,
    filing_status: str = "single",
    mfs_lived_apart: str | None = None,
    tax_exempt: float | None = None,
    ira_amounts: list[float] | None = None,
    scope: dict[str, str] | None = None,
    recipient: str = "taxpayer",
    statement_overrides: list[dict[str, object]] | None = None,
) -> list[dict[str, object]]:
    """Production-shaped acts with controlled ordinary-income components + SSA."""
    global _ug_acts
    original_ug = _ug_acts

    def _ug_with_components(**kwargs: Any) -> list[dict[str, object]]:
        kwargs["wages"] = wages
        # Unemployment → Schedule 1 / Form 1040 line 8 via 1099-G box 1.
        if unemployment is not None and unemployment > 0:
            kwargs["box1_values"] = [unemployment]
            kwargs["close_box1"] = True
        else:
            kwargs["box1_values"] = []
            kwargs["close_box1"] = True
        # Ordinary / qualified dividends and capital-gain distributions.
        if ordinary_dividends is not None:
            kwargs["box1a"] = ordinary_dividends
        if qualified_dividends is not None:
            kwargs["box1b"] = qualified_dividends
        if capital_gains is not None:
            kwargs["box2a"] = capital_gains
        return original_ug(**kwargs)

    _ug_acts = _ug_with_components
    try:
        acts = _ira_acts(
            amounts=[] if ira_amounts is None else ira_amounts,
            close=True,
            qualified_dividends=False,
        )
    finally:
        _ug_acts = original_ug
    acts.pop()  # drop historical package adoption

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_filer1_act(len(acts), kind, payload))

    # Ensure wages / filing status from base corpus; override wages via W-2 if needed
    # is already set by upstream helpers. Adopt SSA vocabulary + scope + successor packages.
    add("bundle-adoption", {"bundle": _load_content("ssa1099.bundle.v2.json")})
    add("bundle-adoption", {"bundle": _load_content("ss-benefits-scope.bundle.json")})
    # Line 2a residual scopes + closed-empty box-12 so tax-exempt line 2a
    # publishes zero for the worksheet W4 pin without Path B INT box-8.
    if not any(
        act.get("kind") == "bundle-adoption"
        and cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("bundle", {})).get("id")
        == "tax.us.2025.line2a-scope.vocabulary"
        for act in acts
    ):
        add("bundle-adoption", {"bundle": _load_content("line2a-scope.bundle.json")})
    line2a_scope_tokens = (
        "no-f1099int-tax-exempt",
        "no-f1099oid-tax-exempt",
        "no-unreported-tax-exempt",
        "no-premium-adjustment",
        "no-child-income-election",
        "no-amt-form-6251",
        "no-credit-using-tax-exempt",
        "no-deduction-using-tax-exempt",
    )
    for token in line2a_scope_tokens:
        fid = f"tax.us.2025.line2a-scope.{token}"
        # skip if already asserted by upstream corpus
        already = any(
            str(cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("finding", {})).get("fact_id", "")).startswith(fid + "|")
            for act in acts
        )
        if not already:
            add(
                "assertion",
                {"finding": _attested(f"demo.ssa.line2a.{token}", f"{fid}|tax-year=2025", "yes")},
            )
    div12_family = "tax.us.2025.f1099div.12"
    if not any(
        act.get("kind") == "bundle-adoption"
        and cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("bundle", {})).get("id")
        == "tax.us.2025.f1099div.box12.vocabulary"
        for act in acts
    ):
        add("bundle-adoption", {"bundle": _load_content("f1099div-box12.bundle.v2.json")})

    scope_vals = {token: "yes" for token in SSA_SCOPE_TOKENS}
    if scope:
        scope_vals.update(scope)
    for token, value in scope_vals.items():
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.ssa.scope.{token}",
                    f"{_ssa_scope_id(token)}|tax-year=2025",
                    value,
                )
            },
        )

    if mfs_lived_apart is not None:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.mfs-lived-apart",
                    f"{MFS}|tax-year=2025",
                    mfs_lived_apart,
                )
            },
        )

    # Override corpus filing status when a non-default status is requested.
    if filing_status != "single":
        replaced = False
        for act in acts:
            finding = cast(
                dict[str, Any],
                cast(dict[str, Any], act.get("payload", {})).get("finding", {}),
            )
            fact_id = str(finding.get("fact_id", ""))
            if fact_id.startswith("tax.us.2025.filing-status|"):
                finding["value"] = filing_status
                replaced = True
                break
        if not replaced:
            add(
                "assertion",
                {
                    "finding": _attested(
                        "demo.ssa.filing-status",
                        "tax.us.2025.filing-status|tax-year=2025",
                        filing_status,
                    )
                },
            )

    # Taxable interest (Form 1099-INT box 1): advance the CGD closed-empty
    # int-b1 horizon so line 2b includes the amount exactly once.
    if interest is not None and interest > 0:
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": "demo.ssa.int.payer",
                    "kind": "tax.us.interest-payer",
                    "label": "Synthetic interest payer",
                }
            },
        )
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": "demo.ssa.int.stmt",
                    "kind": "tax.us.1099int-statement",
                    "label": "Synthetic Form 1099-INT",
                }
            },
        )
        add(
            "member-transition",
            {
                "family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(
                        "demo.ssa.finding.int-b1",
                        "tax.us.2025.f1099int.box1-interest|"
                        "payer=demo.ssa.int.payer,statement=demo.ssa.int.stmt,tax-year=2025",
                        interest,
                    ),
                },
                "successor": {
                    "id": "demo.ssa.int-b1.h1",
                    "predecessor": "demo.cgd.t2.int-b1.h0",
                },
            },
        )
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.closure.int-b1",
                    "tax.us.2025.f1099int.b1.source-closure|"
                    "family-horizon=demo.ssa.int-b1.h1,tax-year=2025",
                    True,
                )
            },
        )

    benefits = [(12000.0, 0.0, 12000.0)] if benefits is None else benefits
    horizon = "demo.ssa.h0"
    add(
        "horizon-genesis",
        {"family": {"id": FAMILY, "version": "v1"}, "scope": SCOPE_KEY, "horizon_id": horizon},
    )
    for index, (b3, b4, b5) in enumerate(benefits):
        statement = f"demo.ssa.statement.{index}"
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": statement,
                    "kind": "tax.us.ssa1099-statement",
                    "label": "Synthetic Form SSA-1099",
                }
            },
        )
        # box5 is the collected member: assert companions first so presence
        # admission sees a complete same-statement witness set.
        ov = {}
        if statement_overrides and index < len(statement_overrides):
            ov = statement_overrides[index]
        kind_val = cast(str, ov.get("kind", "ssa-1099"))
        lump_val = cast(bool, ov.get("lump_sum_election", False))
        recip_val = cast(str, ov.get("recipient", recipient))
        box6_val = cast(float | None, ov.get("box6", 0))
        members: tuple[tuple[str, object, str], ...] = (
            (BOX3, b3, "box3"),
            (BOX4, b4, "box4"),
            (BOX6, box6_val, "box6"),
            (RECIPIENT, recip_val, "recipient"),
            (KIND, kind_val, "kind"),
            (LUMP, lump_val, "lump"),
            (BOX5, b5, "box5"),
        )
        for member_fact_type, member_value, member_suffix in members:
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.ssa.finding.{member_suffix}.{index}",
                        f"{member_fact_type}|statement={statement},tax-year=2025",
                        member_value,
                    )
                },
            )

    if close:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.closure",
                    f"{CLOSURE}|family-horizon={horizon},tax-year=2025",
                    True,
                )
            },
        )

    # Line-2a residual scopes still required by line2a v3 (except removed SS residual)
    # Already present via IRA/UG helpers for many paths; tax-exempt optional Path A/B.

    # Line 2a / box-12: present tax-exempt dividends or closed-empty zero.
    div12_family = "tax.us.2025.f1099div.12"
    horizon = "demo.ssa.div12.h0"
    add(
        "horizon-genesis",
        {
            "family": {"id": div12_family, "version": "v1"},
            "scope": SCOPE_KEY,
            "horizon_id": horizon,
        },
    )
    if tax_exempt is not None and tax_exempt > 0:
        payer = "demo.ssa.div12.payer"
        statement = "demo.ssa.div12.statement.0"
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": payer,
                    "kind": "tax.us.dividend-payer",
                    "label": "Synthetic dividend payer",
                }
            },
        )
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": statement,
                    "kind": "tax.us.1099div-statement",
                    "label": "Synthetic Form 1099-DIV",
                }
            },
        )
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.div12.box13",
                    "tax.us.2025.f1099div.box13-specified-pab-authority|"
                    f"payer={payer},statement={statement},tax-year=2025",
                    None,
                )
            },
        )
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.div12.box12",
                    "tax.us.2025.f1099div.box12-exempt-interest-dividends|"
                    f"payer={payer},statement={statement},tax-year=2025",
                    tax_exempt,
                )
            },
        )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.ssa.div12.closure",
                f"tax.us.2025.f1099div.12.source-closure|family-horizon={horizon},tax-year=2025",
                True,
            )
        },
    )


    adoption = _load_json(SSA_ADOPTION)
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts

def _member_fact_id(fact_type: str, lender: str, statement: str) -> str:
    return f"{fact_type}|lender={lender},statement={statement},tax-year=2025"

def _f1098e_acts(
    *,
    statements: list[Any] | None = None,
    close: bool = True,
    wages: float = 90000,
    filing_status: str = "single",
    sli_scope_overrides: dict[str, str] | None = None,
    sched1_overrides: dict[str, str] | None = None,
    assert_sli_scope: bool = True,
    assert_sched1_scope: bool = True,
    extra: list[dict[str, object]] | None = None,
    horizon_prefix: str = "demo.f1098e.h",
) -> list[dict[str, object]]:
    """Extend the proven SSA-1099/IRA base return with a Form 1098-E
    statement lifecycle, mirroring ``tests/test_f1098_mortgage_interest_
    line12e_track2.py``'s ``_f1098_acts`` shape one family over.

    ``statements=None`` or ``[]`` means a closed-empty family: the source
    family is still closed (when ``close=True``), just with zero current
    members. Every statement gets its own lender/statement entity pair and
    advances the family's own horizon lineage.
    """
    acts = _ssa_acts(benefits=[], close=True, wages=wages, filing_status=filing_status)
    acts.pop()  # drop the SSA-1099 milestone's own trailing adoption

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_filer1_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load_content("f1098e.bundle.json")})
    add("bundle-adoption", {"bundle": _load_content("sli-scope.bundle.json")})
    if assert_sched1_scope and not any(
        act.get("kind") == "bundle-adoption"
        and cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("bundle", {})).get("id")
        == "tax.us.2025.schedule1-adjustments-scope.vocabulary"
        for act in acts
    ):
        add("bundle-adoption", {"bundle": _load_content("schedule1-adjustments-scope.bundle.json")})

    stmts = statements or []
    for s in stmts:
        add(
            "entity-introduced",
            {"entity": {"schema": "entity.v1", "id": s.lender, "kind": "tax.us.student-loan-lender", "label": "Synthetic student loan lender"}},
        )
        add(
            "entity-introduced",
            {"entity": {"schema": "entity.v1", "id": s.stmt, "kind": "tax.us.1098e-statement", "label": "Synthetic Form 1098-E"}},
        )

    add("horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": SCOPE_KEY, "horizon_id": f"{horizon_prefix}0"})
    horizon = f"{horizon_prefix}0"

    for index, s in enumerate(stmts):
        # Companion-presence admission (BOX2, kernel-enforced) requires the
        # companion already current *before* the subordinate (box1) fact
        # touches -- enforcement runs per-act against the fully-updated
        # successor state, so a same-batch-but-later act does not satisfy
        # it. Mirrors tests/test_ssa1099_benefits_line6_track2.py's own
        # "assert companions first" ordering for its box5/box3-6 companion
        # set. Plain "assertion" acts (not "member-transition") keep the
        # family on the genesis horizon; only the late-member path below
        # advances the horizon.
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.f1098e.box2.{index}",
                    _member_fact_id(BOX2, s.lender, s.stmt),
                    s.box2,
                )
            },
        )
        for token, value in s.witnesses.items():
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.f1098e.{token}.{index}",
                        _member_fact_id(f"tax.us.2025.f1098e.{token}", s.lender, s.stmt),
                        value,
                    )
                },
            )
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.f1098e.box1.{index}",
                    _member_fact_id(BOX1, s.lender, s.stmt),
                    s.box1,
                )
            },
        )

    if close:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.f1098e.closure",
                    f"{CLOSURE_TYPE}|family-horizon={horizon},tax-year=2025",
                    True,
                )
            },
        )

    if assert_sli_scope:
        sli_values = {token: "yes" for token in SLI_SCOPE_UNIVERSAL_TOKENS + SLI_SCOPE_LEGAL_ZERO_TOKENS}
        if sli_scope_overrides:
            sli_values.update(sli_scope_overrides)
        for token, value in sli_values.items():
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.sli-scope.{token}",
                        f"tax.us.2025.sli-scope.{token}|tax-year=2025",
                        value,
                    )
                },
            )

    if assert_sched1_scope:
        sched1_values = {token: "yes" for token in SCHED1_LINE_TOKENS}
        if sched1_overrides:
            sched1_values.update(sched1_overrides)
        for token, value in sched1_values.items():
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.sched1.{token}",
                        f"tax.us.2025.schedule1-adjustments-scope.{token}|tax-year=2025",
                        value,
                    )
                },
            )

    for item in extra or []:
        acts.append(item)

    adoption = _load_json(F1098E_ADOPTION)
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts

def _registry() -> Any:
    return install_domain_scoped_supersession(workspace_registry())


def _base_log(wages: float, bundle_version: str, amounts: tuple[tuple[str, float], ...]) -> Path:
    raw = tempfile.TemporaryDirectory(prefix="sli-correction-base-")
    directory = Path(raw.name) / "workspace"
    registry = _registry()
    log = ActLog(directory, registry)
    rows = _f1098e_acts(statements=[], close=True, wages=wages)
    rows.pop()
    for index, row in enumerate(rows):
        item = dict(row)
        item["committed_against"] = index
        item["act_id"] = f"demo.track5.base.{index:03d}"
        log.append(item, expected_revision=index)

    def append(kind: str, payload: dict[str, Any]) -> None:
        revision = log.read().revision
        log.append(_support_act(revision, kind, payload), expected_revision=revision)

    bundle = load_sli_relationship_source_bundle() if bundle_version == "v2" else _load_content("sli-relationship-source.bundle.json")
    append("bundle-adoption", {"bundle": bundle})
    for name, reference in Return.BORROWING.items():
        introduce_borrowing_reference_durably(
            log, registry, reference_id=reference, description=f"{name.title()} study loan",
            actor=USER, at="2026-10-03T09:00:00Z")
    for identity, label, kind in Return.ENTITIES:
        append("entity-introduced", {"entity": _demo_entity(identity, label, kind)})
    _append_source(log, registry, SCHOOL, Return.SCHOOL_KEYS["autumn"],
                   "Riverside College, BSc, autumn 2024", "track5-school-autumn")
    _append_source(log, registry, SCHOOL, Return.SCHOOL_KEYS["spring"],
                   "Riverside College, BSc, spring 2025", "track5-school-spring")
    for statement, amount in amounts:
        keys = Return.STATEMENT_KEYS[statement]
        _append_source(log, registry, BOX2, keys, False, f"track5-box2-{statement}")
        _append_source(log, registry, BOX1, keys, amount, f"track5-box1-{statement}")
    _adopt(log, V41_PACKAGE, V39_RELEASE)
    # Keep the temporary directory alive for the caller that copies it.
    directory_holder[str(directory)] = raw
    return directory


directory_holder: dict[str, tempfile.TemporaryDirectory[str]] = {}


def _adopt(log: ActLog, package_path: Path, release_path: Path) -> None:
    package = json.loads(package_path.read_text(encoding="utf-8"))
    release = json.loads(release_path.read_text(encoding="utf-8"))
    revision = log.read().revision
    item = _support_act(revision, "package-adoption", {
        "package": {"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]},
        "release": {"id": release["id"], "version": release["version"],
                    "checksum": hashlib.sha256(release_path.read_bytes()).hexdigest()},
        "scope": SCOPE, "revision": 1,
    })
    item["actor"] = USER
    log.append(item, expected_revision=revision)


class Return:
    """Recorder-built workspace on a full synthetic return."""

    BORROWING = {"autumn": "demo.track5.borrowing.autumn", "spring": "demo.track5.borrowing.spring"}
    ENTITIES = (
        ("demo.track5.period.autumn24", "Autumn 2024", "tax.us.educational-period"),
        ("demo.track5.period.spring25", "Spring 2025", "tax.us.educational-period"),
        ("demo.track5.institution.river", "Riverside College", "tax.us.educational-institution"),
        ("demo.track5.programme.bsc", "BSc", "tax.us.educational-programme"),
        ("demo.track5.lender.cedar", "Cedar Servicing", "tax.us.student-loan-lender"),
        ("demo.track5.lender.birch", "Birch Servicing", "tax.us.student-loan-lender"),
        ("demo.track5.statement.cedar", "2025 Form 1098-E from Cedar", "tax.us.1098e-statement"),
        ("demo.track5.statement.birch", "2025 Form 1098-E from Birch", "tax.us.1098e-statement"),
    )
    SCHOOL_KEYS = {
        "autumn": (("period", ENTITIES[0][0]), ("institution", ENTITIES[2][0]), ("programme", ENTITIES[3][0])),
        "spring": (("period", ENTITIES[1][0]), ("institution", ENTITIES[2][0]), ("programme", ENTITIES[3][0])),
    }
    STATEMENT_KEYS = {
        "cedar": (("lender", ENTITIES[4][0]), ("statement", ENTITIES[6][0]), ("tax-year", "2025")),
        "birch": (("lender", ENTITIES[5][0]), ("statement", ENTITIES[7][0]), ("tax-year", "2025")),
    }

    def __init__(self, *, wages: float = 50000, amounts: dict[str, float] | None = None,
                 bundle_version: str = "v2") -> None:
        amounts = {"cedar": 3000.0} if amounts is None else amounts
        base = _base_log(wages, bundle_version, tuple(sorted(amounts.items())))
        self.raw = tempfile.TemporaryDirectory(prefix="sli-correction-return-")
        shutil.copytree(base, Path(self.raw.name) / "workspace")
        held = directory_holder.pop(str(base), None)
        if held is not None:
            held.cleanup()
        self.registry = _registry()
        self.log = ActLog(Path(self.raw.name) / "workspace", self.registry)
        self.borrowing = dict(self.BORROWING)
        self.school = {name: fact_id_for(SCHOOL, keys) for name, keys in self.SCHOOL_KEYS.items()}
        self.statement_keys = {name: self.STATEMENT_KEYS[name] for name in amounts}
        self.statement = {name: fact_id_for(BOX1, keys) for name, keys in self.statement_keys.items()}
        self.claims: dict[tuple[str, str, str], str] = {}
        self._serial = 0
        self._common: set[str] = set()

    def _name(self, tag: str) -> str:
        self._serial += 1
        return f"{tag}-{self._serial}"

    def _review(self, name: str) -> dict[str, Any]:
        from packages.tax.sli_relationship_review import prepare_review

        return prepare_review(self.log, self.registry, review_id=f"demo.track4.review.{name}",
                              shown_at="2026-10-03T10:00:00Z",
                              borrowing_refs=tuple(self.borrowing.values()),
                              schooling_fact_ids=tuple(self.school.values()),
                              statement_fact_ids=tuple(self.statement.values()))

    def _clause(self, kind: str, borrowing: str, target: str, response: str) -> dict[str, Any]:
        financing = kind == "financing"
        return {"borrowing_ref": self.borrowing[borrowing],
                "schooling_fact_id": self.school[target] if financing else None,
                "statement_fact_id": None if financing else self.statement[target],
                "financing_response": response if financing else "unanswered",
                "inclusion_response": "unanswered" if financing else response}

    def link(self, kind: str, borrowing: str, target: str, response: str = "yes") -> None:
        from packages.tax.sli_relationship_review import save_review

        name = self._name(f"{kind}-{borrowing}-{target}-{response}")
        saved = save_review(self.log, self.registry, self._review(name),
                            **self._clause(kind, borrowing, target, response),
                            actor=USER, at="2026-10-03T10:01:00Z",
                            submission_id=f"demo.track4.submission.{name}",
                            evidence_id=f"demo.evidence.track4.{name}")
        if kind in saved["claims"]:
            self.claims[(kind, borrowing, target)] = saved["claims"][kind]["finding_id"]

    def outcome(self, kind: str, borrowing: str, target: str, outcome: str) -> None:
        from packages.tax.sli_relationship_review import answer_review_claim, withdraw_review_claim

        finding_id = self.claims.pop((kind, borrowing, target))
        if outcome == "withdrawn":
            withdraw_review_claim(self.log, self.registry, finding_id=finding_id, actor=USER,
                                  at="2026-10-03T10:02:00Z")
            return
        name = self._name(f"{kind}-{borrowing}-{target}-{outcome}")
        answer_review_claim(self.log, self.registry, finding_id=finding_id, review=self._review(name),
                            **self._clause(kind, borrowing, target, outcome),
                            actor=USER, at="2026-10-03T10:02:00Z",
                            submission_id=f"demo.track4.submission.{name}",
                            evidence_id=f"demo.evidence.track4.{name}")

    def answer(self, question: str, borrowing: str, response: str) -> None:
        from packages.tax.sli_relationship_review import (
            prepare_borrowing_answer_review,
            save_borrowing_answer_review,
        )

        name = self._name(f"{question}-{borrowing}-{response}")
        review = prepare_borrowing_answer_review(
            self.log, self.registry, review_id=f"demo.track4.review.{name}", shown_at="2026-10-03T10:00:00Z",
            borrowing_refs=tuple(self.borrowing.values()))
        save_borrowing_answer_review(
            self.log, self.registry, review, borrowing_ref=self.borrowing[borrowing],
            question=QUESTIONS[question], response=response, actor=USER, at="2026-10-03T10:03:00Z",
            submission_id=f"demo.track4.submission.{name}", evidence_id=f"demo.evidence.track4.{name}")

    def common_answers(self, statement: str = "cedar", *, skip: tuple[str, ...] = (),
                       values: dict[str, str] | None = None) -> None:
        self._common.add(statement)
        self.old_answers(statement, skip=(REPLACED, *skip), values=values)

    def old_answers(self, statement: str = "cedar", *, skip: tuple[str, ...] = (),
                    values: dict[str, str] | None = None) -> None:
        for tail in ANSWER_TAILS:
            if tail in skip:
                continue
            value = (values or {}).get(tail, "yes")
            _append_source(self.log, self.registry, f"tax.us.2025.f1098e.{tail}",
                           self.statement_keys[statement], value,
                           self._name(f"track5-{tail}-{statement}"))

    def acts(self) -> tuple[dict[str, Any], ...]:
        return ActLog(self.log.path.parent, self.registry).read().acts


def _link_complete(
    ws: Return, borrowing: str, school: str, statement: str, *,
    loan: str | None = "yes", enroll: str | None = "yes", financing: bool = True,
) -> None:
    if financing:
        ws.link("financing", borrowing, school)
    ws.link("statement-inclusion", borrowing, statement)
    if loan is not None:
        ws.answer("loan", borrowing, loan)
    if enroll is not None:
        ws.answer("enroll", borrowing, enroll)


def _birch_old(ws: Return) -> None:
    ws.old_answers("birch")


def _d1_populate(ws: Return) -> None:
    ws.old_answers("cedar")
    _link_complete(ws, "autumn", "autumn", "cedar", enroll=None)
    _link_complete(ws, "spring", "spring", "cedar")
    ws.outcome("statement-inclusion", "spring", "cedar", "no")
    _birch_old(ws)


def adopt_v42(ws: Return) -> None:
    package = json.loads(V42_PACKAGE.read_text(encoding="utf-8"))
    release = json.loads(V40_RELEASE.read_text(encoding="utf-8"))
    revision = ws.log.read().revision
    item = _support_act(revision, "package-adoption", {
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



OUT = ROOT / "packages" / "sample_data" / "sli_correction_t1"
CONTENT = OUT / "surface" / "content" / "app"

MANIFEST_ID = "demo.surface.sli-correction"
MANIFEST_VERSION = "v1"
RELEASE_ID = "demo.surface-release.sli-correction.2025"
RELEASE_VERSION = "v1"
ACT_ID = "demo.act.adopt.surface.sli-correction.v1"


def _document(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _jsonable(acts: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Round-trip through JSON so every seed act is a plain, serializable
    mapping, the same normalization every existing state already applied."""
    return [json.loads(json.dumps(act)) for act in acts]


def _validated(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for revision, act in enumerate(acts):
        if act.get("committed_against") != revision:
            raise RuntimeError("seed acts are not sequentially committed from zero")
    return acts


def seed_acts_base() -> list[dict[str, Any]]:
    """Two supported forms, on different borrowings, with v42 adopted."""

    ws = Return(amounts={"cedar": 1500.0, "birch": 800.0})
    with ws.raw:
        ws.link("financing", "autumn", "autumn")
        ws.link("statement-inclusion", "autumn", "cedar")
        ws.answer("loan", "autumn", "yes")
        ws.answer("enroll", "autumn", "yes")
        ws.common_answers("cedar")
        ws.link("financing", "spring", "spring")
        ws.link("statement-inclusion", "spring", "birch")
        ws.answer("loan", "spring", "yes")
        ws.answer("enroll", "spring", "yes")
        ws.common_answers("birch")
        adopt_v42(ws)
        acts = _jsonable(ws.acts())
    return _validated(acts)


def seed_acts_d1() -> list[dict[str, Any]]:
    """Cedar carries two borrowings: Autumn (affirmed, with financing and a
    yes loan-cost/enrollment answer) and Spring, whose inclusion on Cedar is
    denied; Cedar's own standing rests on an older yes. Birch is
    older-method only, with no borrowing of its own (plan, Track 2 item 1,
    state "d1")."""

    ws = Return(wages=50000, amounts=STANDARD)
    with ws.raw:
        _d1_populate(ws)
        adopt_v42(ws)
        acts = _jsonable(ws.acts())
    return _validated(acts)


def seed_acts_shared() -> list[dict[str, Any]]:
    """One borrowing ("Autumn study loan") included on both Cedar and Birch
    (plan, Track 2 item 1, state "shared")."""

    ws = Return(amounts={"cedar": 1200.0, "birch": 950.0})
    with ws.raw:
        ws.link("financing", "autumn", "autumn")
        ws.link("statement-inclusion", "autumn", "cedar")
        ws.link("statement-inclusion", "autumn", "birch")
        ws.answer("loan", "autumn", "yes")
        ws.answer("enroll", "autumn", "yes")
        ws.common_answers("cedar")
        ws.common_answers("birch")
        adopt_v42(ws)
        acts = _jsonable(ws.acts())
    return _validated(acts)


def seed_acts_blocked() -> list[dict[str, Any]]:
    """Cedar's borrowing ("Autumn study loan") starts with a recorded "no"
    loan-cost answer, so Cedar starts blocked; Birch ("Spring study loan")
    is unaffected and stays plain-case (plan, Track 2 item 1, state
    "blocked" -- the no -> yes correction case; the mirror image of
    ``tests.test_sli_correction_session.FirstWorkingExample``'s
    post-correction state, seeded as the starting state instead)."""

    ws = Return(amounts={"cedar": 1500.0, "birch": 800.0})
    with ws.raw:
        ws.link("financing", "autumn", "autumn")
        ws.link("statement-inclusion", "autumn", "cedar")
        ws.answer("loan", "autumn", "no")
        ws.answer("enroll", "autumn", "yes")
        ws.common_answers("cedar")
        ws.link("financing", "spring", "spring")
        ws.link("statement-inclusion", "spring", "birch")
        ws.answer("loan", "spring", "yes")
        ws.answer("enroll", "spring", "yes")
        ws.common_answers("birch")
        adopt_v42(ws)
        acts = _jsonable(ws.acts())
    return _validated(acts)


def _save_relationship(
    ws: Any, *, borrowing_ref: str, kind: str, response: str, actor: str, at: str, serial: int,
    schooling_fact_id: str | None = None, statement_fact_id: str | None = None,
) -> None:
    """Save one financing or statement-inclusion answer for an arbitrary
    borrowing reference -- the same shape as ``tests.test_sli_track4_support_chain
    .Workspace.link``, generalized past that helper's fixed ``self.borrowing``
    dict so a custom-labelled borrowing can be linked too."""
    from packages.tax.sli_relationship_review import prepare_review, save_review

    financing = kind == "financing"
    review = prepare_review(
        ws.log, ws.registry, review_id=f"demo.correction.review.dup.{serial}", shown_at=at,
        borrowing_refs=(borrowing_ref,),
        schooling_fact_ids=(schooling_fact_id,) if financing and schooling_fact_id is not None else (),
        statement_fact_ids=(statement_fact_id,) if not financing and statement_fact_id is not None else ())
    save_review(
        ws.log, ws.registry, review, borrowing_ref=borrowing_ref,
        schooling_fact_id=schooling_fact_id if financing else None,
        statement_fact_id=None if financing else statement_fact_id,
        financing_response=response if financing else "unanswered",
        inclusion_response=response if not financing else "unanswered",
        actor=actor, at=at, submission_id=f"demo.correction.submission.dup.{serial}",
        evidence_id=f"demo.evidence.correction.dup.{serial}")


def _save_borrowing_answer(
    ws: Any, *, borrowing_ref: str, question: str, response: str, actor: str, at: str, serial: int,
) -> None:
    """Save one ordinary-question answer for an arbitrary borrowing
    reference, generalized past ``Workspace.answer``'s fixed dict the same
    way ``_save_relationship`` generalizes ``Workspace.link``."""
    from packages.tax.sli_relationship_review import (
        prepare_borrowing_answer_review,
        save_borrowing_answer_review,
    )

    review = prepare_borrowing_answer_review(
        ws.log, ws.registry, review_id=f"demo.correction.review.dup.answer.{serial}", shown_at=at,
        borrowing_refs=(borrowing_ref,))
    save_borrowing_answer_review(
        ws.log, ws.registry, review, borrowing_ref=borrowing_ref, question=question, response=response,
        actor=actor, at=at, submission_id=f"demo.correction.submission.dup.answer.{serial}",
        evidence_id=f"demo.evidence.correction.dup.answer.{serial}")


def seed_acts_duplicate_labels() -> list[dict[str, Any]]:
    """Two borrowings both labelled "Starlight study loan" -- the sole,
    plain-case borrowing on Cedar, and the sole, plain-case borrowing on
    Birch -- distinguishable only by which form each is included on. A
    further, unlinked pair labelled "Twin study loan" is introduced with no
    relationships of its own and is truly identical (plan, Track 2 item 1,
    state "duplicate-labels"; item 5).

    The truly-identical pair is introduced in the same order
    ``tests.test_sli_correction_session._twin_borrowing_seed_acts`` already
    establishes is required: the first borrowing's answer is saved while it
    is still the only current borrowing with that label, and the second,
    relationship-free twin is introduced only afterward. Preparing a review
    against an *already*-indistinguishable pair is refused by
    ``_require_card_distinguishable_in_workspace``, which checks every
    current borrowing in the workspace, not merely the ones a caller
    selects.
    """

    ws = Return(amounts={"cedar": 1100.0, "birch": 900.0})
    with ws.raw:
        actor = USER
        starlight_cedar = "demo.correction.borrowing.starlight-cedar"
        starlight_birch = "demo.correction.borrowing.starlight-birch"
        twin_a = "demo.correction.borrowing.twin-a"
        twin_b = "demo.correction.borrowing.twin-b"

        introduce_borrowing_reference_durably(
            ws.log, ws.registry, reference_id=starlight_cedar, description="Starlight study loan",
            actor=actor, at="2026-10-09T00:00:00Z")
        _save_relationship(
            ws, borrowing_ref=starlight_cedar, kind="financing", schooling_fact_id=ws.school["autumn"],
            response="yes", actor=actor, at="2026-10-09T00:00:01Z", serial=1)
        _save_relationship(
            ws, borrowing_ref=starlight_cedar, kind="statement-inclusion",
            statement_fact_id=ws.statement["cedar"], response="yes", actor=actor,
            at="2026-10-09T00:00:02Z", serial=2)
        _save_borrowing_answer(
            ws, borrowing_ref=starlight_cedar, question="loan-paid-only-school-costs", response="yes",
            actor=actor, at="2026-10-09T00:00:03Z", serial=3)
        _save_borrowing_answer(
            ws, borrowing_ref=starlight_cedar, question="enrolled-at-least-half-time", response="yes",
            actor=actor, at="2026-10-09T00:00:04Z", serial=4)
        ws.common_answers("cedar")

        introduce_borrowing_reference_durably(
            ws.log, ws.registry, reference_id=starlight_birch, description="Starlight study loan",
            actor=actor, at="2026-10-09T00:00:05Z")
        _save_relationship(
            ws, borrowing_ref=starlight_birch, kind="financing", schooling_fact_id=ws.school["spring"],
            response="yes", actor=actor, at="2026-10-09T00:00:06Z", serial=5)
        _save_relationship(
            ws, borrowing_ref=starlight_birch, kind="statement-inclusion",
            statement_fact_id=ws.statement["birch"], response="yes", actor=actor,
            at="2026-10-09T00:00:07Z", serial=6)
        _save_borrowing_answer(
            ws, borrowing_ref=starlight_birch, question="loan-paid-only-school-costs", response="yes",
            actor=actor, at="2026-10-09T00:00:08Z", serial=7)
        _save_borrowing_answer(
            ws, borrowing_ref=starlight_birch, question="enrolled-at-least-half-time", response="yes",
            actor=actor, at="2026-10-09T00:00:09Z", serial=8)
        ws.common_answers("birch")

        introduce_borrowing_reference_durably(
            ws.log, ws.registry, reference_id=twin_a, description="Twin study loan", actor=actor,
            at="2026-10-09T00:00:10Z")
        _save_borrowing_answer(
            ws, borrowing_ref=twin_a, question="loan-paid-only-school-costs", response="yes",
            actor=actor, at="2026-10-09T00:00:11Z", serial=9)
        introduce_borrowing_reference_durably(
            ws.log, ws.registry, reference_id=twin_b, description="Twin study loan", actor=actor,
            at="2026-10-09T00:00:12Z")

        adopt_v42(ws)
        acts = _jsonable(ws.acts())
    return _validated(acts)


STATE_BUILDERS = {
    "base": seed_acts_base,
    "d1": seed_acts_d1,
    "shared": seed_acts_shared,
    "duplicate-labels": seed_acts_duplicate_labels,
    "blocked": seed_acts_blocked,
}


def _seed_log(state: str) -> bytes:
    return b"".join(
        json.dumps(act, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
        for act in STATE_BUILDERS[state]()
    )


def _content_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for path in sorted(CONTENT.rglob("*")):
        if not path.is_file():
            continue
        data = path.read_bytes()
        entries.append({
            "path": path.relative_to(CONTENT).as_posix(),
            "sha256": _sha256(data),
            "bytes": len(data),
        })
    return entries


def render_fixture_files() -> dict[str, bytes]:
    entries = _content_entries()
    manifest_body = {
        "schema": "surface-artifact.v1",
        "id": MANIFEST_ID,
        "version": MANIFEST_VERSION,
        # H4 (plan, Track 0 — readiness for implementation): resolution and
        # build never require Node; the one entry is already a built page.
        "build_command": "true",
        "entrypoint_html": "index.html",
        "entries": entries,
    }
    manifest_checksum = package_instance_checksum(manifest_body)
    manifest = dict(manifest_body, package_checksum=manifest_checksum)

    registry = {"packages": [
        {"id": MANIFEST_ID, "version": MANIFEST_VERSION, "checksum": manifest_checksum},
    ]}
    registry_bytes = _document(registry)
    release = {
        "schema": "release-registry.v1", "id": RELEASE_ID, "version": RELEASE_VERSION,
        "package_registry_sha256": _sha256(registry_bytes),
    }
    release_bytes = _document(release)
    adoption = {
        "schema": "act.v1", "act_id": ACT_ID, "kind": "surface-adoption",
        # Must match ``correction_session.SCOPE_USER``, since
        # ``select_current_adoption`` selects only that user's own adoption acts.
        "actor": "demo.user.filer", "at": "2026-10-08T00:00:00Z", "committed_against": 1,
        "payload": {
            "package": {"id": MANIFEST_ID, "version": MANIFEST_VERSION, "checksum": manifest_checksum},
            "release": {"id": RELEASE_ID, "version": RELEASE_VERSION,
                       "checksum": _sha256(release_bytes)},
            "scope": {"jurisdiction": "us", "year": "2025"}, "revision": 1,
            "audit": {"note": "synthetic SLI correction-session surface; non-authoritative"},
        },
    }

    files: dict[str, bytes] = {
        "surface/manifest/surface-artifact.sli-correction.v1.json": _document(manifest),
        "surface/registry/published-surface-artifacts.json": registry_bytes,
        f"surface/publication_surface/releases/{RELEASE_ID}.{RELEASE_VERSION}.json": release_bytes,
        "surface/adoptions/adopt-sli-correction-v1.json": _document(adoption),
    }
    # One seed act log per named state (plan, Track 2 item 1). Filenames are
    # ``correction_session.STATE_SEED_LOGS``'s own, so the runtime and this
    # generator can never drift apart on where a state's fixture lives.
    for state, path in STATE_SEED_LOGS.items():
        files[path.relative_to(CORRECTION_FIXTURE).as_posix()] = _seed_log(state)
    return files


def content_stats() -> tuple[int, int]:
    entries = _content_entries()
    return len(entries), sum(int(entry["bytes"]) for entry in entries)


def main() -> None:
    for relative, contents in render_fixture_files().items():
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)
    count, total = content_stats()
    print(f"sli_correction_t1 content: {count} entries, {total} bytes")
    print(f"sli_correction_t1 states seeded: {', '.join(sorted(STATE_SEED_LOGS))}")


if __name__ == "__main__":
    main()
