# Track 3 — Curated Inquiry, Register Update, and Owner Options (CQ-2)

Audience: Product, Shared (exploratory record). Status: **exploratory,
non-authoritative.** This document curates Tracks 0–2 of the CQ-2 milestone
into a single account a cold reader can follow without the four upstream
packets open. It creates no product contract, adopts no definition, and
changes no code, schema, rule, or ADR. It does not select a winning
two-sentence answer, does not implement `OV-1`, and does not select or
charter the next milestone.

Inputs curated: `cq2-track-0-inquiry-frame.md` (Track 0, the verified trace),
`cq2-track-1-casual-reader.md` (Account 1, Claude), `cq2-track-1-system-
provenance-grok.md` (Account 2, Grok, run via `mcp__grok__grok_consult`),
`cq2-track-2-explanation-tree.md` (Track 2, the disposition tree and CQ-1
delta). Every claim below is attributed to the section of the packet that
carries it; nothing here is re-derived from source code independently — that
independent re-derivation is Track 0's job and is cited, not repeated.

**Evidence classes**, held throughout, exactly as Track 2 defined them:
**executed** (a committed test run's actual assertions), **static-read**
(code read but not run for this trace), **content** (committed artifact
text, quoted or closely paraphrased), **inference** (a conclusion drawn by
pattern or analogy, not directly observed), **gap** (no committed evidence
found either way).

---

## 1. The situation this inquiry examines

A filer has entered their Form 1099-INT box 1 statement items into the
product and is presented with an affordance asking them to assert —
"declare," "confirm," "say I'm done" — that this one family (box 1 of every
1099-INT they received) is complete. No dollar total on Form 1040 line 2b
has been finalized yet; this is the request that precedes a result, not a
result itself (Track 0 §6).

> **This request affordance is proposed and hypothetical, not committed
> behavior — labeled explicitly 2026-08-19.** No committed code path in
> this repository produces a Form 1099-INT box-1 closure finding, and no
> committed interface asks this question. The one closure-producing path
> that exists (`packages/derivation/entry_loop.py`) is for W-2, not box 1
> (Track 0 §4, V10). The *fact type, family declaration, and closure
> mapping* are committed and were read directly; the *asking of the
> question, its wording, and its controls* are a construct of this inquiry.
> Everything below distinguishes the two, and no statement about the
> affordance's behavior should be read as a statement about shipped
> behavior.

CQ-1 (closed) examined a **system-presented result** — a published number
and its support chain. CQ-2 examines a **system request for a user
declaration**, holding the same tax domain constant (the Form 1099-INT box 1
source family feeding Form 1040 line 2b) so the two inquiries could be
compared on interaction type rather than domain (Track 0 §0 framing; milestone
plan "Experimental design").

The declaration itself, verified independently by Track 0 against committed
content (**content**, quoted verbatim): the fact type
`tax.us.2025.f1099int.b1.source-closure` asserts "every furnished 1099-INT
box-1 statement item is recorded as of that horizon," scoped explicitly to
"box 1 only — never other boxes, non-form interest, or Form 1040 line 2b."
Its invalidator, **as stated in the fact type's own title prose**: "a later
membership transition displaces this closure through horizon succession;
re-attestation on the successor horizon is required" (Track 0 §1). **This
prose is not a complete account of the committed invalidators** — the same
citizen's `supersession` field establishes a second one. See §5, and §14
for why the packets missed it.

---

## 2. Why it has to be the user, not the software

Two true reasons answer different halves of this question, and only one of
them appears in the packet's own plain answer (Track 2 D2, §4.2):

- **The mailbox reason (content, repeated by Account 1):** the software
  cannot check the user's mailbox for statements it has never seen. This
  answers why undocumented interest cannot self-report.
- **The forbidden-inference reason (static-read, Account 2 Attack 6,
  independently re-verified by Track 2 directly against
  `resolve_closure_admissions`'s own docstring):** the engine does not
  merely lack the ability to infer completeness from items already entered
  — it is structurally forbidden to. There is no code branch anywhere that
  computes this boolean from the entered items or their running subtotal.
  This answers a different, sharper question the mailbox story does not
  touch: why entering everything you hold still isn't enough by itself.

Track 2's disposition (§4.2): **both are true and the packet's plain answer
states only the first, which makes it incomplete, not false.** This is
resolvable by explanation — stating both reasons together requires no
product or engine change — and is not treated as a standing tension.

---

## 3. What saying yes actually does — executed

**State A, executed** (Track 0 §5, cross-checked against the committed
golden fixture at
`packages/sample_data/tax/scenarios/unclosed_interest_composition/`): a
current, literal-`True` closure finding for the box-1 family produces a
published `tax.us.2025.interest.b1-subtotal` of `"10"` in the golden report.
Saying yes admits exactly one symbol into the set any rule may require
closed. In Track 0's own words: "nothing downstream of line 2b becomes any
less blocked by this alone." Form 1040 line 2b itself needs all ten of its
required source-family subtotals closed, of which `b1-subtotal` is one
(Track 0 §3).

**What yes does not get you (executed + content, Track 0 §5, §7, §9):**
does not publish, compute, or change line 2b; does not mean the return is
complete; is not the same as signing (`basis: "documentary"` in the one
observed closure-finding-producing code path — a different family, W-2, not
this one — and the family's own scope-limited `closure_claim` text).

---

## 4. The honest "not yet" path — executed

**State B, executed** (Track 0 §5): the same scenario leaves a different
required family, `tax.us.2025.non-form-interest`, without a closure finding.
This produces exactly and only: a block on that family's own subtotal rule
(`SOURCE_SET_UNCLOSED`), a block on line 2b under a *different* code
(`DEPENDENCY_ABSENT`, naming the missing subtotal, not the family — because
the evaluator reaches the missing-pin reference before line 2b's own
closure check), and four further downstream lines each blocked on yet
another missing symbol, none of them the unclosed family. No error, no
crash, no silent zero — `stop_reason: "saturated"`. Already-admitted
families (box 1 included, in this scenario) remain published unaffected.

**This is exactly and only executed for `non-form-interest`, not box 1.**
The admission mechanism is the same code path for every adopted mapping
(static-read, §2 above), so the cascade *shape* is treated as verified
generically; **substituting box 1 as the unclosed family is inference by
analogy, not a second executed run.** Both Track 1 accounts made this
substitution when describing "if I don't declare box 1"; Track 2 flags this
explicitly and does not upgrade it (Track 2 D6). This document does not
upgrade it either.

**"No" is representable in the record and collapsed at admission
(static-read, re-verified directly in code 2026-08-19; supersedes this
document's original "no representable 'no'" claim, which conflated two
layers).** The earlier formulation read `resolve_closure_admissions`'s
docstring — "false, absent, displaced, truthy-non-boolean, or duplicate
closure findings leave the family out of the closed set" — as a statement
about the system. It is a statement about *one function's return value*.
The layers differ:

- **Record layer, with currency information — the five lifecycle histories
  *may* be distinguishable.** The closure fact type declares
  `"value_schema": {"type": "boolean"}`
  (`packages/content/tax/2025/f1099int.bundle.json`), so `false` is
  schema-valid, not a degenerate encoding of absence. A recorded `false`
  finding is a distinct, attributable record entity with its own finding id,
  basis, and evidence; absence is the absence of any such entity. Currency
  adds the ordering: `packages/kernel/currency.py::compute_currency`
  retains displaced findings in `displaced_finding_ids` with a
  `DisplacementReason` naming `kind="correction"` or the withdrawal or
  supersession root. So the record plus its currency view **carries the
  material from which absent, `false`, `true`, corrected, and
  horizon-superseded could be told apart.** Stated as capability, not as a
  delivered feature: no committed consumer for this family reads that
  material, and this document does not claim any consumer presents it.
- **Closure-authority projection — current `false` is distinguishable from
  absence; the history is not preserved.** `marshal_closure_authority`
  (`packages/derivation/marshal.py` lines 172-195) selects current findings
  by fact type, then reads the horizon identity key the mapping names —
  requiring it, and raising `SourceAuthorityError` if it is absent — and
  copies the recorded value through unchanged. It never filters on value,
  and it does **not** compare the horizon it reads against the family's
  current horizon; that comparison happens downstream, in
  `resolve_closure_admissions`. So a *current* `false` becomes a
  `ClosureFindingRecord` carrying `value=False`, whereas absence produces no
  record at all. **That distinction survives this hop.** What does not
  survive is everything else: the projection is built from
  `currency.current_finding_ids` only, so a `true` that was corrected to
  `false` and a `false` that was the user's first and only answer arrive
  identically, with no trace of which they were. **This layer distinguishes
  current-`false` from absence. It does not preserve the five lifecycle
  histories.**
- **Admission layer — and only here — the distinction is destroyed.**
  `resolve_closure_admissions` (`packages/derivation/source_authority.py`
  lines 141–156) reaches the same outcome through three `continue`
  statements, two of which each fold two distinct situations together: no
  current horizon for the family; a candidate count other than exactly one,
  which merges absence with duplicate authority; and a candidate whose value
  is not the boolean `True`, which merges an explicit `false` with a
  truthy-non-boolean. Its return type is `dict[str, ClosureAdmission]`,
  and non-admission is expressed as *key absence*. A dict with no key cannot
  carry a reason. **The collapse is a property of this function's return
  shape, not of the engine's model of the user's answer.**

**Why this correction matters rather than being pedantry.** The original
wording implied that a recorded `false` and no finding at all are equivalent
throughout the record — that the record itself cannot tell them apart. That is
false: the fact schema already permits a recorded boolean `false`, and a
current `false` already survives the projection as a distinct value from
absence. What is lost, and lost only at the admission hop, is the *reason for
non-admission* at the point where a downstream `collect` blocks.

**What this correction does not establish about any eventual fix.** That the
record and projection already distinguish `false` from absence says nothing
about whether the semantics this milestone leaves unsettled — what a `false`
should *mean*, and to whom, at which point — can be delivered without any
further record change. A settled semantics could turn out to need a distinct
fact type, an additional field, or another record-level construct; nothing
here rules that out. This section establishes only what the current record
and projection already carry, not what a future decision would require them
to carry.

**What this does not establish.** That a recorded `false` has been assigned
any product meaning. Nothing committed says whether a `false` means "not
done," a refusal, a withdrawal, a correction of a mistake, or a placeholder;
nothing committed distinguishes an initial `false` from a `true` corrected
to `false`; and no interface exists that would let a user record either.
Structural representability is not settled semantics, and this section
establishes only the former. Which distinctions *should* be carried, and
what each state should mean, is the unsettled `SC-13` decision.

**A precedent exists elsewhere in the architecture, and its significance is
bounded.** `ADR-0055` gave the attachment path
`COMPLETENESS_VALUE_VIOLATION`, described in
`packages/derivation/runner.py` as "a required answer present as a current
finding but valued other than its declared required value — distinct from
absence (`DEPENDENCY_ABSENT`), never folded into it, never silence." This
establishes exactly one thing: **the architecture is capable of carrying an
absence-versus-present distinction through to a blocking site, because it
already does so on another path.** It establishes nothing about the closure
path. It does not show that the closure collapse is local, small, cheap, or
architecturally similar; the two paths differ in their inputs, their
consumers, and what a caller does with the result, and none of that was
examined here. **No implementation shape for a closure-side fix is inferred
or implied, and this track proposes none.** What the precedent does is
change the *question*: from "can the architecture hold this distinction at
all?" (demonstrably yes, somewhere) to "should the closure path carry the
reason for non-admission, and at what cost?" — which is an owner decision
requiring its own scoping work.

- **Interface layer — nothing exists to examine.** No committed code path
  produces a Form 1099-INT box-1 closure finding at all (§1, Track 0 §4
  V10), so there is no box-1 interface, no control, and no copy. Every
  statement about what a user would see is hypothetical.

Track 2's §4.3 disposition is **corrected, not merely restated**: it
recorded the collapse as a settled limit of runtime capability ("not
representable, and this is settled, not ambiguous"). The record layer
contradicts that.

The interface consequence is also narrower than originally written, and
narrower than an earlier draft of this repair stated. **No claim is made
here about what a hypothetical "No, I'm not done" control would write, or
what it would mean.** No such control exists, none is proposed, and what a
product act of that kind should record — an initial `false`, a correction of
an earlier `true`, a refusal, a withdrawal, or something needing its own
fact entirely — is exactly the unsettled `SC-13` question. What *can* be
said without deciding it is a statement about the code, not about the
control: **on today's code, a current recorded `false` and no finding at all
produce the same non-admitted outcome, and that outcome carries no reason to
the blocking site.** So copy claiming that a recorded "no" is distinguished
*from silence at that site* is unsupported by anything committed. That is the
whole of the consequence. It says nothing about what any control would
write — a control that wrote a current literal `true` would produce
admission, and a control implemented as a distinct act, a different fact
type, or a horizon change has no established behavior on this path at all.

---

## 5. How a recorded closure ceases to be admitted

**Corrected 2026-08-19; wording tightened at publication 2026-08-20.** This
section originally stated that horizon succession is *the only* committed
invalidator. That is wrong, and the error mattered: it made the closure look
unrevisable **by construction of the record**, when the record in fact
permits a second transition.

**Terminology in this section is deliberately structural.** "Supersede,"
"correct," and "cease to be admitted" describe what committed code does to a
recorded value. They do not name a user act and do not assign one a meaning.
Whether a later `false` would constitute withdrawal, refusal, retraction,
"not done," or something else is exactly the unsettled `SC-13` decision, and
nothing in this section decides it.

**At least two committed invalidators exist, and they are independent:**

1. **Horizon succession** (Track 0 §1, §7) — a membership transition
   displaces the closure by moving the family's current horizon, so the
   finding keyed on the superseded horizon no longer matches
   `current_horizons` in `resolve_closure_admissions`. System-triggered,
   not a user act.
2. **Same-fact correction on the same horizon** — re-verified in code. The
   fact type declares `"supersession": {"policy": "free"}`
   (`packages/content/tax/2025/f1099int.bundle.json`), and `free` is the
   one policy in `packages/kernel/findings.py` (lines 560–580) that permits
   correction unconditionally: `locked` raises, and
   `closed-on-attestation` gates. A later finding for the same `fact_id`
   then displaces the earlier one as a *correction* root in
   `packages/kernel/currency.py::_finding_corrections`. **A recorded `true`
   can therefore be superseded by a recorded `false` on the same horizon**,
   after which the family is no longer admitted. Note the precise
   mechanism: `_finding_corrections` tracks `latest_by_fact` by **insertion
   order over `state.findings`**, not by timestamp — "later" means
   later-recorded, and nothing in this path consults a clock.

**What remains a genuine gap — narrower than originally stated.** No
committed *user-facing* withdraw/un-declare action exists anywhere Track 0
searched (`entry_loop.py`, `live.py`, `source_authority.py`);
`withdrawn_fact_ids` in `live.py` is confirmed, independently for this
packet, to be a distinct mechanism — retired fact types in state
projection, not a user-initiated unattest action on a closure finding. The
supersession-by-correction path above is a *structural transition the record
permits and that nothing committed invokes, surfaces, or names for this
family*, which is a different and materially weaker claim than "no
invalidator but horizon succession." It is weaker in both directions: it
does not establish an impossibility, and it does not establish a feature.

**Track 2's disposition (§4.4) named this a "product gap, not an explanation
gap."** That framing is preserved as Track 2's own conclusion, but it is not
adopted here without qualification, because it implicitly classifies what an
eventual fix would require — that better copy about an existing mechanism
could not close it — and that classification is not established by anything
in this section. What *is* established, and is the narrower claim this
section actually supports: no committed mechanism currently exists for a
user-facing withdraw or un-declare action on this family, at any layer. Which
layer or layers a fix would need to touch, whether copy describing the
absence honestly would itself resolve the gap Track 2 was pointing at, and
what "closing" this gap would even mean before `SC-13`'s semantics are
settled, are none of them decided here:

- **What is established, structurally.** The fact schema permits a recorded
  boolean `false`. A later same-fact `false` can supersede an earlier `true`
  under `free` supersession. A resulting current `false` survives the
  closure-authority projection as a `ClosureFindingRecord` with
  `value=False`. That current `false` then produces non-admission, and the
  admission result loses the reason for it.
- **What is not established.** That any of this has been assigned the
  product meaning "not done," refusal, withdrawal, or retraction. No
  interface and no committed product act exists for this family, so no
  committed artifact assigns the transition a user-facing meaning at all.
- **What therefore remains open.** The product semantics of absence, an
  initial `false`, a correction to `false`, withdrawal, and horizon
  succession are all unsettled. A `true → false` transition has an
  operational consequence — the family stops being admitted. Whether that
  consequence *is* "taking the declaration back" is the `SC-13` decision,
  not a finding of this milestone.

So the gap is between an available structural transition and an absent
product surface *and* an unassigned product meaning — not between a wish and
an impossibility, and not between a decided meaning and a missing button.

This narrows what the honest explanation may say. The original phrasing —
"I don't know, and neither does the codebase, whether a horizon succession
is ever signalled to you, or what happens if you were wrong without one" —
remains correct on the *signalling* half. On the second half it is partly
overstated and partly still true: the record can carry a corrective `false`,
so the *structural* question "can a later value displace the earlier one" is
answerable; the *product* question "what happens if you were wrong" is not,
because nothing committed says what that recorded `false` would mean or how
a user would reach it.

**What this does not license.** It does not follow that a withdrawal
feature would be built on the correction path, that it would be small, or
that its shape is known. Correction is one structural transition the record
permits; a withdrawal could equally be modelled as a distinct act, a member
transition, a new horizon, or its own fact type, and **nothing committed
chooses among these, because nothing committed implements any of them.**
Nor does it follow that a corrective `false` *should* mean withdrawal — that
is the decision, not an input to it. The gap remains a product decision, and
the decision still has to settle what withdrawal *means* before it can
settle what it looks like. What the correction changes is only this: the
decision starts from a record whose schema and supersession policy do not
foreclose a later `false`, rather than from one that had been shown — wrongly
— to forbid it. No fix shape, locality, or cost follows.

---

## 6. The convergence

Two model families, opposite standpoints, no contact with each other, given
the same single packet (Track 0), **independently selected the same
paragraph of §5 State B as their deepest thread**: that a block caused by a
missing declaration reaches the lines a user actually looks at under a
*different code naming a different missing symbol*, so the declaration that
would fix it is named nowhere the user is looking.

- Account 1 (Claude, casual-invested-reader standpoint): this thread moved
  its answer from an unqualified "we'll clearly tell you why" to a guarded
  claim that stops short of promising the explanation will always point
  back to what was forgotten.
- Account 2 (Grok, system-and-provenance-adversary standpoint, model id not
  pinned by the MCP transport but confirmed not to be Claude): the same
  thread produced "the ask is well-founded as a knowledge gap. It is not
  well-founded as a description of its own runtime."

**What this is evidence for:** that the finding is packet-grounded rather
than a model artifact of either account's own standpoint — two lenses
constructed to notice different things, given nothing but the trace, landed
on the same load-bearing paragraph. That was the explicit methodological
purpose of running Account 2 externally, and it returned a positive result.

**What this is not evidence for:** generality beyond this one packet, this
one artifact set, or this one interaction type; agreement between the
accounts on anything else (see §7 below, where they diverge sharply); or
any claim about how real, non-simulated users would respond — both accounts
are explicitly non-authoritative simulated readings, not user research.

Both accounts also converged, without contact, on two further points: that
the absent withdrawal path is a real termination point rather than a minor
detail, and that the unobserved `basis` value for this specific family is a
genuine gap rather than something safe to infer from the W-2 pattern.

---

## 7. The dispositioned divergence

**Account 2 attacked the packet's own plain answer; Account 1 reproduced it
without noticing tension**, despite having read the same executed State A.
The phrase at issue, from Track 0's own two-sentence plain answer: "...it
needs you to say so before it can use this piece in your return."

- **Account 1** treated this as a fair gloss of admission.
- **Account 2 (Attack 1)** named it *the* misrepresentation: State A is
  executed and shows line 2b unmoved by a successful box-1 `True`; "use
  this piece in your return" is what a person hearing "say you're done"
  will take the click to mean, and the executed consequence does not match
  that expectation.

**Track 2's disposition (§4.1), carried forward here without flattening:**
the phrase is **defective as user-facing copy and defensible as an
engineering gloss, and the ambiguity between those two readings is itself
the defect** — not a reason to withhold a verdict, and not a hedge between
the two poles. "This piece" is technically accurate at the mechanism level
(it can refer to the box-1 subtotal specifically, and that is exactly and
only what a `True` admits). But nothing in the sentence, or in what a user
sees at the moment of clicking "yes," disambiguates "this piece" (the
subtotal, which does change) from "your return" (line 2b, which usually
does not change from this one click alone). Both readings are grammatically
available; the two accounts picked different ones by standpoint, not by
different evidence. This is why Account 1 reproduced the phrase without
tension and Account 2 attacked it — it is the same underlying fact
producing two defensible readings.

**What would settle it further, per Track 2, and was not run for this
packet:** an executed scenario in which box 1 is the *last* of the ten
required families closed (so saying yes does move line 2b), paired with one
in which it is not the last (so it does not) — showing a user both outcomes
from the identical action would settle whether the ambiguity is tolerable
or must be resolved by rewording. That test was not performed here and is
not proposed as an action beyond naming it; no copy is adopted or shipped
by this track.

A further divergence, recorded without disposition because the evidence
does not settle it: **only Account 2 found the yes/no/silence collapse**
(§4 above); **only Account 2 challenged the mailbox explanation** as
incomplete (§2 above) — Account 1 accepted it and built its answer on it;
**only Account 1 reported the packet's own opening technical sections as
unreadable** to a non-expert, then correctly discarded that as having no
user-facing action, since no taxpayer reads those sections. Track 2's own
reading of this split: the casual-reader standpoint absorbed the packet's
framing where the adversarial standpoint attacked it — evidence about the
method itself (a lens that stands where the user stands also inherits what
the user is told), not only about the artifact. This document does not
resolve that methodological observation; it is preserved as reported.

---

## 8. Schedule B / OV-1 — the trace reaches it, substance untouched

Chain, independently re-verified by Track 0 (§8), not re-litigated here:
`b1-subtotal` is one of seven inputs to `interest.positive-total`, which is
one of two subtotals the committed Schedule B attachment rule
(`rule.attachment.schedule-b.v4.json`) tests independently (not summed)
against a dollar threshold. The chain from this declaration to whether
Schedule B attaches under the committed rule is material, not incidental.

Stated, exactly as Track 0 stated it, as counterfactual and never as current
behavior: the current-year IRS *Instructions for Schedule B (Form 1040)*
name additional independent triggers not conditioned on the dollar
threshold — including accrued interest, a bond-premium (ABP) amortization
adjustment, and a nominee distribution — three categories the product
already models by name as separate, already-closed source families in the
same composition. A synthetic filer with a small accrued-interest
adjustment and total interest under the threshold would be required to
attach Schedule B under the IRS instructions; the committed rule as written
would not require it.

**This is `OV-1`, already confirmed by an earlier repair pass in this phase
as a tax-content correctness gap and an owner decision, not new content
here.** CQ-2's independent trace, entered from a different angle (a
declaration request rather than a published result), reaches the same gate.
No fix shape is inferred, and no schema, rule-language, or engine change is
proposed here — the register entry (§10 below) is annotated to record that
a second, independently-run inquiry reached it, and nothing more.

---

## 9. Cross-inquiry delta against CQ-1

Curated from Track 2 §5, which read CQ-1's closed tree (six branches, 16
tensions, four lenses) directly and did not re-derive it.

**Repeated (same branch, substantially unchanged):** the filing-effect
boundary (nothing here is signed or has legal effect; the jurat is later
and distinct); the agency/voice attribution question (a declaration's
speaker is the user, not the system — CQ-2 sharpens this from a wording
concern into a code-verified mechanism claim: the engine structurally
cannot derive the boolean from any other fact); generic blocked-state
messaging (the same fixed `explain` string CQ-1 found is still live in v5,
independently re-confirmed here); the six/five notions of "complete" (CQ-1
named five, CQ-2 carries all five forward and adds legal attestation as a
sixth).

**Changed (same branch, sharper evidence or a shifted terminus):** CQ-1's
retrospective "who supplied this number" becomes CQ-2's prospective "why
does it have to be me" — terminating at an executed/static-read code fact
(no inference branch exists) rather than doctrine alone; CQ-1's
retrospective "does this word imply a jurat" becomes CQ-2's prospective
"can I take this specific action back" — terminating at a genuine mechanism
gap (§5 above) rather than a wording gap; CQ-1's "which family is missing"
finding becomes CQ-2's executed cascade (§4 above) — not only is the text
generic, the block *code itself* changes one hop upstream, evidence CQ-1's
fully-closed fixture could not produce.

**Absent (CQ-1 had it; a request does not raise it):** the arithmetic and
citation-drilling branches (a boolean request has no computed value to
reconcile or drill into); the page-wide staleness and tax-law-classification
branches (no rendered, versioned document exists yet at the point of a
request).

**New (only a request raises this):** the forbidden-inference distinction
(§2 above — a number already computed and shown raises no "why not compute
it yourself" question); the yes/no/silence collapse (§4 above — CQ-1 never
examined a binary user choice); the asymmetric legibility of acting versus
not acting (§4 above — CQ-1's gap was about *which* family is missing in a
static blocked state, not about comparing two possible user actions); the
horizon-membership-not-shown gap (§3, D3 sub-node in Track 2 — CQ-1's
fixture was already closed, so there was no open horizon to show).

---

## 10. Register update

Applied to `docs/phases/claim-boundary-exploration/actionable-considerations.md`
under that register's own admission rule (a consideration is admitted only
if it names both a concrete question/limitation and at least one plausible
user or product action) and consolidation rule (merge, split, remove,
preserve disagreement, promote nothing automatically).

**`CQ-2` closed, with the gap between worded and worked question stated
plainly.** The register's `CQ-2` text reads "Why are you asking me this?"
— a general class of questions about relevance, spanning legal necessity,
computational dependency, product preference, and mere relevance for
requests of any kind. What this milestone actually ran is the sharper "Why
are you asking me to say I'm done?" — one specific instance: a
computational-dependency-gated declaration request for one source family.
That sharper question is answered end to end, verified and executed (§1–§5
above). **The broader CQ-2 class is only partly entered.** This inquiry
tested computational dependency and optionality (§2, §4) thoroughly, and
authority/speaker attribution (§1, §5) substantially; it did not test a
request motivated by product preference alone, or a request for information
not gated by any source-closure mechanism at all — those remain untested
instances of the general class.

**Three new entries admitted** (each names a plausible product action per
the register's own rule). **The first two were consolidated into one on
2026-08-19; the original pair is described here, then the consolidation.**

- The **yes/no/silence collapse** (Track 2 §4.3, static-read) — admitted on
  the premise that no "no" was representable. **Premise false; see §4.**
- The **absent withdrawal path** (Track 2 §4.4, gap, both Track 1 accounts
  converged independently) — admitted on the premise that horizon
  succession was the only invalidator. **Premise false; see §5.** The
  *product* gap survives the correction; the reason it survives does not.
- **Consolidated result — `SC-13`, declaration lifecycle.** With both
  premises corrected, these are one question because they are governed by
  one unsettled semantics, not because they share an implementation. **The
  earlier claim that a "not done" control and a withdrawal path "write the
  same corrective `false` to the same fact" is withdrawn** — that is one
  available product design, not an established consequence, and asserting
  it pre-empted the decision it was offered as a reason for. A withdrawal
  could equally be modelled as a distinct act, a member-transition, a new
  horizon, or a fact type of its own; nothing committed settles this,
  because nothing committed implements any of it. What genuinely joins the
  two is that both require answering the same prior question: **what do
  absence, an explicit `false`, a correction, and a horizon succession each
  *mean* as declaration states — and which of them must be visible to whom,
  at which layer.** Interface actions are selected after that, not before.
  Plausible action: settle those semantics as one decision; then decide
  separately whether non-admission carries its reason to the blocking site,
  whether to offer an explicit "not done" control, and whether to offer a
  withdrawal path.
- The **horizon membership not shown at the moment of the ask** (Track 2
  D3 sub-node, gap — no committed UI or executed box-1 closure act exists
  to check either way) — plausible action: evaluate showing the family's
  current-horizon membership set to the user before asking them to attest
  to it, since the proposition is keyed to a horizon's membership, not to
  "everything in your mailbox."

**One new entry admitted for the dispositioned divergence itself** (§7
above): the ambiguity in "before it can use this piece in your return" —
plausible action: reword to disambiguate subtotal-admission from
return-level effect, or run the box-1-last-vs-not-last executed pair Track
2 names as the test that would settle it further. This is distinct in
evidence and remedy from the existing voice-attribution entries (`SC-9`,
`SC-12`, which concern misattributed agency, not scope ambiguity), so it is
added rather than folded into them, per the consolidation rule's split
criterion.

**One candidate considered and not admitted:** the incompleteness of the
"mailbox" reason alone (§2 above). Track 2 dispositioned this as
*resolvable by explanation* — stating both true reasons together requires
no further owner decision, no product change, and no future action beyond
what this document's own §2 already does. It does not name a *further*
plausible action distinct from what has already been done; admitting it
would create an entry whose only remaining content is "say the thing this
document already said." Per the charter's explicit instruction, listing a
candidate is not by itself grounds for admission.

**`SC-3`, `SC-8`, `SC-9`, `SC-12` annotated, not restated as new.** CQ-2
re-confirmed each of these on a second, structurally different interaction
type (a request rather than a result):

- `SC-3` (generic blocked-message text) — re-confirmed live in form-field
  v5 (Track 0 §3), and CQ-2's executed State B (§4 above) is materially
  sharper evidence than CQ-1 produced: not only does the rendered text stay
  generic, the block *code itself* changes one hop upstream
  (`SOURCE_SET_UNCLOSED` becomes `DEPENDENCY_ABSENT`), and the cascade
  touches four further, unrelated-looking lines. This is new information
  about how the same defect manifests differently by interaction type, not
  a re-derivation of the original finding.
- `SC-8` (the `attested` ordinary-English/kernel-reserved-vocabulary
  collision) — re-confirmed still live in v5 (Track 0 §3); CQ-2 adds that
  this matters more acutely at a declaration request, because the ask is
  the exact moment "attest" is made into a user act (Account 2 Attack 5),
  sharpening why the collision is not merely cosmetic.
- `SC-9` / `SC-12` (voice/authorship, misattributed agency) — CQ-2's D2
  (§2 above) independently re-confirms the underlying doctrine
  (ADR-0009) with a stronger, code-verified basis (no inference branch
  exists anywhere) rather than restating the wording concern CQ-1 raised.

**`OV-1` untouched as to substance; annotated only.** Its register row
records that CQ-2's own independent trace, entered from a declaration
request rather than a published result, reaches the same Schedule B
attachment gate (§8 above). Status, evidence, and owner-decision posture
are unchanged; no fix shape is inferred here or by this annotation.

The full edited register is committed at
`docs/phases/claim-boundary-exploration/actionable-considerations.md`.

---

## 11. Exit-criteria assessment

Assessed individually against the plan's `#Exit criteria` section. An
honest partial is preferred to a generous full, per this track's charter.

**How to read this section.** The texts of criteria 1, 2, and 3 were
**strengthened during the 2026-08-19 repair**, after the tracks had run. Each
of those three entries below therefore states two things separately:

- **Final criterion** — the text as it now stands in the plan's
  `#Exit criteria` section. This is what the grade is assessed against.
- **Criterion as it stood during execution** — the text Track 0 and Track 2
  actually worked under. This is recorded only to explain how an overly
  permissive grade arose. **The final text did not govern, and could not have
  governed, Track 0: it did not exist until the repair.** Track 0 is not
  faulted for failing a rule written afterward. What the original wording
  *did* do was permit a true-but-partial account to be graded met, which is
  why it was replaced.

Criteria 4–7 were not changed; their single stated text is both the
execution-time and the final text. The grades below are the final grades:
**four met, three partially met.**

---

**Criterion 1 — final:** *"every claim in 'Verified concrete witness' has
been independently re-verified by Track 0 against committed artifacts and
runtime behavior (not merely cited from this plan), **each verification
naming the exact artifact surface read, the sibling fields present and not
relied on, and the consumers of the same artifact**."*

**Criterion 1 as it stood during execution:** *"every claim in 'Verified
concrete witness' has been independently re-verified by Track 0 against
committed artifacts and runtime behavior (not merely cited from this
plan)."* The clause requiring the artifact surface, sibling fields, and
consumers to be named was added by the repair, precisely because its absence
is what let row V2 pass.

**Grade: partially met.** **Regraded 2026-08-19**; the original grade of
"met" is withdrawn. The reason for the downgrade does not depend on the
strengthened wording: **Track 0 did not correctly verify every material
witness claim, and the correction came from outside the milestone
afterward.** That failure is assessable against the original text too — a
claim verified against the wrong proposition is not "independently
re-verified" — which is why the regrade stands rather than being an artifact
of moving the goalposts.

Row **V2** ("Invalidator is horizon succession requiring re-attestation")
is graded **Confirmed** on the evidence "Same title text, final sentence,
quoted in §1." That evidence establishes what the fact type's *title says*.
It does not establish what the fact type's *invalidators are* — the same
object's `supersession` field was not read, and it carries a second one
(§5). Track 0 §7 then converted the unverified half into a stronger claim
still: "This is the only staleness/withdrawal mechanism found in committed
code or content." A row can be honestly marked Confirmed against the wrong
proposition, and that is what happened here.

What remains true of this criterion: the other nine rows were independently
re-derived from the cited artifact or code rather than cited from the plan,
which is what the criterion was chiefly guarding against, and V10 carried a
scope clarification Track 0 raised on its own initiative (the one committed
closure-finding-producing code path is for W-2, not box 1). The failure is
not that Track 0 copied the plan — it did not — but that one material claim
was verified against a narrower artifact surface than the claim's scope,
and the verification table gave no place to record that.

---

**Criterion 2 — final:** *"the declaration request has an explicit account of
proposition, speaker, basis, scope, effect, non-effect, **every**
invalidator, and at least one unsupported neighboring inference."*

**Criterion 2 as it stood during execution:** identical except that
"invalidator" was **singular and unquantified** — *"...effect, non-effect,
invalidator, and at least one unsupported neighboring inference."* A single
named invalidator satisfied it on its face, which is how an account naming
one of two passed.

**Grade: partially met.** **Regraded 2026-08-19.** Seven of the eight
elements are stated explicitly and labeled by
name in Track 0 §7, including a labeled "Non-effect (unsupported
neighboring inference)" section stating that declaring box 1 closed does
not support "my taxable interest is final" or "my return is ready to file."
The eighth, **invalidator, was stated incompletely**: it named horizon
succession alone, omitting same-fact correction under `free` supersession
(§5 above). The element is present and the omission is now repaired, but
the criterion asked for an explicit account of the invalidator and the
account given was not complete at the time the criterion was first called
met.

---

**Criterion 3 — final:** *"an honest 'not yet' path exists, grounded in the
engine's actual `blocked` behavior, and the withdrawal/staleness account
states **every** verified invalidator — horizon succession and same-fact
correction under `free` supersession — with the places a further mechanism
could live named and checked, and nothing invented."*

**Criterion 3 as it stood during execution:** *"an honest 'not yet' path
exists, grounded in the engine's actual `blocked` behavior, and the
withdrawal/staleness mechanism is stated **from the verified
horizon-succession behavior**, not invented."* The original text **named
horizon succession as the thing to state**, so an account stating only
horizon succession satisfied it by construction. That is the clearest case
in this milestone of a criterion encoding the very error it was meant to
catch, and it is why the final text enumerates both mechanisms and requires
the search for further ones to be named and checked.

**Grade: partially met.** **Regraded 2026-08-19**, carrying two
qualifications rather than one.
The "not yet" path is executed (Track 0 §5 State B) and treats the blocked
state as non-error, non-crash, non-silent-zero — that half is met. The
staleness half is **not** fully met as originally graded. The mechanism was
stated exactly as the fact type's own *title text* describes it (horizon
succession) and nothing was invented — but the fact type's title text is
not the whole of the committed behavior, and taking it as such produced an
incomplete finding. The same fact type's `supersession` field and the
kernel's correction path establish a second invalidator that the packet did
not state (§5 above). Deriving the invalidator account from the content
citizen's prose while leaving an adjacent field of the same citizen unread
is the specific method error, and it is worth naming because it is
repeatable. The packet remains correct that no user-facing withdraw action
was invented or found. The second qualification, the original scope note:
the executed State B scenario
demonstrates the mechanism using `non-form-interest`, not box 1; the box-1
instance is inference by analogy from the same code path, not a second
executed run (§4 above). The generic mechanism (which family, executed
generically per §2's static-read of the one dispatch path) satisfies the
criterion; a reader should not conclude the box-1-specific cascade was
itself executed.

---

**Criterion 4 (unchanged by the repair; execution-time text and final text
are the same) — "committed behavior and any OV-1 counterfactual are kept
explicitly and visibly separate throughout, with the counterfactual included
only if Track 0 finds the trace materially reaches it."** **Met.** Track 0 §8 states the
material chain, decides the trace reaches the gate, and states the seven
omitted IRS triggers explicitly as counterfactual, never as current system
behavior — repeated verbatim in this document's §8 with the same framing
maintained.

**Criterion 5 (unchanged) — "a cross-inquiry delta against CQ-1 names,
specifically, which explanatory branches repeat, change, are absent, and are
new."** **Met.**
Track 2 §5 names specific branches in each of the four categories with
citations; this document's §9 curates the same four categories without
adding or dropping any.

**Criterion 6 (unchanged) — "the actionable register is updated with a
consolidated, actionable result and no automatic implementation scope is
created."** **Met.** §10
above updates the register: closes `CQ-2` with an honest gap statement,
admits four new entries each tied to a plausible action and a cited packet
section, annotates four existing entries with new evidence rather than
restating findings, leaves `OV-1` untouched as to substance, and declines
one candidate the charter listed, with reasoning given rather than silent
omission. No entry proposes a schema, rule-language, or engine change as
adopted; every "plausible action" is framed as evaluate/decide/test, not
build.

**Criterion 7 (unchanged) — "the owner has enough evidence to choose
cross-inquiry reduction, another contrasting inquiry, a bounded
build/decision milestone, or a stop."** **Met.** §13 below lays out what the evidence in hand supports for
each of the four options, without selecting one.

**Overall, regraded 2026-08-19: four of seven met, three partially met.**
Criteria 1, 2, and 3 are downgraded, all for the same root cause: the
invalidator was verified against the fact type's title prose alone and then
stated as exhaustive, when the same object's `supersession` field carries a
second invalidator (§5). Criterion 1 fails on the verification itself,
criterion 2 on the completeness of the resulting account, and criterion 3
on the staleness half of its requirement. Criterion 3 additionally carries
its original scope note (generic mechanism executed; box-1-specific cascade
is inference by analogy).

The original grade of seven-of-seven was wrong, and *how* it was wrong is
the useful part: no criterion was called met on fabricated evidence. Each
was called met on real, correctly cited evidence that was **incomplete in a
way the grading had no way to test**. The grading checked that each
required element was present and sourced; it did not check whether the
cited artifact surface was wide enough to support the element's claim. A
criterion reading "states the invalidator" is satisfiable by a
true-but-partial answer, and was so satisfied here. That is a defect in how
the criteria were written as much as in how they were graded. The owner
should read the four remaining "met" grades as *not independently
re-verified against the same standard* — they were graded by the same
method that missed this, and only the three named criteria were re-examined
in the repair.

**On the strengthened texts, stated plainly so the record is auditable.**
Criteria 1, 2, and 3 were rewritten *after* the tracks ran, and both texts
are recorded above for each. This creates an obvious hazard — grading past
work against a rule written afterward — and the milestone does not do that:

- The three downgrades are justified against the **execution-time** texts as
  well. A claim verified against the wrong proposition was never
  "independently re-verified" (1); an account naming one of two invalidators
  was never a complete "explicit account" of the request (2); and a
  staleness account that omits a committed mechanism was never a complete
  statement of how the closure goes stale (3). The strengthened texts make
  the failures *legible*; they do not create them.
- Criterion 3 is the honest edge case and is named as such: its
  execution-time text pointed at horizon succession **by name**, so Track 0
  satisfied its letter. The downgrade there rests on the criterion's purpose
  rather than its letter — an "honest 'not yet' path" that omits a committed
  way the answer stops holding is not honest — and a reader who judges that
  too generous to the repair should read criterion 3 as *met on its original
  text and partial on its purpose*. The final grade keeps it partial.
- **Track 0 is not faulted for the strengthened wording.** It could not have
  worked to a text that did not exist. What is recorded against Track 0 is
  the completeness failure itself, which the repair then wrote into the
  criteria so the next inquiry cannot repeat it.

This reconciliation changed no grade. The record stands at **four met, three
partially met**.

---

## 12. Generality assessment

**A reusable explanatory structure does appear to be emerging, but at the
level of method, not yet confirmed at the level of content — and two data
points on the same tax domain is thin evidence for either.**

What repeats structurally across CQ-1 and CQ-2, per §9's delta: the
evidence-class discipline itself (executed / static-read / content /
inference / gap); the practice of building a request- or value-rooted tree
that terminates at verified artifact, code, or explicit gap rather than
assertion; the practice of running two independent standpoint accounts on
one packet and dispositioning their agreement and disagreement rather than
picking a winner; and the practice of closing with a named delta against
the prior inquiry rather than a standalone report. All four of these held
up on a second, structurally different interaction type (a request instead
of a result) without needing to be redesigned. That is method-level
evidence for reusability, and it is real.

What does **not** yet confirm content-level generality: both inquiries
examined the same tax domain (the Form 1099-INT box 1 family feeding Form
1040 line 2b), the same package version family, and the same underlying
computation mechanism (source-closure gating via `require_closed`). Several
of CQ-2's "repeated" branches (§9) are repeated in part *because* they sit
on the same gating mechanism CQ-1 already examined from the result side —
the generic blocked-message finding, for instance, is the same artifact
(`form1040.line-2b.form-field.v5.json`) read twice, not independent
evidence that a *different* artifact would show the same pattern. The
four-way convergence Track 2's cross-inquiry delta documents is real and
should not be understated — but it is convergence within one tax domain
examined from two interaction types, not convergence across domains.

**What a third inquiry would and would not do — corrected 2026-08-19.**
This section originally described a third inquiry on a different tax domain
as what "would confirm" generality. That overstates what a third data point
can deliver. **A third inquiry on a materially different tax domain would
test _transfer_ — whether the structure carries to one further case — and
would not settle generality.** Three points on a deliberately chosen
contrast set is still a small, non-random sample of the product's
interaction space, and a success would license "this transferred once,"
not "this is general." Generality is not the kind of claim this method
reaches by accumulating inquiries; it would require either an argument from
the artifact model itself about why the structure must hold, or coverage
broad enough to be non-anecdotal. Neither is in prospect.

**What a transfer test would look like:** a third inquiry on a domain not
gated by the same source-closure mechanism at all (for example, a
rate/bracket computation, an eligibility test, or a filing-status
determination with no `require_closed` dependency), examined with the same
evidence-class discipline and two-account convergence method, producing a
structurally analogous tree (comparable root type, comparable spread of
terminus classes) without the method being redesigned.

**What would refute transfer:** that same third inquiry requiring a
wholesale restructuring of the branch taxonomy, or the two-account
convergence producing no shared deepest thread, or the evidence-class
discipline proving unable to characterize the new domain's artifacts
cleanly. Note the asymmetry, which is the practical point: **refutation is
decisive where confirmation is not.** One clean failure establishes that
the structure is domain-specific; one clean success establishes only that
it survived a second domain. That asymmetry is a reason to run such an
inquiry if the owner's actual question is "is this method load-bearing
enough to invest in," and a reason not to run it expecting a general
result.

This document does not treat Track 2's four-way delta as settling the
question either way, and does not recommend treating two same-domain
inquiries as sufficient grounds for declaring a general theory — consistent
with the milestone plan's own statement that completion "does not establish
a general theory of declaration requests, user attestation, or claim
integrity across the product."

---

## 13. Owner options

Four options, per the milestone plan's own framing. A recommendation is
offered; it is not a selection, and no option below is chartered.

**Cross-inquiry reduction.** Distill the method-level structure that
repeated across CQ-1 and CQ-2 (§12) — evidence-class discipline, the
standpoint-convergence method, the delta-against-prior-inquiry closing
practice — into a lighter-weight, reusable instrument that does not require
a full four-track cycle each time. Evidence supports this: the method has
now proven itself twice without redesign, and two full cycles is enough to
extract a stable shape. What it does not resolve: whether the *content*
findings (the branch taxonomy) generalize, since a reduction distills what
exists rather than testing new ground.

**Another contrasting inquiry.** The register (§10; also `CQ-3`, `CQ-4`,
`CQ-5` rows) still names untested interaction types. `CQ-3` ("why can't I
see a result?") already has the strongest evidentiary basis of the
remaining candidates via `SC-3`'s four-way convergence, but the register's
own prior repair pass recommended against running it as a full inquiry,
since it would deepen an already-established local defect rather than test
new ground. `CQ-5` ("what are you asking me to agree to?") is a genuinely
different question type — assertion/adoption responsibility rather than
relevance — and this milestone reached its boundary (the closure-vs-jurat
distinction, §5 above) without fully entering it; it is also the strongest
candidate for a **transfer test** *if* paired with a different tax domain,
per §12 — which would establish that the structure carried to one further
case, not that it is general.

**A bounded build or decision milestone.** Several register entries no
longer need further exploration to be decided or built: `SC-3`'s
four-way-converged (now five-way, with CQ-2's sharper cascade evidence)
generic-blocked-message finding; the declaration-lifecycle question that
the 2026-08-19 repair consolidated from the former `SC-13` and `SC-15`
(§10); and `OV-1` itself, which is confirmed and has been an owner decision
since the prior repair pass. Evidence supports this option, and the repair
**better specified** the lifecycle question without making it smaller: the
corrected layer analysis (§4, §5) replaced a false premise — that the record
forbids a recorded "no" — with an accurate structural account, so the
decision now starts from a correct description of what the record permits
and collapses at each layer rather than from a claim of impossibility.
**This is not a claim that the work is small, that its shape is known, or
that any structural transition has been assigned a product meaning** — the
decision must settle what absence, an initial `false`, a correction to
`false`, withdrawal, and horizon succession each mean as declaration states
before any interface or engine action can be selected, and that scoping has
not been done. The repair improved the *inputs* to that decision; it did not
make any part of it.

**A stop.** Two full inquiry cycles (CQ-1, CQ-2) now exist, each closed
with an honest accounting of what was and was not established, a repeatable
method, and a register carrying multiple decision-ready items. An owner
could reasonably judge that further exploratory value from this phase is
declining relative to the decision and build work already unlocked, and
move directly to that work rather than continuing exploration.

**Recommendation, re-assessed 2026-08-19 and unchanged in direction but
better grounded: a bounded build or decision milestone, over the other
three.** The register holds several findings — `SC-3`'s reconfirmed and
sharpened cascade-message gap, the consolidated declaration-lifecycle
question (`SC-13`), and `OV-1` — that are resolvable only by a product
decision or a content-authoring change, not by further explanation or
further inquiry. Running a third exploratory inquiry would add more
inquiry-shaped evidence to a register that already has more
decision-shaped evidence than it has converted into decisions.

The repair pass adds a second argument for the same conclusion, and the
owner should weigh it separately from the backlog argument. Both errors
survived four tracks and a full exit-criteria grading, and were caught by
the owner reading fields adjacent to the ones the packets cited. **Stated
at the width the evidence supports (§14.1): this is not a case of two
models independently converging on a wrong conclusion.** Neither error was
present in both standpoint accounts: the casual-reader account asserts
neither. **Corrected 2026-08-20** — an earlier version of this paragraph said
the external account isolated the representability question and left it open.
It did both: its §4 files the question as a terminus while its Attack 3
asserts an answer, and the disposition track then closed that answer as
settled. The demonstrated blind spot is narrower and more
specific: **a cited static read did not extend to the adjacent fields of
the cited artifact, nor to the consumers whose behavior the claim depended
on**, and nothing in the method required it to.

That is a recording gap, not a reason to distrust the standpoint accounts.
It is addressable by the §14.3 safeguard — a completeness/neighborhood
check on every load-bearing artifact claim — which costs a paragraph per
claim rather than a cycle.

This recommendation remains weighed, not dictated. A third inquiry into a
materially different tax domain is the only path that would test transfer
of §12's structure — and it would test transfer, not settle generality. If
that question matters more to the owner than clearing the decision
backlog, a contrasting inquiry is defensible, and should carry the §14.3
safeguard from its first charter. The owner selects.

---

## 14. What this track found wrong in the prior packets

**Superseded twice: first on 2026-08-19 by the owner-directed repair, then
again the same day when that repair's own reconciliation claim proved
unsupported.** The history is left visible because the second correction is
about how corrections overreach.

This section originally read: "Nothing in Track 0, either Track 1 account,
or Track 2 required a substantive correction during curation." That was
wrong. The first repair replaced it with the claim that two substantive
errors "were common to all four packets." **That was also wrong, and it was
wrong in the direction a repair is most tempted to err — overstating the
contamination.** Reconciled packet by packet against the committed text:

### 14.1 Which error appears in which packet

**Error A — the invalidator account.** Horizon succession stated as the
only staleness/withdrawal mechanism, omitting same-fact correction under
`"supersession": {"policy": "free"}`.

| Packet | Error A |
| --- | --- |
| Track 0 frame | **Originates here.** §7: "This is the only staleness/withdrawal mechanism found in committed code or content." Verification row V2 graded "Confirmed" on the fact type's title text alone. |
| Track 1 casual reader | **Absent.** It reports Track 0's finding and declines to conclude: "my honest answer to 'can I take it back?' would have to be: I don't know, and neither, apparently, does the packet." |
| Track 1 Grok account | **Present, and inconsistently held.** Corrected 2026-08-20: an earlier draft of this table graded it absent, which the committed text does not support. Attack 4 is titled "The user does not own withdrawal. Horizon succession does" and asserts "succession is the only staleness mechanism found" and "the only committed way it dies is a system horizon change"; action 4 calls succession "the invalidator the packet does verify." The same packet also files "any withdrawal path other than horizon succession" under §4, "Where explanation terminates." Both are in the packet; the assertion is the load-bearing one, and it is inherited from Track 0 §7 rather than independently derived. |
| Track 2 tree | **Inherited and hardened.** §4.4: "the only committed invalidator is horizon succession." |
| Track 3 (this document) | Inherited from both. Repaired at §5. |

**Error B — record-layer equivalence.** The claim that a recorded `false`
and no finding at all are the same thing in the record — that the system
holds no distinction between them anywhere. **Scoped deliberately, and
narrowed 2026-08-20:** what is disproven is the *structural* equivalence.
Whether any product act means "refusal" is not settled by this and is not
what the error was. The layer at which `false` and absence genuinely do
converge is admission, and that convergence is not an error.

| Packet | Error B |
| --- | --- |
| Track 0 frame | **Absent.** §2 is accurate and correctly scoped: it describes what `resolve_closure_admissions` *admits*, and says "absent, duplicate, false, or a non-boolean truthy value — falls through." It makes no claim about what the record can hold. |
| Track 1 casual reader | **Absent.** Does not reach the question. |
| Track 1 Grok account | **Present in part, and inconsistently held.** Corrected 2026-08-20: an earlier draft of this table graded it absent, which the committed text does not support. Attack 3 opens accurately on *admission* ("admission requires exactly one candidate whose `value is True`") but then crosses into the record layer — "There is no distinct 'user said no' state" and a user "would have recorded the same thing as having never been asked" — and action 3 warns against "a refusal the runtime cannot hold." Those are Error B. The same packet's §4 separately lists "whether 'false' is a representable user act at all" as a terminus. It did not hold the error as a settled disposition the way Track 2 §4.3 did, but it did assert it. |
| Track 2 tree | **Originates here.** §4.3: "Disposition: not representable, and this is settled, not ambiguous." |
| Track 3 (this document) | Inherited. Repaired at §4. |

### 14.2 What that reconciliation actually shows

**This subsection was itself corrected on 2026-08-20**, after an independent
review of the publication candidate found that the tables above had graded
the Grok account clean of both errors when its committed text asserts both.
What survives that correction is narrower than what was previously claimed
here.

Neither error was present in all four packets: the casual-reader account
asserts neither, and Track 0 asserts only Error A. **Neither error was a
convergence of the two standpoint accounts**, but the reason is weaker than
first stated — not that the external account isolated both questions and
left them open, but that the *other* standpoint account did not reach either
conclusion. The Grok account did assert both, and it did so inconsistently,
naming the same questions as termination points elsewhere in the same
packet. That inconsistency is itself evidence: a standpoint agent can list a
question as unresolved in its own methodology section while relying on the
frame's wrong answer in its substantive attacks.

Both errors entered upstream and were carried, not independently
rediscovered. Error A originates in Track 0 §7, and the Grok account
inherits it from there. Error B originates in Track 2 §4.3 as a *settled
disposition*; the Grok account states it earlier but does not close it, and
**Track 2's disposition authority is what converted a question its own
inputs held open in one place into a settled wrong answer.** The convergence
result at §6 is untouched by both errors, and so is the dispositioned
divergence at §7.

That the disposition track was where an open question became a wrong
conclusion is a finding about the milestone's own design. Track 2 was
deliberately given authority to say which account was right, because CQ-1
had been criticized for splitting differences. That authority worked on the
tension it was chartered to settle (§7) and misfired on a tension it
reached for beyond that charter.

### 14.3 The method lesson, stated at the right width

The demonstrated blind spot is narrow and should not be inflated: **a cited
static read did not extend to all adjacent fields of the cited artifact,
nor to the consumers whose behavior the claim depended on.** Error A cited
the fact type's `title` prose without reading the `supersession` field
beside it in the same object. Error B cited one function's docstring
without reading the `value_schema` of the fact type it consumes or the
currency projection that feeds it. In both cases the artifact was correctly
identified and correctly quoted; the neighborhood was not read.

The evidence-class discipline grades *how strongly* a claim is evidenced
(executed / static-read / content / inference / gap). It has no category
for *how completely* the cited artifact and its consumers were read, so a
partial static read records as a clean static read and passes every
downstream check.

**Safeguard for any future inquiry in this phase.** Every load-bearing
artifact claim must carry a completeness/neighborhood check: name the
artifact, the specific fields read, the sibling fields present and
deliberately not relied on, and the consumers that read the same artifact.
A claim that a behavior is *the only* behavior of its kind requires
enumerating where a competing mechanism could live and reporting that those
places were checked. This is a recording requirement, not a new lens or
round.

Both errors are repaired above. The repair also downgraded exit criteria
1, 2, and 3 (§11), which had been graded on the incomplete accounts.

## Disclosures

- No engine run was performed for this document; all executed evidence
  cited above is Track 0's own committed test run
  (`tests/tax/test_track6_integration.py`), curated and re-cited, not
  independently re-executed here.
- No personal data, real value, real document, workspace location, or
  absolute workstation path appears above. The dollar figure cited
  (`$10`) is from Track 0's synthetic test fixture.
- This document does not select a winning two-sentence answer among the
  probes in the prior packets, per the owner's binding re-aim carried from
  CQ-1 and repeated in this track's own charter.
- The milestone PR is deliberately not opened by this track, per the
  owner's direction. The milestone is not closed and no retrospective is
  written here; closure is a separate, owner-called unit.
