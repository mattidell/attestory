# Retrospective — Less Repeated Work, the Same Defects Caught

## What should inform the next investigation

The repeated derivations visible in a test were not the cause of its repeated
workspace folds. The retained story ran the coordinator, forward runner and
reference runner 11 times each, but the latter two together accounted for
only about 1.4s cumulative and neither called `findings.project`. Recording,
review, coordination and test setup caused the folds. For the next cost
question, retain caller-level attribution before choosing what to remove.

The safe reuse boundary was the observation the coordinator had already
made in that same call. It did not require a retained cache or changes to
the historical source-binding checks. Current state and admission-time state
are not interchangeable, even when they happen to produce the same answer.

The existing manual-marshalling test and a cold row fixture did not prove
the proposed live shortcut was wired correctly. The new regression enters
the coordinator, observes exact local-state identities and the number of
full-current folds, and checks its own publication and saved result. Its
count includes deep-copied equal acts, so another replay cannot evade the
witness merely by copying its input. These observations are the useful
starting point for reviewing the next reuse lifetime.

## Result and limits

The live return no longer reprojects its full history solely to obtain its
current applicability rows. Cold callers and historical prefix readers stay
fresh. No test, runner-parity check, refusal or saved-output assertion was
removed. Independent semantic review found no material issue.

The [measurement note](../phases/engineering-health/milestones/test-cost-and-coverage-evidence/measured-applicability-reuse.md)
separates case timings from diagnostic counts and records the historical
comparison's limitations. It is not a controlled whole-suite speedup. PR #213
holds final publication review and exact-head CI; the earlier implementation
review is not a substitute for those gates.

No material semantic dissent remains. Investigation did not justify culling
the sampled tests or moving application code into separate deployable modules.
Package validation remains a larger measured item, but it already memoizes
schema checks. Its remaining cost needs a more specific account before a new
cache or partial catalog is proposed. Historical lattice construction and
local component commands remain other candidates. The next milestone is not
selected by this closeout.
