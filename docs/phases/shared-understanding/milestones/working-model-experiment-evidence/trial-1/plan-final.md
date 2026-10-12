# Plan: joint return, both spouses with Form 1098-E interest (TY2025)

Endpoint: a readiness claim — does the team understand enough to select an
approach for handling this case, what supports that, or what must be
established first. No representation is selected; nothing is implemented.

## Actions

1. **What the application does today (developed — snapshot 1).** Findings:
   - A 1098-E statement's identity is `lender + statement + tax-year`
     (`packages/content/tax/2025/f1098e.bundle.json`). No key or companion
     fact says whose statement it is (taxpayer vs spouse). The same holds
     for the borrowing reference and the per-statement answers.
   - The person-level answers — `sli-scope.legally-obligated-for-interest`
     and `sli-scope.not-claimed-as-dependent` — are keyed on **tax-year
     only** (`sli-scope.bundle.json`): one yes/no for "the filer".
   - Filing status is a return-level fact; the worksheet already selects the
     MFJ threshold/range and blocks MFS (`SLI_MFS_INELIGIBLE`). So an MFJ
     return with two 1098-Es today would very likely just sum both box-1
     figures under one $2,500 cap — mechanically plausible, but the "filer"
     answers silently stand for two people. **Not yet run**; action 1b.
   - 1b. **Observed (snapshot 3).** A scratch probe (`temp/mfj_probe.py`)
     reuses Track 5's two-statement fixture (Cedar $1,500, Birch $1,800)
     with filing status varied, run through `live_coordinate_run` on both
     runners: single/50k → 2,500; **MFJ/50k → 2,500; MFJ/185k → 1,250**
     (half-way through $170k–$200k); MFS → `SLI_MFS_INELIGIBLE`. The joint
     arithmetic is correct today. Nothing in the run knows the two
     statements belong to different people.
4. **Prior decisions (developed — snapshot 1).** Findings:
   - `student-loan-circumstance-association-evidence/whose-deduction-model.md`:
     the owner directed (2026-09-22) a **filer-centred** model — "no other
     payer's identity is represented unless a concrete supported case
     demonstrates that identity is necessary". Its remaining limitations
     leave "two people each deducting part of one loan" unsettled. It does
     not address a joint return, where both people are on one return.
   - The translation milestone's non-goal: "no universal person, household …
     ontology unless the selected case demonstrates that a bounded
     representation cannot be honest". The joint-return case may be exactly
     such a test, so the team must show whether it is.
   - Same doc names a standing defect: obligation is per loan but recorded
     return-wide.
   - **In-repo precedent:** SSA-1099 has `tax.us.2025.ssa1099.recipient`
     ∈ {taxpayer, spouse}, admitted only on an MFJ return
     (`packages/tax/ssa_benefits.py`). So "which spouse" has been represented
     once, as a per-statement categorical plus a filing-status guard.
   - Phase state: no tax case is proposed; the phase is closing.
     A joint-return question would be new scope for the foreman/owner.

2. **What the law says for MFJ with two 1098-Es (developed — snapshot 2).**
   Sources: 26 U.S.C. § 221; 26 CFR § 1.221-1; Pub. 970 (2025), ch. 4.
   Settled enough to rely on:
   - **One limit, one phase-out, per return.** § 221(b)(1) caps "the
     deduction … for the taxable year" at $2,500; a joint return is one
     taxable year's computation, and § 221(b)(2) gives joint-return
     thresholds (indexed: $170,000–$200,000 for 2025, Pub. 970). Two
     1098-Es do not double the cap. The worksheet's sum-then-cap shape is
     therefore right for MFJ.
   - **Married → must file jointly** (§ 221(e)(2); § 1.221-1(b)(3)). The
     MFS block already encodes this.
   - **Dependency is per individual** (§ 221(c); § 1.221-1(b)(2)). Pub. 970
     phrases it "you (or your spouse if filing jointly)". On a joint return
     the existing single "not claimed as a dependent" answer must cover
     **both** spouses.
   - **Qualification includes a spouse's education** (§ 221(d)(1)(A)), so a
     loan for either spouse's schooling qualifies on the joint return.
   Not settled — needs a named source or an advisor read, not inference:
   - 2a. **Legal obligation across spouses.** § 1.221-1(b)(1) requires "the
     taxpayer" to be obligated. On a joint return, does interest count when
     spouse A paid it on a loan only spouse B is obligated on? Plausibly yes
     (joint filers combine; § 1.221-1(b)(4) deemed payment may also reach
     it) but no source read so far says so directly.
   - 2b. **"Spouse" timing.** Does "as of the time the indebtedness was
     incurred" bind only "dependent" or also "spouse"? Matters for a loan
     one spouse took for the other's schooling before they married. Read
     § 1.221-1(e)(3) and examples.
   - 2c. Whether "per return" wording appears verbatim in Pub. 970 or the
     1040 instructions (fetches returned summaries, not exact text).
   Consequence for the plan: arithmetic needs nothing new for MFJ. The
   question is entirely about **which person each answer is about**.
