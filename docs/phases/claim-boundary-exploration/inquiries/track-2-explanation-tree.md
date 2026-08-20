# Track 2 — Explanation Tree, Tension Catalog, and Lens Mapping

Audience: Product, Shared (exploratory record).

Status: **exploratory, non-authoritative.** Reduction and synthesis of Track 0
and the four Track 1 lens accounts, produced under the owner-re-aimed Track 2
charter (removed at publication curation). Creates no product
contract, adopts no definition, reinterprets no accepted contract. *Claim
boundary* and *explanation tree* are working lenses for this phase, not
governance vocabulary and not terms a user must ever see. No engine run, no
generated artifact, no fixture change; only committed synthetic content, the
four lens accounts, and public tax sources were used.

**Corrected by the final repair.** Where this packet writes "the current
package (v33)," read "the v33 comparison target." v33 is the highest-numbered
core package present in the repository and the version this inquiry chose to
compare against; **no committed artifact designates a current package.** The
supported claim is that the line-2b chain is unchanged between the fixture's
adopted v15 and v33 — not that v33 is current or selected. Node P4's "is this
current" question survives as written; what changes is that "current" turns
out not to be a property the repository confers on any package at all, which
strengthens P4 rather than weakening it.

Per the owner's re-aim: this packet does not select one best two-sentence
answer. The four lens answers in
`docs/phases/claim-boundary-exploration/inquiries/track-1-lens-{a,b,c,d}-*.md`
disagree, and those disagreements are treated here as evidence about what
explanatory structure a rich, intuitive interface would need — not as
candidates to be judged against each other.

---

## 0. The five distinctions, restated as they recur below

The charter names five things that get loosely called "complete" or "ready."
They recur throughout this packet under these short names:

1. **Document completeness** — has the user entered every document they hold.
2. **Source-family closure** — the user's per-family assertion mechanism
   ("I have entered every box-N document as of this horizon").
3. **Tax-coverage completeness** — whether the *product* models every category
   a real return could carry (Lens B's territory).
4. **Computation readiness** — whether *this* value can publish now
   (`published_value` vs `blocked` vs `computed_zero` vs `closure_backed_zero`).
5. **Return/action readiness** — whether the user may do some later thing,
   including file.

Every node below that touches "is it all of it" or "is it done" states which
of these five it means. Collapsing them is exactly the failure Lens A, B, and
C each independently found in Track 0's draft language.

---

## 1. The conceptual explanation tree

The root is the visible value and its shortest honest plain answer. Below it
are six branches, organized by the kind of question a person actually has,
not by the system's internal vocabulary. A seventh element — currency — is a
qualification that attaches across branches rather than a branch of its own,
for reasons given at node **P4**.

```
ROOT  "$1825 — Taxable interest"
  ├─ P  Where did this come from?              (origin / provenance)
  │    ├─ P1  Who is speaking — who supplied this number?
  │    ├─ P2  How was it calculated?
  │    ├─ P3  Can I actually see the pieces?
  │    ├─ P4  Is what I'm looking at current?
  │    └─ P5  Why is this amount treated as taxable interest under the
  │           applicable tax rules — not just that the system classified
  │           it so? [added by Track 3 repair 8]
  ├─ S  Is this all of it?                      (scope)
  │    ├─ S1  Which of my documents did the product actually use?
  │    ├─ S2  Have I told the product about everything I have? (doc. completeness)
  │    ├─ S3  Does the product even have a place for every kind
  │    │      of interest that exists? (tax-coverage completeness)
  │    └─ S4  What does "closed"/"confirmed" actually mean and not mean?
  │           (source-family closure, as a concept)
  ├─ T  Does this matter for my taxes, and how?
  │    ├─ T1  What does this number feed into?
  │    ├─ T2  Does something else have to be filed because of this? (Schedule B)
  │    └─ T3  Where did the interest that's *not* here go? (line 2a)
  ├─ A  Who is telling me this, and what am I entitled to believe?
  │    ├─ A1  Is this the software's independent finding, or my own entry
  │    │      summed back to me?
  │    ├─ A2  Does "confirmed"/"closed" mean I swore to the IRS this is true?
  │    └─ A3  Do the citations mean the IRS reviewed this figure?
  ├─ R  Does this have any effect yet?
  │    ├─ R1  Has anything legal happened because this number is on my screen?
  │    ├─ R2  What is the current derived finding's workspace status, right
  │    │      now, inside this system? [Track 3 repair 5: split from the
  │    │      former single R2]
  │    ├─ R3  Does the rendered output have any standing as a return? (no —
  │    │      answerable)
  │    ├─ R4  At what point do acts here acquire legal effect? (filing —
  │    │      answerable as a boundary statement)
  │    └─ R5  (terminus) What does full instrument-authorship amount to at
  │           the filing boundary? — reserved, unbuilt doctrine (ADR-0009)
  └─ N  What do I do now?
       ├─ N1  Nothing — it published; here's what to check before I sign.
       └─ N2  It's blocked — which *source family* has the product not been
              told is closed? [Track 3 repair 2: this is not "which document
              does the product need" — the product cannot know that; see §1]
```

### P — Where did this come from?

- **P1 — Who supplied this number?** Plain form: *"Is this something the
  software found on its own, or something I put in?"* Answering requires
  distinguishing the pins on the derived finding by `origin` — every
  `role: input` pin on the line-2b finding carries `origin: assertion` (Track
  0 Hop 2; Track 1 Lens C §4). Support today: strong at the mechanism level
  (ADR-0009's authorship doctrine — pins → publication act → adoption act →
  user; "the machinery is never the author of anything") but weak at the
  *rendered* level — draft plain-language copy ("we found") says the
  opposite of what the mechanism supports (Lens A §2–3, Lens C §2, §4).
  **This is the single strongest convergence in the whole material** — see
  §3 below.

- **P2 — How was it calculated?** Plain form: *"What was added and
  subtracted to get $1825?"* Requires the composition (seven positive
  families) and the computation rule (minus three adjustment subtotals),
  Hops 3–4 of Track 0. Support today: the rule and composition artifacts are
  committed and confirmed identical between the fixture's adopted package
  (v15) and current (v33). Gap: the presentation only renders the **net**
  figure and the three adjustment tie-out lines; it does not render the
  **gross** seven-family subtotal, so the subtraction that produces 1825 is
  asserted, not visibly reconciled (Lens B §4, secondary observation).

