# ADR 0051 — The Entry Surface Contract

- Status: **accepted 2026-07-29**, ratified by the owner on the Entry Loop
  (synthetic) milestone close (PR #112). Supersedes ADR-0048's entry-vehicle
  requirements (Decision 1 and the spellcheck condition). ADR-0048's
  contribution boundary (Decision 2) is untouched and remains in force. Held
  across two full usability-evaluation rounds and repeated adversarial
  testing of the entry loop this milestone built.
- Tier: 3
- Date: 2026-07-29
- Supersedes: ADR-0048, Decision 1 only

## Context — a sentence that created the wrong obligation

ADR-0048 answered two questions. The second one — an entry surface emits
`act-contribution.v1` through the existing admission path and never writes a
fact — is the load-bearing one, and it is not in question here.

The first one asked whether a browser form is an acceptable place to type a
real tax fact. It answered yes, conditioned on the surface reusing or equaling
`live_viewing.py`'s confinement and disposal, and on the browser launching with
spellcheck's network path affirmatively closed by a vehicle-level flag or
policy.

That condition turned browser configuration into a product acceptance
condition. Once it is written down, a reviewer is right to ask: where is the
entry vehicle, which flag closes spellcheck, is it tested, what happens on a
crash, what about a hostile local process, how do we know Chrome wrote nothing
unexpected? The first build to touch entry —
`docs/reviews/2026-07-29-entry-loop-synthetic-track1-review.md` — hit exactly
that and blocked on it, correctly, under the rule it was asked to enforce.

The problem is not that the build failed to meet the condition. It is that we
do not want the condition. Browser and workstation behaviour are not things
this product controls, and a promise it cannot keep is worse than no promise.

## Decision — the entry surface is responsible for its own behaviour, not the machine's

An entry surface is responsible for:

- **contribution-only entry** — it emits `act-contribution.v1` through the
  existing admission path and writes no fact or finding itself (ADR-0048
  Decision 2, ADR-0032);
- **validated admission** — input is validated and refused at the boundary
  before anything reaches the act log, and refusal is closed, not partial;
- **redacted failure** — a rejected value is never echoed back, in a response,
  a log line, or a diagnostic (ADR-0046);
- **data-boundary behaviour** — no residency locator in any surface it
  produces, and synthetic data stays synthetic;
- **no false claim of isolation** — it does not present a browser or operating
  system setting as a protection it does not provide.

Browser and workstation behaviour are outside the entry surface's contract.
The product makes no claim to isolate typed data from the owner's browser,
operating system, extensions, or local processes. That is the owner's trusted
environment, which is where ADR-0047 already puts Class C confinement and Class
D workstation preconditions.

**For real entry, the trusted environment is standing operational context, not
a per-session check.** There is no entry-session affirmation, no spellcheck
probe, and no preflight owed by this contract.

## What this does not change

- **ADR-0048 Decision 2.** The contribution boundary, the evidence-linkage
  requirement, and supersession-only correction all stand exactly as written.
- **ADR-0046.** Redaction, accessibility, zero-authority foreclosure, and
  section-level blocked-state salience apply to entry surfaces unchanged.
- **ADR-0047.** The viewing vehicle keeps its confinement and disposal
  properties and its open obligations — the orphan sweep and the
  single-instance-lock artifact belong to whichever milestone next touches
  `packages/derivation/live_viewing.py`. They were never entry's to discharge.
- **ADR-0044's longer-term isolation goal for L4.** Untouched. Narrowing what
  the product claims today does not retire what a hardened maturity level would
  eventually require.
- **The current milestone's work.** Track 0's usability instrument, the four
  Phase A dependency tests, the W-2 loop, the Svelte page, the loopback server,
  the contribution template, the applicator path, the surface-artifact route,
  and Track 2's evaluation procedure are all unaffected.

## Consequences

- ADR-0048's vehicle-level spellcheck requirement is withdrawn. No milestone
  owes an affirmative spellcheck flag, a confined entry vehicle, or a proof
  that typed text stayed off the network.
- Track 1's blocking F1 is obsolete. The review was correct under the rule then
  in force; it is not rewritten. A short recheck records that the governing
  premise changed and confirms whether anything else blocks.
- A `spellcheck="false"` attribute may stay as a reasonable UI setting. It must
  not be named, commented, or documented as a security control.
- A future entry surface that does want machine-level isolation has to argue
  for it on its own terms. It does not inherit one here.
- No maturity cell moves. This is a contract change, not an implementation.

## Left undecided

- Whether real entry (L3) eventually wants an operating-environment check of
  any kind. This ADR says it is not a condition of the entry surface contract;
  it does not say the question can never be reopened by a milestone that has a
  reason.
- What ADR-0044's L4 isolation goal actually requires in practice. Unchanged
  and still unspecified.

## Alternatives considered

- **Amend ADR-0048 in place.** Rejected. ADR-0048's Decision 1 was a real
  decision, reasoned at length, and ratified. Editing it would make the record
  say the project never held that view. A superseding ADR keeps both the old
  position and the reason it changed.
- **Build the entry vehicle the condition asks for.** Rejected. It is
  unbounded — browser flags, crash paths, hostile local software — and none of
  it is the product's responsibility. The condition, not the gap, is the defect.
- **Say nothing and let reviewers waive it case by case.** Rejected. The
  obligation is written down, so every future build inherits it and every
  future reviewer is right to raise it. Waiving a rule repeatedly is how a
  record stops meaning anything.
- **Replace it with "security is handled elsewhere."** Rejected as too vague —
  it invites the next reviewer to ask where and how. The replacement states
  what the surface is responsible for and declines the rest by name.

## Links

- Superseded: `docs/adr/0048-entry-boundary.md` (Decision 1)
- Contribution boundary: `docs/adr/0032-contribution-boundary.md`
- Presentation contract: `docs/adr/0046-presentation-surface-contract.md`
- Viewing environment and trust classes: `docs/adr/0047-live-viewing-environment.md`
- Trust domains: `docs/adr/0044-live-run-system-boundary-and-trust-domains.md`
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- The review this disposes: `docs/reviews/2026-07-29-entry-loop-synthetic-track1-review.md`
