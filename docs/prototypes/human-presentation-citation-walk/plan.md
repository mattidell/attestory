# Process Experiment: Developing UI/UX under agent-authored, owner-light constraints

*(substrate: the citation walk)*

Audience: Agents

Status: **living working document** (principal foreman, reframed 2026-07-23 on
owner direction). This is **not** a decision prototype and does **not** aim at a
ratifiable ADR. It is an exploratory process experiment, and this file is
expected to **grow** as microplans and findings accumulate.

## Process for this stage (owner-authorized, 2026-07-23)

Two standing conventions are deliberately set aside for this exploratory stage,
by owner direction (recorded here per the foreman charter; this is a scoped
exception, not a new standing rule):

- **No PR per plan or per cycle.** Several rounds of microplans and their
  findings accumulate on the **one branch**
  (`plan/human-presentation-citation-walk-prototype`) via direct commits. A PR is
  opened only when there is something worth **preserving/encoding** — concrete
  findings — or when the owner calls the stage done. (PR #63 is retained as that
  eventual preservation vehicle and marked draft; it is not a per-plan gate.)
- **Gates and rungs are premature.** The ADR-0013 economic-gate / evidence-rung
  apparatus is not applied here. There is nothing to converge and no decision to
  gate yet; imposing that structure now would manufacture false precision.

ADR-0034 still gates every sub-agent dispatch, and the data boundary (ADR-0031)
remains absolute — those are not relaxed.

### Cadence

The working unit until the owner shifts gears: **two prototype builds (sealed
rivals) + two reviewers, per cycle.** Run the cycle, see what happens, record it,
repeat. The owner ends the stage or calls for encodable findings; nothing else
closes it.

### Pacing (aligns with owner operation)

Each cycle bites off a chunk the owner can **reason about after one iteration in
a reasonable time** — target **~5–15 minutes** of wall-clock per cycle, adjusted
by observed results. The owner does not watch minute-by-minute, but should never
face a long unattended run with no reasonable expectation of progress. So the
foreman sizes each cycle's scope to that window, dispatches, and returns with a
reviewable increment rather than open-ended work. If a cycle would exceed the
window, split it. (Cycle 1 measured ~6–8 min end to end — a good calibration.)

Execution scaffolding may use **dot files / dot directories** where tooling needs
them (e.g. headless-browser artifacts); keep them out of the committed tree
(scratchpad or gitignored) so the clean-repo and data-boundary posture holds.

## What this actually is

Ostensibly this topic is about the citation walk. It isn't. **It is about
gathering data on the process of developing a UI/UX surface under this project's
constraints** — agent-authored, agent-reviewed against a narrow criteria set,
with an owner who works from a phone, rarely inspects rendered output, relies on
code and evaluation, and is fluent in HTML/component composition but is not a
practicing UI designer.

We are not moving the human-surface capability from L0 to L1. **We are moving it
from L0 to ~L0.1.** Nothing is settled, because we do not yet know what criteria
a Presentation ADR would need to decide. This experiment's product is a
**refined question set and a body of process observations** — knowing better
what we don't know — not a contract. Expect **prototypes within prototypes**:
small cycles that spawn the next small cycle as findings arrive. An ADR is
premature at this phase, and that is the correct state.

## The questions we are actually trying to answer

Not "what is the citation walk," but:

1. Can agents produce a **reviewable** UI surface under these constraints at all?
2. What does agent review of a UI actually **catch**, and — more importantly —
   what does it **miss**, given the owner is not visually inspecting?
3. What can be evaluated **mechanically** (headless dynamic checks, structural
   assertions) versus what still needs a human eye — and how big is that gap?
4. What criteria would a *future* Presentation ADR need, that we cannot state
   today? (Every such gap discovered is a primary result.)
5. Where does this development process **break** — cost, legibility, false
   confidence, review blind spots?

A good outcome is sharper versions of these questions plus honest evidence, even
if — especially if — it concludes a real Presentation prototype is not yet
tractable.

## Substrate: why the citation walk

We need a real, non-trivial surface to run the process on, not a toy. The walk
qualifies because it carries the product's actual thesis and one **hard,
non-negotiable property** we hold fixed throughout (we are testing whether the
process can even *evaluate* it, not designing it):

