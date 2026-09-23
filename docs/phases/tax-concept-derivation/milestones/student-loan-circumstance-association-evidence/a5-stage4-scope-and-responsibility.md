# A5 stage 4 — scope claims and the responsibility applies-to relation

Provisional. Filer-centered. No implementation. Two relations, each saying that something
**applies to** something else, and they are kept apart because they have different bases:

- a **scope claim** is the filer's — they say a circumstance, or an answer, reaches some
  population of reported interest. It is a telling, `attested`.
- a **responsibility** is the application's — a condition applies because a deduction was taken
  through a schooling situation. Nobody asserts it; it is derived, and it establishes nothing.

Engine claims were traced at this commit; levels are stated where they matter.

## Part 1 — scope claims

### What a scope claim is about, and its key

Stage 2 separated what a circumstance *says* from the population the person says it applies to,
and left open whether that claim is keyed on a statement. It is.

**A route-(a) scope claim** — *"this applies to everything on this statement"* — is about a
**pair**: what is applied, and the statement it reaches. Key: the applied item's identity plus
the statement's own identity (the 1098-E box-1 keys: lender, statement, tax year).

Neither half alone will do, for the reason test 1 gave: keyed on the statement alone, two
circumstances applied to one statement collide and the second reads as a correction of the
first; keyed on the circumstance alone, one circumstance applied to two statements collides the
same way.

**For the schooling path this is a financing claim at statement grain.** *"The loans on this
statement paid for my Riverside BSc in autumn 2024"* is the same ordinary telling as stage 2's
financing claim, with the statement's contents as its subject instead of an identified
borrowing. So the scope claim is keyed on the statement plus the schooling situation, and the
student-and-period conclusion of stage 3 takes its period from it exactly as it would from a
borrowing-level financing claim. For a borrowing-keyed circumstance — *"the loans on this
statement also paid for a car"* — the scope claim states that circumstance of every borrowing
the statement reports, keyed on the circumstance and the statement, with no placeholder
borrowing (stage 2).

### What a correction reaches — scope claim against circumstance

Stage 2 said these differ. Here is how, using A2's rows.

| Change | Reaches | Why |
| --- | --- | --- |
| The **schooling circumstance** is corrected | Every financing claim and scope claim naming that situation, on the next derivation | They name its identity; the correction is a new current finding there (stage 3: re-derivation, nothing carried) |
| The **scope claim** is corrected to a different situation | That statement only | The situation is half of the key, so this is **not** a correction in place: the old claim is retracted and a new one asserted. A2's row for an association naming a different target assumed the target was outside the association's identity; under a pair key it is inside it. The outcome A2 wants is unchanged — nothing unresolved, the new target applies at once |
| The scope claim is **narrowed** — "actually only one of these loans" | That statement only | Route (a) becomes route (b): a different population, so retraction of the (a) claim and assertion at the borrowing's grain — not a correction in place |
| The scope claim is **retracted**, nothing replaces it | That statement only | A2's retraction row: an adverse basis withdrawn returns the statement to evaluable (A3). The ask does not hold the figure |
| A **further statement** arrives | Nothing | The claim is keyed on one statement and says nothing about another. A new statement with nothing said about it publishes like any other — A2's last row, answered by the key rather than by detection |
| The statement's **composition** changes — a corrected form covering different loans | **A2's partly-surviving row, with one thing route (a) cannot supply** | A2: what was said about members still present keeps holding; an adverse claim whose scope may reach a *newly present* member is unresolved as to that member; blocked only where a calculation depends on the lapsed part. That applies here unchanged, and only to an **adverse** route-(a) claim — a non-adverse one leaves a new member with nothing adverse said about it, which publishes. What route (a) cannot supply is **which members are new**: it enumerates none, so the surviving part and the unresolved part cannot be told apart from the claim itself. Detecting the change at all is **D9** (a corrected form is a same-member value correction, so the claim still resolves), and holding the unresolved part is **D10** — both untested and on the may-not-rely list. The bounded consumer's demonstration must not depend on this case |

