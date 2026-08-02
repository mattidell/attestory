# Review — Foreman Context Loading

- Date: 2026-07-23
- Reviewer: fresh independent process-and-implementation reviewer
- Object: `origin/main..track/foreman-context-loading-role-capsules`
- Resolved target: `18ef0f5adee1e760e8aefcb41d7819cb265632db`
- Verdict: **NOT READY**

The review-launch record and this report are not reviewed content. The target
range contains the seven commits from `742e548` through `18ef0f5`.

## Blocking finding

**M3 — stale deep-read target.** The active process plan's
`schema_or_fixture` map names `AGENTS.md#Schema Publication Protocol`, but the
selected commit's `AGENTS.md` has no `Schema Publication Protocol` heading or
section. Rendering succeeds because the renderer verifies the tracked file,
not its Markdown fragment; the capsule therefore emits a pointer that cannot
take a foreman to the promised controlling text. This is the charter's stated
failure condition for a stale or absent deep-read pointer.

Smallest remediation: make this exact deep-read target valid by adding the
authoritative schema-publication section at that heading, or point the map to
the existing complete authoritative source that supplies the required
procedure. Then rerender the selected ref and rerun this review measurement.

## Measurements

1. **Advisory boundary — PASS.** `tools/foreman_context.py` resolves the
   supplied ref to one commit, obtains each source blob as `commit:path`, and
   reads its content with `git show commit:path`. Its only worktree calls are
   separate porcelain-status and current-branch reporting. Code inspection
   found no working-tree document read, alternate-ref fallback, remote/config
   lookup, credential access, or personal-output surface. The focused tests
   also prove a selected older ref ignores a newer commit and dirty content is
   not read.
2. **Refusal behavior — PASS.** `tests.test_foreman_context` ran six synthetic
   cases successfully. They show malformed metadata and a missing ref refuse
   with exit 2; a topic mismatch refuses without capsule output; and a dirty
   worktree reports dirty state while the committed topic remains authoritative.
3. **Document contract — FAIL.** The renderer produced a non-prototype capsule
   for the resolved target with the phase-state, handoff, and active-plan blob
   identities, and correctly emitted no seat. The future live-run plan and its
   `SEAT.md` agree on `live-run-trust-domains`, planning-only status, and an
   explicitly unauthorized prototype seat. All 21 deep-read files exist at the
   selected ref, but the `AGENTS.md#Schema Publication Protocol` fragment does
   not, as recorded above. Rendering `--ref HEAD --format markdown` also
   succeeded; the review-launch commit does not change those source documents.
4. **Protocol preservation — PASS.** The modified `AGENTS.md`,
   `PROJECT_PLANNING.md`, foreman role, and handoff consistently state that the
   capsule is advisory, does not authorize dispatch, and yields to controlling
   sources. They preserve ADR-0034's contemporaneous explicit owner approval
   and retain the up-to-five-retrospectives, newest-first read before a new
   milestone plan. ADR-0039's advisory-routing posture is likewise retained.
5. **Role-capsule boundary — PASS.** Builder and reviewer seeds begin from the
   charter capsule and prohibit reconstructing their object from phase-state or
   handoff prose. The clerk seed requires one supplied mechanical task, a
   ref/commit, bounded inputs, output shape, verification, and stop rule; it
   forbids choosing or inferring task state. The role seeds do not require the
   Python renderer, and the renderer is described as foreman-only. The Trusted
   Advisor seed is unchanged in the reviewed range.
6. **Data safety — PASS.** The reviewed additions are documentation, synthetic
   temporary-repository tests, and the renderer. Its subprocess arguments are
   limited to Git revision/blob/status/branch operations; no remote
   configuration, credential, workspace, or personal-output operation is
   present. The changed-path inspection found no committed local-data or
   personal-output surface, and the envelope scan passed.

## Verification

The review worktree has no local `.venv/bin/python3`, so the prescribed checks
were rerun against the project's existing isolated environment while targeting
this review worktree:

- `python3 -m unittest` — pass (full suite; exit 0).
- `python3 -m mypy` — pass: `Success: no issues found in 108 source files`.
- `python3 tools/governance_lint.py` — pass: `governance lint: conformant`.
- `python3 tools/envelope_scan.py --range main..HEAD` — pass (exit 0).
- Focused: `python3 -m unittest tests.test_foreman_context -v` — 6 tests,
  all passed.
- Focused: `python3 tools/foreman_context.py --ref
  track/foreman-context-loading-role-capsules --format markdown` — pass;
  source resolved to `18ef0f5adee1e760e8aefcb41d7819cb265632db`.
- `git diff --check origin/main..track/foreman-context-loading-role-capsules`
  — pass.

No real workspace, credential, remote, personal output, or location was read
or recorded during this review.
