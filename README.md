# Finances — Auditable Tax Computation

A personal tax return engine built so that every value on the return can answer for itself: what findings it rests on, what rules produced it, who asserted or adopted what, and when. Tax meaning lives in declared, versioned rule artifacts — data, not code — executed by a thin engine over an append-only workspace record.

This is the project's third iteration. The first proved a working return generator; the second refined the development process; the third fleshed out the conceptual layer into a ratified governance set as the basis for agent-driven development.

## Where things stand

- **Governance** (`docs/governance/`): the ratified v0.1 set — Constitution, Ontology, Engineering Constraints, Principles, Commentary. The sole contract authority for this repository.
- **Phase state** (`docs/phase-state.md`): on core calculations v53 a filer
  with no qualifying child gets the 2025 earned income credit (see "2025
  earned income credit" below). Use `python3 tools/foreman_context.py --ref HEAD` for
  current routing; publication status is tracked by the pull request's checks.
- **Current bounded capability:** production-shaped synthetic returns cover
  the Form 1099-DIV box-2a direct-reporting route, Schedule K-1 (Form 1065)
  box-5 taxable interest, payer-reported current-inclusion market discount
  from Form 1099-INT box 10 or Form 1099-OID box 5, and covered, basis-
  reported Form 1099-B transactions — short-term or long-term, gain or
  loss — reported directly on Schedule D line 1a/8a without Form 8949,
  including the signed Schedule D line 16, the current-year $3,000/$1,500
  capital-loss limitation (line 21), the Schedule D-bound QDCG line-16 path
  at any sign of Schedule D's result (on core v50 and later, with only
  long-term gain preferential), and an honest attachment
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
pytest                         # full suite, parallel gate run; pytest.ini sets -n auto
pytest -m "not live"           # fast lane, units only; see AGENTS.md "Test lanes"
pytest tests/test_<module>.py  # targeted run while iterating
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

## Mortgage statement answers

The bounded mortgage account reviews the current Form 1098 statement and its
saved ordinary answers. For the v2 filing-unit question set, select v2 when
preparing the review; the saved answers must match the questions actually
shown. The package is core-calculations v45 in published registry v43 and the
student-loan worksheet integration release v43. A synthetic v2 answer set
looks like this:

```python
answers = {
    "filing-unit-owns-home": "yes",
    "shared-main-home": "yes",
    "home-is-collateral": "yes",
    "owes-the-loan": "yes",
    "paid-the-interest": "yes",
    "no-one-else-owes-it": "yes",
    "what-the-money-paid-for": "bought-the-home",
    "this-is-the-original-loan": "yes",
    "mortgage-credit-certificate-received": "not-received",
}
```

The callable review and save operations live in
`packages.tax.f1098_statement_review`: `prepare_f1098_statement_review`,
`save_f1098_statement_review`, `answer_f1098_statement_review_question`,
`correct_f1098_statement_review_answer`, and
`withdraw_f1098_statement_review_answers`, plus
`review_f1098_statement_with_saved_presentation` for a fresh account beside its
saved explanation. Start the example with
`prepare_f1098_statement_review(workspace, bundle_version="v2")`; save that
review with `bundle_version="v2"` (or use its reviewed selection). The first
incremental answer also adopts the reviewed version. The default remains v1
for existing callers. Historical v1 answers retain their personal ownership
and residence meanings; they are not automatically reinterpreted as the v2
filing-unit propositions, and a v1-only record does not supply v45's new
inputs. The v44 route remains available for historical v1 records. Each save is tied to the statement
and answer snapshot it showed. For a personal-expense answer, the two timing
questions may be answered together, one at a time, or left absent. The review
shows the bundle's `not-asked` default declaration (with its parameter id and
version) separately; absence is not an answer offered to the person. A saved
run's actual default provenance comes from its validated explanation. A current
unresolved run is shown from its validated unresolved section, never as a
completed account.
“No” to who paid means neither spouse on a joint return paid any interest and
nobody paid any for them. Third-party or partial payment has its own answer.

