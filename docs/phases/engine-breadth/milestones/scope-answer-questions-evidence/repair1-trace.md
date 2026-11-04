# Repair 1 trace: what the rules and the form text say, before the wording

Source: committed content and milestone plans only (the form text the repo quotes). Where the repo's sources do
not settle a point, it says so and the wording follows the rule.

## S1A: "lines 24a through 24z", and what the twelve facts cover

- `rule.schedule1-line26` (notes): "Add lines 11 through 23 and 25" (`f1040s1.pdf` p.2). The twelve facts are
  `no-line{11,12,13,14,15,16,17,18,19,20,23,25}`; "the 25 absence [is] already subsuming the 24a-24z detail".
- `f1098e-student-loan-interest-agi.md` T0-6: line 22 is a structural zero (reserved); lines 24a-24y have no fact of
  their own; `fact-type-succession-neutral-schedule1.md`: "No Schedule 1 line 21 member exists. Student-loan interest
  is not among the twenty-three"; line 21 is computed by `rule.sli-worksheet`, so a "yes" the engine cannot record
  for it would leave a computable return blocked.
- Settled by the repo: the last item is "any other adjustment listed on Schedule 1 lines 24a through 24z", and the
  sentence must say student loan interest is not counted. Not settled here: what each of 24a-24y is (the repo never
  lists them); the sentence does not try to.

## L2A2: Form 1099-OID

- Reader: only `rule.form1040-line2a`, as an unconditional "yes" (the residual scope, P5 of
  `form1099int-box8-line2a.md`).
- `form1099int-box8-line2a.md` lines 188 and 222: the excluded thing is "Form 1099-OID tax-exempt stated interest or
  tax-exempt OID" ("Form 1099-OID boxes 2 or 11 and all tax-exempt OID"). Taxable OID (box 1, box 5) is a separate,
  recorded family (`f1099oid.box1-interest-oid`, `f1099oid.box5-market-discount`) and line 2b, not this fact.
- So the P0 sentence ("tax-exempt interest or original issue discount on a Form 1099-OID") was ambiguous: an
  ordinary taxable OID statement does not make this fact "no". Word it "tax-exempt interest or tax-exempt OID shown on
  a Form 1099-OID".
- The same group holds `no-unreported-tax-exempt` (tax-exempt interest on no form) and `no-premium-adjustment` ("tax-exempt
  bond-premium or acquisition-premium adjustment", line 211: such adjustments change the amount reported on line 2a).

## L2A3: what "consumes" tax-exempt interest

- Readers of all four facts (`no-amt-form-6251`, `no-credit-using-tax-exempt`, `no-deduction-using-tax-exempt`,
  `no-child-income-election`): only `rule.form1040-line2a`, unconditional "yes".
- The repo names the consumers only by class: "Form 6251 or general AMT computation" and "taxable Social Security,
  child-income elections, credits, or deductions that consume tax-exempt interest" (non-goals). It never lists which
  credits or deductions, and it does not say the child-income election is Form 8814 (the Earned Income Credit plan
  lists Form 8814 among its own Worksheet 1 items). **Not settled by the repo's sources.** The sentence therefore
  says what the rule reads (a credit or deduction that counts tax-exempt interest as part of income) and gives no
  invented examples; "Form 8814" is kept as the form on which a parent elects to report a child's interest and
  dividends, the one reading of "child-income election" the repo's other plans support.

## FTC12: Schedule 2 lines

- Fact `no-schedule2-regular-tax-add`: "Schedule 2 line 1a/1z amounts that would change regular tax for the credit
  cap are absent". Reader: `rule.schedule3-line1-direct-ftc` v3, in a `conditional_dependency_set` active only when
  the box 7 total is more than $0; the cap is min(box 7 total, line 16 tax), and the plan states bounded regular tax
  "equals line 16 when Schedule 2 line 1a/1z and Form 4972 tax are explicitly absent".
- The repo quotes two sources that disagree on the line: Form 1116 line 20 instructions, "Form 1040 line 16 +
  Schedule 2 Part I line 1z, less any Form 4972 tax" (`form1099div-box7-direct-ftc.md` line 193), and the
  "Foreign Tax Credit - How to figure the credit" page, "Form 1040 line 16 + Schedule 2 line 1a" (line 229). The
  fact and the plan treat them as one thing, 1a/1z. **Not settled further by the repo's sources** (they never describe
  what is on lines 1a through 1z). The sentence names both lines, as the fact does: "an amount on Part I line 1a or
  line 1z (an addition to your regular tax)".

## DEP1: "can be claimed" versus "is claimed"

- `standard-deduction.can-be-claimed-as-dependent`: "someone else can claim the taxpayer, or the spouse on a joint
  return, as a dependent" (`rule.form1040-standard-deduction`: yes -> Dependents Worksheet line 4c).
- `sli-scope.not-claimed-as-dependent`: "the filer is not claimed as a dependent by another taxpayer" (Pub. 970 p.33
  Example 2: "neither you nor your parents may deduct"), filer only. `senior-and-dependent-deductions.md` ("Parked by
  this milestone") already records that the SLI fact asks whether the filer "is claimed", where the law and the new
  answer say "can be claimed", including the spouse; the engine-breadth roadmap parks it.
- The two facts therefore do not mean the same thing. DEP1 splits: DEP1 keeps "can someone claim you (or your spouse,
  on a joint return)" for the standard deduction fact; DEP2 asks "is someone claiming you" for the SLI fact. 41
  filer questions.
