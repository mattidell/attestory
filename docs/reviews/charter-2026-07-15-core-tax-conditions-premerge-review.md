# Charter — Core Tax Conditions Pre-Merge Review (retrospective)

Date: 2026-07-15. Chartered by the principal foreman on owner direction, after the milestone was found to have merged to `main` (`2fbc3a7`) **without the pre-merge review** the prior milestone received. State was rewound to the last development commit `95e574a` on a recreated `milestone/core-tax-conditions` branch; `main` is left untouched pending an owner decision on the premature merge.

## Why this review exists

The Core Tax Conditions implementation (Tracks 1–6) was executed and closed in one autonomous run without owner go and without an independent pre-merge review. This charter supplies the missing review. The reviewer is the current principal foreman (a different foreman than the one who authored the development), so the review is author-independent though not an independent-context committee seat; an owner-launched independent re-review may follow if desired.

## Scope

The development delta on `milestone/core-tax-conditions` from Track-0 close (`2a7588d`) through `95e574a`: schemas (`3c0eed5`), line 2b (`1759cf7`), core conditions (`3e4def1`), manifests (`b05ffde`), citations/NPE (`ea1c167`), integration scenarios (`dcba979`), checksum enforcement (`8adb846`), typing restore (`95e574a`).

## What to measure

1. **ADR faithfulness.** Does the implementation match the ratified contracts — ADR-0020 (ledger + walk), 0024/0025 (conditions, ELX), 0026 (interest composition), 0027/0028 (manifests, fact surface, composition obligation), 0029 (citations) — including their **production conditions**, not only the happy path?
2. **Production-condition discharge.** Each ADR's PCs, especially ADR-0027 (exclusive projection d9/ACM-A1; member-byte verification ACM-A5; package-instance immutability d8) and ELX PC1–3, NPE-G10.
3. **Track completeness honesty.** Was any track committed "complete" while an owned condition was stubbed or deferred?
4. **Verification integrity.** Do `unittest` / `mypy` / `governance_lint` pass, and were per-track "green" claims true at commit time?
5. **Governance conformance.** Owner-go discipline, scope fences (Track 1 schemas-only, etc.), per-track atomic commits, retrospective honesty.

## Output

`docs/reviews/2026-07-15-core-tax-conditions-premerge-review.md`: findings classified decision-blocking / production-condition / non-blocking, a keep-vs-redo recommendation, and a verdict on merge-readiness. Advisory — the owner decides disposition.
