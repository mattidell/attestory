<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "sale-explanation-wording",
  "status": "Open 2026-11-25. Track 1 next.",
  "retrospective": null,
  "scope": [
    "the 30 sale-family block explanations (ADR 0088) read plainly on first read: what is wrong with this sale, then what to do, in the filer's words",
    "the 8 sale wash-sale adjustment questions read plainly and ask one thing",
    "every recorded return keeps its numbers, dispositions and block codes"
  ],
  "non_goals": [
    "no schema, projection, engine or kernel change; content successors only",
    "no change to when a sale blocks or to which question a block links",
    "no edit to any published file; new versions only",
    "the family version pin and the all-or-none package rule stay parked (roadmap)"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/sale-explanation-wording.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/sale-explanation-wording.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/sale-explanation-wording.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-24-sale-block-explanations.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# The Sale Block Explanations Read Plainly (2025)

Milestone key: sale-explanation-wording.
Branch: milestone/sale-explanation-wording-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-25.
Starting point: main at `edca594e` (core v106 or later as published there).
Expected target: the next core version, registry and release, content only.

## What we are trying to accomplish

sale-block-explanations (ADR 0088) replaced engine text on 30 sale block
reasons with IRS-grounded sentences. They are correct but hard to read on
first look: two clauses joined by a semicolon, a formula in parentheses,
and inverted phrases such as "a wash-sale loss disallowed was entered".
The foreman's ADR 0088 review asked for a wording pass held to the bar
eic-separated-married met for its question text. The six wash-sale
adjustment questions that milestone adopted, and the two code B ones,
have the same problem ("the nondeductible wash-sale loss in box 1g of
Form 1099-B (or the correct disallowed wash-sale loss, or 0 if none)").

## Wording bar

Each explanation:

- speaks to the filer ("you entered", "this sale"), in at most two short
  sentences: first what is wrong with this sale, then what to do;
- names the form and box the filer can look at (box 1g, box 2, column (g))
  and no engine word (family, member, block, code names, floor, fact);
- has no formula or parenthetical aside; "basis" and "proceeds" may appear
  once each with the form box that shows them;
- stays true to the 2025 Form 8949 and Schedule D instructions, cited in
  the evidence by section;
- is identical across the short-term and long-term families wherever the
  rule is identical, and differs only where the form differs (Form 1099-B
  box versus column (g), corrected basis for code B, net proceeds for
  sales without a Form 1099-B).

Each question asks one thing, names where the number is, and says what to
do when there is no number. It says 0 only where 0 is a valid answer
(Decision 1).

## Stages

1. **Track 1 (build).** First check that adopting a new version of a
   `family-block-explanation` or an `input-question` citizen unpins no
   saved record and changes no number; stop and report if it does.
   Then write the wording to the bar, publish the successors in the next
   core, registry and release, and prove with a full-surface replay that
   only the explanation and question text moved.
2. **Fresh review** against the wording bar and the IRS instructions,
   repair, closeout, final review, merge.

## Track 1 result

Built on `milestone/sale-explanation-wording-2025`. See
[sale-explanation-wording-evidence/track1.md](sale-explanation-wording-evidence/track1.md)
and [wording.json](sale-explanation-wording-evidence/wording.json).

- **Safety check passed.** No recorded act names an explanation or
  input-question citizen. Saved records pin bundles, fact types and
  families, and none of those move. A scratch v107 that adopts v2 of one of
  each replays all 775 recorded lists against v106: 775 passing, 0
  unexpected, outcomes unchanged.
- **Published core v107, registry v105, release v105.** 30
  `family-block-explanation` and 8 sale adjustment `input-question` v2
  successors carry the new sentences, and nothing else moves. Loader
  entries carry v106's.
- **Only words moved.** The full-surface replay of v106 against published
  v107 passes 775 of 775 lists with 0 unexpected differences. It finds no
  number, disposition, block-code or question-target change. Sentence
  replacements (2,405 in 46 lists) and the reason order that follows from
  them are checked by substitution, not blessed by position.
- **Tests.** A fast package and wording-bar test and a live test cover all
  38 synthetic cases and a rendered page.

## Repair 1

The fresh review found SEW-R1 to SEW-R7. The foreman's Decisions 1 to 3
below govern R2, R5 and the accepted reviewer text. Core v107 had not
merged, so its v2 citizens, registry v105 and release v105 were regenerated
in place by `build.py`, with no v3. The package's member pins did not
change.

- **R1** (code B condition). Both code B pairs now say the sale has no loss,
  or lost less, "with the correct basis you entered".
- **R2** (blank box 1g). Applied Decision 1. The covered wash-sale question
  now says that if box 1g is blank, change your answer that it shows one.
  Both box 1g explanations give that same instruction for a blank box 1g.
  The question bar is restated above.
- **R3** (box 12). The sentence starts from the filer's answer ("You said
  your broker reported this sale's basis to the IRS") and gives both ways
  out: box 12 checked, or change the answer.
- **R4** (noncovered question). Uses the reviewer's text: "How much of this
  sale's loss does a wash sale disallow? Use box 1g of your Form 1099-B if
  it shows an amount. If there is none, enter 0." The short-term and
  long-term questions are now identical.
- **R5** (holding period). Applied Decision 2 to all three Form 1099-B
  groups.
- **R6** (who fixes what). The check sentence compares "what you entered"
  with the form boxes and ends "fix whichever amount you entered
  differently". Where the filer supplies the amount with no form box, it
  ends "fix whichever of your entries is wrong".
- **R7** (controls). `replay.py --controls` now writes
  `controls-v107.json`. On four lists the real comparison passes, and both
  the wrong-sentence and the no-substitution controls fail.

The fast wording test also requires each "basis" or "proceeds" to sit next
to a box, a column, "you entered" or "you said". It allows up to three
sentences in a question (Decision 1's text has three) and pins Decision 1.
The replay was re-run on v106 against the regenerated v107: 775 of 775
passing, 0 unexpected, no number, disposition or block-code change.

## Decisions

1. **SEW-R2 (foreman).** A covered sale is in the wash-sale group only when
   box 1g is marked, so a blank box 1g means the answer is wrong, not 0.
   The covered wash-sale question is: "What is the wash-sale loss
   disallowed in box 1g of your Form 1099-B for this short-term or
   long-term sale? If box 1g is wrong, enter the correct amount. If box 1g
   is blank, change your answer that it shows one." The two box 1g
   explanations give the same instruction for a blank box 1g. Bar: a
   question says what to do when there is no number, and that is 0 only
   where 0 is valid.
2. **SEW-R5 (foreman).** All three Form 1099-B groups use: "Check box 2 of
   your Form 1099-B, if it is filled in, and the dates you acquired and
   sold it, since a sale held more than 1 year is long-term."
3. **Reviewer text accepted (foreman).** R1 (the correct-basis condition in
   both code B pairs), R3 (box 12 starts "You said your broker
   reported..." and adds the way out), R4 (the noncovered question text)
   and R6 ("fix whichever amount you entered differently", reworded so the
   filer fixes their own entry).
