# Charter: Track 3 — F1 Remediation (glob-order test fragility)

Date: 2026-07-20. Prepared by the foreman; owner-approved dispatch
(ADR-0034). Branch: `track/dsbs-t3-qdcg-line16` (continue on this branch —
do not open a new one). Governing finding:
`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-20-dsbs-t3-qdcg-line16-review.md`, Finding F1.

## Background

The Track 3 pre-merge review found the required verification battery not
green: two pre-existing, unrelated tests —
`tests/test_frrs_t3_resolver_bootstrap.py::test_changed_member_bytes_under_honest_registry_refuses`
and
`tests/test_frrs_t4_w2_live_integration.py::ResolverCounterProbes::test_member_substitution_has_exact_refusal_and_layout_is_inert`
— fail on this branch though they pass at base `ebec569`. Both tests tamper
with the bytes of "a rule file" selected via an unfiltered
`glob("rule.*.json")` / `next(content.glob("rule.*.json"))`, implicitly
relying on directory/glob ordering to land on a rule file that is actually
a checked member of the specific package or release each test resolves
against. Track 3's new `rule.form1040-line16.v2.json` now sorts first
lexicographically, so the mutation lands on a file that is not a member of
the package/release those two tests actually resolve — the tamper goes
undetected, the expected `Refusal` never fires, and the assertion fails.

This is not a Track 3 correctness defect — the new content file, its
package pin, and its checksums are all independently confirmed correct by
the review (Checks 1–9, all pass). It is a latent fragility in two
FRRS-era tests that predates this branch and was only ever masked by
accidental glob ordering.

## Scope (exactly this, nothing more)

Fix the two tests so each deterministically selects a rule file that is
genuinely a member of the specific package/release/registry surface that
test's own scenario resolves against — not an arbitrary "first" file from
an unfiltered directory glob. Read each test's own `_surface(...)` call
(what package version, release, or registry file it actually points at)
and select a member consistent with that, e.g. by reading the relevant
package/release manifest's own member list and picking a `rule.*` entry
from it, rather than scanning the content directory blind. Preserve each
test's existing assertions and intent exactly (still expects a `Refusal`
with the same `reason` string) — only the file-selection mechanism changes.

Do not touch: any DSBS/Track 3 content, schema, or kernel file; any other
test in either file; the package resolution/validation implementation
itself (`packages/derivation/package_validation.py` or similar) unless you
first confirm in writing that the two tests cannot be fixed without a
production-code change — that would be a charter-stop, escalate rather than
implement it. Do not touch `tools/scaffold_live_acts.py` or
`workspace-seed/`.

## Verification

Before reporting done, all green:
- `.venv/bin/python3 -m unittest` — full suite, confirm both previously
  failing tests now pass and nothing else regresses (full count, not just
  the two)
- `.venv/bin/python3 -m mypy`
- `.venv/bin/python3 tools/governance_lint.py`
- `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD`

Also re-confirm the review's own base comparison methodology is now moot:
run the two previously-failing tests once more standalone to show a clean
pass, and note the exact mechanism change (what each test selects now and
why it's deterministic against its own package/release surface, not
directory order).

## Commit discipline

One commit (or a small tight sequence) on `track/dsbs-t3-qdcg-line16`,
directly following `d858172`/`c0731f4`. Do not push, merge, or edit
`docs/phase-state.md`/`docs/foreman-handoff.md` — the foreman updates those.

## Report back

State: the exact selection mechanism each test now uses, full battery
pass/fail, and whether escalation was needed (and why) if you hit the
charter-stop condition above.
