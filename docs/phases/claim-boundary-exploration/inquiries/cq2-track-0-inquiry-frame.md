# Track 0 Inquiry Frame — "Why are you asking me to say I'm done?" (CQ-2)

> ## ⚠ SUPERSEDED IN PART — one conclusion in this packet is disproven
>
> This packet is retained as the working record given to the Track 1
> standpoint agents. **One of its conclusions is factually wrong** and was
> corrected during the owner-directed factual repair of 2026-08-20.
>
> **Disproven claim — §7, the horizon-only invalidator.** This packet states
> that family horizon succession is "the only staleness/withdrawal mechanism
> found in committed code or content," and its verification table grades that
> claim Confirmed. The grading rested on the `title` prose of the
> `tax.us.2025.f1099int.b1.source-closure` fact and did not extend to the
> fact's adjacent `supersession` field, which carries policy `free`. A later
> finding on the same `fact_id` therefore displaces the earlier one as a
> `correction` in `packages/kernel/currency.py`, independent of any horizon
> change. There are **two** invalidating mechanisms, not one.
>
> **Not disproven — §2, the admission collapse.** §2's account is accurate as
> written: absent, duplicate, `false`, and truthy-non-boolean values all fall
> through `packages/derivation/source_authority.py` alike. This packet does
> **not** assert that a "no" is unrepresentable. That error appears
> downstream: the external Track 1 (Grok) account states it in Attack 3
> without closing it, and Track 2 §4.3 closes it as a settled disposition.
>
> For the corrected account — the four-layer closure model, both invalidating
> mechanisms, and the per-packet reconciliation of which error appears where
> — read
> [`cq2-track-3-curated-inquiry.md`](cq2-track-3-curated-inquiry.md) §4, §5,
> and §14.1. Where this packet and that one disagree, that one governs.

Audience: Product, Shared (exploratory record). This packet is the **only**
context given to the two Track 1 standpoint agents (a fresh Claude
sub-agent and Grok via `mcp__grok__grok_consult`); it must stand alone.

Status: **exploratory, non-authoritative.** Paper analysis plus one executed
committed test suite, both against already-committed synthetic content and
public IRS instruction text. Creates no product contract, adopts no
definition, changes no code, schema, rule, or ADR. "Claim boundary" is a
working lens for this phase, not new vocabulary or a citizen.

Milestone: Declaration Request to Claim Boundary Inquiry (CQ-2), second
worked inquiry in the Claim Boundary Exploration phase. CQ-1 (closed)
examined a **system-presented result** (Form 1040 line 2b's published
number). CQ-2 examines a **system request for a user declaration** — the act
of asking the user to assert something, before any number on this one family
is finalized — holding the same tax domain (the Form 1099-INT box 1 source
family that feeds the same line, 2b) constant so the two inquiries can be
compared.

All artifact and code claims below were independently re-derived by Track 0
by reading the cited file directly on this branch. No claim is cited from
the milestone plan as a substitute for reading the source. Where the milestone
plan's "Verified concrete witness" section made the same claim, Track 0's
independent re-read is recorded as confirmed, not as agreement with the plan.

---

## 1. The declaration this inquiry traces

**Fact type:** `tax.us.2025.f1099int.b1.source-closure`
(`packages/content/tax/2025/f1099int.bundle.json`, `bundle.v2`, entry
`fact-type.v2`, `nature: determinable`, `value_schema: {"type": "boolean"}`).

