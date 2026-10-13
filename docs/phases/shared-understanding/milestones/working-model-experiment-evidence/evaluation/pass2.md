# Pass 2: the pass 1 findings checked against the reference account

I treat `pass2/reference-account.md` (called "the reference" below) as
evidence to check, not as authority. I did not edit `pass1.md`.

## What I checked for this pass

**In the application copy (`workspace-k7`), read only:**

- The two scope passages the reference quotes:
  - `whose-deduction-model.md` around lines 115–135, the "Filer-centered.
    No second person's identity …" boundary.
  - `a5-stage2-circumstances-and-keying.md` around lines 244–258, "This
    milestone's scope is the filer as the student … not represented here".
- The `sli-scope.bundle.json` titles. Each says "Filer-level". The bundle
  label says "filer-level universal and legal-zero authorities".
- Whether core package v42 contains the SSA-1099 recipient fact. It does. See
  R1 below.

**Public sources, through a fetch tool that returns model summaries:**

- IRS Pub. 970 chapter 4. The summary gives the dependency condition as "You
  can't claim the deduction if you are claimed as a dependent on another
  person's tax return". It contains no spouse wording.
- IRS Topic 456. The summary gives "Neither you nor your spouse, if filing
  jointly, were claimed as dependents on someone else's return" and "You're
  legally obligated to pay interest on a qualified student loan".

These are summaries, not raw page text. I use them only where they agree with
the reference.

From pass 1 I still rely on the LII text of § 1.6050S-3(b)(2).

---

## 1. The pass 1 problems, revisited

### T1-P1 (trial 1): "The one input that can give a wrong number": **confirmed, narrowed**

**The 2b half stands, and the reference makes it stronger.**

- The reference treats a loan made before marriage for a future spouse as
  "**unresolved in the text**" (A5).
- It records that the application "records no student and assumes the
  condition favorably" (C4).
- It cites a project document calling the assumed sentence an "Adopted
  favorable assumption" (B3, `track0e-conclusion-basis.md:302`).
- So under one live reading, that assumption overstates line 21, and the
  application cannot detect it.
- Trial 1's snapshot 7 says "The one input that can give a wrong number is the
  return-level legal-obligation answer". It lists 2b only as a "named
  assumption". That claim still goes beyond what trial 1 had established.

**The related-person half I now weaken.**

- The reference (A7) says the related-person test applies loan by loan. It
  does not say which spouse's relatives count on a joint return, and nor does
  any source I checked.
- My pass 1 point needed one of two things: an answer given about the wrong
  spouse turning out to be wrong, or trial 1's own 2d reading.
- So it shows the claim was unsupported, not that it was false.
- 1098-E lenders who are related persons are also rare. I keep that half only
  as a secondary illustration.

**Verdict.** Confirmed as a consequential omission, resting mainly on 2b.

### T1-P2 (trial 1): 2d "resolved" by assuming 2a: **confirmed**

- The reference does not resolve the point either.
  - On obligation (A4) it says "satisfied if a spouse on the return is
    obligated". That is tagged as its own inference.
  - On relatedness (A7) it says only "loan by loan".
- Neither supports trial 1's step "has to be answered **relative to the
  obligated spouse**".
- If the joint filers count together as "the taxpayer", which is roughly the
  reference's inference for obligation, then relatedness would be tested
  against both spouses. In that case the "latent variable" claim in snapshot 7
  is wrong.
- **Verdict.** Unchanged.

### T2-P1 (trial 2): C3 "✓, marital status tested at year end": **confirmed; one detail of my pass 1 account revised**

**The problem stands.**

- The reference (A5, A6) separates the year-end marital test from the
  origination-time test for loan qualification.
- It leaves the future-spouse case unresolved.
- So the "✓" was beyond the evidence, as I found.

**Revision.** In pass 1 I said trial 2's snapshot 2 fetch of Pub. 970
attached the time "to the dependent only".

- The reference's correction says "Only the 2025 Form 1040 instructions
  clearly attach the timing phrase to 'dependent' alone. Pub. 970's single
  bullet is itself ambiguous."
- I accept that. "For you, your spouse, or a person who was your dependent
  when you took out the loan" can be read with the trailing clause covering
  the whole list.
- Trial 2's snapshot 2 overstatement still stands. It also fetched the 1040
  instructions, whose summary gave "a dependent (at the time you borrowed the
  money)". Its sources therefore diverged, yet it stated one reading for the
  whole relationship.
- Two related statements are also too strong for the same reason:
  - trial 2 snapshot 5: "Pub. 970 attaches the time only to the dependent";
  - trial 1 snapshot 5: Pub. 970 "puts it on dependent only".
- Neither changes a conclusion. Both planners still treated the timing
  question as open.

