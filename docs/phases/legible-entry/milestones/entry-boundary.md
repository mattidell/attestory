<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "entry-boundary",
  "milestone_state": "track-2",
  "status": "Plan merged (PR #101). Track 1 built the retention probe (a33458a); its review (367de61) found the charter had named the headless harness, so the findings stood only for headless mode. Track 1b re-ran the same method against the headed vehicle `packages/derivation/live_viewing.py` on a synthetic workspace (513ff93): NO CHANNEL DIFFERED between headless and headed — all five observed not-fired, zero non-loopback egress in either. Two residuals remain open and are the crux for Track 2: the autofill save-confirmation prompt was never driven, and enhanced/cloud spellcheck is opt-in and was not enabled, in either vehicle. Owner directed 2026-07-28: rest ADR-0048 on confinement and profile disposal rather than on the probe negatives, and fold the Track 1b review into the ADR review rather than gating it separately. Track 2 chartered — `docs/reviews/charter-2026-07-28-entry-boundary-track2.md`. All tracks ride on `milestone/entry-boundary` and reach `main-ui` in one closing PR.",
  "scope": [
    "find out what a browser actually keeps when a person types into a form, by running a throwaway probe against a synthetic workspace",
    "decide whether a browser form is an acceptable place for a person to enter real tax facts",
    "decide whether an entry surface writes facts directly or emits contribution events through the existing boundary",
    "ratify the answer as an ADR, with the probe findings as its evidence"
  ],
  "non_goals": [
    "no entry surface, form, or product UI of any kind",
    "no packaging decision — that is the next milestone",
    "no real data, no real workspace, no owner attestation, no maturity claim",
    "no change to the correction-authority policy",
    "no new tax rule, schema, or published citizen"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/legible-entry/milestones/entry-boundary.md",
      "docs/phases/legible-entry/legible-entry-roadmap.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0032-contribution-boundary.md",
      "docs/adr/0044-live-run-system-boundary-and-trust-domains.md",
      "docs/adr/0047-live-viewing-environment.md",
      "tools/presentation_harness/lib/chrome.mjs",
      "AGENTS.md#Data Safety Rules",
      "AGENTS.md#Fixture Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/legible-entry/milestones/entry-boundary.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0032-contribution-boundary.md",
      "docs/adr/0047-live-viewing-environment.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "merge_or_records": [
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ]
  }
}
-->
# Milestone: The Entry Boundary

Status: **Track 1 in flight.** Plan merged in PR #101. Track 1 (the retention
probe) chartered 2026-07-28: `docs/reviews/charter-2026-07-28-entry-boundary-track1.md`.

## What this is for

Today the owner gets tax facts into the product by hand-editing JSON. The
Legible Entry phase is about replacing that with something a person can use.
The obvious way to do it is a web form. This milestone checks whether that
obvious way is safe before anyone builds it.

Everything the product does with real data so far is a **read**. A session
opens a browser, shows something already in the workspace, and leaves nothing
behind. Entry turns that around: the browser becomes the place real financial
data first appears, and it passes through a text input before it lands
anywhere.

Browsers are built to be helpful about typed text. They remember form entries
for autofill, keep drafts for crash recovery, hold undo history, send
spellcheck to a server in some configurations, and learn from dictation. Any
of those could keep a Social Security number or a wage figure somewhere the
product never looks. We do not currently know which of them apply, because
nobody has checked.

So this milestone answers two questions and writes the answer down. It builds
no product.

## The two questions

**1. Is a browser form an acceptable place to type real tax facts?**

"No" is a real possible answer and the milestone is not a failure if that is
where it lands. A previous milestone in this project rejected its own obvious
shape after checking, and was right to. The mistake to avoid is building a
form and trying to confine it afterwards.

**2. Does an entry surface write facts directly, or emit contribution events?**

The product already has a notion of a contribution as a distinct event, separate
from a run (ADR-0032). Nothing currently says a person operating a surface may
originate one against the real workspace. Either that extends naturally, or a
direct write path is warranted, or neither works.

## How we will answer them

### Track 1 — the retention probe

A throwaway script, run against a synthetic workspace only, that types
representative fake values into a form field in the same confined browser
vehicle the viewing sessions already use, then inspects what the browser wrote
to disk and what it attempted to send.

It is not product code and does not ship. It exists to turn question 1 from an
assumption into an observation. It produces a short findings note listing, for
each retention channel: whether it fired, where the text ended up, and whether
the existing confinement already contains it.

Constraints:

- Synthetic fixtures only. The values typed are obviously fake and are chosen
  to be easy to grep for.
- No real workspace, no real path, no residency locator anywhere — not in the
  script, the findings note, the PR, or this thread.
- The script is deleted or parked outside the product tree once the findings
  note is written. We are not maintaining it.

### Track 2 — the decision

An ADR (next number 0048) that states the answers, the reasoning, and the
consequences. Its evidence is the Track 1 findings note plus the existing
boundary contracts.

The ADR should be readable by someone who was not here. It says what an entry
surface may and may not be, in terms someone building one next quarter can
follow without reconstructing this conversation.

## Not in this milestone

- **Packaging.** How a UI actually reaches the workspace is the next
  milestone. Deciding it here would tangle two independent questions.
- **Correction.** The phase roadmap notes that the supersession policy has no
  human face. Real, but it belongs to the milestone that builds an editable
  surface, not this one.
- **Any UI.** No form, no component, no framework choice, no design.
- **Real data.** Nothing in this milestone touches the owner's actual return.

## How we will know it is done

- The findings note exists and names each retention channel with an observed
  result rather than an expectation.
- ADR-0048 is ratified and answers both questions without hedging.
- Someone reading only the ADR can say whether a browser form is permitted and
  what write path it must use.

No maturity cell moves. This milestone is a decision; the matrix measures
capability.

## Shape of the work

Two tracks on one branch, `milestone/entry-boundary`. The plan merges first as
its own PR; the tracks ride as commits and reach `main-ui` together in the
closing PR, per the merge protocol.
