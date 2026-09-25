# A5 stage 4 — scope claims and the responsibility applies-to relation

Part 1 provisional. Part 2: the owner's case-2 choice is recorded (A); the representation is a
provisional candidate for A4's second pass to execute and challenge. Filer-centered. No implementation. Two relations, each saying that something
**applies to** something else, and they are kept apart because they have different bases:

- a **scope claim** is the filer's — they say a circumstance, or an answer, reaches some
  population of reported interest. It is a telling, `attested`.
- a **responsibility** is the application's — a condition applies because a deduction was taken
  on a default-supported eligibility value (A0). Nobody asserts it; it is derived, and it
  establishes nothing.

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

**Not settled.** An earlier version of this part selected a representation and said no
responsibility applies in case 2. Both are withdrawn below: the case-2 claim contradicted A0, and
the representation does not carry what a reader needs. What remains is a distinction, three
worked messages, the owner's case-2 choice, and a comparison of representations.

The named consumer is A6's revealing consumer, which must let the person see each condition that
applies, why, and what it concerns.

### A condition applying, and the application being able to name it

**A0 is unchanged and governs applicability.** F6: institutional eligibility, credential
recognition and the half-time standard "stay the person's responsibility either way — producing
the value manufactures no finding establishing them." So wherever a deduction is taken on a
favourable eligible-student value that came from the default, **the three conditions apply** —
in the nine-credit case, in case 1, and in case 2 alike.

**What a described circumstance changes is not whether they apply but what the application can
say about them.** Two things were run together in the withdrawn claim:

- **Whether a condition applies** — fixed by A0 and the treatment taken. It does not depend on
  anything the person described.
- **Whether the application has the context to name its object** — which school, which
  programme, whose half-time standard. That depends entirely on what the person said, and it
  varies by case.

The responsibility direction's rule against "generic disclaimer text attached to a screen" is a
rule about the **second**: a condition must be bound to the treatment and, where known, the
circumstance that made it applicable. It is not a rule that a condition stops applying when the
circumstance is unknown. Reading it that way was the error.

### The three cases, through the actual message

A1's approval set carries one candidate message, not yet approved:

> *You are responsible for this condition: that the school was an eligible institution and the
> programme led to a recognised credential. It applies because you claimed the student loan
> interest deduction and described studying at [institution] in [period].*

Worked through the three cases, it has two problems before any product choice: it omits the
half-time standard, one of A0's three conditions; and its "because" clause is **true only in the
first case**. The candidates below keep A1's register — it tells someone a condition is theirs
and claims nothing about whether it is met — and vary only what each case supports. All wording
remains the owner's.

**The nine-credit case.** The person said they were enrolled in the BSc and the certificate
programme at Riverside in autumn 2024, nine credits in all, and a financing claim names the
period.

> *You are responsible for these conditions: that Riverside College was an eligible institution;
> that the programme you were pursuing led to a recognised credential; and that your course load
> met Riverside's half-time standard for that programme. They apply because you claimed the
> student loan interest deduction for [statement] and **described enrolling at Riverside College
> in autumn 2024**.*

True as stated. Institution and programmes can be named because the person named them. The
third condition is stated against the course of study, which is where the standard attaches
(stage 2, test 3), and says nothing about whether nine credits met it.

**Case 1 — a financing claim, no attendance or enrolment telling.** The person said only
*this loan paid my tuition for the Riverside BSc in autumn 2024.*

> *You are responsible for these conditions: that Riverside College was an eligible institution;
> that the BSc led to a recognised credential; and that your course load met Riverside's
> half-time standard. They apply because you claimed the student loan interest deduction for
> [statement] and **said this loan paid for the Riverside BSc in autumn 2024**.*

The institution and programme can still be named — the financing claim's key carries them — but
the "because" clause must say what the person actually said. *"You described studying at
Riverside"* would attribute an enrolment telling nobody gave, which is the same misattribution
stage 3 traced at the citation layer, now in words.

**Case 2 — a bare statement.** Nothing about schooling and nothing about what the loans paid
for. The conditions apply (A0); nothing names their object, and nothing says the loans paid for
any particular school. The wording must not imply otherwise — an earlier candidate spoke of
*"the school these loans paid for"*, which presupposes one known school.

A short default-basis note in the ordinary return view:

> *Eligibility for this deduction is taken as met because nothing you've described says
> otherwise.*

And, where the person examines the deduction for this statement, the conditions:

