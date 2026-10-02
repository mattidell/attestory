# Track 12 — account reference boundary report

## Question and evidence limits

This experiment tests whether Track 9's supplied account references can
construct the independently asserted FINANCE and MEMBERSHIP relationships that
Track 10/11 consumers use. All values, labels, identities, and claims below
are synthetic `demo.*` fixtures. This report records current test-only behavior;
it does not choose tax treatment or a production meaning for the untyped
reference strings.

The package assembly uses a scoped test seam to omit FINANCE and MEMBERSHIP
contribution calls before either claim is admitted. It keeps the Track 10
schooling contribution path. The test then admits the account through the
ordinary contribution protocol and persists it with the package adoption.
The test does not remove support from a projected state or intercept kernel,
runner, or coordinator execution. A separate control uses the ordinary Track
10 contribution helper for all relationship claims.

## Recorded identities and declared consumers

Track 9's prototype account type has its own entity-keyed fact identity and an
object value containing borrowing knownness, schooling presence, statement
scope, supplied claim text, and nullable string references. The test answer
mapper copies those fields; no production recorder exists. The fixture uses a
borrowing entity ID and exact schooling and statement fact IDs as reference
values. Those are test conventions, not namespace rules for the product.

The Track 10 candidate declares SCHOOL with keys `situation`, `period`,
`institution`, and `programme`; FINANCE with keys `borrowing`, `situation`,
`period`, `institution`, and `programme`; and MEMBERSHIP with keys `lender`,
`statement`, `tax-year`, and `borrowing`. Its FINANCE observation rule is
subject to FINANCE, joins SCHOOL through `subject_contains_joined`, and
requires schooling support. The statement membership observation is subject
to MEMBERSHIP and consumes FINANCE observations. Track 11's working
EXPECTED/AVAILABLE declaration measures each current raw FINANCE claim
against its available financing result.

The account rule reads `borrowing_reference` as a scalar under the account
subject. A second test-local diagnostic rule reads all three nonempty
reference fields and emits the explicit neutral literal
`demo.financing.observed` under the actual FINANCE symbol. This is a
key-transport probe: it does not convert the references into keys or record a
source claim. The package declaration gives the literal an explicit
`demo.sli.track10.financing@v1` category. The live derived publication records
its symbol, account-keyed fact ID, literal, and pins, but carries no separate
fact-type metadata field. No category or identity authority is inferred from
the rendered symbol.

## Executed unresolved account

The current unresolved account finding is
`demo.finding.sli.track12.account.references-present` under the test account
fact ID, backed by `demo.evidence.sli.track12.account.references-present`.
Its value records `schooling_fact: missing`, `borrowing_identity: unknown`,
`statement_scope: unknown`, and three null references. No current SCHOOL source
finding is present in this case. The saved evidence metadata separately says
`application_treatment: unadopted`; that is capability context, not a user
finding or a blocked result.

After ActLog reopen, both runners agree with the live coordinator. The
test-local scalar rule reads the null borrowing reference and its saved
publication value is the string `"None"`; its only input pin is the account
finding. The unresolved saved record reopens with that current account and
unadopted metadata. The selected account publication's pin closure resolves.
The unchanged carrier's whole-run `complete` flag is false because unrelated
Track 8 horizon input pins remain unresolved; this does not mean the selected
account pin is unresolved.

## Executed references-present route

Before account admission, the fixture has a current borrowing entity, the
referenced SCHOOL finding, and the referenced statement fact. It has no current
FINANCE or MEMBERSHIP source findings. The account answer retains its own
account fact ID and evidence.

Both runners agree after ActLog reopen, and the live coordinator's publications
and dispositions match them. The scalar account reader publishes
`demo.track8.borrowing.a` under an account-keyed result and pins only the
account finding. The diagnostic route is admitted and publishes
`demo.financing.observed` under:

```text
demo.sli.track10.financing|demo.sli.track12.account|account=demo.sli.track12.account.references-present,tax-year=2025
```

Its direct input is the account finding. The actual Track 10 FINANCE
observation consumer receives that FINANCE-named symbol but has only the
account subject keys. It records a blocked row under the corresponding
`demo.sli.track10.financing-observation|<same account fact ID>` symbol, with
`DEPENDENCY_INVALID`, missing `demo.sli.track10.schooling`, and an input pin to
the diagnostic finding. The SCHOOL target itself is current and independently
recorded; it is not joinable through the account-keyed row. No MEMBERSHIP
observation is published because the fixture has no membership subject claim.
The missing target, unknown connection, and unadopted application treatment
therefore remain separate.

