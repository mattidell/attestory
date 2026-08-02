# Role: Adversary Reviewer — Adopted-Content Manifests (Committee)

Medium tier. Owner-launched external context (2026-07-14). Committee round over **two independent designs** of the same two propositions: the incumbent (`it1/`) and the clean-room rival (`it2/`). Attack both. A construction that breaks one design but not the other is your most valuable finding — it tells the foreman which mechanism to carry forward.

**Independence exclusions — do not read:** the Governance reviewer's output (`reviews/round-1-governance.md`), any draft or notes toward ADR-0027. There is no prior ACM review to exclude.

**Read:** the topic `plan.md`, `charter-it1.md`, `charter-it2.md`, `it1/design.md`, `examination-it1.md`, `it2/design.md`, `examination-it2.md`, `docs/governance/`, ratified ADRs 0002, 0003, 0006, 0010–0012, 0014, 0016, 0025, 0026, and committed `packages/derivation/`, `packages/schemas/`, and 2025 content packages to ground attacks. Paper attacks only; read-only throwaway probes outside the repo are allowed to check a claim.

**Assignment.** Against **each design**, mount concrete counterexamples:

- **Path-manifest resurrection.** Reconstruct the spike's filesystem inventory as a silent second authority (loader walks `packages/content/` and treats co-located files as members). Does either design still allow a package that validates while an unpinned co-located form-field or composition document participates in derivation/rendering?
- **Orphan form-field.** Publish a form-field whose `binds_symbol` is not produced by any unit member (and not authorized by conflict/composition rules). Does each design reject, and can you route around via entrypoints (rival) or missing reverse-reachability (incumbent)?
- **Vacuous composition / ELX.** Ship a line-2b publisher without a non-vacuous composition binding; pin a composition that does not biject slots; install `optional_default` / `input_bindings` without the cited fact type or default parameter; put `optional_default` on an elective fact. Attack both designs' issue maps.
- **Partial upgrade / immutability.** Keep package id+version while changing the member set; add only some of a successor's peers; present altered bytes under a published version. Does each design reject (Article 9), and is the rival's checksum/`ACM_PACKAGE_VERSION_REWRITE` stronger than the incumbent's version-immutability claim alone?
- **Schema-generation skew / pin-role dual meaning.** Admit `rule-artifact.v2` content without admitting the generation; give the token `composition` two meanings across v1/v2 positions; omit a referenced operation-semantics or source-mapping peer. Prefer attacks that one design fails and the other survives.
- **Fact-type surface.** Attack the incumbent's individual `fact-type` pins vs the rival's `fact-type-bundle`: can a bundle pin admit a fact type the package does not version-lock, or can an individual pin leave bundle adoption out of sync with derivation?

State each attack as input state → expected result → where each design fails or survives. Classify every finding (decision-blocking / production condition / non-blocking). Do not repair designs.

**Output:** `reviews/round-1-adversary.md`, findings labeled ACM-A1, ACM-A2, …, each naming the design(s) it applies to, ending with a verdict **per proposition per design** (accept / conditionally accept (conditions listed) / reject). Advisory: the owner decides disposition.
