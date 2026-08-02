# Clean-room rival design — Dividend Composition (D3), iteration 2

Sealed rival (no incumbent material). Evidence: **Rung 1** paper schema/content
cases for D3-P2 and D3-P3; **Rung 2** throwaway probes only for P3 case 2
against committed validation/admission. No production edits. All values
synthetic (`demo-*`). D3-P1 is implement-normally substrate (ADR-0015 pattern).

## Claims

**D3-P2.** Form 1040 line **3b** (ordinary dividends) is the family subtotal of
box **1a** over the closed 1099-DIV ordinary family. The universe is **declared**
as composable boxes {1a, 1b} only; boxes **2a, 3, 5, 7, 12** ride each statement
as **recorded, non-composable** content. Box **2a** presence is a named
return-level signal for D2's contradiction check; other excluded boxes are
named-only recordings with no D2 linkage. Composition never sums them.

**D3-P3.** Line **3a** (qualified dividends) is the family subtotal of box **1b**.
Per-statement invariant **1b ≤ 1a** is **rejected at admission** (not recorded).
Line-level **3a ≤ 3b** holds **by construction** when both lines publish over
families whose members were admitted under that invariant (proof below). JSON
Schema cannot express the subset; probes confirm.

## Substrate (D3-P1, not re-bought)

- Entity kind `tax.us.1099div-statement` (logical furnished return; peer to
  evidence; no file/upload/scan keys — ADR-0015).
- Statement sameness: payer + tax year + payer_ref (ADR-0015 / committed
  `packages/tax/statements.py` pattern instantiated for DIV).
- Member transitions + horizons per ADR-0017/0023; contribution per ADR-0032.

## Proposed citizens (paper diffs only)

### Fact types (`bundle.v2` content)

1. **`tax.us.2025.f1099div.box1a-ordinary`** — number; `source_amount: true`;
   quantity pin dividends; keys: payer, statement (`tax.us.1099div-statement`),
   tax-year `"2025"`. Member of ordinary family.
2. **`tax.us.2025.f1099div.box1b-qualified`** — number; same keys; member of
   qualified family.
3. **`tax.us.2025.f1099div.recorded-boxes`** — **not** a family member.
   `value_schema` (shape only; no cross-field compare):

```json
{
  "type": "object",
  "properties": {
    "box_2a": {"type": ["number", "null"]},
    "box_3": {"type": ["number", "null"]},
    "box_5": {"type": ["number", "null"]},
    "box_7": {"type": ["number", "null"]},
    "box_12": {"type": ["number", "null"]}
  },
  "required": ["box_2a", "box_3", "box_5", "box_7", "box_12"],
  "additionalProperties": false
}
```

   Keys: same payer + statement + tax-year. Absent box → `null` (declared
   absence of that box on the statement, not a composable zero line).

### Families + closure (ADR-0014/0016/0017)

| Family id | Member fact | Authorizes subtotal | Closure claim (essence) |
| --- | --- | --- | --- |
| `tax.us.2025.f1099div.1a` | box1a-ordinary | `…dividends.ordinary-subtotal` | Every furnished 1099-DIV box **1a** for TY2025 is recorded. Covers 1a only — not 1b, not 2a/3/5/7/12, not line 3b completeness alone. |
| `tax.us.2025.f1099div.1b` | box1b-qualified | `…dividends.qualified-subtotal` | Every furnished 1099-DIV box **1b** for TY2025 is recorded. Covers 1b only. |

Horizon-keyed closure facts + `source-closure-mapping.v2` per family, same
admission as B1 (`current-literal-true`). Mappings pin exact family versions.

### Universe citizen (paper) — `dividend-universe.v1`

```text
schema: dividend-universe.v1
id: tax.us.2025.dividend-universe
composable: [box_1a → line 3b family, box_1b → line 3a family]
recorded_non_composable: [box_2a, box_3, box_5, box_7, box_12]
return_level_signals:
  box_2a: CAPITAL_GAIN_DISTRIBUTION_RECORDED  # D2 contradiction feed
  box_3|5|7|12: named recording only; no D2 linkage
forbidden: any rule collect / composition slot over recorded_non_composable
honesty: does not claim "all dividend income complete" beyond {1a,1b}
```

