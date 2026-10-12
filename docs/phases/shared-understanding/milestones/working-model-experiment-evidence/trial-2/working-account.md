# Working account

## Snapshot 0 — initial action list

- **Refined:** nothing yet; wrote the first plain-language list of actions.
- **Why now:** the task asks for a starting list before investigation.
- **Evidence:** only a filename scan — the repo has extensive student-loan-interest
  (SLI) / 1098-E work (many `tests/test_sli_*` and `test_f1098e_*` modules), so the
  single-filer path is likely mature.
- **Open questions:** does the app model a spouse or filing status at all? Is
  MFJ currently refused?
- **Next:** develop actions 1–2 together (current state of SLI and of spouse/filing status).
- **Direction change:** none.

## Snapshot 1 — current behavior (actions 1–2)

- **Refined:** what the app does today with 1098-E, scope answers and filing status.
  Done first because every later question depends on whether MFJ is refused,
  silently supported, or partially supported.
- **Evidence:** `packages/content/tax/2025/f1098e.bundle.json`, `sli-scope.bundle.json`,
  `sli-relationship-source.bundle.v2.json` (identity keys of every fact type);
  `rule.sli-worksheet.v5.json` (pins, codes, MFS branch); `parameter.sli-*`;
  `ssa1099.bundle.v2.json` + `packages/tax/ssa_benefits.py` (recipient precedent);
  `docs/phases/engine-breadth/coverage-frontier.md` row 50; the f1098e milestone
  plan's filing-status notes (§466, §560, §924). `OWNER_MODEL.md` has no spouse text.
- **Finding:** MFJ is *not refused*. Nothing in the student-loan path knows a spouse
  exists. Per-return arithmetic (single $2,500 cap, MFJ thresholds) is already present.
  The gap is attribution: whose statement, whose obligation, whose dependency status.
- **Open questions:** is per-return treatment actually correct law for each
  eligibility test? Does the app compute a two-statement MFJ case today, or block
  on some multi-statement rule? Is the SSA recipient pattern a fit, or does a
  1098-E (borrower ≠ student, joint borrowers) need something different?
- **Next:** action 3 (tax law) and then action 4 (probe).
- **Direction change:** the framing shifts from "add MFJ support" to "decide whether
  the existing per-return treatment is correct, and where per-spouse attribution matters".

## Snapshot 2 — 2025 rules for a joint return (action 3)

- **Refined:** the tax law, before probing the app, so I know what "correct" means
  for the probe.
- **Evidence:** IRS 2025 Instructions for Form 1040, Schedule 1 line 21 and the
  worksheet (fetched raw, read directly); IRS Pub. 970 (2025) chapter 4 (fetched
  raw); 26 CFR §1.221-1 via eCFR (b)(1)–(3), (c), (e)(3).
- **Correction to my own process:** a summarizing fetch claimed Pub. 970 says
  "$2,500 per return". The raw text does not contain that phrase. I discarded that
  quote and rest the per-return cap on the worksheet line 1 and §1.221-1(c), and I
  mark it as an inference about joint-return computation. Raw text only from here on.
- **Finding:** joint-return arithmetic is the same shape the app already runs.
  What changes is *who* each eligibility test is about: dependency (either spouse),
  legal obligation (per loan, either spouse), the student's relationship to the borrower.
- **Open questions:** does the app's dependency/obligation question text cover a
  spouse? What does the app actually do with two statements on MFJ today? Is a
  per-statement "whose" fact needed for any computed result, or only for honest
  questions and explanation?
- **Next:** action 4, probing the app with synthetic MFJ cases and reading the
  question wording.
- **Direction change:** none. The snapshot-1 reframing (attribution, not
  arithmetic) is confirmed by the sources.

## Snapshot 3 — probe of current behavior (action 4)

- **Refined:** what the app actually does with an MFJ two-statement return,
  measured rather than inferred, now that I know what the right answer is (snapshot 2).
- **Evidence:** ran `temp/probe_mfj.py` (scratch, reuses
  `tests/test_sli_track5_worksheet_integration.Return` and `run_live`; filing status
  injected through `_f1098e_acts(filing_status=…)` from the Track 6 test). Results:
  MFJ 50k → 2,500; MFJ 180k → 1,668; single 90k → 1,668; MFS → `SLI_MFS_INELIGIBLE`.
  Read the worksheet's legal-zero branch and the scope fact titles. Searched for
  person-facing question text and found none for scope answers.
- **Finding:** the "both spouses" case is *silently supported*. The arithmetic is
  right. The risk is in eligibility answers posed at the "filer" level, chiefly the
  return-level legal-obligation answer, whose "no" zeroes every statement.
