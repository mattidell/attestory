<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Claim Boundary Exploration",
  "topic": "claim-boundary-exploration",
  "active_plan": "docs/phases/claim-boundary-exploration/milestones/declaration-request-claim-boundary-inquiry.md",
  "milestone_state": "closed",
  "retrospective": "docs/milestone-retrospectives/2026-08-20-declaration-request-claim-boundary-inquiry.md",
  "status": "Owner selected CQ-2 (\"Why are you asking me to say I'm done?\") 2026-08-19 as the second worked inquiry, per the actionable-considerations register's own recommendation. Plan drafted and verified directly against committed artifacts before chartering, then APPROVED by the owner 2026-08-19 with the PR deliberately deferred. Tracks 0 and 1 are closed. Track 0 independently confirmed all ten verification claims, recorded executed runtime evidence for both states, and decided the Schedule B gate as materially reached (OV-1 admitted as a bounded counterfactual only). Track 1 ran the two standpoint accounts; they converged independently on the State B misattribution paragraph and diverged on whether the packet overstates what a declaration does, recorded without disposition. Track 2 is closed: it dispositioned the Track 1 split (the phrase \"before it can use this piece in your return\" is defective as user-facing copy and defensible as an engineering gloss, the ambiguity between those readings being itself the defect), settled three further tensions, built a request-rooted evidence-classed tree, and produced the four-way CQ-1 delta. Track 3 is closed and ALL FOUR TRACKS ARE COMPLETE. CQ-2 closed, register entries admitted and annotated, one charter-listed candidate declined under the admission rule. OWNER-DIRECTED FACTUAL REPAIR APPLIED 2026-08-19 in two passes after track completion, no new exploration round. Pass 1: the packets conflated recorded state with derivation admission; re-verified in code against the closure fact type, marshal.py, source_authority.py, kernel/currency.py, and kernel/findings.py, confirming the owner on every point. Pass 2 (owner-directed record repair and publication curation): corrected this plan's own body, not only its metadata, and reconciled the errors packet by packet. TWO SUBSTANTIVE ERRORS, NOT COMMON TO ALL PACKETS - Error A (horizon succession stated as the only invalidator; same-fact correction under free supersession is a second) originates in this plan's Verified-concrete-witness section and Track 0 §7, and hardened in Track 2 §4.4. Error B (an explicit 'no' held unrepresentable) is CLOSED AS A SETTLED DISPOSITION in Track 2 §4.3; Track 0 §2 was accurate. REGRADED 2026-08-20 after independent review of the publication candidate: the external Track 1 (Grok) account, previously recorded as asserting neither error, in fact asserts BOTH - Attack 4 states the horizon-only invalidator and Attack 3 states record-layer equivalence - while its own methodology section files the same two questions as termination points. The casual-reader account asserts neither. Neither error was common to all four packets and neither was a convergence of the two standpoint accounts. Register: SC-13 and SC-15 consolidated into one declaration-lifecycle entry, joined by unsettled semantics rather than by a shared implementation; SC-14 corrected (not showing the membership set impairs evaluation and support, it does not change the proposition asserted); SC-16 retained only on the narrower basis that its scenario pair is specified and runnable, not executed, and tests a bounded causal contrast rather than a frequency. ADR-0055 is recorded as evidence the architecture can carry an absence-versus-present distinction elsewhere; no closure-side fix shape, locality, or cost is inferred. The request affordance is labeled proposed and hypothetical. EXIT CRITERIA REGRADED: four of seven met, criteria 1, 2, and 3 partially met. Criteria 1, 2, and 3 texts corrected so a true-but-partial account no longer satisfies them. Generality: the method is reusable across both inquiries; content-level generality is NOT confirmed, and a third tax-domain inquiry would TEST TRANSFER, NOT SETTLE GENERALITY. Method safeguard added: every load-bearing artifact claim must carry a completeness/neighborhood check. Recommends a bounded build or decision milestone over a third inquiry, flagged as weighed rather than dictated; a recommendation is not a selection. CLOSED by owner direction 2026-08-20 after publication curation. No ADR, governance revision, or implementation was produced. The phase remains active and the next milestone is unselected.",
  "current_role": "Foreman — between milestones; selecting the next within Claim Boundary Exploration",
  "current_prompt": "docs/phases/claim-boundary-exploration/actionable-considerations.md",
  "scope": [
    "trace one plain user question about a system request for a user declaration end to end through the committed Form 1099-INT box 1 source-family closure that feeds Form 1040 line 2b",
    "account for proposition, speaker, basis, scope, effect, non-effect, invalidator, and unsupported neighboring inference, plus an honest 'not yet' and withdrawal path",
    "produce an explicit cross-inquiry delta against the closed CQ-1 inquiry: which explanatory branches repeat, change, disappear, and are new",
    "run two justified independent standpoints rather than four, and assess whether a reusable explanatory structure is emerging"
  ],
  "non_goals": [
    "no OV-1 implementation and no assumption about its eventual schema, rule-language, engine, or content shape",
    "no ADR, governance revision, production UI, canonical copy, schema, rule-language, engine, filing, or tax-coverage change",
    "no general definition of claim, completeness, integrity, or correctness, and no total semantic taxonomy",
    "no automatic selection of a third inquiry or build milestone",
    "no personal data, real-run operation, or professional-attestation claim"
  ],
  "deep_reads": {
    "implementation": [
      "docs/phases/claim-boundary-exploration/milestones/declaration-request-claim-boundary-inquiry.md#Objective",
      "docs/phases/claim-boundary-exploration/milestones/declaration-request-claim-boundary-inquiry.md#Experimental design",
      "docs/phases/claim-boundary-exploration/milestones/declaration-request-claim-boundary-inquiry.md#Verified concrete witness",
      "docs/phases/claim-boundary-exploration/milestones/declaration-request-claim-boundary-inquiry.md#OV-1 posture",
      "docs/phases/claim-boundary-exploration/milestones/declaration-request-claim-boundary-inquiry.md#Scope",
      "docs/phases/claim-boundary-exploration/milestones/declaration-request-claim-boundary-inquiry.md#Non-goals",
      "docs/phases/claim-boundary-exploration/milestones/declaration-request-claim-boundary-inquiry.md#Tracks",
      "docs/phases/claim-boundary-exploration/milestones/declaration-request-claim-boundary-inquiry.md#Data safety",
      "docs/phases/claim-boundary-exploration/claim-boundary-exploration-overview.md#Standing test",
      "docs/phases/claim-boundary-exploration/claim-boundary-exploration-overview.md#Inquiry shape",
      "docs/phases/claim-boundary-exploration/claim-boundary-exploration-overview.md#Principal risks",
      "docs/phases/claim-boundary-exploration/actionable-considerations.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-08-20-declaration-request-claim-boundary-inquiry.md",
      "docs/milestone-retrospectives/2026-08-19-plain-question-claim-boundary-prototype.md",
      "docs/phases/claim-boundary-exploration/claim-boundary-exploration-overview.md",
      "docs/phases/claim-boundary-exploration/actionable-considerations.md",
      "docs/phases/claim-boundary-exploration/inquiries/cq2-track-3-curated-inquiry.md"
    ]
  }
}
-->

