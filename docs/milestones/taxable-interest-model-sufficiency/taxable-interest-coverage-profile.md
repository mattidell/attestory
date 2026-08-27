# Taxable Interest 2025: The Coverage Profile

## What this document is

The **coverage-profile method** of [authority-model.md](authority-model.md),
applied to the worked specimen. It declares an authority boundary, enumerates
the concept's universe from that authority, records the facts each region
requires, and only then compares against what the engine's committed content
represents.

It is not a census of missing features, and it must not be read as one. It is
the instrument that makes the distance between an intensional concept and an
executable build measurable at all. Each entry earns its place by exercising a
distinct modeling requirement.

Read first: [tax-modeling-foundation.md](tax-modeling-foundation.md) for the
eight layers, [concept-coverage-and-claims.md](concept-coverage-and-claims.md)
for the concept/coverage/claim distinction and the closed status vocabulary
restated below, and [authority-model.md](authority-model.md) for the
proposition-level provenance requirements. The concept itself is in
[taxable-interest-concept.md](taxable-interest-concept.md).

The layer names used in the entries (evidence / reported fact / economic fact /
tax classification / composition / derived concept / presentation) are the
specimen-level instantiation of those eight layers.

**On completeness.** The categories below are a lower bound on what this model
does not cover, never an upper one. The enumeration is bounded by the authority
actually examined — declared immediately below — and by the adversarial effort
recorded in
[taxable-interest-adversarial-cases.md](taxable-interest-adversarial-cases.md).
Unlisted does not mean covered.

## Declared authority boundary

The authority consulted for this map is primary and official material for tax
year 2025, in three classes.

**Statute — Internal Revenue Code (read directly).** The following sections
were read in the current prelim edition of Title 26 and are quoted where they
are load-bearing:

- **§ 61(a)** — "Gross income defined"; § 61(a)(4), "Interest".
- **§ 135** — "Income from United States savings bonds used to pay higher
  education tuition and fees".
- **§ 454** — "Obligations issued at discount".
- **§ 1272** — "Current inclusion in income of original issue discount",
  including § 1272(a)(7).
- **§ 1278** — "Definitions and special rules", including § 1278(b).

**Form and form instructions.** Schedule B (Form 1040) 2025, Cat. No. 17146N;
Instructions for Schedule B (Form 1040) 2025; Instructions for Form 1040
(2025), line 2b.

**Publications.** Publication 550, *Investment Income and Expenses*;
Publication 1212, *Guide to Original Issue Discount (OID) Instruments*.

**Treasury Regulations.** **One** regulation was read: **Treas. Reg.
§ 1.1275-4**, the noncontingent bond method for contingent-payment debt
instruments, cited as controlling at C12. No other regulation text was
consulted.

**What was not consulted.** No judicial authority, and no Treasury Regulation
other than the one named above. Where a rule's operative detail lives in the
regulations rather than the statute — the nominee information-reporting
mechanics being the clearest example — this document cites the statutory basis
for the *substance* and the instructions for the *reporting operation*, and
says so at the entry. It does not assert regulatory coverage it did not
verify.

That single-regulation depth is itself a bound on this profile. Under
[authority-model.md](authority-model.md), a proposition whose mechanics the
statute delegates to regulations is only partially supported until those
regulations are read. Several entries below are in that position.

Nothing outside the set above was consulted for a tax claim in this document.

## Source hierarchy and what each class can support

The four classes below are ordered by what they are competent to establish.
The distinction matters because the engine's own citation vocabulary does not
make it (see *Limitations of the authority corpus*).

This is a coarsening of the seven-class hierarchy in
[authority-model.md](authority-model.md), reflecting what was actually
examined here: statute and regulation share a row because only one regulation
was read, and judicial authority does not appear because none was consulted.
The coarsening is a fact about this examination, not a claim that the finer
distinctions do not matter.

| Class | Can support | Cannot support |
| --- | --- | --- |
| Internal Revenue Code; Treasury Regulations | Controlling tax rules; what is includible and why | — |
| Official IRS forms | The reporting surface: which lines exist, their arithmetic and ordering | Why an amount is includible |
| Official IRS form instructions | Filing and reporting operation; who must file what; how to present an adjustment | A complete tax ontology; the boundary of a concept |
| Official IRS publications and other published guidance | Explanation; category discovery; identifying that a category exists | Controlling authority, however readable |

**How this map uses the hierarchy.** Each entry states the class of the
authority it rests on. Where a statutory section establishes the inclusion,
exclusion, timing, or adjustment, it is cited and the conclusion is stated as
a tax conclusion. Where only a form, its instructions, or a publication
supports the entry, the conclusion is bounded to what that class can
establish — that the category exists, or how it is reported — and is not
stated as a determination of what the law requires.

Neither a form, nor its instructions, nor a publication is a complete tax
ontology for taxable interest. The categories below are those these sources
surface; the map does not claim they exhaust the concept.

## The reporting surface, verified

Schedule B (Form 1040) 2025, Part I, verbatim structure:

- **Line 1** — "List name of payer. If any interest is from a seller-financed
  mortgage and the buyer used the property as a personal residence, see the
  instructions and list this interest first. Also, show that buyer's social
  security number and address:"
- **Line 2** — "Add the amounts on line 1"
- **Line 3** — "Excludable interest on series EE and I U.S. savings bonds
  issued after 1989. Attach Form 8815"
- **Line 4** — "Subtract line 3 from line 2. Enter the result here and on Form
  1040 or 1040-SR, line 2b"
- **Note following line 4** — "If line 4 is over $1,500, you must complete
  Part III."

The Part I side note reads: "If you received a Form 1099-INT, Form 1099-OID,
or substitute statement from a brokerage firm, list the firm's name as the
payer and enter the total interest shown on that form."

Two facts from this structure govern much of what follows.