- **Open questions:** is the per-loan obligation problem MFJ-specific, or a
  pre-existing single-filer gap that MFJ makes more likely? Does the owner want
  the return to *know* whose statement is whose (for explanation and trust), even
  where the figure doesn't depend on it? Joint-borrower statements?
- **Next:** action 5, laying out the joint-return cases and the decisions each one
  forces, and what evidence a decision needs.
- **Direction change:** the question is no longer "how to support MFJ" but
  "whether to keep, constrain, or make explicit the support that already exists".
  "Refuse MFJ until attributed" now counts as an option too.

## Snapshot 4 — cases and decisions (action 5)

- **Refined:** turned "attribution matters" into concrete cases and four decisions.
  I did this now because the probe showed what works, and searching for prior
  shared-answer discussion turned up earlier student-loan evidence work that frames
  every option.
- **Evidence:** `whose-deduction-model.md` (owner's filer-centered direction of
  2026-09-22, named defect on return-level obligation), `a5-stage2-circumstances-and-keying.md`
  (filer-as-student scope bound), `a5-stage3-values-and-basis.md` / `a5-stage4-…`
  (borrowing-keyed obligation selected, no consumer), `owner-stated-facts.md`;
  `docs/phase-state.md` "Parked" (shared-answer "no" reaching the whole return);
  `docs/milestone-retrospectives/2026-10-08-account-refinement.md`.
- **Finding:** the project already chose *not* to represent second persons and
  bounded the student to the filer. The MFJ two-spouse case is the first real
  candidate to test the owner's "unless a concrete supported case demonstrates
  identity is necessary" condition. The arithmetic works. The open part is meaning
  and representation.
- **Open questions:** do lenders issue duplicate 1098-Es to co-borrowers (C7)? Can a
  spouse on a joint return be claimed as a dependent (C9)? Is P3 actually still
  unbuilt? (I found no obligation fact in the current SLI bundles.)
- **Next:** verify C7, C9 and P3 so each decision has its evidence. Then map what
  each decision needs, and from whom.
- **Direction change:** the decisions are mostly *owner/meaning* decisions over
  existing positions (P1, P2), not engineering unknowns. The plan now aims to put an
  owner question in front of a prototype.

## Snapshot 5 — correction: C3 conflated two time tests

- **Refined:** case C3 (loan from before the marriage) and the action-3 note on the
  student relationship, prompted by a reviewer question.
- **What was wrong:** C3 was marked ✓ "marital status tested at year end". That is
  the §221(e)(2)–(3) test, and it governs only the joint-filing requirement. Whether
  a loan qualifies is §221(d)(1)(A), tested as of origination. I did not *know*
  which test governed C3. I had *chosen* one without saying so, and it was the
  wrong one for the question. Action 3 had also overstated the reg as settling the
  timing for the whole student relationship.
- **Evidence:** 26 U.S.C. §221(d)(1)(A) and (e)(2)–(3) (Cornell LII, raw text);
  26 CFR §1.221-1(e)(3)(i)(A) and (b)(3) (eCFR, raw text, already fetched in snapshot 2);
  Pub. 970 (2025) ch. 4 "Qualified Student Loan" (raw text).
- **Result:** C3 split. C3a (own schooling, pre-marriage) is "?" because it depends
  on D1, not because of timing. C3b (a pre-marriage loan for the future spouse) is
  **unresolved**. New decision D5: whether the origination-time clause reaches
  "spouse". Statute ambiguous, reg suggests yes, Pub. 970 suggests no; no deciding
  authority found yet.
- **Open questions:** D5's authority. Also, did I conflate tests anywhere else? I
  rechecked the other ✓ rows. C4 and C5 rest on the probe plus worksheet text. C6
  rests on "one joint return needs no split", which is an inference and not a sourced
  rule, so I'm downgrading my confidence there to "likely" (already worded so).
- **Next:** unchanged from snapshot 4 (C7, C9, P3 verification), now with D5 added
  to the authority searches.
- **Direction change:** a rule for the rest of the plan: every ✓ cites the provision
  it rests on. Where two provisions could apply, the row names both and says which
  governs, or says it is unknown.

## Snapshot 6 — verifying C6, C7, C9, P3, D5

- **Refined:** the cases that rested on unverified premises, so each decision
  has a sourced or explicitly-open basis (the rule adopted in snapshot 5).
