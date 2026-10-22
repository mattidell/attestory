# P0 Increment A — the 2025 law and the parameter inventory

Milestone: `tax-on-taxable-income`. Investigation only; no production, content,
schema, test, or golden edit. The plan's P0 action, increment A.

## Primary sources

Downloaded into `temp/tax-on-taxable-income/sources/` (git-ignored) and read
with `pdftotext -layout`:

- **Rev. Proc. 2024-40** — `https://www.irs.gov/pub/irs-drop/rp-24-40.pdf`
  (2025 annual inflation adjustments). This revenue procedure predates the
  2025 mid-year legislative change below; its standard-deduction figures are
  **superseded** for 2025 by that statute. Its rate-bracket thresholds and
  preferential (0/15/20%) breakpoints are **not** touched by that statute and
  remain the governing 2025 figures.
- **2025 Form 1040 and 1040-SR instructions (`i1040gi`)** —
  `https://www.irs.gov/pub/irs-pdf/i1040gi.pdf`, including the 2025 Tax Table,
  Tax Computation Worksheet, Qualified Dividends and Capital Gain Tax
  Worksheet, Social Security Benefits Worksheet, and the standard-deduction
  chart/worksheet. This is the later, more specific, and (for the standard
  deduction) the controlling 2025 document, since it was produced after the
  statute below and states the corrected amounts directly.
- **Pub. L. 119-21 (July 4, 2025), "One Big Beautiful Bill Act," H.R. 1** —
  `https://www.congress.gov/119/plaws/publ21/PLAW-119publ21.pdf` (331 pages;
  only §§70101-70103 are relevant here). Section 70102 amends 26 U.S.C.
  §63(c)(7), effective for taxable years beginning after December 31, 2024
  (i.e., 2025), raising the §63(c)(7) base standard-deduction figures.

**Where Rev. Proc. 2024-40 and the 2025 Form 1040 instructions disagree, the
later statute and the 2025 instruction govern** — this applies to exactly one
figure set: the basic standard deduction. Every other figure in this account
(rate brackets, preferential breakpoints, Social Security worksheet amounts)
is unchanged between the two sources and both agree.

## Verified 2025 values

### 1. The seven-bracket rate schedule (26 U.S.C. §1(j), as adjusted; Rev.
Proc. 2024-40 §2.01, confirmed unchanged by the 2025 Tax Computation
Worksheet, `i1040gi.pdf` p.80)

| Filing status | 10% | 12% | 22% | 24% | 32% | 35% | 37% |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Single | to $11,925 | to $48,475 | to $103,350 | to $197,300 | to $250,525 | to $626,350 | above |
| MFJ / QSS | to $23,850 | to $96,950 | to $206,700 | to $394,600 | to $501,050 | to $751,600 | above |
| MFS | to $11,925 | to $48,475 | to $103,350 | to $197,300 | to $250,525 | to $375,800 | above |
| Head of household | to $17,000 | to $64,850 | to $103,350 | to $197,300 | to $250,500 | to $626,350 | above |

Source: Rev. Proc. 2024-40 §2.01 Tables 1-4 (rp-24-40.txt lines 136-204),
cross-checked against the 2025 Tax Computation Worksheet's subtraction
amounts (`i1040gi.pdf` p.80, which only states the brackets at or above
$100,000, consistent with these thresholds).

Note: Pub. L. 119-21 §70101 amends 26 U.S.C. §1(j) but only changes **how the
12%/22% bracket-boundary inflation adjustment is computed for taxable years
beginning after December 31, 2025** — it does not change any 2025 bracket
threshold. Verified unaffected for tax year 2025.

### 2. The Tax Table rule (`i1040gi.pdf` pp.36, 67-68)

- **Who must use it**: taxable income **less than $100,000** must use the Tax
  Table; **$100,000 or more** must use the Tax Computation Worksheet
  (`i1040gi.pdf` p.36, "Tax Table or Tax Computation Worksheet").
- **Band widths**: $25-wide bands from $0 to $3,000 (verified: table rows
  "950-975", "975-1,000" etc., `i1040gi.pdf` p.68); $50-wide bands from
  $3,000 to $100,000 (verified: table rows "46,750-46,800",
  "46,800-46,850" etc., `i1040gi.pdf` p.67).
