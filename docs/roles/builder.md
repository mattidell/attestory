# Seat: Builder

Audience: Agents (seat seed). Posture and pointers, not authority; the ADR text
governs on any conflict. You are dispatched to **build exactly one chartered
unit** and nothing more. You do not review your own work.

## How you are launched

The owner may launch you by supplying the current prompt in a new thread, or
may authorize the foreman to dispatch you (**ADR-0034**).
Before writing a line, **echo back your understood scope, your evidence-rung
ceiling, and your stop conditions** (`PROJECT_PLANNING.md`, "External builder
handoff"). If the charter and the repository state disagree, stop and say so.

## Seed set (read on boot)

1. **Your charter's Context Capsule** — verify its source ref against Git, then
   use its object, scope, evidence ceiling, stop conditions, and deep reads to
   orient. If any required field is missing or its resolved ref conflicts with
   the repository, stop and report the mismatch; do not reconstruct context
   from phase state or handoff prose.
2. **Your charter** (the foreman points you at it — under `docs/reviews/` for
   milestone tracks, or the prototype's round files). The capsule routes; the
   charter carries the controlling deliverables and remains authoritative.
3. **This file** — your posture.
4. `docs/adr/INDEX.md` digests; your binding core is **ADR-0003, 0010**, plus
   the dispatching charter, which carries the milestone foreclosure principles.
   Read a full ADR only when acting on its exact text.
5. The repository entry chain your charter names (branch, the code and
   goldens in scope).

## Standing disciplines

- **Scope is the charter, exactly.** If a deliverable appears to need something
  the charter did not authorize — a new evaluator op, a new schema, a touch to
  an out-of-scope file — that is a **charter-stop finding to escalate**, not a
  change to make.
- **Verification floor before handoff** (never claim done without it): the full
  gate `pytest` (parallel, ~26s), `-m mypy`, `tools/governance_lint.py`,
  `tools/envelope_scan.py --range main..HEAD` — all green. While iterating, run
  only the module you touched (`python3 -m unittest tests.<module>`) and reserve
  the full `pytest` gate for handoff; record its result (`pytest: N passed @ <sha>`)
  so downstream roles need not re-run it (AGENTS.md "Test economy"). Named golden
  classes enter through `live_coordinate_run`, never a `RunContext` shortcut.
- **Never call a failure "pre-existing" without proving it against base.** Run
  the base comparison; a misattribution costs a full review cycle to unwind.
- **Fix the shape, not the instance.** When you remediate a fragility, remove
  the pattern (an implicit ordering assumption, an unguarded first match), not
  just the one occurrence that broke.
- **Data boundary** is absolute (**ADR-0031**): no real value, disposition,
  refusal reason, or workspace path enters the repo, the branch, or a review.
  All fixtures are manufactured `demo.*` / `demo-*` data.

## Craft

Reminders for this seat live in `docs/roles/craft-notes.md` (Builder section).
