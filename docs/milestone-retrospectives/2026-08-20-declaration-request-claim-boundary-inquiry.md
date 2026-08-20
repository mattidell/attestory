# Retrospective — Declaration Request to Claim Boundary Inquiry (CQ-2)

## What differed from the plan

The plan ran as designed: a Track 0 frame that was the sole evidence boundary
for two independent standpoint accounts, a Track 2 disposition round, and a
Track 3 curation. Two structural changes from CQ-1 were deliberate and both
did what they were meant to do.

**Two standpoints instead of four.** CQ-1's four lenses produced overlap that
Track 2 had to spend effort collapsing. Two justified standpoints — a casual
invested reader on Claude, a system and provenance adversary on Grok, each
given the same packet and no contact — produced a cleaner signal at lower
cost, including the milestone's best methodological result: two model families
on opposite standpoints independently selected the same paragraph as their
deepest thread.

**Track 2 given disposition authority.** CQ-1 was criticized for splitting
differences and leaving the owner to arbitrate. So CQ-2 explicitly asked
Track 2 to disposition the Track 1 split. It did, well, on the copy-ambiguity
question. It also used that same authority to close a question its inputs had
correctly left *open*, and got it wrong. That is the milestone's central
lesson and it is recorded below rather than filed as an incident.

## What it cost

Four tracks, then a two-pass owner-directed factual repair. Both passes were
triggered by the owner reading code, not by the project's own checks — the
same failure mode as CQ-1, in a different disguise.

The repair corrected two substantive errors:

- **Error A — the horizon-only invalidator.** The packets stated that family
  horizon succession is the only mechanism that can invalidate a recorded
  box-1 closure. The `tax.us.2025.f1099int.b1.source-closure` fact carries
  `supersession {"policy": "free"}`, so a later finding on the same `fact_id`
  displaces the earlier one as a `correction` in `packages/kernel/currency.py`
  independent of any horizon change. There are two mechanisms, not one.
- **Error B — the unrepresentable "no".** Track 2 dispositioned that an
  explicit user "no" is "not representable, and this is settled, not
  ambiguous." The fact's `value_schema` is boolean; `false` is recordable and
  is carried through `marshal_closure_authority`, which selects current
  findings by mapped fact type and copies the recorded value through
  unchanged, never filtering on value. What is actually true is narrower and
  lives at a different layer: `resolve_closure_admissions` collapses `false`,
  absence, duplicate authority, and truthy-non-boolean into one non-admitted
  outcome — key absence — and no interface exists to record the `false` at
  all. What is disproven is the *structural* equivalence of a recorded
  `false` and absence, not anything about what a `false` would mean.

The corrected account is four layers, not one: **record (plus currency) /
closure-authority projection / admission result / interface.** What each layer
preserves or collapses differs, and the packets had flattened all four into
"the system cannot represent a no." The record preserves `true`, `false`, and
absence as three distinct states and preserves supersession order. The
closure-authority projection preserves the recorded value: it selects from
currency's current findings, keeps those whose fact type the mapping names,
requires and reads the horizon identity key, and copies the value through
unchanged. It does not compare that horizon with the family's current one —
that happens at admission — so what it excludes is non-current findings and
findings of unrelated fact types, not stale horizons. The admission result is where the value
distinction is lost: `false`, absence, duplicate authority, and
truthy-non-boolean collapse into one non-admitted outcome expressed as key
absence, and the reason does not survive the hop. The interface offers no
affordance to record the `false` at all, so the distinction the lower layers
preserve is never available to the user.

**Neither error was present in every packet, and neither was a two-model
convergence.** Error A originates in the milestone plan's own
verified-witness section and in Track 0 §7, and was hardened in Track 2 §4.4.
Error B is closed as a settled disposition in Track 2 §4.3; Track 0 §2 stated
the admission behavior accurately. The casual-reader standpoint account
asserts neither error. The external Grok account asserts both — Attack 4 the
horizon-only invalidator, Attack 3 record-layer equivalence — while its own
§4 files the same two questions as points where explanation terminates.

**The reconciliation was wrong twice before it was right, and that is the
more instructive fact.** The first draft asserted both errors were common to
all four packets; the owner required a packet-by-packet demonstration and the
claim did not survive it. The corrected version then graded the Grok account
clean of both, which an independent review of the publication candidate
disproved by quoting the packet. A repair pass is not self-checking: the
first overstated contamination, the second understated it, and both were
found by a reader who went back to the text. The per-packet reconciliation
now lives at
`docs/phases/claim-boundary-exploration/inquiries/cq2-track-3-curated-inquiry.md`
§14.1, with both supersessions visible.

Exit criteria were regraded after the repair from seven of seven met to
**four of seven met, three partially met.** Criteria 1, 2, and 3 had texts a
true-but-partial account could satisfy; those texts were strengthened as part
of the repair, and criterion 1 was downgraded because Track 0 did not correctly
verify every material witness claim and the correction arrived afterward.

The strengthened texts are the ones now in the plan, and they did not govern
Track 0 when it ran. So that the record is auditable in both directions, the
curated inquiry §11 states criteria 1, 2, and 3 twice — the final plan text and
the execution-time text as it stood at commit `3b19acc5` — showing both what is
now required and how the original wording admitted the overly permissive grade.
Criteria 4 through 7 are unchanged. The reconciliation changed no grade.

## Material dissent

