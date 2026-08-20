# Track 3 — Curated Inquiry: "Why Is This Amount On My Return?"

Audience: Product, Shared. Written for a reader who has not seen Tracks 0–2 and
will not read them.

Status: **exploratory, non-authoritative.** This packet curates and reduces
already-committed material from Tracks 0–2 of the Claim Boundary Exploration
milestone. It creates no product contract, adopts no definition, and
reinterprets no accepted contract. *Claim boundary* and *explanation tree*
remain working lenses for this phase only. No engine run, artifact generation,
or fixture change was performed here; all claims below are read from
already-committed synthetic content, the four prior packets, and public tax
guidance already cited by those packets.

Sources this packet curates, if you want the underlying detail:
`docs/phases/claim-boundary-exploration/inquiries/track-0-inquiry-frame.md`,
`track-1-lens-a-casual-reader.md`, `track-1-lens-b-tax-practice.md`,
`track-1-lens-c-legal-epistemic.md`, `track-1-lens-d-system-provenance.md`,
`track-2-explanation-tree.md`. You do not need to read them; this packet
states what is now known.

**Repaired twice after owner-side advisor review.** An
owner-side advisor review found overclaims, one materially wrong finding, and
four missing pieces in this packet's earlier version. This revision corrects
them by annotation, in place, marked at each site as "corrected by Track 3
repair N." Nothing here was silently rewritten; where prior text was wrong,
this version says what was wrong and why. The most consequential correction
is repair 2: the earlier "the system knows exactly which document is
missing" finding was wrong — see §1's "strongest convergent finding" and
node N2 in `track-2-explanation-tree.md` for the corrected claim.

---

## 1. What was asked, and what was found

**The question:** a person finishing a simple tax return sees a row on their
Form 1040, "Taxable interest … $1825," and asks, in effect, *why is this
amount on my return?* — a question that actually compresses five different
questions: where did this number come from, is it correct, is it all of it,
does it affect what I owe, and what do I do now.

**The example:** one committed synthetic fixture — a mixed Schedule B
interest-and-adjustments presentation model, Form 1040 line 2b, value `1825`
— traced end to end against core package **v33**, the highest-numbered core
package present in the repository and the comparison target this inquiry
chose. **Corrected by the final repair:** no committed artifact formally
designates a current package, so v33 is not described here as the "current"
or "currently selected" package. The fixture itself was built against an
earlier package, v15. The supported claim is narrow: the line-2b chain is
unchanged between the fixture's adopted v15 and the v33 comparison target.

