# Track 1 — Lens D: System / Provenance Adversary

Audience: Product, Shared (exploratory record).

Status: **exploratory, non-authoritative.** Paper analysis of already-committed
synthetic content only. Creates no product contract, adopts no definition,
reinterprets no accepted contract. "Claim boundary" is a working lens for this
phase, not governance vocabulary. This account is independent of the other
three Track 1 lens accounts; it was written without reading them, per the
charter's independence rule (see the disclosure note at the end).

> **Reader's annotation added by the final repair. This account is preserved
> as written — it is independent evidence and is not rewritten.** Where it
> refers to "the currently selected package" or "the current selected
> package" (v33), read "the v33 comparison target": v33 is the
> highest-numbered core package present in the repository and the version
> this inquiry chose to compare against, and **no committed artifact
> designates a current package.** This account's own §6 recommendation — that
> the project decide and record somewhere committed what "current selected
> package" means — is the finding that survives, and it is strengthened, not
> weakened, by the confirmation that no such designation exists. Recorded as
> `SC-4`.

> The question: **Why is this amount on my return?**
> The amount: `1825` on the `line-2b` row of the committed synthetic fixture
> `packages/sample_data/schedule_b_interest_adjustments/presentation/mixed-schedule-b-interest-adjustments.presentation-model.v1.json`.

---

## 1. Lens and standpoint

I am reading as a downstream consumer who never ran the engine and never will:
a UI renderer, a second-line reviewer, or an auditor who has been handed
exactly one artifact — this presentation model JSON — and nothing else. My
job is not to judge whether `1825` is the right number; my job is to answer
"how much of the chain that produced this number can I recover from what is
in front of me, and at what point do I have to trust something I cannot see."
I care about resolvability: does every reference in this document point
somewhere I can actually go, or does it point into a void I have to fill with
assumed context I happen to have (because I work here) but a genuine outside
consumer would not?

What I notice that a tax-literate or legally-trained reader would not: I do
not care whether "seven-family composition" is the correct tax universe, and
I do not care whether the sentence "confirmed as complete so far" would
mislead a filer. I care about the mechanics of the document itself — which
ids are load-bearing versus decorative, which fields are populated by design
versus by omission, and whether a person with only this file and a text
editor could reconstruct the same trust judgment a person with full repository
access could. A gap that a tax reviewer would call "acceptable summarization"
I might call "unrecoverable provenance," and those are different findings even
when they point at the same field.

---

## 2. Best two-sentence plain answer

I largely keep Track 0's draft answer in substance but would add one clause
Track 0's version omits: a pointer to inspectability, because my lens exists
specifically to test whether a reader can act on "confirmed as complete so
far" rather than just read past it.

> This $1825 is the total taxable interest we found from your 1099-INT,
> 1099-OID, and other interest sources for the year, after subtracting any
> nominee, accrued-interest, or bond-premium adjustments you told us about. It
> doesn't include tax-exempt interest (like from municipal bonds), and it only
> reflects the specific interest documents and adjustment categories
> you've marked as fully entered — tap any part of this number to see which
> categories those are.

