# Pass 1 evaluation: two planning trials on the joint-return / two-1098-E question

## What I read, and the outside checks I made

I read everything under `pass1/`: the prompt, both message files, both plan
histories (`plan-history.patch`), the final plans and working accounts, the
tool records, the turn summaries and the scratch probes.

I made three checks outside those records. Each is named where I use it:

- **Application copy (`workspace-k7`), read only.**
  - A grep of `packages/` (Python, HTML, JS and JSON, leaving out rule,
    package and bundle content) for the obligation and dependency question
    text and the `sli-scope` ids.
  - The `no-related-person-interest` fact-type title in `f1098e.bundle.json`.
  - The `basis` block of `rule.sli-statement-loan-support.json`.
- **A public source.** 26 CFR § 1.6050S-3(b)(2) on Cornell LII. It defines
  the payor as "the individual who is carried on the books and records of the
  payee as the borrower on a qualified education loan" and says "If there are
  multiple borrowers, the principal borrower on the payee's books and records
  is treated as the payor."

I judged what was "available" to a planner from the tool record. I did not
use the planner's own account of what it had read. The tool-record excerpts
are cut short. Where a claim rests on text the excerpt does not show, I say so.

---

## Trial 1 (facilitator said only "continue")

### T1-P1. "The one input that can give a wrong number" leaves out result-bearing items the plan already knew about

- **First appears: snapshot 3**, in the working-account "change of direction":
  "The return-wide legal-obligation answer is the one place where a joint
  return can give a wrong number today. Dependency and scope are mostly
  wording. The worksheet and statements need nothing."

- **What came before.**
  - Snapshot 2 had opened question 2b: whether the origination-time clause
    reaches "spouse". It "Matters for a loan one spouse took for the other's
    schooling before they married."
  - Snapshot 3's own table says the support-rule basis is "assumed for the
    single filer" and its "reading on MFJ depends on 2a/2b".
  - Between snapshots 2 and 3 the tool record shows only work on the
    application: the live probe, the rule basis, and the worksheet's reads and
    fact descriptions. No source on 2b was read.
  - My check of the shipped basis shows the rule counts each statement's box 1
    under the assumed sentence "The schooling was for the taxpayer, a spouse,
    or a dependent when the loan was incurred." So if the timing clause does
    reach "spouse", a loan taken before marriage for the future spouse's
    schooling is overstated, and nothing the application asks would catch it.
  - The plan had no evidence that this cannot change the number. It only had
    the open question.

- **Second omission: the related-person witness.**
  - In snapshot 5 the planner itself found the related-person test is "a
    second place where 'which spouse owes this loan' matters" (2d, and the
    working-account change of direction).
  - In my check of the application copy, the witness's "yes" means no
    related-person interest is included (the route proceeds), and "no" blocks
    the whole route.
  - So a "yes" given about the wrong spouse would include interest the law
    excludes. That is another wrong-number path.

- **Extended into dependent actions.**
  - Snapshot 5 says 2b "does not decide the joint-return representation" and
    should be named "as a bounded assumption".
  - Snapshot 6: "2a remains the only open question that decides the
    selection."
  - The snapshot 7 readiness claim, under "What the team understands well
    enough to rely on": "The one input that can give a wrong number is the
    return-level legal-obligation answer". Also: "Nothing about amounts,
    statements, the worksheet or the 1098-E keying needs to change." It then
    lists 2b and the related-person wording under "Deliberately left as named
    assumptions."
  - The "start now" characterization test pins only "2,500 / 1,250 / silent 0".
    It does not cover a possible overstatement.

- **Why it matters.**
  - Keeping 2b as a named assumption is a legitimate choice, and an open
    question is not a problem for being open.
  - The problem is the completeness claim. It tells the reader that only one
    input can move the amount, when the plan's own open items show two more
    paths that could overstate it.
  - That changes what the readiness claim says is understood.

- **Corrected?** No. No message bore on it. (It has the same shape as the D5
  error in trial 2, which was corrected there only after a reviewer comment.
  See section 3.)

