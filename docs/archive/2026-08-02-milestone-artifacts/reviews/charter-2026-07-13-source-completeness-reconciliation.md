# Charter: Source Completeness And Interest Slice — Post-Merge Reconciliation Review

Date: 2026-07-13. Commissioned by the owner; drafted by the principal foreman. Precedents: `2026-07-10-workspace-kernel-tracks-4-7.md` → `patch-kernel-reconciliation`; `2026-07-11-derivation-cascade-reconciliation.md` → merge `18ce073`.

- **Seat:** reconciliation reviewer, High tier, owner-launched external context, fresh reading.
- **Subject:** the Source Completeness And Interest Slice milestone as merged to `main` (`382a7af`, 2026-07-12; tracks at `9797b66`, `e4a0e4d`, `41a9948`, `871ae60`, `7cab080`). The current branch's committed code contains this merge unchanged — review the working tree at `HEAD`; do not switch branches or check out `wip/`/`archive/` refs.
- **Posture:** all six tracks merged in a single session, and the crew that built them has since had separate governance-process defects found in its Track 0 work on the successor milestone. Verify claims against code and contracts; treat the milestone plan and retrospective as pointers to what was claimed, never as evidence that it holds.

## Scope — verify against the governance set (Constitution, Ontology, Engineering Constraints) and ADRs 0002–0017

1. **Kernel membership-routing boundary (known hole).** The retrospective records that the kernel does not police that member-predicate-matching fact assertions route through member-transition acts — a workspace-service-layer obligation on the honor system. Establish the actual blast radius: what breaks, and which articles are violated, if a fact matching a closed family's member predicate is asserted directly? Does a stale closure-backed zero survive current state when it shouldn't? Is no-resurrection intact under this path?
2. **Atomic horizon transition.** Reproduce the milestone's own guarantees — prefix incremental/rebuild equality, atomic rejection, no-resurrection, isolation — and hunt edges the goldens do not cover (e.g. repeated or empty transitions, interleaved families).
3. **Closure-backed zero lifecycle.** Attestation → published zero → late member arrives → old zero leaves current state without manual withdrawal; re-attestation plus explicit rerun publishes the successor; removal cannot resurrect.
4. **Two-runner parity scope.** What byte-parity actually covers, and what it silently does not (dispositions, coverage read model, blocked states).
5. **Coverage read model.** The claim is that coverage shares the runner's own admission resolution "so coverage and calculation cannot disagree." Verify the sharing is structural, not parallel logic.
6. **Schema registry immutability and adopted-mapping single dispatch** (`RunContext.closed_sets` removal — confirm nothing reintroduces a second dispatch path).
7. **Data safety.** Scan committed milestone content for private paths, real-looking account/identifier digit runs, and non-synthetic amounts.

## Method and boundaries

- Read-only with respect to the repository: your **only** repository write is the review file below. No schema, code, content, or process-document changes; no git write commands; no branch switches.
- You may execute: the full test suite and governance lint via the project `.venv` (`.venv/bin/python -m unittest`, `.venv/bin/python tools/governance_lint.py`), and throwaway probe scripts **in a scratch directory outside the repository** that import the committed packages. Report any verification claim from the retrospective you could not reproduce.
- Independence: do not read `docs/prototypes/` iteration or review material for the successor milestone; it is out of subject.

## Output

`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-13-source-completeness-reconciliation.md` — findings labeled SC-R1, SC-R2, …, each with: the defect, cited articles/ADRs, concrete reproduction (input state → observed → expected), and severity (**patch-candidate** — merged behavior violates a contract or governance article; **production condition** — must be addressed before a dependent feature lands; **non-blocking** — recorded, no action forced). End with a verdict: whether a reconciliation patch branch is warranted, and if so the minimal finding set it must close. Advisory: the owner decides disposition.

## Stop conditions

Stop at the single review file. If a probe suggests a fix, record the finding and the probe — do not implement the fix.
