# Charter: repair after the review of the lines below line 16

Role: Builder (the Track 1 builder, same session). Source HEAD on
milestone/preferential-base-reason-2025. Read
docs/reviews/preferential-base-reason/review.md, finding N1. N2 (line 16)
stays parked. Tests only: no edit under packages/.

## Items

1. **N1.** In tests/test_preferential_base_reason_v91.py:
   - on every authority cell, require the v90 and v91 presentation line
     maps to be equal, not only the producer signature;
   - on the recorded returns, compare the eight question sentences on
     each of the 23 fields with the adopted question citizens' texts,
     not their count, and require the v90 and v91 line maps to be equal;
   - a case whose name says a fact is unanswered must not assert that
     fact: make `_leave_unanswered` reject every one of the eight fact
     ids the name claims absent. The four recorded lists assert seven of
     the eight facts, so rename those cases for what they are (the
     recorded honest return) rather than "unanswered".
   Keep one coordinator run per distinct act list.
2. **Checks.** `pytest tests/test_preferential_base_reason_v91.py
   tests/test_preferential_base_reason_v91_package.py`,
   `pytest -m "not live"`, `python3 -m mypy`,
   `python3 tools/envelope_scan.py --range github/main..HEAD`. If a
   strengthened assertion fails, stop and report it; do not weaken it.
3. **Record.** Append "Repair result" to the plan. One commit per item,
   explicit paths, under the lock. Foreground only.
