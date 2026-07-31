# Capital-Gain Distributions / Line 7a — Track 4 Completion Review

**Verdict: NOT READY**

## Object, posture, and boundary

- Orientation resolved `HEAD` to
  `a7d23db2a88d2edfae57a1a7c92428f59f565d85`; `git rev-parse HEAD`
  independently matched it.
- Exact records range:
  `5d0edba125f70899ea131e6d4479e4c7cf28d955..
  42d757795664c53367dd41a6141b6ec6eff97f94`. It contains one commit and
  exactly the seven chartered records paths. The completion-review
  charter/pointer commit is the records tip's direct successor and is excluded
  from the reviewed object.
- This was a fresh author-independent records review. The Track-4 Builder and
  Track-3 Reviewer threads, summaries, rationale, and self-assessments were not
  consulted.
- Evidence was limited to committed Git topology, read-only PR/CI records,
  accepted ADRs, committed independent reviews, and synthetic evidence. No
  implementation re-review, real browser/workspace, real-data operation,
  future-scope selection, or closeout was performed.
- Merged Tracks 0–2 and the line-7b prerequisite were treated as ratified
  `main` evidence. Track 3 remained reviewed branch evidence. The Track-4
  records and synthetic-complete frontier wording remained provisional.

## Measurements

### 1. Exact object and containment — pass

`git rev-list --count` returned `1`. `git diff --name-only` returned exactly:

1. `README.md`
2. `docs/milestone-retrospectives/2026-07-31-capital-gain-distributions-line7a.md`
3. `docs/phase-state.md`
4. `docs/phases/engine-breadth/coverage-frontier.md`
5. `docs/phases/engine-breadth/engine-breadth-roadmap.md`
6. `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a-deferral-ledger.md`
7. `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md`

No code, test, tool, schema, citizen, content, package, fixture, golden,
manifest, ADR, process log, charter, or context block is in the range. A
byte comparison of the `docs/phase-state.md` `foreman-context-v1` block at
both range endpoints was equal.

### 2. Merged evidence and CI — pass

Read-only GitHub records and Git ancestry independently established:

| PR | Merge commit | `verify` run | Result |
| --- | --- | --- | --- |
| #110 | `1cb12d78553479902a91c654510e7f9c88cc1934` | `30500482118` | `SUCCESS` |
| #111 | `51b0987c0607e3c3e5a16c509f1c586d01314c51` | `30507846591` | `SUCCESS` |
| #120 | `90f12e607cd4ff61770c14859b2a720763361336` | `30592473685` | `SUCCESS` |
| #125 | `ea542ece491d286c760a7409b68ab051e29bf2b1` | `30594747785` | `SUCCESS` |

All four PRs are `MERGED` to `main`, and all four merge commits are ancestors
of `origin/main`. The accepted ADR-0050 decision unit is present at PR #110;
the Track-1 `READY` repair recheck is present at PR #111; the Track-2 repair
and CI-recheck lineage is present at PR #120; and the line-7b prerequisite
review/CI-recheck lineage is present at PR #125. The records do not present a
branch review as merge-CI evidence.

### 3. Track-3 branch evidence — pass

The records tip contains the ordered Track-3 lineage: original implementation
`75c0de90ecd271a8f552657af66206be111b0038`, independent review
`22f281e8094fa126a5424949e01478e15504d11c`, first repair charter and clean
stop, amended generic repair scope `3b3291307d7a4258a2f5476208e1cecd2c0ed103`,
repair `202ae9740da7689478f0cb52386f061b4ff01b1d`, and final focused recheck
`ac31998f0d540357514dbc8ae44dc5e28919043c`.

The committed final recheck is `READY`, closes F1–F3, records exact-byte
identity for all three regenerated valid outputs, and credits unchanged
rendering/redaction evidence. The current branch is 0 behind and 12 ahead of
`origin/main`; Track 3 is not represented as a merge result.

### 4. Ten exit criteria

| Criterion | Completion-review result |
| --- | --- |
| 1. Rival-backed accepted contract | Accurate: satisfied on `main` by ADR-0050 / PR #110. |
| 2. Immutable box-2a source path | Accurate: satisfied on `main` by the reviewed Track-1 unit / PR #111. |
| 3. Line 7a and line 7b publication | Accurate: satisfied on `main` by PRs #120 and #125. |
| 4. Declared downstream recomputation | Accurate: satisfied on `main` by the reviewed Track-2 unit / PR #120. |
| 5. Honest excluded routes | Accurate: satisfied on `main` without a fabricated Schedule D. |
| 6. Lifecycle, package, and explanation battery | Accurate: the named Track-2 review and CI-recheck lineage is merged with green CI. |
| 7. Presentation guarantees | Accurate: satisfied by reviewed branch evidence, not ratified on `main`. |
| 8. Independent reviews and merge CI | Accurate: pending the closing PR's `verify` and owner merge. |
| 9. Coverage frontier | Accurate: prepared and provisional, with Schedule D still separately selectable. |
| 10. Completion records and closeout | **Not ready:** the deferral record is incomplete as measured in F1; review, closing PR/CI, merge, and mechanical closeout otherwise remain honestly pending. |

