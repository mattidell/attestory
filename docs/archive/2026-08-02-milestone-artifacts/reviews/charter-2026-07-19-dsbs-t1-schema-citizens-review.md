# Charter: Track 1 — Schema Citizens — Author-Independent Pre-Merge Review

Date: 2026-07-19. Prepared by the foreman; the owner dispatches this seat
(ADR-0034). The reviewer is author-independent: it reads this charter, the
Track 1 build charter (`docs/reviews/charter-2026-07-19-dsbs-t1-schema-
citizens.md`), the Track 1 section of the milestone plan
(`docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/dividends-schedule-b-slice.md`),
ADR-0035 and ADR-0036 (with the attachment-ontology prototype evidence they
cite), and the branch `track/dsbs-t1-schema-citizens` — not the authoring
session.

## Object under review

The delta `main..track/dsbs-t1-schema-citizens` (six commits: `1d2a58b`
vocabulary reconciliation, `2a08d80` 1099-DIV statement/family/closure
citizens, `60bbbc0` `dividend-universe.v1`, `272b7a9` generic attachment
citizen surface, `95e36ab` handoff docs, `a6f11f3` the two admission-time
validation guards). This is a schema/contract track: **no runtime evaluator
or runner behavior change is in scope beyond what the vocabulary
reconciliation mechanically requires.**

## Falsifiable checks

1. **1099-DIV statement and family citizens (ADR-0035 decisions 1–2).**
   Statement-instance identity follows the ADR-0015 pattern (statement
   entity; payer + tax-year + payer_ref sameness). Two *independent*
   per-box families exist — `tax.us.2025.f1099div.1a` (member fact
   `box1a-ordinary`) and `tax.us.2025.f1099div.1b` (member fact
   `box1b-qualified`) — each with its own horizon-keyed closure declaration
   and `source-closure-mapping.v2` citizen, following the committed
   `family.f1099int-*` / `closure-mapping.f1099int-*` pattern exactly
   (verify by direct comparison, not by inspection of names alone). Fact-type
   citizens declare `value_schema`; bundle rows are present and loader-valid.

2. **`dividend-universe.v1` (ADR-0035 decision 3).** The schema names
   composable boxes {1a → 3b family, 1b → 3a family} and recorded-non-
   composable boxes {2a, 3, 5, 7, 12} as declared, versioned content — not a
   runner-private list. The `recorded-boxes` fact type is keyed to the
   statement and admits explicit `null` as declared absence (confirm the
   value schema actually enforces this, not merely documents it). Three
   named negatives are present and rejected: a composable box without a
   family binding, a box in both sets, and an undeclared box. A registry row
   exists. Confirm the `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal is named
   by this surface but **not raised** anywhere in this delta (raising it is
   Track 2 behavior — flag any exception).

3. **Attachment citizens (ADR-0036 decisions 1–4, schema surface only).**
   The attachment rule citizen is generic: no Schedule-B-specific field,
   trigger shape, or completeness structure baked into the schema itself.
   `collect_members` exists at schema level. The Part III taxpayer-answer
   fact-type pattern pins a categorical `{yes, no}`-shaped (all-truthy
   string) domain, never boolean. The positive examples include the ratified
   generalization posture — a Schedule D stub demonstrating content-freedom,
   distinct from any Schedule-B-specific example (which does not belong in
   this track). Three named negatives are present and rejected: a
   boolean-valued answer fact type; an attachment rule whose completeness
   expression reads a value before presence; a member row outside the
   declared family. Cross-check the shipped shape against
   `docs/archive/2026-08-02-milestone-artifacts/prototypes/attachment-ontology/evaluation-analysis.md` and
   `reviews/confirmation-r1.md` — where the synthesis and the ADR text
   disagree, the ADR governs; note any such disagreement found.

4. **Vocabulary reconciliation (ADR-0036 production condition 3, plus
   production condition 1's vocabulary half).** `SOURCE_SET_UNCLOSED` (the
   runner's actual `BLOCK_CLOSURE` emission) is the code that survives in
   the versioned record/walk/form-field vocabularies; `SOURCE_SET_OPEN` is
   retired everywhere a current instance could carry it (confirm no
   surviving enum, content citizen, or golden still names `SOURCE_SET_OPEN`
   as a current — not merely historical — value). The chosen direction and
   its supporting evidence are stated in one place. `ITEMIZATION_TIE_OUT_
   VIOLATION` is added to the record and walk vocabularies as a name only —
   confirm no derivation-time check, evaluator branch, or kill-test for it
   was built in this delta (that is explicitly owed to a later track).

5. **Admission-time validation guards (deliverable 5).**
   a. *Runtime universe guard.* `validate_package` rejects a `collect`
      targeting a non-family fact type and rejects any rule input naming
      recorded-non-composable content, both with passing rejection tests and
      a passing admission test for a conforming package. Read the guard's
      scoping to `artifact-package.v3`/`.v4` (`package_validation.py`,
      `universe_guard_active`) against the charter and the milestone plan's
      boundary clause ("Existing goldens are regenerated only where the
      versioned vocabulary change demonstrably requires it") — the
      exemption of published v1/v2 package instances is a builder design
      choice, not literal charter text; assess whether it is justified and
      whether it is asserted by an executed test (not merely a comment).
   b. *Presence-encoding guard.* `validate_package` rejects a boolean or
      otherwise falsy-encodable Part III answer fact type on an attachment,
      with rejecting and admitting tests. Confirm the categorical-domain
      check is airtight against an all-empty-string or otherwise
      degenerate-but-technically-non-boolean domain (test the boundary, not
      just the boolean case).

6. **Boundary fence.** No evaluator or runner execution-path change beyond
   what the vocabulary reconciliation mechanically requires (the admission
   guards belong to `package_validation.py`, not the evaluator/runner — this
   is in scope; a change to `evaluator.py` or `runner.py` semantics would
   not be). No 3a/3b/line-9/line-16 rule content. No Schedule B form
   content. No tie-out check implementation. No D2 declared-absence facts.
   No real-workspace access or personal data anywhere in the delta.

7. **Boundary and data safety.** Every fixture, identifier, and golden is
   manufactured `demo.*`/`demo-*` data; no workspace path, real-run detail,
   value, disposition, or refusal text appears anywhere in the delta. Run
   the per-review safety scan over the new fixtures and goldens. Never
   commit `tools/scaffold_live_acts.py` or `workspace-seed/` (owner-held,
   intentionally untracked).

8. **Verification battery (re-run, not trusted).** On the branch:
   `.venv/bin/python3 -m unittest`, `.venv/bin/python3 -m mypy`,
   `.venv/bin/python3 tools/governance_lint.py`, and `.venv/bin/python3
   tools/envelope_scan.py --range main..HEAD` — all green. This is not a
   behavior track: schema-validation evidence (every new citizen positive
   and every named negative; both guards with rejecting and admitting
   tests) is this track's authoritative surface, not a coordinator-from-
   facts golden class.

## Verdict

Write `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-19-dsbs-t1-schema-citizens-review.md` on the
branch with an explicit `ready` / `not ready` verdict and findings numbered
F1…, each tied to a check above with file/line evidence. The foreman
triages findings; the owner holds the merge (ADR-0030). Merge of this track
opens Track 2 (composition and conditional machinery).
