# Review Round 0 — Adversary Delta Confirmation

Reviewer: Codex resume session, 2026-07-10.

Artifact under review: `docs/archive/2026-08-02-milestone-artifacts/prototypes/rule-language/charter-it1.md` v2.
Scope: bounded delta-confirmation only. This review compares charter v2 against the seven required amendments in `round-0-adversary.md`; it does not introduce new attacks.

## Delta results

### 1. Schedule B triggers beyond taxable-interest threshold

Status: confirmed closed.

Charter v2 splits the original Schedule B threshold fixture into F3a (amount-triggered applicability) and F3b (foreign-account Part III applicability regardless of interest amount). The required synthetic case is now explicit: taxable interest of $10, no dividends, asserted foreign-account fact, and Schedule B Part III questions surfaced.

### 2. Schedule B line 3 exclusion and 1099-INT box 3 handling

Status: confirmed closed.

Charter v2 adds F11 for excludable savings-bond interest and 1099-INT box 3 classification. It also permits a narrow zero-excludable synthetic case while requiring a blocked reason when exclusion facts are open, which matches the required amendment.

### 3. 1099-INT box 2 adjustment path

Status: confirmed closed.

Charter v2 adds F12 for the AGI chain: Form 1040 line 9, Schedule 1 line 26, Form 1040 line 10, Form 1040 line 11, and 1099-INT box 2 as the first concrete adjustment. This closes the direct-line-15 bypass identified in the original attack.

### 4. Rounding order trap

Status: confirmed closed.

Charter v2 adds F13 with two sub-dollar additive inputs where per-input and post-total rounding diverge. It requires the artifacts to declare rounding stage, so a stable-but-wrong ordering can no longer pass Q5 unnoticed.

### 5. Smuggled default for rounding convention

Status: confirmed closed.

Charter v2 adds F14 for no-convention blocking. The fixture requires every rule needing the rounding convention to block with schema'd reasons, or requires the design to argue from artifacts why no rounding is not an elective default.

### 6. Misleading artifact via label/output mismatch

Status: confirmed closed.

Charter v2 broadens Q7 to fresh-reader recovery across every artifact kind represented by F1-F14, explicitly including output identity, field mappings, and cross-form bridge declarations. Q11 also requires schema-level shapes for every proposed citizen, act, and record kind, with at least one negative validation example for label/id or prose/id mismatch if the schema can express the distinction.

### 7. Structural evolution trap

Status: confirmed closed.

Charter v2 expands F10 beyond parameter changes to include a paper-only structural evolution probe. It requires the design to name which artifact ids persist, which new ids appear, which versions change, and whether a migration artifact is implicated.

## Dissent

I withdraw the round-0 adversary dissent. Charter v2 closes the seven required amendments from `round-0-adversary.md`; the iteration-1 builder seat may open under the foreman's dispatch.
