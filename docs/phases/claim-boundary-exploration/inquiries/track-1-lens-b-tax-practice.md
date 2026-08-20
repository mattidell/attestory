# Track 1 — Lens B: Tax / Financial-Practice Adversary

Audience: Product, Shared (exploratory record).

Status: **exploratory, non-authoritative.** Paper analysis of already-committed
synthetic content and general public Schedule B guidance, read from memory of
the instructions and not re-fetched in this session (no network access was
used; where I rely on IRS instruction content not present in the repository,
I say so explicitly and flag it as needing a citation check, not as settled
fact). "Claim boundary" is a working lens for this phase, not adopted product
vocabulary. This account creates no product contract and reinterprets no
accepted artifact.

> **Reader's annotation added by the final repair. This account is preserved
> as written — it is independent evidence and is not rewritten.** Two later
> corrections apply when reading it. (1) Where it describes the Schedule B
> attachment rule as testing `interest.positive-total` *plus*
> `dividends.ordinary-total` against the threshold, and treats the
> foreign-account/trust answers as part of the trigger: the runner tests the
> two subtotals **independently** and attaches if **either** exceeds the
> threshold, and the foreign-account and foreign-trust questions are
> completeness requirements applying **after** attachment, not triggers. This
> account's substantive suspicion — that categorical triggers are missing —
> was **confirmed**: the IRS gives eight independent triggers and the
> committed rule implements only the dollar threshold, omitting seven. (2)
> Where it refers to "the current package (v33)": v33 is the highest-numbered
> core package present and this inquiry's comparison target; no committed
> artifact designates a current package. See `OV-1` and the Track 3 curated
> inquiry.

Scope confirmed before writing: lens B, tax/financial-practice adversary;
single user question "Why is this amount on my return?" traced against the
committed synthetic fixture at line 2b (value `1825`); documentation-only,
no engine run, no artifact generation, no fixture or package edit;
exploratory not authoritative; independence from the other three lens
accounts (I did not read, grep, or open any `track-1-lens-a/c/d-*` file);
stop conditions as listed in the charter (engine run, out-of-scope file edit,
governance interpretation, need for a general semantic model, drafting
another track's material, or commit-lock failure).

---

## 1. Lens and standpoint

I am an experienced preparer — call it a CPA in a small practice — reviewing
output from tax-preparation software I did not build, on behalf of a client
whose Form 1040 I am about to sign as paid preparer. My professional exposure
is not academic: a wrong or incomplete Schedule B attachment, an omitted
income category, or a total I cannot reconcile is a due-diligence failure
that follows *me*, not the vendor. I am not reading this the way a taxpayer
reads it — I am reading it the way I read a client's brokerage-supplied tax
package before I trust a single number in it: looking for what the summary
implies is complete, and checking whether that implication survives contact
with the categories real returns actually carry.

What I notice that a casual reader would not: whether the declared "universe"
of a computation (here, the seven-family composition) is the IRS's universe
or the vendor's convenient subset; whether a number that *looks* reconciled
actually reconciles when I do the arithmetic myself; and whether an
attachment or filing trigger is evaluated on the right base amount and the
right conditions — not just a dollar threshold, but the several *categorical*
triggers the Schedule B instructions independently impose regardless of
amount. A casual filer trusts the total. I audit the boundary around the
total, because that boundary is where a return goes from "materially correct
on the numbers I can see" to "correct as filed."

## 2. My best two-sentence plain answer

Track 0's draft (section 4 of the packet) is close, but I would change one
clause. Track 0 wrote:

> This $1825 is the total taxable interest we found from your 1099-INT,
> 1099-OID, and other interest sources for the year, after subtracting any
> nominee, accrued-interest, or bond-premium adjustments you told us about.
> It doesn't include tax-exempt interest (like from municipal bonds), and it
> only reflects the specific interest documents and adjustments you've
> confirmed as complete so far.

My replacement for the first sentence:

> This $1825 is the total of the taxable-interest categories this product
> currently tracks — Form 1099-INT boxes 1, 3, and 10, Form 1099-OID boxes 1
> and 5, Schedule K-1 (Form 1065) box 5, and interest you reported without a
> form — minus the nominee, accrued-interest, and bond-premium adjustments
> you told us about. It doesn't include tax-exempt interest (like from
> municipal bonds), and it doesn't yet cover every category a return can
> carry — for example, interest reported through an estate or trust K-1, or
> seller-financed mortgage interest — so if any of those apply to you, ask
> your preparer whether they need to be added by hand.

