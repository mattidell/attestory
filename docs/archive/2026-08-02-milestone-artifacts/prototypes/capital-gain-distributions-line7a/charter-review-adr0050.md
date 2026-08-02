# ADR-0050 Contract Review Charter

Audience: Reviewer

Date: 2026-07-28. Track 0 of Capital-Gain Distributions and Form 1040
Line 7a.

## Context Capsule

- **Source ref and resolved launch commit:** use the current local
  `decisions/capital-gain-distributions-line7a` branch and verify its commit at
  launch.
- **Exact object:** synthesis commit `6ec26fd`, limited to proposed ADR-0050,
  its advisory index row, and `evaluation-analysis.md`.
- **Role:** fresh author-independent Contract Reviewer, High capability /
  high effort.
- **Scope:** test whether the proposed ADR is a complete, evidence-traceable,
  internally consistent successor contract suitable for owner ratification.
  No production work and no ratification.
- **Stop conditions:** any attempt to repair or rewrite the draft, interpret
  governance, add a proposition, climb the evidence ladder, edit accepted ADR
  history, inspect another agent's thread, use real data, or enter production.
- **Full reads before acting:** this charter;
  `charter-contract-synthesis.md`; proposed ADR-0050;
  `evaluation-analysis.md`; `final-disposition.md`; the topic `plan.md`;
  `round-1-triage.md`; `repair1-confirmation-disposition.md`; both exhibit
  designs/examinations; both committee reviews; both repair
  designs/examinations and confirmations; the milestone plan's Contracts,
  Published-schema and migration posture, Fixtures, and Data Safety sections;
  ADR-0010, ADR-0011, ADR-0012, ADR-0014 through ADR-0017, ADR-0020,
  ADR-0023 through ADR-0025, ADR-0027, ADR-0029, ADR-0032, ADR-0035,
  ADR-0037, ADR-0038, and ADR-0046; `docs/adr/INDEX.md`; and
  `PROJECT_PLANNING.md` sections “Prototype Before Ratification” and
  “Architecture Decision Records.”

## Assignment

Attempt to falsify the proposed contract. The Builder's clause-to-evidence map
is routing, not proof.

### 1. Evidence fidelity and traceability

For each ADR decision clause D1–D9:

- identify the exact selected paper sentence/case and final confirmation
  measurement that supports it;
- flag any normative claim stronger, broader, or more specific than the
  evidence;
- confirm rejected alternatives, topology costs, dissent, repair history, and
  non-blocking observations are represented without rewriting their outcome;
  and
- confirm links use stable named evidence and the two exhibit refs rather than
  relying on an unmerged commit SHA.

Failure is any central clause whose trace ends in self-assessment, an
unconfirmed case, or unsupported synthesis prose.

### 2. Accepted-history and successor compatibility

Check ADR-0050 clause by clause against the accepted ADRs named in its Links:

- no accepted ADR decision text, published schema/content, checksum, or
  historical universe is edited or treated as mutable;
- the versioned-successor effects on ADR-0035 and ADR-0038 are exact and do
  not accidentally supersede unrelated accepted behavior;
- box-2a successor/history exclusivity and package rejection are coherent with
  ADR-0027;
- closure, horizon, correction, supersession, and pin obligations are
  compatible with ADR-0010/0011/0014–0017/0023; and
- disposition, conditional, explanation, citation, and presentation claims
  remain within ADR-0012/0020/0024/0025/0029/0037/0046.

Failure is any silent mutation, dual authority, missing required closure pin,
ambiguous successor boundary, or invented committed substrate.

### 3. Contract completeness and determinacy

Measure ADR-0050 against all eight milestone Contracts clauses. In particular,
try to produce two compliant implementations that disagree on:

- the exact four authority facts or checked conclusion;
- eligible, blocked, guard-inapplicable, and closure-backed-zero outcomes;
- which box-2a representation may contribute;
- line-7a/7b publication and pin sets;
- line 9 and downstream behavior when the direct route is missing or
  guard-inapplicable;
- QDCG selection, worksheet line-3 binding, and both-zero reduction; or
- correction/displacement and contradiction behavior.

If the ADR permits materially different answers, report the ambiguity as
decision-blocking. Specifically test whether N2's “production may refine”
language leaves a required line-9 disposition undecided rather than merely an
implementation presentation choice.

### 4. ADR and index form

Confirm Tier 2 is justified, status is `proposed` and inert, required ADR
sections are present, prose is readable without the thread, the index row
matches the draft without implying acceptance, and no process rule is
misfiled as a product contract.

Run:

```sh
python3 tools/envelope_scan.py --range main..HEAD
```

Do not run the test suite; this is a documentation decision unit.

## Output and verdict

Create exactly:

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/reviews/adr0050-contract-review.md`

Report:

1. D1–D9 as `SUPPORTED` or `UNSUPPORTED`;
2. all eight milestone Contracts clauses as `CLOSED` or `OPEN`;
3. `HISTORY COMPATIBILITY: PASS` or `FAIL`;
4. `ADR/INDEX FORM: PASS` or `FAIL`;
5. numbered falsifiable findings with severity, exact evidence, and the unmet
   charter clause;
6. `READY FOR OWNER RATIFICATION` only if every decision is supported, every
   contract clause is closed, and both compatibility/form checks pass;
   otherwise `NOT READY`; and
7. whether any residual uncertainty requires more evidence rather than a
   bounded drafting repair.

Commit only the review locally and stop. Do not push, merge, repair the draft,
ratify ADR-0050, begin production, or advance the pointer. Return the commit
SHA and all status lines.

## Data safety

All evidence is synthetic and publishable. No personal values, identities,
dispositions, refusal reasons, workspace locations, documents, screenshots,
or private artifacts may enter the review.
