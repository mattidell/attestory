# Track 0 adversarial closure: blocked lines name their question

Date: 2026-11-12. Published baseline: core v87. Evidence successor: the
repaired scratch successor built by `prototype.py` after v87. The scratch
version is evidence notation, not a production version claim.

## Verdict

**PASS.** All eight tables pass, including all ten target cases, the full
recorded-return replay, the 15-field root trace, and the repaired strict
integration surface. The personal-item-loss-on-Form-8949 case now routes its
downstream blocked fields through four existing boundary questions. No numeric
value changed and no previously computing return gained a question.

Every behavior row comes from a synthetic `demo.*` `live_coordinate_run` on
published v87 and the scratch successor. The JSON outputs retain the case ids,
page sentences, blocked-field groupings, and watched hand values.

## Tables

| Table | Verdict | Counts | Notable case ids |
| --- | --- | --- | --- |
| Authority lifecycle | PASS | 11 successors; 17 block declarations; 13 distinct declared names; 10 P0 cases plus 3 long-term authority cases | `sd_yes_nothing`, `lt_no1099_basis_disagrees`, `lt_codeb_adjustment_disagrees`, `lt_wash_adjustment_open` |
| Empty/nonempty matrix | PASS | 10 cases; 20 states; 0 zero-question terminals | all ten P0 ids |
| Late-member traces | PASS | 3 traces; 8 states; 16 live runs | `sale_after_form8949_yes`, `amount_corrected`, `wash_adjustment_after_close` |
| Claim reuse | PASS | 11 successors; 10 live inputs on both cores; 0 numeric differences | `sd_amounts_disagree`, `codeb_amounts_disagree`, `wash_adjustment_open`, `exception1_personal_loss_8949` |
| Neighbour diff | PASS | 775 lists; 1,550 fresh live runs; 677 identical; 69 metadata-only; 25 sentence-only; 4 disposition-only; 0 numeric; 0 new questions on computing returns | all recorded ids classified in `track0-neighbour.json` |
| Integration surface | PASS | 20 states; 0 failing states; 0 blocked fields without a question | `exception1_personal_loss_8949.unanswered`, `exception1_personal_loss_8949.truthful_answer` |
| Downstream-root trace | PASS | 15 fields; all 15 reasonless on v87 and the original scratch successor; every field reaches an unexplainable root | `exception1_personal_loss_8949.unanswered` |
| Root repair | PASS | 1 further successor; 4 existing declared names; 0 presentation or kernel changes | `rule.form1040-line16.v8`, `exception1_personal_loss_8949` |

## Authority lifecycle

`track0-authority.json` enumerates every expression-block declaration. Each of
the 13 distinct names resolves through an adopted input-question citizen or
source-closure mapping, and each resolver sentence appears in at least one live
case. The ten P0 cases show a question when unanswered. Once the truthful
answer or value is recorded, each case either reaches its instruction-derived
hand value or exposes the next named question.

The three long-term cases are included because the P0 reproductions exercise
the short-term twins. They show the long-term basis, code-B adjustment, and
wash-adjustment closure sentences, so no declaration is accepted by structural
inspection alone.

## Empty/nonempty matrix

`track0-matrix.json` retains the unanswered and truthfully answered state of
each P0 case on both cores. All 20 scratch states either compute or show at
least one question citizen. Blank Form 1099-B box 4 values are recorded as
zero, exactly as the published input question instructs, so unrelated payment
lines do not create artificial terminals.

The hand checks use the 2025 instruction arithmetic: the no-1099-B loss is
negative 6,000 before the 3,000 capital-loss limit; the corrected code-B sale
is positive 6,000; and the covered wash sale is negative 5,000.

## Late-member traces

`track0-late.json` records all three required sequences:

- a no-Form-8949 answer of yes, then a sale, then the truthful superseding no;
- a scalar basis that disagrees, then an ordinary-assertion correction to
  8,000; and
- a second wash transaction after closure, the newly open adjustment family,
  then reclosure.

Each open or stale state names a question. The final states reach the hand
values negative 6,000, negative 6,000, and negative 5,000 respectively.

## Claim reuse

`track0-reuse.json` compares each successor with its predecessor after removing
only the additive `block.missing`, normalizing the successor version, and, for
the two wash rules, separately normalizing the decided closure-check preflight.
For the eleventh successor it separately normalizes the new line-16 false-guard
block. All predecessor bodies are then identical. Thus the declarations add no
read, pin, dependency, or answer change. The two wash preflights are the
separate content decision: an open family selects its existing closure
question; a closed family evaluates the predecessor expression unchanged.

The ten live P0 inputs have identical numeric line values on v87 and the
scratch successor. The intended line-16 disposition changes from
`guard_inapplicable` to `blocked` in the repaired dead-end states.

## Neighbour diff

Because the repaired scratch core changes an affected rule,
`rerun-repair-output.json` reruns all 775 recorded act lists in four shards:
677 are identical, 69 change only in blocked-row missing metadata, 25 change
only in question or reason sentences, and four change only the line-16 string
disposition from `guard_inapplicable` to `blocked`. No numeric value changes
and no return that computed before gains a question.

## Integration surface

`track0-surface.json` matches live page reasons against published question
citizens and closure questions. This deliberately recognizes imperative input
questions such as “Enter ... If box 4 is blank, enter $0.” even though the
sentence has no question mark.

Every one of the 20 states that has a blocked field shows at least one exact
question sentence, every displayed question sentence comes from a declared
citizen, and every blocked filer-visible field names at least one question.
The two `exception1_personal_loss_8949` states now route the same four boundary
questions to all downstream blocked fields.

## Downstream trace and repair

`track0-roots.json` records the original failure before repair. All 15 fields
are reasonless on both v87 and the original scratch successor. Their blocked
producer walks reach three expression roots that wait on `tax.total-tax`.
That name has no question citizen and its only producer, Form 1040 line 16, is
guard-inapplicable, so the projection's all-roots rule suppresses every reason.
The evidence cites the content rules and the projection locations for each
walk; no projection change is needed.

`track0-repair.json` records the content-only repair. A line-16 v8 successor
keeps its existing true guard branch and makes the formerly inapplicable false
branch block with four already-authoritative boundary names. The repaired live
case changes line 16 to `blocked`, shows the four questions, and has no silent
blocked field. It adds no citizen, answer, refusal, presentation, or kernel
change.

## Known limitations affecting correctness

No correctness-affecting limitation remains inside the chartered Track 0
surface. This is still prototype evidence: the proposed ADR must be accepted,
and the 11 rule successors, two citizens, schema successor, package successor,
and release successor must be built and reviewed before the behavior can ship.
The replay demonstrates the existing 2025 synthetic neighbor set; it does not
claim broader tax-domain coverage.
