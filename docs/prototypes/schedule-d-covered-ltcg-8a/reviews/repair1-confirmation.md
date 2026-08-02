# Repair 1 Confirmation Review

Audience: prototype committee. Role: author-independent Confirmation
Reviewer, Rung 1 static paper evidence only.

Object measured: repair commit `e6747fd` (`repair1/design.md`,
`repair1/examination.md`), against `charter-repair1.md`, findings CA-02/CA-04
in `round-1-triage.md`, and the retained P1/P2/P3 boundaries of the selected
design at `bbecd3f3aae6777cf06e4bdbe58d91545f4faedd`. `repair1/examination.md`'s
self-reported "resolved" status is not treated as evidence; every claim below
is checked against `repair1/design.md`'s actual sentences.

Confirmed `git show --stat e6747fd`: the repair touches exactly the two
chartered output files (249 + 127 lines added, no other file). `python3
tools/envelope_scan.py --range main..HEAD` reports no findings.

## CA-02: CONFIRMED

Checked against `charter-repair1.md` CA-02 clauses 1-5 and
`round-1-triage.md`'s CA-02 disposition:

1. **Standalone numbered successor sentence.** `repair1/design.md` §1 states
   **P2-S5A** as its own bolded, numbered sentence, textually separate from
   the worked examples in §3.2/§3.3. It reads: "For this bounded class, `B2`,
   the box-2a family, must be **closed**—either closed-empty or
   closed-nonempty—for the Schedule-D completeness boundary to pass." This is
   citable independent of any example. Confirmed.
2. **Closed-empty contributes zero, unchanged.** P2-S5A: "Closed-empty `B2`
   contributes the closure-backed amount zero, exactly as before." Confirmed,
   and re-demonstrated in §3.2 (shared case 7 regression): `L13=0`,
   `P@ps1=4,200` from Schedule D alone.
3. **Closed-nonempty contributes exactly once via line 13, only when the
   Schedule-D producer of `P` is current.** P2-S5A: "When the Schedule-D
   producer of `P` is current, closed-nonempty `B2` contributes its current
   subtotal exactly once through Schedule D line 13." Confirmed textually and
   arithmetically in §3.3 (shared case 6): `L13=1,200` once, `LD16=P=5,200`,
   and `L9` "does not add `L13` or the box-2a subtotal again."
4. **No source-class expansion, no ADR-0050 edit, no second capital-gain
   path.** P2-S5A's closing sentence states all three limits explicitly. Also
   verified against the committed diff: only `repair1/design.md` and
   `repair1/examination.md` were added; no ADR file, schema, or `it2/`
   document was touched.
5. **Both states demonstrated with exact synthetic facts.** §3.2 (closed-empty,
   `B2` closed-empty, `T1c` gain 4,200) and §3.3 (closed-nonempty, `B2=1,200`,
   `T1` gain 4,000, `Q=500`) both give concrete synthetic facts, exact pin
   sets, and the once-only line-13/line-9 arithmetic (`L9@n3` "consumes
   `L7A@l3` once; it does not add `L13` or the box-2a subtotal again").

No falsifying gap found. All five charter clauses are met by the artifact
itself, not by the examination's self-report.

## CA-04: CONFIRMED

Checked against `charter-repair1-confirmation.md` CA-04 clauses 1-6 and the
independent-assessment instruction, and directly against ADR-0050 Decisions 7
and 8:

1. **Exact, falsifiable pin contract per producer signature, no
   "as-applicable" hedge.** Grepped `repair1/design.md` and
   `repair1/examination.md` for "as applicable" / "same pins" / "where
   applicable" — the only match is examination.md's explicit denial ("This is
   not an implicit 'same pins' assertion"). §2.1's table and §2.2's P3-S8
   state exact pin sets per signature. Confirmed.
2. **No accepted Decision 7 pin moves; no new direct line-16 pin beyond
   `selected_line7a -> P`.** §2.3 closing paragraph states this explicitly.
   Independently checked: `COMMON16` (taxable income, filing status, rounding,
   `Q`, `P`, computation parameters, citation) is exactly ADR-0050 Decision
   8's stated direct line-16 set with `L` renamed to `P` — not an expanded
   set. Confirmed, not merely asserted.
3. **Upstream authority stays transitive, never duplicated as a direct
   `TAX16` pin.** §2.2 states C1-C4/box-2a authority remain transitive under
   `P-direct`, and `LD16`/`ATT-D`/`B1`-`B9` remain transitive under
   `P-schedule-d`. Each of §3.1, §3.2, §3.3 explicitly lists what `TAX16`
   does *not* directly pin, matching this rule case by case. This assignment
   of `ATT-D`/`LD16`/`B1`-`B9` as `P`'s own direct pins (not `TAX16`'s) is
   unchanged from the selected `it2/design.md` P3-S4 Schedule-D-producer
   bullet — the repair does not invent a new transitive boundary. Confirmed.
