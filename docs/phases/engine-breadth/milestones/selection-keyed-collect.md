<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "selection-keyed-collect",
  "status": "Open. Track 0 accepted; Track 1 (engine switch, rule-artifact.v16, core v86) chartered; ADR 0085 proposed, awaiting owner acceptance.",
  "scope": [
    "a selection path can collect a keyed source family without any rule publishing a stand-in value under the member fact id",
    "a selection with one real path and a default needs no path on a fact type nothing writes",
    "a successor core retires rule.f1099b-b4-amount-symbol and the inert path, and every return core v85 computes computes the same, with earlier cores byte-identical"
  ],
  "non_goals": [
    "no change to selection semantics other than how a collect path is admitted, and no other rule-language change",
    "no edit to packages/kernel/",
    "no edit to any published schema file; a schema change is a new version"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/milestone-retrospectives/2026-11-10-f1099b-backup-withholding.md",
      "docs/reviews/f1099b-backup-withholding/rereview.md",
      "docs/phases/engine-breadth/milestones/selection-keyed-collect.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/selection-keyed-collect.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/selection-keyed-collect.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/selection-keyed-collect.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# A Selection Path Collects a Keyed Family Directly (2025)

Milestone key: selection-keyed-collect.
Branch: milestone/selection-keyed-collect-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-10.
Starting point: `github/main` at `5ac56b96` (PR #269, core v85).
Owner direction, 2026-11-10: take the derivation gap as its own milestone.

## What we are trying to accomplish

Core v83 sums every Form 1099-B box 4 amount through a selection whose
`amounts` path collects the keyed family. The language makes that path's
`requires` name its collect, and the runner holds the path until the name
is a symbol, but marshal never binds keyed assertions into that symbol.
So a content rule publishes 0 under the box 4 amount's own id
(`rule.f1099b-b4-amount-symbol`), and its explanation walk says 0 beside
a recorded amount. Separately, `rule-artifact.v15` requires two selection
paths, so the rule carries an `inert` path on a fact type nothing writes.
The useful outcome is an engine that admits a collect path on its source
family directly, and a successor core that retires both stand-ins.

## What we know

- `packages/derivation/package_validation.py` requires a path's `requires`
  to be its collect name; `packages/derivation/runner.py` withholds the
  path until that name is in `symbols` (rereview finding 1 cites the lines).
- `rule-artifact.v15` sets selection `paths` `minItems` 2.
- **What we do not know.**
  - Which other adopted rules use the same workaround, on any core.
  - Whether the smallest correct change is in validation and the runner
    (treat a collect's source family as satisfying the path), in marshal
    (bind the keyed assertions), or a new `requires` form; and whether any
    of these changes the meaning of an existing rule.
  - Whether the two-path minimum can drop in a schema successor without
    weakening what `exclusive_presence` guarantees.
  - Whether the change is a rule-language contract that needs an ADR.

## Actions the team will take

1. **P0: measure and design.** Find every workaround of this kind.
   Read the validation, runner and marshal paths. Prototype the smallest
   engine change behind a version switch (as the core-v75 and core-v76
   switches were), and a successor core that retires the symbol rule and
   the inert path. Measure every recorded return on old and new. Say
   whether an ADR is needed and draft it if so. Stop and report before
   editing packages/kernel/ or a published schema file.
2. **Decide.** The engine change, the schema successor if any, the ADR.
   An ADR blocks the PR going ready until the owner accepts it.
3. **Track 0 adversarial closure.** The six artifacts over the change.
4. **Track 1: build.** Engine change, any schema successor, core v86 and
   its registry and release; full suite (derivation is substrate).
5. **Close.** Fresh-reader review, repair, exact-head CI, retrospective,
   roadmap. Merge on green verify (owner standing approval, 2026-11-07).

## Cases that will shape the design

- No box 4 amount; one; two on different statements; one of $0.
- A box 4 amount superseded; withdrawn.
- The explanation walk of line 25b and of the subtotal on each.
- A selection with one real path and a default, and one with two real
  paths, under the old and new validation.
- Every return core v85 computes: identical on v86. Every earlier core:
  byte-identical, including with the switch off.

## Process

Dispatch is through the grok CLI (owner, 2026-11-09). Each unit commits on
this branch as it goes. Any change under packages/derivation/ runs the full
suite before handoff.

## P0 result

P0 is complete. Evidence:
`docs/phases/engine-breadth/milestones/selection-keyed-collect-evidence/p0.md`.

One stand-in on every core: `rule.f1099b-b4-amount-symbol`, from v83.
Thirty-two v85 selections still carry an inert second path. The smallest
engine change is a v86 package switch that stops treating a collect of the
path's activity family as a symbol dependency. Marshal stays as it is.
Drop the two-path minimum in new `rule-artifact.v16`. Scratch v86 retires
the symbol rule and the inert path. Design cases keep the same line values;
the member-id walk of 0 is gone. 596 recorded variants on v85 and v86 are
identical. Proposed ADR 0085. Foreman decides the engine change, v16, and
the ADR.

## Decisions

Foreman, 2026-11-10, on P0. The owner's direction is to proceed on the
recommended choice; the owner adjusts after. ADR 0085 acceptance is the
owner's and blocks the PR going ready.

1. **Engine change as P0 designed**: from `core-calculations` v86 a
   selection path's collect of its own activity family is not a `requires`
   symbol; validation and the runner follow; marshal is unchanged. Earlier
   cores keep today's behaviour, switched by package id and version.
2. **`rule-artifact.v16`** is v15 with selection `paths` `minItems` 1.
   Published v15 is untouched.
3. **ADR 0085** goes to the owner as proposed.
4. **Scope of the successor**: core v86 retires
   `rule.f1099b-b4-amount-symbol` and the box 4 subtotal's inert path
   (subtotal v2 on v16). The inert fact type stays declared in the
   published bundle; retiring it needs a bundle successor and changes
   nothing a filer sees. The other 31 inert paths on v85 are parked, to
   retire as each rule is next succeeded.
5. **Identity**: every recorded return and every design case is
   identical on v86 except that the box 4 amount id is no longer
   published as 0 (P0: 596 of 596).

## Track 0 adversarial closure

Foreman, 2026-11-10: accepted. Six rows PASS; the 596 recorded variants
are identical apart from the retired stand-in; a foreign collect still
must be listed. Track 1 is chartered in
docs/reviews/selection-keyed-collect/charter-track1.md.

Evidence: `docs/phases/engine-breadth/milestones/selection-keyed-collect-evidence/track0-closure.md`.

- Authority-lifecycle table: PASS — `track0-authority.json` (`alc_amount_one`, `alc_amount_zero`, `alc_subtotal_empty`, `alc_amount_superseded`, `alc_amount_withdrawn`, `alc_switch`, `alc_standin_retired`)
- Empty/nonempty authority matrix: PASS — `track0-matrix.json` (`m_no_box4_amount_v85`/`v86`, `m_one_amount_v85`/`v86`, `m_two_statements_v85`/`v86`, `m_zero_amount_v85`/`v86`, `m_one_path_v16_with_default`, `m_one_path_v16_without_default`)
- Late-member lifecycle: PASS — `track0-late.json` (`late_amount_added`, `late_amount_superseded`, `late_amount_withdrawn`, `late_second_statement`); prior subtotal and line 25b findings are absent after each change
- Neighboring capability dependency diff: PASS — `track0-neighbour.json` (`nb_validation`, `nb_bytes_v2_v85`, 596 `identical` recorded variants); the only new selection issue with the switch on is subtotal v1, which Decision 4 retires
- Reused-claim semantic/lifecycle equivalence: PASS — `track0-reuse.json` (`reuse_no_amount`, `reuse_one_amount`, `reuse_two_statements`, `reuse_zero_amount`); line 25b identity and consumers hold; v86 walk shows each recorded amount and not the stand-in 0
- Integration surface: PASS — `track0-surface.json` (six consumers, `surface_v16_add_only`, `surface_runner_wait`, `surface_foreign_collect_missing_requires`); Track 1 still threads `rule-artifact.v16` through derivation enumerations
- Known limitations affecting correctness: none
