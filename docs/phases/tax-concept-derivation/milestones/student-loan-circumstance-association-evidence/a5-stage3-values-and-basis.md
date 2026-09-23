# A5 stage 3 — tax-concept values and their basis

Provisional where it depends on stage 4. Filer-centered. No implementation. Every claim about
the engine below was traced in code at this commit; the level is stated where it matters.

## The question, narrowed

A tax-concept value can arrive three ways: a **direct answer** (the filer is asked it plainly),
**derived from circumstances** (a rule reaches it from ordinary tellings), or
**default-supported** (it takes a value because nothing adverse is supported). When two of
these produce the same value, can a reader of the record tell which it was?

**The consumer that needs the answer.** The bounded consumer from stage 2 does not: a
favourable eligible-student value computes the same interest however it arrived. What needs it
is the reader of *why* — A6's revealing consumer, which must show why a figure published, and
A0's F6 entry, which requires that a default-supported favourable value **carry** that basis
in its record. That is the consumer `a4-bounds.md` D15 recorded as unnamed; it is named here.

## What the engine records today

Traced, not assumed.

| How the value arrives | Record shape | What a reader of the record sees | Level |
| --- | --- | --- | --- |
| Direct answer | A kernel `finding.v2` with `basis` ∈ {documentary, attested, elective} and optional `capture` of what was presented and asserted | The finding itself and its basis | `read` — `finding.v2.schema.json` |
| Derived from circumstances | A `derived-finding.v2` published by a rule. Its pins name the rule, its citations, every `ref` it read, and **every collected finding it read**; each input pin carries `origin` | The rule and everything it read | `read` — `runner.pins_for`, `dependency_pins_for_access` |
| Default, through an `optional_default` binding | A `derived-finding.v2` with `resolved_input.origin: "declared_default"`, pinned to the default's parameter. Any rule reading it publishes with provenance `declared_default`, and pins to *that* finding carry `origin: "declared_default"` — **transitively** | `origin: "declared_default"` on every downstream input pin | `read` — `runner.py` binding setup, publication provenance, `_symbol_pin_entry` |

Two further facts matter below. `derived-finding.v2` has **no `basis` field** — `basis` exists
only on kernel findings. And the per-item pairing path stamps every input pin
`origin: "assertion"` unconditionally (`pairing_dispatch._input_pin`).

## Where the record already suffices — nothing added

**Direct answer against derived.** Different record shapes: a kernel finding with a basis, or a
derived finding naming a rule and what it read. Legal obligation asked plainly is the first; an
adverse eligible-student value reached from an adverse enrolment telling is the second. No
reader can confuse them, and nothing is added.

**A return-wide default against a stated value.** Where a fact has one instance per return and
its binding is `optional_default`, the default is marked at its source and the mark follows it
through every rule that reads it. Nothing is added.

**The plan's question about `basis`.** Whether `finding.v2`'s basis vocabulary suffices was
asked *only if* something must be carried. The answer is that `basis` is the wrong place rather
than an insufficient one: it grades how an **asserted** finding was grounded, and derived
values do not carry it at all. For what it does grade it is adequate here — every stage 2
circumstance and every financing claim is a telling, `attested`, or `documentary` where it comes
from a form. No extension.

## Where it does not — the case

**Test 3's combined total, walked through the record.** The filer said *nine credits at
Riverside* for autumn 2024 and nothing adverse. Stage 2 concluded the calculation proceeds on
F6's default, and the basis must say so. Build the favourable value the obvious way — a rule
reads the period's schooling circumstances and publishes favourable where none is adverse — and
the runner pins every circumstance it read, the nine-credit finding included, with
`origin: "assertion"`.

The record then reads: *favourable eligible-student, from the filer's nine-credit telling.*
That is the misreading A0 forbids. The value came from the default; the telling said nothing
about the § 25A(b)(3)(B) standard; and pins record what a rule **read**, not what **supported**
its value.

**Why the existing default mark cannot be used here.** Two independent reasons.

- `optional_default` substitutes a value **for a symbol that is unbound**. The runner publishes
  the default whenever the binding's symbol was not bound as an input
  (`runner.py`, `if symbol in self.symbols: continue`). The default this milestone needs is not
  that: it is *"no enumerated disqualifier is supported among the facts that are present"* — a
  conclusion about present facts, not a stand-in for an unbound symbol.
