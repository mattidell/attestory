<!-- foreman-context-v1
{
  "version": 1,
  "topic": "presentation-row-completion",
  "milestone_state": "planned",
  "status": "PLANNED 2026-07-28. A RECORDS milestone, and deliberately so. It raises the four remaining Presentation cells (Interest 2b, Dividends 3a/3b, Return-level conditions, Schedule attachments) from L2 to L3 on the strength of the session ALREADY PERFORMED on 2026-07-27 — not a new one. That session rendered all nine published lines and Schedule B Parts I and II from real data; the surface was verified to cover all five columns before this plan was written, so there is no build gap and no hidden one. The owner amends the existing attestation to name the four columns; the foreman moves four cells with a footnote that states plainly that ALL FIVE rest on ONE session so no later reader infers four sittings. On close the matrix is uniformly L3 or better in every cell, which is the intended Real Return phase boundary. Two gaps carry forward UNCLOSED and are named rather than dropped: the classified-refusal path still has no human confirmation (it needs a session to exercise, and this milestone performs none), and the runbook's unidentified unclarity stands. Track 1 is owner-operated; Track 2 is foreman records plus a phase-close recommendation.",
  "scope": [
    "the owner amends the 2026-07-27 attestation to name the Interest, Dividends, Return-level conditions, and Schedule attachments columns, stating observation of each explicitly",
    "raise those four Presentation cells from L2 to L3 with a footnote that states all five columns rest on one session",
    "record the two carried gaps as unclosed and carry them into the next phase",
    "assess whether Real Return closes, and recommend"
  ],
  "non_goals": [
    "no new viewing session, no new browser launch, no new real-data operation of any kind",
    "no code change; no runbook change; no change to the evaluation harness or its manifests",
    "no descriptive detail of the 2026-07-27 session anywhere — the amendment names columns, which is not describing content",
    "no data-boundary maturity movement; that row's L3 ceiling is ratified and permanent (ADR-0044 line 164)",
    "no claim that the classified-refusal path was confirmed, and no claim that four sessions occurred",
    "no new tax rule, form field, citation, schedule, domain, published schema, or citizen",
    "no change to ADR-0031, ADR-0044, ADR-0046, or ADR-0047"
  ],
  "deep_reads": {
    "implementation": [
      "docs/phases/real-return/milestones/presentation-row-completion.md",
      "docs/reviews/2026-07-27-presentation-real-session-attestation-track3-attestation.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/real-return/milestones/presentation-row-completion.md",
      "docs/phases/real-return/maturity-matrix.md",
      "docs/reviews/2026-07-27-presentation-real-session-attestation-track3-attestation.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "dispatch": [
      "docs/roles/foreman.md#Dispatch",
      "AGENTS.md#Dispatch authorization"
    ],
    "merge_or_records": [
      "docs/roles/foreman.md#Standing disciplines",
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ],
    "new_milestone": [
      "docs/phases/real-return/maturity-matrix.md",
      "docs/phases/real-return/real-return-roadmap.md"
    ]
  }
}
-->

# Milestone: Presentation — Completing the Row

Audience: Product (planning instrument); Shared (status)

Phase: Real Return. Selected by the owner 2026-07-28.

## Objective

Move the four remaining Presentation cells — **Interest (2b)**, **Dividends
(3a/3b)**, **Return-level conditions (status, 12, 15, 16)**, and **Schedule
attachments** — from L2 to L3, completing the row.

On close, **every cell in the maturity matrix is L3 or better.** That is the
intended Real Return phase boundary and the reason this milestone is worth doing
now rather than later.

## What kind of milestone this is

**A records milestone.** It performs no session, launches no browser, touches no
real data, and changes no code. It raises four cells on the strength of a
session **already performed on 2026-07-27**, by having the owner amend that
session's attestation to name the columns it covered.

This is stated plainly at the top because it is unusual, and because the risk of
a records milestone is that a later reader mistakes it for four separate
sittings. Every artifact this milestone produces must foreclose that reading.

## Why this is legitimate on the ratified terms

Three facts, in order.

**The surface covers all five columns, verified rather than assumed.** Before
this plan was written, the production-shaped presentation fixture was inspected
directly: it carries sections for lines 1a, 2b, 3a, 3b, 9, 11, 12, 15, and 16,
and a Schedule B citation group with Part I (interest, box-1 / 1099-INT family)
and Part II (ordinary dividends, box-1a / 1099-DIV family). `_resolve_attachment`
in `packages/derivation/presentation_projection.py` projects attachments into the
model. There is no build gap and no hidden one. The previous milestone's
closeout said "no build gap" too and Track 1 then found three code defects, so
this was checked rather than inherited.

**The 2026-07-27 session rendered that surface from real data.** One session,
one render, the whole return.