**Line 4, not line 2, is taxable interest.** The amount that reaches Form
1040 line 2b is net of the § 135 education exclusion. A model that computes
the pre-line-3 amount and publishes it as taxable interest has omitted a
subtraction the form requires.

**The form's own $1,500 note is on line 4.** The note following line 4
conditions **Part III** on line 4 — the post-adjustment, post-exclusion figure
— not on the gross sum of listed interest. This is the Part III trigger, and
is distinct from the "Who Must File" conditions below, which govern whether
Schedule B is filed at all.

The Instructions for Schedule B state eight independent conditions requiring
Schedule B, of which the $1,500 threshold is only the first:

1. "You had over $1,500 of taxable interest or ordinary dividends."
2. "You received interest from a seller-financed mortgage and the buyer used
   the property as a personal residence."
3. "You have accrued interest from a bond."
4. "You are reporting original issue discount (OID) of less than the amount
   shown on Form 1099-OID."
5. "You are reporting interest income of less than the amount shown on a Form
   1099 due to amortizable bond premium."
6. "You are claiming the exclusion of interest from series EE or I U.S.
   savings bonds issued after 1989."
7. "You received interest or ordinary dividends as a nominee."
8. "You had a financial interest in, or signature authority over, a financial
   account in a foreign country or you received a distribution from, or were
   a grantor of, or transferor to, a foreign trust."

Conditions 3, 5, and 7 correspond to adjustment classes the engine already
models. Conditions 2, 4, and 6 correspond to categories it does not model at
all.

**Condition 1 is distributive, and the Form 1040 instructions settle it.**
Read alone, "Over $1,500 of taxable interest or ordinary dividends" would
admit both a distributive reading (either amount alone exceeding $1,500) and a
combined reading (the two summed). The Instructions for Form 1040 state the
two tests separately, one at each line: under line 2b, "If you have more than
$1,500 of taxable interest, you must complete Schedule B"; under line 3b, "If
you have more than $1,500 of ordinary dividends, you must complete Schedule
B." Two independent thresholds, each on its own quantity. The distributive
reading is the official one.

This matters for assessing the engine's attachment rule, and the answer is
favourable: the committed evaluator compares each subtotal against the
threshold separately, which is the operation the authority describes. The
defects in that rule lie elsewhere — in *which* interest quantity it compares
and in the seven conditions it never tests.

## Adjustment mechanics, verified

Per the Instructions for Schedule B, adjustments are not separate lines. Each
is reported *within* line 1: the full reported amount is listed, a subtotal is
struck, and the adjustment is written below it with an identifying label —
"Nominee Distribution", "Accrued Interest", "ABP Adjustment", "OID
Adjustment" — and then applied to reach line 2.

Publication 1212, under "Showing an OID adjustment," directs the holder to
list the full OID on line 1, write "Nominee Distribution" or "OID Adjustment"
below the subtotal, and then **"subtract or add accordingly"** to reach line
2. An OID adjustment therefore has a direction: it can increase the amount, not
only reduce it. This occurs when the correct OID exceeds the figure the payer
reported.

Publication 1212 also directs, under "Adjustment for acquisition premium" and
"Purchase after date of original issue," that a Form 1099-OID box 1 amount
overstates the holder's includible OID when the instrument was bought at an
acquisition premium. The controlling rule is § 1272(a)(7), "Reduction where
subsequent holder pays acquisition premium," which reduces the daily portion
by a fraction whose numerator is the excess of the purchaser's cost over the
issue price plus previously includible OID. The reduction is **conditional**:
it operates only where such an excess exists, so it applies to some, not all,
secondary-market acquisitions.

Publication 1212 also directs, under "Reporting OID," that a recipient
"[i]nclude all OID and qualified stated interest shown on any Form 1099-OID,
boxes 1, 2, and 8." The reportable OID surface is therefore three boxes, not
one. See C16 and C17.

## Category coverage map

Status vocabulary:

- **represented and supported** — the model carries the category and its
  classification path is sound within the declared boundary.
- **represented but semantically collapsed** — a representation exists, but it
  discards a distinction the authority requires.
- **represented but requiring judgment** — represented, but correctness turns
  on an economic or circumstantial fact the workspace does not hold.
- **bounded exclusion** — deliberately and legibly outside the model.
- **unsupported and blocking** — absent, and its absence stops the calculation.
- **unsupported but currently silently omitted** — absent, and the calculation
  proceeds as though the category did not exist. This is the dangerous status.
- **outside the declared authority boundary** — not assessable here.

Every entry below terminates in a product consequence. Categories that could
not materially change a claim, a rule, a consequence, or a successor decision
are not admitted.

---

### C1 — Form 1099-INT box 1 stated interest

