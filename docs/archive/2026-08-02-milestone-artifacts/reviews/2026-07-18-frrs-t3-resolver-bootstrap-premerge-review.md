# First Real Return Slice — Track 3 (Production Resolver & Live Workspace Bootstrap) — Pre-Merge Review

Reviewer: owner-authorized, author-independent pre-merge reviewer (did **not**
implement Track 3). Date: 2026-07-18. Branch: `track/frrs-t3-resolver-bootstrap`
(PR #13). Delta reviewed: **`b8c90f7` → `66a3497`** (the single implementer
commit; 1,391 insertions across 15 files). Docs tip `f2311fc` is process state
only and is not treated as an implementation claim. Charters:
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-18-frrs-t3-resolver-bootstrap-premerge-review.md`
(this seat) and
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-18-frrs-t3-resolver-bootstrap.md` (implementation).
Contracts: **ADR-0033** (primary), **ADR-0031** (live residency bootstrap /
installed gates), **ADR-0032 F1** (raw evaluator closed as a live path; T2
pre-merge F1 carry). Advisory — the owner decides disposition. This review does
not redesign ratified contracts, does not merge, and does not modify
implementation source, tests, fixtures, ADRs, or schemas.

## Verdict

**Not merge-ready. One blocking finding (F1).** Deliverables 1–7 are largely
present and the focused/full suites, mypy, governance lint, and data-safety scan
are green, but the release-surface inventory in
`production_resolver._verify_release_and_registry` raises uncaught
`SchemaValidationError` when a co-located document shares the adoption-pinned
release identity yet fails schema validation. That converts an otherwise clean
resolve into an exception — violating the track’s own “typed refusals, not
exceptions-as-control-flow” rule and the ADR-0033 / module posture that
co-located junk must not become authority **or** crash the authority walk.
Remaining findings are production conditions for Track 4 and non-blocking
residuals (including a forgeable marshalling token residual on F1 evaluator
closure).

## Evidence (re-run by this reviewer on this branch)

Prefer system `/usr/bin/python3` for unittest (foreman note: `.venv` may be
stale; on this host `.venv/bin/python3` is a symlink to system Python 3.11.2).
Mypy is provided by the project venv.

- `python3 -m unittest tests.test_frrs_t3_resolver_bootstrap -v` → **30 tests OK**
  (4.6s). All named kill/golden classes execute: adoption currency (including
  tie / non-user / supersession / wrong scope / future commit / non-advancing
  supersession / conflicting act id), three release/registry/member
  substitutions, exclusive member graph (unpinned inert, same-key impostor,
  package pin mismatch), hard-gate core refusal with eight contained issues, F1
  probes, live-workspace bootstrap + gates, provenance regeneration.
- `python3 -m unittest` (full suite) → **403 tests OK** (64.5s). Matches
  phase-state / handoff claim.
- `.venv/bin/python3 -m mypy packages tools tests` → **Success: no issues found
  in 86 source files**. (Bare `python3 -m mypy` fails: system site-packages has
  no mypy; project venv is required.)
- `python3 tools/governance_lint.py` → **conformant**.
- Data-safety: `git diff b8c90f7..66a3497` scanned for personal/path markers
  (`/Users/`, `/home/…`, `/private/`, `local-data/`, `uploads/`,
  `generated/user/`, SSN-like patterns). The only hit is the Track-3 test’s
  *own* forbidden-token tuple. Fixtures under
  `packages/sample_data/frrs_t3/` use `demo.*` / `tax.us.2025.*` /
  `demo.user.filer-1` / synthetic act ids only; generator
  `tools/generate_frrs_t3_fixtures.py` pins committed public registry bytes and
  does not read personal data. No absolute local machine paths in committed
  Track-3 fixtures.
- Scope fence on names: delta touches only derivation runtime modules, the
  Track-3 synthetic corpus + generator, and the Track-3 test. **No**
  `docs/adr/*` or `packages/schemas/*` edits in `b8c90f7..66a3497`.
