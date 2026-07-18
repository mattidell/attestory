# Retrospective — First Real Return Slice

Written 2026-07-18 by the principal foreman as the Track 5 completion record.
This is the milestone where the product crossed its own synthetic boundary: it
now computes its user's actual return slice, under a data boundary that is
itself a ratified contract. The phase's standing test — *does the product now
do something for its user that it could not do before?* — is met for the first
time in the literal sense the phase was named for.

## Milestone

Carry the owner's real W-2 / 1099-INT facts through a contribution boundary
into a live out-of-repo workspace, resolve a production package, and produce
the owner's actual Form 1040 lines 1a/2b/9/11/12/15/16 with full explanations
— while the repository provably carries zero personal data.

## What shipped

- **Three gate contracts, ratified with rival-backed evidence:** ADR-0031
  (real-data residency: out-of-repo by rule, capability wall, total
  fail-closed classifier, no committed locator), ADR-0032 (contribution as a
  first-class product event distinct from a run; `finding.v2` provenance;
  runs-consume-facts made structural at the runtime input), ADR-0033
  (production package resolution: user adoption pins a verified release;
  bytes verified before a strict exclusive graph resolves).
- **The schema citizens, machinery, and resolver** implementing them (Tracks
  1–3), each merged per-track under ADR-0030 with author-independent
  pre-merge review.
- **The live path** (Tracks 4/4b/4c): W-2 closure mapping as immutable
  horizon-keyed v3 content, the live-run coordinator, repo-side installed
  byte-verified commit/push envelope gates, and the repaired live inputs
  (rounding convention, coordinator-from-facts golden).
- **The real run itself** — performed by the owner alone in a quarantined
  workspace; its entire repo-side existence is the three-fact non-descriptive
  attestation (milestone plan, Verification, PR #20).

## Verification (at close)

Full `.venv/bin/python3 -m unittest` (433+ tests at Track 4c; re-run green at
this track), mypy, governance lint, per-track safety scans, and the installed
envelope gates byte-verified. All synthetic; the real run's evidence is the
attestation only.

## What went right

- **The per-track review chain caught real defects before every merge.**
  Track 3's review found F1 (a schema-invalid co-located release could leak a
  typed-fail-closed violation); Track 4's found a forgeable envelope guard, a
  late path refusal, and a mislabelled quantity; the post-merge Tracks 1–4
  review found ADR-0031's hook condition discharged only as an in-process
  model (→ Track 4b). Every catch produced a scoped, chartered,
  independently re-reviewed repair. ADR-0030's thesis — merge unit = review
  unit — held under load for the first sustained multi-track run.
- **The foreman's synthetic dry run was the milestone's decisive guard.** The
  live path on `main` could not publish any line (F1 record-pin drift, F2
  missing rounding vocabulary, F3 unkeyable W-2 closure) — and the green
  433-test suite had no idea, because no golden drove `live_coordinate_run`
  from an authoritative fact log. The dry run found in minutes what the suite
  structurally could not. Lesson promoted below.
- **The boundary held under support pressure.** The owner's workspace
  preparation hit a pre-flight failure; the debugging loop ran entirely on
  structure — the committed synthetic seed reproduced the *mechanism* clean,
  the owner ran structure-only greps locally, and the fix stayed owner-side.
  A live support interaction completed with zero quarantine detail crossing,
  which is the boundary's first real-world test of its *workflow*, not just
  its scanner.
- **The pre-flight failure was itself the product working.** The kernel
  refused a closure naming a horizon no transition had introduced — exactly
  the class of quiet wrongness (a "closed" family not covering a document)
  the horizon-keyed closure design exists to make a hard error.

## What went wrong — honestly

- **Track 4 shipped goldens that never drove the live entrypoint from facts
  on record.** Root cause of all three live-path defects, and a repeat of the
  Foundation phase's central lesson in a new costume: green proves what was
  driven, not what is owed. The prior phase's version was "the author wrote
  the tests too"; this phase's version is "the goldens started downstream of
  the authoritative surface." The Track 4c repair added the missing golden
  class (coordinator-from-facts), but the class should have been named in the
  Track 4 charter's verification section from the start.
- **ADR-0031's hook condition was discharged as a model, not an
  installation.** The in-process `LiveWorkspace` gates satisfied the letter
  of the tests while a raw `git commit` never met them. Caught by the
  owner-directed post-merge review, fixed by Track 4b — but it is the same
  "looks done, isn't" shape the phase keeps finding, and it was found *after*
  merge, unlike every other catch this milestone.
- **The milestone plan carried a stale evidence contract into the milestone.**
  The original "the disposition report is what reviews cite" wording
  contradicted sensitivity inheritance and had to be corrected by version
  mid-milestone (2026-07-16). Cheap to fix, but the contradiction was
  ratifiable at plan approval — a plan-review gap, not a build gap.

## The pattern, sharpened

Foundation's diagnosis was *shrink the unit until state can't hide inside
it*. This milestone adds the adjacent discipline: **drive the path you claim,
from the surface the user actually enters.** Every defect that survived to
`main` this milestone — the three live-path defects, the in-process hook
model — was a claim verified somewhere *downstream* or *beside* the real
entry surface. The fix each time was the same: a golden or gate at the
authoritative boundary itself (coordinator-from-facts golden; a real
`git commit` refused by a real installed hook). Charters should name the
authoritative-surface golden class explicitly in verification sections.

## Process notes

- ADR-0034 (owner approval per sub-agent dispatch) operated throughout; all
  review seats were owner-dispatched; Tracks 4b/5 were foreman-in-session by
  direct owner instruction.
- The owner-held run tooling (`tools/scaffold_live_acts.py`,
  `workspace-seed/`) is deliberately untracked — the repo carries the
  mechanism, never the operator's convenience surface for real values. This
  worked well and is worth keeping as a pattern.
- Correction discipline inside `L` (edit freely before the first successful
  run; supersession only after) proved understandable in practice.

## Deferrals

Recorded in `docs/phases/real-return/milestones/first-real-return-slice-deferral-ledger.md`
— eleven entries, none silently closed. Highest priority: guarded transport /
credential confinement, which alone holds the data-boundary row at L3.

## Data safety

No personal values, identifiers, workspace locations, or run dispositions
appear in any commit, review, charter, process log, or this retrospective;
the attestation sentence is the only real-run fact on record. Safety scans
and the installed envelope gates were green at every merge and at attestation
recording.

## Closing note

Attestory now does the thing it was named for: the owner's real return slice
computed under an auditable, refusal-honest, provably-quarantined mechanism.
The milestone's most transferable outputs are a boundary that survived
contact with a real support loop, and a verification lesson — *drive the
claimed path from the authoritative surface* — that belongs in every future
charter's verification section.
