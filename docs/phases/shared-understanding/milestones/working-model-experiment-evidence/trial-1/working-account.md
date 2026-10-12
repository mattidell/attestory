# Working account

## Snapshot 0 — initial action list

- **Refined:** nothing yet; wrote the first plain-language list of actions.
- **Why now:** the task asks for a list before investigation.
- **Evidence:** only a filename scan showing the repo has extensive existing
  student-loan-interest (SLI) work — many `tests/test_sli_*` and
  `test_f1098e_*` modules, saved-account and correction tracks.
- **Open questions:** does the application model spouses or filing status at
  all? Is a 1098-E tied to a person today?
- **Next:** action 1 (current behaviour) together with action 4 (prior
  decisions), since the code and documents explain each other.
- **Change of direction:** none.

## Snapshot 1 — current behaviour and prior decisions (actions 1 and 4)

- **Refined:** actions 1 and 4 together, because what the code models and
  what earlier milestones decided explain each other.
- **Why now:** every later action (law per spouse, approaches) depends on
  knowing whether the application has any notion of a second person.
- **Evidence:** `f1098e.bundle.json`, `sli-scope.bundle.json`,
  `sli-worksheet-inputs.bundle.json`, `sli-support-chain.bundle.json`
  (identity keys); entity-kind census over `packages/content`;
  `whose-deduction-model.md`; the translation milestone's non-goals;
  `f1098e-student-loan-interest-agi.md` (MFS gate, MFJ threshold);
  `packages/tax/ssa_benefits.py` (spouse-recipient precedent);
  `docs/phase-state.md`.
- **Open questions:** what the live run actually does with MFJ + two
  statements (inferred, not observed); whether "filer-centred" was meant to
  cover a joint return or simply never considered it; whether the
  return-wide "not claimed as dependent" answer is even the right question on
  a joint return.
- **Next:** action 2 (the law for MFJ), since whether per-spouse facts are
  needed at all is a legal question before it is a modelling one; then 1b.
- **Change of direction:** the question is sharper than snapshot 0 assumed.
  It is less "how do we add up two 1098-Es" (the worksheet probably does)
  and more "whose answers stand for whom": every person-level answer is
  currently singular, and the owner's filer-centred direction is the
  constraint any approach must either live within or show grounds to lift.

## Snapshot 2 — the law for a joint return (action 2)

- **Refined:** action 2, legal content for MFJ with each spouse holding a
  1098-E.
- **Why now:** snapshot 1 showed the open issue is "whose answers stand for
  whom". Whether per-spouse facts are needed is a legal question first.
- **Evidence:** 26 U.S.C. § 221 (LII); 26 CFR § 1.221-1 (LII); IRS Pub. 970
  (2025) ch. 4 on irs.gov. The 1040 general instructions page did not return
  the line 21 text through the fetch tool. All fetches came back as
  summaries, so the exact wording is still to be confirmed (2c).
- **Open questions:** 2a cross-spouse obligation; 2b spouse-timing at
  origination; 2c exact "per return" wording.
- **Next:** action 3: map each existing answer and per-statement witness
  to "about the return", "about one spouse", or "about both", using the
  law above. Run the 1b behaviour probe in the same step, because the
  mapping needs to know what the live run reads.
- **Change of direction:** none. The finding that the arithmetic already
  fits narrows the work. Any approach is about attributing answers, not
  about the worksheet.

## Snapshot 3 — which person each answer is about, and observed behaviour (actions 3 and 1b)

- **Refined:** action 3 is now a table saying, for each input, whether it is
  about the return, one spouse, or both. Action 1b is answered by
  observation instead of inference.
- **Why now:** the law (snapshot 2) says the arithmetic is per return. That
  leaves only attribution, which needs an input-by-input map.
- **Evidence:** a scratch live-run probe, `temp/mfj_probe.py` (not
  committed). It reuses `tests/test_sli_track5_worksheet_integration.py`'s
  two-statement fixture with the filing status patched through
  `_f1098e_acts`. Results: MFJ 2,500 / 1,250, MFS blocked. Also read the
  `basis` of `rule.sli-statement-loan-support.json`, worksheet v5's reads of
  the `sli-scope.*` facts, and those fact types' descriptions.
- **Open questions:** 2a–2c from before; new 2d (related-person test on
  MFJ) and 2e (the dependency question for joint filers). Also whether the
  "1098-E goes to the borrower" inference is allowed as grounds, given the
  project's said/derived/assumed discipline.
- **Next:** action 5, the plausible approaches. The map is now concrete
  enough to say what each approach would have to change and what would
  tell them apart. The open legal points go into action 6.
- **Change of direction:** the problem has narrowed to essentially one input.
  The return-wide legal-obligation answer is the one place where a joint
  return can give a wrong number today. Dependency and scope are mostly
  wording. The worksheet and statements need nothing.

## Snapshot 4 — candidate approaches and their discriminators (action 5)

- **Refined:** action 5 into four candidates (A: return-level, joint
  wording; B: per-loan obligation, filer-centred; C: per-statement
  recipient taxpayer/spouse; D: interim block). For each, the evidence
  that would separate them.
- **Why now:** snapshot 3 narrowed the gap to attribution, chiefly of the
  obligation answer. That is specific enough to list real alternatives.