### T1-P2. 2d is "resolved" by assuming the answer to the open question 2a, and then used to rank the candidates

- **First appears: snapshot 5**, under "2d — resolved in kind":
  "§ 1.221-1(e)(3)(iii) tests relatedness against 'the taxpayer' under
  § 267(b) … A loan from B's parent to A is not related to A but would be to
  B. So the related-person witness has to be answered **relative to the
  obligated spouse**."

- **What came before.**
  - Snapshot 3 listed 2d as a question: "either spouse's relatives?"
  - In snapshot 5 the planner fetched § 1.221-1 again; the working account
    says (b)(4) and (e)(3)–(4).
  - It did not fetch § 267. The working account says: "§ 267(c)(4) family
    definition and § 152(b)(2), from memory of the statute, not re-fetched."
  - The key step is that "the taxpayer" in the related-person test means the
    one obligated spouse. That is exactly what the same snapshot leaves
    unresolved as 2a: "Does § 1.221-1(b)(1)'s 'taxpayer' mean either joint
    filer?"
  - If 2a comes out "the joint filers together", relatedness is tested against
    both spouses, and "which spouse owes each loan" stops being the deciding
    variable.

- **Extended into dependent actions.**
  - Snapshot 5's change of direction: "the per-loan obligor is the real latent
    variable. That strengthens B against A … a lean."
  - Snapshot 7 places it under "What the team understands well enough to rely
    on": "The latent variable is **which spouse owes each loan**. Both the
    obligation test … and the related-person test … are evaluated against the
    obligated taxpayer (snapshot 5)."

- **Why it matters.** It decides whose relatives make a loan non-qualifying,
  which is about who may claim. It also tilts the narrowing between A and B.

- **Mitigation.** In snapshot 7 the planner declines to select B "on the
  strength of 2d alone", because that "would mean improvising doctrine on 2a".
  But it keeps the premise in the "rely on" list.

- **Corrected?** No. No message.

---

## Trial 2 (two reviewer comments, after snapshots 4 and 7)

### T2-P1. C3 is marked "✓" on a year-end marital-status ground the plan did not establish

- **First appears: snapshot 4**, case table: "| C3 | Loan from before the
  marriage | ✓ same as C1; marital status tested at year end |".

- **What came before.**
  - Snapshot 2's action 3 said the student relationship is "judged at the
    time the *borrower* took the loan (Reg. §1.221-1(e)(3)(i)(A); Pub. 970)".
  - That itself overstated its sources. The snapshot 2 tool record shows the
    Pub. 970 fetch attaching the time to the dependent only: "a person who was
    your dependent when you took out the loan". The 1040 instructions summary
    says "a dependent (at the time you borrowed the money)".
  - Between snapshots 2 and 4 the tool record shows no source on timing or
    marital status. Snapshot 3 was the probe and fact titles. Snapshot 4 was
    project documents (`whose-deduction-model.md`, the a5 stage files, the
    retrospective).
  - So the "✓" contradicts the plan's own earlier text and has no source
    behind it.

- **Extended?** Only slightly. C3's ✓ joined the list of cases "already
  handled". No decision (D1–D4) depended on it.

- **Corrected: snapshot 5, after reviewer comment 1.**
  - C3 was split into C3a ("?", depends on D1) and C3b ("unresolved").
  - Action 3 was reworded to "for at least the dependent relationship …
    Whether that timing also reaches 'spouse' is open (D5)".
  - D5 was added.

### T2-P2. D5 reclassified from "changes a result" to "changes … whether a stated assumption is honest"

- **First appears: snapshot 7**, action 6: "So the app **already declares**
  the student relationship and the borrower as assumptions it does not test.
  D5 changes the *truth of a stated assumption*, not a computation." The
  working account says: "That moves D5 from 'changes a result' to 'changes
  whether a stated assumption is honest'."

- **What came before.**
  - Snapshot 5's D5 entry: "If it reaches spouse, C3b is **not** qualified."
  - The snapshot 3 probe and the worksheet reads showed every statement's
    box 1 is summed.
  - In snapshot 7 the planner read the shipped `basis` (the "assumed" list).
    That is the source that came just before the error.
  - Nothing read shows that declaring an assumption changes the computed
    figure. My check of the basis agrees: the sentences are listed under
    "assumed", and they gate nothing.

