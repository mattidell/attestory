# D2 Examination — Iteration 2 (Clean-Room Rival)

Builder: clean-room rival, High tier. Date: 2026-07-16. Design under
examination: `it2/design.md`. Evidence ceiling: Rung 2 (paper schema diffs +
throwaway synthetic probes against committed machinery at `HEAD` and scratch
out-of-repo workspaces). Seal held: no incumbent material read.

## Probe provenance

Throwaway script `probe_d2_it2.py` (session scratchpad, outside the repo;
not committed). Scratch workspaces under the scratchpad stood in for the
ADR-0031 live workspace. 15/15 checks passed. All values synthetic
(41000 / 230 / 42000; `demo-*` identifiers). `git status` after probing:
repository unchanged. Probes exercised only committed code read-only;
the contribution layer itself exists solely as paper diffs in the design.

## D2-P1 — contribution event, provenance linkage, runs-consume-facts

**Verdict: settled at Rung 2.**

- **Event schema (Article 10).** Paper diffs complete and minimal:
  `contribution.v1` (thin anchor citizen), `act-contribution.v1` (payload,
  mirroring `evidence-submitted`), `finding.v2` (optional `contribution_id`),
  `contribution-record.v1` (Article 14 session account). No committed schema
  is mutated; all changes are new published versions. Register additions
  named. Nothing central remains a placeholder.
- **Provenance linkage (Article 12).** Chain finding → contribution →
  evidence → admitting act; document "version" is the immutable evidence id
  (replacement mints a successor id). Consistency enforced at admission
  (contribution's `evidence_id` must appear in the finding's
  `evidence_ids`). Deliberately **not** a standing edge: contributions are
  unsupersedable, so no displacement can originate at one and the two-edge
  doctrine (ADR-0010/0017) holds without exception.
- **Case 1 (contribution produces provenance-bearing facts).** Probed at the
  committed layer: evidence + member-transition admitted `demo-f-w2-a1`
  (41000) with evidence pin and horizon successor; the paper layer adds the
  contribution pin. Positive trace shown in design §4.1.
- **Case 2 (runs consume facts — mandatory kill-test). Passed structurally
  and behaviorally.** `RunContext` has no representable raw-input slot
  (`TypeError` probed); `InputFinding` requires a `finding_id` (`TypeError`
  probed); a value present only as raw content while its finding is withheld
  blocks `DEPENDENCY_ABSENT` with zero publications and a recorded
  disposition; with the finding present, every input/choice pin on the
  published derived finding resolves to a real finding id.
- **Case 6 (run reaching a raw input — mandatory kill-test). Passed.** The
  three probes above show the failure is a type rejection or a loud recorded
  block, never a silent read; no code path exists from the run context to
  evidence content or contribution payloads. The E14.2 extension closes the
  declaration side (a rule cannot name a contribution as a dependency).
- **Case 5 (contribution stays in quarantine — D1 kill-test). Passed at
  Rung 2.** The appender receives `L` only as runtime capability
  (ADR-0031 Decision 1); contribution artifacts carry personal provenance →
  `NEVER_CROSSES` (Decisions 2/7); repo mounted read-only in a live run.
  Probed: the residency relation predicate accepts the scratch `L` and
  rejects a repo-internal path; the repository tree was unchanged
  throughout. Full enforcement (installed gates, guarded transport) is
  ADR-0031's named production surface, consumed not re-proven.

Residuals (named, non-blocking, design §5): fold-before-append appender
obligation (probe observation: `ActLog.append` checks schema/revision only;
semantic admission fires at projection); marshal-only `RunContext`
construction to be made structural in D3; E14.2 static-check extension and
contribution-record registration in Track 2.

## D2-P2 — manual entry as any-order event; correction by supersession

**Verdict: settled at Rung 2.**

- **Anti-wizard / any order (case 3 — mandatory). Passed.** Two scratch
  workspaces, synthetic W-2 and 1099-INT batches applied in opposite orders:
  full read models (current findings, facts, histories, horizons, open
  facts) equal as values. Commutativity is structural — independent
  contributions touch disjoint facts and disjoint horizon chains, and
  currency derives from the record, not arrival order. The only intra-batch
  ordering is reference integrity (contribution/evidence recorded before a
  finding pins them), the same class as the committed evidence rule — not a
  sequence, and no act consults another family's state. A forced entry
  order is unrepresentable in this design.
- **Correction by supersession (case 4). Passed.** A corrected value is a
  new contribution producing a plain assertion of the same fact (ADR-0023
  routing). Probed: currency moved to `demo-f-w2-a1-corr` (42000); the prior
  finding retained non-current with original provenance; both contributions'
  acts on the record; the family horizon did **not** advance, so closure
  authority survives a value correction. No edit, no manual withdrawal, no
  third mechanism.
- **ADR-0023 boundary kill-probes (supporting cases 3/4). Passed as folds.**
  A new member via plain assertion rejects (`FindingModelError`, SC-R1); a
  same-member correction via member-transition rejects (SC-R2). Member
  removal remains the committed member-transition remove.

## Foreclosure-clause conformance

Anti-wizard: no expressible sequence (above). Runs consume facts: cases 2/6.
Schema-as-canon: every new noun has a paper schema before any instance;
no committed schema version is edited. No Tier-3 escalation needed.

## What Rung 2 does not establish

The live appender, gates, and resolver as installed (milestone Tracks 1–3);
multi-party/consent contribution, OCR/import modes, and UI (deferred by the
plan); the marshal-only constructor made structural (D3). None of these gaps
touches the decision surface: the event shape, the provenance linkage, the
structural invariant, the any-order property, and correction-by-supersession
are established on the committed contracts plus minimal additive paper diffs.

**Overall: D2-P1 settled at Rung 2; D2-P2 settled at Rung 2.** All six
Gate-2 cases resolved; mandatory cases 2, 3, 6 passed as kill-tests.
