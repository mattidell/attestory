# Retrospective: Rule Language Design

## Milestone

- Phase: Foundation
- Branch model: declared protocol deviation — documents landed on `main` directly (seat dispatch requires continuous visibility); prototype code lived on iteration branches, concluded as tags `exhibits/rule-language/it0` / `it1` (`362f8a3`) / `it2` (`623957c`), never merged
- Document set: `docs/archive/2026-08-02-milestone-artifacts/prototypes/rule-language/` (charter v2, two examinations, three review rounds plus round 0, two legibility scorings, process log, evaluation analysis)
- Decisions: ADR-0006 (rule artifact language, Tier 3), ADR-0007 (derived-publication act kind, Tier 2, amended pre-ratification), ADR-0008 (derivation record placement, Tier 2) — all ratified 2026-07-10

## Shipped

The rule-artifact language is designed from evidence and ratified. Two clean-room iterations drafted all fourteen charter fixtures (real 2025 federal rules) in genuinely different encodings; three review rounds (plus a charter round) measured them with four independent instruments; the evaluation analysis traces eleven conclusions and eight ratification conditions to followable exhibits. Derivation Machinery re-planning is unblocked.

## Verification

- `python3 -m unittest` (project venv) — 98 tests, OK; `tools/governance_lint.py` — conformant; `mypy` — no issues. Documents only merged; exhibits verified by reviewers from tags with reproducible commands.
- Process verification per the milestone: every iteration has a charter, examination, and reviews; dissent recorded and honored; owner check-ins followed the fixed shape; one owner sampling audit performed (round-2 expressiveness — passed).

## What the process produced that a single designer would not have

- **Independent convergence as evidence.** Two builders who never saw each other's work chose expression trees, separate parameter citizens, role-bearing pins, and a distinct publication act. This is the strongest evidence class in the analysis, and it was only *observable* because the rival was genuinely clean-room.
- **The decisive finding came from attack parity.** Re-running round-1's successful attacks against it2 revealed the schema-file-never-loaded regression — the single most consequential fact of the effort — and the two attacks that *failed* against it2 are the cleanest before/after contract evidence produced.
- **The starved instrument works.** Two fresh-reader legibility reviews, different model contexts, zero wrong recoveries across both corpora, and each found real defects no other instrument caught (round 1: the F5 label mismatch; round 2: the dangling line24/line33 inputs, the MFS/QSS table gap).
- **Dissent discipline paid off at the end.** The governance sign-off's bounded dispute caught a real gap in the ADR drafts (governance-pin runtime source) minutes before ratification; the remedy was adopted verbatim, not reworded.

## The process itself as subject (the milestone's second charge)

Six incidents, four rule versions. The pattern across them is one lesson stated three ways:

1. **Every channel visible at dispatch is a leak channel, and they must be enumerated, not assumed.** The independence rule was breached through role-file ambiguity (round 0), process-log outcome summaries (round 1), and a commit-message body (round 2) — each a *previously unenumerated* channel, each fixed by naming it (v2: peer reviews; v3: log entries and commit bodies event-only during open rounds; v4: one-seat-per-identity). A future process should start from the full enumeration: role files, seat file, log, commit subjects and bodies, auto-injected session context, and session identity itself.
2. **Rules stated as asides get violated; rules stated as rules hold.** The expressiveness examination-ordering requirement was violated in rounds 1 and 2 by *different agents* while it lived in a parenthetical, which convicts the phrasing. After promotion to an explicit rule with a required disclosure point, no violation.
3. **Disclosure discipline is the real safety net.** Every contamination was self-disclosed before the foreman could have detected it independently. Reviews stayed usable because measurements were command-reproducible — reproducibility, not purity, is what made contaminated instruments salvageable.

Other process findings:

- **Succession works.** The foreman seat transferred mid-round to a fresh agent via seat file and log alone; no context was lost that the documents didn't carry. The documents-on-`main` deviation earned its keep here.
- **Charter under-specification shows up as cross-iteration convergent defects.** Both clean-room builders left rounding tie-break and false-vs-blocked semantics evaluator-carried — evidence the *charter* under-specified those points, a diagnostic worth using deliberately next time.
- **Worktree hygiene**: one incident (it1 builder in the primary checkout), fixed by role rule; all subsequent builders/reviewers used disposable worktrees, all removed clean.
- **Owner-authored log entries have no commit convention** — the owner's audit entry sat uncommitted until noticed. If owner audits recur, adopt "owner writes, foreman commits," mirroring the starved-seat convention.
- **Starved seats cannot sign off** on documents that would de-starve them; the analysis records the exclusion explicitly. Acceptable, but it means legibility evidence reaches ADRs only through foreman scoring — a trust link worth keeping visible.
- **Session-date drift**: sign-off sessions self-dated 2026-07-11 during a 2026-07-10 process day. Harmless here; a future process should pin the process-day date in the round file.

## Deviations

- Declared up front: no milestone execution branch (documents on `main`). Honored throughout; prototype code never merged.
- Round 0 (charter review) was added beyond the milestone's minimum — it caught ten charter amendments before any building and was the cheapest defect-removal of the effort.
- The iteration cap (three) was not consumed: two iterations sufficed because the comparative round answered the open questions.

## What carries forward

- The eight ratification conditions in `evaluation-analysis.md` §5 are Derivation Machinery's entry checklist — schema-as-runtime-authority and operation-semantics canon chief among them.
- ADR-0005's process is validated with amendments to adopt: the v4 independence rule set, event-only log/commit hygiene during open rounds, explicit ordering rules, and the leak-channel enumeration above belong in the process definition, not rediscovered per topic.
