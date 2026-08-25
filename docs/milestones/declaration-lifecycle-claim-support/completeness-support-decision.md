# Workspace Calculation Authorization Decision

## Decision

The product uses one standing authorization for ordinary return calculation.
The user authorizes the application to treat the relevant information currently
represented in the workspace as the exhaustive input universe for calculation
within a bounded scope. While that authorization applies, adding, removing,
reclassifying, or correcting workspace facts causes recalculation; it does not
require another source-family confirmation.

The authorization is not a claim that the application objectively knows every
tax fact, that future information cannot arrive, or that the resulting return is
ready to file. It is permission to calculate from the current workspace as the
operative universe. The product must preserve the authorization and the exact
workspace and adopted artifacts used by each run so that the calculation's basis
is explainable.

**When the authorization is first sought.** The product surfaces this decision
when the user first requests a return-level generation or derivation that
requires an exhaustive total — not on ordinary source entry or background
calculation. Entering a 1099-INT amount, correcting a value, or any other
routine workspace edit does not itself prompt for authorization.

**When the authorization is declined or later suspended.** There is no
separate "workspace is a work in progress" fact or product state; absence of
the authorization does not assert that the workspace is incomplete. Instead:

- the application requests a narrower, explicit confirmation wherever a
  particular exhaustive claim actually requires one (see "Narrow source-family
  confirmations" below);
- only the specific result that depends on the missing confirmation is
  blocked — unrelated facts and calculations remain available;
- the application may still show a directly sourced value (what one document
  reports) or a sum explicitly limited to recorded items, without presenting
  either as an exhaustive return total.

Calculated values are ordinary run outputs: not provisional facts, not
qualified derived-finding standing, not saved scenarios, and not a second
class of result merely because the runner calls one a publication. This
decision settles what a calculated result *means*, not how or whether it is
persisted. Persistence — whether a result is transient, appended to the
workspace act log, projected as a current derived finding, or held some other
way — is a separate question this decision does not resolve.

As an observed fact about the current implementation, not a product decision:
current production execution returns calculated `RunResult.publications` and a
run record without appending those calculated values as current workspace
findings (`packages/derivation/production_executor.py:11-20,23-69`;
`packages/derivation/live.py:213-247`;
`packages/derivation/runner.py:104-115,1289-1340,1372-1393`). Ordinary
derived-result publication remains governed by the existing governance and
accepted contracts — ADR-0007 Decision 1 and ADR-0010 Decisions 1-2 — exactly
as ratified. Whether the current implementation's non-append behavior matches
those contracts is a separate implementation question from this completeness
decision, and this document neither selects that behavior for preservation nor
proposes a successor or narrowing of ADR-0007/0010 to accommodate it.

Filing is separate. The calculation authorization is not the taxpayer's filing
declaration, creates no tax liability, and does not authorize filing.

## Two independent support requirements

A calculation that claims a tax total — for example, "your 2025 total taxable
interest is $X" — requires two independent things to be true. Neither
substitutes for the other, and the standing authorization supplies only the
first.

**A. Workspace-record sufficiency.** The current workspace is treated as the
complete input record for this calculation. This is what the standing
authorization (or, when it is inactive, a narrower family confirmation)
supplies: permission to calculate as though the current workspace contains
every fact the user has to give it for this calculation context. It says
nothing about whether the right facts were ever asked for.

**B. Tax-model sufficiency.** The application's adopted, versioned fact
vocabulary, classification rules, composition, exclusions, and adjustments
support the exact tax concept being claimed — here, "total taxable interest"
as a 2025 US-federal concept, not merely the sum of whatever fact types the
product happens to have declared. This is established, if at all, by the
application's own declared artifacts and their coverage account. **The
user's workspace authorization cannot supply it.** Authorizing "use what's in
my workspace" says nothing about whether the workspace's vocabulary was ever
capable of holding every category of fact the tax concept requires.

The standing authorization, and its narrower fallback, therefore supply only
workspace-record sufficiency. Presenting an exhaustive-total claim as fully
supported requires tax-model sufficiency as well, and that must come from the
adopted rules' own coverage — not from the user's permission to use the
workspace, however broad that permission is.

## Tax and product boundary

The federal return asks for taxable totals, not a separate affirmation for each
application-defined source family. The 2025 Form 1040 reports taxable interest on
line 2b and carries one return-level declaration covering the return and its
accompanying schedules and statements. That declaration is made under penalties
of perjury and is qualified by the taxpayer's knowledge and belief
([2025 Form 1040](https://www.irs.gov/pub/irs-pdf/f1040.pdf)).

Document inventory is not the tax universe. IRS Publication 550 says that all
taxable interest must be reported even when no Form 1099-INT was received, and it
describes adjustments and other interest sources beyond Form 1099-INT box 1
([IRS Publication 550 (2025), “How To Report Interest Income”](https://www.irs.gov/publications/p550)).
The Form 1040 instructions likewise ask for total taxable interest on line 2b
([2025 Instructions for Form 1040, line 2b](https://www.irs.gov/instructions/i1040gi)).

These federal materials do not contain or require the application's internal
source-family closure facts. Lack of such a fact is therefore an application
support condition, not a tax-law prohibition on generating a draft calculation.
Presenting an ordinary return calculation as an exhaustive total honestly
requires both support requirements above: the standing authorization supplies
workspace-record sufficiency, but it says nothing about whether the
application's adopted vocabulary was ever built to hold every category of
fact "total taxable interest" requires. Tax-model sufficiency must come from
the adopted rules' own declared coverage.

Closure historically served two computational needs: permitting zero when a
collectible family had no members, and supporting the exhaustiveness of broader
nonzero totals such as Form 1040 line 2b. The successor contract must preserve
both needs; closure was not only a zero-from-absence mechanism
(`packages/derivation/evaluator.py:118-141,206-211`;
`packages/content/tax/2025/rule.form1040-line2b.v4.json:165-206`).

**What actually requires completeness support is the proposition being
presented, not the numeric value.** Zero and nonzero are not the dividing
line:

- "This source reports $X" is a claim about one document or record and
  requires no source-family closure and no tax-model coverage claim.
- "The recorded items sum to $X," honestly presented as a sum over recorded
  items and nothing broader, likewise requires neither. Turning reported
  amounts into a tax-domain result — classifying which amounts count, under
  which jurisdiction and tax year, net of which exclusions and adjustments —
  is the adopted rules' responsibility, not something a mere sum
  accomplishes.
- "Your total taxable interest is $X" — including when $X is zero — is an
  exhaustive-total claim and requires **both** support requirements above: a
  basis for treating the workspace as the complete input record (the standing
  authorization when active, or the narrower confirmation when it is
  inactive), **and** a basis for treating the application's adopted
  vocabulary and rules as covering the tax concept being claimed. The
  authorization can supply only the first.

A nonzero value does not, by itself, establish that no additional relevant
fact is missing, and does not by itself establish that the adopted rules
modeled every category tax law recognizes. A zero value does not, by itself,
establish that a source family is known to be empty, or that no unmodeled
category of taxable interest could exist. Both require the same two kinds of
basis — workspace-record sufficiency and tax-model sufficiency — before
either is presented as an exhaustive total; neither basis is supplied by the
other.

## What the authorization does

| Question | Selected answer |
| --- | --- |
| What does the user authorize? | Treat the relevant current workspace facts as the exhaustive calculation universe within the authorization's scope. |
| What changes after an ordinary workspace edit? | The engine recalculates from the new current revision. The authorization continues. |
| What does the authorization support? | Workspace-record sufficiency only: ordinary return calculation and an explanation of why the current workspace could be treated as the complete input record for it. |
| What does it not support? | Tax-model sufficiency — whether the adopted vocabulary and rules cover every category the claimed tax concept requires. It also does not support objective tax completeness, source-content accuracy, filing readiness, or a claim that no later information will arrive. Tax-model sufficiency must come from the application's own declared coverage account, never from the user's authorization. |
| How does it end? | Suspension, withdrawal, or supersession by another authorization. Ending it removes calculation authority; it does not assert that the workspace is known to be incomplete. |
| What is recorded per run? | The authorization in effect, exact workspace revision and current findings, adopted rules and artifacts, calculated results, and dispositions. |

The authorization is standing but not unbounded. Reuse is legitimate only while
the run remains inside the authorization's declared scope. Ordinary fact
membership and value changes are inside that scope by design.

## Current behavior and required contract change

The current engine does not implement this decision. It implements per-family
closure:

1. `marshal_closure_authority` extracts current closure findings and current
   family horizons from projected record state
   (`packages/derivation/marshal.py:158-205,382-400`).
2. `resolve_closure_admissions` admits one family only when exactly one current
   finding for that family's current horizon has literal Boolean `true`; false,
   absent, displaced, non-Boolean, or duplicate findings do not admit it
   (`packages/derivation/source_authority.py:100-166`).
3. The runner exposes those admissions as `Environment.closed_sets`
   (`packages/derivation/runner.py:166-183,286-295`).
4. Empty `collect`, every `count`, and every `require_closed` consult that set
   (`packages/derivation/evaluator.py:118-141,206-211`).
5. Form 1040 line 2b unconditionally calls `require_closed` for all ten adopted
   interest families before it reads their subtotals
   (`packages/content/tax/2025/rule.form1040-line2b.v4.json:91-102,165-206`).

Current horizons deliberately make per-family closure expire on addition,
removal, or membership-changing reclassification. A same-member value
correction does not advance the horizon (`docs/adr/0017-recorded-family-horizons-for-closure-freshness.md`,
Decisions 3-7). That lifecycle conflicts with the selected direction: ordinary
workspace changes must recalculate without renewing the standing authorization.

Accepted contracts therefore cannot simply be relabeled:

- ADR-0007 Decision 1 and ADR-0010 Decisions 1-2 require calculated derived
  findings to enter the workspace record and projection through
  derived-publication acts. Ordinary derived-result publication remains
  governed by those decisions exactly as ratified. That current production
  does not call `append_publications` is an observed implementation fact, not
  a preservation this decision selects; whether that gap should be closed by
  wiring production to the existing contract, or addressed some other way, is
  a separate implementation question outside this completeness decision.
- ADR-0006 Decision 8 requires declared source-set closure before absence is
  treated as zero. A successor must preserve the honesty property while changing
  which authority satisfies it.
- ADR-0011 Decisions 4-5 define closure as a named-family, attested,
  affirmative-only determinable fact. The calculation authorization is instead
  a reusable permission over a bounded workspace calculation universe.
- ADR-0014 Decisions 1-5 require adopted per-family mappings, exactly one
  current true closure finding, a single internal dispatch, and exact closure
  pins. A successor must replace or narrow that exclusive admission contract;
  a second hidden authority path would violate Decision 4.
- ADR-0017 Decisions 3, 5, and 7 intentionally expire closure at every
  membership transition and require re-attestation. That is the opposite of
  continued authorization across ordinary edits.
- ADR-0026 Decision 5 requires line 2b to consume all family subtotals with
  closure, and Decision 6 prescribes horizon succession and rerun rather than
  manual withdrawal for late-family membership. The composition remains useful,
  but its authority and lifecycle contract must be reconciled.
- ADR-0032's runs-consume-facts boundary remains compatible: a run request must
  not carry invented tax values. The standing authorization and workspace
  revision must be obtained through an accepted record path, then marshalled
  with current facts and adopted artifacts.

No accepted ADR is edited here. Implementation requires an explicit successor
or narrowing decision before code or content changes.

## Present defects and gaps

The one committed entry producer for this family of behavior does not ask for
authorization. First W-2 wage entry creates a membership transition and a
separate literal-true W-2 closure finding with `basis: "documentary"`
(`packages/derivation/entry_loop.py:75-78,770-807`). The act envelope records
`actor`, but the closure value is manufactured from wage entry. It is neither
the attested closure required by ADR-0011/0017 nor the selected standing
workspace authorization. Kernel validation permits documentary basis for this
determinable fact when evidence is present; it does not enforce closure-specific
attestation (`packages/kernel/findings.py:524-558,582-590`). This is a current
behavioral defect to remove or supersede, not a precedent for automatic
authorization.

No committed 1099-INT entry surface captures a closure or workspace calculation
authorization. The 1099-INT content declares the box-1 closure fact, mapping,
and family, but the only production entry-loop closure write is the W-2-specific
constant and branch above (`packages/content/tax/2025/f1099int.bundle.json:23-35`;
`packages/content/tax/2025/closure-mapping.f1099int-b1.json:2-10`).

Current internal provenance is stronger than current reader visibility. A
closure-dependent derived finding pins the rule, mapping, family declaration,
closure finding, sources actually read, parameters, and operation semantics
(`packages/derivation/runner.py:297-395`). A production run record identifies
the workspace revision, governance and adoption pins, and per-rule dispositions;
published dispositions carry finding/act/symbol ids and blocked dispositions
carry codes and missing dependencies. The separately supplied
`adopted_packages` set gates the adoption pin but is not copied into the record
(`packages/derivation/production_executor.py:23-69`;
`packages/derivation/records.py:188-248`;
`packages/schemas/derivation/derivation-record.v7.schema.json:3-178,286-341`). Numeric presentation
recursively finds source leaves but classifies closure-backed zero separately
and removes closure leaves from reader citation sites; the attachment path also
filters direct closure leaves (`packages/derivation/presentation_projection.py:122-124,177-188,248-264,349-400`).
The selected direction requires the standing authorization to remain visible in
run explanation provenance rather than disappear at presentation.

## Narrow source-family confirmations (fallback)

When the standing workspace authorization is inactive — never adopted,
declined, or currently suspended — and a particular exhaustive claim still
needs a basis, the application requests an explicit confirmation scoped to
one source family instead. That confirmation is not the default interaction
while the standing authorization is active; it exists only as the narrower
fallback described above under "When the authorization is declined or later
suspended."

Because a source-family confirmation concerns the completeness of a
particular current *membership* set, its invalidation follows membership,
not content:

- adding a member to that family invalidates the confirmation;
- removing a member from that family invalidates the confirmation;
- a membership-changing reclassification invalidates the confirmation;
- correcting the value of an already-represented member does **not**, by
  itself, invalidate it — a content correction changes no membership.

**A family confirmation establishes only the exact proposition declared for
that family — never a broader tax concept.** Confirming the Form 1099-INT
box-1 family establishes only that every applicable box-1 statement item
within that family's declared scope is represented. It does not establish
that all taxable interest is represented, that every legally relevant
interest category exists in the product's vocabulary, or that Form 1040 line
2b's exhaustive-total claim is supported by itself. Even if every family the
adopted composition currently declares is confirmed, that proves the
declared composition's own input set is closed — nothing more — unless the
adopted contract separately establishes that the declared composition is
coextensive with the full tax concept it presents (ADR-0026 decision 7's
honesty gate is explicit that the current composition's claim must not be
read this way).

This is adopted product behavior for the fallback case, not a deferred
possibility. What remains deferred is only its technical representation —
what citizen or act records it, how it is keyed, and how it is marshalled —
which belongs to the successor contract, not to this decision.

## Deferred alternatives

These possibilities are not selected architecture. Reopen one only when its
named product need exists; do not design its schema, storage, identity,
evaluator container, interface, or publication mechanism in advance.

- **Action-scoped affirmation** — reopen only if a concrete use case requires a
  true affirmation for one execution while forbidding later reuse.
- **Conditional or hypothetical execution** — reopen only if users need a
  calculation that intentionally departs from current workspace state.
- **Provisional-fact or provisional-return status** — reopen only if a concrete
  product action requires two result standings with materially different
  permitted uses.
- **Saved scenarios or premise citizens** — reopen only if users need durable,
  editable, comparable alternative workspaces.
- **A distinct negative-completeness value** — reopen only if a concrete need
  requires the product to record an affirmative "known incomplete" claim
  rather than mere absence of authorization or confirmation.
- **A new persistence model for calculated results** — reopen only if a
  concrete need requires calculated results to be stored, projected, or
  reused in a way current production behavior does not already provide.

Assumption, affirmation, and withdrawal remain useful analytical distinctions.
An assumption is not evidence; an authorization is permission; withdrawal ends
permission without asserting incompleteness. Those distinctions do not make any
deferred mechanism a production requirement.

## Principal remaining decision: authorization scope

The remaining product-contract question is how far one authorization reaches.
At minimum the scope may need to identify the workspace, taxpayer or return
subject, tax year, and adopted calculation vocabulary or package boundary. If a
future package adds a materially new category of relevant information, the
product must not silently treat the old authorization as covering that expanded
universe.

The decision is not whether every ordinary source addition needs renewed
confirmation; it does not. The decision is which changes alter the meaning of
the calculation universe itself. A future contract must state that boundary and
the corresponding supersession rule before implementation. Identity,
authorship, storage shape, and interface copy remain downstream design work.

## Successor investigation: derived tax concepts and model coverage

This decision distinguishes workspace-record sufficiency from tax-model
sufficiency without designing how the second is declared, established, or
explained. That design is separate successor investigation, not answered
here:

- Whether a derived tax concept — "2025 US-federal taxable interest for this
  taxpayer," independent of Form 1040 line 2b or Schedule B — needs a
  first-class declaration beyond a rule's output symbol, or whether the
  current symbol-plus-rule-plus-quantity-vocabulary shape (as in
  `tax.us.2025.interest.taxable-total`) is sufficient long-term.
- How jurisdiction, taxpayer or subject, tax year, tax regime, quantity, and
  coverage attach to that derived concept if it is given its own
  declaration.
- Whether the current form-oriented source facts (a logical Form 1099-INT
  statement's box-1 amount, for example) adequately distinguish reported
  facts, underlying economic facts, and legal classification, or whether
  economic-event facts without a form (already partially present, e.g.
  non-form interest) should eventually replace or supplement form-oriented
  facts more broadly.
- How model-coverage provenance — the fact that a composition currently
  covers seven positive families and three adjustment classes, and no more —
  reaches run explanation, so a reader can see not just what was calculated
  but what the adopted vocabulary was and was not built to cover.

None of these questions is answered by this decision. Answering them is not
required to keep workspace-record sufficiency and tax-model sufficiency
correctly distinguished today.
