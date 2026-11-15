# Charter: repair after the line 12d review

Role: Builder (the Track 1 builder, same session). Source HEAD on
milestone/line12d-boxes-2025. Read docs/reviews/line12d-boxes/review.md
findings S1 and S2. Core v90, registry v88 and release v88 are not merged,
so they are edited in place; nothing published on `github/main` changes.

## Items

1. **S1, one true sentence.** The four spouse form fields share one
   `guard_inapplicable` explain that names filing status even when the
   section is only the other state of a box the return shows. Replace
   that explain on all four with: "This line 12d box does not apply to
   this return, or the box is the other checked/not-checked state." Change
   nothing else in those citizens. Update prototype.py so its build is
   again byte-identical to the four files, then regenerate the checksums
   that depend on them (core v90, registry v88, release v88) and keep the
   package test green. Splitting the hidden case into its own disposition
   is out of scope; it belongs with the parked one-section-per-box
   question.
2. **S2, the unanswered case.** Add one live case to
   tests/test_line12d_boxes_v90.py that does not call
   `state_taxpayer_facts` and does not default the taxpayer facts: a
   single return with age and blindness unstated. Expect both You boxes
   and line 12e blocked, and assert the drawn page section shows the
   blocked copy with the question, not "not checked". Drop or rename the
   `*_unanswered` matrix names the review's N1 shows are the false-answer
   run, so no name claims a case it does not run.
3. **Checks.** Run tests/test_line12d_boxes_v90.py,
   tests/test_line12d_boxes_v90_package.py, the fast lane, mypy and
   `python3 tools/envelope_scan.py --range github/main..HEAD`. The full
   replay is not re-run: a sentence change cannot move a number, and
   rerun-output.json records dispositions and values, not explain text.
   If rerun-output.json or any Track 0 evidence file does record the old
   sentence, say so in the report and stop rather than regenerate it.
4. **Record.** Append "Repair result" to the plan with what changed and
   the checks. One commit per item, explicit paths, under the lock.
