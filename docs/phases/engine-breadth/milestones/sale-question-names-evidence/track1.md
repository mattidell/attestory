# Track 1 evidence for sale question names

On core v109 and compatible successors, the saved page names eligible Box C
and F sales beside existing proceeds, basis, and wash-sale questions. The
projection uses the evaluator's shared pairing test for proceeds and basis,
and current member validation publications for wash-sale fixes. It preserves
the recorded label as display text. A single sale, indistinguishable
labels, or incomplete attribution leaves the generic reason. The basis
consistency cases retain their existing basis question.

The replay resolves the parent of the sole commit whose subject starts
with `build(sale-question-names)` from Git history. It loads that
projector alongside the production projector and uses the same live
coordinator and run ID for both. Expected names and their positions are
fixed by case. The comparison checks the full saved model after those
insertions and checks the report structurally, with exact types. It also
checks where the original question references land and compares the class
and path-masked message on failed saves. The page probe executes the
production renderer and checks the ordered prefixes where names appear.

One replay used 10 workers across 49 shards. There were zero unexpected
differences. The renderer matched the name prefixes on 226 sections.

| Corpus | Lists | Matching saves | Matching errors | Lists gaining names | Names added |
| --- | ---: | ---: | ---: | ---: | ---: |
| Recorded | 775 | 691 | 84 | 0 | 0 |
| Synthetic | 19 | 19 | 0 | 7 | 352 |

The replay rejected mutations to name text and order, a removed name and a
removed named reason, a spurious name, a redirected question reference,
a changed block code, changes to named and unnamed saved surfaces, changes
to outcomes and error details, and an incorrect changed-list total.

The 49 focused tests passed. They exercised both boxes with two and three
sales, answered peers, label collisions, the single-sale and consistency
cases, and display-only validation. They also removed or corrupted the
inputs used for attribution on published v108, adopted v109 and a live
synthetic v110 that retains the v109 member pins. The fast lane passed
2,330 tests with eight skips, and mypy passed. The full suite is delegated
to CI verify.

Set `SALE_REPLAY_SUMMARY` to an ignored output path and run from the repository root.

```sh
python3 docs/phases/engine-breadth/milestones/sale-question-names-evidence/track1_replay.py \
  --workers 10 --out "$SALE_REPLAY_SUMMARY"
```

[Replay script](track1_replay.py) · [Replay summary](track1-replay-summary.json)
