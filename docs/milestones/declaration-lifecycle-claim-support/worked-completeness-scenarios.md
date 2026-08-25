# Worked Workspace-Authorization Scenarios

## Scenario boundary

These scenarios use one synthetic 2025 Form 1040 line-2b sequence. All ids and
amounts are demonstrative. The selected behavior is conceptual: the current
engine still uses per-family closure and does not implement a standing
workspace-exhaustiveness authorization.

A current `rounding.convention` finding and the adopted rules' other
non-completeness prerequisites are present throughout. Each scenario varies
only workspace interest facts and calculation authority.

The adopted line-2b rule reads ten subtotal symbols and unconditionally checks
all ten source families with `require_closed`
(`packages/content/tax/2025/rule.form1040-line2b.v4.json:91-102,111-206`).
Each family subtotal has its own rule. For box 1, a nonempty `collect` aggregates
current rows without reading closure; an empty `collect` blocks unless the box-1
family is admitted (`packages/content/tax/2025/rule.f1099int-b1-subtotal.json:11-33`;
`packages/derivation/evaluator.py:118-131`). Line 2b can therefore block for lack
of closure even when a nonempty box-1 subtotal was calculated.

Every scenario below distinguishes two independent supports a "line 2b is $X"
claim needs: **workspace-record sufficiency** (the current workspace is
treated as the complete input record — what the standing authorization or a
narrower confirmation supplies) and **tax-model sufficiency** (the adopted
ten-family composition and its three adjustments cover the tax concept
"total taxable interest" — which the authorization never supplies, and which
the committed composition's own text scopes narrowly, per
`completeness-support-model.md`). A scenario account that says workspace
facts are complete is never, by itself, an account that the tax model is
complete.

For every selected-direction scenario, a run must identify the standing
authorization, exact workspace revision and current findings, adopted package,
rules, parameters and operation semantics used, results, and dispositions. The
production record already stores the revision and adopted artifacts, while
derived finding pins carry rule and input dependencies
(`packages/derivation/production_executor.py:23-69`;
`packages/derivation/runner.py:297-395`). The authorization itself and its reader
visibility are not implemented.

## 1. Standing authorization is adopted

**Setup.** The user first requests a return-level generation requiring an
exhaustive total (line 2b) in synthetic workspace `demo.workspace.1040` for
tax year 2025 — not on ordinary 1099-INT entry — and at that point authorizes
the application to treat relevant current facts as the exhaustive calculation
universe. The exact adopted-package boundary is left to the open scope
decision.

| Question | Account |
| --- | --- |
| Current committed behavior | No such authorization citizen or capture path exists. The closest mechanism is one literal-true closure finding per family and current horizon. The 1099-INT box-1 content declares that narrow fact, but no committed 1099-INT entry path writes it (`packages/content/tax/2025/f1099int.bundle.json:23-35`; `packages/content/tax/2025/closure-mapping.f1099int-b1.json:2-10`). |
| Selected behavior | One standing authorization becomes applicable across ordinary fact additions, removals, reclassifications, and corrections within scope. This is workspace-record sufficiency only; it says nothing about whether the adopted tax vocabulary and rules cover the tax concept the user will later ask for. |
| Required work | Define a successor contract for the authorization, its scope, capture, currency, supersession, marshalling, and explanation provenance. Reconcile ADR-0011/0014/0017 rather than adding a second authority path. |
| Not established | That the workspace is objectively complete; that no later information can arrive; that every tax rule is implemented; that filing is authorized; or that the application's adopted vocabulary is tax-model sufficient for any tax concept it will later be asked to calculate. |

The W-2 entry loop is not a capture precedent: it automatically creates
documentary literal-true closure from wage entry without asking
(`packages/derivation/entry_loop.py:75-78,770-807`). That present defect must not
be generalized into automatic workspace authorization.

## 2. No taxable-interest facts stand

**Setup.** At workspace revision `demo.revision.001`, no current facts populate
any of line 2b's ten interest families. The standing authorization applies.

