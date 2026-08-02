# Covered Long-Term Gains, Schedule D Line 8a — Track 2 Production Builder Charter

Audience: Builder.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** `main-engine` at
  `ec738499d1d8e25634ac5414c3e709829dbc00ac` (ADR-0052, Track 1, and
  ADR-0053 are all on `main-engine`; the ratified line is `main-engine`,
  not `main`, as of PR #145). CI `verify` completed successfully on this
  commit before the owner merge.
- **Exact object or commit range:**
  `track/schedule-d-covered-ltcg-8a-track2`, created directly from
  `ec738499d1d8e25634ac5414c3e709829dbc00ac`. Do not continue building on
  the spent Track-1 branch.
- **Role:** one Builder, High tier / high effort. This is a contract-dense
  production integration track, not a prototype or review.
- **Scope and evidence-rung ceiling:** implement ADR-0052 Decisions 3-7 and
  ADR-0053's two resolutions (the `attachment-rule.v3` categorical
  requirement shape and the single-rule/internal-`choose` selected-
  preferential-base pattern): Schedule D content, the selected
  preferential-base rule, line 7a/9/16 successors, package successor,
  admission/package interlocks, coordinator integration, lifecycle
  behavior, and authoritative synthetic goldens. Production-shaped
  synthetic integration is the ceiling. No presentation/browser or
  real-data work.
- **Stop conditions:** stop and report if `main-engine` at the SHA above is
  not what CI verified; if an accepted historical schema/content/package/
  ADR (including ADR-0036, ADR-0050, ADR-0052, ADR-0053, or any Track-1
  citizen) would need mutation; if a new evaluator operation or generic
  substrate beyond `choose`/`require_closed`/`collect`/`all`/`any`/
  `categorical_compare` appears necessary; if the accepted pin topology
  cannot be represented by existing declared machinery; if short-term
  transactions, losses, carryovers, Form 8949, other Schedule D sources,
  UI redesign, or Track-3 presentation becomes necessary; or if any
  real/private material would be needed.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md`
  (Contracts, Fixtures, Verification sections);
  `docs/adr/0052-covered-long-term-gains-schedule-d-line-8a.md` (Decisions
  3 through 7 specifically); `docs/adr/0053-covered-ltcg-schedule-d-attachment-and-producer-substrate.md`;
  ADR-0010, ADR-0011, ADR-0012, ADR-0020, ADR-0023, ADR-0027, ADR-0029,
  ADR-0032, ADR-0036, ADR-0038, and ADR-0050 only where the implementation
  turns on their exact accepted text; every Track-1 production citizen
  (`family.f1099b-covered-ltcg.json`, `closure-mapping.f1099b-covered-ltcg.json`,
  `f1099b-covered-ltcg.bundle.json`, `schedule-d-boundary.bundle.json`);
  `packages/schemas/tax/attachment-rule.v2.schema.json` (the schema this
  track's v3 successor extends);
  `packages/content/tax/2025/rule.attachment.schedule-b.v3.json` (the
  closest existing attachment-rule.v2 instantiation to imitate for
  itemization/tie-out shape);
  `packages/content/tax/2025/rule.form1040-line7a.json`,
  `rule.form1040-line7b.json`, `rule.form1040-line9.v3.json`,
  `rule.form1040-line16.v3.json`, `qdcg.bundle.json`;
  `packages/content/tax/2025/package.core-calculations.v10.json`,
  `published-packages.v5.json`;
  `packages/content/tax/2025/schedule-d-required.conclusion-binding.json`
  and `rule.schedule-d-required.conclusion.json` (ADR-0050's C1-C4 checked
  conclusion, the direct-route input this track's selected-preferential-base
  rule pins); `packages/derivation/evaluator.py` (the `choose`,
  `require_closed`, and `collect` operators this track's central rule
  uses); `packages/derivation/live.py`; `packages/derivation/runner.py`;
  `packages/derivation/marshal.py`; `packages/derivation/package_validation.py`;
  `packages/tax/loader.py`; `packages/kernel/schema_registry.py`;
  `tests/test_schedule_d_covered_ltcg_8a_t1_citizens.py`;
  `AGENTS.md#Schema Publication Protocol`; `AGENTS.md#Fixture Rules`; and
  `AGENTS.md#Data Safety Rules`.

Before editing, echo the resolved `main-engine` SHA, the Track-2 scope and
ceiling, the immutable-history constraint, and every stop condition.

## Goal

