# Track 1 evidence

## Build and adoption

I adopted the interrupted builder's production and test commits `52446b436`
and `929272607`. The worktree was clean at pickup. The build adds
`answer-explanation.v1` and `artifact-package.v45` and adopts the four
approved Exception 1 explanations in core v109, registry v107 and release
v107. The manifest diff adds exactly two entries with matching checksums.
The published package, registry and release match the P0 scratch digests.
[Generation record](track1-build.json)

In `8af3c673f` I made the projection require exactly one current finding per
fact, including when two findings give the same answer. The projection now
appends the sorted, unlinked explanation sentences after the existing
reason indices and question references are assigned. Package validation
uses the existing index for the pinned fact type's enum, which also covers
standalone fact types. I moved the rejection controls to small synthetic
packages in the fast lane and replaced the live computing control with a
recorded sale.

## Published replay

[replay.py](replay.py) ran 18 fresh shards across nine workers. The v108
run used the projection from the parent of the `build(line16-next-step)`
commit. The v109 run used the current production projection. The comparator
checked the saved model and report and admitted each added explanation only
when the line was blocked and its linked question had exactly one current
finding with the declared fact type, version and value. The run used no
checkpoint inputs.

- **801 passed, 0 failed and 0 unexpected differences** across 775 recorded
  and 26 probe lists. Of these, 717 had expected changes and 84 returned
  identical errors on both cores.
- The same 25 lists as P0 gained explanations. The replay counted 448 C1,
  280 C2, 224 C3 and 224 C4 additions across 700 field reason lists. Values,
  dispositions, block codes, question links and recorded rows matched.
- The failing control appended the approved C1 “no” explanation to blocked
  line 16 on the unanswered C1 probe. The comparator rejected both the
  added sentence and the corresponding change to the reason list order.

The [Track 1 replay summary](track1-replay.json) records the affected lists,
code and content hashes, and control result. The [P0 replay](replay.json)
records the earlier scratch run.

## Verification

- The fast tests cover both schema checksums, package and registry additions,
  release linkage, loader switches, validation and dependency edges for
  bundled and standalone fact types, and exact-fact and bare-type lookup
  when several findings or facts are current.
- Live tests exercise one, two and four failed criteria, a corrected answer,
  an unanswered criterion, the personal-loss boundary and a recorded sale.
  The saved-page DOM check draws the explanations beside the existing links.
- The focused run, including the schema registry, consumer, switch and
  envelope tests, passed 90 tests. The final fast package module passed 18.
  Mypy on eleven touched Python files, governance lint and the
  `github/main..HEAD` envelope scan passed.

I interrupted the initial full-suite invocation near its 45-minute limit
with 2,536 passed, 13 skipped and two Chromium timeouts. Six subsequent file batches
accounted for 6,106 of the 7,958 collected tests, with 6,075 passed,
25 skipped and six Chromium timeouts. Batch seven ended partway through.
The foreman deferred the remaining local batches to CI `verify`, the
full-suite gate of record.

All seven unique browser tests that timed out across those runs passed when
retried by node ID on `8af3c673f`. The six batch-five tests also passed in
focused runs against the starting commit `b9d529f7d`. The saved-graph
browser test reproduced its timeout on that starting commit and passed in
batch six on the Track 1 commit.

## Closeout

The focused and batched tests ran on the milestone branch at `8af3c673f`.
Main remained at core v108 after PRs #318 and #314. PR #314 also touches the
presentation projection. The foreman will reconcile the shared projection
at closeout and use CI `verify` for the integrated candidate. The foreman
recorded both schema-intent proposals, `answer-explanation.v1` and
`artifact-package.v45`, on `milestone-schema-ledger` in `34aab8c4d`.
