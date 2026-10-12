# Student-loan interest: where each ground for line 21 comes from

This is a working domain model, not a schema or a contract. It covers one
filer, one borrowing, one schooling circumstance and one Form 1098-E. It
separates four kinds of ground that can lead to the same Schedule 1 line 21
amount:
- what the person said;
- the tax concept;
- what the application assumes;
- the conditions it leaves with the person.

It also lists the questions that remain before that path is extended.

The returning planning participant of *Planning with a Case Expert*
(`docs/phases/shared-understanding/milestones/returning-planner.md`) wrote
it, and its first-person voice is kept. It was revised through a case
expert's challenges, the owner's challenges and two independent reviews.
The last review found it adoptable with corrections, and those corrections
are applied. The episode history is in that plan's "Track 1 first
observations" and "Outcome". Claims about today's behavior name the rule,
code or test they rest on. Re-check them before relying on them in a later
change.

Bounded to one filer, one borrowing, one schooling circumstance and one Form
1098-E. This is a plain-language account built by reading today's content and
code (`packages/tax/sli_relationship_recording.py`,
`packages/content/tax/2025/rule.sli-worksheet.v5.json`,
`rule.sli-statement-combined-standing.json`,
`rule.sli-sum-inclusion-loan-cost-no.json`, `rule.sli-statement-loan-
support.json`, `rule.sli-statement-support-reason.json`,
`sli-relationship-source.bundle.v2.json`, `sli-combined-standing.bundle.json`,
`sli-scope.bundle.json`, `packages/derivation/presentation_projection.py`,
`packages/derivation/correction_session.py`), against the project's own
accepted ADR on the open statutory question
(`docs/adr/0076-per-subject-scheduling-and-binding-relationships.md`,
cross-checked against the primary regulatory text at
law.cornell.edu/cfr/text/26/1.221-1), and against tests
(`tests/test_sli_correction_session.py`,
`tests/test_sli_line21_explanation_page.py`,
`tests/test_sli_line21_explanation_data.py`) re-run or newly found and
read, not just cited. It is also corroborated against the historical
design record (`a0-tax-concept-facts.md`, `responsibilities-and-
circumstances.md`, `relationship-capability-handoff.md`) only where that
record explains *why* a current shape looks the way it does. Historical
design prose is not treated as current behavior anywhere below; every claim
about what the application does today is a claim about the rule and code
files named with it. My own reading supplied the mechanism; the case
expert, an independent final review, and the owner's own repair-round
challenges each supplied `run`-level confirmation or a correction I had not
found myself — for the adverse answer's wording, the favorable case's
rendered page, a fourth mechanism I had read past, a correction lifecycle I
had mischaracterized, and a product question I had framed around the wrong
remedy. All re-run or re-read by me, not taken on anyone's say-so. What is
still `read` only, not `run`, is listed in "What remains unresolved."

## In plain language, with one example

Maya has one student loan ("Autumn study loan," serviced by Cedar) and one
2025 Form 1098-E from Cedar reporting $3,000 of box-1 interest. This is
`C1`, the exact fixture both the explanation-data and the production-page
tests use, so the numbers below are run, not invented.

Maya tells the application four things: the loan financed her autumn 2024
schooling; the 1098-E's $3,000 includes interest on that loan; the loan
paid only for school costs; and she was enrolled at least half-time. She
also answers the handful of required return-level questions (filing
status, total income of $50,000, no competing Schedule 1 adjustments, not
a dependent, and so on) favorably. Nothing here is a lie or a trick — it
is the ordinary favorable case.