The defect this repairs: Track 0's sentence names the *forms* ("1099-INT,
1099-OID, and other interest sources") but not the *box-level and
entity-level boundary* of what is tracked, and it does not disclose that the
category list is a product-defined subset rather than the full space of
taxable-interest sources the Internal Revenue Code recognizes. A preparer
reading "we found... from your 1099-INT, 1099-OID, and other interest
sources" would reasonably infer the software covers the ordinary universe of
interest income a client might have. It covers a well-chosen slice of it
(see section 4) — but the sentence as drafted does not say so, and an
ordinary reader has no way to know the difference between "no such interest
exists in your situation" and "this software doesn't have a slot for that
category yet." That distinction matters more to a preparer than to a casual
filer, because the preparer is the one who has to catch it before signing.

## 3. What an intelligent casual user could still misunderstand

- **"We found" reads as "we found everything."** A person with income from a
  trust (Schedule K-1, Form 1041, box 1) or a seller-financed mortgage would
  read Track 0's sentence and reasonably conclude the software already
  accounted for it, because it names "1099-INT, 1099-OID, and other interest
  sources" without a boundary. There is no modeled family for estate/trust
  K-1 interest or seller-financed mortgage interest in this package (see
  section 4) — so for those two real, common categories, "we found" is
  silently false rather than silently zero.
- **"After subtracting any... adjustments you told us about" sounds
  optional.** A practitioner knows that accrued interest purchased and bond
  premium amortization are not merely nice-to-report adjustments a user might
  volunteer — for a bond held with accrued interest paid to the seller, or an
  election under section 171 to amortize taxable bond premium, *not*
  reporting the adjustment is itself a compliance error, and in the accrued-
  interest case, filing Schedule B is separately required by the fact of the
  adjustment, not by the dollar total (see section 4). "You told us about"
  invites the false belief that omitting the adjustment is a safe default.
- **A user could believe "over $1,500 triggers Schedule B, under $1,500
  doesn't" is the *whole* rule.** It is the headline rule, but it is not the
  only one. If the software's UI ever surfaces an attachment decision as a
  single amount comparison, a preparer knows that is incomplete; a casual
  filer with a small nominee amount or a small accrued-interest adjustment
  would not know a schedule is required at all (see section 4 — this is the
  deepest thread, and it is a real gap, not a hypothetical one).
- **"Confirmed as complete so far" (Track 0's closing clause) could read as
  "the IRS agrees this is complete."** A closure declaration is the
  taxpayer's or preparer's own assertion, not a third-party check. This
  reading risk is closer to Lens C's territory (I flag it, but do not
  develop it — see section 7).

## 4. The deepest thread I followed

**Question:** Is the seven-family composition (Hop 4 of Track 0, artifact
`tax.us.2025.interest-composition` v4) the right universe for deciding both
(a) the line-2b amount and (b) whether Schedule B must be attached at all —
and does the attachment rule implement the *whole* "who must file Schedule B"
condition, or only the dollar-threshold branch of it?

**What I opened, in order, and what each said:**

1. `packages/content/tax/2025/interest-composition.v4.json`
   (`tax.us.2025.interest-composition` v4, `taxable-interest-composition.v1`).
   Its `required_universe.claim` reads: "Seven declared positive
   taxable-interest families forming the gross Schedule B Part I line-1
   basis, without subtractive adjustments." It also `publishes`
   `tax.us.2025.interest.positive-total` — the **gross** sum of the seven
   families, before the three adjustment subtractions.

2. `packages/content/tax/2025/rule.form1040-line2b.v4.json`
   (`tax.us.2025.rule.form1040-line2b` v4, `rule-artifact.v3`). Confirms the
   published line-2b value (`tax.us.2025.interest.taxable-total`) is the
   seven-family sum **minus** the three Schedule B adjustment subtotals
   (nominee, accrued interest, ABP). This is the net figure a filer actually
   sees at 1825.

3. `packages/content/tax/2025/rule.attachment.schedule-b.v4.json`
   (`tax.us.2025.rule.attachment.schedule-b` v4, `attachment-rule.v6`). Its
   `requirement` block compares `tax.us.2025.interest.positive-total` (the
   **gross**, pre-adjustment figure from step 1 — not the net `taxable-total`
   from step 2) plus `tax.us.2025.dividends.ordinary-total` against a
   threshold parameter, `strictly_greater_than`. Its `completeness` block
   adds two more required answers (foreign account, foreign trust) and a
   conditional obligation naming FinCEN Form 114 when a foreign account is
   present. **There is no branch in this artifact that requires attachment
   because a nominee distribution, accrued-interest adjustment, or ABP
   adjustment exists, independent of the dollar threshold.**

4. `packages/content/tax/2025/parameter.schedule-b-threshold.json`
   (`tax.us.2025.parameter.schedule-b-threshold` v1). Confirms the threshold
   value is `1500`.