**L3 asserts that the capability operated — not that the owner audited it.**
Footnotes 7 and 11 have said so since 2026-07-18: "L3 asserts the *capability
operated*, not any particular disposition." Extending the claim to columns the
same session rendered is therefore a statement of the same kind already ratified,
not a weaker one.

## The one thing only the owner can supply

ADR-0031 Decision 7's shape includes that the owner **observed dispositions in
quarantine**. Naming a column asserts observation of that column.

The plan does not assume this and cannot verify it. The amended attestation must
state it, so that the record says what was actually true rather than what was
on screen. If the owner did not observe a given column's content during the
session, **that column does not move**, and the milestone closes with fewer than
four cells raised. That outcome is a success, not a failure — it is the control
working.

## Scope

As the capsule's `scope`.

## Non-goals

As the capsule's `non_goals`. Two worth restating:

- **No new session.** The owner directed this explicitly. Nothing here launches a
  browser or touches the residency.
- **No claim beyond observation.** The footnote asserts capability operation for
  the columns the owner names, on one session, and nothing else.

## Data safety

The amendment names **columns**, which is not describing content — the same
distinction the previous milestone's plan drew when it noted the owner may name
additional columns at attestation time. Everything else is unchanged and
unrelaxed: no value, identifier, disposition, screenshot, residency locator, path
fragment, canonicalized form, or derived identifier in the repository, a review,
the PR, chat, or the retrospective.

No real data is accessed by this milestone at all.

## Gaps that do not close here, and why

Both carry into the next phase **named**, not dropped:

1. **The classified-refusal path has no human confirmation.** That a browser
   which fails to start arrives as a stable reason code rather than a traceback
   rests on tests and independent review only. Closing it requires a session to
   exercise it in, and this milestone performs none. It is the oldest open gap on
   this path.
2. **The runbook has an unidentified unclarity**, reported by its first human
   user, sentence unknown. Closing it requires someone to use the runbook again.

Neither is a blocker for the cells being raised: both concern the *failure* path
and the *instructions*, while the claim concerns the capability that operated.
They are restated here so the next phase inherits them explicitly.

## Verification

No code changes, so the suite is a regression check rather than evidence:

```text
pytest
python -m mypy
python tools/governance_lint.py
python tools/envelope_scan.py --range main..HEAD
```

**This block is the CI `verify` sequence deliberately.** The previous milestone's
charters listed a narrower floor that omitted `mypy`, and a strict-mode type
error consequently survived a build, two repairs, and three independent review
passes with everyone reporting green in good faith. A verification floor quietly
narrower than the gate reports green on work that is not.

## Exit criteria

1. The 2026-07-27 attestation carries a dated amendment naming the columns the
   owner observed, stating observation explicitly, and remaining non-descriptive.
2. The maturity matrix shows Presentation at L3 in every column the owner named,
   with a footnote stating that **all five columns rest on one session**,
   performed 2026-07-27, and that four were added by amendment.
3. The footnote claims capability operation, not disposition correctness, and
   does not imply more than one session occurred.
4. Both carried gaps are recorded as unclosed, with the reason.
5. A phase-close recommendation is on the record, with the matrix state that
   supports it.
6. No descriptive detail anywhere; `envelope_scan.py` clean over the full range.

## Review gates

**Track 1** has no agent work to review; its gate is the foreman checking the
amendment against ADR-0031 Decision 7's shape and ADR-0047 precondition 5 before
filing.

**Track 2** is reviewed for exactly one failure mode: **does any artifact read as
though more than one real session occurred?** The matrix footnote, the
retrospective, the phase-state briefing, and the PR body are each read for that.
Secondary: every cited SHA resolves, no cell moved that the owner did not name,
the data-boundary row is untouched, and the envelope scan is clean.

## Tracks

### Track 1 — The owner amends the attestation

Owner-operated. The owner states which of the four columns they observed during
the 2026-07-27 session, and affirms that the amendment adds no descriptive
detail. The foreman files it as a dated amendment section inside
`docs/reviews/2026-07-27-presentation-real-session-attestation-track3-attestation.md`,
so the record and its history stay in one place.

The five ADR-0047 preconditions are **not re-affirmed** — they were affirmed for
the session on 2026-07-27 and this milestone performs no new session. The
amendment says so explicitly rather than restating them, which would falsely
suggest a second act.

### Track 2 — Records and phase assessment

Foreman. Move the named cells with the footnote required by exit criteria 2–3.
Record both carried gaps. Write the retrospective. Update
`docs/phase-state.md`. Assess whether Real Return closes — the phase has no
pre-written ladder, only the standing test *"does the product now do something
for its user that it could not do before?"* — and put a recommendation on the
record for the owner's decision.

## Execution economy

Almost nothing. No builder, no reviewer, no dispatch. One owner statement and one
foreman records pass, on one branch, reaching `main` as a single PR at close.

## Execution record

Filled in as tracks complete.
