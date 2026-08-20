# Track 2 — Explanation Tree, Tension Catalog, and CQ-1 Delta (CQ-2)

> ## ⚠ SUPERSEDED IN PART — two conclusions in this packet are disproven
>
> This packet is retained as the working record of the disposition round.
> **Two of its conclusions are factually wrong** and were corrected during the
> owner-directed factual repair of 2026-08-20. Both are dispositions this
> packet asserted with authority, and one of them *closed a question its
> upstream inputs had correctly left open*.
>
> **Disproven claim 1 — §4.3, "not representable."** This packet dispositions
> the question of whether a user "no" is representable as *"not representable,
> and this is settled, not ambiguous."* That is wrong. The
> `tax.us.2025.f1099int.b1.source-closure` fact has
> `value_schema {"type": "boolean"}`, so a `false` finding is recordable and
> is carried in the closure-authority projection built by
> `packages/derivation/marshal.py`, which selects current findings by fact
> type and copies the recorded value through unchanged — it never filters on
> value. What is true is narrower: **admission** collapses `false`, absence,
> duplicate authority, and truthy-non-boolean into the same non-admitted
> outcome, and no interface exists to record the `false`. Record, projection,
> admission, and interface are four distinct layers; this packet conflated
> them.
>
> This error **originates here as a settled disposition.** Track 0 §2 stated
> the admission behavior accurately. The external Track 1 (Grok) account is a
> mixed case, corrected 2026-08-20: its §4 lists "whether `false` is a
> representable user act at all" as a point where explanation terminates,
> while its Attack 3 and action 3 assert the record-layer collapse anyway.
> That packet stated the error without closing it; **this** packet closed it.
> The two models did not converge on it, and what disposition authority added
> was the conversion of a question held open in one place into a settled
> wrong answer.
>
> **Disproven claim 2 — §4.4, the horizon-only invalidator.** This packet
> repeats and hardens Track 0 §7's claim that "the only committed invalidator
> is horizon succession." The `source-closure` fact carries
> `supersession {"policy": "free"}`, so a later finding on the same `fact_id`
> displaces the earlier one as a `correction` independent of any horizon
> change. There are **two** invalidating mechanisms.
>
> For the corrected account — the four-layer closure model, both invalidating
> mechanisms, and the per-packet reconciliation of which error appears where
> — read
> [`cq2-track-3-curated-inquiry.md`](cq2-track-3-curated-inquiry.md) §4, §5,
> and §14.1. Where this packet and that one disagree, that one governs.

Audience: Product, Shared (exploratory record). Status: **exploratory,
non-authoritative.** This packet dispositions two Track 1 standpoint
accounts against the Track 0 packet and against committed code; it does not
propose a schema, rule-language, engine, ADR, or content change, and it does
not select a winning two-sentence answer. "Claim boundary" and "explanation
tree" remain working lenses for this phase, not governance vocabulary.

