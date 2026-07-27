<!-- foreman-context-v1
{
  "version": 1,
  "topic": "data-boundary-hardening-bar",
  "milestone_state": "planning",
  "retrospective": null,
  "status": "Planning, 2026-07-27. Owner selected this after the Presentation Live Viewing Boundary close-out, choosing to redefine what L4 means for the data-boundary row rather than pursue an enforcement substrate. Scope is the data-boundary row only; the vehicle is an in-place amendment to ADR-0044. No maturity lift and no implementation: this milestone sets a bar, it does not clear one.",
  "scope": [
    "establish that maturity-matrix footnote 8 sets an unratified bar and that a planning instrument may not acquire requirements by observation",
    "name the threat mechanical authority separation would actually address, and show why owner attestation is the wrong instrument for it",
    "amend ADR-0044's future implementation gate to name production conditions for the data-boundary row that are dischargeable by audit and constraint of live-run code rather than by process confinement",
    "state for each named condition what evidence discharges it and what its current disposition is",
    "rewrite maturity-matrix footnote 8 to cite the ratified bar, and record honestly that the row remains L3 with every condition undischarged"
  ],
  "non_goals": [
    "no data-boundary L4 claim and no maturity lift of any cell",
    "no discharge of any named condition — naming a condition and meeting it are separate milestones, deliberately",
    "no selection, prototype, or evaluation of an enforcement substrate (sandbox-exec/Seatbelt, container, separate OS identity, VM)",
    "no change to ADR-0044's four trust domains, the intended live supply crossing, or the owner-authorized elevation residual",
    "no change to ADR-0031's residency rules or ADR-0047's channel classification, including Class C's text",
    "no audit of maturity-matrix footnotes other than footnote 8",
    "no implementation, no test, no tooling change, no new tax rule, form field, citation, schedule, domain, published schema, or citizen",
    "no residency locator, path fragment, or derived identifier in the repository, a review, a PR, chat, or the retrospective"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/real-return/milestones/data-boundary-hardening-bar.md",
      "docs/adr/0044-live-run-system-boundary-and-trust-domains.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0047-live-viewing-environment.md",
      "docs/phases/real-return/maturity-matrix.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/real-return/milestones/data-boundary-hardening-bar.md",
      "docs/adr/0044-live-run-system-boundary-and-trust-domains.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0047-live-viewing-environment.md",
      "docs/phases/real-return/maturity-matrix.md",
      "docs/phase-state.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "dispatch": [
      "docs/roles/foreman.md#Dispatch",
      "AGENTS.md#Dispatch authorization"
    ],
    "merge_or_records": [
      "docs/roles/foreman.md#Standing disciplines",
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ],
    "new_milestone": [
      "docs/phases/real-return/maturity-matrix.md",
      "docs/phases/real-return/milestones/data-boundary-hardening-bar.md"
    ]
  }
}
-->
# Milestone: Data Boundary — Hardening Bar

Status: **Planning, 2026-07-27.** Not yet chartered.

## Objective

Replace the unratified mechanical-separation requirement on the data-boundary
row with named production conditions that can actually be discharged, ratified
as an amendment to ADR-0044.

**This milestone raises nothing.** It ends with the row still at L3 and every
named condition undischarged. Its product is a bar the project can aim at
instead of one it cannot reach.

## Current state and the correction this plan encodes

Maturity-matrix footnote 8 currently reads, in part:

> ADR-0044 defines the intended Developer/Supply, Publication, Live-Run Data,
> and Owner Authorization domains but implements no mechanical authority
> separation; **that missing enforcement is what holds this row short of L4.**

The first clause is an accurate observation. The second is a requirement — and
it was never argued as one. ADR-0044 routes enforcement-substrate selection to a
"future implementation gate" without deciding that a substrate is the *only*
route to L4; the footnote quietly converted a deferral into a definition.

The result is a cell that reads as an unfinished task but is really an
unexamined assumption. It has not moved while its neighbours have. A planning
instrument that acquires requirements by observation rather than ratification
distorts every selection made from it, which is the specific harm this milestone
exists to stop.

### What the level definition actually requires

> **L4** — Hardened: named production conditions discharged; deferrals retired.

Nothing in that says "mechanically enforced." The Correction & supersession
lifecycle row is already L4 across every domain, and it got there by making a
named condition — unrestricted supersession — expressible and enforced at an
existing dispatch site. Named, then discharged. That is the pattern.

### What mechanical separation would actually be for

This is the load-bearing derivation and Track 1 must make it explicitly, not
assume it.

Mechanical authority separation does not defend against the owner. ADR-0031's
non-descriptive attestation already covers what the owner does, and the owner
has accepted that responsibility. Separation defends against **a
Developer/Supply-domain process reaching Live-Run Data unintentionally** — code
that logs a path it should not, writes a diagnostic to the wrong place, or reads
beyond its charter.

That threat is live here in a way it is not in most projects: this repository is
authored by agents, runs on the owner's machine, and holds a runtime capability
pointing at real tax documents. The posture remains accidental leakage, not
malice.

The owner's attestation is the wrong instrument for it — not insufficient,
**wrong in kind**. The owner can attest to what they did. They cannot attest to
what an unexercised code path did, because they did not write it. That gap is
what footnote 8 is gesturing at, and it is dischargeable by auditing and
constraining live-run code, which is a different thing from confining a process.

### The shape the new conditions should take

Track 1 derives these; this plan names the shape so the track is reviewable, and
deliberately does not fix the list.

