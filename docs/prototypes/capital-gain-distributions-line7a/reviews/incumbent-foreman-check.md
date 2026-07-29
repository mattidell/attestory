# Incumbent Foreman Check

Date: 2026-07-28

Object: incumbent Rung-1 paper design at
`1a7530faa68cd382f5216e2a4f1373416632a3ae`, relative to launch commit
`42644186fa736df5c0e4f9ea71ed2415fe3038c8`.

This is an owner-directed early foreman check, not either of the two independent
committee reviews required after the rival round. It records the result
durably so a later repair Builder does not depend on thread context.

## Verdict

**NOT READY.** P1–P3 are not settled at Rung 1.

## Findings and Gate-5 classification

### F1 — Box-2a presence was narrowed to positivity

**Proposition:** P2  
**Classification:** `decision-blocking`

S2.6 raises `CAPITAL_GAIN_DISTRIBUTION_RECORDED` only for a current
**positive** successor box-2a member. ADR-0035 decision 3 and the committed
admission check define the signal by box-2a **presence**: every non-null
reported value, including numeric zero, raises it. The design therefore
weakens an accepted interlock while claiming to consume it unchanged.

Required resolution: the successor signal feed preserves non-null presence
semantics, and the paper cases include a zero-valued present member as a
kill case. Changing the accepted signal semantics is not an incumbent repair.

### F2 — Direct-route disposition depends on guard evaluation order

**Proposition:** P1  
**Classification:** `decision-blocking`

S3.1 declares
`all([require_closed(f1099div.2a), categorical_compare(schedule-d-required,
"no")])`. The committed evaluator evaluates `all` left-to-right and
short-circuits. With current authority `"yes"` and an open or stale family,
`require_closed` raises before the categorical guard can yield false. The
result is blocked, contradicting S1.3's unconditional
`guard_inapplicable` promise. With authority missing and an open family, the
same order also prevents the walk from naming the missing authority.

Required resolution: state a declared conditional structure whose disposition
does not rest on incidental operand order, then instantiate the combined
authority/family states.

### F3 — The line-16 handoff has no defined absent-line-7a path

**Proposition:** P3  
**Classification:** `decision-blocking`

S3.4 makes the worksheet condition and preferential base read
`line7a-total`, while S1.2/S1.3 deliberately leave that publication absent
when authority is missing or `"yes"`. No declared optional binding or
selection mechanism grounds the claimed “otherwise literal 0.”

For Q=0 with positive box 2a and missing authority, the committed evaluator
encounters an absent derived `line7a-total` before the conditional dependency
set can name the missing contributable declaration. For Schedule D required,
line 9 cannot publish without its new line-7a input, so lines 11 and 15 do not
produce the taxable-income input that line 16 requires; line 16 therefore
cannot reach the claimed `guard_inapplicable` result.

Required resolution: define the exact declared dependency/disposition path
through line 7a, line 9, taxable income, and line 16 for missing and `"yes"`
authority. It must neither default a blocked capital-gain path to zero nor
reach raw statement content.

### F4 — Mandatory negative cases are not concrete

**Propositions:** P1/P3  
**Classification:** evidence defect supporting F3

Case 3 says `capital-gain-distributions` may be present or absent and Q may be
positive. Case 4 leaves Q unspecified. Those alternatives produce materially
different line-16 evaluation paths. The charter requires concrete facts,
current/displaced states, pins, and walks rather than alternative prose.

Required resolution: split the materially distinct variants and give each
exact current facts and non-publication results. At minimum, exercise Q=0 and
Q-positive where the path differs.

## Checks

- Only the two chartered output files changed in the Builder commit.
- `git diff --check 42644186..1a7530fa` passed.
- `python3 tools/envelope_scan.py --range main..HEAD` passed.
- No production code, schema, content, ADR, real-data, or Schedule D artifact
  entered the commit.

## Recommendation

Do not mark the incumbent settled and do not spend the single repair pass yet.
Proceed according to the approved rival-round sequence. If the owner later
directs the bounded repair allowed after the rival round, its charter should
name F1–F4 explicitly and preserve the Rung-1 ceiling.
