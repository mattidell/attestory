# Plan: joint return where both spouses have Form 1098-E interest (TY2025)

Goal: decide whether the team understands enough to select an approach for
handling a married-filing-jointly return on which each spouse has student-loan
interest reported on their own 1098-E — and if not, what must be established first.
No representation is selected and nothing is implemented here.

## Actions

1. **Establish current behavior (done, snapshot 1).** What the app does today:
   - A 1098-E is identified by `lender` + `statement` + `tax-year` only
     (`f1098e.bundle.json`). There is **no borrower/recipient** key or fact;
     the statement does not say whose it is.
   - Line 21 is computed by `rule.sli-worksheet.v5`: line-1 subtotal across all
     statements → $2,500 cap (per return) → MAGI phase-out keyed on
     `filing_status` (MFJ: $170k / $30k range, already in parameters) → block on MFS
     (`SLI_MFS_INELIGIBLE`).
   - Return-level answers (`sli-scope.*`: legally-obligated-for-interest,
     not-claimed-as-dependent, no-2555/4563/PR) are keyed by `tax-year` only — one
     answer per return, not per spouse.
   - Per-borrowing answers (financing, loan-paid-only-school-costs,
     enrolled-at-least-half-time, statement-inclusion) are keyed by borrowing /
     schooling situation; nothing names whose borrowing or which student.
   - Coverage frontier row (line 50) retires the "single statement, fully
     eligible" class; MFS excluded. Nothing claims or refuses MFJ-with-two-borrowers.
2. **Establish current spouse/filing-status handling (done, snapshot 1).**
   - `filing_status` is a return-level asserted fact, MFJ accepted by the worksheet.
   - Precedent: SSA-1099 carries a per-statement `tax.us.2025.ssa1099.recipient`
     fact (`taxpayer|spouse`), guarded so `spouse` is admitted only on MFJ
     (`packages/tax/ssa_benefits.py`). This is the only spouse-aware pattern found.
   - Implication: today an MFJ return with two 1098-Es (one per spouse) would
     probably compute — two statements summed, one cap — with the return-level
     answers silently standing for both spouses. Whether that is *right* is the
     question; to be confirmed by running a synthetic case (action 4).
3. **Establish the 2025 rules for a joint return (done, snapshot 2).** Findings,
   each tagged with how it bears on the app:
   - **One cap, one worksheet per return.** Worksheet line 1 "total interest you
     paid … Don't enter more than $2,500"; Reg. §1.221-1(c) "may not exceed $2,500"
     for any taxable year. No source grants $2,500 per spouse. *(Inference: a joint
     return is one computation; spouses with $2,000 + $2,000 get $2,500. The app's
     sum-then-cap already does this.)*
   - **Joint MAGI thresholds** $170,000 / $30,000 (instructions line 5/7; Pub. 970
     Table 4-2). *Already in parameters.*
   - **MFS bar**: Reg. §1.221-1(b)(3). *Already blocks.*
   - **Dependency bar covers both spouses**: 1040 instructions: "You, or your
     spouse if filing jointly, aren't claimed as a dependent on someone else's …
     return." *App has one return-level answer; whether its wording asks about
     both spouses is unverified.*
   - **Legal obligation is per loan and per obligor**: Reg. §1.221-1(b)(1) "the
     taxpayer has a legal obligation … under the terms of the qualified education
     loan"; Pub. 970 "You are legally obligated to pay interest on a qualified
     student loan". On a joint return either spouse may be the obligor of a given
     loan. *The app asks one return-level yes/no, which can't say "this loan is my
     spouse's obligation, that one is mine". It's ambiguous even for a single filer
     with several loans, and more pressing for MFJ.*
   - **Student may be "you, your spouse, or your dependent"**, tested as of the
     time the *borrower* took the loan for at least the dependent relationship
     (Reg. §1.221-1(e)(3)(i)(A); Pub. 970). Whether that timing also reaches
     "spouse" is open (D5). On a joint
     return the "you" is whichever spouse borrowed, so a spouse's pre-marriage loan
     for their own schooling qualifies. *The app's enrollment answer says "the
     student" without naming who. Unknown whether that matters for computation.*
   - **Related-person loans excluded, and a spouse is a related person** (Pub. 970).
     *A loan from one spouse to the other is not qualified. Exotic for 1098-E
     lenders; note only.*
   - **1098-E goes "to each borrower"** (Pub. 970), so on MFJ each spouse typically
     receives their own. Joint borrowers (e.g. legacy spousal consolidation loans)
     may produce one statement covering both. The form names the borrower, which the
     app does not capture.
   - Not found: any 2025 rule that makes the computation itself differ per spouse.
     Every per-spouse distinction is in *eligibility attribution*, not arithmetic.
