# Track 1 evidence for sale question names

On core v109 and compatible successors, the saved page names eligible Box C
and F sales beside existing proceeds, basis, and wash-sale questions. The
projection uses the evaluator's shared pairing test for proceeds and basis,
and current member validation publications for wash-sale fixes. Before
attribution, it reconciles the supplied currency set with projected state
and verifies each wash-sale witness against its content-derived ID. It
counts answered peers' recorded labels for collisions, including labels
that are the peers' own entity IDs. Projector, validator, text observer and
renderer treat Unicode whitespace and format characters as blank. A single
sale, indistinguishable labels, or incomplete attribution leaves the
generic reason. Basis consistency keeps the existing basis question.

The replay resolves the parent of the sole commit whose subject starts
with `build(sale-question-names)` from Git history. It loads that
projector alongside the production projector and uses the same live
coordinator and run ID for both. Expected names and their positions are
fixed by case. The comparison checks the full saved model after those
insertions and checks the report structurally, with exact types. It also
checks where the original question references land and compares the class
and path-masked message on failed saves. Both sides must match the landed
baseline's outcome census. The recorded error case keys must also match
the digest established from the member-reads-once timing and line16-names
Track 1 evidence. The DOM probe executes the production renderer and
compares each section's blocked reason text and sale prefixes in order.
It checks that each prefix sits beside its expected question, and that
sections that expect no prefix display none.

One replay used 10 workers across 49 shards. There were zero unexpected
differences. The renderer matched 61,060 sections, including 226 with
sale names.

| Corpus | Lists | Matching saves | Matching errors | Lists gaining names | Names added |
| --- | ---: | ---: | ---: | ---: | ---: |
| Recorded | 775 | 691 | 84 | 0 | 0 |
| Synthetic | 19 | 19 | 0 | 7 | 352 |

The replay rejected mutations to name text and order, a removed name and a
removed named reason, a spurious name, a redirected question reference,
a changed block code, changes to named and unnamed saved surfaces, changes
to outcomes and error details, and an incorrect changed-list total.
Repair controls also rejected the same setup error replacing a saved
return on both sides, a compensated save/error swap that preserved
the census, a spurious prefix on a single-sale page, and a correct
prefix beside an unrelated question.

The 59 targeted tests passed. Before the repair, ten focused checks failed
across the four code findings. They exercised both boxes with two and three
sales, answered peers, label collisions, the single-sale and consistency
cases, and display-only validation. They also removed or corrupted the
inputs used for attribution on published v108, adopted v109 and a live
synthetic v110 that retains the v109 member pins. The fast lane passed
2,333 tests with eight skips, and mypy passed. The full suite is delegated
to CI verify.

Set `SALE_REPLAY_SUMMARY` to an ignored output path and run from the repository root.

```sh
python3 docs/phases/engine-breadth/milestones/sale-question-names-evidence/track1_replay.py \
  --workers 10 --out "$SALE_REPLAY_SUMMARY"
```

[Replay script](track1_replay.py) · [Replay summary](track1-replay-summary.json)
