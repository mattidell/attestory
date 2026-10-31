# P0: which core a correction recalculates on

Evidence: `probe.py` (run from the repository root) and its output `probe-output.json`.
Synthetic `demo.*` data only. Ceiling: reproduced trace and paper design. No code,
content or test change; no kernel or schema change is needed (stop condition not hit).

## Summary

The session does not recalculate a core-v66 workspace on v40 or v42. It refuses.
`live_coordinate_run` verifies the adopted release's attested registry against the
session's fixed registry (`published-packages.v40.json`), they differ, and the run is
refused `REGISTRY_CHECKSUM_MISMATCH`. The session reports only `calculated: false`,
so a filer who adopts the current core cannot get a recalculated correction at all.
A workspace that adopts v42 (every committed correction fixture does) works, and
that is the only case the fixed surface serves. The fix is to build the surface from
the workspace's own current adoption, which the repository already does in one place
(`_default_production_surface_for_adoption`).

## 1. Pins

Version words: core v66 = package v66, release v64, registry v64. The v42 core the
session was built for = package v42, release v40, registry v40.

| Where | What it fixes | Read by |
| --- | --- | --- |
| `packages/derivation/correction_session.py:176` `CORE_CONTENT = packages/content/tax/2025` | the member directory (every package/citizen body) | `core_calculations_surface` (193); `f1099k_statement_recording` indirectly (member dir default) |
| `correction_session.py:177-179` `CORE_RELEASE_DIR = packages/sample_data/student_loan_worksheet_integration/publication_surface/releases` | the release directory (27 releases, includes v40 and v64) | `core_calculations_surface` (193); imported by `packages/tax/f1099k_statement_recording.py:99,105-107` (a circular, odd dependency of tax on the session module) |
| `correction_session.py:180` `CORE_V40_REGISTRY = CORE_CONTENT / "published-packages.v40.json"` | **the one version pin**: the registry the release must attest | `core_calculations_surface` (193) |
| `correction_session.py:189-194` `core_calculations_surface(repo_root)` | builds the `PublicationSurface` from the three constants; no adoption read | `CorrectionRuntime.initialize` (830, used for the opening run and handed to `_adopt` 850), `CorrectionRuntime.open` (877), `runners/sli_correction_evaluation.py:44` (imports it, builds the temporary-session surface passed to `CorrectionRuntime(...)` at 196), 46 call sites in `tests/test_sli_correction_session.py` |
| `correction_session.py:747,898` `self._surface` | the surface held for the life of the runtime | `calculate` (1273) and `_recalculate` (1326), the only two calculation calls after the opening run |
| `correction_session.py:173-175` comment | says "v42 ... no new package, release, or registry version is needed" | documentation only |
| `packages/tax/f1099k_statement_recording.py:139` fallback `published-packages.{rel_ver}.json` | uses the *release* version as the registry name (right today only because release and registry numbers are equal) | taken only when no registry in the member dir matches the release's attested hash |
| fixture seed logs `packages/sample_data/sli_correction_t1/workspace/acts*.jsonl` (5 states) | each ends in two adoptions: core v41 (release v39), then v42 (release v40, revision 2) | `initialize` seeding; so every session workspace starts on v42 |
| `tests/test_sli_track1_combined_standing.py:52,558,651` | `V40_REGISTRY`, `adopt_v42`, a run on the v40 surface | the correction tests via `T1.adopt_v42` |

Not pins (checked): `RUN_SCOPE`, `SCOPE_USER` (170-171) are the year and user, not a
version. The surface-artifact route (`SURFACE_REGISTRY`, `SURFACE_RELEASES`,
`SURFACE_ADOPTION`, `_surface_publication`, `resolve_correction_surface`) resolves the
*page* artifact from a separate fixture registry; it is not the tax core and is out of
this milestone. `runners/sli_correction_evaluation.py` itself fixes no version; it
inherits the session's surface. `select_current_adoption` is already what
`live_coordinate_run` uses to pick the adopted package, so only the *registry/release
supply* is pinned, not the package choice.

## 2. Reproduction (public entry point)

`probe.py`: for each return, build the acts as `tests/test_w2g_gambling.py` and
`tests/test_withholding_closure.py` do, rewrite the actor to the session's
`demo.user.filer`, write them to a session workspace, then `CorrectionRuntime.open`
and `.calculate()`. Compare with a fresh `live_coordinate_run` on the v66 surface
(`published-packages.v64.json`).

