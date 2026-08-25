# Workspace Calculation Claim Support

## Supported product claim

The selected product claim is:

> The user has authorized the application, within the authorization's declared
> scope, to treat the relevant facts current in this workspace revision as the
> exhaustive input universe for this ordinary return calculation.

This is a claim about permission and reliance, not objective completeness. It
does not say that every tax fact exists in the workspace, that every source is
accurate, that every applicable tax rule is implemented, that future
information cannot arrive, or that the return is ready to file.

The authorization is standing. Within scope it applies after ordinary additions,
removals, reclassifications, and corrections. Each run must still identify the
exact current revision it used.

## Two independent things an exhaustive-total claim needs

Presenting a result as an exhaustive tax total — "your 2025 total taxable
interest is $X" — requires two independent supports, and this claim-support
account covers only the first:

**A. Workspace-record sufficiency** — the current workspace is treated as the
complete input record for this calculation. The standing authorization (or,
when it is inactive, a narrower family confirmation) is exactly this support,
and the account below is its claim-support template.

**B. Tax-model sufficiency** — the adopted, versioned fact vocabulary,
classification rules, composition, exclusions, and adjustments cover the
exact tax concept being claimed. This is a claim about the application's own
declared artifacts and their coverage account, never about the user's
authorization. No amount of workspace authorization, and no number of
confirmed source families, supplies it. See `completeness-support-model.md`
for what the currently adopted line-2b composition does and does not
establish about this.

## Claim-support account (workspace-record sufficiency only)

| Field | Required account |
| --- | --- |
| Proposition | The application may treat the relevant current workspace facts as the complete input record for ordinary return calculation within a bounded scope. This proposition is about workspace-record sufficiency only — it says nothing about whether the adopted tax vocabulary covers the concept being calculated. |
| Speaker or author | The user supplies the authorization through a future accepted capture path. Current `act.v1.actor` is an opaque recorded identifier, not proof of a natural person's identity. |
| Basis and authority | The standing authorization itself, current and applicable to the run's scope. It is not inferred from data entry, document presence, a Boolean field, or successful arithmetic. |
| Context and scope | At least an identified workspace or return context, subject/taxpayer, tax year, and an adopted calculation-vocabulary boundary if those dimensions are selected for the successor contract. |
| Dependencies | Current authorization; exact workspace revision; current projected findings; adopted package, rules, parameters, mappings or successor artifacts, citations, and operation semantics actually read. |
| Invalidators | Suspension, withdrawal, supersession, or departure from the declared scope. Ordinary member and value changes are not invalidators. |
| Unsupported nearby inference | Objective tax completeness; content accuracy; **tax-model sufficiency — that the adopted vocabulary and rules cover every category the claimed tax concept requires**; filing readiness; legal effect; no future information; or that a missing authorization proves incompleteness. Tax-model sufficiency is never established by this authorization, regardless of its scope. |
| Permitted user consequence | The product may perform and present an ordinary calculation from the current workspace, explain its inputs and authority, and recalculate after ordinary edits. Without a current authorization or narrower confirmation, it may still present a directly sourced value or a sum explicitly limited to recorded items, and unrelated facts and calculations remain available. |
| Required refusal or qualification | Without a current applicable authorization, the product must not characterize an exhaustive-total claim — including a zero — as calculated from a complete input record, regardless of the numeric value. Even with a current authorization, the product must not present an exhaustive-total claim as fully supported unless the adopted rules' own coverage account separately supports the tax concept being claimed. A source-level claim ("this source reports $X") or a recorded-items sum, honestly labeled as such, requires neither support and is not refused. |

## Why documents are not the proposition