- It produces **one value per symbol**, not one per key. An earlier version of this section said
  a default never reaches keyed facts with several members. That was wrong: marshal leaves such
  a symbol unbound and puts the members in sources, so the default **still publishes** — one
  value for the symbol, sitting beside the members rather than applying to any of them. A
  default for *this* period while another period has an answer is still not something the
  mechanism expresses; it simply fails differently from how this section first described.

**A related behaviour, recorded rather than pursued.** Marshal also leaves a symbol unbound
when it is *not* a collect name and its current findings **disagree** — the Track 6b guard,
whose comment says the intent is that the runner then blocks with `DEPENDENCY_ABSENT`. On an
`optional_default` binding, the runner would instead publish the default. Whether any
production binding reaches that combination was not checked, and it is outside this milestone.
It is one more reason the rejected alternative below — every disqualifier an
`optional_default` fact — is not taken. `read`.

So the one mark the record has for default-supported cannot be produced for the value that
most needs it.

## Selected (provisional): a favourable value rests on a named conclusion

**The favourable value pins a separate, named conclusion — *no enumerated adverse circumstance
is supported for this subject* — and that conclusion is what pins the circumstances it
examined.** An adverse value pins the adverse circumstance directly.

Read in order, the record then says what happened:

> favourable eligible-student for the filer, autumn 2024
> ← *no enumerated adverse schooling circumstance is supported for the filer, autumn 2024*
> ← the circumstances examined, the nine-credit telling among them

**What this changes, stated exactly.** The nine-credit finding is still pinned, still as an
`assertion`-origin input — now an input to the absence conclusion rather than to the favourable
value. There is no pin role meaning "examined, not grounds", and this selection does not need
one: for a conclusion that nothing adverse is supported, everything examined **is** its grounds,
so the pin is true. What is false in the obvious build is the nine-credit finding pinned
directly as grounds for *eligible student*, and that is what the selection removes.

**The limit, which a reviewer found.** The distinction is carried by **what the pinned finding
is** — its symbol — and not by anything on the pin, which carries an id, a version, a role and an
origin. A reader who walks pins by origin alone sees an assertion two hops up and learns
nothing. A6's revealing consumer must dereference the finding a favourable value rests on and
report what it is. That is ordinary for a consumer whose job is to say why; it is stated so it is
not assumed.

**The subject's key is the one stage 2 selected for the value**, so the conclusion is per
subject rather than per statement: the student and the period for eligible-student; the
borrowing for use of proceeds and the *solely* test. Stage 2's derived-conclusions table has the
same shape on every row — adverse from a supported telling, favourable by default — so the
selection covers each constituent the bounded consumer evaluates, not only F6.

**Why this is the smallest.**

- **No schema change.** Both findings are ordinary derived findings. The distinction lives in
  *what the favourable value pins and what that thing is* — which provenance already carries,
  for a reader who follows the pin to the finding.
- **It makes the pairing path's hard-coded origin correct rather than wrong.** The named
  conclusion really is derived from assertions, so `origin: "assertion"` on a pin to it is true.
  Carrying the default in `origin` instead would make that hard-coding a mislabel by
  construction on any per-item path.

**Alternatives, and why not.**

| Alternative | Why not |
| --- | --- |
| Add a third `origin` value for "favourable because nothing adverse" | A schema and runner change to carry what a named conclusion already carries. `origin` is computed from a finding's inputs, not from which branch of a rule produced its value, so it would need new runner logic as well, and the pairing path would mislabel it |
| Add a `basis` to derived findings | `basis` grades an assertion's grounds. Putting a derivation's quality there conflates the two layers A0 separates |
| Leave it to presentation to infer from the value and the rule | A reader who sees a favourable value pinning the nine-credit finding cannot tell from the record whether that finding supported it. A0 requires the record to carry it, not a reader to reconstruct it |
| Make every disqualifier an `optional_default` fact defaulting to "not adverse" | Reintroduces the per-fact-type limit above, and substitutes a value for each unasked question — which is a claim about each one rather than the one true statement that nothing adverse was supported |

**What the selection depends on that nothing demonstrates.** Publishing one categorical
conclusion **per key of a single subject** — one per student-and-period, one per borrowing.
Categorical publication is `run` (D6, D16a), and per-item publication is `run` (D1, D13a), but
the per-item mechanism that has run publishes one finding **per pairing** — a pair of pinned
sides. A conclusion keyed on one subject is not a pairing, and a component having run is not
the behaviour having run. **Owed to A4's second pass**, and added to `a4-bounds.md`'s owed
table.

## The asymmetry the status key exposes

Stage 2 keyed eligible-student on the student and the period. An adverse value needs a period —
an adverse telling is *about* one. The favourable default needs none: where the filer described
no schooling at all, or no financing claim names a period, there is no period to key the
conclusion on, and A3 still says the consumer proceeds.