- **Independent structural probes (not trusting test names alone):**
  - `inspect.signature(live_run)`: no `inputs` / `sources` / `raw_inputs` /
    `scenario` / `VAR_KEYWORD`; `live_entrypoint_accepts_raw_inputs()` is
    `False`.
  - `live.py` runtime path is `marshal_live_run_context` →
    `execute_marshaled`; it does not call `runner.run`.
  - `execute_marshaled(RunContext(...))` raises `TypeError` (type fence).
  - **Counter-probe:** `MarshalledRunContext(hand_assembled_RunContext_with_InputFinding)`
    is accepted by `execute_marshaled` — forge succeeds (see F2).
  - **Blocking counter-probe:** co-located schema-invalid release sharing
    `id`/`version` with the honest release causes
    `SchemaValidationError` instead of `ResolvedGraph` or `Refusal` (see F1).
  - Clean interest-slice adoption resolves to `ResolvedGraph` with 19 members;
    unrepaired core adoption refuses `HARD_GATE_REFUSED` with exactly the eight
    RG-1 codes (4×`MEMBER_UNREACHABLE`, 2×`MAPPING_FACT_TYPE_NOT_ADMITTED`,
    1×`SCHEMA_NOT_ADMITTED`, 1×`ROLE_MISMATCH`); no `resolved_members` on
    `Refusal`.
  - Release pin checksum matches committed release bytes; release attests the
    committed `published-packages.json` SHA-256.

## Deliverable-by-deliverable

1. **Release-rooted, current-user adoption resolver (ADR-0033 Decision 1) —
   faithful.** `select_current_adoption` / `resolve_production_package` consider
   only well-formed `act-package-adoption.v1` acts by `scope_user` in
   `run_scope` at `workspace_revision`; supersession is applied; unique max
   revision is required; zero candidates and ties refuse with typed reasons
   (`ADOPTION_NONE_CURRENT`, `ADOPTION_AMBIGUOUS`). Non-user automation never
   selects even at higher revision; wrong scope and future-committed acts refuse.
   Non-advancing supersession refuses rather than erasing current authority.
   Conflicting bodies for the same `act_id` refuse. No caller package id / path /
   catalog / fixture `adoption_pin` selects authority on this path. Executed
   goldens cover these cases.

2. **Verify release → registry → package/member (Decision 2) — mostly
   faithful; inventory exception hole (F1).** Authority chain loads release
   candidates from the publication surface by identity + adoption-pinned
   checksum (no id→path join), then checks registry bytes against
   `package_registry_sha256`, then verifies package instance against adoption pin
   + published registry, then member pins by registry-expected citizen
   checksums. Executed kill-tests: forged release
   (`RELEASE_ABSENT_OR_MISMATCH`); replaced registry under honest release
   (`REGISTRY_CHECKSUM_MISMATCH`); changed member bytes
   (`MEMBER_ABSENT_OR_MISMATCH`); changed package body
   (`PACKAGE_ABSENT_OR_MISMATCH`). **Gap:** co-located schema-invalid release
   documents that match pinned identity raise uncaught
   `SchemaValidationError` (F1) rather than being skipped or refused.

3. **Exclusive verified member graph or refuse (Decision 3) — faithful.**
   Member corpus admits only checksum-verified bodies for exact pins;
   byte-identical digests collapse via dict keying; unpinned co-located file is
   inert (PC1 golden); same-key impostor with different bytes is ignored (PC2 /
   same-key golden); clean interest-slice returns `ResolvedGraph` with
   `validation.ok == True`. Hard gate: unrepaired core package returns
   `Refusal("HARD_GATE_REFUSED", …)` with eight contained issues and no graph —
   no allowlist / clean subset. Filesystem order independence is implemented by
   digest matching + sorted inventory; the suite’s order test is weak (F4) but
   the mechanism is order-independent by construction.

