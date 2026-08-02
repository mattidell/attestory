# Charter: Track 2 — Contribution Machinery

Date: 2026-07-17. Foreman-authored implementation charter, **proposed for owner
approval** before implementation. Milestone: First Real Return Slice; Track 2 of
the amended Tracks. Lands on `track/frrs-t2-contribution-machinery`; branch +
pre-merge review gate + no-ff merge (ADR-0030).

- **Type:** implementation track (single implementer + author-independent pre-merge
  review gate; no rival — that is the prototype structure, already discharged).
- **Implements:** ADR-0032 (D2) runtime behavior over the Track-1 schema citizens,
  on **synthetic in-repo fixtures only**.

## Objective

Manual-entry contribution turns synthetic real-shaped values into
**provenance-bearing facts** through a recorded product event distinct from a run,
and a run **structurally consumes facts, not inputs**. Everything the D2 committee
left as a named production condition is discharged here or explicitly carried to
Track 3.

## Deliverables

1. **Contribution applicator.** A manual-entry `act-contribution.v1` batch produces
   `finding.v2` facts through the successor carrier acts (`act-assertion.v2` /
   `act-member-transition.v2`), each finding carrying `contribution_id`. Admission
   enforces ADR-0032 Decision 2: the contribution's `evidence_id` is a member of
   the finding's `evidence_ids`; the contribution pin stays out of
   `pins.finding_ids` (provenance-only, no derivation edge).
2. **Contribution record.** `contribution-record.v1` is written as the Article-14
   process account (started → terminal phase), and the schema is **registered** in
   the runtime registry so the record is admitted (ADR-0032 named condition).
3. **Runs consume facts, not inputs — the MUST condition (ADR-0032 Decision 3).**
   (a) `run-request.v1 ≠ RunContext` — closing the request does not close the
   evaluator input type; (b) a **marshal-only `RunContext` constructor** that
   builds the run context from current record state only; (c) a **live-entrypoint
   reachability kill-test** proving a directly-constructed / hand-assembled
   `InputFinding` (the `derive.py` fixture-adapter path) is unreachable from a live
   run. The Adversary's `7770000`-ghost-id bypass must be closed structurally, not
   by policy.
4. **E14.2 static check.** Package validation **rejects** a rule that declares a
   contribution as a dependency (the declaration-side half of runs-consume-facts).
5. **Schema wiring.** Register the Track-1 kernel/derivation contribution citizens
   (`act-contribution.v1`, `contribution.v1`, `contribution-record.v1`,
   `finding.v2`, `act-assertion.v2`, `act-member-transition.v2`, `run-request.v1`)
   in the runtime registries so acts admit and findings carry v2 provenance.
6. **Negative goldens the D2 ADR names.** Committed goldens for: a run reaching a
   raw input **fails** (kill-test); any-order equivalence (two contribution orders
   over independent facts → equal current state); correction-by-supersession (a new
   contribution supersedes via ordinary assertion; the family horizon does **not**
   advance; both findings on the record; no edit/withdrawal); and a same-member
   correction routed through member-transition **rejects** (SC-R2).

## Scope fence (do not cross)

- **No production resolver, no live-workspace bootstrap, no release/adoption
  behavior** — Track 3 (the D3 schemas exist as citizens; do not implement their
  resolution here). No RG-1 package repair here.
- **No W-2 closure mapping, no live-run harness** — Track 4. **No OCR, no UI.**
- **Synthetic in-repo fixtures only.** The D1 residency/leak wall is consumed
  conceptually; its *installed* gates are Track 3. No real data, ever.
- Do not edit the ratified ADRs or the Track-1 schema citizens (implement to them;
  a genuine schema defect is surfaced, not patched).

## Verification (all green, re-run and reported)

- `.venv/bin/python3 -m unittest` (full suite) green, fully synthetic.
- `.venv/bin/mypy packages tools tests` clean; `tools/governance_lint.py`
  conformant.
- The runs-consume-facts kill-test and the E14.2 static check are executed goldens,
  not asserted.
- Data-safety scan clean; every value/identifier synthetic.

## Review gate

Author-independent pre-merge review before merge (a charter for it is authored when
the branch is ready). Findings classified blocking / scope defect / production
condition / non-blocking. Owner-held merge (ADR-0030); owner-approved dispatch of
any sub-agent (ADR-0034).

## Exit criteria

A manually-entered synthetic contribution produces provenance-bearing facts a run
then consumes; the run has no structural path to a raw input (kill-test green); a
rule cannot name a contribution dependency (E14.2 green); correction supersedes
without horizon advance; all verification green; the D2 named production conditions
are discharged or explicitly carried to Track 3 in the branch's closing note.
