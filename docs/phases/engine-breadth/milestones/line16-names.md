<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "line16-names",
  "status": "Open 2026-11-17. Track 0b passed; Decisions 10-11; Track 1 chartered.",
  "scope": [
    "on a return with Schedule D required and no sale recorded, Form 1040 line 16 and the lines that explain through it name the same questions as the other blocked fields",
    "every recorded return keeps its numbers, and every other line 16 block keeps its names unless P0 shows the added names are true there"
  ],
  "non_goals": [
    "no engine, schema, projection, page or kernel change unless P0 shows content cannot do it, and then only after the foreman decides",
    "no change to which answer a path needs or to any refusal code",
    "repeated shared questions on the page belong to the blocked-sale-pages milestone",
    "Path B, the boundary answers on lines 18-19 and the Form 8949 code L question stay parked"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/line16-names.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/line16-names.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/line16-names.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/line16-names.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Line 16 Names All Its Questions (2025)

Milestone key: line16-names.
Branch: milestone/line16-names-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-17.
Starting point: main at `e5e28402` (core v94, registry v92, release v92).
Expected target: core v95, registry v93, release v93.

## What we are trying to accomplish

On a return where Schedule D is required and no sale is recorded, most
blocked Form 1040 lines name eight questions: the four sale questions
and the four Exception 1 questions (preferential-base-reason, core v91).
Line 16 and four lines that explain through it (line 20, Schedule 3
lines 1 and 8, Schedule 8812 worksheet A line 5) name only the four sale
questions. A filer reading line 16 is not told that the Exception 1
answers can unblock it, though no sale answer can on a return with no
sale. The useful outcome is that line 16 names the same true questions
as the lines around it.

## What we know

- preferential-base-reason Decision 8 chartered a line 16 successor that
  names the eight questions only in that state, and its Track 1 parked
  it: in `line16-gate.json`, nine of the ten blocked-names-question cases
  were identical, but `exception1_personal_loss_8949` (an Exception 1
  "no" for a personal-item loss on Form 8949 with no sale recorded) sits
  in the same branch of line 16's guard and its names grew from four to
  eight. Values stayed blocked and equal.
- That case was protected only because it was a pinned blocked-names-
  question case, not because eight names are wrong there.

**What we do not know.** Whether the gap still reproduces on core v94;
whether, on `exception1_personal_loss_8949`, each of the eight questions
is true and answering it could unblock line 16 (if so, the case should
change; if not, the state must be told apart); whether a line 16 successor
alone fixes the four lines that explain through it; and whether any
computing return is affected.

## Actions the team will take

1. **P0: reproduce, trace and design** on published v94 and a scratch
   successor.
2. **Decide.**
3. **Track 0 adversarial closure.**
4. **Track 1 build.**
5. **Fresh review, repair, close.**

## Cases that will shape the design

Synthetic `demo.*` act lists: the four recorded honest returns that
gained the Exception 1 questions on core v91 (`m_2a_only_exc1_only2a_no`,
`m_empty_exc1_nolosses_no`, `m_empty_exc1_only2a_no`, `t4_s1_removed`);
the ten blocked-names-question cases, `exception1_personal_loss_8949`
first; Exception 1 answered yes and no; a recorded sale; a wage-only
return with no Schedule D as the neighbour; single, joint and separate.

## P0 result

P0 completed on published core v94 and a scratch-only core v95 successor;
see [evidence](line16-names-evidence/p0.md) and its scripts/JSON outputs.
The gap reproduces: five page fields name four questions while the other
23 blocked fields on each of the four recorded target returns name eight.
A line 16 v9 successor on existing rule-artifact v17 alone updates all five;
no dependant successor or engine/schema/projection/page/kernel edit is needed.

P0 recommends a narrower condition: required Schedule D, no represented sale,
and the existing no-Form-8949 answer **yes**. The personal-loss case records
that answer **no**; none of sixteen individual yes/no replacements unblocks
line 16. Local 2025 instructions support preserving its four names rather
than presenting Exception 1 as a truthful escape from the reported item.
All ten pinned cases remain identical on the narrow prototype. Single,
joint, separate and represented-sale neighbours retain their values.

The full foreground replay completed 775 lists with 9 workers in 1,405.37 s:
687 identical successes, 84 identical errors, 4 exact expected naming
changes, zero unexpected. No saved value, disposition, refusal code or row
membership changed. Eight classifier mutation controls pass. The part file
is retained outside Git and identified in the operational JSON handoff.

**Decisions before Track 0:** ratify the narrow naming condition; preserve
the protected personal-loss case; disposition the measured unanswered-boundary
behavior (line 16 uses its existing dependency fallback and shows the one
boundary question, with unchanged blocked disposition/code/value). The broad
alternative is retained as comparison evidence. Path B, lines 18/19, code L
and shared-question repetition remain parked as planned.

## Decisions

Foreman, 2026-11-17, on P0 (`line16-names-evidence/p0.md`).

1. **Narrow successor.** Build `rule.form1040-line16` v9 on
   rule-artifact v17 as prototyped: inside v8's existing four-name block,
   a required Schedule D with `schedule-d-boundary.no-form8949-sources`
   answered yes names the eight questions (four sale, four Exception 1);
   answered no keeps the four. Values, requires, pins and every other
   branch are v8's. No dependant successor: lines 20, Schedule 3 lines 1
   and 8 and Schedule 8812 worksheet A line 5 explain through line 16.
2. **The personal-loss case keeps four names.** A filer who reports a
   personal-item loss on Form 8949 cannot truthfully clear it through an
   Exception 1 answer (P0 answered each of the sixteen alternatives; none
   unblocks line 16), so naming them would point the filer at questions
   that do not help. The broad variant is rejected.
3. **Unanswered Form 8949 boundary.** When that boundary answer is
   missing, v9's guard falls back to line 16's existing dependency block,
   and the page asks the open boundary question instead of v94's four
   sale questions. Disposition, code and value are unchanged, and the
   boundary question is the one the filer must answer first. Accepted;
   Track 0 confirms the sentence the filer sees is true and enough.
4. **Parked items stay parked:** the code L question, Path B, lines
   18-19 and repeated shared page questions (blocked-sale-pages).
5. **Track 0** reuses P0's part file and closes the boundary states,
   filing statuses, late answers and corrections, and the drawn page.

## Track 0 adversarial closure

Completed the six-item charter on the unchanged narrow P0 scratch successor.
**FAIL on Item 1; not ready for Track 1.** See
[closure evidence](line16-names-evidence/track0-closure.md) and the six
`track0-*.json` outputs generated by `track0.py`.

| Item | Verdict | Evidence |
| --- | --- | --- |
| 1. Every name is a way forward | FAIL | 112 live runs; 49/56 target/name pairs have no truthful one-answer route onward. 42 never change the block for either answer; seven only change it through a false Form 8949 answer. |
| 2. Boundary states | PASS | 36 combinations; all 1,110 blocked field occurrences have an actionable sentence; full reason text retained without punctuation filtering. |
| 3. Late answers and corrections | PASS | Actual correction and retraction preserve history, displace old answers, do not revive the old yes, and use current sale answers. |
| 4. Neighbours | PASS | All 86 page fields on each of 16 cases match v94 in value, disposition and sentences, including every pinned case and all computing neighbours. |
| 5. Drawn page | PASS | Target and unanswered-boundary pages draw eight and one questions respectively on all five watched fields, with no safe-render alert. |
| 6. Replay reuse | PASS | Content bytes unchanged; 775 saved results strictly reclassified: 687 identical successes, 84 identical errors, four exact naming changes. Original wall time 1,405.37 s; no new live replay. |

The seven positive Item 1 pairs are only-box-2a on six targets and
no-capital-losses on `m_empty_exc1_nolosses_no`. The smallest measured repair
is to declare the corrective criterion for each state, rather than eight
names indiscriminately. It preserves Decisions 2 and 3 but needs a foreman
disposition of Decision 1's fixed-eight condition. No production or scratch
content was edited during this unit, and no larger-change stop was needed.
The foreman must disposition the failure before production build and decide
the standard for jointly mistaken criteria before extrapolating the repair.

## Track 0 disposition

Foreman, 2026-11-17, on `line16-names-evidence/track0-closure.md`.
Items 2-6 pass. Item 1 fails: on the four recorded targets and three
neighbours, 49 of 56 name/target pairs give the filer no truthful answer
that moves line 16. That includes v94's own four sale names, and it
equally describes the eight names `rule.selected-preferential-base` v11
already shows on the other 23 blocked fields. Matching those fields would
spread names that do not help.

6. **Decision 1 is replaced.** The target is not "the same names as the
   other fields" but "the answers that make Schedule D required". On a
   return where Schedule D is required, no sale is recorded and
   `no-form8949-sources` is answered yes, Schedule D is required only
   because an Exception 1 criterion fails. The block names exactly the
   Exception 1 criteria whose current answer fails the exception; those
   are the answers a filer can correct, or, if they are right, the reason
   a sale must be recorded. Criteria that pass and the four sale and
   boundary names are not named in that state.
7. **Both rules follow.** `rule.form1040-line16` v9 and a
   `rule.selected-preferential-base` v12 successor declare the same
   state-sensitive names in that state, so line 16, its four dependants
   and the 23 fields agree. Every other branch of both rules is
   unchanged: Decision 2 (known Form 8949 work keeps its names) and
   Decision 3 (an unanswered boundary asks the boundary question) stand.
8. **How the filer reads it.** Track 0b confirms that, for each failing
   criterion, the page sentence is true and that the field shows no
   sentence for a criterion that passes. If the projection cannot show
   the reason without a page change, stop: page wording belongs to
   blocked-sale-pages.
9. **Track 0b** redesigns the scratch content, reruns item 1 (and
   items 2 and 4 on the new content) and the full replay in parallel.

## Track 0b

All five charter items pass on the final scratch successor built from
published core v94. See [closure](line16-names-evidence/track0b-closure.md),
`prototype.py --track0b`, `track0b.py`, `classify.py --track0b`, and the
`track0b-*.json` evidence.

| Item | Verdict | Evidence |
| --- | --- | --- |
| 1. Redesign | PASS | Line 16 v9 and preferential-base v12 on existing rule-artifact v17. Each tree has 14 choose nodes and 15 nonempty leaves; no helpers or new operators. Undoing only the declaring blocks restores v8/v11 except version/notes. |
| 2. Names and progress | PASS | All 15 failing subsets across three statuses plus four recorded targets: 49 states, 100 name pairs, 249 live runs. Every truthful correction removes exactly that criterion or unblocks/moves the line; none is omitted. |
| 3. Every affected field agrees | PASS | All 1,372 field occurrences show exactly the failing-criterion sentences, with no passing criterion, sale/boundary question or extra sentence. |
| 4. Nothing else moved | PASS | 36 boundary states retain values/dispositions and accepted non-target behavior; all 86 fields on each of 16 neighbours, including the ten pinned cases and six computing cases, match v94. |
| 5. Full replay | PASS | 775 lists, nine workers, 8,799.32 s: 687 identical successes, 84 identical errors, four exact expected changes, zero unexpected. No saved value, disposition, code or row-membership change; all 11 classifier controls pass. |

The final content declares the exact no-valued Exception 1 criteria in both
target blocks. With multiple failures, correcting one moves to the exact
remaining set. Decisions 2 and 3 remain intact. The direct binary tree is
minimal for its 15 distinct nonempty literal outputs; its selected path
evaluates three or four criterion comparisons. No production content,
test, schema, engine, projection, page or kernel file changed in this unit.

The full replay part is retained outside Git and identified in the
operational JSON handoff. The builder recommends these two successors for
Track 1 under Decisions 6–9; no larger-change stop was required.

## Track 0b disposition

Foreman, 2026-11-17, on `line16-names-evidence/track0b-closure.md`. All
items pass: each failing criterion is named, each truthful correction
removes exactly its name, the 23 preferential-base fields and line 16's
dependants agree, and the full replay changes only the four recorded
targets' names (687 identical, 84 same error).

10. **Build the minimized shape.** `rule.form1040-line16` v9 and
    `rule.selected-preferential-base` v12 on rule-artifact v17, each a
    nested choose over the four existing criteria with fifteen literal
    leaves; no helper rules and no new operator.
11. **Measure speed before publishing.** The Track 0b replay took
    8,799 seconds against about 1,400 for P0's on the same lists.
    Track 1 times v94 and the successor on the same lists, under the
    same load, before publishing. If the successor is materially
    slower (more than 10% per list), stop and report.

## Track 1 result

Item 1 speed gate: **PASS**. On 40 fixed recorded lists (eight from each
recorded set, including all four targets), nine workers timed each core
back to back in the same worker, with twenty baseline-first and twenty
successor-first pairs. Nothing else was running from this builder.
Median elapsed time per list: v94 **7.536449 s**, Track 0b successor
**7.496203 s**; ratio **0.994660**. The median paired ratio is 0.998897.
The 1.10 stop threshold is not exceeded. This controlled measurement does
not establish why the earlier full-replay wall times differed.
See `line16-names-evidence/track1-speed.json` and `track1_speed.py`.

**Built:** core v95, registry v93, release v93. The two new computation
citizens are `rule.form1040-line16` v9 and
`rule.selected-preferential-base` v12, both on rule-artifact v17 and
byte-identical to the accepted minimized Track 0b prototype. The successor
package, registry and release were generated with
`python3 -m tools.package_successor` and are also byte-identical to that
prototype's generated files. Exactly two members and entrypoints change;
registry v93 adds only the two citizens and one package. The v95 loader
declarations and covered-flag map carry v94 unchanged. No published citizen
or schema was edited; 1,801 earlier content/release files retain their bytes.

The core-enumeration test includes v95. The two current required-versus-read
allowlist entries for line 16 carry their existing rationales from v8 to
v9, with no change to their symbols, reasons or required inputs. This was
identified by the fast lane and repaired as a version-only metadata update.

**Published replay:** all 775 recorded lists on v94 and v95, nine workers,
foreground, **1,428.48 seconds**. Strict classification is exactly
**687 identical successes, 84 identical errors, four expected failing-criterion
changes, zero unexpected**. No saved line value, disposition, refusal code
or row membership changes. Only the line 16/preferential-base missing names
and their matching sentences change, on the four recorded targets. All
eleven rejection controls pass. The part stays outside Git and is identified
in the operational JSON handoff; `track1-replay.json` holds the classification.

**Tests:** `tests/test_line16_names_v95.py` runs seven distinct act lists
once each through published `live_coordinate_run`, the presentation
projection and saved page model: one, two and four failures, a real
same-fact correction, the personal-loss case, the unanswered boundary, and
an unchanged computing neighbour. Expected names come from input findings.
All seven pass. Its measured calls are 18.75–19.68 seconds, so it is live.
The new package module verifies fourteen fast checks, including frozen
prototype hashes, the two replacements, add-only registry, release,
loader/allowlist carry-forward and all earlier bytes. Both new modules were
run with an unrelated evidence directory first on PYTHONPATH. The package
module's initial optional-`citations` key assumption was fixed and only that
failed assertion was rechecked; the later fast lane verifies the complete
current module. Details are retained in `track1-tests.json`.

**Checks:** the five touched core-switch tests pass; the seven related
required-versus-read checks plus the new allowlist assertion pass. Final
fast lane: **1,837 passed, 8 skipped** in 15.29 seconds. Mypy: no issues in
509 source files. The requested `github/main..HEAD` envelope scan and
whitespace/scope checks pass. `track1-checks.json` records these checks.
CI `verify` remains the gate of record for the full suite; no push occurred.

**Deviations:** none. Each numbered item is committed separately. No
kernel, derivation, schema, presentation or recording change was needed.
