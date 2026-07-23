# Review Charter — Foreman Context Loading

Status: **prepared; no reviewer is authorized by this charter.** Under
ADR-0034, the owner must explicitly approve the current reviewer role and this
charter before any dispatch.

## Object of review

The complete Foreman Context Loading milestone from `origin/main` through
`track/foreman-context-loading-t2`, including the planning record, ADR-0042,
paper evidence, renderer/tests, and re-entry-document changes.

## Reviewer role and independence

One fresh, independent process-and-implementation reviewer. The foreman wrote
the reviewed material and must not review its quality. The reviewer receives no
real-workspace, credential, remote, personal-output, or location context.

## Measurements

1. **Advisory boundary.** Read ADR-0042's Decision and compare it to
   `tools/foreman_context.py`. Demonstrate whether the code reads only the
   explicit selected commit's blobs; reports worktree state separately; and has
   no fallback to working-tree document content, another ref, a remote, or a
   private-data surface. Failure: a code path or fixture permits any forbidden
   fallback or access.
2. **Refusal behavior.** Run `tests.test_foreman_context` and inspect its
   fixture cases. Confirm that malformed metadata, a missing ref, topic
   disagreement, and a dirty worktree have the claimed outcomes. Failure: an
   invalid/mixed state yields a successful capsule, or dirty content becomes
   authoritative.
3. **Document contract.** Render
   `tools/foreman_context.py --ref HEAD --format markdown`; independently
   verify its source blobs and all deep-read targets exist at that selected ref.
   Confirm the active process milestone legitimately has no seat while the
   future live-run prototype's plan and `SEAT.md` agree. Failure: a capsule
   source/deep-read pointer is stale, absent, or contradictory.
4. **Protocol preservation.** Compare the modified `AGENTS.md`,
   `PROJECT_PLANNING.md`, foreman role, and handoff against ADR-0034 and
   ADR-0039. Failure: any wording lets the capsule authorize a dispatch, omit
   the five-retrospective read before new-milestone planning, or become a
   competing authority.
5. **Data safety.** Inspect committed paths and renderer subprocess arguments.
   Failure: a committed fixture/record contains personal or absolute local
   data, or the tool can inspect a workspace, credential, remote configuration,
   or personal output.

## Required verification

Run the full verification floor:

```sh
.venv/bin/python3 -m unittest
.venv/bin/python3 -m mypy
.venv/bin/python3 tools/governance_lint.py
.venv/bin/python3 tools/envelope_scan.py --range main..HEAD
```

## Verdict

Return `READY` only if every measurement is explicitly run or directly
inspected with no blocking finding. Otherwise return `NOT READY`, identify the
measurement, exact path, and the smallest evidence-backed remediation. Do not
expand scope into live-run enforcement, credential controls, or generic context
summarization.
