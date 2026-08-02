# Charter: Track 2 — Composition and Conditional Machinery (Dividends and Schedule B Slice)

Date: 2026-07-19. Prepared by the foreman. Branch:
`track/dsbs-t2-composition-conditional-machinery`. Governing contracts:
ADR-0035, ADR-0036, the milestone plan's Track 2 section and
Contracts/Data-safety/Verification sections
(`docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/dividends-schedule-b-slice.md`), the
attachment-ontology synthesis
(`docs/archive/2026-08-02-milestone-artifacts/prototypes/attachment-ontology/synthesis.md`) and the dividend-
composition rival examination
(`docs/archive/2026-08-02-milestone-artifacts/prototypes/dividend-composition/examination-it2.md`), and the
citizens Track 1 landed (`packages/content/tax/2025/family.f1099div-*`,
`closure-mapping.f1099div-*`, `dividend-universe.v1`,
`packages/schemas/tax/attachment-rule.v1.schema.json`,
`packages/derivation/package_validation.py`'s admission guards).

## Scope basis

The milestone's Track 2 description is terse ("3a/3b composition behavior,
line-9 content extension, the Schedule B existence conditional and its
trace, over synthetic fixtures"), but both ADRs bound their remaining
production conditions to Tracks 1–3, and Track 3 is dedicated solely to line
16/D2 — unrelated to 1099-DIV composition or the attachment. The synthesis
and rival examination are explicit that the mechanisms this track owes are
machinery, not just the trigger: `collect_members` is "a named new
mechanism (production condition, Track 1/2)" (schema surface landed in
Track 1; the mechanism itself is owed here); the tie-out invariant is
"Tracks 1–2 build"; the 1b ≤ 1a subset check's "named locus must be
admission machinery (Track 2 production condition)". Track 2 is therefore
read as: everything ADR-0035/0036 owe short of line 16 (Track 3) and
closure content/live integration (Track 4) — the full attachment build-out,
not only its existence conditional. **This scope reading is a foreman
judgment call over a genuinely terse plan sentence; flagged to the owner
for confirmation before build dispatch, not settled by this charter alone.**

## Goal

Land the composition and conditional machinery ADR-0035/ADR-0036 owe beyond
schema citizens: the admission-time subset enforcement and same-batch
ordering for 1099-DIV, the 3a/3b/line-9 rule content, and the complete
Schedule B attachment — existence conditional, itemization via
`collect_members`, the tie-out invariant, and Part III completeness — with
the coordinator-from-facts goldens the milestone's Verification section
names as this milestone's authoritative surface.

## Deliverables

1. **1099-DIV admission-time subset enforcement (ADR-0035 decision 4).**
   The 1b ≤ 1a invariant enforced at tax-layer admission — after per-finding
   `value_schema` validation, before state mutation — on every path that
   admits a box1a or box1b finding (assertion or member transition).
   Rejection semantics, each with a test: qualified present with ordinary
   absent rejects; qualified > ordinary rejects; a correction of the
   ordinary value re-checks the current qualified value for the same
   statement; removing ordinary while qualified remains current rejects. A
   violating pair is never recorded (rejection, not recording).

2. **Same-batch admission ordering (ADR-0035 adversary-minor production
   condition).** Define and kill-test admission ordering when both boxes'
   findings for one statement arrive in the same contribution batch, so the
   paired check cannot be sequenced around (e.g., admitting 1b before 1a
   within one batch must not let a stale-view check pass a genuinely
   violating pair). ADR-0032 terminal contribution-batch failure applies.

3. **Lines 3a/3b composition (ADR-0035 decisions 1–2, D3).** Ordinary
   dividend line 3b composes from box 1a over the closed
   `tax.us.2025.f1099div.1a` family; qualified line 3a composes from box 1b
   over `tax.us.2025.f1099div.1b`. Each line `require_closed`s only its own
   family (per-box closure independence): closed-empty publishes an honest
   zero; undeclared or open blocks that line independently. Both lines flow
   to form-field dispositions with citations, following the committed
   line-2b pattern.

4. **Line 9 extension (Tier 1 content).** Total income absorbs line 3b under
   the existing line-9 rule contract — content only, no reopened contract.

5. **Schedule B attachment — existence conditional (ADR-0036 decisions 1–2).**
   The attachment rule citizen instantiated for Schedule B: the requirement
   conditional is declared rule content over the interest (2b-side) and
   ordinary-dividend (3b-side) subtotals, strictly-greater-than the cited
   $1,500 threshold parameter (exactly $1,500 is not over), with citation.
   Not-required publishes the atomic `guard_inapplicable`-family disposition
   (inputs, threshold, citation, per-trigger outcome — never silence).
   Sibling line rules (3a/3b/2b/line-9) never reference the attachment
   symbol — verify against committed runner source that a blocked
   attachment cannot propagate to a line.