The added clause ("tap any part... to see which categories those are") repairs
a defect Track 0's version does not name: the draft answer asserts a summary
("the specific interest documents and adjustments you've confirmed as
complete") without asserting that the summary is inspectable. From this
artifact alone, I can confirm the underlying data to make that clause true
*exists* (the finding's `pins` array enumerates each family's closure
assertion by id), but I cannot confirm from the artifact that any rendering
surface actually exposes it to the reader in named form — `pinLabels` is
empty and the closure pin ids (e.g. `demo.md.closure.int-b1`) are not
resolvable to a human label anywhere in this document. A two-sentence answer
that implies inspectability without the artifact demonstrating inspectability
is, from my lens, the sharper defect than any wording nuance in the original.

---

## 3. What an intelligent casual user could still misunderstand

- **That the five "citation" pins shown for line 2b are the actual audit
  trail.** They are not the same set as the finding's own thirty-nine-entry
  `pins` array (verified below, section 4) — they are a *different*, narrower
  set (recursively-resolved raw source leaves), and none of the five resolve
  to a human label. A user who clicks through expecting to see "your 1099-INT
  from Bank X" would instead see a bare id like `demo.md.finding.1099int@v1`
  with no further explanation available from this document alone.
- **That "$1825" and "the seven-family composition" describe the same
  computation vintage as everything else on the page.** The same presentation
  document also renders `line-11` (AGI) and `line-12` (deductions, published
  at `$15000`) under form-field ids (`tax.us.2025.form1040.line-11`,
  `tax.us.2025.form1040.line-12`) that do not exist at all in the currently
  selected core package (v33) — see section 4. A user reading top to bottom
  has no way to know that some rows on their own review screen are
  structurally retired relative to what the product currently computes, while
  the line-2b row they are asking about is not.
- **That an empty `pinLabels` map means something is broken.** It does not
  necessarily; the generator code treats an absent evidence label as a
  legitimate state for a directly-attested finding with no scanned document
  behind it (section 4). A user or reviewer who assumes "empty labels = data
  loss" would misdiagnose a normal state as an error.
- **Track 0's open question 4, answered directly:** given that the row's
  top-level metadata does not name the adopted package while the nested
  finding does, and given that referenced finding/pin ids do not resolve to
  committed files, how much of the provenance chain is recoverable without
  external context? Answer, from this fixture alone: the *direct one-hop*
  lineage (rule id+version, composition id+version, citation id+version,
  which named closures were asserted) is fully recoverable by reading the
  `pins` array on the finding. The *evidentiary* leaves (what document backs
  each closure) and the *human labels* for any of it are not recoverable from
  this document; a consumer must have out-of-band access to the run's
  evidence records (not committed anywhere in this repository) to go further.
  CB-A2's pattern — "included universe knowable only by cross-referencing the
  current package, not by reading the presentation output" — is confirmed,
  and I found a second, distinct instance of the same pattern below (the
  retired line-11/line-12 form-field ids) that is not about an *added*
  family but a *removed* one.

---

## 4. Deepest thread

**Thread:** does the fixture's staleness relative to the currently selected
package (v15 adopted vs. v33 current, per the charter and Track 0) go beyond
"a family was added" (CB-A2 as stated) to something that would change what a
downstream consumer can trust about the *rest of the same document*, not just
the line-2b row?

**What I opened:**
- `packages/content/tax/2025/package.core-calculations.v15.json` and
  `...v33.json` — compared `members` lists programmatically (165 members in
  v15, 363 in v33; also confirmed v33 adds a top-level `conflict_semantics`
  key absent from v15, a schema-level difference beyond membership count).
- Diffed member-id sets: 203 ids added between v15 and v33, but also **5 ids
  removed**, not merely superseded in place:
  `tax.us.2025.form1040.line-11`, `tax.us.2025.citation.form1040.line-11`,
  `tax.us.2025.form1040.line-12`, `tax.us.2025.citation.form1040.line-12`,
  `tax.us.2025.rule.form1040-line12`.
- Confirmed the line-2b chain itself is unaffected: `tax.us.2025.rule.
  form1040-line2b` (v4), `tax.us.2025.interest-composition` (v4),
  `tax.us.2025.rule.attachment.schedule-b` (v4), and `tax.us.2025.form1040.
  line-2b` (v5) are all present, identically versioned, in both v15 and v33.
  This matches Track 0's claim and I found nothing that contradicts it.
- Confirmed the *replacement* structure in v33: `tax.us.2025.form1040.
  line-11a`, `line-11b`, and `line-12e` now exist where plain `line-11` and
  `line-12` used to (consistent with the "line-12e succession" work visible
  in this repository's commit history, though I did not need to read that
  history to verify the package content itself).
- Re-opened the committed presentation model fixture and confirmed its
  `line-11` and `line-12` sections are present, rendered, and — for
  `line-12` — carry a `published_value` of `15000`, pinned to
  `tax.us.2025.package.core-calculations` role `adoption` version `v15`,
  exactly like line-2b's own adoption pin.
- Read `packages/derivation/presentation_projection.py` (`_resolve_field_row`,
  `_raw_leaves`, `_leaf_pins`, `_evidence_label`, lines ~130–265) to confirm
  what `citationSites` and `pinLabels` are *designed* to contain, rather than
  guessing from the fixture alone. Finding: `citationSites` pin ids are
  deliberately the recursively-resolved raw *source* leaves (non-closure),
  a different set by design from the finding's own top-level `pins` (direct
  one-hop lineage: rule, composition, closures, package members). I confirmed
  programmatically that line-2b's five `citationSites` pin ids and its
  finding's thirty-nine `pins` ids have **zero overlap** — expected given the
  code, but not obvious from reading the fixture alone. I also confirmed
  `_evidence_label` explicitly treats an absent label as legitimate ("no
  invented text") for a directly-attested finding with no evidence
  reference — so `pinLabels: {}` for this fixture is consistent with the
  generator's normal behavior, not necessarily proof of a stale or broken
  export. I could not settle *which* of those two explanations applies here,
  because the run's evidence-lifecycle records are not committed content
  (see section 5).

**What this changed:** it did not change my answer to line-2b itself — the
line-2b chain is confirmed unaffected across v15→v33, same as Track 0 found.
It changed the *boundary* of what I would tell a downstream consumer about
trusting the rest of the document. "The fixture is 18 versions behind" is
true but, read narrowly, invites the inference that the drift is purely
additive (new families appearing, old ones untouched) — CB-A2's own framing.
What I found is that the drift also includes **outright removal and
restructuring** of members two rows away from the one being asked about, on
the very same page. A consumer who trusts "well, line-2b's own chain is
unchanged, so this whole document is basically current" is making an
inference the artifact does not support family-by-family; each row's staleness
has to be checked independently, and this document gives no signal — no
version marker, no staleness flag, nothing beyond the buried `v15` adoption
pin — that would let a reader know line-11 and line-12 are, structurally,
retired concepts while line-2b is current.

---

## 5. Where the explanation terminates

I stop at the following evidence, and name what lies beyond it:

- **The direct lineage is fully recoverable from the artifact.** The finding's
  `pins` array names the exact rule, composition, citation, and closure-
  assertion ids and versions that produced `1825`. I did not need anything
  outside this file to recover that layer.
- **The package member-list diff (v15 vs. v33) is fully recoverable from
  committed content**, because both package files are checked in. I stop
  short of asserting v33 is *authoritatively* "the current selected package"
  in any formal, committed-registry sense — I could not find a committed
  pointer file or index that declares a package version "current" or
  "selected." I verified v33 only as the highest-numbered
  `package.core-calculations.v*.json` file present in
  `packages/content/tax/2025/`, which is the same convention the charter and
  Track 0 both rely on. That convention is a reasonable working assumption
  but is itself something a downstream consumer cannot verify from the
  presentation artifact — or even from the package directory listing alone,
  without knowing the naming convention is load-bearing.
- **The generator code (`presentation_projection.py`) explains what
  `citationSites` and `pinLabels` are supposed to contain**, and I read that
  code, not just the fixture, to ground this account. I stop at the code as
  committed; I did not run it.
- **What I could not settle:** whether this specific fixture's empty
  `pinLabels` reflects (a) leaf findings that were genuinely attested with no
  underlying document, or (b) a fixture that was hand-authored or generated
  by an earlier version of the projection logic and simply never carried
  evidence records. Both are consistent with what I can see. Settling it
  would require either the original run's evidence-lifecycle state (not
  committed) or a live regeneration of this fixture against current code (a
  run — out of scope for this documentation-only unit; a stop condition I am
  naming rather than crossing).