| Question | Account |
| --- | --- |
| Current committed behavior | Every empty family subtotal reaches `collect`'s empty branch and blocks unless its own family is in `env.closed_sets`. With none of the ten subtotals available, line 2b never becomes eligible and `finalize_unreached` records `DEPENDENCY_ABSENT` for the missing subtotal symbols; if those dependencies were present, its guard would separately require all ten family admissions (`packages/derivation/evaluator.py:118-131,206-211`; `packages/derivation/runner.py:1188-1247`; `packages/content/tax/2025/rule.form1040-line2b.v4.json:91-102,165-206`). |
| Selected behavior | The standing authorization supplies workspace-record sufficiency: the application may treat the current, empty workspace as the complete input record for each of the ten declared families, so each subtotal may calculate as zero. Whether "zero across these ten families" honestly means "$0 total taxable interest" is a separate, tax-model question — one the currently adopted composition's own scope (seven positive families plus three adjustments, per `completeness-support-model.md`) does not resolve by itself; nothing here proves that scope is coextensive with the full tax concept. The zero is an ordinary run output, but it cannot be presented as the exhaustive tax total unless tax-model sufficiency is independently established. |
| Required work | Replace or narrow the per-family closure admission contract so one applicable authorization can honestly support workspace-record sufficiency for both empty-family zeroes and a broader total. Separately, and not resolved by that work, is whether the adopted composition's declared scope should be presented as tax-model-sufficient for "total taxable interest," or only for the ten families it actually declares. |
| Not established | That each source family is independently known empty; that taxable interest can never later appear; that the return is ready to file; or that the ten-family composition is a complete account of taxable interest as a tax-law concept. |

## 3. One interest fact is added

**Setup.** At revision `demo.revision.002`, one current 1099-INT box-1 amount of
`500` is added. The standing authorization remains applicable.

| Question | Account |
| --- | --- |
| Current committed behavior | The box-1 subtotal's nonempty `collect` can calculate `500` without reading box-1 closure. With no closure for the other nine empty families, their subtotals block and line 2b finalizes as `DEPENDENCY_ABSENT` before its guard can run. If the other nine subtotals are closure-backed but box 1 remains unadmitted, line 2b becomes eligible and then blocks at the box-1 `require_closed`. Either path prevents line-2b publication (`packages/derivation/evaluator.py:118-131,206-211`; `packages/derivation/runner.py:1188-1247`; `packages/content/tax/2025/rule.form1040-line2b.v4.json:91-102,165-206`). |
| Selected behavior | Recalculate line 2b from revision 002 without renewed confirmation. The new result pins the current amount and authorization, along with the adopted rule and other dependencies. Turning "one logical statement reports $500 in box 1" into "$500 contributes to 2025 US-federal taxable interest" is the adopted composition's classification act, not something the entered amount or the workspace authorization performs by itself. |
| Required work | Make line-2b exhaustiveness depend on the standing authorization rather than renewed per-family horizon closure, while preserving the ten-family composition. |
| Not established | That the entered amount is accurate; that it came from every possible taxable-interest source; that line 2b equals a mere document sum; or that the ten-family composition it feeds is a tax-model-complete account of taxable interest. |

At this `500` value, Form 1040 line 2b is the committed reader surface if the
rule can publish. Schedule B is not required merely by this amount because its
threshold condition is strictly greater than `1,500`
(`packages/content/tax/2025/rule.attachment.schedule-b.v4.json:273-287`;
`packages/content/tax/2025/parameter.schedule-b-threshold.json:1-12`).

## 4. Another fact is added or a value is corrected

**Setup A.** Revision `demo.revision.003a` adds a second box-1 fact of `200`.

**Setup B.** Alternatively, revision `demo.revision.003b` corrects the existing
`500` fact to `550` without changing its family membership.