Make the accepted class execute entirely through declared, versioned
production artifacts: the eligible transaction family and completeness
boundary (Track 1) drive a real Schedule D attachment, the selected
preferential base picks the correct producer without double-counting or
reach-around, line 7a/9/16 recompute correctly, and the correct QDCG or
ordinary tax publishes.

## Deliverables

1. **`attachment-rule.v3` schema (ADR-0053 Decision 1).** Publish an
   additive successor to `attachment-rule.v2` (unused version;
   `attachment-rule.v2` untouched, immutable history). Its `requirement`
   block becomes a `oneOf` between the existing threshold shape (unchanged)
   and a new categorical shape: `{kind: "family_nonempty", source_family:
   <pin>, citation: <pin>}`. Semantics: required when the pinned source
   family is current and closed with at least one member; not required
   when current and closed-empty; `blocked` when unclosed — never a
   silent default. Commit the schema, register it, and commit one
   hand-written positive instance (Payload Instantiation Gate) plus a
   negative for each new constraint (missing `kind` discriminant, a
   categorical requirement missing `source_family`, and a family reference
   to a nonexistent citizen).
2. **Schedule D attachment content.** Publish `attachment.schedule-d.v1`
   under `attachment-rule.v3`, instantiating ADR-0036's attachment
   ontology with content only (no ontology change): line 8a columns (d)
   proceeds sum, (e) basis sum, (h) gain sum via `collect_members` over
   Track 1's eligible-transaction family, tied out to (d)-(e); line 13
   consuming the closed box-2a subtotal (accepted history, ADR-0050) once,
   per ADR-0052 Decision 2's adopted P2-S5A successor; line 15 as line 8a
   plus line 13; line 16 equal to line 15 for this bounded gain-only slice.
   The attachment's requirement trigger uses the new categorical shape,
   pinned to Track 1's eligible-transaction family. Completeness reads all
   nine boundary authorities (Track 1's two closures plus seven
   declarations) via presence-before-value, naming every missing/violated
   authority exactly on `required-and-incomplete`.
3. **Selected preferential-base rule (ADR-0053 Decision 2).** Publish
   **one** rule citizen, `publishes:
   "tax.us.2025.schedule-d-covered-ltcg-8a.selected-preferential-base"`
   (or equivalent exact naming — state your chosen identifier and keep it
   consistent across all consumers), with a top-level `choose` keyed on
   whether the eligible long-term family is current and closed-nonempty
   (`require_closed` plus a nonempty `collect` check, the same idiom every
   existing family-gated rule uses):
   - closed-nonempty branch: requires the Schedule D attachment
     `required-and-complete` and Schedule D line 16; publishes line 16's
     value; pins the attachment and all nine boundary authorities
     transitively through it, never directly.
   - otherwise (closed-empty) branch: requires ADR-0050's checked
     conclusion and the closed box-2a subtotal; publishes the box-2a
     value (including closure-backed zero) when the conclusion is
     current `"no"`; `guard_inapplicable` when the conclusion is current
     `"yes"`; `blocked(DEPENDENCY_ABSENT)` naming the exact missing set
     otherwise.
   Do not create a second rule that also publishes this symbol — package
   validation must reject that as a duplicate producer (ADR-0027 Decision
   5), and this track's whole point is that it never needs to.
4. **Line 7a/7b/9 successors.** Publish a line-7a successor that consumes
   the selected preferential base exactly once (no other input). Line 7b
   is unchanged from the existing `rule.form1040-line7b.json` — confirm
   and cite that no new version is needed, per ADR-0052 Decision 5 ("line
   7b is never affirmatively checked on the Schedule-D route," and the
   direct-route behavior is already correct in the existing rule). Publish
   a line-9 successor that adds the new line-7a publication exactly once
   to its existing inputs (wages, taxable interest, ordinary dividends);
   never reads Schedule D line 8a/13, a family subtotal, or a raw
   transaction member directly; a blocked or guard-inapplicable line 7a
   makes line 9 `blocked(DEPENDENCY_ABSENT)` on selected line 7a.
