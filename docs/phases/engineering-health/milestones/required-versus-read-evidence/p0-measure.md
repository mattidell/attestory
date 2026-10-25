# P0 — required-but-unread inputs in shipped content

Scripts and raw output beside this file, all run at `4fbefda9`:
`p0_static_scan.py` → `p0-static-scan.txt`; `p0_path_scan.py` with
`p0_path_probe.py` over the modules in `p0-route-modules.txt` →
`p0-path-scan.txt`. Numbers below are pasted from those outputs.

## Static scan (a required symbol referenced nowhere in the rule)

```
core-calculations | 54 | 15706 | 323 | 5 | 318
first-tax-slice | 1 | 1 | 0 | 0 | 0
interest-slice | 1 | 19 | 5 | 0 | 0
LATEST PACKAGE tax.us.2025.package.core-calculations@v54: 2 hits, 1 distinct rule ids
```

The latest package's only hit is `form1040-line16` v6, which requires
`filing_status` and `tax.us.2025.income.taxable-income` that its value reads
only through worksheet rules it pins. Superseded versions include
`eic-eligibility` v1 (core v53), whose `no-qualifying-child` answer was
referenced nowhere, one of the earned income credit milestone's known cases.

## Path scan (a required input absent from a published finding's runtime pins)

```
published findings: 33631
matched to a rule evaluation: 27826
rule versions with an absent required input: 57
rule-symbol pairs absent on every published finding: 43
rule-symbol pairs absent on some but not all published findings: 164
```

33 of the 57 rule versions are in core v54. 729 published findings carry a
rule pin with no matching `pins_for` record (Form 1099-K statement rules and
the interest current-year adjustment subtotal) and are not covered; 5,076
are inputs or declared defaults.

The scan detects the pre-repair shapes of two of the three earned income
credit cases (`eic-early-stop` v1, 33/36; `eic-answer.no-unsupported-situations`
v1, 31/36). The third is not separately distinguishable.

## Classification of the 33 rule versions in core v54

| Class | Count | Example |
| --- | --- | --- |
| By-design scope closure (compiler member-validation gates) | 8 | `f1099b-covered-w-lt-adjustment-subtotal` v2, 252/252 |
| Over-declared: a derived or return-level input read only on some branches | 25 | `eic-early-stop` v2 requires the derived `eic.answer.no-unsupported-situations`, read only on its stop branches; `ss-benefits-worksheet` v3; `dependents-worksheet-line-1` spouse boxes on unmarried returns |
| Misleading question or correction hazard (of the rows examined) | 0 | — |

The Foreman reclassified two rows the builder had called misleading:

- `eic-early-stop` v2 requires the answer rule's derived output, not the
  person's fact. Its default path is 0 whatever that symbol is, and the
  answer rule asks the person only where the EIC contract says. Its
  "absent on every finding" result also reflects coverage: no v54 test takes
  the branch that reads it. The runner blocks `DEPENDENCY_ABSENT` when any
  required symbol is missing (`packages/derivation/runner.py`), so the
  derived answer must exist even on the 0 path; that adds no question,
  because `eic-gate-result` v2 and `eic-eligibility` v2 already require it.
- `f1098-line8a` v2 requires Form 1098 box 3 (origination date), a document
  field, read only after the residence and payment gates. The Form 1098
  milestone made box 3 required authority for the statement
  (`docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md`);
  it is not a question a person answers.

The two flagged rows and the gate rows were examined; the 25 over-declared
rows were classified by shape (a derived or return-level input read only on
some branches), not each traced. In the rows examined, wherever an unread
requirement could change a result it does so through a branch condition that
is itself read and pinned.

## What the path scan measures

The path scan measures content and test coverage together. A rule-symbol
pair is "absent on every finding" either because the content over-declares
or because no test reaches the branch that reads it. A gate on it would fail
on coverage gaps as often as on content defects.
