# Examination: Capital-Gain Distributions → Line 7a (Incumbent It1)

Audience: Reviewers, foreman, owner

**Seat:** Incumbent Builder — conclusion-level topology.
**Design under examination:** `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/it1/design.md`
**Launch commit:** `42644186fa736df5c0e4f9ea71ed2415fe3038c8`
**Evidence rung:** Rung 1 (static paper instances only).

This examination reports each proposition separately. Status is **settled at
Rung 1** only when the design supplies concrete instances, failure states,
pins, and successor contract sentences sufficient for an ADR to adopt or
reject without a further evidence rung. Unresolved items are named; none are
silently absorbed into a fourth proposition.

---

## P1 — Direct-route authority

### Status: **Settled at Rung 1** (for the chartered conclusion-level topology)

### Claim examined

ADR-0038's contributed categorical `tax.us.2025.schedule-d-required` is
sufficient authority for the direct line-7a route when the design defines
missing, `"yes"`, `"no"`, correction, and supersession without inventing
finer eligibility facts.

### Evidence cited

| Requirement | Case / location | Result |
| --- | --- | --- |
| Positive 1 | Design Case 1 (`sdr-no` → line7a=400) | Authority authorizes publication; pins include `demo-finding.sdr-no`. |
| Positive 2 | Design Case 2 (same authority, multi-payer 550) | Authority is return-level, not per-payer. |
| Negative 1 | Design Case 3 (authority missing) | Blocked; walk names `schedule-d-required`; no zero inference; no Schedule D. |
| Negative 2 | Design Case 4 (`sdr-yes`) | `guard_inapplicable`; structurally distinct from Case 3; no attachment. |
| Lifecycle | Design Case 6 both directions | Supersession displaces line7a/line9/line16; reverse republishes without history edit. |
| Map | Design §6 P1 map | Producer → authority → consumer → failure complete. |
| Contradiction neighbor | Design Case 5 | Interlock remains admission-locus; does not invent a second authority. |
| Successor sentences | Design S1.1–S1.5 | Adoptable/rejectable contract text. |

### Accepted contracts consumed unchanged

- ADR-0038 decision 1 (`schedule-d-required` fact type, domain, no default).
- Free supersession policy already on the fact type.
- ADR-0010 displacement via ordinary edges.

### Production conditions (not Rung-1 blockers)

- Goldens for missing / yes / no / bidirectional supersession.
- No UI or contribution default that inserts `"no"`.
- Explanation pin of the authority finding on every published line7a.

### Unresolved (explicit; non-blocking for chartered topology)

- **U1** (design §6 P1): whether process/UI should warn when `sdr-no` coexists
  with capital-transaction signals outside this milestone. That is a honesty
  cost of **conclusion-level** authority, not a missing case in the matrix.
  A rival component-backed topology may treat U1 as decision-blocking for
  *its* comparison; under this charter the incumbent may not silently replace
  the topology. Reviewers should score U1 as residual uncertainty of the
  topology, not as missing Case 3/4 evidence.

### Rung judgment

Paper distinguishes all five authority states with exact current/displaced
findings. No schema probe is required to understand missing vs `"yes"` vs
`"no"`. **P1 settled at Rung 1** for the incumbent shape.

---

## P2 — Box-2a family promotion

### Status: **Settled at Rung 1**

### Claim examined

The smallest versioned successor statement/member/family/closure shape makes
box 2a composable while preventing any rule or package from collecting both
it and the historical recorded/non-composable representation, and preserves
the CAPITAL_GAIN_DISTRIBUTION_RECORDED contradiction feed.

### Evidence cited

| Requirement | Case / location | Result |
| --- | --- | --- |
| Positive 1 | Case 1 single member + closure + subtotal 400 | Family pattern mirrors ADR-0035 1a. |
| Positive 2 | Case 2 two members pins once each; subtotal 550 | Multi-payer composition. |
| Negative 1 | Case 8a–c historical collect / mixed graph | Rejected by S2.7 exclusivity + universe guard. |
| Negative 2 | Case 7b open; Case 7d stale | No silent zero; blocked until current true closure. |
| Lifecycle | Case 7a–f full table | Closed-empty → zero; correction/removal/horizon succession specified. |
| Interlock under successor | Case 5 with member feed | Signal from positive member; both orders + same-batch fail closed. |
| Map | Design §6 P2 map | Complete. |
| Successor sentences | Design S2.1–S2.8 | Fact type, family, closure, universe v2, recorded-boxes v2, exclusivity. |

### Accepted contracts consumed unchanged

- ADR-0035 decisions 1–3 (identity, per-box families, recorded non-composable
  posture for remaining boxes).
- Historical `f1099div.bundle` `recorded-boxes@v1` and `dividend-universe@v1`
  bytes immutable.
- ADR-0038 decision 5 contradiction mechanism (feed migrates; rule unchanged
  in spirit).

### Closed-empty disposition (explicit)

Case 7a: closed-empty + `sdr-no` → **subtotal and line7a publish 0**, not
inapplicable. Inapplicability remains authority-`"yes"` only (Case 4). This
matches ADR-0016 closed-empty honesty for other per-box families.

### Production conditions

