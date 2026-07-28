# Retrospective: Presentation — Real Session and Attestation

Phase: Real Return. Completed 2026-07-27.
Plan: `docs/phases/real-return/milestones/presentation-real-session-attestation.md`.

**Result: Presentation moves L2 → L3 in the W-2 wages (1a) column.** The first
maturity lift for the Presentation row since it was created, and the first time
this project's human surface has run on the owner's real data.

## What happened

Three tracks. One agent-built, two owner-operated, all on one branch, one PR at
close.

**Track 1** was chartered as a documentation track — write the runbook for the
owner's sitting, and define a failure vocabulary that is mechanical rather than
evaluative, because ADR-0047 precondition 5 forbids the owner from describing a
defect they see during the real session. It produced the runbook. It also
produced **three real code defects**, all found by independent review, and all in
code the previous milestone had already rehearsed and passed.

**Track 2** launched a real headed browser against a synthetic workspace and
rendered the product page. Clean pass, one skipped item, one soft finding.

**Track 3** was the real session and the attestation. Non-descriptive, five
preconditions affirmed individually, one cell moved.

## The lesson: a rehearsal covers the paths it drives, and nothing else

The Live Session Path milestone rehearsed this code end to end and returned a
clean result. It drove the happy path and three designed refusals. That is a
real exercise and it caught real things. It did not catch any of these:

1. **`LiveViewingError` is a sibling of `PresentationSessionError`, not a
   subclass.** Roughly a third of the runbook's own reason-code table reached the
   owner as an uncaught traceback — the one text the non-descriptive vocabulary
   is structurally unable to describe. A documentation track found this by
   writing down what the owner would see.
2. **Teardown's `except` was too narrow for its own promised code to be
   reachable.** "Teardown did not complete" was legal vocabulary for a condition
   that could not actually arrive as that code.
3. **Ctrl-C left an orphaned headed browser** still displaying the real return,
   plus a `.live-view/session-*` directory holding that browser's profile and the
   disk cache of the render — while the preflight's backup-and-indexing guarantee
   binds only at session *start*. Residue outliving the session outlives the
   guarantee.

None of the three is exotic. All three sit one step off the happy path, and the
third is the single most likely way a human actually ends a program. The durable
form of this: **a rehearsal's value is bounded by the set of endings it drives,
and "the user gets bored and hits Ctrl-C" is an ending.**

## The lesson that repeated: fail-open drift

Twice in this milestone the obvious repair was to fix the **runbook template**
rather than the library — add a `try/finally` to the snippet the owner copies,
add a broader `except` to the example. Twice the foreman directed the fix into
`open_presentation_session`, `launch`, and a context manager instead.

The reason is a failure class this project has now named three times: **a
guarantee that lives only in a copyable example silently no-ops the moment
someone adapts it.** The owner who retypes the snippet from memory, or trims it,
gets none of the protection and no signal that it is gone. Structure survives
adaptation; templates do not.

This is worth promoting past this milestone. When a fix can go in either the
mechanism or the example, it goes in the mechanism, and the example is left as
an example.

## What the arrangement was actually for

The plan's central design move was putting a **synthetic real-browser rehearsal
between the build and the real session**, with a hard gate. That looked like
caution. It was structural.

The constraint: the owner's attestation is non-descriptive, so if the real
session renders something wrong, **the person who saw it is the one person
forbidden to say what it was**. A page defect found during Track 3 arrives
unactionable. Track 2 exists so that the first real render is not also the real
session — it puts a real browser on the real product page in the one context
where description is safe and repair is cheap.

It worked in the weak sense: Track 2 found no page defect, so the gate never
fired. It worked in the strong sense too, which is easier to miss — it gave the
interrupt-teardown repair its **first human confirmation** (no surviving browser,
no surviving session directory), and it did that before the browser in question
was displaying the owner's real return.

Reviewing it honestly: if Track 2 had been skipped and Track 3 had gone fine
anyway, the milestone would have looked identical from the outside. That is the
usual shape of a control that works. The argument for it is not that it caught
something; it is that the cost of it catching nothing is one owner hour, and the
cost of it being absent when needed is a defect nobody is allowed to report.

## Review economy

Track 1 ran five agent cycles: build, review, repair, recheck, repair, recheck.
That is more than intended for a documentation track, and every extra cycle was
caused by real defects rather than by review churn — the reviewer twice found
things by **running** the path rather than reading it, which is the single
highest-yield behaviour in this milestone's record.

