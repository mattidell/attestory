# Track 1 — Payer and broker names on repeated statement labels

The saved page appends a recorded payer or broker name to an attributed
statement question when the exact statement label is shared by current
statements of the same form and tax year. Each statement in the group
must have one current party of the expected kind, and the names must
distinguish all the statements after case folding and whitespace
collapse. An answered statement still counts. The page preserves the
recorded spelling and spacing in the prefix.

Forms 1099-INT, 1099-DIV, IRA-family 1099-R and 1099-G use the payer in
the attributed answer identity. Form 1099-B box 4 and box 7 use the
broker from the sale findings read by the originating pairing. A
current 1099-B statement anchor can establish a peer. SSA-1099 remains
statement-only.

## Inputs and controls

The focused tests in `tests/test_statement_payer_labels.py` exercise
each supported question with repeated labels, an answered peer, and
statement labels differing only in case or spacing. They also exercise
SSA-1099, compatible successor eligibility and the earlier-core gate.
The following controls remove or corrupt inputs used to display a name.

| Input | Control |
| --- | --- |
| Exact answer identity and adopted question version | Remove the question version or pin a successor with an extra key. Remove the target statement, year or payer key, or supply an out-of-contract year. |
| Originating paired block | Move the pairing to an inactive arm and produce the same missing type from a separate block. |
| Current findings and exact paired input pins | Retract a peer while omitting the precomputed currency argument. Make a paired pin stale, remove it, point it to a missing finding, or corrupt its version or origin. |
| Current same-form, same-year statement identity and plain label text | Blank a statement label, substitute another statement kind or move the peer's finding to another year. Distinct case and spacing stay distinct. |
| One party per statement, with agreement across contributing records | Give one statement contradictory parties or remove its broker key. Add another sale of the same statement and remove its pin or change its broker. |
| Current party of the expected kind and usable recorded name | Displace the party, change its kind, remove or blank its label, repeat the party identity, or supply equal or near-equal names. |
| Display-only saved reason | Remove or blank the statement or year, use a blank or non-string name, add an answer fact or member label, or reference the payer-labelled reason from a question group. |

The browser test in `tests/test_presentation_question_groups_v3.py`
asserts the complete visible question with a payer name containing
repeated spaces and an ampersand. It checks the absence of a question
group link.

## Full-surface replay

Run from the repository root.

```sh
python3 docs/phases/engine-breadth/milestones/statement-label-payer-evidence/replay_track1.py \
  --workers 9 \
  --out docs/phases/engine-breadth/milestones/statement-label-payer-evidence/replay_track1_summary.json
```

The script resolves the parent of the unique commit beginning
`build(statement-label-payer)` from `HEAD` history. Both projections
use the live coordinator with the same act list, run identity, core
v109, registry v107 and release v107. The shared run uses 38 shards.
The comparator checks the exact expected name at each reason index,
the order of the names, and each corpus's count of changed lists. It
compares the entire saved model and report after applying only the
expected insertions to the baseline. The shared full-surface snapshot
can alias generated identities when needed.

| Corpus | Lists | Successful saves | Matching errors | Lists gaining names | Names added |
| --- | ---: | ---: | ---: | ---: | ---: |
| Recorded | 775 | 691 | 84 | 0 | 0 |
| Synthetic | 21 | 21 | 0 | 10 | 174 |

The three controls remove one name, swap two names or add a name where
statement labels differ. The exact comparison rejects all three. The
page script renders the expected prefixes beside the original question
in the 20 synthetic cases with a labelled question. The all-answered
case has no labelled question. The text observer agrees at each expected
name position. The replay records zero other differences across the
saved model and report. [Replay summary](replay_track1_summary.json)
