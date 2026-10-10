# Finances — Auditable Tax Computation

A personal tax return engine built so that every value on the return can answer for itself: what findings it rests on, what rules produced it, who asserted or adopted what, and when. Tax meaning lives in declared, versioned rule artifacts — data, not code — executed by a thin engine over an append-only workspace record.

This is the project's third iteration. The first proved a working return generator; the second refined the development process; the third fleshed out the conceptual layer into a ratified governance set as the basis for agent-driven development.

## Where things stand

- **Governance** (`docs/governance/`): the ratified v0.1 set — Constitution, Ontology, Engineering Constraints, Principles, Commentary. The sole contract authority for this repository.
- **Phase state** (`docs/phase-state.md`): Engine Breadth is active; the next
  breadth milestone is unselected.
- **Current bounded capability:** production-shaped synthetic returns cover
  the Form 1099-DIV box-2a direct-reporting route, Schedule K-1 (Form 1065)
  box-5 taxable interest, payer-reported current-inclusion market discount
  from Form 1099-INT box 10 or Form 1099-OID box 5, and covered, basis-
  reported Form 1099-B transactions — short-term or long-term, gain or
  loss — reported directly on Schedule D line 1a/8a without Form 8949,
  including the signed Schedule D line 16, the current-year $3,000/$1,500
  capital-loss limitation (line 21), the correct Schedule D-bound QDCG
  line-16 path at any sign of Schedule D's result, and an honest attachment
  disposition/explanation walk. A short-term or long-term capital-loss
  carryover derived from a bounded 2024 prior-return authority via the
  IRS Capital Loss Carryover Worksheet is included on Schedule D lines 6
  and 14, with lines 7/15/16/21 and Form 1040 line 7a/9 recomputed
  accordingly. A covered, basis-reported Form 1099-B transaction routed
  to Form 8949 solely by a broker-reported box-1g wash-sale loss (code W)
  is also supported, through Schedule D lines 1b/8b. One or more 2025 Form
  1098-E statements' deductible student-loan interest, each form supported
  by its older eligibility answers, its recorded loan detail, or both,
  capped at $2,500 and reduced by the MAGI phaseout, is computed on the Student Loan
  Interest Deduction Worksheet and carried through Schedule 1 lines 21/26
  into Form 1040 line 10 and AGI — the first supported route on the
  income-adjustment side of the return. Any amount carried
  forward into 2026, noncovered securities, digital assets, every Form
  8949 adjustment code other than W, other Schedule D sources,
  subtractive interest adjustments, MFS filers, other Schedule 1 Part II
  adjustments, filing, and broader securities history remain outside the
  supported classes.
- **Planning** (`PROJECT_PLANNING.md`, `docs/phases/`): the planning protocol and phase/milestone/track documents.
- **Agent guide** (`AGENTS.md`): operating rules for development agents.
- **Decisions** (`docs/adr/`) and **retrospectives** (`docs/milestone-retrospectives/`).
- **Historical documents** (`docs/archive/`): completed execution evidence and
  superseded planning. Reference only; not a source of contracts.
- **Legacy engine** (`archive/`): the pre-governance v2 implementation.
  Reference only; not a source of contracts or current patterns.

## Verification

```sh
pytest                         # full suite, parallel gate run (~61s; pytest.ini sets -n auto)
pytest -m "not live"           # fast lane, units only (~4s); see AGENTS.md "Test lanes"
pytest tests/test_<module>.py  # targeted run while iterating (~2s)
python3 tools/governance_lint.py   # governance set structural checks
python3 -m mypy                # type checks (tools)
python3 tools/foreman_context.py --ref HEAD --format markdown  # advisory foreman re-entry routing
python3 tools/audit_push_envelope_posture.py  # local synthetic hook/bypass posture
python3 -m packages.kernel.runners.inspect_workspace --workspace packages/sample_data/kernel/demo_workspace
python3 -m packages.derivation.runners.derive --scenario packages/sample_data/derivation/scenarios/first_slice/scenario.json
python3 -m packages.derivation.runners.derive --scenario packages/sample_data/tax/scenarios/two_w2_same_employer/scenario.json
python3 -m packages.derivation.runners.derive --scenario packages/sample_data/tax/scenarios/closure_backed_zero_1099int/scenario.json
```