Inputs read: `cq2-track-0-inquiry-frame.md` (Track 0), `cq2-track-1-casual-
reader.md` (Account 1, Claude), `cq2-track-1-system-provenance-grok.md`
(Account 2, Grok), and `track-2-explanation-tree.md` (CQ-1's closed tree,
read only, not re-derived). Two additional source reads were made directly
against committed code to settle load-bearing claims before dispositioning
(cited inline): `packages/derivation/evaluator.py` (`require_closed`) and
`packages/derivation/source_authority.py`
(`resolve_closure_admissions`'s own docstring, which states outright that
"false, absent, displaced, truthy-non-boolean, or duplicate closure findings
leave the family out of the closed set" — confirming, in the code's own
words, the collapse Account 2's Attack 3 describes).

---

## 1. Why the root cannot be a value

CQ-1's tree rooted at `ROOT "$1825 — Taxable interest"` — a published
number the user can point at. This inquiry's root is a **request**, not a
value: the moment an affordance asks the user to assert something, before
any number on this family is finalized (Track 0 §6). That difference is not
cosmetic. A value-rooted tree can always answer "what am I looking at?" by
pointing at the rendered figure; a request-rooted tree cannot, because there
is nothing rendered yet to point at except the ask itself. Every branch
below therefore begins one step earlier than CQ-1's did: not "where did this
number come from," but "what, exactly, am I being asked to say is true, and
what does saying it do." This is recorded as a finding, per the charter's
instruction that the root's difference is itself evidence, not merely
scaffolding for the rest of the tree.

```
ROOT  "Declare Form 1099-INT box 1 complete?"  (a request, not a value)
  ├─ D1  What am I being asked to assert?                (proposition)
  ├─ D2  Why does it have to be me?                       (speaker)
  ├─ D3  What exactly does this cover, and not cover?      (scope)
  ├─ D4  What happens if I say yes?                        (effect)
  ├─ D5  What does yes NOT get me?                         (non-effect)
  ├─ D6  What happens if I'm not ready — nothing, or no?    (not-yet path)
  └─ D7  How does this go stale, or get taken back?         (invalidator)
```

---

## 2. The explanation tree

Each node states the proposition, its evidence class, and — where the two
Track 1 accounts bear on it — how they align or split.

**Evidence classes used below:** **executed** (a committed test run's
actual assertions), **static-read** (code read but not run for this trace),
**content** (committed artifact text, quoted or closely paraphrased),
**inference** (a conclusion drawn by pattern or analogy, not directly
observed), **gap** (no committed evidence found either way).

### D1 — What am I being asked to assert?

**Proposition (content):** "every furnished 1099-INT box-1 statement item
is recorded as of that horizon" — the fact type's own title text, quoted
verbatim in Track 0 §1. Boolean, `value_schema: {"type": "boolean"}`
(content).

**Terminus, not a gap:** the artifact states its own proposition precisely.
A reader who reaches this depth has the exact sentence the system will
store a `True` against.

### D2 — Why does it have to be me, not the software?

**Proposition (static-read):** `resolve_closure_admissions` never derives
this boolean from any other fact; a family is admitted only from an
existing closure finding, current and literal-`True` (Track 0 §2, confirmed
directly against `source_authority.py` for this packet). The function's own
docstring states the negative space explicitly: everything that is not a
current unique `True` — "false, absent, displaced, truthy-non-boolean, or
duplicate" — "leave[s] the family out of the closed set." There is no
inference-from-entered-items branch anywhere in this code.

**Account split, dispositioned here (this is the milestone's central
tension — full disposition in §3.1):** Track 0's own plain answer gives one
reason ("the software can't check your mailbox"). Account 2's Attack 6
gives a second, non-identical reason (the engine can see the entered list
and is *forbidden* to treat it as closed). **Both are true and they answer
different sub-questions of D2.** The mailbox story answers "why can't the
software know about paper it has never seen" (true, and the only available
answer for undocumented interest). The forbidden-inference story answers
"why doesn't three entered items plus a running subtotal count as done"
(also true, and the mailbox story does not touch it — see §3.2). D2 is not
fully answered by either account alone; it needs both.

### D3 — What exactly does this cover, and not cover?

**Proposition (content):** box 1 of Form 1099-INT only — "never other
boxes, non-form interest, or Form 1040 line 2b" (fact type title, Track 0
§1); the family's own `closure_claim` repeats the same limit (Track 0 §1).

**Sub-node, evidence class gap — the horizon is not shown to the asker.**
Account 2's Attack 6, second half: the proposition is keyed to "the family
membership horizon current at attestation," not to "everything in your
mailbox." No committed UI or executed box-1 closure act exists to check
whether an interface would show the asker which items are currently in that
horizon's membership set before asking them to attest to it (Track 0 §1–§2,
no UI found). This is a **gap**, not a finding about current behavior — the
packet contains no UI to inspect. Recorded as a genuine open question, not
resolved by inference.

### D4 — What happens if I say yes? (effect)

**Proposition, dispositioned as executed — this is the headline
disposition (full evidence in §3.1):** saying yes admits exactly one symbol,
`tax.us.2025.interest.b1-subtotal`, into the closed set (Track 0 §2–§3,
§7). **Executed, State A** (Track 0 §5): a current literal-`True` closure
finding produces a published `b1-subtotal` of `"10"` in the golden fixture
— and Form 1040 line 2b, in the *same* executed report, is not asserted to
move; Track 0's own gloss states plainly that closing box 1 alone means
"nothing downstream of line 2b becomes any less blocked by this alone."