The key does real work in the fifth row: a statement-keyed claim cannot silently reach a
statement nobody spoke about, which the "all my loans" claim in A2 could.

### Case 2 — where the default attaches when no period is identified

Stage 3 left this open: with no financing claim and no scope claim there is no period, so no
student-and-period conclusion, and A3 still says the consumer proceeds.

**Selected: the statement.** The favourable result rests on a named conclusion keyed on the
statement's identity — *no enumerated adverse circumstance bears on the interest this statement
reports* — which is the scope the consumer actually computes over, and the only one always
present when there is interest to compute.

- **Why not the borrowing.** In case 2 there may be no identified borrowing at all (a statement
  with nothing enumerated), and where borrowings *are* identified, a borrowing-level default
  conclusion says nothing the statement-level one does not unless a partial reduction needs it.
- **Input pins — as designed, not as demonstrated.** The statement's own reported-interest
  finding, the finding that establishes the subject, as the financing claim did in case 1. That
  depends on the owed per-key publication pinning its item. Pairing dispatch (D1, `run`) is the
  nearest analogue and pins both sides of a pairing, but `a4-bounds.md` is explicit that a
  conclusion keyed on one subject is not a pairing, so D1 does not show this. No schooling input, because nothing about schooling
  exists. **If** the item is pinned as designed, the conclusion has an asserted input and the
  origin hazard stage 3 handed on — a conclusion with no asserted input still marked
  `"assertion"` — does not arise. Whether it is pinned is part of what G2 must see.
- **What the current presentation projection would cite.** The walk passes through the
  favourable value and the conclusion to the statement's box-1 finding, which is already the
  amount's citation. The reader sees the 1098-E cited and **nothing about eligibility** — the
  silence stage 3 traced, now with a conclusion behind it that the reader cannot reach.
- **Test obligation.** Case 2 now has a key, pins and a traced citation, so it **becomes a G2/A6
  test case**: the reader must say that eligibility rests on the default. It depends on the same
  undemonstrated behaviour as stage 3 — one conclusion published per key of a single subject —
  with the statement added as a third key kind.

**Case 1 keeps its key.** Where a financing claim or scope claim names a period, the
student-and-period conclusion stands; the statement-level one, if published there too, pins it.
Whether both are needed in case 1 is left to the demonstration: the period one is required
because the status is shared across statements (stage 2, test 2); the statement one is required
only in case 2.

**A partial reduction's remainder is not settled here.** Where one borrowing on a statement
carries an adverse circumstance and the rest carry none, the reduced figure pins the adverse
chain for that portion, and the remainder is default-supported with nothing yet selected to
carry that basis. That is part of the partial-reduction behaviour already owed to G2.

### Obligation applied to a statement

Stage 3 keyed legal obligation on the borrowing and left a statement as a permissible
population. Same shape as any scope claim: where only the statement is known, the answer is
keyed on the obligation fact and the statement; where borrowings are identified, on the
borrowing. **No consumer in this milestone**, and stage 3's constraint on A6 stands: it is not
posed per loan or per statement through the incumbent tax-year fact.

## Part 2 — the responsibility applies-to relation

The five decisions `responsibilities-and-circumstances.md` routed here, each answered against
the named consumer: A6's revealing consumer, which must let the person see each condition that
applies, why, and what it concerns — *this treatment, this period, this statement's interest.*

### What makes a responsibility apply

A responsibility applies **where a deduction is taken through a schooling situation without the
situation's conditions being established** — which is exactly where the favourable value rests
on stage 3's named conclusion. It does not apply where an adverse circumstance is supported: no
deduction is taken on that path, so there is nothing for a condition to be left open *for*.