3. **Who each answer is about on a joint return (developed — snapshot 3).**
   | Input (keying) | Law on MFJ | Today | Gap |
   | --- | --- | --- | --- |
   | Filing status (return) | return | return | none |
   | 1098-E box 1/2 (statement) | summed per return | summed | none for amounts; no "whose" |
   | Loan-cost, enrollment, financing, inclusion (borrowing/statement) | per loan; "the student" may be either spouse | per borrowing | none found |
   | Five per-statement witnesses, e.g. related-person (statement) | related-person is a relation between *the taxpayer* and the creditor: either spouse on MFJ? | per statement, worded "the filer" | wording; law point → 2d |
   | `legally-obligated-for-interest` (return) | per person **per loan** (§ 1.221-1(b)(1)) | one yes/no for "the filer"; read by worksheet v5 | **real**: see below |
   | `not-claimed-as-dependent` (return) | each spouse (§ 221(c)); but a joint filer generally cannot be anyone's dependent (§ 152(b)(2), refund-only exception) | one yes/no for "the filer" | wording, and an almost-always-yes question → 2e |
   | Scope: Form 2555/4563, PR/Samoa (return) | Pub. 970 route if either spouse files them | return-wide | wording only ("you or your spouse") |
   | Support-rule basis (`rule.sli-statement-loan-support.json`, "assumed") | "indebtedness the taxpayer incurred"; "schooling for the taxpayer, a spouse, or a dependent" | assumed for the single filer | reading on MFJ depends on 2a/2b |

   **The concrete failure.** On a joint return the single obligation answer
   cannot say "I'm obligated on Cedar; my spouse is obligated on Birch".
   Answered from one spouse's view, "no" sends the whole return to $0 (the
   description calls it "a definite $0 for this return") although the other
   spouse's loan qualifies. **Observed (snapshot 4):** the probe with
   `legally-obligated-for-interest=no` on MFJ publishes line 21 = **0**,
   with no reason text. The project's correctness claims are framed as
   "fails closed; never publishes a *favourable* value it should not"
   (`account-refinement.md`). That framing does not cover a confident
   *unfavourable* zero. That is an under-claim with a correct-looking
   result. Answered "yes" for both, it is right. It also matches the
   standing defect from snapshot 1 (obligation is per loan, recorded
   return-wide); the joint case makes it reachable by an ordinary person.
   **Mitigating evidence:** a 1098-E is furnished to the borrower, so a
   statement in either spouse's name is itself strong evidence that that
   spouse is obligated on that loan. Whether the team may rely on that is
   a question about grounds (assumed vs. said), not arithmetic.

   New legal sub-questions: 2d related-person test on MFJ (either spouse's
   relatives?); 2e whether the dependency question should be asked of a
   joint filer at all.