**The headline finding, corrected by Track 3 repair 1 (the original wording
overclaimed):** the number is *mechanically reconstructible* from committed
artifacts — every artifact that produced it (a computation rule, a
seven-family composition, source-family closures, citations, an attachment
rule) is committed, versioned, and readable, and the chain *reaches* citation
artifacts that name authority. Reaching a pointer to authority is not the same
as being traceable to authority — the citation artifacts on this chain are
bare pointers naming a source, not quoted rule text (established precisely in
§2's re-examined P3/A3 nodes and restated at repair 8 below). Neither claim
extends to "trustworthy," which asserts something about reliability this
inquiry never tested. But the *plain-language description* of that number, as
first drafted, does not accurately reflect what the artifacts support. Four
independent adversarial readers, working from different standpoints and
without seeing each other's work, converged repeatedly on the same handful of
specific defects in that plain-language layer — not in the underlying
computation. **What the evidence supports: the computation is mechanically
reconstructible from committed artifacts, and the chain reaches pointers to
tax authority — not the substance of a rule. The first sentence describing it
was not yet honest about who is speaking, what is included, and what happens
when something is missing.**

### The plain answer, and why it changed

The first drafted answer read:

> This $1825 is the total taxable interest we found from your 1099-INT,
> 1099-OID, and other interest sources for the year, after subtracting any
> nominee, accrued-interest, or bond-premium adjustments you told us about.
> It doesn't include tax-exempt interest (like from municipal bonds), and it
> only reflects the specific interest documents and adjustments you've
> confirmed as complete so far.

Every one of the four adversarial reviewers rewrote it, and not for the same
reason:

- **A casual, invested reader** (a non-expert who reads carefully) rewrote
  "we found" to "you entered" and "confirmed as complete so far" (which reads
  as a compliment — *you did it, it's done* — rather than as the rolling
  caveat it is meant to be) to an instruction: "check your list of accounts
  against what's here before you file."
- **A tax/financial practitioner** rewrote the first sentence to name the
  actual box- and entity-level boundary of what the software tracks (Form
  1099-INT boxes 1, 3, 10; 1099-OID boxes 1 and 5; a partnership K-1 box 5;
  interest with no form) and added an explicit disclosure that real
  categories the software does not yet model exist (estate/trust K-1
  interest, seller-financed mortgage interest, a savings-bond exclusion
  interaction) — because "we found ... from your 1099-INT, 1099-OID, and
  other interest sources" reads as a claim of complete domain coverage that
  the artifacts do not support.
- **A legal/epistemic reader** rewrote "we found" for the same reason as the
  casual reader, but grounded the correction in this project's own accepted
  authorship doctrine (ADR-0009: "the machinery is never the author of
  anything"; a derived finding's authority runs pins → publication act →
  adoption act → user), and added an explicit filing-effect boundary
  statement directly into the two-sentence answer itself: "nothing about
  this figure has legal effect until you file."
- **A system/provenance reader** kept the original wording closest to intact
  but added a clause claiming inspectability ("tap any part of this number to
  see which categories those are") — then found, on checking, that the
  artifact does not yet support that claim: the underlying pin data exists,
  but no rendering surface currently resolves those ids to a name a reader
  would recognize.

**These four rewrites are not a poll to be resolved into a winner.** They
disagree about what belongs in two sentences and where — and that
disagreement is itself evidence about what a real explanation interface needs
to be able to do (see §4). No single two-sentence answer was adopted by this
milestone, by owner direction, precisely to preserve that evidence.

### The strongest convergent finding

**Corrected by Track 3 repair 2.** The original wording of this finding
claimed the system "knows exactly which document is missing" and that the
message fails to say so. That is wrong in an important way, and the error was
repeated in the Foreman's own summaries of this milestone. It is corrected
here, and every downstream restatement of it in this packet and in
`track-2-explanation-tree.md` (annotated in place) and
`actionable-considerations.md` (register entry `SC-3`) has been rewritten to
match.

**What is actually true, verified directly against the committed rule
artifact `tax.us.2025.rule.form1040-line2b` v4 and the form-field artifact
`tax.us.2025.form1040.line-2b.form-field` v5:** the computation rule carries
ten distinct `require_closed` conditions in its `when` clause, one per
constituent *source family* (seven positive interest families plus the three
Schedule B adjustment families) — not seven, as an earlier restatement in
Track 2's node N2 said; that count is corrected in place there too. When one
of those `require_closed` conditions fails, the rule's `blocked.missing`
field can in principle identify which *source-family subtotal symbol* is
unmet. The form field's own `dispositions.blocked` then collapses all of that
back down to one generic sentence — *"Taxable interest is blocked because one
or more constituent interest families are unclosed or their dependencies are
missing"* — rendered identically across all four blocked codes
(`DEPENDENCY_ABSENT`, `DEPENDENCY_INVALID`, `CATEGORICAL_DOMAIN_MISMATCH`,
`SOURCE_SET_UNCLOSED`), confirmed by reading the artifact directly.

That is real, and it is worth having: specificity that exists upstream (which
source family is unclosed) is discarded downstream (one undifferentiated
sentence). But "which source family is unclosed" is **not the same claim** as
"which document is missing." A `require_closed` check tests whether the user
has declared a source family *closed* as of a horizon — an assertion the user
makes, not a fact about what paper the user holds. An unmet closure is
consistent with several different real situations: the user holds a document
in that family and has not yet entered it; the user holds no document in that
family and has not said so; or the user simply has not reached that step of
entry yet. The rule and the form field cannot distinguish these from each
other — nothing in the committed artifacts asserts which one applies. A
rendered message that said "you are missing your box-3 document" would
assert something the system does not know and the artifacts do not support.

The real, corrected finding: **the honest downstream message is about an
undeclared source family, not a missing document.** Independently, without
reading each other's work, three different reviewers (the casual reader, the
practitioner, and the provenance reader) and the original trace all
separately hit the same wall — the generic, undifferentiated blocked
sentence — and all four routes converge on the same underlying gap: the
family-level specificity that exists in the rule's `when` clause and
`blocked.missing` field never reaches the sentence a person would read. Four
independent routes to the identical finding, from readers with different jobs
and different things they were looking for, is the strongest single piece of
evidence this inquiry produced — the finding survives the correction; only
what it is a finding *about* changes.

---

## 2. The explanation tree, in its settled form

Rather than a single answer, the milestone's second track built a tree: one
root sentence, six branches organized around what a person is actually
asking, each traced to what currently supports it and where support runs out.

**Corrected by Track 3 repairs 2, 5, and 8** (matches the corrected tree in
`track-2-explanation-tree.md` §1; this compact reproduction was stale before
this repair):

```
ROOT  "$1825 — Taxable interest"
  ├─ P  Where did this come from?              (origin / provenance)
  │    P1 who supplied it · P2 how it was calculated ·
  │    P3 can I see the pieces · P4 is this current ·
  │    P5 why is this taxable interest under the applicable rules [new]
  ├─ S  Is this all of it?                      (scope)
  │    S1 which of my documents were used · S2 have I told you everything ·
  │    S3 does the product even have a place for every kind of interest ·
  │    S4 what does "closed" mean and not mean
  ├─ T  Does this matter for my taxes?
  │    T1 what does it feed into · T2 does something else have to be filed ·
  │    T3 where did the excluded interest go
  ├─ A  Who is telling me this, and what can I believe?
  │    A1 the software's finding, or my own entry summed back ·
  │    A2 did I swear this to the IRS · A3 do the citations mean IRS review
  ├─ R  Does this have any effect yet?
  │    R1 has anything legal happened (answerable) ·
  │    R2 workspace status now (answerable) · R3 rendering has no legal
  │    standing (answerable) · R4 legal effect enters at filing (answerable) ·
  │    R5 fuller instrument-authorship (deliberate terminus)
  └─ N  What do I do now?
       N1 nothing blocking — here's what to check ·
       N2 blocked — which *source family* is undeclared (not "which document")
```

Five distinctions recur across almost every branch, and every branch that
blurred them was independently caught by at least one reviewer: **document
completeness** (has the user entered every document they hold), **source-
family closure** (the user's own per-category "I've entered everything in
this bucket" declaration), **tax-coverage completeness** (whether the
*product* even has a slot for a given category of interest), **computation
readiness** (can this specific number publish right now), and **return/
action readiness** (may the user do some later thing, including file). A
sentence that says "is it complete" without saying which of these five it
means is where every misreading in this inquiry actually originates.

### One path, worked end to end (progressive disclosure)

This is the demonstration of how a person could descend from a plain sentence
to real technical detail without ever hitting internal vocabulary, walking
the "is this all of it?" branch (S3), because it is where the strongest
convergent evidence and the sharpest stopping point both sit.

**Depth 0 — shown by default, next to the number.**

**Corrected by Track 3 repair 4** (this defect exists in this packet's own
prior draft of the same worked path; corrected here and in
`track-2-explanation-tree.md`): the original sentence said "the interest
documents you entered," implying every dollar came with a document — not
true of the composition artifact, which includes a non-form interest family.

> This $1825 is the total taxable interest you entered — whether it came
> with a form like a 1099-INT or 1099-OID, or you reported it without one —
> minus any nominee, accrued-interest, or bond-premium adjustments. It
> doesn't include tax-exempt interest like municipal bond interest, which is
> reported on a different line of your return.

**Depth 1 — reached by an explicit "what's included" control, not implied by
depth 0 alone.**

> This covers interest from 1099-INT and 1099-OID forms, interest reported
> through a partnership Schedule K-1, and interest you told us about that
> didn't come with a form. If you have a kind of interest income that isn't
> one of those, it may not be included yet — see below.

**Depth 2 — reached by explicit further descent.**

> Specifically, this includes: Form 1099-INT boxes 1, 3, and 10; Form
> 1099-OID boxes 1 and 5; interest from a partnership Schedule K-1, box 5;
> and interest you reported without a form. It does not currently include
> interest reported through an estate or trust (a Form 1041 Schedule K-1),
> seller-financed mortgage interest someone paid you directly, or the
> interaction with the savings-bond interest exclusion (Form 8815).

**Terminus — stated, not silent.**

**Corrected by Track 3 repair 4:** the original terminus said "you (or your
preparer) would need to report them separately for now," implying an
available manual-entry, alternative-reporting, or filing route this
milestone never established exists, is supported, or is safe.

> If any of those missing categories apply to you, this product doesn't yet
> have a place for them. They won't show up on this line, and entering them
> elsewhere in this product will not cause them to be included here. This
> product does not currently tell you how or where to report them — that is
> outside what it does today.

A person can descend three layers without ever encountering "composition,"
"family," "closure," or "pin," and the exact box-level detail the
practitioner reviewer insisted must stay reachable survives intact at depth
2 — it is simply not the first thing shown. Each layer stays true to the one
above it, and the terminus does not pretend to enumerate every possible
category (it names three illustrative ones, explicitly not exhaustive), does
not pretend the gap doesn't exist, and does not imply a workaround the
product has not established.

### Where every branch actually terminates

Every branch of this tree hits a wall, and every wall is nameable rather than
silent:

- **P3** (can I see the pieces): no — the individual document-level dollar
  amounts behind the 1825 total are not committed as separate files anywhere
  in this fixture's directory. This is a genuine floor of what this fixture
  can show, not a copy-writing problem.
- **P4** (is this current): partially — the direct one-hop chain for line 2b
  is confirmed *unchanged* between the fixture's adopted v15 and the v33
  comparison target, but nothing in the rendered document tells a
  reader that two *other* rows on the very same page (`line-11`, `line-12`)
  are built from package members that have since been outright removed, not
  merely superseded. A reader who confirms one row is unchanged has no basis
  to infer the rest of the page is. Note that "current" is not a property any
  committed artifact confers on a package; see the correction in §1.
- **R2–R5, formerly one node** (what is this figure's standing right now,
  before filing): **corrected by Track 3 repair 5** — the former single R2
  node collapsed four things that come apart. Three are answerable now:
  **R2**, the current derived finding's workspace status (a computed,
  revocable, updatable `published_value` inside this system, right now);
  **R3**, the rendering's lack of legal standing (the drawn output is not a
  return and has no standing as one); and **R4**, the point at which acts
  acquire legal effect (filing — a distinct, later act; nothing has been
  filed, transmitted, or signed). Only **R5**, the fuller
  instrument-authorship question, is a genuine terminus: this project's own
  accepted governance (ADR-0009) names, explicitly, "what instrument-
  authorship amounts to at the filing boundary" as reserved, unbuilt
  doctrine. A positive characterization beyond R2, R3, and R4 would be
  improvising governance that does not yet exist. **The tree stops at R5 by
  design; R2 through R4 are not part of that stop.**