4. **Four-row Decision 7 table correctly resolved for `P-direct`; Schedule-D
   route adds none of its rows.** §2.3's four rows were checked line-for-line
   against ADR-0050 Decision 7's table:
   - `Q>0`/closure-`P=0` -> declaration `"no"` + conclusion `"no"` (matches
     R2-Q2);
   - `Q=0`/`P>0` -> conclusion `"no"` only (matches R2-Q1/R2-E — and this is
     exactly the row `round-1-triage.md`'s CA-04 dissent said was missing: "a
     direct-route Q=0/P>0 result still owes the conclusion-'no' direct pin");
   - `Q>0`/`P>0` -> declaration `"yes"` + conclusion `"no"` (matches);
   - `Q=0`/closure-`P=0` -> none (matches R2-Q3).
   §2.3 then states the Schedule-D route adds none of these four rows'
   pins for any `Q`. §3.3 (case 6) independently confirms this: despite
   `Q>0`/`P>0`, `TAX16@t3` carries neither declaration nor conclusion because
   Schedule D produced `P` — this is the exact scenario CA-04's dissent
   flagged as unresolved in the pre-repair design, and it is now resolved.
   Confirmed.
5. **Nonnumeric `P` states handled before `COMMON16` assembly, no silent
   numeric default.** §2.2's second paragraph gives exact dependency sets for
   `blocked`, `guard_inapplicable`, and numeric-`P`/blocked-`Q`, each stopping
   before any declaration/conclusion/numeric-parameter read. §2.4's ledger
   independently instantiates `blocked` and `guard_inapplicable` with
   concrete synthetic facts and confirms `TAX16`'s exact dependency set in
   each case. Confirmed.
6. **Forward/reverse correction with exact pins; no displaced finding
   revives.** §4.1 (direct-to-Schedule-D) and §4.2 (Schedule-D-to-direct)
   trace exact current/displaced states at each step and explicitly state "No
   displaced direct finding revives" / "No displaced Schedule-D result
   revives" / "No old finding revives." Confirmed.

**Independent assessment of the no-route-tag claim.** The claim rests on two
already-settled, unchanged facts: (a) `P-direct` and `P-schedule-d` pin
disjoint authority sets (box-2a family/C1-C4 versus `LD16`/`ATT-D`/`B1`-`B9`,
with zero overlap), and (b) selected P3-S4 (unchanged by this repair) makes
the two producers mutually exclusive. Given disjoint pin sets and exclusive
production, the current producer is mechanically recoverable from which
authority set `P`'s current publication pins — no case in §3 or §4 requires
inspecting a route tag to resolve, and no case produces an ambiguous or
overlapping pin set. This holds for every repaired case (direct-only,
Schedule-D-only, both-gain, forward correction, reverse correction, and every
row of the atomic ledger). The repair correctly scopes the *mechanical
enforcement* of exclusivity (schema/validator representation) to CA-06 and
does not claim more than the Rung-1 paper contract; that scoping is accurate,
not evasive.

No falsifying gap found for CA-04.

## REGRESSION BOUNDARY: INTACT

- **P1 untouched.** The repair makes no P1 statement; `repair1/examination.md`
  states this directly, and `repair1/design.md` never restates or edits any
  P1-Sx sentence. Confirmed by the diff (`e6747fd` touches no P1 material) and
  by content inspection.
- **`B1`, `B3`-`B9` unchanged.** `repair1/design.md`'s header states "P2-S1
  through P2-S4 and P2-S6 through P2-S8 remain unchanged"; only P2-S5 is
  replaced by P2-S5A, and that replacement narrows to the `B2` closure
  requirement only. No other boundary authority's required state changed.
- **Exactly-one-producer arithmetic for `P` holds.** P3-S4 (mutual exclusion)
  is explicitly listed unchanged; every repaired case (§3.1-§3.3, §4.1-§4.2)
  shows exactly one current `P` publication, never two.
- **Honest non-publication preserved.** §2.4's ledger and §4's correction
  traces distinguish `blocked`, `guard_inapplicable`, closure-backed zero, and
  published value throughout; no case collapses a missing/blocked state into
  zero or a fabricated value. §2.4's closing paragraph on Schedule-D boundary
  failure (`B7="no"`) explicitly rejects falling back to the direct
  candidate's stale `"yes"` conclusion.
- **QDCG state-partition shape unchanged.** `repair1/design.md` §2.2 states
  the partition "still selects QDCG exactly when `Q>0 or P>0`, and ordinary
  tax exactly when current authoritative `Q=0` and closure-backed `P=0`" —
  the same shape as selected `it2/design.md` P3-S6 and ADR-0050 Decision 7.

No regression found.

## Findings

No falsifiable findings survived independent verification. Every CA-02 and
CA-04 clause is met by an exact sentence, table, or worked case in
`repair1/design.md` itself, not by inference or by trusting
`repair1/examination.md`'s self-report. The regression boundary is intact
under direct inspection of the diff and the unchanged sentences.

## Uncertainty Rung 1 cannot distinguish

The route-tag/no-tag question (CA-04 clause 3 and the independent-assessment
instruction) is settled as a **paper** contract only: disjoint pin sets plus
mutually exclusive producers make the signature recoverable on paper. Rung 1
cannot show that the committed schema/validator substrate mechanically
enforces this exclusivity or exposes the signature without a schema change —
that is CA-06, correctly named and left open by the repair. This is not a
defect in the repair; it is the pre-existing, correctly-scoped boundary
between Rung 1 and Rung 2 that this repair does not climb.

## Overall verdict: READY

Both CA-02 and CA-04 are confirmed against the exact repaired artifact, and
the regression boundary is intact. No repair, synthesis, or scope change is
recommended.