5. **Line-16/QDCG successor.** Publish a line-16 successor identical in
   shape to the current `rule.form1040-line16.v3.json` except for the
   single substitution `selected_line7a -> selected preferential base`
   (ADR-0052 Decision 6's ledger row for Decision 7). Preserve every
   existing STOP/branch/pin behavior unchanged: `blocked`/
   `guard_inapplicable` states before `COMMON16` assembly; QDCG selected
   when `Q>0` or the selected value `>0`; ordinary tax only when both are
   closure-backed zero; the four branch-specific declaration/conclusion
   direct pins from ADR-0050 Decision 7, applied only when the selected
   value has the direct-producer signature (never when it has the
   Schedule-D-producer signature, per ADR-0052 Decision 4's exact pin
   table).
6. **Package successor.** Publish a coherent successor route:
   `package.core-calculations.v11`, `published-packages.v6`, and (if the
   milestone's synthetic adoption pattern requires it) a new demo release/
   adoption analogous to Track 1's fixtures. The v11 graph selects exactly
   one current version of: Track 1's identity/family/closure/declaration
   citizens (already on `main-engine`, unchanged), the new
   `attachment-rule.v3` schema, `attachment.schedule-d.v1`, the selected-
   preferential-base rule, and the new line 7a/9/16 successors, plus every
   unchanged existing consumer. The v10/v5 graph remains resolvable and
   compatible. Package validation must reject: a mixed graph pairing a
   current Schedule D attachment result with a displaced boundary
   authority; a raw transaction, family subtotal, or Schedule D line read
   reaching line 9 or the QDCG worksheet directly; two rules publishing
   the selected-preferential-base symbol; and a non-`{yes,no}` domain on
   any boundary declaration (already enforced by Track 1's schemas —
   confirm it survives composition, do not re-implement it).
7. **Pins, explanations, and correction currency.** Enforce ADR-0052
   Decision 7's exact pin table per producer signature without duplicating
   transitive lineage. Missing-component walks name the exact absent set.
   Forward and reverse transaction/boundary/box-2a corrections displace
   the full Schedule D → selected-preferential-base → line 7a → line 9 →
   taxable income → line 16 chain and never revive displaced history.
8. **Authoritative synthetic goldens.** Add production-shaped synthetic
   coordinator-from-facts goldens through `live_coordinate_run` from an
   act log — never a hand-built `RunContext` — for every non-presentation
   kill-test class named in ADR-0052's Decision 7 kill-test set and the
   milestone plan's Fixtures section: single/multi-broker/multi-transaction
   eligible returns; each of the nine completeness components individually
   missing or violated; box-2a present-and-nonzero alongside an eligible
   transaction (both gains preserved exactly once via line 13); box-2a
   closed-empty (Schedule-D-only route); family lifecycle states; forward
   and reverse route-transition correction with no revived history;
   historical/raw reach-around and dual-producer rejection; non-covered/
   adjustment-code exclusion (already proven at admission in Track 1 —
   confirm it propagates, do not re-litigate); and the QDCG/ordinary
   branch split for both producer signatures.

## Boundary

No presentation projection or product-page/browser work (Track 3); no real
session; no short-term transactions, losses, carryovers, Form 8949,
noncovered securities, digital assets, or other Schedule D sources; no
filing or transmission; no UI redesign; no historical migration. Do not
edit accepted ADRs (including ADR-0052/ADR-0053), published historical
schemas, manifest entries, content versions, or packages — including
`attachment-rule.v2`, ADR-0050's box-2a family, or any Track-1 citizen. Add
new unused versions and manifest rows only where a new schema is actually
necessary; a new evaluator operation or generic substrate is a stop, not
an implicit extension. Do not copy prototype code
(`prototypes/schedule-d-covered-ltcg-8a/it2/design.md` etc.) into
production — reimplement against ADR-0052, ADR-0053, and established
accepted patterns.

## Verification before handoff

Create focused Track-2 test module(s) for the attachment, the selected-
preferential-base rule, and coordinator/lifecycle/package-validation
behavior, and run each while iterating. Also run once:

```text
python3 -m unittest tests.test_schedule_d_covered_ltcg_8a_t1_citizens
python3 -m unittest tests.test_schema_registry
python3 -m unittest tests.derivation.test_package_validation
git diff --check main-engine..HEAD
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main-engine..HEAD
```

Run only touched focused modules while iterating; do not repeatedly run
the full suite. CI `verify` is the gate of record. Inspect every
intentional golden and manifest diff before handoff.

## Handoff

Commit the complete Track-2 implementation as one implementation commit
after the charter/base commit. Leave the worktree clean and report the
SHA, exact files, focused results, golden entrypoint evidence, manifest
inspection, your chosen selected-preferential-base identifier, and any
charter-stop finding. Do not review the work, push, open a PR, begin
Track 3, or modify the charter/pointers. The foreman will charter an
independent Track-2 review.
