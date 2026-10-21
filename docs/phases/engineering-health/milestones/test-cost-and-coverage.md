<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "test-cost-and-coverage",
  "status": "Closed on this branch. Live claim applicability uses the return's own current projection; cold and historical reads remain fresh. No tests were removed. Case measurements and their limits are recorded separately from publication CI.",
  "retrospective": "docs/milestone-retrospectives/2026-10-21-test-cost-and-coverage.md",
  "scope": [
    "identify repeated engine work and distinct assurance after fold-local lattice reuse",
    "avoid a redundant current applicability fold inside one live return",
    "preserve cold reads, historical source binding, saved results and test coverage"
  ],
  "non_goals": [
    "no changed tax treatment, source-use contract, schema or durable state",
    "no test cull, weaker CI, partial catalog or application split",
    "no cross-run cache, substituted historical state or skipped validation"
  ],
  "deep_reads": {
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/test-cost-and-coverage.md",
      "docs/phases/engineering-health/milestones/test-cost-and-coverage-evidence/measured-applicability-reuse.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-21-test-cost-and-coverage.md"
    ]
  }
}
-->

# Less Repeated Work, the Same Defects Caught

Milestone key: `test-cost-and-coverage` · Engineering Health · closed on this
branch. Publication status belongs to PR #213 and its exact-head checks.

## Purpose

Tests should spend time exercising behavior that could be wrong, rather than
rebuilding the same information. The previous milestone made workspace replay
cheaper. This milestone investigated what still costs time, whether expensive
tests protect different defects, and whether a smaller amount of work could
produce the same trustworthy result.

A live return was replaying the whole workspace history once to calculate the
return and again to check whether recorded student-loan relationships still
applied to their sources. The second current read now uses the state the
return already read. Checks about an earlier point in history still read that
earlier point. Nothing is retained for the next return.

## Actions completed

1. Distinguished CPU and repeated work from waiting for CI or running a
   smaller selection of tests.
2. Read the retained post-optimization profile's callers and a bounded sample
   of tests, their fixtures and actual assertions before ranking changes.
3. Compared engine reuse, test overlap and component-suite boundaries. The
   sample justified no test removal or application split.
4. Selected one-invocation applicability reuse after independent review of
   its authority, aliasing, historical checks and proposed evidence.
5. Built the shared private computation and real-coordinator regression;
   preserved the existing story, control, refusal and parity assertions.
   Independent semantic review found no material issue.
6. Kept ordinary timing, diagnostic counts and publication verification
   separate; retained the bounded measurement note and its limitations.

## Evidence for the choice

The previous milestone's retained synthetic story profile counted 199
`findings.project` folds and 11 live returns. Test-side forward and reference
derivations together used about 1.4s cumulative; neither caused those folds.
The folds came from recording, review, live coordination and test setup.
Eight cold applicability reads used about 7.218s cumulative, largely
reprojecting a current state the coordinator already had. These nested,
instrumented times are not ordinary CPU or suite-saving estimates.

The story and its amount-only control protect different correction, recovery
and explanation behavior. Source inspection also sampled the mortgage
lifecycle, nominee Track 2 and student-loan saved-account-reference tests;
they exercise different integration seams. No current module-cost ranking or
redundancy proof was established for those samples. Shared output amounts
did not justify deleting their distinct witnesses.

Package validation was a larger profile item, about 22.674s across the 11
returns. It already uses content-addressed schema-validation memoization;
neither a gate skip nor another cache follows from that total. Current and
historical lattice reads were also significant, but need their own lifetime
and preservation evidence. The selected current-read boundary was smaller
and easier to establish without changing authority.

## Track 0 adversarial closure

Independent design review found the bounded boundary ready for implementation.
Its obligations are preserved by the code and regression tests, not by a
review label alone.

| Observation | Authority and lifetime | Required change behavior |
| --- | --- | --- |
| Live current applicability rows | Exact local acts tuple, registry, projected state, derived currency and state-derived lattice, within one coordinator call | A new return reads its own changed acts; no prior object or rows survive. |
| Public cold applicability rows | Fresh `_current` projection, currency and lattice | Calls without the live observation still read afresh. |
| Admission-time and reviewed-predecessor binding | Actual historical prefix and its currency | A current state never substitutes for the earlier finding identity, amount, correction id or single-use evidence. |

- Authority-lifecycle: PASS — the three observations above retain their
  separate authorities; the shared row algorithm changes no source-use rule.
