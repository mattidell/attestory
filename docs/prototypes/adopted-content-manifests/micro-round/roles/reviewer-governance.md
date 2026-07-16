# Role: Governance Reviewer — ACM Micro-Round Residuals (Committee)

Medium tier. Owner-launched external context (2026-07-15). Committee round over
**two independent residual designs** of MR-P1 and MR-P2: incumbent
(`micro-round/it1/`) and clean-room rival (`micro-round/it2/`). Measure both;
make convergence and divergence explicit. Parent **ADR-0027 floor is settled**
— do not re-litigate extend-not-fork package.v2, typed graph, role canon,
admitted_schemas, exclusive projection, or form-field producer integrity.

**Independence exclusions — do not read:** the Adversary reviewer's output
(`micro-round/reviews/round-1-adversary.md`), any draft or notes toward residual
ADR-0028 (or any residual ADR).

**Read:** `micro-round/plan.md`, `charter-it1.md`, `charter-it2.md`,
`it1/design.md`, `examination-it1.md`, `it2/design.md`, `examination-it2.md`,
`docs/governance/`, accepted ADRs 0003, 0006 (esp. decision 6), 0010, 0012,
0014, **0025**, **0026**, **0027** (Not Decided N1/N2 as problem statements),
and committed `packages/schemas/` (fact-type, bundle, act-bundle-adoption,
source-closure-mapping), `packages/derivation/`. Parent main-round ACM reviews
are optional context for G1/A3/A4/A7 problem statements only — do not treat
main-round mechanism picks as residual answers.

**Assignment.** For **each design**, measure both propositions:

- **MR-P1 (fact surface).** Does exact membership work without pretending HEAD
  `fact-type.v1`/`bundle.v1` already have `version`? Are schema successors (or
  an alternate exact-identity rule) explicit? Pin unit (individual fact-type vs
  bundle vs dual) justified? Inclusion joins defeat pin/bundle drift (A7)?
  Mapping fact-type fields closed (A4)? Wholesale `act-bundle-adoption`
  reconciled, not papered over? ADR-0006 decision 6 discharged?
- **MR-P2 (composition obligation).** Is the obligation discoverable **without**
  a composition citizen already present (A3 non-circular)? Does the design
  reject bare multi-source sums that never declare obligation (not only
  declared-but-incomplete packages)? Provenance-only `composition` pin retained
  (ADR-0026/0027)? Form-fields not authority (ADR-0012)? No Article 11 runner
  symbol table?
- **Structural divergence you must rule on:**
  - it1: dual pin (package `fact-type-bundle` vocabulary + exact fact identity
    in joins); package field `composition_obligations[]` + structural
    multi-source completion forcing declaration.
  - it2: package `fact-type` pins + inclusion into adopted `bundle.v2`; separate
    `composition-obligation.v1` governance citizen pinned with role `governance`.
  State which surfaces better discharge N1/N2, or a hybrid naming parts.

Classify findings (decision-blocking / production condition / non-blocking).
Do not repair designs.

**Output:** `docs/prototypes/adopted-content-manifests/micro-round/reviews/round-1-governance.md`,
findings **MR-G1, MR-G2, …**, verdict **per proposition per design**
(accept / conditionally accept (conditions) / reject), and a one-line
carry-forward recommendation for residual ADR (~0028). Advisory: owner decides.
