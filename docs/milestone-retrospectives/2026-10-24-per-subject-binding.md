# Retrospective — A Per-Subject Rule Reads Only Its Own Subject

## Result

- **A per-subject rule now binds only its own subject's answers.**
  `packages/derivation/subject_dispatch.py` recognises a per-subject input by
  the subject's distinguishing identity keys (entity or non-literal keys,
  excluding tax year, jurisdiction and family) and binds it from the
  subject's own scope or blocks `DEPENDENCY_ABSENT`; it never falls through
  to the run-wide environment. `packages/derivation/live.py` discovers
  per-subject inputs generally instead of only for Form 1099-K. Return-level
  inputs such as filing status keep their run-wide binding.
- **The exposed shipped rule** was the Form 1098 residence-interest reason
  (core v44 to v54): with two statements, the second's reason published as
  qualified and pinned the first statement's answers. Line 8a's
  one-statement limit kept every Schedule A and Form 1040 amount right; the
  fix removes the hazard before that limit is lifted.
- No content, schema or rule-language change; every golden is unchanged.

## What the evidence changed

- **The EIC child probe found it.** A model choice for a tax milestone
  exposed an engine defect in shipped code. The probe's comparison of rule
  shapes was worth more than its answer for the EIC.
- **"Wrong result" needed one more level of checking.** P0 reported a wrong
  shipped result from the per-statement finding; the Foreman ran the return
  level and found it contained. Both facts went into the plan.
- **Failing tests first, with one correction.** The regression tests were
  committed as strict expected failures before the engine change. The final
  review found that at that commit the EIC test failed in its own act
  builder, so its expected failure was a harness error, not the defect.
  Track 1 rebuilt that harness (rule-language operators and the refusal id).
  The final test file fails on `origin/main` at the defect itself
  (`'published' != 'blocked'`) and passes with the fix; no assertion was
  removed. A failing-first test has to fail for the reason it names.

## Process

- P0 and Track 1 ran on agy Gemini Flash, one conversation; Track 1 was
  paused mid-run at the owner's request (uncommitted edits left in the tree,
  a patch saved) and resumed with a brief naming the two things to check:
  key classification and preserved assertions.
- The final review ran on a Haiku 5.5 sub-agent, the owner's choice for
  dispatch after this track. It classified all 191 required inputs of the
  shipped per-subject rules and found none misclassified, and its cleanup
  notes (one copy of the key helper, an unreachable branch, the horizon key)
  were applied before ready.

## Follow-ups

- `live.py` falls back silently when a binding's pinned fact type is missing,
  where the old Form 1099-K path raised; the review could not show the case
  unreachable.

- A corpus-wide required-versus-read check.
- The EIC tie-breaker rules.
- `explain()` re-expansion of shared inputs.