- **P5** (why is this amount treated as taxable interest under the
  applicable tax rules — **added by Track 3 repair 8**): the tree previously
  never asked this. It traced *that* the system classified the amount as
  taxable interest, never *why* that classification is right. Examined
  directly: both citation artifacts on this chain
  (`tax.us.2025.citation.form1040.line-2b`,
  `tax.us.2025.citation.schedule-b`) are bare authority pointers — an
  authority family, a form id, a tax year — with no quoted instruction text
  committed behind either. The honest terminus: the classification rests on
  the project's own content plus an unquoted reference to IRS authority, and
  the user-facing explanation stops there. This is the evidence behind
  repair 1's narrower claim about what "reaches authority" means.
- **S3** (does the product cover every real category): no, and it does not
  currently say so anywhere a user would see. At least three real,
  non-exotic categories (estate/trust K-1 interest, seller-financed mortgage
  interest, the savings-bond exclusion interaction) are absent from the
  product with no disclosed boundary.

### Disagreements preserved, not resolved

These are findings, not indecision, and this inquiry does not flatten them
into a single recommendation:

1. **Where the filing-effect boundary belongs.** One reviewer's rewrite puts
   "nothing about this figure has legal effect until you file" *inside* the
   two-sentence root answer. The other three reviewers' rewrites, and the
   original draft, do not surface it at that depth at all. This may not be a
   wording dispute with a single right answer — it may depend on context a
   general tree cannot settle (a review-and-sign screen, where the
   legal-effect reminder is urgent, versus an in-progress entry screen,
   where it is premature). Not resolved; carried into the register (see
   `OV`-adjacent entry `SC-11` below).
2. **How much detail belongs in the first sentence.** One reviewer
   deliberately kept the root answer at the form-name level and pushed
   exactness to an instruction one layer down. Another reviewer rewrote the
   *same* sentence to name boxes and entities explicitly. Both are
   defensible answers to the identical question for different readers; the
   milestone treats this as evidence that box-level detail belongs one layer
   beneath the root, not as a contradiction to resolve.
3. **How to signal that document-completeness might still be missing.** One
   reviewer's fix is behavioral (an instruction: "check your list before you
   file"); another's is navigational (an affordance: "tap to see which
   categories") — and the navigational fix, on inspection, is not yet
   something the artifact can actually back up. Both are legitimate
   directions; which one is right depends on whether a future surface can
   actually deliver the inspectability the second reviewer assumed.

### One correction to the trace itself

One reviewer, checking the original trace's own language, found it slightly
imprecise: the trace described all fourteen "assertion"-origin pins behind
the number as "the user's own closure declarations." That is true for the
seven direct closure-declaration pins, but not for the ten computed-subtotal
pins that trace back to a closure only transitively — those are the system's
arithmetic over document entries, not literal statements the user typed. Both
kinds of pins share the same technical tag, but they are not the same kind of
speaker. This is recorded because it is exactly the kind of collapse this
inquiry exists to catch, including in its own prose.

### Routing example: one compressed question, six investigations [added by Track 3 repair 7]

A person asks a single, short, entirely ordinary question: **"Is this
correct?"** — pointing at the $1825. That one sentence compresses at least
six different investigations, each with a different owner and a different
answer, and a system that answers only one of them has answered the wrong
question for anyone who meant a different one:

1. **Arithmetic** — did the subtraction run correctly? Answer: yes, verified
   against the committed rule (`rule.form1040-line2b` v4) and composition
   (`interest-composition` v4); the gross-minus-adjustments arithmetic is
   correct *given its inputs*, though not visibly reconciled in the rendered
   output (P2). Owner: the computation rule.
2. **Inputs** — are the numbers that went into the arithmetic themselves
   right? Answer: unknowable from committed content alone; the system can
   show which subtotals it summed (S1) but not verify a subtotal against the
   taxpayer's actual paper. Owner: the user, at data entry.
3. **Document completeness** — has the user entered everything they hold?
   Answer: unknowable; this is exactly what a source-family closure asserts
   (S2, S4), and a closure is a user declaration, not a system verification.
   Owner: the user's own closure declarations.
4. **Product coverage** — does this product even model every category of
   taxable interest that could apply? Answer: no — at least three real
   categories (estate/trust K-1 interest, seller-financed mortgage interest,
   the savings-bond exclusion interaction) are absent with no disclosed
   boundary (S3). Owner: the product's own modeled universe.
5. **Tax characterization** — is this amount correctly classified as taxable
   interest under the applicable tax rules, as opposed to correctly summed?
   Answer: the classification rests on the project's own content plus an
   unquoted pointer to IRS authority (P5, added by repair 8); nothing on this
   chain quotes or tests the underlying rule text. Owner: tax-content
   correctness, partly outside this milestone's evidence ceiling.
6. **Currency** — is what's shown built from the rules currently in effect,
   or something stale? Answer: partially — the line-2b chain itself is
   confirmed unchanged from v15 through the v33 comparison target, but
   nothing tells a reader whether the *page* it's rendered on is (P4), and no
   committed artifact declares any package "current" at all. Owner:
   package/version tracking.

**The point:** "Is this correct?" has no single answer because it is not one
question. A system that replies to it with one sentence necessarily picks
which of these six it is actually answering — usually #1 (arithmetic),
because that is the easiest to verify from committed content — while the
person asking may have meant #3, #4, or #5. This is one worked example, not
a general routing scheme; it is not claimed that every compressed question
fans out into exactly these six, or that these six are exhaustive for a
different question.

### Exit-criterion 3 matrix [built by Track 3 repair 6]

Exit criterion 3 asks that every material invited belief or action have an
identified **speaker, basis, scope, invalidator, and unsupported neighboring
inference**. This matrix builds that five-tuple explicitly, adding a sixth
field the charter also asked for: **available deeper path**. It did not
previously exist as a single artifact; the pieces were distributed across
Track 0, the four lens accounts, and Track 2's tree (§5's prior grading of
criterion 3 said as much). **Chosen unit: the tree's leaf nodes** (P1–P5,
S1–S4, T1–T3, A1–A3, R1–R5, N1–N2, per §2's now-corrected tree), rather than
an unbounded list of material propositions, because the tree already
partitions the material claims into the smallest units this milestone
independently validated, and each node maps to exactly one row below. Where a
field cannot be filled from the evidence this milestone produced, the row
says so plainly rather than guessing — an honest hole is worth more than a
plausible fill, per the charter.

