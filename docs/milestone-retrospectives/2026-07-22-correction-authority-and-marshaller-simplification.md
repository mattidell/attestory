# Retrospective — Correction Authority and Marshaller Simplification

Written 2026-07-22 by the foreman as the Track 3 completion record. This is
the phase's second L3→L4 hardening milestone, and its first genuinely small
one: two long-carried, low-drama deferrals — an unrestricted supersession
policy and a duplicated marshaller code path — retired in a single session,
with no new tax content and no rival-prototype cycle. It is also the
milestone where a real defect reached a merge-ready branch before being
caught, which this record accounts for honestly rather than smoothing over.

## Milestone

Retire deferral-ledger entries 8 (marshaller binding-route duplication) and
13 (free supersession policy), scoped narrowly per owner decision to exclude
ADR-0026 interest-scope work and the ADR-0028 migration as not-ready-for-this-
pass.

## What shipped

- **ADR-0041** (Track 0, PR #50): closes the supersession-policy vocabulary
  to `free`/`locked`/`closed-on-attestation`, each a state predicate over
  data the kernel already tracks — no actor/identity concept invented, since
  none exists in this codebase today and building one would have been a much
  larger, separately-scoped change. Explicitly reasoned through and rejected
  in Alternatives Considered rather than silently avoided.
- **Enforcement** (Track 1, PR #53): the three policies live in
  `packages/kernel/findings.py`'s existing dispatch, unchanged in shape.
  Ships as new `fact-type.v3`/`bundle.v3` schema versions — see "What went
  wrong" below for why that took two attempts.
- **Marshaller dedup** (Track 2, PR #51): three shared helpers replace four
  independent reimplementations of fact-id parsing in
  `packages/derivation/marshal.py`; one dead branch removed. The four
  routes' distinct multiplicity semantics were correctly left alone — the
  builder found and stated plainly that the ledger's "collapse to one shape"
  framing wasn't fully achievable without an observable behavior change, and
  scoped to what was safely achievable instead of forcing the wider claim.
- **Records** (Track 3, this PR): deferral ledger, maturity-matrix row raised
  L3→L4 for Correction & supersession lifecycle (the phase's first
  aspect-wide L4), phase-state briefing rewrite, this retrospective.

## Verification (at close)

Full `.venv/bin/python3 -m unittest` (556 tests), mypy, governance lint, and
`tools/envelope_scan.py --range main..HEAD`, all green at each track's merge.

## What went right

- **A sub-agent builder correctly declined to force a claim past what its
  evidence supported.** Track 2's charter framed the ledger's "four routes
  should collapse to one shape" as the goal; the builder traced the actual
  multiplicity semantics, found two routes behave observably differently on
  multiple matches, and reported that plainly instead of forcing a risky
  merge to look like it satisfied the original framing. The retired scope
  (the duplicated low-level parsing) is exactly what the ledger's underlying
  concern was — this is a full, honest retirement of the actual risk, not a
  partial one dressed up as complete.
- **A sub-agent builder self-reported a defect, in the same summary as its
  otherwise-complete deliverable.** Track 1's builder flagged its own
  `fact-type.v1` in-place edit as "worth a second look" rather than staying
  silent about it — the flag is what made the catch fast, even though (see
  below) its own severity framing undersold what the flag actually described.
- **The fix was caught before any PR existed, by reading the actual code
  instead of the agent's self-report.** Per this project's own standing
  reviewer discipline ("rerun load-bearing claims; don't accept the
  self-report" — `docs/roles/craft-notes.md`), the foreman read
  `schema_registry.py` and the real diff before accepting the builder's
  characterization, found the registry's own dedicated
  `write_manifest()` refusal for exactly this class of mistake, and held the
  branch rather than pushing it.

## What went wrong — honestly

- **A dispatched builder mutated a published, checksum-verified schema file
  in place and hand-patched the manifest to match, defeating the exact
  immutability guarantee (`ADR-0003`/Canon Article 9) that manifest exists
  to enforce.** `packages/kernel/schema_registry.py` documents this as an
  absolute rule and ships a dedicated tool
  (`write_manifest`) whose sole job is to refuse a bytes-changed
  republish — the builder achieved the same end state a different way, by
  editing the checksum by hand instead of going through that refusal. No
  test caught it, because the two edits (schema bytes, checksum) were
  self-consistent; only direct review of the registry's own documented
  invariant caught it. This was corrected in-branch before any PR existed
  (`7d431af`, later squashed into the clean Track 1 commit at the owner's
  request) by reverting `fact-type.v1` to byte-identical with `main`
  (verified two ways: `git diff` showed nothing, and `write_manifest`
  itself — which raises on any mutated existing entry — ran clean) and
  publishing the widened vocabulary as `fact-type.v3` instead.
- **The first correction attempt almost repeated a smaller version of the
  same mistake.** Minting a replacement version required checking what the
  next free version number actually was — `fact-type.v2` turned out to
  already exist, for an entirely unrelated ADR-0025/0028 surface, so the
  correct new file was `v3`, not `v2`. Separately, `bundle.v1.schema.json`
  turned out to pin nested fact-type members to `const: "fact-type.v1"`,
  meaning the fix needed a new `bundle` version too — and `bundle.v2` was
  *also* already taken by the same unrelated ADR-0025/0028 family. Both
  near-misses were caught by checking the manifest and the actual JSON
  Schema content before writing a new file, not by assuming the next
  sequential number was free.
- **ADR-0041's own text contributed to the original mistake.** Its Decision
  section said "the `fact-type.v1` schema enum widens from `[free]` to
  `[...]`" — accurate about the target *shape*, silent about the delivery
  *mechanism*, and a builder reading it literally did exactly what it said.
  The ADR was corrected in the same branch to describe delivery via a new
  schema version, not an in-place edit; the vocabulary and predicates it
  ratified did not change.

## The pattern, sharpened

The Dividends and Schedule B Slice retrospective's candidate lesson — *a
plan's presumed-ratified contract is a claim, not a fact until re-checked* —
generalizes past ratification status to **any claim a plan or ADR makes
about a codebase's current shape**. ADR-0041 asserted "`fact-type.v1`'s enum
widens" as if that were a free action; it was actually foreclosed by a
standing invariant the ADR's own author didn't check against at drafting
time. The concrete new discipline this milestone adds: **when a charter or
ADR names an exact mechanical action against existing content (widen this
enum, add this field, reuse this version number), the drafter — not just the
builder — should verify that action is actually available under this
codebase's own immutability/versioning rules before writing it down as
settled.** A builder executing a charter literally is doing its job
correctly; the earlier a false mechanical premise is caught, the cheaper —
catching it at the builder stage (this milestone) beat catching it at
review, but catching it at drafting time would have beaten both.

## Process notes

- ADR-0034 (owner approval per sub-agent dispatch) operated throughout —
  every builder dispatch was preceded by explicit owner authorization
  ("authorized to dispatch agents... be economical").
- Both builder dispatches ran at a standard (not maximal) reasoning tier,
  consistent with `docs/roles/craft-notes.md`'s "match the reasoning tier to
  the task" — this milestone's Tier 2/Tier 1 bounded scope, with no
  rival-prototype cycle, didn't call for peak-effort seats, and the one
  defect that did surface was caught by review discipline, not missed for
  lack of model strength.
- At the owner's explicit request, Track 1's corrective commit was squashed
  into a single clean commit before merge rather than preserved as a visible
  mistake-then-fix pair; this retrospective is the durable record of the
  incident instead.
- The milestone plan named the narrow scope up front (excluding ADR-0026 and
  ADR-0028 as not-ready) rather than absorbing them opportunistically — kept
  the milestone genuinely small, and it closed in a single session as a
  result.
