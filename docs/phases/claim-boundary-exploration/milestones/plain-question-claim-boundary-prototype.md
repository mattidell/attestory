<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Claim Boundary Exploration",
  "topic": "claim-boundary-exploration",
  "milestone_state": "planned",
  "status": "Owner-approved 2026-08-19. The phase and opening line-2b inquiry are selected; Track 0 is next. No agent round, ADR, or implementation has begun.",
  "current_role": "Foreman — charter Track 0 inquiry frame and current-system trace",
  "current_prompt": "docs/phases/claim-boundary-exploration/milestones/plain-question-claim-boundary-prototype.md",
  "scope": [
    "trace one plain user question through one committed synthetic Form 1040 line-2b example verified against a named comparison package (v33, the highest-numbered core package present)",
    "produce a plain answer, progressive explanation, claim-boundary trace, adversarial accounts, and actionable synthesis",
    "test whether the inquiry format is useful before designing a general explanation system"
  ],
  "non_goals": [
    "no ADR, governance revision, production UI, schema, rule-language, engine, filing, or tax-coverage change",
    "no exhaustive semantic taxonomy or general definition of claim, integrity, completeness, or correctness",
    "no personal data, real-run operation, or professional-attestation claim"
  ],
  "deep_reads": {
    "new_milestone": [
      "docs/milestone-retrospectives/2026-08-18-engine-breadth.md",
      "docs/phases/claim-boundary-exploration/claim-boundary-exploration-overview.md",
      "docs/phases/claim-boundary-exploration/actionable-considerations.md"
    ]
  }
}
-->

# Milestone: Plain Question to Claim Boundary Prototype

- Phase: Claim Boundary Exploration
- Milestone key: `claim-boundary-exploration`
- Status: **planned; owner-approved 2026-08-19**
- Base: `origin/main` at `373c0c2f7621c6350db1493df1685f1c141410cb`
- Branch: `milestone/claim-boundary-exploration-phase-definition`
- Decision posture: exploratory and non-authoritative; no ADR is produced

## Objective

Determine whether a concrete plain-language user question can be traced through
the existing system deeply enough to produce a useful ordinary answer, expose
the boundaries of what that answer invites the user to believe or do, and
identify a small set of actionable product consequences.

The worked question is:

> Why is this amount on my return?

The bounded example is Form 1040 line 2b, “Taxable interest,” using a committed
synthetic interest-adjustment presentation fixture. That fixture adopted an
earlier package (v15), but its line-2b rule v4 and form-field v5 are unchanged
in core package v33 — the highest-numbered core package present and this
milestone's comparison target. No committed artifact designates a current
package. Track 0 must verify the rest of the material chain against that
comparison target before treating it as evidence. The
milestone is successful if the example makes a narrower next product question
possible. It need not prove a general claim model or produce a shippable
explanation surface.

## Current state

The repository already carries:

- a seven-family positive-interest composition and three separately
  closed Schedule B adjustment classes;
- a versioned Form 1040 line-2b field, cited computation rule, adopted package,
  derived finding pins, explanation text, and presentation-model projection;
- synthetic presentation evidence at
  `packages/sample_data/schedule_b_interest_adjustments/presentation/mixed-schedule-b-interest-adjustments.presentation-model.v1.json`;
- accepted contracts distinguishing findings, rules, citations, source-family
  closure, publication, explanation, presentation, and the filing boundary; and
- no product artifact that answers the selected user question in a deliberately
  plain, progressively decompressible way.

The selected fixture is complex enough to test the inquiry: the visible amount
rests on multiple positive source families, multiple adjustment classes,
closures, a rule, a citation, a form-field mapping, and a presentation model.
Its complexity is evidence to inspect, not language to repeat to the user.

## Scope

1. Establish the exact user situation and the interpretations compressed into
   the selected question.
2. Reconstruct the synthetic line-2b support chain from presentation row through
   field, finding, pins, rules, source-family authority, citations, and relevant
   official tax instructions; verify every material selected version against the
   v33 comparison package.
3. Draft the shortest useful plain answer before writing technical exposition.
4. Provide progressive explanation layers for origin, calculation, tax
   relevance, included and excluded scope, uncertainty, and possible next
   action.
5. For every material statement or affordance, trace what the user is invited
   to believe or do, who supplies that proposition, what supports it, what
   invalidates it, and which nearby inference is unsupported.