| Node | Speaker | Basis | Scope | Invalidator | Unsupported neighboring inference | Available deeper path |
| --- | --- | --- | --- | --- | --- | --- |
| P1 — who supplied it | The user, via `origin: assertion` pins the system aggregates (not the system itself, per ADR-0009) | Pins tagged `origin: assertion` on the line-2b finding (Track 0 Hop 2); ADR-0009's authorship doctrine | Covers only the assertion-origin pins on this one finding; says nothing about whether the assertions are themselves accurate | A pin introduced by a future rule/composition change that is not assertion-origin (e.g. a synthesized default) would break the "you entered it" framing for that portion | A reader could infer the software independently found or verified the interest income, rather than aggregating what was declared | P3 (thin), P2 |
| P2 — how calculated | The computation rule and composition artifacts | `rule.form1040-line2b` v4 (subtract op) and `interest-composition` v4 (seven families), confirmed identical v15/v33 | Covers the arithmetic operation only; not whether inputs are individually correct | A mismatch between the rendered net figure and an independently recomputed gross-minus-adjustments figure — untestable today because the gross subtotal is never rendered | A reader may assume the net figure is visibly reconciled against a gross total; it is asserted, not shown | None further in committed content; SC-5 (unadopted) would add it |
| P3 — can I see the pieces | The finding's `pins` array vs. the presentation row's `citationSites` (disjoint sets by design) | 39 pins vs. 5 `citationSites`, confirmed reading `presentation_projection.py`; `pinLabels` empty | Names ids only; no id resolves to a human-readable label in this fixture | Not applicable — this is a floor, not a claim that could later be shown false | A reader could assume "citation" ids are drillable evidence, or that all 39 pins are inspectable when 34 are not exposed as citation sites | **Nowhere deeper — stated explicitly, a genuine floor of the committed fixture** |
| P4 — is this current | No artifact states this; a reader must diff package files by hand | Line-2b chain confirmed identical between the fixture's adopted v15 and the v33 comparison target (Track 0); `line-11`/`line-12` built from now-removed v15 members (Lens D §4) | Applies per-row, not per-page, and only across the two package versions actually compared; confirming one row says nothing about another | A future package change to the line-2b chain's own artifacts without a fixture refresh would invalidate the "unchanged" claim for that row | A reader who confirms line-2b is unchanged may infer the whole page is, or may infer that some package has been formally designated current — neither follows | None — no committed field declares a "current package" at all (SC-4, unadopted) |
| P5 — why is this taxable interest under the applicable rules [new, repair 8] | The citation artifacts, naming (not quoting) an IRS authority family; ultimately the project's own content | `citation.form1040.line-2b` v1, `citation.schedule-b` v1 — bare pointers, confirmed by reading both files | Names the authority family and form only; no quoted instruction text; does not itself justify the classification | Not applicable as a floor — would only change if quoted authority text were committed behind these ids | Rendering these pointers as inline "citations" could imply IRS review or endorsement (A3's latent risk) | **Nowhere deeper within this milestone's evidence ceiling — stated explicitly** |
| S1 — which documents were used | The composition + this fixture's own data | Four of seven families directly traceable (Track 0 Hop 5); three others present only as pin references | Covers what is separable from committed data in this one fixture only, not a general claim | Not applicable to this specific fixture as committed | A reader could assume every family's individual contribution is visible; three of seven are not | None — the three non-separable families' individual contributions are not committed anywhere in this fixture's directory |
| S2 — have I told you everything | The user, via per-family closure declarations | The closure mechanism exists; each family's own `closure_claim` text is precise and self-limiting | Covers only what a family's closure asserts, not real-world document completeness the system could verify | A stale or withdrawn closure moves the dependent disposition to `blocked` — implicit in the mechanism, not systematically stated per node before this matrix | "Confirmed as complete so far" reads as praise/certainty, not the revocable declaration it is (tension #2) | S4; the family's own `closure_claim` text |
| S3 — does the product cover every category | The composition's own `required_universe.claim` field, stating what it covers, not what it omits | Lens B verified the composition is a defensible subset missing estate/trust K-1, seller-financed mortgage, and Form 8815 interaction — no modeled family, slot, or disclosed non-goal for any of the three | Covers the v33 package's modeled universe only, not the domain-complete universe under U.S. tax law | Adding a modeled family/slot for any of the three named categories would close that specific gap; otherwise stable until the package changes | The dollar total invites belief in a closed inventory rather than a boundaried composition (Lens A) | The worked S3 progressive-disclosure path (§2), terminating honestly at the three-category floor |
| S4 — what "closed" means | Each source family's own `closure_claim` text (not currently rendered to a user) | E.g. the box-3 family's `closure_claim`, precise and self-limiting, confirmed by reading the artifact | Covers exactly one family per closure; explicitly disclaims coverage of other boxes or total taxable interest | Present-tense declarative phrasing ("is recorded") could read as an already-completed fact rather than a conditional declaration (Lens C) — closed by rewriting to conditional voice, not adopted here (`SC-12`) | "Attested" collides with the kernel's reserved `basis: attested` vocabulary (ADR-0009), a terminology-hygiene risk if reused (`SC-8`) | None currently rendered — the text is not surfaced anywhere in the rendering path |
| T1 — what does this feed into | No speaker — **under-supported; no lens developed this** | The general fact that line 2b feeds AGI is established (Track 0 Hop 6–8); how far the consequence propagates is not traced | Cannot be stated beyond "feeds AGI" | **Cannot be filled from present evidence** | A reader may assume the full downstream tax consequence (credits, phase-outs) has been traced; it has not | **Cannot be filled from present evidence — an honest hole, not a resolved node** |
| T2 — does something else have to be filed | The attachment rule (`rule.attachment.schedule-b` v4), a system-authored artifact | Verified directly against the artifact and the runner: **either** `interest.positive-total` **or** `dividends.ordinary-total`, tested independently (not summed), strictly greater than a threshold parameter. The foreign-account and foreign-trust questions are `completeness.required_answers` applying after attachment, not triggers | Covers only the dollar-threshold trigger — one of the eight independent IRS triggers; the other seven categorical triggers are not implemented (repair 3) | **Confirmed invalidated as a completeness claim by repair 3** — IRS Instructions for Schedule B 2025 name categorical triggers the committed rule does not test | A reader could assume the $1,500 threshold is the whole rule; it is not | The committed rule artifact itself; beyond it lies the confirmed content gap (repair 3 / `OV-1`) |
| T3 — where did excluded interest go | The composition artifact (excludes box 8 explicitly) | Composition explicitly excludes Form 1099-INT box 8 (Track 0 Hop 5b) | Covers only the exclusion itself; the draft answer states what is excluded, not where it lands | Not applicable as a floor; would be invalidated only if a future draft claimed a specific line-2a placement without verifying it | A muni-bond holder could worry the amount "fell out of the return entirely" (Lens A) | Naming line 2a explicitly — identified, not yet adopted as content |
| A1 — software's finding or my own entry | Same artifacts as P1, reader's stake framed as reliance rather than provenance | Same as P1 | Same as P1 | Same as P1 | The "we found" framing invites a reliance misattribution distinct from, though related to, P1's provenance misattribution | Same as P1 |
| A2 — did I swear this to the IRS | A workspace closure declaration (revocable, pre-filing) vs. the Form 1040 jurat (a distinct legal act) | The mechanical distinction is real, grounded in how closures work (Lens C §3.2) | Covers the conceptual distinction only; nothing in the rendered row or citation sites states it to a user | Would be closed by surfacing the distinction explicitly in rendered copy; not currently done | "Confirmed as complete" could read as carrying jurat-level legal weight before filing has occurred | None currently rendered |
| A3 — do citations mean IRS review | The two citation artifacts (bare pointers) | Confirmed directly by reading both files — no quoted instruction text behind either | As currently rendered, a latent risk, not realized — the fixture does not present these as inline citations | Becomes realized the moment a future surface renders these pointers as inline citations next to a dollar amount | A reader could infer IRS endorsement/review that no artifact on the chain asserts or could assert | Same terminus as P5 — the citations are pointers, not substance |
| R1 — has anything legal happened | Ordinary fact (filing is a distinct, later act) plus the workspace state | Nothing has been filed, transmitted, or signed (Lens C §4) | Answerable as a negative/boundary statement only | Invalidated the moment filing occurs — outside this milestone's evidence ceiling | None identified — comparatively low risk | R2–R4 for the affirmative pre-filing state |
| R2 — current derived finding's workspace status [split, repair 5] | The engine, describing its own internal disposition state | Form-field disposition `published_value`, confirmed by reading the artifact | An internal-workspace fact only; carries no claim about legal standing | Any subsequent input change that flips the disposition (e.g. a closure withdrawal) invalidates this characterization for that value | A reader could conflate "published inside the workspace" with "filed" — R3/R4 exist to block that inference | R3, R4, R5 |
| R3 — rendering's lack of legal standing [split, repair 5] | Ordinary fact about what a rendering is | No artifact asserts a rendering is a return; a governance-consistent default, not drawn from a specific citation | Applies to any rendered output in this system, not line-2b-specific | Would only change with a future governance decision granting some rendering formal standing, which does not exist | A polished, form-labeled rendering could look official enough to be mistaken for a filed return | R4, R5 |
| R4 — legal effect entering at filing [split, repair 5] | Ordinary fact plus governance framing | Filing is a distinct act (Lens C §4); ADR-0009's pins → publication act → adoption act → user chain implies further acts before legal effect attaches | Names the boundary point only; does not characterize what crossing it produces | Not applicable — a boundary statement, not a falsifiable content claim | A reader might assume "filing" and "adoption act" are the same event, when ADR-0009 leaves that mapping to R5 | R5 (terminus) |
| R5 — fuller instrument-authorship question [split, repair 5] | No speaker — explicitly reserved, unbuilt doctrine | ADR-0009's own "What T1 still reserves" section | **Cannot be stated — that is the point of the reservation** | **Cannot be filled from current evidence; would require a future ADR** | Any positive characterization of pre-filing standing beyond R2–R4 would be improvising governance that doesn't exist | **None — the tree's one deliberate governance terminus** |
| N1 — nothing blocking | The disposition's own `published_value`/`computed_zero` state, reframed by Lens A as an instruction | Connects to S1/S2 for which documents are reflected | Covers the concrete instruction ("check your list") only; does not itself certify completeness | A document the user holds but never entered would invalidate reliance on "nothing blocking" as a completeness signal | "Nothing blocking" could be misread as "everything is accounted for," when it only means required inputs are present | S1/S2/S4 |
| N2 — blocked / undeclared family [corrected, repair 2] | The rule's `require_closed` conditions (data layer); the form field's generic `explain` string (rendered layer) | Verified directly: ten `require_closed` conditions, one generic explain string across four codes | Identifies which source-family closure is unmet, not which document is missing (repair 2) | Would be closed by a family-specific rendering of the explain text — not yet done (`SC-3`) | A rendered message naming a specific document would assert something the system does not know | None currently rendered; `SC-3` names the plausible fix |

**Weakest field, as the charter anticipated:** invalidator. Six of twenty-two
rows (P3, P5, S1, R3, R4, R5) have no meaningful invalidator because they are
floors or boundary statements, not falsifiable content claims — recorded as
such rather than forced into a fill. Two rows (T1, R5) cannot be filled at
all from present evidence, and both are named as honest holes rather than
guessed at.

---

## 3. What generalized, what did not, and what went untested

One worked example cannot prove any of this generalizes. What follows states
the basis for each claim; items marked conjecture are conjecture.

### Generalizes beyond line 2b

- **The five distinctions (document completeness, source-family closure,
  tax-coverage completeness, computation readiness, action readiness).**
  Established, not conjecture, for this line: every branch of the tree that
  risked collapsing two of these was independently caught by at least one
  adversarial reader. The basis for believing this generalizes is structural,
  not example-specific — any line built from source-family closures and a
  declared composition (which is most of this product's computed-line
  architecture) has the same five distinctions available to collapse.
  **Conjecture beyond that:** whether the same five distinctions are
  sufficient, or whether a differently-shaped line (see below) surfaces a
  sixth.
- **The voice/authorship defect ("we found" misattributing agency).** This is
  grounded in ADR-0009, an accepted, project-wide authorship doctrine, not in
  anything specific to interest income. Any user-facing text summarizing a
  derived finding is exposed to the identical risk. **Established as a
  general risk; not yet tested against a second line's actual draft copy.**
- **The convergence pattern itself, as a signal.** Four independently
  standpointed readers reaching the identical finding (the blocked-state
  message) is strong evidence *for that specific finding*. Whether running
  four independent lenses is generally worth its cost for future inquiries is
  **conjecture** — this milestone ran it once and found real value, but has
  not compared it against a cheaper method.
- **The "honest terminus" design discipline** (say where the explanation
  stops, rather than silently declining to raise the question) is a general
  principle with no line-2b-specific content in it. **Conjecture** that it
  is sufficient on its own without a broader evaluation instrument.

### Specific to line 2b

- The seven-family composition, the three subtractive adjustment classes, the
  Schedule B attachment threshold, and the specific box numbers all exist
  because this particular line has this particular shape (positive families
  minus adjustments, with an attachment side-effect). A line with a simpler
  shape would not exercise S3, T2, or the gross/net reconciliation gap (P2)
  at all.
- The specific staleness example (retired `line-11`/`line-12` package
  members visible on the same rendered page) is a real instance of a general
  risk (row-level currency is not page-level currency), but the *particular*
  removed members are an artifact of this fixture's history, not something
  that recurs identically elsewhere.
- The Schedule B independent-attachment-trigger gap, **resolved by Track 3
  repair 3 (see `OV-1`, discussed below)** — it is no longer an open
  verification question, it is a confirmed tax-content correctness gap — is
  specific to Schedule B's actual "who must file" rule and does not
  generalize to lines without an attachment side-effect.

### Could not be tested here

- **A line with no adjustments.** This example's richness (seven positive
  families, three adjustments, an attachment rule, a tax-exempt neighbor) is
  exactly why S3, T2, and P2 exist as branches; a line without that shape
  would not exercise them, and the tree's remaining branches (P1, P3, P5,
  A1–A3, R1–R5, N1–N2 — the R and P node counts corrected per repairs 5 and
  8) have not been checked against a simpler line to see whether they still
  apply cleanly or whether some of the tree's structure was itself an
  artifact of this line's complexity.
