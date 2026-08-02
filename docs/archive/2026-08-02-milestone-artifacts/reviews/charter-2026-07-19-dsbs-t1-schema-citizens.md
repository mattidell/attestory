# Charter: Track 1 — Schema Citizens (Dividends and Schedule B Slice)

Date: 2026-07-19. Prepared by the foreman; builder dispatched under the
owner's standing authorization for this continuation (ADR-0034). Branch:
`track/dsbs-t1-schema-citizens`. Governing contracts: ADR-0035, ADR-0036,
the milestone plan's Track 1 section and Contracts/Data-safety/Verification
sections (`docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/dividends-schedule-b-slice.md`),
and the established citizen patterns (ADR-0015/0016/0017/0026 content under
`packages/content/tax/2025/`, schemas under `packages/schemas/`).

## Goal

Land every schema/contract citizen the ratified ADRs owe this milestone,
with positive examples, named negatives, registry rows, and
schema-validation tests — plus the two admission-time validation guards and
the one vocabulary reconciliation explicitly assigned to Track 1. **No
runtime behavior**: no evaluator semantics, no composition or attachment
rule execution, no line content, no coordinator goldens (those are Tracks
2–4).

## Deliverables

1. **1099-DIV statement and family citizens (ADR-0035 decisions 1–2).**
   Statement-instance identity on the ADR-0015 pattern (statement entity;
   payer + tax-year + payer_ref sameness); two independent per-box families
   `tax.us.2025.f1099div.1a` (member fact `box1a-ordinary`) and
   `tax.us.2025.f1099div.1b` (member fact `box1b-qualified`), each with its
   own horizon-keyed closure declaration and `source-closure-mapping.v2`
   content citizen, following the committed `family.f1099int-*` /
   `closure-mapping.f1099int-*` pattern. Fact-type citizens with
   `value_schema`s; bundle rows.
2. **`dividend-universe.v1` (ADR-0035 decision 3).** A new schema-versioned
   citizen naming composable boxes {1a → 3b family, 1b → 3a family} and
   recorded-non-composable boxes {2a, 3, 5, 7, 12}; the non-member
   `recorded-boxes` fact type keyed to the same statement with explicit
   `null` as declared absence. Schema, positive example, named negatives
   (at minimum: a composable box without a family binding; a box in both
   sets; an undeclared box), registry row. The
   `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal is *named* by this citizen
   surface (its raising is Track 2 behavior).
3. **Attachment citizens (ADR-0036 decisions 1–4, schema surface only).**
   The declared shape needed to author an attachment rule: the attachment
   rule citizen (generic — no Schedule-B-specific field, trigger shape, or
   completeness structure), the `collect_members` expression surface at
   schema level, and the Part III taxpayer-answer fact-type pattern with
   the load-bearing categorical `{yes, no}` domain. Positive examples must
   include the ratified generalization posture (the ADR's Schedule D stub
   demonstrates content-freedom; a B-specific example belongs to Track 2+).
   Negatives at minimum: a boolean-valued answer fact type; an attachment
   rule whose completeness expression reads a value before presence; a
   member row outside the declared family. Derive the exact shape from the
   confirmed synthesis (`docs/archive/2026-08-02-milestone-artifacts/prototypes/attachment-ontology/` —
   `evaluation-analysis.md` and `reviews/confirmation-r1.md`); where the
   synthesis and this charter disagree, the ADR text governs.
4. **Vocabulary reconciliation (ADR-0036 production condition 3, owner
   disposition: in Track 1).** The runner emits `SOURCE_SET_UNCLOSED`
   (`packages/derivation/evaluator.py` `BLOCK_CLOSURE`; scenario goldens
   carry it) while `derivation-record.v2`, `npe-walk.v1`, and
   `form-field.v2` enums permit `SOURCE_SET_OPEN`. Reconcile by versioned
   schema change; the ADR takes no position a direction could invert —
   choose the direction the committed evidence supports, state it in one
   place with the evidence, and carry every dependent enum, content
   citizen, and golden coherently. In the same versioned change, add
   **`ITEMIZATION_TIE_OUT_VIOLATION`** to the record and walk vocabularies
   (ADR-0036 production condition 1's vocabulary half — the derivation-time
   check and its kill-tests are owed to later tracks and must NOT be built
   here).
5. **Admission-time validation guards.**
   a. *Runtime universe guard (ADR-0035, owed Track 1):* package validation
      rejects any rule whose `collect` targets a non-family fact type or
      whose inputs include recorded-non-composable content, with tests.
   b. *Presence-encoding guard (ADR-0036 production condition 2):* package
      validation rejects a boolean or otherwise falsy-valued Part III
      answer fact type on an attachment, with tests.

## Boundary

No evaluator/runner execution changes beyond what the vocabulary
reconciliation mechanically requires; no 3a/3b/line-9/line-16 rule content;
no Schedule B form content; no tie-out check; no D2 declared-absence facts;
no real-workspace access or personal data. Existing goldens are regenerated
only where the versioned vocabulary change demonstrably requires it, each
regeneration named and explained in the track summary. Owner-held run
tooling (`tools/scaffold_live_acts.py`, `workspace-seed/`) stays untracked.

## Verification

Schema-validation tests cover every new citizen positively and every named
negative. Both validation guards have rejecting and admitting tests. Before
handoff: full `.venv/bin/python3 -m unittest`, `.venv/bin/python3 -m mypy`,
`.venv/bin/python3 tools/governance_lint.py`, and `.venv/bin/python3
tools/envelope_scan.py --range main..HEAD` — all green. This is not a
behavior track, so the standing authoritative-surface golden-class
requirement attaches to Tracks 2–4, not here; schema-validation evidence is
this track's authoritative surface.

## Review gate

One integrated per-track branch and review unit (ADR-0030): an
author-independent pre-merge review follows completion; the owner holds the
merge.
