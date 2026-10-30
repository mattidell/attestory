<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "explanation-sharing",
  "status": "Complete: shared explanations and saved recovery retain full lineage; isolated test browser reuse, bounded startup and safe owner failure evidence preserve the tested boundaries. Required exact-head CI is the publication gate.",
  "scope": [
    "explain each shared input once and reference it at every reuse",
    "preserve a walk from each result to every actual dependency, including its producer and pin role",
    "keep explanation storage proportional to unique nodes and dependency edges while preserving published presentation history"
  ],
  "non_goals": [
    "no tax package, rule or parameter publication",
    "no change to tax results, evidence authority, currency or admission",
    "no broad reader redesign, CI redesign or unrelated performance refactor"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md",
      "docs/phases/engineering-health/milestones/explanation-sharing.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/explanation-sharing.md"
    ],
    "review": [
      "docs/roles/qualitative-review.md",
      "docs/phases/engineering-health/milestones/explanation-sharing.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-28-explanation-sharing.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md",
      "docs/phases/engineering-health/milestones/explanation-sharing.md"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-28-explanation-sharing.md"
}
-->

# Explain a Shared Input Once

Milestone key: `explanation-sharing`. Phase: Engineering Health.
Primary branch: `milestone/explanation-sharing-2025`, cut from `origin/main`.

## Purpose and current state

A calculation can use the same input through several intermediate results.
At opening, its explanation repeated the input and its supporting explanation
at every use. A historical core v58 line 27a observation reported 9,885 tree
nodes over 218 findings, without its reproduction procedure. A person following any line should still reach all of its inputs,
but a saved explanation should record shared information once and show where
it is reused. This reduces storage and traversal work without shortening the
evidence behind an answer.

The original walker already accepted a node memo, while its recursive
dictionary and text output expanded children at every path.
P0 distinguishes object reuse, serialized size, reader traversal, and runtime
cost. The parked measurement is a starting observation, not a corpus-wide
baseline. The earned-income-credit retrospective dated 2026-10-23 records the
historical observation; the former phase-state record has since been retired.

## Scope, constraints and preserved meaning

The milestone covers published-finding explanations, every caller that embeds
or renders them, and saved presentation recovery. A shared result keeps its
finding identity, value, producer, version and complete pin lineage. Every
incoming use keeps its own role. Authorization attached at a walk root stays
scoped to that walk. Blocked, absent, historical and cyclic cases retain their
existing meaning; reuse must not hide a failure or silently truncate a path.

No tax package, rule or parameter is published. No calculation, admission,
currency or question behavior is changed. The following files belong to the
parallel withholding milestone and are excluded: `packages/kernel/findings.py`,
`packages/kernel/act_log.py`, `packages/tax/loader.py`, and
`packages/derivation/live.py`. Do not claim core v59, registry v57 or release
v57. The owner subsequently authorized bounded Chrome lifecycle observation,
isolated test-browser reuse and a test-session startup limit. Diagnostic CI
steps leave shard selection, coverage accounting and the verify gate intact;
broader CI redesign remains outside this milestone. The explanation and tax
contracts remain unchanged.
All assignments use this milestone's own primary worktree and commit lock.

## Plan and readiness gates

1. **P0 — measure and map.** Commit a reproducible census of every committed
   presentation golden, reporting schema, roots, expanded nodes, distinct
   findings/provenance references, dependency edges and bytes. Reproduce the
   core v58 line 27a case or account precisely for a changed measurement. Trace
   all consumers of `explain()` and its output: projection/saved presentation,
   non-publication explanations, CLI/text, browser code and tests, including
   indirect imports. Compare internal-only reuse with an explicit shared output
   shape. State what a reader gains or loses and recommend the smallest complete
   change. P0 edits no production code or schema.
2. **Selection.** Refine the contract and build boundaries from P0. The owner
   assigned the capability and permits successor output shapes; implementation
   can proceed when evidence selects a meaning-preserving representation.
   A newly discovered change to evidence authority or an accepted ADR's meaning
   returns to the owner. Before any schema edit, consult and append intent to
   the schema ledger under `docs/process/concurrent-work.md`.
3. **Track 1 — shared explanation through caller and saved recovery.** P0
   showed the walker and its consumers must change together. Combine the two
   provisional build steps into one atomic implementation unit: shared
   walk/output, NPE, CLI, successor presentation, strict saved loading and
   bounded browser traversal. Use the selected contract below. Full pytest and
   mypy follow the integrated build, not a half-integrated API checkpoint.