The user's ordinary mental model may be “use everything I have entered,” and an
interface may explain the authorization with familiar document examples. The
technical proposition must be about relevant workspace information, not “all
documents.” IRS Publication 550 requires taxable interest even when no Form
1099-INT was received and describes sources and adjustments beyond a document's
box-1 amount
([IRS Publication 550 (2025)](https://www.irs.gov/publications/p550)).

The accepted 1099-INT box-1 family is narrower still: its `closure_claim` covers
only furnished box-1 statement items and expressly excludes other boxes,
non-form interest, and line 2b
(`packages/content/tax/2025/family.f1099int-b1.json:2-9`). Form 1040 line 2b's
adopted composition consumes ten positive and adjustment families
(`packages/content/tax/2025/rule.form1040-line2b.v4.json:91-102,111-206`).
Document completeness and tax-total support therefore cannot be equated.

Reported amounts do not become a tax-domain result by being summed. Turning
"this statement reports $X" into "$X counts toward 2025 US-federal taxable
interest" is a classification act performed by adopted rules: which
jurisdiction and tax year apply, which amounts are positive contributors,
which are excluded, and which are subtracted as adjustments. That
classification is tax-model sufficiency's work, not workspace-record
sufficiency's — a user's authorization to use the workspace never performs
it, and neither does an unqualified arithmetic sum.

## The claimed concept is not the form field that presents it

"2025 US-federal taxable interest for this taxpayer" is the tax-domain
concept a claim-support account must actually be about — not "Form 1040 line
2b," and not "Schedule B." The current repository represents this concept as
the output of an adopted rule, published under the symbol
`tax.us.2025.interest.taxable-total`
(`packages/content/tax/2025/rule.form1040-line2b.v4.json`); Form 1040 line 2b
presents that symbol's value by binding to it
(`packages/content/tax/2025/form1040.line-2b.form-field.v5.json`), and it
does not own the concept's identity. Whether a bare symbol, rule, and
quantity-vocabulary binding is a sufficient long-term declaration of a
derived tax concept, or whether it needs a stronger, fact-type-like
citizen of its own, is successor investigation and is not decided here.

## Authorization, assumption, affirmation, and withdrawal

These terms answer different questions:

- **Authorization** permits the application to use the current workspace as its
  calculation universe. This is selected.
- **Affirmation** asserts a proposition as true. Existing source closure is
  framed as an affirmation, but the selected calculation authorization need not
  assert that no relevant fact exists outside the workspace.
- **Assumption** directs a hypothetical calculation without asserting truth.
  This remains deferred because no concrete product need requires intentional
  departure from current workspace state.
- **Withdrawal** ends permission for future reliance. It does not assert that
  the workspace is incomplete and does not rewrite the authority or results of
  earlier runs.

An initial negative declaration is unnecessary. No authorization means only
that calculation authority is not established. Suspension or withdrawal returns
to that state.

## Current evidence and its limits

### Current closure is narrower than the selected authorization

The committed 1099-INT mapping reads a Boolean closure fact keyed to one family
horizon and admits only that family's subtotal under a current-literal-true
condition (`packages/content/tax/2025/closure-mapping.f1099int-b1.json:2-10`).
`marshal_closure_authority` copies only the current finding id, fact type,
horizon, and value into the runner's closure record; it does not carry basis,
evidence, capture, contribution, or author information
(`packages/derivation/marshal.py:158-205`;
`packages/derivation/source_authority.py:65-97`).
`resolve_closure_admissions` then uses that reduced record to admit or block the
family (`packages/derivation/source_authority.py:100-166`).

This machinery establishes that per-family closure can supply operational
admission. It does not establish that a collection of closure booleans is the
right product authorization, or that the selected standing authorization can be
inserted into the same shape without changing accepted contracts.

### W-2 entry currently invents support

On first W-2 wage entry, `entry_loop.py` creates the wage membership transition
and a second assertion carrying literal-true closure with documentary basis and
evidence (`packages/derivation/entry_loop.py:75-78,770-807`). Nothing in that
flow asks the user to authorize exhaustive workspace calculation or attest W-2
family completion. Kernel validation accepts documentary basis for a
determinable fact when evidence exists and does not enforce closure-specific
attestation (`packages/kernel/findings.py:524-558,582-590`).

The behavior cannot support the product claim. Data entry is the basis for the
wage fact; it is not evidence that the user granted standing calculation
authority. The future capture path must record authorization as its own act or
fact under a successor contract, not manufacture it from an unrelated answer.

### Current author information is limited

An `act.v1` assertion envelope carries `actor`, while its finding payload carries
`schema`, `id`, `fact_id`, `value`, `basis`, `evidence_ids`, optional `capture`,
`pins`, and `contribution_id`. Closure admission reads neither the envelope
actor nor most of those payload fields
(`packages/schemas/kernel/act.v1.schema.json:7-20`;
`packages/schemas/kernel/finding.v2.schema.json:7-86`;
`packages/derivation/source_authority.py:65-105`). The `actor` string records
attribution but the kernel does not verify a session, role, or natural-person
identity; ADR-0041 records that limitation explicitly
(`docs/adr/0041-correction-authority-policy.md:54-70`).

This is enough to say which recorded act supplied current authority. It is not
enough to claim who personally understood or approved it. Whether later product
needs require stronger identity or authorship is separate from the authorization
scope decision.

### Run provenance is necessary but reader visibility is incomplete

For each closure read, `runner.pins_for` records the exact mapping, declaration,
and closure finding; it also pins rules, sources, refs, parameters, operation
semantics, and citations actually used (`packages/derivation/runner.py:297-395`).
The production start and completion records identify the run, workspace revision,
adoption and governance pins, and per-rule dispositions. Published dispositions
carry finding/act/symbol ids and blocked dispositions carry codes and missing
dependencies. The supplied adopted-package set gates the adoption pin but is not
stored as a second package list (`packages/derivation/production_executor.py:23-69`;
`packages/derivation/records.py:188-248`;
`packages/schemas/derivation/derivation-record.v7.schema.json:3-178,286-341`).

Numeric presentation omits closure leaves from reader citation sites even when
the embedded derived finding retains them
(`packages/derivation/presentation_projection.py:122-124,177-188,248-264`).
The selected direction therefore requires an explanation surface that can name
the standing authorization and exact workspace revision. Displaying source
citations alone does not explain why the application treated those sources as
exhaustive.

## Historical results and later changes

A run result is a fixed account of one execution. A later edit or authorization
withdrawal does not mutate it. As an observed implementation fact, the
production path currently returns calculated `RunResult.publications` and a
run record separately from current workspace findings
(`packages/derivation/production_executor.py:23-69`;
`packages/derivation/live.py:213-247`;
`packages/derivation/runner.py:1289-1340,1372-1393`). Ordinary derived-result
publication remains governed by ADR-0007 Decision 1 and ADR-0010 Decisions 1-2
exactly as ratified; whether current production's behavior matches those
decisions is a separate implementation question, not something this
completeness decision resolves or needs to resolve.

A later run recalculates from the new current revision and records its own
dependencies. It may be related to an earlier run for explanation, but the
earlier process record is not a derivation input. ADR-0010's derivation edges
remain grounded in semantic pins, and ADR-0026 Decision 4's `composition` role
is provenance-only and creates no derivation edge. Neither contract authorizes
using a process record as a tax input.

## Deferred claim forms

The following propositions are not required by the selected direction:

- “I affirm this workspace is exhaustive for this one execution only.” Reopen
  only if later reuse must be expressly forbidden.
- “Calculate as though a proposition were true.” Reopen only for intentional
  hypothetical departure from current workspace state.
- “This result is provisional.” Reopen only if a concrete action needs two
  result standings with different permitted uses.
- “This saved scenario has its own premise set.” Reopen only for durable,
  editable, comparable alternative workspaces.
- “This workspace is known incomplete.” Reopen only if a concrete need
  requires an affirmative negative-completeness claim, distinct from mere
  absence of authorization or confirmation.

These remain semantic distinctions, not an architecture awaiting
implementation.

One claim form is **not** deferred: “this source family's current membership
is complete,” used only as the narrow fallback confirmation when the standing
workspace authorization is inactive. Its invalidation follows membership, not
content — adding, removing, or reclassifying a member invalidates it;
correcting an already-represented member's value does not. Its technical
representation remains successor-contract work; its semantics are decided.

This claim form proves only what it declares. Confirming the Form 1099-INT
box-1 family establishes that every applicable box-1 statement item within
that family's declared scope is represented — nothing about total taxable
interest, nothing about whether every legally relevant interest category
exists in the product's vocabulary, and nothing about line 2b by itself.
Confirming every family the adopted composition currently declares proves
only that the declared composition's own input set is closed, unless the
adopted contract separately establishes that the composition is coextensive
with the full tax concept it presents.

## Open scope account

The standing authorization must bind enough context that later reuse is honest.
The unresolved question is which context changes alter the authorized universe:
workspace, taxpayer or return subject, tax year, adopted package, and calculation
vocabulary are the leading candidates.

Ordinary fact membership and value changes are expressly reusable. A materially
expanded future package may not be. Until the successor contract defines that
boundary, the product must not claim an old authorization covers newly introduced
categories merely because the same workspace still exists.
