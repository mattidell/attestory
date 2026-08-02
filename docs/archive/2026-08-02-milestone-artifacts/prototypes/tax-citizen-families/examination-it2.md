# Examination — Iteration 2 (clean-room rival)

Builder seat: rival (`roles/builder-rival.md`). Branch:
`prototypes/tax-citizen-families/it2`. This is an independent, clean-room answer
to `charter-it1.md`. It was built without reading the incumbent iteration's
outputs; see **Clean-room disclosure** below for exactly what was and was not
read.

All exhibit paths are under `docs/archive/2026-08-02-milestone-artifacts/prototypes/tax-citizen-families/it2/`. The
single command that reproduces every result here:

```
PYTHONPATH=. python3 docs/archive/2026-08-02-milestone-artifacts/prototypes/tax-citizen-families/it2/tools/harness.py
```

It prints 77 checks, all `[PASS]`, exit 0. A captured run is committed at
`it2/EVIDENCE.txt`. The harness validates every citizen against the **published
kernel and derivation schemas** (the ratified runtime authority, Article 9) via
the real `SchemaRegistry`, and executes every fixture on **both** shipped
runners — the forward saturation runner and the demand-driven reference runner —
so any portability divergence would fail (E11.2).

## Clean-room disclosure

Read: `docs/governance/` (constitution, ontology, principles, engineering
constraints, commentary, records), `charter-it1.md`, `SEAT.md`, the First Tax
Slice plan and its planning inputs, ADRs 0002–0010, and the **ratified machinery
this content is authored onto** — the published schemas under
`packages/schemas/{kernel,derivation}`, the operation-semantics canon, and the
runner/evaluator/loader/package-validator source (`packages/derivation/`,
`packages/kernel/schema_registry.py`). Official primary tax sources were
verified at build time (see F8). *Not read:* `examination-it1.md`, `reviews/`,
`process-log.md`, the it1 branch/exhibit, or any review of any iteration. The
ADRs and machinery are shared, ratified material both builders target; reading
them is necessary to author conforming content and does not touch the
incumbent's design choices.

## Design in one paragraph

Two runner conveniences in the shipped Derivation Machinery are, for real tax
content, under-specified: form lines are bare `publishes` strings, and
source-set closure is a bare `closed_sets: frozenset[str]` handed to the runner.
This rival makes both first-class **declared content**. Two new citizen
families are added — `form-field.v1` (Q2/Q3/Q5) and `source-citation.v1` (Q5) —
and closure becomes an **elective fact** modeled on the *unchanged* kernel
`fact-type.v1` (Q1/Q4). Everything else is authored in the ratified rule
language. The derivation core is untouched: form fields and citations are never
runner inputs (E11.3), so the derived findings are identical whether or not they
exist (F8 parity is structural).

## The load-bearing finding