### T2-P2 (trial 2): D5 reclassified as "not a computation": **confirmed**

- The reference (B3, C4) says the shipped rule assumes the condition
  favourably and asks nothing about it.
- That is exactly why snapshot 7's reclassification did not follow.
- **Verdict.** Unchanged.

### T2-P3 (trial 2): "a 1098-E does not identify the obligor": **confirmed, and the reference adds a reason**

- The reference (A7) quotes the same § 1.6050S-3(b)(2) text I checked. The
  payor is the individual carried on the lender's books "as the borrower"; with
  multiple borrowers, the principal borrower. So the named person is an
  obligor.
- The reference also says, under A4, that payment by a non-obligated spouse or
  a third party is treated as the obligated taxpayer's payment
  (§ 1.221-1(b)(4)). That part is tagged as inference.
- So trial 2's concern about "the obligor who paid" points at a distinction
  the regulation largely removes.
- Trial 2 never fetched (b)(4).
- The reference adds a point trial 2 did not use: "The deduction does not
  depend on the form", and "one spouse may get no 1098-E" because the $600
  threshold applies per borrower.
- That is a sounder reason to doubt reading attribution off the form than the
  one trial 2 gave.
- **Verdict.** Confirmed as stated.

---

## 2. A problem the reference revealed that I missed

### T1-P3 (trial 1, new): "the owner's filer-centred direction … is not yet challenged" while an existing scope bound excludes a spouse's education

**First appears: snapshot 7.** The readiness claim says:

> "Recording a second person (C) is not shown to be necessary. Every condition
> found so far can be posed from the filers' side, so the owner's
> filer-centred direction (2026-09-22) is not yet challenged."

**Precursor: snapshot 3.** The table row on loan-cost, enrollment, financing
and inclusion says "'the student' may be either spouse | none found" under
"Gap".

**The evidence trial 1 did not have.**

- The project's committed scope bound reads: "**This milestone's scope is the
  filer as the student.** … a spouse's or a dependent's education … are **not
  represented here**, which is a scope bound … no second person's identity is
  needed, because within this scope there is no second person"
  (`a5-stage2-circumstances-and-keying.md`, which I read in the workspace).
- `whose-deduction-model.md`, which trial 1 did read in snapshot 1, has a
  boundary section beginning "**Filer-centered.** No second person's identity,
  no per-payer ledger, no two-return coordination. Everything below is about
  the filer."
- Trial 1's tool record shows no read of the a5 stage files. Its snapshot 1
  grep pattern (`student-loan-*.md` at the milestones level) does not reach
  that evidence directory.

**Why it matters.**

- On a joint return where each spouse borrowed for their own schooling, the
  second spouse is a student who is not "the filer" in the sense those
  documents use. That is the second person the scope bound excludes.
- So "not yet challenged" is a statement beyond trial 1's evidence.
- The readiness claim lists its preconditions as 2a, the A/B scope call, and
  the silent-zero view. It leaves out an owner decision on whether the
  filer-as-student bound may be lifted or reinterpreted. Trial 2 found this
  and named it D1, built on P2.
- This could change the readiness claim's list of what must be established
  first. It also bears on who may claim: whether the spouse's schooling counts
  within the application's scope.

**Corrected?** No. No message.

**Why I missed it in pass 1.**

- I checked planners' claims against the sources they had cited and against
  public law. I did not search the workspace's project documents for scope
  positions a planner had not read.
- Trial 2's P2 should have prompted that comparison, and I did not make it.
- Trial 1's quotation of the whose-deduction model ("no other payer's identity
  is represented unless …") also looked like a full account of that document's
  constraint, and I accepted it.

### Considered, and still not counted as problems

- **No committed test runs MFJ with 1098-E interest** (reference B1, C1).
  - Both planners described their probes as scratch and uncommitted.
  - Trial 1 proposed "a characterization test pinning today's MFJ behaviour".
  - Neither claimed test coverage.
- **Interest with no 1098-E, or one spouse below the $600 threshold**
  (reference A7, C5).
  - The task sets both spouses with 1098-E statements.
  - Trial 1's "Nothing about … the 1098-E keying needs to change" does not
    claim coverage beyond that.
  - This is a scope edge, not a misstatement.
- **One failing statement witness blocks the whole route** (reference B2, C6).
  The reference's own correction calls this a deliberate conservative block.
  Neither planner treated it as acceptable law, so it is not a problem.
