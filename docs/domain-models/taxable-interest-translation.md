# Taxable Interest Translation

A working model, maintained by agents. It is not a contract, not an ontology,
and not a deliverable anyone should grade for completeness. Its job is to make
the translation legible — to the owner, and to the next agent who has to decide
where a fact belongs. Edit it freely. Delete parts that stop earning their
space.

---

## Part 1 — The simple account

### The life circumstance

You bought a bond partway through its interest period. Bonds pay interest in
chunks, on fixed dates. If you buy one in the middle, the seller has already
"earned" part of the next payment, so you pay them for it as part of the
purchase. Then the next payment date arrives and the issuer pays the **whole**
period's interest to you, because you now own the bond.

At year end the payer sends you a Form 1099-INT reporting the whole payment.
That form is correct. It is also not your income. You are holding some of that
money on behalf of the person you bought from, and you already paid them for
it.

Two true statements, one number apart. The product's job is to hold both, and
to be able to say why they differ.

### What the document contributes

The Form 1099-INT contributes **an attributed report**: *this payer said this
statement paid this much*. That is all. It is true regardless of your tax
position, and nothing downstream may rewrite it.

It cannot contribute the circumstance. No box on any 1099-INT asks whether you
bought mid-period. The payer does not know and is not required to find out.

### What the person contributes

An **ordinary fact about a purchase**: *I bought this bond on this date, and I
paid the seller this much for interest that had already built up.*

This is the load-bearing design commitment of the whole milestone. The person
supplies what they did. They do not supply what it means for their taxes. The
question "did you buy a bond partway through an interest period?" is answerable
by someone who has never heard of Schedule B. The question "do you have any
accrued-interest adjustments?" is not — it asks the user to have already done
the classification the product exists to do.

### What law and convention contribute

Three different kinds of support, and the difference matters:

- **Statute** (IRC § 61(a)(4)) puts interest in gross income. It is the
  default that something has to displace.
- **A form instruction** (Instructions for Schedule B, line 1) tells you to
  report *all* your taxable interest on line 1, says the accrued interest "is
  taxable to the seller," and tells you to subtract it and label the
  subtraction "Accrued Interest." Operationally that settles the **income**
  question: if you must report all your taxable interest and then subtract
  this, this is not your taxable interest.
- **A publication** (Pub. 550, *Bonds Sold Between Interest Dates*) is what
  explains *why*: the payment is a return of your capital, not income, and it
  reduces your basis in the bond.

Notice what is missing. There is no regulation directly on point for the
ordinary buyer. The nearest one (Treas. Reg. § 1.61-7(d)) addresses the
**seller**. The next nearest (§ 1.61-7(c)) is a **different transaction** — a
bond in default bought at a discount, "traded flat" — that reaches the same
words by a different route. A model that flattens "statute," "instruction,"
"publication," and "adjacent regulation" into one undifferentiated "authority"
has thrown away real information.

### What the application does

It translates. Concretely:

1. It takes the payer's report as a report, keeping it intact.
2. It takes the person's ordinary account of their purchase as an ordinary
   fact, keeping it separate.
3. It works out that both concern **the same bond**.
4. It applies an adopted rule that says what the law makes of that pairing.
5. It puts the resulting number on the return, and can show its work.

Step 3 is the one the product does not currently have any way to do, and it is
the reason this milestone exists.

### What reaches the return

The includible amount reaches Form 1040 line 2b through the existing Schedule B
path. The full reported amount still appears on Schedule B line 1; the accrued
portion is subtracted below it and labelled.

### What the application cannot yet do

Honestly, and in the user's terms:

- It cannot carry the basis reduction into the year you sell the bond. It
  knows the reduction happened; nothing consumes it later.
- It does not handle savings-bond education exclusions, bonds bought at a
  discount, bond premium, tax-exempt bonds, bonds held for someone else, or
  bonds in default. These are neighbours, not gaps — different rules, not
  unwritten code.
- It cannot cite a Treasury Regulation at all; the citation vocabulary has no
  family for one.
- It cannot read a trade confirmation. The person tells it what happened.

---

## Part 2 — The frontier

Enough of the surrounding territory to locate the slice honestly. Most of this
is deliberately *not* implemented; it is here so that we can tell the
difference between "outside the slice" and "forgotten."

### The referents

