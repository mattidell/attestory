# Retrospective: Questions Say What Their Rules Read (2025)

Milestone key: question-wording. Plan:
`docs/phases/engine-breadth/milestones/question-wording.md`.
Closed 2026-11-11. Core v87, registry v85, release v85: content only.

## What happened

Three parked wording items came in together: the wash-sale adjustment
amount questions asked of every covered sale, the Exception 1 words invited
a yes beside a zero-net sale, and the age and student-loan dependency words
did not match the 2025 rules. P0 found every item content only and the 298
recorded returns identical on v86 and a scratch v87. Track 0 passed on all
six tables. It also surfaced two limitations the words cannot fix (a
recorded wash sale with only the adjustment family open asks nothing; age
and blindness are never asked). The foreman disposed both as outside the
milestone under the owner's standing grant, and they are parked.

Track 1 built core v87. The fresh review then found the new Exception 1
words wrong for a large population: "did not sell ... other property"
caught personal-item losses and sales inside an IRA, which need no Schedule
D, so a truthful filer answered no and was blocked with no question. The
repair limited the clause to reportable sales. The repair's own extra
sentence ("losses on personal items do not count") contradicted the Form
1099-K and 1099-S reporting rule; the builder flagged it, and the re-review
found that a Form 1099-K loss may also go on Schedule 1. The final words
count a personal-item loss only with a Form 1099-S or when reported on
Form 8949.

P0 started on grok, whose balance ran out mid-unit; Opus sub-agents
finished P0, Track 1 and the first repair. The owner then directed no
Opus or Sonnet fallback when grok is at its limit, and grok finished the
remaining repairs and re-reviews.

## What worked

- Running each sentence through the real coordinator as a truthful filer
  would read it. Every wording defect was found that way, not by reading.
- Regenerating the branch-only v87 members in place, since none had
  reached a ratified line.

## What to change

- A question's words are a population claim. Before deciding words, list
  who is asked and every way a truthful member of that population could
  read each clause, including the things the law excludes (IRA sales,
  personal-use property, alternative reporting places).
- A foreman's charter wording is a claim too. The extra sentence in the
  repair charter introduced the second defect; quote the instruction first,
  then write the words from it.

## Follow-ups

Parked in the roadmap: the wash-sale page that asks nothing, and the false
(now also truthful) Exception 1 "no" that refuses with no question. Age and
blindness being asked is the next milestone (age-blindness-asked).
