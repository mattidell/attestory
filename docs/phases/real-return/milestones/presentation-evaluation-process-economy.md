<!-- foreman-context-v1
{
  "version": 1,
  "topic": "presentation-evaluation-process-economy",
  "milestone_state": "closed",
  "retrospective": "docs/milestone-retrospectives/2026-07-25-presentation-evaluation-process-economy.md",
  "status": "closed early by owner direction 2026-07-25; Track 0 is the accepted economy foundation; Track 1 was rejected and not merged; Tracks 2-3 were retired",
  "scope": [
    "versioned UI/UX iteration workload observation and comparison data",
    "machine-readable presentation-iteration baseline with explicit missing and estimated values",
    "quality-adjusted comparison of UI/UX execution treatments on comparable work",
    "dependency-free path-independent browser evaluation harness",
    "one isolated reusable Chrome session per batch run",
    "criteria by fixture by candidate by tamper-case matrix execution",
    "reusable synthetic fixtures and citation-walk example templates",
    "deterministic evaluation reports and reproducible economy summaries",
    "milestone-local tier-matched builder and reviewer allocation"
  ],
  "non_goals": [
    "no product presentation surface or maturity-matrix lift",
    "no presentation contract ADR or information-design framework",
    "no evaluation or conclusion about non-presentation workflows",
    "no cost-only optimization or economy claim that ignores result quality",
    "no causal claim from unmatched historical and treatment observations",
    "no real workspace, credential, remote URL, personal output, or network access",
    "no generic browser automation framework or dependency installation",
    "no routine rival builders or duplicate artifact reviewers for already-settled criteria"
  ],
  "deep_reads": {
    "implementation": [
      "docs/phases/real-return/milestones/presentation-evaluation-process-economy.md#Tracks",
      "docs/prototypes/human-presentation-citation-walk/analysis/04-economy.md",
      "docs/prototypes/human-presentation-citation-walk/analysis/05-technical-findings.md",
      "docs/prototypes/human-presentation-citation-walk/reference/harness-seed/README.md",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "launch": [
      "docs/roles/foreman.md#Spawning",
      "docs/adr/0043-foreman-dispatch-instruction.md#Decision",
      "docs/adr/0013-prototype-economic-gates.md#Decision",
      "docs/phases/real-return/milestones/presentation-evaluation-process-economy.md#Presentation execution economy and review allocation"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/prototypes/human-presentation-citation-walk/analysis/01-feature-citation-walk.md",
      "docs/prototypes/human-presentation-citation-walk/analysis/05-technical-findings.md",
      "docs/phases/real-return/milestones/presentation-evaluation-process-economy.md#Review gates"
    ],
    "new_milestone": [
      "PROJECT_PLANNING.md#Required Milestone Plan Contents",
      "docs/milestone-retrospectives/2026-07-24-presentation-exploratory-milestone.md",
      "docs/milestone-retrospectives/2026-07-23-live-run-system-definition-and-trust-domains.md",
      "docs/milestone-retrospectives/2026-07-23-foreman-context-loading.md",
      "docs/milestone-retrospectives/2026-07-22-push-envelope-preflight-and-bypass-visibility.md",
      "docs/milestone-retrospectives/2026-07-22-correction-authority-and-marshaller-simplification.md"
    ],
    "schema_or_fixture": [
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules",
      "docs/governance/constitution.md#Article 18 — Quarantine",
      "docs/governance/engineering-constraints.md#E18.3 (Quarantine) — Synthetic provenance"
    ],
    "merge_or_records": [
      "docs/adr/0030-branch-and-merge-strategy.md#Decision",
      "docs/roles/foreman.md#Standing disciplines",
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ]
  }
}
-->
# Milestone: Presentation Evaluation Process Economy

Status: **closed early by owner direction 2026-07-25; closeout PR #68 merged
as `a14e8bf`.** The owner-approved planning unit merged in PR #65 (`1fd3d4c`)
and Track 0 merged in PR #66 (`870c8ed`). Track 0 is the accepted
presentation-economy foundation. Track 1's independent review returned
`NOT READY`; its implementation was not merged, its prepared repair/re-review
were retired unexecuted, and Tracks 2–3 were canceled. This is an honest
partial close, not completion of the original 15 exit criteria.

## Objective

Create a durable presentation-iteration economy learning loop:

```text
declare comparable work → observe cost and outcome → compare a treatment
→ retain the data → choose the next improvement
```

The Presentation Exploratory Milestone's repeated browser-review work is the
first measured workload, and a reusable evaluation harness is the first
intervention. One command will evaluate a matrix of synthetic fixtures,
candidate surfaces, criteria, and tamper cases in one isolated browser session.
A companion presentation-economy toolkit will preserve the UI/UX workload
definition, historical baseline, treatment observations, coverage/quality
results, and qualified comparison so later presentation-development and review
changes can be evaluated against accumulated data rather than impressions.

The milestone is successful only if it improves the project's ability to
**learn about economy in UI/UX iteration over time**. A cheaper presentation
execution that checks less, misses seeded defects, or shifts work invisibly to
another role is not an economic improvement.

## Owner closeout disposition — 2026-07-25

The owner stopped the milestone after determining that its primary purpose was
to establish a foundation for monitoring and managing presentation-milestone
cost, not to perfect a general browser harness before any product presentation
milestone existed.

- **Accepted foundation:** Track 0's versioned presentation workload,
  observation, and comparison contracts; the source-faithful historical
  baseline; strict missing/approximate-value treatment; participating-role
  completeness; quality-before-cost comparison; and append/supersession path.
- **Preserved negative evidence:** Track 1's `NOT READY` review and execution
  trace. The review found six blockers and showed that Chrome execution was
  batched and relatively compact while context ingestion and adversarial
  reasoning remained material costs.
- **Not adopted:** the unrepaired Track 1 harness implementation. It remains on
  `track/presentation-economy-t1-harness-core` as historical branch evidence
  and is not an executable project capability.
- **Retired:** the Track 1 repair and delta-review charters, Track 2 standing
  corpus/paired pilot, and Track 3 operating-integration gate.
- **Next use:** actual presentation milestones declare their work and record
  observations through Track 0. A later workload may justify a smaller
  workload-specific helper; the failed general harness is not a prerequisite.

The foreman also records the allocation rule established by this run: known
adversarial classes must be supplied to both Builder and Reviewer as shared
inputs. The Builder closes applicable known classes; mechanical checks verify
them; the Reviewer is chartered around the remaining novel boundary. The
foreman, not the Reviewer, is accountable for avoiding repeated discovery
spend.

## Current state

The exploratory milestone demonstrated a stable
surface-a-criterion → specify → verify loop across five cycles. It preserved:

- six proof-of-concept Node scripts containing the recurring CDP, contrast,
  citation-identity, keyboard, blocking, and fault-injection checks;
- two synthetic fixture descriptions and two converged citation-walk
  implementations;
- evidence that roughly 65–80% of the exercised UI-quality surface is
  mechanically checkable; and
- evidence that reviewers cost roughly 1.5–2 times builders largely because
  each reviewer rebuilt the same browser and check apparatus.

The scripts under
`docs/prototypes/human-presentation-citation-walk/reference/harness-seed/` are
reference-only: they hard-code ports and candidate paths, duplicate CDP
plumbing, assume an externally launched browser, and are not runnable as a
single battery. The fixtures are human-readable Markdown rather than a
machine-driven standing corpus. The two final prototypes remain useful rival
examples, but neither is selected as a product presentation contract.

The economy analysis records per-agent tokens, tool calls, and wall time for
most builder/reviewer runs, but the table is prose, some values are approximate
or missing, the foreman's cost was not measured, and the recurring-check share
was not isolated from reasoned review. It is valuable historical evidence, not
a controlled baseline. Today the repository has no machine-readable workload
definition, observation format, comparison tool, quality-normalization rule, or
appendable dataset for evaluating whether a later presentation-development or
review change actually improved execution.

Node and Chrome are external execution prerequisites, not repository
dependencies. The implementation must discover or accept an explicit Chrome
executable at runtime and fail honestly when unavailable; it must not download
a browser or add a package manager.

## Decision posture

This milestone makes reversible internal tooling and fixture-organization
choices. It introduces no workspace citizen, published schema, product
contract, or mandatory project-wide review doctrine. The economy workload,
observation, and comparison shapes and the harness manifest/result shapes are
versioned tool-local diagnostic interfaces, documented and test-pinned but not
authoritative workspace state.

No ADR is planned. ADR-0013 already establishes tier matching and the foreman's
scope-and-economy duty; ADR-0043 already governs dispatch. The exploratory
analysis already exercised rival builds and repeated reviews for the check
logic. Re-running a decision prototype would pay again for settled evidence.
If implementation requires choosing a user-visible presentation meaning,
making the harness normative, or changing dispatch authority, stop and route
that proposition separately at the appropriate decision tier.

## Scope

1. Add a dependency-free presentation-economy toolkit under
   `tools/presentation_economy/` that strictly validates UI/UX workload,
   observation, and comparison data and emits deterministic summaries.
2. Convert the exploratory milestone's C1–C5 cost table into a
   machine-readable, provenance-linked baseline. Preserve missing values as
   missing and approximate values as approximate; never reconstruct data that
   was not captured.
3. Define quality-adjusted comparison: cost deltas are interpretable only
   alongside comparable scope, criteria coverage, seeded-defect detection,
   review outcome, rework, and cost shifted to other roles.
4. Promote the reference scripts into a dependency-free Node harness under
   `tools/presentation_harness/`, instrumented to emit economy observations as
   well as deterministic evaluation results.
5. Launch one fresh, isolated Chrome process per harness invocation, reuse it
   across the batch, and use a fresh target for each matrix case.
6. Serve only repository-relative candidate files over an ephemeral loopback
   HTTP origin. Reject remote URLs and out-of-repository paths; detect and fail
   any non-loopback browser request.
7. Move candidate paths, selectors, fixture expectations, criterion parameters,
   and tamper definitions out of check code and into a versioned manifest.
8. Execute criteria × fixtures × candidates × tamper cases in one run. A
   failing check must not prevent independent cases from running; a harness,
   browser, load, timeout, or malformed-manifest failure must never appear as a
   criterion pass.
9. Emit a deterministic JSON report on standard output plus a compact
   human-readable summary. Reports contain criterion ids, outcomes, fixed
   reason codes, and repository-relative target names—never page HTML, rejected
   values, temporary paths, ports, or browser locations.
10. Promote the minimal and rich-reuse synthetic fixtures into a
   machine-readable standing corpus and preserve both converged citation-walk
   shapes as example templates without declaring either the product design.
11. Pin each settled criterion to its provenance cycle and an executable check,
   preserving the exploratory analysis's
   `{criterion, automated check, provenance-cycle}` trace.
12. Run one bounded, owner-authorized comparison of equivalent presentation
    review work under a manual-baseline treatment and a harness-assisted
    treatment. Record both quality and cost, label the evidential limits, and
    seed an appendable dataset for later presentation-iteration experiments.
13. Document how a future UI/UX development or review change declares its
    workload, baseline, treatment, quality floor, measurements, and limits; how
    it appends observations; and how comparison results inform rather than
    dictate a presentation-process decision.

## Non-goals

- No user-facing application, product renderer, product template selection,
  form-field integration, or change to any maturity-matrix cell.
- No presentation-surface ADR, agent-driven-evaluation ADR, information-design
  framework, aesthetic rubric, or claim that human taste has been automated.
- Evaluation of tax-rule, schema, kernel, governance, security,
  prototype-decision, and other non-presentation work is outside this
  milestone's scope. The plan makes no economic claim about those workflows.
- No cost-only score, universal productivity ranking, agent leaderboard, or
  optimization that treats fewer tokens, calls, agents, or seconds as success
  when coverage or result quality changed.
- No causal claim from the historical C1–C5 table or a single unmatched
  before/after run. Historical, paired-pilot, and repeated evidence remain
  visibly distinct.
- No implementation of the unresolved redact-versus-echo, diagnostic-value, or
  blocked-salience product decisions named by the exploratory analysis.
- No generic Playwright/Selenium replacement, browser farm, screenshot
  service, visual-diff platform, dependency download, or network-backed check.
- No real workspace, real return, personal fixture, credential, remote URL,
  owner browser profile, quarantined output, or absolute local path in a
  manifest or report.
- No change to governance, published schemas, tax rules, artifact packages,
  runners, live-run tools, or data-boundary maturity.
- No automatic disposition of reasoned reviewer findings. The harness reports
  mechanical evidence; it does not judge information design or aesthetics.
- No transcript, prompt, chain-of-thought, page body, or agent identity in the
  economy dataset. Observations contain bounded execution metadata and outcomes.
- No parallel implementation manifest. Tracks are intentionally sequential
  because measurement precedes intervention and the standing corpus consumes
  the harness contract. The bounded comparison runs its two treatment seats
  sequentially in isolated contexts after their shared workload is frozen,
  avoiding shared-resource contention as an unmeasured wall-time confounder.

## Contracts

### Presentation-economy workload, observation, and comparison

The presentation-economy toolkit has three strict, tool-local JSON versions.
Their declared subject is UI/UX presentation iteration, development, and
review:

- `presentation-economy-workload.v1` freezes the UI/UX unit being compared:
  candidate surface/range, fixture and criterion set, seeded defects, required
  outputs, quality floor, role boundaries, and the one presentation-iteration
  intervention under evaluation.
- `presentation-economy-observation.v1` records one execution: workload id,
  historical/paired/repeated evidence class, treatment label, role and abstract
  tier/effort, agent and browser/session counts, tokens/tool calls/wall seconds
  when actually available, cases/criteria completed, seeded defects detected,
  verdict, rework/recheck events, task-duration budget and observed duration,
  dispatch-batch identity/size and execution mode, foreman idle gap, directly
  observed cache status, and provenance. Every nullable measure carries a
  missing-reason; approximate measures carry an explicit approximation flag.
  Cache status is never inferred from elapsed time or tokens: when the
  orchestration surface does not expose it, it remains explicitly missing.
- `presentation-economy-comparison.v1` references baseline and treatment
  observations, checks workload compatibility, reports per-measure raw deltas
  and ratios, reports coverage/quality equivalence separately, sums cost across
  every participating role, and states an evidence-strength/caveat result.

The toolkit validates and summarizes these files:

```text
.venv/bin/python3 -m tools.presentation_economy validate \
  --dataset <repo-relative-path>
.venv/bin/python3 -m tools.presentation_economy compare \
  --workload <repo-relative-path> \
  --observations <repo-relative-path> \
  --baseline <label> --treatment <label>
```

The comparison command refuses a quality-adjusted economy verdict when the
workloads differ materially, the declared quality floor is not met, a seeded
defect expected by the workload is missed, or a participating role's cost is
unknown for the specific measure being claimed. It may compare a complete
wall-time measure while leaving tokens uninterpretable, for example. It still
reports the raw observations and the exact reason any comparison is
unavailable. Missing data is a result, never a prompt to estimate.

Historical C1–C5 rows are labeled `historical-observational`; the bounded
same-workload manual/harness comparison is labeled `paired-pilot`. Neither is
called causal evidence. Future repeated observations can strengthen the record
without rewriting older rows.

### Quality-adjusted economy

Economy is evaluated as two adjacent results, never one blended score:

1. **Cost:** tokens, tool calls, wall time, task budgets and observed durations,
   dispatch batch/mode, foreman idle gaps, directly observed cache status,
   number/tier of agents, launches, iterations, rechecks, and rework—summed
   across the execution boundary so moving work from reviewer to foreman or
   harness is visible.
2. **Outcome:** declared coverage completed, seeded defects detected, false
   pass/error behavior, review verdict, novel findings, and quality-floor
   satisfaction.

A treatment is economically promising only when the comparable outcome floor
holds and at least one declared cost measure improves without an undeclared
cost shift. The data may show regression, no interpretable difference, or
insufficient evidence; all are valid outcomes. The toolkit informs a later
presentation-milestone foreman/owner judgment and never selects a UI/UX process
change itself. This milestone draws no inference about non-presentation work.

### Command

The public operator surface for this milestone is:

```text
node tools/presentation_harness/run.mjs --manifest <repo-relative-path>
```

An optional runtime-only `--chrome <path>` override may identify an installed
browser. It is never recorded in output or committed configuration.

Exit status is stable:

- `0`: every selected criterion case passed;
- `1`: the harness completed and at least one criterion case failed; and
- `2`: the run could not produce trustworthy criterion results because its
  manifest, target, browser, server, load, injection, or internal execution
  failed.

The process must terminate the browser and remove its temporary profile on
every exit path.

### Manifest

`presentation-evaluation-manifest.v1` is a strict, tool-local JSON shape. It
declares only repository-relative candidates and synthetic fixtures; criterion
ids and parameters; tamper-case ids and injections; timeouts; and the expected
matrix. Unknown keys, duplicate ids, unknown criterion/tamper references,
remote URLs, absolute paths, path traversal, and non-synthetic fixtures are
refused before Chrome launches.

The manifest is configuration for a repository tool, not a workspace citizen
or a published JSON Schema. Its validator and committed positive/negative
examples are the declaration and test surface. If a later consumer needs this
shape as authoritative state, that is a new contract decision.

### Result

`presentation-evaluation-report.v1` is deterministic for the same manifest and
candidate bytes. It records:

- manifest version and repository-relative manifest name;
- each candidate, fixture, tamper case, and criterion id;
- `pass`, `fail`, or `error`, with a closed reason-code vocabulary;
- aggregate counts; and
- a final `passed` boolean.

Ordering is manifest order with criterion ids as the stable tie-breaker.
Ephemeral ports, timestamps, process ids, absolute paths, browser versions,
page content, console dumps, and injected/rejected values are excluded.

The harness also emits a separate `presentation-economy-observation.v1`
fragment for the run. Unlike the deterministic correctness report, this
observation intentionally carries measured wall time, browser/session counts,
case counts, and tool-visible execution measures. Keeping the artifacts
separate prevents volatile measurements from defeating golden determinism
while preserving the UI/UX iteration cost data needed for comparison.

### Check boundary

Checks are named modules over CDP/DOM/computed-style observations. Settled
mechanical criteria include:

- rendered-value and honest-blocking guards;
- visible fail-loud behavior with subsection blast containment and redacted
  diagnostics;
- citation identity and resolvable reuse backlinks;
- landmark, heading, keyboard, focus-visible, and contrast checks; and
- the standardized T1/T2/T3 tamper cases.

Every check names its driving technique. In particular, keyboard checks use
real CDP key events, contrast recomputes WCAG luminance from computed style,
and failure checks use pre-load script injection. Static source claims and
`DESIGN.md` assertions are never accepted as results.

Information-design judgment and aesthetic quality remain outside the result
boolean. The harness may expose observations that help those reviews, but may
not convert an unratified heuristic into a pass/fail requirement.

## Fixtures

The committed presentation-economy data fixtures are:

1. A faithful C1–C5 historical dataset transcribed from
   `analysis/04-economy.md`, with source-row citations, explicit approximate
   values, and explicit missing values—including the unmeasured foreman cost.
2. Valid single-run, paired-pilot, and repeated-run examples for the three
   economy data versions.
3. Invalid examples covering unknown keys, negative counts/durations, missing
   reasons absent for null measures, approximate values without flags,
   incompatible workload ids, cost-shift omissions, unmet quality floors, and
   a comparison that tries to claim causality from historical data.
4. A frozen presentation-review comparison workload: same candidates,
   fixtures, criterion set, T1/T2/T3 seeded cases, required report, and quality
   floor for both treatments. The manual arm executes the complete mechanical
   and residual reasoned-review brief without the new harness. The
   harness-assisted arm consumes the committed mechanical report and executes
   the same residual reasoned-review brief. Neither arm sees the other's result.

All committed presentation fixture material is constructed and uses obvious
`demo-*` identities:

1. `minimal`: one published line with two sources plus one honestly blocked
   line.
2. `rich-reuse`: published interest, dividends, and Schedule B sections reusing
   the same fact citations, plus one honestly blocked line.
3. Manifest-invalid negatives: traversal, remote URL, absolute path, unknown
   ids, duplicate ids, unknown keys, and a fixture not marked synthetic.
4. Runtime negatives: missing target, page-load failure, criterion timeout,
   injected malformed/unknown state, browser exit, and an attempted
   non-loopback request.
5. Two example-template candidates preserving the final freeze-based and
   signature-detection citation-identity strategies. They are regression
   targets and reusable starting examples, not product contracts.

The checked-in corpus includes an expected normalized report for the valid
matrix. Golden updates are intentional, generated only through the harness,
and inspected criterion-by-criterion.

The presentation-economy dataset is append-only by record identity: corrections
add a superseding observation with a reason rather than silently rewriting a
measured value. Dataset validation rejects duplicate observation ids and
dangling workload/comparison references.

## Verification

Focused verification must prove:

```text
.venv/bin/python3 -m unittest tests.test_presentation_economy
.venv/bin/python3 -m tools.presentation_economy validate \
  --dataset docs/presentation-economy/datasets/presentation-exploratory-baseline.v1.json
.venv/bin/python3 -m tools.presentation_economy compare \
  --workload docs/presentation-economy/workloads/presentation-review.v1.json \
  --observations docs/presentation-economy/datasets/presentation-harness-pilot.v1.json \
  --baseline manual --treatment harness-assisted
node --test tools/presentation_harness/tests/*.test.mjs
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/corpus/citation-walk/manifest.json
```

The presentation-economy commands cover strict version validation,
missing/estimated value honesty, provenance, workload compatibility, cost-shift
accounting, task-duration/batching/idle-gap/cache telemetry (including refusal
to infer cache status), quality-floor enforcement, evidence-strength labels,
and deterministic comparison output. The committed historical baseline must
reproduce the published C1–C5 UI/UX iteration table exactly where values exist
and must not fill its gaps.

The Node test command covers strict manifest validation, deterministic
normalization, reason-code closure, matrix expansion, and lifecycle cleanup
using synthetic/local test doubles where appropriate. The harness command is a
required real-Chrome integration run over the committed corpus; a skip or
unavailable browser is not completion evidence.

The real-Chrome run must additionally demonstrate:

- one isolated temporary profile and one browser process serve the whole batch;
- fresh targets prevent cross-case state leakage;
- every request stays on the ephemeral loopback origin;
- fault injection exercises the actual pre-load/throw path;
- all independent cases run after a criterion failure;
- malformed configuration and infrastructure errors exit `2`, never `0`;
- the normalized report matches its reviewed golden; and
- a rerun is byte-identical.

The paired pilot must freeze one workload before either treatment dispatch,
use the same abstract tier/effort and seeded cases, keep the seats independently
contexted, and capture all participating-role costs available from the
orchestration surface. Its comparison must report:

- whether both treatments met the same coverage and seeded-defect floor;
- raw per-treatment tokens, tool calls, wall time, agent count, rework, and
  verdict without hiding nulls;
- cost shifted into harness setup, foreman coordination, or rechecks;
- which differences are measured, merely historical context, or still unknown;
  and
- no economy conclusion beyond the frozen presentation workload from the
  single pair.

Every track also runs:

```text
.venv/bin/python3 -m unittest
.venv/bin/python3 -m mypy
.venv/bin/python3 tools/governance_lint.py
.venv/bin/python3 tools/envelope_scan.py --range main..HEAD
git diff --check main..HEAD
```

## Data safety

The harness is an outside-quarantine development tool and therefore accepts
synthetic repository material only. It:

- rejects remote URLs, path traversal, and candidate/fixture paths outside the
  repository;
- creates only a temporary browser profile and loopback HTTP server;
- fails any browser request outside loopback;
- never reuses the owner's browser profile, cookies, extensions, or signed-in
  session;
- never serializes page bodies, error values, temporary paths, or local browser
  locations into reports; and
- leaves ad hoc reports and browser artifacts uncommitted.

Committed fixtures carry an adjacent manufacturing-provenance note and obvious
demo identifiers. The implementation and review both run the envelope scan.
No real-data run or owner attestation belongs to this milestone.

Presentation-economy observations describe UI/UX iteration work, never user
data or agent content. They may record abstract role/tier/effort, counts,
durations, verdicts, criterion ids, branch/PR names, and repository-relative
evidence pointers. They exclude prompts, responses, reasoning traces, page
content, local absolute paths, model-account identity, credentials, environment
variables, and remote configuration. A provenance pointer names the committed
source record; it does not copy that record's content into the dataset.

## Presentation execution economy and review allocation

The design space for the settled checks already had ten builds and ten reviews.
Routine implementation therefore uses one builder and one specialized
independent reviewer per track—no rival builder and no duplicate general
reviewer. The sole exception is the bounded Track 2 paired pilot: one manual
and one harness-assisted participant execute the same frozen review workload
to generate comparative data. They are measurement participants, not the
track's independent gate reviewer. ADR-0043 requires explicit owner
authorization before every dispatch, including each pilot seat.

| Unit | Builder | Reviewer | Economic boundary |
| --- | --- | --- | --- |
| Track 0 — measurement substrate | Medium / medium | High / high, measurement-integrity lens | Comparability and quality-adjustment are novel; review attacks false economy and invented precision. |
| Track 1 — harness core | Medium / medium | High / high, technical-adversary lens | Novel failure semantics, instrumentation, and browser lifecycle justify the one High review. |
| Track 2 — corpus and paired pilot | Medium / medium builder; two Medium / medium pilot participants | High / high, comparison-integrity lens | Check logic is settled, but equivalent-work measurement and cost-shift accounting require independent scrutiny. |
| Track 3 — operating record | Foreman; Economy clerk eligible only for mechanical collation if separately authorized | Medium / medium, records lens | No artifact-quality or economic interpretation is delegated to a clerk. |

Reviewers receive the exact workload, harness command where applicable, seeded
negative cases, expected reason codes, and committed golden in their charter.
A reviewer does not rebuild the check rig. Pilot participants receive the same
frozen object and quality floor; only the treatment-specific apparatus differs.
Rechecks along the same review lineage may reuse that seat at lower effort; a
first independent review and each pilot arm use fresh contexts.

The foreman re-enters from this plan and the track record rather than carrying
raw builder/reviewer transcripts. Economy observations are recorded from the
orchestration result and committed source records, not reconstructed from
transcript prose. The implementation branch and PR unit follow ADR-0030: each
track is its own review/merge unit, and a track begins only after its predecessor
is owner-merged to `main`.

## Review gates

### Track 0 gate

The reviewer independently reconstructs the C1–C5 source table from
`analysis/04-economy.md`, compares every populated/approximate/missing field,
and attacks the comparison validator with mismatched workloads, missed seeded
defects, hidden role costs, and incomplete observations. A blocking finding is
any invented value, silently dropped null, mutable-in-place observation,
cost-only verdict, causal label unsupported by evidence class, or economy
verdict emitted when comparability/quality requirements fail.

### Track 1 gate

The reviewer reruns the real browser lifecycle against synthetic temporary
pages and attempts the named failure cases. A blocking finding is any path
where an infrastructure/configuration error becomes a pass, external network
access occurs, candidate content enters the report, cleanup is skipped, or
batch cases do not share exactly one isolated browser process. The reviewer
also reconciles the harness observation against the run: case/session/launch
counts and duration must be measured, while unavailable agent-level costs must
remain null rather than inferred.

### Track 2 gate

The reviewer runs the committed matrix twice, compares the normalized bytes,
checks every criterion's provenance mapping, and injects one controlled failure
per check family. A blocking finding is any hard-coded candidate/port/temp path,
unexercised settled criterion, false pass, cross-case leak, unexplained golden
delta, non-synthetic fixture, or claim that either example is the product
design.

The reviewer then audits the paired-pilot workload and observations: both arms
must receive the same object, criteria, seeded defects, tier/effort, and quality
floor; treatment-specific differences must be declared; all participant,
foreman, harness, recheck, and rework costs must be present or explicitly
unknown; outcome equivalence must be evaluated before cost; and the comparison
must remain labeled a single paired pilot. A blocking finding is any hidden
scope difference, missed seeded defect treated as savings, participant acting
as their own gate reviewer, omitted cost shift, or economy claim generalized
beyond the frozen presentation workload or framed as causal.

### Track 3 gate

The reviewer checks that the observation/compare and harness guidance matches
the executable commands, the append/correction and evidence-strength rules are
usable by a future presentation milestone, the documented subject remains
UI/UX presentation work, the residual reasoned-review boundary remains
explicit, the phase and handoff pointers agree, no maturity cell or ADR status
changed, and the retrospective distinguishes measured improvement, regression,
unknowns, and future UI/UX hypotheses without inventing savings.

## Exit criteria

1. The C1–C5 baseline is machine-readable and source-faithful: every known,
   approximate, and missing value agrees with the economy analysis, and the
   unmeasured foreman cost remains explicitly missing.
2. Strict presentation workload, observation, and comparison versions let a
   future UI/UX milestone declare an iteration/review intervention, append
   measurements, correct by supersession, and reproduce a deterministic
   summary.
3. The economy tool refuses quality-adjusted comparison when work is
   materially different, the quality floor fails, a seeded defect is missed,
   or participating-role cost is unknown for the claimed measure; raw
   observations and independently complete measures remain visible.
4. One documented command executes the complete committed matrix in one
   isolated, reused Chrome process and exits according to the stable contract.
5. The harness contains no candidate-specific path, fixed port, temporary
   location, or duplicated CDP implementation; those vary through strict
   manifest data or shared modules.
6. The committed valid corpus covers both fixtures, both converged example
   shapes, all settled criterion families, and T1/T2/T3 injections.
7. Named invalid/configuration/browser/network cases fail closed and cannot be
   counted as criterion passes.
8. The normalized evaluation report is deterministic and content-free, while
   a separate economy observation truthfully preserves volatile run measures.
9. Browser/profile/target lifecycle tests prove isolation, reuse, and cleanup.
10. A frozen same-workload paired pilot records both manual and
    harness-assisted execution, checks outcome equivalence before cost, accounts
    for shifted work, and labels its single-pair evidential limit.
11. Documentation distinguishes mechanical evidence from information-design
   and aesthetic judgment and gives future reviewers an extension recipe.
12. Documentation gives future presentation milestones a repeatable
    declare → observe → compare → retain procedure and prevents cost-only or
    incomparable claims.
13. Each track passes its focused checks, real-Chrome proof where applicable,
   full verification floor, and independent review.
14. All committed fixtures are synthetic with manufacturing provenance; no real
   workspace, credential, remote URL, or personal output is consulted.
15. The retrospective reports actual execution-cost and outcome observations,
    names unknowns and the next evaluable economy hypotheses, and makes no
    product presentation maturity or unsupported causal claim.

## Tracks

### Track 0 — Economy measurement substrate and historical baseline

**Goal:** make UI/UX iteration economy an accumulative, quality-aware evidence
surface before optimizing the first presentation workload.

**Boundary:** this track covers presentation workloads only. It adds no harness
implementation, general process mandate, agent ranking, global productivity
score, reconstructed missing metric, or claim that historical observations
isolate a causal lever.

**Inputs:** `analysis/04-economy.md`, its cited C1–C5 cycle record, ADR-0013's
scope/economy and tier principles, and the repository's synthetic/data-safety
rules.

**Outputs:** `tools/presentation_economy/` validator/comparison modules;
`tests/test_presentation_economy.py`;
`docs/presentation-economy/README.md`;
`docs/presentation-economy/datasets/presentation-exploratory-baseline.v1.json`;
valid/invalid data fixtures; and the frozen
`docs/presentation-economy/workloads/presentation-review.v1.json`.

**Verification:** source-row reconciliation; strict positive/negative tests;
missing/approximate value checks; append/supersession tests; workload
compatibility and quality-floor mutations; deterministic comparison output; and
the full verification floor.

**Migration risk:** none. This is a new presentation-process dataset. Historical
prose remains the source evidence and is linked rather than rewritten.

**Data safety:** bounded execution metadata and repository-relative provenance
only; no agent content, identity, machine path, or real-data surface.

### Track 1 — Instrumented harness core and fail-closed lifecycle

**Goal:** implement the shared command, strict manifest/report contracts,
loopback server, isolated reusable Chrome lifecycle, CDP client, matrix
executor, deterministic result normalization, and honest economy-observation
emission.

**Boundary:** no standing citation-walk corpus, product surface, external
dependency, screenshot/visual-diff feature, reasoned-review criterion, or
agent-cost inference unavailable to the harness process.

**Inputs:** owner-merged Track 0 data contracts; the six reference harness-seed
scripts; `analysis/04-economy.md`; `analysis/05-technical-findings.md`; Node
standard-library/runtime Web APIs; and an installed Chrome executable.

**Outputs:** `tools/presentation_harness/` core modules, README contract
sections, validator positive/negative examples, focused Node tests, and a
validated `presentation-economy-observation.v1` fragment per run.

**Verification:** strict-validation and lifecycle tests; synthetic temporary
pages exercise batch continuation, reason-code closure, no-network behavior,
timeout/browser-exit error handling, deterministic normalization, and cleanup.
One real-Chrome smoke matrix proves actual CDP behavior before review; its
observation reconciles to the run while unavailable agent measures stay null.

**Migration risk:** none to workspace or tax artifacts. The new command has no
predecessor; the reference seed remains historical evidence and is not edited.

**Data safety:** only temporary constructed pages and repo-relative synthetic
inputs; reports exclude content and machine-local data.

### Track 2 — Standing corpus, batch regression, and paired economy pilot

**Goal:** make the exploratory milestone's settled checks reusable without
fixture re-authoring or reviewer-built apparatus, then generate the first
quality-adjusted treatment comparison.

**Boundary:** preserve both example shapes; do not select a product design,
change presentation meaning, add information-design/aesthetic verdicts, or
generalize a single paired pilot into a causal economy claim.

**Inputs:** accepted Track 1 command; the minimal/rich-reuse fixture
descriptions; both cycle-5 reference prototypes; the criterion/provenance list;
T1/T2/T3 and live-fault cases; and Track 0's frozen comparison workload.

**Outputs:** machine-readable synthetic corpus, two example templates,
manifest-driven full matrix, criterion provenance registry, manufacturing
provenance note, normalized golden report, extension documentation, separately
authorized manual/harness-assisted pilot observations at
`docs/presentation-economy/datasets/presentation-harness-pilot.v1.json`, and a
derived comparison under `docs/presentation-economy/comparisons/`.

**Verification:** required real-Chrome full matrix twice with byte-identical
normalized output; controlled failures per check family; golden diff review;
same-workload/quality-floor pilot validation; cost-shift and evidence-label
checks; focused Python/Node tests; and the full verification floor.

**Migration risk:** reference material is promoted by copy/translation, never
rewritten as though its exploratory history changed. Existing product artifacts
and published schemas are untouched.

**Data safety:** all identifiers remain `demo-*`; manifests contain only
repository-relative paths and no remote origin. Pilot observations contain
only bounded execution metadata and outcomes.

### Track 3 — Operating integration and completion record

**Goal:** make the economy learning loop and harness reusable by later UI/UX
presentation work and close the milestone honestly.

**Boundary:** no universal review mandate, product ADR, information-design role
contract, maturity lift, unmeasured savings claim, or automatic process choice.

**Inputs:** owner-merged Tracks 0–2, their independent reviews, historical and
pilot datasets, actual command timings/result counts, and every recorded
comparison caveat.

**Outputs:** final presentation-economy append/compare guidance,
operator/reviewer harness pointers, phase roadmap and handoff status, and the
milestone retrospective with the next measurable UI/UX economy hypotheses. A
short craft-note promotion occurs only if the owner separately approves its
exact wording; otherwise the toolkit README and milestone record remain the
guidance.

**Verification:** commands and paths in documentation are rerun; records agree
with Git and reviews; baseline/pilot/comparison lineage closes; no ADR/matrix
change appears; full verification floor and records review pass.

**Migration risk:** documentation/pointer changes only.

**Data safety:** completion records contain only synthetic test counts, bounded
execution metadata, and non-descriptive process observations—never agent/page
content, identity, or local machine paths.
