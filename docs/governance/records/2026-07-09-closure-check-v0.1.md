---
artifact: closure-check
version: "0.1"
status: record
date: 2026-07-09
---

# Closure Check — v0.1 of the Five-Document Set

Run as five passes: term resolution, citation integrity, parentage, detection runnability, open-work reconciliation. Results below; defects numbered, each with a proposed fix.

**Pass 1 — Term resolution (Constitution → Ontology).** Every italicized operative term traced. All resolve to defined entries except:

*Defect 1 — "workspace revision" is undefined.* Article 6 pins acts "against a specific workspace revision," and derivation records identify "the workspace state" evaluated — the same concept, unnamed in the Ontology. §1 defines currency but never the point-in-the-record designation that pins reference. Fix: one entry in §1 — a *revision* is a derived designation of a position in the act sequence, computable from the record like currency, never stored as independent state. Cheap, and it retroactively cleans up the derivation-record entry's "workspace state" phrasing.

*Near-defect — "the declined claim" in Article 2 presupposes claim sameness.* Suppression requires knowing when two proposals are the same claim; the Ontology stayed deliberately silent (declared-rule territory, per the §3 note). Acceptable as drafted, but the article should say "as declared proposal-handling rules define sameness" or the register should mark claim-identity as rule-artifact scope. Recommend the register note — keeps the article clean.

**Pass 2 — Citation integrity (all documents).**

*Defect 2 — Article 14 cites Article 19 for governance versioning; Article 19 is Filing.* The governance-version-pinning provision actually lives in the Constitution's closing governance note, which is not a citable article. Fix options: (a) reword Article 14 to cite "the governance note," or (b) promote governance versioning to a short Article 20. Recommend (a) — D17's content is one sentence and doesn't warrant an article until it grows, which the earlier flag anticipated.

Everything else checks: every ENG entry cites a real article; Commentary notes all annotate existing articles or ontology sections; the Judgment/Legibility and Atomicity/Publication cross-cites resolve; the Ontology's quarantine-crossing-as-grant matches Article 16.

**Pass 3 — Parentage (Articles ↔ Principles).** Complete in both directions, as reported in the Principles draft. One observation, not a defect: Principle IV generates two articles (4, 12) and Principle VI generates two (6, 8) — the merged principles carry double load, which is fine, but if either pair ever diverges doctrinally, that's the seam where a principle splits.

**Pass 4 — Detection runnability (ENG debt register).** Per the ENG governance note, entries without runnable detections are debt. Fully runnable: E1.2, E2.1, E2.2, E3.1, E5.1, E5.2, E6.1, E7.1, E8.1, E9.1, E11.1, E11.2, E12.1, E13.1, E13.2, E14.1, E14.2, E15.1, E16.1, E18.1, E18.2, E19.1. Review-dependent (debt): E1.1, E7.2, E10.1 (audits and schema review — partially mechanizable against the register, but the register format must stabilize first), E11.3 (the grep is runnable; "every behavior difference attributable" is not), E17.1 (reconstructability is testable; "displayable to the user" is a product check), E18.3 (manifest check is runnable once the manifest format exists). Six debt entries, all with a mechanization path — recorded as the conformance suite's backlog, none blocking.

**Pass 5 — Open-work reconciliation.** The Ontology's reserved entries (derived-finding authority; stance/position), the Commentary's register, and the forum list agree, with one asymmetry worth noting: *stance* is reserved in the Ontology but no constitutional article consumes it — positions surface only in Commentary notes on Articles 3 and 19. That's legitimate (reserved entries are open work, and the Constitution shouldn't norm what isn't settled), but it means stance currently has no normative home at all; when T2 resolves, it lands as either an Article 3 amendment or a new article. Logged. Full open-work register: T1 (instrument framing, recorded), T2 (stance/position), redaction detail, multi-party authority rules, D18 canonical names (now cheap — the working names held through all five documents unchanged), consent-mechanism product design, six detection-mechanization items, claim-sameness rule scope.

**Disposition.** Two defects, both one-sentence fixes; applying them and stamping the set v0.1 unless you want to see the fix wording. The check itself validated the architecture it tested: the term-resolution pass was mechanical because the Ontology gated vocabulary, and the parentage pass was mechanical because the table forced descent — the disciplines paid for themselves on first use.

---

**Disposition addendum (2026-07-09).** Both defects were closed with user-ratified wording and the set stamped v0.1: Defect 1 by the Revision entry in Ontology §1 and the consequential derivation-record edit in §6; Defect 2 by the Article 14 citation reword and the rewritten citable governance note. The Principles document, initially absent from the repository, was recovered and installed with the set. The debt register (six review-dependent detections) and the open-work list carry forward intact as the conformance backlog. See ADR-0001.