6. **Itemization via `collect_members` (ADR-0036 decision 3, production
   condition 4).** Build the named mechanism: Part I/II rows pin the member
   findings of the same closed family, at the same horizon, that lines
   2b/3b already collected; rows subtotal; each subtotal ties to its named
   line (2b, 3b). Row shape (payer + amount) is Schedule-B content, not
   ontology — keep it that way; do not generalize row shape into the
   generic attachment schema (already closed in Track 1).

7. **Tie-out invariant (ADR-0036 production condition 1).** The
   derivation-time check that the itemization's row-sum equals its line's
   published value, same closed family, same horizon. Violation hard-fails
   the attachment derivation only — never publishes a divergent form, never
   blocks the line. Both named kill-tests required: stale row set (a row's
   source finding superseded after subtotal but before tie-out) and stale
   line (the line's published value superseded independent of the
   itemization). Use the `ITEMIZATION_TIE_OUT_VIOLATION` vocabulary Track 1
   already added to the record/walk schemas — do not add a new code.

8. **Part III completeness (ADR-0036 decisions 1, 4).** Two new contributed
   taxpayer-assertion fact types on the Track-1-landed categorical `{yes,
   no}` pattern: foreign financial account, foreign trust. Completeness
   checks each required answer's presence independently before any value is
   read (a `no` is a present answer; no evaluation order may mask an
   absent answer — test this directly, not by inspection). A `yes` on
   foreign-account adds the 7b country requirement to the required set and
   *names* the FinCEN-114 obligation (never produces it — no FinCEN-114
   content, filing, or form-field of any kind). A `yes` on foreign-trust
   behaves likewise for its own named obligation, if any is ratified —
   otherwise state explicitly what ADR-0036 requires here and do not
   invent unratified obligation content. Every answer finding is pinned
   unconditionally regardless of value, so supersession has an input edge
   both ways.

## Verification — authoritative-surface golden class (mandatory, named)

Per the milestone's promoted lesson ("every behavior track's charter names
its authoritative-surface golden class explicitly... a green suite without
these named goldens is not evidence") and the standing lesson from the
Track 0a review chain (an author-independent review found paper-case
coverage split between `live_coordinate_run` and a disallowed `RunContext`
shortcut) — **every one of the following must be an executed golden
entering through `live_coordinate_run` from an authoritative act log, never
a `RunContext` shortcut**:

1. 3a/3b publication (both present; qualified-zero/ordinary-present; both
   families closed-empty; one family undeclared/open blocking its line
   only).
2. Line 9 with dividends folded in.
3. Schedule B attachment, not-required outcome (both subtotals at or below
   threshold).
4. Schedule B attachment, required-and-complete outcome — the whole form:
   Part I/II itemizations tying to 2b/3b, Part III both answers present
   (both `no`; at least one `yes` with its branch content, e.g. 7b
   country).
5. Schedule B attachment, required-and-incomplete outcome — honest block
   naming exactly the missing required answer(s), independently for each
   answer absent alone and both absent together.
6. The 1099-DIV same-batch ordering kill-test (deliverable 2) and the two
   tie-out kill-tests (deliverable 7, stale row set and stale line) —
   these may be runner/admission-level tests rather than coordinator
   goldens where the defect is not fact-log-observable, but must be
   executed, not asserted by comment.

Additionally: full `.venv/bin/python3 -m unittest`, `.venv/bin/python3 -m
mypy`, `.venv/bin/python3 tools/governance_lint.py`, and `.venv/bin/python3
tools/envelope_scan.py --range main..HEAD` — all green before handoff.

## Boundary

No line-16/D2 content (Track 3). No 1099-DIV closure-mapping *content*
changes beyond what Track 1 already landed. No live-run harness extension,
owner real data, or workspace access (Track 4). No FinCEN-114 filing
content of any kind — naming the obligation is in scope, producing it is
not. Does not reopen D1/D2/D3 ratified decisions or Track 0/1 citizens
except where this track's own admission-time subset/ordering checks
require new code in the admission path (deliverables 1–2) — any such
change is additive, not a reinterpretation of Track 1's guards. Owner-held
run tooling (`tools/scaffold_live_acts.py`, `workspace-seed/`) stays
untracked. All fixtures and goldens are manufactured `demo.*`/`demo-*`
data — the owner's real 1099-DIV shapes inform synthetic fixtures only by
re-expression, per the milestone's Data-safety section.

## Review gate

One integrated per-track branch and review unit (ADR-0030): an
author-independent pre-merge review follows completion; the owner holds
the merge. Given this track's size (two ADRs' remaining production
conditions in one branch), the review charter should consider whether a
single delta review suffices or whether the foreman should propose an
interim checkpoint — the foreman's call at handoff, not pre-decided here.
