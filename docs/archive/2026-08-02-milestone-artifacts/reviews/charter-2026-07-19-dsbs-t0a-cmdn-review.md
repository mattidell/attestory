# Charter: Track 0a — ADR-0037 Conditional Multi-Dependency Substrate — Author-Independent Pre-Merge Review

Date: 2026-07-19. Prepared by the foreman; **the owner dispatches this seat**
(ADR-0034). The reviewer is author-independent: it reads this charter, the
Track 0a plan (milestone plan `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/
dividends-schedule-b-slice.md`, "Track 0a"), ADR-0037 with its CMDN prototype
evidence, and the branch `codex/dsbs-t0a-cmdn-production` — not the authoring
session.

## Object under review

The delta `main..codex/dsbs-t0a-cmdn-production` (one commit, `c0508cb`):
`rule-artifact.v3` / `artifact-package.v3` schema citizens with positive and
negative corpus, the shared-evaluator `conditional_dependency_set` node,
package-validation admission for v3 (including nested-ref reachability),
runner/record/NPE threading, the synthetic coordinator test family, and the
tracking-docs advance.

## Falsifiable checks

1. **Plan fidelity.** Each of the plan's four output stages is present and
   complete: (a) v3 schemas with a fully resolved synthetic positive (Payload
   Instantiation Gate — every required field named concretely) and the named
   negatives (empty members, non-`ref` member, malformed shapes); (b) the node
   in the *shared* evaluator, admitted by **both** runners through the
   ordinary schema/validation path — no runner-private rule identifier, no
   tax/form branch; (c) blocked disposition, durable record, and NPE walk
   carrying **all and only** absent active members in declared member order,
   with record/NPE schema versions retained (any version bump must be a
   separately explained migration — verify none was smuggled); (d) a
   coordinator-from-facts fixture family whose goldens enter through
   `live_coordinate_run` from an authoritative act log, covering the six CMDN
   paper cases (inactive/no members; active/all present; active/two absent;
   active/one absent; contribution and member-supersession lifecycle;
   no-reach-around mutation).
2. **ADR-0037 conformance.** The shipped contract matches the ratified ADR:
   one declared condition expression; non-empty ordered `members` of `ref`
   expressions only; a false condition succeeds without reading, naming,
   access-logging, or pinning any member; a true condition evaluates every
   member exactly once, accumulates only dependency-absence, and propagates
   every non-absence failure unchanged. Confirm the evaluator loop cannot
   double-count or reorder members and that inactive isolation is asserted by
   test, not merely by inspection.
3. **Pin integrity (targeted).** `runner.py` now skips pinning an accessed
   ref with no `symbol_pin` entry (absence has no finding identity). Verify
   this skip can never drop a pin for a **present** member or any other
   present ref on the published path — i.e., establish there is no reachable
   state where a symbol was read, holds a current finding, and is absent from
   `symbol_pin`. Published results must pin the evaluated condition and every
   active present member through the existing access-log and derivation
   edges; the mutation tests must actually reject an omitted active-member
   pin.
4. **Admission and reachability.** `artifact-package.v3` admission is
   mechanical (v3 alongside v1/v2, no semantic fork); the new
   `_iter_ref_names` reachability walk cannot mark a genuinely unreachable
   member reachable, and existing v1/v2 exclusive-member-graph behavior is
   unchanged (no regenerated golden without a demonstrated contract cause).
5. **Scope fence.** The delta contains no QDCG worksheet, declared-absence
   fact type, dividend or Schedule B content, tax-specific missing-list path,
   UI aggregation, or third currency edge; it does not reopen D1/D3 or alter
   existing v1/v2 citizens' semantics. Docs changes are tracking-record
   advances only, and every factual claim in them matches git and the branch.
6. **Boundary and data safety.** Every fixture, identifier, and golden is
   manufactured `demo-*` data; no workspace path, real-run detail, value,
   disposition, or refusal text appears anywhere in the delta. Run the
   per-review safety scan over the new fixtures and goldens.
7. **Verification battery (re-run, not trusted).** On the branch:
   `.venv/bin/python3 -m unittest`, `.venv/bin/python3 -m mypy`,
   `.venv/bin/python3 tools/governance_lint.py`, and
   `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` — all green.
   The authoritative-surface golden class is mandatory evidence; a green unit
   suite without it is insufficient. Primary/reference runner byte equality
   must be covered by an executed test.

## Verdict

Write `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-19-dsbs-t0a-cmdn-review.md` on the branch with an
explicit `ready` / `not ready` verdict and findings numbered F1…, each tied
to a check above with file/line evidence. The foreman triages findings; the
owner holds the merge (ADR-0030). Merge of this track is the gate for D2
adoption; the reviewer does not evaluate D2 itself.
