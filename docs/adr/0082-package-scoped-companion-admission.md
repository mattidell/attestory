# ADR 0082 — Package-Scoped Companion Admission

- Status: **accepted** (2026-10-28; owner-accepted after the Form 1099 withholding final review)
- Tier: 2
- Date: 2026-10-27

## Context

A domain loader declares companion presence pairs (a member fact type needs a
same-statement companion), companion value domains (a companion may carry only
listed values, for example absent-or-zero), and companion equalities. The
loader installs them on every registry. The kernel enforces them whenever it
folds a finding into state (`_enforce_companion_presence`, reached from
`apply_assertion` and `apply_member_transition` inside `project`, and from
`apply_act` on the lifecycle path of `ActLog.append`). The live run passes the
same pairs to the runner so a collected member's companions are pinned and a
corrected companion displaces the derivation (ADR-0010).

None of that knows which package is in force. The maps are global, so a
successor package cannot admit a value an earlier package must refuse. The
Form 1099 withholding milestone needs exactly that: Form 1099-G box 4 and
Form SSA-1099 box 6 are today an absent-or-zero authority witness because no
package reads the amount; a successor package that counts withholding on Form
1040 line 25b needs the amount admitted. P0 (section 3) showed that relaxing
the global maps admits withholding that v58's line 25b rule never reads and
the return silently omits it.

## Decision

1. **The package in force picks the maps.** Companion presence pairs and
   companion value domains are resolved from the package that will read the
   statement. A package with no declaration (every package published before
   this decision) is governed by the global maps, byte for byte as before.
   Companion equalities, declaration/signal contradictions and subset pairs
   stay global; no package needs them to vary.

2. **Where the package comes from.**
   - *At run.* `live_coordinate_run` has already resolved the package
     (`resolve_production_package`: scope, user, workspace revision, ADR-0033).
     It builds a registry copy for that package
     (`findings.companion_registry_for_package`) and uses it for the
     projection, the marshalled pairs and the runner's companion pins, so
     admission and provenance use one resolution. The log is not rescanned.
   - *At projection and append.* `findings.project` and `ActLog.append` have
     no resolver inputs. They take the package from the log itself: among its
     `package-adoption` acts, the one with the greatest `revision` (the later
     act on a tie) (`findings.package_in_force`). Where the registry carries no
     package declarations, this is skipped and the registry is used as is.
   - *A log with no adoption act* has no package in force: the global maps
     apply, as they do today.
   - The live run and the log scan can name different packages only when the
     resolver would refuse or select by scope or user; the live run always
     uses the resolver's choice, and a statement that choice would refuse
     stops the run (decision 4).

3. **How a package declares them.** A loader map keyed by the adopted
   package's `(id, version)`
   (`packages.tax.loader.domain_package_companion_declarations`), installed on
   the registry as `package_companion_declarations`. An entry is
   `{"presence_pairs": {subordinate: companion | [companions] | None},
   "value_domains": {companion_type: frozenset | None}}` and overlays the
   global maps: a pair replaces the global pair for that subordinate, a domain
   replaces the global domain for that companion type, and `None` removes the
   entry (a removed domain leaves the fact type's `value_schema` as the only
   restriction). An entry with any other key, or whose parts are not mappings,
   is refused (`FindingModelError`), never ignored. A successor package adds its
   entry in the change that publishes it; the first is core calculations v59,
   which lifts the absent-or-zero requirement for Form 1099-G box 4 and Form
   SSA-1099 box 6.

4. **Never silent.** A run never computes over a statement its own package
   would refuse. A log recorded under a successor and run under an earlier
   package fails projection with the companion fact named (the earlier
   package's maps apply to it), before any rule is evaluated; nothing is
   published. `ActLog.append` and `append_batch` apply the same fold to a
   `package-adoption` act (when the registry declares any package overlay) and
   refuse an adoption under which the existing log would no longer project,
   rather than write a log that cannot be run. The lifecycle path of `append`
   applies the maps of the package in force.

5. **Provenance follows.** The pairs handed to the runner are those of the
   resolved package, so a collected member's companions are pinned and
   displacement edges form under whichever package reads the statement.

6. **No new act kind, no act schema change, no schema version.** The package is
   read from the existing `act-package-adoption.v1`. Nothing under
   `packages/content/` or `packages/schemas/` changes.

## Why earlier packages are unaffected

For a package in force with no entry (every package before core v59), and for
a log with no adoption act, `companion_registry_in_force` resolves to the
registry's global maps unchanged. For the live run, the copy for a package with no
entry carries the same global maps. Pairs, domains, error text and pins are
the same objects' contents as before; every existing test and golden is
unchanged. After a successor adds an entry, only that package's key resolves
differently; packages are immutable once published, so an earlier package's key
cannot acquire an entry.

## Production conditions

1. A successor package's entry is added in the same change that publishes the
   package, and its release test proves (through `live_coordinate_run`) that the
   entry admits what the package reads and that the previous package still
   refuses it.
2. Any recorder that applies acts with `apply_act` directly (rather than
   through `project` or `ActLog.append`) must take its registry from
   `companion_registry_in_force(acts, registry)`; otherwise it admits under the
   global maps. The recorders for the 1098, 1099-K and nominee families call
   `apply_act` directly with the global maps today and are not touched by this
   decision; the first successor that declares an entry for a family they
   record must route them through `companion_registry_in_force` first.
3. The adoption-ordering assumption is stated, not hidden: in a log, the
   adoption that puts a successor in force should precede the statements it
   admits. A statement written before the adoption is checked against the
   package in force at that moment only on the lifecycle `append` path; every
   projection checks it against the log's final package in force.

## Consequences

- Form 1099 withholding can admit 1099-G box 4 and SSA-1099 box 6 amounts under
  its successor package while v58 and every earlier package keep refusing them.
- A package author states companion semantics beside the package, not in a
  global table every package shares.
- Corrected or re-adopted packages change admission of the whole log, and the
  log is rechecked when they are adopted.

## Alternatives considered

- **Relax the global maps (P0 repair section 3, option (a)).** No kernel
  change, but an earlier package then admits withholding its line 25b never
  reads; the return silently drops it. P0 measured a refund of $508 become a
  $92 balance due. Rejected: violates "never silent".
- **A false zero witness (option (c)).** Keep the check and have the filer
  assert zero beside a nonzero amount to pass admission. Rejected: it records a
  false statement to satisfy a gate (ADR-0038, Article 9).
- **Declare the overlay inside the package content under a successor schema.**
  Keeps the declaration in the package checksum, but needs a new
  `artifact-package` schema version, validation, closure and republishing
  across the loader for a map with one entry (core v59). Deferred: the loader key
  `(id, version)` is stable because packages are immutable, and the content form
  can replace the loader map later without changing the kernel resolution.
- **Scan the log for the package in the live run too.** Rejected: the
  resolver's scope, user and revision rules would then be duplicated, and the
  two could disagree.

## Links

- Extends: ADR-0010, ADR-0033
- Evidence: `docs/phases/engine-breadth/milestones/form-1099-withholding-evidence/p0-verify-and-design.md` section 3
- Tests: `tests/test_package_scoped_companion_admission.py`, `tests/test_form_1099_withholding.py`
