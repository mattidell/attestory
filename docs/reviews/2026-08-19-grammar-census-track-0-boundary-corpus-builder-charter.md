# Builder Charter — Grammar Census Track 0: Term Boundary and Bounded Corpus

Audience: Builder

## Context Capsule

- Source ref and resolved launch commit: `HEAD` on
  `milestone/grammar-census-engine-language-map`; resolve and verify the SHA
  against Git before acting.
- Exact object or commit range: this charter and the active plan
  `docs/phases/grammar-census/milestones/engine-language-map.md`.
- Milestone key and primary branch: `grammar-census` /
  `milestone/grammar-census-engine-language-map`. Primary worktree is the
  one you are launched in; verify `git rev-parse --show-toplevel` and
  `git branch --show-current`.
- Assigned paths: **write exactly one file** —
  `docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md`.
  Everything else in the repository is read-only for you, including
  `docs/phase-state.md`, the milestone plan, and this charter.
- Role: Builder.
- Scope: produce the boundary map and the bounded corpus. Nothing else.
- Stop conditions: see "Stop conditions" below.
- Full reads before acting:
  - `docs/phases/grammar-census/milestones/engine-language-map.md` —
    `#Objective`, `#Scope`, `#Non-goals`, `#Term boundary`,
    `#Evidence layers`, `#Census unit`, `#Deliverables`, `#Tracks`,
    `#Parallel Work Manifest`, `#Data safety`
  - `docs/adr/INDEX.md`
  - this charter

## Goal

Bound what this census is about to catalogue, and bound the evidence it will
read, so that Tracks 1a–1c can run independently against a defined corpus
rather than each inventing its own.

Two deliverable halves, one file.

### Half one — the boundary map

The plan's `#Term boundary` names seven surfaces. For **each** one:

