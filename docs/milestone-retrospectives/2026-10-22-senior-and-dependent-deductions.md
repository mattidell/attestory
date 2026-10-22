# Retrospective — The 2025 Senior Deduction and a Dependent's Standard Deduction

## Result

- **The enhanced deduction for seniors computes on core v51.** Schedule 1-A
  Part V is published line by line (33-37) and reaches Form 1040 line 13b:
  $6,000 for each taxpayer or spouse aged 65 or older with a valid SSN,
  reduced by 6 percent of AGI above $75,000 ($150,000 joint), $0 when married
  filing separately, whether or not the return itemizes. A single filer aged
  65 or older with $50,000 of wages had $0 on line 13b; the law gives $6,000.
- **A dependent's standard deduction computes on line 12e.** The dependents'
  worksheet is published line by line (1-4c). A single dependent with $3,000
  of wages gets $3,450 instead of $15,750.
- **Four new questions, each read by exactly one rule family.** Whether
  someone can claim the taxpayer or spouse, whether the return claims none of
  the tips, overtime or car loan deductions, and a valid SSN for each person
  aged 65 or older, asked only where it can change the result.
- **No schema, expression operation or engine change.** Earlier packages and
  their goldens are unchanged.

## What the evidence changed

- **P0 showed the existing Schedule 1-A answer could not stay.** It was one
  yes/no for all of Schedule 1-A; a senior answering truthfully was blocked.
  It was replaced by an answer scoped to Parts II-IV.
- **P0 traced an assertion end to end before anything was built.** Fact type,
  recorded act, package binding and rule reference are all generic, so the
  milestone was content only. The conditional SSN requirement used the
  existing `conditional_dependency_set` operation.
- **The worksheet's $900 test is a larger-of.** Earned income is over $900
  exactly when earned income plus $450 is over $1,350, so line 2 needs no
  threshold and no strict-comparison boundary.
- **The age question's wording does not match its law.** "Over 65 years of
  age" can exclude someone who turned 65 during 2025; both consuming rules
  mean born before January 2, 1961. The fact was kept and the wording parked.

## Process

- **A size flag found a defect.** Standard deduction v3 first copied v2's
  formula into its non-dependent branch (8.8KB). Reviewing why exposed that
  worksheet line 1 counted the spouse's boxes on every return while v2 counted
  them only on married and surviving-spouse returns. Gating line 1 like v2
  made the regular deduction exactly line 3 plus line 4b; v3 shrank to 4.5KB,
  and a test proves the identity against v50 for every filing status.
- **The final review found two legibility defects.** The dependent fact
  type's title still said no rule read it, and worksheet line 1 was 5.6KB.
  The Foreman corrected the title and wrote line 1 with one spouse-box test
  (4.3KB) before the PR was marked ready.
- **One builder session ran every unit.** P0, both tracks, the repair and the
  goldens resumed the same Sonnet builder, so no unit re-derived the input
  path.
- **Charters said the worktree is supplied at launch.** No unit used
  `--no-verify`. The first Track 1 commit carried session trailers; curation
  removed them.

## What it cost

All units ran on one Sonnet builder sub-agent: P0 about 11 minutes (100 tool
calls), Track 1 about 20 minutes (118), Track 2 about 8 minutes (54), the
line 1 and v3 repair about 13 minutes (77), and the goldens about 18 minutes
(105). The final review ran on a fresh Sonnet reviewer.

## Follow-ups

- The age questions' wording: born before January 2, 1961, and a death in
  2025 before age 65.
- `tax.us.2025.sli-scope.not-claimed-as-dependent` asks whether the filer "is
  claimed"; the law and the new answer say "can be claimed", including the
  spouse on a joint return. Two answers now carry one concept.
- Schedule 1-A Parts II-IV (tips, overtime, car loan interest) remain
  declared absent.
- Worksheet lines as presentation rows, verified ids for the capital-loss and
  Social Security amounts, and citation artifacts for statutes and revenue
  procedures carry over from the previous milestone.
