# Source Completeness Reconciliation Patch — Pre-Merge Review

- Reviewer seat: patch reviewer, Medium tier, owner-launched external context
- Subject: branch `patch-source-completeness-reconciliation` at `92d7e7d`
  (commits `12d1f8a`, `c8ddb30`, `92d7e7d`), built under
  `docs/reviews/charter-2026-07-13-source-completeness-patch.md` to close
  SC-R1 and SC-R2 of
  `docs/reviews/2026-07-13-source-completeness-reconciliation.md`
- Independence: this review did not inherit builder claims; it inspected the
  patch via detached worktree / `git show`, re-ran the reconciliation
  reproductions as throwaway probes outside the repository, and ran the full
  verification suite on the patch tree via the project `.venv`
- Status: advisory. The owner decides and merges non-ff to `main`.

## Findings

### SC-PR1 — ADR number collides with the milestone branch sequence

- Severity: **merge-blocking**
- Defect: The patch lands the boundary ADR as
  `docs/adr/0018-member-assertion-and-transition-boundaries.md`. That number
  is free on current `main` (and on the patch base `5116e01`), but
  `milestone/core-tax-conditions` already occupies **0018–0022**
  (`0018-citation-resolver-contract` through `0022-adopted-content-manifests`).
  Merging the patch as ADR-0018 forces a later collision when the milestone
  lands.
- Required correction: renumber the patch ADR to the next globally free
  number **0023** (filename, title, and any self-references) before merge.
  Status remains `proposed` until owner ratification at merge.

### SC-PR2 — ADR Links embed absolute local machine paths

- Severity: **non-blocking**
- Defect: The ADR Links section uses `file:///Users/mattidell/git/personal/finances/...`
  URLs for the charter, review, and precedent ADRs. Existing ADRs cite
  repository-relative paths (backticks or relative markdown links), not host
  absolute paths. The absolute form is machine-specific and will not resolve
  for other checkouts.
- Reproduction: `git show 12d1f8a:docs/adr/0018-member-assertion-and-transition-boundaries.md`
  Lines under `## Links`.
- Recommended correction: rewrite Links to repo-relative paths when applying
  SC-PR1 (e.g. `docs/reviews/...`, `docs/adr/0016-...`).

### SC-PR3 — Committed regression probes are admission-unit, not full review path

- Severity: **non-blocking**
- Defect: The charter asked for end-to-end probes of the review's accepted-act
  paths. The committed tests
  (`tests/source_completeness/test_track5_lifecycle.py::RegressionProbes`)
  correctly assert `FindingModelError` at `apply_act` for both defects, and
  SC-R2 also checks that an ordinary same-member correction remains admitted.
  They do not, however, follow the review's SC-R1 path through empty-family
  zero publication and coverage observation before the plain assertion, nor
  do they explicitly assert post-rejection horizon / closure / zero / coverage
  currency on the full path.
- Why not merge-blocking: independent external probes (below) re-ran both
  review paths exactly and confirmed the corrected outcomes. Because the fix
  is admission rejection, the bad projected state (late member current under
  `b1.h0` with `closed` coverage and a live zero) is unreachable once
  `apply_act` raises. The committed probes would fail on pre-patch tip
  `5116e01` (both paths accepted there).
- Optional follow-up: thicken the committed SC-R1 probe to open with the zero
  and assert pre/post currency if desired; not required for merge once SC-PR1
  is fixed.

## SC-R1 closure (verified)

**Builder choice:** reject-at-admission for a plain `assertion` whose fact
type is a registered family member predicate and whose fact is not already a
current family member. Same-member corrections remain on the ordinary
assertion path.

**Rationale (accepted on the merits):**

- Matches ADR-0017 decision 3 (membership change requires an atomic horizon
  successor) and decision 4 (same-member value correction does not advance
  the horizon), and ADR-0016's closed-universe constraint on B1 zeros.
- Preferable to atomic routing of plain assertions: keeps ordinary acts
  non-horizon-advancing and avoids a composite act kind (ADR alternatives
  section is honest on this point).
- Preferable to post-fact / coverage-only validation: keeps invalid sequences
  out of the act log (Articles 7, 12, 13).
- Placement is **kernel-enforced** in `apply_assertion`, not relocated to an
  honor-system workspace service. Predicate configuration is
  registry-carried and populated by `tax_registry()` from declared source
  families — appropriate for a content-agnostic kernel. Bare
  `SchemaRegistry` instances start with an empty predicate set (SC-R1 is a
  no-op until the consuming builder fills it); production tax admission goes
  through `tax_registry()`, which does populate it.