### 5. Frontier and roadmap fidelity — pass

`synthetic complete` is bounded to the eligible box-2a-only direct route and
names coordinator, lifecycle, package, explanation, and presentation evidence.
The frontier and roadmap disclaim real-data evidence, filing readiness, general
capital-gains support, and Schedule D support. Schedule D and positive-interest
expansion remain unchosen candidates, and Engine Breadth remains open.

### 6. Deferral completeness — finding F1

The ledger correctly narrows the box-2a retirement; carries the named
Schedule-D/transaction, excluded-box, interest-source, subtractive-adjustment,
migration, and infrastructure entries; preserves legacy no-`citations`
compatibility without calling it validation; and classifies repaired findings
and clean stops as discharged events. It omits one still-active predecessor
interest obligation, described in F1.

### 7. Retrospective quality — pass

The retrospective uses the compact lessons-only shape and says
`Merged: pending closing PR`. It preserves the official-instructions
correction, component-authority cost, line-7b prerequisite stop, clean
legacy-rule-wall stop, generic-invariant lesson, and credited-evidence lesson
without duplicating the implementation/test ledger. Follow-ups carry
reactivation triggers, and the next-plan changes do not select future scope.

### 8. README, phase, and lifecycle honesty — pass

README and phase prose state only the bounded synthetic capability and pending
review/merge. The plan carries the retrospective path, omits
`initial_briefing_follow_up`, remains `track-4`, and does not claim `closing`
or `closed`. The records-range phase-state machine block remains byte-identical
and points to the Builder; only the excluded direct-successor charter commit
moves the pointer to the Completion Reviewer.

### 9. Data safety and close boundary — pass

No new statement contains descriptive real-run material, private values,
dispositions, refusal reasons, credentials, or locators. No real-data
attestation was invented. The unit did not select the next milestone, create
or merge a PR, close Engine Breadth, or perform mechanical closeout.

## Finding

### F1 — The active Schedule-B multi-family interest deferral is dropped

The predecessor Dividends and Schedule B ledger carries:

```text
5. Schedule B Part I ties to the box-1/1099-INT family only.
Reactivate: an interest-breadth milestone that admits a second 1099-INT
family, or any milestone that must prove Schedule B Part I against more than
one family.
```

That entry remains active: no later ledger or reviewed evidence retires it.
The new ledger carries K-1 box 5 and market-discount sources in entry 8 and
subtractive adjustments in entry 9, but contains no `Schedule B Part I`,
`box-1/1099-INT`, `multi-family`, trigger, or exact predecessor-entry
reference. Its catch-all entry 12 is expressly limited to infrastructure and
operating items and therefore does not carry this declared-universe interest
obligation.

Reproduction:

```text
rg -n "Schedule B Part I|box-1/1099-INT|multi-family" \
  docs/phases/real-return/milestones/dividends-schedule-b-slice-deferral-ledger.md
# hits predecessor entry 5 and its trigger

rg -n "Schedule B Part I|box-1/1099-INT|multi-family" \
  docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a-deferral-ledger.md
# no matches
```

This violates the completion charter's requirement that every named interest
item remain carried with a trigger or exact predecessor reference. The
smallest residual is the missing carried disposition for that predecessor
entry; no implementation, contract, schema, content, package, fixture, test,
ADR, governance, or Real Return matrix change is implicated.

## Verification

```text
git rev-list --count 5d0edba125f70899ea131e6d4479e4c7cf28d955..42d757795664c53367dd41a6141b6ec6eff97f94
# 1

git diff --name-only 5d0edba125f70899ea131e6d4479e4c7cf28d955..42d757795664c53367dd41a6141b6ec6eff97f94
# exactly the seven paths listed in Measurement 1

git diff --check 5d0edba125f70899ea131e6d4479e4c7cf28d955..42d757795664c53367dd41a6141b6ec6eff97f94
# clean

python3 tools/governance_lint.py
# governance lint: conformant

python3 tools/envelope_scan.py --range main..HEAD
# clean

python3 tools/foreman_context.py --ref HEAD --format markdown
# track-4; Completion Reviewer pointer; 0 behind / 12 ahead of origin/main;
# spent false; no initial briefing follow-up
```

No full suite or real-data operation was run.