> *You are responsible for these conditions on the interest reported on [statement]: that
> whatever education these loans paid for was at an eligible institution; that it was in a
> programme leading to a recognised credential; and that the course load met that institution's
> half-time standard. They apply because you claimed the student loan interest deduction for this
> statement. Which school and programme are not known here — nothing you've described names
> them.*

Candidate wording; approval is the owner's.

### The owner's choice: A

The owner chose **A** for inspectable content (2026-09-23). The comparison that informed it:

| | A — show it, bound to the statement, unnamed | B — show only the default basis |
| --- | --- | --- |
| A0 | Kept: the conditions apply and are shown | A0's applicability stands, but at the reader the conditions are silent where nothing names them |
| Responsibility direction | Bound to a treatment — this statement's interest — and says why it cannot be more specific | Satisfies "bound to a circumstance" by never showing an unbound one |
| Who sees it | Case 2 is the ordinary return; nearly every filer claiming this deduction can see the conditions | Only those who describe schooling see them, which rewards silence |

**What the choice fixes at the reader:**

- **Where the conditions appear.** When the person examines the deduction for a bare 1098-E,
  the three applicable conditions are shown, tied to that statement, with the school and
  programme **explicitly unknown**. The ordinary return view may carry only the short
  default-basis note and reveal the conditions in a contextual explanation.
- **What they must not become.** Not questions, not required confirmations, and not a generic
  screen-wide warning. They are bound to the statement's treatment and read as information.
- **A0 is unchanged**, and its reader consequence is what A0 already said: the conditions are
  the person's either way.

**What the choice does not establish.** How each condition's identity, its approved wording and
the carrier to the reader are realised — which the next two sections show a citation-only
representation cannot do on current artifacts — stays something **G2 and A6 must demonstrate**.
This is a decision about what the reader shows, not evidence that it can.

### Testing the citation-pin representation against the three conditions

The withdrawn selection carried responsibilities as the named conclusion's rule `citations`.
Tested against what a durable reader must recover for each condition:

| A durable reader must recover | Citation-only, on current artifacts |
| --- | --- |
| **Which condition applies** | **No.** `citation.v1` is a legal locator. Locator granularity is whatever content declares, so one citation to § 25A(b)(3) would stand for both credential and half-time. The credential condition runs through § 25A(b)(3)(A) to HEA § 484(a)(1), and the same authority backs the **adverse** enrolment determination stage 2 traced for spring 2025 — so one locator appears both as an applied rule and as a responsibility. Eligible institution rests on the definition in § 221(d)(2), which refers to § 25A(f)(2). Nothing maps a set of citations to a condition. No citation citizens for any of these exist in content today |
| **That these are responsibilities, not ordinary citations** | **No.** Same role, same list, same citizen type. "Pinned by a default conclusion" would distinguish them only if that rule cited nothing of its own — and it should cite its own authority, § 221(d)(1)(C) and (d)(3) |
| **The approved wording** | **No home.** `citation.v1` has no text. The rule's `notes` field is free developer text, not governed wording. The projector's own rule for reader strings (module docstring): every string is either a value the coordinator itself published or recorded, or content declared on a resolved citizen — a form field's label, description or citation, an attachment's title or itemization label, or a raw finding's evidence label. None of the declared sources is a condition message. A published value reaches the model as a form field's value, or inside the nominee-adjustment provenance text (`provenanceGroups`, not read by the citation-walk page); a responsibility finding's value would reach neither |
| **The circumstance it concerns** | **Partly.** The conclusion's input pins give the financing claim, hence institution, programme and period; which component each condition concerns is not carried |
| **The treatment it qualifies** | **Yes, by reverse join** in the durable record: the dispositions whose pins name the conclusion's finding id, up to the amount. `read` |

**Citation-only representation is unproven**, and on current artifacts it fails the first three
rows.

### Smallest viable alternatives, compared