- **A line the user enters directly**, rather than one the system derives
  from closures and a rule. The authorship question (P1/A1) is answered here
  by pointing at pins and an adoption chain; a directly entered value has a
  different, probably simpler, provenance story this inquiry did not trace.
- **A line whose value depends on another form's output** (a downstream
  consumer of a prior computed value, rather than a source-family
  aggregation). T1 ("what does this number feed into?") was explicitly named
  as under-supported by every reviewer for exactly this reason — no lens
  drilled into how far the line-2b consequence actually propagates.
- **A real multi-user or amended-return situation.** Everything here concerns
  a single synthetic filer's single-horizon closures. Whether the closure/
  horizon concept holds up the same way when a return is reopened for
  amendment, or when more than one person's entries are involved, was
  explicitly noticed and explicitly declined by more than one reviewer as
  outside their assignment.
- **Whether a real, non-simulated reader actually reads any of this the way
  the adversarial accounts predict.** Every reviewer's account is a strong
  model agent's simulation, not user research. More than one reviewer
  explicitly names this as the next check before spending further effort on
  their own proposed wording fix.
- **The pre-filing legal-standing question itself (R2).** Not a gap in this
  inquiry's method — a deliberate, governance-grounded stop. This project's
  own accepted doctrine has not yet decided what a pre-filing figure's
  standing is, so no inquiry using only this evidence ceiling could test it
  further.

---

## 4. Consolidated register

This section explains what changed in `actionable-considerations.md` and why.
The full, current register is in that file, not duplicated here.

### Admission rule applied

The register's five-part consolidation rule (merge, split, remove, preserve
disagreement, promote nothing automatically) was applied to every current
entry — `CQ-1`–`CQ-5`, `SC-1`–`SC-10`, `GR-1`, `AR-1`, `GD-1`, `OV-1` — plus
one new candidate this track identified.

