# Role: Governance Reviewer — Citation Resolution (Committee)

Medium tier. Owner-launched external context (2026-07-15). Committee round over
**two independent designs** of CIT-P1 and CIT-P2: incumbent (`it1/`) and
clean-room rival (`it2/`). Measure both; make convergence and divergence
explicit. Do not re-litigate ADR-0012 dispositions or ADR-0027/0028 membership
floor.

**Independence exclusions — do not read:** the Adversary reviewer's output
(`reviews/round-1-adversary.md`), any draft or notes toward ADR-0029.

**Read:** `plan.md`, `charter-it1.md`, `charter-it2.md`, `it1/design.md`,
`examination-it1.md`, `it2/design.md`, `examination-it2.md`, `docs/governance/`,
accepted ADRs **0003**, **0006**, **0012**, **0027**, **0028**, and committed
form-field / rule / package surfaces. Inert ADR-0018 may be read as superseded
prior art only.

**Assignment.** For **each design**, measure both propositions:

- **CIT-P1.** Is a citation a citizen vs value vs pin (or hybrid) without a
  second membership authority? Authority families for v1 justified? Attachment
  to form-fields (and rules if claimed) respects ADR-0012 presentation-only?
  Identity/version/immutability Article 9?
- **CIT-P2.** What "verifiable" means: structure only vs display canonicalization
  vs external corpus registry? Contained issues? Article 11 — no legal
  interpretation, no live fetch?
- **Structural divergence you must rule on:**
  - **it1:** required `display` + deterministic display canonicalization; case 5
    as package-member closure miss (`CLOSURE_MISSING_CITATION`); authority
    families IRC / IRS_AUTHORITY with nested details.
  - **it2:** no canonical-display claim; case 5 explicitly **not** external-corpus
    miss (structural accept only; no `legal_verified`); authority_family
    `us-code` / `irs-form` locators; explicit overreach issue.
  State which surfaces better discharge the plan floor without false
  "verified" confidence or runner legal logic — or a hybrid naming parts.

Classify findings (decision-blocking / production condition / non-blocking).
Do not repair designs.

**Output:** `docs/prototypes/citation-resolution/reviews/round-1-governance.md`,
findings **CIT-G1…**, verdict **per proposition per design**, one-line
carry-forward for candidate ADR-0029. Advisory.
