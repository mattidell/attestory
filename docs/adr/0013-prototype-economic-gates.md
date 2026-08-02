# ADR 0013 — Prototype Economic Gates and the Prototype Plan

- Status: **retired** (ADR-0045, 2026-07-25) — history only, not authority. Previously: accepted (ratified 2026-07-12)
- Tier: 3
- Date: 2026-07-12

> **Retired 2026-07-25 by [ADR-0045](0045-agent-instruction-consolidation.md).**
> Process is the owner's operational domain and is no longer recorded as ADRs.
> This record is retained permanently as history and rationale — cite it for
> *why* a practice exists, never as binding authority. Its still-operative
> content lives in `PROJECT_PLANNING.md`, "Prototype Economic Gates".

## Context

ADR-0005 established that consequential decisions are made from prototype
evidence, and it anticipated its own amendment "as lessons accumulate." The
first full run of that process — the Tax Citizen Families prototype, First Tax
Slice Track 0 — supplied the lesson. It reached correct modeling conclusions but
was uneconomical: it combined several distinct Tier 2 decisions into one gate and
used production-path integration as the acceptance standard for all of them, so
reviewer thoroughness converted into unbounded scope growth (four iterations,
sixteen reviews, ~6,100 lines of process documents, and much of implementation
Tracks 1–5 performed speculatively inside Track 0).

The process retrospective
(`docs/archive/2026-08-02-milestone-artifacts/prototypes/tax-citizen-families/process-retrospective.md`) diagnosed five
cost drivers — too many decisions per gate, prototype/implementation evidence
conflated, adjacent defects expanding the charter, green-check incentives, and a
partly-false "finished machinery" premise — and proposed an economic-gates set.
That set correctly named the levers but was stated as principles with no
operational home and no accountable owner, so nothing forced them during a run.
This ADR ratifies an operationalized version.

Full proposal and rationale, including the gate-by-gate evaluation against the
recorded cost: `docs/archive/2026-08-02-milestone-artifacts/proposals/prototype-economic-gates.md`.

## Decision

The Prototype-Driven Decisions process in `PROJECT_PLANNING.md` is extended (not
replaced) with:

1. **Economic Gates 0–8** — decision inventory, per-proposition eligibility
   score, paper instantiation as the mandatory first rung, a four-rung evidence
   ladder climbed one rung at a time, fixed caps with session-bounded cost review
   (no cost-ratio trigger), foreman-owned review triage, partial ratification,
   production-adoption discipline, and a role capability budget.

2. **A mandatory prototype plan.** An owner-approved, committed
   `docs/prototypes/<topic>/plan.md` precedes the first charter of any prototype
   topic. It is reviewed by the owner alone. Its sections instantiate the gates
   explicitly. This makes the gates committed, reviewable structure rather than
   advice.

3. **Role capability budget (Gate 8).** Reasoning capability is a priced input.
   Each role is assigned a capability tier (abstract High / Medium / Economy in
   plans) and reasoning effort matched to task difficulty and the current
   evidence rung. A named-model example map across Anthropic, ChatGPT, Gemini,
   Grok, and open source lives in the protocol document and is refreshed as
   families ship; tier semantics, not the roster, are load-bearing. Fresh-reader
   legibility review is deliberately lower-tier because a strong model repairs
   the gap the test exists to expose.

4. **Foreman as scope-and-economy steward.** The foreman is accountable for the
   implementation — including reviews and the actions reviews propose — staying
   inside the declared scope boundaries and the spirit of economic efficiency:
   triaging findings and rerouting out-of-charter proposals, enforcing the
   evidence ladder and paper-first rule, tracking the fixed caps, assigning and
   dynamically revising role capability tiers as the decision clarifies, and — if
   able to spawn sub-agents — asking the owner for confirmation before spawning
   and dispatching each at the plan's assigned tier. These are stewardship
   duties; the foreman still never reviews artifact quality, overrules a
   committee finding on the merits, or resolves dissent by rewording it.

## Consequences