| Referent | What it is | In the slice? |
| --- | --- | --- |
| **Taxpayer** | The return subject | Yes — exists today as scope |
| **Obligation** | The bond itself. Persists across years, survives the statement | **Yes — new** |
| **Acquisition** | One purchase of an obligation on a date, with an accrued component | **Yes — new** |
| **Reported item** | One payer's report of one statement's box-1 amount | Yes — exists today |
| **Payer / broker** | Who reports | Exists today, only as issuer |
| **Tax authority** | Statute, regulation, publication, instruction | Partial — no regulation family |
| **Classification** | What the law makes of the pairing | **Yes — new, rule-owned** |
| **Includible amount** | The current-year income conclusion | Yes — derived |
| **Basis consequence** | The other half of the same conclusion | Recorded, **not consumed** |
| **Disposition** | The later sale or redemption | No — deferred |
| **Return projection** | Schedule B, line 2b | Yes — exists today |
| **Explanation** | What a reader can recover | Yes — this milestone raises it |
| **Refusal** | What the product says when it cannot conclude | Yes |
| **Professional handoff** | "Ask a CPA about this" | No — named only |

### The strata

The same subject matter appears at five levels. They are related, not
identical, and collapsing any adjacent pair is the characteristic failure.

| Stratum | Subject | Authored by | Example |
| --- | --- | --- | --- |
| **Document model** | A form | The payer | "Box 1 of statement S is 1200" |
| **Ordinary interaction** | A life event | The person, prompted | "I bought it on 15 May and paid 300 accrued" |
| **Canonical workspace** | The world | The workspace | "Obligation B; acquisition A of B on 15 May with accrued 300; reported item R of B" |
| **Tax derivation** | The law's verdict | An adopted rule | "900 includible; 300 not includible, reduces basis in B" |
| **Return presentation** | A form line | The projection | "Line 2b = 900" |

The document model and the ordinary interaction are both **input projections**.
Neither is canonical. The canonical layer is source-independent precisely so
that a fact learned from a document and a fact learned from a person can be
about the same thing.

### Where the product refuses, and why refusal is a feature

Four distinct silences, which today are one silence:

| Situation | What the product should say |
| --- | --- |
| Report present, purchase question never asked | "I need to ask you something about this bond" |
| Purchase confirmed, amount not supplied | "How much did you pay the seller for accrued interest?" |
| Purchase supplied, no report matches it | "You told me about this bond; I have no 1099 for it" |
| Purchase supplied, several reports could match | "Which of these does this purchase concern?" |

The incumbent collapses all four into "the Schedule B accrued-interest class is
not closed." It blocks — which is correct, and better than guessing — but it
cannot say which of the four it is in, so it cannot help.

### Neighbours, named so we can decline them honestly

Savings-bond education exclusion (§ 135) · original issue discount · market
discount · bond premium amortization · nominee ownership · tax-exempt interest
· bonds traded flat (§ 1.61-7(c)) · previously-reported interest · joint-return
subject identity · state conformity.

Each is a *different rule*, not a missing feature. The product should be able
to recognise it is near one and say so.

---

## Part 3 — The canonical slice

This is the part that becomes code. Everything above is orientation.

### The five propositions, restated as canonical facts

The prior milestone separated the propositions
(`docs/milestones/reported-interest-tax-concept/accrued-interest-item-model.md`).
This milestone assigns each to a stratum and an owner.

| | Proposition | Stratum | Author | Canonical? |
| --- | --- | --- | --- | --- |
| P1 | Statement S reports 1200 in box 1 | document | payer | reported item |
| P2 | On 2025-05-15 I bought B and paid 300 accrued | ordinary | person | acquisition |
| P3 | The accrued part is not the buyer's income; it reduces basis | derivation | **rule** | derived |
| P4 | Disclose it on Schedule B this way | presentation | instruction | projection |
| P5 | Line 2b is 900 | presentation | projection | projection |

The single most important cell in that table is **P3's author**. Today, the
person supplies P3's output as an input. That is the defect.

### What must be true of the canonical layer

1. **Identity is the obligation, not the form row.** Two bonds under one payer
   are two obligations. Today they are one aggregate.
2. **The report and the purchase name the same obligation.** Otherwise nothing
   connects them and any pairing is an accident of arithmetic.
3. **Association is checked, not assumed.** Exactly one match is a
   translation; zero or several is a question for the user.
4. **Corrections are independent.** Correcting the payer's report must not
   rewrite what the person said, and vice versa.
5. **The rule owns the classification.** The ordinary input must never contain
   the words "accrued interest adjustment."

### Semantic cases T1–T9

Every candidate shape must express all nine honestly. Amounts are synthetic.

Common fixture: subject `demo.subject.filer-1`, tax year 2025, payer
`demo.payer.harbor-bank`, statement `demo.stmt.1099int.harbor-2025-a` reporting
1200 in box 1, obligation `demo.obligation.orchard-note-2031`, acquisition
`demo.acq.orchard-2025-05-15` with accrued 300.

