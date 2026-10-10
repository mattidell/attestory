# Retrospective — Reviewing and Correcting the Account Behind a Result

## What differed from the plan

The plan assumed that connecting a displayed answer to the recorder might be
the uncertain part. P0 found the opposite. The durable correction already
worked:

- it was keyed by the borrowing's identity and refused a stale predecessor;
- one save reached every form that includes the borrowing.

What was missing were four connections around that save:

- from a displayed answer to its current target;
- from a confirmation to the save;
- from the save to a recalculation;
- from one saved result to another.

Neither line had a surface for this question. `main-ui` held only a broader
W-2 pattern, so no integration between the lines was needed.

P1 recommended serving a plain page from the repository. R2 showed that this
misread its precedent: the only write-capable page reaches the workspace
through the ADR 0049 surface-artifact route. The selected home was the same
session with its page delivered as a one-entry surface artifact and a no-op
build. That needed no Node, no schema and no ADR.

Track 0 closed on prototype evidence, and the integrated session then lost
four of its guarantees:

- `choose` prepared a review of the selected borrowing only, so the
  distinguishability check had nothing to compare;
- the clue formatter rendered every financing outcome as "financed", so a
  withdrawn financing still saved;
- the page claimed "nothing changed" after a failed response;
- the page showed codes instead of the explanation.

The owner's integrated review found these. Three rounds followed, each
tracing one more connection:

- the repair, reviewed by R3;
- corrections, including attribution by identity;
- explanation parity with the citation walk, then R4's redaction and amount
  corrections.

Track 2 added named synthetic states to the runner, a retry that only
recalculates, earlier results, the shared borrowing, duplicate labels and
the no → yes direction. R5 then made three low corrections. It also found
that two identical borrowings can be visible in a result, and that the page
refuses them without writing.

## What it cost

- **Reviews before production:** three. R1 reviewed P0 and the plan; R2
  reviewed P1 and Track 0; T0b ran the claims R2 found asserted.
- **Track 1:** the build, then three repair or correction rounds and an
  explanation-parity unit, with reviews R3 and R4. The owner's own review
  started the first round.
- **Track 2:** the build, review R5 and one correction unit.
- **Interruptions:** Sonnet units hit usage limits three times; each resumed
  from committed units. Track 2's continuation, R5 and the R5 corrections ran
  on Grok, as the owner directed (about $1.8–$1.9 per unit).
- **The full suite** took about 19–21 minutes locally. CI on `main` already
  took 51–82 minutes before this milestone, so AGENTS.md's figure of about
  61 seconds is out of date. The new module adds about 2–3 minutes. Sharing
  its initial run helps only within one xdist worker.

## Follow-ups

- **Owner visual check and wording.** The owner has the per-state walkthrough
  in the README. The wording is provisional. The constant tables are copied
  from the citation walk because each surface artifact is self-contained, so
  a change to the wording must be made in both pages.
- **Independent reader assessment.** Not performed. Whether a reader who has
  not seen the engine can identify the borrowing, answer, change and result
  is still qualitative and unmeasured.
- **The identical-pair refusal** does not say which clue the two borrowings
  share.
- **In the blocked state**, the confirmation starts with the proposed answer
  equal to the current one.
- **The correction session is synthetic only**, like the W-2 entry loop. Using
  a real workspace would need the residency path and an owner decision.
- **AGENTS.md's test-lane timings** need re-measuring. That belongs to process
  work, not this milestone. On the last correction unit, the fast lane
  reported 22 budget overruns, all in modules this milestone did not change.

## What should change in the next plan

A safeguard demonstrated with a helper is evidence about the helper, not
about its caller. When Track 0 closes on a prototype, list each safeguard
with the inputs that make it work. Then have the integrated review check that
the production caller still supplies those inputs. Here the
distinguishability check worked only because the prototype showed both
borrowings; `choose` showed one.

Information the backend keeps can be lost on its way to the person: in a
formatter, a renderer, or a runtime that passes rows without their reasons.
Before calling an interaction complete, trace each displayed claim back to
the model field it comes from. Check the page for any sentence that promises
something the page does not show, such as "the reason is named above".

Exception text is not a message for the person. Map each class of refusal to
a fixed sentence at the surface boundary. Then a later change to a recorder's
message cannot leak through the page.
