# Review: Workspace Kernel Tracks 4–7 (Resumed Work)

- Date: 2026-07-10
- Reviewer: seeding agent (authored governance installation, kernel plan, and Tracks 1–3)
- Scope: commits `37c3d57` (Track 4), `659c643` (Track 5), `d45b49c` (Track 6), `906bd21` (Track 7), merge `c8799ce`, retrospective/status `f11c2ce`
- Status: advisory. The owner decides whether to act, ignore, or snapshot-and-reset.
- Verification observed at review time: `python3 -m unittest` 88 tests OK; `tools/governance_lint.py` conformant; mypy strict clean (30 files); fixture runner reproduces goldens.

## Verdict

**Keep.** The resumed work is faithful to the milestone plan's intent and to the seeded contracts — my uncommitted Track 4 schema drafts were adopted nearly verbatim, and the fold/projection architecture from Tracks 1–3 was extended rather than reinvented. The findings below are additive fixes, none structural; nothing here warrants a reset. Findings 1–3 should be addressed **before or at the start of Derivation Machinery**, because that milestone builds directly on the affected seams.

## Strengths

- **Contract continuity.** Track 4 schemas match the seeded drafts (only cosmetic description edits). The two-step validation pattern (shallow act payload schema, then `validate_declared` on nested citizens) was preserved consistently.
- **E1.1's behavioral half is exactly right.** Findings compare byte-equal across evidence replacement and withdrawal; evidentiary standing is a derived view (`evidentiary_standing`), never state. This is the article's core claim, proven the correct way.
- **Honest boundary on derived findings.** Assertion acts reject `pins` outright ("derived finding pins are not admitted in the kernel yet"), keeping the T1 reserved entry unresolved instead of quietly improvised. Documented as a Tier 1 decision in the retrospective.
- **Semantic validation happens in the fold, before append** — a workspace cannot commit semantically inadmissible acts (unknown facts, non-current evidence, value-schema violations, duplicate findings).
- **The retrospective is candid** about the interrupted-state mess: the continuation branch, the manifest hash patching, the environment drift (`python3` vs `.venv`). This is the disclosure discipline the owner posture wants.
- **Deterministic read models** (sorted keys, stable JSON) made the containment drill and goldens trivial — carried directly from the milestone plan's lessons.

## Findings

Ranked by how much they matter to what comes next.

### 1. Individuation-edge displacement is not drivable from the record

There is no `act-entity-superseded.v1`. The only way to displace along an individuation edge is `compute_currency(root_displacements=..., extra_edges=...)` — parameters that let **any caller** inject displacement roots and edges from outside the record. E7.2's conformance test passes by injecting the very edges it checks.

Two problems. First, the milestone plan's Track 5 scope ("eager displacement along individuation edges"; the plan's act list includes entity supersession) is satisfied only by synthetic stand-ins, so the cascade has never run from an act. Second, and worse as a shape: Article 7 says displacement is "a consequence of the record, not a fan-out of writes" — a production API where displacement roots are caller-supplied is a violation-shaped affordance sitting exactly where Derivation Machinery will integrate. It is read-only today, so nothing is corrupted, but the next consumer will reach for it.

**Recommendation:** add `act-entity-superseded.v1` (small, symmetrical with evidence replacement), drive the E7.2 and fact-displacement tests from committed acts, and move `root_displacements`/`extra_edges` out of the public signature into a test-support helper.

### 2. Basis/nature coherence is unenforced (Article 3 adjacency)

Verified by probe: an `elective`-basis finding is accepted on a **determinable** fact, and an `attested`-basis finding is accepted on an **elective** fact. The Ontology is explicit that elective answers are *constituted by choice*; the fact type's declared nature and the finding's basis are currently independent free choices.

This will bite in Derivation Machinery: E3.1 (no operative defaults) requires elective facts to block derivation until closed by a choice — if an elective fact can be "closed" by an attested finding, the E3.1 detection has a hole exactly where it matters.

**Recommendation:** enforce the biconditional in `_validate_finding`: `fact.nature == "elective"` ⇔ `finding.basis == "elective"`.

### 3. `supersession.policy` is declaration theater

`fact-type.v1` requires a `supersession.policy` declaration, and nothing anywhere reads it. A declared rule that no machinery consults is the inversion of Legibility's complaint — vocabulary that looks load-bearing and is not. With only `"free"` published this is behaviorally invisible, which is exactly why it should be fixed cheaply now: either consult it (assert `policy == "free"` at correction time, so the seam exists and is exercised) or annotate the schema description that enforcement arrives with restricted policies.

### 4. E7.1's materialization check exercises the mechanism, not a store

`assert_materialization_matches` diffs a caller-supplied dict. No production materialization exists yet, so this is acceptable — but when a projection cache lands (read-model files already have `write_projection`), the E7.1 drill must target the real artifact, not a toy mapping. Note for the conformance README's future-work list.

### 5. Minor

- `inspect_workspace.main()` duplicates the `inspect_workspace()` helper instead of calling it (registry/log construction repeated).
- Evidence currency classification is computed independently in `findings._current_evidence` and again in `currency.compute_currency` — drift risk when evidence lifecycle gains states.
- Fixture findings carry `capture` with `presented == asserted` although nothing proposed the claims and no consultation exists to reference. Capture exists to preserve *what was shown*; using it decoratively in fixtures dilutes the vocabulary. Drop it from fixture findings that model direct manual entry.
- Branch hygiene: `milestone-workspace-kernel` (parked at Track 3) and `milestone-workspace-kernel-track4` are both reachable from `main` and deletable under the new posture rules.

## Alignment notes

- The work respects the governance set where it counts: no second store, no tolerant readers, no stored currency, immutable schemas, synthetic-only fixtures with a path-marker safety test.
- The deviations disclosed in the retrospective were handled correctly (continuation branch preserved per-track commits; the manifest immutability check caught the premature hash).
- The E8.1 N/A rationale in `tests/conformance/README.md` is properly scoped as milestone-local, not permanent.