### Merges

- **`SC-4` and `SC-7` merged into a revised `SC-4`.** Both entries asked the
  same underlying product question — can a reader tell what package version
  produced or backs a given rendered number — from two angles that had been
  written as if they were different questions: `SC-4` asked whether a
  rendered row should surface its adopted-package identity; `SC-7` asked
  whether a row should carry a per-row currency signal and whether "current
  selected package" is formally defined anywhere. On inspection these are one
  product question with two plausible actions, not two questions. Merged;
  both actions are retained inside the merged entry. `SC-7`'s number is
  retired rather than reused.

### Splits

- **`SC-9` split into a revised `SC-9` and a new `SC-12`.** The original
  entry bundled two actions that need different evidence and different
  owners: rewriting a *draft, unshipped* plain-answer's voice (a pure
  copy-drafting decision, no committed artifact touched) and rewriting the
  *already-committed* `closure_claim` text inside multiple source-family
  content files (a content-authoring change to existing package artifacts,
  with versioning and package-maintainer implications). This is exactly the
  charter's own example of what must split: "what the interface should say"
  versus "whether the underlying content supports saying it." `SC-9` now
  covers only the copy-voice question; `SC-12` covers the family-artifact
  rewrite, cross-referenced to `SC-9`.

### New entry

- **`SC-11` added: where the filing-effect boundary belongs in a rendered
  answer.** This is disagreement 1 in §2 above — one reviewer's rewrite
  states the filing-effect boundary inside the root two-sentence answer;
  three do not. It meets the admission rule (a concrete question, plus a
  plausible action: test both placements against different screen contexts
  before committing to one) and the register's own rule to preserve
  unresolved disagreement when a later decision could turn on it. Recorded
  as open, not resolved, consistent with how the milestone treated it.

### Checked for a hinted merge and found none

The charter flagged "blocked-message" entries as a likely merge candidate,
alongside voice/authorship and adopted-package. On inspection, there is only
one register entry about the blocked-state message (`SC-3`) — the four-way
convergence on this finding lives across the source packets (Track 0, three
lenses), not as parallel register rows. No merge was made; `SC-3`'s evidence
citation was strengthened instead to note the convergence, since a single
entry backed by four independent findings is stronger evidence than one, and
that strength should be visible to whoever next reads the register.

### Status updates (not merge/split/remove, but a live rule applied)

- **`CQ-1`** ("Why is this amount on my return?") marked **closed —
  executed by this milestone**. Its plausible action (prototype a plain
  answer and decompression path; identify gaps; build adversarial tests) has
  been carried out in full by Tracks 0–2. It is retained, not removed,
  because it is the record of what this milestone was; its status is updated
  so it no longer reads as an open candidate.
