# Fresh-reader review: noncovered sales

- Seat: reviewer
- Branch: `milestone/noncovered-sales-2025`
- Reviewed commit: `(removed at closeout)`
- Comparison line: `github/main` (0 behind, 42 ahead; merge-base `e73d32cf19f2f0033853f314df36141a9a946f06`)
- Charter: `docs/reviews/noncovered-sales/charter-review.md`
- Plan read whole: `docs/phases/engine-breadth/milestones/noncovered-sales.md`

Scope judged: a return with a Form 1099-B sale whose basis the broker did not report computes Schedule D and Form 1040 line 7a from a filer-supplied basis on core v79; earlier cores keep the prior path; a sale outside the class is refused by an answer. Evidence ceiling: committed code, content, tests, and this reviewer's own coordinator runs. The builder's thread and self-reported suite were not used. `pytest` was not re-run. Governance text was not read.

Method: core v79 pinned the way the v79 tests pin it, then `live_coordinate_run` through the track executor. The prototype installer that replaces the coordinator was not called. Filers are synthetic `demo.*` findings on the wage base (wages 50,000, single). Cases: one noncovered long-term gain (proceeds 6,000, basis 2,000); one noncovered short-term loss (2,000 / 8,000); one noncovered long-term sale with code W (4,000 / 7,000, adjustment 1,000); one covered and one noncovered sale of each term (covered short-term 5,000 / 4,000, noncovered short-term 3,000 / 2,000, covered long-term 8,000 / 5,000, noncovered long-term 6,000 / 2,000). Covered halves use `basis_reported_to_irs` `yes`.

## 1. Tax correctness

Hand method. Form 8949 box B (short-term, basis not reported) is Schedule D line 2. Box E is line 9. Column (h) is proceeds minus basis, then combined with a code W amount in column (g) as a positive wash-sale disallowance. Line 7 is the sum of the short-term lines this package publishes (1a, 1b, 2, 6). Line 15 is the sum of the long-term lines it publishes (8a, 8b, 9, 13, 14). Line 16 combines 7 and 15. A gain on 16 is Form 1040 line 7a. A loss on 16 is limited on line 21 to the smaller of the loss and 3,000 for a single filer. Taxable income is wages plus line 7a, minus the 2025 single standard deduction of 15,750. Tax is the 2025 Form 1040 tax table (50-dollar band, midpoint, ordinary rates 10 percent to 11,925 and 12 percent to 48,475). Long-term gain that fits under the single 0 percent threshold of 48,350 is taxed at 0. The official instruction PDFs named by the citation citizens are not in this workspace; the arithmetic uses the form mechanics recorded in the milestone law note and those published 2025 figures.

