# ADR Index

Audience: Agents (always-load routing surface); governed by ADR-0039.

**Advisory:** this index routes reading; it is not authority. All *accepted*
ADRs bind whether or not a charter lists them; on any conflict between a
digest here and the ADR's text, the text governs. Digests condense the
Decision, not the Context. Statuses `rejected` / `superseded` / `proposed`
are **inert** — never load as authority (ADR-0013 amendment).

**Role cores** — always read, regardless of task:
- **Foreman core:** 0005, 0013, 0030, 0034 (+ `docs/phase-state.md`,
  `docs/foreman-handoff.md`, the active milestone plan).
- **Builder/reviewer core:** 0003, 0010 (+ the dispatching charter, which
  carries the milestone foreclosure principles).

| ADR | Status | Tags | Binding digest |
| --- | --- | --- | --- |
| 0001 | accepted | governance | The governance set v0.1 is the project's contract authority. |
| 0002 | accepted | kernel | The authoritative store is an append-only JSONL act log. |
| 0003 | accepted | kernel, schema | Every citizen is a JSON Schema document; IDs are opaque strings; no noun without a schema. |
| 0004 | rejected | — | Inert. |
| 0005 | accepted | process | Consequential (Tier 2/3) decisions require prototype evidence. |
| 0006 | accepted | rules | The rule-artifact language: declared rules with expression trees; no computation outside declared content. |
| 0007 | accepted | kernel, rules | Derived publications are their own act kind, pinned to runtime source. |
| 0008 | accepted | kernel | Derivation records are written at derivation time, alongside the act. |
| 0009 | accepted | facts | Derived-finding shape; authority lives in the attribution chain, never in the payload. |
| 0010 | accepted | facts, currency | Derived findings project into currency; a superseded pinned input displaces its consumers to non-current. |
| 0011 | accepted | facts, closure | Tax fact identity keys and source-set closure: zero is never assumed, only declared. |
| 0012 | accepted | presentation | Form fields are citizens; rendered dispositions are atomic (one disposition kind per state, no state-in-value). |
| 0013 | accepted | process | Prototype economic gates 0–8; owner-approved topic plan before first charter; rival evidence every round; foreman-authored fixes need a confirmation pass; non-accepted ADRs are inert. |
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
| 0030 | accepted | process | Merge unit = review unit: per-ADR and per-track no-ff PRs to a continuous `main`; owner merges. |
| 0031 | accepted | boundary | Real data lives out-of-repo by rule; fail-closed classifier; envelope gates; nothing personal ever crosses. |
| 0032 | accepted | boundary | Contribution is a first-class event distinct from a run; runs consume facts, never inputs; batches fail closed. |
| 0033 | accepted | packages | Production package resolver: user adoption pins a verified release; bytes verified before a strict exclusive graph resolves. |
| 0034 | accepted | process | Every foreman sub-agent dispatch requires explicit owner approval (reviewer seats pre-authorized by plan approval). |
| 0035 | accepted | composition | 1099-DIV: two per-box families (1a→3b, 1b→3a); `dividend-universe.v1`; recorded-non-composable boxes; admission-locus 1b ≤ 1a rejection; `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal. |
| 0036 | accepted | attachments | Attachment citizen: three atomic states; declared requirement conditional; `collect_members` rows + `ITEMIZATION_TIE_OUT_VIOLATION`; presence-semantics categorical Part III; generic across schedules. |
| 0037 | accepted | rules, explanation | `conditional_dependency_set`: one walk names every absent member of a conditional dependency set (rule-artifact.v3 only). |
| 0038 | accepted | worksheet | Line 16: QDCG worksheet as declared v3 successor rule; capital-gain inputs bound to declared-absence facts; bidirectional admission-locus contradiction interlock; qualified-zero reduction grounded in the dependency-set contract. |
| 0039 | accepted | process | This index is the advisory always-loaded routing surface: charters route by tag, agents read Decision sections by default, role cores apply; all accepted ADRs bind regardless of routing and text governs over digest. |
