<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "nominee-interest-ownership-translation",
  "milestone_state": "planned",
  "status": "Selected and planned. Gates P1 (framing and product value) and P2 (tax and artifact evidence) are both COMPLETE and their findings are absorbed into this plan; Gate P3 (experiments and track decomposition) is COMPLETE and its findings are absorbed, so all three planning gates are closed and a Track 0 charter may be issued. P3 found that no case in N1a-N12 supplies a material product discriminator between the R-A and R-B representations, so the rival comparison is dropped and the representation choice is deferred; that the authorized evidence rung is PAPER with no executable prototype pre-authorized; that N5 is a paper transfer test against ADR-0070 Decisions 8-10 rather than two prototypes; and that the durable-publication gap is orthogonal, so Track 0 observes run-local RunResult provenance. P2 established the Schedule B reduction predicate (belonging, expressly applicable even if the income was later distributed) and found THREE authority-specific information-reporting formulations -- the literal IRC 6049(a)(2) conjunction with its $10 threshold, the form instructions' belonging/allocable-amount language, and the regulation's middleman/actual-ownership/credited-or-set-apart language -- whose relationship no retrieved source reconciles. No single normalized reporting predicate is established; P3 may test the separation of consequences but must not choose among or combine the formulations, and if implementation appears to require a unified predicate the owner may select qualification, refusal, separately attributed guidance, deferral, or further research, but cannot determine unresolved law -- a legally normalized predicate requires adequate authoritative reconciliation, and absent that the honest milestone result is partial. P2 also found no clean beneficial-ownership test, verified that committed arithmetic and rendering consume the legacy nominee fact when present, and found no ordinary-language producer of it in the searched committed production areas (bounded Branch B). P1 closed the negative-answer question -- an explicit no is a transient interaction response creating no durable allocation fact -- and required an ordinary-circumstance disambiguation before any nominee allocation is captured, because a bare who/how-much cannot separate nominee ownership from a bond buyer reimbursing a seller for accrued interest (N9b). Planning review is deliberately staged before Track 0: framing, evidence architecture, and experiment/track decomposition are reviewed independently and repaired in the plan before any implementation charter is issued. The milestone tests whether the document-and-ordinary-fact translation method transfers from accrued interest to nominee interest: a payer reports interest to the taxpayer, but a stated share actually belongs to another person. That legacy consumer path does not represent the owner, connect the allocation to a report or source-independent interest circumstance, derive the adjustment from ordinary facts, or surface the information-reporting consequence. The plan does not assume the Schedule B reduction and the information-reporting obligation share a factual predicate, and P2 established none; the paired cases N10 (ownership without established payment) and N12 (payment without established ownership) keep that assumption falsifiable in both directions, and their non-inference requirements are selected invariants. No production shape is selected by this plan.",
  "scope": [
    "model 2025 Form 1099-INT box-1 reports across bounded interaction and evidence conditions: no recorded nominee allocation and no response to the ownership question (N1a); an explicit negative response (N1b); one or more affirmative allocations to non-spouse actual owners (N2, N4); full allocation away from the taxpayer (N3); and two distinct same-payer reports in one tax year with an allocation attached to only one of them, both where that allocation is supportable on its own report (N11a) and where it is not (N11b). These describe interaction and evidence conditions, not findings about who owns the interest in the world; an unanswered question establishes no ownership proposition either way",
    "preserve the payer report as documentary evidence while eliciting ordinary ownership and allocation facts without asking the user to supply a preclassified Schedule B adjustment",
    "determine whether the canonical translation seams accepted for accrued interest transfer unchanged, require parameterized extension, or expose a genuinely new identity, allocation, authority, lifecycle, or interaction decision",
    "derive and explain the taxpayer's nominee-distribution reduction, and determine what separately establishes the information-reporting obligation rather than assuming it shares the reduction's predicate (N10 and its converse N12, in which a transfer alone establishes no ownership), without implementing Forms 1096 or 1099-INT filing",
    "compare the canonical result with the current legacy nominee-adjustment path, preventing omission and double subtraction while preserving published history",
    "use the smallest executable evidence that discriminates viable representations, then charter production only if no consequential semantic decision remains"
  ],
  "non_goals": [
    "no joint-return or spouse-allocation model; the spouse exception is a named boundary rather than an invented subject rule",
    "no trusts, custodial accounts, minors, foreign owners, disputed ownership, backup withholding, or comprehensive information-return filing system",
    "no general allocation ontology and no claim that nominee interest exhausts ownership or allocation questions",
    "no reopening of standing workspace authorization, per-family confirmation, later-year basis reuse, or the deferred adjusted-basis representation choice",
    "no replacement of the current Schedule B nominee path before compatibility and migration behavior are demonstrated",
    "no schema, ADR, package, or production implementation before the plan's three planning-review gates and Track 0's evidence gates are satisfied"
  ],
  "deep_reads": {
    "implementation": [
      "docs/adr/0010-derived-finding-projection-and-currency.md",
      "docs/adr/0009-derived-finding-shape.md",
      "OWNER_MODEL.md#The Product Model",
      "OWNER_MODEL.md#The Domain Model Model",
      "docs/domain-models/taxable-interest-translation.md#The plain-language stratum",
      "docs/adr/0068-acquisition-report-identity-association.md",
      "docs/adr/0070-accrued-amount-supportability-rule.md",
      "docs/adr/0071-rule-owned-current-year-and-basis-consequences.md",
      "docs/adr/0072-legacy-pairing-scoped-interest-coexistence.md",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-ownership-translation.md#Planning review cycle",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-ownership-translation.md#Fixed product cases",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-ownership-translation.md#Evidence and experiment architecture",
      "PROJECT_PLANNING.md#Frontier Reduction and Direct-Build Routing",
      "PROJECT_PLANNING.md#Prototype Economic Gates",
      "PROJECT_PLANNING.md#Track 0 Adversarial Closure Gate",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/adr/0010-derived-finding-projection-and-currency.md",
      "docs/adr/0009-derived-finding-shape.md",
      "OWNER_MODEL.md#The Product Model",
      "docs/domain-models/taxable-interest-translation.md#The plain-language stratum",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-ownership-translation.md#Planning review cycle",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-ownership-translation.md#Fixed product cases",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-ownership-translation.md#Success and stop conditions",
      "docs/roles/qualitative-review.md",
      "AGENTS.md#Data Safety Rules"
    ]
  }
}
-->

# Nominee Interest Ownership Translation

## Milestone identity

- Phase: Tax Concept Derivation
- Milestone key: `nominee-interest-ownership-translation`
- Primary branch: `milestone/nominee-interest-ownership-translation`
- State: planned; no implementation track is chartered
- Roadmap role: Adjacent Translation Case, the first normalization test

## Plain-language purpose

A bank may send the taxpayer a Form 1099-INT showing `$1,200`, even though
`$450` of that interest actually belongs to another person. The form is not
necessarily wrong: it reports what the payer paid under the name or account it
used. The taxpayer still reports the full form amount on Schedule B, identifies
the portion received as a nominee, subtracts that portion, and reports `$750`
as their own interest from that item.

Committed content already contains arithmetic and rendering behavior that can
consume a legacy “Nominee Distribution” adjustment fact **when that fact is
present**. Two things follow, and they must be kept apart.

First, that path gets the arithmetic right only once ordinary life has already
been translated into tax-form terminology and reduced to a tax adjustment.
Second, **Gate P2 found no ordinary-language producer of that fact in the
searched committed production areas** — a bounded Branch B result recorded in the
table below, which does not claim that no producer exists anywhere. The gap is
missing behavior, not missing evidence of a hidden producer there.

This milestone asks the product to perform the translation instead.

The interaction must not presuppose its own answer. The product asks a
gating question first, and pursues the circumstance only if the answer is yes:

> **First:** “Does any of the interest on this form belong to someone else?”

Asking “this form includes interest that belongs to someone else — who?”
would assert the existence of another owner and lead the user into confirming
it. The gating question leaves “no” as an ordinary, unremarkable answer.

