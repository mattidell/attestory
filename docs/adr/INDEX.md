# ADR Index

Audience: Agents (always-load routing surface). This file is the normative
home for its own routing rules; ADR-0039, which created it, is retired to
history (ADR-0045).

**Advisory:** this index routes reading; it is not authority. All *accepted*
ADRs bind whether or not a charter lists them; on any conflict between a
digest here and the ADR's text, the text governs. Digests condense the
Decision, not the Context. Statuses `rejected` / `superseded` / `proposed` /
`retired` are **inert** — never load as authority.

**ADRs are product and contract decisions only (ADR-0045).** Process — seats,
the milestone loop, dispatch, chartering, review cadence, branch and merge
mechanics, context routing — is not recorded here. Its operative homes are
`AGENTS.md`, `PROJECT_PLANNING.md`, and `docs/roles/`, and it changes by owner
direction without an ADR. `retired` marks the seven former process ADRs: kept
as rationale, never cited as authority.

**Role cores** — each seat boots from its seed file in `docs/roles/`, which
carries posture and points here for the binding ADRs:
- **Foreman** (`docs/roles/foreman.md`) — no product-ADR core; its operating
  rules are `AGENTS.md`, `PROJECT_PLANNING.md`, and its seat file
  (+ `docs/phase-state.md`, the active plan).
- **Builder** (`docs/roles/builder.md`) / **Reviewer**
  (`docs/roles/reviewer.md`) — core ADRs 0003, 0010 (+ the dispatching
  charter, which carries the milestone foreclosure principles).
- **Advisor** (`docs/roles/advisor.md`) — owner-launched counsel; the only
  seat that reads `docs/governance/`.

There is no clerk seat (ADR-0045).