- **`AR-1`** (an ongoing model-agent adversarial program) — its stated
  trigger ("after the opening inquiry defines a concrete object and
  evaluation question") is now **met**. This is recorded as a live decision
  available to the owner, not as a decision made here: whether to
  institutionalize the four-lens pattern this milestone used once.
- **`GD-1`** (a governance reader's companion) — its trigger ("after inquiry
  work clarifies the project's user-facing story") is **partially met**: the
  explanation tree in §2 above is exactly this kind of clarifying artifact,
  but only for one narrow slice (one computed line), not the project's
  broader story. Left as a candidate, not triggered.
- **`SC-1`, `SC-2`, `SC-3`, `SC-6`** — retained unchanged in substance;
  annotated with pointers to the concrete evidence this milestone produced,
  so a future reader does not have to re-derive the connection between the
  general risk these entries name and the specific findings that instantiate
  it. `SC-2` in particular: its "mistaken speakers" probe category is now
  concretely represented by `SC-9`; the rest of `SC-2`'s scope (omitted
  qualifiers, stale bases, unsupported actions, broader UI implications)
  remains open and untested.

### Removals

**None.** Every current entry, after this review, still names at least one
plausible action a later decision could act on. Nothing was found whose only
remaining value is general intellectual interest. This is recorded explicitly
because a silent absence of removals could otherwise look like the rule was
skipped rather than applied and found not to trigger.

### Status re-updates [Track 3 repair 9 — revisits five flagged entries]

- **`OV-1`** — reclassified from open verification to **confirmed tax-content
  correctness gap**, per repair 3. See the dedicated section below.
- **`SC-3`** — **restated.** The entry's own question column already asked
  the correct thing ("name the specific missing family instead of a generic
  message"), but its evidence column said "a user cannot tell which document
  type to go confirm" — this conflated family-level specificity with
  document-level specificity, exactly the error repair 2 corrects. Reworded
  in `actionable-considerations.md`: the entry is about a discarded, named
  *source family*, not a named document.
- **`GD-1`** — reassessed, status **unchanged (partially met, not
  triggered)**. This repair charter itself is, if anything, evidence *for*
  `GD-1`'s premise rather than against it: this milestone's own governance-
  adjacent output (the plain-language tree) needed a dedicated repair pass
  to correct overclaims and an outright factual error before it was safe to
  stand as the milestone's record — exactly the kind of clarity gap `GD-1`
  proposes a reader's companion would help catch earlier. Left as a
  candidate, not triggered, because this remains true for one narrow slice
  only, not the project's broader governance story.
- **`SC-4`** — reassessed. The merge that absorbed the former `SC-7` is
  checked against the artifacts this repair pass verified independently (the
  citation and rule artifacts read for repairs 2, 3, and 8) and found
  **accurate**: no committed artifact declares a formally "current" package
  version, and the `line-11`/`line-12` staleness example remains as
  described. No change made to the entry beyond what the prior Track 3
  already recorded.
- **`CQ-1`** — reassessed. **Remains closed — executed by this milestone**,
  with a caveat added: this repair charter corrected two significant
  overclaims within that execution (the mechanism-trustworthiness framing,
  repair 1; the blocked-state finding, repair 2) and confirmed one new
  content gap (`OV-1`, repair 3). Closure records that CQ-1's specified
  action — prototype a plain answer and decompression path; identify gaps;
  build adversarial tests — was carried out, including, now, its own
  correction. It does not mean the execution was free of error; the
  milestone's own practice of correcting itself in the open (this is the
  third such correction in its history) is part of what "executed" means
  here, not a reason to reopen the entry.

### `OV-1` — resolved: confirmed tax-content correctness gap [repair 3]

`OV-1` is **no longer open.** The Foreman retrieved the official IRS
*Instructions for Schedule B (Form 1040)*, tax year 2025, "Who Must File."
A taxpayer must file Schedule B if **any** of the following applies:

1. Over $1,500 of taxable interest or ordinary dividends.
2. Interest from a seller-financed mortgage where the buyer used the
   property as a personal residence.
3. Accrued interest from a bond.
4. Reporting OID less than the amount shown on Form 1099-OID.
5. Reporting interest income less than the amount shown on a Form 1099 due
   to amortizable bond premium.
6. Claiming the exclusion of interest from series EE or I U.S. savings bonds
   issued after 1989.
7. Interest or ordinary dividends received as a nominee.
8. A financial interest in or signature authority over a foreign financial
   account, or a distribution from / grantor of / transferor to a foreign
   trust.

Source: `https://www.irs.gov/instructions/i1040sb` (2025).

Lens B's suspicion was correct. Verified directly against the committed
`tax.us.2025.rule.attachment.schedule-b` v4 artifact and against the runner
that evaluates it (`packages/derivation/runner.py`).

**Corrected by the final repair — the earlier wording of this paragraph
described the rule inaccurately.** The `requirement` block names two
subtotals, `interest.positive-total` and `dividends.ordinary-total`, and one
threshold parameter, `parameter.schedule-b-threshold`. The runner tests each
subtotal **independently** against the threshold and requires the schedule if
**either** one is strictly greater. It does **not** add the two subtotals
together. Separately, the foreign-account and foreign-trust questions live in
`completeness.required_answers`: they are completeness requirements that
apply *after* Schedule B has attached, and they are **not** attachment
triggers in the committed rule.

**The gap, stated accurately.** The IRS instructions give **eight independent
triggers**, any one of which requires Schedule B. The committed rule
implements exactly **one** of them — condition 1, the dollar threshold — and
omits the other **seven categorical triggers**. Conditions 2
through 8 above are **categorical triggers with no dollar threshold**. Three
of them — accrued interest, ABP adjustment, and nominee — correspond to
adjustment classes this product already models by name
(`tax.us.2025.scheduleb.adjustment.accrued-interest`,
`.abp-adjustment`, `.nominee`) and already renders on the very fixture this
milestone examined. A synthetic filer with a $40 nominee adjustment and $200
of interest must file Schedule B under the actual IRS rule; the committed
rule as written would not require it.

**Recorded as a confirmed tax-content correctness gap, kept distinct from
explanation-design work.** This is not fixed here: no rule change is
proposed, no replacement content is drafted, and no content artifact is
touched, per the charter's explicit instruction. Its scope: the gap affects
whether Schedule B attaches for at least three real, non-exotic
categories of filer already representable in this product's own data model;
it does not affect the line-2b computation itself (line 2b's own arithmetic
is unaffected by whether Schedule B attaches). Remediation — whether and how
to extend `rule.attachment.schedule-b`'s `requirement` block — is an owner
decision, not made here.

---

## 5. Exit-criteria assessment [regraded by Track 3 repair 10]

Graded strictly against the milestone plan's eight criteria
(`docs/phases/claim-boundary-exploration/milestones/plain-question-claim-boundary-prototype.md#Exit criteria`),
against the **repaired** state, not the previous grading. Per the charter:
some criteria that passed before may now fail, and a repair that improves
the record while lowering a grade is a success, not a failure. Checked here
against every one of the ten repairs; the actual outcome is a net
*improvement* on one criterion (3) and no new failures — that is reported
plainly rather than reshaped to look more dramatic than it is.

1. **The selected positive and boundary states have end-to-end curated
   inquiry traces.** — **Met, unchanged.** Track 0 traces both CB-P1 (the
   fixture as committed, hops 0–8) and CB-N1 (the paper mutation removing
   one closure) end to end, with every material artifact version-checked
   against the v33 comparison target. None of the ten repairs touch
   Track 0 (outside this track's assigned paths); this grading does not
   re-verify Track 0's own prose beyond what repairs 2 and 8 independently
   confirmed against the underlying artifacts (see the handoff's "checked
   and found accurate" notes).

2. **A casual-reader answer exists at two sentences or fewer, with optional
   deeper layers that remain connected to actual support.** — **Met, with
   the same qualification as before, now strengthened.** Multiple
   two-sentence answers exist (the original draft plus four independent
   rewrites), all traceable to committed support. Repair 4 corrected the
   worked depth-0 sentence and terminus in §2's progressive-disclosure path
   to be *more* accurately connected to actual support (no longer implying
   every dollar came with a document, no longer implying an unestablished
   workaround). The milestone deliberately did not converge on one
   canonical text — an owner re-aim, not a shortfall — so "an answer
   exists" remains true in the plural, not the singular.

3. **Every material invited belief or action has an identified speaker,
   basis, scope, invalidator, and unsupported neighboring inference.** —
   **Partially met. Corrected by the final repair — the previous "Met"
   grade was too generous.** Repair 6 built the matrix
   that did not previously exist: every leaf node of the corrected tree
   (P1–P5, S1–S4, T1–T3, A1–A3, R1–R5, N1–N2) now has an explicit six-field
   row (the charter's five fields plus "available deeper path") in a single
   artifact, rather than requiring a reader to reconstruct it from three
   separate packets. Two fields (T1's invalidator and available-deeper-path,
   R5's basis-adjacent fields) are explicitly marked as honest holes rather
   than filled with a plausible guess, consistent with the charter's
   instruction that an honest hole outweighs a plausible fill.

   **Why this is partial and not met.** Two reasons, both structural rather
   than cosmetic. First, the matrix contains fields that are explicitly
   unfillable from present evidence; a criterion demanding that *every*
   material belief have an identified basis, scope, and invalidator is not
   satisfied by a table that honestly marks some of those cells empty. The
   honest hole is the right disclosure and still a hole. Second, the
   criterion as written refers to the beliefs invited by "that answer" —
   singular — and the owner re-aimed this milestone away from selecting any
   canonical answer. The matrix therefore grades a structure the criterion
   was not written against. The matrix is a real gain and the criterion is a
   real remaining limitation; both are true, so this is the milestone's one
   unmet-in-full criterion.

4. **All four independent lenses have produced bounded accounts.** —
   **Met, unchanged.** All four `track-1-lens-*.md` files exist, each with
   its own independence disclosure, and each stayed within its assigned
   standpoint without adopting another lens's territory. No repair touches
   these files.

5. **Synthesis distinguishes domain defects, communication defects, engine
   or provenance gaps, explicit limitations, and unactionable research.** —
   **Met, unchanged and reinforced.** Track 2 §3 classifies every lens
   finding into a branch, qualification, navigation need, or
   separately-tagged issue. Repair 3's confirmed tax-content gap (`OV-1`) is
   explicitly kept "filed distinctly from explanation design," per the
   charter's own instruction and this packet's `OV-1` section — the
   distinction criterion 5 asks for is exercised, not weakened, by
   resolving `OV-1` from unverified to confirmed.

6. **The actionable register and roadmap reflect the result without
   converting it into automatic implementation scope.** — **Met. Corrected
   by the final repair — this was graded "not met" at a moment when only the
   register half was done.** The register half was corrected by repairs 2,
   3, and 9 (`SC-3`'s conflation, `OV-1` resolved, `GD-1`/`SC-4`/`CQ-1`
   reassessed), and no repair promotes anything into implementation,
   governance, or a committed milestone. The roadmap half was outside the
   repair Builder's three assigned paths and was synchronized by the Foreman
   immediately afterward. Both halves now reflect the result, so the
   criterion is met.

7. **No product contract or governance meaning has been adopted.** —
   **Met, unchanged.** Every packet in this milestone, including this one,
   carries an explicit non-adoption disclaimer; ADR-0009 and other accepted
   governance are read and cited, never reinterpreted. The R2–R5 split
   (repair 5) and the new P5 node (repair 8) are working-lens labels within
   the same non-adopted vocabulary this packet has always used, not new
   governance terms; R5 is, if anything, a sharper statement that
   instrument-authorship at the filing boundary remains reserved, not an
   attempt to resolve it.

8. **The owner has enough evidence to select a contrasting inquiry, a
   narrower build or decision milestone, a pivot, or a stop.** — **Met,
   unchanged.** See §6 below. The four options are laid out with their
   costs; none is selected here, and selecting the next milestone remains
   the owner's. **Corrected by the final repair:** the recommendation *within*
   option A was realigned from `CQ-3` to `CQ-2` on the owner's stated
   purpose for the phase, and `SC-3`/`OV-1` are named as narrower build or
   decision work rather than as grounds for another four-lens inquiry.

**Summary, as corrected by the final repair: seven of eight criteria met.
The one remaining limitation is criterion 3, partially met — the per-node
matrix is a real gain but carries explicitly unfillable fields, and the
criterion's "that answer" premise assumes a canonical answer this milestone
was deliberately re-aimed away from selecting. Criterion 6 is met: the
register and roadmap are both synchronized. The intermediate grading, which
marked criterion 3 met and criterion 6 not met, was a snapshot taken between
the repair and the Foreman's roadmap synchronization and is superseded
here.**

---

## 6. Options for the owner

Four kinds of move are available, each with a real cost and a real return.
This section lays them out; it does not choose among them.

### A. A contrasting inquiry (register `CQ-2` through `CQ-5`)

Running a second full four-lens inquiry against a different plain question,
on the same or a different line, would directly test the conjecture in §3
that the tree's structure generalizes. It is the only option that produces
new evidence about generalization rather than acting on what is already
known. Cost: a full second Track 0–2 cycle (inquiry frame, four independent
lens accounts, synthesis) — the same scale of effort this milestone already
spent once. Candidates, in the order the register currently lists them:

- **`CQ-2`, "Why are you asking me this?"** — tests a genuinely different
  part of the product (a request for information, not a computed result),
  and with it relevance, purpose, authority, and optionality. It is the
  strongest contrasting case for whether the five distinctions and the tree
  shape hold outside a "why is this number here" question entirely. **This
  is the recommended inquiry if exploration continues** (see the
  Recommendation below).
- **`CQ-3`, "Why can't I see a result?"** — has the most existing evidence
  behind it, because the blocked-state finding converged four independent
  ways in *this* milestone. **Not recommended, corrected by the final
  repair.** That evidence is a reason to act on the finding, not to re-run a
  cycle around it; and the inquiry would organize itself around internal
  disposition codes, which is the vocabulary this phase is trying to keep
  users from having to learn. It also tests only
  disposition-generalization, not line-generalization (same fixture,
  different state).
- **`CQ-4`, "What can I do next?"** and **`CQ-5`, "What are you asking me to
  agree to?"** — both remain candidates; the register defers them until
  `CQ-1` (this milestone) reaches, respectively, action-readiness and
  assertion/adoption territory, which it has now done at the boundary (N1/N2,
  A2).

### B. A narrower build or decision milestone

Rather than another exploratory cycle, act directly on the highest-
convergence, best-evidenced findings this milestone already produced: the
voice/authorship rewrite (`SC-9`), the family-specific blocked-message
content change (`SC-3`/`CQ-3`'s evidence base), or a decision on the now-
**confirmed** `OV-1` Schedule B categorical-trigger gap (repair 3 —
verification is done; what remains is whether and how to extend the
attachment rule). This costs less than a full contrasting inquiry and
converts already-strong evidence into a decision, at the cost of not testing
whether the tree generalizes — it commits to acting on what one example
showed before confirming a second example shows the same shape.

### C. A pivot

Two register entries are now plausibly triggered rather than merely
candidate: `AR-1` (the model-agent adversarial program, whose stated trigger
condition is now met) and `GD-1` (a governance reader's companion, partially
evidenced by this milestone's own tree). Either would shift the phase's
center of gravity from "trace one example deeply" to "build a durable
capability." Cost: both are larger, more open-ended undertakings than either
A or B, and `GD-1` in particular risks the phase's own standing warning
against "current-design anchoring" if pursued before a second contrasting
inquiry exists to compare against.

### D. Stop here — a genuine case

The milestone produced one complete, well-evidenced worked example: a fully
traced positive and boundary case, four independent adversarial accounts, a
settled explanation tree with an honest terminus at every branch, and a
freshly consolidated actionable register. **Note, factual:** exit criterion
3's milestone-level gap (no systematic
speaker/basis/invalidator/neighbor-inference tuple, node by node) is
substantially addressed by repair 6's matrix in §2 above, though the
criterion remains only **partially** met — the matrix carries fields that
cannot be filled from present evidence, and it grades a structure the
criterion's singular-answer wording was not written against.
The inquiry *format* itself, not the domain coverage, was and
remains what most needed attention — and that is arguably better fixed by
revising the format before running it again than by running it again in its
current shape. The
phase's own risk list explicitly warns against expanding breadth before
reducing what is already known, and this milestone's own consolidation found
zero entries whose value had actually run out — a genuinely mature, still-
live register, not a backlog of loose ends demanding a next inquiry to
justify itself. Stopping does not waste anything already produced: the tree,
the register, and this packet remain usable reference material regardless of
what happens next. The real cost of stopping is that the generalization
conjecture in §3 stays a conjecture indefinitely, and the two-sentence
answer's disagreements (§2) stay unresolved design questions rather than
becoming design decisions informed by a second data point.

### Recommendation

**Corrected by the final repair. The earlier recommendation here was `CQ-3`,
"Why can't I see a result?" That recommendation is withdrawn**, on the
owner's stated purpose for this phase. `CQ-3` would deepen a message defect
this milestone has already established locally, and it would organize the
next inquiry around the product's internal disposition codes — the opposite
of the direction this phase is testing, which is whether a user can
understand what the system says without first learning the system's own
vocabulary. Strong existing evidence for a finding is a reason to act on the
finding, not a reason to spend a second full four-lens cycle re-confirming
it.

**If exploration continues, the recommended inquiry is `CQ-2`, "Why are you
asking me this?"**

Reasoning: it is the stronger *contrasting* case. It moves from a computed
result to a request for information, and in doing so it tests relevance,
purpose, authority, and optionality — four things this milestone's tree
barely touches, because a displayed number does not ask the user for
anything. That is what makes it evidence about generalization rather than
evidence about the same wall seen from a fifth angle. It also exercises the
five standing distinctions against a case where document completeness and
source-family closure are live in a different way: the system is asking,
rather than reporting.

**`SC-3` and `OV-1` remain available as narrower build or decision work**
(option B). They are the two highest-value concrete findings in hand — a
correctable message defect and a confirmed tax-content correctness gap — and
acting on either is a legitimate next move. Neither is a reason to run
another four-lens inquiry; they are already specific enough to act on
directly.

**What would change this recommendation:** if the owner's priority is
testing whether the tree's structure generalizes to a *different kind* of
line — a directly entered value, a line with no adjustments, or a line that
depends on another form's output, all named in §3 as untested — then a
contrasting-*line* inquiry using the same format beats any further `CQ`. If
the priority is economy over exploration, option B is the better fit than
any inquiry at all. And if the owner judges that a fresh, context-starved
legibility read of this milestone's own output would be more informative
than either, that read is a standing owner-held instrument belonging to a
different mechanism than the phase's own next-inquiry selection.

**This section recommends within option A; it does not select the next
milestone. That remains the owner's.**

---

## Notes on evidence and process

- No engine run, `live_coordinate_run`, or artifact generation was performed.
  Every claim above is read from the six source packets, already-committed
  synthetic content those packets cite, the milestone plan's own text, and
  (for `OV-1` specifically, per repair 3) the official IRS *Instructions for
  Schedule B (Form 1040)*, tax year 2025, "Who Must File," quoted in the
  Track 3 repair charter and above.
- This packet re-verified, directly against committed content, every claim
  the Track 3 repair charter made about blocked codes, closure semantics,
  and citation contents (see repairs 1, 2, 3, and 8); all were confirmed
  accurate against the artifacts as read. `OV-1` — previously flagged as an
  unverified professional recollection — is now a **confirmed** tax-content
  correctness gap, not merely unverified.
- No personal data, real value, real document, private output, disposition,
  refusal reason, or absolute workstation path appears above.
