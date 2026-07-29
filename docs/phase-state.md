<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "entry-loop-synthetic",
  "active_plan": "docs/phases/legible-entry/milestones/entry-loop-synthetic.md",
  "status": "Phase Legible Entry, accepted PR #100. Milestone 3, The Entry Loop (synthetic), is OPEN — plan PR #109 merged at 506f785 — TRACK 0 BUILD HAS LANDED at 0ddc0a5 (docs/phases/legible-entry/entry-usability-criteria.md: five loop steps, three criteria each, labelled mechanical or judgement; an ADR-0046 carry-over disposition; a two-agent scoring procedure that preserves disagreement rather than averaging it). ITS REVIEW RETURNED NOT READY at 4d78d27 (docs/reviews/2026-07-28-entry-loop-synthetic-track0-review.md) with eight findings, two blocking: F1 criterion 3.3 is labelled Mechanical but its trigger is 'if the user might reasonably expect them to', which is not mechanically checkable and sits in the fatal scoring class; F2 the cell-pass rule and the disagreement rule do not determine a unique verdict, because a Disputed criterion is a Pass+Fail pair and the text supports both readings. Weakening: F3 the ADR-0046 disposition silently drops Requirement 6 (accessibility) and Foreclosure 2 (no derived value from invalid or blocked input) and half-carries Requirement 4's blast containment; F4 five mechanical criteria are under-specified for agreement; F5 evaluation premises are stated as setup facts rather than unconfirmed dependencies; F6 the evaluator pairing is only exemplified; F7 the build recorded no verification at all; F8 'submission posture' over-reaches a phase where filing is out of scope. THE REPAIR LANDED at 4d8e7cb and ITS FOCUSED RECHECK IS CHARTERED: docs/reviews/charter-2026-07-28-entry-loop-synthetic-track0-repair-review.md. The repair kept 3.3 in the mechanical class and made it observable through a fixed untouched W-2 comparison set (the charter's preferred F1 route), stated the aggregation rule once, carried the accessibility baseline and the derived-from-invalid foreclosure, named the three run dependencies as unconfirmed, fixed the two evaluator briefs, dropped 'submission posture', and recorded verification. THE RECHECK RETURNED NOT READY at 319521c but narrowly: F1-F4 and F6-F8 ALL CLOSED, and implementation independence, scope, and five-step coverage all re-passed with no regression. F5 is the only thing open and it is one paragraph — the document's fail-closed fixture condition (every expected-impact member must change, every untouched-comparison member must stay unchanged) is not among the three named run dependencies, and seeding W-2 as the only missing family does not imply it, so a Track 2 conductor could believe the instrument runnable and only discover mid-evaluation that 3.2 and 4.2 cannot be scored. F5 CLOSED at 1e48443 as a fourth named run dependency, worded identically to the fail-closed passage, with the count moved from three to four and verification recorded. TRACK 0 IS COMPLETE AS WORK. NOTE FOR THE RECORD: its last formal verdict is the NOT READY at 319521c; the F5 close was accepted on inspection rather than by a third review cycle, on the foreman's recommendation, because the check was mechanical. If the owner wants a READY on the record, it needs either a tight recheck or an explicit owner-acceptance note. TRACK 1 IS CHARTERED: docs/reviews/charter-2026-07-29-entry-loop-synthetic-track1.md — the first product build of the phase, in two phases: Phase A confirms the four run dependencies against the code and STOPS AND REPORTS if any fails, Phase B builds the five-step W-2 loop against Track 0's criteria. TRACK 1 BUILD LANDED at 2a00193 — 14 files, ~7,170 insertions: packages/derivation/entry_loop.py, a Svelte EntryPage, a published surface artifact with its own adoption and registry entry, a production-shaped synthetic seed, tools/generate_entry_loop_t1_fixtures.py, and tests/test_entry_loop_t1.py. A loopback runtime admits browser-originated act-contribution.v1 through the existing contribution applicator and act log, then recomputes through live_coordinate_run. PHASE A HELD AND IS CARRIED AS EXECUTABLE REGRESSION: the four run dependencies exist as four named tests rather than as a prose report. Verification recorded with no omissions; 703 passed. ITS REVIEW GATE IS CHARTERED: docs/reviews/charter-2026-07-29-entry-loop-synthetic-track1-review.md. That review does NOT score the usability criteria — Track 2 does that under the fixed two-evaluator procedure, and scoring early would preempt it. The novel boundary worth the review spend is the loopback endpoint that accepts typed input and turns it into a contribution; every prior surface in this project only displayed. The reviewer also records that the earlier likely failure mode, a judgement split over criterion 3.3, is no longer the likely one; fixture construction is. The foreman decided the F2 aggregation rule rather than leaving it to the Builder: evaluators score Pass/Fail only; a split becomes Disputed; a cell passes iff every mechanical criterion is Pass/Pass and no judgement criterion is Fail/Fail; a Disputed mechanical fails the cell; a Disputed judgement escalates to the owner without failing it. This is the first milestone in the phase that builds product and the first that can move a cell. Owner scope decisions: W-2 only across all five loop steps, leaving 15 of 20 cells for later; criteria written BEFORE the surface so the L2 scorer is not shaped by what it scores; the per-field explanation schema emerges from the build and is recorded at close. Four tracks: 0 criteria, 1 build, 2 evaluate, 3 record and close. Track 1 must confirm against the code, before writing any surface, that a synthetic workspace can be seeded so W-2 is the only missing family — the 'know the return is complete' step depends on it. NO MATURITY CELL HAS MOVED IN THIS PHASE. Milestone 1, The Entry Boundary (PR #102, c451a40), accepted ADR-0048: a browser form is acceptable for typing real tax facts on stated conditions, and an entry surface emits act-contribution.v1 through the existing admission path rather than writing facts. It also found that confinement is not total — the vehicle writes a single-instance lock outside the confined tree. Open from it: nothing has searched for the residency locator outside confinement (every run looked for typed tokens only); the singleton lock is a second orphan surface; crash-reporter and GPU-cache paths are narrowed, not closed; the spellcheck flag's mechanism is undesigned. Milestone 2, Packaging the Surface (PR #108, 2fb6761), built the delivery route: surface-artifact.v1 carries opaque UI bytes into Live-Run Data under its own adoption, verified by digest and never read for meaning, reusing ADR-0033's release/registry chain; artifact-package.v4 is untouched and stays that way. ADR-0049 is PROPOSED, NOT RATIFIED — ratification is the owner's. The repository does not store the vendored dependency tree (owner decision, 370f8a6): node_modules is gitignored and rebuilt with npm ci in packages/sample_data/surface_t1/content/app plus tools/generate_surface_t1_fixtures.py; six surface tests skip without it. Carried open from it: the build's output is never digest-verified (trust is verified inputs plus one fixed command; determinism checked byte-identical on one machine under Node v25.8.0, unverified across machines or versions); offline enforcement is macOS sandbox-exec only with no CI coverage; surface_resolver imports three underscore-private names from production_resolver; the sample page uses no TypeScript. tools/build_orientation_block.py defaults to --ref main, a stale Real-Return-era branch — the live trunk is main-ui. Process: a milestone gets one PR to open and one to close; tracks keep their review gate but not their own PR; PRs target main-ui. Phase documentation uses plain, product-facing language; the habit being corrected is writing every planning document as though defending it to a hostile auditor. Prior phase Real Return closed 2026-07-28 with every cell L3 or better, read narrowly — it was breadth- and hardening-limited by construction. Its milestone-by-milestone detail was cut from this file 2026-07-28 and lives in its roadmap, plans, retrospectives, and Git. THE PHASE-BOUNDARY LEGIBILITY AUDIT IS STILL DUE and is owner-spawned — the foreman must not launch it. TOOLING FIXED MID-TRACK at bd7211c: render_context took a literal origin/main default and two of its three callers never resolved the line, so orientation on the surface work refused as if the branch were stale; it now derives the ratified line, and AGENTS.md says --ref HEAD rather than --ref main and notes that a merged PR for a milestone branch is expected mid-milestone because a milestone opens with one PR and closes with another. TRACK 1 REVIEW RETURNED NOT READY at db4c69d: F1 blocking (the build neither closed nor recorded ADR-0048's entry-vehicle spellcheck condition), F2 and F3 weakening (no committed regressions for the endpoint's security-relevant refusals, though the reviewer manually exercised eight classes and all failed closed with redacted responses and no log advance; and the compiled browser client is never driven against the loopback API). Measurement 1 PASSED: the reviewer mutated all four Phase A dependency tests and each failed correctly. THE OWNER WITHDREW ADR-0048's ENTRY-VEHICLE CONDITION on 2026-07-29. ADR-0050 (docs/adr/0050-entry-surface-contract.md, PROPOSED) supersedes ADR-0048 Decision 1 only; Decision 2, the contribution boundary, stands. An entry surface owes contribution-only entry, validated admission that fails closed, redacted failure, data-boundary behaviour, and no false claim of isolation. Browser and workstation behaviour are the owner's trusted environment, where ADR-0047 already puts Class C and Class D. For real entry the trusted environment is standing operational context, not a per-session check: no entry-session affirmation, no spellcheck probe, no owed preflight or launch flag. ADR-0047's viewing-vehicle obligations and ADR-0044's L4 isolation goal are unaffected. CONSEQUENCE FOR TRACK 1: F1 is obsolete. The existing review is NOT rewritten — it was correct under the rule then in force — and the reviewer disposes it on a short recheck that confirms the governing premise changed and that nothing else blocks. The builder repair is now F2 and F3 only, plus one wording check that nothing presents spellcheck=\"false\" as a security control. Milestone open question 3 (does the viewing preflight cover an entry session) is CLOSED by ADR-0050; the milestone plan and the ADR index are amended to match. TRACK 1 REPAIR LANDED at 2e62c4a — tests only, 272 insertions, no product code: seven fail-closed regressions for the endpoint classes the prior reviewer had only observed by hand, and a real-Chrome test (tests/helpers/entry_loop_browser_client.mjs, driven through the presentation harness) that runs the compiled Svelte client against the live loopback API. 711 tests, verification recorded with no omissions. ITS REVIEW GATE IS CHARTERED: docs/reviews/charter-2026-07-29-entry-loop-synthetic-track1-repair-review.md — the verdict is for TRACK 1 AS A WHOLE, since this is the gate that lets Track 2 evaluate against this surface. Two things worth the review spend: the seven refusal tests were written against behaviour that already passed, which is exactly when a test can assert nothing and stay green; and the browser test is guarded by skipUnless on Node, a local Chrome, and the vendored tree, so whether F3 is closed or merely written depends on whether it actually runs. TRACK 0's RECORD GAP IS CLOSED BY OWNER ACCEPTANCE, 2026-07-29: docs/reviews/2026-07-29-entry-loop-synthetic-track0-owner-acceptance.md. The owner read the F5 change and accepted docs/phases/legible-entry/entry-usability-criteria.md at 1e48443 as the instrument Track 2 scores against, before Track 2 ran and therefore without knowledge of what it scored. This is owner acceptance, not a review verdict; the NOT READY at 319521c stands as the last formal verdict and is not converted into anything else.",
  "current_role": "Reviewer — The Entry Loop (synthetic), Track 1 repair review",
  "current_prompt": "docs/reviews/charter-2026-07-29-entry-loop-synthetic-track1-repair-review.md"
}
-->
# Phase State