- **Evidence:** 26 CFR §1.6050S-3(a)–(c) (eCFR raw: one payor = principal borrower);
  Instructions for Forms 1098-E and 1098-T (IRS, raw: one 1098-E per borrower, may
  aggregate loans; silent on co-borrowers); 26 U.S.C. §152(b)(2) (LII raw); grep of
  `packages/content/tax/2025/*bundle*.json` for obligation facts; web search plus
  The Tax Adviser (Mar. 2008) for D5.
- **Findings:** C7's double-count fear is not the reporting rule's pattern. The
  more important finding is the inverse: **the person named on a 1098-E is the
  principal borrower, not necessarily the obligor or payer**. So any "whose is
  this statement" fact read off the form (the SSA-recipient analogy in D2b) would
  record *who the lender lists*, not *who is obligated*. That weakens D2b as a
  route to fixing C8. C9's dependency bar is very likely moot on a genuine joint
  return by §152(b)(2). P3 is confirmed unbuilt. D5 is still open.
- **Open questions:** D5 (authority). Whether the owner regards the spouse as part
  of "the filer" (D1). Neither can be settled by more engineering investigation.
- **Next:** map each decision to what would settle it, who settles it, and in what
  order (action 5 completed into an evidence plan). Then the readiness claim.
- **Direction change:** the SSA-1099 recipient precedent looked like the obvious
  template in snapshot 1. It is a poorer fit than it looked, because a 1098-E names
  a lender-chosen principal borrower, not the person the deduction's tests are about.

## Snapshot 7 — evidence map per decision, and two more probes

- **Refined:** turned D1–D5 into an ordered evidence plan (who settles each, with
  what). I ran two cheap probes first, because they could change the map.
- **Evidence:** `temp/probe_mfj2.py` via `run_live` (MFJ): obligation "no" →
  `computed_zero`; rendered page via `run_live(render_page=True)` and its
  embedded model. `packages/content/tax/2025/rule.sli-statement-loan-support.json`
  `basis` (said/derived/assumed/left_with_person). AGENTS.md "Stop when your unit
  turns on governance text".
- **Findings:** C8's wrong-zero is now demonstrated, not just read from rule logic.
  The shipped rule already *assumes* the student relationship (in the reg's reading,
  which bears on D5) and that "the taxpayer" incurred the borrowing. So for a joint
  return the open questions are what those assumption sentences mean and whether they
  are true. The arithmetic is not in question. That moves D5 from "changes a result"
  to "changes whether a stated assumption is honest". It also adds a low-cost
  candidate for D2.
- **Open questions:** whether "filer"/"person" is governance-defined (I may not read
  governance; flagged as an escalation trigger). What the T.D. 9125 preamble says.
- **Next:** refinement 8, the readiness claim.
- **Direction change:** D2 prototypes are now conditional on D1, not a default
  stage. Two of the five decisions (D1, D5) are owner/authority questions that no
  prototype can settle.

## Snapshot 8 — correction of D5's reclassification; readiness claim

- **Refined:** (1) D5's classification, prompted by a reviewer question; (2) the
  readiness claim, as this is refinement 8.
- **What was wrong:** snapshot 7 said D5 "changes whether a stated assumption is
  honest" rather than a result. That does not follow from actions 4–5. Snapshot 5
  established that under the reg's reading C3b is not qualified. The probes and the
  rule show box 1 is counted under the assumption regardless. A false assumption
  therefore means an overstated line 21, and the app asks nothing that would reveal
  C3b. I had treated declaring an assumption as if it made the result right. It
  only makes a possible error visible. D5 is result-bearing (under one reading);
  under the other, only the wording is off.
- **Evidence:** no new sources. I re-read snapshot 5's D5 entry, the
  `rule.sli-statement-loan-support.json` basis, and the snapshot 3/7 probe results.
- **Readiness claim:** **not ready to select an approach.** The mechanics are
  understood, measured and sourced (see plan action 7). Correctness itself depends on
  D1 (owner: meaning of "filer" on a joint return) and D5 (authority: timing for
  "spouse"), then D3 (owner: order relative to the per-borrowing obligation fix).
  D2 and D4 follow from those. Separately, the owner should be told now that MFJ
  two-spouse returns already compute, with a demonstrated wrong-zero (C8) and a
  possible undetectable overstatement (C3b).
- **Open questions:** D1, D5, D3 as above. Whether "filer" is governance-defined.
- **Next (for the team):** write the D1 brief; run the D5 preamble search; record
  current MFJ behavior in the coverage frontier as an observation.
- **Direction change:** none in the conclusion's direction. But two of my corrections
  had the same shape: treating an unstated choice (C3) or a declared assumption (D5)
  as settled. So the readiness claim rests only on measured behavior and quoted
  sources, and names everything else as open.