- **Extended into dependent actions.**
  - The D5 row in the snapshot 7 table: "Interim: the assumption sentence
    already carries the reg's reading. The question is whether to keep it, or
    to bound C3b out."
  - The new D2 candidate: "The assumed-basis mechanism is itself a candidate
    for D2: state the joint reading as an assumption rather than represent
    identity."

- **Corrected: snapshot 8, after reviewer comment 2.** The text now reads
  "**D5 is result-bearing** … line 21 is **overstated**". The D5 row and the
  readiness claim changed. What did not change is analysed in section 3.

### T2-P3. "A 1098-E does not identify the obligor," used to weaken one representation and carried into the readiness supports

- **First appears: snapshot 6**, C7 row: "the 1098-E names only the principal
  borrower, so the **named person need not be the obligor who paid**." The
  working account says: "the person named on a 1098-E is the principal
  borrower, not necessarily the obligor or payer."

- **What came before.**
  - Snapshot 2 said "The form names the borrower".
  - Snapshot 1 asked whether the SSA recipient pattern fits "a 1098-E
    (borrower ≠ student, joint borrowers)".
  - In snapshot 6 the planner fetched § 1.6050S-3 and the 1098-E/1098-T
    instructions. The tool-record excerpt does not show the defining sentence.
  - My check on LII: the payor is "the individual who is carried on the books
    … as the borrower", and with multiple borrowers the principal borrower is
    treated as the payor.
  - So the named person is a borrower, and so an obligor. The source supports
    "not necessarily the only obligor, and not necessarily the payer". It does
    not support "not necessarily the obligor".
  - Whether the payer matters was not established either. Trial 2 never
    fetched § 1.221-1(b)(4) (third-party payments). The snapshot 2 regulation
    excerpt covers (b)(1)–(3), (c) and (e)(3).

- **Extended into dependent actions.**
  - Snapshot 6's change of direction: the SSA-1099 recipient precedent "is a
    poorer fit … because a 1098-E names a lender-chosen principal borrower,
    not the person the deduction's tests are about".
  - The D2 row in snapshot 7: "form-named attribution (SSA-style) records the
    principal borrower, not the obligor".
  - Snapshot 8's readiness supports: "So a 1098-E does not identify the
    obligor or payer, and per-person attribution read off the form would
    record the wrong thing."

- **Why it matters.** It affects who may claim, since it is about whose
  obligation a statement shows. It also removes one candidate representation
  from consideration on a premise stronger than the source.

- **Corrected?** No, and no message touched it.

