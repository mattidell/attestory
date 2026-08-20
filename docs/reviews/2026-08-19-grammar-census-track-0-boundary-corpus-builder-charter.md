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
