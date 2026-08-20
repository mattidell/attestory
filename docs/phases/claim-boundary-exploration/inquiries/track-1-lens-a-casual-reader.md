# Track 1, Lens A — Casual Invested Reader

Audience: Product, Shared (exploratory record).

Status: **exploratory, non-authoritative.** One of four independent lens
accounts produced under the Track 1 charter (removed at publication
curation; its independence rule is restated in the disclosure note below).
Paper analysis of already-committed synthetic content only. No engine run,
generation, or fixture modification was performed. Creates no product
contract and adopts no definition. "Claim boundary" is a working lens for
this phase, not new vocabulary.

The question: **Why is this amount on my return?** — Form 1040 line 2b,
$1825, in the committed fixture
`packages/sample_data/schedule_b_interest_adjustments/presentation/mixed-schedule-b-interest-adjustments.presentation-model.v1.json`.

---

## 1. Lens and standpoint

I file my own return. I pay attention — I read the review screen before I
sign, I've noticed there's a Schedule B, and I roughly know I have a savings
account, a brokerage account, and a bond fund that each send me some kind of
1099 in late January. I am not a CPA and I have never typed the word
"composition" into a sentence about my taxes. When software tells me a
number, I want to know two things in this order: does this match what I
actually got in the mail, and do I need to do anything else before I sign.
I do not care, unless something is wrong, how the number was assembled
internally — I care whether it is complete and whether it is mine.

What I would notice that a professional reviewer would not: I read every
sentence as if it were spoken to me by a person, and I flinch at words that
sound like the software is talking about itself instead of about my money.
"We found," "confirmed as complete so far," "constituent interest
families," "dependencies" — these are the words that make me stop reading
the sentence and start wondering who is on the other end of it. A
practitioner reads past that language to the substance underneath; I read
the language itself as the first signal of whether I can trust what follows.
I also notice, more than a technical reviewer would, whether the sentence
tells me what to *do* next — I am not auditing the artifact chain, I am
deciding whether to keep clicking "continue" or go dig out another envelope.

---

## 2. My best two-sentence plain answer

Track 0's draft:

> This $1825 is the total taxable interest we found from your 1099-INT,
> 1099-OID, and other interest sources for the year, after subtracting any
> nominee, accrued-interest, or bond-premium adjustments you told us about.
> It doesn't include tax-exempt interest (like from municipal bonds), and it
> only reflects the specific interest documents and adjustments you've
> confirmed as complete so far.

I would keep the first sentence's content but not its second sentence, and I
would rewrite both for register. My replacement:

> This $1825 is the total taxable interest from the 1099-INT, 1099-OID, and
> other interest documents you entered, minus any nominee, accrued-interest,
> or bond-premium adjustments — it does not include tax-exempt interest like
> municipal bond interest, which goes on a different line. If you have an
> interest document you haven't entered yet, this number won't include it —
> check your list of accounts against what's here before you file.

