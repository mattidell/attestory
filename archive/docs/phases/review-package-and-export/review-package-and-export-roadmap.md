# Review Package and Export Roadmap

## Roadmap

### Milestone 1: Export Package Contract

Define the package manifest, included artifacts, provenance fields, path rules, and unsupported-scope disclosures.

This milestone matters because export packages become durable artifacts and need explicit schemas before generation.

### Milestone 2: Synthetic Review Package Generation

Generate deterministic synthetic review packages from completed workspace runs.

This milestone matters because synthetic package generation proves the contract without introducing personal data risk.

### Milestone 3: Human-Readable Review Packet

Create a concise human-readable review packet that summarizes source inputs, validation, coverage, resolution, return outputs, warnings, and unsupported fields.

This milestone matters because users need a portable explanation, not only raw JSON artifacts.

### Milestone 4: Personal Export Controls

Enable personal export packages only after local path, deletion, redaction, and ignored-output guarantees are tested.

This milestone matters because export is a high-risk personal data workflow.

### Milestone 5: Package Verification And Reproducibility

Add verification tools that inspect package manifests, included artifacts, checksums or content references, and reproducibility for synthetic packages.

This milestone matters because review packages should be trustworthy and easy to audit.

## Status

Phase status:
- Future high-level phase.

Active milestone:
- None.

Implementation notes:
- This phase should not claim official filing support.
- Milestone plans should be created under `docs/phases/review-package-and-export/milestones/` before implementation.
- Export package contracts should be schema-first.

Project impact:
- Export schemas.
- Review package generation.
- Artifact manifests.
- Documentation and disclosures.
- Data safety tests.