| Question | Account |
| --- | --- |
| Current committed behavior | Both nonempty box-1 collections calculate their current subtotal without reading closure. Addition advances the box-1 horizon and displaces closure keyed to its predecessor; same-member value correction does not advance the horizon. In either case line 2b still requires all ten current family admissions (ADR-0017 Decisions 3-7; `packages/derivation/evaluator.py:118-131`). |
| Selected behavior | Recalculate from the chosen new revision. The same standing authorization applies to both the added-member and corrected-value case. |
| Required work | Preserve record-derived current findings and correction/membership provenance while decoupling authorization reuse from family-horizon succession. |
| Not established | That addition and correction are the same record act, or that their currency histories may be collapsed. They share only the authorization-reuse outcome. |

## 5. Interest facts are removed, including the last one

**Setup.** Revision `demo.revision.004` removes one current interest fact.
Revision `demo.revision.005` removes the last one. The authorization remains
applicable.

| Question | Account |
| --- | --- |
| Current committed behavior | Each accepted membership removal advances the family horizon and displaces predecessor-horizon closure. After the last removal, the box-1 subtotal's empty `collect` blocks until a new true closure finding exists for the successor horizon; line 2b also blocks (`docs/adr/0017-recorded-family-horizons-for-closure-freshness.md`, Decisions 3, 5, and 7; `packages/derivation/evaluator.py:118-131`). |
| Selected behavior | Recalculate after each removal without renewed authorization. After the last removal, zero becomes applicable again for the box-1 component and, if no other interest facts stand, for line 2b — with the same qualification as Scenario 2: the standing authorization supplies workspace-record sufficiency for the zero, not a tax-model claim that the ten-family composition exhausts "total taxable interest." |
| Required work | Preserve member-transition and currency history, but stop using ordinary membership succession as an invalidator of the workspace authorization. |
| Not established | That a removed fact never existed, that zero is timeless, or that the authorization asserted each family was empty. |

## 6. Authorization is suspended or withdrawn

**Setup.** After revision 005, the user suspends or withdraws the standing
authorization without asserting that the workspace is incomplete. Line 2b is
then requested again, and separately, the user supplies a narrower box-1-only
confirmation instead.

| Question | Account |
| --- | --- |
| Current committed behavior | There is no workspace-authorization mechanism to withdraw, and no per-family fallback-confirmation mechanism either. Removing, falsifying, or displacing one family closure makes that family non-admitted. An empty subtotal blocks at `collect`; if that leaves a required subtotal absent, line 2b finalizes as `DEPENDENCY_ABSENT`. When all subtotals exist but one nonempty family lacks admission, line 2b instead reaches and blocks at that family's `require_closed`. A nonempty family subtotal can remain mechanically calculable because nonempty `collect` does not read closure, but line 2b cannot publish without all ten admissions (`packages/derivation/source_authority.py:141-166`; `packages/derivation/evaluator.py:118-131,206-211`; `packages/derivation/runner.py:1188-1247`; `packages/content/tax/2025/rule.form1040-line2b.v4.json:91-102,165-206`). |
| Selected behavior | Line 2b, as an exhaustive-total claim, lacks authority and blocks — it is not presented as the ordinary return total, and no "workspace is a work in progress" state is asserted. Only line 2b (the dependent result) blocks; the box-1 amount and unrelated facts remain available, and may be shown as a directly sourced value or a recorded-items sum. If the user instead supplies the narrower box-1 confirmation, that confirmation supports only box-1's own contribution — line 2b still requires the other nine families' own workspace-record basis, standing or narrower, before it can publish as an exhaustive total. Even with all ten families' workspace-record basis established, that establishes only the declared composition's own input set is closed; it does not separately establish that the composition is tax-model sufficient for "total taxable interest." The box-1 confirmation is invalidated by adding, removing, or reclassifying a box-1 member; correcting an already-represented box-1 amount does not invalidate it. Earlier run results retain the authorization and revision they actually used. |
| Required work | This scenario's semantics — no negative-completeness claim, dependent-result-only blocking, family-confirmation invalidation by membership not content — are decided. What remains is successor-contract work: an act kind or citizen shape for the standing authorization's suspension/withdrawal and for the narrower family confirmation, reconciled with ADR-0017's per-family horizon lifecycle and ADR-0026 Decision 6's "no manual withdrawal" clause. |
| Not established | That the workspace is known incomplete, that earlier authorized runs were invalid when made, or that withdrawal or an unmet confirmation is a correction to `false`. |

