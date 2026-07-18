# Charter: Track 1 — D3 schema-additions pre-merge re-review

Date: 2026-07-17. Owner-launched, **author-independent** reviewer (must not be the
seat that implemented the D3 additions). Focused re-review gating the merge of
**PR #8** after the 2026-07-17 Track 1 scope amendment (PR #9, merged).

Scope of review: **only the D3 schema-citizen delta** on
`track/frrs-t1-boundary-contribution-schemas` — the change from the
previously-reviewed point `109defb` (D1/D2 scope, verdict merge-ready) to current
HEAD. The D1/D2 citizens were already reviewed in
`2026-07-17-frrs-t1-premerge-review.md` and are **not** re-opened here except where
the D3 additions touch shared files (the generator, the manifest, the Track-1
test, `published.json`).

Read: the entry chain, the milestone plan's amended **Track 1** section, ADR-0033
(esp. Decision 1), the implementation charter
`charter-2026-07-17-frrs-t1-d3-schema-additions.md`, and the prior review record.

## Check

1. **Schema fidelity to ADR-0033 Decision 1.**
   - `release-registry.v1`: immutable identity includes the SHA-256 of the exact
     package registry document it attests; per-citizen-registry SHA-256s modeled
     where split. No invented fields.
   - `act-package-adoption.v1`: pins exact package `{id, version, checksum}` **and**
     release `{id, version, checksum}`, structured scope, revision, optional
     same-scope supersession, non-authoritative audit metadata.
2. **The payload-vs-envelope actor decision.** The implementer placed the "user
   actor" on the `act.v1` envelope (mirroring `act-contribution.v1`/`act-assertion.v2`)
   and left sole-current-user-in-scope selection to Track-3 admission. Judge
   whether that is faithful to the committed act convention and ADR-0033 (which
   describes the act as *pinning* the user actor) — or whether the payload must
   itself carry/constrain the actor. This is the single most contestable choice.
3. **Registry rows + integrity.** Each new schema has a `published.json` row whose
   sha256 equals the schema-file bytes; the registry loads without a mutation or
   unlisted-file error.
4. **Examples, negatives, byte-regeneration.** The two positive examples validate;
   the two named negatives reject for the **right** constraint (missing release;
   missing package-registry sha) — not merely because a declared schema can't be
   found; the generator renders the corpus deterministically and the
   provenance-manifest lists every artifact with a matching sha256
   (`test_fixture_corpus_is_regenerated_from_its_public_pins` green); positive/
   negative counts track `NEW_SCHEMAS` (12).
5. **Scope fence.** No resolver runtime, no wiring into a production registry or
   loader, no ADR edits; only schemas, examples, negatives, registry rows, the
   generator, the manifest, and the test changed.
6. **Synthetic-only data.** No personal path or value; all identifiers `demo.*`;
   checksums are synthetic 64-hex literals.
7. **Verification.** Full suite, `mypy packages tools tests`, `governance_lint.py`,
   and the data-safety scan green (re-run and reported).

## Output and constraints

Do not redesign the ratified ADR-0033 contract or authorize runtime behavior.
Classify each finding as **blocking**, **scope defect**, **production condition**,
or **non-blocking**. Produce exactly one review record:
`docs/reviews/2026-07-17-frrs-t1-d3-schemas-rereview.md`. Do not modify
implementation files, run git write commands, commit, or merge. Stop after the
review record is complete.