- **P3 — Can I actually see the pieces?** Plain form: *"Show me the actual
  documents that added up to this."* Requires resolving pin ids to
  human-readable evidence. Support today: **thin**. The finding's own `pins`
  array (39 entries) names exact rule/composition/closure ids, but the
  presentation row's five `citationSites` are a *different, disjoint* set —
  recursively-resolved raw source leaves, not the same list (Lens D §4,
  confirmed by reading `presentation_projection.py`). `pinLabels` is an
  empty object in this fixture, so none of those ids resolve to a name a
  reader would recognize (Track 0 Hop 0; Lens A §7; Lens D §2–3). No
  individual document-level amount (e.g., "your 1099-INT box 1 was $X") is
  committed anywhere in this fixture's directory (Track 0 Hop 2; Lens A §5;
  Lens D §5). **This is a genuine floor, not a rendering oversight to fix by
  writing better copy** — the underlying evidence records are not committed
  content.

- **P4 — Is what I'm looking at current?** Plain form: *"Is this number
  built from today's rules, or an old version?"* This node is a
  **qualification that attaches to the whole page**, not a branch specific
  to line 2b, because Lens D found the staleness question does not resolve
  per-line: the same rendered document that carries a current, unaffected
  line-2b chain also carries `line-11` and `line-12` sections built from
  package ids that no longer exist in the current package (v33) — a
  **removal**, not merely an addition (Lens D §4). Support today: the direct
  package-member diff is fully recoverable from committed content, but no
  field in the presentation schema or fixture tells a reader which rows are
  current versus retired; a reader (or reviewer) has to diff package files
  by hand. There is also no committed artifact that formally declares which
  package version is "current" — Track 0, Lens B, and Lens D all independently
  relied on the "highest version number in the directory" convention without
  a committed pointer confirming it (Lens D §5).

- **P5 — Why is this amount treated as taxable interest under the applicable
  tax rules? [Added by Track 3 repair 8.]** Plain form: *"Not just that the
  system classified this as taxable interest — why is that classification
  right?"* Every other node in this tree, including P1–P4, traces *that* the
  system arrived at a classification and how the computation ran; none of
  them trace *why* the tax-law classification itself is correct. Support
  today: examined directly against the two citation artifacts on this
  chain, `tax.us.2025.citation.form1040.line-2b` (v1) and
  `tax.us.2025.citation.schedule-b` (v1). Both are bare authority pointers —
  an `authority.family` (`irs-instructions`), a `form_id`, and a `tax_year` —
  with **no quoted instruction text** committed behind either id. The honest
  statement is that the classification rests on the project's own content
  (the composition and rule artifacts) plus an unquoted reference to an IRS
  authority family; the user-facing explanation terminates there. This is
  the evidence behind repair 1's narrower claim about what "reaches
  authority" means. **This is a terminus, like R5, not a gap this track
  proposes to close** — closing it would mean committing quoted IRS
  instruction text as package content, which is out of this track's scope
  and not something explanation design alone can fix.

### S — Is this all of it?

This branch is where the five distinctions collide hardest, because a
single English sentence ("is this all of it?") can mean any of three of
them.

- **S1 — Which of my documents did the product actually use?** Requires
  naming the *populated* families in this fixture (four of seven directly
  traceable: `f1099int.b1`, `f1099int.b3`, `f1099oid.b1`,
  `non-form-interest`, plus three adjustment families) versus the three
  remaining positive families present only in pin references
  (`form1065-k1.box5`, `f1099int.b10`, `f1099oid.b5`) whose individual
  contribution cannot be separated from committed data (Track 0 Hop 5).

- **S2 — Have I told the product about everything I have?** (**document
  completeness**.) This is what a source-family closure actually attests —
  see S4. Support today exists as a mechanism (per-family closure
  assertions with horizons) but the plain-answer draft's phrasing of this
  concept ("confirmed as complete so far") is the single most contested
  sentence in the whole material — see §3.

