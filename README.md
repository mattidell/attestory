# Finances — Auditable Tax Computation

A personal tax return engine built so that every value on the return can answer for itself: what findings it rests on, what rules produced it, who asserted or adopted what, and when. Tax meaning lives in declared, versioned rule artifacts — data, not code — executed by a thin engine over an append-only workspace record.

This is the project's third iteration. The first proved a working return generator; the second refined the development process; the third fleshed out the conceptual layer into a ratified governance set as the basis for agent-driven development.

## Where things stand

- **Governance** (`docs/governance/`): the ratified v0.1 set — Constitution, Ontology, Engineering Constraints, Principles, Commentary. The sole contract authority for this repository.
- **Phase state** (`docs/phase-state.md`): the active phase and milestone. Currently the Foundation phase: governance installation, then the workspace kernel, derivation machinery, and a first tax slice.
- **Planning** (`PROJECT_PLANNING.md`, `docs/phases/`): the planning protocol and phase/milestone/track documents.
- **Agent guide** (`AGENTS.md`): operating rules for development agents.
- **Decisions** (`docs/adr/`) and **retrospectives** (`docs/milestone-retrospectives/`).
- **Archive** (`archive/`): the pre-governance v2 engine and historical docs. Reference only; not a source of contracts.

## Verification

```sh
python3 -m unittest            # test suite
python3 tools/governance_lint.py   # governance set structural checks
python3 -m mypy                # type checks (tools)
```

## Data safety

Nothing personal is committed: no real tax documents, no personal fact instances, no artifacts derived from personal data. Committed fixtures are synthetic and publishable. Personal work stays under ignored paths (`local-data/`, `temp/`, `private-archive/`, `uploads/`, `generated/user/`). See Article 18 (Quarantine) and the data safety rules in `AGENTS.md`.