4. **Review and close.** Foreman reviews ordinary units; a fresh independent
   Reviewer inspects the final curated range for semantics, reader reachability,
   schema/history integrity, data safety and closeout. Complete full pytest and
   mypy for derivation changes, curate per PROJECT_PLANNING.md, synchronize
   against the then-current ratified line and both concurrent milestones, and
   obtain green CI on the final head. Mark ready at least 30 seconds after the
   last push. The owner holds the merge.

P0 is a bounded measurement/design spike. Rival production prototypes are not
planned: the question is whether the requested sharing survives serialization,
not a new authority or identity model. If P0 exposes materially different
meaning or migration choices that paper cannot settle, revise the plan before
building rather than silently extending the spike.

## Cases and evidence

| Case | Required property |
| --- | --- |
| Every committed presentation golden | Baseline inventory is complete and reproducible; legacy bytes stay unchanged. |
| Core v58 line 27a | Same value, producer and reachable support; shared output size is measured against its actual reachable graph. |
| Diamond and repeated layered reuse | Each finding has one canonical explanation, all use edges remain traversable, growth follows nodes and edges rather than path count. |
| Same finding under `input` and `choice` | Each use keeps its role even if its target explanation is shared. |
| Two roots sharing input | Each root reaches its full support without leaking another root's authorization or context. |
| Missing pin, unknown leaf and cycle | Existing honest leaf/refusal behavior survives; reuse never conceals a cycle. |
| Blocked result and published predecessor | Failure detail and published lineage remain reachable through the actual NPE path. |
| Corrected input and saved historical run | No reuse across incompatible snapshots; the saved run remains explainable without the live run. |

P0 selected the exact regression paths and successor schema families. Tests
must exercise the real walker and serializer, normal presentation projection
and fresh saved-file loading, plus the affected CLI/browser route. Canonical
reachability and edge metadata, not headings or matching node counts alone,
establish preservation. Schema integrity is checked by
`tests/test_schema_registry.py`; data-safety checks precede pushes. No fixture
is regenerated merely to make a changed shape pass under its old version.

## Completion and deferrals

Complete when each newly generated explanation stores shared inputs once,
every result can still reach its complete actual support, all identified
consumers handle the selected shape, legacy saved presentations remain readable
and byte-identical, the corpus measurements demonstrate the size change, and
the final candidate passes independent review and required CI. The bound is
O(nodes + edges), since retaining many actual uses necessarily retains edges.
Keep storage-size and execution-time findings separate.

Reader polish, richer tax wording, a general explanation architecture,
persistent cross-run caches, test culling and new tax coverage are deferred.
All data and committed artifacts are synthetic `demo.*` cases. Personal data,
local outputs and absolute machine paths remain excluded. The retrospective,
measured outcome and roadmap preserve that boundary.

## P0 result and selected contract

[P0 evidence](explanation-sharing-evidence/README.md) inventories 36 presentation
goldens and nine examples. None saves the recursive `ExplanationNode` tree;
their root pins and flattened citation sites do not contain enough intermediate
findings to reconstruct it. The two identified core v58 line 27a cases expand
to 8,608 and 8,684 occurrences over 241 and 245 distinct IDs, respectively.
The historical 9,885/218 lacks a recorded scenario/counting procedure and is
not a reproducible comparison baseline. This corrects the initial saved-tree
premise without weakening the requested complete saved dependency walk.

1. Normal explanation output is a versioned graph, not a recursively copied
   tree. `explain()` and multi-root output use one run-local node table;
   `.to_dict()`/JSON/text preserve references on reuse. Any old recursive-tree
   conversion is explicit compatibility code, not the normal consumer path.
2. Node content carries exact finding identity, version, value, symbol and
   producer. Ordered edges retain every recorded pin's role, version and
   other metadata, including repeated edges. A role belongs to the incoming
   use, not the canonical target. Provenance references remain distinguishable
   from actual findings. Canonical-key conflicts fail rather than choosing
   whichever payload was seen first; identity is never guessed from names.
3. The table belongs to one immutable input snapshot/run. Each root retains
   its requested context and authorization, outside the shared node content.
   Active-path cycle detection precedes reuse. Serialization and validation
   reject dangling targets, cycles and conflicting identities. An intentionally
   unknown pin remains an explicit bare reference leaf under existing walker
   semantics; it is not a dangling table reference or a fabricated finding.