**The shipped runner cannot pin a closure assertion.** In `evaluator.py`,
`closed_sets` is a `frozenset[str]`; an empty-but-closed `collect` returns `[]`
(→ a published zero) but contributes **no pin**, because only *source* findings
become pins and there are none. So the machinery's "closure-backed zero" pins
nothing about closure — exactly the gap charter F3/F4/Q4 targets ("a
closure-backed zero … pins the closure assertion").

This rival's answer, entirely within the ratified contract: model closure as an
**elective finding** (`us.f1040.*-sources.closure`), feed it to the runner as a
`choice` input symbol, and have the line-mapping rule's `when` guard *read* it.
The `AccessLog` then records the reference, so the published zero pins the
closure finding. `closed_sets` degrades to a mere **projection** of those
findings (Article 5), and the stale-projection probe (F11) fails safe: a
`closed_sets` string with no backing finding leaves the rule's required symbol
absent → it blocks, never publishing a fake zero. Whether the machinery should
make `closed_sets` finding-backed natively is a candidate follow-on **machinery**
decision, surfaced here rather than papered over (plan Non-Goals).

## Fixture evidence map (F1–F12)

| Fixture | Where | Result |
|---|---|---|
| **F1** peerage + evidence mutation | harness §4; `us.w2.wage` fact type | Wage fact id is a function of `{employer, tax-year}` only — computed with zero documents. Evidence swap and removal leave finding value + identity byte-stable; only `evidence_ids` change (E1.1). |
| **F2** 1099-INT box distinction | `fixtures/box_distinction`; line-2b rule | `box` is a fact-type **identity key**; line 2b `collect`s box 1 + box 3 (both federally taxable); box 8 (tax-exempt) is present but excluded **by non-membership**, not by an unstated "taxable" filter. line 2b = 800, box-8 900 does not leak. |
| **F3/F4** closure-backed zero | `fixtures/wages_only_closed_interest`, `interest_only_closed_w2` | Empty **closed** set publishes 0; the zero **pins the closure finding** (verified in §8 walk). |
| **F5** absence/invalidity matrix | fixtures `present_zero_interest` (present-value-0), `wages_only_closed_interest` (closure-backed 0), `unclosed_interest` (open → `DEPENDENCY_ABSENT`), `invalid_source_value` (`DEPENDENCY_INVALID`) | Four states, four **distinct declared reasons**, no exception text. Each has an explanation path (§8). |
| **F6** Form 1040 core fields | `content/form-fields.2025.json` | Lines 1a, 2b, 9, 11, 12, 15, 16 as declared `form-field.v1` citizens with label, citation, binds_symbol, rendered-absence. |
| **F7** rendered absence + false guard | `form-field.rendered_absence`; line-12 standard/itemized split | Five dispositions declared per line; the **false guard** is the itemized branch: with `itemize-election=false` it is `inapplicable` (guard_result false), its non-existence explained by the record's inapplicable disposition, never a blank convention. |
| **F8** citation placement + mutation + parity | `content/citations.2025.json`; harness §3, §5 | Citations are inert `source-citation.v1` citizens referenced by id; ≥1 fully resolved (std-deduction, rate-schedule). A resolved-flag that disagrees with the fields (locator stripped) is caught. Parity is **structural**: `RunContext` has no citation field, so citation text cannot change any output. |
| **F9** evolution + mixed-year | `content/evolution/`; harness §9 | Later-year parameter (`standard-deduction.2026`, verified) and a later-year form-field version; the 2025 files are byte-immutable; a mixed-year package (2025 member in a 2026-scoped package) is **rejected** with `SCOPE_MISMATCH` by the ratified package validator (year lives in scope content, never in ids). |
| **F10** supersession cascade | harness §6 | Correcting the W-2 finding displaces line 1a and all downstream derived findings along ADR-0010 derivation edges (extracted from `input`/`choice` pins); line 2b (independent) is not displaced; re-derivation republishes corrected tax (3368). |
| **F11** coverage + stale projection | harness §7 | Coverage is recomputed fresh from current closure findings + run blocks (never stored), rebuilds byte-identical, and names the open interest set as a gap. A stale "closed" projection publishes no zero. |
| **F12** positive + negative schema | harness §1 (positives), §3 (negatives) | All positives validate; six negatives fail for their declared reason, including an **undeclared shape** (extra property) and a **wrong schema version** (`form-field.v2`). |

## Questions (Q1–Q10)

**Q1 — Is `fact-type.v1` sufficient?** Yes; no new version or companion is
forced. All seven tax fact types (W-2 wage, 1099-INT interest-by-box, filing
status, rounding convention, itemize election, and two source-set closures)
conform to the **unchanged** kernel `fact-type.v1` (harness §1). The two content
pressures the charter raised are absorbed by existing structure: **box meaning**
is an `identity_key` (`box` literal), and **closure** is an elective fact with a
`{complete: true}` `value_schema`. The only felt limitation is that
`supersession.policy` enumerates only `free`; every fact in this slice is
legitimately free-supersedable (wages correct freely; an elective closure or
election re-asserts freely), so the slice does not exercise a
governed-supersession policy — a real need the moment a method/convention fact
enters, but out of scope here and **not** a blocker for this slice.

**Q2 — Are form fields first-class citizens?** First-class citizens
(`form-field.v1`), not bare rule-output symbols and not (in this slice)
generated content. A bare `publishes` string cannot carry line identity, a human
label, a source citation, rendered-absence meaning, or tax-year versioning — the
exact reasons §5.6 deferred the family. Crucially they are **not consumed by the
runner** (E11.3 forecloses form identifiers in scheduler code): `binds_symbol`
is a one-way bridge from an abstract line to the derivation symbol that fills it.
Lifecycle: immutable, versioned per tax year (F9 shows a 2026 successor with the
2025 field untouched); the optional `lineage` field keeps the family
generator-ready without this slice choosing generation.

**Q3 — Where does rendered-absence live?** On the form field, as a
`rendered_absence` map keyed by **disposition** — and the disposition is
*recovered*, never stored. A fresh reader distinguishes the three nothings from
artifacts alone: a **computed zero** is a derived finding pinning a computation;
a **closure-backed zero** is a derived finding pinning a *closure finding*; a
**guard non-existence** is *no finding* plus a run-record `inapplicable`
disposition carrying the guard result and the pins the guard read. Two further
declared states — `blocked_unclosed` and `blocked_invalid` — are read from the
run record's distinct block codes. Explanation always terminates at declared
content + record + findings (Article 15), demonstrated in §8.

**Q4 — Closure as facts.** Nature: elective. Identity keys: `{tax-year}` per
source family (wages; taxable interest). Basis: elective (the assertion
constitutes it). Supersession: free — re-opening a set supersedes the closure
finding, which displaces the zero along a derivation edge (F10/ADR-0010). Pins:
the closure-backed zero pins the closure finding by id (§8). This is the rival's
central move over the shipped `closed_sets` string (see "load-bearing finding").

**Q5 — Source citations.** Inert `source-citation.v1` citizens, referenced by id
from form fields (and available to rules/parameters). "Fully resolved" requires
document identity + tax-year applicability + a precise locator; the validator
recomputes `resolved` and rejects a disagreeing flag (F8/F12). Non-operative
parity is **structural**, not merely tested: no derived finding can pin a
citation and the runner has no citation input, so citation text is provably
incapable of changing evaluation output. Citations carry no personal data.

**Q6 — Peerage (Article 1).** Preserved and enforced by the kernel schema
itself: `fact-type.v1.identity_keys` admits only `entity` and `literal` keys —
no source option exists. The wage fact is keyed on the employer entity and the
tax year; the interest fact on payer, year, and box. F1 shows replacing or
removing the supporting evidence changes only `evidence_ids`, leaving finding
value and identity byte-stable.

**Q7 — Canon / Declaration (Articles 9/10).** Every load-bearing noun is
schema'd before instances: the two new families have committed schemas and
positive instances; consumers reject undeclared shape (F12 includes an
undeclared-property and a wrong-schema-version negative, both rejected by strict
validation — no tolerant reader). Positives validate under the published runtime
authority; negatives fail for the declared reason.

**Q8 — Legibility (Article 11).** All tax meaning is in declared artifacts:
rule expression trees over the closed operation vocabulary, parameters as
separate citizens, box→line mapping as declared source-set membership,
rendered-absence as declared content. The runner contains no form identifiers;
form fields and citations sit entirely outside derivation. Portability holds:
both runners agree on every fixture (§2).

**Q9 — Record / coverage (Article 14).** Coverage is derived fresh from current
closure findings and the run's block surface, rebuilds byte-identical, and is
never stored as a second copy of form state. The stale-projection probe fails
safe because closure is load-bearing as a *finding*, not as the projected string
(F11).

**Q10 — Tier.** **Tier 2, contract-foundational.** `form-field.v1` and
`source-citation.v1` are new, durable citizen families that adopted production
content will depend on (plan §"Evidence And Decision Gate"; ADR-0006
consequences). Under ADR-0005 they need prototype evidence before an ADR — this
exhibit plus the incumbent's are that evidence. Two sub-answers are honestly
**Tier 1**: fact-type sufficiency (Q1) reuses an existing schema unchanged, and
closure-as-elective-fact (Q4) is content authored on an existing schema. They
are reported as Tier 1 findings folded into the Tier 2 family decision, not as
independent contract changes.

## Negative results and limitations (offered as evidence)

- **Closure blocking code.** To make the closure-backed zero *pin* the closure
  finding, this design routes an open set through a missing `choice` symbol, so
  the recorded block is `DEPENDENCY_ABSENT` naming the closure symbol — not the
  evaluator's native `SOURCE_SET_UNCLOSED`. This is a deliberate trade
  (pinnability over the coarser native code) and is a real divergence a reviewer
  should weigh; the native code cannot pin.
- **Line 16 uses the rate schedule for all incomes.** The real Form 1040
  mandates the Tax Table below $100,000; materializing it is deferred breadth.
  Declared in the rule note, not hidden.
- **Line 11 (AGI) carries line 9 forward.** The narrow no-adjustment case;
  Schedule 1 is out of scope and line 10 is structurally zero.
- **Governed supersession is unexercised** (Q1): only `free` policy appears,
  which is correct for this slice but leaves the method/convention path unproven.
- **No storage-level fault injection.** The runner/record atomicity conditions
  (E6.1/E14.1) are the machinery's ratification conditions, not re-proven here.

## Exhibit index

See `it2/README.md` for the file map. Schemas: `it2/schemas/`. Content:
`it2/content/` (bundle, rules, parameters, package, form-fields, citations) and
`it2/content/evolution/` (2026). Fixtures: `it2/fixtures/scenarios.json`.
Harness + captured run: `it2/tools/harness.py`, `it2/EVIDENCE.txt`.
