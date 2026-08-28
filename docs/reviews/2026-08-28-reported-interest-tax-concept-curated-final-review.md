# Final publication review — Reported Interest to Tax Concept Vertical Slice

**Seat:** author-independent Reviewer (curated closeout / publication)
**Object:** `milestone/tax-concept-derivation-phase-definition` at
`05587ce17b7601944d4412e89ea4bcbeba0cb517`
**Range:** `origin/main` (`9159a13d261f5005523ad58f8893ffffd735f204`)..`HEAD`
**Date:** 2026-08-28
**Source ref:** `HEAD` (orientation commit SHA matched Git)

## Curation note (added after the original review)

The branch was linearized after this review first passed: the long chain of
per-round adversarial-review and repair commits was squashed into one commit
per complete unit of work, and the `ours`-merge that had kept the it6
exhibit commit reachable without promoting its tree was replaced by rebasing
that prototype line directly into the branch, followed by an explicit
removal of the prototype files in the closeout commit. The tree this review
inspected is byte-identical to the tree at the original commit this record
first described; only the commit graph shape and the SHAs below changed.
The `it5` and `it6` exhibit tags were moved to their new commits (content
unchanged); `it1`-`it4` were not touched. Sections below describing the
graph shape, tag table, and SHAs reflect the curated history; the verdict,
checks, and evidence findings are unchanged from the original pass.

This record does not reopen the settled invariant that a displaced producer
cannot support a current explanation, and it does not enlarge the remaining
product question about the split state.

## The box

- **Enters:** one synthetic 2025 Form 1099-INT box-1 item, one
  accrued-interest-at-purchase circumstance, a distinct box-3 TI-A1 coverage
  probe, official-source treatment (Pub. 550 against IRC § 61(a)(4)), and
  exhibit `exhibits/reported-interest-tax-concept/it6`.
- **Authority:** paper treatment plus executed prototype comparison; prototype
  shapes are evidence, not production contracts.
- **May publish:** a durable milestone record, archived charter/examination,
  closed lifecycle pointers, and a frontier-reduction method. The durable
  conclusion is that necessity for a separately recoverable item-level
  determination is **not established**.
- **Must remain outside:** new citizens, published schemas, ADRs, production
  representations, prototype working files on the milestone tree, working
  it3/it4/it5 independent-review files, and personal data.
- **Unchanged neighbors:** published schema bytes and checksums; it1–it5
  exhibit tags (it5 retagged to its curated SHA, content unchanged); the
  incumbent production interest path.

## Verdict

**READY**

No blocking findings. No non-blocking findings that fail a chartered check.

## Blocking findings

None.

## Non-blocking findings

None measured against the chartered checks.

## Checks

### 1. Commit range vs the tree

Tree diff `origin/main...HEAD` and two-tree `origin/main HEAD` are identical:
13 documentation files, `2507` insertions / `111` deletions (unchanged from
the original pass; the curation rewrote history, not content).

- `PROJECT_PLANNING.md`
- `docs/archive/2026-08-28-reported-interest-tax-concept/README.md`
- `docs/archive/2026-08-28-reported-interest-tax-concept/prototypes/reported-interest-tax-concept/charter.md`
- `docs/archive/2026-08-28-reported-interest-tax-concept/prototypes/reported-interest-tax-concept/examination.md`
- `docs/milestone-retrospectives/2026-08-28-reported-interest-tax-concept.md`
- `docs/milestones/reported-interest-tax-concept/README.md`
- `docs/milestones/reported-interest-tax-concept/accrued-interest-item-model.md`
- `docs/milestones/reported-interest-tax-concept/incumbent-representation.md`
- `docs/milestones/reported-interest-tax-concept/synthetic-case-specification.md`
- `docs/phase-state.md`
- `docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md`
- `docs/phases/tax-concept-derivation/tax-concept-derivation-overview.md`
- `docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md`

Commit walk `origin/main..HEAD` after curation: linear, one commit per
complete unit of work (phase establishment; treatment establishment; the
seven-round adversarial-review repair; one commit per prototype iteration
it2/it3+it4/it5/it6; the frontier-reduction doc; closeout; this review).
The it5 and it6 prototype commits are direct ancestors of HEAD; their
prototype files are added on those commits and removed by the closeout
commit, so HEAD's tree carries none of them. No merge commit remains.