- Empty/nonempty behavior: PASS — no current inclusion keeps the existing
  empty fast path. A valid current inclusion keeps its exact source row; an
  unbound source rewrite stays unresolved. No family-absence or completeness
  authority is introduced.
- Change and late authority: PASS — reviewed corrections, wrong/reused
  evidence, legacy admission, withdrawal/restoration and successive live
  states retain their existing behavior. History is not erased or retargeted.
- Neighboring dependencies: PASS — no new prerequisite for marshalling,
  standalone cold readers or unrelated statements; historical readers remain.
- Claim equivalence: PASS — the finding/source identities, predicate loop,
  correction bindings and output row shape are unchanged.
- Integration surface: N-A for a new producer — no externally bound symbol,
  consumer cardinality or schema changes. Existing saved line 21 is tested
  through the real coordinator, not a new stand-in.
- Known semantic limitations: no unresolved implementation finding. Existing
  product limitations are unchanged; no wider cache is licensed by this result.

## Track 1 — one live observation

The coordinator creates one normalized local acts tuple, projects it and
computes currency. If current statement inclusions exist, its private helper
builds the lattice from that same state's `fact_state` and calls the shared
row computation. Public `current_claim_applicability(acts, registry)` keeps
its existing signature and fresh `_current` read, supplying its already-built
lattice to the same computation. The private route accepts no precomputed
applicability rows and has no cross-run cache.

Normalization is a shallow copy, not a new deep-immutability contract. The
projector and synchronous readers do not mutate the act dictionaries; the
live regression also checks the original input remains unchanged.
Historical admission/predecessor functions, append refusal and correction
evidence checks remain intact. No new ADR, schema, stored record or tax rule
was needed.

## Preservation evidence

- A recorded 1500-to-unscoped-1900 source rewrite enters real
  `live_coordinate_run`. Delegating wrappers observe the exact local tuple,
  registry, state, currency and real lattice reaching the shared computation.
  They require no `_current` and one full-current projection, counting an
  equal deep-copied full sequence as a second fold rather than evading it.
  The coordinator's own publications show `applicability-unestablished`, its
  inclusion row is `unresolved-applicability`, and saved line 21 is blocked.
- Manual current-input comparisons establish full-row agreement with the
  fresh cold API. The separate 1775-to-2900 bypass case is row evidence, not
  a coordinator marker witness.
- A legacy missing-confirmation fixture executes the real admission-prefix
  reader before and after a same-identity source change, without retargeting.
  The valid reviewed correction executes the actual predecessor reader.
  Wrong/reused evidence, refused writes and saved history remain covered.
- Existing empty and withdrawn-inclusion cases, unrelated statements, the
  amount-only worksheet control, financing withdrawal/restoration/re-answer,
  interrupted save/recovery, saved explanation and forward/reference parity
  remain. Financing withdrawal and inclusion withdrawal keep distinct reasons.

The unoptimized live path's second fold was corroborated by source inspection;
the new test cannot run unchanged on that old code because its private helper
did not exist. No executed old-base differential is claimed. Focused semantic
checks passed across the original 25 passing cases and the final repaired
live-wiring test. Repository mypy, lint and diff checks passed. Full CI is
the publication gate, not replaced by those focused results.

## Measurement and remaining work

The [measurement note](test-cost-and-coverage-evidence/measured-applicability-reuse.md)
records the unchanged story/control commands, ordinary CPU and wall time,
separate diagnostic counts, raw-output retention and limits. It does not
establish a whole-suite speedup. PR #213 carries final publication review and
the curated head's own CI status.

No test was removed, skipped or weakened. No component-only CI gate or
application packaging split was selected. Dynamic packages and shared
kernel/derivation paths still require the full integration gate.

The next milestone is unselected. Remaining candidates are package-validation
cost, repeated current versus historical lattice construction, defensible
test replacements and useful local component commands. Partial catalogs,
broader caches and CI sharding need their own evidence; sharding shortens
waiting without necessarily reducing CPU. This milestone changes no tax
coverage. See the [retrospective](../../../milestone-retrospectives/2026-10-21-test-cost-and-coverage.md)
and [roadmap](../engineering-health-roadmap.md).

## Publication review scope

The independent final review checks the exact curated range against
`origin/main`: production and test equivalence to the reviewed implementation,
unchanged historical/cold authority and saved behavior, atomic commit
boundaries, schema history, removal of working artifacts, coherent closed
state, safety, measurement claims and their limits. Final acceptance still
requires green `verify` on the exact pushed candidate. Review and measurement
are not substitutes for that check.