**Proposition and scope (verbatim from the fact type's own title):**

> "User-attested closure of the Form 1099-INT box-1 source family for 2025,
> keyed on the family membership horizon current at attestation (ADR-0017):
> true asserts every furnished 1099-INT box-1 statement item is recorded as
> of that horizon. This claim covers box 1 only — never other boxes,
> non-form interest, or Form 1040 line 2b (ADR-0016)."

**Invalidator (verbatim, same title):**

> "A later membership transition displaces this closure through horizon
> succession; re-attestation on the successor horizon is required."

**Declaring family:** `tax.us.2025.f1099int.b1`
(`packages/content/tax/2025/family.f1099int-b1.json`, `source-family.v1`):
`member_predicate.fact_type = tax.us.2025.f1099int.box1-interest`,
`authorizes_subtotal = tax.us.2025.interest.b1-subtotal`. Its own
`closure_claim` text: "Every interest amount reported in box 1 of a Form
1099-INT furnished to the taxpayer for tax year 2025 is recorded as a
statement item. This claim covers Form 1099-INT box 1 only: it says nothing
about other 1099-INT boxes, interest not reported on Form 1099-INT, or total
taxable interest (Form 1040 line 2b)."

**Closure mapping:** `tax.us.2025.closure-mapping.f1099int-b1`
(`packages/content/tax/2025/closure-mapping.f1099int-b1.json`,
`source-closure-mapping.v2`) pins family `tax.us.2025.f1099int.b1` v1
exactly, `member_fact_type: tax.us.2025.f1099int.box1-interest`,
`closure_fact_type: tax.us.2025.f1099int.b1.source-closure`,
`closure_horizon_key: "family-horizon"`, `admits_symbol:
tax.us.2025.interest.b1-subtotal`, `admission.condition:
"current-literal-true"`.

---

## 2. Why the user, not the software — verified against code

`packages/derivation/source_authority.py`, function
`resolve_closure_admissions`: for each adopted mapping, the code looks up
closure findings whose `fact_type` matches the mapping's closure fact type
and whose `horizon_id` equals the family's *current* horizon
(`current_horizons.get(family_id)`). A family is admitted only if exactly
one such candidate exists **and** `candidate.value is True` (a boolean
`True`, not merely truthy). Any other case — absent, duplicate, false, or a
non-boolean truthy value — falls through with a `continue` and the comment
"blocked, never zeroed." There is no branch anywhere in this function, or in
`packages/derivation/marshal.py`'s `marshal_closure_authority` (which builds
the candidate list from only *current* findings, via
`currency.current_finding_ids`), that computes or infers this boolean from
any other fact. It is asserted by a closure finding or it is absent.

`ClosureAdmission` (same module) records `mapping_id`, `mapping_version`,
`declaration_id`, `declaration_version`, `horizon_id`, and
`closure_finding_id` — the full attribution chain for whatever admits the
family.

`packages/derivation/runner.py` line 178 calls `resolve_closure_admissions`
and line 290 builds `closed_sets=frozenset(self.admissions)` — the exact set
the evaluator checks (§3 below). This is the one dispatch path; no
alternative admission route exists in the runner.

---

## 3. Consuming code and what "blocked" means at runtime — verified

