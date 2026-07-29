<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "entry-loop-synthetic",
  "status": "Planned 2026-07-28, milestone 3 of Legible Entry. The first milestone in this phase that builds product. Scope settled by the owner: W-2 only, all five loop steps, synthetic workspace, no real data and no L3 claim. Usability criteria are written before the surface is built (Track 0) so the L2 claim has a scorer that was not shaped by the thing it scores. The per-field explanation schema is left to emerge from the build and is written down at close, not designed up front. Four tracks, each one build-and-review cycle. Milestone opens on one PR and closes on another; tracks keep their review gate and land on the milestone branch. Prerequisite to confirm before Track 1 writes code: that a synthetic workspace can be seeded so W-2 facts are the only thing missing, and that the surface can be served and can emit act-contribution.v1 through the existing admission path. Check it against the code, do not assume it. Amended 2026-07-29: the owner withdrew ADR-0048's entry-vehicle condition and ADR-0051 replaced it. Browser and workstation behaviour are the owner's trusted environment, not the entry surface's contract; the surface owes contribution-only entry, validated admission that fails closed, redacted failure, data-boundary behaviour, and no false claim of isolation. Open question 3 (does the viewing preflight cover an entry session) is closed, and Track 1's blocking review finding is disposed by recheck rather than by building a vehicle.",
  "scope": [
    "write the usability evaluation criteria for entry, and how a cell is scored against them, before any surface exists",
    "build the guided entry loop for W-2 on a synthetic workspace: know what is missing, enter a fact, see it land, correct an entered fact, know the return is complete",
    "drive entry through act-contribution.v1 on the existing admission path, per ADR-0048",
    "ship the surface through the surface artifact and build it at the workspace, per ADR-0049",
    "run the usability evaluation against the built loop and record the result",
    "record the per-field explanation shape that the build actually needed",
    "move the W-2 column of the entry-loop matrix to L2 only if the evaluation passes"
  ],
  "non_goals": [
    "no real data, no real workspace, no owner attestation, no L3 claim",
    "no 1099-INT, 1099-DIV, or taxpayer-assertion entry",
    "no filing",
    "no new tax rule and no change to any derivation package",
    "no change to artifact-package.v4",
    "no new correction-authority mechanism -- every fact type stays free",
    "no separate missing-facts screen",
    "no entry vehicle, no browser launch flag, no spellcheck control, no entry-session preflight or affirmation -- per ADR-0051"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/legible-entry/milestones/entry-loop-synthetic.md",
      "docs/phases/legible-entry/legible-entry-roadmap.md",
      "docs/adr/0048-entry-boundary.md",
      "docs/adr/0051-entry-surface-contract.md",
      "docs/adr/0049-surface-artifact.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "AGENTS.md#Data Safety Rules",
      "AGENTS.md#Fixture Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/legible-entry/milestones/entry-loop-synthetic.md",
      "docs/adr/0048-entry-boundary.md",
      "docs/adr/0051-entry-surface-contract.md",
      "docs/adr/0049-surface-artifact.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "merge_or_records": [
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ]
  }
}
-->
# Milestone: The Entry Loop (synthetic)

