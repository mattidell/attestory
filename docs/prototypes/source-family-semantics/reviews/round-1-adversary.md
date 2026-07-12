# Round 1 — Adversary Review

Reviewer: Adversary. Medium/medium. Same six cases applied to both papers
(it1 = five-part declaration, it2 = closed-set-is-the-claim). Peer review not read.

## Case 1 — Non-form taxable interest (design case 3)

Attempted substitution: wire a true, empty box-1 closure directly into an L2B
guard as if `S(B1)` were `T(TI)`.

- it1: **Resisted.** Failure map rejects any mapping/calculation reading
  box-3/non-form interest under a box-1 mapping; box-1 closure "may not
  directly authorize a line-2b zero."
- it2: **Resisted.** §3: `L2B` "requires declared taxable-interest input
  T(TI)... may use S(B1) as one component, never as T(TI) by implication."
- Residual gap (both): the block is narrative, not structural — neither paper
  defines what *prevents* a future L2B rule's guard from declaring `S(B1)` as
  its `T(TI)` input (no schema constraint or "subtotal" vs "final-input" type
  distinction exists). Both defer the guard mechanism to "a future rule."

## Case 2 — Box 3 on the same statement (design case 4)

Attempted substitution: treat the statement, not the box-1 fact, as the
member unit, or truncate coverage to "1099-INT items: complete."

- it1: **Resisted** at the fact level — membership is "findings whose... item
  is box 1," not the statement; box 3 is explicitly not swept in.
- it2: **Resisted** at the fact level — source instance is "the box-1 item on
  [statement]," not the statement; §6 names this exact attack as the reason a
  document-level family fails case 4.
- Residual gap (both): presentation is out of scope (it2 §7 defers "UI
  language"; it1 gives no label rule). A coverage label dropping "box-1"
  would reintroduce the ambiguity both papers argue against semantically;
  neither invariant reaches the rendered string.

## Case 3 — Two statements, one payer (design case 2)

Attempted substitution: payer-keyed aggregation collapsing two statements
into one member.

- it1: **Resisted**, explicit: "two instances from one payer remain two
  members."
- it2: **Resisted**, explicit: names payer-keyed aggregation as a case-2
  failure of the rejected alternative.
- Adjacent, unresolved in both: statement-instance *sameness* (duplicate
  upload vs. two originals) is delegated to ADR-0015, listed as **Not
  Decided**. A naive implementation could double-count a duplicate upload —
  inflated, not narrowed, but the "member count" both papers treat as ground
  truth isn't a decided quantity yet.

## Case 4 — Late discovery after a pinned zero (design case 5)

Attempted substitution: after late member evidence is discovered, leave the
prior closure finding untouched and see if the old zero stays current.

- Both require "a later act withdraws or supersedes" the closure finding (it1
  step 2, it2 step 4), but describe discovery and withdrawal as sequential
  without tying them together.
- **Path found, not resisted, in both:** neither paper specifies what
  *detects* the contradiction between newly-discovered member evidence and an
  existing true closure finding, or what *triggers* the withdrawal. If the
  late statement is discovered but nothing re-asserts the closure fact to
  false/not-current, the old finding stays current under ADR-0011's
  affirmative-only rule, and the pinned zero it authorized stays current
  under ADR-0010 — nothing has contradicted it from the kernel's point of
  view. This is round-1.md's named failure ("any late-discovery lifecycle
  that leaves a false zero current"). Both papers specify correction
  mechanics once triggered, not the trigger itself — the sharpest shared gap
  found this round.

## Case 5 — Narrow closed, broad open (design case 6)

Attempted substitution: a dashboard rolls up several closed narrow families
into "income sources complete," implying line-level totals are final.

- it1: not addressed — no rollup consumer is in scope.
- it2: partially addressed — §1 requires a consumer to "name the family (or
  an explicitly declared composition of families)," forcing a rollup to
  declare its composition, but gives no coextensiveness check — a stated
  requirement, not demonstrated resistance.
- Neither paper is exploited; flagged unaddressed rather than resisted.

## Case 6 — Misleading "all interest" language (rejected-rival critique)

Attempted substitution: name a family `taxable-interest` but scope member
predicate, mapping, and coverage to box 1 only — recreating each paper's
rejected rival by renaming all parts consistently, not breaking equality.

- it1: the defense is that the rival "is a mismatch among all five declared
  parts" — but that only holds if `Claim` text is checked against `Member
  universe` for coextensiveness beyond authoring intent, which is not
  required.
- it2: sharper exposure. Its invariant `closure claim = member predicate =
  mapping input set = coverage subject` is **satisfied** by a family named
  `taxable-interest` with box-1-only membership/mapping/coverage — all sides
  stay consistently box-1-scoped. The invariant catches internal
  inconsistency, not external mislabeling; §6's rejection argues from case
  failures, not from the invariant itself.
- **Not resisted by either design's formal mechanism**, only by narrative
  argument. Applies equally to both papers.

## Summary

Both papers resist every case-level attack the round's case set is built to
catch (box-3 leakage, payer collapse, direct box-1→line-2b substitution). The
exploitable/unaddressed territory is shared, not differentiating:

1. **Late-discovery trigger is undefined in both** — correction mechanics are
   specified, not what forces re-examination of a closure finding when
   contradicting evidence arrives. Maps directly onto round-1.md's failure
   criterion; highest-priority open question before promotion.
2. **Naming/label coextensiveness is unchecked in both** — it2's formal
   invariant and it1's coextensiveness claim are both defeated by consistent
   mislabeling, not just mismatched parts.
3. Presentation wording (labels, rollups) is deferred by both and is where
   "narrow closed/broad open" is most likely to erode in practice.

No path found where one design resists a case the other fails — the papers
are adversarially equivalent on the six-case set; residual risk is shared
infrastructure (trigger + naming discipline) neither paper defines.
