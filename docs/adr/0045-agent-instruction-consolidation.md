# ADR 0045 — Agent Instruction Consolidation and the Process Domain

- Status: **accepted** (owner direction 2026-07-25)
- Tier: 2
- Date: 2026-07-25
- Analysis: `docs/adr/analyses/0045-agent-instruction-consolidation.md`

## Context

The agent instruction surface — `AGENTS.md`, `PROJECT_PLANNING.md`, the seat
files under `docs/roles/`, and the runner-specific definitions under
`.claude/` — grew by accretion. Each new process decision was recorded in the
document nearest to hand, and the same rule now appears in three to five
places in three to five wordings:

- The spawn / dispatch / owner-launch definition appears in `AGENTS.md`
  ("Prototype-process dispatch"), `docs/roles/foreman.md` ("Dispatch"), and
  `PROJECT_PLANNING.md` ("Spawn, dispatch, and owner launch").
- The CI verification floor appears in `AGENTS.md` ("Test economy"),
  `foreman.md`, `builder.md`, `reviewer.md`, and `.claude/agents/builder.md`.
- The Context Capsule contract appears in `PROJECT_PLANNING.md` and is
  re-described in all four seat files.
- The orientation-tool invocation appears in six places with three different
  `--ref` arguments and two different interpreter paths.

Duplication is not merely verbose. When an agent encounters two near-identical
statements of one rule it cannot determine which is operative, so it spends
reasoning on reconciliation — a task with no correct answer — or reads both
sources and inflates its context. Observed symptoms: unreliable seat
comprehension, agents re-deriving state the tooling already publishes, and
context bloat that persisted after the owner's manual trimming.

Two instructions were additionally unevaluable rather than merely duplicated.
"Read these before substantial work" gave no test for *substantial*, and named
`docs/phase-state.md` for all seats while `builder.md` and `reviewer.md`
forbid orienting from phase state. "Given owner authorization in this foreman
thread" described a *category* of authorization without supplying a
*procedure* for recognizing one, so foremen inferred authorization from tone.

The clerk seat, meanwhile, has been superseded by tooling. `docs/roles/clerk.md`
already records (2026-07-25 economy amendment) that a clerk spawn is the most
expensive way to do mechanical work and that the default is a tool. Its one
recurring task — answering "what is the current prompt?" — is served directly
by the `foreman-context-v1` block in `docs/foreman-handoff.md`, which
`tools/foreman_context.py` and `tools/build_orientation_block.py` read.
Maintaining `docs/foreman-clerk-task.md` remained mandatory continuity work for
a role that should no longer be dispatched.

Underneath all of this sits a structural cause. Process was recorded as ADRs —
seven of them by 2026-07-25 (0005, 0013, 0030, 0039, 0040, 0042, 0043), several
with three or four amendments each. That gave workflow the same standing as a
ratified product contract, with three costs the owner named directly:

- **Every process adjustment became a ratification event.** Retiring a seat or
  moving a rule required drafting, evidence, and a supersession chain, so the
  instruction surface lagged the way the owner actually wanted to work.
- **Agents argued from process ADRs against owner direction.** An accepted ADR
  binds regardless of routing (ADR-0039 decision 2), so a seat could and did
  cite a stale process clause back at the owner as though it were a contract.
- **The ADRs drifted from their operative documents.** ADR-0030 is the clearest
  case: it replaced milestone-granularity merging with per-track and per-ADR
  units, but `PROJECT_PLANNING.md`'s "Milestone Execution Branch Protocol" was
  never updated and still described the model ADR-0030 abolished. Two normative
  statements of the merge unit disagreed, and only the one nobody read was
  current.

Product and contract decisions genuinely need the ADR apparatus: they are
long-lived, they bind artifacts already written against them, and their cost of
reversal is high. Process does not have that shape. It is the owner's own
working method, it changes as the owner learns, and its cost of reversal is one
edit.

## Decision

**1. `AGENTS.md` is a router, not a rulebook — and every rule has exactly one
normative home.**

`AGENTS.md` carries only what binds every seat regardless of role: seat
routing, the milestone loop, dispatch authorization, the shared invariants, and
a map of where authority lives and when it is read. Where a rule's normative
home is another document, `AGENTS.md` links to it and does not restate it.