- **Midpoint method**: each band's published tax is the ordinary-schedule tax
  on the band's midpoint, rounded to the nearest whole dollar. The
  instructions do not state this formula in words, but it is independently
  verified here by reconstruction: for the single-filer $46,800-$46,850 band,
  midpoint $46,825, tax = $1,192.50 + ($46,825 - $11,925) × 12% = $5,380.50,
  which rounds (round-half-up) to **$5,381** — exactly the published table
  entry at that band (`i1040gi.pdf` p.67, row "46,800 46,850", Single column).
  The same check at the $950-$975 band (midpoint $962.50, tax = $962.50 ×
  10% = $96.25 → $96) matches the published entry exactly.
- **$100,000 boundary**: confirmed above; also independently re-derivable
  from the 2025 Tax Computation Worksheet's own first row, "At least
  $100,000 but not over ...".

### 3. The 0/15/20% preferential-rate thresholds (26 U.S.C. §1(h), §1(j)(5);
Rev. Proc. 2024-40 §3.03, confirmed identical in the 2025 QDCG Worksheet,
`i1040gi.pdf` p.37)

| Filing status | Max 0% amount | Max 15% amount (20% begins above) |
| --- | --- | --- |
| Single | $48,350 | $533,400 |
| MFJ / QSS | $96,700 | $600,050 |
| MFS | $48,350 | $300,000 |
| Head of household | $64,750 | $566,700 |

Both sources agree exactly; unaffected by Pub. L. 119-21.

### 4. The standard deduction (26 U.S.C. §63(c), as amended by Pub. L.
119-21 §70102; `i1040gi.pdf` pp.20-21, 2025 Standard Deduction Worksheet for
Dependents line 3)

| Filing status | 2025 basic standard deduction (verified, post-statute) |
| --- | --- |
| Single / MFS | **$15,750** |
| MFJ / QSS | **$31,500** |
| Head of household | **$23,625** |

Rev. Proc. 2024-40 §2.17 had these at $15,000 / $30,000 / $22,500
respectively (`rp-24-40.txt` lines 456-460) — those are the figures Pub. L.
119-21 §70102(b) struck and replaced (`$12,000`→`$15,750` combining the
former base-plus-inflation mechanics into the single new base amounts above;
the Act's own text shows the arithmetic as `$18,000`→`$23,625` for head of
household and `$12,000`→`$15,750` for single/MFS, `publ119-21.txt` lines
4968-4973). The 2025 Form 1040 instructions (produced after enactment) state
the corrected $15,750/$31,500/$23,625 figures directly and are the ones used
here.

### 5. Additional standard deduction for age 65 or blindness (26 U.S.C.
§63(f); Rev. Proc. 2024-40 §2.17, confirmed in the 2025 Standard Deduction
Worksheet, `i1040gi.pdf` p.21 line 4b)

| | Married (each box, i.e. taxpayer or spouse) | Unmarried (single or HoH) |
| --- | --- | --- |
| Amount | **$1,600** | **$2,000** |

Unaffected by Pub. L. 119-21 (that act amends §63(c)(7), not §63(f)). Both
sources agree exactly.

### 6. Capital-loss limit (26 U.S.C. §1211(b)(1))

$3,000 ($1,500 if married filing separately). This is a fixed statutory
amount, not inflation-indexed, and is not restated in either downloaded
source (Rev. Proc. 2024-40 only lists inflation-adjusted items; the Form 1040
instructions do not restate Schedule D's own loss-limitation mechanics). It
is recorded here from the Internal Revenue Code's own, long-stable text
rather than re-derived from either downloaded 2025 document in this
investigation — **flagged as verified against general tax-law knowledge, not
against a freshly downloaded 2025-dated primary source**. A reviewer wanting
a document-dated citation should pull the 2025 Instructions for Schedule D
(not downloaded here) or the current 26 U.S.C. §1211(b) text directly.

### 7. Social Security Benefits Worksheet amounts (26 U.S.C. §86; `i1040gi.pdf`
p.31, Social Security Benefits Worksheet lines 8 and 10)

| | MFJ | Single / HoH / QSS / MFS-lived-apart |
| --- | --- | --- |
| First threshold (line 8) | $32,000 | $25,000 |
| Second threshold (line 10) | $12,000 | $9,000 |

These four amounts are fixed statutory thresholds (unchanged since 1993),
confirmed directly in the 2025 worksheet text.

## Parameter inventory: core v49 against the verified 2025 values

