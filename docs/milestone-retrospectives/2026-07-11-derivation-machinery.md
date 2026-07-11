# Retrospective — Derivation Machinery

- Milestone: Derivation Machinery (Foundation phase)
- Branch: `milestone/derivation-machinery`
- Merge commit: `e1608bf` (non-ff into `main`, 2026-07-11)

## Shipped

Derivation is executable without tax meaning living in code. An adopted,
versioned rule package is evaluated over published schemas and an
operation-semantics canon; derived values become `derived-finding.v1` citizens
published through `derived-publication` acts with role-bearing pins; runs are
bounded by paired records; and any derived value explains itself by walking its
pins. Six tracks:

1. **Language schemas + canon** — the ADR-0006 grammar as published, enforced
   schemas with per-operation required-field constraints (the it2
   schema-never-loaded defect), one role vocabulary across all positions, and
   versioned `round`/`range_lookup`/`bracket_fold` canon.
2. **Package contract** — closed-manifest validation as a contained outcome:
   scope-as-content, reference closure, unique output ownership; the it2 attack
   corpus rerun as tests.
3. **Records + gate** — the ADR-0008 append-only record stream, adoption gate,
   paired started/closing records, crash-window recovery.
4. **Saturation runner** — eligibility, saturation, publication with pins from
   versioned inputs, the absent/invalid/closure blocking vocabulary, two-layer
   source-set closure.
5. **Purity + portability** — a second demand-driven runner proving byte-equal
   findings; sealed-execution and deletion-attribution checks.
6. **Explanation + CLI** — a pin-graph explanation walker, the `derive` runner,
   and subprocess goldens.

All eight `evaluation-analysis.md` §5 ratification conditions discharged with
cited tests (see the milestone plan's entry-checklist table); §5.6 form-field
/fact-type families deferred to First Tax Slice as planned.

## Verification

- `python3 -m unittest` → 168 passed (72 new derivation tests).
- `python3 -m mypy` → clean, 47 source files, strict.
- `python3 tools/governance_lint.py` → conformant.
- `python3 -m packages.derivation.runners.derive --scenario …/first_slice/scenario.json`
  → derives line1a=42000, line9=42000, line16=1559 with explanation trees.
- Data safety: fixtures synthetic; scans for absolute paths and private markers
  clean.

## Decisions

- **ADR-0009 (Tier 3, ratified as amended)** — derived-finding shape. Building
  the runner forced the derived-finding authority question; per the reserved-
  entry guardrail it was surfaced, not improvised. A derived finding is its own
  citizen (`derived-finding.v1`: symbol/value/pins, no human basis); its
  authority is the attribution chain the pins carry (the Ontology recorded-
  instrument framing), which is defined doctrine, not the reserved T1 entry.
- **Tier 2 (under ADR-0009 decision 2)** — `act-derived-publication.v1` carries
  a `derived-finding.v1`, and the ADR-0007 lineage pins live on that embedded
  finding rather than being duplicated on the act. The kernel `finding.v1` is
  untouched; human and machine findings are distinct citizen families.
- **Tier 1** — self-declaring `schema` field (not the prototype's
  `schema_version`) for kernel consistency; blocked *codes* are the evaluator's
  runtime category (DEPENDENCY_ABSENT / _INVALID / SOURCE_SET_UNCLOSED /
  LOOKUP_MISS), giving decision-8's distinguishing vocabulary; the second runner
  shares the pure evaluator and per-rule step and differs only in scheduling
  (portability is about order/serialization independence, not re-deriving
  arithmetic).

## Deviations

- **Track 4 pause.** The runner was blocked mid-build pending ADR-0009 and
  resumed after ratification. The pause was the reserved-entry guardrail working
  as designed.
- **Schema amendment to a committed Track-1 artifact.** ADR-0009 decision 2
  repointed `act-derived-publication.v1` from `finding.v1` to
  `derived-finding.v1` after Track 1 had shipped it; the manifest was
  regenerated (in-milestone settling, schema unmerged/unadopted). Committed
  separately (`c9f6161`) with rationale.
- **Kernel act-log envelope persistence not wired (incomplete Track-4 edge).**
  The runner produces validated `derived-publication` act *payloads* and
  persists completion *records* to the record stream, but publication acts are
  not yet appended as `act.v1` envelopes into the kernel act log. ADR-0008 puts
  publication acts in the act log; doing so needs a registry spanning both the
  kernel and derivation act schemas (a combined-registry choice). Deferred and
  listed as a follow-up rather than improvised — no §5 ratification condition
  depends on it, but the plan listed "act-log integration" and this edge is
  unfinished.

## Data safety

Committed content is synthetic and publishable: demo ids, no real documents, no
personal facts, no absolute machine paths. Scans over the new schema/canon/
fixture trees are clean.

## Follow-ups

- **Act-log envelope persistence** for publication acts (combined registry over
  kernel + derivation act schemas). Likely a small Tier-2 ADR on registry scope.
- **§5.6 form-field/fact-type citizen families** — First Tax Slice, against real
  content (already a carried obligation in `first-tax-slice-inputs.md`).
- **Real-content portability re-proof and full canon corpora** — the prototype
  tables were fixture-minimal by design; production adoption needs the real
  table/bracket corpora and a portability re-proof at scale (§5.2/§5.4).
- **Currency/displacement** must fold `derived-finding.v1` into the derivation-
  edge graph (kernel `currency.py`) in a later track.

## Planning lessons

- **The Payload Instantiation Gate (now in `PROJECT_PLANNING.md`) is the direct
  lesson.** The ADR-0009 fork was latent when Track 1 pointed the publication
  act at `finding.v1` with no worked derived-finding instance; a single hand-
  written instance would have hit the un-suppliable `basis` at planning time,
  and the ADR would have been written before the runner was attempted.
- **Surface reserved-boundary decisions at the cheapest point.** The pause cost
  a half-built runner; instantiation would have cost a paragraph. Same decision,
  earlier and cheaper.
- **Plan line-items deserve their own instantiation check too.** "Act-log
  integration" read as a one-liner in the Track 4 plan but hid a combined-
  registry decision; naming a concrete first act envelope during planning would
  have exposed it.