The single-source rule is general and applies to every process document: a
normative statement lives in one file. Other files reference it by name. A
restatement — even an accurate one — is a defect to remove, not a convenience
to keep, because it cannot be kept in sync and it forces reconciliation.

**2. Dispatch authorization is a literal string test.**

The foreman may dispatch a sub-agent only when a message from the owner in the
foreman's live thread **literally contains the string `I authorize dispatch`**.
No paraphrase, no implication, and no approving tone authorizes a dispatch.
Absent that string, the foreman prepares the charter, states that the role is
prepared but not launchable, and stops.

The authorization is single-use and bound to the role and charter current when
it was granted. It does not carry to a later role, a re-dispatch after a
charter revision, or a subsequent thread. Authorization remains ephemeral
thread context and is never repository state.

This supersedes the descriptive formulations in ADR-0034 and ADR-0043 with an
evaluable one; the substance is unchanged, only its testability.

**3. The clerk seat is retired.**

`docs/roles/clerk.md` and `docs/foreman-clerk-task.md` are deleted. There is no
clerk seat, no Clerk Task Capsule, and no obligation to maintain a
current-prompt record separate from the handoff's `foreman-context-v1` block.
Mechanical work is done by the foreman inline, or by a tool when it recurs or
its output is bulky. The clerk provisions of ADR-0034 and ADR-0042 are inert as
to the seat; those ADRs are not edited, per the in-place amendment prohibition.

**4. Governance reading belongs to the advisor, not to executing seats.**

The foreman, builder, and reviewer have **no boot-time or "significant work"
obligation to read `docs/governance/`**. That instruction is removed, not
relocated to a narrower trigger.

Governance is upheld by two mechanisms instead:

- **Mechanically, continuously** — `tools/governance_lint.py` and
  `tools/envelope_scan.py` run in the CI `verify` check on every PR and block
  merge on red. Structural conformance is a gate, not a reading assignment.
- **By judgment, at owner-called points** — the trusted advisor
  (`docs/roles/advisor.md`, ADR-0040) is the standing governance overseer. This
  **amends ADR-0040 decision 2** to add the governance set to the advisor's
  seed, and adds governance conformance to its remit at the existing invocation
  points: milestone selection, plan approval, Tier 3 ratification, retrospective
  review, and phase boundaries.

Because doctrine is no longer resident in executing seats, a seat that believes
its unit turns on governance text **stops and escalates to the owner**, who may
call an advisor consultation. This is a stop condition, which an agent can
evaluate, replacing a read obligation, which it could not.

`docs/governance/` remains the sole contract authority and still requires a new
version and owner ratification to change (Constitution; ADR-0001). Nothing here
weakens the governance set's standing; it changes only who reads it and when.

**5. Process is the owner's operational domain, not ADR territory.**

How work is organized — seats and their responsibilities, the milestone loop,
dispatch, chartering, review cadence, branch and merge mechanics, context
routing, capability tiers, prototype gates — is **operational method**. It is
changed by owner direction and an edit to the document that norms it. It
requires no ADR, no ratification, no prototype evidence, and no supersession
chain.

ADRs are reserved for **product and contract decisions**: the governance set,
the kernel and act log, schemas and citizen shapes, the rule language,
composition and closure semantics, data-residency and trust boundaries — the
things later artifacts are written against and cannot cheaply be rewritten.

Three consequences of this line:

- **No agent may cite a process ADR against owner direction.** Where owner
  direction and a process document disagree, the direction governs and the
  document is updated to match. An agent that believes a change is unwise says
  so once, plainly, and then complies.
- **A change to a seat, a workflow, or a cadence is a documentation edit**, made
  in the same PR as the work that motivated it.
- **The single-source rule of decision 1 is what keeps this safe.** Removing the
  ADR layer is only sound because each process rule has exactly one operative
  home; the ADRs were a second copy, and a second copy that could not be edited.

**6. The seven process ADRs are retired.**