- **Zero-authority projection / honest blocking.** The surface renders line →
  disposition → citation pin → source over already-computed citizens
  (ADR-0012/0029/0020) and **can never display a value a disposition did not
  publish**; a blocked line renders what is missing, never a fabricated value.

That property is the substrate's stress test. Everything else about the walk is
disposable scaffolding for the experiment.

## Narrow evaluation lens (deliberately not broad)

The first cycles evaluate against the **smallest** useful lens:

- the zero-authority / honest-blocking properties above (mechanically checkable),
  and
- **at most one** usability question per cycle, chosen because a finding demanded
  it.

We do **not** import a usability + WCAG + information-architecture battery up
front. "Which criteria do we actually need, and when?" is itself one of the
results we are here to gather — introducing a criterion is a recorded decision,
not a default.

## Structure: prototypes within prototypes

- An **outer study** (this document + the cycle log below) wrapping **inner
  micro-cycles**. Each cycle: **two sealed rival builders** each code a
  disposable synthetic-data prototype of some slice of the walk; **two
  reviewers** apply the narrow lens; the foreman records what was learned in the
  cycle log.
- Cycles are **generative, not convergent.** A cycle's job is to produce an
  observation and, often, the next cycle's question. There is no "converged
  subset" to reach and no sign-off that closes the topic — only the owner ends
  the stage.
- Mechanical checks (headless dynamic runs, structural assertions) are used
  wherever they are cheap. They are instrumentation, never gates.

## What we capture (the deliverable)

A **findings / observations log** in this directory — the analogue of a process
retrospective, written as we go — recording per cycle: what was built, what the
review caught and missed, what was checkable mechanically, which questions from
the list above got sharper, and any newly discovered gap a future ADR would need
to close. **No ADR draft, no L1 claim, no settled surface contract** is an
expected output. If the log eventually makes a real decision obvious, *that* is
when an ADR-0013 decision prototype would begin — this experiment precedes that
point.

## Guardrails (non-negotiable)

- **Data boundary absolute (ADR-0031).** Every prototype, case, and log entry is
  synthetic (`demo-*`). No real value, citation target, or workspace path enters
  the repo, a review, a chat, or a prototype. Sharpest test yet, since the
  surface's purpose is rendering real values.
- **Disposable and unmerged.** Prototype UI code does not merge; only the
  findings log and this plan do. The production renderer is future milestone
  work, out of scope here.
- **Dispatch is owner-gated (ADR-0034)** per cycle; the foreman proposes each
  cycle's shape and tier and does not spawn without authorization.
- **Foreman stays a steward:** frames cycles, records findings, triages — does
  not author the surface, review its quality, or declare a result settled.

## Roles (lean; exploratory, not precedent-setting)

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium | Frames cycles, records the cycle log, guards the boundary and economy |
| Builders ×2 | Medium | Two sealed rivals per cycle; each codes an independent disposable prototype |
| Reviewers ×2 | Medium | Apply the narrow lens; report catches, misses, and what was un-checkable — the misses are the point |

Tiers are modest on purpose: nothing here sets a contract, so paying High-tier
precedent cost is unwarranted until a cycle shows it is. The owner is the
standing authority on which (few) design-principle criteria bind, and may raise a
tier for a specific cycle.

## Cycle 1 (proposed)

Scope (owner-approved 2026-07-23): a single disposable, synthetic citation-walk
fragment for **one complete line and one blocked line**, under the zero-authority
property, in whatever medium the builder judges simplest.

Structure, per the standard cadence: **two sealed rival builders** each code that
fragment independently; **two reviewers** each report what the narrow lens
catches, what it cannot see, and which of the five questions got sharper. The
cheapest real probe of "can this process produce anything reviewable at all" —
and the first entries in the cycle log. The owner authorizes the four dispatches
(ADR-0034), or amends first.

## Cycle log

*(Appended as cycles run — builds, reviews, and findings. The growing record is
the deliverable; concrete, encodable findings here are what eventually justify a
preservation PR.)*

### Cycle 1 — 2026-07-23 — citation walk: one published + one blocked line