# Milestone: Declaration Request to Claim Boundary Inquiry

- Phase: Claim Boundary Exploration
- Milestone key: `declaration-request-claim-boundary-inquiry`
- Status: **approved 2026-08-19; all four tracks complete; owner-directed
  factual repair applied in two passes 2026-08-19/2026-08-20; CLOSED by owner
  direction 2026-08-20.** Retrospective:
  `docs/milestone-retrospectives/2026-08-20-declaration-request-claim-boundary-inquiry.md`.
  The next milestone is unselected. The repair corrected a record/admission layer conflation
  and established the four-layer closure account (record + currency /
  closure-authority projection / admission / interface). **Two substantive
  errors were found, and neither was present in every packet**: the
  horizon-only-invalidator error originates in this plan's verified-witness
  section and Track 0 §7 and was hardened in Track 2 §4.4; the
  no-representable-"no" error is closed as a settled disposition in Track 2
  §4.3, while Track 0 §2 was accurate. **Regraded 2026-08-20** after
  independent review of the publication candidate: the external Track 1 (Grok)
  account asserts both errors in its attacks — previously and wrongly recorded
  as asserting neither — while filing the same two questions as termination
  points in its own methodology section. The casual-reader account asserts
  neither.
  The repair also consolidated `SC-13` and `SC-15` and **regraded the exit
  criteria to four of seven met, three partially met** (criteria 1, 2, and 3
  partially met); no new exploration round was run. See
  `docs/phases/claim-boundary-exploration/inquiries/cq2-track-3-curated-inquiry.md`
  §4, §5, §11, §14.