4. **Live workspace bootstrap at D1 residency location — present; full
   ADR-0031 installed-hook surface not complete (F3).**
   `bootstrap_workspace(WorkspaceCapability, repo_root=…)` refuses in-repo
   locations, symlinks, `.git` inside `L`, capability flags that grant write /
   publication / network, and same-inode bridges; creates `L` outside the repo
   from capability only (no committed locator). Runtime boundary registry loads
   `classification.v1` (and sibling boundary citizens) — **Track-1 pre-merge F2
   discharged**. `classify` is total/fail-closed with description inheritance;
   `guard_commit` / `guard_push` refuse `NEVER_CROSSES`; `live_output_path`
   quarantines writes under `L`. Integrity-checked git hooks, guarded transport,
   and a structural requirement that the live entrypoint hold a workspace
   capability are **not** installed here (production condition → Track 4).

5. **Close raw evaluator as a live path (ADR-0032 F1 / T2 carry) —
   substantially advanced; residual forge channel (F2).** Production path:
   `live_run` → `marshal_live_run_context` → opaque `MarshalledRunContext` →
   `production_executor.execute_marshaled` → private `_execute`. `live.py` no
   longer imports `runner.run`. `execute_marshaled` rejects non-token types.
   Fixture adapter import fence is checked for production modules. Empty-state
   `live_run` yields no ghost findings. Residual: `MarshalledRunContext` is a
   public dataclass whose constructor accepts any hand-assembled `RunContext`
   (including `InputFinding`); `runner.run` remains public for fixtures.
   Accidental entrypoint route is closed; deliberate forge of the token is not.

6. **Named ADR-0027/0028 production conditions (D3 ledger) for Track 3 —
   discharged in mechanism + goldens; T4 carry is implicit (F5).**
   - PC1 unpinned-co-located → executed (`test_unpinned_co_located_file_is_inert`).
   - PC2 conflict / same-key → executed (`test_same_key_impostor_…`).
   - PC3 registry-verified package and members → executed (clean resolve +
     package/member substitution kills + `verify_published_package`).
   - RG-1 left unrepaired; hard gate refuses core with eight issues (correct
     Track-3 default).
   - PC(T4) ledger rows (role canon, form-field integrity, ADR-0028 surface,
     etc.) and first real run remain for Track 4; phase-state / handoff carry
     RG-1, W-2 closure, live-run integration, first real run, but there is no
     dedicated Track-3 closing note restating the full ADR-0033 §4 PC(T4) table.

7. **Synthetic kill/golden corpus — executed, not stubs.** 30 focused tests
   run real resolver / bootstrap / live_run code against synthetic
   `demo.*` fixtures regenerated from public pins
   (`test_fixture_corpus_regenerates_from_public_pins`). Coverage matches the
   charter list for release substitution, adoption currency, same-key, missing /
   mismatched pins (via absence and checksum mismatch), hard-gate refusal, and
   F1/D1 probes. Weak spots: order-independence golden (F4); no dedicated
   golden for the co-located invalid-release inventory case that exposes F1.

## Findings

### F1 — Co-located schema-invalid release documents crash resolution with an uncaught exception
**Classification: blocking.**  
**Where:** `packages/derivation/production_resolver.py:214-225`
(`_verify_release_and_registry`).  
**Description:** Release inventory validates candidates with
`schemas.validate(RELEASE_SCHEMA, candidate)` inside a `try` that catches only
`(OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError)`.
`SchemaValidationError` (from `packages.kernel.schema_registry`) subclasses
`Exception`, **not** `ValueError`. A co-located file that shares the pinned
release `id`/`version` but fails schema validation therefore aborts the whole
resolve with an exception instead of being skipped (as malformed member
candidates are) or returned as a typed `Refusal`. Independent reproduction:
place `aaa-junk.json` (same id/version, missing `package_registry_sha256`)
beside an honest release that matches the adoption pin → clean interest-slice
adoption raises `SchemaValidationError` instead of returning `ResolvedGraph`.
Control with only the honest file succeeds. This contradicts ADR-0033 Decision 2
surface hygiene, the module contract (“typed refusals, never
exceptions-as-control-flow”), and the Track-3 posture that co-located junk is
inert.  
**Suggestion:** Catch `SchemaValidationError` (or a broader validation base) in
that inventory loop and `continue`, matching the member-candidate inventory
pattern; add an executed golden that co-locates an identity-matching invalid
release with an honest release and expects `ResolvedGraph` (or a typed
refusal if product policy is “any identity collision refuses”). Do not
paper over by letting the exception authorize anything.

