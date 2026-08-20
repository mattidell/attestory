# Track 0 Inquiry Frame — "Why is this amount on my return?" (Form 1040 line 2b)

Audience: Product, Shared (exploratory record).

Status: **exploratory, non-authoritative.** This packet is paper analysis of
already-committed synthetic content and public tax instruction text. It
creates no product contract, adopts no definition, and reinterprets no
accepted contract. "Claim boundary" here is a working lens for this phase,
not new vocabulary or a citizen. Governance and accepted ADRs remain
authoritative for what existing artifacts mean.

Selected scenario: Form 1040 line 2b, "Taxable interest," traced against the
committed fixture
`packages/sample_data/schedule_b_interest_adjustments/presentation/mixed-schedule-b-interest-adjustments.presentation-model.v1.json`
(`presentation-model.v1`, `runId` `demo.sbia.golden.combined`), adopted under
core package v15 (`packages/sample_data/schedule_b_interest_adjustments/adoptions/adopt-core-v15-current.json`),
verified against core package v33
(`packages/content/tax/2025/package.core-calculations.v33.json`,
`artifact-package.v25`).

**Corrected by the final repair.** This packet originally called v33 the
"current selected" package. It is not. v33 is the highest-numbered core
package present in the repository and the comparison target this inquiry
chose; **no committed artifact designates a current package.** The supported
claim throughout this packet is narrower than "current" — it is that the
line-2b chain is **unchanged** between the fixture's adopted v15 and v33.
Read every later mention of "the current package" in this file as "the v33
comparison target."

---

## 1. User situation and compressed subquestions

Picture someone who has just finished a simple return in a review screen. They
see a row labeled "Taxable interest" on what will become Form 1040, with a
dollar amount next to it, under a section that also lists other lines (wages,
capital gains, other income) they recognize less confidently. They did not
build this number by hand; they uploaded or answered questions about a few
1099 forms and some other interest they knew about, and the product produced
a total. They ask, out loud or to themselves:

> Why is this amount on my return?

That single sentence compresses several different questions, and the person
asking it usually is not aware they are asking more than one:

- **Where did this number come from?** Which documents or answers they gave
  turned into this figure, and can they see the pieces that were added
  together?
- **Is it correct?** Not "did the software do arithmetic right" but "does this
  match what I actually received," which the person cannot verify from the
  number alone.
- **Is it all of it?** Whether every interest-bearing account or document they
  have is reflected, or whether something is missing that they need to add.
- **Do I owe because of it?** Whether this number, by itself, is the thing
  that increases their tax, or whether it is one ingredient among several.
- **What do I do now?** Whether they need to take an action — find a missing
  document, correct an entry, attach something, or nothing at all.

The person does not use words like "closed," "source family," "composition,"
or "disposition." They are asking about a number on a form they will sign.
Any explanation that starts by naming those internal terms has already lost
the thread of the actual question, which is about provenance, correctness,
completeness, tax consequence, and next action — in the user's own terms, not
the system's.

---

## 2. The support chain, traced against current content

Each hop below states: the artifact id and version selected by the *current*
package (core v33) unless marked otherwise, the file, what it contributes to
the visible number, and who is speaking through it — the user (an assertion
they made or a document they hold), the source document itself, an adopted
project artifact (the product's own construction), or tax authority (the IRS
text the artifact claims to implement).

### Hop 0 — Presentation row

- **Artifact:** section `line-2b` inside the committed presentation model
  (`presentation-model.v1` schema; no separate id/version of its own — it is
  the rendering, not a versioned citizen).
- **Contributes:** the rendered label "Taxable interest," the disposition
  `published_value`, and the displayed value `1825` (a synthetic figure), plus
  five `citationSites` naming pin ids (`demo.cgd.t2.finding.rounding`,
  `demo.md.finding.1099int`, and three `demo.sbia.finding.*` adjustment pins)
  that the row's tie-out points a reader toward.
- **Who is speaking:** an adopted project artifact — the presentation layer
  reporting the current disposition of a finding that was computed under an
  adopted package.