`packages/content/tax/2025/package.core-calculations.v49.json` adopts nine
`demo.parameter.*` members. Every one is in scope; no non-`demo.*` numeric
tax-law parameter among the rules this investigation traces (line 16, the
preferential base, the standard deduction, the Social Security worksheet)
was found unverified.

| Parameter id / version | File | Current value(s) | Verified 2025 value(s) | Match? | Consuming rule(s) |
| --- | --- | --- | --- | --- | --- |
| `demo.parameter.tax-brackets.2025` v2 | `parameter.tax-brackets.v2.json` | 3 brackets per status (10/12/22%), e.g. single: $0-$11,600 (10%), $11,600-$47,150 (12%), above (22%) | 7 brackets per status, see table 1 above | **No** — only 3 of 7 brackets; thresholds are the pre-2025 (2024) amounts | `rule.form1040-line16` v5 (ordinary-base `bracket_fold`) |
| `demo.parameter.qdcg-preferential-brackets.2025` v2 | `parameter.qdcg-preferential-brackets.v2.json` | 1 bracket per status, flat 15% from $0, no upper bound | 3 bands per status: 0%, 15%, 20%, with the breakpoints in table 3 above | **No** — no 0% or 20% band at all | `rule.form1040-line16` v5 (preferential-base `bracket_fold`) |
| `demo.parameter.standard-deduction-base.2025` v1 | `parameter.standard-deduction-base.json` | single/MFS $15,000; MFJ/QSS $30,000; HoH $22,500 | single/MFS $15,750; MFJ/QSS $31,500; HoH $23,625 | **No** — these are the *pre-Pub.L.119-21* Rev.-Proc.-2024-40 amounts, now superseded for 2025 | `rule.form1040-standard-deduction` v1 |
| `demo.parameter.additional-deduction-rate.2025` v1 | `parameter.additional-deduction-rate.json` | single/HoH $2,000; MFJ/MFS/QSS $1,550 | unmarried (single/HoH) $2,000; married (each) $1,600 | **Partial** — single/HoH correct; MFJ/MFS/QSS is $1,550, should be $1,600 (a plain inflation-figure error, unrelated to the mid-year statute) | `rule.form1040-standard-deduction` v1 |
| `demo.parameter.capital-loss-limit.2025` v1 | `parameter.capital-loss-limit.json` | $3,000 (MFS $1,500) | $3,000 (MFS $1,500), per §1211(b)(1) | **Match** (see caveat in item 6 above: verified from general knowledge, not a freshly downloaded 2025 document) | `rule.schedule-d-line21` v1 |
| `demo.parameter.ss-benefits-base-amount.2025` v1 | `parameter.ss-benefits-base-amount.json` | MFJ $32,000; all others $25,000 | MFJ $32,000; all others $25,000 | **Match** | `rule.ss-benefits-worksheet` v3 |
| `demo.parameter.ss-benefits-second-tier.2025` v1 | `parameter.ss-benefits-second-tier.json` | MFJ $12,000; all others $9,000 | MFJ $12,000; all others $9,000 | **Match** | `rule.ss-benefits-worksheet` v3 |
| `demo.parameter.ss-benefits-half-rate.2025` v1 | `parameter.ss-benefits-half-rate.json` | 50% flat | 50% flat (statutory, §86(a)(1)) | **Match** | `rule.ss-benefits-worksheet` v3 |
| `demo.parameter.ss-benefits-85-rate.2025` v1 | `parameter.ss-benefits-85-rate.json` | 85% flat | 85% flat (statutory, §86(a)(2)) | **Match** | `rule.ss-benefits-worksheet` v3 |

### Summary

- **Four mismatches**: the rate schedule (wrong bracket count and
  thresholds), the preferential brackets (missing 0%/20% bands), the standard
  deduction base (superseded by the 2025 mid-year statute), and the married
  additional-deduction amount ($1,550 should be $1,600, a plain error
  independent of the statute).
- **Five matches**: the capital-loss limit and all four Social Security
  worksheet amounts.
- The single/HoH additional-deduction amount ($2,000) is correct; only the
  married figure is wrong.
- No rule in this traced set applies the 2025 Tax Table below $100,000 (see
  Increment B).

Continued in `p0-path-and-cost.md` (Increment B: the current path, the
short-term defect, the Tax Table expressibility verdict, and the cost of
change).
