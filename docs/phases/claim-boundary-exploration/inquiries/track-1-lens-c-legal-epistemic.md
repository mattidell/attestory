# Track 1, Lens C — Legal / Epistemic Adversary

Audience: Product, Shared (exploratory record).

Status: **exploratory, non-authoritative.** One of four independent lens
accounts produced under the Track 1 charter (removed at publication
curation; its independence rule is restated in the disclosure note below).
Paper analysis of already-committed synthetic content and public tax
sources; no run, no execution, no generated artifact. Creates no product
contract, adopts no definition, reinterprets no accepted contract. "Claim
boundary" is a working lens for this phase, not governance vocabulary.
Governance and accepted ADRs remain authoritative for what existing
artifacts mean.

Case emphasis: **CB-A1** — does the output hold the line between tax
meaning, computational support, and the legal effect that attaches only at
filing?

I did not read, open, grep, or `git log` any other `track-1-lens-*` file,
and I did not read the other lenses' assignment blocks beyond the routing
table in the charter. No contamination to disclose.

---

## 1. Lens and standpoint

I am reading as someone whose job is to ask, of any sentence a piece of
software puts in front of a taxpayer: *who is speaking, what exactly are
they claiming, and what is the reader now entitled to believe as a result?*
That is a legal-drafting habit as much as a tax habit — it does not require
me to know whether the seven-family composition is the right domain
coverage (that is a different adversary's job); it requires me to know
whether every sentence's speaker and scope are accurate, and whether a
reasonable reader would infer more than the artifact actually supports. I
take an unfiled rendering seriously in both directions: it has no legal
effect (nobody has signed anything, nothing has been transmitted to the
IRS), and it is not therefore inert or meaningless — it is a computed
statement resting on the user's own entries, and language that blurs *which*
of those two things it is does real harm even before a return is filed.

What I notice that a casual reader or a practitioner would not: passive and
third-person constructions that quietly relocate agency ("we found," "a
current cited derived finding publishes," "is recorded as a statement
item"); present-tense declarative claims sitting where a conditional or
attributive claim belongs; and vocabulary reused across a legal register and
a casual one in ways that could collide (e.g., "attested," "confirmed," and
"closed" all have ordinary meanings a taxpayer would apply to the actual act
of filing and signing, distinct from their technical meanings here).

---

## 2. My best two-sentence plain answer

I would change Track 0's draft. Track 0's version:

> This $1825 is the total taxable interest we found from your 1099-INT,
> 1099-OID, and other interest sources for the year, after subtracting any
> nominee, accrued-interest, or bond-premium adjustments you told us about.
> It doesn't include tax-exempt interest (like from municipal bonds), and it
> only reflects the specific interest documents and adjustments you've
> confirmed as complete so far.

My replacement:

> This $1825 is the taxable-interest total your return currently shows,
> built from the 1099-INT, 1099-OID, and other interest items you've entered
> and told the software are complete, minus any nominee, accrued-interest,
> or bond-premium adjustments you entered — it excludes tax-exempt interest
> like municipal-bond interest. Nothing about this figure has legal effect
> until you file; right now it reflects what you told the software, not an
> independent check against your documents or a determination by the IRS.

The specific defect this repairs: "we found" attributes discovery/agency to
the system. Verified against governance: ADR-0009 (`docs/adr/0009-derived-finding-shape.md`)
holds, as ratified doctrine, that "the machinery is never the author of
anything" and that a derived finding's authority runs through its pins to a
publication act, to an adoption act, to the user — "the user is the author
of both finding kinds ... the way the results in a spreadsheet belong to the
person who built the sheet." "We found" says the opposite of the project's
own authorship doctrine: it tells the user the software went and discovered
something, rather than that the software summed what the user put in. It
also invites exactly the CB-A2-adjacent inference that the system
independently verified completeness — which the fixture's own evidence (see
§3, §5) does not support. My version also states the filing-effect boundary
explicitly, in the two sentences themselves, rather than leaving it to
prose underneath the draft answer (as Track 0 does) — that boundary is my
case emphasis and I think it belongs in the sentence a user actually reads.

---

## 3. What an intelligent casual user could still misunderstand

Concrete misreadings, checked against the actual fixture content
(`packages/sample_data/schedule_b_interest_adjustments/presentation/mixed-schedule-b-interest-adjustments.presentation-model.v1.json`,
`line-2b` section, and the citation artifacts it points at):

1. **"We found" reads as an audit claim.** A reader could believe the
   software independently verified their interest income against some
   external record (payer filings, IRS matching), rather than summing
   entries the user made and told the software were complete. Nothing in
   the committed chain performs any such independent verification — the
   `pins` on the line-2b finding are the adopted package, the rule, the
   citation, and the user's own closure assertions and their transitively
   derived subtotals (see §4). There is no payer-side or IRS-side input pin
   anywhere in this finding.

2. **"Confirmed as complete" reads as a legal attestation.** Track 0's
   phrase risks being read as equivalent to the jurat a taxpayer signs on
   Form 1040 ("under penalties of perjury..."). It is not — it is a
   workspace-level closure declaration, a different act with different
   consequences, made before filing and revocable/updatable up to that
   point. Nothing in the rendered row or its citation sites distinguishes
   "you told the software this category is done" from "you swore to the
   IRS this is true." My replacement avoids the word "confirmed" for this
   reason and states the filing boundary directly instead of implying it.

3. **The citation pointers could be read as IRS sign-off, if ever rendered
   as inline "citations."** I opened both citation artifacts on this
   line's chain:
   `packages/content/tax/2025/citation.form1040.line-2b.json` and
   `packages/content/tax/2025/citation.schedule-b.json`. Both are, as
   committed, bare authority pointers — `{schema: citation.v1, authority:
   {family: "irs-instructions", form_id, tax_year}}` — with no quoted
   instruction text, no publication section, no URL. As currently rendered
   in this fixture, they surface only as `citationSites` entries with
   plain tie-out text ("Reported subtotal: 1825") and a `pinId`, not as a
   user-facing footnote reading "per IRS Publication X §Y." That is a
   real mitigation — the fixture does not currently claim more than it can
   support. But the word "citation" in ordinary usage implies verification,
   and if any future surface renders these pointers as inline citations
   next to the dollar amount, an intelligent reader could reasonably infer
   the IRS reviewed and endorsed this specific figure, which no artifact
   on this chain asserts or could assert.

4. **"Attested closed" in the `closure_backed_zero` disposition's explain
   text collides with a distinct technical meaning elsewhere in the
   project.** The line-2b form field's `closure_backed_zero` disposition
   (`packages/content/tax/2025/form1040.line-2b.form-field.v5.json`, as
   embedded in the presentation row) reads: "A current derived finding
   publishes a zero because all constituent families are **attested closed**
   on their current horizons..." The kernel's `finding.v1` schema reserves
   `basis: attested` specifically for a human determination distinct from a
   document or an election (ADR-0009, Context section). A derived finding
   has no `basis` field at all — ADR-0009 decision 1 is explicit that
   giving one a human-authority `basis` like `attested` "would misrepresent
   authority." The disposition's explain text uses "attested" as ordinary
   English, not as the kernel's reserved vocabulary, but a reader who knows
   the schema (or a future engineer copying this string into a different
   surface) could read it as claiming the closure itself is a kernel
   `finding.v1` with `basis: attested`, which it structurally is not on
   this chain. This did not change my two-sentence answer — it is a
   terminology-hygiene risk in a string that is not shown to the casual
   user in this fixture's rendering path — but it is concrete enough to
   name (see §6.5).

---

## 4. The deepest thread I followed

**Question:** Does CB-A1's required distinction — computational support
versus the legal effect that attaches at filing — actually hold up as
something this project's own governance can support, or would a fuller
answer here require inventing doctrine that does not exist yet?

**What I opened, in order:**

- `packages/schemas/derivation/derived-finding.v2.schema.json` — confirmed
  the `pin` shape: `role` enum includes `input`; a pin with `role: input`
  *requires* an `origin` of `assertion` or `declared_default`. The schema's
  own description states origin is recorded "transitively" — i.e., it marks
  where the resolved chain ultimately bottoms out, not that the tagged pin
  is itself a raw user act.
- The `line-2b` finding's own `pins` array (re-examined from the fixture
  already cited above): every `role: input` pin carries `origin: assertion`
  — both the seven `demo.*.closure.*` pins (e.g. `demo.md.closure.int-b1`,
  `demo.sbia.closure.nominee`) *and* the ten `finding:derived:*` pins (e.g.
  `finding:derived:14be17055289ccf0eaade470`). Track 0's Hop 2 states "the
  `origin: assertion` pins are the user's (or their preparer's) own closure
  declarations." That is true for the `demo.*.closure.*` pins. It is not
  precise for the `finding:derived:*` pins: those are *computed subtotal
  findings* — the system's arithmetic over underlying document entries —
  that happen to trace transitively back to an assertion rather than to a
  system-supplied default. Both pin kinds share `origin: assertion`, but
  one is a direct user declaration and the other is a machine computation
  resting on one. A reader working only from Hop 2's prose (not the schema)
  could reasonably — and wrongly — read all fourteen `assertion`-origin
  pins as literal statements the user personally made. This is exactly the
  "speaker role... misattributed" question the charter asked me to check,
  and I find a real, if narrow, imprecision in Track 0's account: it
  collapses "directly asserted by the user" and "computed, but
  assertion-backed" under one description.
