# Source Completeness Prototype - Process Log

Dated, event-only entries while rounds are open; outcome summaries at round
close (log hygiene per `roles/foreman.md`).

## 2026-07-12

- Foreman seat taken by this session (Fable 5) on owner instruction to begin
  the milestone; no predecessor for this topic — no succession entry needed.
- Topic directory created: `plan.md` (Gates 0–8 instantiated), `SEAT.md`,
  role files under `roles/` (foreman specialized from
  `docs/prototypes/_role-templates/foreman.md`; builder and reviewer files
  adapted from the tax-citizen-families topic; no starved legibility seat per
  ADR-0013 amendment).
- Status: plan awaiting solo owner approval. No charter written.
- Owner approved `plan.md` (solo review per ADR-0013) and said "begin";
  foreman records that instruction as the per-spawn confirmation for the it1
  builder. Plan status line updated to approved.
- `charter-it1.md` issued: rung 1 paper, SC-P1/P2/P3 only, branch
  `prototypes/source-completeness/it1`, examination ≤ 200 lines.
- Dispatch: Builder it1 spawned as foreman sub-agent at High tier / high
  effort, exactly as the plan's Gate 8 table assigns — no tier revision.
- Session note: owner flagged the session limit is near; foreman handoff note
  (`docs/foreman-handoff.md`) refreshed for mid-iteration succession.
- Owner directed a halt of the it1 builder sub-agent; stopped before any
  deliverable was produced (it had completed grounding reads and created the
  branch only). Empty branch ref `prototypes/source-completeness/it1`
  (pointing at `10c0b01`, zero commits) deleted. Charter it1 remains issued
  and unworked; builder count under Gate 4 stays 0 of 2 used, since no
  iteration artifacts exist. Re-dispatch requires fresh per-spawn owner
  confirmation.
- Foreman succession: Codex session took the foreman seat on the owner's
  instruction to continue progress. Git reconciliation found that the it1
  branch had subsequently landed `d47d12c` with four paper deliverables,
  superseding the handoff note's empty-branch state.
- Conformance check: `d47d12c` changes only the four charter-permitted
  documents; `examination-it1.md` is 114 lines (cap 200); no code or production
  schema changed; the builder remained at rung 1. Builder count is now 1 of 2.
- Foreman error: the succeeding foreman ran the mechanical conformance read
  before recording succession, contrary to the role file's ordering rule.
  Corrected immediately in this log; no artifact-quality judgment or mutation
  occurred.
- Owner instruction: do not spawn builder agents unless explicitly instructed.
  Rival dispatch is paused regardless of the plan's ordinary next action.
- Iteration 1 integrated to `main`; tip `d47d12c` preserved as immutable tag
  `exhibits/source-completeness/it1`; concluded branch deleted. No builder was
  dispatched during integration.
- Owner explicitly instructed the foreman to spawn the rival builder.
  `charter-it2.md` issued at rung 1 for SC-P1/P2/P3 on
  `prototypes/source-completeness/it2`; rival remains High tier / high effort,
  unchanged from Gate 8 because clean-room novel synthesis remains the task.
- Dispatch: clean-room rival spawned as `/root/source_completeness_rival_it2`
  with no forked conversation context. Its read allowlist names only the rival
  role, governance, ADR-0011, plan, and `charter-it2.md`; iteration 1 outputs,
  exhibit tags, examinations, reviews, seat/log, and handoff were explicitly
  denied.
- Foreman error / isolation incident: the rival initially switched the shared
  primary checkout instead of creating a separate worktree. Before artifact
  work began, a foreman dispatch-record commit (`518a4c9`) consequently landed
  on the rival branch. The rival stopped immediately, attested it had created
  no files or commits and had not read the accidental commit, and the foreman
  moved the dispatch record to `main` as `7537002`, restored the rival branch to
  `de22faa`, and created isolated worktree
  `/tmp/finances-source-completeness-it2`. Rival work then resumed there. No
  incumbent-artifact context leak occurred; the branch history is clean.
- Iteration 2 conformance: commit `82ffb7f0` changes only `it2/design.md` and
  `examination-it2.md`; examination is 99 lines (cap 200); no code or
  production schema changed; rung 1 held. Builder cap is now 2 of 2 used.
- Iteration 2 integrated to `main`; tip `82ffb7f0` preserved as immutable tag
  `exhibits/source-completeness/it2`; concluded branch and isolated worktree
  deleted.
- Committee round 1 assembled in `round-1.md`: governance-fidelity and
  adversary only, both High tier / high effort as planned, with parity across
  both paper designs and no rung climb authorized.
- Dispatch: governance reviewer `/root/sc_round1_governance` and adversary
  reviewer `/root/sc_round1_adversary` spawned concurrently in separate
  contexts, branches, and worktrees. Each was denied the same-round peer output
  and assigned the unchanged High/high Gate 8 tier.
