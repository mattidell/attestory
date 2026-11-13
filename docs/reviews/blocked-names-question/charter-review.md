# Charter: fresh-reader review of blocked lines naming their question

Role: Reviewer. Source HEAD on milestone/blocked-names-question-2025,
diffed against `github/main`. Plan:
docs/phases/engine-breadth/milestones/blocked-names-question.md (read it
whole). Contract: docs/adr/0086-block-declares-missing-names.md (accepted).
You have not seen the build, so judge from the committed schemas, code,
content, tests and evidence, not from summaries. Do not read governance.

## Questions

1. **The contract.** Does `rule-artifact.v17` add exactly the optional
   `missing` on an expression `block` (non-empty, unique, non-empty
   names) and nothing else? Does the evaluator raise the selected block's
   code with exactly the declared names, and v16 and earlier exactly as
   before? Try a v17 rule with and without `missing`, and a v16 rule.
2. **Routing only.** Can a declared name change a read, a pin, scheduling,
   a closure, an answer or a number? Construct the case if you can.
3. **Every dead end closed.** For each of the ten Track 0 cases and the
   Form 1040 line 16 case, run the real coordinator on core v89 with
   synthetic `demo.*` findings, unanswered and answered truthfully: does
   every blocked filer-visible field name a question, and does the
   truthful answer reach the 2025-instruction hand value? Is any question
   shown that the filer cannot answer, or that names the wrong thing?
4. **Line 16.** On the 4 recorded returns where line 16 changes from
   inapplicable to a named block: is the block true, and does the
   question it names lead to the right number?
5. **Immutability.** Are the schema manifests and registry v87 add-only,
   every new citizen byte-identical to prototype.py's build, and the
   loader change limited to v89? Is the diff over packages/kernel empty?
6. **CI cost and isolation.** The live module makes 329 runs in about 12
   minutes. Name runs that test nothing a sibling does not. Evidence
   loaded only through tests/evidence_loader.py?
7. **Data safety.** `python3 tools/envelope_scan.py --range
   github/main..HEAD`. No absolute or temp-directory path in the review.

Run `pytest` only to confirm a specific failing claim.

## Deliverable

docs/reviews/blocked-names-question/review.md, committed (explicit path,
under the collaboration-commit lock; retry with backoff if held). Each
finding: file:line, reproduction, severity (blocking, should-fix or
note), fix. End with a verdict: ready, or the blocking list. No other
edits.
