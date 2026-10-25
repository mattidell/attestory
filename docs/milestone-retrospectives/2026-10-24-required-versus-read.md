# Retrospective — Every Required Answer Is Read

## Result

- **Measured, not assumed.** In the latest core package one rule
  (`form1040-line16` v6) requires two inputs its expression never
  references, and 33 rule versions require an input that some published
  finding did not read: 8 by-design compiler gates and 25 over-declared
  derived or return-level inputs. None of the rows examined is a question
  that cannot change its result or a correction hazard; the 25 over-declared
  rows were classified by their shape, not each traced.
- **A static check gates CI** in the fast lane: every required symbol must be
  referenced by its rule, or be in a committed allowlist with a reason.
- **The path scan is a tool,** `tools/required_versus_read.py path`, with a
  seeded test that it reports an answer read only on an untaken branch and
  does not report it once the branch is taken.
- No production engine, content, schema or rule-language change.

## What the evidence changed

- **The problem was smaller than the earned income credit reviews
  suggested.** Their three defects were caught and repaired; the corpus has
  none left. The check's value is prevention.
- **A runtime probe over tests measures coverage too.** `eic-early-stop` v2
  shows its answer "never read" because no v54 test takes the branch that
  reads it, and `form1040-line16` v6 left the capital-gains worksheet's
  line 25 unread on 122 findings from 89 tests. A gate on the path scan would fail on coverage gaps as
  often as on content.
- **Two "misleading questions" were over-declarations.** The builder flagged
  `eic-early-stop` v2 and `f1098-line8a` v2; one requires a derived symbol
  and the other a document field, neither a question a person answers.

## Process

- First milestone on Haiku 5.5 builders (P0 and Track 1). The scans were
  real and reproducible; the builder omitted the evidence summary, citing the
  builder seat's report rule, and skipped the seeded path test for want of a
  fixture until pointed to the EIC child probe's throwaway surface. The
  Foreman wrote the summary and reclassified two rows. The Haiku 5.5 final
  review found that the summary's "no hazard" claim was stated for every row
  but established only for those examined, and an unsupported count; both
  were corrected.

## Follow-ups

- 729 published findings in the P0 run (`p0-path-scan.txt`; Form 1099-K
  statement rules, the interest current-year adjustment subtotal) carry a
  rule pin with no matching `pins_for` record, so the path scan cannot see
  them.
- The evidence scripts duplicate the tool's static logic and probe; they are
  historical.
- The static walk reads `member_fact_types` but not the singular
  `member_fact_type` or `derived_activity.fact_type`; no rule requires a
  symbol through them today.
- A per-row trace of the 25 over-declared rows, if a later change makes one
  matter.