**ADR-0005, ADR-0013, ADR-0030, ADR-0039, ADR-0040, ADR-0042, and ADR-0043** are
marked **`retired`** — a status meaning: retained permanently as history,
citable as the record of why a practice exists, and **not loaded as authority**.
`retired` joins `rejected` / `superseded` / `proposed` as an inert status. It
differs from `superseded` in that no successor ADR carries the contract forward;
the content moved to an operative document instead.

Their decision text is not edited — only the status line and a pointer, per the
in-place amendment prohibition. Each one's still-operative content has a live
home, and where the live home had drifted it is corrected in the enacting
change:

| Retired | Operative home now |
| --- | --- |
| 0005 — prototype evidence | `PROJECT_PLANNING.md`, "Prototype-Driven Decisions" |
| 0013 — economic gates, tiers, foreman stewardship | `PROJECT_PLANNING.md`, "Prototype Economic Gates" |
| 0030 — branch, PR, and merge strategy | `PROJECT_PLANNING.md`, "Branch, PR, and Merge Protocol" — **rewritten here**, replacing the stale milestone-granularity protocol |
| 0039 — advisory index and routing | `docs/adr/INDEX.md`, its own header |
| 0040 — trusted advisor seat | `docs/roles/advisor.md` |
| 0042 — context capsules | `PROJECT_PLANNING.md`, "Foreman context routing" and "Builder and reviewer context capsules" |
| 0043 — dispatch instruction | `AGENTS.md`, "Dispatch authorization" (decision 2 above) |

**ADR-0045 is the last process ADR.** It records the boundary; it does not
norm the process it releases. A future process change edits `AGENTS.md`,
`PROJECT_PLANNING.md`, or a seat file and needs nothing from this record.

## Consequences

**Enables.** A seat boots by reading one short router plus its own seat file.
Reconciliation work disappears because the second copy does. The dispatch rule
becomes mechanically checkable by the foreman and auditable by the owner after
the fact. Retiring the clerk removes a mandatory continuity chore and one
routinely-stale file.

**Forecloses.** No process document may restate a rule normed elsewhere.
Adding a rule now requires choosing its single home. Mechanical work may no
longer be delegated to a spawned mechanical seat; it is inline foreman work or
a tool.

**Requires.** `PROJECT_PLANNING.md` remains the normative home for planning,
capsule contracts, and prototype gates; the seat files remain the normative
home for per-seat posture; `docs/adr/INDEX.md` remains the ADR routing surface.
Each must be edited to delete what it duplicates rather than to add a
cross-reference alongside a retained copy.

**Accepted risk — decisions 5 and 6.** Process rules lose the durability an
accepted ADR gave them: an operative document can be edited without evidence,
without a committee, and without leaving a supersession trail beyond Git
history. Three things bound that. The change is visible in a PR diff rather
than buried in an amendment. Git history preserves what a rule said and when it
changed, which is what a supersession chain actually provided. And the retired
ADRs remain readable as the rationale record, so an agent that wants to know
*why* a practice exists still has the argument — it simply may not cite it as
authority. The judgment being accepted is that process changing too slowly has
been the observed failure, and process changing too casually has not.

**Accepted risk.** Decision 4 trades execution-time doctrine awareness for
CI enforcement plus advisor review. A builder can now author a contract-shaped
change with no governance text in view; `governance_lint.py` checks structural
integrity of the governance set, not the conformance of new artifacts to it.
The mitigations are the foreman's charter scope, the escalation stop condition
above, and the advisor's plan-approval review. If a governance violation
reaches `main` under this regime, the correct response is to reconsider this
decision, not to reintroduce a vague read obligation.

## Links

- Retires **ADR-0005**, **ADR-0013**, **ADR-0030**, **ADR-0039**, **ADR-0040**,
  **ADR-0042**, **ADR-0043** (decision 6); each keeps its text and gains a
  status line plus a pointer here.
- Renders the clerk provisions of **ADR-0034** (already superseded) and
  **ADR-0042** inert as to the seat; neither is edited.
- Operative documents this record enacts: `AGENTS.md`, `PROJECT_PLANNING.md`,
  `docs/roles/`, `docs/adr/INDEX.md`.
- Unaffected: every product and contract ADR. Decision 5 draws a line around
  process only.