**On the recommendation.** Track 3 recommends a bounded build or decision
milestone over a third inquiry, on the ground that the register now holds more
decision-shaped evidence than has been converted into decisions. The
counter-argument is real and is recorded rather than dismissed: content-level
generality is *not* confirmed — both inquiries share one tax domain, one
package version, and one closure mechanism, so much of the apparent
cross-inquiry "repetition" is the same artifact read twice. A third inquiry in
a materially different tax domain **would test transfer, not settle
generality**, and two data points cannot distinguish a reusable explanatory
structure from a property of this one closure. The recommendation is weighed,
not dictated.

**On what the repair licenses.** The corrected layer analysis is *structural*
and licenses only structural conclusions: the fact schema permits a recorded
boolean `false`, a later same-fact `false` can supersede an earlier `true`, a
current `false` survives the closure-authority projection, the resulting
non-admission loses its reason, and no interface or committed product act
exists for this family. ADR-0055's `COMPLETENESS_VALUE_VIOLATION` separately
shows the architecture can carry a present-but-wrong-value versus absent
distinction at a different attachment path.

Two inferences were drawn from this during repair and both were withdrawn at
owner direction; both should stay withdrawn. The first was that a closure-side
fix is therefore local, small, or better-specified — ADR-0055 is evidence of
architectural capability elsewhere, and no implementation shape, locality, or
cost follows from it. The second, subtler and caught last, was **treating an
available structural transition as settled declaration semantics**: saying the
record "already supports reversal" or "can represent taking the declaration
back." It cannot be said to represent that, because nothing committed assigns
a recorded `false` any product meaning. A `true → false` transition has an
operational consequence — the family stops being admitted — but whether that
consequence *is* withdrawal, refusal, an initial "not done," or a corrected
mistake is exactly the open `SC-13` question. Structural representability is
not assigned meaning, and the repair's own language kept sliding from the
first into the second.

**On the consolidated SC-13.** `SC-13` and `SC-15` are merged because they are
one declaration-lifecycle question, but they are joined by *unsettled
semantics*, not by a shared implementation. The claim that "not done" and
withdrawal necessarily write the same corrective `false` was asserted during
repair and then withdrawn: it is a product-design option, not an established
consequence. The decision has to be framed around the semantics of absence,
explicit `false`, correction, and horizon succession before any interface
action is selected.

## Reusable lessons

**A citation is not a verification, and the gap is completeness, not
strength.** The milestone ran an evidence-class discipline — executed /
static-read / content text / inference / gap — and it worked as designed. It
grades *how strongly* a claim is evidenced. It has no category for *how
completely the cited artifact was read.* Both errors passed a Confirmed
grading because the cited static read did not extend to the adjacent fields of
the cited artifact, nor to the consumers whose behavior the claim depended on.
Error A's origin is precisely this: the `title` prose of the closure fact
names only horizon succession, and the sibling `supersession` field two lines
away says otherwise.

**Safeguard adopted for future inquiries:** every load-bearing artifact claim
must name the artifact, the fields actually read, the sibling fields present
and not relied on, and the consumers whose behavior the claim depends on. A
claim that cannot fill those four slots is graded as a gap, not as confirmed.

**Disposition authority is a sharp tool.** Granting Track 2 the authority to
close splits fixed CQ-1's real defect and immediately produced a new one:
authority to settle a question is also authority to settle it wrongly, and a
downstream agent has no way to tell "the inputs disagreed" from "the inputs
were correctly uncertain." The distinction between *dispositioning a split*
and *closing an open question* should be explicit in the next disposition
charter. Where an upstream account records that explanation terminates, that
terminus is evidence and must be carried forward, not converted into an
answer.

**Two agents agreeing is weaker evidence than it feels.** The convergence
result is real and valuable, but the errors show its limit: independent
standpoints on the *same packet* test whether the packet's framing is robust
to standpoint, not whether the packet is true. Neither account tested Error A;
the adversarial one inherited it from the frame and built an attack on top of
it. Convergence measures the packet, not the world.

**An agent can file a question as open and answer it anyway.** The Grok
account's §4 lists "whether `false` is a representable user act at all" and
"any withdrawal path other than horizon succession" as points where
explanation terminates, and its Attacks 3 and 4 assert answers to both. A
methodology section declaring uncertainty is not evidence that the substantive
argument respected it. Any future curation must read the argument, not the
self-report — the first correction of this milestone's reconciliation took the
self-report at face value and graded the packet clean.

## Follow-ups

- The consolidated `SC-13` declaration-lifecycle question is the register's
  largest decision-shaped item and remains unselected. It requires semantic
  decisions about absence versus explicit `false` versus correction versus
  horizon succession before any interface work.
- `SC-16` is retained on the narrow basis that its scenario pair is
  **specified and runnable, not executed**, and can test a bounded causal
  contrast rather than establish how often the condition occurs. Running it is
  available work.
- `OV-1` is unchanged in substance: a confirmed tax-content correctness gap
  (one of eight independent Schedule B triggers implemented) and an owner
  decision. CQ-2's trace independently reached it. No fix shape is inferred.
- The completeness/neighborhood safeguard above is currently recorded in the
  curated inquiry and this retrospective. If a third inquiry is selected, it
  should move into the inquiry charter template.

## What should change in the next plan

Whatever is selected, the plan should state — in the plan, not in a charter —
that a claim about a committed artifact must carry its completeness check, and
that an upstream "explanation terminates here" is a finding to preserve rather
than a gap to fill. Both of this milestone's errors would have been caught by
one of those two rules.