- `docs/adr/0009-derived-finding-shape.md` (accepted, ratified 2026-07-11)
  — read in full. Decision 1 establishes that a derived finding's ground is
  "mechanical and fully pinned: pins → publication act → adoption act →
  user," and that this chain "is the recorded instrument framing... the
  user's authorship, reachable through the record." This is the doctrinal
  basis for my §2 correction ("we found" understates that the number is the
  user's own construction, not the system's).
- The same ADR's "What T1 still reserves" section, read carefully, names as
  explicitly **unbuilt**: "what instrument-authorship amounts to at the
  filing boundary (where workspace acts meet legal acts)." That is not a
  tangential reservation — it is *the* boundary CB-A1 asks Track 1 to test.
- `docs/governance/README.md` — confirmed "T1 derived-finding authority" is
  still listed in the standing conformance backlog as review-dependent open
  work, not resolved doctrine, as of this reading.
- `AGENTS.md` (lines ~223–227) — confirmed the live guardrail text: "do not
  build on reserved or deferred ontology entries," and "stop when your unit
  turns on governance text." I did not need to interpret Constitution,
  Ontology, or Engineering Constraints text to reach this finding — ADR-0009
  itself, an accepted ADR, already states the reservation in its own body.
  I am reporting what it says, not resolving it.