- The prototype process gains a committed, owner-reviewed planning artifact and a
  named owner for scope and economy; the levers named in the retrospective become
  enforceable rather than advisory.
- Cheaper evidence is paid for first: paper instantiation and single-rung climbs
  replace default end-to-end integration, and one prototype topic can no longer
  silently consume its downstream implementation tracks.
- Reasoning cost becomes an explicit, adjustable input; later dispatches in a
  converging run run at lower tiers.
- The foreman's workload grows (triage, budget tracking, tier assignment) and the
  owner's decision surface grows by one artifact (plan approval) but shrinks per
  round (fewer, better-scoped iterations).
- ADR-0005's core decision is unchanged; this ADR extends its process. Future
  material lessons amend the process by a further superseding ADR.

## Amendment (2026-07-12) — Optional foreman helper

Same-day owner discussion refined decision 4. The foreman seat splits into a
judgment core and a clerical shell; the shell may be delegated. Within the
prototype process, the foreman may delegate mechanical, auditable clerical work
(SEAT.md maintenance, round-file assembly, exhibit tagging, log-hygiene
formatting, traceability existence checks, data-safety scans, disposition-packet
collation, dictated status/wording edits) to an Economy- or Medium-tier helper
under the sub-agent confirmation gate, remaining fully accountable. The helper
never triages findings, decides dispositions, assigns capability tiers, changes
scope, composes status meaning, reviews artifact quality, or approves anything.
It is an optional economy, not a required seat, and is formalized for the
prototype process only (the milestone lifecycle may adopt the same principle
later). This is a refinement of the foreman stewardship role, not a new decision.

## Amendment (2026-07-12) — Reviewer sub-agent dispatch