---

## 6. Concrete actions the project could take

- **Add a per-row staleness signal.** A field on each rendered section (or at
  minimum, in `citationGroups`) that names the package version(s) whose
  members compose that specific row's chain, independent of the top-level
  `runId`/`pinLabels` metadata, so a downstream consumer does not have to
  cross-reference package files by hand to learn that `line-11`/`line-12` are
  retired relative to `line-2b` on the same page.
- **Distinguish "citation leaf" from "lineage pin" in the schema's own
  vocabulary**, or document the distinction somewhere a downstream consumer
  can find it. Right now the fact that `citationSites` and the finding's
  `pins` are disjoint by design is knowable only by reading
  `presentation_projection.py`; nothing in the presentation-model schema
  itself or the fixture states this.
- **Decide, and record somewhere committed, what "current selected package"
  means as a formal claim** — a pointer/registry file, or an explicit
  statement that "highest version number in the directory" is the intended
  convention — since two independent Track 0/Track 1 accounts have both now
  relied on that convention without a committed artifact asserting it.
- **Probe: regenerate this fixture (or an equivalent) against v33** and diff
  the resulting `pinLabels`/`citationSites` against the committed v15-adopted
  fixture, to settle the open question in section 5 about whether empty
  `pinLabels` here is a legitimate attested-only state or a staleness
  artifact. (Documentation-only work cannot do this; it is a probe for a
  future unit with run authority.)