This route covers one current Form 1098 statement, its reported box 1 interest,
and the selected ordinary circumstances. It does not allocate mixed use,
cover multiple mortgages or homes, or compute the mortgage credit. After an
answer changes, an earlier saved calculation is identified by its recorded
run and workspace revision; a different revision means recalculation is
needed.

## Personal-item sale on Form 1099-K

The bounded Form 1099-K route reviews each current Form 1099-K statement and its
saved circumstance answers for a personal item sold through a payment card or
third-party settlement organization. When the family is closed and every current
statement's answers establish a nondeductible personal loss, the statements'
Box 1a gross amounts are added and entered at the top of Schedule 1 (Form 1040)
exactly once, while the return's net income on Form 1040 lines 8 and 9 remains
unchanged. Each statement keeps its own reason, figures and saved explanation;
any other reason on any statement, a blocked statement or an unclosed family
blocks the combined entry.

The route names but does not report other outcomes: transactions resulting in a
gain or profit, transactions that broke even, items not acquired by purchase,
items with lasting improvements or other basis adjustments, transactions
involving digital assets, transactions with federal backup withholding (Box 4),
sales where the person paid additional shipping beyond a platform-supplied label
(`additional-seller-shipping-unsupported`),
or missing/unanswered circumstance questions.
For any of these, the route publishes an unresolved condition on the statement
whose explanation states why the loss entry cannot be computed and that the
return's income does not yet account for the Form 1099-K statement.

The package is `core-calculations.v49` in published package registry `v47` and
release `demo.release.sli-worksheet-integration.2025.v47.json`. It adopts Form
1099-K family `v2`, whose closure authorizes the sum of the current statements.
Workspaces adopting `core-calculations.v48` or earlier keep the one-statement
`v1` family. A synthetic
supported loss answer set looks like this:

```python
answers = {
    "covers-only-single-item": "yes",
    "acquired-by-purchase": "yes",
    "primary-purpose-at-acquisition": "personal-use",
    "exclusive-personal-use": "yes",
    "digital-asset-involvement": "no",
    "agreed-item-price": 800.0,
    "shipping-arrangement": "platform-pass-through",
    "platform-fees": 80.0,
    "seller-paid-shipping": 0.0,
    "sales-tax-collected-by-platform": 56.0,
    "refund-amount": 0.0,
    "buyer-paid-shipping": 24.0,
    "purchase-cost": 1000.0,
    "cost-basis-known": "yes",
    "lasting-improvements-or-adjustments": "no",
}
```

The callable recording, review, and save operations live in
`packages.tax.f1099k_statement_recording` and
`packages.tax.f1099k_statement_review`: `record_f1099k_statement_durably`,
`record_f1099k_no_statements_durably`, `prepare_f1099k_statement_review`,
`save_f1099k_statement_review`, `answer_f1099k_statement_review_question`,
`correct_f1099k_statement_review_answer`,
`withdraw_f1099k_statement_review_answers`,
`retract_f1099k_statement_durably`, `close_f1099k_family_durably`, and
`review_f1099k_statement_with_saved_presentation`. The writers take the Form
1099-K family version from the workspace's adopted package. When a workspace
recorded on `v1` writes under `v49`, the same save records the family handover
(ADR 0079); the earlier completeness answer stops counting and must be
answered again. Removing a statement records its removal and retracts its Box 4
and answers in one save; the family is then closed again before the entry is
calculated. A removed statement cannot be recorded again under the same
payer, year and reference; the writer refuses before saving. A workspace
recorded on `v1` and adopted onto `v49` can answer the completeness question
again without adding a statement: `close_f1099k_family_durably` (or a
correction with `close_family=True`) records the handover and the fresh
closure in one save. Each saved explanation is matched to its statement by
the full payer, statement and tax-year keys, and a statement's review says
its Box 1a was entered on Schedule 1 only when the top entry published. Initial review saves require
answering all 15 circumstance questions; subsequent corrections and withdrawals
record against their current finding identities and advance the revision. A
saved calculation retains the Form 1099-K report (payer and Box 1a), the
chosen answers, actual assumptions ("none"), and the five computed figures
(`amount-realized`, `selling-expenses`, `net-proceeds`, `adjusted-basis`,
`expected-box1a-gross-amount`) plus the categorical comparison
(`net proceeds < adjusted basis` for a loss, `net proceeds > adjusted basis`
for a gain). If an answer changes, earlier saved calculations report
`recalculation-needed`.

