What's genuinely working (keep all of this)
The planning architecture is excellent. Audience separation (User/Agent/User+Agent), phase→milestone→track hierarchy, planning commits before implementation, per-track commits, two-gate review — this is real orchestration infrastructure, and it's why you can remote-drive this project at all. Most people running agent workflows have nothing like it.

Contract-first development is your product thesis expressed as engineering. Schemas, golden fixtures, deterministic runs, and the run manifest are the audit story. field-resolution.json with dependency-aware resolution is the seed of your differentiating feature. This alignment between how you build and what you're building is rare and worth protecting.

The agent briefs are a genuine decision log. Every decision recorded with "why it matters," explicit out-of-scope lists, follow-up points. The product-boundary-contract brief in particular reads like a competent staff engineer's design review.

The defaults you've been accepting are mostly good judgment. You asked directly, so let me be specific. Reviewing the decision logs: in-memory read models instead of durable JSON artifacts (avoided schema/fixture/safety overhead for a projection layer — correct), jurisdiction as a list with only federal supported (cheap structural headroom, no speculative implementation — correct), run payloads as immutable snapshots rather than independent snapshot objects (right product concept), deferring partial-write recovery and failure modeling (correct — YAGNI until a surface needs it), rejecting the recursive JsonValue type (correct, that path is misery). I found no default I'd call a bad call. Your delegation instinct is fine.

Can you work smarter? Yes, three concrete changes:

Tiered decision protocol (add to PROJECT_PLANNING.md). Tier 1 — reversible, internal (typing strategy, file layout, fixture organization): agent decides, logs in the brief, never asks. Tier 2 — contract shapes future surfaces consume: agent decides with a stated default in the plan; you veto asynchronously or it stands. Tier 3 — user-visible concepts, naming, boundaries, anything irreversible or thesis-relevant: surfaced to you, framed in product terms, with a recommendation and what each option forecloses. Require every milestone plan to open with a "Decisions for the user" section capped at ~3 Tier-3 items. If a plan has zero Tier-3 decisions, that itself is a signal it might not need your review gate at all.

Collapse gates for low-risk milestones. When you approve a plan, also pre-authorize completion-on-green: if all tracks verify and nothing deviated from plan, the agent merges and reports. Keep the two-gate flow only for milestones carrying Tier-3 decisions. This roughly halves your synchronous involvement.

Standard brief header. Briefs are ~10KB each; six of them landed today. Mandate a 10-line header: what shipped, Tier-1/2 decisions taken (one line each), Tier-3 questions pending, recommended next action. You read headers; you dive only when flagged. And create a single docs/decision-log.md where follow-up points get consolidated with a status, reconciled at each milestone boundary — briefs reference it instead of accumulating orphan lists.

