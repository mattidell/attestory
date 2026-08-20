# Retrospective — Plain Question to Claim Boundary Prototype

## What differed from the plan

The plan asked Track 2 to reduce four competing lens answers into one good
two-sentence answer. The owner re-aimed it mid-milestone: the competing answers
are probes, and their *differences* are the evidence of what explanatory
structure an interface would need. That produced a materially better artifact —
an explanation tree with six branches and a tension catalog — than the original
reduction would have. The lesson is that "pick the winner" is the wrong shape
for an exploratory milestone whose purpose is to discover structure; converging
early destroys the signal the milestone exists to collect.

It also broke a grading criterion. Exit criterion 3 refers to the beliefs
invited by "that answer," singular. After the re-aim there is no singular
answer, so the criterion grades a structure it was not written against. Nobody
noticed until the second advisor review. **Re-aiming a milestone obligates
re-deriving its exit criteria in the same act.**

## What it cost

Four tracks, then two full repair rounds, both triggered by owner-side advisor
review rather than by the project's own checks.

Both repair rounds traced to the same root cause: the Foreman wrote
descriptions of committed artifacts into charters from reading comprehension
rather than verification, and builders reasonably treated the charter as
settled. A wrong description of the Schedule B attachment rule ("subtotals
summed" instead of "tested independently"; foreign-account questions called
triggers when they are post-attachment completeness requirements) propagated
into four packets and the register before anyone opened `runner.py`. Same
pattern produced a `require_closed` count of seven against an actual ten, and
an "unmet closure means a document is missing" finding that the data does not
support at all.

The one thing that worked without repair was lens independence. Three of four
Track 1 builders hit the sibling-file boundary and disclosed the near-miss
rather than reading. Four-way convergence on the blocked-state message is
trustworthy *because* the accounts could not have copied each other.

## Follow-ups

- **`OV-1` — Schedule B categorical triggers.** IRS gives eight independent
  "Who Must File" triggers; the committed rule implements one. Three of the
  seven omitted (accrued interest, ABP adjustment, nominee) are already modeled
  by name in this product. Reactivates whenever Schedule B attachment is
  touched for any reason, or when a filer case with a sub-threshold adjustment
  is added. Confirmed correctness gap, not explanation design.
- **`SC-3` — family-specific blocked message.** Reactivates when the blocked
  disposition's `explain` string is next edited, or when entry UX reaches
  source-family declaration.
- **`SC-4` — no committed artifact designates a current package.** Every
  account in this milestone relied on the "highest version number wins"
  convention. Reactivates the next time any document needs to state which
  package backs a rendered value.

## What should change in the next plan

Charters must cite verification, not recollection. When a charter asserts what
a committed artifact does, the Foreman reads the artifact — and the code that
consumes it — before writing the sentence, or marks the claim explicitly
unverified so the builder checks it. A confident wrong charter is more
expensive than an honestly uncertain one, because it converts one error into a
propagated one.