4. **Probe the current app (done, snapshot 3).** Scratch probe `temp/probe_mfj.py`
   (ignored) reuses Track 5's synthetic return through `run_live`, the production
   live path, with core v41. Two statements: Cedar $2,000 (autumn borrowing),
   Birch $1,500 (spring borrowing), standing for "one per spouse". All answers yes.
   | filing status | total income | line 21 |
   | --- | --- | --- |
   | MFJ | 50,000 | **2,500** published (sum 3,500, capped once) |
   | MFJ | 180,000 | **1,668** published (joint phase-out, same ratio as single at 90,000) |
   | single | 90,000 | 1,668 published |
   | MFS | 50,000 | blocked `SLI_MFS_INELIGIBLE` |
   - **Conclusion:** an MFJ return with both spouses' 1098-Es **already computes
     a correct figure when every answer is truthfully "yes" for the household**.
     Nothing refuses it. Nothing in the result says whose statement is whose.
   - **Where it can go wrong** (rule logic read from `rule.sli-worksheet.v5`, plus
     fact titles in `sli-scope.bundle.json`):
     a. `legally-obligated-for-interest` is "the filer … on the loan(s) claimed",
        one answer per return. A "no" is a *return-level legal zero*: it zeroes
        both spouses' interest. A person whose spouse is the obligor on one loan
        has no truthful single answer. Real risk of a wrong $0, or of a "yes"
        that glosses a loan neither spouse is obligated on.
     b. `not-claimed-as-dependent` is "the filer". The law says "you, or your spouse
        if filing jointly". *(Mitigation, from general law and not verified in a
        source here: a person filing a joint return generally cannot be claimed
        as a dependent unless the return is only a refund claim, so this mostly
        matters for wording and explanation, not the amount.)*
     c. Per-borrowing answers (enrolled half-time, paid only school costs) say "the
        student" without naming them. Nothing asks whether the student was the
        borrower, the borrower's spouse, or the borrower's dependent at the time.
        This is also true for single filers today. MFJ adds a second borrower.
   - No person-facing question text exists for the scope answers. They are
     asserted facts shown as pins (`below-floor.presentation-model.v1.json`), so
     "wording" here means fact-type meaning plus explanation text.
   - Not probed: explanation/presentation page rendering for MFJ (the projection
     reads filing status into parameter keys; MFJ keys exist).
