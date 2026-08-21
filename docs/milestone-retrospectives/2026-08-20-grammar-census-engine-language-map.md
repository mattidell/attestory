# Retrospective — Grammar Census: Engine Language Map

## What differed from the plan

The plan's Track 2 charter, filed by the Foreman, covered only one of its
three named deliverables — the reconciliation. Representative traces and the
tension catalog were left for a later charter that didn't exist yet. The
Track 2 Builder caught this itself, recorded the gap in its handoff report,
and correctly did not expand its own scope to fill it. Track 2b closed it as
a continuation unit inside Track 2, not a new track — `foreman_context.py`'s
milestone-state validator only admits `track-<digits>`, and reaching for
`track-2b` as a state value (which I initially wrote) would have been wrong:
Track 2 wasn't done, so the state correctly stayed `track-2` until all three
deliverables existed. The tooling's narrower vocabulary caught a framing
error in my own prose before it was committed.

The dispatch mechanism changed mid-milestone by explicit owner direction:
Tracks 0–2 ran as Claude sub-agents; from Track 1 onward the owner directed
use of the `grok` CLI as a same-worktree, same-branch Builder with
`--permission-mode bypassPermissions`, and Track 3 was cut short when the
tool's API balance was exhausted (HTTP 402) mid-run for both concurrent
streams. Both had committed incrementally up to that point; the Foreman
salvaged and verified the last uncommitted section of one stream rather than
losing it or re-dispatching for a small remainder.

## What it cost

One repair cycle, entirely self-generated rather than owner-triggered: Track
0's boundary corpus went through five rounds before closing, three of them
finding citation defects the round before had introduced (an off-by-one line
span, a false claim about what a prior round said, an inherited version-series
gap). None of the five rounds was requested by the owner; each was the
Foreman or a Builder checking the previous round against source and finding
it wanting.

The single most expensive individual finding was also the most valuable one.
A Foreman ruling made during Track 0 — that a depth bound is enforced "twice,
on the module side" — was falsified by Track 2's adversarial reconciliation,
which ran the two enforcement code paths against the same synthetic input and
watched them diverge. Every citation in the ruling's sentence was correct in
isolation; the sentence was still false, because the function connecting the
citations was never opened. The correction cost one standalone record and
three file edits. It did not cost a re-derivation of Track 0, because the
census's structure — isolated readings, adversarial reconciliation required
to spot-check agreement rather than trust it — meant the error was contained
to one sentence's reasoning rather than propagating into the corpus.

## What worked without repair

Track 1's three-way independence held for real, not just on paper: each
stream reported seeing a sibling's deliverable appear mid-run and declined to
open it. That independence is what let Track 2's reconciliation treat
agreement across all three as evidence rather than as one reader's opinion
copied twice — and it is also what let the one failed three-way agreement
(the predicate-depth bound) surface as a disagreement with the evidence
instead of a consensus nobody questioned.

Incremental committing survived two unplanned kills — one from a harness
background-task limit, one from an exhausted API balance — with zero lost
work in the first case and one salvageable, verifiable section in the
second. The instruction to commit as you go, not at the end, was cheap to
give and paid for itself twice.

## The lesson worth carrying forward

A verification method is only as good as its willingness to turn on its own
author. This milestone's structure — three isolated readers, a reconciler
required to spot-check rather than trust, a Foreman who corrects his own
ruling on the record rather than quietly walking it back — caught an error I
made and would not have caught by re-reading my own reasoning. The
correction record exists because the alternative (leaving a falsified
sentence standing in a closed deliverable, unflagged) would have satisfied
exit criterion 4 in letter while violating it in substance. The next
milestone that includes a Foreman ruling should assume it will eventually be
checked by evidence the milestone itself produces, and should not treat that
as a failure mode to prevent — it is the mechanism working.