- Base: `origin/main` at `20cf03abfefef07e28a9b80f8047f5c22d8ccc9b` (PR #181
  merged; this is the current ratified tip)
- Branch: `milestone/declaration-request-claim-boundary-inquiry-cq2`
- Decision posture: exploratory and non-authoritative; no ADR is produced

## Objective

Determine whether the system can explain a **request for a user declaration**
well enough for a casual but invested user to understand, at minimum: the
proposition asserted, why the system needs the user rather than the software
to assert it, the exact scope of the assertion, what becomes possible
afterward, what does not follow from it, what the user can do if not ready,
and how the assertion can become stale, be withdrawn, or cease to support a
downstream result.

The worked question is:

> Why are you asking me to say I'm done?

This is CQ-2 from the register
(`docs/phases/claim-boundary-exploration/actionable-considerations.md`),
recorded by the Track 3 repair charter as the recommended next inquiry if
exploration continues — recommendation, not automatic selection; the owner
selected it directly for this milestone.

## Experimental design

Hold the tax domain constant, change the interaction type:

- CQ-1 (closed) examined a **system-presented result** — a published number
  and its support chain.
- CQ-2 examines a **system request for a user declaration** — the act of
  asking the user to assert something, before any number is finalized on it.

The same domain lets the milestone produce an explicit cross-inquiry delta:
which explanatory branches repeat, which change, which disappear, and which
are new to a declaration-request interaction that a presented-result
interaction never raised.

## Verified concrete witness

No behavior below is asserted from recollection; each line was read directly
from the cited artifact or module on `origin/main` at `20cf03ab`.

**The declaration:** the Form 1099-INT box 1 source-family closure —
`tax.us.2025.f1099int.b1.source-closure`, declared in
`packages/content/tax/2025/f1099int.bundle.json` (`bundle.v2`, fact-type
`tax.us.2025.f1099int.b1.source-closure`, `nature: determinable`,
`value_schema: boolean`). This is the assertion behind the "say I'm done"
request for one source family that feeds Form 1040 line 2b, the same line
CQ-1 examined — satisfying the "familiar family" instruction while changing
only the interaction type.

**Proposition and scope, verified from the artifact's own title text:**
"*User-attested closure of the Form 1099-INT box-1 source family for 2025,
keyed on the family membership horizon current at attestation (ADR-0017):
true asserts every furnished 1099-INT box-1 statement item is recorded as of
that horizon. This claim covers box 1 only — never other boxes, non-form
interest, or Form 1040 line 2b (ADR-0016).*" The scope boundary is stated in
the artifact itself, not inferred.

**Invalidators — corrected 2026-08-19; this plan originally recorded only
the first and called it the committed answer.** Two committed mechanisms
invalidate the closure, and reading only the fact type's title prose finds
one of them:

1. **Horizon succession**, from the title text: "*A later membership
   transition displaces this closure through horizon succession;
   re-attestation on the successor horizon is required.*" A new horizon,
   not a timeout, not a UI action.