The application does **not** ask Maya whether the loan is a "qualified
education loan" or whether she was an "eligible student" — those are its
own legal categories, not things she is asked to self-classify. Instead:
her four answers feed a rule that, finding no disqualifying answer and no
open question anywhere on the one statement, treats the statement as
fully supported; the worksheet then computes $2,500 as the deduction
(capped interest, reduced by her income's position in the phase-out), and
publishes it to Schedule 1 line 21.

The explanation Maya can actually open, on the real page, separates three
things by name: **What you told us** (her four answers, word for word);
**What the application took as given** (five sentences it assumed without
asking — for example, that the $3,000 is entirely this one loan's
interest, and that no scholarship reduces her school costs) — these are
shown to her, but she currently has no way to tell the application if one
is wrong; and **Conditions left with you** (four things, like whether
Cedar's program meets the school's own definition of half-time enrollment,
that the application never checks and is not claiming to have checked).

If Maya later discloses that the loan actually paid for a laptop as well
as tuition — answering "no" to "did the loan pay only for school costs" —
the whole $2,500 stops being computed. The application does not produce a
smaller number; it blocks, using the same kind of refusal code it would
use for a question nobody had answered yet, though the *sentence* she sees
is specific to what she said, not generic. Separately, if she had already
seen the $2,500 explanation and only later gave that "no," the save that
records her new answer is real and durably supersedes her old "yes." The
page never pretends the old $2,500 is still current: it labels it "an
earlier result... unchanged" wherever it appears, shows the correction's
own outcome in its own titled section, and offers an explicit "Calculate"
action for a fresh number. If Maya closes the page and comes back later,
a real browser-driven test of exactly that — confirm, close, reopen — shows
the reopened page's own "earlier result" already reading "blocked," not
the stale $2,500.

## The working model

Four distinct kinds of ground reach the published amount
(`tax.us.2025.schedule1.line21-sli-deduction`), and the current code keeps
them apart with four different mechanisms, not four different sentences for
the same thing. (An earlier version of this document had three; the owner's
repair round is why there are four; the plan's "Track 1 first
observations" and "Outcome" record that history.)

**1. Required filer- and return-level assertions.** Total income, the
twelve `no-lineNN-*` Schedule 1 absence flags that the "combined" path pins
(the Schedule-1-adjustments-scope succession table has thirteen members;
`no-line24z-writein` is not one of this rule's pins), and the five
`sli-scope.*` filer exclusions (not claimed as a dependent, no Form 2555, no
Form 4563, no Puerto Rico/Samoa income, legally obligated for the interest)
are each named as a `pins` entry with `role: input` and `origin: assertion`
in `rule.sli-worksheet.v5.json`. Each must be an explicit current finding
before the rule runs at all; a missing one blocks with `DEPENDENCY_INVALID`
before the loan itself is even reached. These are not defaulted. Filing
status is also required (it appears in the same path's `requires`), but it
is a different pin shape: `role: choice`, with no `origin` field — a
selected value, not an asserted input, though still a gate.

**2. Ordinary relationship-level circumstance answers, at the one
borrowing.** The person can affirm that the borrowing financed the named
schooling (`financing-relationship`) and that the one 1098-E's box 1 includes
interest on it (`statement-inclusion-relationship`), and separately answer
yes/no/cannot-tell to two further questions keyed to the borrowing itself:
whether the loan paid only for school costs
(`loan-paid-only-school-costs`), and whether the student was enrolled at
least half-time (`enrolled-at-least-half-time`). Each is its own current,
correctable, independently withdrawable finding
(`sli_relationship_recording.py`). Neither borrowing-level fact type asserts
the composite classification it sits beneath: both titles explicitly
disclaim it ("no qualified-loan... assertion", "no eligible-student
assertion").

**3. Facts the application assumes outright, with no answer and no gate at
all.** `rule.sli-statement-loan-support.json`'s `basis.assumed` names five:
the expenses fell in a reasonable period around the loan; the school costs
stand in for qualified higher education expenses with no scholarship or
other tax-free-assistance offset; the schooling was for the taxpayer, a
spouse or a dependent when the loan was incurred; the named borrowing is
indebtedness the taxpayer incurred; and box 1 holds no loan the person did
not record, so the whole box 1 is this loan's interest. None of these five
has a fact type a person can answer or a rule can gate on — unlike
mechanism 2, there is no yes/no/cannot-tell question, and no recorded "no"
could currently change any of them. They are not hidden: the presentation
layer shows them verbatim, under their own heading, as "What the
application took as given" — distinct from "What you told us" (mechanism
2) — but showing an assumption is not the same as making it answerable.
One of the five is exactly a circumstance the historical
`a0-tax-concept-facts.md` F9 table anticipated a person would eventually be
asked: "whose education it paid for" is F9's own row, matched exactly. A
second, "the named borrowing is indebtedness the taxpayer incurred," is
*not* an F9 row — F9's table has no "own indebtedness" entry, and a
repository-wide search for that phrase finds nothing. Its nearer anchor is
the statute's own chapeau ("incurred by the taxpayer") and, separately,
a0's F7 ("legally obligated to pay the interest"), which a0 treats outside
F9's table and explicitly defers ("what it takes to *be* legally
obligated... is as far as this milestone needs to go") — a related but
different question from whether the taxpayer incurred the debt at all. The
current build assumes both instead of asking either, which is the point
that survives; only the F9 cross-reference for the second one does not.

**4. Conditions the application represents as applying but never solicits or
establishes.** Institutional eligibility, whether the program leads to a
recognized credential, whether the course load meets the institution's own
half-time standard, and the cost-of-attendance figure the institution would
set are named in the computation's own explanation —
`rule.sli-statement-loan-support.json`'s `basis.left_with_person` — but
contribute no finding, no pin and no gate. They are visible, not consumed,
shown under "Conditions left with you," and — unlike mechanism 3 — framed
as the *person's* responsibility rather than the *application's* own stated
assumption.

A fifth basis key, `derived` (three sentences about current-row counts,
e.g. "exactly one current affirmed inclusion"), is read by the rule but is
not passed into the presented explanation at all
(`presentation_projection.py::_sli_support_basis` builds only `answers`,
`assumed` and `leftWithPerson`) — it is working plumbing, invisible to the
person, and belongs to none of the four mechanisms above.

**The favorable conclusion is produced from a default, not from an
affirmative favorable finding.** When none of (1) or (2)'s required answers
is disqualifying, and no applicability marker, unresolved link, withdrawn
link or denied inclusion is current on the one statement, that statement's
`tax.us.2025.sli.statement-combined-standing` is the literal category
`none`. Only then does the worksheet's single live ("combined") path compute
the capped, MAGI-phased-out dollar amount; the rule's own notes state "the
only favorable combined value is none."

**What a later, unfavorable answer does, in this one-statement case.** A
"no" to either borrowing-level question changes that one statement's
category away from `none` (via `rule.sli-sum-inclusion-loan-cost-no.json`
and `rule.sli-statement-combined-standing.json`). Because there is exactly
one statement in this bounded case, that single change is enough to fail the
worksheet's across-all-statements "every current statement is `none`" test,
which **blocks the entire computation** with `DEPENDENCY_INVALID` rather
than producing a smaller number — the bounded case degenerates to "compute
the full favorable amount, or block," with no prorated middle value,
because nothing in the current rule graph allocates a disqualified loan's
interest. The person is not shown a generic "missing information" sentence
for a fact already supplied: `sli-combined-standing.bundle.json` carries a
specific sentence per disqualifying category (for example, "You said the
loan on this statement did not pay only for school costs. The deduction is
worked out here only for a loan used only for school costs."), and
`presentation_projection.py` has a dedicated function
(`_selection_blocked_reasons`) whose purpose is to attach that specific
sentence, statement by statement, to the blocked line — not a generic
dependency-missing message. **This is corroborated at `run`, not only
`read`:** the case expert ran `tests/test_sli_correction_session.py::
BlockedNoToYesCase` and `FirstWorkingExample::
test_choose_cedar_confirm_yes_to_no` and confirmed both the block and the
specific, attributed wording for a recorded "no" (as against a reassuring
"no answer yet" sentence for a merely missing one).

**A statement's own favorable standing is not the same signal as the
deduction having computed — this case only makes them look the same.**
The expert's two-statement fixture showed a statement row reading
`statement-combined-standing: none` / `statement-loan-support:
plain-case-supported` while the return's own `line21_value` was still
`None`, because a *different* statement was adverse. In this task's
one-statement bounded case, the per-statement standing and the
across-all-statements worksheet gate necessarily agree — there is only one
row to check — but that agreement is a property of the bounding, not a
general fact about the mechanism. A consumer or explanation built by
reading one statement's row in isolation, generalized past this bounded
case, would be reading the wrong signal.

**Why this matters, in the milestone's own terms.** In this one case there
are five different things, and the current rules keep them on five
different mechanisms, none collapsed into another:

- a user-supplied ordinary circumstance (the two borrowing answers and the
  two relationship links) — correctable, and *defeating* when adverse;
- a canonical tax concept (qualified education loan / eligible student) —
  never directly asserted by anyone;
- a default basis reached only when no supported disqualifier is current
  (the `none` standing) — favorable, but defeasible by mechanism 2's "no";
- an outright assumption with no defeater fact type at all (mechanism 3,
  `basis.assumed`) — favorable, shown, but not currently answerable or
  gateable by anything the person could say;
- the representation that a third-party condition applies without being
  established (mechanism 4, `left_with_person`) — framed as the person's
  own responsibility, not the application's assumption, and consuming
  nothing either way.

Mechanisms 3 and 4 look alike from a distance — both are visible,
unconsumed, and un-gated — but they are not the same claim. Mechanism 4
says "this is on you, we don't check it." Mechanism 3 says "we assumed
this on your behalf, and you cannot currently tell us otherwise even if you
know better." I did not notice mechanism 3 at all in this document's first
three committed versions; the plan's "Outcome" records that.

## What remains unresolved

- ~~The data-to-screen gap.~~ **Settled by an independent final review,**
  which cited and I independently re-ran (1 passed):
  `tests/test_sli_line21_explanation_page.py::SavedLine21ExplanationPage::
  test_c1_shows_separate_answers_assumptions_working_and_run`. It renders
  this exact bounded case through the real production page
  (`live_session.py::_render_page` → `citation-walk.v1.html`) and asserts
  three distinct, non-overlapping groups — "What you told us", "What the
  application took as given", "Conditions left with you" — with
  "Deduction: 2500" present and no `DEPENDENCY_INVALID` text, and
  `citation-walk.v1.html` renders `row.basis.leftWithPerson` inside each
  statement's own card. The committing commit (`e544af11`) predates my own
  first working-model commit (`5b719dac`); this was findable, not newly
  produced. Carried forward as a fact the model relies on, not as an open
  question.
- ~~Correction-time behavior, and what a person sees afterward.~~
  **Settled, after two rounds of my own mischaracterization.** I first
  wrote this as "the prior figure is retracted and replaced" (wrong — the
  original is kept, deliberately, per `CorrectionRuntime`'s own docstring:
  the saved presentation "is never written, modified, or used as write
  authority"; a confirmed save starts a *new* run under its own output
  name instead). I then read `RecoveryRuntime::
  test_calculated_outcome_is_recovered_by_its_own_token`'s own comment —
  "the defect: `state()` still serves the original 2300" — as describing
  what a real person would see on returning to the application, and made
  that the model's top open question. On the facilitator's challenge, I
  checked what that comment actually refers to: `RecoveryRuntime`'s own
  docstring says it tests only "`CorrectionRuntime.outcome` and
  token-bound `retry`," via a fixture (`_open()`) that constructs the
  runtime with a **fixed**, pinned `saved_presentation_path` — deliberately
  unlike the real reopening path, `CorrectionRuntime.open()`
  (`correction_session.py:850`), which carries no such fixed input and
  resolves "the earlier result" fresh from the workspace's durable state
  each time it is constructed. I read the actual served page
  (`packages/sample_data/sli_correction_t1/surface/content/app/index.html`)
  and found it never presents the old figure as current: every appearance
  is labeled "This is an earlier result" / "...— unchanged," the
  correction's own outcome renders in its own titled section, and an
  explicit "Calculate" action is offered. I then ran
  `tests/test_sli_correction_resumption.py::SavedAccountResumption::
  test_reopened_page_shows_the_correction_and_drops_an_old_token` (1
  passed, a real headless-browser driver): it confirms a correction, closes
  that process, opens a genuinely new one against the same durable
  workspace, and the reopened page's own "earlier result" banner already
  reads "Line 21: blocked" before any further click. The comment I had
  built an action around describes one test fixture's own documented,
  narrow contract — not the production reopening path, which is tested
  separately and passes. Carried forward as a fact the model relies on,
  not as an open question.
- **Mechanism 3 (`basis.assumed`) is read, not run, and not yet checked
  against the statute the way mechanism 2 was.** I have not confirmed, by
  running a case, that any of the five assumed items would actually cause
  a wrong number if false — only that nothing currently asks about them or
  could gate on them if the person volunteered a contrary fact.
- **"Block vs. prorate" was the wrong frame — see action 2 below.** The
  expert's two-statement fixture (Cedar adverse, Birch untouched) already
  showed that Cedar's "no" produces `line21_value: None` for the *return*,
  not just a change to Cedar's own row — the all-statements gate blocking
  everything is not purely an artifact of this task's one-statement bound.
  My own close reading of `docs/adr/0076-per-subject-scheduling-and-
  binding-relationships.md`, cross-checked against the primary regulatory
  text, shows "prorate" (a portion-based rule) is the *weakest*-supported
  of the law's options for a single disqualified loan, not the natural
  next build. A later working-account trial (run for action 3) found
  something
  stronger than the statute reading alone: the rule already produces a
  definite stated zero, not a block, for two filer-level conditions
  (`not-claimed-as-dependent`, `legally-obligated-for-interest`), reasoned
  explicitly in content as "the law's own definite $0... not a block" —
  while loan-cost and enrollment "no" still hit the generic
  `DEPENDENCY_INVALID` block. What remains open is narrower than either
  version above: not whether a stated zero is possible (it already
  exists, elsewhere in this rule), but why it stops before loan-cost and
  enrollment, and whether it should.
- **Whether the filer-level pins get the same explanation quality —
  partly answered, not fully.** The working-account trial found that
  `not-claimed-as-dependent` answered "no" reaches a definite number
  (`Deduction: 0`, via `Z1`), which I had not expected — so the filer-level
  pins are not simply falling through to an undifferentiated block the
  way I first assumed. What I still have not found is any test asserting
  an *attributed sentence* for that zero, the way `BlockedNoToYesCase`
  asserts one for loan-cost. Whether the rendered page explains the $0 by
  name or just states the number is open. Independent review did not
  check this either (explicitly left unverified).
- **One count was wrong.** Mechanism (1) said "thirteen" `no-lineNN-*`
  pins; the `combined` path pins twelve (`no-line24z-writein` is a member
  of the Schedule-1-adjustments-scope succession table, not of this rule's
  pins). Corrected above; does not change which mechanism each pin belongs
  to.

## Development action plan

Each action names what it would settle and why that matters; none selects
an implementation. Four earlier actions are not listed here because they
no longer name a remaining question: rendering the favorable explanation on
the real page, the adverse answer's wording, the `left_with_person`
items' per-statement grouping, and what a person sees after a correction
(including on reopening the application later) are each already confirmed
at `run` (`test_c1_shows_separate_answers_assumptions_working_and_run`,
`BlockedNoToYesCase` / `test_choose_cedar_confirm_yes_to_no`,
`test_reopened_page_shows_the_correction_and_drops_an_old_token`) and are
now load-bearing facts in "The working model" above, not open actions. The
last of these was my own top action in the version before this one; a
facilitator challenge led me to check what its cited comment actually
referred to, and it was a narrow test fixture's own documented contract,
not the production reopening path, as recorded in the plan's "Outcome".
One narrower question survives from the `left_with_person` item; see
action 1 below.

1. **Confirm the `left_with_person` grouping and per-item wording hold
   outside the one page already tested.** The production-page test proves
   per-statement grouping on one entry point; it does not prove the same
   for any other presentation surface, and it does not check that each of
   the four items' individual wording matches
   `rule.sli-statement-loan-support.json` rather than just their count and
   disjointness from "What you told us."
   *Settles:* whether the one tested page generalizes or is a special
   case.
   *Matters because:* this is the one distinction the whole milestone is
   about; a silent regression on an untested entry point would be exactly
   the kind of thing a single passing test cannot catch.

2. **Decide, as an explicit product question, what a known, disclosed
   disqualifying answer should produce for a single loan** — a definite
   stated amount (zero, under a whole-loan-disqualification reading) or
   today's undifferentiated block — now that the law has been checked
   rather than assumed. `docs/adr/0076-per-subject-scheduling-and-binding-
   relationships.md` (Part 3, status: not decided) and the primary text
   (26 U.S.C. § 221(d)(1); Treas. Reg. § 1.221-1(e)(3), (e)(4) Example 6,
   independently confirmed by fetching the regulation) distinguish four
   things my earlier framing ran together:
   - *Qualification of one borrowing* — whether this loan, as a whole, was
     incurred "solely" to pay qualified higher education expenses. This is
     what loan-cost and enrollment bear on, and it is a per-loan question
     — § 221(a) allows interest "on any qualified education loan," tested
     loan by loan.
   - *Allocation among borrowings* — when a person has more than one loan,
     each is tested on its own facts; a disqualified loan does not touch a
     separate loan's own figure. Nothing to build here beyond testing each
     loan independently, which is not what this bounded, one-borrowing
     case exercises.
   - *Exclusion of nonqualifying interest within one loan* ("portion-
     based," i.e. prorating) — my earlier framing treated this as the
     natural missing piece. The regulation does not support it: Example 6
     decides the *whole loan* is not a qualified education loan for mixed
     use, with "no fraction," and ADR 0076 independently finds "no quoted
     sentence states that proportion." A single disqualified loan is the
     weakest-supported candidate for allocation machinery, not the
     strongest.
   - *The application's current refusal* — a generic `DEPENDENCY_INVALID`
     block for the loan-cost/enrollment case, the same code used for a
     genuinely missing answer. ADR 0076 names this posture
     ("unresolved-blocks") as arguably the *wrong* one for a case the
     statute actually decides, as against a case where the status is
     genuinely unknown.
   **This is not only a reading of the law — it is already the rule's own
   split.** A working-account trial run for action 3 below found that
   `rule.sli-worksheet.v5.json` does not block uniformly: when
   `not-claimed-as-dependent` or `legally-obligated-for-interest` answers
   "no," the rule's own inner arithmetic returns a definite `0`, not a
   block — confirmed by `tests/test_sli_line21_explanation_page.py`'s `Z1`
   case ("Deduction: 0", no "Limit " text) — and
   `sli-scope.bundle.json` titles these two fact types explicitly as "legal
   zero, not a block... the law's own definite $0 for this return, not
   missing information and not a block." The *other* three `sli-scope.*`
   pins (no Form 2555, no Form 4563, no Puerto Rico/Samoa income) and the
   four double-benefit witnesses still block outright
   (`SLI_UNIVERSAL_COMPONENT_VIOLATION`) on "no," same as loan-cost and
   enrollment do. So the question is no longer "should the application
   ever state a zero instead of blocking" — it already does, reasoned
   explicitly, for two specific conditions. The sharper question: why does
   that same treatment stop before reaching loan-cost and enrollment,
   which Example 6 arguably decides just as definitely as dependent status
   does, and should it extend there.
   *Settles:* whether today's block for loan-cost/enrollment is a
   considered choice distinct from the dependent/obligation treatment (and
   if so, on what ground), or an inconsistency nobody has looked at
   together — a materially smaller and better-grounded question than
   "build proration," and sharper than my own first reading of the statute
   alone produced.
   *Matters because:* commissioning portion-based allocation from an
   unchecked premise would build the regulation's *least* supported
   option; the rule's own existing zero-vs-block split shows the
   better-supported alternative is not hypothetical — it is already
   running, for a sibling condition, in the same file.

3. **Trace whether a missing or unfavorable filer-level pin gets a
   comparably specific explanation** to the two borrowing-level answers, or
   falls back to a generic missing-dependency message. **Partly run, not
   fully:** the same working-account trial found that at least one filer-
   level pin (`not-claimed-as-dependent`) does reach a definite, specific
   *number* ("Deduction: 0") rather than a generic block — a finding this
   action had not anticipated — but no test I found asserts an attributed
   *sentence* for it the way `BlockedNoToYesCase` does for loan-cost. Open:
   whether the actual rendered page explains the $0 figure by name, or
   just states it.
   *Settles:* whether the explanation quality demonstrated for the
   relationship work generalizes to the filer-level responsibilities, or is
   a special case built only there.
   *Matters because:* the milestone frames one path from what a person can
   know and say to what the application can calculate and explain — if only
   one kind of ground on that path is legible, a future reader of this
   milestone could overstate how much of the path is actually solved.

4. **Decide, as an explicit product question, what should happen to each
   of mechanism 3's five `basis.assumed` items** — stay a silent, un-gated
   assumption disclosed only as "what the application took as given"; or
   become an ordinary answerable circumstance, the way `a0-tax-concept-
   facts.md`'s F9 table originally anticipated for "whose education it
   paid for" (F9's own row) and, on a different anchor, the statute's
   chapeau and a0's separately-deferred F7 for "is this the taxpayer's own
   indebtedness"; or something else. Do not build a new fact type or
   question from this action alone — it asks for the decision, not the
   implementation.
   *Settles:* whether the gap between "disclosed as an assumption" and
   "answerable, with a channel to disconfirm it" is an accepted product
   posture or an unfinished piece of the relationship work that stopped
   partway through the circumstances a0 and F9 together name.
   *Matters because:* a person who actually knows one of these five facts
   is false currently has no way to tell the application so, and no
   amount of care in presenting "what the application took as given"
   changes that; deciding whether that is acceptable is a product
   question, not a wording question.