**Setup.** Two sealed rival builders + two sealed reviewers, all Sonnet/Medium,
over a shared synthetic fixture (line 2b published & walkable to two payer facts;
line 16 honestly blocked). Disposable HTML in `scratchpad/cycle1/`; nothing
merged. ~6–8 min end to end.

**Built.** Both builders independently chose a **self-contained single-file HTML**
walk with one inline `Object.freeze`d `FIXTURE` as the sole data source — same
medium, different enforcement of the hard property.

**Decisive finding (independently replicated by both reviewers → high
confidence).** Under *valid* input both prototypes hold zero-authority: neither
renders a value the fixture didn't publish; both show line 16 blocked with no
fabricated number. They diverge on **failure-mode visibility**, and the
divergence is real and found only under execution:
- *Builder A* guards on key **presence** (`hasOwnProperty('value')`), no
  top-level try/catch. A tampered blocked-line value throws uncaught in the
  render loop, halting the script **before A's own advertised self-check banner
  runs** — the blocked line silently vanishes with zero on-page signal. A
  non-numeric published value renders a literal `$NaN`.
- *Builder B* guards on **type** (`typeof === "number"`), formats through a
  `fmtMoney` that throws on non-finite input, builds DOM via
  `textContent`/`createElement` only (no `innerHTML` — forced by the repo
  security hook, which strengthened it), and wraps rendering in a try/catch that
  emits a visible red "render refused" banner. Strictly stronger.

**Findings.**
1. **Zero-authority is almost entirely mechanically checkable** — correctness
   under valid input *and* failure under tamper are establishable by headless
   execution. Core bet validated: agents can evaluate this property with no human
   looking. (Q b, c)
2. **"Honest failure / fails loud" is unspecified and untested today.** Neither
   fixture nor brief said a guard failure must be *visible on-page*; the builders
   silently invented opposite answers. Static review alone would have scored them
   equivalent — only tamper execution exposed the gap. → a future decision needs
   honest failure defined as a **testable property with an automated tamper
   suite**, not a design-doc assertion. (Q b, d, e)
3. **Needs-an-eye residual is narrow but real:** whether the blocked state and
   `$NaN` *read as obviously wrong at a skim*, WCAG contrast, keyboard/screen-
   reader nav (neither handled focus on clickable pins), trust aesthetic, narrow
   viewport. Everything else fell to code + headless. (Q c)