- New citizens only as new versions; manifest add-only.
- Resolver exclusivity kill-tests for Case 8.
- Signal feed tests from successor members.
- Optional Rung-2 probe (plan Gate 3 question) is **not** required to settle
  the sentences if reviewers accept S2.7 as the mechanical distinction
  contract; U3 notes residual desire for a kill-test in production tracks.

### Unresolved

- **U2**: forward-only contribution vs migration of historical
  `recorded-boxes@v1` workspace rows — production Track concern.
- **U3**: mechanical validator proof of mixed-graph rejection — production or
  optional probe; paper already states the reject contract.

### Rung judgment

All required negative and lifecycle family states are instantiated with
concrete horizons and finding ids. Historical immutability is respected via
successors only. **P2 settled at Rung 1.**

---

## P3 — Line 7a and QDCG handoff

### Status: **Settled at Rung 1**

### Claim examined

Declared bindings carry the box-2a subtotal to line 7a, into line 9 exactly
once, and into QDCG as a selected publication; Schedule-D-required `"yes"`
remains an honest inapplicable/non-publication route with no fabricated
Schedule D; double-count and direct-read attacks fail closed.

### Evidence cited

| Requirement | Case / location | Result |
| --- | --- | --- |
| Positive 1 | Case 1 line7a=400; line9 +400 once; QDCG base Q+400 | Full handoff. |
| Positive 2 | Case 10 Q=0, line7a=400 worksheet; contrast both-zero reduction | Preferential path without breaking ADR-0038 reduction. |
| Negative 1 | Case 4 sdr-yes | No line7a publish; line16 inapplicable; no Schedule D. |
| Negative 2 | Case 9a–c | Double-count and raw collect unrepresentable under adopted pins / package rules. |
| Lifecycle | Case 6 | line7a, line9, line16 displace together on authority supersession. |
| Missing authority impact | Case 3 | Downstream does not invent zero capital gains. |
| Map | Design §6 P3 map | Complete. |
| Successor sentences | Design S3.1–S3.6 | line7a rule, form fields, line9 v3, line16 v3 base binding, no raw read. |

### Accepted contracts consumed unchanged

- Line 9 as sum of declared published totals (v2 shape extended, not
  rewritten in place).
- ADR-0037 `conditional_dependency_set` for multi-absent walks and false
  condition reduction.
- ADR-0038 posture that `"yes"` on Schedule D is out-of-scope for worksheet
  completion inside this engine slice.
- Form-field disposition vocabulary (published / zero / blocked /
  guard_inapplicable).

### Line 16 condition expansion (examined)

S3.4 expands the declaration-demand condition to
`any([Q>0, line7a-total>0])`:

- Preserves **qualified-zero and capital-gain-zero** reduction (declarations
  unread) — Case 10 contrast.
- Enables **qualified-zero and positive line7a** preferential taxation —
  Case 10 primary.
- Does not read raw box 2a; only `line7a-total`.

This is a declared successor to line16 v2 notes (which bound CG to literal 0
and gated only on Q). It is not a silent HEAD claim.

### Production conditions

- Package pin moves for line9 v3 and line16 v3.
- Goldens: Cases 1, 2, 3, 4, 6, 9, 10.
- Presentation of line 7a/7b without rejected-value leakage.
- Citation citizens for line 7a/7b.

### Unresolved

- **U4**: fine-grained line-7b presentation control — disposition-level at
  paper; not authority.
- **U5**: `cgd-yes` with closed-empty box2a and `sdr-no` — engine publishes
  line7a=0; process warning optional. Not a double-count path.

### Rung judgment

Handoff, single entry into line 9, QDCG binding, inapplicability, and attack
unrepresentability are all shown with concrete symbols and pins. **P3 settled
at Rung 1.**

---

## Cross-proposition mandatory cases

| Case | P1 | P2 | P3 | Notes |
| --- | --- | --- | --- | --- |
| 1 eligible single | + | + | + | Baseline publish. |
| 2 eligible multi | + | + | + | Subtotal pins. |
| 3 authority missing | − mandatory | (family may close) | − downstream | No zero inference. |
| 4 Schedule D required | − mandatory | n/a | − mandatory | Inapplicable ≠ blocked. |
| 5 contradiction | adjacent | − mandatory | n/a | Admission, both orders + batch. |
| 6 authority lifecycle | lifecycle | n/a | lifecycle | Bidirectional. |
| 7 family lifecycle | n/a | lifecycle | closed-empty zero | Six states. |
| 8 historical reach-around | n/a | − mandatory | adjacent | Exclusivity. |
| 9 double-count / direct-read | n/a | adjacent | − mandatory | Pins-only consumers. |
| 10 qualified-zero neighbor | n/a | n/a | + and contrast | Reduction preserved. |

---

## Summary for foreman

| Proposition | Rung-1 status | Decision-blocking gaps |
| --- | --- | --- |
| **P1** | Settled at Rung 1 | None for chartered topology. Residual **U1** topology honesty cost — flag for review comparison with rival, not a missing matrix case. |
| **P2** | Settled at Rung 1 | None. **U2/U3** are production-condition / optional probe. |
| **P3** | Settled at Rung 1 | None. **U4/U5** presentation/process residuals. |

**Files produced (this iteration only):**

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/it1/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/it1/examination.md`

**Stop compliance:** No production code, schema edit, probe, fourth
proposition, real data, Schedule D implementation, merge, PR, rival review,
or repair begun.