No multi-slot line-2b-style composition is required: each of 3a/3b is a
**single-family** subtotal + form-field bind (ADR-0016 decisions 4–5 apply as
"subtotal authorizes only its claim," not as interest multi-slot bijection).

### Rules + form fields (content shape)

- Subtotal 1a / 1b: `collect` + `round` over each family (mirror
  `rule.f1099int-b1-subtotal.json`).
- Line 3b rule: publishes ordinary-subtotal symbol when family 1a
  `require_closed`; binds form field `form1040.line-3b`.
- Line 3a rule: publishes qualified-subtotal when family 1b `require_closed`;
  binds `form1040.line-3a`.
- Citations: `citation.form1040.line-3a` / `line-3b`.
- Neither rule may `collect` recorded-boxes or name box_2a as input.

### Subset enforcement locus (P3) — **admission machinery**

**Locus:** tax-layer admission after committed per-finding `value_schema`
validation (`findings._validate_finding`), before state mutation — on every
path that admits a box1a or box1b finding (plain assertion *or*
member-transition). Contribution batches fail closed (ADR-0032
`validation-failed` terminal) when any successor raises.

**Check (paper semantics):** let S be the statement key of the finding. Read
current (or same-batch pending) values O = box1a for S, Q = box1b for S
(missing Q treated as “no qualified finding”; missing O when Q is present is
reject). Reject with `FindingModelError` / contribution failure if Q is present
and (O is absent or `Q > O`). Same-member value correction of O re-checks any
current Q for S; removing O while Q remains is reject (member-transition half).

**Why not schema-only:** Draft 2020-12 `value_schema` cannot compare two
fields or two findings (`$data` is SchemaError; constant `maximum` is not
relative to 1a). Probes below.

**Why not composition-only:** a design that records Q > O and “handles later”
is silent wrongness (foreclosure). Rejection must prevent the violating pair
from becoming current members.

**Why not both as primary:** composition may *re-assert* the invariant as a
defense-in-depth block, but the **named structural locus** is admission so
bad data never enters the lattice.

## Line-level subset proof (case 3)

Let admitted statements be S₁…Sₙ. For each i, either no Qᵢ finding, or
Oᵢ ≥ Qᵢ ≥ 0 (admission). Line 3b = Σ Oᵢ over current 1a members (closed);
line 3a = Σ Qⱼ over current 1b members (closed). Every Qⱼ is paired to an Oⱼ
on the same statement with Qⱼ ≤ Oⱼ; every unpaired O contributes ≥ 0 to 3b
only. Therefore Σ Q ≤ Σ O whenever both lines publish. **Q.E.D.**

**Divergence guard:** families have distinct horizons (ADR-0017). Members
cannot diverge into “Q without O” because admission forbids it. Horizons may
advance independently when only one box’s membership changes; that does not
break the sum inequality. If family 1b is open, 3a **blocks** (honest);
3b may still publish — subset is a relation on published values, not a
requirement that both lines always publish together. Undeclared / unadopted
family → both lines block when their rules `require_closed` fail (case 5).

## Cases

### 1 — Two positives

**(a)** Statement `demo-stmt-alpha` (payer `demo-payer-alpha`): 1a=900, 1b=600;
recorded-boxes all null. Close both families. → 3b=900, 3a=600; citations on
both form fields; 600 ≤ 900 visible from pins to the single statement pair.

**(b)** Add `demo-stmt-beta`: 1a=400, 1b=0; close. → 3b=1300, 3a=600. Beta
contributes ordinary only; Q=0 is admitted (0 ≤ 400).

### 2 — Subset kill-case (mandatory) — Rung 2

Attempt: `demo-stmt-kill` with 1a=100, 1b=250 in one contribution batch
(member-transitions for both + recorded-boxes).

- **Dies at admission** of the 1b finding (or batch validation), with
  `FindingModelError` / contribution `failed` — **before** either value is
  current if ordered so the check sees both; if 1b is presented without 1a,
  dies for absent ordinary. **Never** a current member pair with 1b > 1a.
