# Track 1: one path on the married-taxpayer rules

Published core v105, registry v103, release v103, from published v104.
The two successors keep the separated-recorded path and the published
default. No engine, kernel, schema, projection, or page change. The
married-taxpayer question, its fact, and the credit are unchanged. The
inert fact type stays in its published bundle.

## What the schema and the runner already do

`rule-artifact.v17` accepts one selection path. Its `selection.paths`
array has `minItems` 1:

```json
"paths": {
  "type": "array",
  "items": { "$ref": "#/$defs/selection_path" },
  "minItems": 1,
  "uniqueItems": true
}
```

`rule-artifact.v14`, which the v1 rules use, sets that `minItems` to 2.
That is why each v1 rule carries the inert path.

The runner does not count declared paths. It counts paths whose activity
is true. More than one active path refuses. One active path evaluates
that path. No active path evaluates the default:

```python
if len(active) > 1:
    return "conflict", refusal
if active:
    return "path", active[0]
return "default", default
```

A one-path rule is the two-path rule with the second path inactive.
Checked on both rules, through that plan: with no separated-spouse fact,
v1 and v2 both take the default named `neither`; with only that fact,
both take `separated-recorded`. With only the inert fact, v1 takes the
inert path and v2 takes the default. With both facts, v1 refuses and v2
takes `separated-recorded`. The package validator accepted the one-path
bodies. Nothing in the engine was edited.

## Files

New citizens, under the 2025 content directory. The fast size guard
already covers `rule.eic-*.json` at 5,000 bytes, so these two names did
not need a new cap.

| File | Bytes | sha256 |
| --- | --- | --- |
| `rule.eic-married-taxpayer-recorded.v2.json` | 4,296 | `561330e1968ceb3d719cbdf34ba6206a703c2f65134410beabab7ac601a1e8f5` |
| `rule.eic-married-taxpayer-from-separated.v2.json` | 4,360 | `6fed16b5745863be2e0ab5349df95fc3e7fe36ce4762aefd9e3fdc9ff9464ac6` |

`design.py` builds each body from the published v1 file. Schema becomes
`rule-artifact.v17`, version becomes `v2`, and the paths array keeps
only `separated-recorded`. Every other field, including the default and
the refusal, is the v1 field. Neither file names
`eic.married-taxpayer-inert`.

`package.core-calculations.v105.json` is 241,297 bytes, file sha256
`fbe38b6b14f62e8e82fa7c2faede2baaac32618305854159786f9c9112df48f4`,
package checksum
`77e0652f9a96bb46acd8f237e7f1ad10a8ea99d8a1d7763c9b4dcc3ddff640d1`.
It is the same size as v104 because the two pins change version and
schema text of the same length. `published-packages.v103.json` is
322,194 bytes, sha256
`e536b45c1722208968b5a1b2039d2aceddd28ee5850bdc201e8806f8b5ad3f84`.
The registry inserts the two v2 citizens beside their v1 rows and
inserts the v105 package row. Older rows are unchanged. Release
`demo.release.sli-worksheet-integration.2025.v103.json` is 211 bytes,
sha256
`9b8f188993711e97bd9148b1191f95e3fb1ef827352a8211cc3efc911e135c5b`,
and differs from v102 only in version and the v103 registry digest.
Package v105's members equal v104 except the two rules, which move from
v1 on rule-artifact v14 to v2 on rule-artifact v17. The v105 loader
entries carry v104's covered-flag map and companion declaration. No
schema manifest changed. Published v104 and the v1 rules were not edited.

## Replay

Full-surface replay of the 775 recorded lists, published v104 against
published v105. Expectations were the two rule versions, v1 to v2, and
the package version, v104 to v105. A numeric change matches none of them.

All 775 lists pass. 691 are success on both cores and carry the package
version (358,053 recorded version fields). 84 are error on both cores
with the same snapshot. Zero lists fail. Zero unexpected differences.
Zero lists change a number. The two rule expectations are unused: the
recorded lists do not pin either rule, so those version fields are not
on the surface the replay compares. The live cases below are where those
rules run.

## Tests

`tests/test_eic_married_one_path_v105_package.py` checks that the
published successors match the design, that v105 replaces only those two
pins, that the registry is add-only, that the release digest is the v103
registry file, and that the v105 loader entries equal v104.
`tests/test_content_file_sizes.py` already caps both new names at 5,000
bytes through the `rule.eic-*` glob. `tests/test_noncovered_sales_v78_switch.py`
includes v105 in the covered-flag list because the loader entry carries
v104's map. `tests/test_eic_married_one_path_v105.py` reruns every
eic-separated-married live case on v105 through `live_coordinate_run`:
the 31 hand returns and the six focused cases (37 tests). Credits and
asked flags match the hand. A stored inert fact is still refused at
assertion, with and without a separated-spouse answer.

The package, size, and covered-flag tests passed together (11 passed).
The live module passed (37 passed). `pytest -m "not live"` passed (1,984
passed, 8 skipped, 6,001 subtests). `python3 -m mypy` reported no issues
in 545 source files.
