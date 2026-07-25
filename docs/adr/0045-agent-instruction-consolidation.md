# ADR 0045 — Agent Instruction Consolidation

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

**Accepted risk.** Decision 4 trades execution-time doctrine awareness for
CI enforcement plus advisor review. A builder can now author a contract-shaped
change with no governance text in view; `governance_lint.py` checks structural
integrity of the governance set, not the conformance of new artifacts to it.
The mitigations are the foreman's charter scope, the escalation stop condition
above, and the advisor's plan-approval review. If a governance violation
reaches `main` under this regime, the correct response is to reconsider this
decision, not to reintroduce a vague read obligation.

## Links

- Supersedes the descriptive dispatch-authorization language in **ADR-0034**
  (already superseded by 0043) and **ADR-0043**.
- Amends **ADR-0040** decision 2 (advisor seed) and its remit.
- Renders the clerk provisions of **ADR-0034** and **ADR-0042** inert as to the
  seat; those ADRs remain unedited.
- Operative documents: `AGENTS.md`, `PROJECT_PLANNING.md`, `docs/roles/`.
- Related: **ADR-0005**, **ADR-0013** (prototype gates and foreman stewardship),
  **ADR-0030** (PR rule), **ADR-0039** (ADR index routing).
