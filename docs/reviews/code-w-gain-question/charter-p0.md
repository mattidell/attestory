# Charter: P0 of a blocked code W gain asks the filer something

Role: Builder. Source HEAD on milestone/code-w-gain-question-2025.
Plan: docs/phases/engine-breadth/milestones/code-w-gain-question.md (read
it whole). Precedents: gain-break-even (evidence and retrospective),
sale-reasons-plain (P0: sale family meaning text is pinned), ADR-0062,
ADR 0086 (a block may declare missing names), blocked-sale-pages (question
groups), and the full-surface replay in tools/recorded_replay.py (`full`).
Do not read governance.

## Scope

1. **Trace.** On published core v103, synthetic demo.* sale returns through
   the real live coordinator: covered and noncovered, short and long term,
   with a code W adjustment (box 1g) on a gain, a break-even and a loss.
   Record what blocks, each root tuple (artifact, code, missing), the page
   sentence and any question group, citing rule ids and
   presentation_projection.py file:line.
2. **Sources.** Quote the 2025 Instructions for Form 8949 on code W and
   box 1g, and ADR-0062 Decision 2: what is the filer's error or missing
   answer on a code W gain, and what should they correct or answer?
3. **Content route.** As scratch successors on v103: can a question the
   page's walk reaches be attached (an input question for the fact the
   block reads, ADR 0086 declared missing names on the blocking rule, a
   closure question), without editing pinned sale family meaning text and
   without unpinning saved sale records? Say whether a route changes which
   answer an unrelated path needs.
4. **If content cannot**, name the smallest projection or schema change
   (file:line) and whether it needs an ADR; do not build it; stop.
5. **Replay.** For a content route, full-surface replay of the 775
   recorded lists, v103 against the scratch successor, expected changes
   declared; report pass/unexpected, unused expectations, number changes.
6. **Size.** Scratch rule files against `tests/test_content_file_sizes.py`.

## Deliverables

In docs/phases/engine-breadth/milestones/code-w-gain-question-evidence/:
p0.md (trace, sources, route or stop, replay, sizes, decisions for the
foreman), scripts a later test will need, small JSON. Fill a "P0 result"
section in the plan. No production, test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed. Fetched sources
  stay in ignored temp/.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn. Do not edit packages/ or
  tests/.