### F2 — `MarshalledRunContext` is a forgeable public token; `runner.run` remains a public fixture entrypoint
**Classification: non-blocking** (residual of T2 F1 / charter deliverable 5).  
**Where:** `packages/derivation/marshal.py:28-37`,
`packages/derivation/production_executor.py:10-19`,
`packages/derivation/runner.py:551-559`.  
**Description:** The live entrypoint path is correctly closed: no raw-input
parameter, marshaller-only construction from record state, production executor
type-fenced to `MarshalledRunContext`. But `MarshalledRunContext` is an ordinary
public dataclass; constructing
`MarshalledRunContext(RunContext(..., inputs=[InputFinding(...)]))` and calling
`execute_marshaled` succeeds — a hand-assembled ghost id reaches `_execute`.
`runner.run` remains public for fixture scenarios (documented). The suite’s F1
tests check signature names, fixture-adapter import absence, and empty-state
`live_run`; they do not probe token forgeability.  
**Suggestion (optional hardening, Track 4 if deferred):** make the token
unforgeable outside `marshal_live_run_context` (e.g. module-private subclass /
`__slots__` + sealed factory, or a capability object not constructible as a
public dataclass), and/or add a kill-test that forging the token is rejected.
Acceptable to leave `runner.run` as an explicitly fixture-facing API if
production modules never import it (already true for `live.py`).

### F3 — ADR-0031 “installed, integrity-checked hooks” and guarded transport are not yet product-installed
**Classification: production condition (Track 4).**  
**Where:** `packages/derivation/live_workspace.py` (library gates only; no hooks).  
**Description:** Track 3 correctly bootstraps `L` from a capability, audits
topology, loads boundary schemas into a runtime registry (discharges T1 F2), and
exposes total classification + commit/push envelope guards as callable methods
exercised outside pure schema tests. ADR-0031’s production-condition list also
names integrity-checked commit/push **hooks** a run entrypoint structurally
requires, and **guarded transport** so raw `git push` / `--no-verify` cannot
bypass the gate. Those are absent; `live_run` does not require a
`WorkspaceCapability` / `LiveWorkspace`. Appropriate residual before first real
data in Track 4 — record so it is not treated as fully discharged by Track 3.  
**Suggestion:** Track 4 installs hooks + guarded transport and wires the live
run path to a bootstrapped capability before personal artifacts enter `L`.

### F4 — Filesystem-order independence golden does not vary layout
**Classification: non-blocking.**  
**Where:** `tests/test_frrs_t3_resolver_bootstrap.py:279-286`.  
**Description:** The test runs the same clean resolve twice and compares member
id sets. Implementation is order-independent (sorted paths + digest admission),
but the golden does not shuffle filenames, directory nesting, or candidate order
to falsify order dependence.  
**Suggestion:** Co-locate a second verified-or-impostor body under a path that
sorts before/after the real member and assert identical admission (the same-key
impostor test already covers the hard case partially).

### F5 — No dedicated Track-3 closing note restating the full ADR-0033 §4 PC(T4) carry list
**Classification: non-blocking.**  
**Where:** process docs (`docs/phase-state.md` / `docs/foreman-handoff.md` on
`f2311fc`); implementer commit has no closing note file.  
**Description:** Deliverable 6 asks to discharge T3 ledger items and
**explicitly** carry `PC(T4)` items in a closing note. Phase-state carries RG-1,
W-2 closure mapping, live-run integration, and first real run to Track 4, but
does not restate the full ADR-0033 §4 table (role canon, form-field integrity,
ADR-0028 fact/composition surface, reject-direction goldens, etc.). Mechanism
discharge of PC1–PC3 for T3 is real (see deliverable 6).  
**Suggestion:** On merge or Track-4 plan open, list the ADR-0033 §4 `PC(T4)` rows
explicitly once so none are lost.