This is the **single re-entry document.** It carries the machine-readable
`foreman-context-v1` block above, a **product briefing** in ordinary language,
the current operational state, and durable pointers. It describes *now*: durable
history lives in milestone retrospectives, review records, ADRs, and Git, and
this file links there rather than retelling it.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
.venv/bin/python3 tools/foreman_context.py --ref HEAD --format markdown
```

Reconcile its source commit and worktree report with Git, then read the
action-specific sources it names. If it refuses, inspect those committed sources
directly and resolve the disagreement before acting. The capsule reports state;
it does not change the data boundary or replace accepted authority.

## Product briefing (as of 2026-07-26, after Presentation L2 grounding)

**What it does now.** Attestory computes its user's **actual return slice**: the owner's real W-2, 1099-INT, and 1099-DIV facts, held in a quarantined out-of-repo workspace, flow through a contribution boundary (contribution is a first-class product event, distinct from a run; runs consume facts, structurally), resolve a byte-verified production package (a current user adoption pins a verified release; only the strict `validation.ok == True` exclusive member graph executes), and produce Form 1040 lines **1a, 2b, 3a, 3b, 9, 11, 12, 15, and 16** with full explanations, plus Schedule B (Parts I/II payer itemizations tying to 2b/3b, Part III via two contributed taxpayer-assertion facts) when the $1,500 conditional requires it — publishing, or blocking honestly with a walkable account of what is missing. Line 16 is the QDCG worksheet over contributed declared-absence facts, with a bidirectional interlock against the capital-gain-distribution signal. Taxable interest (2b) remains an OID-inclusive declared coextensive composition; the 1099-DIV declared universe is boxes 1a/1b only (2a/3/5/7/12 are named honest-block exclusions); standard deduction and tax remain declared rule artifacts over a first-class filing-status domain. Every source family — including both dividend box families — closes over a **horizon-keyed declared set**, so a stale closure is a hard projection error, never a quietly wrong line. The repository provably carries zero personal data: out-of-repo residency by ratified rule (ADR-0031), a fail-closed classifier, per-review safety scans, and installed byte-verified commit/push envelope gates in every clone. The only repo-side fact about any real run is a three-fact non-descriptive attestation (Ontology §8). A correction to an already-answered fact is no longer necessarily unrestricted: a fact type may declare `locked` (never correctable again) or `closed-on-attestation` (correctable until a named closure fact attests true), enforced at the existing supersession-policy dispatch (ADR-0041); every fact type shipped today still declares `free`, unaffected, by choice.

**Shims in place.** E8.1 UI coverage partially met — a citation-walk renderer exists, satisfies ADR-0046 end to end, and as of 2026-07-27 has been exercised in a real viewing session against the owner's real residency, carrying Presentation to **L3 across all five columns** — the W-2 wages (1a) cell on that session's attestation (matrix footnote 14), the other four on a 2026-07-28 amendment naming the columns the owner observed in that same single session (footnote 15). No other form or schedule has a human surface. Mechanical separation between Developer/Supply and Live-Run Data **not implemented**, which holds the data-boundary row at L3; guarded publication transport / credential confinement also not implemented, as a separate publication-integrity deferral; a synthetic push-envelope posture audit makes the hook/`--no-verify` bypass visible but does not protect an owner push; ADR-0026's further interest sources and subtractive adjustments deferred; ADR-0028 historical-v1 migration deferred; the declared dividend universe excludes boxes 2a/3/5/7/12; Schedule B is the only implemented schedule attachment; `closed-on-attestation` reaches only fact types keyed identically to their gate fact type, not yet differently-keyed per-item facts. The complete named list with reactivation triggers: `docs/phases/real-return/milestones/correction-authority-and-marshaller-simplification-deferral-ledger.md` (which also dispositions the Dividends and Schedule B Slice ledger's entries this milestone touched — two, both retired).

**What the completed milestones establish.** Live-Run System Definition and Trust Domains accepts ADR-0044 as the project's bounded security position: Developer/Supply, Publication, Live-Run Data, and Owner Authorization are separate logical authority domains; the intended live supply crossing is the current owner-adopted, byte-verified package; and guarded transport belongs to publication integrity rather than the live-data privacy wall. It implements no isolation mechanism, schedules none, and leaves the data-boundary row at L3. The Presentation Exploratory Milestone then demonstrated an agent-authored, agent-reviewed UI-development loop on a synthetic citation walk: roughly 65–80% of the exercised quality surface was mechanically checkable, while information-design judgment remained distinct and under-served. Presentation Evaluation Process Economy added the Track 0 declare → observe → compare → retain foundation: strict presentation workload/observation/comparison contracts, a source-faithful historical baseline, participating-role completeness, and quality-before-cost enforcement; its proposed general browser harness failed independent review and was not merged. Browser Evaluation Runner Completion then finished that same runner as trustworthy tooling: it adopted the preserved implementation commit rather than rebuilding it, repaired the review's six blocking correctness classes plus two owner-accepted post-verdict residuals (R1/R2), and completed the transferred lifecycle/output measurements, under one focused delta review and one focused recheck. It added no product UI, ADR, or maturity lift; it removes the "runner not trustworthy" blocker on starting presentation work. Presentation — Citation Walk on Real Derivation Output then spent that unblocked capacity: it ratified ADR-0046 (Presentation Surface Contract) straight from the exploratory milestone's existing five-cycle evidence rather than re-deriving it, and shipped the first conforming human surface. Its lasting result is the contract, not the page — zero-authority foreclosure (nothing renders without a source citation), blanket redaction of rejected values, section-level blocked-state salience — and the demonstration that an independent review gate catches contract violations the builder's own 23-criterion manifest passed clean (F1, F2). It lifts Presentation to L2. A later boundary inspection corrected its proposed next bar before that proposal merged as a new plan.

**What just completed.** Presentation — L2 Integration Grounding corrected the
prior closeout's unsupported conclusion that a real exercise
required no further building. Before this milestone, renderer integration
started from a hand-shaped model, the coordinator discarded the publications
and resolved graph needed to construct it, and the browser harness was
intentionally synthetic-only. Track 1 closed the coordinator-to-model gap on a
production-shaped synthetic run. Its first Builder correctly stopped before
writing code because the existing demo manifest requires line 2a and
guard-inapplicable line 9 states absent from the resolved production package.
The amended charter preserves that manifest as the full renderer regression
floor and adds a dedicated manifest for the coordinator-generated golden.
That build landed as `81c5504` on the milestone branch. Independent review
`e36086a` returned `NOT READY` on one coordinator-level projector-failure path.
The plan's single repair landed as `759c9fa`; focused recheck `4a74ffd` returned
`READY`. Track 2 records the resulting six-row capability state in the maturity
matrix, and completion review `7f6ae79` returned `READY`. PR #86 merged as
`1f3bb9a` with CI `verify` green. Presentation remains L2: no live browser
invocation vehicle exists and no real operation occurred. The next milestone
is unselected.

**Nature of the pending schema/contract change.** None pending. `fact-type.v3` and `bundle.v3` are published; any further correction-authority extension is separately chartered. ADR-0044 is accepted positioning, not a mechanism decision: any authority-separation implementation requires a later owner-selected milestone, mechanical proof, and real-run verification before an L4 claim.

## Current state (2026-07-28)

**Phase: Legible Entry.** Accepted 2026-07-28 in PR #100. The phase is about
getting the owner from a pile of tax documents to a computed return without
opening a text editor. Roadmap:
`docs/phases/legible-entry/legible-entry-roadmap.md`.

- **Milestone 1, The Entry Boundary — closed 2026-07-28.** PR #102 merged at
  `c451a40`; **ADR-0048 accepted**. A browser form is acceptable for typing real
  tax facts on stated conditions, and an entry surface emits
  `act-contribution.v1` through the existing admission path rather than writing
  facts directly. No product code changed and no maturity cell moved — it was a
  decision, and the instrument measures capability.

  What it means for building the entry surface: the form runs inside the
  confined vehicle rather than a browser someone opens themselves; entry hands a
  contribution to the existing boundary; the spellcheck network path must be
  closed by an explicit flag. It says nothing about what the form asks or how a
  field explains itself — that design is entirely still ahead.

  It also established that **confinement is not total**: the vehicle writes a
  single-instance lock outside the confined tree, surviving a crash, holding no
  typed content. That was believed total before this milestone.

  Retrospective: `docs/milestone-retrospectives/2026-07-28-entry-boundary.md`.

- **Open, and carried in ADR-0048 rather than fixed.** Most consequential:
  **nothing has searched for the residency locator outside confinement** — every
  run looked for typed tokens only, and the locator is protected in its own
  right. Also: the singleton lock is a second orphan surface sitting outside the
  residency with nothing sweeping it; crash-reporter and GPU-cache paths are
  narrowed but not closed; the spellcheck flag's mechanism is undesigned.

- **Milestone 2, Packaging the Surface — closed 2026-07-28.** PR #108 merged at
  `2fb6761`. UI code now has a sanctioned route into the live workspace: a
  **second, separate artifact** (`surface-artifact.v1`) with its own adoption,
  carrying program bytes verified by digest and never read for meaning. It hangs
  off the same release and registry verification the rule package already uses,
  and **`artifact-package.v4` is untouched** — the package's promise that
  everything in it validates stays true without a footnote. One trivial Svelte
  page ships through it, builds at the workspace with the network off, and opens
  in the live-viewing vehicle on a synthetic workspace. No maturity cell moved:
  this is the delivery route, not the loop.

  **ADR-0049 is proposed, not ratified.** Ratification is the owner's.

  The plan for this milestone shipped a false premise — it said the UI would
  ship as members of the adopted package, which is impossible, and that survived
  a plan PR and an owner decision built on it. Caught only because chartering
  forced someone to open the schema. Retrospective:
  `docs/milestone-retrospectives/2026-07-28-packaging-the-surface.md`.

- **The repository does not store the vendored dependency tree** (owner
  decision 2026-07-28, landed after the close as `370f8a6`). `node_modules/` is
  gitignored. It ships inside the artifact; it is checked into nothing. Rebuild
  it before running the surface tests:

  ```sh
  (cd packages/sample_data/surface_t1/content/app && npm ci)
  python3 tools/generate_surface_t1_fixtures.py
  ```

  Six tests skip without it, so the digest and refusal evidence is reproducible
  on demand rather than continuously checked. The data-safety test is
  deliberately unguarded and runs everywhere.

- **Open from milestone 2, carried not fixed.** The build's **output is the one
  thing in the chain no digest covers** — trust is verified inputs plus one fixed
  command. Determinism was checked byte-identical on one machine under Node
  v25.8.0 and is unverified across machines or Node versions; that is the same
  gap as the Node precondition seen from the other side. Offline enforcement is
  proved only under macOS `sandbox-exec`, with no CI coverage, because the tests
  need Node and Chrome present. `surface_resolver.py` reuses three
  underscore-private names from `production_resolver.py` — real reuse, fragile
  coupling. The sample page uses no TypeScript, so that toolchain cost is
  untested and will appear later.

- **Milestone 3, The Entry Loop (synthetic) — open.** Plan PR #109 merged at
  `506f785`. Plan:
  `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`. This is the
  first milestone in the phase that builds product, and the first that can move
  a cell.

  Scope, settled by the owner: **W-2 only, all five loop steps.** The usability
  criteria are written in Track 0 **before** the surface is built, so the thing
  scoring the L2 claim was not shaped by the thing it scores. The per-field
  explanation schema is left to emerge from the build and recorded at close.
  Four tracks: criteria, build, evaluate, record and close.

  One premise Track 1 must check against the code before writing anything: that
  a synthetic workspace can be seeded so W-2 is the only missing family. The
  "know the return is complete" step depends on it.

  **Track 0 is chartered** —
  `docs/reviews/charter-2026-07-28-entry-loop-synthetic-track0.md`. A Builder
  writes the entry usability criteria and the procedure that scores a cell
  against them, with no product code. Its stop conditions are worth knowing
  about: if the criteria cannot be written without seeing an implementation, or
  if the phase's evaluation method cannot produce a defensible L2 verdict, that
  is a finding and the track reports it rather than writing around it.

- **`tools/build_orientation_block.py` defaults to `--ref main`,** which is a
  stale Real-Return-era branch in this repository. The live trunk is `main-ui`;
  pass it explicitly.

- **Filing is out of scope** for this phase (settled 2026-07-28). The phase ends
  at a complete, computed return.

- **Process changes, now in force.** A milestone gets one PR to open
  it and one to close it; tracks keep their review gate but no longer get their
  own PR. Phase documentation uses plain, product-facing language.

- **The phase-boundary legibility audit is still due.** It is owner-spawned by
  design; the foreman must not launch it.

- **The Real Return phase is closed** (owner decision, 2026-07-28). Its standing
  test is met and every cell of its maturity matrix is L3 or better. Read that
  narrowly: it was breadth- and hardening-limited by construction, and the owner
  still enters facts by hand-editing JSON. Legible Entry replaces the Real
  Return maturity matrix rather than extending it. Phase-close record:
  `docs/phases/real-return/real-return-roadmap.md`, "Phase close — 2026-07-28".

### Prior phase detail (Real Return)

Cut 2026-07-28. Real Return's milestone-by-milestone history lived here and now
lives where it belongs: `docs/phases/real-return/real-return-roadmap.md`, the
milestone plans under `docs/phases/real-return/milestones/`, the retrospectives
under `docs/milestone-retrospectives/`, the review records under
`docs/reviews/`, and Git. What still bears on work ahead is kept below rather
than retold here.

- **Data boundary:** all committed evidence remains synthetic. Do not access or
  record a real workspace, credential, remote, output, or location. The
  owner-held live-run helpers remain untracked.

## Pointers

Active phase: **Legible Entry** — `docs/phases/legible-entry/`. Roadmap and
current prompt: `docs/phases/legible-entry/legible-entry-roadmap.md`. Milestone
selection in this phase follows the proposed sequence in that roadmap; the
instrument is the entry-loop matrix described there, which replaces Real
Return's rather than extending it.

Prior phase: **Real Return** — closed 2026-07-28,
`docs/phases/real-return/real-return-roadmap.md` ("Phase close — 2026-07-28").
Foundation before it: `docs/phases/foundation/foundation-roadmap.md`. Their
milestone-by-milestone history lives in those roadmaps, the milestone plans, the
retrospectives under `docs/milestone-retrospectives/`, and Git — the detail
below is kept only where it bears on work still ahead.

Completed in this phase:

- **The Entry Boundary** — closed 2026-07-28, PR #102 at `c451a40`. ADR-0048
  accepted. Plan:
  `docs/phases/legible-entry/milestones/entry-boundary.md`; retrospective:
  `docs/milestone-retrospectives/2026-07-28-entry-boundary.md`.
- **Packaging the Surface** — closed 2026-07-28, PR #108 at `2fb6761`. ADR-0049
  proposed. Plan:
  `docs/phases/legible-entry/milestones/packaging-the-surface.md`; retrospective:
  `docs/milestone-retrospectives/2026-07-28-packaging-the-surface.md`; charters
  `docs/reviews/charter-2026-07-28-packaging-the-surface-track{1,2}.md` and
  reviews `docs/reviews/2026-07-28-packaging-the-surface-track{1,2}-review.md`,
  both READY.

**➡️ Next action: run Track 0** — Builder, entry usability criteria,
`docs/reviews/charter-2026-07-28-entry-loop-synthetic-track0.md`, on branch
`milestone/entry-loop-synthetic`.

Two things are outstanding and are the owner's, not the foreman's: **ADR-0049 is
proposed and awaits ratification**, and the **phase-boundary legibility audit is
due** and is owner-spawned by design.

The Real Return milestone-by-milestone chain that used to be listed here is
retained in "Prior phase detail (Real Return)" above, in each milestone's plan
and retrospective, and in Git. Two of its items are still open and follow into
this phase: the **classified-refusal path has never been confirmed by a human**
(the oldest open item on this path; it needs a session to close), and the
**session runbook has an unidentified unclarity** — whoever uses it next should
note where it reads badly at the moment it reads badly.

The four owner constraints from that milestone remain in force as a standing
posture, and all four are the same constraint from different sides: **this
repository does not author its own boundary enforcement.** No confinement code —
the `sandbox-exec` profile is owner-held outside the supply chain. No probes —
`PreflightProbes` stays an injected input defaulting to `UNKNOWN`; nothing here
reads backup state, indexing state, or the process table. No locator in any
surface: server logs, request paths, subprocess arguments, diagnostics, test
names. And `sandbox-exec`'s deprecation is a named, owner-accepted residual, not
a blocker.

Both `track/presentation-citation-walk-track1` and
`track/browser-evaluation-runner-completion` may be deleted; their content is
fully contained in `main` at `2d4c195` and `c329afd` respectively.

Standing operational notes: `PROJECT_PLANNING.md` ("Branch, PR, and Merge Protocol") governs per-track PRs, owner merges, and `main` as the continuous ratified record; `AGENTS.md` ("Dispatch authorization") governs dispatch; the owner-held run tooling (`tools/scaffold_live_acts.py`, `workspace-seed/`) is intentionally untracked; every fresh clone runs `tools/install_envelope_hooks.py` once (the suite enforces it). The GitHub remote stays **private** (standalone owner decision to change).

Durable history — Foundation's record lives in `docs/phases/foundation/foundation-roadmap.md`; the First Real Return Slice's track-by-track history lives in its milestone plan, retrospective, and git history. The Dividends and Schedule B Slice's track-by-track history (D1/D2/D3 ratification, Tracks 0/0a/1–4, reviews, repairs, the real run) lives in its milestone plan, its retrospective, the review records under `docs/reviews/`, and git history — no longer restated here.

## Durable pointers

- Foreman posture and verification floor: `docs/roles/foreman.md`.
- Operating rules: `AGENTS.md` and `PROJECT_PLANNING.md`. Process is not in the
  ADR corpus (ADR-0045); `docs/adr/INDEX.md` routes product contracts only.
- Accepted decisions bearing on the work ahead:
  `docs/adr/0044-live-run-system-boundary-and-trust-domains.md` (trust domains),
  `docs/adr/0046-presentation-surface-contract.md` (the display-side surface
  contract, and the nearest prior art for entry criteria),
  `docs/adr/0048-entry-boundary.md` (entry emits contributions),
  `docs/adr/0049-surface-artifact.md` (proposed; how UI code arrives).
- Agent-driven UI method, and the evaluation-analysis documents behind it:
  `docs/prototypes/human-presentation-citation-walk/plan.md` and its
  `analysis/` directory.
- Completed-milestone lessons: `docs/milestone-retrospectives/`.
- Charters and review records: `docs/reviews/`, named by date and track. The
  per-charter list that used to be enumerated here was cut 2026-07-28; the
  directory is the index.