**Exact review reproduction (external probe, patch tree `92d7e7d`):**

1. B1 bundle adoption, genesis `b1.h0`, true closure `b1.closure.h0`
2. Publish empty-family zero (value `"0"`)
3. Introduce payer + statement entities
4. Pre-assertion: horizon `b1.h0`, closure current, zero current, coverage
   `closed`
5. Plain `assertion` for
   `tax.us.2025.f1099int.box1-interest|payer=demo-payer-bank-alpha,statement=stmt.demo-payer-bank-alpha.2025.a,tax-year=2025`
   at `120`

**Observed (corrected):** `FindingModelError` —
`cannot assert member fact ... through a plain assertion; must use a
member-transition instead`. Act log unchanged: horizon `b1.h0`, closure
current, zero current, coverage `closed`, no member finding.

**Baseline (`5116e01`):** the same plain assertion was accepted with horizon
still `b1.h0` (defect present).

`packages/tax/loader.py` and `packages/kernel/schema_registry.py` changes are
justified: they are the only way to surface declared member predicates to the
kernel admission check without baking tax content into the kernel.

## SC-R2 closure (verified)

**Exact review reproduction (external probe):**

1. Same B1 genesis setup; introduce payer + statement
2. Accept `member-transition` assert of the B1 fact at `120` with successor
   `probe.h1`
3. Submit second `member-transition` assert of the identical fact at `125`
   with successor `probe.h2`

**Observed (corrected):** `FindingModelError` —
`transition asserting fact ... already in the family is rejected: same-member
correction belongs on the ordinary assertion path`. Horizon remains
`probe.h1`; `probe.h2` is not recorded. Ordinary plain `assertion` for the
value correction is then accepted without advancing the horizon.

**Baseline (`5116e01`):** second transition accepted; horizon advanced to
`probe.h2`.

**Genuine membership changes still admit:** external probe confirmed a second
distinct member add advances the horizon, and a subsequent remove advances
again. Existing lifecycle suite covers incremental/rebuild equality, atomic
rejection of malformed transitions, family isolation, old-zero displacement
after valid transition, re-attestation + rerun, and no-resurrection.

## Scope discipline

Diff against `main...patch` (`5116e01...92d7e7d`):

| Path | Role |
| --- | --- |
| `docs/adr/0018-member-assertion-and-transition-boundaries.md` | proposed Tier-2 boundary ADR (SC-PR1 renumber) |
| `packages/kernel/findings.py` | SC-R1 + SC-R2 admission checks |
| `packages/kernel/schema_registry.py` | `family_member_predicates` set |
| `packages/tax/loader.py` | populate predicates from source-family content |
| `tests/source_completeness/test_track5_lifecycle.py` | regression probes |

No successor-milestone content, no prototype material, no absorbed adjacent
defects. Commit shape matches the charter: ADR commit, then one commit per
finding (`c8ddb30` SC-R1, `92d7e7d` SC-R2), messages cite finding ids.

### ADR substance (aside from number and Links)

- Status `proposed`, Tier 2: correct.
- Context cites the reconciliation review and SC-R1/SC-R2: correct.
- Decisions match the implemented boundary (reject plain new-member
  assertion; reject same-member transition; registry-carried predicates).
- Consequences and alternatives are accurate and aligned with Articles 7, 12,
  and 13.

## Verification (patch tree `92d7e7d`, project `.venv`)

| Check | Result |
| --- | --- |
| `.venv/bin/python -m unittest` | 316 tests OK (~13.5s) |
| `.venv/bin/python tools/governance_lint.py` | `governance lint: conformant` |
| `.venv/bin/python -m mypy` | Success: no issues found in 69 source files |
| Lifecycle guarantees | green via suite (including Track 5 lifecycle) |
| External SC-R1 / SC-R2 exact reproductions | both corrected outcomes confirmed |
| Pre-patch baseline `5116e01` | both defect paths accepted |
| Data-safety scan of patch diff | synthetic fixture labels only; no private-path markers or account-shaped digit runs in code/tests. Absolute machine paths appear only in the ADR Links (SC-PR2). |

Note: unittest count is 316 vs the reconciliation review's 314 — consistent with
the two new probe methods.

## Verdict

**Merge-ready after listed corrections.**

Mandatory before merge:

1. **SC-PR1** — renumber the boundary ADR from **0018** to **0023**
   (filename and title).

Recommended in the same correction commit:

2. **SC-PR2** — replace absolute `file://` Links with repository-relative
   citations.

SC-PR3 is advisory only. Functional closure of SC-R1 and SC-R2 is verified;
scope is disciplined; boundary choice and kernel placement are sound.