| Alternative | Condition identity | Distinct from ordinary citations | Wording | Circumstance | Treatment | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| **One responsibility rule per condition**, each publishing a categorical finding per schooling situation (and per statement in case 2, since A was chosen) | The rule and its symbol | Yes — the rule *is* the condition, so its citations are that condition's authorities and nothing else's | **No home** — same gap as above | Input pins: the financing or scope claim, and the grain in the symbol's key | Input pin to the favourable conclusion, then reverse join | Three per-key publications per situation — the same owed mechanism, with its citation carriage also owed. No new schema to derive it. Never read by another rule, so never consumed |
| A fact type per condition, its `title` as wording and `identity_keys` as grain | Yes | Yes | Only by repurposing `title`, which today holds developer description and which the projector does not read | Via keys | Not by itself | Fact types type kernel findings, which are someone's assertion; a responsibility is not. Whether a derived symbol can carry a fact type's identity was not traced. Not smaller |
| A content declaration mapping each condition to its authorities, grain and wording | Yes | Yes | **Yes** — the only candidate with a governed home for approved wording | Via declared grain | Not by itself | Very likely a new citizen kind and schema |
| Wording held in A6's consumer, keyed by condition rule id | — | — | Yes, but owner-approved tax wording would sit in code, outside content governance | — | — | No schema. Pairs only with the first row |

**Provisional candidate for A4's second pass — not an adopted contract:** the per-condition rule
for identity, circumstance and treatment, with the **wording home open** between a content
declaration and A6's consumer. Every column it satisfies depends on the owed per-key publication
and has not run, so it is not selected on paper. A4's second pass executes and challenges it;
**after those checks A5 selects it with reasons, revises it, or reports an explicit partial
result.** Whether any schema is needed is open with the wording home, and is not assumed.

### What still holds from the withdrawn selection

These were argued for the citation shape; each carries to the per-condition rule unchanged,
and none is demonstrated.

- **Lifecycle: re-derivation, no separate state.** A responsibility applies while the favourable
  conclusion it rests on is published from current findings. An adverse circumstance makes the
  conclusion inapplicable and the responsibility lapses. Horizon identity-keying was weighed and
  not taken: it displaces rather than re-derives, and a responsibility has no
  *findable-but-unsupported* state — it is not the person's claim, so A2's third leg never arises.
  Where A2 holds part of a figure unresolved, that part's treatment is not taken and no
  responsibility applies to it meanwhile; nothing here needs D10.
- **Inside provenance, never as an input.** Under the per-condition rule each responsibility is
  its own derived finding with its own disposition row; nothing reads it, so nothing consumes it.
- **Does not reach the reader today.** On the field path the projector walks through derived
  findings on `input` and `choice` pins and validates citations only for the rule owning a form
  field; a finding nothing pins is not reached at all. The attachment-adjustment
  `provenanceGroups` walk is the one place intermediate citation pins are emitted, limited to
  nominee rows and not read by the citation-walk page. The reader carrier stays open (stage 3).

## Handoff

**To the owner** — approval of the per-case candidate wording above. A1's single candidate
responsibility message lacked the half-time condition and had a "because" clause true only in the
nine-credit case; the three candidates here replace it for approval.

**To stage 5** — nothing from this part.

**To A6** — three reader test cases, each needing the default basis shown: the nine-credit case
and case 1, which also need each of the three conditions shown with its approved wording, the
circumstance it concerns and the treatment it qualifies, distinguishable from ordinary citations;
and case 2, where the three conditions are shown tied to the statement with school and programme
explicitly unknown — in a contextual explanation behind a short default-basis note, never as a
question, a required confirmation or a screen-wide warning — with each condition's identity,
approved wording and the treatment it qualifies recoverable, and its circumstance shown as
unknown rather than recovered. The representation is the provisional candidate above, for A4's second pass to execute and
challenge before A5 selects, revises or reports it partial.

## Dependence on A4

| Depends on | Level |
| --- | --- |
| Rule citations pinned on the ordinary evaluation path and kept in the durable record | `read` — `pins_for`, `ledger_pins_for`, `derivation-record.v9` |
| Declared rule citations carried by a **per-key** publication | **untested**, and the existing per-item paths do not do it by default — part of the owed per-key publication |
| An applicability-gated rule recorded `inapplicable` when it does not apply | `read` — runner, record v9 disposition enum |
| One conclusion published per key of a single subject — student-and-period, borrowing, statement — and, under the provisional candidate, one responsibility finding per condition per situation | **untested** — owed, `a4-bounds.md` |
| A reader recovering, per condition, its identity, approved wording, circumstance and treatment, distinct from ordinary citations | **untested**; citation-only representation fails three of the five on current artifacts — owed to G2 and A6 |
| Telling "still resolvable" from "still supported" on a statement's composition change | **untested** — D9; may not be relied on |
| Holding that interval as its own state | **untested** — D10; may not be relied on |
