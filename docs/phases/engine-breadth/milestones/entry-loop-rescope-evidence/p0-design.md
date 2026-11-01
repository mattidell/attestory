# P0 evidence: entry-loop rescope

This is an evidence/design note, not a production change. `probe.py` runs the
committed legacy entry-loop seed without modifying it, runs the complete
synthetic helper return against the actual published v70/v68 chain, and
re-pins a separate in-memory copy of the thin legacy seed to v70 to observe
partial-entry behavior. The repeatable output is `probe-output.json`.

## Findings

### Surface resolution

`SyntheticW2EntryRuntime` currently constructs a fixed publication surface at
`frrs_t3/publication_surface/releases` plus
`packages/content/tax/2025/published-packages.json`
(`packages/derivation/entry_loop.py:528-532`). The current helper return adopts
`package.core-calculations@v70` and release `demo.release.sli-worksheet-integration.2025@v68`.
`resolve_adopted_surface` resolves that exact release by its adoption pin and
byte checksum, then resolves the registry by the release's registry checksum;
it does not infer filenames from a package version
(`packages/derivation/production_resolver.py:207-277`). Its actual result is
`published-packages.v68.json` under the
`student_loan_worksheet_integration` release directory. Offering the v70
adoption to the entry loop's fixed `frrs_t3` release directory returns
`RELEASE_ABSENT_OR_MISMATCH`; the runtime refuses before evaluation.

Recommendation for Track 1: resolve the surface named by the current adoption
using `resolve_adopted_surface`, with a caller-owned, explicit release/member
search root. Do not derive a path from `package.version`, nor make the v70
surface the implicit default for the existing v6 seed. Preserve the v6 route
and seed behavior; an adoption whose release cannot be found on its configured
surface should fail closed.

### Bounded line membership

The current v6 loop hard-codes `EXPECTED_IMPACT_LINES` as
`1a, 9, 11, 15, 16`, comparison lines as `2b, 3a, 3b, 12`, and their union as
`EVALUATION_LINES` (`packages/derivation/entry_loop.py:81-83`). Those are
display line IDs, not a package-derived role contract. The real v70 package
projects 41 Form 1040 fields. Among them are the focused W-2 Box 1 rows, the
Box 2 withholding row 25d, refund/amount-owed rows 35a/37, and rows outside
this entry loop such as `6d-not-checked`. The package also projects fields
from other forms, where line-number equality is not Form 1040 identity.

The published `form-field.v3` shape carries `form`, `line`, `label`,
`binds_symbol`, citation and dispositions, but no value-type or entry-role
property (`packages/schemas/tax/form-field.v3.schema.json`). Thus package
bindings can supply the selected fields' current identities, labels and
symbols, but cannot say which rows belong to this loop or which group they
occupy. “Every numeric field” is also not safe: numeric output alone neither
establishes monetary meaning nor membership in this bounded entry surface.

Recommendation: keep a small, explicit entry profile keyed by the adopted core
package identity/version (and validate its checksum through normal package
resolution). Each profile names exact package field `(id, version)` members
and their `expected-impact` or `untouched-comparison` role. Resolve those
members from the adopted package and use the package citizen for presentation;
verify IRS Form 1040 identity (`form_id=1040`, `authority=IRS`,
`jurisdiction=US-federal`, adopted tax year) and binding identity. Validate
that available values are numeric monetary values and accept only the existing
computed dispositions; do not use numericity as a selector. Unknown package
profiles fail closed instead of widening the UI.

The observed profiles are:

| Adopted core | Expected impact | Untouched comparison |
| --- | --- | --- |
| v6 | 1a, 9, 11, 15, 16 | 2b, 3a, 3b, 12 |
| v70 | 1a, 9, 11a, 11b, 15, 16 | 2b, 3a, 3b, 12e |

The v70 member identities are `form1040.line-1a@v1`, `line-9@v1`,
`line-11a@v1`, `line-11b@v1`, `line-15@v1`, `line-16@v1` for impact, and
`line-2b@v6`, `line-3a@v1`, `line-3b@v1`, `line-12e@v1` for comparison.
Both 11a and 11b bind the same AGI symbol in v70; retain both explicitly as
distinct Form 1040 display fields. The line-2b field is member version v6 in
the v70 package, so pin the exact citizen identity rather than resolving by
visible line text alone. The v6 seed's nine original rows remain exactly its
v6 profile.