| Case | Line | Hand | Engine |
| --- | --- | --- | --- |
| lt_gain | Schedule D 1a | 0 | 0, closure_backed_zero |
| lt_gain | Schedule D 2 | 0 | 0, closure_backed_zero |
| lt_gain | Schedule D 7 | 0 | 0, computed_zero |
| lt_gain | Schedule D 8a | 0 | 0, closure_backed_zero |
| lt_gain | Schedule D 9 | 4,000 | 4,000, published |
| lt_gain | Schedule D 15 | 4,000 | 4,000, published |
| lt_gain | Schedule D 16 | 4,000 | 4,000, published |
| lt_gain | Schedule D 21 | 0 | 0, computed_zero |
| lt_gain | Form 1040 7a | 4,000 | 4,000, published |
| lt_gain | Form 1040 15 | 38,250 | 38,250, published |
| lt_gain | Form 1040 16 | 3,875 | 3,875, published |
| lt_gain | Form 8949 box E (d)/(e)/(g) | 6,000 / 2,000 / 0 | 6,000 / 2,000 / 0 |
| st_loss | Schedule D 1a | 0 | 0, closure_backed_zero |
| st_loss | Schedule D 2 | −6,000 | −6,000, published |
| st_loss | Schedule D 7 | −6,000 | −6,000, published |
| st_loss | Schedule D 8a | 0 | 0, closure_backed_zero |
| st_loss | Schedule D 9 | 0 | 0, closure_backed_zero |
| st_loss | Schedule D 15 | 0 | 0, computed_zero |
| st_loss | Schedule D 16 | −6,000 | −6,000, published |
| st_loss | Schedule D 21 | 3,000 | 3,000, published |
| st_loss | Form 1040 7a | −3,000 | −3,000, published |
| st_loss | Form 1040 15 | 31,250 | 31,250, published |
| st_loss | Form 1040 16 | 3,515 | 3,515, published |
| st_loss | Form 8949 box B (d)/(e) | 2,000 / 8,000 | 2,000 / 8,000 |
| wash | Schedule D 1a | 0 | 0, closure_backed_zero |
| wash | Schedule D 2 | 0 | 0, closure_backed_zero |
| wash | Schedule D 7 | 0 | 0, computed_zero |
| wash | Schedule D 8a | 0 | 0, closure_backed_zero |
| wash | Schedule D 9 | −2,000 | −2,000, published |
| wash | Schedule D 15 | −2,000 | −2,000, published |
| wash | Schedule D 16 | −2,000 | −2,000, published |
| wash | Schedule D 21 | 2,000 | 2,000, published |
| wash | Form 1040 7a | −2,000 | −2,000, published |
| wash | Form 1040 15 | 32,250 | 32,250, published |
| wash | Form 1040 16 | 3,635 | 3,635, published |
| wash | Form 8949 box E (d)/(e)/(g) | 4,000 / 7,000 / 1,000 | 4,000 / 7,000 / 1,000 |
| mixed | Schedule D 1a | 1,000 | 1,000, published |
| mixed | Schedule D 2 | 1,000 | 1,000, published |
| mixed | Schedule D 7 | 2,000 | 2,000, published |
| mixed | Schedule D 8a | 3,000 | 3,000, published |
| mixed | Schedule D 9 | 4,000 | 4,000, published |
| mixed | Schedule D 15 | 7,000 | 7,000, published |
| mixed | Schedule D 16 | 9,000 | 9,000, published |
| mixed | Schedule D 21 | 0 | 0, computed_zero |
| mixed | Form 1040 7a | 9,000 | 9,000, published |
| mixed | Form 1040 15 | 43,250 | 43,250, published |
| mixed | Form 1040 16 | 4,115 | 4,115, published |
| mixed | Form 8949 box B (d)/(e)/(g) | 3,000 / 2,000 / 0 | 3,000 / 2,000 / 0 |
| mixed | Form 8949 box E (d)/(e)/(g) | 6,000 / 2,000 / 0 | 6,000 / 2,000 / 0 |

Every watched line on these four runs was `saturated`, with `presentation_valid` true. The committed `EXPECTED["v79"]` dollars for `lt_gain`, `st_loss`, and `wash` match this table. No expected dollar in those objects is wrong. Schedule D line 7 is absent from `_line_map` (`tests/test_noncovered_sales_v79.py:2021`) and from those expected objects. The live page publishes the hand sum. The four-sale return is not an expected object in that file. A code W recorded on a gain (proceeds 6,000, basis 2,000, adjustment 500) stays blocked, which is the lawful refusal of a disallowance on a sale that is not a loss; the engine does not publish 4,500.

## 2. Engine

The shared answer is counted once. `marshal_closure_authority` appends each current finding of a v4 fact type once, keyed by fact type and finding id, with `horizon_id=""` (`packages/derivation/marshal.py:281-300`). `_admit_group` takes that record only when exactly one candidate exists (`packages/derivation/source_authority.py:404-407`). Two current answers admit nothing.

`no` admits a listed family only when that family has a current horizon and zero current members (`source_authority.py:432-433`). `yes` admits each listed family that has a current horizon and is not stale (`source_authority.py:434-435`). `stale_group_families` treats the current answer as the last assertion of the v4 fact, then strips only a listed family whose later member-transition action is `assert` or `reclassify` (`source_authority.py:113-167`). A removal does not strip. Any other value, or a missing answer, admits nothing.

A v4 mapping cannot satisfy a family it does not list: admission walks `mapping_family_rows`, and a second mapping that claims the same family raises `SourceAuthorityError` (`source_authority.py:423-427`). The v2/v3 path still requires one current boolean-true finding on that family's current horizon and ignores member counts (`source_authority.py:346-375`). A repeated horizon id remains illegal in the kernel; this range does not edit `packages/kernel/`.

The covered-flag refusal is installed only for `("tax.us.2025.package.core-calculations", "v79")` (`packages/tax/loader.py:137-147`). The map names five object types (`loader.py:113-119`). A current member with `basis_reported_to_irs` `no` refuses that family (`source_authority.py:242-265`); the row code becomes `DEPENDENCY_INVALID` and the missing token is `BASIS_NOT_REPORTED_ON_COVERED` (`source_authority.py:268-278`). Live, the covered long-term object on path A blocks line 8a and its downstream lines with the dedicated sentence, and the closure-check row carries that token. The same function covers the other four object types. `covered-ltcg-txn` is named in the map and has no publisher on this package, so that fifth object was not measured here. A package that does not name the map passes an empty refusal set (`source_authority.py` admission preamble). New behavior is gated on a v4 mapping and on that v79 map.

