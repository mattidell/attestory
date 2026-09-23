# A5 stage 4 — scope claims and the responsibility applies-to relation

Part 1 provisional; **Part 2 not settled** — it returns a product choice to the owner and
leaves the representation at a preferred candidate. Filer-centered. No implementation. Two relations, each saying that something
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
worked messages, a product choice for the owner, and a comparison of representations.

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
for. The conditions apply (A0); nothing names their object. Two candidates, and the choice
between them is the owner's:

> **A.** *You are responsible for these conditions: that the school these loans paid for was an
> eligible institution; that the programme led to a recognised credential; and that your course
> load met that school's half-time standard. They apply because you claimed the student loan
> interest deduction for [statement]. You haven't said what these loans paid for, so the school
> isn't named here.*

> **B.** No condition message. Only the default basis stage 3 requires: *eligibility for this
> deduction is taken as met because nothing you described says otherwise.*

A third shape — inviting the person to describe their schooling — is excluded by A1's register:
the message "must not read as a question or as something to resolve here".

### The product choice returned to the owner

**What happens at the reader when a condition applies but the application cannot name its
school or programme?**

| | A — show it, bound to the statement, unnamed | B — show only the default basis |
| --- | --- | --- |
| A0 | Kept: the conditions apply and are shown | A0's applicability stands, but at the reader the conditions are silent where nothing names them. That changes what A0 means to the person, and is the owner's to decide, not this stage's |
| Responsibility direction | Bound to a treatment — this statement's interest — and says why it cannot be more specific. Not screen-level text, but not bound to a described circumstance either | Satisfies "bound to a circumstance" by never showing an unbound one |
| Who sees it | Case 2 is the **ordinary** return: a 1098-E and nothing else said. Under A nearly every filer claiming this deduction sees the conditions | Under B most filers never see them; only those who describe schooling do, which makes describing your schooling the way to acquire responsibilities |
| Reads as | Closer to a disclaimer, softened by naming the statement | Quieter; risks the silence stage 3 called a failure |

**Recommendation: A.** A0 says the conditions are the person's either way, and B would hide them
from exactly the people who said least — while showing them to people who volunteered more,
which rewards silence. A's binding to one statement and its plain reason for not naming the school
are what keep it from being screen-level boilerplate. **A0 is not changed by this stage under
either choice**; if the owner chooses B, A0's reader consequence is amended by that decision.

### Testing the citation-pin representation against the three conditions

The withdrawn selection carried responsibilities as the named conclusion's rule `citations`.
Tested against what a durable reader must recover for each condition:

| A durable reader must recover | Citation-only, on current artifacts |
| --- | --- |
| **Which condition applies** | **No.** `citation.v1` is a legal locator. Locator granularity is whatever content declares, so one citation to § 25A(b)(3) would stand for both credential and half-time. The credential condition runs through § 25A(b)(3)(A) to HEA § 484(a)(1), and the same authority backs the **adverse** enrolment determination stage 2 traced for spring 2025 — so one locator appears both as an applied rule and as a responsibility. Eligible institution rests on the definition in § 221(d)(2), which refers to § 25A(f)(2). Nothing maps a set of citations to a condition. No citation citizens for any of these exist in content today |
| **That these are responsibilities, not ordinary citations** | **No.** Same role, same list, same citizen type. "Pinned by a default conclusion" would distinguish them only if that rule cited nothing of its own — and it should cite its own authority, § 221(d)(1)(C) and (d)(3) |
| **The approved wording** | **No home.** `citation.v1` has no text. The rule's `notes` field is free developer text, not governed wording. The projector admits reader text only from a form field's label, description or citation, an attachment's title or itemization label, or a finding's evidence label — none is a condition message |
| **The circumstance it concerns** | **Partly.** The conclusion's input pins give the financing claim, hence institution, programme and period; which component each condition concerns is not carried |
| **The treatment it qualifies** | **Yes, by reverse join** in the durable record: the dispositions whose pins name the conclusion's finding id, up to the amount. `read` |

**Citation-only representation is unproven**, and on current artifacts it fails the first three
rows.

### Smallest viable alternatives, compared

| Alternative | Condition identity | Distinct from ordinary citations | Wording | Circumstance | Treatment | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| **One responsibility rule per condition**, each publishing a categorical finding per schooling situation (and per statement in case 2, if A is chosen) | The rule and its symbol | Yes — the rule *is* the condition, so its citations are that condition's authorities and nothing else's | **No home** — same gap as above | Input pins: the financing or scope claim, and the grain in the symbol's key | Input pin to the favourable conclusion, then reverse join | Three per-key publications per situation — the same owed mechanism, with its citation carriage also owed. No new schema to derive it. Never read by another rule, so never consumed |
| A fact type per condition, its `title` as wording and `identity_keys` as grain | Yes | Yes | Only by repurposing `title`, which today holds developer description and which the projector does not read | Via keys | Not by itself | Fact types type kernel findings, which are someone's assertion; a responsibility is not. Whether a derived symbol can carry a fact type's identity was not traced. Not smaller |
| A content declaration mapping each condition to its authorities, grain and wording | Yes | Yes | **Yes** — the only candidate with a governed home for approved wording | Via declared grain | Not by itself | Very likely a new citizen kind and schema |
| Wording held in A6's consumer, keyed by condition rule id | — | — | Yes, but owner-approved tax wording would sit in code, outside content governance | — | — | No schema. Pairs only with the first row |

**Preferred candidate, not selected:** the per-condition rule for identity, circumstance and
treatment, with the **wording home open** between a content declaration and A6's consumer. It is
not selected because the owner's case-2 choice changes what it publishes, and because every
column it satisfies depends on the owed per-key publication and has not run. Whether any schema
is needed is open with the wording home, and is not assumed.

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

**To the owner** — the case-2 choice above, A or B, with A recommended. And A1's candidate
responsibility message needs the half-time condition and a "because" clause per case before it
can be approved.

**To stage 5** — what the filer paid in a shared-payment case. Nothing from this part; stage 5
does not depend on the case-2 choice or the representation.

**To A6** — three reader test cases, each needing the default basis shown: the nine-credit case
and case 1, which also need each of the three conditions shown with its approved wording, the
circumstance it concerns and the treatment it qualifies, distinguishable from ordinary citations;
and case 2, whose condition display follows the owner's choice. The representation is the
preferred candidate above until something runs.

## Dependence on A4

| Depends on | Level |
| --- | --- |
| Rule citations pinned on the ordinary evaluation path and kept in the durable record | `read` — `pins_for`, `ledger_pins_for`, `derivation-record.v9` |
| Declared rule citations carried by a **per-key** publication | **untested**, and the existing per-item paths do not do it by default — part of the owed per-key publication |
| An applicability-gated rule recorded `inapplicable` when it does not apply | `read` — runner, record v9 disposition enum |
| One conclusion published per key of a single subject — student-and-period, borrowing, statement — and, under the preferred candidate, one responsibility finding per condition per situation | **untested** — owed, `a4-bounds.md` |
| A reader recovering, per condition, its identity, approved wording, circumstance and treatment, distinct from ordinary citations | **untested**; citation-only representation fails three of the five on current artifacts — owed to G2 and A6 |
| Telling "still resolvable" from "still supported" on a statement's composition change | **untested** — D9; may not be relied on |
| Holding that interval as its own state | **untested** — D10; may not be relied on |
