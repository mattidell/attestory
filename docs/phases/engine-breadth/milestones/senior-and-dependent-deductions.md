<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "senior-and-dependent-deductions",
  "status": "P0 complete; contract settled. Track 1 builds the senior deduction on core v51.",
  "scope": [
    "compute the 2025 enhanced deduction for seniors (Schedule 1-A Part V) and carry it to Form 1040 line 13b, as successor content",
    "compute a dependent's limited standard deduction on line 12e when someone can claim the taxpayer or spouse as a dependent",
    "ask only the questions those rules read, each with a meaning that matches its consuming rule",
    "keep earlier packages, saved presentations and their goldens unchanged"
  ],
  "non_goals": [
    "no deduction for qualified tips, overtime or car loan interest (Schedule 1-A Parts II-IV); they stay declared absent",
    "no Puerto Rico exclusion, Form 2555 or Form 4563 in modified AGI; returns that need them stay outside the supported class",
    "no new income source, form or attachment; earned income for the dependent worksheet comes only from income the engine already computes",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction",
    "no edit to any published schema, adopted package, parameter or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/milestone-retrospectives/2026-10-22-tax-on-taxable-income.md",
      "docs/phases/engine-breadth/milestones/senior-and-dependent-deductions.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/senior-and-dependent-deductions.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/senior-and-dependent-deductions.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-22-tax-on-taxable-income.md",
      "docs/phases/engine-breadth/milestones/senior-and-dependent-deductions.md",
      "docs/phases/engine-breadth/coverage-frontier.md"
    ]
  }
}
-->

# The 2025 Senior Deduction and a Dependent's Standard Deduction