| Return | Fresh run on v66 | Session, workspace adopting v66 | Session / fresh, workspace adopting v42 |
| --- | --- | --- | --- |
| Form 1099-G with box 4 withholding, family closed | publishes 243 values, nothing blocked | `calculated: false`, `REGISTRY_CHECKSUM_MISMATCH` | v42 cannot project the return (`FindingModelError`: companion presence on the withholding facts it does not know) |
| Form 1099-G withholding, family not confirmed | 236 values; line 25b blocked `SOURCE_SET_UNCLOSED`, 25d/33/34/35a/36/37 wait | `calculated: false`, `REGISTRY_CHECKSUM_MISMATCH` | `FindingModelError` |
| Form W-2G winnings and withholding | 243 values | `calculated: false`, `REGISTRY_CHECKSUM_MISMATCH` | `FindingModelError` |

So there is no value to compare on v40/v42 for a v66 workspace: the session never
reaches a v40/v42 calculation. The refusal comes from the release/registry check
before the package is read, so no silently stale numbers are produced today. The cost
is that the session cannot be used on the current core at all.

To observe a value difference, the session's own seed workspace (a v42-era SLI return,
adopting v42) was recalculated by the session, and the same acts after appending a v66
adoption were run fresh on v66 (`seed_workspace` in the output):

- Session on v42: calculated; 144 values, 25 blocked.
- Same acts after adopting v66: the session still refuses (`REGISTRY_CHECKSUM_MISMATCH`);
  a fresh v66 run publishes 171 values and blocks 154 rules, because the seed return
  lacks answers v43-v66 ask for (child count closure, Schedule 1 and Schedule A attachments, credits).
- Values published by both are equal (no changed value among the common symbols).
  Published only on v42: AGI, total income, `schedule1.line21-sli-deduction`,
  Schedule 1 line 26, Social Security lines 6a/6b. Published only on v66: 19 symbols
  (dependents worksheet, EIC, Form 1098 box 9, Form 1099-K box 4, ODC conflicts, CTC).
  So on the sparse seed, a v66 recalculation would stop publishing the AGI and line 21
  value until the filer answers the new questions. Track 1's v66 tests must use a
  complete return, and `_line21_view` must be shown to tolerate a blocked line 21.

Adoptions the fixed surface does not contain (probe `unrecognised_adoptions`), what
the session does today; all surface to the filer as only `calculated: false` /
`saved-not-calculated`:

- adoption pins a release not on the release surface: `RELEASE_ABSENT_OR_MISMATCH`
- no adoption in scope: `ADOPTION_NONE_CURRENT`
- adoption of any release whose attested registry is not v40 (every release after v40,
  and v39 and earlier): `REGISTRY_CHECKSUM_MISMATCH`

Hence the session today serves exactly one core, v42, not "whatever the workspace adopted".

## 3. Design

Resolve the surface from the workspace's current adoption, per calculation.

**New function** (in `packages/derivation/production_resolver.py`, next to
`select_current_adoption`, whose output it consumes; or a small sibling module if the
owner prefers `production_resolver` untouched):

```
surface_for_current_adoption(acts, *, run_scope, scope_user, workspace_revision,
                             release_dir, member_dir, schemas) -> PublicationSurface | Refusal
```

1. `select_current_adoption(...)`. A `Refusal` is returned as is
   (`ADOPTION_NONE_CURRENT`, `ADOPTION_AMBIGUOUS`, `ADOPTION_SUPERSESSION_INVALID`).
2. Find in `release_dir` the release whose id, version and **byte checksum** equal the
   adoption's release pin (as `_verify_release_and_registry` does). None: `RELEASE_ABSENT_OR_MISMATCH`.
3. Find in `member_dir` the `published-packages*.json` whose sha256 equals that release's
   `package_registry_sha256`. None: `REGISTRY_ABSENT`. No filename guess. This removes
   the `published-packages.{rel_ver}.json` fallback.
4. Return `PublicationSurface(release_dir, that_registry, member_dir)`.

Trust is unchanged: `live_coordinate_run` / `resolve_production_package` still verify
release bytes, registry bytes, package, members. The new function only chooses *which
registry to offer*; offering the wrong one still refuses, never miscalculates.

This is what `_default_production_surface_for_adoption`
(`packages/tax/f1099k_statement_recording.py:96-146`) already does, minus the fallback,
returning a `Refusal` instead of a guessed path. Move it (call sites:
`f1099k_statement_recording.py:199`, `ssa_family_handover.py:27,95`) so the recorder, the
SSA handover and the session share one resolver and `tax` no longer imports a constant
from `correction_session`.

**Refusals when the adopted core is unknown.** No adoption or unknown release/registry:
the function returns the typed `Refusal`. The session's public surface already reduces
any refusal to `calculated: false` (`calculate`) or `saved-not-calculated`
(`_recalculate`) with a fixed sentence, and `initialize` raises
`correction-opening-calculation-refused`. Those sentences, and the rest of the protocol,
stay as they are. No new refusal string, no change to the saved presentation or the
act log. (Whether to *name* the cause to the filer is a protocol change; deliberately not proposed.)