### 2. Contract preservation

No citizen, published schema, ADR, or production path appears in the range.
`git diff --name-only origin/main HEAD -- packages/ docs/adr/` is empty.
Durable conclusion in
`docs/milestones/reported-interest-tax-concept/README.md`, the plan, phase
state, roadmap, retrospective, and archived examination: **necessity is not
established; no representation is recommended on necessity grounds.**

### 3. Published-schema integrity

`git diff origin/main HEAD -- 'packages/schemas/**/published.json'
'packages/schemas/**/*.schema.json'` is empty. No published schema bytes or
checksums were mutated.

### 4. Working-review removal

HEAD `docs/reviews/` contains only pre-existing unrelated files
(`2026-08-05-form1099int-box8-line2a-final-review.md`,
`2026-08-08-form1099r-ira-line4b-curated-final-review-charter.md`,
`README.md`) plus this record. No working it3/it4/it5 independent-review
files remain at HEAD.

### 5. Prototype code absent from HEAD

`git cat-file -e HEAD:prototype/reported_interest/run.py` and
`HEAD:tests/test_reported_interest_prototype.py` fail. Those paths exist on
the it6 exhibit commit (an ancestor of HEAD) and are removed by the closeout
commit that follows it, so they are not in the HEAD tree.

### 6. Exhibit tag it6; it1–it4 not rewritten, it5 retagged

`exhibits/reported-interest-tax-concept/it6` is an annotated tag peeling to
`a4ebf48aa409ddd0e2a7d1d8a32dc5290b220646`, an ancestor of HEAD
(`git merge-base --is-ancestor` exit 0). `exhibits/.../it5` was moved to
`e60757f8295dde1565b78c8631365591910a3cfc`, also an ancestor of HEAD; its
tree content is identical to the pre-curation it5 commit.

| Tag | Object | Peel |
| --- | --- | --- |
| it1 | lightweight commit | `0d0784364830e796bfd877c6ef775ba9ad7ab845` |
| it2 | annotated | `14e50d3e21e3102ebfb6d4bc184da27ea2242104` |
| it3 | annotated | `865486cd0e3a0c44adaf55be4fb658845e380b0a` |
| it4 | annotated | `c374c809e2bf009d134ab85ced3b0eb01a8b4a9b` |
| it5 | annotated | `e60757f8295dde1565b78c8631365591910a3cfc` |
| it6 | annotated | `a4ebf48aa409ddd0e2a7d1d8a32dc5290b220646` |

it5 and it6 are ancestors of HEAD, by direct rebase rather than a bookkeeping
merge. it1–it4 are not; they remain tagged historical exhibits off the
pre-curation first-parent line, exactly as before curation.

### 7. Archive topology

`docs/archive/2026-08-28-reported-interest-tax-concept/README.md` is a boundary
README: evidence not authority; names the curated it6 peel SHA; states
it1-it4 were not rewritten, it5 was retagged with unchanged content, and
prototype code is not in the archive or on the branch (the it5/it6 commits
are ancestors of the branch, but their files are removed by the closeout
commit that follows them). Charter and examination live at
`prototypes/reported-interest-tax-concept/{charter,examination}.md`.
Milestone README and synthetic-case-specification inbound links target those
archive paths. `docs/prototypes/reported-interest-tax-concept/` is absent from
HEAD and from durable-doc link text.

### 8. Closed lifecycle

Both `docs/phase-state.md` and the plan YAML have
`milestone_state: closed`, retrospective
`docs/milestone-retrospectives/2026-08-28-reported-interest-tax-concept.md`,
`current_role: Foreman — between-milestones selection`, next milestone
unselected, and no `initial_briefing_follow_up` key.
`python3 tools/foreman_context.py --ref HEAD --format markdown` reports
milestone state **closed** and next transition **selecting a new milestone**.
JSON: `"initial_briefing_follow_up": false`.

### 9. Frontier-reduction method

`PROJECT_PLANNING.md` § **Frontier Reduction and Direct-Build Routing** is
present. Phase overview, roadmap (Later-Year Basis Consequence Frontier), and
milestone README cite
`PROJECT_PLANNING.md#frontier-reduction-and-direct-build-routing`. The
diff vs `origin/main` adds that section and allows a durable disposition
without manufacturing an ADR.

