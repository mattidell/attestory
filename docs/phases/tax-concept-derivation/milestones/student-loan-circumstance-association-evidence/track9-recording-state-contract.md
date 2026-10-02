# Track 9 candidate recording-state contract

## Purpose and boundary

This experiment asks whether the existing act, finding, contribution, derivation,
and saved-output machinery can preserve an ordinary answer about student-loan
circumstances when its real-world connection is not yet known. It does not decide
student-loan eligibility or deduction treatment.

The experiment must keep three questions separate: whether an answer was
supplied, whether the identity and scope of its connection are known, and whether
the application has adopted a tax consequence. A missing answer has no account
or finding. A supplied but unresolved answer has a current, addressable account
and its supplied evidence; it is not silence and it does not identify a loan by
guess. A resolved answer names only identities established by the supplied
claim. No amount, lender, year, row order, generated identifier, or equal value
may stand in for a real-world identity.

## Candidate representation

Treat the account identity and the referent identity as different things. The
test-only producer may introduce a synthetic account entity with its own stable
account ID, then contribute an account finding whose value explicitly records
which connections are known and which remain unresolved. The account ID is only
the address of the supplied answer; it is never a placeholder student loan,
schooling situation, statement, or legal indebtedness.

Keep these claim kinds independently addressable and correctable:

1. A schooling circumstance, such as a supplied period or status account.
2. A financing claim connecting an identified borrowing to an identified
   schooling circumstance.
3. A statement-membership claim connecting an identified statement to an
   identified borrowing and declaring its scope.

Knownness is per connection: distinguish an unknown borrowing identity, a known
borrowing with an unknown statement portion or scope, and a missing schooling
fact. One generic `unknown` flag must not erase which part is known. In the A5
financing pair, a known financing claim retains both the borrowing and the
situation identities; two equal-valued situations remain distinct. Do not
duplicate a single schooling circumstance once per borrowing. An account may
become usable for a relationship consumer only when a current supplied claim
names the required real identities. Correcting or retracting one claim
does not correct, retract, or invert either of the others. A correction must
retain its predecessor lineage; a retraction ends current support without
asserting an opposite answer.

## Required observations

| Case | Required observation |
| --- | --- |
| No answer | No account, circumstance, borrowing, or relationship claim is invented. |
| Complete account | Separate circumstance and financing identities survive contribution, admission, persistence, and recovery without a tax classification. |
| Present but unresolved | The account and its evidence remain current and addressable; no referent is guessed and it is not represented as absent or complete. |
| Resolve an account | The successor preserves correction lineage; current support drops superseded findings while unrelated claims remain current. |
| Shared circumstance correction | One corrected circumstance is consumed by two financing/statement paths; each exact supporting set changes, while a third independent path stays unchanged. |
| Equal-valued situations | Two distinct circumstance and financing identities reach the collection consumer and saved evidence; equality or count alone is not proof of identity. |
| Retract an account | Only its current support changes; history remains recoverable without treating the retraction as an opposite assertion. |
| Mixed-period account, no adopted treatment | Supplied periods and relationship support remain present; lack of an adopted consequence is not represented as a missing fact, blocked row, failure code, or tax result. |

The experiment starts with test-only synthetic answer mapping and declarations.
It must use existing contribution/admission, persisted act-log reopen, package
admission, marshalling, both runners, and actual saved output. Recovered current
state—not the original answer objects—must drive the consumer. Pins must identify
the computation/version, each actual subject, and all relevant current source
findings, while excluding unrelated and superseded claims. After a run, discard
live objects and the workspace, reopen the saved output, and compare the
relationships and neutral evidence results.

## Limits

Existing SLI declarations currently include statement amount and statement
witnesses plus filer-level scope witnesses; they do not declare schooling or
borrowing-to-situation facts. Track 8's statement-to-borrowing claim requires a
borrowing identity in its fact identity, so omitting that identity is rejected
during kernel projection. This experiment may add only test-local synthetic
declarations to discover whether a separately addressed account can pass the
existing substrate. Any such mapping/declarations are prototype inputs, not
production recording capability or a published contract.

No experiment result establishes legal eligibility, a favorable/adverse
conclusion, a deduction, a default from link count, a production producer, or
acceptance of G2 or ADR 0076 Part 3. If the existing package, storage, or saved
presentation boundary cannot carry the required distinction and support set,
stop at the smallest failing case and name the exact missing producer-to-consumer
capability. Do not repair the substrate, publish a schema, or invent a tax
failure/result to make the case appear executable.
