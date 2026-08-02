# Covered Long-Term Gains, Schedule D Line 8a — Track 1 Builder Charter

Audience: Builder.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** `main` at
  `ad2683b716d8dfbbbbef573539cddca002770792` (ADR-0052 and its complete
  evidence chain are on `main`).
- **Exact object or commit range:** build on
  `track/schedule-d-covered-ltcg-8a-track1`, starting from the source commit
  above. The Track-1 review range will be `main..HEAD`.
- **Role:** one Builder, Medium tier / medium effort. This is production
  reimplementation from an accepted contract, not a new design round and not
  a review.
- **Scope and evidence-rung ceiling:** implement only Track 1's versioned
  schema/content citizens and their contract evidence — ADR-0052 Decision 1
  (transaction source family and identity) and Decision 2 (the nine-part
  completeness boundary, including the adopted P2-S5A box-2a-closed
  successor). The ceiling is schema/content publication plus validation: no
  evaluator, coordinator, contribution-admission, Schedule D content, QDCG/
  line-16 binding, package-successor, presentation, or real-data behavior.
- **Stop conditions:** stop and report if an accepted historical schema,
  manifest entry, content version, checksum, or ADR (including ADR-0036 or
  ADR-0050) would need mutation; if a fully resolved positive instance
  cannot be written honestly; if the work requires interpreting governance
  text, a new generic substrate, runtime evaluator/coordinator behavior, or
  any citizen not assigned below; or if any real value, identity, document,
  disposition, reason, workspace location, or generated private artifact
  would be needed.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md`
  (Supported Source Class, Completeness Boundary, and Contracts sections);
  `docs/adr/0052-covered-long-term-gains-schedule-d-line-8a.md` (Decisions 1
  and 2 specifically); `docs/adr/0015-1099-int-statement-instance-identity.md`;
  `docs/adr/0016-source-family-claim-and-composition.md`;
  `docs/adr/0010-derived-finding-projection-and-currency.md`;
  `docs/adr/0023-member-assertion-and-transition-boundaries.md`;
  `docs/adr/0011-tax-fact-identity-and-source-closure.md`;
  `packages/schemas/derivation/source-family.v1.schema.json`;
  `packages/schemas/derivation/source-closure-mapping.v2.schema.json`;
  `packages/content/tax/2025/family.f1099div-2a.json` and
  `closure-mapping.f1099div-2a.json` (the closest existing single-level
  identity/closure pattern to imitate at the anchor level);
  `packages/content/tax/2025/family.form1065-k1-box5.json` and its closure
  mapping (a nested-composition precedent to compare against, though this
  track's identity is an *independent* family, not nested — see ADR-0052
  Decision 1);
  `packages/content/tax/2025/rule.schedule-d-required.conclusion.json` and
  `schedule-d-required.conclusion-binding.json` (the existing categorical
  `{yes, no}` declared-fact pattern this track's seven absence declarations
  follow); `packages/tax/loader.py`;
  `AGENTS.md#Schema Publication Protocol`; `AGENTS.md#Fixture Rules`; and
  `AGENTS.md#Data Safety Rules`.

Before editing, echo the resolved source commit, the Track-1 scope and
evidence ceiling, the immutable-history constraint, and every stop
condition.

## Goal

Publish the versioned identity, family, closure, and completeness-boundary
citizens that ADR-0052 requires before any Schedule D content or downstream
computation can be built.

## Deliverables

1. **Statement anchor.** Add a content citizen for the 2025 Form 1099-B
   statement anchor fact: identity `(tax-year, subject, broker-ref,
   logical-statement-ref)`, per ADR-0052 Decision 1. Evidence, file, upload,
   scan, and document identifiers must not enter the identity — reject them
   at schema level where the existing pattern supports it.