5. `packages/content/tax/2025/family.scheduleb-adjustment.nominee.json`,
   `family.scheduleb-adjustment.accrued-interest.json`,
   `family.scheduleb-adjustment.abp-adjustment.json` (each
   `source-family.v1` v1). Each `closure_claim` is precise about what a
   closure over that family covers, but none of the three artifacts, nor the
   attachment rule that itemizes them, states that the *existence* of an
   entry in any of these three families is itself an independent Schedule B
   filing trigger.

**What I believe this means, stated as a practitioner would, and flagged as
needing verification against the current IRS Schedule B instructions rather
than adopted as settled:** the "Who Must File" condition for Schedule B, as I
know it from practice, is not solely a $1,500 threshold on interest or
dividends. It also independently requires Schedule B when a taxpayer has,
among other things, accrued interest purchased on a bond, a bond-premium
amortization election reducing reported interest, or interest/dividends
received as a nominee for someone else — regardless of dollar amount. This
package's `rule.attachment.schedule-b` v4 does not implement that
independent trigger; it only tests the gross seven-family total against
$1,500 (plus the two foreign-account/trust answers). A synthetic client with,
say, a $40 accrued-interest adjustment and total interest under $1,500 would,
on this artifact's logic, not be required to attach Schedule B — which, if my
recollection of the instructions is right, would be wrong. **This is stated
as a decision question for the project, not as an adopted correction**: it
would need verification against the current-year Schedule B instructions
text (a citation artifact currently exists only as an authority pointer —
`tax.us.2025.citation.schedule-b`, `citation.v1` — with no quoted instruction
text committed to check this against), and if confirmed, would be a rule
(`attachment-rule.v6` instance) change, which is out of my documentation-only
authority to make.

**Secondary observation from the same walk, not pursued as the deep thread
but recorded because a signing preparer would catch it on inspection:** the
committed presentation fixture's Schedule B citation group shows a tie-out
line "Reported subtotal: 1825" under the "Part I: Taxable Interest" heading,
immediately followed by three separate adjustment tie-out lines ("Adjustment:
-100", "-50", "-25" for Nominee, Accrued Interest, and ABP respectively — see
`citationGroups` in the presentation fixture). The "Reported subtotal: 1825"
figure equals the net line-2b value exactly, not the gross seven-family sum
(gross would need to be `1825 + 100 + 50 + 25 = 2000` for the three
adjustment lines shown beneath it to reconcile visibly). Nothing in the
committed presentation model shows the gross figure or an explicit
"gross − adjustments = net" line. A preparer reconciling Schedule B Part I
by eye, the way one habitually checks a client statement, cannot verify from
this rendering alone that 1825 is arithmetically consistent with the three
adjustment amounts shown next to it — the subtraction is asserted, not shown.
This sharpens, from a reconciliation-habit angle, the gap Track 0's Hop 2
already named generally (individual box amounts are not committed as
separate files).

**Did this thread change the answer or its boundary?** Yes, on the primary
question: it is why my two-sentence answer in section 2 names the specific
box- and entity-level boundary rather than repeating "1099-INT, 1099-OID, and
other interest sources," and it is why I would not, as a preparer, treat
"the seven-family composition" as a settled universe without checking the
attachment-trigger question against the current instructions. The secondary
tie-out observation did not change the answer's text, but it is a concrete
reason a preparer would not fully trust the presentation without opening the
underlying findings — a reason distinct from, and additional to, the
document-level-detail gap Track 0 already recorded.

## 5. Where my explanation terminates

I stop at the artifacts themselves: the `rule-artifact.v3` computation, the
`attachment-rule.v6` attachment condition, the `taxable-interest-composition.v1`
declared universe, and the `citation.v1` authority pointers, all as committed
to the current package (v33) and confirmed identical to the fixture's adopted
package (v15) for every artifact I opened except the composition and rule I
did not re-diff (I relied on Track 0's confirmation that the material chain —
rule v4, composition v4, attachment-rule v4, threshold parameter v1 — is
identical v15/v33, and spot-checked the attachment rule and composition files
directly myself against the current-package copies, which are the only copies
present at a single path in this repository layout). Beyond that: the
citation artifacts carry no quoted IRS instruction text, so I cannot verify
my recollection of the Schedule B "Who Must File" independent triggers
against a committed source — that verification requires a public IRS source
this session did not fetch, and is exactly the kind of thing I would check
before ever advising a real client. I also cannot verify the individual
document-level amounts behind the 1825 total; those are not committed as
separate files in this fixture's directory (confirmed — same gap Track 0
found at Hop 2).