- **Evidence:** re-ran the scratch probe with the obligation answer "no" on
  MFJ: line 21 = 0, no reasons. Read
  `docs/phases/evolving-workspace-accounts/milestones/account-refinement.md`
  ("shared answer" sections, P0 question 1, the correctness framing) and
  `docs/milestone-retrospectives/2026-10-08-account-refinement.md` (parked
  items). Read the fixture's `sli_scope_overrides` and
  `SLI_SCOPE_LEGAL_ZERO_TOKENS` in `tests/test_f1098e_student_loan_interest_agi_track6.py`.
- **Open questions:** 2a still decides most of it. Does the
  `whose-deduction-model.md` five-case table (obligor vs. payer) collapse on
  a joint return? Is fact-type description text covered by bundle
  checksums (affects A's cost)? Is the parked shared-answer question owned
  by another milestone?
- **Next:** action 6. Resolve or bound 2a–2e from primary sources as far as
  a planner can, and name which ones need an advisor read (governance is
  out of bounds for me and for the team's builder seats).
- **Change of direction:** I expected the decision to be "do we model the
  spouse?". The evidence says the first decision is legal (2a). Modelling
  the spouse (C) is a later question that only arises if A and B fail.
  The 0-publishing behaviour adds an interim-safety item (D) the team
  should consider whatever it selects.

## Snapshot 5 — the legal unknowns, resolved or bounded (action 6)

- **Refined:** action 6, as a status for each of 2a–2e plus three
  non-legal unknowns (6a–6c), each with how to find it out.
- **Why now:** snapshot 4 showed that 2a decides between the candidates,
  so it had to be pushed as far as public sources allow before claiming
  readiness either way.
- **Evidence:** 26 CFR § 1.221-1 (b)(4) and (e)(3)–(4) on LII; IRS Topic
  456 (2025); an irs.gov-restricted search (its summaries mention a
  "combine your spouse's amounts" sentence, but I could not tie it to the
  line 21 instructions, so I do not rely on it); the Illinois Tax School
  post and a general search, both secondary and silent on 2a; § 267(c)(4)
  family definition and § 152(b)(2), from memory of the statute, not
  re-fetched. That is a weaker basis, flagged as such.
- **Open questions:** 2a (decisive, unresolved); 2b (bounded); 6a–6c.
- **Next:** decide whether 6b is worth one quick look (it is cheap and
  affects only A's cost), then write the readiness claim (action 7).
- **Change of direction:** 2d moved the picture. I treated the
  related-person witness as wording. It is actually a second place where
  "which spouse owes this loan" matters, so the per-loan obligor is the
  real latent variable. That strengthens B against A, and I record it as a
  lean, not a selection. C is still not needed unless 2a says a payer or
  obligor identity must be carried.

## Snapshot 6 — the surface and the cost of change (6a, 6b)

- **Refined:** 6a and 6b, the two non-legal unknowns that could still
  change the readiness claim.
- **Why now:** both were cheap to check. If either had shown something
  large (an existing question that people already answer per spouse, or a
  very cheap A), the claim would change.
- **Evidence:** a grep for the `sli-scope` fact ids across `packages/`,
  `tools/` and the README. They appear only in rule and bundle content,
  sample-data act logs and fixture generators. Read
  `packages/derivation/presentation_projection.py` (only scope-unresolved
  sentences for SLI). Read core calculations v42's member list (id +
  version pinning of `sli-scope.vocabulary`) and its top-level keys.
- **Open questions:** 2a remains the only open question that decides the
  selection. Whether "explain, don't silently zero" is accepted as a
  constraint is for the owner.
- **Next:** the readiness claim (action 7). I see no further investigation
  a planner can do on 2a without the advisor seat. More public searching
  has already returned only secondary sources that are silent on it.
- **Change of direction:** 6a stops being a precondition. Because the
  questions were never posed to a person, the joint case is a design task
  for new questions, not a correction of misleading ones. That moves the
  reader assessment after selection, and it removes one argument for C
  ("people will answer for themselves"), which can be handled in the
  wording of A or B.

## Snapshot 7 — readiness claim (action 7)

- **Refined:** action 7, the readiness claim with its supports and
  preconditions.
- **Why now:** snapshots 5–6 left exactly one open question that decides
  the choice (2a), which a planner cannot settle without the advisor seat,
  and one scope choice that belongs to the owner/foreman. Further searching
  would not change the claim.
- **Evidence:** the claim rests on what earlier snapshots established:
  the live probes (MFJ 2,500 / 1,250 / silent 0, MFS blocked), §§ 221 and
  1.221-1, Topic 456 and Pub. 970 (2025), the keying of every SLI input,
  the owner's filer-centred direction, and the absence of any person-facing
  question for the return-level answers. Nothing new was consulted this
  step.
- **Claim:** not ready to select. Ready to narrow to A (return-level,
  joint wording) or B (per-loan obligation, filer-centred). C (recording
  whose statement it is) is deferred unless 2a requires it. Preconditions:
  the 2a advisor determination, the A/B scope decision, and the owner's
  view on silent zeros.
- **Open questions:** as listed in plan action 7. 2b is held as a named
  assumption.
- **Next:** if the facilitator allows a further refinement, it would be to
  sharpen action 7's characterization-test step into concrete cases,
  using the existing Track 5 fixture.
- **Change of direction:** none since snapshot 5. The claim is "narrowed,
  not ready" rather than "ready". Selecting B on the strength of 2d alone
  would mean improvising doctrine on 2a, which the project reserves for
  the advisor.