Two foreman calls worth recording:

- **Independent review over self-review.** The foreman wrote both the plan and
  the build charter, including the mechanical-versus-evaluative line the
  vocabulary turns on. A foreman review could test the builder's execution of
  that line but not the line itself. The independent reviewer found all three
  code defects.
- **Beyond-charter changes reviewed as new work.** The builder twice went past
  its findings and flagged both honestly. Those changes were re-chartered as
  fresh review scope rather than accepted on the builder's account of them, and
  the second recheck confirmed one carried an unclaimed bonus and one carried an
  overstated sentence.

The last residual — an overstated runbook sentence about what the library
guarantees — was closed by the **foreman directly** rather than by a third build
cycle, and recorded in the review record precisely because no independent reader
had seen that edit.

## The charter's verification floor was narrower than the gate

The closing PR failed CI twice, on two independent defects, both introduced by
the same repair commit and both invisible to everything this milestone ran.

The first was a test asserting `URLError` where Linux raises
`ConnectionResetError` — a platform's errno encoded as if it were the contract.
Every exercise of that path had run on macOS, including the reviewer's, who
verified the repair by running it. That one is **the milestone's main lesson in
miniature**: the exercise covered what it drove.

The second is the more useful finding. With the test fixed, CI reached the
`mypy` step for the first time and failed there — a `strict = True` type error
that had sat in the code through a build, two repairs, and three independent
review passes.

**It was never looked for.** Every Track 1 charter carried the same verification
block: three `unittest` modules, two harness manifests, `envelope_scan.py`,
`git diff --check`. CI runs `pytest`, `mypy`, `governance_lint.py`,
`envelope_scan.py`. The charter simply omitted the type check, so no builder and
no reviewer ever ran it, and every one of them reported green in good faith.

That is a foreman defect, not a builder or reviewer one, and it is the cheapest
correction available from this milestone: **a charter's verification block
should be the CI sequence, or a stated subset with the omission justified.** A
floor quietly narrower than the gate reports green on work that is not.

The repair itself preserved what mattered: the classified error is still raised
after its handler exits with `sys.exc_info()` clear, which is the
locator-confinement property the second repair existed to establish and the
reviewer verified independently. Only the control flow around it moved. Detail
in the milestone plan's execution record.

## Honest gaps at close

- **The classified-refusal path has no human confirmation.** Track 2's
  browser-start-failure exercise was skipped, which its charter permitted. That a
  failing browser arrives as a stable reason code rather than a traceback rests
  on tests and review only. Named in matrix footnote 14.
- **The runbook has an unidentified unclarity.** Its first human user reported it
  as "not very clear, but fine" and the specific sentence was not identified. It
  is carried open rather than closed by guesswork — a rewrite aimed at the wrong
  sentence is worse than no rewrite.
- **Four Presentation cells remain L2.** Nothing technical separates them from
  the one that moved; the record separates them. Extending the claim needs an
  attestation that names those columns.
- **Track 1's four residuals stand**, plus the owner-held pair — invocation
  discipline and the `cd` history entry — that nothing this repository writes can
  close.

## A near-miss worth recording

Mid-milestone the foreman used `git add -A` on a commit while an owner-supplied
attestation file sat in the working tree. Nothing leaked, because the file had
not been created yet — **luck rather than discipline.** The file was gitignored,
and explicit paths were used for every subsequent commit. In the one milestone
where real data finally enters the picture, "it happened to be fine" is not the
standard.

## Pointers

- Track 1 build: `748b8e8`; repairs `894ff23`, `36317be`.
- Track 1 reviews: `docs/reviews/2026-07-27-presentation-real-session-attestation-track1-review.md`,
  `...-track1-recheck.md`, `...-track1-recheck2.md` (READY).
- Runbook and vocabulary: `docs/runbooks/presentation-real-session.md`.
- Track 2 rehearsal record:
  `docs/reviews/2026-07-27-presentation-real-session-attestation-track2-rehearsal.md`.
- Track 3 attestation:
  `docs/reviews/2026-07-27-presentation-real-session-attestation-track3-attestation.md`.
- Maturity movement: `docs/phases/real-return/maturity-matrix.md`, footnote 14.