### D5 — What does yes NOT get me? (non-effect)

**Proposition (executed + content):** does not publish, compute, or change
line 2b (all ten pins required, Track 0 §3); does not mean the return is
complete or signed (Track 0 §7, §9). This node is where the six notions
(§4 below) are sharpest: D5 is exclusively about source-family closure,
never about computation readiness, return readiness, or attestation.

### D6 — What happens if I'm not ready? (the honest "not yet" path)

**Proposition, executed, State B** (Track 0 §5): an absent declaration does
not error, does not zero, does not crash — `stop_reason: "saturated"`. The
rule requiring the family blocks with `SOURCE_SET_UNCLOSED`; already-closed
families remain published unaffected.

**Sub-node, dispositioned — the cascade misattribution (full disposition in
§3.2):** in the executed scenario, six entries block; exactly one names the
actual unclosed family (`non-form-interest-subtotal`); line 2b itself blocks
under a different code (`DEPENDENCY_ABSENT`) naming a missing subtotal, not
the family; four further downstream lines each name yet another missing
symbol, none of them the family (Track 0 §5, both accounts' deepest thread).
**Executed for `non-form-interest`, not box 1** — the box-1 substitution
that both accounts (implicitly Account 1, explicitly Account 2) use to
describe "if I don't declare box 1" is **inference by analogy from the same
admission mechanism**, not a second executed run. This distinction is
preserved here exactly as Account 2 flagged it and is not upgraded.

**No representable "no" (static-read, disposition in §3.3):**
`resolve_closure_admissions` treats every non-`True` case identically —
absent, false, duplicate, and garbage all fall through the same `continue`.
There is no third state. An interface that offered an explicit "No, I'm not
done" button would be recording exactly the same engine state as if the
user had never been asked (Account 2 Attack 3, static-read, confirmed
directly against the function's own docstring for this packet).

### D7 — How does this go stale, or get taken back? (invalidator)

**Proposition (content):** "a later membership transition displaces this
closure through horizon succession; re-attestation on the successor horizon
is required" — the fact type's own invalidator text (Track 0 §1, §7).

**Gap, not resolved by inference (disposition in §3.4):** no committed
user-facing withdraw/un-declare action exists anywhere Track 0 searched
(`entry_loop.py`, `live.py`, `source_authority.py`); `withdrawn_fact_ids` in
`live.py` is confirmed (independently, for this packet) to be a distinct
mechanism — retired fact types in state projection, not a user-facing
unattest action on a closure finding. Whether a horizon succession is ever
signalled to the user, and what happens if the user is wrong *without* a
membership change (forgot a form, horizon unmoved), is unanswered by any
committed artifact. This is the tree's second explicit terminus.

---

## 3. Worked progressive-disclosure path, with explicit terminus

One path, exercising D4→D6, because it is where the two accounts converged
independently on the same paragraph and where the tension catalog's central
dispositions live.

**Depth 0 — root, at the moment of the ask.**

> You're the only one who can say whether every 1099-INT you received with
> box 1 interest has been entered.

Test: true as far as it goes (D2's mailbox half); does not yet claim what
saying yes does.

**Depth 1 — reached by "what does saying yes do?"**

> Saying yes tells the system this one piece — box 1 of your 1099-INT forms
> — is ready to use; it does not, by itself, finish or total your return.

**Depth 2 — reached by "does it show up anywhere?"**

> Saying yes unblocks this one figure so it can be added into your total
> interest once every other required piece is also ready. Until then, your
> total taxable interest can still show as not-ready, even though this one
> piece was accepted.

**Terminus, explicit.**

> If your total taxable interest is still showing as blocked after you say
> yes, that does not mean your "yes" didn't work — it means something else
> the total needs is still outstanding. This product does not currently
> point back at which piece from the place you're looking; you would need
> to check each source individually.

Test: this terminus is the honest floor supported by executed evidence
(Track 0 §5 State B, both accounts' deepest thread) — it does not promise a
pointer the code does not build, and it does not claim more than depth 2
supports. Past this point, a user must trust, ask, or guess which of the
remaining nine families is the actual cause; no committed content resolves
that for them.

---

## 4. Tension catalog

Each entry: name, both poles with evidence, and disposition —
**resolvable by explanation**, **resolvable only by a product decision**, or
**standing** (genuinely unresolved on current evidence).

### 4.1 — Does "before it can use this piece in your return" misrepresent the runtime? [DISPOSITIONED]

**Pole A (Track 0's own plain answer, reproduced near-verbatim by Account
1):** "the software... needs you to say so before it can use this piece in
your return." Both casual-reader-standpoint tellings treat this as a fair
gloss of admission.

**Pole B (Account 2, Attack 1):** State A is executed and shows line 2b
unmoved by a successful box-1 `True` (Track 0 §5, §7's own gloss: "nothing
downstream of line 2b becomes any less blocked by this alone"). "Use this
piece in your return" is what a person hearing "say you're done" will take
the click to mean, and the executed consequence — an intermediate subtotal
publishes, the line the user actually looks at does not move, the blocked
text does not mention box 1 — does not match that expectation.

**Disposition: the phrase is defensible read narrowly and defective read as
a user would naturally read it — and the ambiguity between those two
readings is itself the defect, not a reason to withhold a verdict.** The
charter offered three verdicts (defective, defensible, ambiguous) and the
supported answer is a fourth: the phrase is ambiguous *in a specific,
identifiable way*, and that specific ambiguity is what makes it defective as
copy. "Ambiguous" is not being used here as a hedge between the two poles;
it names the mechanism by which one pole is right about the sentence and the
other is right about the reader. The phrase is technically accurate at the
mechanism level:
"this piece" can be read as referring to the box-1 subtotal specifically,
and admitting that subtotal into `closed_sets` is exactly and only what a
`True` does (Track 0 §2–3, executed §5). But nothing in the sentence, or in
what a user sees on screen at the moment they click "yes," disambiguates
"this piece" (the box-1 subtotal, which does change) from "your return"
(taxable interest / line 2b, which usually does not change from this one
click alone). A reader has no way to tell, from the sentence alone, which
of those two things "use... in your return" refers to — and the executed
State A result (subtotal published, line 2b unmoved) is evidence *for* the
narrower reading and evidence *against* the naive reading, not evidence
that either reading is wrong on its face. **This is exactly why Account 1
reproduced the phrase without noticing tension and Account 2 attacked it:
both readings are grammatically available, and the accounts picked
different ones by standpoint, not by different evidence.** The phrase is
therefore judged **defective as user-facing copy** (it does not disambiguate
a distinction — subtotal admission vs. return-level effect — that this
inquiry has shown to be load-bearing) while being **defensible as an
engineering gloss** (it is not false about the mechanism it actually
describes). What would settle it further: an executed scenario in which box
1 is the *last* of the ten families closed, so that saying yes does move
line 2b, paired with one in which it is not the last — showing a user both
outcomes from the identical action would settle whether the ambiguity is
tolerable or must be resolved by rewording. That test was not run for this
packet and is not proposed as an action beyond naming it.

**Resolvable by explanation** — a rewording that names "this one piece"
explicitly (as Depth 1–2 in §3 attempt) removes the ambiguity without any
product or engine change. Not a standing tension; not a product-decision
tension. It is a wording defect with a demonstrated fix shape already
sketched in §3, which this track does not adopt as copy per its non-goals.

### 4.2 — "Can't check your mailbox" vs. "can see the list, forbidden to close it" [DISPOSITIONED]

**Pole A (Track 0 §6, repeated by Account 1):** the software can't check
the user's mailbox, so it needs the user to say so.

**Pole B (Account 2, Attack 6):** the engine can see the exact list of
items the user already entered in this product; §2's admission mechanism
does not compute completeness from that list under any circumstance — it is
not permitted to, not merely unable to. "Mailbox" implies a search problem;
the actual mechanism is a structural refusal to infer closure from any
fact, including facts the system already holds.

**Disposition: both are true, and they are honest answers to two different
sub-questions, not competing answers to one question — but the packet's
plain answer states only Pole A, which makes it incomplete, not false.**
D2 above already separates these: Pole A explains why the system cannot
originate the "every item is in" fact for items it has never seen (this
holds regardless of code — no software can observe a physical mailbox).
Pole B explains why the system does not treat "N items entered, subtotal
computed" as sufficient even for items it has already seen and priced
(§2's `resolve_closure_admissions`, confirmed by the function's own
docstring: there is no inference branch, by design, not by omission). A
user who has entered three 1099-INT forms and sees a running $10 subtotal
and is then asked to separately declare "done" is being asked something
Pole A alone does not explain — Pole A only explains why paper the system
never saw can't count itself; it says nothing about why paper it did see
still needs a separate assertion. **Does the difference matter to a user?
Yes, specifically at the moment a user who has entered everything they hold
wonders why entering it wasn't enough** — that is precisely the gap Pole B
fills and Pole A does not. This is not evidence the mailbox story is wrong;
it is evidence it is a partial answer being asked to do a full answer's
job.

**Resolvable by explanation** — both reasons can be stated together without
any product or engine change; the packet's own two-sentence answer already
has room for one more clause. Not standing.

### 4.3 — Is an explicit "no" representable? [DISPOSITIONED]

**Static-read, confirmed directly against `source_authority.py` for this
packet:** `resolve_closure_admissions`'s own docstring states that "false,
absent, displaced, truthy-non-boolean, or duplicate closure findings leave
the family out of the closed set" — one non-admission outcome for five
distinct input conditions, including an explicit `False`. Admission
requires exactly one current candidate with `value is True` (Track 0 §2);
anything else, including a deliberate `False`, produces the same
non-admission as never having asked.

**Disposition: not representable, and this is settled, not ambiguous.**
The code path is read directly, its own docstring names the collapse in
its own words, and there is no branch anywhere that distinguishes "user
declined" from "user was never asked." This is **standing** as a question
of current runtime capability — no explanation can make "no" distinct from
"not yet" when the engine itself does not distinguish them; only an engine
change could do that, which is out of this track's authority to propose.
What *is* resolvable by explanation, without an engine change: an interface
is free to describe declining and not-yet-answering as the *same* thing
today ("skip for now"), which would be an honest description of the actual
engine state rather than a misrepresentation — Account 2's own action 3
makes exactly this point, and it is adopted here as a disposition, not a
new action.

### 4.4 — Absent withdrawal path: explanation gap or product gap? [DISPOSITIONED]

**Evidence:** Track 0 §1, §7 — the only committed invalidator is horizon
succession, a system-triggered event, not a user act; no committed
user-facing un-declare/withdraw control exists anywhere searched
(`entry_loop.py`, `live.py`, `source_authority.py`); `withdrawn_fact_ids`
in `live.py` is a distinct, unrelated mechanism (confirmed directly, this
packet: `packages/derivation/live.py` line 197,
`validate_projected_source_boundary(state.findings.values(),
state.withdrawn_fact_ids)` — retired fact types in state projection, not a
user-initiated unattest action on a closure finding). Both Track 1 accounts
independently reached the same conclusion without contact (Grok's
convergence note).

**Disposition: it is a product gap, not an explanation gap, and the
distinction matters for what Track 3 does with it.** An explanation gap
would mean the mechanism exists and committed content simply fails to
surface it — that would be fixable by better copy alone. That is not this
case: there is no mechanism to surface. No amount of rewording produces a
withdraw action that does not exist in code. The honest explanation of this
gap ("I don't know, and neither does the codebase, whether a horizon
succession is ever signalled to you, or what happens if you were wrong
without one") is itself the correct explanation — not a placeholder for a
better one. **Resolvable only by a product decision** (whether to build a
withdrawal mechanism, and if so what it does) — not standing, because
"standing" would imply genuine ambiguity in what the evidence shows, and
there is none: the evidence unambiguously shows absence.

### 4.5 — Additional tension the accounts expose, not named by the charter: yes is locally visible, not-yes is globally diffuse [asymmetry, both accounts independently reach it]

**Pole A:** saying yes is one action with one traceable consequence (admits
one named symbol; Track 0 §2–3, §5).

**Pole B (Account 2, "Asymmetry" in Attack 2; Account 1's "deepest thread"
independently the same paragraph):** not saying yes, once a downstream rule
needs it, produces a diffuse, differently-coded, differently-named cascade
that does not point back at the missing declaration (Track 0 §5 State B,
executed).

**Disposition: real, executed (for `non-form-interest`; box 1 by
inference), and this is the strongest convergent finding in the packet —
already dispositioned as the §3 worked terminus above.** Recorded here for
completeness of the catalog rather than re-argued. **Resolvable only by a
product decision** — the fix (naming the missing family at the point a
downstream line blocks) is a content/schema-authoring change (interpolating
which family into `blocked.explain`), inherited from CQ-1's own SC-3
finding and re-confirmed live here; this track does not adopt or propose
that change, only confirms it is the same shape of gap CQ-1 already named.

---

## 5. Cross-inquiry delta against CQ-1

CQ-1's tree: six branches (P, S, T, A, R, N), 16 tensions, four lenses. Read
only, not re-derived, per the charter.

### Repeated — same branch, substantially unchanged content

- **Filing-effect boundary (CQ-1's R1/R4 ↔ CQ-2's D5, D7 sub-node on legal
  attestation).** Both inquiries independently land on the same negative/
  boundary fact: nothing here is filed, signed, or has legal effect; the
  jurat is a distinct, later act (CQ-1 §1 R1/R4; CQ-2 Track 0 §7, §9 notion
  6). The evidentiary basis is the same across both inquiries —
  `basis: "documentary"` in the one observed closure-finding code path,
  and the family's own scope-limited text — not independently re-derived
  here, consistent with the non-goal against re-running CQ-1's lenses.
- **Agency/voice attribution (CQ-1's P1/A1, "we found" vs. "you entered" ↔
  CQ-2's D1/D2).** Both inquiries independently find that a declaration's
  speaker is the user, not the system, and that system-voice copy risks
  misattributing authorship (CQ-1 tension #3, convergent across two lenses;
  CQ-2 Track 0 §7 "Speaker" field, both Track 1 accounts). CQ-2 sharpens
  rather than repeats verbatim: where CQ-1's tension was about *wording*
  ("we found" implying discovery), CQ-2's D2 is about a *mechanism* claim
  (the engine structurally cannot derive the boolean from any other fact) —
  a stronger, code-verified version of the same underlying doctrine
  (ADR-0009), not a restatement.
- **Generic blocked-state messaging (CQ-1's N2/SC-3, four-way convergence ↔
  CQ-2's D6 sub-node, §4.5).** CQ-1 found the `blocked` explain string
  identical across all codes; CQ-2 independently re-confirms the same
  artifact is still live in v5 (Track 0 §3, "inherited... not a new
  finding") and both Track 1 accounts independently re-derive the user-
  facing consequence for this specific interaction. Same underlying content
  gap, same artifact, re-confirmed rather than re-derived.
- **The six/five distinctions (CQ-1's §0 ↔ CQ-2's §6 below).** CQ-1 named
  five; CQ-2 explicitly carries all five forward and adds a sixth (legal
  attestation, split out from document completeness — see CQ-1's tree §9
  note and CQ-2's own milestone plan "Distinguishing 'complete'" section).
  Repeated with one addition, not changed in substance.

### Changed — same branch, altered content, evidence, or terminus

- **P1 "who supplied this" → D2 "why does it have to be me."** CQ-1's P1
  asked about a *published number's* authorship after the fact
  (retrospective: who made this figure). CQ-2's D2 asks the same authorship
  question *prospectively*, at the moment of the ask, and with a materially
  different evidentiary terminus: CQ-1's P1 terminated at ADR-0009 doctrine
  plus rendered-copy gaps; CQ-2's D2 terminates at an executed/static-read
  code fact (no inference branch exists) that is stronger evidence than
  doctrine alone — the engine's *inability* to infer this fact is now
  directly demonstrated, not merely asserted as governance policy.
- **A2 "does confirmed mean I swore to the IRS" → D5/§4.4's invalidator
  question.** CQ-1's A2 addressed a *retrospective* worry about a number
  already on screen (does its label imply a jurat). CQ-2's version is
  *prospective and active*: the user is being asked to click something, and
  the open question shifts from "what does this word imply" to "can I take
  this specific action back." The evidence class also changes: CQ-1's A2
  terminated at a wording/rendering gap (content); CQ-2's D7 terminates at
  a genuine mechanism gap (no code exists), a harder floor.
- **N2 "which family is missing" → D6's cascade (§4.5).** CQ-1 found the
  *rendered text* was generic across four codes at one line. CQ-2's
  executed evidence (Track 0 §5 State B) is a materially sharper version:
  not only is the text generic, but the *code itself* changes one hop
  upstream (`SOURCE_SET_UNCLOSED` becomes `DEPENDENCY_ABSENT`), and the
  cascade touches four further, unrelated-looking lines. CQ-1 could not
  make this claim because it examined a fully-closed fixture; CQ-2's
  executed State B is new evidence CQ-1's committed packets do not contain.

### Absent — CQ-1 had it; a declaration request does not raise it

- **P2 "how was it calculated," P3 "can I see the pieces" (arithmetic /
  citation-drilling branches).** CQ-1's tree spent two full nodes on
  reconciling a published dollar figure against its constituent pins and
  citation sites. CQ-2's root is a boolean request, not a computed value —
  there is no arithmetic to reconcile and no dollar figure to drill into at
  the point of the ask (Track 0 §1: `value_schema: boolean`). This
  disappears structurally, not by oversight: a yes/no request has no
  computation to show its work for.
- **P4 "is this current" as a page-wide staleness qualification, and P5
  "why is this taxable interest under tax law."** CQ-1's P4 and P5 concern
  a rendered document's package-version currency and a computed value's
  legal classification. CQ-2 has no rendered document (D1's terminus is the
  proposition's own text, not a package-versioned page) and makes no tax-
  law classification claim (the closure fact type does not classify
  anything as taxable; it only asserts a document-entry fact). Both are
  absent because their subject matter — a rendered, classified, versioned
  value — does not exist yet at the point CQ-2 examines.
- **T1/T3 "what does this feed into," "where did excluded interest go."**
  These trace a *number's* downstream consumption and a *number's*
  exclusion. CQ-2's request precedes any number; D4/D5 answer "what does
  saying yes feed into" only at the level of *closed-set membership*, not
  at the level of a dollar amount flowing anywhere. Structurally absent for
  the same reason as P2/P3.

### New — only a declaration request raises this; a presented result never did

- **D2's forbidden-inference distinction (§4.2).** CQ-1's root was always
  already a number; there is no "why does the system need the user rather
  than compute it itself" question to ask about a number that has already
  been computed and shown. This question is intrinsic to a *request*, not
  transferable to a result.
- **The yes/no/silence collapse (§4.3).** CQ-1 never examined an
  interaction with a binary user choice at all; there was nothing to
  decline. This tension exists only because CQ-2's interaction type has an
  affirmative act to perform or withhold.
- **The asymmetric visibility of yes vs. not-yes (§4.5, D6).** CQ-1's N2
  gap was about *which family* is missing when something is already
  blocked — a static state. CQ-2's asymmetry is about the *difference in
  legibility between two possible user actions* (act vs. don't act) for
  the same request — a question that only exists when there is an action to
  compare against its absence.
- **The horizon-membership-not-shown gap (D3 sub-node).** CQ-1's fixture
  was already closed; there was no open horizon whose membership a user
  might need to see before attesting to it. This gap is intrinsic to the
  *moment before* attestation, which CQ-1's presented-result frame never
  examined.

---

## 6. The six notions, kept distinct

Reused from Track 0 §9 and the milestone plan's own list; this tree does
not redefine them, only checks that no node above collapses one into
another.

1. **Document completeness** — D3's horizon-membership question touches
   this but does not resolve it: the fact type asserts a claim *about* the
   taxpayer's paper; no artifact verifies the paper itself. Kept distinct
   from source-family closure at D1/D3.
2. **Source-family closure** — exactly D1–D2's proposition. The tree's
   entire root-level scope.
3. **Product tax-coverage completeness** — not raised by this tree at all;
   the b1 family's existence as a modeled category is presupposed, not
   examined (out of scope, consistent with the milestone plan).
4. **Computation readiness** — D4/D5/§3's terminus, kept explicitly
   separate from D1's proposition: whether line 2b's rule has all ten pins
   is a system-side fact the user is never asked about directly.
5. **Return/filing readiness** — D5 explicitly denies this follows from D4;
   untouched by one family's closure, stated plainly.
6. **Legal attestation** — D7's `basis: "documentary"` evidence keeps this
   distinct from D1's proposition; §4.4's disposition treats a withdrawal
   mechanism's absence as a product gap precisely because attestation-grade
   permanence is not what this declaration claims to be.

No node above uses "complete," "closed," "done," "attested," or "confirmed"
to mean more than one of these six without stating which one it means. The
D2/§4.2 disposition is the sharpest test of this discipline: it required
holding "document completeness" (mailbox) and "source-family closure"
(admission mechanism) apart as two distinct reasons for the same ask,
rather than treating them as restatements of one idea.

---

## 7. OV-1

Included once, bounded exactly as Track 0 §8 already states it, because it
bears directly on D4/D5's non-effect claim (closing box 1 is one of seven
inputs to `interest.positive-total`, which is one of two subtotals the
committed Schedule B attachment rule tests, per Track 0 §8's independently
re-verified chain). Stated here only as the counterfactual Track 0 already
established: the committed rule implements one of several IRS "Who Must
File" triggers; the b1 family itself carries no accrued-interest, ABP, or
nominee content, so declaring it closed does not by itself decide whether
Schedule B attaches (Track 0 §8, both Track 1 accounts' independent
"declined to promote to an action" agreement). No fix shape is inferred.
Not attached to any other node — it does not bear on D1, D2, D3, D6, or D7,
and is not forced onto them.

---

## 8. What this track found wrong in the prior packets

Nothing in Track 0 or either Track 1 account required a substantive
correction — both accounts' technical claims were re-checked directly
against `source_authority.py` and `live.py` for this packet and held.
Two precision notes, not corrections:

- Account 1's two-sentence answer reproduces the "before it can use this
  piece in your return" phrase from Track 0 §6 without attribution as a
  quote; this is not an error (Account 1 was reading only the Track 0
  packet and had no reason to treat the phrase as borrowed rather than
  independently composed), but it is why §4.1 above treats the two
  accounts' split as evidence about *readable ambiguity*, not as one
  account being wrong and the other right.
- Account 2's Attack 3 cites "the exact-one check" as the mechanism that
  would fail on a duplicate `True`; this packet's own direct re-read of
  `resolve_closure_admissions`'s docstring confirms this exactly
  ("duplicate closure findings leave the family out of the closed set"),
  so Account 2's claim is upheld, not merely accepted on trust.

---

## Disclosures

- No engine run was performed for this packet; the executed evidence cited
  throughout is Track 0's own committed test run
  (`tests/tax/test_track6_integration.py`), not independently re-executed
  here, per the charter's instruction to read Track 0's evidence rather
  than re-derive it. Two direct source reads were made against
  `packages/derivation/source_authority.py` and
  `packages/derivation/live.py` to verify specific claims before
  dispositioning them (cited inline in §4.3 and §4.4); no additional test
  run was performed.
- No personal data, real value, real document, workspace location, or
  absolute workstation path appears above. Dollar figures cited ("$10")
  are from Track 0's synthetic test fixture, not a real filer's data.
- This packet does not select a winning two-sentence answer among the
  three probes in the prior packets, per the owner's binding re-aim carried
  from CQ-1.
