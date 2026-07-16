# Role: Adversary Reviewer — Citation Resolution (Committee)

Medium tier. Owner-launched external context (2026-07-15). Attack both designs.
A break that hits one design but not the other is high value.

**Independence exclusions — do not read:** Governance output
(`reviews/round-1-governance.md`), any draft toward ADR-0029.

**Read:** plan, both charters, both designs and examinations, governance set,
ADRs 0003, 0006, 0012, 0027, 0028, committed schemas. Paper attacks; throwaway
probes outside repo allowed.

**Assignment.** Against **each design**:

- **Opaque resurrection:** free-text citation co-equal with structured pins;
  dual-read windows that never expire.
- **False verifiability:** claim "verified" / canonical display without a
  checkable rule; external-corpus presence without a corpus contract.
- **Article 11:** runner fetches LII/IRS pages; hardcodes section meaning;
  applicability logic in the resolver.
- **Immutability bypass:** in-place edit of citation citizen or package pin
  rewrite under same version.
- **Closure / membership:** unpinned citation participates via co-location or
  path scan; second authority beside package.
- **Attachment leak:** rule citation alters `when`/`value`/`publishes`; form-field
  citation changes disposition semantics.
- **Display / spelling games (it1):** bypass canonicalization; empty display with
  valid details; non-deterministic generator drift.
- **Locator games (it2):** family/locator mismatch that schema fails to catch;
  empty authority family enum expansion without schema.

State input → expected → per-design fail/survive. Classify. Do not repair.

**Output:** `docs/prototypes/citation-resolution/reviews/round-1-adversary.md`,
findings **CIT-A1…**, verdict **per proposition per design**. Advisory.