Addressing the open question addressed to this lens directly: **the
seven-family composition is a defensible, well-scoped subset of ordinary
Form 1099-INT/1099-OID/K-1 taxable interest, but it is not the complete
universe a real return can carry** — at minimum, interest reported through a
Form 1041 (estate/trust) K-1, seller-financed mortgage interest, and any
Series EE/I savings-bond interest exclusion interaction (Form 8815) are
absent from the modeled families, and the composition's own `claim` field
does not disclose that absence; it states only what it *does* cover. And
**"declare the box-3 closure" does not, by itself, tell a practitioner what
they are attesting to** — the underlying `f1099int-b3` family's
`closure_claim` text is precise and would be sufficient if surfaced verbatim
("every interest amount reported in box 3... is recorded... says nothing
about other 1099-INT boxes... or total taxable interest"), but the presently
committed `blocked` disposition explain string on the form field is generic
across every missing dependency, not family-specific (confirmed at Hop 1/CB-N1
of Track 0), so a practitioner acting on the *current* rendered text alone
would not yet see that precise language — only the generic one.

## 6. Concrete actions the project could take

- Verify, against the current-year Schedule B instructions text, whether
  Schedule B attachment is independently required by the presence of a
  nominee, accrued-interest, or ABP adjustment regardless of the $1,500
  threshold, and if so, file a decision question about extending
  `tax.us.2025.rule.attachment.schedule-b`'s `requirement` block with that
  independent trigger. (This needs authority verification before any rule
  change; recorded here as a question, not an instruction.)
- Add a rendered "gross seven-family subtotal" line to the Schedule B Part I
  citation group, above the per-adjustment tie-out lines, so the
  gross-minus-adjustments arithmetic that produces the net line-2b figure is
  visible in the rendering rather than only assertable from the rule
  artifact.
- Content-probe: does the product's category list disclose, anywhere a
  preparer would see it, which taxable-interest categories it does *not*
  yet model (estate/trust K-1 interest, seller-financed mortgage interest,
  Series EE/I exclusion interaction)? If not, that absence-of-disclosure is
  itself an actionable gap, independent of whether those categories are ever
  built.
- Decision question: should the `blocked` disposition's `explain` string be
  made family-specific (naming which of the ten `require_closed` conditions
  failed) rather than generic? Track 0 already recorded this as SC-3; this
  account reaches the same gap from the practitioner-reconciliation angle and
  confirms it independently.
- Content-probe: commit the quoted instruction text (or a durable excerpt)
  behind `tax.us.2025.citation.schedule-b` and
  `tax.us.2025.citation.form1040.line-2b`, so a claim like "the seven-family
  composition matches Schedule B Part I" can be checked against source text
  in-repository rather than only against a preparer's memory of the
  instructions, as this account had to do.
- UI/content experiment: test whether a preparer-facing view (as opposed to
  the taxpayer-facing one) should surface the full `closure_claim` text per
  family rather than the generic disposition explain string, since the
  closure_claim text already exists in committed artifacts and is precise
  enough to answer "what am I actually attesting to."

## 7. Threads I deliberately discarded

- **OID acquisition-premium / market-discount subtleties beyond boxes 1 and
  5.** The composition already models 1099-OID box 1 and box 5 (market
  discount) and 1099-INT box 10 (market discount). Finer OID adjustment
  mechanics (e.g., acquisition premium netting that happens on the 1099-OID
  itself before it reaches the taxpayer) are typically pre-netted by the
  payer and would not change what this product needs to model at the box
  level. No plausible near-term action; discarded.
- **Foreign interest and Form 1042-S sourced interest.** Real, and a genuine
  gap in the seven-family universe, but I could not find any modeled
  boundary artifact (family, composition slot, or even a disclosed
  non-goal) to check against — there is nothing committed to verify or
  contradict, so any statement I could make would be speculation about an
  absent feature rather than a finding about present content. Recorded in
  section 6 as part of the general disclosure probe instead of pursued as
  its own thread.
- **Whether the closure horizon concept (a closure being time-keyed and
  capable of going stale) matches how a preparer actually re-opens a prior
  year's data for an amendment.** This shades into system/provenance
  territory (Lens D's assignment) rather than tax-practice adversary
  territory; I noticed it but it is not mine to develop.
- **Whether "we found" as phrasing (Track 0's draft, and Lens A's likely
  territory) is the right register for a casual reader.** I addressed the
  substance of what it implies (section 3) but declined to rewrite it as a
  tone/register problem — that is Lens A's assignment, not mine.

---

## Disclosure

I did not read, open, grep, or `git log` any `track-1-lens-a-*`,
`track-1-lens-c-*`, or `track-1-lens-d-*` file, and I did not read any
section of the charter beyond the lens table and my own (Lens B) assignment
block. I relied on my own professional recollection of the Schedule B "Who
Must File" independent triggers rather than a fetched or committed source
document; every place that recollection is load-bearing is flagged above as
needing verification, not treated as settled.