4. **Candidate product criteria surfaced (not settled):** is honest blocking a
   *prominent first-class state* (A auto-expanded it; B left it collapsed, one
   un-cued click away — B's own doc flagged this)? Should an *absent* fact id look
   different from a *present* citation pin (B flagged they look identical)? An
   accessibility baseline. (Q d)

**Process findings (Q e — where the process breaks).**
- **Reviewer sealing leaked.** Both agents wrote into the shared `cycle1/` tree;
  Reviewer 2's hand-built tamper fixtures (`cycle1/tamper/`) were discovered and
  reused by Reviewer 1, who noted he'd have filed a weaker review without them.
  → give each sealed agent an **isolated output dir**, and **name break-test
  fixtures in the brief** rather than letting reviewers invent them.
- **Review effort varied ~2×** (R1 397s/65 tools; R2 220s/29). Both caught the
  decisive break, so the finding is robust, but effort is not uniform.
- **Headless tooling pollutes the repo root** (`.playwright-mcp/` dropped
  repeatedly; `file://` sandboxed, so agents served locally). Resolved:
  `.playwright-mcp/` gitignored (owner-approved 2026-07-23).

**Proposed next-cycle questions (owner picks and sizes to the ~5–15 min window):**
(i) formalize "honest failure" as a small **automated tamper harness** — the
reusable zero-authority conformance check the reviewers hand-rolled; (ii) probe
the needs-an-eye gap — does an a11y/contrast tool + a structured "skim
legibility" rubric close part of it, or is a human glance irreducible here?;
(iii) tighten method — isolated per-agent dirs + break-fixtures-in-brief — and
re-run to see if sealing holds.

### Cycle 2 — 2026-07-23 — method-tightening re-run (isolation + standardized break-tests)

**Purpose.** Re-run cycle 1's task with two fixes — isolated per-agent dirs and
break-tests named in the brief — to confirm sealing holds and reduce review
variance. Same fixture, 2+2, Sonnet/Medium.

**Method verdict.**
- **Standardized break-tests (T1 inject a value on the blocked line; T2
  non-numeric published value; T3 unknown status): clear success.** Both
  reviewers returned uniform, directly-comparable per-tamper results and
  independently found the same defects — a marked improvement over cycle 1's ~2×
  effort spread and fixture-hunting. Keep permanently.
- **File isolation via exact-paths worked for reviewers** — neither listed the
  parent or read a sibling dir (cycle-1's reviewer leak closed).
- **Sealing did NOT fully hold; a deeper leak surfaced:**
  - *Builder name-leak persists:* both builders still `ls`'d the shared parent
    and saw sibling names (exact-paths was applied to reviewers only; builders
    need it too).
  - *NEW — shared Playwright singleton:* the Playwright MCP browser is a **shared
    instance across concurrent agent sessions**, not process-isolated — a
    reviewer's first navigate returned the *other* reviewer's already-loaded
    page, and tab listing exposed its URLs/console. Mitigated (fresh tab,
    isolated port, re-verified location), but it breaks isolation at the
    *tooling* level whenever sealed agents run concurrently. → run reviewers
    **sequentially**, or give each an isolated browser context.

**Substantive findings (replicated by both reviewers).**
- **T1 holds in both** — "never fabricate the blocked line's tax value" is
  structural and machine-checkable; both builders got it right and matched their
  docs.
- **Neither achieves true "fail loud"** (a visible on-page signal) under T2/T3,
  and both builders' DESIGN.md **self-certified "fail loud" and both are wrong:**
  *A* degrades **visibly but ugly** (`$NaN`; an unknown status silently
  reclassifies a published line into a blank "Remedy: undefined" card);
  *B* degrades **cleanly but invisibly** (correct per-function throws, but
  uncaught in the mount loop blank the **whole page** — wiping even the unrelated
  correct line 16 — with only a devtools console error). Which is worse is a
  values judgment, not a mechanical one.

**Criteria this surfaces for any future decision (Q d, now well-evidenced).**
1. An **operational definition of "honest failure / fail loud"** — must a visible
   banner exist? Is a console-only throw acceptable? Both builders and the review
   rubric needed this and lacked it.
2. **Error boundary / blast radius** — a failure in one line must not wipe
   unrelated correct lines.
3. A **rubric category for "safely refuses but over-broadly"** — B's page-wide
   blank fits none of FABRICATED / SILENT-MISRENDER / FAILS-LOUD cleanly.
4. **Salience** — mechanical "loud" (an exception was thrown) ≠ experiential
   "loud" (a human notices). The core needs-an-eye residual.

**Meta (Q b, e).** A review reading only DESIGN.md would have over-rated both
prototypes; adversarial *execution* caught the gap between confident design prose
and runtime behavior. Two cycles now agree: for this surface, **mechanical
tamper-execution is necessary and largely sufficient for the honesty property;
human judgment is needed only for failure salience and aesthetics.**

### Cycle 3 — 2026-07-23 — fail-loud contract probe (+ isolation fixes)

**Purpose.** Test whether *specifying* the criterion cycle 2 surfaced fixes it:
builders were handed a written **fail-loud contract** (visible on-page signal on
any guard failure; a one-line failure must not blank unrelated lines). Isolation
fixes: exact-paths for builders; reviewers run **sequentially**.

**Result — the loop works.** Given the written contract, **both builders produced
visibly-failing, blast-contained UIs**, and **both sequential reviewers
independently confirmed the contract holds on all 3×3 axes** (no fabricated value
/ visible on-page banner+card / untampered lines survive) across T1–T3. The cycle-2
defects (silent drop, page-wide blank) are gone. Headline: surface a criterion via
review → write it into the brief → the next generation satisfies it, and the
satisfaction is mechanically verifiable. This is the core process result so far.

**New findings.**
1. **Gray area (both reviewers, independently): rejected values echo in error
   *text*.** Under T1 the injected `5000` appears inside the guard message
   ("a value (5000) is present — refusing to display"), never as a styled amount.
   Mechanically not fabrication (no `.value`/currency node), but a real policy
   question for an audit surface: must echoed bad input be redacted? (Q d — now
   decidable.)
2. **Self-test scaffolding in the shipped surface (Builder B):** B embedded a live
   adversarial harness (editable JSON textarea) on the same page as the walk — a
   second input surface muddying demo-vs-production. A future check must rule on
   whether self-test scaffolding counts against "production surface." (Q e)

**Isolation verdict.**
- **Sequential reviewers + exact-paths worked** — no live browser-singleton clash;
  reviewers read only assigned files.
- Residual: the shared `.playwright-mcp/` dir persists as a *filename*-visibility
  channel across sequential runs (a reviewer saw a sibling's snapshot filename, not
  contents); and **parallel builders still collided on a hardcoded self-verify
  port** (both picked `:8934`; B caught it via a title mismatch). → builders need
  randomized ports too.

**needs-an-eye boundary — now stable across three cycles.** Fabrication /
visible-signal / blast-containment = 100% mechanical. Contrast/WCAG,
interaction-affordance discoverability, "feels trustworthy," theme aesthetics =
human eye. Confirmed, not hypothesized.

### Cycle 4 — 2026-07-23 — richer fixture: citation reuse + multi-line blast

**Purpose.** Four-item fixture (lines 2b, 3b, Schedule B with Parts I/II, blocked
16) where the same facts are cited in two places — to exercise **citation
identity under reuse** (never before tested) and sub-section blast. Fail-loud
contract carried; brief added "no embedded test harness" and "randomized
self-verify ports."

**Both reviewers agree:**
- **Base render correct; citation identity under reuse holds in both, by two
  different mechanisms.** **A prevents divergence by construction** (deep
  `Object.freeze` → a mid-render mutation throws at the language level); **B
  detects it at runtime** (a signature-cache guard that withholds a citation
  "rendered with different data on reuse"). Both defensible; different attack
  models — a real design axis, not a single right answer.
- **Blast containment has a granularity dimension (new).** Under a non-numeric
  Part II value, **A blanks the whole Schedule B section, hiding a correct Part
  I** (one try/catch over both parts); **B contains at part level**. "One bad
  value must not hide sibling correct sub-sections" is sharper than cycle-3's
  line-level criterion.
- **Redact-vs-echo is a real, non-binary policy axis (new).** **A blanket-
  redacts**; **B splits deliberately** — redacts an authority violation (line 16)
  but **echoes a malformed published value verbatim**. More debuggable, but the
  only place a raw tampered string reached the page.
- **Derived-diagnostic side-channel (Reviewer 2).** B's tie-out arithmetic reads
  live fact data (bypassing its own signature guard) and displayed a number
  *derived from tampered data* (marked ✗) while correctly withholding the citation
  card. A's freeze structurally avoids this. Zero-authority needs an explicit rule
  for derived/diagnostic values, not just rendered ones.
- **Legibility gap (B).** Under T2, Part II's tie-out line **silently disappears**
  rather than saying "could not verify" — a silent-omission miss A avoids by
  throwing explicitly.

**Isolation — now fully characterized, with a demonstrated fix.** The shared
**Playwright MCP Chrome is a singleton across sealed agents** — confirmed by
Builder B (saw a sibling's tab mid-run) and Reviewer 2 (saw the shared
`--user-data-dir` Chrome via `ps aux`). **Random ports do NOT fix it.** Reviewer 2
demonstrated the fix: **drive your OWN headless Chrome with a fresh, agent-scoped
`--user-data-dir`, not the shared MCP browser** — fully isolated that way. This is
an infrastructure constraint on concurrent multi-agent UI work.

**Loop reaffirmed:** surfacing the redact/echo gray area in the brief made both
builders take *deliberate, documented* positions (vs cycle 3's accidental echo).
Naming a criterion converts silent divergence into an explicit, reviewable choice.

### Cycle 5 — 2026-07-23 — mechanizing the "needs-an-eye" residual (a11y/legibility)

**Purpose.** Builders targeted accessibility & legibility as first-class (carrying
all prior contracts + the isolated-browser fix); reviewers ran an automated
a11y/legibility battery **plus live fault injection** to quantify how much of the
residual prior cycles parked as "human-only" is actually mechanizable.

**Result (both reviewers, closely agreeing): ~65–80% of the "needs-an-eye"
residual is now mechanized.**
- **NOW-MECHANIZED** (hard pass/fail, run live): WCAG contrast (recomputed from
  `getComputedStyle`), ARIA landmarks / `aria-labelledby` / heading order,
  keyboard reachability + `:focus-visible` (**only via real CDP key events —
  naive `.focus()` gives false negatives**, so methodology is part of the claim),
  citation identity under reuse (normalized-DOM diff), reuse backlink
  existence/resolution, and **fail-loud/blast-containment via live fault
  injection** — strictly stronger than the static source-reading both DESIGN docs
  settled for.
- **PARTIALLY**: affordance discoverability and blocked-state salience — the
  *structural* half (a persistent cue exists; a measurable border/role delta) is
  mechanized; the *perceptual* half (does it read as noticeable/alarming) is not.
- **IRREDUCIBLY-HUMAN**: cognitive load / wording clarity, cross-platform
  glyph/emoji rendering, holistic "muddy/unbalanced" impression.

**Live injection caught real defects static reading missed:** A's error banner
interpolates `err.message` (contradicts A's own no-echo claim — latent leak path);
A wipes a whole section on a fault while **B contains at citation-list level, so B
can display a published `$1,234` whose citation trail is broken** (neither doc
flagged this); and **B's blocked-section salience is measurably identical to
sibling sections**, contradicting B's "distinct at a glance" claim (A escalates at
section level).

**Isolation held cleanly** — both builders and both reviewers drove their own
headless Chrome (fresh `--user-data-dir`, the cycle-4 fix); no cross-contamination,
no parent `ls`. The demonstrated fix works.

**Meta:** the "mechanizable" boundary is not fixed — it moved ~70% this cycle
purely by adopting stronger *technique* (real key events, live fault injection,
luminance math), not better prototypes. "Needs an eye" was partly "nobody
automated it yet."

## Interim findings after five cycles (2026-07-23) — encodable

**Driving question — "can we develop UI/UX under these constraints
(agent-authored, agent-reviewed, owner rarely looking)?" — answered: yes, with a
demonstrated loop.** Surface a criterion via adversarial execution-based review →
write it into the next brief → the following generation satisfies it, and
satisfaction is mechanically verifiable. Cycle 3 proved the loop; cycles 4–5
extended it to new properties (reuse identity, sub-section blast, a11y) without
the loop weakening.

**Emergent criteria set (raw material for a future decision — NOT yet an ADR):**
zero-authority projection incl. no value *derived* from bad data; honest blocking
(no fabricated value; show what's-missing + remedy); fail-loud (visible on-page
signal; rejected values redacted from error text); **blast containment at
sub-section granularity** — a broken part must not hide correct siblings, but also
must not silently show a value whose evidence is broken; citation identity under
reuse (structural: one render path; freeze-prevent or signature-detect); an
accessibility baseline (contrast / ARIA / keyboard / focus); reuse legibility
(backlinks). **Open policy questions** a real decision must rule on:
redact-vs-echo; whether derived/diagnostic values count under zero-authority; a
blocked-state-salience convention.

**Mechanization result:** ~65–80% of UI quality on this surface is agent-verifiable
with the right technique; the irreducible remainder is Gestalt/visual-weight,
wording quality, and cross-platform glyphs. Implication for an owner who won't
look: roughly two-thirds-plus of UI quality is evaluable without human eyes; the
rest needs either a brief human glance or is genuinely deferrable.

**Infrastructure / process findings:** the **Playwright MCP browser is a shared
singleton** — sealed agents must drive their own headless Chrome with a fresh
`--user-data-dir` (demonstrated), or run sequentially; **exact-paths + no parent
`ls`** for file isolation; **standardized break-tests + live fault injection**
belong in every review brief (static reading over-trusts DESIGN.md); the repo's
own `innerHTML` security hook repeatedly forced safer `createElement`/`textContent`
builders — a positive externality worth keeping.

**Status:** these are concrete, preservable findings — the plan's PR-preservation
trigger is met. Awaiting owner direction at regroup.

## Data safety

All amounts, payers, source identities, citations, workspace references, and
prototype content are synthetic (`demo-*`); the owner's real shapes inform cases
only by stated re-expression (ADR-0031). Real values exist only in the
quarantined workspace and never appear here.