`packages/content/tax/2025/rule.form1040-line2b.v4.json`: `requires` lists
exactly ten symbols — seven positive-interest family subtotals
(`b1-subtotal`, `b3-subtotal`, `oid-subtotal`, `non-form-subtotal`,
`form1065-k1-box5-subtotal`, `b10-market-discount-subtotal`,
`oid-b5-market-discount-subtotal`) and three Schedule B adjustment subtotals
(`scheduleb-nominee-subtotal`, `scheduleb-accrued-interest-subtotal`,
`scheduleb-abp-adjustment-subtotal`). `b1-subtotal` is one of the ten. The
rule's `when` block contains ten `{"op": "require_closed", "source_set":
...}` conditions, one per family, plus a non-negative-result guard; `value`
computes the seven-family sum less the three adjustment subtotals.

`packages/derivation/evaluator.py`: the `require_closed` operator (line 206)
checks `source_set not in env.closed_sets` and raises `EvalBlocked(
BLOCK_CLOSURE, [source_set])` — `BLOCK_CLOSURE = "SOURCE_SET_UNCLOSED"` — on
a miss. This is a **block**, an `EvalBlocked` exception the runner catches
and reports as a disposition, not a zero and not a silent skip.

`packages/content/tax/2025/form1040.line-2b.form-field.v5.json`
`dispositions.blocked`: the `codes` list includes `"SOURCE_SET_UNCLOSED"`
(among three others); the `explain` text is one fixed string — "Taxable
interest is blocked because one or more constituent interest families are
unclosed or their dependencies are missing." — **the same string regardless
of which of the ten families is the actual cause.** This is inherited from
CQ-1 (that inquiry's SC-3 finding, re-verified here directly against v5, not
re-derived): closing box 1 alone cannot, by itself, tell a user *which*
family is still open if others remain unclosed, because the rendered text
does not vary by cause. CQ-2 treats this as background context, not a new
finding.

Also inherited and re-verified, not re-litigated: `finding.v2`'s `basis`
enum is exactly `{"documentary", "attested", "elective"}`
(`packages/schemas/kernel/finding.v2.schema.json`), and the same form-field
v5's `closure_backed_zero` disposition explain text reads "...all
constituent families are attested closed on their current horizons..." —
using "attested" in an ordinary-English sense that collides with the
kernel's reserved `basis: attested` vocabulary (ADR-0009's SC-8 finding from
CQ-1, confirmed still present in v5). Separately and independently verified:
the one committed closure-finding-producing code path found in this
repository, `packages/derivation/entry_loop.py` (the W-2 closure act, lines
784–795 — not a 1099-INT box-1 closure act; no committed code path
currently produces a 1099-INT box-1 closure finding), writes
`"basis": "documentary"`, never `"attested"`, into the finding it creates.
The ordinary-English collision in the explain string and the kernel's
structural `basis` value are two separately verified facts, not the same
fact restated twice — and no committed code exercises the 1099-INT box-1
closure act itself, so V10's evidence is about the shape of the one
producing path that exists, not about this specific family's own act.

---

## 4. Verification table (V1–V10, independently re-derived)

| # | Claim | Status | Evidence |
| --- | --- | --- | --- |
| V1 | Closure fact type's proposition, scope limit, boolean value schema | **Confirmed** | `packages/content/tax/2025/f1099int.bundle.json` — title text quoted in §1 verbatim; `value_schema: {"type": "boolean"}` |
| V2 | Invalidator is horizon succession requiring re-attestation | **Confirmed** | Same title text, final sentence, quoted in §1 |
| V3 | Family's `closure_claim`, `member_predicate.fact_type`, `authorizes_subtotal` | **Confirmed** | `packages/content/tax/2025/family.f1099int-b1.json` — all three fields read directly, quoted in §1 |
| V4 | Mapping pins exact family/version, names closure fact type and `family-horizon` key, admits only `interest.b1-subtotal` | **Confirmed** | `packages/content/tax/2025/closure-mapping.f1099int-b1.json` — all fields present exactly as claimed |
| V5 | Admission requires current, literal-true closure finding on current horizon; no code path derives the boolean | **Confirmed** | `packages/derivation/source_authority.py::resolve_closure_admissions` (boolean-True-only admission, no derivation branch); `packages/derivation/marshal.py::marshal_closure_authority` (only current findings considered) |
| V6 | `rule.form1040-line2b` v4 has ten `require_closed`-gated pins; `b1-subtotal` is one | **Confirmed** | `packages/content/tax/2025/rule.form1040-line2b.v4.json` — ten `requires` entries, ten `require_closed` conditions in `when`, counted directly |
| V7 | `require_closed` blocks (not zeroes) on a missing family | **Confirmed** | `packages/derivation/evaluator.py` line ~206–209: `EvalBlocked(BLOCK_CLOSURE, ...)` raised, `BLOCK_CLOSURE = "SOURCE_SET_UNCLOSED"` |
| V8 | `blocked` explain text is generic across all ten families (inherited SC-3) | **Confirmed, still live in v5** | `packages/content/tax/2025/form1040.line-2b.form-field.v5.json` — one fixed `explain` string for the `SOURCE_SET_UNCLOSED` code (and three other codes) |
| V9 | `finding.v2` `basis` enum is `{documentary, attested, elective}`; `closure_backed_zero` explain text uses "attested" in ordinary-English sense (inherited SC-8) | **Confirmed, still live in v5** | `packages/schemas/kernel/finding.v2.schema.json` (enum exact); form-field v5 `closure_backed_zero.explain` text |
| V10 | The one committed closure-finding-producing code path writes `"basis": "documentary"` | **Confirmed, with a scope correction** | `packages/derivation/entry_loop.py` lines 784–795. **Correction of a possible over-read of the plan:** this code path produces a **W-2** closure finding (`W2_CLOSURE_FACT_ID`), not a 1099-INT box-1 closure finding. No committed code path in this repository currently exercises the 1099-INT box-1 closure act itself. The claim as stated in the plan — "the one committed closure-finding-producing code path" writes `basis: documentary` — is accurate on its own terms (it does not claim the path is for box 1); Track 0 flags this because a careless reading could conflate "the one closure-producing path found" with "a box-1-specific path," which the code does not support. |

No claim required correction to its substance; V10 required a scope
clarification to prevent a plausible misreading. This is a materially
smaller correction than CQ-1's Track 0 (which refuted two Foreman claims
outright) — recorded plainly per the charter's standing instruction to say
so either way.

---

## 5. Runtime behavior — both states, **executed**

A committed test harness exists and was run:
`python3 -m pytest tests/tax/test_track6_integration.py` — 4 tests, 19
subtests, all passed, including the `unclosed_interest_composition`
scenario. The evidence below is **executed**, not static-read: the cited
values come from the test run's actual assertions against the CLI-produced
report, cross-checked against the scenario's own committed golden fixture at
`packages/sample_data/tax/scenarios/unclosed_interest_composition/`
(`scenario.json` and `expected/report.json`).

### State A — declared / closed (box 1 admitted)

The scenario's `closure.findings` includes a current, literal-true closure
finding for `tax.us.2025.f1099int.b1.source-closure` on the horizon named as
current for that family (`closure.current_horizons` maps
`tax.us.2025.f1099int.b1` to that same horizon id). The committed golden
`expected/report.json` shows `tax.us.2025.interest.b1-subtotal` published
with value `"10"` (one $10 synthetic box-1 interest item), attributed to
rule `tax.us.2025.rule.f1099int-b1-subtotal`. The b3 and OID families are
also closed in this scenario and both subtotal to `0`. Declaring box 1
closed here does exactly one thing: it admits `b1-subtotal` into the closed
set so a rule that requires it stops blocking on that one family — nothing
downstream of line 2b becomes any less blocked by this alone.

### State B — not yet ready (a required family absent)

The same scenario leaves `tax.us.2025.non-form-interest` with a current
horizon (`closure.current_horizons` names one) but **no** closure finding
for that family's closure fact type. The executed test asserts (and the
golden fixture shows) that this produces, exactly and only:

- `tax.us.2025.rule.non-form-interest-subtotal` blocked with code
  `"SOURCE_SET_UNCLOSED"`, `missing: ["tax.us.2025.non-form-interest"]`.
- `tax.us.2025.rule.form1040-line2b` blocked with code
  `"DEPENDENCY_ABSENT"`, `missing:
  ["tax.us.2025.interest.non-form-subtotal"]` — **not** `SOURCE_SET_UNCLOSED`
  at the line-2b rule itself, because the evaluator reaches the missing-pin
  reference before line 2b's own `require_closed` check on that source set;
  the root cause (an unclosed family) surfaces as a different code one hop
  downstream. This is a verified, executed nuance: the code a user's UI
  would see attached to line 2b is not always the same code that names the
  actual cause one hop up the chain.
- Four further downstream lines also blocked with `DEPENDENCY_ABSENT`,
  cascading from the same root cause — and each one names a *different*
  missing symbol, none of which is the unclosed family: `form1040-line9`
  (missing `interest.taxable-total`), `-line11` (missing
  `income.total-income`), `-line15` (missing `income.agi`), and `-line16`
  (missing `income.taxable-income`). Six blocked entries in total, of which
  exactly one — `non-form-interest-subtotal` — names the actual unclosed
  family. By the time the cause reaches the lines a user actually looks at,
  the declaration that would fix it is named nowhere in the blocked record.
- No error, no exception surfaced to a caller, no silent zero: `stop_reason`
  in the report is `"saturated"` (the run reached a stable fixed point with
  some rules blocked, not a crash).

This is exactly the "not yet ready" case: an absent declaration blocks the
rules that require it and cascades forward; it does not zero, does not
error, and does not affect the already-admitted `b1-subtotal`,
`b3-subtotal`, or `oid-subtotal` findings, which remain published in the
same report.

---

## 6. The user situation and the plain answer

**Situation:** a filer has entered their Form 1099-INT box 1 statement
items in the product and is presented with an affordance asking them to
assert — "declare," "confirm," "say I'm done" — that this one family (box 1
of every 1099-INT they received) is complete. No dollar total on line 2b has
been finalized yet; this is the request that precedes it, not the result
that follows it.

**Compressed subquestions inside "Why are you asking me to say I'm done?":**

- Why do you need *me* to say this — can't the software just check?
- What exactly am I agreeing is true?
- Does saying yes finish my return, or just this one piece?
- What if I'm not sure / not ready — what happens if I say nothing, or no?
- Can I take it back later if I'm wrong or get another form?
- Is this the same as signing my return?

**Plain answer (two sentences, written only after the trace above):**

> You're the only one who knows whether every 1099-INT you received with box
> 1 interest on it has been entered — the software can't check your mailbox
> for you, so it needs you to say so before it can use this piece in your
> return. Saying yes here only covers this one form's box 1; it doesn't
> finish your return, and it isn't the same as signing it.

---

## 7. Claim-boundary trace

- **Proposition:** every Form 1099-INT box 1 statement item furnished to the
  taxpayer for 2025 is recorded as of the current family-membership horizon.
- **Speaker:** the taxpayer (user-attested; the artifact's own title says
  "User-attested"). The system supplies the mechanism and the scope
  boundary; it does not supply, infer, or verify the underlying fact.
- **Basis:** in the one committed closure-finding-producing code path this
  repository has (a different family, W-2 — see §3), the finding's
  structural `basis` is `"documentary"`, one of three kernel-reserved values
  (`documentary`, `attested`, `elective`; ADR-0009). No committed code
  currently writes a box-1 closure finding, so this family's own eventual
  `basis` value is not directly observed, only inferable from the pattern.
- **Scope:** box 1 of Form 1099-INT only — explicitly and repeatedly, in the
  fact type's own title and the family's own `closure_claim` text — never
  other 1099-INT boxes, never non-form interest, never Form 1040 line 2b
  itself.
- **Effect:** admits `tax.us.2025.interest.b1-subtotal` into the set any
  rule may require closed (verified in §2–3); nothing else. It does not
  publish, compute, or change any value by itself.
- **Non-effect (unsupported neighboring inference):** declaring box 1
  closed does **not** mean line 2b is published — line 2b requires all ten
  pins closed (§3) — and it does **not** mean the return is complete or
  signed. "I said box 1 is done" does not support "my taxable interest is
  final" or "my return is ready to file."
- **Invalidator:** a later membership transition on this family displaces
  the closure through horizon succession; re-attestation on the successor
  horizon is required (verified verbatim in §1). This is the only
  staleness/withdrawal mechanism found in committed code or content — no
  committed UI "un-declare" or "withdraw" action exists anywhere in the
  codebase searched for this inquiry (`entry_loop.py`, `live.py`,
  `source_authority.py`); a distinct `withdrawn_fact_ids` mechanism exists
  in `packages/derivation/live.py` but is a different, unrelated concept
  (retired fact types in state projection, not a user-facing unattest
  action on a closure) and this inquiry does not extend a claim about it.

**Honest "not yet" path:** verified directly from State B (§5) — if the
user is not ready, or has not yet entered everything, no closure finding is
recorded, the family stays out of the closed set, and any rule requiring it
blocks with `SOURCE_SET_UNCLOSED` (or, one hop downstream, `DEPENDENCY_ABSENT`
citing the missing subtotal). This is a legitimate, expected, non-error
state, not a failure — the executed test run confirms the engine treats it
exactly this way.

---

## 8. Schedule B / OV-1 gate — decided: the trace materially reaches it

Chain, independently re-verified:

- `tax.us.2025.interest.b1-subtotal` is one of the seven `requires`/`pins`
  entries in `packages/content/tax/2025/rule.interest-positive-total.json`,
  which publishes `tax.us.2025.interest.positive-total`.
- `packages/content/tax/2025/rule.attachment.schedule-b.v4.json`'s
  `requirement` block: `"subtotals": ["tax.us.2025.interest.positive-total",
  "tax.us.2025.dividends.ordinary-total"]`, `"comparison":
  "strictly_greater_than"`, tested independently (not summed) against
  `tax.us.2025.parameter.schedule-b-threshold`.

So closing box 1 is one of seven inputs that must all be closed before
`interest.positive-total` can publish, and that subtotal is one of the two
values the committed Schedule B attachment decision tests. The chain is
material, not incidental: the declaration this inquiry traces sits directly
on the path to whether Schedule B attaches under the committed rule.

**Stated explicitly as counterfactual, never as current behavior:** the
committed `rule.attachment.schedule-b.v4` implements exactly one of the
IRS's Schedule B "Who Must File" triggers — the dollar threshold on
interest/dividend totals. The current-year IRS *Instructions for Schedule B
(Form 1040)*, "Who Must File" (`https://www.irs.gov/instructions/i1040sb`),
name additional, independent triggers not conditioned on that dollar
threshold — including a nominee distribution, an accrued-interest
adjustment, and a bond-premium (ABP) amortization adjustment, three
categories this product already models by name as separate, already-closed
source families in the same composition (visible in the
`rule.attachment.schedule-b.v4.json` itemization block). **If** a filer had,
for example, a small accrued-interest adjustment but total interest and
dividends under the dollar threshold, the IRS instructions would require
Schedule B to attach; the committed rule as written would not require it.
This is a counterfactual about IRS rule coverage, not a description of what
the committed rule currently does, and not an assumption about how it would
be fixed — no schema, rule-language, or engine change is proposed or implied
here. (This gap is the same one the CQ-1/CQ-2 milestone's actionable
register already records as `OV-1`, confirmed there as a tax-content
correctness gap and out of scope for implementation in this milestone; Track
0 is not re-litigating that resolution, only confirming the trace reaches
it.)

