# Engine Language Map — Exit-Criteria Assessment

Filed by the Foreman 2026-08-20 on acceptance of Track 3
(`4dbc23e3`, `3bd1c5bd`). This is Foreman work, withheld from both Track 3
streams by charter. It assesses the eight exit criteria in
`docs/phases/grammar-census/milestones/engine-language-map.md#Exit criteria`
against the full deliverable set:

- Track 0: `track-0-boundary-and-corpus.md` — `4f66bc83`
- Track 1a/1b/1c: `983b6102` / `495adeac` / `bb5ea26b`
- Track 2: reconciliation `f276cc5b`, traces `3dba1a80`, tension catalog
  `5ba385c1`
- Track 3: map `4dbc23e3`, comparison brief `3bd1c5bd`
- Foreman correction: `docs/reviews/2026-08-20-grammar-census-foreman-correction-5b-ii-ruling-reasoning.md`

## 1. A casual but technically invested reader can understand the boundary and layers from the synthesis alone

**Met.** `track-3-engine-language-map.md` states what kind of language the
engine has, where the boundary falls (including the amended, ruling-dependent
criterion, stated plainly with the alternative a rejecting reader would
reach), how the layers relate in a run, what a clause can express, and what
it cannot. It is grounded — every claim traces to a `U-###`, `T#`, trace, or
shown execution — without being a second copy of the census table. I read it
as a synthesis, not an index, which is the test the criterion sets.

## 2. Declared, implemented, observed-in-use sets separately enumerated then reconciled

**Met.** Three independent, isolated readings (108 / 90 / 84 constructs)
reconciled into 166 rows with an explicit status per construct. Independence
was verified operationally, not just asserted: each stream reported seeing
sibling deliverables appear without opening them.

## 3. Every material semantic claim cites a committed source or a shown synthetic execution

**Substantially met, with one class of exception recorded honestly.** The
citation discipline held across all seven deliverables and was checked, not
assumed — I independently reproduced several counts (368 `categorical_compare`
nodes, the `when.op` distribution, the `attachment-rule.v3`/`v5` hash
prefixes, `_bracket_fold`'s unread canon binding, `truth_table`'s absence)
and all matched. The one deliberate exception is Track 3b's external-system
characterizations, which are explicitly marked unverified per its charter —
that marking is itself part of meeting this criterion, not a violation of it.

## 4. Material disagreements and unknowns remain visible, not normalized away

**Met, and stress-tested.** The clearest evidence: a Foreman ruling's own
stated reasoning was falsified by Track 2's spot-check S2, and the record
does not erase the ruling — it strikes the false sentence, keeps the
original text visible as struck-through history, and files a standalone
correction record explaining what was wrong and why the label didn't move.
A reader who rejects the enforcement-versus-declaration distinction is told,
in the plain-language map itself, that they will draw the boundary
differently. Eight Track 2 open questions survive uncollapsed into either
answer.

## 5. Representative traces connect syntax to consequences, executed evidence distinguished from static reading

**Met.** Six traces, each step tagged Executed or Inferred, three ending in
something other than a published finding (an `inapplicable` with a real
`guard_result`, a `SOURCE_SET_UNCLOSED` block, an internal
`FAMILY_VALIDATION_BLOCKED`). The traces stream added a discipline the
charter didn't require — closing each trace with the nearby inferences its
evidence does *not* support — which strengthens this criterion beyond its
letter.

## 6. The tension catalog contains only entries with a stated plausible next action

**Met.** Nine entries, each with evidence, affected layer, consequence,
uncertainty, and next action. Eighteen candidates were considered and
recorded as dropped rather than either padding the catalog or silently
discarding them — visible triage, which is what this criterion is actually
protecting against.

## 7. A follow-on comparative review can be scoped from the brief's explicit questions, not a generic survey

**Met.** Seven dimensions, each driven by a named census artifact (a trace,
a tension entry, a reconciled construct), each with the external systems
that bear on it and the questions that would move an engine decision. The
brief separately names which comparisons would be superficial — required by
the plan and easy to skip; it wasn't skipped. Of the six dimensions an
external model raised during Track 0, one (constitutive-versus-prescriptive)
was dropped outright as not attached to anything the census pressured, and
that drop is recorded rather than silently absorbed.

## 8. No grammar change, product contract, ADR, governance interpretation, or external-standards claim

**Met.** Every defect found in this census — the `attachment-rule.v5`/`v3`
`$id` collision, the predicate-depth divergence, `_bracket_fold`'s unread
canon, `OPERATION_VOCABULARY` as dead code, `truth_table`'s absent reader —
is recorded as a finding with production code, schema, and ADR content
unchanged throughout. The diff discipline (one file per Builder commit) held
across eleven Builder units and two Foreman-authored records.

## Overall

**All eight criteria are met.** The milestone is complete. The two process
deviations from plan — the Foreman correcting his own ruling on evidence the
milestone itself produced, and the Foreman committing 3b's final section
after a killed run rather than re-dispatching — are both recorded in the
commit history and in this assessment rather than smoothed over, which is
what criterion 4 asks of the whole milestone including its own conduct.

Whether the census is **reliable enough to close** and what a **strongest
case against its conclusions** looks like are answered in the final report,
alongside the bounded choices for what follows. This document establishes
only that the eight stated criteria are satisfied.
