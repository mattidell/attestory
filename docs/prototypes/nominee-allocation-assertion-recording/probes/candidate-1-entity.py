"""Candidate 1 probe: a separately individuated allocation-statement entity.

Track 0 charter, checkpoint T0-A
Track 0, checkpoint T0-A.

This probe is executed, not read. It runs real acts through the real
committed kernel (``packages.kernel.act_log``, ``packages.kernel.facts``,
``packages.kernel.findings``, ``packages.kernel.currency``,
``packages.kernel.read_models``) -- no kernel code is modified, no test
file is touched.

Candidate 1's shape:

  - a "report" is an ordinary ``entity.v1`` citizen (kind
    ``demo.report-1099int``) -- one per identified Form 1099-INT report.
  - an "allocation statement" -- the user's ordinary claim that a stated
    amount from one identified report belongs to one named other person
    -- is *itself* a separately individuated ``entity.v1`` citizen (kind
    ``demo.nominee-allocation``), one per (report, owner) pair.
  - the recorded fact type is keyed on *both* entities:
    ``demo.nominee-allocation.amount`` with identity keys
    ``report`` (entity, kind ``demo.report-1099int``) and
    ``allocation`` (entity, kind ``demo.nominee-allocation``).
  - withdrawal is ``act-entity-superseded.v1`` against the allocation
    entity, with ``replacement`` omitted (the schema's own withdrawal
    case; see ``packages/schemas/kernel/act-entity-superseded.v1.schema.json``).

Committing mirrors the real production writer
(``packages/derivation/entry_loop.py``): every act is semantically
applied against a running ``FindingState`` (``findings.apply_act``)
*before* it is appended to the act log (``ActLog.append`` only checks
JSON-Schema shape, never kernel invariants -- appending a well-formed
but semantically illegal act would otherwise land in the log with no
warning, which this probe demonstrates explicitly is possible if that
pre-check is skipped).

Only synthetic ``demo.*`` / ``demo-*`` identities and values appear
anywhere in this file. No real taxpayer data. No absolute workstation
paths are written to any committed artifact (the workspace directory
used to run the act log lives under a temporary directory).
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT))

from packages.kernel import currency, facts, findings, read_models  # noqa: E402
from packages.kernel.act_log import ActLog, ActLogError  # noqa: E402
from packages.kernel.facts import FactModelError  # noqa: E402
from packages.kernel.findings import FindingModelError, _NO_CURRENT_VALUE, _current_value_for_fact  # noqa: E402
from packages.kernel.schema_registry import SchemaRegistry  # noqa: E402

SEP = "=" * 78


def line(msg: str = "") -> None:
    print(msg)


def header(title: str) -> None:
    line()
    line(SEP)
    line(title)
    line(SEP)


# ---------------------------------------------------------------------------
# Act builders (synthetic demo.* / demo-* identities only)
# ---------------------------------------------------------------------------

_AT_COUNTER = [0]


def _at() -> str:
    _AT_COUNTER[0] += 1
    n = _AT_COUNTER[0]
    return f"2026-09-05T00:{n // 60:02d}:{n % 60:02d}Z"


def make_act(index: int, kind: str, payload: dict[str, Any], actor: str) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"demo-act-{index:03d}",
        "kind": kind,
        "actor": actor,
        "at": _at(),
        "committed_against": index,
        "payload": payload,
    }


def entity(entity_id: str, kind: str, label: str) -> dict[str, Any]:
    return {"schema": "entity.v1", "id": entity_id, "kind": kind, "label": label}


def evidence(evidence_id: str, label: str, content: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "evidence.v1",
        "id": evidence_id,
        "kind": "demo.report-1099int-copy",
        "label": label,
        "content": content,
    }


def bundle() -> dict[str, Any]:
    return {
        "schema": "bundle.v1",
        "id": "demo.nominee-allocation-vocab",
        "label": "Demo nominee-allocation recording vocabulary",
        "fact_types": [
            {
                "schema": "fact-type.v1",
                "id": "demo.nominee-allocation.amount",
                "title": (
                    "Amount from one identified 1099-INT report the user says "
                    "belongs to one named other person"
                ),
                "nature": "determinable",
                "identity_keys": [
                    {
                        "name": "report",
                        "kind": "entity",
                        "entity_kind": "demo.report-1099int",
                    },
                    {
                        "name": "allocation",
                        "kind": "entity",
                        "entity_kind": "demo.nominee-allocation",
                    },
                ],
                "value_schema": {"type": "number", "minimum": 0},
                "supersession": {"policy": "free"},
            }
        ],
    }


def allocation_fact_id(report_id: str, allocation_id: str) -> str:
    return facts.fact_id_for(
        "demo.nominee-allocation.amount",
        (("report", report_id), ("allocation", allocation_id)),
    )


def finding(
    finding_id: str,
    fact_id: str,
    value: Any,
    evidence_ids: list[str],
    basis: str = "attested",
) -> dict[str, Any]:
    return {
        "schema": "finding.v1",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": basis,
        "evidence_ids": evidence_ids,
    }


def act_for_finding(acts: tuple[dict[str, Any], ...], finding_id: str) -> dict[str, Any] | None:
    """The exact join used to recover attribution: walk committed acts and
    find the one whose payload carries this finding id (assertion or
    member-transition carrier). Attribution (actor, time) lives only on the
    act envelope, never on the finding citizen itself (finding.v1 has no
    actor/at field)."""
    for act in acts:
        payload = act.get("payload", {})
        candidate = payload.get("finding")
        if isinstance(candidate, dict) and candidate.get("id") == finding_id:
            return act
        member = payload.get("member")
        if isinstance(member, dict):
            member_finding = member.get("finding")
            if isinstance(member_finding, dict) and member_finding.get("id") == finding_id:
                return act
    return None


class Rejected(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class Workspace:
    """A running (act log, semantic state) pair.

    ``commit`` mirrors the real writer path (``entry_loop.py``): it
    semantically applies the act to a running ``FindingState`` *before*
    appending it to the act log, and never appends an act that failed
    semantic application. ``append_unchecked`` skips the semantic
    pre-check on purpose, to demonstrate what the bare ``ActLog`` alone
    does and does not enforce.
    """

    def __init__(self, registry: SchemaRegistry) -> None:
        self.registry = registry
        self._tmp = tempfile.TemporaryDirectory()
        self.log = ActLog(Path(self._tmp.name), registry)
        self.state = findings.initial_state()
        self.idx = 0

    def cleanup(self) -> None:
        self._tmp.cleanup()

    def commit(self, kind: str, payload: dict[str, Any], actor: str = "demo-user-matt") -> dict[str, Any]:
        act = make_act(self.idx, kind, payload, actor)
        new_state = findings.apply_act(self.state, act, self.registry)  # semantic check first
        self.log.append(act, expected_revision=self.idx)  # then commit (schema-shape check only)
        self.state = new_state
        self.idx += 1
        return act

    def append_unchecked(self, kind: str, payload: dict[str, Any], actor: str = "demo-user-matt") -> dict[str, Any]:
        """Append straight to the log, skipping the semantic pre-check --
        demonstrates that ``ActLog`` alone validates JSON-Schema shape only."""
        act = make_act(self.idx, kind, payload, actor)
        self.log.append(act, expected_revision=self.idx)
        self.idx += 1
        return act

    def acts(self) -> tuple[dict[str, Any], ...]:
        return self.log.read().acts

    def view(self) -> currency.CurrencyView:
        return currency.compute_currency(self.state)

    def try_semantic(self, kind: str, payload: dict[str, Any]) -> tuple[bool, str | None]:
        """Try applying an act semantically WITHOUT committing it anywhere
        (neither to the running state nor to the log) -- pure dry run,
        exactly the shape ``apply_contribution_batch`` performs in the real
        writer before ``entry_loop.py`` ever calls ``ActLog.append``."""
        act = make_act(self.idx, kind, payload, "demo-user-matt")
        try:
            findings.apply_act(self.state, act, self.registry)
            return True, None
        except (FindingModelError, FactModelError) as exc:
            return False, str(exc)


def run() -> None:
    registry = SchemaRegistry()  # real committed packages/schemas/kernel
    ws = Workspace(registry)

    header("SETUP: bundle adoption, report entities, evidence")
    ws.commit("bundle-adoption", {"bundle": bundle()})
    ws.commit(
        "entity-introduced",
        {"entity": entity("demo-report-1099int-001", "demo.report-1099int", "Demo Payer Inc 1099-INT report 001")},
    )
    ws.commit(
        "entity-introduced",
        {"entity": entity("demo-report-1099int-002", "demo.report-1099int", "Demo Payer Inc 1099-INT report 002 (same payer)")},
    )
    ws.commit(
        "evidence-submitted",
        {
            "evidence": evidence(
                "demo-evidence-report-001",
                "Copy of demo 1099-INT report 001",
                {"report_id": "demo-report-1099int-001", "payer": "demo-payer-inc", "box1": 1000},
            )
        },
    )
    ws.commit(
        "evidence-submitted",
        {
            "evidence": evidence(
                "demo-evidence-report-002",
                "Copy of demo 1099-INT report 002",
                {"report_id": "demo-report-1099int-002", "payer": "demo-payer-inc", "box1": 900},
            )
        },
    )
    line(f"committed acts so far: {len(ws.acts())}")

    # -----------------------------------------------------------------
    header("A2 -- one owner's allocation records")
    # -----------------------------------------------------------------
    ws.commit(
        "entity-introduced",
        {"entity": entity("demo-alloc-r001-pat", "demo.nominee-allocation", "Pat's allocation of report 001")},
    )
    fact_id_pat_r001 = allocation_fact_id("demo-report-1099int-001", "demo-alloc-r001-pat")
    line(f"fact id for Pat/report-001: {fact_id_pat_r001}")
    ws.commit(
        "assertion",
        {"finding": finding("demo-finding-pat-r001-v1", fact_id_pat_r001, 600, ["demo-evidence-report-001"])},
    )
    view = ws.view()
    line(f"current finding ids: {sorted(view.current_finding_ids)}")
    a2_pass = "demo-finding-pat-r001-v1" in view.current_finding_ids
    line(f"A2 executed result: current={a2_pass}")

    # -----------------------------------------------------------------
    header("A3 -- several owners are distinguishable")
    # -----------------------------------------------------------------
    ws.commit(
        "entity-introduced",
        {"entity": entity("demo-alloc-r001-kim", "demo.nominee-allocation", "Kim's allocation of report 001")},
    )
    fact_id_kim_r001 = allocation_fact_id("demo-report-1099int-001", "demo-alloc-r001-kim")
    line(f"fact id for Kim/report-001: {fact_id_kim_r001}")
    ws.commit(
        "assertion",
        {"finding": finding("demo-finding-kim-r001-v1", fact_id_kim_r001, 400, ["demo-evidence-report-001"])},
    )
    view = ws.view()
    line(f"current finding ids: {sorted(view.current_finding_ids)}")
    distinct_fact_ids = fact_id_pat_r001 != fact_id_kim_r001
    both_current = {"demo-finding-pat-r001-v1", "demo-finding-kim-r001-v1"} <= view.current_finding_ids
    line(f"fact ids distinct: {distinct_fact_ids}")
    a3_pass = distinct_fact_ids and both_current
    line(f"A3 executed result: {a3_pass}")

    # -----------------------------------------------------------------
    header("A4 -- correcting Pat leaves Kim at the same identity and revision")
    # -----------------------------------------------------------------
    kim_finding_before = dict(ws.state.findings["demo-finding-kim-r001-v1"])
    kim_current_before = "demo-finding-kim-r001-v1" in view.current_finding_ids
    acts_before_correction = ws.acts()

    ws.commit(
        "assertion",
        {"finding": finding("demo-finding-pat-r001-v2", fact_id_pat_r001, 650, ["demo-evidence-report-001"])},
    )
    view = ws.view()
    kim_finding_after = dict(ws.state.findings["demo-finding-kim-r001-v1"])
    kim_current_after = "demo-finding-kim-r001-v1" in view.current_finding_ids

    acts_after_correction = ws.acts()
    new_acts = acts_after_correction[len(acts_before_correction):]
    kim_touched_by_correction = any("kim" in json.dumps(a["payload"]) for a in new_acts)

    identity_same = kim_finding_before == kim_finding_after  # record identity, not value equality
    pat_v1_displaced = "demo-finding-pat-r001-v1" in view.displaced_finding_ids
    pat_v2_current = "demo-finding-pat-r001-v2" in view.current_finding_ids
    line(f"Kim's finding record identical before/after (dict equality): {identity_same}")
    line(f"Kim's finding still current after Pat's correction: {kim_current_before} -> {kim_current_after}")
    line(f"Pat v1 displaced, reason: {view.reasons.get('demo-finding-pat-r001-v1')}")
    line(f"Pat v2 current: {pat_v2_current}")
    line(f"acts newly written during the correction: {[a['act_id'] for a in new_acts]}")
    line(f"any new act names Kim: {kim_touched_by_correction}")
    a4_pass = (
        identity_same
        and kim_current_before
        and kim_current_after
        and pat_v1_displaced
        and pat_v2_current
        and not kim_touched_by_correction
        and len(new_acts) == 1
    )
    line(f"A4 executed result: {a4_pass}")

    # -----------------------------------------------------------------
    header("A5 -- an allocation on report A cannot attach to / be mistaken for report B")
    # -----------------------------------------------------------------
    ws.commit(
        "entity-introduced",
        {"entity": entity("demo-alloc-r002-pat", "demo.nominee-allocation", "Pat's allocation of report 002")},
    )
    fact_id_pat_r002 = allocation_fact_id("demo-report-1099int-002", "demo-alloc-r002-pat")
    line(f"fact id for Pat/report-002: {fact_id_pat_r002}")
    ws.commit(
        "assertion",
        {"finding": finding("demo-finding-pat-r002-v1", fact_id_pat_r002, 900, ["demo-evidence-report-002"])},
    )
    view = ws.view()

    # The fact id a report-002 allocation entity for Pat WOULD need to answer
    # report 001's proposition is a different string entirely -- constructed
    # here to show it never matches any recorded finding's fact_id.
    cross_report_fact_id = allocation_fact_id("demo-report-1099int-001", "demo-alloc-r002-pat")
    cross_report_current_value = _current_value_for_fact(ws.state, cross_report_fact_id)
    report_001_pat_value = _current_value_for_fact(ws.state, fact_id_pat_r001)
    report_002_pat_value = _current_value_for_fact(ws.state, fact_id_pat_r002)
    fact_ids_distinct = fact_id_pat_r001 != fact_id_pat_r002
    line(f"report-001 Pat fact id: {fact_id_pat_r001}")
    line(f"report-002 Pat fact id: {fact_id_pat_r002}")
    line(f"fact ids distinct across reports: {fact_ids_distinct}")
    line(
        "current value under report-001+alloc-r002-pat (should be open/no-current, never 900): "
        f"{'<no current value>' if cross_report_current_value is _NO_CURRENT_VALUE else cross_report_current_value!r}"
    )
    line(f"current value under report-001+alloc-r001-pat: {report_001_pat_value!r}")
    line(f"current value under report-002+alloc-r002-pat: {report_002_pat_value!r}")

    # Adversarial, dry-run only (never committed to the running state or the
    # log): try citing report 002's evidence on a fresh assertion against
    # report 001's fact id. Evidence is provenance only (Article 1) -- this
    # is the honest limit, and it is deliberately NOT prevented by fact
    # identity, which is exactly what this dry run demonstrates.
    ok, err = ws.try_semantic(
        "assertion",
        {"finding": finding("demo-finding-cross-evidence-attempt", fact_id_pat_r001, 999, ["demo-evidence-report-002"])},
    )
    line(f"DRY RUN (never committed): cross-report evidence citation on report-001's own fact id blocked: {not ok}")
    if err:
        line(f"  (rejected: {err})")
    else:
        line(
            "  (kernel allows this at the semantic layer -- evidence is provenance, not identity; "
            "this is a documentary-quality concern, never a fact-identity leak, since the amount "
            "still only ever answers report-001's own fact id)"
        )

    a5_pass = fact_ids_distinct and cross_report_current_value is _NO_CURRENT_VALUE
    line(f"A5 executed result (fact-identity separation): {a5_pass}")

    # -----------------------------------------------------------------
    header("A6 -- withdrawal removes current support without a negative claim")
    # -----------------------------------------------------------------
    view_before_withdrawal = ws.view()
    pat_v2_current_before_withdrawal = "demo-finding-pat-r001-v2" in view_before_withdrawal.current_finding_ids
    line(f"Pat v2 current before withdrawal: {pat_v2_current_before_withdrawal}")

    withdrawal_act = ws.commit(
        "entity-superseded",
        {"entity_id": "demo-alloc-r001-pat"},  # replacement OMITTED -- withdrawal
    )
    view = ws.view()

    pat_v2_current_after = "demo-finding-pat-r001-v2" in view.current_finding_ids
    pat_v2_displaced_after = "demo-finding-pat-r001-v2" in view.displaced_finding_ids
    withdrawal_reason = view.reasons.get("demo-finding-pat-r001-v2")
    pat_v2_value_unchanged = ws.state.findings["demo-finding-pat-r001-v2"]["value"] == 650
    kim_still_current = "demo-finding-kim-r001-v1" in view.current_finding_ids
    withdrawal_wrote_a_finding = "finding" in withdrawal_act["payload"] or "member" in withdrawal_act["payload"]
    authorship_act = act_for_finding(ws.acts(), "demo-finding-pat-r001-v2")

    line(f"Pat v2 current after withdrawal: {pat_v2_current_after}")
    line(f"Pat v2 displaced after withdrawal: {pat_v2_displaced_after}, reason kinds: "
         f"{[r.kind for r in withdrawal_reason] if withdrawal_reason else None}")
    line(f"Pat v2's recorded value unchanged (still 650, not 0/false/negative): {pat_v2_value_unchanged}")
    line(f"Kim unaffected by Pat's withdrawal: {kim_still_current}")
    line(f"withdrawal act payload: {withdrawal_act['payload']} (no finding/member key -> no finding written)")
    line(f"withdrawal wrote a finding: {withdrawal_wrote_a_finding}")
    if authorship_act:
        line(
            f"authorship of withdrawn finding demo-finding-pat-r001-v2 recoverable: "
            f"act_id={authorship_act['act_id']} actor={authorship_act['actor']} at={authorship_act['at']}"
        )
    a6_pass = (
        pat_v2_current_before_withdrawal
        and not pat_v2_current_after
        and pat_v2_displaced_after
        and withdrawal_reason is not None
        and any(r.kind == "individuation" for r in withdrawal_reason)
        and pat_v2_value_unchanged
        and kim_still_current
        and not withdrawal_wrote_a_finding
        and authorship_act is not None
    )
    line(f"A6 executed result: {a6_pass}")

    # -----------------------------------------------------------------
    header("A11 -- can (report, owner) become current again after withdrawal?")
    # -----------------------------------------------------------------
    # Attempt 1: un-supersede/re-supersede the same entity -- there is no
    # "reactivate" applier in packages/kernel/facts.py; the only lever it
    # exposes is entity-superseded again, and apply_entity_superseded
    # requires the entity to currently be "current" -- it is not.
    ok, err = ws.try_semantic("entity-superseded", {"entity_id": "demo-alloc-r001-pat"})
    line(f"DRY RUN: supersede the withdrawn entity again -> blocked: {not ok}")
    if err:
        line(f"  error: {err}")

    # Attempt 2: assert directly onto the SAME fact id the withdrawn entity
    # answered. The lattice only ever projects facts for CURRENT entities
    # (packages/kernel/facts.py facts_of, include_displaced=False by
    # default), so the withdrawn entity's fact_id is absent from the
    # default lattice -- _validate_finding must reject it as unknown.
    ok, err = ws.try_semantic(
        "assertion",
        {
            "finding": finding(
                "demo-finding-pat-r001-v3-same-fact-id-attempt",
                fact_id_pat_r001,  # the exact same fact id as before
                650,
                ["demo-evidence-report-001"],
            )
        },
    )
    line(
        f"DRY RUN: assert a NEW finding on the SAME fact id ({fact_id_pat_r001}) "
        f"after withdrawal -> blocked: {not ok}"
    )
    if err:
        line(f"  error: {err}")
    same_fact_id_reassertion_blocked = not ok

    # Attempt 3: the exact path that DOES work -- a brand-new allocation
    # entity for the same (report, owner) proposition, with its own new
    # fact id.
    ws.commit(
        "entity-introduced",
        {
            "entity": entity(
                "demo-alloc-r001-pat-2",
                "demo.nominee-allocation",
                "Pat's allocation of report 001 (re-asserted after withdrawal)",
            )
        },
    )
    fact_id_pat_r001_reasserted = allocation_fact_id("demo-report-1099int-001", "demo-alloc-r001-pat-2")
    ws.commit(
        "assertion",
        {
            "finding": finding(
                "demo-finding-pat-r001-reasserted-v1",
                fact_id_pat_r001_reasserted,
                650,
                ["demo-evidence-report-001"],
            )
        },
    )
    view = ws.view()
    reassertion_current = "demo-finding-pat-r001-reasserted-v1" in view.current_finding_ids
    reassertion_new_fact_id = fact_id_pat_r001_reasserted != fact_id_pat_r001
    kim_untouched_by_reassertion = ws.state.findings["demo-finding-kim-r001-v1"] == kim_finding_after
    kim_still_current_after_reassertion = "demo-finding-kim-r001-v1" in view.current_finding_ids

    # True currency (the read-model view, currency.compute_currency): is the
    # OLD, withdrawn fact id answered by any CURRENT finding?
    old_fact_id_current_by_true_currency = any(
        ws.state.findings[fid]["fact_id"] == fact_id_pat_r001 for fid in view.current_finding_ids
    )

    # Contrast with findings._current_value_for_fact -- the internal
    # "last-inserted-wins" reader used only by specific enforcement checks
    # (subset invariants, companion presence, closed-on-attestation gates).
    # It consults state.withdrawn_fact_ids (populated ONLY by
    # member-transition remove/reclassify) but NEVER consults entity
    # individuation/supersession. This is executed, not inferred:
    internal_reader_value = _current_value_for_fact(ws.state, fact_id_pat_r001)

    line(f"re-assertion fact id: {fact_id_pat_r001_reasserted}")
    line(f"re-assertion current: {reassertion_current}")
    line(f"re-assertion fact id is a NEW/different fact id from the withdrawn one: {reassertion_new_fact_id}")
    line(
        "the OLD (withdrawn) fact id is NOT answered by any current finding, per true "
        f"read-model currency (currency.compute_currency): {not old_fact_id_current_by_true_currency}"
    )
    line(
        "CAVEAT -- executed, not inferred: findings._current_value_for_fact (the internal "
        "reader used ONLY by subset-invariant / companion-presence / closed-on-attestation "
        f"enforcement, never by the read model) still returns {internal_reader_value!r} for the "
        "withdrawn fact id -- it consults state.withdrawn_fact_ids (member-transition only) and "
        "never entity supersession, so it disagrees with true currency here. No domain rule in "
        "this probe's bundle uses that reader against demo.nominee-allocation.amount, so nothing "
        "is wrong for THIS milestone's scope -- but a future subset-invariant/companion rule "
        "declared over this fact type would silently see the withdrawn entity's old value as "
        "still live. Flagged as an open caveat, not a disqualifier."
    )
    line(
        "Kim's identity/revision still untouched by the whole withdraw+reassert sequence: "
        f"{kim_untouched_by_reassertion and kim_still_current_after_reassertion}"
    )

    a11_same_identity_possible = not same_fact_id_reassertion_blocked  # never demonstrated
    a11_new_identity_possible = (
        reassertion_current and reassertion_new_fact_id and not old_fact_id_current_by_true_currency
    )
    line(f"A11 executed result: same-fact-identity reassertion possible: {a11_same_identity_possible}")
    line(f"A11 executed result: new-fact-identity reassertion possible: {a11_new_identity_possible}")

    # -----------------------------------------------------------------
    header("Bonus: ActLog alone does not enforce kernel semantics (schema-only)")
    # -----------------------------------------------------------------
    # Demonstrates the gap the Workspace.commit() wrapper closes above by
    # pre-applying semantically. Appended straight to a FRESH throwaway log
    # (never mixed into the probe's real log), so this cannot corrupt any
    # of the results already reported.
    scratch_registry = SchemaRegistry()
    scratch_ws = Workspace(scratch_registry)
    scratch_ws.append_unchecked("bundle-adoption", {"bundle": bundle()})
    scratch_ws.append_unchecked(
        "entity-introduced",
        {"entity": entity("demo-alloc-scratch", "demo.nominee-allocation", "Scratch allocation")},
    )
    # No report entity, no evidence, no fact type covering it: this is a
    # completely bogus entity-superseded payload the *envelope schema*
    # happily accepts (entity_id is just a free string) -- ActLog.append
    # writes it with zero semantic complaint.
    scratch_ws.append_unchecked("entity-superseded", {"entity_id": "demo-entity-that-was-never-introduced"})
    line(
        "ActLog accepted an entity-superseded act naming an entity that was "
        "never introduced -- schema validation alone permits this; only "
        "findings.project()/facts.apply_act() over the read-back acts raises:"
    )
    try:
        findings.project(scratch_ws.acts(), scratch_registry)
        raised = False
    except FactModelError as exc:
        raised = True
        line(f"  project() raises on replay: {exc}")
    line(f"semantic error only surfaces on projection/replay, not on append: {raised}")
    scratch_ws.cleanup()

    # -----------------------------------------------------------------
    header("History, attribution join, and coupling -- summary reads")
    # -----------------------------------------------------------------
    acts = ws.acts()
    read_model = read_models.build_read_model(acts, registry)
    line(f"total committed acts: {len(acts)}")
    line(f"total distinct fact ids the read model has ever projected: {len(read_model['facts'])}")
    all_finding_ids = sorted(ws.state.findings)
    line(f"all finding ids ever recorded (never deleted -- history_by_fact retains all): {all_finding_ids}")
    line(f"current finding ids (final): {sorted(ws.view().current_finding_ids)}")
    line(
        "attribution join used throughout: finding_id -> the committed act whose "
        "payload.finding.id (or payload.member.finding.id) equals it -> act['actor'], act['at']. "
        "No actor/time field exists on the finding citizen itself (finding.v1 schema has no such property)."
    )
    for fid in all_finding_ids:
        a = act_for_finding(acts, fid)
        if a:
            line(f"  {fid}: actor={a['actor']} at={a['at']} act_id={a['act_id']}")
        else:
            line(f"  {fid}: NO OWNING ACT FOUND (unexpected)")

    header("RESULT SUMMARY")
    line(f"A2  one owner records:                              {a2_pass}")
    line(f"A3  several owners distinguishable:                  {a3_pass}")
    line(f"A4  correcting Pat leaves Kim untouched at identity: {a4_pass}")
    line(f"A5  report A cannot be mistaken for report B:        {a5_pass}")
    line(f"A6  withdrawal without a negative claim:             {a6_pass}")
    line(f"A11 same-fact-id reassertion possible:               {a11_same_identity_possible}")
    line(f"A11 new-fact-id reassertion possible:                {a11_new_identity_possible}")

    ws.cleanup()


if __name__ == "__main__":
    run()