- **S3 — Does the product even have a place for every kind of interest
  that exists?** (**tax-coverage completeness**.) This is Lens B's deepest
  thread and it is *not* the same question as S2. The seven-family
  composition's own `claim` field states what it covers, not what it
  omits (Track 0 Hop 4). Lens B verified the composition is a defensible
  subset of ordinary Form 1099-INT/1099-OID/K-1 interest but is missing, at
  minimum: interest reported through a Form 1041 estate/trust K-1,
  seller-financed mortgage interest, and any Series EE/I savings-bond
  exclusion interaction (Form 8815) — real, common categories with **no
  modeled family, composition slot, or disclosed non-goal** anywhere in the
  package (Lens B §4, §7). Support today for *disclosing* this boundary to
  a user: **none** — nothing in the plain answer or the composition's own
  text signals that a boundary of this kind exists (Lens A §3, independently
  reaching the same conclusion from the reader's side: "the dollar total
  invites belief it is a closed inventory, not a boundaried composition").

- **S4 — What does "closed"/"confirmed" actually mean, and not mean?**
  Requires each source family's own `closure_claim` text, which is precise
  and self-limiting (e.g., the box-3 family's claim: "this claim covers Form
  1099-INT box 3 only... it says nothing about... total taxable interest").
  Support exists at the artifact level but is **not currently surfaced to a
  user anywhere in the rendering path** (Lens A §4; confirmed independently
  by Lens B §5 and Lens C §6.3). Two further qualifications belong here, not
  as new branches: the `closure_claim` text is written in present-tense
  declarative voice ("...is recorded...") rather than conditional/attributive
  voice, which risks reading as an already-completed fact rather than what a
  user's own declaration would mean (Lens C §6.3); and it uses "attested" in
  ordinary English immediately adjacent to the kernel's reserved
  `basis: attested` vocabulary from ADR-0009, a collision risk if the string
  is ever copied into a new surface (Lens C §3.4).

### T — Does this matter for my taxes, and how?

- **T1 — What does this number feed into?** Not independently explored by
  any lens at the line-2b boundary; the material chain (Hop 6–8 of Track 0)
  supports the general fact that line 2b feeds AGI, but no lens drilled into
  *how far* that consequence propagates. Recorded here as an
  under-supported node, not as a finding — a gap in the evidence this track
  can point to, not resolve.

- **T2 — Does something else have to be filed because of this?** Requires
  the Schedule B attachment rule (Hop 7 of Track 0). Support today: the
  committed `attachment-rule.v6` instance compares the **gross** positive
  total plus ordinary dividends against a $1,500 threshold, plus foreign
  account/trust questions. Lens B's deepest thread found this may not be
  the *whole* rule — see §4 (separate correctness issue, not resolved here).
  What the tree can say honestly today, without resolving that question: the
  dollar-threshold test is real and implemented; whether it is the *only*
  test is an open verification question, and an explanation that presents
  the threshold as the complete rule would be overclaiming.

- **T3 — Where did the interest that's not here go?** Line 2a, tax-exempt
  interest. Support today: the composition explicitly excludes Form
  1099-INT box 8 (Track 0 Hop 5b), but the plain-answer draft only says
  what is excluded, not where it lands — Lens A independently found this
  is exactly the phrasing gap that would make a muni-bond holder worry the
  amount "fell out of the return entirely" (Lens A §3).

### A — Who is telling me this, and what am I entitled to believe?

- **A1 — Software's own finding, or my entry summed back?** See P1; this is
  the same underlying fact read through a different question (authorship
  vs. speaker-attribution). The two nodes are kept distinct because P1
  answers "where did the number come from" (a provenance question) while A1
  answers "who is making a claim to me right now" (a reliance question) —
  the artifacts are the same, the reader's stake is different.

- **A2 — Does "confirmed"/"closed" mean I swore something to the IRS?**
  Requires distinguishing a workspace closure declaration (revocable,
  updatable, pre-filing) from the Form 1040 jurat ("under penalties of
  perjury..."). Support today: the distinction is real and grounded in how
  closures work mechanically, but **nothing in the rendered row or its
  citation sites currently states this distinction to a user** (Lens C §3.2).
  This is the node where Lens B's and Lens C's independent findings
  converge exactly (§3 below).

- **A3 — Do the citations mean the IRS reviewed this figure?** Requires
  opening the citation artifacts themselves. Support today: both citation
  artifacts on this chain (`citation.form1040.line-2b`,
  `citation.schedule-b`) are, as committed, bare authority pointers — an
  authority family, a form id, a tax year — with **no quoted instruction
  text** (Track 0 Hop 6; Lens C §3.3 independently confirms by opening both
  files). As currently rendered, this is a real mitigation: the fixture does
  not currently present these as inline "citations" a reader could
  over-read. The finding here is a **latent risk**, not a realized one: *if*
  a future surface ever renders these pointers as inline citations next to
  a dollar amount, a reader could reasonably infer IRS endorsement that no
  artifact on the chain asserts or could assert.

### R — Does this have any effect yet?

- **R1 — Has anything legal happened?** Answerable today as a negative/
  boundary statement: nothing has been filed, transmitted, or signed; the
  figure has no legal effect until then. This much is settled by the
  ordinary fact that filing is a distinct, later act (Lens C §4).

**Corrected by Track 3 repair 5.** The former single R2 node collapsed four
things that come apart; each is now its own node.

- **R2 — The current derived finding's workspace status.** Answerable today:
  inside this system, right now, the value is a `published_value`-disposition
  derived finding — a computed result the engine currently stands behind
  given the closures and inputs on record, revocable and updatable as those
  change. This is a fact about the workspace's own internal state, stated
  without reference to any legal or filing consequence.

- **R3 — The rendering's lack of legal standing.** Answerable today: the
  drawn output — the row on the page — is not a return and has no standing
  as one. Nothing about a rendered document constitutes a filed instrument;
  producing a rendering is not an act with legal consequence.

- **R4 — Legal effect entering at filing.** Answerable today as a boundary
  statement, the same content the former R2 called R1's "negative statement":
  filing is the distinct, later act at which acts here first acquire legal
  consequence; nothing has been filed, transmitted, or signed as of the
  workspace state this tree describes (Lens C §4).

- **R5 — Terminus: the fuller instrument-authorship question.** This is the
  only genuine terminus among the four. ADR-0009's own "What T1 still
  reserves" section names, as explicitly unbuilt doctrine, "what
  instrument-authorship amounts to at the filing boundary" (Lens C §4,
  quoting the accepted ADR directly). A positive characterization beyond R2,
  R3, and R4 — "this is your working determination," "this is a mere
  preview," or any other framing of what the pre-filing figure's standing
  *amounts to* as an instrument — would be improvising governance doctrine
  that does not yet exist. **The tree stops here by design, not by
  omission.**

### N — What do I do now?

- **N1 — Published, nothing blocking.** Requires connecting to S1/S2 (which
  documents are reflected) so the instruction is concrete: *check your own
  list of interest-bearing accounts against what's shown* — an instruction,
  not a state description (Lens A §2's rewrite makes exactly this move).

- **N2 — Blocked or an undeclared family.** This is the CB-N1 boundary case.
  **Corrected by Track 3 repair 2** — the node's own name is corrected here
  from "which document does the product need" to what the artifacts actually
  support. Support today at the *data* layer is strong, and more extensive
  than previously stated: the computation rule
  (`tax.us.2025.rule.form1040-line2b` v4) carries **ten**, not seven,
  distinct `require_closed` conditions in its `when` clause — one per
  constituent source family, seven positive interest families plus the
  three Schedule B adjustment families — so the system *can* in principle
  identify which *source-family closure* is unmet (verified directly against
  the rule artifact; Track 0 §3, CB-N1 discusses the same mechanism).
  **That is a narrower claim than "which document is missing."** A
  `require_closed` check tests whether the user has *declared* a source
  family closed as of a horizon, not whether the user holds or lacks a
  particular document — an unmet closure is consistent with the user holding
  an unentered document, holding no document and not having said so, or
  simply not having reached that step; the artifacts do not distinguish
  these, and no committed content asserts which one applies in a given case.
  Support at the *rendered* layer is weak: the `blocked` disposition's
  `explain` text is one generic sentence, identical across all four blocked
  codes (`DEPENDENCY_ABSENT`, `DEPENDENCY_INVALID`,
  `CATEGORICAL_DOMAIN_MISMATCH`, `SOURCE_SET_UNCLOSED`), and does not
  interpolate which family is undeclared (Lens A §4, confirmed directly
  against the form-field artifact; Lens B §5 and Lens D §7 independently
  confirm the same gap). **This is the strongest four-way convergence in the
  material** (Track 0 + three lenses) — see §3. The convergence is on the
  discarded-specificity gap; it is not evidence that the system can name a
  missing document.

---

## 2. Catalog of recurring tensions

Bounded by usefulness, not by count — each entry below could change the
organization, content, navigation, qualification, or evaluation of an
explanation. None is discarded to reach a round number.

1. **Exactness vs. reachable depth.** Lens B's box/entity-level enumeration
   is unsuitable as root-level copy but is exactly right one layer down.
   Shows up at S3, P2, T2. What turns on it: whether "depth" is a real
   design primitive (a person can descend) or the tree collapses into one
   compromise sentence, which the charter explicitly forbids.

2. **State description vs. instruction.** "Confirmed as complete so far"
   (a state description) reads as reassurance; "check your list before you
   file" (an instruction) reads as a caveat, from the same underlying fact.
   Shows up at S2, N1. What turns on it: whether the *same* information
   protects a reader from a wrong inference or invites one, purely by
   grammatical mood.

3. **Agency attribution ("we found" vs. "you entered").** Shows up at P1/A1;
   grounded in accepted doctrine (ADR-0009), not just a style preference.
   What turns on it: whether the explanation's very first clause is
   consistent with who the project's own governance says is the author of
   the number.

4. **Boundary disclosure vs. conciseness.** Naming what is excluded (S3,
   T3) makes the plain answer longer and could read as hedging; omitting it
   lets a reader assume more coverage than exists. What turns on it:
   whether the tree needs a standing "there's a boundary here, even if I
   don't enumerate it" signal at the root, independent of whether the deep
   enumeration is ever shown.

5. **Visible arithmetic vs. simple total.** The rendered figure is net; the
   gross subtotal and the three adjustments are shown as separate tie-out
   lines that don't visibly reconcile to the net figure (P2). What turns on
   it: whether a reconciling reader (a preparer habitually checking a
   client statement) can trust the number without opening the underlying
   rule artifact.

6. **Technically inspectable vs. actually inspectable.** The finding's
   `pins` array names everything mechanically, but `citationSites` is a
   disjoint, narrower set, and `pinLabels` is empty (P3). What turns on it:
   whether "you can drill into this" is a true claim a rendered surface can
   make, or only a true claim about the underlying data model.

7. **Closure as assertion vs. closure as verification.** "Closed,"
   "confirmed," and "attested" all carry ordinary meanings a taxpayer would
   apply to the act of signing (S4, A2). What turns on it: whether a reader
   could reasonably (and wrongly) believe a workspace declaration already
   carries the weight of a jurat, before filing has even happened.

8. **Uniform generic messaging vs. condition-specific detail in blocked
   states.** N2's `explain` string is identical across four distinct codes,
   though the rule data can distinguish them. What turns on it: whether a
   blocked user has a concrete next action or has to guess.

9. **Row-level currency vs. page-level trust.** A reader who confirms
   line-2b's own chain is current has no basis to infer the rest of the
   page is current — line-11/line-12 on the *same document* are structurally
   retired (P4). What turns on it: whether "this row is right" can ever be
   answered without also answering "is the page I'm reading it on right."

10. **Product-declared universe vs. domain-complete universe.** The
    composition's own `claim` field is internally self-consistent (it says
    exactly what it covers) but is silent about what it doesn't (S3). What
    turns on it: whether "tax-coverage completeness" is knowable from the
    artifact alone, or only by comparison against a domain expert's
    independent knowledge — which this project cannot encode into the
    artifact's own text without a product-coverage decision.

11. **Dollar-threshold framing vs. categorical triggers.** If Schedule B's
    "who must file" test is ever presented as a single amount comparison,
    it may be incomplete (T2) — an open verification question, not a
    resolved fact, but one that constrains what T2 may honestly claim until
    resolved.

12. **Internal vocabulary vs. plain language, at every depth.** Every lens
    independently flagged specific words ("constituent interest families,"
    "dependencies," "closure," "attested," "composition") as the reader's
    first signal of trust or distrust, not neutral technical terms. What
    turns on it: whether the tree's own node names (used for design
    purposes in this packet) ever leak into rendered copy — they must not.

13. **Honest termini vs. the appearance of a complete answer.** Every lens
    independently hit a wall it could name precisely (P3's missing
    document-level detail, R2's reserved T1 doctrine, S3's undisclosed
    domain gap, P4's undeclared "current package" convention). What turns
    on it: whether an interface is designed to *say* where it stops, or
    is designed to look complete by silently declining to raise the
    question.

14. **Citation-as-pointer vs. citation-as-endorsement.** A bare authority
    pointer, rendered as an inline "citation," invites an inference of IRS
    review that the artifact does not support (A3). What turns on it:
    whether the word "citation" itself is safe to use as a UI affordance
    without qualification.

15. **Local answer sufficiency vs. accepted-doctrine limits.** R1 can be
    answered from committed content and general fact; R2 cannot be, without
    exceeding what the project's own accepted ADR has settled. What turns
    on it: whether a designer notices the difference between "I don't know
    yet" and "the project has decided not to say" before writing copy that
    implies the latter is actually the former, or vice versa.

16. **Root-level placement of the filing-effect boundary.** Lens C's
    rewrite puts "nothing about this figure has legal effect until you
    file" *inside* the two-sentence root answer; the other three lenses'
    rewrites do not surface it at that depth at all. This is not the same
    tension as #15 — it is a genuine open design fork about *where in the
    tree* R1 belongs, not about what R1 may say. See §3's disagreements.

---

## 3. Mapping every lens finding to its place

Findings are grouped by lens, then classified as **[Branch]**, **[Qual]**
(qualification attached to a node), **[Nav]** (navigation need — evidence
about moving between depths), or **[Issue]** (a separate correctness,
maintenance, or governance question — kept visibly apart from the tree).
Convergences and disagreements are called out where found.

### Lens A — Casual invested reader

| Finding | Placement |
| --- | --- |
| "Confirmed as complete so far" reads as praise, not caveat | **[Qual]** S2 — tension #2 |
| "We found" implies discovery, not supply | **[Qual]** P1/A1 — tension #3. **Converges independently with Lens C §2, §4.** |
| "Doesn't include tax-exempt interest" doesn't say where it went | **[Qual]** T3 |
| Dollar total invites belief in a closed inventory, not a boundaried composition | **[Branch cue]** S3 (the branch already exists from Lens B's deeper drill-down; Lens A independently supplies the *reader-side* symptom — see convergence below) |
| CB-N1 blocked-state explain string is generic, unusable by a reader | **[Qual]** N2. **Converges with Track 0's own SC-3, and independently with Lens B §5 and Lens D §7 — the strongest convergence in this material.** |
| Register: replace state description with instruction | **[Qual]** applies to S2/N1 (tension #2), a content-drafting probe, not an artifact change |
| Register: name where tax-exempt interest lands | **[Qual]** T3, content-only |
| Register: interpolate missing family name into blocked explain text | **[Issue]** — a content/schema-field-authoring change (SC-3, already in the register); this track does not adopt it, only confirms placement |
| Register: probe a real naive reader against the current blocked.explain string | **[Nav]** — an evaluation probe, not a tree node; recorded in §5 |
| Register: one-line boundary signal at the root, without full enumeration | **[Branch]** — this is exactly what S3 needs at the root depth; see the worked path in §4 |
| Discarded: pronoun referent of "we" in draft-only prose | not placed — no committed copy artifact to check against, correctly discarded |
| Discarded: reconstructing the $1825 sum from visible data | not placed — outside this lens's question, correctly discarded |
| Noticed but not pursued: empty `pinLabels`, unresolved pin ids | **[Issue]**, Lens D's territory — correctly deferred, and Lens D independently develops it (see below) |

### Lens B — Tax/financial-practice adversary

| Finding | Placement |
| --- | --- |
| "We found" reads as "we found everything" for unmodeled categories (estate/trust K-1, seller-financed mortgage) | **[Branch]** S3 |
| "After subtracting adjustments you told us about" sounds optional when it is often mandatory | **[Qual]** T2, and touches N1 (the instruction a signing preparer needs) |
| "$1,500 triggers Schedule B" read as the whole rule | **[Qual]** T2, paired with an **[Issue]** below |
| "Confirmed as complete so far" could read as IRS agreement | **[Qual]** A2. **Converges independently with Lens C §3.2** — Lens B flags it but explicitly defers development to Lens C ("closer to Lens C's territory... I flag it, but do not develop it," §3), and Lens C does develop it. |
| Deepest thread: seven-family composition is a defensible subset, not the complete domain universe (missing estate/trust K-1, seller-financed mortgage, Series EE/I exclusion interaction) | **[Branch]** S3 *and* **[Issue]** — the disclosure gap is a branch (the tree needs a node saying the boundary exists); the underlying absence of those families from the product is a genuine tax-coverage-completeness limitation, not something an explanation can fix by wording alone |
| Deepest thread: attachment rule tests only the gross-vs-threshold branch; Lens B's professional recollection is that accrued-interest, ABP, and nominee entries independently trigger Schedule B regardless of amount, unverified against committed IRS text | **[Issue]** — explicitly the charter's carried open item (see the charter's "One open item to carry, not settle"). Not a branch: this constrains what T2 may honestly claim, but resolving it requires public-source verification this track does not perform. |
| Secondary: gross seven-family subtotal not shown; net figure and three adjustment lines don't visibly reconcile | **[Qual]** P2, **[Nav]** — a reader who wants to verify the subtraction has no path to the gross figure today |
| Register: verify against IRS Schedule B "who must file" text | **[Issue]** — carried, see above |
| Register: add rendered gross subtotal line | **[Qual]**/**[Nav]** on P2 |
| Register: disclose uncovered categories | **[Branch]** S3, same as above |
| Register: family-specific blocked explain text | **[Issue]**, converges with SC-3 (already registered) |
| Register: commit quoted instruction text behind citation artifacts | **[Issue]** — a content/maintenance gap underlying A3's terminus |
| Register: preparer-facing surfacing of full `closure_claim` text | **[Nav]** — a depth/audience question, see §4 and tension #1 |
| Discarded: OID acquisition-premium subtleties | not placed — pre-netted upstream, no action, correctly discarded |
| Discarded: foreign interest/Form 1042-S | **[Issue]**, named but not developed — no modeled boundary artifact to check against; recorded as part of the general disclosure probe (folds into S3/SC-10 below) |
| Discarded: closure-horizon staleness vs. amendment workflow | correctly deferred to Lens D's territory |
| Discarded: register-of-tone question about "we found" | correctly deferred to Lens A's territory |

### Lens C — Legal/epistemic adversary

| Finding | Placement |
| --- | --- |
| "We found" contradicts ADR-0009's authorship doctrine | **[Qual]** P1/A1. **Converges independently with Lens A §2–3** — the strongest cross-lens agreement on wording, reached by two lenses with entirely different standpoints (reader comfort vs. governance conformance). |
| "Confirmed as complete" risks reading as a legal jurat | **[Qual]** A2. **Converges independently with Lens B §3** (Lens B flagged, Lens C developed). |
| Citation pointers could be over-read as IRS sign-off if ever rendered as inline "citations" | **[Branch]** A3, currently a **latent** risk, not realized in the committed fixture |
| "Attested closed" collides with the kernel's reserved `basis: attested` vocabulary | **[Issue]** — terminology hygiene in committed content (`form1040.line-2b.form-field.v5.json`), not itself a tree branch, though it constrains what S4/A2 may safely quote verbatim |
| Track 0's Hop 2 imprecisely describes all fourteen `origin: assertion` pins as "the user's own closure declarations"; ten of them (`finding:derived:*`) are computed, assertion-backed subtotals, not direct user statements | **[Issue]** — a documentation-accuracy finding about Track 0's own prose, not a tree branch; it sharpens P1/A1's distinction between "directly asserted" and "computed but assertion-backed," which this tree's P1 node now states with that sharper distinction |
| Deepest thread: CB-A1's distinction (computational support vs. legal filing effect) holds up for negative/boundary statements but not for a positive characterization of pre-filing standing, per ADR-0009's own "What T1 still reserves" | **[Branch]** R1 (supported) and R2 (explicit terminus, unsupported by design — see §1) |
| Side-note: `AGENTS.md`'s enumerated T1 guardrail sentence no longer appears verbatim; the enumeration now lives only in `docs/governance/README.md`'s backlog | **[Issue]** — minor, verified documentation drift, not developed further |
| Register: rewrite "we found" project-wide, consistent with ADR-0009 | **[Qual]** P1/A1 |
| Register: state the filing-effect boundary explicitly near computed lines | **[Branch]** R1 — but see the disagreement below about *where* (root vs. deeper) |
| Register: rewrite `closure_claim` strings to conditional/attributive voice before ever surfacing them | **[Qual]** S4, **[Issue]** (a content-authoring change to multiple family artifacts, not adopted here) |
| Register: decision question — should a pre-filing standing statement be recorded, or should everything stay negative/boundary-only until T1 resolves | **owner-held, not this track's to answer** — recorded as-is in §5 |
| Register: audit disposition `explain` strings for reuse of kernel-reserved vocabulary | **[Issue]**, same as "attested" finding above |
| Register: correct the pin-speaker-role description in any future written trace | **[Issue]**, documentation-accuracy, applies to this packet's own P1 language (addressed directly in §1) |
| Discarded: whether the seven-family composition is the correct domain universe | correctly deferred to Lens B's territory (Lens B develops it; see S3 above) |
| Discarded: provenance recoverability (empty `pinLabels`, unresolved ids) | correctly deferred to Lens D's territory (Lens D develops it; see below) |
| Discarded: the Schedule D attachment row visible elsewhere on the same fixture | correctly out of scope — a different line |
| Discarded: the ten `closure-mapping.*` package pins' own text | correctly discarded — redundant with the pattern already established from four family files |

### Lens D — System/provenance adversary

| Finding | Placement |
| --- | --- |
| Added clause "tap to see categories" asserts inspectability the artifact does not demonstrate | **[Qual]** P3, **[Nav]** — names the exact gap: the underlying data to make the clause true *exists* (pins), but no rendering surface currently exposes it in named form |
| `citationSites` (5) and the finding's `pins` (39) are disjoint sets by design, confirmed by reading `presentation_projection.py` | **[Branch]** P3, **[Issue]** — the disjointness itself is undocumented anywhere a downstream consumer could find without reading generator code |
| Empty `pinLabels` is not necessarily broken — the generator treats an absent label as legitimate for a directly-attested finding | **[Qual]** P3 — a caution against over-interpreting absence as defect |
| Track 0's open question 4, answered: direct one-hop lineage is fully recoverable from the artifact; evidentiary leaves and human labels are not, without out-of-band access | **[Branch]** P3, confirming and sharpening the node's honest terminus |
| Deepest thread: fixture staleness includes outright removal (`line-11`, `line-12` package members), not just addition — a pattern distinct from CB-A2's framing | **[Branch]** P4 (new node this track names explicitly, per §1) |
| No committed artifact declares which package version is "current"; the "highest version number" convention is relied on by multiple accounts without a committed pointer | **[Issue]** — a governance/registry gap underlying P4 |
| Register: per-row staleness signal | **[Branch]** P4 |
| Register: distinguish citation-leaf from lineage-pin vocabulary in schema/docs | **[Issue]**, converges with the disjoint-sets finding above |
| Register: record what "current selected package" formally means | **[Issue]** |
| Register: regenerate fixture against v33 and diff pinLabels/citationSites | **[Issue]** — explicitly requires a run; out of this documentation-only track's authority, correctly named as a future probe rather than performed |
| Register: UI experiment on unresolved citation pin rendering | **[Nav]** — an evaluation probe for P3, recorded in §5 |
| Register: decision question on whether raw-id-only resolution is an accepted schema terminus | **owner-held, not this track's to answer** |
| Discarded: seven-family composition's tax-domain correctness | correctly deferred to Lens B |
| Discarded: whether closure-claim wording would mislead about completeness | correctly deferred to Lens C |
| Discarded: granularity of `activeCodes` on blocked dispositions | correctly discarded — restates Track 0's SC-3 with no new action |
| Discarded: Schedule D's blocked state elsewhere in the fixture | correctly out of scope |
| Discarded: reused `rounding` pin id across five unrelated lines | correctly discarded — fully explained by generator code, no new action |
| Disclosure: recognized Lens A's filename in a broad grep, did not open it | honor-rule disclosure, no placement needed |

### Cross-lens convergences (stronger than any single account)

1. **"We found" misattributes agency** — Lens A (reader comfort) and Lens C
   (governance conformance) reach the identical correction independently
   from entirely different standpoints. Placed at P1/A1.
2. **"Confirmed as complete" risks an authority inference** — Lens B flags
   it and explicitly defers; Lens C develops it fully. Placed at A2.
3. **The generic blocked-state explain text is a real gap** — Track 0 names
   it first (CB-N1, seeded as SC-3), then Lens A, Lens B, and Lens D each
   independently re-derive the same finding from reader-comfort,
   practitioner-reconciliation, and mechanical angles respectively. Four
   independent routes to the same node (N2) is the single strongest piece
   of convergent evidence in the whole inquiry.
4. **The boundary of "taxable interest" is invisible from the plain
   answer** — Lens A finds the reader-side symptom (the dollar total
   invites belief in a closed inventory); Lens B independently finds the
   domain-side cause (real categories are absent and undisclosed). Both
   place at S3, from opposite directions.

### Preserved disagreements

1. **Where the filing-effect boundary belongs (R1).** Lens C's rewrite
   states it explicitly inside the two-sentence root answer. Track 0's
   original, Lens A's, Lens B's, and Lens D's rewrites do not surface it at
   the root at all — they leave it as background prose Track 0 supplied
   underneath the draft. This is not a wording dispute to resolve by
   picking a winner: it indicates that *how urgently* the filing-effect
   boundary needs to be root-level content may depend on context a
   generalized tree cannot settle — e.g., whether the surface is a review
   screen the user is about to sign (Lens C's implicit context) versus an
   in-progress entry screen (Lens A's and Lens D's implicit context, where a
   document is still being gathered). **Recorded as tension #16, not
   resolved.**

2. **How much box/entity-level detail belongs in the first sentence.**
   Lens A deliberately keeps the root answer at the form-name level
   ("1099-INT, 1099-OID, and other interest documents") and pushes exactness
   to an instruction ("check your list before you file"). Lens B rewrites
   the *same* first sentence to name boxes and entities explicitly
   ("Form 1099-INT boxes 1, 3, and 10, Form 1099-OID boxes 1 and 5, Schedule
   K-1 (Form 1065) box 5..."). Both are defensible answers to the identical
   question, for different readers. This is not a contradiction the tree
   needs to resolve — it is direct evidence that **S3's box-level detail
   belongs one layer beneath the root, reachable but not mandatory at
   depth zero**, exactly the shape the worked path in §4 uses.

3. **How much the plain answer should hedge on document completeness.**
   Lens A's rewrite states the caveat as an instruction ("check your list");
   Lens D's rewrite states it as an affordance ("tap any part... to see
   which categories those are") that the fixture cannot currently back up.
   Both are attempts to solve tension #2 (state description vs. instruction)
   but choose different mechanisms — one behavioral, one navigational. Not
   resolved; both are legitimate design directions depending on whether the
   eventual surface can actually deliver inspectability (P3's terminus).

---

## 4. Worked demonstration: progressive disclosure down the "Is this all of it?" branch

One path, worked end to end, showing the actual language at each depth,
with an explicit terminus. This exercises S3 (tax-coverage completeness),
because it is where the strongest cross-lens convergence (finding 4 above)
and the sharpest terminus (Lens B's domain-gap finding) both sit.

**Depth 0 — root.** Rendered next to the number, no interaction required.

**Corrected by Track 3 repair 4.** The original depth-0 sentence said "the
interest documents you entered," which implies every dollar in this total
came with a document — untrue of the composition itself, which includes a
non-form interest family (`tax.us.2025.non-form-interest`), confirmed
directly against the committed composition artifact. A disclosure path that
implies "interest means a form you received" misdescribes the modeled
universe. Corrected:

> This $1825 is the total taxable interest you entered — whether it came
> with a form like a 1099-INT or 1099-OID, or you reported it without one —
> minus any nominee, accrued-interest, or bond-premium adjustments. It
> doesn't include tax-exempt interest like municipal bond interest, which is
> reported on a different line of your return.

Test: no internal vocabulary ("we found," "constituent," "composition,"
"closed" are all absent). A reader can stop here and have a true, if
incomplete, answer, and that answer no longer implies a document is always
required.

**Depth 1 — reached by an explicit "what's included" affordance, not implied
by the root sentence alone.**

> This covers interest from 1099-INT and 1099-OID forms, interest reported
> through a partnership Schedule K-1, and interest you told us about that
> didn't come with a form. If you have a kind of interest income that isn't
> one of those, it may not be included yet — see below.

Test: names the boundary's *existence* honestly (tension #4) without yet
requiring the reader to know box numbers. This is the layer Lens A's
one-line addition targets.

**Depth 2 — reached by "see below" or an equivalent explicit descent.**

> Specifically, this includes: Form 1099-INT boxes 1, 3, and 10; Form
> 1099-OID boxes 1 and 5; interest from a partnership Schedule K-1, box 5;
> and interest you reported without a form. It does not currently include
> interest reported through an estate or trust (a Form 1041 Schedule K-1),
> seller-financed mortgage interest someone paid you directly, or the
> interaction with the savings-bond interest exclusion (Form 8815).

Test: this is Lens B's box/entity-level language, verbatim in substance,
reached only by explicit descent — not forced on the depth-0 reader. Every
noun here is a real form or box a taxpayer could hold, not a system
abstraction.

**Terminus — explicit, not silent.**

**Corrected by Track 3 repair 4.** The original terminus said "you (or your
preparer) would need to report them separately for now" — this implies an
available manual-entry, alternative-reporting, or filing route that nothing
in this milestone establishes exists, is supported, or is safe. Corrected to
state the limitation and stop:

> If any of those missing categories apply to you, this product doesn't yet
> have a place for them. They won't show up on this line, and entering them
> elsewhere in this product will not cause them to be included here. This
> product does not currently tell you how or where to report them — that is
> outside what it does today.

Test: this is the honest floor. It does not say "check with support" (a
dead end Lens A specifically flagged for the *blocked*-state string, and
the same failure mode would apply here if this terminus pretended the
product already handles the gap). It does not imply a workaround the product
has not established (the corrected defect). It also does not attempt to
enumerate every conceivable domain category (Lens B's own three examples are
illustrative, not exhaustive, and the composition artifact itself makes no
claim to exhaustiveness). What lies beyond this terminus — whether and when
those categories get built, or where else a filer would report them — is a
product-roadmap and tax-practice question this product does not answer, and
the tree stops rather than inventing an answer.

**What this demonstrates:** a person can descend three layers without ever
encountering "composition," "family," "closure," or "pin," and the exact
technical content Lens B insisted must stay reachable (box 1, box 3, box
10, box 5, box 5) survives intact at depth 2 — it is simply not the first
thing shown. Each layer stays true to the one above it: depth 1 does not
contradict depth 0, and depth 2 does not contradict depth 1; the terminus
does not claim more than depth 2 supports.

---

## 5. Interface and evaluation consequences

A small set, none of them production UI design.

1. **Depth must be a real, navigable primitive, not a formatting choice.**
   The worked path in §4 only works because deeper layers exist and are
   reachable from shallower ones without forcing descent. Any prototype
   built from this tree needs an actual mechanism for "show more," not just
   a longer paragraph.

2. **Provenance needs two distinguishable evidence tiers, not one.** Lens D
   found the code already treats "lineage pins" (rule, composition,
   closures) and "citation-site leaves" (raw evidence) as different sets by
   design. An explanation surface that treats them as one undifferentiated
   pile of ids will either overpromise inspectability (implying every id is
   drillable to a labeled document) or underuse the structure that already
   exists. This is a structural requirement on any future presentation
   surface, not a copy fix.

3. **Blocked/incomplete states need condition-specific text as a template
   capability**, not a single generic sentence — this is SC-3, now converged
   on four independent times (§3), and it is the strongest single signal in
   this inquiry that a specific content/schema change (not merely
   better prose) is warranted.

4. **Row-level currency needs to be independently knowable**, or any "is
   this current" question a reader asks about one row cannot be honestly
   answered without also answering it for the whole page — see tension #9
   and node P4.

5. **Voice consistency ("who is speaking") is a cross-cutting authoring
   constraint, not a one-off copy edit.** The "we found" defect and the
   `closure_claim` present-tense-declarative defect are the same underlying
   problem (system-voice claiming what is actually the user's own
   assertion) appearing in two different artifact types (draft plain
   answers and source-family content). A style rule applied once to a
   two-sentence answer will not fix the family artifacts it doesn't touch.

6. **The filing-effect boundary's placement (root vs. deeper) is an open
   design question, not a settled one** — disagreement #1 in §3. Any
   evaluation of a future explanation surface should test both placements
   against different contexts (review-and-sign screen vs. in-progress entry
   screen) rather than assuming one is universally correct.

7. **Honest termini should be treated as a first-class design element.**
   Every branch in §1 that reached a wall (P3's missing document-level
   detail, R2's reserved doctrine, S3's undisclosed domain gap, P4's
   undeclared package convention) named that wall precisely. A future
   evaluation should test whether a reader descending a real interface can
   tell the difference between "there's nothing more to show you" and "I
   haven't built the next layer yet" — those are different findings and a
   silent stop conflates them.

8. **Evaluation probes should be phrased as node-recovery questions**, not
   generic usability questions: for a given surface, can a reader
   independently state which of the five distinctions (§0) a given sentence
   is actually making a claim about? Can they name, in their own words,
   what they would have to go do from a blocked state? This tree gives a
   concrete battery (one probe per leaf node) rather than a general claim-
   integrity instrument, consistent with the charter's bound against
   producing a general semantic model here.

---

## 6. What generalizes, and what does not (conjecture, marked as such)

**Conjecture, not established by this inquiry:** the six top-level branches
(P, S, T, A, R, N) look like they would recur for other computed-line
questions in this product ("why is this amount," "why can't I see a
result," "what do I do next" are all named as candidate follow-up inquiries
in the actionable register). The *specific* leaf content (seven-family
composition, Schedule B threshold, box numbers) is entirely specific to
line 2b and would need to be re-derived, not copied, for any other line.
This track does not test that conjecture against a second line and does not
claim it holds beyond this one worked example.

**Established by this inquiry, not conjecture:** the five distinctions in
§0 are real and load-bearing for line 2b specifically — every branch above
that risked collapsing them was independently caught by at least one lens.

---

## Disclosures

- No engine run, `live_coordinate_run`, or artifact generation was
  performed. All findings above are read from the four committed lens
  accounts, the Track 0 packet, already-committed synthetic content named
  therein, and the milestone plan.
- This packet does not select a single best two-sentence answer, per the
  owner's re-aim; §4's worked path shows one depth-progression, not a final
  answer.
- No personal data, real value, real document, private output, disposition,
  refusal reason, or absolute workstation path appears above.