2. **Same-fact correction on the same horizon**, from the *same citizen's*
   `supersession` field: `{"policy": "free"}`, which
   `packages/kernel/findings.py` treats as permitting correction
   unconditionally (`locked` raises; `closed-on-attestation` gates). A
   later finding for the same `fact_id` displaces the earlier one as a
   correction root in `packages/kernel/currency.py::_finding_corrections`,
   so a recorded `true` can be superseded by a recorded `false` without any
   membership transition.

Neither mechanism is a user-facing action; no committed code path invokes
either for this family. The original wording of this section is the direct
source of the milestone's Error A — see
`docs/phases/claim-boundary-exploration/inquiries/cq2-track-3-curated-inquiry.md`
§14.1.

**Declaring family:**
`packages/content/tax/2025/family.f1099int-b1.json` (`source-family.v1`) —
`member_predicate.fact_type = tax.us.2025.f1099int.box1-interest`,
`authorizes_subtotal = tax.us.2025.interest.b1-subtotal`. Its
`closure_claim` text: "*Every interest amount reported in box 1 of a Form
1099-INT furnished to the taxpayer for tax year 2025 is recorded as a
statement item. This claim covers Form 1099-INT box 1 only...*"

**Closure mapping (the adopted authority bridge, ADR-0014):**
`packages/content/tax/2025/closure-mapping.f1099int-b1.json`
(`source-closure-mapping.v2`) pins the exact family id/version, names
`member_fact_type` and `closure_fact_type`, `closure_horizon_key:
"family-horizon"`, `admits_symbol: tax.us.2025.interest.b1-subtotal`.
Cross-pair validation is `validate_mapping_against_family` in
`packages/derivation/source_authority.py`.

**Why the user, not the software:** `resolve_closure_admissions` in
`source_authority.py` admits a family only from an adopted mapping plus a
**current, literal-true closure finding** keyed to the **current horizon**
(`marshal_closure_authority` in `packages/derivation/marshal.py`). There is
no code path that derives or infers this boolean; it is asserted or absent.
`ClosureAdmission` (same module) records the exact mapping/declaration
version and finding id admitted — the attribution chain ADR-0009 requires.

**Consuming code:** `rule.form1040-line2b.v4.json` — `requires` includes
`tax.us.2025.interest.b1-subtotal` among ten pins (seven positive-interest
families plus three Schedule B adjustment families); the rule's `value`
computes the seven-family sum less the three adjustment subtotals. The
`require_closed` operation is evaluated in `packages/derivation/evaluator.py`
(`env.closed_sets` check, `EvalBlocked(BLOCK_CLOSURE, ...)` on miss).

**What becomes possible / what does not follow — verified from
`form1040.line-2b.form-field.v5.json` disposition text:** closing this one
family does not, by itself, publish line 2b; line 2b's `published_value`
disposition still requires all ten pins closed. Closing box 1 alone can only
ever produce `blocked` (nine still open) or contribute toward
`closure_backed_zero`/`published_value` once every other family is also
closed. **Confirmed still-live from CQ-1 (SC-3, re-verified here, not
re-derived):** the `blocked` explain text is the same generic string
regardless of which of the ten families is unclosed — "*one or more
constituent interest families are unclosed or their dependencies are
missing*" — so the current rendering cannot itself tell a user which
declaration is still outstanding. CQ-2 treats this as inherited context, not
a new finding to re-derive.

**Vocabulary note verified, not reused as authority:** `finding.v2`'s
`basis` enum is `{documentary, attested, elective}` (ADR-0009: a human
determination a derived finding structurally cannot carry). The
`closure_backed_zero` disposition explain text says "...all constituent
families are **attested** closed..." — the SC-8 collision CQ-1 already
flagged, confirmed still present in v5, not re-litigated here. Separately,
and worth distinguishing rather than conflating: the one committed
closure-finding-producing code path this milestone found
(`packages/derivation/entry_loop.py`, the W-2 closure act) sets the
finding's actual schema `"basis": "documentary"`, not `"attested"` — so the
ordinary-English collision and the kernel's structural `basis` value are
independently verified facts, not the same fact restated twice.

