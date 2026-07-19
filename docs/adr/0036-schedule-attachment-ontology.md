# ADR 0036 — Schedule Attachment Ontology

- Status: **accepted** (owner ratification 2026-07-19, Tier 3)
- Tier: 3
- Date: 2026-07-19

## Context

Schedule B is the first form whose *existence* the product computes:
required when taxable interest or ordinary dividends exceed $1,500, carrying
payer itemizations (Parts I/II) derived from statement facts on record and
taxpayer answers (Part III) contributed as facts. Nothing in the ontology
could represent a form's existence, completeness, or where *its*
incompleteness blocks. Owner directions bind: all of Schedule B in scope
(FinCEN 114 named, never produced); dependency-form completeness (no
structurally born-blocked attachment); honest blocking for factual
incompleteness only.

Prototype evidence: `docs/prototypes/attachment-ontology/` — plan, two
sealed builders, independent governance (Medium) and adversary (High)
reviews with a split verdict, a foreman synthesis of reviewer-checked
elements, and — per the ADR-0013 2026-07-15 amendment — an independent
confirmation pass that returned NOT-CONFIRMED on the first synthesis and
**CONFIRMED-WITH-CONDITIONS** on the owner-approved bounded revision
(`reviews/confirmation-r1.md`, both rounds). The confirmed synthesis
(`synthesis.md`) is the shape ratified here.

## Decision

1. **The attachment citizen.** A schedule attachment is a derived finding
   published by a declared attachment rule, with three states as **atomic
   dispositions on the ratified triad** (no embedded state field):
   *not-required* publishes a walkable inapplicability disposition (inputs,
   threshold, citation, per-trigger outcome — never silence);
   *required-and-complete* publishes the whole form content, pinned to
   every consumed fact; *required-and-incomplete* blocks with the standard
   non-publication walk naming each missing contributable fact. Sibling
   line rules cannot reference the attachment symbol, so an attachment's
   block cannot propagate to a line (verified against committed runner
   source in review).

2. **The requirement conditional is declared rule content** over existing
   subtotals (interest 2b-side, ordinary dividends 3b-side for Schedule B),
   with citation; boundary semantics are strictly-greater-than the cited
   threshold parameter (exactly $1,500 is not over).

3. **Itemization rows.** The generic surface fixes only: rows pin the
   member findings of the same closed family, at the same horizon, that
   the line's subtotal collected (via `collect_members`, a named new
   mechanism); rows subtotal; the subtotal ties to a named line. Row
   *shape* (Schedule B's payer + amount) is per-schedule content, not
   ontology. The tie-out — row-sum equals the line's published value — is
   a **new named invariant** (`ITEMIZATION_TIE_OUT_VIOLATION`): a
   derivation-time check whose violation hard-fails the attachment
   derivation only — never publishes a divergent form, never blocks the
   line. It is stated here as unbuilt contract text (confirmation round 1
   established no committed path expresses it).

4. **Completeness is presence-semantics with pinned encoding.** Part III
   answers are categorical declared facts on the existing
   taxpayer-assertion pattern — value domain `{yes, no}`, never boolean.
   Completeness is: every required answer *exists as a current finding*,
   checked independently per answer before any value is read (a "no" is a
   present answer; no evaluation order can mask an answer). Branch content
   requirements read values only after presence holds: a "yes" on
   foreign-account adds 7b country to the required set and *names* the
   FinCEN-114 obligation; a "yes" on foreign-trust likewise. Every answer
   finding is pinned unconditionally, whatever its value, so supersession
   has an input edge in both directions (a superseded answer displaces the
   attachment to non-current; a late answer supersedes the blocked
   disposition by re-run, never edit).

5. **Generalization is load-bearing.** The citizen surface carries no
   Schedule-B-specific field, trigger shape, or completeness structure;
   both builders and the confirmation pass demonstrated the shape on a
   Schedule D stub without modification. A future schedule instantiates
   this ADR with content only.

## Production conditions (owed to Tracks 1–3; never allowlisted)

1. **Tie-out invariant:** `ITEMIZATION_TIE_OUT_VIOLATION` added to the
   record and walk vocabularies by versioned schema change; the
   derivation-time check built with both named kill-tests (stale row set,
   stale line); violation fails the attachment only.
2. **Presence-not-truthiness:** the completeness expression checks each
   required answer's presence independently of every other answer's value;
   the categorical `{yes, no}` domain pin is load-bearing — package
   validation must reject a boolean or otherwise falsy-valued Part III
   answer fact type on an attachment.
3. **Emit/record error-vocabulary reconciliation:** the pre-existing
   discrepancy — the runner emits `SOURCE_SET_UNCLOSED` while committed
   record/walk enums permit `SOURCE_SET_OPEN` (adversary A6, confirmed
   against source) — is reconciled by versioned schema change **in Track 1**
   (owner disposition at ratification, 2026-07-19: repair in-milestone
   because Track 1 already versions the same vocabularies and this
   milestone's goldens would otherwise pin the inconsistency; a standalone
   track would have been the disposition had it not impacted scope). This
   ADR takes no position the reconciliation could invert.
4. **`collect_members`** as a named new mechanism (same-family same-horizon
   member collection with per-row pins).
5. The milestone plan's coordinator-from-facts golden classes for the
   attachment (both existence outcomes, the complete form, both Part III
   branches, the honest block).

## Consequences

- Every future schedule (D, 1, 2, 3…) inherits the citizen shape; adding
  one is content plus this ADR's mechanisms, not new ontology.
- The product can now be *honestly incomplete at form granularity*: line
  values publish while a required attachment blocks, each with its own
  walkable account — the owner's dependency-form-completeness and
  factual-incompleteness rulings made structural.
- The FinCEN-114 obligation is representable as a named non-produced
  obligation — a pattern for future out-of-return filings.

## Alternatives Considered

- **State-in-value-field disposition (rival it2):** one `published`
  disposition with an embedded state discriminator. Rejected: breaks
  ADR-0012 atomicity (governance G1).
- **`choose`-chain completeness (incumbent it1):** rejected: masked one
  Part III answer behind another — a required-incomplete form published
  whole (adversary, decision-blocking); its divergence guard also rested
  on a misapplied citation.
- **Boolean Part III answers with `all(...)`:** rejected by confirmation
  round 1: falsy-value short-circuit recreates the masking hole; the
  categorical domain pin is the repair.
- **Tie-out via committed error vocabulary:** rejected by confirmation
  round 1: no committed path expresses it; honestly stated as new
  contract.

## Links

- Prototype evidence: `docs/prototypes/attachment-ontology/` (synthesis.md
  is the confirmed shape; reviews/ carries the full chain including the
  NOT-CONFIRMED round — retained per governance, never deleted)
- Builds on: ADR-0012 (form fields), 0019/0024/0025 (conditionals),
  0020/0029 (explanations, citations), 0014–0017 (families, closure),
  0010 (currency), 0032 (contribution), 0035 (dividend composition)
- Consumed by: milestone Tracks 1–3 (schemas, machinery, content), D2
  (shares the taxpayer-assertion pattern for declared-absence facts)