- **Authority**: § 61(a)(4) ("gross income means all income from whatever
  source derived, including … (4) Interest") establishes includibility.
  Class: statute. Schedule B Part I note and Pub 550, "Form 1099-INT",
  establish the reporting route. Class: form instructions + publication.
- **Proposition**: A payer reported $X of interest to this taxpayer for 2025.
- **Evidence**: Form 1099-INT; brokerage substitute statement.
- **Representation**: `tax.us.2025.f1099int.box1-interest`
  (`packages/content/tax/2025/f1099int.bundle.json`), keyed `payer` +
  `statement` + `tax-year`, no evidence key.
- **Classification path**: family `tax.us.2025.f1099int.b1` →
  `interest.b1-subtotal` → composition slot → line-2b rule.
- **Rule**: included, at face value.
- **Closure requirement**: `require_closed` on the b1 family.
- **Status**: **represented and supported** as a *reported fact*.
- **Unsupported neighbouring inference**: that the box 1 figure is the
  taxpayer's includible amount. It is not, whenever a nominee, accrued-interest,
  or bond-premium circumstance applies — which is precisely why the
  Instructions provide the three adjustment labels.
- **Consequence**: safe at claim levels 1–3; carries no independent support
  for level 4.

### C2 — Treasury and US savings-bond interest (1099-INT box 3)

- **Authority**: § 61(a)(4) establishes includibility. Class: statute. Pub
  550, "U.S. obligations", "U.S. Savings Bonds", "U.S. Treasury Bills, Notes,
  and Bonds", identifies the category and its state treatment. Class:
  publication.
- **Representation**: `tax.us.2025.f1099int.box3-interest`
  (`packages/content/tax/2025/interest_composition.bundle.json`); family
  `tax.us.2025.f1099int.b3`.
- **Rule**: included at face value; federally taxable, generally
  state-exempt (state treatment is outside scope).
- **Status**: **represented but requiring judgment**.
- **Judgment not represented**: whether a Series EE/I bond cashed in 2025
  qualifies for the education exclusion (see C13). Box 3 does not disclose
  it, and nothing in the model asks.
- **Consequence**: for a taxpayer who qualifies for the exclusion, the model
  will include an amount the form directs to be excluded, with no signal.

### C3 — Taxable OID (1099-OID box 1)

- **Authority**: § 1272(a)(1) ("there shall be included in the gross income of
  the holder of any debt instrument having original issue discount, an amount
  equal to the sum of the daily portions") establishes current inclusion;
  § 1272(a)(7) establishes the acquisition-premium reduction. Class: statute.
  Pub 1212, "Figuring OID on Long-Term Debt Instruments" and "Refiguring OID",
  explains the computation. Class: publication.
- **Representation**: `tax.us.2025.f1099oid.box1-interest-oid`; family
  `tax.us.2025.f1099oid.b1`.
- **Rule**: included at face value.
- **Status**: **represented but requiring judgment**.
- **Judgment not represented**: acquisition premium. Under § 1272(a)(7) the
  daily portion is reduced where the holder's cost exceeds the issue price
  plus previously includible OID. The circumstance that determines whether the
  reduction applies at all, and its size — acquisition date and cost — is not
  represented anywhere in the model.
- **Consequence**: for any secondary-market OID instrument acquired at a cost
  giving rise to acquisition premium under § 1272(a)(7), the model computes
  the payer's figure rather than the holder's, and overstates silently. Not
  every secondary-market acquisition produces acquisition premium; the defect
  is that the model cannot tell which do, because neither the condition nor
  the inputs to it are representable.

### C4 — Taxable interest received without an information return

- **Authority**: Instructions for Form 1040, line 2b ("Include taxable
  interest you received or accrued during 2025"); Pub 550 categories
  including "Interest on tax refunds", "Usurious interest", "Gift for opening
  account", "Interest on insurance dividends", "Interest on condemnation
  award". Class: form instructions + publication.
- **Representation**: `tax.us.2025.non-form-interest.amount`; family
  `tax.us.2025.non-form-interest`.
- **Status**: **represented but semantically collapsed**, on two counts.
- **Collapse 1 — the residual predicate disagrees with itself.** The family's
  `closure_claim` in `packages/content/tax/2025/family.non-form-interest.json`
  reads "Every interest amount received without a Form 1099-INT statement
  instance for tax year 2025 is recorded." The fact-type title in
  `packages/content/tax/2025/interest_composition.bundle.json` reads
  "Interest income received without a Form 1099-INT/OID statement instance
  for 2025." The family omits OID; the fact type includes it. Neither
  mentions Schedule K-1. A K-1 box 5 interest amount satisfies "received
  without a Form 1099-INT/OID statement instance" on its face, and is also a
  member of the K-1 family — the two predicates overlap.
- **Collapse 2 — identity is payer + tax-year only.** Two distinct non-form
  interest amounts from the same payer cannot be represented as two facts.
- **Unsupported neighbouring inference**: that a residual family named for
  what it lacks covers every category the model has not otherwise named. It
  does not. The predicate is membership in one fact type; the prose cannot
  enlarge it.
- **Consequence**: the residual is not a safety net. It is one more narrow
  slot whose name suggests otherwise.

### C5 — Schedule K-1 interest

- **Authority**: Schedule B Part I (payer listing). Class: form.
- **Representation**: `tax.us.2025.form1065-k1.box5-interest`; family
  `tax.us.2025.form1065-k1.box5`, keyed `partnership` + `k1-statement` +
  `tax-year`.
- **Status**: **represented and supported** for Form 1065 box 5 only.
- **Bounded exclusion, legibly declared**: the family's `closure_claim`
  states it "excludes other K-1 forms, boxes, attached statements,
  partnership basis, and total taxable-interest completeness." Schedule K-1
  (Form 1041) and Schedule K-1 (Form 1120-S) interest are therefore outside
  the model.
- **Consequence**: a beneficiary of an estate or trust, or an S-corporation
  shareholder, has interest the model cannot represent; the overlap with C4's
  residual (above) makes the routing ambiguous rather than blocked.

### C6 — Market discount, current-inclusion election

- **Authority**: § 1278(b), "Election to include market discount currently" —
  on election, market discount "shall be included in the gross income of the
  taxpayer for the taxable years to which it is attributable", and the
  included amount "shall be treated as interest". Class: statute. Pub 1212,
  "Market discount" (broker reports box 5 of Form 1099-OID on written notice
  of the election), explains the reporting. Class: publication.
- **Representation**: `tax.us.2025.f1099int.box10-market-discount` and
  `tax.us.2025.f1099oid.box5-market-discount`; families
  `tax.us.2025.f1099int.b10` and `tax.us.2025.f1099oid.b5`.
- **Status**: **represented and supported**, with a legible bound. Both
  families' `closure_claim`s scope themselves to the section 1278(b)
  current-inclusion election and expressly disclaim "disposition-time market
  discount, basis, or total taxable interest."
- **Consequence**: this is the model's best-declared surface. Market discount
  accrued but *not* currently elected — recognised on disposition as ordinary
  income — is outside it, and says so.

### C7 — Nominee distributions

- **Authority**: Instructions for Schedule B, "Nominees" ("interest you
  received as a nominee (that is, in your name, but the interest actually
  belongs to someone else)"); Schedule B requirement condition 7. Class: form
  instructions. **This entry is bounded to the reporting operation.** What the
  examined authority establishes is the operation Schedule B performs, the
  definition those instructions use, and the committed representation of it.
  It does not establish the substantive allocation. § 61(a)(4) establishes
  that interest is gross income; it does not by itself determine whose gross
  income a given amount is, and beneficial ownership is not settled by the
  fact that a form instruction describes a subtraction. **The controlling
  nominee allocation and information-reporting rules were not read**, so no
  claim is made here about the substantive result — only about what the
  instructions direct and what the model represents.
- **Economic fact**: the amount belonged to another person.
- **Representation**: `tax.us.2025.scheduleb.adjustment.nominee.amount`;
  family `tax.us.2025.scheduleb.adjustment.nominee`, keyed `tax-year` +
  `adjustment-instance`.
- **Status**: **represented but semantically collapsed**.
- **Collapse**: the family title is "Synthetic Nominee Distribution
  adjustment instances", its `closure_claim` is bounded by "the bounded
  Schedule B interest-adjustment surface" — that is, by itself — and the
  adjustment carries `quantity: tax.us.2025.quantity.taxable-interest`, the
  same quantity as the inclusions it reduces, while being constrained
  nonnegative. Direction lives only in the rule's `subtract` operator, not in
  the fact.
- **Judgment not represented**: nothing links a nominee adjustment to the
  statement it adjusts. The adjustment instance is keyed only by tax year and
  an opaque instance identifier.
- **Consequence**: a correct total is reachable; an explainable one is not.
  The product cannot say *which* reported amount was reduced or why.

### C8 — Accrued interest paid to seller

- **Authority**: Instructions for Schedule B, "Accrued interest" ("identify
  the amount to be subtracted as 'Accrued Interest'"); Pub 550, "Bonds Sold
  Between Interest Dates"; Schedule B requirement condition 3. Class: form
  instructions + publication.
- **Representation**: `tax.us.2025.scheduleb.adjustment.accrued-interest.amount`.
- **Status**: **represented but semantically collapsed**, identically to C7.
- **Consequence**: as C7.

### C9 — Amortizable bond premium

- **Authority**: Instructions for Schedule B, "ABP Adjustment"; Schedule B
  requirement condition 5. Class: form instructions. The amortizable
  bond-premium rules of § 171 and the regulations under it **were not read**;
  this entry is therefore bounded to the reporting operation and to the
  engine's representation of it, and does not determine the correct
  amortization amount.
- **Representation**: `tax.us.2025.scheduleb.adjustment.abp-adjustment.amount`.
  Its `closure_claim` correctly notes the case "where the payer did not
  already net the amount."
- **Status**: **represented but requiring judgment**, and collapsed as C7.
- **Judgment not represented**: whether the payer already netted the premium
  is the whole question, and the model has no representation of Form 1099-INT
  boxes 11, 12, or 13 (bond premium) against which to check.
- **Consequence**: the user is silently made responsible for a determination
  the product could otherwise assist with; double-reduction is not detectable.

### C10 — OID adjustment

- **Authority**: Pub 1212, "Showing an OID adjustment"; Instructions for
  Schedule B ("identify the amount to be subtracted as 'OID Adjustment'");
  Schedule B requirement condition 4. Class: publication + form instructions.
- **Representation**: **none**. There is no OID-adjustment family, fact type,
  subtotal, or row.
- **Status**: **unsupported but currently silently omitted**.
- **Aggravating fact**: Pub 1212 directs the holder to "subtract or add
  accordingly." An OID adjustment may be *upward*. The engine's line-2b rule
  has exactly one `subtract` node with three fixed operands, and all three
  adjustment fact types are constrained nonnegative. Even if an OID
  adjustment family were added, an upward adjustment would remain
  inexpressible without a rule change.
- **Consequence**: the Schedule B instructions name exactly four adjustment
  labels — Nominee Distribution, Accrued Interest, ABP Adjustment, OID
  Adjustment. The model carries three of them. This is the one it omits, it
  comes from the same instructions that supply the other three, and its
  absence is invisible.

### C11 — Seller-financed mortgage interest

- **Authority**: Schedule B Part I line 1, verbatim; Instructions for
  Schedule B ("list first any interest the buyer paid you… Be sure to show
  the buyer's name, address, and SSN"); Pub 550, "Installment sale payments";
  Schedule B requirement condition 2. Class: form + form instructions +
  publication.
- **Representation**: **none**. The string "seller-financed" does not occur
  anywhere in `packages/content/` or `docs/adr/`.
- **Status**: **unsupported but currently silently omitted**.
- **Where it would land today**: `non-form-interest`, whose identity is
  `payer` + `tax-year` and which has no place for the buyer's address or SSN
  — data the form requires and which is, additionally, personal data of a
  third party.
- **Consequence**: two failures at once. The amount is includible but the
  required Part I disclosure is not producible, and the amount independently
  triggers a Schedule B requirement the engine does not detect.

### C12 — Contingent-payment debt instruments

- **Authority**: **Treas. Reg. § 1.1275-4**, controlling; Pub 1212
  (contingent-payment debt instrument rules), explanation only. Class:
  regulation, with a publication as secondary.
- **Economic facts**: that the instrument is a contingent-payment debt
  instrument at all; its **comparable yield** — "the yield at which the issuer
  would issue a fixed rate debt instrument with terms and conditions similar
  to those of the contingent payment debt instrument"; its **projected payment
  schedule**; the **actual contingent payments** made during the year; and the
  resulting **positive or negative adjustment**.
- **Representation**: **the reported amount is represented; the circumstance
  and the adjustment machinery are not.** A CPDI can report OID in Form
  1099-OID box 1, and `tax.us.2025.f1099oid.box1-interest-oid` represents that
  reported amount like any other. What has no representation is everything
  needed to decide whether that reported amount is the includible amount: no
  fact type marks an instrument as contingent-payment, none carries the
  comparable yield or the projected payment schedule, none records actual
  contingent payments, and there is no route by which a positive or negative
  adjustment — or a supported corrected amount and its provenance — could
  reach the total.
- **Status**: **represented but requiring judgment** — the reported amount is
  carried, and whether it is the includible amount turns on circumstantial
  facts the workspace does not hold. It is the most demanding instance of that
  status in this map, because the missing facts are not merely unrecorded:
  even supplied, they would have to be *computed with*, and the model has no
  adjustment route to compute into. Under § 1.1275-4 the holder accrues
  interest on the noncontingent bond method using the comparable yield and
  projected payment schedule; where actual payments differ, a positive
  adjustment is additional interest income, and "a net negative adjustment
  first reduces interest for the taxable year that the taxpayer would
  otherwise account for on the debt instrument." Pub 1212 states plainly that
  for these instruments the amount reported on Form 1099-OID may be
  inaccurate.
- **Consequence**: the engine ingests box 1 and carries it through unchanged.
  Where the reported figure happens to equal the correct accrual the total is
  right by coincidence; where an adjustment applies, the total is wrong in
  either direction and nothing in the model can register it. The repair is
  therefore **not merely declarative** — declaring the category out of scope
  would at least make the boundary legible, but making it correct requires
  representing the circumstance and either performing the adjustment
  computation or admitting a supported corrected amount with its provenance.
  Which of those to build is not decided here.

### C13 — Series EE/I savings-bond education exclusion

- **Authority**: **§ 135(a)**, "Income from United States savings bonds used
  to pay higher education tuition and fees" — "In the case of an individual
  who pays qualified higher education expenses during the taxable year, no
  amount shall be includible in gross income by reason of the redemption
  during such year of any qualified United States savings bond." Class:
  statute. § 135(b)(1) limits the exclusion where redemption proceeds exceed
  expenses; § 135(c)(1) defines a qualified bond and § 135(c)(2)(A) defines
  qualified higher education expenses as "tuition and fees required for the
  enrollment or attendance of (i) the taxpayer, (ii) the taxpayer's spouse, or
  (iii) any dependent". Schedule B line 3, verbatim ("Excludable interest on
  series EE and I U.S. savings bonds issued after 1989. Attach Form 8815"),
  and Schedule B requirement condition 6 establish the reporting route. Class:
  form + form instructions.
- **This is a gross-income exclusion, not a form mechanic.** § 135(a) operates
  on includibility in gross income. Schedule B line 3 is where that exclusion
  is *reported*; it is not what creates it. That distinction decides much of
  what follows, and it is why the omission is a tax-model defect rather than a
  presentation defect.
- **The exclusion is not a dollar-for-dollar function of expenses.**
  § 135(b)(1) limits it where aggregate redemption proceeds exceed qualified
  expenses, and Form 8815 implements that limit as a ratio: net qualified
  expenses divided by **total redemption proceeds, principal and interest**,
  applied to the interest included in those proceeds. A taxpayer with $2,000
  of expenses against $5,000 of proceeds carrying $3,000 of interest excludes
  $1,200, not $2,000. Any model of this exclusion needs the proceeds figure,
  not only the expense figure.
- **Economic facts required**, each of which the model would have to
  represent: that the bonds are series EE or I **issued after 1989**; that the
  taxpayer was the **owner** and had reached **age 24 before the issue date**
  (§ 135(c)(1)(B)); a **filing status other than married filing separately**
  (§ 135(d)(3)); redemption during 2025; **total redemption proceeds,
  principal plus interest**; the **interest included in those proceeds**;
  **qualified higher education expenses** paid for the taxpayer, spouse, or a
  dependent at an eligible institution; **nontaxable educational benefits**
  netted against those expenses; **modified AGI** against the § 135(b)(2)
  phaseout; and whether any of those same expenses was **taken into account
  for an education credit or for the nontaxable part of a Coverdell ESA or
  qualified tuition program distribution**, which § 135(d)(2) requires be
  subtracted from the qualified expenses before the § 135(b) limitation is
  applied. None of these has a fact type.
- **Representation**: **none on the interest route.** The only occurrence of
  Form 8815 in the 2025 content is
  `tax.us.2025.ss-benefits-scope.no-form-8815` in
  `packages/content/tax/2025/ss-benefits-scope.bundle.json`, a
  *declared-absence* assertion used to bound the Social Security benefits
  worksheet. The asymmetry is between artifacts, not intentions: on the Social
  Security route committed content represents a bounded no-Form-8815
  proposition, and on the interest route no artifact stands in any relation to
  Form 8815 — neither an exclusion constituent nor a declared absence. That
  establishes that declared absence is an available and already-used device in
  this corpus; it establishes nothing about whether the omission here was
  considered.
- **Status**: **unsupported but currently silently omitted**, and structurally
  the most serious.
- **Structural aggravation**: this is not a missing constituent of a sum. It
  is Schedule B **line 3**, and line 4 — the amount that goes to Form 1040
  line 2b — is defined as line 2 minus line 3. The engine's Schedule B
  itemisation (`rule.attachment.schedule-b.v4.json`, part `part-i-interest`)
  ties its positive subtotals less its three adjustment subtotals directly to
  `tax.us.2025.interest.taxable-total`. There is no line 3, and no place in
  the `tie_out` for one.
- **The bounded finding.** In the § 135 fact pattern, and assuming the modeled
  positive families and the three modeled adjustment classes otherwise
  reproduce the correct pre-line-3 amount, the engine publishes that
  pre-line-3 amount as `taxable-total`, while the official line-2b route
  requires line 4 — the pre-line-3 amount **less** the § 135 exclusion. The
  engine has no representation of that subtraction.

  This is deliberately narrower than "the model computes Schedule B line 2."
  The model does not necessarily compute line 2 either: C10, C11, C16, C17,
  and C18 are categories or adjustment classes that also feed line 2 and that
  the model does not represent, and C3, C9, and C15 are circumstances that can
  make a modeled amount wrong. The established claim is about the *missing
  subtraction*, not about the model reproducing line 2.
- **Consequence**: for a taxpayer in this fact pattern the published line-2b
  value is overstated by the excluded amount, with no block, no qualification,
  and a `published_value` disposition indistinguishable from a correct one.

### C14 — Tax-exempt interest boundary

- **Authority**: Pub 550, "State or Local Government Obligations";
  Instructions for Form 1040, line 2a. Class: publication + form
  instructions. **§ 103, the exclusion's statutory basis, was not read**, so
  this entry establishes that the boundary exists and that the engine
  implements one, not that the engine's boundary is drawn where § 103 draws
  it.
- **Representation**: `tax.us.2025.f1099int.box8-tax-exempt-interest` carries
  `quantity: tax.us.2025.quantity.tax-exempt-interest`, distinct from
  `quantity.taxable-interest`, and routes to line 2a. A companion authority
  fact type `tax.us.2025.f1099int.box9-specified-pab-authority` admits only
  explicit null or numeric zero and hard-blocks a nonzero value.
- **Status**: **represented and supported**, bounded to the structural claim.
  This is the model's strongest exclusion boundary and the one place where a
  distinct quantity does real work. The supported claim is that box 8 cannot
  leak into line 2b — a property of the artifact graph, verifiable without
  § 103. Whether the engine's tax-exempt boundary coincides with § 103's is
  not established here.
- **Consequence**: improper inclusion of box 8 into line 2b is structurally
  prevented. Correctly.

### C15 — Frozen deposits

- **Authority**: Pub 550, "Interest income on frozen deposits". Class:
  publication — category discovery only; the statutory and regulatory basis
  for deferring inclusion of frozen-deposit interest **was not read**.
- **Representation**: the *amount* is representable. Interest credited to a
  frozen account and reported by the payer enters
  `tax.us.2025.f1099int.box1-interest` like any other box 1 amount. What has
  no representation is the *circumstance* — that the deposit is frozen and the
  amount is therefore not currently withdrawable — which is what may defer
  inclusion.
- **Status**: **represented but requiring judgment**. The category is not
  missing from the model; the fact that determines its timing is.
- **Consequence**: the model includes the amount currently, with no signal,
  and cannot ask the question that would establish whether it should. This is
  the same failure shape as C3 and C9 — a reported amount consumed as an
  economic fact — rather than an absent category. Low incidence; admitted
  because it is a third independent instance of the pattern, and because the
  three adjustment families name frozen deposits in their `closure_claim`s as
  something they say nothing about, which a reader could mistake for a
  declared exclusion.

### C16 — Qualified stated interest on Form 1099-OID (box 2)

- **Authority**: § 61(a)(4) establishes includibility. Class: statute. Pub
  1212 directs the recipient to "[i]nclude all OID and qualified stated
  interest shown on any Form 1099-OID, boxes 1, 2, and 8," and describes box 2
  as the qualified stated interest paid or credited during the calendar year.
  Class: publication.
- **Proposition**: a debt instrument that carries OID **may also** carry
  qualified stated interest, reported separately from the OID accrual. Many
  OID instruments carry none — a stripped obligation pays no periodic interest
  at all — so this is a category that arises for some instruments and not
  others. The payer instructions confirm it is optional in a second sense:
  box 2 is where qualified stated interest on the obligation is entered, but
  a payer "may report any qualified stated interest on this obligation on Form
  1099-INT rather than on Form 1099-OID."
- **Evidence**: Form 1099-OID; brokerage substitute statement.
- **Representation**: **none.** The only OID fact types in
  `packages/content/tax/2025/interest_composition.bundle.json` are
  `tax.us.2025.f1099oid.box1-interest-oid` and
  `tax.us.2025.f1099oid.box5-market-discount`. There is no box 2 fact type,
  family, or subtotal, and `rule.form1040-line2b.v4.json` neither requires nor
  closes one.
- **Classification path**: none. The amount has nowhere to go except the
  residual `non-form-interest` family, whose own predicate (C4) excludes
  amounts accompanied by a Form 1099-OID statement instance.
- **Status**: **unsupported but currently silently omitted**.
- **Unsupported neighbouring inference**: that representing Form 1099-OID box
  1 represents Form 1099-OID. It represents one of the three boxes the
  publication directs the recipient to include.
- **Consequence**: a holder of an OID obligation that also pays qualified
  stated interest has an includible amount the model cannot record anywhere,
  and the total is understated with no block and no signal. How often that
  holding arises was not measured, and no prevalence claim is made: the entry
  is admitted on the same rule as every other, that the amount materially
  affects line 2b when it exists.
- **Plausible repair**: a box 2 fact type, family, and subtotal, added to the
  composition as an eighth positive constituent.

### C17 — OID on U.S. Treasury obligations (Form 1099-OID box 8)

- **Authority**: § 1272(a)(1) establishes current inclusion of OID. Class:
  statute. Pub 1212 describes box 8 as "[t]he OID on a U.S. Treasury
  obligation for the part of the year the owner held the debt instrument," and
  places it in the same "boxes 1, 2, and 8" reporting instruction. Class:
  publication.
- **Proposition**: OID accrued on a Treasury obligation is includible for
  federal purposes, and is reported in a box distinct from box 1.
- **Representation**: **none**, on the same evidence as C16.
- **Status**: **unsupported but currently silently omitted**.
- **Aggravating fact**: the model *does* separately represent Treasury and
  savings-bond stated interest through Form 1099-INT box 3 (C2), so the
  Treasury category is not conceptually foreign to it. The omission is
  specific to the OID route.
- **Consequence**: a holder of Treasury STRIPS or a similar instrument has an
  includible accrual with no representation. Understated total, no block.
- **Plausible repair**: as C16. Whether box 8 warrants a family distinct from
  box 1 turns on whether the model needs to preserve the federal/state
  treatment difference, which is out of scope here.

### C18 — U.S. savings-bond interest previously reported under a § 454 election

- **Authority**: **§ 454(a)** permits a holder of a non-interest-bearing
  obligation issued at a discount to "at his election made in his return for
  any taxable year, treat such increase as income received in such taxable
  year," and provides that on making the election the accumulated increase
  from acquisition to the start of the election year "shall also be treated as
  income received in such taxable year." Class: statute. Pub 550, "U.S.
  savings bond interest previously reported", states the reporting
  consequence: "If you reported the increase in redemption value of series EE
  or I bonds each year, you must report the difference between the total
  interest shown on Form 1099-INT and the interest you previously reported."
  Class: publication.
- **Proposition**: where the election was made in an earlier year, the Form
  1099-INT furnished at redemption reports the *cumulative* interest, most of
  which the taxpayer has already included in prior years' income. Only the
  difference is includible now.
- **Evidence**: the redemption-year Form 1099-INT, plus the taxpayer's own
  prior-year returns — evidence the payer does not hold and the engine has no
  route to.
- **Representation**: **none.** No fact type, family, subtotal, or adjustment
  row represents a previously reported amount, and the string does not occur
  in the 2025 content.
- **Classification path**: the full box 1 or box 3 amount enters the total at
  face value.
- **Status**: **unsupported but currently silently omitted**, and it is a
  further subtractive need, distinct from the four adjustment labels the
  Schedule B instructions enumerate: it is not one of them, and it reduces the
  includible amount for a different reason — the amount was already taxed.
- **Structural aggravation**: this is not merely a missing family. Like C10,
  it is an adjustment the model's shape does not accommodate — the line-2b
  rule's `value` is one `subtract` node with three fixed operands. Adding a
  further subtractive class requires changing the rule's shape, not only adding
  content.
- **Consequence**: the taxpayer most affected is one who followed an election
  the Code expressly offers, and the error is an *overstatement* that can be
  large — potentially decades of accrual taxed twice. There is no block, no
  qualification, and a `published_value` disposition.
- **Plausible repair**: a previously-reported adjustment class, which forces
  the same contract question C10 raises and which decision D5 must resolve.

---

## Adjacent routes that are not line-2b coverage

The categories above are admitted on the map's own rule: each must materially
affect the amount reported on Form 1040 line 2b. The following interest-bearing
routes fail that test and are **not** counted as coverage, positive or
negative. They are recorded only so a later reader does not read their absence
from the map as a finding.

**A child's interest elected onto a parent's return (Form 8814).** Where a
parent elects to report a child's interest and dividends, 2025 Form 8814 line
12 directs: "Subtract line 11 from line 6. Include this amount in the total on
Schedule 1 (Form 1040), line 8z. In the space next to that line, enter 'Form
8814' and show the amount." The elected income therefore reaches the parent's
return through Schedule 1 line 8z, not through the parent's line 2b. It is a
different route to a different line, outside this map. Whether the engine
should model it is a real question and not this one; the Form 8814 conditions,
the $2,700 and $13,500 boundaries at its line 4, and the child's own filing
alternative were not assessed here.

**Interest reported elsewhere on the return.** Tax-exempt interest reaches
line 2a rather than line 2b and is treated at C14 because the boundary between
the two lines *is* material to line 2b. Investment interest expense, student
loan interest, and mortgage interest are deductions rather than income and do
not bear on this concept at all.

## Limitations of the authority corpus

### Current artifacts are not cited to controlling law

`packages/schemas/derivation/citation.v1.schema.json` defines exactly four
authority families: `us-code` (requiring `title` and `section`), `irs-form`,
`irs-instructions`, and `irs-publication`.

Of the 74 citation citizens in `packages/content/tax/2025/`, 71 are
`irs-instructions`, 2 are `irs-publication`, 1 is `irs-form`, and **none is
`us-code`**.

The distinction to hold onto: **the capability exists and is unused.** This is
a corpus gap, not a schema gap. Every statutory section relied on in this map
— §§ 61(a)(4), 135, 454, 1272, 1278 — is expressible as a `us-code` citation
citizen today with no vocabulary change. Closing this gap is content work.

### The engine cannot cite a line, and this one is a schema limit

The `irs-instructions` authority variant carries `form_id` and `tax_year` and
nothing else. There is no locator field. Consequently
`packages/content/tax/2025/citation.form1040.line-2b.json` resolves to
`{family: irs-instructions, form_id: 1040, tax_year: 2025}` — the 2025 Form
1040 instructions as an entire document. The words "line 2b" appear only in
the filename and the citizen id.

The three Schedule B adjustment citations
(`citation.scheduleb-adjustment.nominee.json`,
`citation.scheduleb-adjustment.accrued-interest.json`,
`citation.scheduleb-adjustment.abp-adjustment.json`) are byte-identical apart
from their ids: all three resolve to `{irs-instructions, 1040-SCH-B, 2025}`.
The citation layer cannot distinguish a nominee distribution from a bond
premium.

The schema is candid about this. Its own description states that resolution
"is structural/adoption-only and does not claim external legal verification."

### What follows

Every tax claim the engine currently makes about taxable interest is cited, at
best, to a document that explains *reporting operation*. Under the source
hierarchy at the head of this document, form instructions cannot establish the
boundary of a tax concept. So no citation **in the present corpus** is
competent to support the proposition "US-federal taxable interest for 2025 is
$X."

The two limits behind that sentence have different remedies, and conflating
them would misdirect the work. Reaching controlling law needs new content in
an existing vocabulary. Reaching a specific line needs a vocabulary change
with corpus-wide consequences.

This is a limitation of the corpus, not a claim that the computed amounts are
wrong. Most of them, most of the time, will be right — because the
instructions describe the ordinary case accurately, and the ordinary case is
common.

## Actionable gaps

Ranked by product consequence, not by frequency.

1. **The § 135 education exclusion is absent** (C13). It is a gross-income
   exclusion under § 135(a), reported at Schedule B line 3, and the engine
   publishes the pre-line-3 amount as `taxable-total` with no representation
   of the subtraction. Because § 135(a) governs includibility in gross income,
   the exclusion belongs to the final taxable-interest concept as a matter of
   tax substance; that is settled by statute and is not an owner decision.
   What is open is **structure**: which artifact kind implements the
   subtraction, whether a separate pre-exclusion intermediate corresponding to
   Schedule B line 2 is also declared, and how Schedule B presents a
   subtraction whose substance is already determined.
2. **Three material positive or subtractive categories are absent from the
   OID and savings-bond routes** (C16, C17, C18). Form 1099-OID box 2
   (qualified stated interest) and box 8 (Treasury OID) are two of the three
   boxes Pub 1212 directs the recipient to include, and neither is
   representable. Savings-bond interest previously reported under a § 454
   election is a further subtractive need whose omission overstates the total
   by the whole of the prior-year accrual. C18 shares C10's structural
   problem: the rule's single `subtract` node has exactly three operands and
   cannot take another.
3. **Seller-financed mortgage interest is absent** (C11), including the
   buyer-identity disclosure the form requires and the independent Schedule B
   trigger it creates.
4. **The OID adjustment class is absent** (C10), and the rule shape forbids
   an upward adjustment even in principle.
5. **The Schedule B requirement test is defective in two established ways,
   and a third alleged defect does not survive inspection.** The four
   statements below are kept apart because they have different
   evidence and different remedies. The account rests on
   `rule.attachment.schedule-b.v4.json`'s `requirement` block and on the only
   code path that evaluates it, `packages/derivation/runner.py:884-913`.

   **(a) Wrong symbol and wrong basis — established.** The `requirement`
   names `tax.us.2025.interest.positive-total`, the *gross* seven-family
   figure, before any adjustment. The authority's basis is taxable interest,
   and Schedule B's own note conditions Part III on **line 4** — the
   post-adjustment, post-exclusion figure. The rule tests a quantity the
   authority does not name.

   **(b) Omitted non-threshold branches — established.** Only condition 1 is
   implemented. Conditions 2 through 8 are not tested at all. The
   `requirement` shape admits a subtotals-versus-threshold comparison and
   nothing else, so the omission is structural rather than an oversight in
   the content.

   **(c) Combined-threshold over-trigger — does not exist, and the
   threshold combination is correct.** The `requirement` lists two subtotals,
   `interest.positive-total` and `dividends.ordinary-total`, and a reader
   could take the list to mean they are summed before comparison. They are
   not. `packages/derivation/runner.py:908-913` builds one trigger per
   subtotal, each comparing that subtotal alone against the threshold, and
   sets `required = any(t["over"] for t in triggers)`. Executing that logic
   against $800 of interest and $800 of ordinary dividends yields `over:
   False` for both and `required: False` — no attachment.

   That is the right behaviour, not merely a tolerable one. The Instructions
   for Form 1040 state the two thresholds separately, one under line 2b and
   one under line 3b, so the distributive comparison the evaluator performs is
   the operation the authority describes. This aspect of the rule is sound and
   is recorded here so that the two defects below are not read as
   contaminating it.

   **(d) Consequences.** The **under-trigger is the real defect**, and it
   follows from (b) rather than from (a). A taxpayer with $600 of interest and
   a $100 nominee distribution must file Schedule B under condition 7; the
   engine will not require it — and `rule.form1040-line2b.v4.json` will still
   subtract the $100, publishing a reduced line 2b with no attachment
   disclosing the reduction and no row labelled "Nominee Distribution"
   anywhere. Three of the untested conditions (3, 5, 7) correspond to
   adjustment classes the model already carries, so the engine holds the facts
   that would prove Schedule B is required and does not consult them.

   In the over-trigger direction, (a) creates the *potential* for one —
   `positive-total` can exceed $1,500 where the correct basis does not — but
   it does not produce an observable false positive, because the basis differs
   from line 4 only when an adjustment or the § 135 exclusion is nonzero, and
   each of those circumstances independently requires Schedule B under
   conditions 3, 5, 6, or 7. The two errors mask each other. This is worth
   stating plainly: a reviewer who checks only whether the threshold behaviour
   is observably wrong will find that it is not, and will conclude the rule is
   sound. The defect in (a) is that the rule names a quantity the authority
   does not, not that it currently yields a wrong answer.
6. **Reported amounts are taken as includible amounts** (C1, C3, C9, C15).
   Acquisition premium under § 1272(a)(7), payer-netted bond premium, and
   frozen-deposit timing are three independent instances. In each the payer's
   figure is representable and the circumstance that would correct it is not,
   so the discrepancy is not merely uncomputed — it is unaskable.
7. **The residual family does not reach** (C4). Its predicate is narrower
   than its name, disagrees with its own fact type, and overlaps the K-1
   family.
8. **Adjustments have no link to what they adjust** (C7, C8, C9), so no
   explanation of a reduced total is producible.
9. **No artifact-level improvement above is citable to controlling authority
   as the corpus stands** — but the two limits behind that have different
   remedies and should not be worked as one item.

   **(a) Controlling law: content work, no vocabulary change.**
   `citation.v1` already defines a `us-code` authority family carrying `title`
   and `section`. Every statute this map relies on is expressible today. The
   gap is that none of the 74 committed citation citizens uses the family.

   **(b) A precise IRS form or instruction line: vocabulary work.** The
   `irs-instructions` authority variant has no line or section locator, so
   "line 2b" cannot be recorded even in principle. This one does require a
   citation-vocabulary change, and it is the only demonstrated vocabulary
   limitation of the two.