**What the saved correction records.** Nothing new. The core is recorded where it
already is: the workspace's adoption act and the run provenance. The correction acts
and the saved presentation keep their shape.

**Keeping an older workspace on its core.** Selection follows the adoption: a v42
workspace resolves release v40 and registry v40 (identical to today), a v41 or earlier
adoption resolves its own registry if its release is on the surface, and a
workspace that later adopts v66 (adoption revision 3) moves to v66 for the next
calculation, which is the intent. Per-calculation, not at construction, so a runtime
that is open when the filer adopts picks it up.

**Files to change** (Track 1):

1. `packages/derivation/production_resolver.py` (or a new sibling): add the function.
2. `packages/derivation/correction_session.py`: delete `CORE_V40_REGISTRY` (180) and the
   v42 comment (173-175); keep `CORE_CONTENT` and `CORE_RELEASE_DIR`; replace
   `core_calculations_surface(repo_root)` (189) by a function taking the acts and
   revision and calling the new resolver; resolve in `initialize` (830), `calculate`
   (1273 region) and `_recalculate` (1326 region) from `self._log.read()`. `CorrectionRuntime.__init__`
   keeps `surface` as an optional explicit override (the temporary runner builds it, tests use it).
   `__all__` (1673-1694) updated; keep `CORE_RELEASE_DIR` exported.
3. `packages/tax/f1099k_statement_recording.py`: drop `_default_production_surface_for_adoption`
   (96-146) and the import from `correction_session`; use the shared function.
4. `packages/tax/ssa_family_handover.py`: import from the shared place.
5. `packages/derivation/runners/sli_correction_evaluation.py` (44, 190-216): drop the fixed
   surface; the temporary runner builds the opening run's surface from the seed acts.
6. Tests (below). No fixture changes (the seed logs adopt v42 and stay so).

No kernel, schema, content, or package change. The `surface-adoption` route is untouched.

**Tests that pin v40/v42, and what they protect.**

- `tests/test_sli_correction_session.py` (46 uses of `core_calculations_surface(REPO)`;
  `T1.adopt_v42` at 1090; docstring at 10), `tests/test_sli_correction_resumption.py`
  (`initialize`/`open` on the v42 seed), `tests/test_sli_track1_combined_standing.py`
  (`V40_REGISTRY` 52, 651): these protect the correction protocol on the v42 baseline
  (choose, review, confirm, retry, resumption, redaction). Keep them as history, on
  v42; they pass unchanged if the new function resolves v42 to v40 (it must, and a
  new test pins that equality). The 46 call sites are an API change if
  `core_calculations_surface` is renamed; keep a thin `core_calculations_surface(repo_root)` (the v42 surface, tests only)
  or switch them to the resolver in one mechanical edit.
- New in Track 1: (a) a v66-adopted complete return (the W-2G and 1099-G cases above)
  corrected through `open`/`calculate`/save, published values equal a fresh
  `live_coordinate_run` on v66; (b) the same on an older adopted core (v42) equal to
  today; (c) a workspace that re-adopts v66 mid-session switches core; (d) refusals
  (no adoption, unknown release, unknown registry) end in the existing fixed outcomes;
  (e) the resolver returns the v40 registry for the committed seed adoption.

## 4. Expected behaviour

On v66 (complete return, adopting v66): `open` then `calculate` succeeds; the
calculation resolves registry v64 / package v66; published values and blocked rows
equal a fresh `live_coordinate_run` on v66 for the same acts (the three cases above,
after the fix); a correction saved through the session recalculates on v66. The 1099-G
unconfirmed case shows line 25b blocked `SOURCE_SET_UNCLOSED` after a correction too.
Open risk to test in Track 1: the SLI line 21 view on v66 (`_line21_view`) when the
return publishes line 21 and when it is blocked; not exercised here (the seed return
is too sparse for v66 to publish it).

On an older adopted core (v42 or any adoption whose release is on the surface): the
calculation resolves the registry that release attests; behaviour and values are
identical to today for v42 and the same correction fixtures. A return built with
questions newer than the adopted core still cannot be projected on that core
(`FindingModelError`, shown for v42 above); that is the older core's own boundary, the
session catches the exception and reports `calculated: false` as it does today.

With no adoption, or an adoption whose release is not on the release surface: refused
as today (`calculated: false`, `saved-not-calculated`, or the opening refusal).

## Unresolved for the decision step

- Place of the new function: `production_resolver.py` vs a sibling module (the
  resolver module is substrate-adjacent, so a full-suite run either way).
- Whether the filer should be told *why* a calculation did not run (a protocol
  change; not proposed).
- The release directory is the student-loan integration surface; releases for cores
  newer than v64 must be added there by their milestones as today. Not a pin to remove here.
