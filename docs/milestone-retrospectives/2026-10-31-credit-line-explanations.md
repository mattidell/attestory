# Retrospective — Each Credit Line Explains Itself (2025)

## Result

- **The child tax credit lines explain themselves on core v64.** Form 1040
  lines 19 and 28, Schedule 8812 lines 4, 14, 17 and 20 and Credit Limit
  Worksheet A line 5 had carried line 27a's earned income credit texts since
  core v55: line 19 told a reader it was "the earned income credit from
  Worksheet A line 6". Each now explains its own line in every disposition.
- **No value changed.** Seven form-field successors; no rule, code or schema
  change.
- **A copied explanation now fails a test,** whether it names another line
  or repeats another field's text.

## What the evidence changed

- **"Not wrong" is not "accurate".** The first successors named the right
  line but described line 19 as the child tax credit alone; the review read
  the rules and found it is both credits. Texts were then written from the
  rule, not the label.
- **A survey tuned to its known answer misses the next one.** The first rule
  flagged 52 fields and was narrowed until it returned exactly the seven;
  the review planted a copy that the narrowed rule missed. Comparing texts
  across fields catches what pattern rules do not.

## Process

- No P0: the defect and the fix were read directly from content. One build,
  one review, one repair, all Sonnet 5.5.
- Stacked on #235 by owner direction; this package is core v64.

## Follow-ups

- Generic form-field texts ("blocked", closed-empty boilerplate on
  arithmetic lines) and blocked texts that never name the missing input
  (parked).