**And only where a circumstance was described.** The responsibility direction binds a condition
to *the circumstances and treatment that made it applicable* — "because they claimed this
deduction **and described this enrolment**" — and rules out generic disclaimer text. In case 2
nothing about schooling was described, so **no responsibility applies there**: stating the
schooling conditions against a bare statement would be exactly the generic disclaimer the
direction forbids. What case 2 owes the reader is stage 3's — that eligibility rests on the
default — which is a basis, not a responsibility. So the statement-level conclusion's rule
declares none of the schooling conditions; only the student-and-period conclusion's does.

So in the nine-credit case and case 1 the applies-to relation has three parts, all of which are
on the record in the favourable case: the **condition** (for the schooling path: that the institution is an eligible
educational institution, that the programme leads to a recognised credential, that the load is
at least half-time by the institution's own standard); the **circumstance** it concerns (the
schooling situation, reached through the financing claim or scope claim); and the **treatment**
(the interest on the statement whose figure depends on it).

### Is an existing citizen enough — selected: rule citations on the named conclusion

**The named conclusion's rule declares, as its `citations`, the authority for each condition
it leaves to the filer.** On the ordinary evaluation path the runner pins every declared rule
citation on the publication (`runner.pins_for`, role `citation`). **That is not every path.** The
per-item and dispatch paths assemble their own pins and do not call `pins_for`: the current-year
subtotal dispatch pins only the rule, adoption and governance, and a pairing-scoped rule gets a
citation only where the calling code adds one explicitly (`pairing_consequences.py`, the one
`_citation_pin` call). The named conclusion is per-key, so it will not be on the ordinary path —
**carrying its declared citations is part of the owed per-key publication**, not something the
existing per-item paths already do. The instance binding comes from
the same publication's input pins — the financing claim or scope claim naming the situation, or
in case 2 the statement. Condition, circumstance and treatment are then all on one publication.

Three facts make this fit rather than approximate:

- **It is gated exactly right.** The named conclusion is published only when nothing adverse is
  supported — an applicability gate, recorded as `inapplicable` otherwise — so its citations
  appear only where a deduction is taken on the default. An adverse value pins its adverse
  circumstance and carries none of them.
- **It is never consumed as a value.** Citation pins are not read by the evaluator. So the
  selection introduces no confirmation requirement, no block, and no favourable finding about
  any condition, which is what the responsibility direction requires.
- **Its value is its identity.** Because the conclusion is published only in the favourable
  case, which conclusion it is says what its value is. That matters below, since the durable
  record carries no values.

**What it does not carry, stated so it is not assumed.** A citation citizen (`citation.v1`) is a
legal locator — a U.S. Code title and section, an IRS form, instructions or publication. It
does not say *"applies but not established"*; that meaning comes from being pinned by a
default conclusion, and a citation pinned by an ordinary rule means the authority it applied.
It carries no plain-language condition either; the wording of every responsibility message is
the owner's, in A1's approval set. And the pin list is flat: which component of the situation
each condition concerns — the institution, the programme, the load — is not on it. The
responsibility direction asks for *what it concerns* at the grain of treatment, period and
statement, which the input pins give; component-level binding is not needed and not claimed.

**The `default` pin role is not used.** It exists in the pin-role enums of `derived-finding.v2`
and `derivation-record.v9`, and nothing in the runner produces it. Adopting an unused role to
mean "left to the filer" would be defining new semantics while appearing to reuse old ones.

**Alternatives, and why not.**

| Alternative | Why not |
| --- | --- |
| A derived finding per responsibility — *condition C applies to situation S for treatment T* | Gives each responsibility its own identity and component binding, at the cost of another per-key publication for every condition on every situation. Nothing in the named consumer needs per-responsibility identity yet; revisit if A6 does |
| Reconstruct purely from content and findings, with nothing pinned | Content can say which conditions attach to schooling situations, but only the conclusion's pins say which situations the deduction actually ran through. Without them a reconstruction can attach conditions to situations not on the path |
| Horizon identity-keying | Weighed, as the plan requires, and not taken. It displaces a claim rather than re-deriving it, and a responsibility has no *findable-but-unsupported* state to protect — it is not the person's claim, so A2's third leg never arises, and the first two are given by re-derivation from current findings |