| ADR | Status | Tags | Binding digest |
| --- | --- | --- | --- |
| 0001 | accepted | governance | The governance set v0.1 is the project's contract authority. |
| 0002 | accepted | kernel | The authoritative store is an append-only JSONL act log. |
| 0003 | accepted | kernel, schema | Every citizen is a JSON Schema document; IDs are opaque strings; no noun without a schema. |
| 0004 | rejected | — | Inert. |
| 0005 | retired | — | Inert (see 0045); prototype-evidence rules now live in `PROJECT_PLANNING.md`. |
| 0006 | accepted | rules | The rule-artifact language: declared rules with expression trees; no computation outside declared content. |
| 0007 | accepted | kernel, rules | Derived publications are their own act kind, pinned to runtime source. |
| 0008 | accepted | kernel | Derivation records are written at derivation time, alongside the act. |
| 0009 | accepted | facts | Derived-finding shape; authority lives in the attribution chain, never in the payload. |
| 0010 | accepted | facts, currency | Derived findings project into currency; a superseded pinned input displaces its consumers to non-current. |
| 0011 | accepted | facts, closure | Tax fact identity keys and source-set closure: zero is never assumed, only declared. |
| 0012 | accepted | presentation | Form fields are citizens; rendered dispositions are atomic (one disposition kind per state, no state-in-value). |
| 0013 | retired | — | Inert (see 0045); economic gates now live in `PROJECT_PLANNING.md`. |
| 0014 | accepted | closure | Source-closure mappings are adopted, immutable content. |
| 0015 | accepted | facts, composition | Statement-instance identity (1099-INT pattern): payer + tax year + payer_ref; the template every statement family instantiates. |
| 0016 | accepted | closure, composition | Family claim and composition: a subtotal authorizes only its claim; per-box closure independence. |
| 0017 | accepted | closure | Family horizons are recorded entities; a closure naming a stale horizon is a hard projection error. |
| 0018 | superseded | — | Inert (see 0029). |
| 0019 | rejected | — | Inert (see 0024). |
| 0020 | accepted | explanation | Non-publication explanation walking: every block is a walkable ledger entry. |
| 0021 | proposed | — | Inert (see 0026). |
| 0022 | superseded | — | Inert (see 0027). |
| 0023 | accepted | facts | Member assertion vs. member transition boundaries; how facts enter and leave family membership. |
| 0024 | accepted | rules | Conditional structures in the rule language (guards; `guard_result`/inapplicable dispositions). |
| 0025 | accepted | rules | Expression extensions: declared optional defaults and categorical comparison. |
| 0026 | accepted | composition | Line 2b: declared coextensive interest composition; named deferrals (K-1, market discount, subtractive adjustments). |
| 0027 | accepted | packages | Adopted-content manifests: package membership closure; exclusive execution projection; co-located content is inert. |
| 0028 | accepted | packages | Package fact-surface membership and the composition-obligation trigger. |
| 0029 | accepted | explanation | Citation resolution contract; semantic pins. |
| 0030 | retired | — | Inert (see 0045); branch/PR/merge protocol now lives in `PROJECT_PLANNING.md`. |
| 0031 | accepted | boundary | Real data lives out-of-repo by rule; fail-closed classifier; envelope gates; nothing personal ever crosses. |
| 0032 | accepted | boundary | Contribution is a first-class event distinct from a run; runs consume facts, never inputs; batches fail closed. |
| 0033 | accepted | packages | Production package resolver: user adoption pins a verified release; bytes verified before a strict exclusive graph resolves. |
| 0034 | superseded | — | Inert (see 0043). |
| 0035 | accepted | composition | 1099-DIV: two per-box families (1a→3b, 1b→3a); `dividend-universe.v1`; recorded-non-composable boxes; admission-locus 1b ≤ 1a rejection; `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal. |
| 0036 | accepted | attachments | Attachment citizen: three atomic states; declared requirement conditional; `collect_members` rows + `ITEMIZATION_TIE_OUT_VIOLATION`; presence-semantics categorical Part III; generic across schedules. |
| 0037 | accepted | rules, explanation | `conditional_dependency_set`: one walk names every absent member of a conditional dependency set (rule-artifact.v3 only). |
| 0038 | accepted | worksheet | Line 16: QDCG worksheet as declared v3 successor rule; capital-gain inputs bound to declared-absence facts; bidirectional admission-locus contradiction interlock; qualified-zero reduction grounded in the dependency-set contract. |
| 0039 | retired | — | Inert (see 0045); this index norms its own routing rules. |
| 0040 | retired | — | Inert (see 0045); the advisor seat is normed by `docs/roles/advisor.md`. |
| 0041 | accepted | facts, closure | Closes `supersession.policy` to `free`/`locked`/`closed-on-attestation`; state-gated only, no actor/identity concept. |
| 0042 | retired | — | Inert (see 0045); capsule routing now lives in `PROJECT_PLANNING.md`. |
| 0043 | retired | — | Inert (see 0045); dispatch is normed by `AGENTS.md`. |
| 0044 | accepted | boundary, security | Defines Developer/Supply, Publication, Live-Run Data, and Owner Authorization as distinct trust domains; guarded transport is publication integrity, while L4 awaits later mechanical separation and verification. |
| 0045 | accepted | process | The last process ADR. `AGENTS.md` is a router; every rule has exactly one normative home. Dispatch requires the owner's literal string `I authorize dispatch`, single-use and charter-bound. Clerk seat retired. Governance reading moves off executing seats to CI plus the advisor. Process leaves the ADR corpus; 0005/0013/0030/0039/0040/0042/0043 retired. |
| 0046 | accepted | presentation | Presentation Surface Contract: zero-authority projection, honest blocking, fail-loud, sub-section blast containment, structural citation identity, accessibility baseline; derived/diagnostic values are zero-authority; blanket redact on rejected values; blocked-state salience is section-level. Ratifies the Presentation Exploratory Milestone's five-cycle convergence; no matrix-cell claim by itself. |
| 0047 | accepted | boundary, presentation, security | Live viewing environment: a viewing session is an activity within Live-Run Data with a human consumer, not a new domain. Total four-class channel classification (A named residual / B controlled by construction / C not closeable by the vehicle, no substrate selected or evaluated / D workstation precondition). Residency backup, content indexing, and detectable clipboard-history retention are refusals, not warnings. Enumerates the five conditions under which the ADR-0031 attestation is honest. Diagnostics emit reason codes, never locators. Selects no enforcement substrate; lifts no maturity row. **Amended 2026-07-27:** records a first-principles Seatbelt (`sandbox-exec`) evaluation — inherited kernel-enforced network denial works if the top-level process is confined; escape is unavailable to unprivileged code; the interface is deprecated and SBPL drifts across releases — and places both Class C confinement and Class D precondition observation in the owner's trust domain, outside the project supply chain, so the constrained supply chain does not author its own boundary. `PreflightProbes` stays an injected input. Class C stays open, no row moves, and the data-boundary L3 ceiling is accepted as permanent. |
| 0048 | accepted, Decision 1 superseded by 0051 | boundary, presentation | Entry Boundary: a browser form is acceptable for typing real tax facts, resting on `live_viewing.py`'s confinement (every one of the four destinations it computes is checked inside the residency before any write — not a claim that these are the only destinations Chrome uses) and disposal-on-close (a single mechanism covering those four destinations at once), not on the retention probe's per-channel negatives, which were untested preconditions (an unaccepted save prompt, opt-in spellcheck) dressed as tested ones. Conditioned on affirmatively closing the spellcheck network path rather than relying on its observed-off default. A repair (Track 2) widened the filesystem search outside the confined tree and found a real, verified exception — Chrome's own single-instance-lock socket and authentication token, holding no typed content — refuting "confinement is already total" as a fact while supporting "no typed content escaped"; the crash-reporter-database question remains open. A crash-orphaned profile is untidy, not an escape, for the destinations actually confined, and only for as long as ADR-0047's backup/indexing preconditions hold over however long the orphan survives. An entry surface's only write authority is emitting `act-contribution.v1` through the existing admission path (ADR-0032); no direct fact write, no new actor/origin field. Ratified 2026-07-28 (PR #102). |
| 0049 | accepted | boundary, packages | Surface Artifact: UI program bytes cross into the live workspace through a second, separate adopted artifact (`surface-adoption` kind, reusing `act-package-adoption.v1`'s payload unchanged), never as members of `artifact-package.v4` — a member is a typed citizen whose whole graph hard-validates, and a raw file has no such validation to give. Reuses ADR-0033 Decisions 1–2 (release-rooted adoption; release verified before registry) unchanged; diverges only at member resolution, where a manifest's flat `entries` are checked one file at a time by SHA-256, never parsed. Every input is digest-verified (941 entries, 5.07 MB vendored); the build's output is not, because it did not exist until the workspace produced it — the chain is provenance (verified inputs, a verified command) not content identity, and that is not sufficient to claim the served bytes equal any previously reviewed bytes, since nothing publishes a digest for the output. The same-machine half of the underlying determinism assumption is **checked, not assumed**: two runs of the fixed command over identical inputs produce byte-identical `dist/` trees (Node v25.8.0, one machine), ruling out embedded timestamps, randomized ordering, and per-run identifiers — while saying nothing across machines, Node versions, or platforms. That cross-environment byte-identity check, re-run on toolchain upgrade, is the named remaining future work. Names Node as a new "build-toolchain precondition" category, deliberately not filed under ADR-0047 Class D (a total classification of session-leakage channels, not build-time functional requirements); the Node-version risk is exactly the half the same-machine check could not cover, so it and the residual build-output gap close together or not at all. Ratified 2026-07-29 (PR #112). |
| 0050 | accepted | composition, worksheet | Direct Form 1040 line-7a capital-gain distributions use four Exception-1 components and a checked Schedule-D conclusion; a successor box-2a family; line 7a/7b; line 9 once, with guard-inapplicable line 7a blocking line 9 and taxable income through line 9; and a line-16 QDCG partition (Q>0 or L>0) with branch-specific declaration pins and the exact line-7b citation, without mutating ADR-0035/0038 history. |
| 0051 | accepted | boundary, presentation | Entry Surface Contract: supersedes ADR-0048's entry-vehicle requirements (Decision 1 and the affirmative spellcheck condition); ADR-0048's contribution boundary (Decision 2) stands unchanged. An entry surface is responsible for contribution-only entry, validated admission that fails closed, redacted failure, data-boundary behaviour, and making no false claim of isolation. Browser and workstation behaviour are outside the entry surface's contract — the product makes no claim to isolate typed data from the owner's browser, OS, extensions, or local processes, which is where ADR-0047 already puts Class C and Class D. For real entry the trusted environment is standing operational context, not a per-session check: no entry-session affirmation, no spellcheck probe, no owed preflight. ADR-0047's viewing-vehicle obligations (orphan sweep, single-instance-lock artifact) and ADR-0044's longer-term L4 isolation goal are unaffected. No maturity cell moves. Ratified 2026-07-29 (PR #112). |
| 0052 | proposed | composition, worksheet, attachments | Covered Long-Term Gains, Schedule D Line 8a (**not ratified**): independent anchor-keyed transaction family one level below the statement pattern; nine-part completeness boundary read directly with no synthesizing conclusion, box-2a closed (not closed-empty) adopted successor; Schedule D line 8a/13/15/16 as an ADR-0036 content instantiation (categorical attachment-requirement schema gap named, not resolved); a shared `selected-preferential-base` symbol with an exact per-producer pin contract superseding named ADR-0050 Decision 5/7 clauses for the versioned graph only; exactly-one-producer mechanical enforcement named, not resolved. |