Workspaces meet the completeness requirement for the Form 1099-K family only
when they adopt release `v46` or later (with vocabulary bundle `v3`); more than
one statement requires release `v47`. Workspaces on earlier releases do not contain the five computation rules, the successor
reason rule, or the pass-through additional-shipping coverage stop. When no Form 1099-K was received, recording that fact durably
via `record_f1099k_no_statements_durably` closes the statement family
closed-empty and enters 0 at the top of Schedule 1.

## 2025 tax on taxable income

On `core-calculations.v50` (published registry `v48`, release
`demo.release.sli-worksheet-integration.2025.v48.json`), Form 1040 line 16 and
the standard deduction use verified 2025 law instead of the earlier
placeholder parameters:

- the seven-bracket rate schedule (Rev. Proc. 2024-40), through the Tax Table
  below $100,000 (tax on the band midpoint, rounded) and the Tax Computation
  Worksheet at $100,000 or more;
- the Qualified Dividends and Capital Gain Tax Worksheet, published line by
  line (lines 4–25) so the explanation walk reaches each step, with the 0,
  15 and 20 percent bands;
- only the smaller of Schedule D lines 15 and 16 taxed at preferential rates,
  so short-term gain is taxed at ordinary rates;
- the 2025 standard deduction of $15,750 / $31,500 / $23,625 (Pub. L. 119-21)
  with the $1,600 married and $2,000 unmarried additional amounts for age 65
  or blindness.

Workspaces adopting `core-calculations.v49` or earlier keep their earlier
results; adopting v50 recomputes.

## 2025 senior deduction and a dependent's standard deduction

On `core-calculations.v51` (registry `v49`, release
`demo.release.sli-worksheet-integration.2025.v49.json`):

- **Enhanced deduction for seniors** (Schedule 1-A Part V, lines 33–37, to
  Form 1040 line 13b): $6,000 for each taxpayer or spouse aged 65 or older
  with a valid SSN, reduced by 6 percent of AGI above $75,000 ($150,000
  joint); $0 when married filing separately. It applies whether the return
  itemizes or not.
- **A dependent's standard deduction** (the Standard Deduction Worksheet for
  Dependents, lines 1–4c, to line 12e): the larger of $1,350 or line 1z plus
  $450, capped at the basic amount, plus the age and blindness additions.

v51 asks four new yes/no questions: whether someone can claim the taxpayer or
spouse as a dependent, whether the return claims none of the tips, overtime
or car loan interest deductions (Schedule 1-A Parts II–IV, which stay
uncomputed), and a valid SSN for each person aged 65 or older. The dependent
and Parts II–IV answers are required; a missing answer blocks with the fact
named. The Parts II–IV answer replaces v50's single Schedule 1-A answer.

## 2025 refund or amount owed

On `core-calculations.v52` (registry `v50`, release
`demo.release.sli-worksheet-integration.2025.v50.json`), every computed return
continues past tax after credits (line 22) to the line a person acts on:

- total tax (line 24), with Schedule 2 Part II taxes (line 23) declared
  absent by a question;
- federal income tax withheld from W-2 box 2 (line 25a) and Forms 1099-INT,
  1099-DIV and 1099-R box 4 (line 25b), summed across statements; line 25a
  blocks unless every W-2 has a box 2 answer ($0 allowed);
- estimated tax payments (line 26), refundable credits declared absent
  (lines 27-32), and total payments (line 33);
- the overpayment (line 34), split between a refund (line 35a) and an amount
  applied to 2026 estimated tax (line 36, asked only when there is an
  overpayment), or the amount owed (line 37), with no estimated tax penalty
  (line 38) declared by a question.

A return without foreign tax now reaches line 22 without the direct foreign
tax credit's election and eligibility questions. Form 1099-K, 1099-G and
SSA-1099 withholding are not yet summed.

