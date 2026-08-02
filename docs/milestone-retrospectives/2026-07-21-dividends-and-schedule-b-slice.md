# Retrospective — Dividends and Schedule B Slice

Written 2026-07-21 by the principal foreman as the Track 5 completion record.
This is the milestone where the product proved its second hard trace case:
Schedule B's $1,500 attachment conditional, walkable end to end, alongside a
new worksheet pattern (line 16's QDCG shape over declared-absence facts) that
generalizes past this one line. The phase's standing test — *does the product
now do something for its user that it could not do before?* — is met a
second time: the owner's real 1099-DIV facts now flow through the same
return, growing it to Schedule B and the QDCG-adjusted line 16.

## Milestone

Carry the owner's real 1099-DIV facts through the existing contribution
boundary; grow lines 3a/3b and line 9; compute — with a walkable trace —
whether Schedule B exists and, if so, deliver the whole form (Part I/II
itemizations tying to 2b/3b, Part III via two contributed taxpayer-assertion
facts); make line 16 the QDCG worksheet over contributed declared-absence
facts.

## What shipped

- **Four gate contracts, ratified with rival-backed evidence:** ADR-0035
  (D3 — two per-box 1099-DIV families, `dividend-universe.v1`, 1b ≤ 1a
  admission-locus rejection, 3a ≤ 3b by construction), ADR-0036 (D1 — the
  attachment citizen: three atomic states, `collect_members` itemization,
  `ITEMIZATION_TIE_OUT_VIOLATION`, presence-semantics Part III, demonstrated
  generically on a Schedule D stub), ADR-0037 (the generic
  `conditional_dependency_set` evaluator-node contract D2 needed as a
  prerequisite, not D2 content itself), ADR-0038 (D2 — the QDCG worksheet:
  declared-absence citizens, single-successor/lazy-reduction/present-yes
  posture, bidirectional admission-locus interlock kill-tested all three
  orders).
- **The schema citizens and composition/conditional machinery** implementing
  them (Tracks 1–3), each merged per-track under ADR-0030 with
  author-independent pre-merge review.
- **The live path** (Track 4): confirming goldens proving the closure and
  line-9 mechanisms generalize to the dividend families under the v6-pinned
  package, an extended `tools/scaffold_live_acts.py`, and the composed
  whole-slice `live_coordinate_run` golden (Schedule B + QDCG resolving
  together) that no earlier track's tests exercised.
- **The real run itself** — performed by the owner alone in a quarantined
  workspace; its entire repo-side existence is the three-fact non-descriptive
  attestation (milestone plan, Verification, PR #40).
- **Process work landed alongside the milestone, not gating it:** ADR-0030's
  PR-vs-commit amendment, ADR-0039 (advisory index/routing), ADR-0040
  (trusted-advisor seat), canonical role seed files under `docs/roles/`, and
  retirement of the old foreman role template in favor of
  `docs/roles/foreman.md` as single source.

## Verification (at close)

Full `.venv/bin/python3 -m unittest` (509 tests at Track 2/3/4), mypy,
governance lint, per-track safety scans, and `tools/envelope_scan.py`. All
synthetic; the real run's evidence is the attestation only.

## What went right

- **The per-track review chain caught a real defect before merge, again.**
  Track 2's review found F1 — Schedule B Part I's tie-out compared itemized
  box-1 rows against line 2b's *full four-family sum*, which would have
  spuriously misfired for any filer with interest from more than one
  1099-INT source. Every Track 2 fixture happened to hold non-box-1 interest
  at zero, so the green suite had no idea; the reviewer's own re-derivation
  (not trust in the report) found it. Repaired narrowly, with a regression
  golden, before merge — the same ADR-0030 thesis (merge unit = review unit)
  held again.
- **The charter-named authoritative-surface golden class, promoted as a
  standing requirement from the First Real Return Slice retrospective, did
  its job.** Every track's charter named its golden class in advance; Track
  4's composed golden (Schedule B + QDCG resolving together in one
  `live_coordinate_run`) is what actually made the real run possible — no
  earlier track's tests exercised that combination, and without it the
  owner's first real attempt would have found the gap live instead of in
  review.
- **A missing ratification was caught before it became a defect, not after.**
  On resuming as foreman post-Track-2-merge, D2 (line 16) turned out never
  to have been ratified — Track 3's plan text presumed an ADR that did not
  exist, and the D2 prototype had stalled at a not-confirmed confirmation
  round since before ADR-0037 merged. The foreman chartered a repair and a
  second confirmation round rather than proceeding on an unratified
  contract; ADR-0038 ratified cleanly on the second pass. Caught at the
  right layer — before any Track 3 content was built on top of it, not
  after.
- **The boundary held under a second real run's pressure.** The owner's
  first workspace attempt refused honestly (`RELEASE_ABSENT_OR_MISMATCH`
  against a stale package pin); the diagnosis stayed entirely structural
  (reproduced from committed fixtures) and the fix was rebuilding the
  workspace from the updated scaffold — no live detail crossed during a
  second real debugging loop.

## What went wrong — honestly

- **A shared-`.git`-refs race clobbered the primary checkout's `main` branch
  pointer, twice, during Track 4's dispatch.** A foreman foreground command
  and a concurrently-dispatched agent's worktree setup collided; one
  incident briefly reached `origin/main` before being caught and corrected.
  No commits were lost (reflog-recoverable both times), but it was closer to
  data loss than any incident in the prior milestone. Root cause: running
  foreground git mutations on the primary checkout while a background
  agent's worktree isolation was still being established.
- **The D2 ratification gap existed for longer than it should have.** It
  originated at plan approval — Track 3's plan text was written presuming a
  ratification that had not happened — and was not caught until a foreman
  resumed post-merge and read the prototype state directly rather than
  trusting the plan text. Cheaper to catch at plan-review time than
  mid-milestone, though it was still caught before any dependent content was
  built, unlike the shape of defect the First Real Return Slice retrospective
  warned about.
- **One builder dispatch was interrupted by an API session-limit error
  mid-task** (Track 2, deliverables 3–4). The foreman reconciled the
  uncommitted work directly rather than re-dispatching blind, finding it
  substantially correct with one wrong test expectation and one mypy bug.
  Worked out, but reconciling an interrupted dispatch's state without a
  fresh independent read is exactly the kind of judgment call ADR-0034's
  dispatch discipline exists to make rare, not routine.

## The pattern, sharpened

The First Real Return Slice's lesson — *drive the claimed path from the
authoritative surface* — held under a second milestone's load: naming the
golden class in the charter up front, not after a gap is found, is what
turned "the composed Schedule-B-plus-QDCG path was never tested" from a
live-run surprise into a Track 4 deliverable. This milestone's own candidate
addition: **a plan's presumed-ratified contract is a claim, not a fact until
re-checked against the actual decision record** — Track 3's plan text
presumed ADR-0038 existed before it did, and the gap surfaced only because a
foreman re-read the prototype's own state rather than the plan's summary of
it. Future milestone plans that name a decision topic's ADR before that ADR
is ratified should mark the reference as provisional, not settled.

## Process notes

- ADR-0034 (owner approval per sub-agent dispatch) operated throughout; all
  review seats were owner-dispatched; Track 5 is foreman-in-session by
  direct owner instruction, per its own charter.
- The owner-held run tooling (`tools/scaffold_live_acts.py`,
  `workspace-seed/`) stayed deliberately untracked through a second real run
  and a second workspace rebuild — the pattern from the prior milestone held.
- The "PR for every unit including pure documentation" correction (ADR-0030
  amendment, mid-milestone) means this milestone's process record is more
  complete than the prior one's: the D2/ADR-0038 prototype-and-ratification
  work briefly went to `main` directly before the correction, an exception
  the amendment does not retroactively fix but that is binding for
  everything after.

## Deferrals

Recorded in
`docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/dividends-schedule-b-slice-deferral-ledger.md`
— fourteen entries, none silently closed; three new to this milestone (the
declared dividend-universe exclusion, Schedule B Part I's single-family
scope, and Track 4's scaffold-visibility observation), one prior-ledger
entry re-affirmed as touched but not retired
(the marshaller binding-route simplification), the rest carried untouched.
Highest priority, unchanged from the prior ledger: guarded transport /
credential confinement, which alone holds the data-boundary row at L3 across
every domain the matrix now covers.

## Data safety

No personal values, identifiers, workspace locations, or run dispositions
appear in any commit, review, charter, process log, or this retrospective;
the attestation sentence is the only real-run fact on record. Safety scans
and the installed envelope gates were green at every merge and at
attestation recording.

## Closing note

Attestory's real return slice now covers a second income class and its
first schedule attachment, computed under the same auditable,
refusal-honest, provably-quarantined mechanism the first milestone
established — proof the boundary and the review discipline generalize, not
just the first domain they were built for. The milestone's most transferable
output is the sharpened lesson above: a plan's cited ADR is a claim to
re-verify, not a fact to inherit.