Core v78 byte-identity was not re-rendered in this review. See limitations.

ADR-0079 containment still runs for v4 families. Group mappings contribute their listed family pins to `adopted_family_versions`, and the shared loop then raises `SourceAuthorityError` when a family has multiple active version chains (`marshal.py:325-355`).

## 3. Schemas

`git diff github/main -- packages/schemas packages/kernel` adds two files and appends two manifest lines. `packages/kernel/` is untouched.

- `packages/schemas/derivation/source-closure-mapping.v4.schema.json` is new. sha256 `4381cb8d33f3331bfc1fd11b118a233268a0448a74bf1df7bb6a33d7f85a23f6`, matching the new `published.json` entry.
- `packages/schemas/derivation/artifact-package.v41.schema.json` is new. sha256 `99adceccf2cc94a69e87cf138d56bbeda9bf9dfb225845b8433aab9a9e94d57a`, matching the new `published.json` entry.

No existing checksum in `published.json` changes. Under `packages/content`, the diff against `github/main` is 37 additions and no modifications.

## 4. ADR 0084

Status remains **proposed** (`docs/adr/0084-grouped-source-closure.md:3`). The plan withholds a ready PR until the owner accepts it. That is a publication gate, recorded below as a note.

The decision sentences match the code that was read:

- Decision 1: the v4 schema lists one closure fact and the family rows; `artifact-package.v41` is the new package schema; v3 and v40 files are unmodified.
- Decision 2: one current finding, `horizon_id=""`, `no` only with zero members, `yes` until a later add or reclassify, removal leaves the admission, any other value or two answers admit nothing, the pin is the family's current horizon plus that finding.
- Decision 3: the refusal map is a sibling of the companion declaration, only the package that names it applies it, the blocked row is `DEPENDENCY_INVALID` / `BASIS_NOT_REPORTED_ON_COVERED`, and the live page shows "Record this sale as a noncovered sale. The broker did not report its basis to the IRS."

ADR-0014 decision 3 remains the rule for earlier mappings: one boolean-true finding on the current horizon (`source_authority.py:365-375`). ADR-0084 says it supplements that rule and the diff does not edit ADR-0014. ADR-0017 decision 2 still keys horizon-keyed closure facts; the v4 finding is recorded outside that key by decision 2 of ADR-0084, and staleness for those families is the later member-transition, while each family's own horizon is still required for admission. ADR-0079's both-current refusal still runs, as cited above. ADR-0082's package overlay is how the v79 scalar pairs are installed (`loader.py`, the v79 companion declaration); a scalar without its sale fails projection with the companion fact named. ADR-0082 decision 6 describes that companion change. The new schema versions belong to the grouped-closure citizen, which ADR-0084 names. None of these four accepted records is edited by this range.

## 5. What the filer sees

On `wage_unclosed`, lines 2, 7, 9, 15, 16, 21 and Form 1040 lines 7a, 15, and 16 are blocked. Each blocked watched line carries the one sentence "Did you sell any securities whose basis was not reported to the IRS?" The distinct-sentence count on the page is 1. Lines 1a and 8a are closure-backed zeros.

On the covered long-term refusal, line 8a and the downstream lines are blocked with the dedicated sentence. The row code is `DEPENDENCY_INVALID` and `missing` is `BASIS_NOT_REPORTED_ON_COVERED`. The page reason is non-empty.

On code W recorded on a gain, line 9 and the downstream lines are blocked with both constraint meanings: "A wash-sale disallowance is recorded on a sale that is not a loss." (`family.f1099b-noncovered-lt.json:84`) and "The wash-sale disallowance exceeds this sale's own loss." (`family.f1099b-noncovered-lt.json:119`). Both are true of their `violated_when` clauses: the wash amount is positive and the proceeds are at least the basis, and 500 is greater than the floored loss of 0. The page is not the empty "waiting for the basis" fallback.

The closure-backed zero explains are false of one authority that selects that disposition. See the should-fix finding.

## 6. Scalar recorded without its sale

A current short-term proceeds finding of 100 with no sale object, run through the live coordinator on core v79, raises `FindingModelError` before any presentation page. The message names `tax.us.2025.f1099b.noncovered-st-txn.proceeds` as current and `tax.us.2025.f1099b.noncovered-st-txn` as having no current value, and says the finding is rejected. The committed companion test calls the enforcer directly. The live path also refuses the pair, with no page.

## 7. Data safety

`python3 tools/envelope_scan.py --range github/main..HEAD` exited 0 and printed nothing, which is that tool's clean result. A separate search of added diff lines for absolute machine-path prefixes found none.

An administrative ride-along in the same range flips ADR-0083 from proposed to accepted (2026-11-06). It is outside this charter's object.