## 2025 earned income credit

On `core-calculations.v53` (registry `v51`, release
`demo.release.sli-worksheet-integration.2025.v51.json`), Form 1040 line 27a is
the earned income credit for a filer with no qualifying child: EIC Worksheet A
on W-2 box 1 and AGI, read from the printed 2025 EIC Table
(`tax.us.2025.parameter.eic-table-2025`, the 0-child columns).

- Investment income over $11,950 asks only the unsupported-situations answer.
  Yes publishes line 27a as $0. No blocks. The other EIC questions stay unasked.
- AGI at or above $68,675 asks no EIC question and publishes line 27a as $0.
  Step 1 tests Form 1040 line 11b, and $68,675 is the largest completed amount.
- W-2 box 1 at or above $68,675 while AGI is below it asks the
  unsupported-situations answer. Yes publishes $0. No blocks. The other
  questions stay unasked. A clergy or church-employee Schedule SE amount can
  put worksheet earned income below box 1, and that situation is inside this
  answer.
- Otherwise the return answers whether it has a qualifying child. Married
  filing separately and head of household with no qualifying child are $0.
- After that answer, AGI at or above the 0-child completed amount ($19,104
  other, including qualifying surviving spouse; $26,214 joint) publishes $0
  with no further EIC question. Step 1 tests line 11b against that amount.
- Box 1 at or above that amount while AGI is below it asks the
  unsupported-situations answer for single, married filing jointly and
  qualifying surviving spouse returns. Yes publishes $0. No blocks.
- The remaining questions (SSN, residency, age, main home, dependency, and
  the same unsupported-situations answer for Form 2555, Form 8862, Worksheet
  B, combat pay, a Medicaid waiver exclusion, and Worksheet 1 items) are
  asked only when the status is single, married filing jointly, or
  qualifying surviving spouse and both box 1 and AGI are below that amount.
- A failing answer gives $0 with the test named. A missing required answer
  blocks with the fact named. A qualifying child or an unsupported situation
  is outside the class.
- Lines 28-31 have their own absence answer, required on every
  successor-package return, replacing v52's lines 27a-31 answer.

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

### Returning to a saved account

Stop-and-return works the same way outside the repository, across a real restart of the process. Wording is provisional.

1. Create an empty directory outside this repository to hold one synthetic account — any directory of your own choosing is fine; never a path inside this repository.
2. `python3 -m packages.derivation.runners.sli_correction_evaluation --workspace DIR --init` (optionally with `--state NAME`) seeds that directory once and serves it, the same as the temporary states above.
3. Review Autumn on Cedar and correct it, the same as any state above.
4. Stop the process (Ctrl-C, or any other way it ends). The saved correction and the account's history are now durable in that directory.
5. `python3 -m packages.derivation.runners.sli_correction_evaluation --workspace DIR` (without `--init`) opens that same directory again and serves it.
6. The opened page shows each borrowing's current answer and, where one exists, its earlier answer, read fresh from the directory — never reseeded. It also shows the latest earlier result, if one is recorded, and offers one action: calculate from the saved answers.
7. Calculating runs one fresh calculation from those saved answers and never saves a second time. The result is headed as calculated from the saved answers in this session, not as an earlier result.
8. From there, a further correction works as before: choose an answer, confirm it, and see the recalculated result.

If a calculation was started and never finished before the process stopped, the opened page still shows the saved answers, says the calculation did not finish, and shows the latest completed result if one exists; nothing is seeded or reset, and calculating is still offered. A review token issued by a stopped process is never honored by a new one: confirming, checking its outcome, or retrying with that token reports that the outcome cannot be determined in this session — never "Not saved" — and the page drops that old token once told so by the server, not merely because a request to it failed to arrive.

## Data safety

Nothing personal is committed: no real tax documents, no personal fact instances, no artifacts derived from personal data. Committed fixtures are synthetic and publishable. Personal work stays under ignored paths (`local-data/`, `temp/`, `private-archive/`, `uploads/`, `generated/user/`). See Article 18 (Quarantine) and the data safety rules in `AGENTS.md`.
