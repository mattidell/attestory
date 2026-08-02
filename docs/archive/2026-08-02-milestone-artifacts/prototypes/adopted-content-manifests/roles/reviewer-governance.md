# Role: Governance Reviewer — Adopted-Content Manifests (Committee)

Medium tier. Owner-launched external context (2026-07-14). Committee round over **two independent designs** of the same two propositions: the incumbent (`it1/`) and the clean-room rival (`it2/`). Measure both and make their convergence and divergence explicit — that comparison is the point of the round.

**Independence exclusions — do not read:** the Adversary reviewer's output (`reviews/round-1-adversary.md`), any draft or notes toward ADR-0027. There is no prior ACM review to exclude.

**Read:** the topic `plan.md`, `charter-it1.md`, `charter-it2.md`, `it1/design.md`, `examination-it1.md`, `it2/design.md`, `examination-it2.md`, `docs/governance/`, ratified ADRs 0002, 0003, **0006** (esp. decisions 3/6/7/9), 0010–0012, 0014, 0016, **0025**, **0026**, and committed `packages/derivation/` (`package_validation.py`, `loader.py`), `packages/schemas/`, and the 2025 content packages as reference. The inert spike and ADR-0022 may be read as superseded prior art (both designs reject them).

**Assignment.** For **each design**, measure both propositions against the governance set:

- **ACM-P1 (membership surface).** Does the unit **extend** or honestly **succeed** ADR-0006's closed package without inventing a second authority (path inventory, directory walk, or parallel manifest)? Judge concrete membership: which citizen kinds are pins; how bidirectional closure and version-lock work; whether form-fields, source-family/mapping, composition, fact-types/bundles, and operation-semantics are in the closed graph. Confirm validation remains **contained** per defect (decision 3), package versions are **immutable** (Article 9), and membership/`composition` pins create **no** new standing-affecting derivation edge (ADR-0010; composition provenance-only per ADR-0026).
- **The structural divergence — you must rule on it.** Both designs claim `artifact-package.v2` extension, but they diverge on mechanism:
  - **Incumbent:** `admitted_schemas` string list; individual `fact-type` member pins; binding codes (`FORM_FIELD_DANGLING_BINDING`, `COMPOSITION_*`, `ELX_*`, `MEMBER_SCHEMA_UNADMITTED`).
  - **Rival:** `schema_contracts` with published checksums + `content_role`; `role_vocabulary` canon pin; `entrypoints` (esp. form_fields); `fact-type-bundle` as a member kind; typed closed-graph rule; codes `ACM_*` including package-version rewrite and role-semantic divergence.
  State which surface better discharges ADR-0006 decisions 6–7 and the plan's floor (form-fields + post-0006 authority + vacuous-binding defeat) without runner-resident policy (Article 11) or dual pin-role meanings.
- **ACM-P2 (binding + schema-generation).** Confirm every named join rejects at load (form-field → published symbol; composition pin → matching composition + slot bijection; `input_bindings` / `optional_default` → fact type + parameter; family ↔ mapping ↔ subtotal; rule refs → pinned peers). Judge schema-generation coexistence: does each design prevent silent partial load of unadmitted `*.v2` content and pin-role dual meaning when `composition` enters the shared vocabulary?

Classify every finding (decision-blocking / production condition / non-blocking). Do not repair designs. Where the two designs converge, say so — independent convergence is the strongest signal available.

**Output:** `reviews/round-1-governance.md`, findings labeled ACM-G1, ACM-G2, …, each naming the design(s) it applies to, ending with a verdict **per proposition per design** (accept / conditionally accept (conditions listed) / reject) and a one-line recommendation on which design's membership surface and binding mechanism to carry into ADR-0027 (or a hybrid, naming the parts). Advisory: the owner decides disposition.
