# Track 1: unconfirmed families name their question (core v75)

An unconfirmed constrained family names its existing completeness question, and
a blocked selection line names that question beside its selection reason, from
core v75. Earlier cores stay as they are. Synthetic demo data only.

## Switch

`unconfirmed_family_names_closure_question` in `packages/tax/loader.py` is the
switch. It is on when the adopted package is `tax.us.2025.package.core-calculations`
at v75 or later, and off for every other package. Nothing in a schema or a
published file carries it. The runner reads it from the run's adoption pin.
The presentation projection reads it from the same function, using the
package id and version `live_coordinate_run` already resolved.

Core v75 also has a companion-declaration entry that shares v74's declaration.
That entry does not turn the switch on. It keeps v75 from falling back to the
global companion maps, which would refuse amounts v74 admits.

## Engine

With the switch on, `_evaluate_family_validation` records `SOURCE_SET_UNCLOSED`
naming the family id when that family is not admitted. That is the code
`require_closed` records. The existing closure walk then copies the family's
closure question. An admitted family still validates as it does today. With
the switch off, the unadmitted block stays `DEPENDENCY_ABSENT`.

## Projection

With the switch on, a blocked selection line still gets its selection reason.
The closure walk then runs, and any question it returns is added beside that
reason. The sentences are sorted and a question the selection already states
is not repeated. Selection reasons keep their fact id and statement label.
With the switch off, a selection reason still skips the walk.

Form 1099-K's Schedule 1 lines are the case: the root is already
`SOURCE_SET_UNCLOSED` on the family, and the selection reason is the
unanswered single-sale sentence. From v75 both sentences are named.

## Successor

`tools/package_successor.py` built core v75, registry v73, and release v73
from v74 / v72 / v72 with `v74-to-v75.json`. No member, binding, or entrypoint
changed. The registry's citizen list is unchanged and adds only the v75
package entry, between v74 and v8. The build reported no inherited
inconsistencies. The release's registry hash is the sha256 of
`published-packages.v73.json`.

## Lines that gain a question

`tests/test_closure_question_coverage.py` measured these against the P0 survey.

Each wash-sale family, with and without a member, blocks 32 lines. On v74 none of those lines names the question. On v75 every one of them does. That is 128 line instances: `f1099b.covered-w-st` and `f1099b.covered-w-lt`, each with no member and with one member.

Form 1099-K with one member blocks 30 lines. On v74, `sch1-10` and `sch1-top` name only "The question regarding single item sale scope has no current answer." On v75 those two lines also name "Have you recorded every gross payment amount in box 1a of every Form 1099-K you or your spouse received for 2025 for personal items you sold?" The other 28 lines are unchanged. That is 2 line instances.

Form 1099-K with no member already names its question, including on those two lines, and stays that way. The sample `f1099int.b1` (both variants), `w2` (both), `f1099b.covered-w-st-basis` (no member), and `f1098` (no member) matches the survey on v74 and on v75, in published amounts and in presentation.

A confirmed base return, and an admitted covered short-term wash-sale family, publish the same amounts and the same presentation on v75 as on v74.

The cases above gain the closure question on 130 line instances.

## Checks

`pytest tests/test_closure_question_coverage.py`: 19 passed.

`python3 -m mypy packages/derivation/runner.py packages/derivation/presentation_projection.py packages/derivation/live.py packages/tax/loader.py tests/test_closure_question_coverage.py`: no issues found in 5 source files.

`pytest -m "not live"`: 1645 passed, 8 skipped, 3914 subtests passed.

`python3 -m mypy tests/test_capital_gain_distributions_line7a_line7b_prerequisite.py`: no issues found in 1 source file.

`pytest`: 4247 passed, 24 skipped, 7986 subtests passed.

No earlier-core golden moved.