- name it as it actually appears in this repository (concrete paths, schema
  names, module names — not the plan's abstract phrasing);
- classify it: **grammar proper**, **grammar-adjacent**, or **uncertain**;
- state the reason, in a sentence or two, tied to committed evidence;
- if uncertain, say exactly what evidence would settle it.

"Grammar proper" versus "grammar-adjacent" is the judgment this track exists
to make. A defensible reason is what makes the classification useful; an
unreasoned classification is worse than an `uncertain` one. If a surface in
the repository fits none of the seven, add it and say so. If one of the seven
turns out not to exist here, say that too — that is a finding, not a gap in
your work.

### Half two — the bounded corpus

For each of the plan's six `#Evidence layers`, record:

- the exact committed artifacts in scope, by path (and version where the
  artifact is versioned);
- whether the repository carries any **canonical "current" designation** for
  that layer — an adoption record, registry, manifest, package selection, or
  other committed evidence;
- if it does: cite that evidence exactly;
- if it does not: **say so plainly**, then define the bounded corpus this
  census will use instead and give the reason it is defensible.

**Do not infer that the highest-numbered file is current.** Claim Boundary
Exploration established that no committed artifact designates a current core
package; it did *not* establish the same for schema and semantics artifacts.
Determine that here, from evidence.

The corpus you define is binding on Tracks 1a–1c. Make it something a cold
reader can execute against without guessing.

## Constraints

- **Documentation only.** Change no production code, schema, package, test,
  fixture, or tax content. Your diff must be exactly one new file.
- Cite every material claim to a committed path. Where the artifact is
  versioned, cite the version. Paraphrase is not a citation.
- Distinguish what you read from what you inferred. Where you infer, say so
  and say what would falsify it.
- Do **not** begin cataloguing constructs. That is Tracks 1a–1c. If you find
  yourself enumerating clause types, stop — you have left scope.
- Do **not** read any artifact under
  `docs/phases/claim-boundary-exploration/`. Track 1 must stay independent of
  it, and your packet is what Track 1 reads.
- Do not open or push a PR. Do not push the branch.
- No personal, private, or real filer data. No absolute workstation paths in
  anything you commit.

## Stop conditions

**Representational gaps are recorded, not fatal.** If the corpus cannot
represent a distinction the census will need without a code or contract
change, write it down as a tension-catalog candidate in a clearly-labelled
section and **continue working**. That is evidence, not a blocker.

Return to the Foreman without completing only if a trustworthy census cannot
be produced at all from the available corpus — for example, if no defensible
bounded corpus can be defined for a whole evidence layer. Say which layer and
why.

Also return if this charter and the plan disagree about your scope. The plan
controls; do not resolve the conflict yourself.

## Committing

Follow `docs/process/concurrent-work.md`. Acquire the worktree commit lock
before staging, stage only your one assigned path, inspect
`git diff --cached --name-only` to confirm nothing else is in the index, then
commit and release the lock.

Run `python3 tools/governance_lint.py` before handoff.

## Handoff report

Report to the Foreman:

1. the commit SHA;
2. the boundary-map classifications, and which ones you marked uncertain and
   why;
3. for each evidence layer, whether a canonical current designation exists,
   and the corpus you bounded where it does not;
4. every representational gap you recorded;
5. anything in the plan that your reading suggests is wrong, missing, or
   unworkable for Tracks 1a–1c — say it plainly rather than working around
   it silently;
6. your turn count and tool-call count.

---

# Repair round 2 — the boundary map (half one)

Filed by the Foreman 2026-08-19 after an external adversarial read of the
boundary map and source verification of its source-dependent claims. Round 1
(the Layer 4 corpus defects) is complete and accepted at `ad2bbe27`; do not
revisit it. This round touches **half one only**.

Supporting record, read it first:
`docs/reviews/2026-08-19-grammar-census-track-0-boundary-map-external-critique.md`.

## The finding

The boundary map's binary label is carrying at least five different criteria,
and the label — not the reasoning — is what the three isolated Track 1 streams
will inherit. They cannot cross-check each other, so a frame error survives
adversarial reconciliation intact: all three readers share it.

The criteria actually in use across the eight entries are: centrality to the
clause tree; being a field of the rule-artifact citizen; having a schema-typed
versioned citizen; ADR-contracted rather than incidental; expressed-by-a-rule
versus presupposed-by-a-rule; and "don't fold this vocabulary into surface 1."
The last is bookkeeping, not a classification test. Applied evenly, several of
these reverse the map's own answers — "presupposed, not expressed" would demote
surfaces 3, 4, and 7 alongside 8, since a rule never declares an
operation-semantics shape, a package shape, or an npe-walk shape either.

## Two contradictions confirmed against source — fix these, they are decided

1. **Rounding modes are classified on both sides.** Surface 6 places
   rounding-mode dispatch in grammar-adjacent on the stated ground that
   surface 6's contents live in "registry-populated Python dictionaries, not a
   schema-validated citizen." Rounding modes are in
   `packages/schemas/derivation/operation-semantics.v1.schema.json` — the
   citizen surface 3 classifies grammar proper. The same construct is
   classified twice, oppositely, according to which file was read.

2. **`act-package-adoption.v1` is cross-filed.** It is cited as a concrete
   surface for surface 4 (grammar proper), and its schema title is "Package
   adoption act payload" — making it a member of the act family that surface 8
   classifies grammar-adjacent.

## Two findings that survive verification and improve the map

3. **Surface 5's mini-language is correctly adjacent, for the wrong reason.**
   `TERM_OPS`/`PREDICATE_OPS` appear in no attachment-rule schema — Python
   only. Replace "structurally distinct vocabulary the census must not fold
   into surface 1" (bookkeeping) with the principled reason that matches
   surface 6's test: it is not declared in a schema-typed citizen. Note
   separately, because it is true and consequential, that the map's own phrase
   "independently closed expression grammar" concedes it *is* a grammar; the
   census should treat "how many languages are here" as an open question, not
   settle it by labelling the second one adjacent.

4. **Surfaces 2 and 6(i) stand.** Blocking codes are schema enums in
   `derivation-record.v2..v7`, `npe-walk.v1..v3`, and
   `checked-conclusion-binding.v1` — surface 2's claim is true.
   `findings.py`'s invariant pairs have no schema anywhere — surface 6's
   factual basis for that component is true.

## What to produce

Rewrite half one so the label is derived, and the derivation is visible.

1. **State one primary criterion up front**, in one sentence, and apply it to
   all eight surfaces without exception. Name it. If applying it evenly
   reverses an entry's current label, reverse the label and say so.
2. **Record orthogonal axes per surface**, in a table, so Track 1a/1b/1c
   inherit the axes rather than a lossy binary. At minimum:
   - declared in a schema-typed, separately versioned citizen? (yes/no, cite)
   - expressed by a rule-artifact, presupposed by one, or produced around one?
   - does it change a computed result's value or disposition? (yes/no)
   - is it itself a closed expression grammar? (yes/no)
   - is its meaning fixed by an accepted ADR? (cite, or none)
3. **Mark `uncertain` wherever the axes disagree.** Zero uncertain across
   eight entries is not credible for a first-pass boundary over an
   incrementally accumulated language, and the plan's exit criterion 4
   requires that material disagreements stay visible rather than being
   normalized away. The current map resolves every collision silently, which
   is what this round is correcting. Contested at minimum: surface 5 as a
   whole, surface 6's rounding and displacement-closure components, surface 7
   versus 8, and the surface 4 versus 8 pair jointly.
4. **Do not simply reclassify surface 8 as proper to make a schema-based test
   come out consistent.** That test is defensible and nearly reproduces the
   existing labels, but it conflates module-level well-formedness with clause
   expressiveness. If you adopt it, state what it costs. A module-versus-store
   distinction (packages as compilation units, acts/facts as the store) is
   available and may be the better cut — evaluate it explicitly rather than
   arriving at it by default.
5. **Split surface 6.** It concatenates three unlike things: domain axioms as
   registry data, currency/projection normalization, and rounding modes. The
   stated reason covers only the first. Classify the components separately.

## Constraints

Unchanged from round 1: one assigned path
(`docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md`),
documentation only, no production change, no reading of
`docs/phases/claim-boundary-exploration/`, commit-lock protocol, governance
lint before handoff, no push and no PR.

Do not weaken a classification to `uncertain` merely to satisfy item 3. An
entry is uncertain when the axes genuinely disagree, and you must say which
axes and how. An unreasoned `uncertain` is worse than a reasoned wrong answer.

---

# Repair round 3 — Foreman ruling and two flagged inconsistencies

Filed by the Foreman 2026-08-20. Round 2 is **verified and accepted** at
`9104aa48`: every source-dependent claim it introduced was checked against
source by the Foreman and holds, including the reversal of 5b-i, which
overturned both the external critique and the Foreman's own earlier check.
Do not revisit round 2's classifications except where this section directs.

This round is three bounded edits to one file, plus one correction to a
review record.

## 1. Foreman ruling on 5b-ii — `MAX_PREDICATE_DEPTH = 6` is **grammar proper**

The escalation asked whether "ADR-mandated but deliberately not
schema-enforced" counts as proper or adjacent. Ruling: **proper.** Reverse
the label and record the ruling and its reasoning in the entry.

The reasoning, which the entry must carry:

- The stated primary criterion asks whether the surface **constrains what a
  rule-artifact — or a citizen that composes or extends one — may express.**
  A depth bound of six on `member_constraints[].violated_when` is exactly a
  constraint on what a `source-family.v2` citizen may express. It meets the
  criterion on its own terms.
- The `uncertain` arose from reading the schema-typed-citizen axis as a test
  of *whether the rule is part of the declared language*, when it is a test
  of *which mechanism enforces it*. ADR-0066 decision 2 states both facts in
  one sentence — "Resolver admission rejects predicate depth greater than
  six; JSON Schema is not claimed to enforce recursive depth by itself" —
  which is a deliberate allocation of enforcement, not a disclaimer of
  contract.
- **The Foreman verified an enforcement site the round-2 reading missed.**
  The bound is enforced at package admission:
  `packages/derivation/package_validation.py:2037-2055` defines its own
  `MAX_PREDICATE_DEPTH = 6` and rejects deeper predicates. That is the same
  admission gate that makes surface 4 grammar proper — a package carrying an
  over-deep predicate is refused before it can execute. The bound is
  therefore enforced by contract, twice, on the module side of the
  module/store line.
- Splitting 5b-i and 5b-ii would place a closed vocabulary and its own
  well-formedness rule on opposite sides of the boundary, on the strength of
  a mechanism difference the ADR made on purpose.

Update the 5b-ii axes row accordingly. The "Schema-typed citizen?" cell
should say **No — enforced at resolver admission by contract, not by JSON
Schema (ADR-0066 decision 2, deliberate)**, so the axis stays honest while
the label follows the primary criterion.

Then state plainly, in the entry, that this is a **Foreman ruling on a
question the axes did not settle by themselves**, not a mechanical result —
and that a reader who rejects the enforcement-versus-declaration distinction
would reach `adjacent` instead. Exit criterion 4 requires the disagreement
stay visible, not that it be erased by the ruling.

**Half one then carries zero `uncertain` entries by ruling rather than by
silence.** Say that explicitly where the previous revision claimed zero by
silence, so a Track 1 reader can tell the two apart.

## 2. New tension-catalog candidate — the bound is declared twice

Add to "Representational gaps": `MAX_PREDICATE_DEPTH = 6` is defined
independently in two places, as two unrelated literals with no shared
constant — `packages/derivation/declarative_validation.py:20` (the
evaluator's runtime guard, raising `MemberConstraintTooDeep`) and
`packages/derivation/package_validation.py:2037` (the admission gate). ADR
prose names the number a third time. Nothing ties them together, so the
admission gate and the evaluator can silently diverge. Record it as a Track 2
tension-catalog candidate. Do not fix it — this milestone changes no
production code.

## 3. Repair the two inconsistencies you correctly flagged

You were right to flag these rather than edit outside your stated scope.
They are now in scope.

- **"Representational gaps" item 4 is superseded and wrong.** It says
  `declarative_validation.py`'s term/predicate vocabulary "has no published
  schema of its own" and instructs Track 1a to expect no schema-level
  enumeration and read the code instead. Round 2 established the opposite:
  the vocabulary is schema-typed at
  `packages/schemas/derivation/source-family.v2.schema.json` `$defs/term`
  and `$defs/predicate`. Rewrite the item to say what is actually true, and
  reverse the instruction to Track 1a — it **should** find this vocabulary in
  `packages/schemas/`, under `source-family.v2` rather than under any
  `attachment-rule` schema, which is where a reader would naively look. Keep
  it in the gaps list only if a real gap survives the correction; if none
  does, replace it with the discoverability point (the vocabulary lives in a
  citizen whose name does not suggest it) and say the original item was
  wrong.
- **The document header is stale.** "Produced against ... `0f8e078e`" names
  the launch commit of round 1. Change it to record the revision history
  honestly: original at `990888c2`, round 1 (Layer 4 corpus corrections) at
  `ad2bbe27`, round 2 (boundary map re-derivation) at `9104aa48`, round 3
  (this repair) at the commit you are about to make — which you cannot know
  in advance, so name it "this commit" and leave the SHA to the Foreman's
  acceptance record.

## Precision note, non-blocking

The 5b-i citation reads `source-family.v2.schema.json:66,97,178-421`. The
`$defs` block actually spans 171-469 (`term` at 172, `predicate` at 278,
`identity_component` present too). Tighten the range if convenient. The
substantive claim is correct and verified; this is precision, not error.

## Constraints

Unchanged. One assigned path
(`docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md`),
documentation only, no production change, no reading of
`docs/phases/claim-boundary-exploration/`, commit-lock protocol, governance
lint before handoff, no push and no PR.

Do not re-open round 2's other classifications. If you believe one is wrong,
say so in your handoff report and leave it alone.

---

# Repair round 4 — close the hole the round-3 ruling opened

Filed by the Foreman 2026-08-20. Round 3 is **verified and accepted** at
`2d719468`. The Foreman checked every claim in its handoff against source and
all hold, including two corrections to the round-3 charter itself: the
admission-rejection span is `package_validation.py:2051-2056` (the charter's
`2037-2055` stopped one line short), and round 2 did **not** claim zero
`uncertain` "by silence" — it left 5b-ii explicitly uncertain, so the charter
misdescribed it. Using the source over the charter was correct.

This round exists because the round-3 handoff was right about something the
charter had not noticed.

## The finding, which is the Foreman's error

The stated primary criterion opens with a conjunct — "declared in a
**schema-typed**, separately versioned citizen" — that 5b-ii does not
satisfy. The round-3 ruling made 5b-ii proper anyway, on the ground that
resolver admission is an enforcement mechanism rather than a statement about
language membership. Both cannot stand as written. A criterion that its own
document overrides is worse than a criterion that is wrong, because the
override is invisible to the three Track 1 streams that inherit the labels
and never see this reasoning.

The ruling is correct. **The criterion is what needs to change.**

## What to produce

1. **Amend the primary criterion** so it tests for a contractually enforced
   citizen rather than specifically a schema-typed one. The substance:
   a surface is grammar proper when it is declared in a **separately
   versioned citizen whose shape is contractually enforced — by JSON Schema,
   by resolver admission, or by both** — and that citizen meets clause (a) or
   clause (b), which are unchanged. The adjacency clause is unchanged: no
   enforced citizen at all, or the citizen is the data store.

   Word it yourself; do not copy the phrasing above verbatim if you can state
   it more precisely against what the code actually does.

2. **Verify the amendment is monotone before you adopt it, and show the
   check.** Widening an enforcement test can only promote, never demote — so
   the risk is that it silently promotes a row that should stay adjacent. Walk
   **every** row of the axes table and state, in a short paragraph or a
   column, why its label is unchanged. Pay particular attention to 6i and 6ii:
   6ii is ADR-fixed (ADR-0010) and would be promoted by a naive reading of
   "contractually enforced," and must be held adjacent by the store clause
   rather than by accident. If any row's label *does* change, stop and report
   rather than reclassifying — that would mean the amendment is not the small
   repair it appears to be.

3. **Record the amendment as an amendment.** State that round 2 derived the
   criterion, round 3's ruling contradicted it, and round 4 widened it to
   cover the ruling. A reader must be able to see that the criterion was
   fitted to a case after the fact, because that is a real weakness in the
   method and Track 2 should be able to weigh it. Do not present the amended
   criterion as though it had been the criterion all along.

4. **Layer 3's commit pin.** You flagged that Layer 3 still names
   `0f8e078e` as the resolved HEAD. That one is **not** a stale-header defect
   — it pins the commit at which the code-file corpus was enumerated, and no
   production code has changed in any round, so it remains accurate. Leave the
   SHA. Add one clause making clear it is a corpus pin, not the document's own
   revision, so the next reader does not re-flag it.

## Constraints

Unchanged. One assigned path
(`docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md`),
documentation only, no production change, no reading of
`docs/phases/claim-boundary-exploration/`, commit-lock protocol, governance
lint before handoff, no push and no PR.

Do not re-open any classification. This round changes the criterion's wording
and the surrounding narration, not a single label.