5. **Candidate approaches and what separates them (developed — snapshot 4).**
   Listed for comparison. None is selected.
   - **A. Keep the return-level answer; make the joint meaning explicit.**
     On MFJ the obligation (and dependency, scope) questions read "you or
     your spouse", and "the filer" in the assumed basis means either
     spouse. No new identity and no new keying. It is correct **only if**
     the law treats the joint filers as one taxpayer for the obligation
     test (2a). It still cannot express "obligated on one loan, not the
     other", but on MFJ that case may not arise if either spouse's
     obligation suffices. Cost: changes the content of published fact
     types (descriptions sit in adopted bundles), so likely a
     successor-version bundle rather than an edit.
   - **B. Ask obligation per loan, still from the filer's side.** Move
     `legally-obligated` onto the borrowing (or statement) using the
     per-subject machinery of ADR-0076/0077, with "you or your spouse" on
     MFJ. This fixes the standing per-loan defect (snapshot 1) for every
     filing status, not only joint. Still no person identity, so it stays
     inside the owner's filer-centred direction. Cost: new fact type and
     rule versions, a worksheet successor, and correction-page and
     saved-account consequences.
   - **C. Record whose statement it is.** Add a per-statement recipient
     ∈ {taxpayer, spouse} with an MFJ guard (the SSA-1099 precedent), and
     ask obligation and dependency per spouse. This is the only option
     that can show "your spouse's 1098-E" and attribute a "no" to one
     person. It introduces a second person, which the owner's 2026-09-22
     direction reserves for "a concrete supported case [that]
     demonstrates that identity is necessary". The team would have to
     show that A/B cannot be honest first.
   - **D. Interim honesty only.** On MFJ with more than one 1098-E (or
     whenever the obligation answer is "no" on MFJ), block with a sentence
     instead of publishing 0, until A/B/C is decided. This does not handle
     the case. It stops the silent under-claim.
   **What would distinguish them:**
   - 2a (obligation across spouses). If either spouse's obligation
     suffices on a joint return, then A or B is honest and C buys
     presentation, not correctness. If the paying or obligated spouse
     matters per loan, B is the minimum and C may be needed.
   - 2b (spouse-at-origination). If it bites, the deciding fact is
     "whose schooling, married when", which is per borrowing. That favours
     B's keying, not C's.
   - Whether any concrete MFJ case gives a wrong number under B. That is
     the necessity test the owner's direction requires before C.
   - A reader check: does a joint filer understand "you or your spouse" in
     one question, or do they answer for themselves (the failure that
     produces the 0)? A and B depend on this. C sidesteps it.
   - Cost and coupling: the account-refinement retrospective's parked
     "shared-answer no reaching the whole return" is the same shape. Any
     choice here should be consistent with how that is resolved.
