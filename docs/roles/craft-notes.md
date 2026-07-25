# Craft Notes

Audience: Agents filling the foreman, builder, and reviewer seats.

A living record of **pithy, durable reminders** — the how-to-hold-the-tool
lessons that recur across tracks but belong in neither an ADR (they decide
nothing) nor a retrospective (they are not history). Each line is a
reusable heuristic with a one-line why, and — where it helps — the track
that earned it.

This file grows by **promotion**: when a retrospective or advisor counsel
surfaces a lesson worth carrying forward as craft, the owner approves and
the foreman records it here. Keep entries short; if a reminder needs a
paragraph, it probably wants an ADR or a plan section instead. Prune lines
that have hardened into tooling or ratified process.

## Foreman

- **A failed gate rejects readiness, not reusable work.** Preserve the reviewed
  implementation and passing evidence, isolate the failed claims, and charter
  repair from that exact artifact. Starting over destroys evidence, context,
  and learning without buying independence.

- **Separate the instrument from the experiment.** Make an evaluator
  trustworthy as tooling before asking it to support product, process, or
  economy conclusions. Tool completion can succeed while an experiment remains
  unrun.

- **Delta-review the delta.** Reuse unchanged evidence at the scope where it
  remains valid; independently recheck changed behavior, the finding class, and
  adjacent invariants. A repair is not a license to buy the entire first review
  again.

- **Measurement enables a verdict; it does not guarantee savings.** Economy
  telemetry is successful when it supports an honest comparison, including
  `insufficient evidence` or `not economical`.

- **Spend review on novelty; make known attacks shared input.** Before
  chartering a build or review, map prior findings into applicable invariants
  and executable checks. Give that map to both seats, require the builder to
  close the known classes, and tell the reviewer which novel boundary remains
  to probe. Re-paying a reviewer to rediscover a documented class is a foreman
  allocation failure, not reviewer rigor.

