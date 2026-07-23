# H1 Repair 1 governance delta review

Role: Governance reviewer (Medium tier)
Status: completed 2026-07-22
Charter: `charter-repair1-governance-review.md`

## Scope and method

This delta review considered only sealed repair exhibit
`00d1550194b3b63b99312cfa63d2985f06d9c135`: its design, examination, and
`scan_before_release_probe.py`. It did not review the rejected rival,
unmodified incumbent surface, or owner-excluded similarly named work.

I also ran the sealed probe twice from an isolated extraction of that exact
commit. Both executions emitted the derived all-zero new-ref update and the
passing sibling inventory, then produced no guarded-push, raw-push, marker,
tamper, missing-installation, or final exit result. Those incomplete executions
are recorded below as `not run`; the committed examination's transcript is not
substituted for a completed independent result.

## Measurements

| Measurement | Result | Direct evidence |
| --- | --- | --- |
| 1. Ordering and exactness | **not run** | Static evidence is directionally correct: `exact_update()` derives `refs/heads/main <local oid> refs/heads/main <zero oid>`, `scan_exact_update()` feeds it to `envelope_scan.py --push`, and `guarded_push()` returns on a scan failure before `os.pipe()`. The helper's empty `list for-push` advertisement and fixed refspec support the claimed equality with the subsequent push. But the isolated executions stopped after the sibling inventory, before the actual guarded push, marker, tamper, and missing-install checks could establish the required outcomes. |
| 2. Non-skippable raw posture | **not run** | The sealed source does invoke actual raw `git push` and `git push --no-verify` with no descriptor variables, and the examination records the same exit-128 descriptor-absent result. Neither raw case was reached in the incomplete independent executions, so this review cannot confirm the required actual-Git result. |
| 3. Honest same-UID boundary | **pass** | The completed sibling subprocess reported `token-env=pass`, `askpass-env=pass`, `credential-config=pass`, `credential-helper=pass`, and `direct-transport=pass`. The source runs it with the sanitized fixture environment and no passed guard FD; direct helper launch requires the missing descriptor. The design expressly excludes process attachment, memory/descriptor inspection, owner credential authority, and OS escalation as privileged/malicious-owner concerns. That limit is coherent with the plan's named ordinary, non-malicious local-process threat. `own-descriptors` is only a weak supplementary check (FD-directory names are numeric), not the basis for this conclusion. |
| 4. H2/H3 contract | **pass** | H2 names only owner-attested GitHub push protection, secret scanning, and branch protection, expressly denying local proof of their configuration. H3 specifies an E18.1 route inventory and raw/bypass descriptor-absent assertions, plus E18.2 event assertions requiring no `descriptor-created`, `descriptor-passed-to-git`, or `transport-received` before scan acceptance; marker, tamper, and missing-install cases are named. |
| 5. Boundary/process | **pass** | The sealed exhibit uses a runtime-created synthetic token, disposable local helper/repositories, and a constructed marker; it names no real credential, remote, personal data, residency locator, or owner path. It remains a delta-only Rung-2 prototype and adds no scope beyond the ordering repair and H2/H3 paper form. |

## Outcome

No static design violation of the repaired ordering, ordinary same-UID scope, or
H2/H3 paper boundary was found. However, Measurements 1 and 2 are required
actual-Git invariants and remain **not run** in this review: the exact sealed
probe did not complete its guarded or raw transport cases under isolated
execution. This is an evidence blocker to an affirmative delta-review pass,
not a claim that the intended invariant has been disproved. The repair must not
be treated as independently verified until a completed exact-probe transcript
establishes those cases.