- **Not** schema regex: probes show schema accepts the pair.

**Probes (throwaway; committed machinery only):**

| # | Setup | Result |
| --- | --- | --- |
| P1 | Independent `value_schema: {type:number}` validates 200 and 100 separately | Accepts — no subset |
| P2 | Object schema `{box_1a, box_1b}` numbers, required both | Accepts `{100, 200}` |
| P3 | `maximum` const 100 on box_1b | Rejects 200 even when 1a=500 — not field-relative |
| P4 | `maximum: {$data: "1/box_1a"}` | **SchemaError** under Draft 2020-12 |
| P5 | `findings._validate_finding` | Per-fact `value_schema` only; no cross-finding compare |

**Conclusion:** structural rejection requires the admission extension above;
schema-only is unrepresentable.

### 3 — Line-level by construction

Under case 1(b) members, 3a=600 ≤ 3b=1300. No sequence of evaluations can
publish 3a > 3b without a member violating admission (proof). Guard: see
Divergence guard. Order independence: 3a rule does not read 3b symbol; 3b does
not read 3a — pure sums over own collects.

### 4 — Out-of-universe box 2a (mandatory)

Statement `demo-stmt-cg`: 1a=500, 1b=200, recorded `box_2a=75`, others null.

1. Contribution admits (1b ≤ 1a; recorded-boxes is not a family member).
2. 3a=200, 3b=500 publish (2a not in any collect).
3. **Return-level walk:** a return disposition (D2 consumer, not designed here)
   reads current `recorded-boxes` findings; any with `box_2a ≠ null` yields
   named disposition **`CAPITAL_GAIN_DISTRIBUTION_RECORDED`** (statement id +
   finding id pins). D2’s contradiction check consumes that disposition
   against a no-capital-gains declaration → hard error if contradicted.
4. **Contrast box 7:** same statement with `box_7=12` (foreign tax): recorded;
   named recording only; **no** `CAPITAL_GAIN_DISTRIBUTION_RECORDED`; no D2
   linkage. Lines still publish.

### 5 — Empty family

- Both families closed-empty (literal-true closures, no members) →
  ordinary-subtotal=0, qualified-subtotal=0 → 3a=3b=0 **publish**
  (ADR-0014 empty collect + closure).
- Family **undeclared** / not adopted / never closed → `require_closed` fails →
  both lines **block** (`SOURCE_SET_UNCLOSED` / open dependency), never silent
  zero.

### 6 — Universe creep (mandatory)

Composing box 2a into 3a or 3b is **unrepresentable**:

- No family `member_predicate` names recorded-boxes or a box_2a amount type.
- Universe citizen `forbidden` list; package validation (Track 1) rejects a
  rule whose `collect` name is not some adopted family’s member fact type, or
  whose inputs include recorded-non-composable symbols.
- A hand-edited rule summing 2a has no authorized subtotal symbol and no
  form-field bind under the declared universe — not an untested path, an
  illegal citizen graph.

## Producer → authority → consumer → failure map

| Prop | Producer | Authority | Consumer | Failure |
| --- | --- | --- | --- | --- |
| P2 | Contribution of 1a + recorded-boxes | Family 1a claim + universe citizen + closure mapping | 3b rule / form field; D2 reads box_2a signal | Open family blocks 3b; 2a never sums; undeclared family blocks |
| P3 | Contribution of 1b with paired 1a | Admission subset check + family 1b claim | 3a rule / form field | 1b>1a or 1b without 1a → admission reject; open 1b blocks 3a |

## Production conditions (named for Track 1–2; not implemented here)

1. Bundle + families + mappings + rules + form fields + universe citizen.
2. Admission subset check in tax/contribution path (P3 locus).
3. Package validation: collects ⊆ family member fact types; no
   recorded-non-composable in line rules.
4. Goldens: cases 1–2, 4–5 from authoritative fact log (milestone Verification).

## Explicit non-claims

Schedule B (D1), QDCG worksheet (D2) — only box_2a **visibility**. Line-9
growth is Tier-1 content. Interest universe (ADR-0026) untouched. No new
standing-affecting edge.