2. **Eligible transaction source family.** Add a new, independent
   return-level source family and its closure mapping for the covered,
   long-term, gain-only eligible transaction member, per ADR-0052 Decision
   1: member identity `(tax-year, subject, statement-anchor-ref,
   logical-transaction-ref)`, pinning the current anchor finding. The member
   fact type must carry the canonical eligible-transaction predicate fields
   as contributed/attested assertions — covered security, basis reported to
   the IRS, broker-reported long-term classification, no box-1f market
   discount, no box-1g wash-sale adjustment, Ordinary not indicated, QOF not
   indicated, no taxpayer-side adjustment, no collectibles/special-rate
   treatment, and gain-only classification — never a derived
   proceeds-minus-basis comparison. Closure authorizes the multi-transaction,
   multi-anchor sum; closed-empty authorizes subtotal 0. This track
   publishes the family/closure/member citizens only; it does not publish a
   subtotal-consuming rule (that is Track 2).
3. **Seven completeness absence declarations.** Add seven versioned
   categorical `{yes, no}` fact types, one per ADR-0052 Decision 2's
   independent absence declaration: no short-term transactions, no current
   capital losses, no inbound capital-loss carryovers, no Form 8949
   transactions or adjustments, no other Schedule D sources (K-1 gains,
   Forms 2439/4684/4797/6252/6781/8824), no lines-18/19 special-rate
   sources, and no Form 1099-DA or QOF flow. Each has no default, free
   supersession, and presence-before-value semantics, keyed by tax year and
   subject, following the existing `schedule-d-required` C1-C4 declared-fact
   pattern. Do not add a synthesizing conclusion citizen — ADR-0052 Decision
   2 reads all nine authorities (these seven plus the two closures) directly;
   this track publishes only the seven declaration citizens, not a rule that
   reads them.
4. **P2-S5A box-2a-closed successor citation.** Nothing new to publish for
   the box-2a family itself (it is accepted history, ADR-0050) — but add the
   citation citizen(s) needed for Decision 2's adopted successor sentence
   (box-2a must be closed, not closed-empty) and Schedule D line 13's future
   consumption of it, if the milestone plan's citation grounding requires a
   new pin at this track. If no new citation is needed at this track (the
   consuming rule is Track 2's work), state that explicitly rather than
   inventing one.
5. **Publication evidence.** Add every new schema version to its registry
   using `packages.kernel.schema_registry.write_manifest`; the manifest diff
   may only add unused filenames. For every new schema that carries or
   references a payload, commit one hand-written, fully resolved, obviously
   synthetic positive instance (the Payload Instantiation Gate). Add named
   negatives for the load-bearing constraints, including: evidence/file/
   document identifiers substituted for anchor or transaction identity; two
   sales from one anchor collapsing to one member; non-`{yes,no}` domain on
   any of the seven declarations; and a member admitted without every
   required predicate field present.
6. **Contract tests.** Add a focused Track-1 test module covering every
   positive instance and named negative, exact identity/family/closure
   pins, correction preserving one transaction's identity while a sibling
   is unaffected, multi-anchor sums, historical-byte immutability (ADR-0036,
   ADR-0050, and every existing schema/content citizen untouched), and
   manifest additions. Tests must validate content through the same
   loader/registry surface production uses where that surface already
   exists.

## Boundary

No Schedule D content citizen (line 8a/13/15/16 or the attachment); no
`selected-preferential-base` symbol or its producer rules; no Form 1040
line 7a/7b/9 or line-16 successor; no admission interlock, package
successor, coordinator, evaluator, marshaller, resolver, presentation,
browser, README, coverage-frontier, or retrospective change. Do not copy
prototype code (`prototypes/schedule-d-covered-ltcg-8a/it2/design.md` etc.)
into production — reimplement each citizen against ADR-0052 and established
accepted patterns. Do not edit any accepted ADR or published historical
file.

## Verification before handoff

Run the focused modules while iterating:

```text
python3 -m unittest tests.test_schedule_d_covered_ltcg_8a_t1_citizens
python3 -m unittest tests.test_schema_registry
git diff --check main..HEAD
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

If a touched established loader/content test module exists, run that module
once and report it. Do not repeatedly run the full suite; CI `verify` is the
gate of record.

## Handoff

Commit the complete Track-1 implementation as one implementation commit
after this charter commit. Leave the worktree clean and report the commit
SHA, exact files changed, focused command results, manifest-diff inspection,
and any charter-stop finding. Do not review the work, open or merge a PR,
begin Track 2, or modify the charter/pointers. The foreman will take
custody and charter an author-independent Track-1 review.
