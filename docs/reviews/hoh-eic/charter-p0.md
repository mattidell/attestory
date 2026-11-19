# Charter: P0 of the earned income credit for a head of household

Role: Builder. Source HEAD on milestone/hoh-eic-2025.
Plan: docs/phases/engine-breadth/milestones/hoh-eic.md (read it whole).
Precedents: hoh-qualifying-person-evidence/p0.md (section 1 and finding
5, where this was found; probe.py builds head of household returns),
the earned-income-credit and eic-qualifying-children retrospectives (how
the credit and its questions are built), and the full-surface replay in
tools/recorded_replay.py (`full`). Do not read governance.

## Scope

1. **Trace today.** On published core v98: how `rule.eic-status-class`
   and the rules that read it decide the credit for each filing status,
   with and without a qualifying child, and what is asked (including the
   separated-spouse answer). Build synthetic demo.* head of household
   returns (answered yes) with a dependent parent and no child, with an
   EIC qualifying child, and with a child too old for the credit, at low
   and phase-out incomes; and single and married filing separately
   controls. Run them through the real live coordinator and saved page.
   Cite file:line.
2. **Sources.** From the 2025 Form 1040 line 27a instructions (and
   Publication 596 if local), state exactly when a head of household can
   take the credit with no qualifying child, how "married" is judged for
   Step 4 question 1, and how that relates to the head of household
   "considered unmarried" test. Check accepted ADRs and rule notes for a
   bound.
3. **Design.** The smallest honest change: which answer tells an
   unmarried head of household from a married one, whether the record
   (v98's `hoh.tests-met`, the separated-spouse answer, a counted child)
   already proves it, and if not, one new question asked only of a head
   of household with no qualifying child. Never change the credit for
   any other filer. Prototype it as a scratch core successor on
   published v98, loaded from published content, never by editing
   packages/.
4. **Replay.** Full-surface replay of the 775 recorded lists, v98 against
   the scratch successor, with the expected changes declared; report
   pass/unexpected and unused expectations, and pair the probes.

Stop and report if the honest design needs an engine, schema,
projection, page or kernel change, or a new ADR.

## Deliverables

In docs/phases/engine-breadth/milestones/hoh-eic-evidence/: p0.md
(trace, sources with citations, bounds, design, prototype and replay
results, recommendation, decisions for the foreman), scripts and small
JSON. Fill a "P0 result" section in the plan. No production, test or
content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`, retrying every
  10 s for up to 5 min if held.
- Bound every command that can hang (e.g. `perl -e 'alarm 900; exec @ARGV' ...`);
  never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn. Do not edit packages/ or
  tests/.