4. The normal CLI saves one graph across its roots and renders first use plus
   named reuse references. Publish `explanation-graph.v1` and NPE successor
   `npe-walk.v4` under the derivation schema registry after recording intent.
   NPE's actual run/ledger selection, disposition vocabulary, sparse fallback,
   missing and violation evidence remain unchanged. Preserve v1–v3 schema
   bytes and validation; no synthesized completion records.
5. New production saved presentations use a flat `presentation-model.v2`:
   retained top-level fields plus a shared explanation graph and explicit
   section/root references. Publish that successor schema despite v1 having
   been internal. The published shape and strict runtime validator together
   retain the existing specialized-block checks and add graph integrity.
   `presentation-model.v1` files load through an explicit legacy branch;
   missing historical lineage is unavailable, never invented. A named v1
   projection permits full comparisons against all unchanged golden bytes.
6. Published roots reach the actual recorded source and derived support.
   Blocked roots carry only actual recorded dispositions and justified edges;
   unavailable/sparse detail stays explicit. Readers gain a complete saved
   graph and reuse navigation; they must resolve references instead of treating
   each subtree as a self-contained copy. The saved browser supports both
   versions and visible, bounded navigation without materializing every path.
7. Preserve line values, pins, producers, citation sites, specialized account
   meaning and every legacy presentation golden byte. Update tests to assert
   the new graph independently and compare the explicitly projected legacy
   view to its frozen fixture. Memoize repeated source-leaf work where needed
   to prevent the existing flattened-site path from re-expanding shared inputs.
8. New schemas have resolved synthetic positive instances and additive manifest
   entries. The implementation measures actual node/edge/byte results on the
   same P0 v58 cases, and tests linear construction/storage with layered
   diamonds. Storage and runtime improvements are reported separately.

## Execution record

- P0 inventoried 36 original v1 presentation goldens and nine examples. They
  save roots and flattened citations rather than recursive trees. The linked
  census and real v58 replays provide the reproducible comparison.
- Track 1 delivers one graph across explanation, NPE, CLI and saved recovery,
  strict loading, lazy browser traversal and explicit legacy adapters. Every
  reachable recorded pin, producer, role and version remains available.
  All 47 historical presentation files, including merged withholding goldens,
  and every prior schema byte remain unchanged. Three additive derivation
  schemas follow recorded intent; no tax content is published.
- The reproduced line 27a graphs occupy 153,718 and 155,272 compact bytes
  versus 1,594,462 and 1,607,412 expanded-tree bytes. Complete saved files
  grow to about 1.06 MB because they newly retain full lineage. No runtime
  improvement is inferred from these measurements.
- Before-fix provenance controls exposed wrong-kind target substitutions and
  fabricated bare-reference payloads. Graph validation, actual saved loading,
  and published/blocked browser traversal now refuse those mutations while
  retaining legitimate unknown references and same-ID kinds.
- The bounded browser unit below preserves ordinary/recovery assertions while
  reducing repeated launches and coordinating startup. Its focused integrated
  checks passed, including the subsequent diagnostic-transport controls;
  repository mypy passed 432 source files. The
  original derivation implementation also received complete local-suite and
  mypy verification. Captured outputs remain in ignored local evidence.
- Upstream withholding, Form 1099-K, test-cost, package-generator and retired
  phase-state work are preserved. Withholding's 29 tests use the explicit
  legacy adapters; its two golden files are unchanged. Excluded substrate
  files are identical to the ratified line.
- Independent final review and required exact-head verify on PR #229 are the
  publication gates. Historical CI evidence does not substitute for that
  candidate's check. The owner holds the merge.

## Final publication review

### Context Capsule

- Role: Reviewer. Source HEAD at launch; the launch brief supplies its resolved
  commit and the exact `origin/main..HEAD` range. Milestone explanation-sharing,
  primary branch milestone/explanation-sharing-2025; use only its primary tree.
- Orient with `--role reviewer --charter
  "docs/phases/engineering-health/milestones/explanation-sharing.md#Final publication review"`.
  Assigned object: the final curated range, read only. No implementation edits,
  full-suite repetition, push or PR mutation.
- Deep reads: AGENTS.md, Reviewer seat, concurrent-work protocol, qualitative
  review standard, this plan, its evidence and changed sources. ADRs 0020,
  0046 and 0055 apply only at their actual contract boundaries. Do not read
  governance or the purpose-and-governance proposal.