### Lifecycle under A2

**Re-derivation, with no separate state.** A responsibility applies while the conclusion that
carries it is published from current findings. Correct the circumstance to something adverse
and the conclusion becomes inapplicable — the responsibility lapses. Retract the financing
claim and the path moves to case 2 — the responsibilities lapse, because no described
circumstance remains to bind them, and only the default basis is left to show. Where A2 holds
part of a figure as unresolved, that part's treatment is not taken, and no responsibility
applies to it meanwhile. Nothing here needs D10: a responsibility never holds a figure.

### Whether it is in the derivation record

**Inside provenance, in the citation role, on the default conclusion only** — provided the
per-key publication carries the citations, which above is owed. The responsibility
direction left open whether a responsibility sits outside provenance or in a different role
there. It is the second: the default conclusion's favourable value *does* rest on those
conditions being left to the filer, so they are part of what it rests on, in a role that is not
`input`. Citation pins survive into `derivation-record.v9` — the ledger drops only
`computation`, `applicability`, `field-mapping` and `cross-form-bridge` (`runner.ledger_pins_for`)
— and `inapplicable` is a recorded disposition. `read`.

### Persistence or reconstruction

**Reconstructable from what is durable, on paper.** The completed record holds the conclusion's
disposition row (its symbol and rule, which fix its meaning and — being favourable-only — its
value), its citation pins and its input pins. The recorded findings hold the financing claim's
situation; the package holds the citation citizens. So nothing new would need to be stored to
recover *condition, circumstance, treatment*. `read`, not demonstrated.

**And it does not reach the reader today.** On the field path the presentation projection walks
through derived findings on `input` and `choice` pins only (`_leaf_pins`), and validates
citations only for the rule that owns a form field (`_require_declared_field_citation_chain`);
an intermediate conclusion and its citations are not emitted there. One path does emit an
intermediate derived finding's `citation` pins: the attachment-adjustment provenance walk
(`_recorded_derived_pin_identities` keeps `citation` and `computation` pins) writes them as
`citationSites` in `provenanceGroups` — the narrow precedent stage 3 recorded, limited to
nominee adjustment rows, and not read by the citation-walk page. So the claim is: **not emitted
on the path the reader reads**, rather than dropped everywhere.

So this narrows stage 3's open carrier question without closing it: of its three candidates,
read-time reconstruction from the durable record now has everything it would need on the
record. **It is not selected.** The carrier stays open until A6 tests one, and the responsibility
belongs to the same owed reader behaviour: A6's consumer recovering, at the reader, the
conclusion, its meaning, and the conditions it leaves to the filer.

## Handoff

**To stage 5** — what the filer paid in a shared-payment case — nothing new from this stage.

**To A6** — three reader test cases, each needing the default basis shown: the nine-credit case
and case 1 (a financing claim with no schooling circumstance), which also need the conditions
left to the filer shown; and case 2 (no financing claim; the statement-level conclusion), which
must show the default basis and must **not** show schooling conditions it has no circumstance
to bind to.

## Dependence on A4

| Depends on | Level |
| --- | --- |
| Rule citations pinned on the ordinary evaluation path and kept in the durable record | `read` — `pins_for`, `ledger_pins_for`, `derivation-record.v9` |
| Declared rule citations carried by a **per-key** publication | **untested**, and the existing per-item paths do not do it by default — part of the owed per-key publication |
| An applicability-gated rule recorded `inapplicable` when it does not apply | `read` — runner, record v9 disposition enum |
| One conclusion published per key of a single subject — student-and-period, borrowing, **and now statement** | **untested** — owed, `a4-bounds.md` |
| The conclusion and its conditions reaching the reader | **untested**, traced as not reached — owed to G2 and A6 |
| Telling "still resolvable" from "still supported" on a statement's composition change | **untested** — D9; may not be relied on |
| Holding that interval as its own state | **untested** — D10; may not be relied on |
