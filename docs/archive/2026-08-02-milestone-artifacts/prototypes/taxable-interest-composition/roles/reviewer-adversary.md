# Role: Adversary Reviewer — Taxable-Interest Composition (Committee)

Medium tier. Owner-launched external context (2026-07-14). Committee round over **two independent designs** of the same two propositions: the incumbent (`it1/`) and the clean-room rival (`it2/`). Attack both. A construction that breaks one design but not the other is your most valuable finding — it tells the foreman which mechanism and boundary to carry forward.

**Independence exclusions — do not read:** the Governance reviewer's output (`reviews/round-1-governance.md`), any draft or notes toward ADR-0026. There is no prior TIC review to exclude.

**Read:** the topic `plan.md`, `charter-it1.md`, `charter-it2.md`, `it1/design.md`, `examination-it1.md`, `it2/design.md`, `examination-it2.md`, `docs/governance/`, ratified ADRs 0002, 0004, 0006–0012, 0014–0017, and committed `packages/derivation/`, `packages/kernel/`, and Source-Completeness content to ground attacks. Paper attacks only; read-only throwaway probes outside the repo are allowed to check a claim.

**Assignment.** Against **each design**, mount concrete counterexamples:

- **Narrow substitution (ADR-0016 dec 5).** Try to publish line 2b, or a line-2b zero, from a proper subset of constituents — a ref-subset line rule, a mapping that admits the line symbol for a narrow family, coverage that reports the universe complete from box-1 closure. Does the incumbent's V5 / the rival's slot-bijection + `require_closed` actually block every path?
- **Hidden-open-input zero.** Construct a state where a constituent is unclosed but line 2b still publishes a zero, or where a present-source subtotal makes line 2b eligible without every constituent's closure being read.
- **The boundary — find the omitted source.** For **each** universe, name an in-scope *taxable* interest source it omits and show a filer whose line 2b would be understated while the composition reports complete. The incumbent omits taxable OID by design (deferred) — construct the OID filer it silently under-reports. Then test the rival's 4-slot set the same way (market discount, accrued interest at purchase, nominee interest, K-1 interest): does `unreported_taxable_interest` genuinely absorb them, or is the rival's claim of completeness also overstated?
- **Late-member lifecycle.** assert-after-zero, re-attest, member removal/reclassification: does displacement re-fire through the two existing edge kinds only, and can you resurrect the old coextensive zero or orphan a subtotal?
- **Binding integrity.** Attack the rival's new `composition` pin and `require_closed` operation, and the incumbent's package-level binding: can you adopt a package that passes validation yet publishes line 2b from an incomplete universe?

State each attack as input state → expected result → where each design fails or survives. Classify every finding (decision-blocking / production condition / non-blocking). Do not repair designs.

**Output:** `reviews/round-1-adversary.md`, findings labeled TIC-A1, TIC-A2, …, each naming the design(s) it applies to, ending with a verdict **per proposition per design** (accept / conditionally accept (conditions listed) / reject). Advisory: the owner decides disposition.