---

## 9. Distinguishing "complete" — six notions, kept separate

Per the milestone's framing, for this inquiry "done" means exactly: the
user asserts every Form 1099-INT box 1 statement item furnished to them for
2025 is recorded as of the current family-membership horizon. Nothing more.
Six adjacent notions this trace deliberately keeps distinct:

1. **document completeness** — a claim about the taxpayer's own paper; no
   artifact in this chain makes or supports it.
2. **source-family closure** — exactly what this declaration is (§1–§3).
3. **product tax-coverage completeness** — whether the product models a tax
   category at all; out of scope here.
4. **computation readiness** — whether line 2b's rule has all ten pins it
   needs; a system-side fact, not what the user is asked to assert (§3).
5. **return/filing readiness** — untouched by one family's closure.
6. **legal attestation** — the jurat/signature act at filing; this
   declaration is not that act, per `basis: "documentary"` in the one
   verified closure-finding-producing code path (§3) and per the family's
   own scope-limited `closure_claim` text (§1).

---

## 10. Data safety note for the standpoint agents

Everything above is drawn from committed synthetic repository content
(`packages/content/tax/2025/...`, `packages/sample_data/tax/scenarios/...`),
committed code, and public IRS instruction text
(`https://www.irs.gov/instructions/i1040sb`). No personal data, no real
run, no real value, no workspace-specific path beyond repository-relative
file paths already safe to publish. Dollar figures cited (`$10`) are from a
synthetic test fixture, not a real filer's data.