The `derive` runner executes a rule package over the operation-semantics canon and prints each derived value with an explanation tree — the rule that produced it, the findings it consumed (recursing into derived inputs), and the parameters, canon, adoption, and governance it stood on. Explanation is a walk of the finding's pins, never a re-evaluation. The `first_slice` scenario is synthetic demo machinery; the `packages/sample_data/tax/scenarios/` scenarios exercise the real tax content — synthetic W-2 box-1 findings deriving 2025 Form 1040 line 1a, and synthetic Form 1099-INT box-1 findings deriving the B1 source subtotal, including the closure-backed empty-family zero that pins its adopted mapping and closure authority.

`audit_push_envelope_posture.py` is deliberately not a push guard. It builds a
disposable local Git fixture to demonstrate two facts: the installed hook
refuses a seeded marker when Git runs it, and `git push --no-verify` bypasses
that hook. Its `credential_confinement: "unestablished"` result is the point;
it neither examines this clone's credentials/hooks nor protects an owner push.

`python3 tools/audit_push_envelope_posture.py` creates only a fresh temporary
repository and local bare remote. Its JSON record verifies installed hook bytes
and a hooked seeded-marker refusal, then honestly reports that a raw
`git push --no-verify` can reach that synthetic remote. It reports credential
confinement as `unestablished`; it neither contacts a network remote nor
inspects credential material.

## Correction session walkthrough

The synthetic student-loan interest correction session opens one saved result and lets you review one borrowing's loan-cost answer. Wording is provisional. Each command seeds one named state, prints what that state is, and serves the page on loopback. Stop with Ctrl-C. Run the same command again for a clean start.

```sh
python3 -m packages.derivation.runners.sli_correction_evaluation --state STATE
```

`--help` lists the state names.

- **base** — `python3 -m packages.derivation.runners.sli_correction_evaluation --state base`
  Two forms, each with its own borrowing, both answered yes: Cedar carries "Autumn study loan" and Birch carries "Spring study loan". Review Autumn on Cedar and change yes to no. Cedar's new result should show that no, with the earlier yes as history, and say why the form is blocked. Birch stays as it was. The earlier result on the page stays unchanged.

- **d1** — `python3 -m packages.derivation.runners.sli_correction_evaluation --state d1`
  Cedar carries Autumn (affirmed, with financing and a yes loan-cost answer) and Spring, whose inclusion on Cedar is denied. Birch is the older method only, with no borrowing of its own. Under "What the person said", Spring's denial appears attributed to Spring study loan. The "recorded, not used" lines describe the enrollment answer and the loan-cost answer as answers "on a borrowing this form denied". Both Autumn ("included") and Spring ("not included") are offered as loan-cost choices.

- **shared** — `python3 -m packages.derivation.runners.sli_correction_evaluation --state shared`
  One borrowing, "Autumn study loan", is included on both Cedar and Birch. The single choice should name both forms before you confirm. Change the answer to no. Both forms' rows should change, and each should attribute that answer to the same borrowing.

- **duplicate-labels** — `python3 -m packages.derivation.runners.sli_correction_evaluation --state duplicate-labels`
  Two borrowings are both labelled "Starlight study loan", one on Cedar and one on Birch. Each choice shows its own clues (which form it is included on) before you click, so you can tell them apart. Pick one and confirm you opened the form you meant. A further pair labelled "Twin study loan" is truly identical and is not offered; choosing it directly is refused, and nothing is written.

- **blocked** — `python3 -m packages.derivation.runners.sli_correction_evaluation --state blocked`
  Cedar's "Autumn study loan" starts as no, so Cedar starts blocked. Birch's "Spring study loan" stays a plain case. Review Autumn, change no to yes, and confirm. Cedar should unblock, show the new yes, and keep the earlier no as history. Birch stays as it was.

- **historical** — `python3 -m packages.derivation.runners.sli_correction_evaluation --state historical`
  This builds on base, applies one correction (Cedar's loan-cost answer, yes to no) before the page opens, then opens the earlier result. The page should say that result is earlier and not current. Cedar's choice should say the answer has since changed. The confirmation should name the earlier yes and the current no, and say the review is of the current answer. Confirming changes that current answer; it does not write against the old finding, and the earlier result's files stay as they were. A withdrawn answer is not a runner state; the tests cover it, and there the page says there is nothing to correct and offers no save.

## Data safety

Nothing personal is committed: no real tax documents, no personal fact instances, no artifacts derived from personal data. Committed fixtures are synthetic and publishable. Personal work stays under ignored paths (`local-data/`, `temp/`, `private-archive/`, `uploads/`, `generated/user/`). See Article 18 (Quarantine) and the data safety rules in `AGENTS.md`.