- Both reviews completed independently and passed mechanical conformance:
  governance 115/150 lines, adversary 140/150 lines, one permitted output each.
  Reviews landed on `main`; isolated worktrees and review branches removed.
- Gate 5 triage recorded in `round-1-triage.md`. Decision-blocking: SC-P1 real
  enforcement remains unmeasured; incumbent SC-P2 collision/rekeying; both
  SC-P3 family/claim definitions fail adversary alignment. Production
  conditions: caller-set API removal, schemas/structural suites, rival identity
  anti-duplication, selected-mapping uniqueness/pins. SC-D1 remains deferred.
  Recommendation: Gate 6 partial continuation for SC-P1/SC-P2, defer SC-P3,
  owner-authorize rung 2 for SC-P1 only; no rung 3 or repair pass.
- Owner ratified the round-1 disposition and authorized the SC-P1 rung-2
  climb. Owner requested continuity of the original it1 builder and directed
  the foreman to prepare state and report when to resume it; foreman will not
  spawn the builder.
- `charter-it3.md` issued as the plan's single owner-authorized repair pass:
  rung 2 validator/resolver mutations, SC-P1 only, both surviving authority
  shapes, presence-only mutant, exact-pin identity, and caller-injection/
  ambiguity negatives. Rung 3, production work, SC-P2, SC-P3, and SC-D1 remain
  unauthorized. Builder tier stays High/high for the cross-rival defect seam.
- Owner delegated iteration-continuation and evidence-rung progression decisions
  to the foreman within the approved plan and caps. Owner input is required only
  for a genuine process block or when a builder intentionally kept outside the
  foreman's spawned agents must resume in another thread. Iteration 3 is such an
  external-builder handoff; its resume state is prepared and reported.
- Owner supplied handoff feedback: `it3` obscured that the work is a repair
  pass, incumbent-builder continuity and the builder completion contract lived
  outside durable role state, and the owner prompt duplicated the charter.
  Before build work began, foreman renamed the state to `repair1` /
  `charter-repair1.md`, encoded repair continuity and completion/readback
  contracts in the builder role, bound seat→charter→branch→worktree, and added
  the two-message external-builder handshake to the canonical and specialized
  foreman roles. No prototype artifact was discarded.
- Owner clarified iteration posture: prefer additional focused rounds over
  punting a central unresolved problem when each round has a bounded question,
  cost, artifact set, and pass/fail result. Foreman retains scope/economy duty:
  adjacent questions, open-ended evidence, and unmeasurable builds are still
  rerouted or stopped rather than absorbed.
- Repair1 returned commit `5eee68c`; foreman initially compared the branch to
  newer `main` and incorrectly reported that the builder touched foreman-owned
  state. Commit inspection showed only the three charter-permitted artifacts;
  correction issued immediately. This was a foreman comparison-base error, not
  a builder role breach.
- Repair1 conformance: examination 118/200 lines; resolver and mutation suite
  only; no production imports/edits. Foreman reran 15 tests: all pass. Evidence
  proves current literal-true-only admission, exact authority pins, ambiguity
  blocking, caller-set exclusion at the resolver boundary, and kills presence,
  currency-blind, and truthy mutants for both mapping shapes.
- Repair1 integrated and preserved as `exhibits/source-completeness/repair1` at
  `5eee68c`; branch/worktree deleted. The single planned repair-pass cap is now
  consumed.
- Stop-and-decide after the cap: repair1 identified exactly the plan's declared
  real-path uncertainty—whether resolved membership is the sole writer through
  the two-layer collect check. Under the owner's delegated progression authority
  and stated preference for bounded iterations over punting central questions,
  foreman authorized `charter-repair2.md`: one throwaway evaluator copy, SC-P1
  only, no production work. This is an explicit additional bounded pass beyond
  the original repair cap, not silent expansion.
- Repair2 conformance: commit `6144b65` changes only the three charter-permitted
  artifacts; examination is 126/200 lines; no production imports or edits.
  Foreman reran 11 end-to-end prototype tests: all pass for both mapping shapes.
  The copied two-layer path blocks false/absent/displaced/truthy/ambiguous and
  caller-injected authority through publication, pins the exact current finding,
  and kills caller-union and presence-only mutants.
- Foreman disposition: SC-P1's declared executable uncertainty is answered; no
  further builder iteration is warranted. Remaining seam removal, production
  pins, and persisted displacement are milestone production conditions, not
  prototype gaps. Repair2 integrated and preserved as
  `exhibits/source-completeness/repair2` at `6144b65`; branch/worktree deleted.
- Committee round 2 assembled to review executable SC-P1 evidence. Governance
  and adversary remain High/high; conditional expressiveness opens at
  Medium/medium because the evidence now includes a throwaway evaluator. No
  tier changes from the approved plan.
