# Retrospective — Later-Year Basis Reuse Test

The plan allowed Track 0 to close either by naming a first production
vertical or as an explicit partial result. It closed as the partial
result: neither strategy supplies a production-authorized later-year
delivery path today — raw same-run mixed-scope computation does produce
the value — and a fifth composition gap — the absence of an authorized
package/scope contract for composing an earlier determination into a
later disposition calculation — surfaced ahead of everything the plan
anticipated.

## Carry-forward lessons

- **Distinct scope fields must not be assumed equal.** `reporting_year`
  is the tax year the payer's own report covers — a filter on which
  reports may associate — not the year a disposition consumer's rule is
  scoped to (`scope.tax_year`). The domain model keeps these separate,
  and nothing in the engine compares them. A test that sets both to the
  same value tests one configuration. **A successful test configuration
  does not establish an authorized scope-composition contract.**

- **A passing test can encode an unstated assumption in its own
  construction.** The C8b same-run `collect` experiment passed as raw
  fixed-prefix aggregation of live sources. Current package validation
  **mechanically ACCEPTS** the candidate rule, because
  `COLLECT_TARGET_NOT_FAMILY` is **inactive for `artifact-package.v26`**.
  That acceptance does **not** supply the missing **source-family
  declaration**, **closure mapping**, or **semantic authority**;
  therefore **no source-family-authorized traversal has been
  established**.

- **Structural differences are not automatically material product
  differences.** A pin-graph shape or a blocked-row's directness is only
  a product discriminator once some downstream consumer — an explanation
  walk, a refusal surface, a permitted action — is actually exercised
  over it. Absent that, the honest grade is "structural, not material,"
  and a representation choice resting on it stays deferred.

- **An evidence-first milestone can surface a real defect in committed
  product code as a byproduct.** The `COLLECT_TARGET_NOT_FAMILY`
  allowlist gap was found this way, not by auditing
  `packages/derivation/` directly. Treat such byproduct findings as
  first-class output even when the publication boundary forbids fixing
  them.

## Follow-ups

Owner-held decision areas are surfaced and not taken. They remain separate,
and each applies only where a selected case actually reaches it.

- **The contract permitting cross-scope consumption (gap 5).**
  *Trigger:* a consumer that must use a determination from another tax
  context or scope, which meets this gap before the four inherited
  composition gaps. A later-year calculation that stays within one tax
  context does not meet it. Resolving it requires an
  owner-authorized package/scope contract — no adopted 2029 package and
  no cross-scope composition contract exist in committed content today.
  The milestone did not establish whether resolving gap 5 (or the other
  composition gaps) requires schema, kernel, package, content, or other
  changes.
- **The later calculation's consumption policy, and the
  historical-retention question** — related but distinct. Consumption:
  what determination a later calculation may consume — the historical
  execution, a newly derived determination, or a policy permitting
  either. Retention/reportability: whether historical executions should
  independently be retained and reportable. These are not rival
  architectures the owner must pick between: a system may re-derive for
  consumption and retain history for reporting. Re-executing the
  existing 2025 seam required no new schema or kernel machinery — that
  is executed and true — but end-to-end later-year use remains unbuilt,
  and the no-new-machinery finding is about that 2025 seam only.
  Retrieval of a persisted derived finding, as exercised, is blocked
  twice independently (a successor `act-derived-publication` schema
  plus an independent projection change). Neither policy is selected.
- **Authorship of the broker-versus-derived comparison claim** — who
  authors the claim that a broker-reported basis and a product-derived
  adjustment describe the same adjustment. No comparison mechanism
  exists (C11). Track 0's disposable consumer refuses to treat the
  documentary figure as an input; that is a defensible default, not a
  product decision.
- **Whether to repair the collect-target universe guard**
  (`COLLECT_TARGET_NOT_FAMILY`) in
  `packages/derivation/package_validation.py`: its allowlist documents
  itself as binding "artifact-package.v3 onward" but ends at
  `artifact-package.v17`, while production is `artifact-package.v26` —
  the check has never bound a `rule-artifact.v7` collect. Recorded and
  deliberately not fixed; this milestone's boundary forbade touching
  `packages/`. *Trigger:* owner decision to repair the guard, which
  would require re-running any C8b-shaped conclusion that rested on
  package validation staying silent.
- **The A-versus-B representation choice**, deferred again on a
  cleaner ground than before: structural differences (pin topology,
  blocked-row naming) are observed and executed, but no material
  product discriminator was established, because no test exercised
  `explanation.py`'s `walk_npe` or any other downstream consumer of
  either shape. *Trigger:* a consumer that actually reads the
  explanation, a refusal surface, or a permitted action through either
  shape.
- **The four gaps inherited from the prior milestone** (cost-origin
  vocabulary, acquisition-keyed origin producer, per-acquisition
  publication path, declared traversal from acquisition to consequence)
  remain open and unchanged in kind; this milestone only sharpened gap
  4's classification into a selection half and an authorization half.