- Minor, disclosed side-note: ADR-0009's Context section quotes an
  "`AGENTS.md` guardrail" sentence naming "T1 derived-finding authority
  construction" explicitly by name. Current `AGENTS.md` no longer contains
  that literal enumerated sentence — only the generic "reserved or deferred
  ontology entries" phrase remains there, with the enumeration apparently
  now living in `docs/governance/README.md`'s backlog list instead. I note
  this as a small, verified documentation-drift fact, not a defect I am
  equipped to assess further.

**Did this change the answer or its boundary? Yes, and specifically:** it
tells me what a safe pre-filing explanation may and may not claim. It *may*
make negative/boundary statements ("nothing about this figure has legal
effect until you file") — that much is settled by the ordinary fact that
filing is a distinct, later act, and does not depend on resolving T1. It
*may not* make a positive doctrinal claim about what the pre-filing figure
legally or epistemically *is* in the interim — not "this is your official
determination," not "this is a mere preview with no standing," not any
characterization of what "instrument-authorship" amounts to before the
filing boundary — because the project's own accepted ADR says that account
is not yet built. My two-sentence answer in §2 was written to respect that:
it states the boundary (no legal effect until filing) without characterizing
what the number's standing is on the near side of that boundary beyond "it
reflects what you told the software." CB-A1's required result ("the trace
distinguishes tax meaning and computational support from the legal effect of
filing, without pretending the output has no tax-law association") is
achievable within committed doctrine; a *fuller* legal characterization of
the pre-filing state is not, and reaching for one would be improvising T1
doctrine. I record this as a decision question in §6 rather than adopting a
position.

---

## 5. Where my explanation terminates

- On authorship: I stop at ADR-0009's ratified framing (pins → publication
  act → adoption act → user; "the machinery is never the author of
  anything"). Beyond it lies the unresolved T1 question of what that
  authorship amounts to at the filing boundary — explicitly out of reach
  without a governance/ADR action, which is not mine to take.
- On the citations: I stop at what the two citation artifacts on this chain
  actually contain — an authority family, form id, and tax year, no quoted
  text. I cannot verify the underlying IRS instruction language from
  committed content alone (consistent with Track 0's Hop 6 finding, which I
  independently reproduced by opening both files rather than trusting the
  restatement). Whether the artifacts' *characterization* of what those
  instructions require is accurate is a question for public IRS sources
  directly, which is available (Track 0's Hop 8 already grounds the general
  reading of Form 1040 line 2b and Schedule B against public guidance) but
  which I did not re-verify line-by-line — that would be re-doing Track 0's
  Hop 8, not a new legal-epistemic finding.
- On filing's actual legal effect: I stop at "filing is a distinct later
  act with consequences this repository does not model or claim to model."
  What those consequences actually are under federal tax procedure (e.g.,
  what a jurat legally binds a filer to, how amendment interacts with an
  earlier unfiled figure) is outside this repository entirely and is not a
  question committed synthetic content or this codebase's governance can
  settle.

**Addressing Track 0's section-5 question to this lens directly:** does
distinguishing computational support from legal filing effect hold up under
this trace? — largely yes, at the level the fixture actually renders (no
component of the rendered row or its citation sites claims IRS sign-off, and
the governance doctrine behind the number's authorship is real and
citable). Does some hop create an unsupported inference of IRS blessing? —
not as currently rendered, but the bare citation pointers are a latent risk
if ever surfaced as inline "citations" without qualification (§3.3). Is
`closure_claim` language strong enough to mislead about completeness if
surfaced verbatim? — yes, concretely: its present-tense declarative phrasing
("Every interest amount reported in box 1... **is recorded** as a statement
item") asserts a completed fact rather than describing what a user's closure
declaration would mean, and it is not currently gated by any conditional
framing in the artifact text itself (§6.3). It is not currently rendered to
the user in this fixture's presentation path — that is the one piece of
found risk I can report as *latent rather than realized*.

---

## 6. Concrete actions the project could take

1. Change the "we found" / first-person-plural framing in any two-sentence
   or summary explanation of line 2b (and, on the same pattern, any other
   computed line) to voice that attributes the total to the user's own
   entered and closure-declared items, consistent with ADR-0009's
   authorship doctrine — a copy/content change, testable without touching
   the engine.
2. Add an explicit, short filing-effect statement near computed lines in
   a review screen ("nothing here has legal effect until you file and
   sign") — a UI-content experiment, independent of any composition or
   scope question.
3. Before any future surface renders a source-family `closure_claim` string
   verbatim (e.g. in a "why is this closed" or "what does closed mean"
   panel), rewrite the closure_claim text from present-tense declarative
   ("Every ... is recorded ...") to conditional/attributive voice ("If you
   declare this family closed, you are asserting that every ... has been
   recorded ..."). This is a content-authoring change to the family
   artifacts (e.g. `family.f1099int-b1.json`, `family.f1099int-b3.json`,
   `family.f1099int-b8.json`, `family.f1099oid-b1.json`, and by the same
   pattern the other source-family files), flagged now, before the string
   is ever surfaced, not after.
4. **Decision question for the owner/foreman, not mine to answer:** should
   the project record a lightweight, provisional statement of what a
   pre-filing published figure's standing is — sufficient to write a safe
   plain-language answer — or should every user-facing explanation of a
   computed figure be restricted to negative/boundary statements only
   ("no legal effect until filed") until T1 derived-finding authority is
   actually resolved? This sits directly on a named-open governance
   reservation (ADR-0009's "What T1 still reserves"; the backlog entry in
   `docs/governance/README.md`). I am recording the question and stopping,
   per the charter — I am not proposing an answer.
5. Audit disposition `explain` strings across the content package for
   reuse of kernel-reserved vocabulary in an ordinary-English sense —
   "attested" is the concrete instance found (`form1040.line-2b.form-field.v5.json`,
   `closure_backed_zero` disposition) — and either replace the word or
   confirm, in writing, that the collision is intentional and harmless.
6. Correct the speaker-role description of `finding:derived:*` input pins
   in any future written trace (including a revision of Track 0's own Hop 2
   prose, which is not mine to edit): they are computed, assertion-backed
   subtotals, not direct user closure declarations, even though the schema
   tags both with `origin: assertion`. A one-line clarification in whatever
   document next explains pin semantics would prevent the conflation I
   found in §4.

---

## 7. Threads I deliberately discarded

- **Whether the seven-family composition is the legally/practically correct
  universe of "taxable interest."** That is a tax-domain-coverage question
  (Lens B's case emphasis, not mine). My lens is about who is speaking and
  what a reader is entitled to believe, not about whether the declared
  universe is substantively complete. No distinct legal-epistemic action
  follows from pursuing it further than Track 0 already did.
- **How much of the provenance chain a downstream system can actually
  recover** (empty `pinLabels`, unresolved `finding:derived:*` ids). I
  confirmed the same underlying facts as a byproduct of opening the line-2b
  finding, but this is a system/provenance-recoverability question (Lens
  D's case emphasis), not a speaker-attribution or legal-effect question. I
  have no action to add beyond what that lens would already surface.
- **The Schedule D attachment row visible at the top of the same
  presentation model** (`disposition: blocked`, referencing "ADR-0057/0058"
  in its title). I saw this while opening the fixture's top-level
  structure but did not pursue it — it is a different form and a different
  line, off the line-2b chain the charter scopes me to, and any finding
  there would require writing about a second amount, which the charter does
  not authorize.
- **The ten `closure-mapping.*` package pins' own text.** I did not open
  these files. The four source-family `closure_claim` strings I did open
  already established a clear, repeatable pattern (declarative present-tense
  phrasing) sufficient to support the action in §6.3. Opening the remaining
  package files was unlikely to change that action, only add redundant
  confirmation of the same pattern, and the charter caps me to one
  consequential drill-down thread, which I spent on the authorship/T1
  question in §4 instead.

---

## Notes on evidence and process

- No engine run, `live_coordinate_run`, or artifact generation was
  performed. All claims above are read from already-committed synthetic
  content, accepted ADR text, and the current schema/governance-backlog
  files named inline.
- Every artifact-content claim above (citation files, source-family
  `closure_claim` text, the line-2b finding's pins, the `derived-finding.v2`
  schema, ADR-0009's text, and the `docs/governance/README.md` backlog
  entry) was opened and read directly during this session, not restated
  from the charter or from Track 0 without independent verification.
- This account is exploratory and non-authoritative. It creates no product
  contract, adopts no definition of `claim`, `integrity`, `complete`,
  `completeness`, `correctness`, or `fact`, and does not select or rank
  among its own proposed actions.