- **Gap found:** the presentation model's top-level schema
  (`attachments`, `citationGroups`, `pinLabels`, `runId`, `schema`,
  `sections`) carries **no field naming the adopted package or release**. That
  part of the charter's framing is confirmed. However, **the individual
  rendered finding does carry an adoption pin** — see Hop 2. So the precise
  finding is: the *row itself* (and the presentation model's top-level
  metadata) does not say which package produced it; a reader has to open the
  nested finding to find that out. This is a narrower and more accurate
  statement than "the presentation model does not record its adopted
  package" as phrased in the charter — the record exists, just not where a
  reader would look first. Also confirmed: `pinLabels` is an **empty
  object** in this fixture, so none of the pin ids referenced in
  `citationSites` (e.g. `demo.md.finding.1099int`) resolve to a human-readable
  label from the presentation model itself; a reader must resolve them
  elsewhere (they are not present as separate committed files in this
  fixture's own directory either).

### Hop 1 — Form field

- **Artifact:** `tax.us.2025.form1040.line-2b` v5, `form-field.v3` schema,
  file `packages/content/tax/2025/form1040.line-2b.form-field.v5.json`.
  Confirmed byte-identical to the field object embedded in the presentation
  row.
- **Contributes:** binds the symbol `tax.us.2025.interest.taxable-total` to
  Form 1040 line 2b; carries the citation pointer
  `tax.us.2025.citation.form1040.line-2b` v1; and defines the disposition
  vocabulary the row uses to describe its own state (`published_value`,
  `computed_zero`, `closure_backed_zero`, `guard_inapplicable`, `blocked`),
  each with its own render template and plain-English `explain` string
  authored into the artifact itself (e.g. "Taxable interest is blocked
  because one or more constituent interest families are unclosed or their
  dependencies are missing.").
- **Who is speaking:** an adopted project artifact — it defines form
  placement and self-description vocabulary; it does not itself assert a tax
  amount.

### Hop 2 — Derived finding and its pins

- **Artifact:** an inline derived finding, `derived-finding.v2` schema,
  `symbol` `tax.us.2025.interest.taxable-total`, `value` `1825`, embedded in
  the presentation row's `resolved.act.finding` (no separate committed file;
  it exists only inside this fixture).
- **Contributes:** the actual computed number, and a `pins` array recording
  everything the number depended on: the package adoption
  (`tax.us.2025.package.core-calculations`, role `adoption`, version **v15**
  — this is the one place the adopted package identity is recorded), the
  computation rule and citation used, seven closure-assertion pins (one per
  positive interest source family plus the three Schedule B adjustment
  families), seven `finding:derived:*` input pins (the underlying subtotal
  findings), and ten `closure-mapping.*` package pins.
- **Who is speaking:** a mix — the `origin: "assertion"` pins are the user's
  (or their preparer's) own closure declarations ("I have entered every
  document in this category as of this horizon"); the `role: "package"` pins
  are adopted project artifacts; the finding's numeric value itself is the
  system's computed conclusion from those inputs.
- **Gap found:** none of the underlying subtotal `finding:derived:*` ids
  (e.g. `finding:derived:14be17055289ccf0eaade470`) resolve to a committed
  file in this fixture's directory. The packet cannot show the individual
  1099-INT box amounts that summed to 1825; only the rule and composition
  that describe how such amounts would combine, and the tie-out text
  ("Reported subtotal: 1825") in the Schedule B citation group.

### Hop 3 — Computation rule

- **Artifact:** `tax.us.2025.rule.form1040-line2b` v4, `rule-artifact.v3`
  schema, file `packages/content/tax/2025/rule.form1040-line2b.v4.json`.
  **Confirmed identical in v15 and v33** (same version, schema, and role).
- **Contributes:** the actual formula — sum of seven positive-interest
  subtotals (`b1`, `b3`, `oid-b1`, `non-form`, `form1065-k1.box5`, `b10`
  market discount, `oid-b5` market discount) minus three Schedule B adjustment
  subtotals (nominee distribution, accrued interest, ABP adjustment), guarded
  so a negative result is not published if adjustments exceed the positive
  basis. The rule's own `notes` field states this is "the exact seven-family
  positive-interest composition less the three exact closed Schedule B
  adjustment classes."
- **Who is speaking:** an adopted project artifact encoding a computation the
  product asserts implements the tax rule — not itself tax authority.

### Hop 4 — Composition

- **Artifact:** `tax.us.2025.interest-composition` v4,
  `taxable-interest-composition.v1` schema, file
  `packages/content/tax/2025/interest-composition.v4.json`. **Confirmed
  identical in v15 and v33.**
- **Contributes:** the declared "required universe" — its own `claim` field
  states: "Seven declared positive taxable-interest families forming the
  gross Schedule B Part I line-1 basis, without subtractive adjustments." This
  is the artifact that names, structurally, what counts as "taxable interest"
  for this computation and, by omission, what does not (see CB-A2 in
  section 3).
- **Who is speaking:** an adopted project artifact declaring the scope of
  the composition — a product-authored boundary statement, not a tax-law
  quotation.

### Hop 5 — Source-family authority and closures

- **Artifacts:** four families actually populated in this fixture —
  `tax.us.2025.f1099int.b1`, `tax.us.2025.f1099int.b3`,
  `tax.us.2025.f1099oid.b1`, `tax.us.2025.non-form-interest` (each
  `source-family.v1`, v1, **confirmed identical in v15 and v33**) — plus
  their closure mappings (`closure-mapping.f1099int-b1` etc., also confirmed
  identical) and the three Schedule B adjustment source families (nominee,
  accrued interest, ABP adjustment) and their subtotal rules, also confirmed
  identical. The remaining three positive families in the seven-family
  composition (`form1065-k1.box5`, `f1099int.b10`, `f1099oid.b5`) are present
  in the fixture's finding pins but their contribution to the 1825 total
  cannot be separated from the committed data alone.
- **Contributes:** each source family's `closure_claim` states precisely what
  a "closed" declaration for that family does and does not cover (e.g. the
  box-8 family's claim explicitly disclaims boxes 1, 3, 10, and line 2a — see
  Hop 5b). A closure is the user's (or preparer's) assertion that every
  document of that specific kind as of a given horizon has been entered.
- **Who is speaking:** the closure assertions are the user's; the family and
  closure-mapping definitions are adopted project artifacts defining what a
  closure over that family means.

### Hop 5b — Adjacent family not on this chain (context for CB-A2)

- **Artifact:** `tax.us.2025.f1099int.b8` (Form 1099-INT box 8, tax-exempt
  interest), `source-family.v1` v1, file
  `packages/content/tax/2025/family.f1099int-b8.json`. **Confirmed absent
  from v15, present in v33**, along with its closure mapping, subtotal rule,
  the quantity `tax.us.2025.quantity.tax-exempt-interest`, and
  `tax.us.2025.citation.publication-550.tax-exempt-interest`.
- **Contributes:** nothing to line 2b. Its own `closure_claim` states it
  covers "Form 1099-INT box 8 only: it says nothing about boxes 1, 3, or 10
  ... or Form 1040 line 2a completeness." Box 8 tax-exempt interest is
  reported on Form 1040 line 2a, a different line, and is explicitly excluded
  from the taxable-interest composition at Hop 4.
- **Who is speaking:** an adopted project artifact defining a family that is
  adjacent to, and structurally separate from, the line-2b chain.

### Hop 6 — Citations

- **Artifacts:** `tax.us.2025.citation.form1040.line-2b` v1 (`citation.v1`,
  confirmed identical v15/v33) and `tax.us.2025.citation.schedule-b`
  (referenced by the attachment rule's `requirement.citation`). Both citation
  artifacts, as committed, are **authority pointers only** — they carry
  `authority.family`, `form_id`/`publication`, and `tax_year` metadata, not
  quoted instruction text.
- **Who is speaking:** an adopted project artifact naming which IRS source it
  claims to follow. It is not itself the IRS text.

### Hop 7 — Attachment rule (Schedule B)

- **Artifact:** `tax.us.2025.rule.attachment.schedule-b` v4,
  `attachment-rule.v6` schema, file
  `packages/content/tax/2025/rule.attachment.schedule-b.v4.json`.
  **Confirmed identical in v15 and v33.**
- **Contributes:** the full Schedule B Part I row structure (the same seven
  source families and three adjustment rows as the computation rule, restated
  as a form itemization), the requirement that Schedule B attaches when
  positive interest plus ordinary dividends exceeds a threshold parameter
  (`tax.us.2025.parameter.schedule-b-threshold`, confirmed identical
  v15/v33), and Part II (ordinary dividends). Its own `title` field states
  the row structure and the requirement in prose.
- **Who is speaking:** an adopted project artifact implementing the Schedule
  B attachment and itemization rule.

### Hop 8 — Official tax sources (grounding, not permission)

These are cited for what the line and its schedule are *intended* to report,
per general public IRS guidance for Form 1040 and Schedule B (Interest and
Ordinary Dividends): Form 1040 line 2b calls for total taxable interest,
computed from all 1099-INT/1099-OID and other taxable-interest receipts, net
of any adjustments a preparer must subtract (nominee distributions, accrued
interest purchased between interest dates, and amortizable bond premium
elections) — the same three adjustment classes the attachment rule
implements. Schedule B Part I is required when taxable interest exceeds a
dollar threshold or in certain foreign-account/foreign-trust circumstances.
**Corrected by the final repair — this sentence understates the IRS rule and
mislocates the foreign-account condition.** The 2025 IRS instructions give
**eight independent** "Who Must File" triggers, seven of them categorical with
no dollar threshold. The committed rule implements only the dollar-threshold
trigger, testing `interest.positive-total` and `dividends.ordinary-total`
independently (not summed) against the threshold. The foreign-account and
foreign-trust questions are `completeness.required_answers` that apply *after*
Schedule B attaches; they are not attachment triggers. See `OV-1`.
Tax-exempt interest (municipal bond interest, reported in Form 1099-INT box
8) is reported separately, on Form 1040 line 2a, and is not part of taxable
interest — consistent with IRS Publication 550's treatment of tax-exempt
versus taxable interest.

**This section grounds what the line is meant to report; it is not read as
license to describe behavior the package does not implement.** Everything
this packet says the *system* does is stated from the artifacts above, not
from the instruction text.

---

## 3. Positive case CB-P1 and boundary case CB-N1

### CB-P1 — the fixture as committed

The rendered row shows "Taxable interest … $1825," disposition
`published_value`. The support chain (hops 0–7 above) is intact end to end,
with the material chain (rule v4, form-field v5, citation v1, composition v4,
attachment-rule v4, threshold parameter v1) verified identical between the
fixture's adopted package (v15) and the current package (v33). A user asking
"why is this amount on my return" can be shown, in order: the label and
value; the seven-family composition claim; which of those families were
actually populated and which subtotal rows and adjustment rows tie into the
number (via the Schedule B citation group's tie-out text); the closure
assertions that stand behind each family; and the citations to Form 1040 and
Schedule B. What cannot currently be shown from committed content alone: the
individual document-level amounts behind the subtotal findings (they are not
committed as separate files), and — from the row itself, without opening the
nested finding — which package version produced the number.

### CB-N1 — paper mutation, one necessary closure removed

**Mutation (described, not performed):** suppose the `f1099int.b3` closure
assertion referenced by this finding's pins were withdrawn or left stale —
the user never declared "I have entered every box-3 (U.S. Treasury interest)
1099-INT I hold" for the current horizon, or that declaration is now expired.
The computation rule's `when` clause requires `require_closed` on
`tax.us.2025.f1099int.b3` (among the other nine) before it will
publish. **Corrected after the Track 3 repair:** the rule carries **ten**
`require_closed` conditions, not seven — the seven positive families plus the
three subtractive adjustment classes. Track 2 carried the same miscount and it
is corrected there too. With that one requirement unmet, the rule's `when.op: "all"` fails,
and the form field's own `blocked` disposition applies: `DEPENDENCY_ABSENT` /
`SOURCE_SET_UNCLOSED`, with the artifact's own explain text: "Taxable
interest is blocked because one or more constituent interest families are
unclosed or their dependencies are missing." The row would render blank
(`render: ""`).

**What the system could honestly say, working from the artifacts alone:** it
can name the exact unmet requirement — the box-3 (U.S. Treasury interest)
closure declaration is absent or stale — because that is precisely what the
rule's `when` clause and the family's own definition assert is required. It
can state a concrete next action: declare (or renew) the box-3 closure, i.e.
confirm whether all box-3 interest documents for the current horizon have been
entered. It does **not** need to say the whole return, or even the whole
"Taxable interest" concept, is incomplete — the other nine requirements and
their closures remain intact and nameable; only this one is unmet.

**Corrected after the Track 3 repair.** An unmet closure does not establish
that a document exists and is missing. It establishes only that the user has
not declared the family complete, which is equally consistent with holding a
box-3 document and not entering it, holding none, or not having reached the
step. The honest statement names the undeclared family and asks; it does not
assert a missing document.
This distinction — *one named family unclosed* versus *the return is
incomplete* — is exactly the kind of collapse the milestone's standing risk
("infinite decompression"/"a private explanatory dialect") warns against
erasing, and exactly what the boundary case is meant to test whether the
current artifacts can support without a code change. On the evidence read
here, they can: the rule already carries per-family `require_closed` guards
and the form field already carries a disposition explanation string for this
exact case. What is not present in committed content is a rendering that
*names which specific family* is missing in user language — the current
`blocked` disposition's `explain` string is generic across all missing
dependencies, not family-specific. That gap is recorded as an actionable
consideration in `actionable-considerations.md` (see SC-3).

---

## 4. Draft two-sentence answer

> This $1825 is the total taxable interest we found from your 1099-INT,
> 1099-OID, and other interest sources for the year, after subtracting any
> nominee, accrued-interest, or bond-premium adjustments you told us about.
> It doesn't include tax-exempt interest (like from municipal bonds), and it
> only reflects the specific interest documents and adjustments you've
> confirmed as complete so far.

**What it deliberately does not claim:** it does not claim the figure is
legally final or that filing has occurred; it does not claim every possible
interest-bearing account has been found (only that the families the user
declared closed are reflected); it does not use the words "integrity" or
"complete" as a claim about the whole return; and it does not claim to be a
professional tax opinion — it describes what the computation and its
declared inputs support, nothing about what a preparer or the IRS would
independently determine.

---

## 5. Open questions handed to Track 1

Stated as questions, not conclusions, for the four lens accounts to point at
independently:

1. **Casual invested reader:** Does the draft two-sentence answer in section
   4 actually read as an answer to "why is this amount on my return," or does
   it still smuggle in system framing (e.g. "confirmed as complete so far")
   that a first-time user would not parse correctly? Would this reader expect
   to be shown *which* documents contributed, and is the absence of
   document-level detail (Hop 2's gap) a real deficiency or an acceptable
   summary level?

2. **Tax/financial-practice adversary:** Is the seven-family composition
   (Hop 4) actually the correct and complete universe of "taxable interest"
   for an ordinary Form 1040 filer, or does the domain include categories
   this composition's own `required_universe.claim` does not mention (e.g.
   original issue discount variants, foreign interest, seller-financed
   interest)? Does the CB-N1 explanation ("declare the box-3 closure") give a
   practitioner enough to act on, or does it understate what "closed" is
   actually attesting to?

3. **Legal/epistemic adversary:** Does distinguishing "computational support"
   from "legal effect of filing" (CB-A1 in the milestone's synthetic-scenario
   table) hold up under this specific trace, or does some hop above (e.g. the
   citation artifacts being bare authority pointers with no quoted text)
   create an unsupported inference that the number already carries IRS
   sign-off? Is "closure_claim" language (e.g. "every ... amount ... is
   recorded ... as of the keyed horizon") itself a claim strong enough to
   mislead about completeness if surfaced verbatim to a user?

4. **System/provenance adversary:** Given that the presentation row's
   top-level metadata does not name the adopted package (Hop 0) while the
   nested finding does (Hop 2), and given that the referenced
   `finding:derived:*` subtotal ids and `demo.*` pin ids do not resolve to
   committed files in this fixture's own directory, how much of the
   provenance chain is actually recoverable by a downstream consumer (a UI, a
   reviewer, an auditor) without external context? Does CB-A2 — the box 8
   tax-exempt-interest family sitting adjacent to, but invisible from, this
   fixture — represent a broader pattern where "included universe" is
   knowable only by cross-referencing the current package, not by reading
   the presentation output?

---

## Notes on evidence and process

- All version and content claims above were checked directly against the
  committed package files (`package.core-calculations.v15.json` and
  `.v33.json`) and the named content files at this session, not merely
  restated from the charter.
- No engine run, `live_coordinate_run`, or artifact generation was performed.
  All figures and dispositions above are read from already-committed
  synthetic content.
- CB-A1 and CB-A2 (the two adversarial synthetic-scenario rows from the
  milestone table) are named here as grounding for the open questions in
  section 5; their accounts belong to Track 1, not this packet.