The unchanged carrier reopens after the temporary workspace and live
coordinator objects are discarded. Selected account and blocked-consumer input
pins close to the current account finding. The referenced SCHOOL finding is
saved under `context_only` because no selected input pin reads it. The
statement finding also appears in the run's evaluated support through other
Track 8 outputs; the account reader and diagnostic pins do not name it. The
carrier's global `complete` flag is false because its unchanged whole-run
capture includes unrelated unresolved Track 8 horizon pins. The report makes
no claim that the carrier resolves those unrelated targets.

## Correction and retraction

An ordinarily admitted successor changes the account's borrowing reference
from `demo.track8.borrowing.a` to `demo.track8.borrowing.b`, preserving its
schooling and statement references. A fresh ActLog recovery and live run show
the scalar result changing to B; its input pin changes from the predecessor
account finding to `demo.finding.sli.track12.account.corrected`. The diagnostic
FINANCE-named output has the same account fact keys and its pin changes to the
corrected account finding. The saved carrier includes the actual correction
lineage, current successor support, and excludes the displaced predecessor
from evaluated support.

A normal finding retraction then removes the corrected account's current
support. Fresh runners and coordinator emit no account scalar or diagnostic
publication. The reopened carrier's lineage marks the corrected account
displaced and excludes it from evaluated support. The independently recorded
schooling and statement source facts remain current. No relationship claim is
corrected, retracted, or inverted by either account lifecycle act.

## Explicit relationship control and lifecycle independence

The separate working control records Track 10's schooling, five FINANCE, and
three MEMBERSHIP claims through ordinary contribution admission. Track 11's
admitted EXPECTED/AVAILABLE declaration runs over those independent claims.
The live coordinator agrees with both runners. The saved support contains
exactly those five current raw FINANCE finding IDs, all three current
MEMBERSHIP IDs, and the two source SCHOOL findings. Each EXPECTED and AVAILABLE
witness set reaches all five raw FINANCE claims. The three membership
observations publish the neutral value `true`.

Correcting and retracting the account in this combined control leaves the full
finding objects, values, and pins from FINANCE, MEMBERSHIP, EXPECTED, and
AVAILABLE producers unchanged. The raw FINANCE, MEMBERSHIP, and SCHOOL
finding-ID sets also remain exact and unchanged. The account scalar publication
changes to borrowing B on correction, pins the successor account, and
disappears after retraction. The Track 11 consumers do not read the account;
its references are not evaluated dependencies for those consumers.

Saved closure checks traverse each selected publication and selected
disposition input pin at every depth. For every membership observation, the
test compares its complete transitive leaf set with the exact raw membership
finding, every current FINANCE finding for that borrowing, and the corresponding
SCHOOL facts matched by structured identity keys. It excludes the account and
other borrowing's claims. The same exact set is asserted before and after
account correction and retraction. The carrier preserves its known unresolved
unrelated Track 8 horizon pins, so its global `complete` flag remains false
even though selected relationship and lifecycle paths close.

## Finding and disposition

Current declarations can read an account reference as a scalar and can emit a
test-local FINANCE-named row. That row keeps the account identity keys, so the
existing FINANCE observation rule cannot connect it to the independently
recorded SCHOOL target. This is an identity/source-assertion gap, not a missing
schooling fact and not evidence for a favorable or adverse default.

The diagnostic rule is evidence about key transport in the existing grammar.
It is not an adopted source assertion, mapper, reference-resolution contract,
or production route. Constructing a relationship with the required borrowing,
situation, period, institution, and programme keys requires an explicit
mapping or source-assertion decision. That decision is for Foreman/owner
disposition before implementation.

## Verification

- `pytest tests/test_sli_track12_account_reference_boundary.py -q`: 4 passed
  in 47.51 seconds.
- `mypy tests/test_sli_track12_account_reference_boundary.py`: success, no
  issues.
- `pytest tests/test_kernel_fixtures.py -q`: 2 passed, 5 subtests passed.
- `python3 tools/governance_lint.py`: conformant.
- `git diff --check`: passed. The new report and test are synthetic-only.
- Foreman review repairs strengthened the exact diagnostic subject/pin receipt,
  current target-fact presence, exact transitive source closures per membership
  observation, unresolved selected-closure evidence, and account lifecycle
  isolation across independent claims. The focused test was rerun after those
  repairs before review acceptance.
- After Foreman review acceptance, the single full-suite command was
  `set -o pipefail; pytest 2>&1 | tee temp/track12/track12-full-suite.log`,
  run with local socket permission from the start. Exec session: `93162`.
  Result: **2383 passed, 20 skipped in 309.77s (0:05:09)**; exit code 0.
  Executable SHA256 at suite start and completion:
  `54c6fe6e77396a89978d7e3822394535b10ad8871a89a3d81237821e833e6669`.
  Durable log: `temp/track12/track12-full-suite.log`.
- No executable edits were made after the passing full suite; no commit or push
  was made.
