# Charter: P0 of head of household needs a qualifying person

Role: Builder. Source HEAD on milestone/hoh-qualifying-person-2025.
Plan: docs/phases/engine-breadth/milestones/hoh-qualifying-person.md
(read it whole). Precedents: cf-loss-limit-evidence/p0.md (where the
observation was made), the earned-income-credit and child-tax-credit
retrospectives (how filing status and qualifying-child answers are
asked today), f1099b-bartering (a refusing question added by content),
and the full-surface replay in tools/recorded_replay.py (`full`). Do not
read governance.

## Scope

1. **Trace today.** On published core v97: what does each filing status
   change (standard deduction, tax computation, credits), which rules
   read `tax.us.2025.filing-status`, and what is asked or refused for
   head of household and qualifying surviving spouse. Build synthetic
   demo.* returns (head of household with no child or dependent
   recorded; with a qualifying child recorded for the EIC or child tax
   credit; with only an other-dependent relative; qualifying surviving
   spouse with and without a dependent child) and run them through the
   real live coordinator and saved page. Say exactly what each return
   shows. Cite file:line.
2. **Sources.** From the 2025 Form 1040 instructions and Publication 501
   in the local sources, state the head of household and qualifying
   surviving spouse tests (qualifying person, home cost, marital status,
   year of the spouse's death, dependent child) and which of them the
   engine already records or can ask. Check accepted ADRs and rule notes
   for a bound on filing status.
3. **Design.** The smallest honest change. Prefer content: input
   questions that ask the tests the filer must meet, refusing a "no"
   with a named reason, and, where the record already proves a
   contradiction, a refusal. Do not make a filer who qualifies answer a
   question the record already proves, and do not change which answer
   single, married filing jointly or married filing separately needs.
   Prototype it as a scratch core successor on published v97, loaded
   from published content, never by editing packages/.
4. **Replay.** Full-surface replay of the 775 recorded lists, v97 against
   the scratch successor, with the expected changes declared; report
   pass/unexpected and unused expectations, how many recorded returns
   use each status, and whether any computed return newly blocks or
   changes a number.

Stop and report if the honest design needs an engine, schema,
projection, page or kernel change, or a new ADR.

## Deliverables

In docs/phases/engine-breadth/milestones/hoh-qualifying-person-evidence/:
p0.md (trace, sources with citations, bounds, design, prototype and
replay results, recommendation, decisions for the foreman), scripts and
small JSON. Fill a "P0 result" section in the plan. No production, test
or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Bound every command that can hang (for example
  `perl -e 'alarm 900; exec @ARGV' ...`); never `rm -rf`, create fresh
  scratch directories instead.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn. Do not edit packages/ or
  tests/.