- **Charter the invariant, not the symptom.** A remediation charter should
  name the end-state property you want ("select one explicit target; fail
  loudly if it is missing"), not just the outcome ("make the battery
  green"). Ask only for the outcome and a builder will reach it by the
  cheapest path — often reproducing the very shape that caused the defect.
  *(Track 3: the F1 fix re-introduced the first-match smell; a
  property-level charter would have collapsed the R1 round.)*

- **Exclude the charter commit from the object-under-review range.** When
  you charter a re-review of commit X, the object is X's own diff, not
  `charter-commit..X`. A range that swallows its own charter forces the
  reviewer to spend a finding reconciling file counts. *(Track 3: finding
  R2, and again on the next charter until explicitly guarded.)*

- **A clean first review is an upstream win.** When a build passes every
  content check on the first pass, the charter carried the prior track's
  lessons well — that is where the work paid off. When it does not, look
  first at what the charter left implicit, not at the builder.

- **Keep process documents lean; don't count their lines.** A design,
  charter, examination, or review is as long as its declared scope, cases,
  and evidence rung require — write exactly that and stop when the
  obligations are reported. There is deliberately *no* numeric length cap
  (they were tried, miscalibrated on every real topic, and removed);
  don't reintroduce one, and don't pad to
  look thorough. Thorough evidence is not scope pathology; runaway
  *iterations* are — watch those instead.

- **Escalate the architectural wall; don't charter another repair against
  it.** When a blocking finding traces to a missing capability, identity, or
  trust boundary that no bounded repair can move, the choice is the owner's,
  not another patch cycle's. The tell: a finding recurs after a good-faith
  fix, or the fix would need a boundary the topology structurally lacks. And
  when a level proves infeasible, prefer an honest rescope to the *achievable*
  level over abandoning the work that still holds. *(Guarded Transport H1: a
  same-UID credential leak was an identity-boundary decision; the effort that
  drove real evidence escalated it, the one on simulated evidence offered
  another repair.)*

- **Give the owner a clean menu, and name the decision's tier.** A
  stop-for-disposition presents mutually-exclusive options, each with its
  consequence, and says plainly whether you are asking for a tactical call
  (repair/retry) or a Tier-3 architectural/scope decision. A vague "repair or
  stop?" hides which kind of decision it is and nudges the owner toward the
  cheap-looking option. *(Guarded Transport H1: one foreman offered tiered
  options with a recommendation; the other offered repair-or-terminate and
  leaned repair, obscuring an unrecognized Tier-3 fork.)*

- **Reuse a seat along its own lineage; spawn fresh across every independence
  boundary.** Re-task an existing seat with `followup_task` only within its
  role lineage — a builder repairs its own work, a reviewer re-reviews the
  target it first examined — for continuity and lower overhead. **Never**
  reuse a seat across an independence boundary: a clean-room rival, or the
  first independent review of a build, must be a fresh spawn with no exposure
  to the other side. Reuse may carry memory of one's *own* work; it must never
  import knowledge of the counterparty. *(Guarded Transport H1: reuse gave
  better-informed repairs and self-consistent delta reviews; the rivalry still
  requires fresh clean-room seats.)*

- **A new rung is a spend decision, not just an execution step.** Before
  climbing past the authorized rung or opening a round beyond the chartered
  plan, surface the increment and get a nod. There is no standing "dispatch as
  needed" (ADR-0045): each dispatch needs the owner's literal authorization
  string, bound to that role and charter. Approval of the plan authorizes
  execution *within* it, never escalation *of* it.

- **Match the reasoning tier to the task.** Reserve high effort for design,
  adversarial review, and judgment; a recheck-that-findings-were-addressed or
  a formatting normalization can run at a lower tier (`PROJECT_PLANNING.md`,
  Gate 8). Tier is
  the cheapest economy lever. *(Guarded Transport H1: both efforts ran every
  seat at max effort.)*

## Builder

- **Adopt before repairing.** When the plan names a reviewed source artifact,
  transplant it, verify its file set and identity, and make the repair legible
  as a delta. Do not reconstruct equivalent-looking work from memory.

- **Verify a "pre-existing" failure against base before you claim it.**
  Never assert a failing test pre-dates your branch without running the
  base to confirm. The check is cheap; a misattribution is not — it can
  cost a full review cycle to unwind. *(Track 3: two failures claimed
  pre-existing were genuinely branch-caused.)*

- **Fix the shape, not the instance.** When remediating a fragility,
  remove the pattern that caused it (an implicit ordering assumption, an
  unguarded first match), not just the one occurrence that broke. Leaving
  the shape in place invites the next instance.

- **A probe that simulates the surface under test proves nothing.** When a
  prototype climbs to an executable probe, it must exercise the *actual*
  mechanism — real transport, the real adversary path — not a mock, a fake
  upstream, or a printed secret. A simulated probe re-does paper at higher cost
  and manufactures confidence a reviewer will rightly reject; a fake success
  that bypasses the real call is a failure. *(Guarded Transport H1: simulated
  raw-Git probes passed their own assertions, then failed adversary review and
  hid the very boundary the real path exposed.)*

## Reviewer

- **Rerun load-bearing claims; don't accept the self-report.** The
  builder's own account of what the battery shows, or what pre-dates the
  branch, is input — not evidence. Independently rerun the base
  comparison, the live case, the failing test. *(Track 3: the reviewer
  disproved the builder's "pre-existing" claim by rerunning base.)*

- **Grep for the shortcut and the forbidden symbol.** Confirm goldens
  actually enter through the authoritative surface (`live_coordinate_run`,
  not a `RunContext` shortcut) and that forbidden bindings are truly
  absent — by direct grep, not by trusting the structure to exclude them.

- **Judge the evidence type, not just the pass/fail.** A green run on a
  simulated or synthetic probe establishes at most internal coherence, never
  that the real property holds; a probe that cannot complete is unproven, not
  disproven — and not proven either. Carry the evidence-type caveat into the
  verdict so a "pass" never upgrades confidence past what the evidence
  supports. *(Guarded Transport H1: the load-bearing adversary finding was that
  the probe simulated the transport rather than exercising it.)*