5. **Lay out the joint-return cases and the decisions they force (developed,
   snapshot 4).**

   *Prior project positions that bind the framing*
   (`docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/`):
   - P1. **Owner direction 2026-09-22, "filer-centered"** (`whose-deduction-model.md`):
     "No other payer's identity is represented unless a concrete supported case
     demonstrates that identity is necessary." It was written for co-signers and
     third-party payers, not spouses. Whether a joint-return spouse is an "other"
     person or part of "the filer" is **not addressed** there.
   - P2. **Scope bound "the filer as the student"** (`a5-stage2…keying.md`): "a
     spouse's or a dependent's education … are **not represented here**, which is a
     scope bound." The MFJ case runs straight into this bound.
   - P3. **Return-level legal obligation is a named defect** (`whose-deduction-model.md`,
     "Where the incumbent applies a loan-level condition return-wide"). Stage 3 selected
     a borrowing key for a *new* consumer (`a5-stage3`, `a5-stage4` "No consumer in this
     milestone"). The worksheet still reads the tax-year-keyed incumbent (snapshot 3).
   - P4. **Owner-stated facts** (`owner-stated-facts.md`): the box-1 route is a
     legitimate route to total interest. The app must not require the person to know
     tax-domain things such as lender eligibility.

   *Cases* (✓ = current app is right, ? = right only under an unstated reading,
   ✗ = cannot be represented)
   | # | Case | Today |
   | --- | --- | --- |
   | C1 | Each spouse borrowed for own schooling, own 1098-E, each obligated on own | ? computes right if "filer" read as "either spouse" (P2 bound exceeded) |
   | C2 | One spouse's loan paid for the other spouse's schooling | ? qualifies in law; enrollment asked of "the student" |
   | C3a | Before marriage, spouse A borrowed for **A's own** schooling | ? student is "the taxpayer" at origination, so the marriage date seems irrelevant. But on a joint return, whether A counts as "the taxpayer" is D1, so this is not ✓ |
| C3b | Before marriage, A borrowed for **B's** schooling (B later A's spouse, not A's dependent then) | **unresolved — which time test governs is not established** (see D5) |
   | C4 | Combined interest > $2,500 | ✓ capped once (probe) |
   | C5 | Joint MAGI in phase-out | ✓ (probe) |
   | C6 | One statement covers a loan both spouses owe | ✓ Reg. §1.6050S-3(b)(2): with multiple borrowers, only the **principal borrower** is the payor, so one 1098-E. Both spouses' interest is on one joint return, so no split arises *(inference; see C7)* |
   | C7 | Both spouses receive a 1098-E for the **same** loan's interest | ✓ not the required pattern: §1.6050S-3(b)(2) names one payor per loan. Residual risk is a non-conforming lender, or the same statement entered twice (an existing identity question, not MFJ-specific). The inverse matters more: the 1098-E names only the principal borrower, so the **named person need not be the obligor who paid**. That bears on any per-person attribution read off the form (D2) |
   | C8 | Spouse A obligated on loan X; a statement for loan Y neither spouse is obligated on | ✗ one return-level answer (P3) |
   | C9 | Either spouse claimed as someone's dependent | ? §152(b)(2): an individual who "has made a joint return with the individual's spouse" is not treated as a dependent. On a true MFJ return the bar should not bite for either spouse. The refund-only joint-return exception comes from IRS guidance I did **not** verify here. The amount is very likely right. The answer's meaning ("the filer") is still a wording gap |
   | C10 | Loan for a child who was one spouse's dependent at origination | ✗ out of scope already for single filers (dependency-at-origination not asked) |
   | C11 | Explanation of line 21 | ? statements named by lender only; no "yours / your spouse's" |

   *Verification results (snapshot 6)*
   - **P3 confirmed unbuilt**: the only obligation fact in 2025 content is
     `sli-scope.legally-obligated-for-interest` (tax-year key).
     `obligation-acquisition.bundle.json` is the unrelated document-translation
     vocabulary. C8 is a live, pre-existing defect, and MFJ makes it more reachable
     because there are two obligors.
   - **D5 not decided by any authority found.** Searched for statute, reg, Pub. 970 and
     secondary sources (The Tax Adviser, Mar. 2008, which restates the statute only). A
     search-engine summary *asserted* a reading; I discard it as not authority. Still
     open; C3b is narrow (a pre-marriage loan for the future spouse's schooling).

   *Decisions the team must make* (none taken here)
   - D1. **What "the filer" means on a joint return** for the existing filer-level
     answers (dependency, obligation, the student). Is it the couple, the primary
     taxpayer, or each spouse? This reinterprets P1/P2 and is the **owner's** call.
   - D2. **Does the return need to know whose each statement/borrowing is?**
     Options (to compare, not choose): (a) no attribution; reword answers to "you or
     your spouse"; (b) per-statement taxpayer|spouse fact on the SSA-1099 recipient
     precedent; (c) per-borrowing obligor/student attribution; (d) refuse MFJ with any
     1098-E until decided. P1's test is "a concrete supported case demonstrates
     identity is necessary": is C7 or C8 such a case, or only C11 (explanation)?
   - D3. **Order relative to P3**: must the per-borrowing obligation fix land
     before MFJ is claimed, or is MFJ independent of it?
   - D5. **Which time test governs the student relationship (C3b).** Two different
     tests had been run together in C3 (corrected in snapshot 5):
     - *Year-end marital status* (§221(e)(2)–(3), §7703; Reg. §1.221-1(b)(3)) governs
       **only** whether the couple must file jointly to claim. It says nothing about
       whether a loan qualifies.
     - *Loan qualification* (§221(d)(1)(A)) asks whether the expenses were "incurred on
       behalf of the taxpayer, the taxpayer's spouse, or any dependent of the taxpayer
       as of the time the indebtedness was incurred". The reg (§1.221-1(e)(3)(i)(A)) says "a
       student who is the taxpayer, the taxpayer's spouse, or a dependent … at the time
       the taxpayer incurs the indebtedness". Pub. 970 says "For you, your spouse, or a
       person who was **your dependent … when you took out the loan**".
     - The open reading: does the origination-time clause reach "spouse", or only
       "dependent"? The reg's placement reads most naturally as reaching all three. The
       statute's wording is ambiguous. Pub. 970 attaches the time only to the
       dependent. If it reaches spouse, C3b is **not** qualified. If not, C3b
       qualifies on a joint return. I have not found an authority that decides it,
       and Pub. 970 is explanatory, not controlling (the project's own
       `whose-deduction-model.md` takes the same stance). **To establish:** look for a
       preamble to T.D. 9125, a ruling, case law or an IRS FAQ. If none, this is an
       authority question to escalate, not one for the team to pick.
   - D4. **Coverage claim**: what the frontier/maturity matrix says about MFJ with
     1098-E. Today it is silent while the app computes.
6. **Map each decision to what settles it, who settles it, and in what order
   (developed, snapshot 7).**

   *New facts from two more probes (`temp/probe_mfj2.py`, MFJ, Cedar $2,000 + Birch
   $1,500, total income 50,000)*
   - **C8 demonstrated**: with `legally-obligated-for-interest = no`, line 21 is
     `computed_zero`, so both spouses' interest is wiped by one return-level answer.
   - **Rendered line-21 page** publishes 2,500 and names statements by lender. No text
     distinguishes the spouses. The only spouse wording comes from the **declared
     basis** of `rule.sli-statement-loan-support` (ADR-0077 groups), which ships these
     as *assumed*: "The schooling was for the taxpayer, a spouse, or a dependent when
     the loan was incurred." and "The named borrowing is indebtedness the taxpayer
     incurred."
     - So the app **already declares** the student relationship and the borrower as
       assumptions it does not test, and counts each statement's box 1 under them.
       **D5 is result-bearing** (corrected in snapshot 8). If the timing clause reaches
       "spouse", the assumption is false for C3b, the loan is not qualified, and the
       app still counts its interest, so line 21 is **overstated**. If it does not,
       the result is right and only the assumption's wording is too strict. Declaring
       an assumption makes a possible error visible to the reader. It does not make
       the result right. Nothing the app asks distinguishes C3b (marriage date vs.
       origination date is not asked).
     - On MFJ, "the taxpayer" in those sentences is exactly D1's ambiguity, now
       visible to the person.
     - The assumed-basis mechanism is itself a candidate for D2: state the joint
       reading as an assumption rather than represent identity. Still not selected.

   | Decision | Kind | What settles it | Who | Depends on |
   | --- | --- | --- | --- | --- |
   | D1 "filer" on a joint return | meaning / product | Owner decision on a short brief: cases C1, C2, C8, C11; the two readings (couple vs. taxpayer-only); the current shipped assumption wording; P1/P2 as they stand. If "filer"/"person" is a governance-defined term, the team **stops and escalates** (AGENTS.md); I did not read `docs/governance/` | Owner (advisor if governance) | — |
   | D5 timing for "spouse" | authority | Read the T.D. 9125 preamble (69 FR 25489, 2004) and the 1999 proposed-rule preamble; check IRS FAQs. If still silent, escalate. Until settled, under the reg's reading the app **overstates C3b and cannot detect it**. Options to put to the owner: bound C3b out (ask, or refuse when it applies), or accept it as a declared limitation | Team searches; owner disposes | — |
   | D3 order vs. P3 | sequencing | Owner choice between (i) fix obligation per borrowing first (stage-3 design exists, no consumer), (ii) admit MFJ with C8 declared as a known limitation, (iii) hold MFJ. Evidence in hand: the C8 probe | Owner, on foreman recommendation | D1 |
   | D2 whose each statement/borrowing is | representation | Only if D1 says identity matters: rival prototypes (milestone loop stage 2) comparing assumed-basis wording, per-borrowing "you or your spouse" obligation (no second identity), and per-person attribution. Snapshot 6 shows that form-named attribution (SSA-style) records the principal borrower, not the obligor | Builders (rival), reviewer, owner | D1, D3 |
   | D4 coverage claim | documentation | Record today's de facto behavior (MFJ computes; limits C8, C10, C3b) in the coverage frontier whatever else is chosen | Foreman | D1–D3 for the final wording |

   Order: D1 and D5 in parallel (neither needs engineering), then D3, then D2 if it
   is still needed, then D4.

7. **Readiness claim (snapshot 8).**

   **Not ready to select an approach.** The team understands the *mechanics* well
   enough. What it does not yet have is answers to two meaning/authority questions
   that decide what a correct result *is*, plus a sequencing choice that only the
   owner can make. Selecting a representation now would be choosing those answers
   implicitly. That is the error this plan made twice in miniature (C3 in snapshot 5,
   D5's reclassification in snapshot 8).

   *What supports the parts that are understood*
   - Current behavior **measured** on the production live path (`run_live`, core v41),
     not inferred. MFJ with one 1098-E per spouse publishes the right figure when all
     answers are "yes" (2,500 capped once; 1,668 in the joint phase-out). MFS blocks.
   - Joint-return arithmetic matches the 2025 sources: worksheet line 1 cap,
     $170k/$30k joint parameters, §221(e)(2) MFS bar (1040 instructions; Pub. 970 ch. 4;
     26 CFR §1.221-1(b)(3), (c)).
   - Reporting: one 1098-E per loan, naming the principal borrower
     (§1.6050S-3(b)(2)). So a 1098-E does not identify the obligor or payer, and
     per-person attribution read off the form would record the wrong thing.
   - Dependency bar is very likely moot on a genuine joint return (§152(b)(2)).
   - Existing project positions that frame every option: P1 (filer-centered, owner
     2026-09-22), P2 (filer-as-student bound), P3 (per-borrowing obligation designed,
     unbuilt), and the shipped assumed-basis sentences.

   *What must be established first, in order*
   1. **D1, owner:** what "the filer"/"the taxpayer" means on a joint return for the
      filer-level answers and the shipped assumption sentences. Escalate to an advisor
      if it turns on governance-defined terms.
   2. **D5, authority:** whether §221(d)(1)(A)'s origination-time clause reaches
      "spouse". Result-bearing for C3b (possible overstatement the app cannot detect).
      Search the T.D. 9125 and proposed-rule preambles and IRS guidance; if still
      silent, the owner disposes (bound C3b out, or declare it as a limitation).
   3. **D3, owner, on a foreman recommendation:** fix obligation per borrowing (P3)
      before claiming MFJ, admit MFJ with C8 declared, or hold MFJ. C8's wrong-zero is
      demonstrated.
   4. Only then **D2** (representation), by rival prototypes if D1 says identity
      matters, and **D4** (coverage wording).

   *Surface now, independent of selection:* the app **already computes** MFJ
   two-spouse returns silently, with a demonstrated wrong-zero (C8), a possible
   undetectable overstatement (C3b, pending D5), and C10 out of scope. The coverage
   frontier says none of this. This is a finding for the owner, not a change made here.
