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