The selected direction does not choose an act kind or displacement mechanism
for either the standing authorization's suspension or the narrower family
confirmation. A Boolean `false` is not assigned the product meaning
"authorization withdrawn" or "family incomplete."

## 7. Provenance for every result

**Setup.** Compare the zero at revision 001, the `500` result at revision 002,
the recalculation at revision 003, and the zero after revision 005.

| Question | Account |
| --- | --- |
| Current committed behavior | Production run records retain workspace revision, adoption and governance pins, and per-rule dispositions; published dispositions carry output ids and blocked dispositions carry codes and missing dependencies. The supplied adopted-package set gates the adoption pin but is not stored as a second list (`packages/derivation/production_executor.py:23-69`; `packages/derivation/records.py:188-248`; `packages/schemas/derivation/derivation-record.v7.schema.json:3-178,286-341`). Derived findings pin their rule, current source/ref findings, parameters, closure mappings/declarations/findings actually read, operations, and citations (`packages/derivation/runner.py:297-395`). Numeric reader projection exposes source citations but removes closure authority leaves (`packages/derivation/presentation_projection.py:122-124,177-188,248-264`). |
| Selected behavior | Each result identifies the standing authorization, exact revision and current inputs, adopted rule and artifact versions, calculation dependencies, and disposition. The authority is explanation provenance, not a qualification attached to every numeric value. That provenance explains workspace-record sufficiency (why the workspace was treated as the complete input record); it does not by itself explain or certify tax-model sufficiency (why the adopted composition's declared scope was treated as the whole tax concept), which is a separate account the adopted content's own declarations must carry. |
| Required work | Carry authorization identity and scope into run and explanation provenance, and expose it where a reader needs to understand why the workspace was treated as exhaustive. Separately, expose the adopted composition's own declared scope (which families, which adjustments) so a reader can see what tax-model coverage was and was not claimed. |
| Not established | That every dependency must be duplicated as a direct pin when transitive provenance already identifies it; that source citations alone prove calculation authority; or that explaining workspace-record sufficiency also explains tax-model sufficiency. |

History remains immutable. Recalculation creates a new run account; it does not
mutate a prior `RunResult` or promote one result into another.

## 8. Filing remains separate

**Setup.** The user later chooses whether to file a return produced from one of
the authorized calculations.

| Question | Account |
| --- | --- |
| Current committed behavior | The examined calculation runner returns results and records execution; it does not perform a Form 1040 filing declaration (`packages/derivation/production_executor.py:23-69`). |
| Selected behavior | Filing requires its own later act and applicable safeguards. The standing calculation authorization neither performs nor substitutes for it. |
| Required work | None is selected here; filing design is outside this publication. |
| Not established | Tax liability, filing readiness, taxpayer signature, or the return-level knowledge-and-belief declaration. |

The 2025 Form 1040's filing declaration covers the return and accompanying
schedules and statements as a whole
([2025 Form 1040](https://www.irs.gov/pub/irs-pdf/f1040.pdf)). It is not a model
for repeated internal source-family closure.

## Scope-change probe

Ordinary membership and value changes in Scenarios 3-5 do not require renewed
authorization. A materially expanded adopted package presents a different
question: it may change what counts as relevant workspace information. The
successor contract must decide whether workspace, subject/taxpayer, tax year,
and adopted calculation vocabulary are identity or applicability dimensions of
the authorization.

Until that decision is made, no scenario establishes that an authorization for
one calculation universe silently covers a later, broader one.