The specific defect I'm repairing: Track 0's second sentence
("...only reflects the specific interest documents and adjustments you've
confirmed as complete so far") is the sentence in the whole passage most
likely to be *misread in the wrong direction* by exactly the reader this
lens represents — see section 3, first bullet. "Confirmed as complete so
far" reads to me as reassurance ("you've confirmed it, so it's fine") rather
than as the caveat it's meant to be ("this only covers what you've told us;
tell us more if there's more"). I keep the same information but state it as
an instruction ("check your list... before you file") rather than as a
description of a system state ("you've confirmed... so far"), because an
instruction tells me what to do and a state description makes me guess.
I also moved "we found" to "you entered," because "we found" is precisely
the phrase in Lens instructions I was asked to test, and on reading it
plainly, my answer is that it does raise the question in section 3.

---

## 3. What an intelligent casual user could still misunderstand

Concrete misreadings, not categories:

- **"Confirmed as complete so far" reads as a compliment, not a warning.**
  A careful-but-non-expert reader parses "you've confirmed X as complete" as
  past-tense praise — *I did the thing, it's done* — not as a rolling
  condition that could still be false for documents not yet entered. The
  actual meaning (per Hop 5/CB-N1: a closure is a per-family assertion that
  can be missing or stale) is closer to "as far as what you've told us
  covers." Those are different sentences to a person deciding whether to
  keep digging through mail for more 1099s.

- **"We found" makes me wonder how.** The charter asked me to test this
  directly. My honest answer: yes, it worries me a little, for about one
  second, and then I remember I'm the one who uploaded or typed the
  numbers — so "found" reads as slightly wrong (nothing was discovered; I
  supplied it), not as alarming. The bigger problem than the worry is the
  slight inaccuracy: "found" implies the software went and got something on
  its own, and if I ever *do* wonder how, the honest answer is "you told
  us," which is a better sentence anyway because it correctly assigns the
  work to me.

- **"Doesn't include tax-exempt interest" could read as "irrelevant to
  you," not "reported elsewhere."** A reader with a municipal bond fund
  could take the excluding clause as "we skipped this," full stop, and not
  realize it means "it's on a different line of the same return, still
  accounted for." Track 0's phrasing doesn't say where it went. A reader
  who owns muni bonds and sees no mention of where that interest lives
  might reasonably worry it fell out of the return entirely rather than
  landing on line 2a.

- **The dollar total invites belief it is a closed inventory, not a
  boundaried composition.** Nothing in the plain answer signals that
  "taxable interest" here means exactly seven declared families (Hop 4;
  `tax.us.2025.interest-composition` v4, `required_universe.claim`:
  "Seven declared positive taxable-interest families forming the gross
  Schedule B Part I line-1 basis"). A reader has no way to know from the
  number or the sentence whether some category of interest they hold (say,
  interest from an estate, or seller-financed interest — categories Lens B
  is asked to test for domain completeness) is even eligible to appear
  here. I can't personally judge whether the seven-family list is
  tax-complete — that's Lens B's job — but I can say the plain answer gives
  me no way to notice the boundary exists at all.

- **The CB-N1 blocked state, as currently specified, does not tell this
  reader what to do.** The form field's `blocked` disposition explain
  string (verified in
  `packages/content/tax/2025/form1040.line-2b.form-field.v5.json`, embedded
  identically in the presentation fixture's `field.dispositions.blocked`) is:
  *"Taxable interest is blocked because one or more constituent interest
  families are unclosed or their dependencies are missing."* Reading this as
  the target persona: "constituent interest families" and "dependencies"
  are not words I use about my own taxes, and "one or more" tells me
  nothing about which one. Track 0 already found (section 3, CB-N1) that
  the rule and family definitions could in principle name the exact missing
  family (e.g. "box 3, U.S. Treasury interest"), but the actually-rendered
  `explain` string, as I read it verified above, is generic across every
  possible missing dependency. If this were the sentence I actually saw on
  a blank line 2b, I would not know what to do next — I'd have to guess or
  contact support. Track 0's own finding (SC-3 in
  `actionable-considerations.md`, referenced but not itself in scope for me
  to open) already names this gap; my independent read of the same artifact
  confirms it from the reader's side rather than the artifact's side.

---

## 4. The deepest thread I followed

I drilled into the CB-N1 blocked-state explain string, because Track 0's
open question to this lens asks specifically whether this reader would know
what to do when it appears, and because it's the one place in the whole
chain where a generic system sentence is the *only* thing standing between
a person and a dead end.

What I opened and checked directly, beyond what Track 0 already cited:

- `packages/content/tax/2025/form1040.line-2b.form-field.v5.json` — the
  `blocked` disposition's `explain` field, confirmed byte-identical to the
  copy embedded in the presentation fixture's `sections[5].field` object.
  Generic across all four `blocked` codes
  (`DEPENDENCY_ABSENT`, `DEPENDENCY_INVALID`, `CATEGORICAL_DOMAIN_MISMATCH`,
  `SOURCE_SET_UNCLOSED`) — the same one sentence renders for all of them.
- `packages/content/tax/2025/family.f1099int-b3.json` — the box-3 family's
  own `closure_claim`: *"Every interest amount reported in box 3 of a Form
  1099-INT furnished to the taxpayer for tax year 2025 is recorded as a
  statement item. This claim covers Form 1099-INT box 3 only: it says
  nothing about other 1099-INT boxes, interest not reported on Form
  1099-INT, or total taxable interest (Form 1040 line 2b)."* This text is
  precise and scoped — but it lives on the *family* artifact, not on the
  *blocked-disposition* explain string a user would actually see. Nothing
  in the rendering path I traced connects the two: the form field's
  `blocked.explain` does not interpolate a family name or reference the
  family's own `closure_claim` text.
- `packages/content/tax/2025/rule.form1040-line2b.v4.json` (already cited
  by Track 0) — confirmed the rule's `when` clause does carry seven
  distinct `require_closed` conditions, one per family, meaning the
  computation layer *can* in principle know exactly which one failed. The
  gap is entirely in the presentation-facing `explain` text, not in the
  underlying data.

**Did this change my answer?** It sharpened rather than changed it. My
two-sentence answer in section 2 already avoids over-promising ("check your
list... before you file" rather than naming a specific missing family),
precisely because the drill-down confirmed that the artifact chain, as
currently rendered to a user, cannot yet name the specific family in the
blocked case — only the underlying rule data could support that, and it
isn't surfaced. So the boundary of what a plain answer can honestly claim
in the CB-N1 state is narrower than Track 0's optimistic framing ("the
system already carries per-family guards and explanation strings")
suggested to me on first read of section 3: the *guard* exists, but the
*explanation string a user sees* does not yet use it. That is a rendering
gap, not a data gap, and it belongs to Track 0's SC-3, which I independently
re-derive here from the reader's side rather than defer to.

---

## 5. Where my explanation terminates

I stop at the same three edges Track 0 does, verified independently:

- The individual document-level amounts behind the 1825 total (the
  underlying `finding:derived:*` subtotal ids) are not committed as
  separate files anywhere in this fixture's directory — I checked; there is
  no sibling file for `finding:derived:630fc8ba506b2ea2ef0f2f35` or its
  seven subtotal inputs. I cannot show a reader "here is your 1099-INT box
  1 amount, here is your box 3 amount" from committed content alone. That
  is a genuine floor on how far *this* trace can decompress, not a defect I
  can resolve by reading harder.
- Whether the seven-family composition is the legally correct universe for
  an ordinary filer is outside what I, as this lens, can adjudicate — I can
  only report that the plain answer gives no signal the boundary exists
  (section 3). Lens B is the account that can actually test the domain
  question.
- I do not know, and did not check, whether the box-3 closure declaration
  in the fixture is itself real or stale — CB-N1 is a paper mutation, not
  something performed. My account of the blocked-state explain string is
  about the artifact's rendered text as committed, not about any actual
  blocked run.

---

## 6. Concrete actions the project could take

- Replace "confirmed as complete so far" with an instruction-shaped
  sentence ("check X before you file") in any future plain-answer draft, on
  the evidence in section 2/3 that the state-description phrasing reads as
  reassurance rather than caveat to this persona. This is a content
  probe — worth testing against an actual naive reader, not just this
  simulated one.
- Add, to the plain answer or an adjacent one-line note, where excluded
  tax-exempt interest actually goes ("reported separately on line 2a"),
  rather than only saying what it excludes. Concrete content change, no
  schema or artifact touch required — it's a sentence-composition decision
  for whoever drafts the eventual answer text.
- Interpolate the specific missing family name into the `blocked`
  disposition's rendered `explain` text, using the per-family
  `require_closed` conditions the rule (`rule.form1040-line2b.v4.json`)
  already carries and the scoped `closure_claim` text each family artifact
  (e.g. `family.f1099int-b3.json`) already carries. This is a rendering/
  content change to the form-field's disposition template, not a new
  artifact type; I flag it as a decision question for whoever owns
  form-field content, since it touches a schema field's authored text, not
  something this documentation-only track can adopt.
- Run a probe question against a genuinely naive reader (not a simulated
  lens): given only the rendered `blocked.explain` string as committed
  today, can they state in their own words what they'd have to go do? My
  prediction, from this account, is no — worth confirming against a real
  person before spending effort on the interpolation fix above.
- Consider a one-line addition to the plain answer naming the boundary of
  "taxable interest" as used here (e.g. "this covers interest reported on
  1099-INT, 1099-OID, and similar documents you entered") so a reader with
  an unusual interest source at least knows there's a category question to
  ask, without requiring the answer to enumerate all seven families by
  name.

---

## 7. Threads I deliberately discarded

- **Whether "we" in "we found" refers to a company, a model, or a specific
  feature.** I considered pursuing who or what "we" grammatically resolves
  to in a shipped product, but there is no committed user-facing copy
  artifact that uses first-person plural — the plain answer is Track 0's
  draft prose, not a rendered string from any fixture. Chasing the referent
  of a pronoun in draft-only prose has no artifact to check against and no
  action it could produce beyond what I already said in section 3 (replace
  "we found" with "you entered").
- **Whether the $1825 figure itself is plausible arithmetic given the
  fixture's constituent parts.** I could have tried to reconstruct the sum
  from whatever subtotal data is visible, but Hop 2's own gap (no committed
  subtotal files) makes this unverifiable from committed content, and even
  if I could reconstruct it, arithmetic correctness is not this lens's
  question — a casual reader does not re-derive the sum, they ask whether
  the *inputs* are theirs and complete. No plausible action for this lens.
- **The empty `pinLabels` map and unresolved `demo.*` citation-site pin
  ids in the presentation fixture's top level.** I opened the fixture and
  noticed this (see section 4's file list) while locating the `blocked`
  disposition text, but this is squarely Lens D's provenance question, not
  a casual-reader question — a person reading the review screen never sees
  a `pinLabels` object. Reporting it here only to disclose that I saw it in
  the course of my own drill-down, not as an angle I pursued.

---

## Disclosures

- I did not open, read, or search for any `track-1-lens-b`,
  `track-1-lens-c`, or `track-1-lens-d` file, and did not encounter one
  unintentionally while working only inside my assigned output path and the
  shared-substrate/verification files named in the charter.
- No engine run, `live_coordinate_run`, or artifact generation was
  performed. All figures, disposition text, and claim strings above were
  read directly from already-committed content at the commit named in the
  Orientation Block for this session.
- No personal data, real value, or workspace path appears above.
