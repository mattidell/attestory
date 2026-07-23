# Plain-Language Analysis — Foreman Context Capsule

Companion to [ADR-0042](../0042-foreman-context-capsule.md). The ADR is the
normative record.

## What changes

Foremen will start from a short, generated briefing instead of repeatedly
opening every long process document before they know what work is active. The
briefing identifies one exact committed repository revision, the active seat
and topic, the hard stops, the next permitted action, and the documents that
must be read before a particular action.

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

## What it enables

A resumed foreman can quickly see the safe next move and load only the
authorities needed for that move. This reduces repeated context cost while
making stale or mixed repository state more obvious.

## What it does not do

It does not replace governance, accepted ADRs, charters, reviews, or owner
approval. It does not inspect a real workspace, credential, remote, personal
output, or any other private material. It also does not make the live-run
trust-domain prototype start; that topic still needs its own owner-approved
charter and dispatches.
