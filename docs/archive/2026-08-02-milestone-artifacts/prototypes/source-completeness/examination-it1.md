# Examination: Iteration 1 — Incumbent Paper Design

Date: 2026-07-12. Builder seat (`roles/builder.md`), rung 1 (paper only), under
`charter-it1.md` and the approved `plan.md`. Branch
`prototypes/source-completeness/it1`; design exhibits under `it1/`.

## What was built

One incumbent paper design for SC-P1/P2/P3, grounded on the *real* artifacts,
not abstractions:

- `it1/sc-p1-mapping-design.md` — closure-to-`collect` mapping as a dedicated
  adopted citizen `source-closure-mapping.v1` + a resolver that is the sole
  writer of layer-2 `closed_sets` membership + closure-finding pin wiring.
- `it1/sc-p2-identity-design.md` — 1099-INT identity keyed by
  payer + account + tax-year; statement/document out of the key.
- `it1/sc-p3-source-family.md` — source family = (member_fact_type, scope),
  one name shared by collect node, mapping, and coverage read model.

Real seam cited: `evaluator.py:107-119` (two-layer `collect`), `runner.py:71,138`
and `runners/derive.py:31` (caller-supplied `closed_sets`), `runner.py:143-154`
(`pins_for`), `content/tax/2025/w2.bundle.json` (`tax.us.2025.w2.source-closure`
— real boolean, tax-year-keyed closure fact type), `rule.wages-line1a.json`
(`source_set:"tax.us.2025.w2"`).

## Pre-declared checks (charter §"Pre-declared checks")

1. **Every Gate 2 fixture present and fully resolved, no placeholders.** MET.
   SC-P1 (a) interest true-closure zero, (b) same shape on the real W-2 closure
   fact type, (c) false-closure block, (d) displaced-closure block, lifecycle
   trace, producer→authority→consumer→failure map — all concrete
   (`it1/sc-p1-mapping-design.md`). SC-P2 two-account distinctness, correction,
   two rejected rival keys, evidence-keyed negative, lifecycle
   (`it1/sc-p2-identity-design.md`). SC-P3 definition exercised by those
   (`it1/sc-p3-source-family.md`). No `TODO`/placeholder in any instance.
2. **Affirmative-only stated against the REAL two-layer check, not an
   abstraction.** MET as a *design statement*; see the rung finding below for
   why paper cannot fully *prove* it. The design quotes the actual
   `evaluator.py` collect body and locates enforcement at the resolver
   (`f.value is True`, single writer of L2 membership).
3. **No identity key contains an evidence or document key (Article 1).** MET.
   SC-P2 chosen key = payer + account + tax-year (citizens peer to evidence);
   the evidence/document-keyed candidate is worked as a *rejected negative*, and
   the statement-id rival is rejected partly for the same reason.
4. **The empty-source zero's explanation walk reaches the authorizing closure
   finding through pins.** MET *by design change*: today it does NOT (the
   explanation defect — `pins_for` pins no closure finding for an empty
   collect). The design adds an `AccessLog.closure_admits` set + a
   `closure-authority` pin role so the walk terminates at the closure finding.
   This is a required production change, not an existing property; disclosed.
5. **Negatives fail for the declared reasons, not incidentally.** MET.
   (c) false → `f.value is True` fails at the resolver → not admitted →
   `source_set not in closed_sets` → `BLOCK_CLOSURE`. (d) displaced → resolver
   reads only the current finding (ADR-0010); a displaced true never authorizes.
   Rival key rejections fail on the exact declared collision/correction break,
   worked in `it1/sc-p2-identity-design.md`.

## Negative results disclosed

- **The design is not free.** SC-P1 requires two real production changes:
  (i) replace the caller-supplied `RunContext.closed_sets` with a resolver over
  an adopted mapping + current closure findings; (ii) add closure-finding pins to
  `pins_for` via a new `AccessLog` field and `Environment.closure_authority`.
  Neither exists today. Stated as production conditions, not hidden.
- **No production adoption surface exists** that builds `RunContext` from current
  findings + an adopted mapping. Routed as a *separate patch/decision* (Gate 2
  note), not a charter expansion, not a rung climb.
- **Only the incumbent shape was built.** The mapping-as-adopted-parameter rival
  (closure) and the payer/statement-keyed rivals fully worked as a design are
  it2's clean-room charter. Within it1, SC-P2's rival *keys* were exercised only
  far enough to show their collisions — sufficient to reject them, not a
  substitute for the it2 rival design (ADR-0005 rivals-not-refinements).

## Per-proposition disposition

| Prop | Claim | Status | Driving question if climb |
|---|---|---|---|
| SC-P1 mapping **shape** | dedicated `source-closure-mapping.v1` citizen + resolver + closure-pin wiring | **settled at paper** | — |
| SC-P1 **affirmative-only enforcement** | only current-true admits, on the real two-layer path, no value-insensitive adapter | **needs rung 2 → 3** | *Does the resolver's `f.value is True` admission hold when a throwaway evaluator actually runs the real two-layer `collect` check — i.e. is there no adapter layer that reintroduces the it4 presence-vs-value defect?* |
| SC-P2 identity **key** | payer + account + tax-year; statement/document excluded | **settled at paper** | — (collision and correction-break are visible without code) |
| SC-P3 source **family** | (member_fact_type, scope) as one shared name | **settled at paper** | — (ratifies inside the SC-P1 ADR, not its own) |

### Why SC-P1 enforcement recommends a climb (charter §Evidence rung)

Paper settles the *shape* — where the value check must live and that the
resolver is the single writer. It cannot settle question 2 (plan Gate 3), which
is the whole reason SC-P1 scored T=2: the it4 defect was *invisible to design
intent* — the last adapter "meant" to check closure yet admitted on presence.
A paper claim "the resolver checks `is True`" has exactly that failure's shape:
sound on paper, defeatable by an intermediary. Only rung 2 (validator/resolver
mutations over the closure + mapping schemas) and then rung 3 (a throwaway
evaluator exercising a *copy* of the real two-layer check with true/false/absent/
displaced closure findings) can show no adapter is needed. This is a **finding**,
per the charter — not a license to climb; the foreman/owner decide, and the it2
rival should build against the same charter first so any climb runs on both
designs for attack parity.

## Minimum-subset reachability (plan Gate 6)

The Gate 6 floor — SC-P1's mapping shape with affirmative-only *semantics* —
is reached at paper for the shape and specified for the enforcement, pending the
climb. SC-P2 key composition is reachable now; a statement-vs-account tie-break
did not arise (statement is simply out of the key), so no edge is deferred.
SC-P3 ratifies as a definition inside the SC-P1 ADR.

## Handoff

Rung 1 exhausted for the incumbent. Recommend: (1) it2 clean-room rival on the
same charter (mapping-as-parameter; payer/statement-keyed identity); (2) then the
committee round 1 (governance-fidelity + adversary) with attack parity; (3) the
affirmative-only rung climb decided at that disposition, run on both designs if
authorized. Builder count under Gate 4: 1 of 2 used. Primary checkout to be
restored to `main`; design exhibits preserved by the forthcoming
`exhibits/source-completeness/it1` tag.
