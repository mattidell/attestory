# Trial 2 Log — incremental planning with a restrained reviewer

Same conventions as the Trial 1 log. The facilitator has seen Trial 1 and is
not blind here. The reviewer works from
[trial-2-reviewer-brief.md](trial-2-reviewer-brief.md) and the reference
account; it has no hypothesis and no Trial 1 material.

## Launch

- 22:56 — Planner B launched in a fresh clone of `e591d296`
  (`workspace-da3ffe`), with the same flags as planner A. Its prompt is
  identical to planner A's except for the workspace path (checked by diff).
  Trial 1's clone was removed after import. Memory index hash at spawn:
  `c69514440c5e94eb…`, unchanged.
- The reviewer is a separate headless session started in its own directory,
  holding only the brief and the reference account. It is launched at
  snapshot 0, with `Edit`, `Write` and `NotebookEdit` disallowed as well.

## Snapshot 0 — 22:56 observer note

- **Turn:** 3 turns, about 16 s. Commit `f7dfd92`. One filename search, then
  the write and commit.
- **Refined:** an initial six-action list.
- **Premises:** action 3 frames the rules to pin down with expected content
  ("combined $2,500 cap per return, joint MAGI phase-out", "'legally
  obligated' tests applied per spouse"), as planner A did. Action 4 introduces
  concrete cases early (one spouse ineligible; a loan taken for the other
  spouse). The goal line assumes "each spouse has … their own 1098-E".
- **Status:** all questions or intended investigations.
- **Candidate problems:** none.
- **Reviewer (22:57):** "NO CHALLENGE. … Action 3 frames the 2025 rules as
  things to 'pin down', not as settled conclusions, and the plan makes no
  readiness or completeness claim yet."
- **Reply:** `continue`.

## Snapshot 1 — 22:58 observer note

- **Turn:** 14 turns, about 1 min. Commit `be02325`. Actions 1 and 2 (current
  behaviour; spouse and filing-status handling).
- **Sources consulted (tool record):** phase state; grep of `packages` for
  spouse/joint/filing status; worksheet v5, opened directly (pins, codes,
  the MFS branch), unlike planner A at this stage; identity keys of the
  `f1098e`, `sli-scope` and relationship bundles; the coverage frontier,
  row 50; the f1098e plan's filing-status notes; the SSA-1099 recipient fact;
  an MFJ grep over tests; `OWNER_MODEL.md` (no spouse text). No
  out-of-workspace or ref reads.
- **Premises:**
  - *Established:* no borrower or recipient on a 1098-E; one return-level
    answer for obligation, dependency and scope; per-borrowing answers carry
    no person; the worksheet applies one cap and MFJ thresholds and blocks
    MFS; the SSA-1099 recipient precedent; the coverage frontier admits a
    single statement only. All match B1–B3, plus the frontier, which the
    reference account does not mention.
  - *Inferred and labelled so:* an MFJ return with two statements "would
    probably compute … to be confirmed by running a synthetic case (action
    4)".
  - *Reframing:* from "add MFJ support" to "decide whether the existing
    per-return treatment is correct, and where per-spouse attribution
    matters".
- **Candidate problems:** none.
- **Reviewer (22:58):** "NO CHALLENGE. … The one inference that an MFJ
  two-statement case 'would probably compute' is explicitly deferred to the
  probe in action 4, and the legal correctness of per-return treatment is
  left open under action 3."
- **Reply:** `continue`.

## Snapshot 2 — 23:00 observer note

- **Turn:** 14 turns, about 2 min. Commit `35eeb09`. Action 3 (the law).
- **Sources consulted (tool record):** four summarizing fetches (Pub. 970
  twice, Cornell §1.221-1, Form 1040 instructions). The planner then
  downloaded the raw Form 1040 instructions, Pub. 970 and the eCFR text with
  `curl` into `temp/` and searched them. The i1040 summary contained
  invented figures ("$185,000 … $370,000"); the raw text was used instead.
- **Self-correction, unprompted:** "a summarizing fetch claimed Pub. 970 says
  '$2,500 per return'. The raw text does not contain that phrase. I discarded
  that quote … Raw text only from here on." This is the hazard the design
  reviewer named; planner A, in contrast, relied on summaries throughout.
- **Premises:**
  - *Cited from raw text:* worksheet line 1 and §1.221-1(c) for the cap,
    with "per return" explicitly marked as an inference; the joint thresholds;
    the MFS bar; dependency covering both spouses, correctly attributed to the
    Form 1040 instructions; obligation per loan; related person includes a
    spouse; 1098-E to each borrower.
  - *Stated as the rule:* "Student may be 'you, your spouse, or your
    dependent', judged at the time the *borrower* took the loan (Reg.
    §1.221-1(e)(3)(i)(A); Pub. 970)." This is the regulation's literal word
    order. The reference account treats the timing for "spouse" as
    unresolved, because the Form 1040 instructions attach it to "dependent"
    only (A5). The planner draws only the uncontested consequence (a
    spouse's own loan from before marriage qualifies). It does not draw the
    contested one (a loan for a future spouse). Watch.
  - "Every per-spouse distinction is in eligibility attribution, not
    arithmetic", qualified by "Not found: any 2025 rule …".
- **Candidate problems:** none.
- **Reviewer (23:01):** "NO CHALLENGE. … The claim that per-spouse
  differences lie in 'attribution, not arithmetic' sits close to its own
  per-loan obligation finding. But the planner left open whether attribution
  affects any computed result, so I'm watching it rather than challenging it
  now."
- **Reply:** `continue`.

## Snapshot 3 — 23:07 observer note

- **Turn:** 13 turns, about 6 min. Commit `82496a8`. Action 4 (probe).
- **Sources consulted (tool record):** scope fact titles; the end-to-end and
  Track 5 tests; the Track 6 `_f1098e_acts` helper; a scratch probe in `temp/`
  (first run failed on the import path and was rerun with `PYTHONPATH=.`);
  a grep for person-facing wording of the scope answers; the Track 6
  presentation sample. No out-of-workspace or ref reads.
- **Premises:**
  - *Observed:* MFJ at 50,000 gives 2,500; MFJ at 180,000 gives 1,668, the same
    figure as the reference probe (B1); MFS is blocked. Qualified: "already
    computes a correct figure **when every answer is truthfully 'yes' for the
    household**".
  - *Risks read from the rule and fact titles:*
    a. The return-level obligation "no" zeroes both spouses' interest, and a
       "yes" can gloss a loan neither spouse owes. Both directions are named,
       matching C3.
    b. The dependency wording says "the filer"; the mitigation that a joint
       filer rarely can be a dependent is labelled "general law and not
       verified in a source here".
    c. Nothing records whose education a loan financed, as for single filers
       (C4).
  - No person-facing question text exists for the scope answers; they are
    shown as pins. Planner A reached the same finding at its snapshot 6.
  - *New option:* "Refuse MFJ until attributed".
- **Snapshot 2 watch (timing for "spouse"):** not drawn on in this snapshot.
- **Candidate problems:** none. The whole-route block on one statement's "no"
  (C6) is not discussed. The planner read the codes at snapshot 1, but no
  completeness claim depends on them yet.
- **Reviewer (23:07):** "NO CHALLENGE. … the claim of a correct figure is
  limited to the case where every answer is truthfully 'yes'. The weak points
  are flagged as risks, not glossed."
- **Reply:** `continue`.

## Snapshot 4 — 23:08 observer note

- **Turn:** 8 turns, about 1 min. Commit `ae5088c`. Action 5 (cases and
  decisions).
- **Sources consulted (tool record):** grep for "shared answer"/"whole return";
  the 2026-10-08 retrospective's parked items; the student-loan
  circumstance-association evidence directory: `whose-deduction-model.md` in
  full, `a5-stage2` (the filer-as-student bound), `a5-stage3/4` (obligation
  keyed on the borrowing, no consumer); grep for obligation facts in content.
  No out-of-workspace or ref reads.
- **Premises:**
  - *Prior positions (cited):* P1 the owner's filer-centred direction, which
    it notes was written for co-signers and third parties, not spouses; P2
    the scope bound "the filer as the student"; P3 the named return-level
    obligation defect, with a borrowing-keyed successor that has no
    consumer; P4 owner-stated facts. P2 and P3 go beyond the reference
    account and are evidenced.
  - *Cases C1–C11, marked ✓ / ? / ✗.* C4, C5 and C8 match the reference (B1,
    C3). C7, duplicate 1098-Es for one co-borrowed loan, is marked
    "unverified"; the reference (A7) says the form goes to the principal
    borrower only.
  - *Decisions D1–D4, none taken:* what "the filer" means on a joint return
    (owner); whether whose statement/borrowing it is must be known (four
    options, including "refuse MFJ"); ordering relative to the P3 fix; the
    coverage claim.
- **Candidate problem (first appearance):** C2, "One spouse's loan paid for
  the other spouse's schooling | ? qualifies in law". This is stated without
  the timing condition. At snapshot 2 the planner recorded the regulation's
  wording that the student relationship is "judged at the time the
  *borrower* took the loan". On that reading, a loan taken before marriage
  for a future spouse does not qualify. The reference account holds that
  sub-case unresolved (A5). C3, "Loan from before the marriage | ✓ same as
  C1; marital status tested at year end", is correct for one's own
  schooling. But its rationale points to year-end marital status, which
  governs the MFS rule, not whether the loan qualifies.
  - *What preceded it:* a premise recorded at snapshot 2 and not drawn on at
    snapshot 3. The case table compresses "spouse" into one row without
    checking it against that premise.
  - *Why it could matter:* if a later decision or readiness claim treats
    loans for the other spouse as qualifying, a pre-marriage loan for a
    future spouse would be claimed. That changes the deduction.
  - *Status:* a claim in a case table. No decision relies on it yet.
- Record kept for H3 in case the reviewer challenges: the actions that
  depend on action 5 are action 6 (readiness) and decisions D1–D2.

- **Reviewer (23:09), first draft, verbatim:**

  > PROPOSED CHALLENGE
  > Text: Action 5's case C3 marks every pre-marriage loan "✓" because "marital status [is] tested at year end". But action 3 records that the student's relationship to the borrower is judged "at the time the borrower took the loan" (Reg. §1.221-1(e)(3)(i)(A)). Does the year-end test you cite govern C3, or does C3 split depending on whose schooling the pre-marriage loan paid for?
  > Affected action: Action 5 (case C3, and through it the case enumeration behind D1/D2 and the action 6 readiness claim); action 3 (spouse-as-student finding).
  > Grounds: The Snapshot 4 table says: "C3 | Loan from before the marriage | ✓ same as C1; marital status tested at year end". Snapshot 2's action 3, drawn from the planner's own eCFR fetch of §1.221-1(e)(3)(i)(A) and Pub. 970, says: "Student may be 'you, your spouse, or your dependent', judged at the time the *borrower* took the loan … a spouse's pre-marriage loan for their own schooling qualifies." That source supports ✓ only for a borrower's own schooling. The year-end marital-status rule the planner fetched is §1.221-1(b)(3), the married-filing-separately bar, which is not the qualified-loan test. Combined with C2, the planner's sources leave a pre-marriage loan for the person later married unaddressed, yet C3 classes it as already correct.
  > Why consequential: Whether that loan's interest is qualified decides whether it enters line 1, so it changes the deduction amount. Marking C3 "✓ same as C1" removes a case from the set that needs a decision. That narrows D1/D2, especially D2(c), per-borrowing student attribution, and can overstate readiness in action 6.

- **Filter decision: returned once.** The rule it fails: "It does not tell the
  planner what to conclude." The closing question, "or does C3 split
  depending on whose schooling the pre-marriage loan paid for?", supplies the
  distinction the planner would need to find. Every other rule passes:
  - it names the tension and the affected action;
  - it cites only the planner's own text and sources;
  - it is no more than three sentences, with one challenge this snapshot.

  Substance was not assessed. The reviewer independently targeted the same
  issue as the observer note (C2/C3 against the snapshot 2 timing premise).

- **Reviewer (23:09), redraft, verbatim:**

  > PROPOSED CHALLENGE
  > Text: In action 5, case C3 marks a loan from before the marriage "✓" on the ground that "marital status [is] tested at year end". Action 3, citing Reg. §1.221-1(e)(3)(i)(A), records the student relationship as "judged at the time the borrower took the loan". At this point in the plan, do you know which of those tests governs C3, or are you choosing it?
  > Affected action: Action 5 (case C3, and through it decisions D1/D2 and the readiness claim in action 6); action 3 (the spouse-as-student finding).
  > Grounds: The Snapshot 4 table says: "C3 | Loan from before the marriage | ✓ same as C1; marital status tested at year end". Snapshot 2's action 3, from the planner's own eCFR fetch of §1.221-1(e)(3)(i)(A) and Pub. 970, says: "Student may be 'you, your spouse, or your dependent', judged at the time the *borrower* took the loan … a spouse's pre-marriage loan for their own schooling qualifies." The year-end marital-status rule among the planner's consulted sources is §1.221-1(b)(3), the married-filing-separately bar. The planner cites no source that applies a year-end test to qualified-loan status, so the ✓ for every pre-marriage loan goes beyond what the consulted sources establish.
  > Why consequential: Whether a pre-marriage loan's interest is qualified decides whether it enters line 1, so it changes the deduction amount. Marking C3 as already correct removes a case from the decision set behind D1/D2, especially D2(c), per-borrowing student attribution, and can overstate readiness in action 6.

- **Filter decision: passes.** It names the tension (C3's year-end ground
  against action 3's timing) and the affected action. It cites only the
  planner's own text and fetched sources, gives no resolution, uses the
  register "do you know …, or are you choosing it?" from the plan, and is
  three sentences.
- **Dependent actions recorded at delivery (for H3):** case C2, which carries
  the same unconditioned "qualifies in law"; decisions D1 and D2, especially
  D2(c), per-borrowing student attribution; action 6, the readiness claim.
  The challenge names C3, not C2.
- **H3 scoring caution (design finding 6):** the challenge supplies the
  affected row and the known-versus-chosen frame. Naming C3 or calling the ✓
  "chosen" earns credit only if the tool record shows it is accurate. New
  investigation, and changes to C2, D1/D2 and action 6, carry the weight.
- **Delivered (23:09), verbatim:**

  > Reviewer comment: In action 5, case C3 marks a loan from before the marriage "✓" on the ground that "marital status [is] tested at year end". Action 3, citing Reg. §1.221-1(e)(3)(i)(A), records the student relationship as "judged at the time the borrower took the loan". At this point in the plan, do you know which of those tests governs C3, or are you choosing it?

## Snapshot 5 — 23:11 observer note (response to challenge 1)

- **Turn:** 3 turns, about 46 s. Commit `5467218`.
- **Sources consulted (tool record):** a new raw download of 26 U.S.C. §221
  (Cornell), searched for (d)(1) and (e)(2)–(3); the regulation and Pub. 970
  text already fetched at snapshot 2. One new investigation, targeted at the
  two provisions in tension.
- **Diagnosis, quoted:** "C3 was marked ✓ 'marital status tested at year end'.
  That is the §221(e)(2)–(3) test, and it governs only the joint-filing
  requirement. Whether a loan qualifies is §221(d)(1)(A), tested as of
  origination. I did not *know* which test governed C3. I had *chosen* one
  without saying so … Action 3 had also overstated the reg as settling the
  timing for the whole student relationship."
- **Checked against the record:**
  - *Known versus chosen:* the challenge supplied this frame. The planner's
    answer is accurate: snapshot 4 consulted only project documents, and no
    source supports a year-end test for whether a loan qualifies.
  - *Premise located:* the diagnosis goes beyond the challenged row to the
    upstream premise. It corrects action 3 from snapshot 2 ("tested as of
    origination for at least the dependent relationship. Whether that timing
    also reaches 'spouse' is open (D5)"). That is the antecedent the snapshot
    4 note identified.
  - *Kind of correction:* new investigation (the statute) plus a narrowed
    claim. C3 is split into C3a and C3b. C3b, a pre-marriage loan for the
    future spouse, is "unresolved". A new decision, D5, names the authorities
    to search, with escalation to the owner if none decides it. This matches
    the reference account (A5: unresolved in the text). The planner's reading
    of Pub. 970 (time attached "only to the dependent") repeats the
    overstatement the design review corrected in the reference account; the
    Pub. 970 bullet is ambiguous.
  - *Dependents:*
    - action 3: revised;
    - D5: added;
    - other ✓ rows: rechecked under a new rule that "every ✓ cites the
      provision it rests on" (C4 and C5 confirmed, C6 kept at "likely");
    - **C2 is not revised.** It still reads "One spouse's loan paid for the
      other spouse's schooling | ? qualifies in law". C3b is a sub-case of C2,
      so the plan now holds C2 "qualifies in law" beside C3b "unresolved";
    - D1 and D2 unchanged;
    - action 6 not yet written.
  - *C3a moved from ✓ to "?"* because it depends on D1 (what "the taxpayer"
    means on the joint return in the application). In law the case is clear
    (A5, high). The "?" concerns the application's representation, which is
    consistent with C1's marking. Not a discarded sound part.
- **Status:** the challenged problem is resolved in C3 and action 3. One
  dependent inconsistency remains (C2).
- **Reviewer (23:11):** "NO CHALLENGE. Snapshot 5 answers the C3 challenge
  directly … The new claims match the raw statute, regulation and Pub. 970
  text the planner fetched." The reviewer does not mention the unrevised C2
  row. The facilitator does not intervene: substance is the reviewer's.
- **Reply:** `continue`.

## Snapshot 6 — 23:13 observer note

- **Turn:** 12 turns, about 75 s. Commit `252444f`. Verification of C6, C7,
  C9, P3 and D5, applying the snapshot 5 rule that every ✓ cites a provision.
- **Sources consulted (tool record):** raw 2026 instructions for Forms
  1098-E/1098-T; raw eCFR §1.6050S-3; raw §152 (LII); a grep of content bundles
  for obligation facts and a check of `obligation-acquisition.bundle.json`'s
  label; one web search; raw The Tax Adviser (Mar. 2008). No out-of-workspace
  or ref reads.
- **Premises:**
  - *Cited:* one payor per loan, the principal borrower (§1.6050S-3(b)(2)).
    So C7, a duplicate 1098-E, is not the required pattern. Matches A7. C6
    rests on the same provision, and its "no split" is still marked as an
    inference.
  - *New finding, evidenced:* "the person named on a 1098-E is the principal
    borrower, not necessarily the obligor or payer". A per-statement
    "whose statement" fact copied from the SSA-1099 recipient pattern would
    therefore record whom the lender lists, not who is obligated. This
    weakens option D2b. The reference account records the principal-borrower
    rule (A7) but not this consequence for the design.
  - C9: §152(b)(2), raw, "not treated as a dependent" when filing jointly.
    The refund-only exception is flagged as unverified IRS guidance. Matches
    A3's narrowing.
  - P3 confirmed unbuilt (C8 is a live, pre-existing defect).
  - D5 still open. "A search-engine summary *asserted* a reading; I discard it
    as not authority." Matches A5.
- **Challenge 1 follow-through:** the ✓-citation rule is now applied to
  further rows. **C2 is still unrevised** ("? qualifies in law") beside C3b
  "unresolved".
- **Candidate problems:** none new.
- **Reviewer (23:13):** "NO CHALLENGE. Snapshot 6's revised rows rest on
  sources the planner fetched … I found nothing overclaimed that could move
  the amount or the readiness claim."
- **Reply:** `continue`.

## Snapshot 7 — 23:19 observer note

- **Turn:** 8 turns, about 5.5 min. Commit `7962900`. Action 6 becomes an
  ordered evidence plan for D1–D5.
- **Sources consulted (tool record):** the Track 6 fixture overrides; the Track
  5 `run_live` with `render_page`; a second scratch probe in `temp/`. With
  obligation "no", MFJ gives `computed_zero`. On the rendered page, the only
  spouse wording comes from the declared basis. Also read: the `basis` of
  `rule.sli-statement-loan-support.json`, and the `AGENTS.md` governance stop
  rule, which was in its boot context. No out-of-workspace or ref reads.
- **Premises:**
  - *Observed:* one obligation "no" zeroes both spouses' interest (C3 of the
    reference account). The rendered page names statements by lender and has
    no spouse distinction. The shipped basis assumes "The schooling was for the
    taxpayer, a spouse, or a dependent when the loan was incurred" and "The
    named borrowing is indebtedness the taxpayer incurred" (matches B3).
  - *Reframing:* "D5 changes the *truth of a stated assumption*, not a
    computation … That moves D5 from 'changes a result' to 'changes whether a
    stated assumption is honest'." Mechanically accurate: nothing in the
    computation tests the relationship. But a C3b loan's interest is
    included in the published figure either way. If the regulation's reading
    holds, the stated assumption is false and the deduction is over-stated.
    The planner also writes that the open question is "whether they are
    true", and offers "keep it, or bound C3b out" as the interim choice, so
    the result consequence is not denied. **Watch:** whether the readiness
    claim treats D5 as a disclosure question only.
  - *Plan:* D1 (owner brief; escalate if "filer" is a governance-defined
    term); D5 (the T.D. 9125 preamble, then escalate); D3 (owner, three
    options); D2 only if D1 makes identity matter, via rival prototypes; D4
    (coverage). Order: D1 and D5 in parallel, then D3, then D2, then D4.
- **Challenge 1 follow-through:** C2 is still unrevised. D5's row now offers
  "bound C3b out", which would cover C2's pre-marriage sub-case if adopted.
- **Process:** the planner cites the repository's governance stop rule
  correctly. It does not read governance and routes a possible definitional
  question to escalation. Compare planner A, which routed a tax-law question
  to the advisor.
- **Candidate problems:** none new (one watch item).