Owner-directed refinement of decisions 3 and 4. When the foreman agent has
sub-agent capability, it spawns the committee reviewers as sub-agents **by
default**, each at the plan's stage-appropriate tier, in independent contexts.
Owner approval of the prototype plan (which names the reviewer seats and tiers)
is the standing authorization, so reviewers need no per-spawn confirmation; the
general confirmation gate still applies to non-reviewer spawns. Within-round
independence holds (reviewers do not see each other's in-progress work). When the
foreman lacks sub-agent capability, reviewers are owner-launched from role files
as before. This amends the `AGENTS.md` prototype-process-dispatch guardrail,
which previously reserved context-starved seats to owner launch.

Owner-directed follow-on (same day): prototype legibility review is a normal
foreman-spawned reviewer and is no longer a context-starved seat. The starved
fresh-reader rigor moves to a periodic, owner-spawned **Legibility Audit** at the
project level (`docs/legibility-audits/`), decoupling that measurement from every
prototype iteration.

## Amendment (2026-07-13) — Rival evidence every round; non-accepted ADRs are inert

Owner-directed after the Core Tax Conditions governance remediation, in which a
foreman satisfied the plans' rival requirement by having the incumbent author
both competing shapes in one context. Two rules are now explicit:

1. **Genuine rivalry per round.** Every prototype round requires independently
   contexted rival evidence: build rounds get a clean-room rival builder (denied
   all incumbent material), and review rounds get reviewers in independent
   contexts. A single context authoring competing shapes does not satisfy the
   rival requirement, and an evaluation may not claim it does.

2. **Non-accepted ADRs are inert.** Agents treat only `accepted`-status ADRs as
   binding contracts. `proposed` drafts guide work on their own topic only and
   must not be implemented against outside their prototype. Rejected or
   superseded ADRs are retained — never deleted — with their status marked, and
   are explicitly ignored as authority while remaining citable as history.

## Amendment (2026-07-15, **accepted** — owner ratification 2026-07-15) — Foreman-authored fixes default to confirmation

Owner-directed after the Core Tax Conditions Track 0.b residual round, in which
the foreman closed a decision-blocking adversary finding (a force-declare
under-trigger, MR-A7) by authoring a broadened rule itself, then surfaced it to
the owner as an "if this feels out-of-evidence, say so" question and otherwise
defaulted toward ratification. The broadened rule over-fired on ordinary
downstream arithmetic (line 9 = 1a+2b), an over-trigger direction no builder or
reviewer had tested.

The two-builder/two-reviewer structure guards against *builder* blind spots; it
places no guard on a fix the *foreman itself* authors to close an adversary
finding. This amendment adds that guard:

1. **Confirmation by default.** A fix the foreman authors to resolve an adversary
   or governance finding — not itself designed by a builder or checked by a
   reviewer — defaults to a **scoped confirmation pass** (a single reviewer seat
   is sufficient) before it enters ratifiable ADR text. The foreman recommends
   that pass **proactively** and states the specific case(s) it must exercise —
   including the direction opposite the original finding (if the finding was
   under-inclusion, the pass must test over-inclusion, and vice versa).

2. **Communication is the foreman's obligation, not the owner's burden.**
   Surfacing such a fix as an owner-judged "is this in-evidence?" question does
   **not** satisfy (1): the owner is not positioned to adjudicate whether a round's
   evidence supports a fix — that is the foreman's assessment to make. The
   conservative default (further review) is the foreman's to set; it must never be
   contingent on the owner detecting a problem the owner cannot see. When in
   doubt, the foreman recommends more evaluation, not less.

## Amendment (2026-07-20, owner-directed) — Gate-4 document-length caps removed

The Gate-4 **numeric document-length caps are removed.** This covers both the
original 800–900 line per-document caps and their 2026-07-16 recalibration
(design ≤ 300, examination ≤ 120, charter ≤ 100, total topic ≤ 1,800) — the
latter had lived only in the foreman role template, never in this ADR or
`PROJECT_PLANNING.md`, and contradicted the process doc, which already bounds
document length by obligation rather than line count.

A line target measures the wrong thing: thorough evidence is not scope
pathology, and every real Tier-3 topic exceeded the numbers, so they functioned
as noise rather than control. Document length is bounded by the pre-declared
scope, cases, evidence rung, and measurement charter — an author stops when
those obligations are completely reported, not when a file reaches an economic
target (`PROJECT_PLANNING.md`, Gate 4).

What Gate 4 keeps: the **structural caps** (iteration / reviewer / repair
counts) and **session-bounded cost review** with stop-and-decide on genuine
scope pathology — unchanged. The residual "keep process documents lean"
guidance is a **craft heuristic, not a gate parameter**
(`docs/roles/craft-notes.md`); do not reintroduce a numeric cap.

## Alternatives Considered

- **Keep the v1 gates as retrospective guidance.** Rejected: advisory gates with
  no home and no owner are exactly what failed in Track 0.
- **A cost-ratio stop-and-decide trigger (prototype cost as a fraction of
  estimated implementation cost).** Rejected by the owner: session usage is
  already bounded, so a session boundary is a natural cost-shape review point and
  a computed ratio adds machinery without adding control.
- **Committee-review the prototype plan.** Rejected by the owner: plan approval
  is the owner's alone; adding a committee round to the plan reintroduces the
  cost the gates exist to cut.
- **Bind role tiers to named models in each prototype plan.** Rejected: plans
  would rot as models release. Plans use abstract tiers; the protocol document
  carries the refreshable named-model map.

## Links

- Extends: ADR-0005 (consequential ADRs require prototype evidence)
- Evidence: `docs/archive/2026-08-02-milestone-artifacts/prototypes/tax-citizen-families/process-retrospective.md`
  (Cost Record, Why Cost Expanded, Economic Gates v1)
- Proposal and gate-by-gate evaluation: `docs/archive/2026-08-02-milestone-artifacts/proposals/prototype-economic-gates.md`
- Process definition amended: `PROJECT_PLANNING.md`, Prototype-Driven Decisions
  (Prototype Economic Gates)
- Prototype-foreman doctrine: `PROJECT_PLANNING.md`, Prototype-Driven Decisions
  (the retired role template is tombstoned at
  `docs/prototypes/_role-templates/foreman.md`; milestone role seeds live in
  `docs/roles/`)
