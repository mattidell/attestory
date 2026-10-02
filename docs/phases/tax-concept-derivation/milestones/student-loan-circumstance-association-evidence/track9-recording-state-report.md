# Track 9 recording-state experiment report

## Contract and evidence boundary

The candidate contract is in `track9-recording-state-contract.md`. The
experiment asks whether an addressable ordinary account can remain distinct
from an unresolved real-world referent and whether the existing recording and
derivation path can consume one supplied account field. It does not select tax
treatment.

The prototype account identity is a synthetic account entity key. Its value
separately records borrowing knownness, schooling-fact presence, statement
scope, supplied claim text, and explicit nullable references. A null referent
does not become an entity or an inferred borrowing. The output in the consumer
experiment is one status field; it does not claim a resolved financing or
statement-membership join.

## Existing machinery observed

- Kernel bundle adoption accepts a test-local `fact-type.v2` declaration with
  an account entity identity and an object-valued answer. Entity introduction,
  evidence submission, contribution, and a `finding.v2` assertion pass the
  existing projection/contribution boundaries.
- `ActLog.append` and `ActLog.read` persist and reopen the synthetic account
  acts. A fresh schema registry and fresh projection recover the current
  finding, its exact value, evidence identity, and account fact identity.
- A disposable package copied from the Track 6b reader can be resealed with a
  test-only account bundle, input binding, and a `rule-artifact.v12`
  per-account rule that reads `borrowing_identity`. Package validation accepts
  it. The production resolver, marshaller, forward runner, reference runner,
  and live writer execute using the reopened act log.

## Executed cases

| Case | Observation |
| --- | --- |
| Present answer, borrowing unknown, schooling fact missing, statement scope unknown | The answer stays a current finding under its own account ID, with explicit null references and its supplied evidence. Its fact ID has no borrowing key. |
| Neutral account consumer | Both runners publish the exact account-scoped symbol with value `unknown`. The publication pins name `demo.finding.sli.account-a` as its sole input and `demo.rule.sli.track9.account-state@v1` as computation. |
| Live save and reopen | The result file preserves the published disposition, exact suffixed symbol, derived finding ID, and source finding pin. It does not copy the publication value or computation pin into the result disposition. The standard presentation has no section for this neutral account publication. |
| Attempted field bindings | A form field bound to the exact suffixed per-account symbol is rejected by package validation with `FORM_FIELD_BINDING_MISSING`. Binding the field to the unsuffixed base symbol admits, but live presentation projection fails with `missing or ambiguous disposition join ... 0 row(s)`. These are two attempted binding routes, not proof that every possible saved carrier is unavailable. |

The test-only ordinary-answer mapper, declarations, and package wrapper are
experiments, not production recording or an adopted package. The neutral rule
copies only the borrowing-knownness scalar. The output pin identifies the
current account finding; this consumer does not read schooling presence,
statement scope, or referent values.

## Precise save boundary

The live result writer in `packages/derivation/live.py` writes run status,
authorization, and `dispositions`. That result preserves the source input pin,
but omits the derived publication value and computation pin. The
presentation writer delegates to `build_presentation_model`, which projects
declared form-field sections and its supported calculation, attachment, and
provenance views. This neutral account publication is not included in those
declared views. The source account value remains in the separately persisted
act log during the run; the standalone saved result does not duplicate it.
The two attempted form-field bindings fail at their respective exact
boundaries described above. No reader or substrate code was changed. Other
saved carriers and richer account consumers were not tested, so this does not
establish a general saving limitation.

The saved presentation also retains the helper package's original Track 6b
statement views. Those views do not consume this account; any amount or default
text they display is not a treatment or consequence for the unresolved account.

## Cases not executed

- No relationship answer versus a present unknown was not compared through the
  account consumer in one test; the ordinary empty-workspace route remains the
  existing SLI package behavior only.
- A resolved account naming real supplied borrowing/schooling/statement
  references, correction lineage, shared-situation correction, equal-valued
  distinct situations, and account retraction were not exercised.
- A mixed-period account and an unadopted tax consequence were not exercised.
- The neutral consumer publishes one status value and its source input pin.
  Its saved disposition retains the exact symbol and source finding identity,
  but omits that value. Other account fields, referent joins, saved-value
  recovery, and a consumer that preserves the full support set remain
  untested.

No result here establishes a legal conclusion, favorable/adverse treatment,
deduction, default from link count, production producer, G2 acceptance, or
acceptance of ADR 0076 Part 3. The next bounded design question is how a neutral
per-account consumer should save absent, complete, and present-but-unresolved
accounts with their full current supplied fields and support through correction.
An unadopted tax rule is an application capability, not a user fact, and stays
independent. This experiment does not select that carrier or make a claim about
other package and presentation shapes.

## Verification record

- `pytest tests/test_sli_track9_recording_state.py`: 3 passed in 13.12s.
- `mypy tests/test_sli_track9_recording_state.py`: success, no issues.
- `python3 tools/governance_lint.py`: conformant.
- `git diff --check`: success.
- One earlier escalated `pytest` run completed with 2366 passed, 20 skipped,
  and 1 failure in 136.24s. It failed at
  `tests/test_build_orientation_block.py::RepositoryAnchorTests::test_every_committed_deep_read_anchor_resolves`: the milestone plan cited
  the nonexistent heading anchor `#Owner clarification — mixed-period tax
  treatment deferred` in the Track 7 decision brief. The bad route was
  introduced with Track 9 routing and then corrected in the milestone plan.
  The first run was not
  tee'd, so its full output has no durable log; its terminal session was
  `57089`.
- One final captured full-suite run used `pytest 2>&1 | tee
  temp/track9/pytest-full.log` (with `pipefail`), session `33715`, and exited
  0: 2369 passed, 20 skipped in 134.26s. The ignored log is retained at
  `temp/track9/pytest-full.log`.