- Ceiling: evidence of this completed representation and bounded test-resource
  behavior; no product-design round. Stop for governance interpretation,
  excluded-path edits, published-history mutation or new product behavior.

Verify complete pin/producer/role/version preservation, root authorization,
run isolation, NPE selection, cycle/dangling refusal, direct graph construction,
saved-source/reuse navigation and explicit legacy boundaries. Reuse earlier
independent checks where implementation bytes are unchanged.

For browser resources, trace actual caller reuse into distinct contexts,
same-origin storage isolation, success/error/timeout/killed borrower cleanup,
worker/owner/browser failure, fresh recovery/lifecycle selection and lazy
ownership. Distinguish fake ready-handshake process-ownership controls from
real Chrome scenario/storage evidence. Verify allowlisted startup diagnostics
through the Node/Python boundary and unchanged opt-in grace behavior. Check separate-process startup exclusion, Python/Node interoperability,
bounded queue/active timing and uncertain-owner refusal without stealing.
Inspect direct CLI entrypoints and their conservative rendering serialization;
ready-browser work must still overlap. No original scenario assertion, skip,
flags, active allowance, shard coverage or verify gate may be weakened.

Check unchanged golden bytes, additive schema history and current intent,
synthetic data, complete consumer coverage, durable commit units, removal of
working charters, closed routing and honest measurement limits. Excluded
parallel-work files must match main. Report falsifiable findings, successful
checks and a semantic verdict separately from exact-head CI. Run a focused
reproduction only to confirm a concrete failing claim; do not duplicate a full
suite. Return material repairs to the owning track and review their final
surface again.

## Bounded Chrome readiness investigation

The [startup investigation](explanation-sharing-evidence/chrome-startup.md)
retains original launch flags, the ten-second active allowance and failure
outcomes. Opt-in observations distinguish late readiness, exit and continued
non-readiness, including a bounded diagnostic grace period. Safe process/file
samples and post-shard probes provide evidence without replaying a scenario.
The full instrumented run passed, with two delayed starts observed at 5.21 and
7.39 seconds. Neither crossed ten seconds. Disk-wait samples support an I/O
hypothesis but do not establish the historical failure's cause; runner images
also differed. No timeout/flag remedy or elimination of intermittency is
claimed. Retain the observer for a naturally occurring failure.

## Bounded test browser reuse and startup limiting

Ordinary correction scenarios reuse one lazy browser per pytest worker with a
new isolated context per invocation. The explicit reused cases are confirmed,
indistinguishable, stale-financing, withdrawn, shared, duplicate-labels, unblock
and d1-visible. Every resumption case and the unconfirmed,
dropped-not-calculated, unknown-token, refresh-calculated, retry and historical
correction cases retain fresh browsers, as do lifecycle controls. No failed
scenario is replayed.

A session-scoped startup slot shared across workers is held until readiness
or failed-launch cleanup. Queue waiting is bounded separately and excluded
from active startup timing. An abandoned slot is not stolen: uncertain startup
ownership fails within the queue bound. Ordinary ready-browser work can
continue independently. Contexts are disposed on success, error and borrower
disconnection. Python owns the worker browser process group and private profile
root; normal worker teardown closes it. A deterministic ready-handshake fake
child exercises hard-owner process/profile cleanup through the actual helpers;
real Chrome controls establish isolated contexts and application behavior.
This is not crash recovery across a host shutdown. Startup failures cross the
Node/Python boundary as allowlisted outcomes, codes and numeric measurements;
unknown causes remain unknown. Diagnostics never silently replay a failure.
The extended observation grace remains opt-in; ordinary startup keeps the
original active allowance and cleanup timing.

Direct Chromium commands in saved graph, line 21 explanation/reasons and
worksheet tests join the same slot. Without a separate readiness handshake,
they hold it until the short command completes, conservatively serializing
that rendering. Model generation remains outside it. The real viewing-vehicle
test releases on its existing launch/readiness return; its product implementation
is unchanged. Standalone callers remain fresh, and non-browser workers launch
nothing eagerly. No new dependency, Chrome flag or active allowance is added.

[Resource evidence](explanation-sharing-evidence/browser-resources.md) records
actual launch counts, same-origin isolation, cleanup, cross-process and
cross-language controls and their limits. Two real scenarios launched two
fresh browsers versus one reused browser. Sampled timing is confounded by warm
caches and load; it is not a suite speedup measurement or a historical-cause
finding. Focused checks and mypy passed; final publication uses the unchanged
required CI gate after fetching and synchronizing with main.