6. Exercise at least one positive state and one boundary state in which a
   necessary source-family authority or dependency is absent, so the inquiry
   explains both appearance and nonappearance.
7. Obtain independent exploratory accounts from four lenses:
   casual invested reader, tax/financial-practice adversary,
   legal/epistemic adversary, and system/provenance adversary.
8. Reduce the accounts into the smallest actionable changes, limitations,
   evaluation probes, and bounded future inquiries.
9. Update the actionable consideration register and recommend whether the next
   inquiry should concern relevance, visibility, action readiness, attestation,
   grammar, governance narrative, or no continuation.

Explorers may follow a discovered angle beyond the initial decomposition when
they can name the answer, implication, action, limitation, evidence need, or
future product requirement it could materially change.

## Non-goals

- No production answer text, interface, interaction design, or implementation.
- No schema, citizen, engine, runner, rule artifact, tax content, package,
  release, fixture-generation, or presentation-model change.
- No ADR, governance amendment, adopted definition, or claim of doctrinal
  resolution.
- No comprehensive definition of `claim`, `integrity`, `complete`,
  `completeness`, `correctness`, or `fact`.
- No use of `integrity` or `complete` as required user-facing design terms.
- No general CPA, tax-preparer, lawyer, or consumer simulation beyond the
  selected question and scenario.
- No conclusion that a generated return has legal effect before filing, and no
  use of that boundary to deny that the computation and placement represent tax
  meaning.
- No filing, transmission, entry-surface, real-data, or additional tax-coverage
  work.
- No durable catalog entry without a plausible action path.

## Contracts and authority posture

This milestone creates no product contract. Governance and accepted ADRs remain
the authority for what existing artifacts mean. Inquiry documents may describe
tensions, possible defects, or candidate revisions, but they do not reinterpret
an accepted contract into new behavior.

The working phrase *claim boundary* remains an exploratory lens. If the inquiry
shows that a durable representation, user-visible concept, or governance change
is needed, the milestone records the decision question and stops short of
adopting it.

Official tax sources are used to determine what the selected line and its
components are intended to report. Model-agent accounts may criticize or
compare that reading; they are not treated as tax or legal authority.

## Inquiry artifacts

The milestone produces:

- `inquiries/why-is-this-amount-on-my-return.md` — the curated end-to-end
  inquiry, plain answer, decompression layers, support trace, boundary state,
  and claim-boundary map;
- exploratory accounts under
  `inquiries/why-is-this-amount-on-my-return/`, one per assigned lens;
- a synthesis section in the curated inquiry distinguishing converged findings,
  material dissent, discarded threads, and actionable consequences;
- an updated `actionable-considerations.md`; and
- roadmap and phase-state updates only if the owner selects what follows.

Working agent accounts are evidence for the milestone, not permanent project
authority. At close, retain only accounts needed to recover material dissent or
the synthesis; remove redundant working prose.

## Synthetic scenarios

| Case | Situation | Question exercised | Required result |
| --- | --- | --- | --- |
| CB-P1 | Existing mixed positive-interest and adjustment presentation fixture publishes line 2b | Why is this amount here? | A plain answer connects the visible amount to the relevant asserted/derived support, computation, form placement, included scope, limitation, and next inspection path. |
| CB-N1 | Paper mutation removes or makes stale one necessary source-family closure while leaving the neighboring presentation context otherwise recognizable | Why is there no amount yet? | The explanation identifies the exact missing authority or dependency and a concrete next action without calling the return globally incomplete. |
| CB-A1 | Same positive state, read as though the rendered return were legally operative | What may the user infer? | The trace distinguishes tax meaning and computational support from the legal effect of filing, without pretending the output has no tax-law association. |
| CB-A2 | Same positive state, but visible text omits the bounded source universe or adjustment qualification | What could mislead? | At least one adversary tests whether a reasonable user would infer broader taxable-interest coverage than the support warrants. |

The negative and adversarial cases are paper probes against synthetic content.
They do not require modifying committed fixtures or running personal data.

## Agent focus and leeway

Every account begins with the exact user question and ends with:

1. the best two-sentence plain answer it can support;
2. what an intelligent casual user could still misunderstand;
3. the deepest thread it followed and why that thread changed the answer or its
   boundary;
4. the evidence or authority at which its explanation terminates;
5. concrete actions the project could take; and
6. threads it deliberately discarded because they had no plausible action.