- **UI experiment:** render the fallback path for an unresolvable citation pin
  (bare `pinId@pinVersion`) to a test user and see whether they read it as "a
  broken link," "a technical detail I can ignore," or "evidence of a bug" —
  the three readings imply different remediation priorities and none is
  obvious a priori.
- **Decision question (do not adopt):** should a presentation-model consumer
  ever be expected to resolve `finding:derived:*` or `demo.*.closure.*` ids
  without a companion evidence/label export, or is the current design (raw
  ids visible, human labels optional) an accepted terminus for this schema
  version? This is a schema-scope question; I am recording it, not answering
  it.

---

## 7. Threads deliberately discarded

- **Whether the seven-family composition is the right tax universe.** Not my
  lens; Lens B's territory. I did not evaluate it beyond confirming (Hop 4/5
  in Track 0, which I spot-checked against
  `packages/content/tax/2025/interest-composition.v4.json` and found
  consistent) that the composition's own `claim` field states its scope
  explicitly, which is itself a provenance-recoverable fact regardless of
  whether the scope is tax-correct.
- **Whether closure-claim language would mislead a user about completeness.**
  Legal/epistemic territory (CB-A1), not a provenance-recoverability question.
  I noticed the closure claims exist and are inspectable per-family from the
  `pins` array, which is as far as my lens needs to go; whether their wording
  is safe to surface verbatim is a different account's question.
- **Whether the `activeCodes` vocabulary on blocked dispositions
  (`DEPENDENCY_ABSENT`, `SOURCE_SET_UNCLOSED`, etc.) is itself sufficiently
  granular for CB-N1's "name the specific missing family" case.** I opened
  the `line-2b` field's `blocked` disposition text and confirmed it is
  generic (not family-specific), matching what Track 0 already reported (its
  SC-3 reference in `actionable-considerations.md`, which I did not open — it
  is out of my assigned path). I discarded going further because Track 0
  already named this gap and routed it to the durable register; re-deriving
  the same finding through my lens would not add a new action, only a
  restatement.
- **The Schedule D attachment's `blocked`/`DEPENDENCY_ABSENT` state visible
  elsewhere in the same fixture (`tax.us.2025.rule.attachment.schedule-d`,
  "ADR-0057/0058").** Structurally interesting (another same-document
  vintage question) but not connected to line 2b's support chain in any way
  I could trace without opening ADR text, which the charter's stop conditions
  reserve for Foreman/advisor consultation, not this unit.
- **Whether the `demo.cgd.t2.finding.rounding` pin id's reuse across five
  unrelated lines (`line-1a`, `line-2b`, `line-3a`, `line-3b`,
  `line-sch-d-13`) indicates something about fixture construction quality.**
  I noticed this while diffing citation pin sets and considered it as a
  possible second deep thread, but discarded it: it is fully explained by the
  generator code I already read (a shared "rounding" evidence assertion can
  legitimately back multiple unrelated derived findings if the underlying
  run reused one synthetic input across categories), and pursuing it further
  would not change any answer or surface a new actionable gap beyond what
  section 6 already proposes for citation-leaf documentation.

---

## Disclosure

While grepping the repository broadly for other uses of `citationSites` and
`pinLabels` (a repository-wide search, not a search scoped to sibling
tracks), one grep result surfaced the *filename*
`docs/phases/claim-boundary-exploration/inquiries/track-1-lens-a-casual-reader.md`
in a match list. I did not open, read, or otherwise inspect its contents — I
recognized the path as a sibling's file from the filename alone and excluded
it from further reads. Reporting this per the charter's honor rule even
though no content was seen.

No other stop condition was hit. This account required no engine run, no
artifact generation, no fixture modification, and no interpretation of
`docs/governance/`. Where a thread would have required an ADR, a schema
change, or a governance reading to go further, it is recorded as a decision
question in section 6 and not adopted.
