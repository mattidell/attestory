# Plain-Language Analysis — Agent Instruction Consolidation

Companion to [ADR-0045](../0045-agent-instruction-consolidation.md). The ADR is
the normative record.

## What changes

Four things.

`AGENTS.md` stops being a rulebook and becomes a router. An agent opening it
finds which seat it holds, how the milestone loop works, when a dispatch is
authorized, the handful of rules that bind everyone, and a map of where
everything else lives. It no longer restates the planning protocol, the ADR
format, the retrospective format, the schema-publication protocol, the commit
conventions, or the document layout — each of those already had a home
elsewhere, and now only lives there.

Dispatch authorization becomes a literal phrase. The foreman may spawn a
sub-agent only if the owner's message contains the exact words
`I authorize dispatch`. Nothing else counts — not "go ahead", not "sounds
good", not an obviously approving reply.

The clerk seat is removed. The work it did is either one foreman turn or a
tool, and the one recurring thing it answered — what the current prompt is —
already lives in a machine-readable block at the top of the handoff note.

Reading the governance set stops being an execution-time duty. The foreman,
builder, and reviewer no longer read `docs/governance/` as a matter of course.
Governance is checked by CI on every pull request and reviewed by the trusted
advisor at the decision points the owner already calls.

## Why it is needed

The instruction set had grown until the same rule appeared in three to five
documents, each phrased a little differently. That is worse than one long
document. Faced with two near-identical statements of one rule, an agent cannot
tell which is authoritative, so it either reads both — inflating its context —
or picks one and hopes. Neither produces reliable behaviour, and the effect
showed up as exactly the symptom the owner reported: agents that no longer
seemed to understand instructions that used to work.

Two rules were also written in a form no agent could act on. "Read these before
substantial work" never defined *substantial*. "Given owner authorization in
this foreman thread" described what authorization *is* without saying how to
recognize one, so foremen inferred it from the owner's tone — which is exactly
the failure the rule existed to prevent.

## What it enables or protects

A seat now boots from one short router plus its own seat file, so the context
it carries is smaller and the parts of it that conflict are gone. The dispatch
rule becomes something the foreman can check against the transcript and the
owner can audit afterwards, rather than a judgment call. Retiring the clerk
removes a standing chore and a file that went stale between refreshes.

Most durably, the single-source rule means the next process decision has to
pick a home rather than being appended wherever it is convenient. That is what
stops the problem recurring.

## What it does not do

It does not change the governance set's authority. `docs/governance/` remains
the sole contract authority and still requires a new version and the owner's
ratification to change. Only the question of *who reads it and when* moved.

It does not change the planning protocol, the branch and merge rules, the
prototype gates, the data boundary, or any seat's substantive posture. The
material `AGENTS.md` gave up was already written down elsewhere; deleting the
copy changed no rule.

It does not edit any accepted ADR in place. ADR-0034 and ADR-0042 still mention
the clerk; that text stands as history, and this record makes it inert as to
the seat.

## The risk worth naming

Removing governance from executing seats means a builder can write a
contract-shaped change with no doctrine in view. The CI lint checks that the
governance set is structurally sound — it does not check that a new artifact
conforms to it. The safeguards are the charter's scope, a stop-and-escalate
rule when a seat believes its work turns on governance text, and the advisor's
review before a plan is approved.

If a governance violation reaches `main` under this arrangement, the honest
response is to revisit this decision rather than to quietly reinstate a vague
instruction to "read the governance files."