### F6 — Member-byte substitution golden allows `HARD_GATE_REFUSED` as an alternate success
**Classification: non-blocking.**  
**Where:** `tests/test_frrs_t3_resolver_bootstrap.py:213`.  
**Description:** After tampering a `rule.*.json` body, the assertion accepts
`MEMBER_ABSENT_OR_MISMATCH` **or** `HARD_GATE_REFUSED`. Independent probe of a
pinned member body yields `MEMBER_ABSENT_OR_MISMATCH` (correct). Allowing
`HARD_GATE_REFUSED` would also pass if a tampered body were wrongly admitted and
failed later validation — masking a Decision-2 failure as a Decision-3 hard-gate
refusal.  
**Suggestion:** Assert the precise reason
`MEMBER_ABSENT_OR_MISMATCH` (or `PACKAGE_*` for package tamper) for substitution
kills.

### F7 — Resolver, workspace bootstrap, and `live_run` are not yet a single production pipeline
**Classification: production condition (Track 4)** — in charter scope for T3 as
machinery pieces, not first real run.  
**Where:** `live.py` has no call to `resolve_production_package` or
`bootstrap_workspace`; `live_run` still takes an `adoption_pin` parameter for
evaluator pin audit (pre-existing T2 shape), which is **not** used as package
authority by the new resolver.  
**Description:** Track 3 correctly stands up the three machines on synthetic
fixtures. Wiring “current adoption → resolved exclusive graph → marshalled live
run inside bootstrapped `L`” is the first-real-run / smoke surface owned by Track
4 per the implementation charter. Not a scope defect.  
**Suggestion:** Track 4 integration should pass resolved member graph + record
state into `live_run` and never accept a caller-selected package path as
authority.

## Scope fence — clean

The implementer delta is confined to:

- `packages/derivation/production_resolver.py` (new)
- `packages/derivation/live_workspace.py` (new)
- `packages/derivation/production_executor.py` (new)
- `packages/derivation/live.py`, `marshal.py`, `runner.py` (F1 fence / token)
- `packages/sample_data/frrs_t3/**` (synthetic release + adoption acts)
- `tools/generate_frrs_t3_fixtures.py`
- `tests/test_frrs_t3_resolver_bootstrap.py`

No RG-1 core-package content repair; no real personal data; no W-2 closure
mapping; no live-run smoke harness / first real run; no OCR/UI; no edits to
ratified ADRs or Track-1 schema citizens. Docs tip `f2311fc` only updates
phase-state / foreman-handoff process pointers.

## Process honesty

Claims in `docs/phase-state.md` and `docs/foreman-handoff.md` (on `f2311fc`) that
Track 3 is implemented at `66a3497`, that focused suite is 30 green / full suite
403 green / mypy clean (86 files) / governance lint conformant, and that the next
step is author-independent pre-merge review under owner authorization, match what
this reviewer re-ran and the branch tip. The “no review seat has been dispatched”
line was accurate at docs-tip time; this review is the owner-authorized seat that
line anticipated. No overclaim that RG-1 is repaired or that the first real run
has landed.

## Recommendation

**Hold the merge until F1 is fixed and re-verified** (catch schema-validation
failures in the release inventory; add the co-located invalid-release golden;
re-run focused + full suite / mypy / governance lint). F2 is a non-blocking F1
residual; F3 and F7 are expected Track-4 production conditions; F4–F6 are
non-blocking hygiene. Owner-held merge (ADR-0030) after repair + optional
delta-only re-check. This reviewer does **not** merge, push, or open GitHub
review API objects.