6. **What is still unknown, and how to find it out (developed — snapshot 5).**
   Status of the legal sub-questions after a second pass at primary and
   IRS sources:
   - **2c — resolved enough.** The IRS (Topic 456, 2025): deduct "the
     lesser of $2,500 or the amount of interest you actually paid"; the
     MFJ phase-out is given as one combined range (Pub. 970). Secondary
     sources say outright that two spouses get $2,500, not $5,000. The
     live probe matches. No further work.
   - **2e — resolved; changes wording, not shape.** Topic 456 and Pub. 970:
     "neither you nor your spouse, if filing jointly, were claimed as
     dependents". So on MFJ the existing return-level answer must be posed
     about both spouses. Keying it per person is not required, because one
     "no" for either spouse denies the whole joint return, which a single
     return-level fact can carry. § 152(b)(2) makes "no" rare for joint
     filers, but the IRS still asks, so the team should keep the question.
   - **2a — NOT resolved; this is the deciding question.** § 1.221-1(b)(1)
     and Topic 456 say "you're legally obligated" with **no** "or your
     spouse" extension, while the same list *does* extend the dependency
     test to the spouse. That asymmetry may mean nothing (on a joint return
     "you" is both filers) or it may be deliberate. No primary source read
     says that interest paid by spouse A on a loan only spouse B owes
     counts on the joint return. § 1.221-1(b)(4)'s deemed-payment rule
     would cover B's own loan however it was paid, if B is the obligated
     "taxpayer". Secondary sources read for this point (Illinois Tax School,
     the search results) do not address it.
     *How to settle:* an advisor consultation (the project routes
     doctrine to the advisor seat; builders may not interpret governance),
     against § 6013 joint-return principles, § 1.221-1(b), and any
     rulings or court cases on joint filers and § 221/§ 163 obligation.
     Mortgage-interest obligation on joint returns is a likely analogue to
     search.
   - **2b — narrowed, still ambiguous.** The regulation's wording ("a student
     who is the taxpayer, the taxpayer's spouse, or a dependent … *at the
     time the taxpayer incurs the indebtedness*") can read the timing onto
     "spouse". Pub. 970 ("a person who was your dependent when you took out
     the loan") puts it on dependent only. It matters only for a loan one
     person took for the other's schooling before they married. It is a
     per-borrowing condition currently in the "assumed" basis, so it does
     not decide the joint-return representation. Name it as a bounded
     assumption to keep visible. Settle it with the advisor if 2a goes there.
   - **2d — resolved in kind.** § 1.221-1(e)(3)(iii) tests relatedness
     against "the taxpayer" under § 267(b). § 267(c)(4) family includes
     ancestors and siblings, not in-laws. A loan from B's parent to A is
     not related to A but would be to B. So the related-person witness has
     to be answered **relative to the obligated spouse**. This is the same
     per-loan-per-obligor dimension as 2a. It adds evidence that the
     obligor on each loan is the latent variable, whichever approach is
     chosen.
   **Other unknowns, and how to find them out:**
   - 6a. **Revised (snapshot 6).** No page asks the obligation, dependency
     or scope questions. They appear only as seeded assertions in sample
     data and test fixtures (`packages/sample_data/sli_correction_t1/…`,
     `tests/…track6._f1098e_acts`). `presentation_projection.py` has no
     sentence for them, which is why the observed 0 carries no reason.
     So there is no current wording to reader-test. Whatever approach is
     chosen, the team is **designing these questions for the first time**,
     and a reader assessment belongs with the drafted wording, after
     selection. It is not a precondition for selection. What *is* a
     precondition: agree that a joint-return 0 caused by the obligation
     answer must be explained, not silent (it bears on D).
   - 6b. **Resolved (snapshot 6).** Core calculations v42 pins
     `tax.us.2025.sli-scope.vocabulary` by id and version, and workspaces
     adopt bundles by content (`bundle-adoption` acts). So even A's
     rewording is a bundle successor plus a package successor, not an
     edit. A is cheaper than B only by the per-subject keying. B has
     in-repo machinery (ADR-0076/0077 per-subject rules, shared-key counts)
     and a precedent for fact-type succession
     (`fact-type-succession-neutral-schedule1`). Cost does not separate
     the candidates much.
   - 6c. Who owns the parked "shared-answer no reaching the whole return"
     item. That is a foreman/owner question, not research.
7. **Readiness claim (developed — snapshot 7).**

   **Claim: not yet ready to select an approach. Ready to narrow the
   choice to two candidates and to start one bounded step now. Selection
   waits on one legal determination and one scope decision.**

   *What the team understands well enough to rely on:*
   - The arithmetic is not in question. One $2,500 cap and one combined
     MAGI phase-out per joint return (§ 221(b); Pub. 970; Topic 456), and
     the live run already produces it: MFJ $1,500 + $1,800 → 2,500, and at
     $185k → 1,250 (snapshot 3 probe). Nothing about amounts, statements,
     the worksheet or the 1098-E keying needs to change.
   - The dependency and scope conditions are return-level on a joint
     return, posed about both spouses (Topic 456; Pub. 970). That is a
     wording matter for questions no page asks yet (snapshot 6).
   - The one input that can give a wrong number is the return-level
     legal-obligation answer. A "no" given from one spouse's perspective
     publishes a silent line 21 = 0 (snapshot 4 probe).
   - The latent variable is **which spouse owes each loan**. Both the
     obligation test (§ 1.221-1(b)(1)) and the related-person test
     (§ 1.221-1(e)(3)(iii) with § 267) are evaluated against the obligated
     taxpayer (snapshot 5).
   - Recording a second person (C) is not shown to be necessary. Every
     condition found so far can be posed from the filers' side, so the
     owner's filer-centred direction (2026-09-22) is not yet challenged.
     C stays available only if 2a requires it.

   *What must be established before selecting:*
   1. **2a, by advisor consultation.** The question: "On a married-filing-
      jointly return, is interest on a qualified education loan
      deductible when only one spouse is legally obligated on that loan,
      including when the other spouse made the payment? Does § 1.221-1(b)(1)'s
      'taxpayer' mean either joint filer?" Outcomes map to candidates:
      either spouse suffices → A or B; the obligated spouse must be the
      payer, or be identified → B at minimum, possibly C.
   2. **The A/B scope decision, by owner/foreman.** B also repairs the
      standing per-loan obligation defect for single filers
      (`whose-deduction-model.md`), and it overlaps the parked
      "shared-answer no reaching the whole return" item
      (account-refinement retrospective). Whether the joint-return work
      absorbs those is a scope call, not something the evidence decides.
   3. **The owner accepts or rejects one constraint:** a joint-return zero
      produced by the obligation answer must be explained, not silent.

   *Can start now, whatever the selection:* a characterization test
   pinning today's MFJ behaviour (2,500 / 1,250 / silent 0), so any
   approach is measured against it. The interim block (D), if the owner
   wants protection before selection.

   *Deliberately left as named assumptions:* 2b (spouse-at-origination
   timing, per borrowing, already in the "assumed" basis); the related-person
   wording relative to the obligated spouse.