Status: **open.** Plan merged 2026-07-28 (PR #109, `506f785`). Track 0 closed;
Track 1 built and reviewed `NOT READY`. Its blocking finding rested on
ADR-0048's entry-vehicle condition, which the owner withdrew on 2026-07-29
(ADR-0051). Track 1 is in a scoped repair covering the two coverage findings,
plus a recheck that disposes the blocking one.

## What this is for

The owner still gets tax data into this system by editing JSON by hand, and
still finds out what is missing by reading a machine's account of it. Two
milestones have cleared the way: one decided a browser form is an acceptable
place to type a tax fact and that it must hand its work to the existing
contribution boundary rather than write anything itself, and one built the
route that gets UI code onto the machine at all.

Neither built any part of the thing a person uses. This one does.

The loop is the product here, not the form. A person opens the surface, sees
what the return is missing, types one of those facts, watches it land, fixes it
if they got it wrong, and keeps going until the return computes. The
missing-facts account is the guide through that loop, not a separate page to
reconcile against by hand — a form beside a diagnostic report is exactly the
legibility failure this phase exists to remove.

Everything here runs on synthetic data. No real return is touched and no
maturity row reaches L3 in this milestone.

## What the owner decided, 2026-07-28

**W-2 only, all five steps of the loop.** One fact family taken all the way
through rather than four families taken partway. W-2 is the simplest family and
the one with the most precedent in the system. Fifteen of the twenty matrix
cells are deliberately left for later milestones. The reasoning: a loop that
works end to end for one thing tells us whether the loop is right; a loop that
covers four families but stops before correction and completion tells us
nothing about whether a person can finish.

**The usability criteria are written before the surface is built.** A cell in
this phase reaches L2 when a usability evaluation passes, and that evaluation
does not exist yet. Writing it after the build means writing it in the shape of
whatever got built. It goes first, and the build aims at a bar someone else set.

**The per-field explanation schema is left to emerge.** The phase thesis wants
a representation of the explanation, context, and navigation each point of
entry carries. We will find that shape by building W-2 fields and seeing what
they need, and write it down at close. The last milestone's plan asserted a
shape nobody had tried and was wrong about it; the correction is to make the
claim after the attempt, not before.

## What is still open

**1. Can a synthetic workspace be arranged so W-2 is the only thing missing?**
The fifth step of the loop is "know the return is complete," and a return needs
more than a W-2. The intended answer is to seed the synthetic workspace with
every other fact already present, so the only gap the loop has to close is the
one being built. Confirm that against the code before writing any of the
surface. If it does not hold, the fifth step needs a different design and this
plan is wrong about it.

**2. What serves the page, and how does a contribution get from the browser to
the admission path?** ADR-0048 settled that the surface emits
`act-contribution.v1` rather than writing facts, and ADR-0049 settled how the
code arrives. The mechanism in between — what process is listening, what it
accepts, what it refuses — is not settled and is Track 1's to find out against
the existing code.

**3. ~~Does the viewing preflight cover an entry session?~~ Closed by
ADR-0051, 2026-07-29.** This asked what browser confinement an entry session
owes, because ADR-0048 made it a condition of entry being acceptable at all.
The owner withdrew that condition: browser and workstation behaviour are the
owner's trusted environment, not the entry surface's contract. The entry
surface owes contribution-only entry, validated admission that fails closed,
redacted failure, data-boundary behaviour, and no false claim of isolation.
Nothing here owes a preflight, a launch flag, or a spellcheck control.

**4. What does correction look like when nothing can refuse it?** Every fact
type shipped today declares `free`, so a correction on synthetic W-2 data is
always allowed. The interesting refusals of ADR-0041 cannot occur here. The
correction step is therefore about whether a person can find and change an
answered fact and understand what happened — not about refusal design. Do not
build refusal UI for a refusal that cannot fire.

## How we will answer them

### Track 0 — usability criteria for entry

Write the criteria a guided entry loop has to meet, and the procedure that
scores a cell against them. Concrete enough that two agents evaluating the same
surface would agree on most of it, and specific to entry rather than generic
usability advice — what a person must be able to tell about a field before
typing in it, what they must be able to tell after, and what "I know the return
is complete" has to look like to count.

It should also say who evaluates and how disagreement resolves. The phase's
stated method is a mix of agent viewpoints, with the owner reviewing the
criteria, the evidence, and the result. Where evaluators disagree, that
disagreement is signal, and the procedure should say what happens to it rather
than averaging it away.

The existing presentation contract (ADR-0046) is the nearest thing to prior
art: zero-authority foreclosure, blanket redaction, section-level salience.
Read it, but do not assume entry inherits it — it was written for a surface
that only displays.

This track writes no product code and scores nothing yet.

### Track 1 — build the loop for W-2

The guided loop, end to end, on a synthetic workspace:

- **know what is missing** — the surface shows the outstanding W-2 facts, as
  the guide through entry rather than a report beside it;
- **enter a fact** — fields that explain what they are asking for and why;
- **see it land** — the person can tell the fact was accepted, and what it
  changed;
- **correct an entered fact** — find an answered fact, change it, understand
  the result;
- **know the return is complete** — the loop ends somewhere definite, with a
  computed return.

Entry emits `act-contribution.v1` through the existing admission path. The
surface ships and builds by the route the last milestone established. Reuse
what exists; if something turns out not to be reusable, stop and report rather
than writing a parallel path.

Track 0's criteria are visible to this track. Building toward a known bar is
the point of writing it first.

### Track 2 — evaluate

Run Track 0's procedure against Track 1's surface and record the result,
including where evaluators disagreed. If the evaluation fails, that is a real
outcome and the milestone reports it rather than adjusting the criteria to fit.
A repair cycle is fine; rewriting the bar is not.

### Track 3 — write it down and close

Record the per-field explanation shape the build actually needed — what each
point of entry carries for explanation, context, and navigation — as a short
ADR. Then move the W-2 column of the entry-loop matrix to L2 if and only if
Track 2 passed, file the retrospective, and close.

## Not in this milestone

No real data, no real workspace, no attestation. No 1099-INT, 1099-DIV, or
taxpayer-assertion entry. No filing. No new tax rule, no change to any
derivation package, no change to `artifact-package.v4`. No new
correction-authority mechanism — every fact type stays `free`. No separate
missing-facts screen, by design.

## How we will know it is done

- A person can go from an incomplete synthetic return to a computed one by
  typing W-2 facts into the surface, without opening a text editor.
- Entry goes through `act-contribution.v1` on the existing admission path.
  Nothing in the surface writes a fact.
- An entered fact can be corrected through the surface.
- Track 0's criteria existed before Track 1's code, and Track 2 scored against
  them unchanged.
- The W-2 column moves to L2 only if that evaluation passed. If it did not, the
  column does not move and the milestone says why.
- The per-field explanation shape is written down as something observed, not
  proposed.
- The data-safety scan passes and no real workspace was involved.

## Shape of the work

Four tracks, sequential, each one build-and-review cycle. Track 0 sets the bar,
Track 1 builds, Track 2 scores, Track 3 records and closes. The milestone opens
on this PR and closes on another; tracks keep their review gate and land on the
milestone branch without their own PRs.

Plans and charters here are written for a reader who knows the product and not
the record.