Conditions should be **properties of the live-run code path** — what it may
reach, what it may emit, and what independent inspection has confirmed — rather
than properties of the operating system's process model. Candidate shapes:
declared filesystem reach that is mechanically checkable; absence of any egress
surface in live-run code; locator confinement proven across every live-run path
rather than only the viewing vehicle; and independent context-starved audit
coverage of those paths.

An enforcement substrate, if one is ever evaluated and holds, then becomes *one
way to discharge one condition* — not the definition of the level.

## The failure this plan is most exposed to

**A bar the current state already meets is not a bar.** The tempting outcome is
a set of conditions that read well and happen to describe what the repository
does today, which would move the row to L4 on the strength of a document. That
is the exact failure this project has repeatedly caught in other forms.

Track 1 must therefore state, for each named condition, its **current
disposition**, and at least one condition must be currently **undischarged**. If
Track 1's honest derivation finds that every condition it can name is already
met, the correct action is to stop and report that — the conclusion would then
be that the row deserves L4 today, which is an owner decision and not this
milestone's to take.

The Track 1 review gate measures this directly.

## Milestone stages

1. **Track 1 — decision.** Amend ADR-0044; one independent decision review.
2. **Track 2 — records.** Rewrite footnote 8, update the matrix and roadmap,
   file the retrospective, close phase state; one independent completion review.

No prototype. This is a direct system-definition amendment, matching how
ADR-0044 and ADR-0047 were made: owner-accepted decision records, no prototype,
no committee. The economic gates in `PROJECT_PLANNING.md` are satisfied by that
precedent rather than bypassed.

## Scope

- Establish the unratified-bar finding and the principle behind it.
- Derive what mechanical separation is for, and why attestation cannot cover it.
- Amend ADR-0044's future implementation gate with named conditions, each with
  its discharging evidence and current disposition.
- Rewrite footnote 8 to cite the ratified bar.
- Record that the row stays L3.

## Non-goals

As the capsule's `non_goals`. The two worth restating in prose:

- **No condition is discharged in this milestone.** Naming and meeting are
  separate, deliberately, so that the bar is set without the pressure of
  simultaneously clearing it.
- **No substrate work of any kind**, including a Seatbelt prototype. If the
  amendment makes a substrate look attractive, that is a future owner selection.

## Verification

```text
python3 tools/envelope_scan.py --range main..HEAD
git diff --check
```

Every commit SHA cited in a record must resolve.

There is no test obligation: this milestone changes no code. A track that finds
itself wanting to write one has left its boundary and should stop and report.

## Data safety

Derived from accepted records only. No real workspace, locator, or machine
configuration is consulted.

## Exit criteria

1. ADR-0044 carries an accepted amendment naming the data-boundary row's L4
   conditions, each with discharging evidence and current disposition, and at
   least one currently undischarged.
2. The amendment states why mechanical separation is not the only route, without
   claiming a substrate is impossible or unnecessary — Seatbelt remains an
   unevaluated candidate and the amendment must not resolve that either way.
3. Footnote 8 cites the ratified bar and no longer sets one of its own.
4. The data-boundary row is L3 in every domain, unchanged.
5. Both review gates returned `READY`, and the retrospective is filed.

## Review gates

**Track 1 (decision).** Measurements: the unratified-bar finding is derived from
the cited text rather than asserted; the threat derivation shows why attestation
is the wrong instrument rather than merely an incomplete one; every named
condition has stated discharging evidence and a stated current disposition; at
least one is undischarged; no condition is stated so vaguely that its discharge
would be a matter of opinion; the amendment forecloses nothing about Seatbelt in
either direction; and no maturity claim is made anywhere.

**Track 2 (records).** Measurements: footnote 8 sets no bar of its own; the row
is unchanged at L3 across all five domains; every cited SHA resolves; the
retrospective records the finding in a form a future reader can apply to another
footnote; and no other cell moved.

## Tracks

### Track 1 — Amend ADR-0044's hardening gate

**Goal:** ratify a dischargeable definition of L4 for the data-boundary row.

**Boundary:** decision record only. No code, no prototype, no substrate
evaluation, no maturity lift, no change to the four domains.

**Inputs:** ADR-0044 (especially the future implementation gate), maturity-matrix
levels and footnote 8, footnote 7's evidential basis for every L3, ADR-0031
Decision 7's attestation shape, ADR-0047's Class C residual and its Class A
owner-authorized elevations, and the Correction & supersession row as the
project's one worked example of reaching L4.

**Outputs:** the ADR-0044 amendment, an updated ADR index entry, and one
independent decision review.

**Migration risk:** none; the amendment changes no behavior.

### Track 2 — Records and handoff

**Goal:** record the new bar and the unchanged level, exactly.

**Boundary:** records only. No implementation, no repair, no next-milestone
selection.

**Outputs:** footnote 8 rewritten, matrix and roadmap updated, retrospective,
phase-state close-out, and one independent completion review.

**Migration risk:** documentation only.

## Execution economy

| Unit | Role | Effort | Boundary |
| --- | --- | --- | --- |
| Track 1 decision | Foreman or Builder | one focused pass | ADR amendment only |
| Track 1 review | Reviewer | one focused pass | seven measurements above |
| Track 2 records | Builder | one focused pass | records only |
| Track 2 review | Reviewer | one focused pass | five measurements above |

Repair cap: one findings-only repair per review, per the standing convention.

## Execution record

| # | Unit | Role | Authority | Result |
| --- | --- | --- | --- | --- |
| 0 | Milestone selection | Owner | Owner direction, 2026-07-27 | After a briefing on both live frontiers, the owner rejected pursuing an enforcement substrate and selected redefining the bar. Scope: data-boundary row only. Vehicle: in-place ADR-0044 amendment |