| Case | Document input | Ordinary input | Required observation |
| --- | --- | --- | --- |
| **T1** fully includible | box-1 1200 | no acquisition applies | 1200 includible, and the *reason* is recorded, not assumed |
| **T2** accrued treatment | box-1 1200 | acquisition, accrued 300 | report still 1200; 900 includible; 300 basis consequence |
| **T3** missing answer | box-1 1200 | acquisition confirmed, amount absent | names the missing ordinary question; no default |
| **T4** fact without report | none matching | acquisition, accrued 300 | fact stays understandable; nothing invented on the return |
| **T5** ambiguous association | two reported items for the obligation | one acquisition | refuses; identifies the ambiguity |
| **T6** document correction | corrected to 1000 | unchanged | conclusion moves to 700; ordinary fact untouched |
| **T7** circumstance correction | unchanged 1200 | corrected to 250 | conclusion moves to 950; report untouched |
| **T8** identity discriminator | two obligations, one payer | facts concern one | the *right* item is affected |
| **T9** unsupported neighbour | box-3 savings bond | education expenses | describes what it cannot translate; claims no coverage |

T5 and T8 are the discriminating pair. They are the two cases the incumbent
cannot express at all, and the two that force canonical identity to be real
rather than decorative.

---

## Part 4 — What the engine can and cannot do today

Read from the committed artifacts and code, not from prior prose.

### Cheaper than expected

**Entity kinds cost nothing.** `entity.v1` already contemplates "a
counterparty, an **account**, a property." Entity kinds are free-form strings
validated by a naming pattern; there is no registry to extend. `tax.us.obligation`
and `tax.us.obligation-acquisition` need no schema change. The prior
milestone's "the modelled domain is a domain of documents" is a finding about
*content*, not about the kernel.

**Object-valued canonical members already exist in production.** The Form
1099-B wash-sale work established the pattern: one rich object-valued fact type
keyed on real identity components, carrying declarative per-member constraints,
plus thin scalar families that project single numbers out for aggregation
(`projects_from`). The accrued-interest acquisition fits this shape exactly.

**Per-member derived findings already exist.** Family validation publishes one
finding per member, pinned to that member's own fact, so a per-item conclusion
is displaced by a correction to that item.

**Cross-family identity matching already exists.** ADR-0066 decision 4 declares
identity components that bind to fact-id keys or member fields, and the runner
compares them across families.

### The genuine constraint

**The expression language cannot join or iterate.** `marshal.py` builds a flat,
unkeyed symbol table: one fact type, one symbol, one value. A rule's `ref`
reads a scalar. Multi-member fact types reach a rule only as an aggregate
(`collect`) or a universal witness. ADR-0066 decision 2 states it directly for
the member-predicate grammar: no iteration, no cross-member read.

So the engine **cannot compute per item**. Line 2b is, and remains,
Σ(reported) − Σ(accrued).

This is less limiting than it first looks, and being precise about why is worth
the paragraph. The item-level requirement in T5 and T8 is not an *arithmetic*
requirement — the sums are the same either way. It is an **association**
requirement: before the subtraction is legitimate, each accrued fact must be
shown to concern exactly one reported item. That is a check performed over
declared identity components, which is exactly the shape of machinery ADR-0066
already built — only with the opposite polarity.

`identity_exclusivity` asserts *these must not match*. The canonical slice
needs *this must match exactly one*.

### The one thing that has to be added

An additive successor family declaration carrying an **association**
requirement alongside the existing exclusivity one: for each member of this
family, the declared identity components must resolve against the counterpart
family's current members exactly once. Zero matches and several matches are
distinct, named, blocking dispositions.

Everything else in the slice is content: new entity kinds, new fact types, a
new family, a new rule, new citations, and a projection into the existing
line-2b path.

---

## Part 5 — Open questions

Held here rather than pretended away.

1. **Does the basis consequence need a durable home this year?** It is
   derived and recorded. Nothing consumes it until a disposition exists.
   Deferred deliberately; a later-year consumer should test a canonical model,
   not decide whether one should exist.
2. **What is the ordinary input surface actually made of?** This milestone
   defines a structured projection and a plain-language rendering of the
   answer. It does not build an interface, and free-text interpretation is out
   of scope.
3. **Pub. 550's basis language is inherited, not re-verified.** The Schedule B
   line-1 instruction text was confirmed verbatim during this milestone and
   supports the current-year income conclusion. Pub. 550's body could not be
   retrieved through available tooling; the heading's existence in the 2025
   publication was confirmed. Since the basis half is recorded but not
   consumed, nothing load-bearing this year rests on the unverified half —
   but a later-year milestone must verify it before relying on it.
4. **The citation vocabulary still has no Treasury Regulation family.** It
   costs corroboration here, not the citation itself. It will bite on any
   proposition whose best support is regulatory.