The lens controls what the agent notices, not the conclusion it must reach.
Accounts may disagree and may recommend stopping the project or abandoning the
working frame.

## Evaluation questions

- Can a casual reader recover what the visible amount represents without
  learning the engine's vocabulary first?
- Does the plain answer preserve the distinctions needed for tax and legal
  adequacy?
- Can every material clause be traced to existing support or identified as a
  product judgment?
- Does the answer identify the system, user, source document, adopted artifact,
  and tax authority in the correct speaking roles?
- Does the presentation invite a broader inference than its included universe,
  horizon, authority, or action readiness supports?
- Can the inquiry explain a blocked state as a concrete missing condition and
  next action rather than a global completeness judgment?
- Does progressive decompression add clarity at each layer, or merely restate
  project terminology?
- Which discovered distinctions would change a product answer, engine
  requirement, explanation capability, explicit limitation, or future test?
- Which distinctions are intellectually real but presently unactionable?

## Verification

The milestone is documentation-only. Completion evidence consists of:

- direct traceability from the curated inquiry to the named synthetic fixture,
  current content artifacts, accepted contracts, and official tax sources;
- all four synthetic cases explicitly answered;
- each required independent account present and bounded to the selected
  question;
- a synthesis that separates convergence, dissent, discarded threads, and
  actionable consequences;
- every new actionable-register entry naming a plausible action;
- no ADR, schema, code, package, published artifact, or personal-data change;
- a final candidate diff whose changed paths are all under `docs/`;
- `python3 tools/governance_lint.py`; and
- CI `verify` on the final candidate as the gate of record.

The milestone does not score the prose by expert confidence alone. A fresh
reader must attempt the declared recovery questions without access to the
authoring discussion. The plan may use model agents for that measurement, while
recording that the result is simulated evidence rather than user research.

## Data safety

Only committed, obviously synthetic repository artifacts and public tax sources
may be used. Inquiry documents must not describe a real run, real value, real
document, private output, disposition, refusal reason, or workspace location.
No agent receives personal data. Model-agent accounts remain safe to publish.

## Tracks

### Track 0 — Inquiry frame and current-system trace

- Fix the selected scenario, user situation, compressed subquestions, support
  chain, official-source set, positive case, and boundary mutation.
- Draft the initial two-sentence answer only after the trace can support it.
- Stop if the fixture cannot represent the selected question without a code or
  contract change; record that as an actionable result rather than expanding
  the milestone.

### Track 1 — Independent expansion accounts

- Run the four lens-specific inquiries from isolated starting contexts sharing
  only the Track 0 packet and the standing agent-focus questions.
- Permit each account to drill into one consequential angle.
- Do not ask an explorer to consolidate or disposition its own expansion.

### Track 2 — Adversarial reduction and plain-answer prototype

- Compare accounts by user consequence rather than shared terminology.
- Test competing short answers against domain adequacy, likely over-inference,
  action clarity, and decompression quality.
- Preserve material dissent and remove threads without a plausible project
  action.

### Track 3 — Curated inquiry and next selection

- Produce the curated inquiry and update the actionable register.
- State what generalized, what remained specific to line 2b, and what the
  example could not test.
- Recommend one bounded next inquiry, a pivot, or phase close. The owner selects
  the next move.

## Track 0 adversarial closure

Not applicable. Track 0 does not settle contributed authority, aggregate or
absence declarations, claim reuse, or a neighboring integration contract. It
reads existing accepted artifacts as the object of an exploratory product
inquiry and makes no implementation-ready decision.

## Exit criteria

The milestone is complete when:

1. the selected positive and boundary states have end-to-end curated inquiry
   traces;
2. a casual-reader answer exists at two sentences or fewer, with optional
   deeper layers that remain connected to actual support;
3. every material invited belief or action in that answer has an identified
   speaker, basis, scope, invalidator, and unsupported neighboring inference;
4. all four independent lenses have produced bounded accounts;
5. synthesis distinguishes domain defects, communication defects, engine or
   provenance gaps, explicit limitations, and unactionable research;
6. the actionable register and roadmap reflect the result without converting
   it into automatic implementation scope;
7. no product contract or governance meaning has been adopted; and
8. the owner has enough evidence to select a contrasting inquiry, a narrower
   build or decision milestone, a pivot, or a stop.

Completion establishes that the exploration method yielded a useful bounded
result once. It does not establish a general semantic model, user-validated
communication utility, professional correctness, or claim integrity across the
product.