So the favourable value can arise where the status key has nothing to fill it. That is the
asymmetry A0 calls the milestone's central fact, showing up in the keying. **Not resolved
here.** Where no period is known, the default must attach to whatever scope *is* known — the
borrowing, or the statement under route (a) — and that is the applies-to and scope question
stage 4 owns.

## The financing claim's basis and the circumstance's

Stage 2 asked whether the pair's basis can differ from the basis of the circumstance it names.

**They are independent, and each record carries its own.** Both are tellings. A financing claim
may be documentary — a disbursement record naming the school and term — while the enrolment it
points at is attested, or the reverse; each finding says which.

**The three qualities do not combine across them.** A financing claim is never default-supported:
nothing defaults *"this loan paid for that"*, and without one there is no connection at all.
The circumstance it names can be absent, which is the normal case — period known, nothing
adverse said, favourable by default — and the named conclusion for that period pins the
financing claim that established the period and no adverse circumstance. The reverse, a
defaulted financing claim pointing at a stated enrolment, cannot occur. **No joint quality is
recorded. Nothing added.**

## Legal obligation — its key

**The incumbent** (`sli-scope.bundle.json`,
`tax.us.2025.sli-scope.legally-obligated-for-interest`): keyed on `tax-year` alone, supersession
`free`, "filer-level", no default, and a "no" is a definite zero for the whole return.

**What it is about.** 26 CFR § 1.221-1(b)(1): the taxpayer must have a legal obligation to make
interest payments **under the terms of the loan**. The subject is the borrowing.

**What the incumbent key does to a per-loan answer.** A1 poses *"Are you legally obligated to
pay this loan?"* — per loan. Under a tax-year key, two answers about two loans are two findings
for **one** fact, and currency treats a later finding for the same fact as a correction of the
earlier (`kernel/currency.compute_currency`). The second loan's answer displaces the first. It
is test 1's collision again — a different loan recorded as a correction of this one — and with
a "no" on one loan and a "yes" on another it resolves to whichever was said last. `read`.

**Selected:** the obligation fact's subject is the **borrowing**, not the tax year. A statement
remains a permissible population to apply an answer to, exactly as stage 2 left scope claims —
where only the statement is known, the answer is applied to what it reports, and whether that
application is keyed on the statement is stage 4's.

**Basis:** a direct answer, `attested`, with no default. That agrees with both the incumbent's
"no default" and A1, where "no" is material.

**Consumer: none in this milestone, and stage 2's boundary had a gap here.** Its table listed
what the bounded consumer evaluates and what is deferred, and obligation appeared in neither.
It is now in the deferred row, with the same limit as the rest: the consumer's output does not
establish that the filer was obligated on any loan. The incumbent is not changed.

**A consequence for A6, which is a team matter and follows from the selection.** The
demonstration must not pose obligation per loan through the incumbent fact, because that is the
silent displacement above. Posing it per loan requires a consumer keyed per loan; until one
exists, it is either posed return-wide as the incumbent does, or not posed.

## Correction reaching dependents — stage 2's open question

Whether a correction to a shared record reaching every dependent statement needs anything
carried on the record, or is entirely re-derivation.

**Re-derivation, and nothing is carried.** A correction is a new finding for the same fact;
currency displaces the old one; the next run marshals only current findings, and every conclusion
that pinned the old finding is reached again from the new one. The named conclusion above adds
nothing to this — it is re-derived like any other. `read`.

That answers what the record needs. It does not demonstrate that the reach actually happens
across several statements from one shared circumstance, which stays `a4-bounds.md`'s first owed
row and G2's to see.

## Handoff to stage 4

- Where a favourable default attaches when no period is known, and whether that scope is the
  borrowing or the statement.
- Whether a scope claim — including an obligation answer applied to a statement's contents — is
  keyed on the statement, and what a correction to it reaches (carried from stage 2).
- The responsibility applies-to relation, as the plan defines stage 4.

## Dependence on A4

| Depends on | Level |
| --- | --- |
| Direct and derived values distinguishable by record shape | `read` — schemas and `pins_for` |
| A return-wide default marked at source and transitively | `read` — runner. Five `optional_default` uses exist in the production package |
| A categorical conclusion published in the same run as amounts | `run` — D6, D16a |
| One categorical conclusion published per key of a single subject | **untested** — owed; see above |
| A correction reaching every statement from one shared record | **untested** — owed, `a4-bounds.md` first row |