## OV-1 posture

OV-1 (the Schedule B categorical-trigger gap) is a **confirmed correctness
gap, not selected for implementation here.** Do not assume the schema,
rule-language, engine, or eventual fix shape.

`tax.us.2025.interest.b1-subtotal` (this milestone's declared family) feeds
`tax.us.2025.interest.positive-total`
(`rule.interest-positive-total.json`), which is one of the two subtotals
`rule.attachment.schedule-b.v4.json`'s `requirement` block tests against the
dollar threshold — so a chain exists from this declaration to the
committed Schedule B attachment decision. If, and only if, Track 0's
end-to-end trace actually reaches a "does declaring this family closed
affect whether Schedule B attaches" branch, the milestone may state the
IRS's seven omitted categorical triggers as an explicit bounded
counterfactual — never as current system behavior, never with an assumed
fix shape. If the trace does not reach that branch, OV-1 stays outside the
inquiry entirely rather than being forced in; the b1 family itself carries
no accrued-interest, ABP, or nominee content — those are separate,
already-closed source families in the same composition.

## Scope

1. Fix the exact user situation: a declaration-request affordance for the
   1099-INT box 1 closure, presented to a filer who has entered their box 1
   statement items and is being asked to assert the family is complete.
2. Verify the full material chain above end to end (already done for this
   plan; Track 0 re-derives it independently rather than trusting the plan's
   own summary, per this phase's standing discipline).
3. Draft the shortest useful plain answer to "Why are you asking me to say
   I'm done?" before decomposition.
4. Build a progressive explanation tree answering, at minimum, the seven
   numbered questions in the objective, each terminating at verified
   artifact or code, or at an explicit product judgment.
5. Produce a claim-boundary trace: proposition, speaker, basis, scope,
   effect, non-effect, invalidator, and at least one unsupported neighboring
   inference (e.g., "closing box 1" does not mean "line 2b is done," does
   not mean "my return is done," does not mean the amount is legally
   attested).
6. Provide an honest "not yet" path: what the interface can honestly say to
   a user who is not ready to assert this, verified against what the engine
   actually does with an absent or false closure finding (blocked
   disposition, not an error).
7. State withdrawal/staleness precisely from **both** verified invalidator
   mechanisms above — horizon succession and same-fact correction under
   `free` supersession — and enumerate where a further mechanism could
   live before calling the account complete. Do not invent a UI unattest
   action that does not exist in committed code, and equally do not report
   the absence of a *user-facing* path as the absence of any invalidator.
   **Corrected 2026-08-19**: this instruction originally named only the
   horizon-succession mechanism, which is how the incomplete account was
   chartered rather than merely tolerated.
8. Compare explicitly against the closed CQ-1 inquiry
   (`docs/phases/claim-boundary-exploration/inquiries/track-3-curated-inquiry.md`
   and its constituent tracks): which explanation-tree branches repeat
   (e.g., filing-effect boundary, voice/authorship), which change (subject
   shifts from a computed number to a boolean assertion), which disappear
   (no "why is this number specifically this value" arithmetic branch),
   and which are new (why the user and not the software; what an assertion
   authorizes that computation alone cannot).
9. Update the actionable-considerations register: close or reassess CQ-2,
   note any new SC-entries this inquiry's evidence supports, and record
   whether a reusable explanatory structure is beginning to emerge across
   the two inquiries.
10. Recommend the next step: cross-inquiry reduction, another contrasting
    inquiry, a bounded build/decision milestone, or a stop. The owner
    selects.

Explorers may follow a discovered angle beyond the initial decomposition
when they can name the answer, implication, action, limitation, evidence
need, or future product requirement it could materially change — same
standing leeway as CQ-1, same admission rule for the register.

## Non-goals

- No OV-1 implementation; no assumption about its eventual schema,
  rule-language, engine, or content shape.
- No production UI or canonical copy.
- No ADR or governance revision.
- No schema, rule-language, engine, filing, or tax-coverage change.
- No general definition of claim, completeness, integrity, or correctness.
- No total semantic taxonomy.
- No automatic selection of a third inquiry or build milestone.
- No re-running all four CQ-1 lenses by default (see "Independent
  standpoints" below for the leaner, justified alternative).
- No reproduction of the full CQ-1 explanation tree; only the delta against
  it.

## Distinguishing "complete" — this inquiry's qualified sense only

Per the owner's framing, this milestone does not define "complete"
generally. For this inquiry, "done" (the word a UI would use to ask for
this declaration) means exactly: the user asserts that every Form 1099-INT
box 1 statement item furnished to them for 2025 is recorded as of the
current family-membership horizon. Nothing more. The milestone must keep
these six notions visibly distinct wherever the explanation tree touches
them, reusing CQ-1's own list plus the sixth this inquiry adds:

1. **document completeness** — a claim about the taxpayer's paper, which no
   committed artifact in this chain makes or supports;
2. **source-family closure** — exactly what this declaration is (verified
   above);
3. **product tax-coverage completeness** — whether the product models a tax
   category at all (SC-10 territory, out of scope here);
4. **computation readiness** — whether line 2b's rule has all ten pins it
   needs (a system-side readiness fact, not what the user is asked to
   assert);
5. **return/filing readiness** — untouched by one family's closure;
6. **legal attestation** — the jurat/signature act at filing (ADR/SC-12
   territory), which this declaration is explicitly not, per
   `basis: "documentary"` in the one verified closure-finding-producing
   code path and per the family declaration's own scope-limited
   `closure_claim` text.

## Independent standpoints

CQ-1 ran four full lenses by default because the format itself was
unproven. The format is now proven once; this milestone tests generalization
leanly, not by repetition. Propose exactly **two** independent standpoints,
each justified by a specific disagreement or gap this interaction type is
likely to expose that a single account would not catch:

1. **Casual invested reader** (Claude sub-agent, `general-purpose` or
   `Explore`-derived, spawned fresh with only the Track 0 packet). Carried
   over from CQ-1 because the standing test is explicitly about this
   reader, and CQ-1 found this lens's misattribution findings (SC-9, "we
   found") were among the strongest convergences — the same voice risk
   plausibly recurs in a declaration request ("we found this is complete"
   would be a worse error here, since it would misattribute the user's own
   assertion to the system).
2. **System and provenance adversary, run on Grok** (`mcp__grok__grok_consult`,
   confirmed reachable this session). Justified narrowly: CQ-1's Lens D
   (system/provenance) independently re-derived the strongest single
   finding of that inquiry (SC-3) by reading the presentation generator
   directly. A declaration request's defining risk is different from a
   presented result's: whether the request accurately represents what the
   engine actually does with the assertion (blocks vs. computes vs.
   silently ignores) rather than whether a shown number is misleading.
   Running this lens on a different model (Grok, not Claude) is also a
   deliberate methodology check the owner authorized: does an
   independently-different model reach the same verified facts through the
   same code, or does it diverge — itself evidence about whether these
   findings are model-artifacts or code-grounded.

**Not run by default, with reasons:**

- *Tax/financial-practice adversary* (CQ-1 Lens B): CQ-1's practice-lens
  findings were almost entirely about the presented **number** (gross vs.
  net subtotal, undisclosed categories) — see SC-5, SC-10. A declaration
  request has no number yet; the practice-relevant question ("what does a
  preparer expect this checkbox to mean") collapses into the scope-trace
  work Track 0 already does directly against the family and mapping
  artifacts. Not run unless Track 0 surfaces a live practice disagreement.
- *Legal/epistemic adversary* (CQ-1 Lens C): produced SC-8, SC-9, SC-11,
  SC-12 — voice, vocabulary collision, and boundary-placement findings. The
  ones most relevant here (SC-8's `attested` collision, SC-12's
  `closure_claim` voice) are **inherited, verified, and cited above**, not
  re-derived; re-running the full lens would mostly reproduce that
  inheritance. Track 0's own claim-boundary trace step is scoped to catch a
  genuinely new instance of this class if one exists for a declaration
  specifically (e.g., does asking a user to "attest" collide the same way
  the disposition text already does).

This leaves the milestone materially leaner than CQ-1 (two standpoints
instead of four, one of them explicitly comparative-methodology rather than
purely additive) while keeping a justified reason, tied to CQ-1's own
evidence, for each inclusion and each omission.

## Tracks

### Track 0 — Inquiry frame and verified trace

- Independently re-verify every artifact and code claim in "Verified
  concrete witness" above against `origin/main` at the branch base — do not
  trust this plan's summary as a substitute for reading the cited files.
- Fix the user situation and draft the two-sentence plain answer only after
  the trace supports it.
- Determine whether the trace reaches a Schedule B attachment branch; if so,
  state the OV-1 counterfactual per the posture above; if not, leave OV-1
  out.
- Exercise both a "ready to declare" and a "not yet ready" concrete
  synthetic case using existing scenario fixtures
  (`packages/sample_data/tax/scenarios/unclosed_interest_composition/` or
  equivalent) as evidence for what the engine actually does in each case —
  do not describe hypothetical UI behavior no code path implements.

### Track 1 — Two independent standpoint accounts

- Casual invested reader (Claude, spawned fresh from the Track 0 packet
  only).
- System/provenance adversary (Grok, via `mcp__grok__grok_consult`, same
  packet).
- Neither account consolidates or dispositions its own findings.

### Track 2 — Explanation tree, tension catalog, and CQ-1 delta

- Build the progressive explanation tree for the declaration request,
  answering the seven numbered questions in the objective.
- Catalog tensions the two standpoints expose.
- Produce the explicit cross-inquiry delta against CQ-1: repeated, changed,
  disappeared, new branches (see Scope item 8).
- Keep the six completeness-adjacent notions (see above) visibly distinct
  throughout.

### Track 3 — Curated inquiry, register update, next-step recommendation

- Curate the end-to-end inquiry document.
- Update `actionable-considerations.md`: close or reassess CQ-2; add or
  annotate SC-entries the evidence actually supports; do not promote
  anything into implementation scope.
- State explicitly whether a reusable explanatory structure appears to be
  emerging across CQ-1 and CQ-2, and what evidence would confirm or refute
  that after only two data points.
- Recommend cross-inquiry reduction, a contrasting inquiry, a bounded
  build/decision milestone, or a stop.

## Exit criteria

The milestone is complete when:

1. every claim in "Verified concrete witness" has been independently
   re-verified by Track 0 against committed artifacts and runtime behavior
   (not merely cited from this plan), **each verification naming the exact
   artifact surface read, the sibling fields present and not relied on, and
   the consumers of the same artifact** (**criterion text corrected
   2026-08-19**: a row was graded Confirmed against a narrower surface than
   its claim's scope, which the original wording permitted);
2. the declaration request has an explicit account of proposition, speaker,
   basis, scope, effect, non-effect, **every** invalidator, and at least one
   unsupported neighboring inference (**corrected 2026-08-19**: "invalidator"
   singular was satisfiable by a true-but-partial account);
3. an honest "not yet" path exists, grounded in the engine's actual
   `blocked` behavior, and the withdrawal/staleness account states **every**
   verified invalidator — horizon succession and same-fact correction under
   `free` supersession — with the places a further mechanism could live
   named and checked, and nothing invented (**criterion text corrected
   2026-08-19**: it previously read "stated from the verified
   horizon-succession behavior," which a true-but-partial account
   satisfied);
4. committed behavior and any OV-1 counterfactual are kept explicitly and
   visibly separate throughout, with the counterfactual included only if
   Track 0 finds the trace materially reaches it;
5. a cross-inquiry delta against CQ-1 names, specifically, which
   explanatory branches repeat, change, are absent, and are new;
6. the actionable register is updated with a consolidated, actionable
   result and no automatic implementation scope is created; and
7. the owner has enough evidence to choose cross-inquiry reduction, another
   contrasting inquiry, a bounded build/decision milestone, or a stop.

Completion does not establish a general theory of declaration requests, user
attestation, or claim integrity across the product. It establishes whether
this second, materially different interaction type extends, contradicts, or
leaves untested the explanatory structure CQ-1 produced.

## Data safety

Only committed, obviously synthetic repository artifacts, existing scenario
fixtures, and public tax/IRS sources may be used. No personal data, real
run, real value, or workspace detail. Grok is an external model call;
Track 1's Grok-lens prompt must contain only the same synthetic Track 0
packet already safe to publish in CQ-1's Track 1 accounts — no repository
secrets, no local paths beyond what is already committed and public.

## Verification

Documentation-only, same posture as CQ-1: `python3 tools/governance_lint.py`,
CI `verify` as gate of record, final candidate diff entirely under `docs/`.

## Execution record

All four tracks ran and closed, followed by a two-pass owner-directed factual
repair. The milestone is **closed**; no ADR, governance revision, schema,
rule-language, engine, or content change was produced.

- **Track 0 — closed.** `inquiries/cq2-track-0-inquiry-frame.md`. Independent
  re-verification of the plan's witness claims, executed evidence for both
  runtime states, and the Schedule B gate decided as materially reached, so
  `OV-1` entered as a bounded counterfactual only. **Superseded in part by the
  repair:** §7's horizon-only invalidator claim is disproven; §2's admission
  account stands. Carries a supersession notice.
- **Track 1 — closed.** `inquiries/cq2-track-1-casual-reader.md` and
  `inquiries/cq2-track-1-system-provenance-grok.md`. Two independent
  standpoints, same Track 0 packet as sole evidence boundary, no contact. They
  converged on the State B misattribution paragraph and split on whether the
  packet's plain answer overstates what a declaration does; the split was
  recorded without disposition. **Regraded 2026-08-20** after independent
  review of the publication candidate: the casual-reader account asserts
  neither of the errors the repair corrected, but the Grok account asserts
  **both** — Attack 4 the horizon-only invalidator, Attack 3 record-layer
  equivalence — while filing the same two questions as termination points in
  its own §4. The earlier record here said neither account asserted either
  error; that was wrong, and the Grok packet now carries a supersession notice
  added later than the other two for that reason.
- **Track 2 — closed.** `inquiries/cq2-track-2-explanation-tree.md`.
  Dispositioned the Track 1 split, settled further tensions, built the
  request-rooted evidence-classed tree, and produced the four-way CQ-1 delta.
  **Superseded in part by the repair:** §4.3's "not representable" disposition
  and §4.4's horizon-only invalidator claim are both disproven. Carries a
  supersession notice.
- **Track 3 — closed.** `inquiries/cq2-track-3-curated-inquiry.md` and the
  updated `actionable-considerations.md`. Curated account, register update,
  exit-criteria assessment, generality assessment, owner options with a
  recommendation that does not select.
- **Owner-directed factual repair — complete, two passes.** Corrected the
  record/admission layer conflation into the four-layer closure account,
  enumerated both invalidating mechanisms, reconciled the two errors packet by
  packet (§14.1), consolidated `SC-13`/`SC-15`, corrected `SC-14`, narrowed
  `SC-16`, bounded what ADR-0055 licenses, added the completeness/neighborhood
  safeguard, and regraded the exit criteria. No new exploration round was run.

**Exit criteria: four of seven met, three partially met** (criteria 1, 2, and
3 partially met). Per-criterion evidence is in
`inquiries/cq2-track-3-curated-inquiry.md` §11; the criterion texts themselves
were corrected during the repair so that a true-but-partial account no longer
satisfies them.