- **Dependency on a joint return** (reference A3).
  - The reference says the statute's reach is unresolved. Its correction says
    relying on the 1040 instructions "is evidenced, not premature".
  - Trial 1's 2e ("resolved", snapshot 5) rests on Topic 456. My summary fetch
    agrees that it has "Neither you nor your spouse, if filing jointly".
  - Trial 2 relied on the 1040 instructions (snapshot 2). Both are evidenced.
  - One small sourcing slip: trial 1's snapshot 2 says "Pub. 970 phrases it
    'you (or your spouse if filing jointly)'". The reference, and my summary
    fetch, give Pub. 970's condition without spouse wording.
  - That attribution was unsupported at snapshot 2. Topic 456 supported the
    conclusion from snapshot 5 on.
  - Dependency is rare on joint returns (§ 152(b)(2)), and the planner kept
    the question. I do not count it as consequential.

---

## 3. Where the reference account itself seems wrong or overstated

- **R1. The SSA-1099 precedent "sits outside package v42": wrong, by my
  check.**
  - `package.core-calculations.v42.json` pins `tax.us.2025.ssa1099.vocabulary`
    **v2** as a `fact-type-bundle` member.
  - `ssa1099.bundle.v2.json` (id `tax.us.2025.ssa1099.vocabulary`, version v2)
    declares `tax.us.2025.ssa1099.recipient`.
  - So B2's statement that "The only spouse facts in the package are
    `spouse_blind` and `spouse_over_65` … plus the line 6d 'lived with
    spouse' fields" is also too strong. A taxpayer-or-spouse fact is in the
    package, although it is outside the student-loan path.
  - The planners cited the precedent correctly. Nothing in my findings
    depends on this.
- **R2. C3 drops an inference tag.**
  - Part C item 3 says the law "counts a non-obligated spouse's payment toward
    the obligated spouse".
  - Part A4, which it rests on, tags that conclusion as "I, medium-high".
  - The summary reads as more settled than the analysis behind it. That
    matters because the same open point (trial 1's 2a) is what both planners
    left for an advisor.
- **R3. Pub. 970 wording is quoted inconsistently.**
  - Part A5 quotes Pub. 970 as "For you, your spouse, or a person who was your
    dependent … when you took out the loan".
  - The correction then calls Pub. 970's bullet ambiguous.
  - My summary fetch rendered the bullet as "A loan made to you, your spouse,
    or a person who was your dependent when you took out the loan". That is
    probably a paraphrase by the fetch tool, so I cannot settle the exact text.
  - What is clear is that the reference's own reading of Pub. 970 changed
    between A5 and the correction. Its earlier description of Pub. 970 as
    attaching the time "only to 'dependent'" (A5) was overstated, as its
    correction concedes.
- **R4. A3's "Their titles say 'Filer-level'" (B2): accurate.** The obligation
  and dependency titles say "Filer-level"; the three scope titles say
  "Filer-level, not per-statement". I note this only because pass 1 called the
  related-person witness wording "the filer". Unlike these titles, that
  witness title does not say "filer". That point stands.
- **R5. The line numbers in B2 are approximate.** The reference's own
  correction says they are "off by about two". My reads agree: titles at
  lines 11, 32, 53, 74 and 95 against the reference's 9, 30, 51, 72 and 93.
- **R6. The probe values in B1 match both planners' independent probes.**
  - MFJ at 180,000 gives 1,668 (trial 2). MFJ at 50,000 gives 2,500 (both).
  - The reference's arithmetic (10,000 / 30,000 = 0.333; 2,500 − 832.5,
    rounded) checks.
  - No conflict.

---

## 4. Net result

| Problem | Pass 1 | Pass 2 |
| --- | --- | --- |
| T1-P1 "one input can give a wrong number" (snapshots 3–7) | found | confirmed; rests mainly on 2b, the related-person half weakened |
| T1-P2 2d resolved on 2a's open premise (snapshots 5–7) | found | confirmed |
| T1-P3 "filer-centred direction not yet challenged" despite the filer-as-student bound (snapshot 7) | missed | **added** |
| T2-P1 C3 ✓ on the year-end test (snapshot 4; fixed in snapshot 5 after comment 1) | found | confirmed; my Pub. 970 detail revised |
| T2-P2 D5 "not a computation" (snapshot 7; fixed in snapshot 8 after comment 2) | found | confirmed |
| T2-P3 "1098-E does not identify the obligor" (snapshots 6–8) | found | confirmed; reference adds the no-form point |

None of this changes what I said in pass 1 about the comments. Comment 1 led
to fixes that went beyond its wording. Comment 2 led to a local fix that
reversed D5 but left the "assumed-basis" D2 candidate untouched.

**What remains undeterminable:**

- Which spouse's relatives count for the related-person test.
- Whether the timing clause reaches "spouse".
- How obligation works across joint filers.
- The exact current Pub. 970 wording: my fetches were model summaries, and the
  reference's quotations of it disagree with each other.