### 10. Data safety

- `python3 tools/envelope_scan.py --range origin/main..HEAD` — exit 0
- `python3 tools/governance_lint.py` — `governance lint: conformant`
- `git diff --check origin/main..HEAD` — exit 0

Synthetic `demo.*` identities only in the exhibit fixtures inspected.

### 11. Durable claims vs executed it6 evidence

Inspected from a detached worktree at the curated it6 SHA
(`a4ebf48aa409ddd0e2a7d1d8a32dc5290b220646`, removed after measurement; no
prototype files were placed on the milestone branch). Tree content at this
SHA is identical to the pre-curation it6 exhibit; all figures below match
the original pass exactly.

`python3 -m pytest tests/test_reported_interest_prototype.py -n0` →
**40 passed**. Focused source-report tests
(`source_report`, `evaluate_reported_omits`, `ti_a1_source_report`,
`ti_b2_source_report`, `ti_a1_refuses`, `ti_a1_is_the_box`) → **6 passed**.

Direct TI-B2 / TI-A1 source-report provenance, all four packagings:

- TI-B2: amount `1200`; reads are the statement amount, payer, and
  obligation; `authority=()`; `coverage_id=None`;
  `accounted()` = `{authority:omitted, coverage:omitted}`; treatments
  present (A/C/E includible+basis, B determination).
- TI-A1: amount `840`; distinct `stmt-b` box-3 reads; same omitted
  authority/coverage tokens; treatment `SLICE_COVERAGE_UNSUPPORTED`; no
  treatment artifacts; source report remains.

`evaluate_reported` at it6 calls `_run(..., authority=(), coverage_id=None,
coverage_version=None)`. That matches
`docs/milestones/reported-interest-tax-concept/README.md` (“support is the
exact statement reads; tax authority and accrued-interest coverage are
omitted. On TI-A1 the treatment refuses and the reported $840 remains”).

Unamended later-year scores match the archived examination table exactly:

| Packaging | artifact-object-only | currentness | object-store access | full-workspace |
| --- | --- | --- | --- | --- |
| A | 3/6 | 5/6 | 3/6 | 6/6 |
| C | 4/6 | 6/6 | 4/6 | 6/6 |
| E | 3/6 | 5/6 | 4/6 | 6/6 |
| B | 4/6 | 6/6 | 4/6 | 6/6 |

Task 5 is recorded-partition recovery; task 6 without a currentness grant is
unknown (fails the task), and with a grant reports
`fact_version_current=...` without treating reconstruction as currentness.
That matches the durable README and synthetic-case-specification.

### 12. Relative Markdown links

All 17 relative Markdown links in the curated milestone, archive, phase,
retrospective, and phase-state docs resolve, including
`PROJECT_PLANNING.md#frontier-reduction-and-direct-build-routing` and the
archive charter/examination inbound links. Named backtick paths in those
documents exist on disk.

## Qualitative standard

**Meaning.** The published claim is a bounded negative: this slice does not
establish that a new item-level citizen is necessary. Arithmetic is shared
across packagings; remaining differences are later-year recovery and
currentness under named in-memory grants.

**Authority.** Paper treatment (Pub. 550 / IRC § 61(a)(4)) plus exhibit it6.
No ADR or schema is cited as adopted.

**When authority changes.** Source and circumstance corrections were executed
in the exhibit; rule/authority/coverage/reporting succession were not, and
the durable record leaves them open.

**Failing evidence.** A HEAD tree containing `prototype/reported_interest/`
or the it3/it4/it5 review files, a published-schema diff, an it6 peel other
than the curated SHA above, a rewritten it1-it4 tag or an it5/it6 retag with
changed content, a recommendation of a production representation, or
TI-B2/TI-A1 source-report `accounted()` carrying tax authority/coverage
would have failed this review. None of those were observed.

## Charter contradictions

- Orientation `--role reviewer` cannot load this closed plan (no `review`
  action). The dispatch charter still described the object; HEAD matched.
- `gh` was not installed; PR listing was not run. Divergence was taken from
  Git and `foreman_context.py`.