- **Contrast with trial 1.** In snapshot 3, trial 1 made the hedged opposite
  inference ("a 1098-E is furnished to the borrower, so a statement in either
  spouse's name is itself strong evidence that that spouse is obligated") and
  left its use as a question.

---

## 3. Trial 2: the delivered comments

### Comment 1 (after snapshot 4): C3's year-end test versus action 3's origination-time test

**What it exposed.** C3's ✓ rested on a test ("marital status tested at year
end") that the plan had not tied to loan qualification. The plan's own action 3
pointed to a different, origination-time test. The comment asked whether this
was known or chosen.

**Did the planner locate the premise and its stage?** Yes, at both places.

- In the case table (snapshot 4) it named the source of the year-end idea:
  "That is the §221(e)(2)–(3) test, and it governs only the joint-filing
  requirement."
- In the law step (snapshot 2) it said: "Action 3 had also overstated the reg
  as settling the timing for the whole student relationship."
- It answered the question as asked: "I did not *know* … I had *chosen* one
  without saying so."

**Evidence used.**

- One new fetch: the raw text of § 221 from LII. This is the snapshot 5
  `usc221` curl, which pulled (d)(1) and (e)(2)–(3).
- The snapshot 2 fetches of the regulation and Pub. 970, reused.
- The new statement that statute, regulation and Pub. 970 diverge rests on
  that fetched text.

**What changed.**

- C3 split into C3a and C3b.
- The action 3 bullet was reworded.
- D5 was added, with "**To establish:** … preamble to T.D. 9125, a ruling,
  case law or an IRS FAQ. If none, this is an authority question to escalate".
- A process rule: "every ✓ cites the provision it rests on".
- A recheck of C4–C6. C6 was "downgrad[ed] … to 'likely'", although its text
  already said that.
- In snapshot 6, D5 was pursued with a search and The Tax Adviser (2008).

**What did not change.**

- D1–D4, and the "Next" step ("unchanged from snapshot 4").
- C10 (loans for a dependent) was not revisited, though it rests on the same
  timing clause.

**Diagnosis or compliance?** Partly separable. The comment supplied both
quotations and the "know or choose" framing, and the planner's answer echoes
that framing. Several things go beyond the comment:

- naming §§ 221(e)(2)–(3) and 7703 as where the year-end idea comes from;
- the C3a/C3b split, which separates a loan for one's own schooling, where
  timing hardly matters, from a loan for a future spouse;
- the three-way reading of statute, regulation and publication;
- a new primary-source fetch.

These suggest real diagnosis of the mechanism. Two things the records cannot
show: whether the planner would have reached this without the prompt, and
whether "the reg's placement reads most naturally as reaching all three" is an
independent judgment.

### Comment 2 (after snapshot 7): D5's reclassification

**What it exposed.** Snapshot 7 moved D5 out of "changes a result". Snapshot 5
and the probes had already shown that, under one reading, C3b is not qualified
and its box 1 is still counted.

**Did the planner locate the premise and its stage?** Yes.

- It traced the error to snapshot 7's reading of the assumed basis: "I had
  treated declaring an assumption as if it made the result right. It only
  makes a possible error visible."
- It placed the contradiction against actions 4–5.

**Evidence used.** No new sources: "I re-read snapshot 5's D5 entry, the
`rule.sli-statement-loan-support.json` basis, and the snapshot 3/7 probe
results." The tool record agrees. Snapshot 8 has a single edit command and no
reads.

**What changed.**

- The action 6 bullet now says D5 is result-bearing and line 21 is overstated.
  It adds the converse: "If it does not, the result is right and only the
  assumption's wording is too strict."
- The D5 row: "Interim: the assumption sentence already carries the reg's
  reading" was replaced by "the app **overstates C3b and cannot detect it**",
  with options to bound C3b out or declare it.
- The readiness claim names "a possible undetectable overstatement (C3b)".

**What did not change.**

- The bullet "The assumed-basis mechanism is itself a candidate for D2: state
  the joint reading as an assumption rather than represent identity" is kept
  word for word.
- The D2 row still lists "assumed-basis wording" as a rival prototype.
- The correction's own principle (a declared assumption does not make the
  result right) applies to that candidate wherever a joint-return assumption
  could be false. One example is the shipped sentence "The named borrowing is
  indebtedness the taxpayer incurred", read against D1. The planner did not
  carry the principle there.
- The readiness text also misdates its own history. It speaks of "C3 in
  snapshot 5, D5's reclassification in snapshot 8", but the errors were made
  in snapshots 4 and 7 and corrected in 5 and 8.

**Diagnosis or compliance?** Mostly not separable. The comment named the
snapshot 5 text and the probe finding. The planner used exactly those, and
nothing else, to reverse the classification. Its restatement adds little the
comment did not imply. The untouched D2 candidate leans toward a local
correction rather than a diagnosis applied across the plan. The closing
generalization ("two of my corrections had the same shape") is reflective, but
nothing dependent changed because of it.

---

## 4. Candidate episodes considered and rejected

1. **Trial 1, snapshot 6, "No page asks the obligation, dependency or scope
   questions".**
   - The planner's grep was cut short by `head`, so the evidence was thin.
   - My own grep of the application copy found no person-facing text posing
     these answers outside rule, bundle and package content and sample data.
     The claim holds.
   - Trial 2 reached the same finding in snapshot 3.
