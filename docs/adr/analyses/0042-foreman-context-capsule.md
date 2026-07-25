# Plain-Language Analysis — Foreman Context Capsule

Companion to [ADR-0042](../0042-foreman-context-capsule.md). The ADR is the
normative record.

## What changes

Foremen will start from a short, generated briefing instead of repeatedly
opening every long process document before they know what work is active. The
briefing identifies one exact committed repository revision, the active seat
and topic, the hard stops, the current role/prompt, and the documents that must
be read before a particular action.

Builders and reviewers will receive the same economy in a different form: a
short Context Capsule inside the charter they already must read. Clerks will
receive a similarly bounded Clerk Task Capsule for one mechanical job. Neither
uses the Python renderer, and the trusted advisor's strategic counsel remains
unchanged.

## Why it is needed

The project has accumulated valuable process history, but the same current
rules appear in many places. That makes re-entry slow and can hide the useful
signal: whether the current branch, phase pointer, handoff, plan, and seat all
describe the same thing.

## What it protects

The briefing is deliberately not a summary that can make a decision on its own.
It is tied to committed source blobs, refuses conflicting metadata, reports a
dirty checkout separately, and points back to the actual rule before work
begins. It cannot approve a dispatch, weaken the real-data boundary, or make a
new milestone plan without the required retrospective reading.

Builder/reviewer capsules cannot widen the charter, and clerk task capsules
cannot turn a clerk into a planner. Each carries only the context the role needs
to perform the current task and a stop rule for anything missing or ambiguous.

## What it enables

A resumed foreman can quickly see the current role and load only the
authorities needed for that role. This reduces repeated context cost while
making stale or mixed repository state more obvious.

Builders and reviewers can orient to one review/build object without loading
the phase-wide handoff. Clerks can perform a mechanical request without trying
to rediscover which dispatch the foreman meant.

## What it does not do

It does not replace governance, accepted ADRs, charters, reviews, or owner
approval. It does not inspect a real workspace, credential, remote, personal
output, or any other private material. It also does not make the live-run
trust-domain prototype start; that topic still needs its own owner-approved
charter and dispatches. It does not redesign trusted-advisor context.
