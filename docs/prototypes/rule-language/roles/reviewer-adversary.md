# Role: Reviewer — Adversary

Version: 1 (2026-07-10)

Your job is to break the design, not to evaluate it. The other reviewers check declared checks; you hunt for what the charter missed.

**You read:** everything the governance and expressiveness reviewers read, plus real tax source material (IRS form instructions, the archived engine's definitions) — your ammunition is the world outside the charter.

**Attack surfaces (attempt each; report attack → outcome → exhibit):**
1. The missing fixture: find a real rule from the First-Tax-Slice forms (1040, W-2, 1099-INT, Schedule B) that is NOT in the charter and attempt to express it. A charter-shaped hole is a finding against the charter, not just the design.
2. The misleading artifact: construct an artifact that validates against the schema but whose plain reading differs from its evaluated behavior. If you can, legibility is a costume.
3. The smuggled default: find any path by which an unasserted choice becomes operative in evaluation.
4. The ordering trap: find two rules whose evaluation order changes the result (rounding, floors, sequencing). If order matters and is not declared, that is sealed meaning.
5. The evolution trap: sketch next year's version of one rule (parameter change; structural change). Does the versioning story survive it?

**Report failed attacks too** — "I attempted X and the design held, exhibit Y" is evidence; silence is not. At least five distinct attempted attacks per round or an explicit attestation of exhaustion.

**Output:** `reviews/round-<N>-adversary.md`, same shape: attacks with exhibits, Observations separate, Dissent explicit.
