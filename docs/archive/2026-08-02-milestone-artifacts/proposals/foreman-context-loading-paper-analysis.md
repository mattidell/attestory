# Paper Analysis — Foreman Context Loading

Related plan: `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/foreman-context-loading.md`.
Candidate decision: ADR-0042.

## Gate 0 — decision inventory

| ID | Proposition | Tier | Scope boundary |
| --- | --- | --- | --- |
| FC1 | A foreman may begin from a generated, provenance-bearing capsule plus action-specific deep reads rather than a wholesale prose load. | 2, process | Routing only; no authority is condensed or displaced. |
| FC2 | The capsule must read one explicit committed Git ref, name its source blobs, and refuse malformed or contradictory volatile state. | 2, process/tooling | No working-tree content, network remote, credential, or workspace access. |
| FC3 | The five-retrospective read is required before planning a new milestone, but not on every execution-resume. | 2, process | No exemption for a new milestone plan. |

FC1 is primary. FC2 and FC3 are tightly dependent: without provenance and a
clear load boundary, a short brief would merely hide drift or weaken planning.

## Gate 1 — eligibility

| Proposition | Blast radius | Migration cost | Residual uncertainty | Cannot test cheaply in implementation | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| FC1 | 2 | 1 | 1 | 1 | 5 |
| FC2 | 2 | 1 | 1 | 1 | 5 |
| FC3 | 1 | 1 | 1 | 0 | 3 |

Scores 4–5 require a paper spike and ADR draft, not a rival build prototype.
The alternatives are distinguishable from existing documents and synthetic Git
fixtures; no unresolved production substrate or user-facing boundary requires a
prototype rung.

## Gate 2 — paper instantiation

### Positive A — coherent prototype re-entry

A foreman selects `origin/main`, whose phase state names an active prototype
topic, milestone plan, prototype plan, and seat record. The capsule exposes the
assigned foreman role, planning-only status, synthetic stop condition, no
dispatch permission, and the paths/blob ids supporting each statement. The
foreman reads the full dispatch ADRs and charter only if the owner authorizes a
launch. The capsule saves repeat reading but cannot authorize a dispatch.

### Positive B — ordinary implementation resume

A foreman selects a committed track branch. The capsule reports the branch's
dirty-state warning and points to the active plan, track, verification floor,
and merge/records deep-read set. Before claiming the track complete, the
foreman reads the controlling verification and merge instructions and runs
them; the capsule itself cannot turn a green-looking status into completion.

### Negative A — inconsistent active state

Phase state names topic `alpha`, while the seat says `beta`. A prose-only boot
could miss the mismatch or choose one by familiarity. The capsule rejects the
selected ref and reports the conflicting relative paths and values. It does not
fall back to `HEAD`, the working tree, or another remote ref.

### Negative B — stale or dirty checkout

A foreman is on a local branch behind `origin/main` with uncommitted edits. A
working-tree summary could blend current state with a planned but uncommitted
state. The capsule reads only `--ref`'s committed blobs, reports the branch and
porcelain state separately, and leaves the foreman to reconcile before acting.

### Lifecycle

`foreman selects ref -> renderer resolves one commit -> renderer reads declared
tracked sources -> validates shared identifiers -> emits compact routing record
with source blobs -> foreman chooses proposed action -> foreman performs the
mapped full reads -> action follows its existing approval/review rules`.

The capsule is never on the authority path: an accepted ADR, plan, charter,
role, or governance clause remains controlling whenever it applies.

### Producer → authority → consumer → failure map

| Produced datum | Owning authority | Consumer | Failure behavior |
| --- | --- | --- | --- |
| Active phase/plan pointer | `docs/phase-state.md` | Capsule, foreman | Missing or unparsable pointer refuses. |
| Current status/next permitted action | `docs/foreman-handoff.md` | Capsule, foreman | Topic/status disagreement refuses. |
| Scope, non-goals, deep-read triggers | active milestone plan | Capsule, foreman | Missing action map refuses. |
| Assigned seat, rung, stop conditions | prototype `SEAT.md` | Capsule, foreman | Missing/mismatched seat refuses. |
| Binding decision text | accepted ADR/governance/role documents | Foreman at action time | Capsule only routes; full text controls. |
| Revision identity | selected Git commit and blob ids | Foreman/reviewer | Unresolvable ref or source refuses. |

## Alternatives compared

| Shape | Result |
| --- | --- |
| Full corpus on every resume | Safe but repeatedly expensive; it obscures the operational question beneath repeated history and reminders. |
| Hand-maintained summary file | Rejected: a second narrative authority drifts, repeating the failure ADR-0030 was designed to prevent. |
| LLM/generic compression | Rejected: lossy and untestable; cannot prove source revision or preserve negative conditions. |
| Binary compression | Rejected: it saves storage, not model context; an expansion step recreates the same prose. |
| Generated capsule plus deep reads | Selected: compact, deterministic, source-attributed, and explicitly non-normative. |

## Conclusion

Paper evidence distinguishes the alternatives and exposes no question requiring
a prototype implementation before the process contract can be ratified. FC1 and
FC2 converge on a deterministic advisory capsule; FC3 preserves the expensive
retrospective read exactly where it protects new-milestone planning. This is
sufficient evidence for a Tier 2 ADR, not a claim that a renderer has already
been implemented.
