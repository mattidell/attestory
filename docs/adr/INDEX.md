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