2. **Trial 1, snapshot 3, "a 1098-E is furnished to the borrower … strong
   evidence that that spouse is obligated".** It was hedged as a question
   about grounds and not used in the claim. The § 1.6050S-3 text supports it.
3. **Trial 1, snapshots 3 and 5, § 152(b)(2) "from memory" (married-dependent
   bar).** It is accurate (trial 2 fetched it in snapshot 6), and trial 1
   kept the question anyway. Nothing consequential rests on it.
4. **Trial 1, snapshot 3, the related-person witness "worded 'the filer'".**
   - In my check, the title does not say "the filer". It describes the box 1
     content.
   - This is a wording imprecision. The consequential part is covered in
     T1-P1 and T1-P2.
5. **Trial 1, snapshots 2 and 7, "Nothing about amounts … needs to change"
   for the arithmetic itself.** It is supported by § 221(b) and the probe. The
   overreach is the completeness part, counted in T1-P1.
6. **Trial 2, snapshot 3, "already computes a correct figure when every answer
   is truthfully 'yes' for the household".** It is true for the case probed
   (each spouse's own schooling). C3b was later carved out explicitly.
7. **Trial 2, snapshot 3, the dependency answer "mostly matters for wording …
   not the amount".** It was flagged "not verified" and then verified in
   snapshot 6.
8. **Trial 2, snapshots 4 and 6, C6 and C7 ("one statement" and "no double
   count").** These were flagged as inference or unverified and then grounded
   in § 1.6050S-3. Residual risks are named.
9. **Trial 2, the related-person question on a joint return (whose
   relatives?) is never raised.**
   - It would be an omission against the snapshot 8 claim that "the mechanics"
     are understood.
   - I rejected it as not consequential. 1098-E issuers are lenders in a trade
     or business, and trial 2 had recorded related-person loans as "Exotic for
     1098-E lenders" (snapshot 2).
   - D1 ("what 'the filer' means") would reach it in any case.
   - By the same reasoning, the related-person part of T1-P1 is the weaker
     half of that problem. The 2b half carries it.
10. **Trial 2, snapshot 6, "one 1098-E per loan" and the use of the 2026
    1098-E instructions.** These are minor imprecisions with no effect on
    amount or claimant.
11. **Trial 1, snapshot 4, A's cost premise ("descriptions sit in adopted
    bundles").** It was hedged ("likely") and checked in snapshot 6. It
    affects cost only.
12. **Trial 1, snapshot 2, "a loan for either spouse's schooling qualifies on
    the joint return".** The same snapshot opens 2b on exactly this point, so
    I did not count it separately from T1-P1.

---

## 5. What the records do not let me determine

- **Full fetched text.** Tool-record excerpts are cut short, and several web
  results are model summaries. I cannot see exactly what the planners read.
  Examples: the defining sentence of § 1.6050S-3 in trial 2 snapshot 6;
  whether Topic 456 actually lacks "or your spouse" for obligation (trial 1,
  snapshot 5); the Pub. 970 dependency wording trial 1 quotes in snapshot 2.
- **Reasoning between tool calls.** I cannot see why a planner wrote a
  specific sentence. Examples: trial 2's snapshot 4 ✓ on C3, and trial 1's
  "the one place".
- **Counterfactuals.**
  - Whether trial 2 would have corrected C3 or D5 without the comments.
  - Whether trial 1 would have caught T1-P1 had it received a similar comment.
  - Trial 1's uncorrected parallel error is suggestive, but the planners are
    separate sessions and the errors are not identical.
- **The reviewer's coverage.** What the reviewer considered and chose not to
  raise, and why. T2-P3, for example, went unremarked.
- **The underlying law.** Whether 2a/D1 (obligation across joint filers) or
  2b/D5 (timing for "spouse") has a deciding authority. Neither planner found
  one. I did not research them, so I cannot say how large the overstatement
  risk in T1-P1 and T2-P2 really is.
- **Whether "filer" or "person" is defined in `docs/governance/`.** It was
  barred to both planners, and I did not read it. Either term could affect
  D1 and 2a.