**What “belong to” rests on (Gate P2, dependency D1).** P2 searched the
retrieved authorities and found **no clean beneficial-ownership test**. The
operative words throughout are “actually belongs to someone else,” “actual
owner,” “amounts that actually belong to another person,” and “actually owned by
another person” — used without a definition. Publication 550's sibling example
(deposit share plus a sharing agreement, the Form 1099 issued under the
taxpayer's SSN) illustrates one ordinary pattern; it is explanatory, not a test.

The product may therefore treat an affirmative answer as **the bounded evidence
it has selected to support its Schedule B classification** — the user's
attributed ordinary statement that some of the interest reported in their name on
this form is actually another person's, given **after** the N9b circumstance
routing below. **A user's assertion does not make the real-world legal condition
true.** The account is layered, and **Track 0 must preserve the layers** as a
**semantic requirement** (no schema is selected here):

- the **adopted fact type and the derived fact lattice define the canonical
  question** — what may be asserted, and about what — **independently of any
  author**;
- the **finding supplies the answer**: `finding.v2` carries `fact_id`, `value`,
  `basis`, `evidence_ids`, and optional `pins`. It carries **no actor and no
  timestamp**;
- the **enclosing assertion act supplies attribution**: `act.v1` carries `actor`,
  `at`, and `committed_against` (the revision), with `act-assertion.v2` as the
  `payload` wrapping the `finding`. **Who said it and when lives on the act, not
  in the finding**;
- a **derived finding separately carries the rule-produced tax value**:
  `derived-finding.v2` carries `symbol`, `value`, `version`, and `pins`, and has
  **no actor and no human `basis`**. ADR-0009 does **not** say its authority
  exists independently of an author. It says `basis` is the kernel's vocabulary
  for the grounds of a *human* determination, that a derived finding's ground is
  instead mechanical and fully pinned, and that its authority is carried by an
  attribution chain — **pins → publication act → adoption act → user** — which
  **ultimately reaches the adopting user**. The author is reached *through the
  chain*, not absent from it (ADR-0009, ADR-0010);
- so a rule may derive canonical tax meaning — the supported nominee-reduction
  amount and the taxpayer's remainder — from the payer report together with the
  attributed ordinary finding, and the result is **a derived determination with a
  walkable chain, not merely another user assertion**.

Attribution therefore belongs to the **act**, the answer to the **finding**, the
question to the **fact type and lattice**, and the derived tax value to the
**derived finding** — unless authorship is itself the proposition being modelled.
**Track 0 must preserve that placement and must not relocate attribution into the
proposition.** No nominee schema is selected here. What the user supplies is **not** a legal
nominee classification, a determination that any information-reporting
formulation is satisfied, or proof of title, registration, or cash movement.

The **owner may choose the product posture** — qualification, refusal, separate authority-indexed guidance, deferral, or seeking further authoritative reconciliation. The **owner does not determine what unresolved law means.** A claim that one normalized predicate is legally correct **requires adequate authoritative reconciliation**; if that is required and unavailable, the honest milestone result is a **partial result**, not a convenient normalization. The product, not the user,
applies “Nominee Distribution.” The absence of a legal test is a recorded
finding, not a defect to be repaired by inventing one.

**An affirmative answer does not yet identify a nominee circumstance**, and the
product must not proceed straight to “who and how much.” Case N9b is the
falsifying control: a bond buyer who reimbursed the seller for accrued interest
the form will report to them can answer the gating question with almost exactly
the sentence a nominee case produces. “Who and how much” alone cannot tell those
apart, and capturing an allocation at that point would manufacture a nominee
reduction out of a purchase reimbursement.

So an affirmative answer leads to an **ordinary-circumstance disambiguation
before any nominee allocation is captured.** The intake must elicit enough
ordinary context to route the circumstance to one of:

- interest **received or held for another owner** — the nominee circumstance
  this milestone models;
- a **bond purchase in which the buyer reimbursed the seller** for accrued
  interest — routed to the accrued-interest translation already accepted for
  this phase;
- **another or uncertain circumstance** — requiring qualification or follow-up
  rather than a default into either of the above.

**Gate P2 established that this is a real circumstance split**, not a
presentational nicety. Schedule B lists nominee receipt and accrued interest as
**separate** Who-Must-File bullets and as separately labelled subtractions —
“Nominee Distribution” for interest belonging to another, “Accrued Interest” for
amounts paid to a seller, which the instructions say is “taxable to the seller.”
Publication 550 (*explanatory*) treats the buyer's pre-purchase accrual as a
**return of capital reducing basis**. The committed accrued-interest path
publishes **two** consequences from `accrued_interest_paid_to_seller` — a
current-year adjustment and an item-level basis consequence — while the legacy
nominee type carries no acquisition date, seller, basis publication, or report
association. The two differ in **facts, label, taxable person, and companion
consequence**, and similar ordinary language can produce either:

| Ordinary fact | Nominee ownership | Accrued-interest reimbursement (N9b) |
| --- | --- | --- |
| Who the other person is | the actual owner of that interest | the seller of the obligation |
| Acquisition of the instrument | not the distinguishing event | purchase between interest payment dates |
| Who is taxed on that slice | the actual owner | the seller |
| Companion consequence | a possible information return to the owner, on its own predicate | basis reduction for the buyer |

This is a required product property, not interface copy: the plan does not
prescribe wording, screens, or ordering beyond the constraint that routing
context is elicited before an allocation is taken. This resolves into a **bounded T0-A paper requirement**: elicit the
circumstance **before** an allocation is captured, route the N9b accrued-interest
circumstance **away from** nominee treatment, and **never ask the user to choose
a tax label**. That is the whole requirement — Track 0 does not design production
intake, screens, or wording. The user is asked about their
circumstances in ordinary terms and is **never asked to pick a tax label** or to
say which translation applies.

The invariant governing a negative answer is **asymmetric**:

- **silence or absence is never attributed to the user as a denial** — this is
  unconditional;
- during the **active interaction**, the product may acknowledge the answer the
  user has just given;
- **after the interaction, “no” supplies no durable workspace claim.** Gate P1
  decided that retaining an explicit negative earns nothing that pays for a
  durable representation and its lifecycle;
- the durable state therefore **converges with N1a**;
- later explanations may say only that **no nominee allocation is recorded** —
  never that the user previously denied other ownership.

The two directions are not symmetric, and that is the point: an affirmative
answer opens a disambiguation, while a negative answer closes the interaction
without leaving a claim behind.

Throughout, the division of labor is fixed: **the user supplies an ordinary
account of who owns what, and the product supplies the tax classification.**
The user is never asked for the words “nominee distribution,” for a Schedule B
line, or for a tax result.

The application should preserve what the payer reported, preserve what the
user says about actual ownership, apply the adopted rule, and explain the
resulting taxpayer share. Where the conditions for nominee information reporting
are established, it should separately surface that consequence. **Gate P2
established no shared predicate**: the Schedule B reduction rests on belonging,
while the reporting formulations remain authority-indexed and unreconciled, and
this milestone **preserves that separation** rather than treating it as a
question still to be settled. It must not treat forwarding money, sharing an account,
or naming a person as proof of beneficial ownership without an accountable user
statement.

## The abstract product question

Does the established translation method generalize from a purchase
circumstance to an ownership-allocation circumstance?

That question breaks into four decisions:

1. **Canonical proposition.** What ordinary proposition should persist: an
   allocation of one reported amount, an allocation of a source-independent
   interest receipt, an ownership relationship, or some combination?
2. **Identity and cardinality.** What identifies the taxpayer, each actual
   owner, the economic interest being allocated, and the payer report; and how
   can several owners or several reports coexist without accidental merging?
3. **Authority and supportability.** What does the user actually assert, what
   does the payer report establish, and what prevents allocated-away amounts
   from exceeding the amount to which they apply?
4. **Consequences.** Do the Schedule B reduction and the nominee
   information-reporting obligation rest on the same factual predicate, or does
   the reporting obligation require something the reduction does not — an
   onward payment, credit, or distribution to the other owner? **Gate P2
   answered this and the answer is asymmetric:** Schedule B's belonging
   condition is established for the return reduction, while literal
   § 6049(a)(2), the IRS filing instructions, and 26 CFR 1.6049-4 retain
   **separate authority-indexed formulations** and no single reporting predicate
   was established. So the live question is how **each separately supported
   proposition produces its own consequence, provenance, and explanation**, with
   its own authority and correction behavior — and what additional ordinary fact
   the payment-conjunct formulation requires. The milestone does not assume a
   shared predicate or a single supporting proposition, and **does not attempt to
   settle the legal interpretation**.

The purpose is not to minimize the number of model layers. It is to determine
which layer owns each proposition so the user is not asked to perform the tax
classification and the engine does not mistake a document report for economic
ownership.

## Why this case is next

Nominee interest is materially different from accrued interest while remaining
small enough to execute:

- accrued interest translates a purchase event into two tax consequences;
- nominee interest translates an ownership allocation into a return reduction
  supported by belonging, and may separately give rise to an
  information-reporting obligation whose formulations remain authority-indexed
  and unreconciled — so the test is whether the **translation method can preserve
  consequences with differently established or unresolved support**, not whether
  executable evidence can settle legal interpretation;
- both begin with a payer report and an ordinary user statement;
- both must associate facts, enforce an amount boundary, derive rather than ask
  for the tax adjustment, preserve provenance, and coexist with a legacy
  Schedule B adjustment path.

This makes nominee interest a direct test of whether the prior method is a
reusable product cadence or a bond-purchase-specific success. The alternative
roadmap candidates are deliberately deferred:

- the Series EE/I education exclusion combines bond eligibility, qualified
  expenses, ownership, filing status, and income limitation;
- bond-premium amortization adds an election and basis lifecycle;
- either would make a failed transfer difficult to attribute to one cause.

## Current committed behavior to preserve and challenge

The plan records this as a starting hypothesis to be re-read and tested during
planning review and Track 0, not as proof supplied by a filename.

| Layer | Current artifact and fields | What it establishes | What it does not establish |
| --- | --- | --- | --- |
| Report | `f1099int.bundle.json`: box-1 fact identity is payer + statement + tax year; value is the reported number | A particular payer statement reported an amount | Who economically owns any portion |
| Legacy nominee input | `scheduleb-adjustment.nominee.bundle.json`: value is a nonnegative amount; identity is tax year + generic adjustment instance | A fact type exists that can carry a preclassified nominee adjustment amount | That any surface exists by which a user can contribute one; actual-owner identity, report association, allocation basis, or why the amount belongs elsewhere |
| Legacy family and admission | `family.scheduleb-adjustment.nominee.json` and `closure-mapping.scheduleb-adjustment.nominee.json` | Current, closed adjustment members authorize the subtotal | That the family is a canonical ownership model or that its closure is product-appropriate |
| Computation | `rule.scheduleb-adjustment.nominee-subtotal.json` collects and sums the legacy amounts | A nominee subtotal can be calculated | How any member was derived from ordinary facts |
| Return | `rule.form1040-line2b.v6.json` subtracts that subtotal; `rule.attachment.schedule-b.v5.json` renders nominee rows | The current line-2b and Schedule B paths consume the subtotal | A production intake path, actual-owner explanation, or information-return consequence |
| Intake | **Branch B, bounded.** Gate P2 searched the committed production areas — all Python under `packages/derivation/` (including `entry_loop.py`, a W-2 Box 1 slice), `packages/tax/` (including `obligation_acquisition_mapping.py`, whose ordinary answers are accrued-interest only and fail closed on unrecognized fields), `packages/kernel/`, `packages/presentation/`, `packages/sample_data/entry_loop_t1/`, and `tools/*.py`, plus a repository grep for the amount fact-type id | **No ordinary-language producer of the legacy nominee amount was found in those searched areas.** The gap is missing behavior, not missing evidence of a hidden producer there. Attested amounts reach the engine only through the generic contribution path used by tests, and the `tools/` fixture generators, neither of which is a product surface | **Not** that no producer exists anywhere, and **not** that this milestone is the only possible product path. P2's exclusions stand: uncommitted or local UI, `archive/`, binary and media files, and any mapper writing the fact under a different identifier were not searched |

The current path is a compatibility baseline, not the selected canonical
design. A later implementation must not double-subtract if both legacy and new
representations are present, and must not silently convert an old adjustment
into a richer ownership claim it never contained.

## Tax and administrative boundary

**Gate P2 verified this boundary against retrieved primary and official
sources.** What follows records what P2 established, with authority levels kept
distinct. The sources and their locators are listed here so this account remains
supportable after the working P2 review record is removed at publication
curation.

### Sources and locators

| Source | Locator used | Authority level |
| --- | --- | --- |
| [2025 Instructions for Schedule B (Form 1040)](https://www.irs.gov/instructions/i1040sb) ([PDF](https://www.irs.gov/pub/irs-pdf/i1040sb.pdf)) | Part I, **“Nominees”**; Part I, **“Accrued interest”**; the TIP following the Nominees paragraph; General Instructions, **“Use Schedule B (Form 1040) if any of the following applies”** | form instruction |
| [IRC § 6049](https://uscode.house.gov/view.xhtml?edition=prelim&num=0&req=granuleid%3AUSC-prelim-title26-section6049) | **§ 6049(a)(1)** (persons who make payments of interest) and **§ 6049(a)(2)** (nominee receipt together with payments); definition of interest at § 6049(b) | statute |
| [26 CFR 1.6049-4](https://www.ecfr.gov/current/title-26/section-1.6049-4) | **(a)(2)** payor including collector/middleman; **(d)(6)(i)** interest deemed paid when credited or set apart; **(f)(4)** definition of *middleman* and the actually-owned-portion sentence with its spouse exception | regulation |
| [2025 General Instructions for Certain Information Returns](https://www.irs.gov/instructions/i1099gi) | Part A, **“Who Must File” → “Nominee/middleman returns”** | form instruction |
| [Instructions for Forms 1099-INT and 1099-OID](https://www.irs.gov/instructions/i1099int) ([PDF](https://www.irs.gov/pub/irs-pdf/i1099int.pdf)) | **“Who Must File”**; **“When is a payment made?”**; Specific Instructions for Form 1099-INT | form instruction |
| [IRC § 61(a)(4)](https://uscode.house.gov/view.xhtml?edition=prelim&num=0&req=granuleid%3AUSC-prelim-title26-section61) | § 61(a)(4), interest as gross income | statute |
| [Publication 550](https://www.irs.gov/publications/p550) | Chapter 1, **“Nominee distributions”**; **“Bonds Sold Between Interest Dates”**; **“Accrued interest on bonds”** | **IRS publication — explanatory corroboration, not controlling law** |

Quoted operative text for each is preserved in the P2 review record while that
record exists; the locators above are sufficient to re-retrieve every source
independently.

### A1 — what establishes the Schedule B reduction

The **2025 Instructions for Schedule B (Form 1040)**, Part I, "Nominees"
(*form instruction*) condition the reduction on interest reported in the
taxpayer's name that **actually belongs to someone else**. The taxpayer reports
the full Form 1099-INT amount on line 1, enters "Nominee Distribution" below the
subtotal, subtracts it, and carries the result to line 2.

The instructions expressly direct that the full amount be reported on line 1
**"even if you later distributed some or all of this income to others."** The
condition the instruction states is belonging, **not** a subsequent distribution.
The attributed ordinary statement is the bounded evidence the product accepts to support applying the Schedule B classification. The resulting reduction is a **supported tax determination** whose provenance identifies the assertion, payer report, rule, and authority; it is **not an independently proven beneficial-ownership finding**. Publication 550 (*explanatory, not controlling*)
corroborates the same subtraction as "the amount that actually belongs to
someone else" and adds no payment condition.

**Operative reporting instruction for completing Schedule B.** These are form
instructions telling a filer how to complete the schedule; the plan does not
present them as controlling tax law. No retrieved statute states the "Nominee
Distribution" row as such. IRC § 61(a)(4)
(*statute*) supplies only that interest is gross income.

### A2 — what establishes the information-reporting obligation

**P2 did not establish one normalized information-reporting predicate.** It
retrieved three formulations, each with its own authority level and operative
consequence. They are recorded separately and are **not** reconciled here.

| # | Formulation | Authority | Operative consequence |
| --- | --- | --- | --- |
| 1 | **IRC § 6049(a)(2), read literally** — a person who receives payments of interest **as a nominee** *and* who **makes payments aggregating $10 or more** during the calendar year to another person **with respect to the interest so received** | statute | A return setting forth the aggregate amount of such payments and the name and address of the person paid. Two conjuncts and a threshold. |
| 2 | **2025 General Instructions for Certain Information Returns**, "Nominee/middleman returns"; and the Schedule B TIP | form instruction | Receiving a Form 1099 for "amounts that actually belong to another person" makes the recipient a nominee who must file one return per other owner "showing the amounts allocable to each," with a spouse exception. These paragraphs do **not** restate a later-payment conjunct. |
| 3 | **26 CFR 1.6049-4** — payor includes one who *collects on behalf of another* or acts as a **middleman**; middleman includes a nominee who pays, collects on behalf of, **or** otherwise acts as intermediary, and a person is a middleman "as to any portion … actually owned by another person" | regulation | An ownership-portion and intermediary-role formulation, expressed differently from the statute's two conjuncts. |

**Their relationship is unresolved.** P2 retrieved all three and found **no
retrieved source reconciling them**. This is recorded as an *unresolved
relationship among authority-specific formulations* — **not** as a proven legal
contradiction, and **not** as a harmonized product rule. Each may be doing
different work: the statute defines a statutory obligation, the form
instructions tell a filer how to complete Forms 1099/1096, the regulation
implements the section.

Two further elements attach to their own authorities and must not drift:

- the **$10 aggregation threshold** is **statutory** (§ 6049(a)(2)), corroborated
  by the 1099-INT/OID filer instruction to file for persons paid at least `$10`;
- **"makes payments" is not limited to a cash transfer.** 26 CFR
  1.6049-4(d)(6)(i) (*regulation*) deems interest paid when **credited or set
  apart** to a person without substantial limitation or restriction, made
  available so it may be drawn at any time; the 1099-INT/OID instructions
  (*form instruction*) state the same rule in the same terms.

### A3 — whether an additional ordinary fact is required

The demonstrated difference is **specific**: Schedule B's belonging condition
differs from the literal § 6049(a)(2) conjunction, which adds nominee receipt
**plus** a payment aggregating `$10` or more. The relationship of the other
information-reporting formulations — the IRS filing instructions and 26 CFR
1.6049-4 — to those two and to each other **remains unresolved**, so nothing
below generalizes into a claim that every formulation differs from every other.

| Consequence | Ordinary proposition that would support it | Askable without a tax conclusion? |
| --- | --- | --- |
| Schedule B reduction | An attributed ordinary statement that some of the interest reported in the taxpayer's name is a named other person's, in a stated amount — the bounded evidence the product accepts, not an independently proven ownership finding | Yes — an ordinary ownership/partition statement, **after** N9b circumstance routing. The product supplies the "Nominee Distribution" classification. |
| Information reporting under formulation 1 | The same nominee receipt **plus** payments — including a credit or setting-apart meeting the deemed-payment rule — aggregating `$10` or more to that person with respect to that interest | Yes — whether the taxpayer paid, credited, or set the interest apart so the other person could draw it. That is an ordinary cash/account fact. |

So an **additional payment-or-credit fact is required to evaluate formulation 1
without inferring it from ownership.** It is **not** required for the Schedule B
reduction, and it must never be used to suppress a supported reduction.

### A4 — how the formulations relate

They address **different obligations**, and P2 did not rank them.

- Schedule B governs how the taxpayer reports **their own** taxable interest.
  Its nominee language is belonging-in-the-taxpayer's-name. Its "even if you
  later distributed" clause governs still listing the full amount on line 1; it
  is not a requirement that a distribution have occurred.
- § 6049 is an information-return statute about **payments of interest**.
  Paragraph (a)(2) is specifically the nominee-who-then-pays case; (a)(1) is the
  person who makes payments of interest. That (a)(2) exists as a separate
  conjunctive rule is itself evidence the two facts were not drafted as one.
- The form instructions and the regulation use nominee, middleman,
  actual-ownership, allocation, and credited-or-set-apart language that P2 could
  not tie back to a single retrieved account.

**Neither direction of silent rewriting is permitted:** do not treat the form
instructions as writing the statute's payment conjunct out, and do not treat the
statute as writing a payment conjunct into the Schedule B reduction.

**Constraint on Gate P3 and everything after it.** P3 may preserve and test the
**separation of consequences**. It must **not choose among these formulations or
silently combine them**, and must not select one as "the" reporting predicate
for convenience. If later implementation appears to require a single unified
reporting predicate: the **owner may choose the product posture** —
qualification, refusal, separate authority-indexed guidance, deferral, or seeking
further authoritative reconciliation. The **owner does not determine what
unresolved law means.** A claim that one normalized predicate is legally correct
**requires adequate authoritative reconciliation**; if that is required and
unavailable, the honest milestone result is a **partial result**, not a
convenient normalization.

### What the plan still refuses to infer

The plan does not assume that account title, possession, transfer of cash, or a
user-interface answer by itself decides legal ownership. The spouse exception is
mapped but not implemented because the project has not settled joint-return
subject semantics; both the regulation's middleman definition and the 1099GI
nominee paragraph carry spouse exceptions, which is why the boundary is named
rather than invented.

### The two consequences do not share one established predicate

**Gate P2 settled the shape of this question without normalizing it.** The
Schedule B reduction rests on belonging (A1). The information-reporting
obligation has **three authority-specific formulations whose relationship P2
could not resolve from retrieved sources** (A2). Interest may belong to another
owner in a year in which nothing was paid, credited, or set apart for them.

Accordingly **no section of this plan may treat the reduction and the reporting
obligation as automatically co-occurring**, and none may adopt a single
reporting predicate. The paired cases **N10** (ownership without established
payment) and **N12** (payment without established ownership) keep the assumption
falsifiable in **both** directions, and their non-inference requirements are
selected invariants rather than open questions:

- **N10.** The attributed ordinary statement is the bounded evidence the product
  accepts for the Schedule B classification, so a supported reduction is not
  suppressed because payment is unestablished. **Ownership alone does not
  establish literal § 6049(a)(2)'s payment conjunct**, does not prove one
  normalized reporting obligation, and does not satisfy every formulation — but
  it **may still support explicitly attributed IRS filing-instruction guidance**,
  which must not be suppressed.
- **N12.** Reduction `$0`, remainder `$1,200`: **payment alone does not establish
  belonging or the Schedule B reduction**. The missing ordinary ownership fact is
  asked for, not inferred.

**Preserved unknown.** Whether N12's onward transfer independently falls within
**another § 6049 route** — for instance § 6049(a)(1) "payments of interest" as
defined by § 6049(b) — is **UNVERIFIED**. P2 retrieved (a)(2) as a separate
nominee-and-pays rule but retrieved no source classifying a non-owner's
forwarding of bank interest under (a)(1). Closing it requires a primary source or
an explicit owner decision to refuse the inference; it must not be closed by
reasoning. Relatedly, P2 could not rank whether the regulation's
"portion … actually owned by another" path implements (a)(2) or adds a separate
middleman rule, and P3 must not collapse them.

## Planning review cycle

Planning is deliberately iterative. These are planning gates, not retrospective
ceremony. Findings are repaired directly into this plan; interim review records
remain working artifacts and are removed during publication curation unless a
finding becomes durable product knowledge.

No Track 0 charter may be issued until all three gates pass.

### Gate P1 — framing and product value — **COMPLETE, absorbed**

Review only the plain-language purpose, abstract product question, scope, and
fixed cases. The Reviewer attacks:

- whether the user is being asked for an ordinary fact or a tax conclusion;
- whether nominee interest is sufficiently distinct to test method transfer;
- whether the case is small enough to attribute a failure;
- whether a named non-goal actually removes a fact needed by the positive case;
- whether the result would improve calculation, explanation, or user guidance.

Output: corrected purpose, boundary, and scenario outline. Do not review a
schema or implementation that does not yet exist.

### Gate P2 — tax and artifact evidence — **COMPLETE, absorbed**

Review the tax boundary and the current-behavior map after each load-bearing
claim names the exact fields read, relevant sibling fields not relied upon, and
downstream consumers. The Reviewer independently checks:

- statutory versus form-instruction versus explanatory claims;
- the current legacy input, subtotal, line-2b, Schedule B, package, and intake
  paths;
- whether the apparent gap is missing behavior or merely missing evidence;
- whether any accepted ADR already answers the proposed question;
- compatibility and migration surfaces that a production successor would
  touch.

Output: an evidence map with bounded claims and explicit unknowns.

### Gate P3 — experiments and track decomposition — **COMPLETE, absorbed**

Review the falsifiable claims, rival shapes, evidence ladder, economic gates,
and proposed tracks. The Reviewer attacks:

- whether each experiment can fail the claim it purports to test;
- whether rival shapes differ in observable product behavior;
- whether a paper question is being disguised as a coding task;
- whether one prototype is being asked to settle several independent choices;
- whether production is chartered before identity, authority, correction,
  coexistence, and explanation are settled.

Output: a final plan that identifies which questions need disposable evidence,
which can transfer directly from accepted contracts, and the exact condition
under which production may begin.

The Foreman may combine adjacent repairs in one plan revision, but may not mark
a gate passed merely because a later section assumes its answer. A change to an
earlier gate's conclusion reopens every later section that depends on it.

## Fixed product cases

Track 0 must retain these cases through planning, evidence, and any prototype.
Amounts and identifiers are synthetic.

Two different quantities appear below and must never be conflated. **Reduction**
is the amount allocated away from the taxpayer. **Share** is the computed
remainder — the reported amount minus recorded reductions — which is what
continues into the taxable-interest calculation. A share is arithmetic, **not a
finding that the taxpayer economically owns that amount**; where no reduction is
recorded, the share is simply the reported amount carried forward. Every case
states both wherever both are defined, so the arithmetic is checkable
independently of the semantics still under review.

| Case | Facts | Required product result | What it tests |
| --- | --- | --- | --- |
| N1a — no recorded allocation, no response | One box-1 report for `$1,200`; the workspace holds **no nominee allocation and no response** to the ownership question | **Operational result:** no nominee reduction applies, and the reported `$1,200` continues into the current taxable-interest calculation on the tax and artifact baseline Gate P2 verified. **Product claim:** the product may say that no nominee allocation is recorded. It may **not** say the user denied other ownership, and may not treat the unanswered question as establishing economic ownership of the full amount | Silence is not an assertion |
| N1b — explicit negative response | Report `$1,200`; the user is asked the gating question and **answers no** | Same arithmetic as N1a: reduction `$0`, remainder `$1,200`. During the active interaction the product may acknowledge the answer just given. **After the interaction the answer supplies no durable workspace claim** — it creates no negative allocation fact, and the durable state converges with N1a. Later explanations may say only that no nominee allocation is recorded, never that the user previously denied other ownership | Transient acknowledgement leaves no durable claim |
| N2 — partial allocation | Report `$1,200`; user states `$450` belongs to one non-spouse actual owner, and separately that `$450` was paid on to that owner | Preserve the reported `$1,200`; derive reduction `$450` and remainder `$750`. The attributed ordinary statement is the bounded evidence the product accepts to support applying the Schedule B classification; the resulting reduction is a supported tax determination whose provenance identifies the assertion, payer report, rule, and authority, not an independently proven beneficial-ownership finding. For information reporting, evaluate each authority-indexed formulation on its own terms: **record which scenario facts are present or absent for each**, surface **only the instruction or conclusion the cited authority expressly supports** and attribute it to that authority, preserve the unresolved relationships and unknowns, and otherwise **qualify or defer** the product conclusion. Do not manufacture three competing legal conclusions merely to avoid selecting one. The case supplies the payment fact; it does not decide that the payment fact is what makes reporting required | Positive translation |
| N3 — full allocation | Report `$1,200`; all `$1,200` belongs to another owner | Reduction `$1,200`; share `$0` with provenance, not disappearance of the payer report | Zero and explanation |
| N4 — several owners | Report `$1,200`; `$300` belongs to one owner and `$150` to a second; the case also supplies a distinct onward-payment fact for each owner, so payment is not the variable under test | Two distinguishable allocations; aggregate reduction `$450`; remainder `$750`, on the same supported-determination footing as N2. Per owner, evaluate each authority-indexed formulation on its own terms: **record which scenario facts are present or absent for each**, surface **only the instruction or conclusion the cited authority expressly supports** and attribute it to that authority, preserve the unresolved relationships and unknowns, and otherwise **qualify or defer** the product conclusion. Do not manufacture three competing legal conclusions merely to avoid selecting one, keeping each owner's consequence and explanation separable. Allocation alone does **not** establish literal § 6049(a)(2)'s payment conjunct and must not be treated as proving one normalized reporting obligation; the filing-instruction outcome may still be surfaced **explicitly attributed as IRS filing-instruction guidance** | Cardinality and aggregation |
| N5 — over-allocation | Report `$1,200`; allocations total `$1,250` | **Paper transfer test against ADR-0070 Decisions 8–10.** Determine whether nominee over-allocation has the same relevant proposition, authority, and consumer properties as the accrued case. If it does, **inherit** that posture: preserve the payer report; the over-allocated set as a whole contributes no reduction (no still-supportable subset is accepted, since choosing whose claim to drop is a determination the product cannot make); full retraction of the composing claims; the dependent result **blocks** rather than presenting an unreduced remainder as a settled number; and never a negative remainder. If it does **not**, name the precise product difference and **return the deviation as a decision**. Do not prototype both policies merely to observe that they differ | Supportability posture transfer |
| N6a — corrected report, allocation still supportable | Same logical report, amount corrected from `$1,200` to `$1,000`, allocations total `$450` | Recompute against the **current amount on that same identity**: reduction `$450`, remainder `$550`, without rewriting history. That is the whole case — the report identity is unchanged, only its amount moved | Recomputation on same-identity amount correction |
| N6b — correction creates over-allocation | Same logical report corrected from `$1,200` down to `$400` while an allocation of `$450` remains attached to it | **Supportability re-evaluation after the same-identity correction makes the allocation excessive.** The allocation was supportable before and is not after: no stale reuse of the `$450`, and never the negative remainder `-$50`. Resolves under whatever N5 disposition is reached, since this is the same supportability invariant under a lifecycle rather than at first entry | Supportability under correction |
| N7 — corrected allocation | The amount allocated to one other owner changes from `$450` to `$400` | Prior consequences become non-current; replacement reduction `$400` and the taxpayer's replacement share `$800` | Ordinary-fact correction |
| N8 — legacy and canonical coexistence | Legacy `$450` adjustment and a new ordinary-fact-derived `$450` consequence describe the same circumstance | One subtraction or an explicit migration/refusal: reduction `$450` and share `$750`. Never the doubled reduction `$900` and its `$300` share | Compatibility and double counting |
| N9a — wrong-problem control, erroneous form | User says the payer's form amount itself is erroneous | Route to corrected-document handling; do not manufacture nominee ownership. No nominee reduction is derived | Nominee versus document correction |
| N9b — wrong-problem control, accrued interest | The taxpayer bought a bond between interest dates and reimbursed the seller for interest the form will report to them, and answers the gating question **“yes, some of this belongs to someone else”** | Route to the **accrued-interest** translation already accepted for this phase; derive **no nominee reduction** and manufacture no nominee ownership. The ordinary sentence is nearly identical to N2's, so the product must distinguish the circumstances by what it elicits, not by the words the user used. This case does not reopen accrued-interest semantics; it requires only that nominee intake not capture them | Nominee versus purchase reimbursement |
| N10 — ownership without established payment | Report `$1,200`; user states `$450` belongs to another owner, but **no onward payment, credit, or distribution to that owner has been established** | The reduction is supported: the attributed ordinary statement is the bounded evidence the product accepts, the instruction's stated condition is belonging rather than a later distribution, so reduction `$450` and remainder `$750` stand as a supported determination and must not be suppressed for want of payment. For reporting, evaluate each authority-indexed formulation on its own terms: **record which scenario facts are present or absent for each**, surface **only the instruction or conclusion the cited authority expressly supports** and attribute it to that authority, preserve the unresolved relationships and unknowns, and otherwise **qualify or defer** the product conclusion. Do not manufacture three competing legal conclusions merely to avoid selecting one. **Ownership alone does not establish literal § 6049(a)(2)'s payment conjunct**, does not prove one normalized reporting obligation, and does not satisfy every formulation; it **may still support explicitly attributed IRS filing-instruction guidance**, which the product must not suppress | Consequences with differently established support |
| N11a — two same-payer reports, one valid allocation | **Two distinct** box-1 reports in the same tax year from the **same payer** — `$1,200` (report A) and `$800` (report B) — with an allocation of `$450` attached to **report A only** | Reduction `$450` and remainder `$750` stay **associated with report A**; report B yields reduction `$0` and remainder `$800`. **No leakage**: the allocation must not reduce report B. Same-payer identity must not cause the reports to collapse. For any information-reporting result, evaluate each authority-indexed formulation on its own terms: **record which scenario facts are present or absent for each**, surface **only the instruction or conclusion the cited authority expressly supports** and attribute it to that authority, preserve the unresolved relationships and unknowns, and otherwise **qualify or defer** the product conclusion. Do not manufacture three competing legal conclusions merely to avoid selecting one | Leakage and report identity |
| N11b — allocation unsupportable on its own report | Same payer, same year: report A `$300` and report B `$800`, with an allocation of `$450` attached to **report A only**. `$450` exceeds report A alone but is less than the two reports combined | The `$450` is **not supportable** against the report it is attached to and contributes no reduction; its output follows **whatever N5 disposition is reached**, applied to report A. **Report B is unaffected at `$800` regardless.** Under no disposition may the `$450` be accepted by drawing on the combined `$1,100`. The observable failure is cross-report **merging or borrowed support** accepting an otherwise-invalid allocation | Merging and borrowed support, separately observable |
| N12 — payment without established ownership | Report `$1,200`; an onward payment, credit, transfer, or distribution to another person **is** established, but **no ownership allocation has been established** | Reduction `$0`, remainder `$1,200`. **Payment alone does not establish belonging or the Schedule B reduction** — it may be relevant evidence, but the product asks for the missing ordinary ownership fact rather than inferring it. For reporting, evaluate each authority-indexed formulation on its own terms: **record which scenario facts are present or absent for each**, surface **only the instruction or conclusion the cited authority expressly supports** and attribute it to that authority, preserve the unresolved relationships and unknowns, and otherwise **qualify or defer** the product conclusion. Do not manufacture three competing legal conclusions merely to avoid selecting one; nominee receipt is unestablished, and whether the transfer independently falls within another § 6049 route is a preserved unknown that must not be closed by reasoning | The converse of N10: payment alone does not establish ownership |

**N1a and N1b converge in durable state.** The binding invariant
is only the asymmetric one stated under `## Plain-language purpose`: silence must
never be reported as denial. **Their durable states converge**, because Gate P1
closed the retention question: an explicit “no” is a transient interaction
response and creates no durable negative allocation fact. P1 found no
demonstrated product, explanation, correction, or audit value that would pay for
a durable representation and its lifecycle, and noted that a retained denial
tempts the reading — which N1a forbids — that the taxpayer owns the whole amount.
This is a decision, not a deferral, so no reopening trigger is named: a future
requirement to attest that the ownership question was *answered* would be new
work, not a continuation of this one. **P3 does not take retention up, and
Track 0 does not inherit it as an open design question.** This plan selects no
schema, negative fact, persistence mechanism, or lifecycle.

Note also that in N1a the `$1,200` is the **computed remainder after recorded
reductions**, of which there are none. It is not a separately established finding
that the taxpayer economically owns the whole amount. The table's `share` column
carries that meaning throughout: a computed remainder, not an ownership
determination.

**No case may resolve the unresolved relationship among the reporting formulations.** Where a
case supplies an onward-payment or credit fact, it supplies it as a *fact of the
scenario*, never as a finding that the fact is what makes information reporting
required. Every required result that touches the reporting consequence is
therefore phrased as *evaluate each authority-indexed formulation on its own
terms, record which scenario facts are present or absent for it, surface only
what that authority expressly supports with the authority named, and otherwise
qualify or defer* — never as a fixed obligation, never as a selection among the
formulations, and never as an assumption that a given formulation applies at all.
Applicability is itself part of what remains unresolved. If any case is later
found to assert what the law requires, that case is defective and must be
repaired, not relied upon.

N10 and N12 are a **pair, and both carry fixed non-inference and
consequence-separation requirements.** N10 has ownership without established
payment; N12 has payment without established ownership.

- **N10.** An ownership allocation alone does **not** establish literal
  § 6049(a)(2)'s payment conjunct, does **not** prove one normalized reporting
  obligation, and does **not** satisfy every formulation. It **may** support
  explicitly attributed IRS filing-instruction guidance, which must not be
  suppressed. What is forbidden is silent normalization, not attributed guidance.
- **N12.** A payment alone does **not** establish belonging or the Schedule B
  reduction.

Those requirements are selected product invariants, not open questions. **Gate P2
completed without establishing one normalized information-reporting predicate;
the authority-indexed formulations therefore travel forward as they are** — but the invariants are not weakened merely because that
legal determination remains open. An open authority question is not a licence to
infer in either direction.

**N6a is a single instantiated case**: correction of the amount on the same
logical report, followed by recomputation against that current amount. Gate P3
determined it does **not** discriminate R-A from R-B, and that no case in
N1a–N12 supplies a material product discriminator; the rival comparison is
dropped and the representation choice is deferred. N6a carries no invalidation
branch — invalidating a report *identity* is a different event these facts do not
instantiate, and N6b already covers supportability under same-identity
correction.

The spouse exception, an absent Form 1099, trusts/custodians, and contested
ownership are mapped as boundaries. They are not silently treated as N1a, N1b, N2,
N10, or N12.

## Evidence and experiment architecture

Track 0 begins with a transfer table, not a blank-sheet design:

| Prior seam | Transfer question |
| --- | --- |
| Canonical object-valued ordinary fact + field-ref access | Can an ownership allocation be expressed honestly as one current fact, or does arbitrary owner cardinality require a different shape? |
| Report association | Does an allocation concern a specific report, a source-independent interest item/account, or both? Which correction cases discriminate them? |
| Supportability | Can the existing per-item plus aggregate boundary establish `sum(allocated away) <= reported amount` without conflating several reports? |
| Rule-owned consequences | The accrued-interest precedent already proves **multiple publications behind a shared gate** (ADR-0071 publishes two findings gated on the same supportability verdict). That is not the open question. Nominee interest asks whether consequences can be **independently gated and independently explained**: the belonging-supported Schedule B determination not gated on payment; the authority-indexed reporting evaluations not inferred from belonging; the extra payment/credit fact an input to literal § 6049(a)(2) only; and separate provenance and correction behavior for each. **N10 must detect suppression of the reduction merely because payment is absent. N12 must detect a reduction inferred from payment alone.** No experiment may select, combine, or rank the unreconciled formulations. |
| Ordinary-input mapping | Can the user answer in plain ownership language without supplying “nominee distribution” or a tax result? And can the intake elicit enough ordinary context to **route the circumstance** — interest held for another owner, a bond purchase reimbursing a seller for accrued interest, or another/uncertain case — before an allocation is captured? N9b shows that a bare “who and how much” cannot. Does the accrued-interest intake seam transfer, extend, or need a new routing decision? |
| Legacy coexistence | Does ADR-0072's no-silent-conversion posture transfer, and what property differs if it does not? |

For each seam, the disposition is exactly one of:

- **transfer unchanged**, demonstrated against the nominee cases;
- **bounded extension**, naming the added property and affected consumers;
- **new decision**, with a product behavior that distinguishes rival shapes;
- **not needed**, with the case that proves its absence harmless.

### Deferred representation alternatives

**Gate P3 determined that N6a does not discriminate these representations, and
that no case in N1a–N12 supplies a material product discriminator.** The
representation choice is therefore **deferred**, and the rival comparison is
**dropped**.

- **R-A — report-linked allocation.** A current allocation identifies the payer
  report and actual owner directly.
- **R-B — source-independent ownership allocation.** A current allocation
  identifies an interest-bearing account, receipt, or other economic item and
  actual owner; a separate association relates it to the payer report.

Why N6a fails as a discriminator: "same logical report corrected from `$1,200`
to `$1,000`" is an **amount correction of one identity**, not a change of report
identity. Under both shapes the allocation still reaches that report — R-A
directly, R-B through the association — so both recompute `$450` against
`$1,000`, and both must refuse a stale `$450` once the amount no longer supports
it (N6b). Pin currency under ADR-0010 is not a representation-shape difference.
No other case exercises an allocation whose identity is an economic item with no
named report, or a report-identity replacement.

**Do not build rival prototypes, and do not select either shape by architectural
preference.** A structural difference with no exercised downstream consumer is
not a material product discriminator — the precedent is the prior milestone's
deferred adjusted-basis choice.

**Track 0 may still find that an accepted seam already governs the required
representation** — for instance ADR-0068's circumstance-plus-pairing shape. If
so, that must be shown as **contract transfer**, reading the accepted text and
demonstrating that it governs this case. **It may not be inferred from
resemblance.** Similarity is not transfer evidence.

**Reopening trigger.** A concrete consumer involving a source-independent
allocation, a report-identity replacement, or another case in which the two
representations produce **materially different product behavior**. Absent such a
consumer, the choice stays deferred and no rival evidence is commissioned.

### Provenance layers: intended chain versus committed behavior

The ADR-0009/0010 attribution chain above is the **intended contract**. Committed
behavior does not currently realize it end to end, and **Track 0 must not mistake
one for the other.**

| | |
| --- | --- |
| **Intended chain** | derived finding → publication act → adoption act → user (ADR-0009) |
| `derived-finding.v2` | carries `symbol`, `value`, `version`, `pins`; **no actor, no human `basis`** |
| **Current publication path** | production returns `RunResult` publications and does **not append them to the act log**. `append_publications` exists in `packages/derivation/runner.py` but has **no caller under `packages/`** — only tests call it |
| **Current publication schema** | `act-derived-publication.v1` fixes `finding.schema` to **`derived-finding.v1`**, not `v2` |

So **run-local provenance and durable act-log provenance are not the same
thing**, and the durable `derived-finding.v2` publication chain **is not
currently available**.

**Gate P3 determined this gap is ORTHOGONAL to the nominee-interest decision.**
Same-year translation never asks whether a *prior-year* derived finding can be
retrieved — that was the previous milestone's question. Nominee correction asks
only "given current facts, do not reuse a stale amount," which run-local
re-derivation observes.

So **Track 0 observes run-local `RunResult` provenance.** It must **not** claim
ADR-0010 act-log displacement — such a claim would be false on the production
path — and must **not** select a publication-schema repair. Durable derived
findings are **not** a requirement of this milestone.

### Decision inventory and authorized evidence rung

This replaces a bare evidence ladder with the compact account the **Prototype
Economic Gates** require. One primary proposition, two dependent secondaries.

#### P-T1 (primary) — do the accrued-interest translation seams transfer?

Does the established document-and-ordinary-fact translation method transfer from
a purchase circumstance to a nominee ownership-allocation circumstance, and where
it does not, which seam is a **bounded extension** versus a **new decision**?

| Gate 1 axis | Score | Reason |
| --- | --- | --- |
| Future blast radius | 2 | Governs how every later ownership/allocation case is translated |
| Migration cost | 1 | Coexists with a live legacy nominee consumer (N8); no published schema is edited |
| Residual uncertainty after paper examples | 1 | Six seams with accepted contracts to read; paper can classify most |
| Inability to test cheaply during implementation | 1 | The seams have committed analogues that can be exercised cheaply |
| **Total** | **5** | **paper spike plus ADR draft** — not prototype-eligible |

- **Two positives:** N2 (single owner, allocation and payment both present);
  N4 (two owners, per-owner separation).
- **Two meaningful negatives:** N9b (accrued-interest reimbursement must route
  away and derive no nominee reduction); N1a (absence produces no allocation and
  no attributed denial).
- **Lifecycle trace:** N2 → N7 (allocation corrected `$450`→`$400`) → remainder
  `$800`, prior consequences non-current, nothing rewritten.
- **Producer → authority → consumer → failure:** ordinary intake produces an
  attributed finding → the assertion act carries actor and time → a rule derives
  the reduction against the payer report → line 2b and Schedule B consume the
  subtotal. **Failure:** the derivation reaches the consumer with no recoverable
  attribution chain, or reaches it from a circumstance that was never routed.
- **Authorized rung: paper.**
- **Single observation that would justify climbing:** paper cannot classify a
  seam as transfer, bounded extension, or new decision because the accepted
  contract's text does not reach the nominee case either way.

#### P-T1a (secondary) — do separately supported consequences need independent gates?

Can the seam carry the belonging-supported Schedule B determination and the
authority-indexed reporting evaluations with **independent gates**, rather than
behind one shared gate?

| Gate 1 axis | Score | Reason |
| --- | --- | --- |
| Future blast radius | 2 | Any consequence pair with unequal support inherits the answer |
| Migration cost | 0 | No published artifact changes to answer it |
| Residual uncertainty after paper examples | 1 | ADR-0071 and the rule language's inapplicable dispositions are readable |
| Inability to test cheaply during implementation | 1 | A gate arrangement is observable in rule shape |
| **Total** | **4** | **paper spike plus ADR draft** |

- **Two positives:** N2 and N4 — reduction derived, reporting evaluated
  separately per formulation with the authority named.
- **Two meaningful negatives:** N10 — a design that **suppresses** the
  belonging-supported reduction because payment is absent; N12 — a design that
  **infers** a reduction from payment alone.
- **Lifecycle trace:** correcting the payment fact must not displace the
  belonging-supported reduction; correcting the allocation must not invent a
  reporting obligation. The observation is the **pin set**, not a legal ranking.
- **Producer → authority → consumer → failure:** two rules, each with its own
  gate and pins → separate provenance → separate explanation. **Failure:** one
  gate suppresses or fabricates the other consequence, or the two share a pin set
  that couples their correction behavior.
- **Authorized rung: paper.**
- **Single observation that would justify climbing:** paper plus ADR-0071 and the
  accepted rule contracts leave a **specific technical uncertainty** about
  whether independently gated consequences are expressible at all.

#### P-T1b (secondary) — does ADR-0070's supportability posture transfer?

Does the accrued-interest over-claim posture transfer to nominee over-allocation
(N5) and to supportability re-evaluation after correction (N6b)?

| Gate 1 axis | Score | Reason |
| --- | --- | --- |
| Future blast radius | 1 | Bounded to supportability of allocated-away amounts |
| Migration cost | 0 | No published artifact changes to answer it |
| Residual uncertainty after paper examples | 0 | ADR-0070 Decisions 8–10 are directly readable |
| Inability to test cheaply during implementation | 1 | Behaviour is observable in a blocked/retracted result |
| **Total** | **2** | **implement normally** — no spike, no prototype |

- **Two positives:** N5 (`$1,250` against `$1,200`); N6b (`$450` against a
  report corrected to `$400`).
- **Two meaningful negatives:** publishing a negative remainder; accepting a
  still-supportable **subset** and silently dropping the rest.
- **Lifecycle trace:** supportable at entry → correction makes it excessive →
  the dependent result must not silently reuse the stale amount.
- **Producer → authority → consumer → failure:** allocation set → supportability
  verdict → dependent subtotal. **Failure:** a partially-accepted set, or a
  remainder presented as a settled number under an unstated confidence.
- **Authorized rung: paper.**
- **Single observation that would justify climbing:** a named product difference
  between the nominee and accrued cases that makes ADR-0070's posture
  inapplicable — which is a **decision to return**, not an experiment to run.

#### Authorized rung, and what may not bypass it

**The currently authorized evidence rung for this milestone is PAPER.** No
executable prototype is pre-authorized, and no "optional spike" may bypass the
planning and review gate.

If T0-A cannot settle a genuinely **technical capability** question at paper,
**stop**: repair the plan, or create the owner-approved
`docs/prototypes/<topic>/plan.md` that `PROJECT_PLANNING.md` requires before the
first charter of any prototype topic. Do not absorb an executable spike into the
Track 0 charter by calling it optional. If paper instead exposes a missing
production substrate, route that substrate as a separate patch or decision
rather than folding it into this milestone.

- **N10/N12** may justify a later disposable independent-gate test **only if**
  paper and the accepted rule contracts leave a **specific technical
  uncertainty** — not merely to watch two rules fire, which ADR-0071 already
  demonstrates.
- **N8** remains a **paper compatibility analysis** until a concrete successor
  producer is proposed. At that point the Track 0 integration-surface artifact
  and real-consumer execution become **mandatory**.

The four rungs remain paper → construction → disposable execution →
production-shaped vertical. Do not climb a rung that cannot change a decision. A
working arithmetic prototype does not establish intake, authority, identity,
correction, coexistence, or explanation.

## Track structure

### Track 0 — transfer and discrimination

Track 0 produces:

- a concise nominee-interest addition to the fluid taxable-interest domain
  model;
- paper transfer dispositions for every seam (P-T1);
- N1a–N12 paper traces with named kill conditions;
- the P-T1b disposition on ADR-0070's supportability posture, inherited or
  deviated-with-reasons;
- the P-T1a disposition on independently gated consequences;
- a decision-ready contract proposal **or** an honestly bounded partial result.

**Track 0 reuses Gate P2's tax and artifact map as established input and does not
redo that research.**

Track 0 is built in three reviewed checkpoints rather than one long draft:

1. **T0-A — semantics.** Reuse the P2 tax and artifact map as established input.
   Produce the **ordinary-question / routing box**; the **authority-lifecycle
   table** and the **empty/nonempty matrix** (adversarial-closure artifacts 1–2);
   and **paper transfer dispositions for each seam**. Do not re-verify A1–A4,
   H1, or Branch B.
2. **T0-B — traces.** Complete the **N1a–N12 paper traces with named kill
   conditions**, including the **late-authority trace** and the **claim-reuse
   proof** (adversarial-closure artifacts 3–4). **No rival implementations and no
   formulation-ranking experiment.**
3. **T0-C — synthesis.** Synthesize the transfer dispositions; produce the
   **neighboring-capability diff** and the **N8 compatibility account**; produce
   an **integration-surface artifact only if a successor externally bound
   producer is proposed**; and return either a decision-ready contract or an
   honestly bounded partial result.

The Reviewer checks each checkpoint before the next begins. Repairs are folded
into the checkpoint they correct. A later contradiction reopens the dependent
checkpoint instead of accumulating a compensating paragraph.

### Contract unit — conditional

Charter only if Track 0 selects a contract with no consequential owner decision.
It may add or supersede ADRs and schemas required by the selected canonical
shape. It must instantiate every new payload before implementation depends on
it and must not edit published schema history.

### Production unit — conditional

Charter only after the contract unit. Expected capability, subject to Track 0:
ordinary-input mapping, canonical facts, association/supportability, derived
nominee consequences, legacy coexistence or migration, package adoption,
Schedule B and line-2b integration, explanation, and synthetic fixtures.

### Integration unit — conditional

Required if the production unit changes an externally bound symbol or migration
path. It exercises N1a–N12 through the real entry, derivation, package,
presentation, and explanation boundaries and preserves unrelated taxable-
interest behavior.

## Review placement

- Planning: independent review at P1, P2, and P3.
- Track 0: independent review at T0-A, T0-B, and T0-C because these checkpoints
  settle product meaning and evidence, not merely implementation mechanics.
- Contract and production: Foreman review at each atomic unit; independent
  review only where the final plan identifies unresolved semantic risk.
- Final publication: one author-independent review of the curated exact range.

The working reviews are not publication deliverables. Their durable findings
must be absorbed into the domain model, plan, ADR, tests, retrospective, or
phase state according to what they establish.

## Contracts and boundaries

Accepted contracts remain binding until evidence supports a successor. Track 0
must read their exact text where relied upon, especially ADR-0068 through
ADR-0072. Similarity is not transfer evidence.

The milestone may recommend a successor contract when the Product Model
requires it. It must state the value, cost, risk, and displaced work in plain
language. No contract is changed in this planning commit.

The current standing workspace authorization remains the operational universe
convention. The milestone does not ask for per-family “done” declarations or
infer incompleteness from absence of an allocation.

### Compatibility surfaces for N8 (Gate P2)

A production successor that replaces or coexists with the legacy nominee amount
would touch, at minimum:

- the fact type `tax.us.2025.scheduleb.adjustment.nominee.amount` — **published
  history, never edited in place**;
- its source family, closure mapping, subtotal rule, and citation;
- the line-2b subtractand `scheduleb-nominee-subtotal` and the `require_closed`
  guard on the nominee family — present in v6 **and** in the historical v4/v5;
- the Schedule B attachment nominee row, in v5 and v4;
- the adjustment-slot tables in `packages/derivation/package_validation.py`;
- the core-calculations package admissions of those artifacts.

**Double subtraction is a live risk independent of Branch B.** No
ordinary-language producer was found in the enumerated searched committed
production areas, but attested legacy facts can still be present — the committed
tests inject them — so N8 remains a real compatibility case rather than a
hypothetical one. The enumerated exclusions stand and the negative search is not
broadened beyond them.

**ADR-0072 is an analogy only.** It retires the **accrued-interest** legacy input
surface for new obligations and defines that coexistence path. It is
accrued-specific: it does not name nominee, does not govern nominee interest, and
does not migrate it. Its no-silent-conversion posture is a *transfer question*
this milestone must answer for itself, not an answer it may inherit. No accepted
ADR supplies a beneficial-ownership test, a nominee ordinary-intake mapping, or
either information-reporting formulation.

## Verification

Planning and Track 0 name exact commands after current consumers are mapped.
At minimum:

- focused current-behavior tests for Schedule B interest adjustments;
- the accrued-interest integration checkpoint as the transfer baseline;
- an intake-routing probe showing that an affirmative gating answer is
  disambiguated before an allocation is captured, with N9b routed away from
  nominee handling;
- new N1a–N12 tests at the selected evidence rung, including a cross-report
  non-leakage check for N11a, separate merging and borrowed-support checks for
  N11b, and a no-inference-from-transfer check for N12;
- package/schema tests for any new published artifact;
- presentation and explanation probes for any externally visible consequence;
- repository mypy for typed Python changes;
- full test suite for any change under `packages/kernel/` or
  `packages/derivation/`;
- governance lint, envelope scan, and diff check at handoff.

Only synthetic `demo.*` / `demo-*` identities and values may be committed.

## Success and stop conditions

The milestone succeeds when it does all of the following, whether or not it
reaches production:

1. explains the nominee-interest problem in language a user can understand;
2. keeps the payer report, ordinary ownership statement, tax classification,
   return reduction, and information-reporting formulations distinct — each with
   its own authority, provenance, and consequence — and **preserves the absence
   of an established shared predicate** rather than resolving it. Success does
   **not** require deciding whether the legal predicates ultimately coincide;
3. verifies the current legacy path and every downstream consumer it would
   affect;
4. resolves N1a–N12 without inventing ownership from document structure or cash
   movement, and routes an affirmative gating answer to the right circumstance
   rather than defaulting it into a nominee allocation (N9b);
5. classifies every prior translation seam as transfer, extension, new
   decision, or unnecessary;
6. uses executable evidence only where it can discriminate product behavior;
7. prevents omission, over-allocation, stale reuse, double subtraction, and
   cross-report leakage, merging, and borrowed support between simultaneous
   reports (N11a, N11b);
8. leaves a production work packet with no unresolved semantic decision, or an
   explicit partial result with one smallest reopening trigger. **The
   unreconciled reporting formulations do not by themselves force a partial
   result.** Separately attributed guidance, qualification, refusal, or deferral
   may constitute a **complete bounded product contract**. Call the result
   partial only if a required product behavior cannot be specified without
   unsupported legal normalization, or another consequential decision remains
   unresolved;
9. records a simple owner-facing model of what transferred and what did not;
10. completes P1–P3 and T0-A–T0-C review before any production charter.

Stop and return to the owner if:

- the positive case requires deciding joint-return subject or spouse ownership;
- the product cannot ask an ordinary ownership question without asking the user
  to make a legal or tax classification;
- the viable representations differ on a material product behavior that the
  bounded prototypes cannot discriminate;
- compatibility requires silently upgrading a legacy adjustment into an
  ownership claim;
- implementation would require a general information-return filing system,
  general ownership ontology, or another material expansion not justified by
  N1a–N12.

Do not stop merely because the selected result requires a bounded successor
contract or a somewhat larger implementation. Agents may recommend and build a
larger scope when they can explain its product value, cost, risk, and displaced
work in plain language.

## Track 0 adversarial closure

PENDING. Track 0 must complete the six artifacts required by
`PROJECT_PLANNING.md`, including the integration-surface artifact if it proposes
a successor producer for the externally bound nominee subtotal or taxable-
interest symbol. No production charter is ready while any applicable row is
missing or failed.