## Findings

### explain-closure-zero-false-denial

- Severity: should-fix
- File: `packages/content/tax/2025/schedule-d.line-2.form-field.json:30` and `packages/content/tax/2025/schedule-d.line-9.form-field.json:30`
- Claim: The `closure_backed_zero` explain says the filer said they have no sales of that term. The line-2 and line-9 rules select that disposition whenever the term's families are closed, including when the shared answer is `yes` and that term simply has no member. The page renderer writes `instruction.explain` for a numeric disposition (`packages/presentation/pages/citation-walk.v1.html:1006`). On the live long-term gain page the shared answer is `yes` and line 2 is `closure_backed_zero` 0, so the filer is shown "You said you have no short-term sales whose basis was not reported, so Schedule D line 2, column (h), is zero." The same false denial appears on line 9 of the short-term loss and on line 2 of the wash sale. The published number is the correct zero.
- Reproduction: Pin core v79. Run the long-term gain case (proceeds 6,000, basis 2,000, `basis_reported_to_irs` `no`, shared answer `yes`) through `live_coordinate_run`. Read Schedule D line 2. Disposition is `closure_backed_zero`. The form-field explain for that disposition is the denial sentence, and the page template appends it.
- Fix: Keep the denial sentence only for the answer value `no`. When the answer is `yes` and that term has no members, say the line is zero because no sale of that term was recorded. One sentence cannot cover both authorities.

### adr-0084-still-proposed

- Severity: note
- File: `docs/adr/0084-grouped-source-closure.md:3`
- Claim: The record is still proposed. Its own consequences say the owner accepts it before the PR goes ready, and that the text is not authority until then. The sentences match the code. This review does not treat proposed status as a computation defect.
- Reproduction: Read the status line. Compare decisions 1–3 with the citations in section 4.
- Fix: The owner accepts the record, or the plan keeps the PR draft. No code change follows from the status alone.

### covered-ltcg-not-on-this-package

- Severity: note
- File: `packages/tax/loader.py:116`
- Claim: `COVERED_FLAG_REFUSAL_OBJECTS` names `tax.us.2025.f1099b.covered-ltcg-txn`. Core v79 publishes no such member, so the dedicated sentence cannot be shown for that object through this package. The covered long-term path was measured live. The other three published object types share the same function and were not each re-run here.
- Reproduction: Read the map. Search the v79 package for a covered-ltcg member publisher.
- Fix: Leave the fifth key until a package publishes that object, or drop it from the map that v79 names. Either way, say which objects this package can actually refuse.

### line-7-unasserted

- Severity: note
- File: `tests/test_noncovered_sales_v79.py:2021`
- Claim: `_line_map` does not include Schedule D line 7. The live page matches the hand sum (0, −6,000, 0 on the three committed cases; 2,000 on the four-sale return). No expected dollar is wrong. The test gap is that a wrong line 7 would still pass the digest those cases assert.
- Reproduction: Compare `EXPECTED["v79"]["lt_gain"]["lines"]` with the watched line list in the charter. Line 7 is absent.
- Fix: Add line 7 to the digest for the cases that publish a short-term total.

## Limitations

- The 2025 Form 8949 and Schedule D instruction PDFs are not in this workspace. Citation citizens for those lines are stubs. The hand figures use the milestone law note plus the published 2025 standard deduction, tax-table midpoint, ordinary brackets, and 0 percent long-term threshold.
- Core v78 was not re-rendered. The switch test checks that earlier packages do not name the refusal map. Gating in the code that was read is by v4 mapping schema and by the v79 map. Ungated derivation hunks (presentation projection, source authority, the tax loader, package validation, the runner, marshal, authorization closure) were read at the functions cited above and were not exhaustively diffed line by line against `github/main`. This review does not claim a byte-identical v78 render from a fresh run.
- `boundary_no_with_member`, duplicate horizon, a late `yes` after a member, and the covered short-term and covered wash objects were read from the admission code and, where present, from the committed expected dispositions. They were not re-executed on the coordinator in this review.
- On a pure noncovered return the Schedule D form-field lines publish and the Schedule D attachment disposition is `guard_inapplicable`. The four-sale return publishes that attachment. Form 8949 publishes in both, and the box B and E tie-out texts carry the column amounts. The attachment `when` was not diagnosed, so this is not a finding.
- The full suite was not run. CI on the commit remains the gate of record.

## Verdict

**ready.** The blocking list is empty.

The should-fix explain shows the filer a denial they did not make, on a line whose published amount is the lawful zero. It does not refuse the return and it does not mis-tax it. The plan's own gate still withholds a ready PR until the owner accepts ADR-0084.
