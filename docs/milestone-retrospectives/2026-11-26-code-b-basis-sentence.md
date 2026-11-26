# Retrospective: The Code B Wash-Sale Explanations Name the Correct Basis

Milestone key: code-b-basis-sentence. Plan:
`docs/phases/engine-breadth/milestones/code-b-basis-sentence.md`.
Closed 2026-11-26. Core v108, registry v106, release v106.

## What happened

sale-explanation-wording parked SEW-F2: the two code B wash-sale
explanations read the correct basis the filer entered but told them to
check only box 1d and box 1g. The plan fixed the sentence and one build
track published v3 of the four explanations, reusing the #313 build and
replay scripts by import. The replay passed with only the declared
sentence and version moves. The fresh review was READY and found that box
1g itself may be figured from the wrong basis (CBB-R1), which predates the
milestone and is parked.

## What worked

- Importing the previous milestone's build and replay scripts instead of
  copying them made a content successor a short, checked track.
- Having the reviewer put its report in its final message, not a file,
  avoided the stalled write seen in same-label-members.

## What to change

- The plan's wording decision checked the sentence against the block's
  rule but not against how the broker figures box 1g. Read each box the
  sentence names against how it is filled, not only against the rule.