The probe also ran a matched pair of complete v70 helper returns, changing only
the synthetic Box 1 finding from $50,000 to $90,000. Both coordinator runs had
zero blocked rows. All six proposed impact fields changed; the four proposed
comparison fields did not. But Form 1040 lines 22, 24, 34, 35a and 37 changed
too, while 25d stayed at $4,500. That confirms the selected role behavior on
the actual v70 package, and shows why selecting every value-diff or every
numeric Form 1040 row would broaden this focused UI. This is a controlled
complete-return differential, not a claim that the v70 runtime currently
records a partial first-entry transition.

The Box 2 withholding field (25d) is deliberately observation-only here. The
complete helper return supplies Box 2 as a fixture input and produces a
derived 25d value, but the existing browser contribution contract admits only
`w2_box1`. Do not add a Box 2 control or promote 25d to a Box 1 impact row.
Likewise, the 35a/37 values are observed core outputs, not a reason to enlarge
the current entry loop.

### Partial-entry behavior

The legacy `_line_values` reader uses its fixed list and includes a field when
the presentation model has that line. A blocked field is retained with
`computed=false` and `value=null`; an absent expected line causes
`entry-state-unavailable` (`packages/derivation/entry_loop.py:380-416`). The
snapshot is complete only if the W-2 Box 1 finding exists, there are no blocked
rows anywhere in the run report, and every selected line is computed
(`packages/derivation/entry_loop.py:587-649`).

On the unchanged v6 seed, the initial view has one missing Box 1, five blocked
impact lines and four computed comparison lines. After a real runtime
contribution of $50,000 to Box 1, all nine are computed; the five impact rows
change and the four comparison rows remain unchanged. The v6 values are
1a=$50,000, 9/11=$53,234, 15=$38,234, 16=$4,356, with comparison values
2b=$1,234, 3a=$600, 3b=$2,000, 12=$15,000. These are existing fixture values,
not a new golden expectation.

The re-pinned thin v6 seed resolves on the actual v70 surface but produces 209
blocked rows (174 `DEPENDENCY_ABSENT`, 35 `SOURCE_SET_UNCLOSED`). On its v70
Form 1040 projection, selected fields 1a, 2b, 9, 11a/11b, 12e, 15 and 16 are
blocked; 3a and 3b still publish. The old exact-line reader refuses this v70
projection because lines 11/12 are no longer present as those identities.
This is evidence that a current-core seed needs the same complete closure and
absence-answer pattern as `current_core_returns.base_return()`; that helper
already contains Box 1 and Box 2 and is not itself a thin entry seed. Do not
interpret a zero Box 1 finding as “not entered.”

### Recorder, supplied/defaulted/derived values

The real v6 recorder accepts a single `w2_box1` contribution. It validates the
value against the W-2 Box 1 format, then records through the workspace ActLog
and real `project` / `apply_contribution_batch` path. On first entry it records
a W-2 member transition and successor family-closure assertion; a correction
to an existing current Box 1 is an assertion. The supplied source value is not
a computed tax line (`packages/derivation/entry_loop.py:726-853`). The runner
then invokes `live_coordinate_run` over the current ActLog and builds the
presentation snapshot from its report and projection (`entry_loop.py:587-649`).

The v70 completeness-pattern fixture supplies its W-2 Box 1 ($50,000) and Box
2 withholding ($4,500) in its synthetic acts. The live v70 coordinator run
resolves with zero blocked rows; Form 1040 25d is $4,500, refund 35a is $625,
and amount owed 37 is $0. Those amounts are derived outputs. Box 2 does not
exist in the legacy entry seed or browser contribution template.

For package inputs, v70 declares 12 `required` and 24 `optional_default`
bindings. When an optional binding lacks an input, `Runner` looks up that
exact fact-type version's declared `optional_default` parameter and pins the
parameter; it is not a browser-entered fact (`packages/derivation/runner.py:439-485`).
The line outputs are then derived by the resolved package's rules in the live
coordinator. The probe and this note contain only synthetic `demo.*` evidence.

## Foreman choices before Track 1

1. Adopt an explicit, fail-closed, per-core entry profile for the two observed
   packages. Use package form bindings for field identity/label/symbol, but not
   as a source of unrepresented role or money-type metadata.
2. Keep partial fields in the profile with their blocked/computed status; do
   not filter by whether a runtime value currently exists.
3. Keep Box 2 as fixture/arithmetic input only, not a new entry control or
   protocol field. Keep the established v6 seed and its nine-line behavior.
4. Preserve publication-surface resolution by adoption. Use an explicit
   release/member root and the resolver's checksum chain; refuse rather than
   silently substituting the old fixed surface.

No package/schema/content, kernel, protocol, or runner-attachment change is
needed for this evidence-backed app-level profile. If Track 1 chooses to put
role/value-kind metadata into package form fields instead, that is a separate
published-content/schema decision and must stop for owner direction; it is not
required by these findings.