Milestone key: senior-and-dependent-deductions.
Branch: milestone/senior-and-dependent-deductions-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-22.
Starting point: `origin/main` at `2bcff400` (PR #217 merged). Runs in parallel
with the mortgage same-borrowing milestone (PR #216); whichever merges second
takes the next free package, registry and release versions.

## What we are trying to accomplish

The last milestone made line 16 and the standard deduction follow 2025 law,
and named two deductions it did not compute:

- **The enhanced deduction for seniors.** For 2025 through 2028, each taxpayer
  or spouse born before January 2, 1961 with a valid SSN may deduct up to
  $6,000, reduced by 6 percent of modified AGI above $75,000 ($150,000 for a
  joint return). Married taxpayers must file jointly. It is Schedule 1-A
  Part V, and its total reaches Form 1040 line 13b through Schedule 1-A
  line 38. It applies whether the return itemizes or not.
- **A dependent's standard deduction.** When someone can claim the taxpayer
  (or the spouse on a joint return) as a dependent, line 12e is the
  dependents' worksheet: the larger of $1,350 or earned income plus $450,
  capped at the basic standard deduction, plus the age and blindness
  additions.

Today line 13b is zero by a mandatory assertion that the return has no
Schedule 1-A deduction at all. A taxpayer aged 65 or older who answers that
question truthfully is outside the supported class; one who answers it
carelessly loses up to $6,000 ($12,000 joint). Line 12e gives a dependent the
full standard deduction because nothing asks whether someone can claim them.
The useful outcome is that both returns compute correctly, each from a
question whose meaning matches the rule that reads it.

No new return class becomes computable beyond those two populations, and no
earlier result changes.

## What we know

- **Law (downloaded, ignored under `temp/tax-on-taxable-income/sources/`).**
  Schedule 1-A Part V lines 31-37 and Part VI line 38 (`f1040s1a-2025`); its
  instructions on page 110 of the 2025 Form 1040 instructions (`i1040gi-2025`,
  "Enhanced Deduction for Seniors": valid SSN, joint filing, death in 2025
  before age 65, MAGI is Part I line 3); the Standard Deduction Worksheet for
  Dependents and its earned-income footnote (`i1040gi-2025`, line 12e);
  Pub. L. 119-21 (`publ119-21`).
- **Engine.** Core v50's standard deduction rule v2 reads
  `taxpayer_over_65`, `spouse_over_65` and the two blindness facts, which
  workspaces record as assertions. `rule.form1040-line13b` v1 is zero when
  `tax.us.2025.schedule1a.no-additional-deductions-declared` is "yes" and
  blocks otherwise. `rule.form1040-line14` v1 adds lines 12e, 13a and 13b;
  line 15 v2 subtracts line 14 from AGI. Nothing records a valid SSN or that
  someone can claim the taxpayer or spouse.
- **What we do not know.** Whether the recorded age-65 assertion means
  "born before January 2, 1961" as both the standard deduction and Part V
  read it; how a new assertion reaches a rule on the real path (question,
  act, resolution, marshalling); whether the dependent worksheet's earned
  income reduces to line 1z for every route the engine computes, or which
  Schedule 1 earned-income lines can appear; how line 34's 6 percent product
  rounds; and whether the old Schedule 1-A absence assertion can remain or
  needs a narrower successor covering only Parts II-IV.

## Actions the team will take

1. **P0 — verify and trace.** Record each 2025 amount and condition with its
   citation. Trace the age-65 assertion from question to the standard
   deduction rule on the real coordinator, and say exactly what adding a new
   assertion (valid SSN, can-be-claimed) takes on that path. Inventory the
   earned-income components the dependent worksheet would read and which the
   engine can produce. Hand-compute the case table below. No content changes.
2. **Decide.** Settle the contract here: new fact types and their question
   wording, the successor to the Schedule 1-A absence assertion, rule ids and
   versions, rounding, and compatibility for saved history. A new expression
   operation, schema successor or owner-visible choice returns to the owner
   first.
3. **Track 1 — the senior deduction.** Fact types, one rule per Schedule 1-A
   Part V line, successor line 13b, one successor package, registry and
   release, and cases through the real path.
4. **Track 2 — the dependent's standard deduction.** Fact types, the
   dependents' worksheet as rules, a successor standard-deduction rule, and
   cases through the real path, on the same successor package if Track 1 has
   not been published, or the next one.
5. **Close.** Fresh-reader review of the curated candidate, the full lane
   before ready, exact-head CI, retrospective, coverage-frontier and parked
   list.

## Cases that will shape the design

- Single, 66, AGI $60,000: $6,000. Single, 66, AGI $95,000: $4,800. Single,
  66, AGI $175,000: $0.
- Joint, both 65 or older, AGI $160,000: $5,400 each, $10,800. Joint, one
  spouse 65 or older: one amount. Joint, both 65 or older, one without a valid
  SSN: one amount.
- Married filing separately, 66: $0.
- Itemizing return with a 66-year-old: the deduction still applies.
- Dependent, single, wages $3,000: $3,450. Wages $500: $1,350. Wages $20,000:
  $15,750. Dependent, 66 and blind, wages $3,000: $3,450 plus two additional
  amounts.
- A return answering none of the new questions on a successor package is
  blocked with the missing facts named, never a silent zero.
- Every existing golden keeps its package and its result.

These figures are the Foreman's reading of the forms. P0 recomputes them from
the sources and corrects any that are wrong.

## P0 result

P0 is complete ([law and path](senior-and-dependent-deductions-evidence/p0-law-and-path.md)).
Every case figure above is confirmed; the dependent aged 66 and blind with
$3,000 of wages is $7,450 ($3,450 plus two $2,000 single additional amounts).

- **No schema successor, expression operation or engine change is needed.**
  An assertion reaches a rule through a fact type, a recorded act, the
  package's `input_bindings` and the rule's `ref`; all of it is generic. New
  questions are content.
- **The Schedule 1-A absence answer cannot stay.** It covers Parts II-V in one
  yes/no, and a senior must answer "no", which blocks. A narrower answer for
  Parts II-IV is needed.
- **The 2025 standard deduction parameters already hold the worksheet's line 3
  and line 4b amounts.** They are reused.
- **Earned income is line 1z on every route the engine computes.** Every other
  component in the worksheet footnote is declared absent before line 10 or 26
  can compute.
- **The probe shows the gap.** A single filer aged 65 or older with $50,000 of
  wages gets $17,750 on line 12e and $0 on line 13b; the law gives $6,000 on
  line 13b.
- **The age question's wording is loose.** `tax.us.2025.taxpayer-over-65` is
  titled "over 65 years of age"; both the standard deduction and Part V mean
  born before January 2, 1961, which includes everyone who turned 65 during
  2025. The meaning both rules read is the same, so this milestone keeps the
  fact and parks the wording with the question surface.
- **The law is silent on a dependent claiming the senior deduction.** Nothing
  bars it; the engine allows it.
- **Line 34 has no rounding step of its own.**

## Contract

1. **New questions** (one `fact-type.v2` bundle, `yes`/`no`, no default):
   - `tax.us.2025.senior-deduction.taxpayer-valid-ssn` and
     `tax.us.2025.senior-deduction.spouse-valid-ssn`: the person has a social
     security number valid for employment, issued before the due date of the
     2025 return including extensions.
   - `tax.us.2025.standard-deduction.can-be-claimed-as-dependent`: someone
     else can claim the taxpayer, or the spouse on a joint return, as a
     dependent for 2025. One answer for the return, because the worksheet
     governs the whole joint return if either spouse can be claimed.
   - `tax.us.2025.schedule1a.no-parts-ii-iv-deductions-declared`: the return
     claims no deduction for qualified tips, qualified overtime compensation
     or qualified passenger vehicle loan interest.
2. **A question is required only where its answer can change the result.**
   The dependent and Parts II-IV answers are required on every return that
   adopts the successor package. A valid-SSN answer is required only for a
   person recorded as 65 or older, and the spouse's only on a joint return; a
   return with no such person computes without it. A missing required answer
   blocks with the fact named, never a silent zero.
3. **Senior deduction, one rule per Schedule 1-A line.** Line 31 is AGI.
   Lines 32-37 are rules with three cited parameters: the $6,000 amount, the
   $75,000 / $150,000 threshold by filing status, and the 6 percent rate.
   Line 34 is the exact product; nothing rounds that the form does not round.
   Married filing separately is $0 at lines 36a and 36b. Line 13b's successor
   is line 37 when the Parts II-IV answer is `yes`.
4. **Dependents' worksheet, one rule per line.** Line 1 counts the four age
   and blindness boxes. Line 2 is the larger of $1,350 or line 1z plus $450,
   which is the worksheet's $900 test exactly. Line 3 reuses
   `standard-deduction-base`, line 4b reuses `additional-standard-deduction`,
   and 4a and 4c follow the form. Two cited parameters hold $1,350 and $450.
   The standard deduction's successor is line 4c when the dependent answer is
   `yes`, and today's computation otherwise.
5. **Successor content only.** One core-calculations package, registry and
   release (v51, v49 and v49 unless PR #216 merges first), an adoption fixture
   and new goldens. Earlier packages, saved presentations and goldens stay
   byte-identical.
6. **Data safety.** Any statutory parameter with a six-digit amount gets a
   cited per-id exemption in the data-safety gate. The full lane runs before
   the PR is marked ready.

## Parked by this milestone

- The age questions' wording (born before January 2, 1961, and a death in
  2025 before age 65) on the question surface.
- `tax.us.2025.sli-scope.not-claimed-as-dependent` asks whether the filer "is
  claimed", where the law and the new dependent answer say "can be claimed",
  including the spouse on a joint return. Two answers now carry one concept.
