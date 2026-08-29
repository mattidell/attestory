# Review Charter — Document and Ordinary-Fact Translation Vertical

Audience: Reviewer

## Review target

The complete milestone candidate: `origin/main..HEAD` on
`milestone/document-ordinary-fact-translation`, head
`0cac5ce9c59fdc0b85108b13e9f26af0d89e3b98`, draft PR #188. Three commits — the
plan, Track 0 (`6758be16`), Track 2 (`0cac5ce9`). No prototype round exists;
Track 1 collapsed, and whether that collapse was justified is in scope.

This charter's own commit rides along on top of `0cac5ce9`. Call it out if you
wish, but the review object is `0cac5ce9` and its two ancestors, not the
charter.

Verify `0cac5ce9` against Git before reading anything else. If it does not
match, stop and report the mismatch.

## Independence

The milestone lead worked owner-directed and self-reported. Its evidence
documents — `docs/milestones/document-ordinary-fact-translation/`
`canonical-slice.md` and `production-translation.md`, and
`docs/domain-models/taxable-interest-translation.md` — are part of the
candidate and are themselves under review. **Read them as claims to falsify,
not as an account to confirm.** Every load-bearing number, line reference, and
"this was the only viable route" argument is to be re-derived from source.

## Required questions

**Necessity of the unpredicted schema successor.** `attachment-rule.v9` was
minted on the argument that an adjustment row's `kind` is a class-authority
key pinning both label and family token, so a fourth adjustment class cannot
borrow an existing one, and that `runner.py`'s Part I tie-out makes the
Schedule B row arithmetically mandatory once line 2b subtracts. Test both
halves against the code. Three cheaper routes are recorded as rejected in
`production-translation.md` §3; determine whether each rejection holds and
whether a fourth route was missed. Confirm v9 is genuinely additive over v8
and that `artifact-package.v26` is additive over v25.

**Whether the generalizations are strictly stronger.** Two version-pinned
checks became version-keyed maps (`_ADJUSTMENT_SURFACES`, and the Schedule B
class-surface check de-gated from `v4`). The claim is that an unrecognized
successor now declares no adjustment surface and *fails*, rather than silently
widening. Construct the unrecognized-version case and confirm it fails.
Confirm the de-gated Schedule B check is safe against v1, v2 and v3 by
inspecting their `adjustment_rows`, not by trusting the claim that they are
empty. Check 10c's allowance was widened from an equality to a three-member
set; confirm that widening does not admit an attachment shape that should be
refused.

**Whether the input forces a tax classification.** This is a plan stop
condition. The canonical payload must ask for ordinary facts only. Inspect the
committed `value_schema` and fixtures directly. The lead's own test
(`test_the_person_supplied_no_tax_classification`) asserts the absence of a
word list; judge whether that test is a real guarantee or a rehearsal, and
whether the field *names* and *semantics* — not just the vocabulary — stay on
the ordinary-fact side of the line.

**Whether T1–T9 are honestly exercised.** `tests/test_obligation_acquisition_translation.py`
claims package-level coverage of all nine plan scenarios. For each, confirm the
test drives the authoritative surface rather than a shortcut, and that the
assertion would actually fail if the behavior regressed. Pay particular
attention to T3 (an absent answer must be *named*, not defaulted), T5 and T8
(the identity discriminator), and T9 (refusal without silent coverage claims).
Check the refusal assertions read the family's own synthesized
member-validation artifact and not a run-wide code sweep that would pass for
the wrong reason.

**Whether the departures from the Track 0 design are sound.** Four are
recorded: payer-level rather than statement-level association; keeping the
`subject` identity key; making three recognition fields optional; Schedule B
declaring `itemizes_members` only. Assess each on its merits, and specifically
whether the optional-fields change weakens any constraint that was previously
load-bearing.

**Whether Track 1's collapse was justified.** The claim is that Track 0 left
one viable canonical shape. Judge whether the rejected alternatives were
genuinely non-viable or merely inconvenient.

**Published history and data safety.** Confirm no published schema version was
mutated, that both `published.json` manifests were appended and not rewritten,
and that historical package bytes are intact. Confirm every committed identity
is obviously synthetic and that no absolute workstation path, personal
document, or real amount entered the branch.

## Evidence standard

Rerun, do not accept. Run the full suite (the change touches
`packages/derivation/`), `python3 tools/governance_lint.py`, and
`python3 tools/envelope_scan.py --range origin/main..HEAD`.

The lead reports that the fast lane (`pytest -m "not live"`) fails identically
at `6758be16` and at the head — six `fast-lane budget exceeded` failures,
byte-identical sets — and therefore that no regression was introduced.
**Re-measure this yourself** in a detached worktree; it is the single claim
most convenient to the lead and least verified by CI. Note that the count is
timing-sensitive under `-n auto`; compare the sets.

## Deliverable

Write your record incrementally to the scratchpad path supplied in your launch
prompt, appending as you go rather than holding it to the end. Do not commit;
do not modify the candidate; do not touch `docs/phase-state.md`.

Return a falsifiable **READY** or **BLOCKED** verdict tied to head
`0cac5ce9`. Each finding: what you checked, how you checked it, what you
found, and its severity. A missed cheaper route for the schema successor, a
generalization that is weaker rather than stronger, an input that forces a tax
classification, a mutated published schema, or a data-boundary breach is
blocking.

If you conclude the candidate is sound, say so plainly. A review that
manufactures findings to look thorough is worse than one that finds nothing.
