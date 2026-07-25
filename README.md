# Finances — Auditable Tax Computation

A personal tax return engine built so that every value on the return can answer for itself: what findings it rests on, what rules produced it, who asserted or adopted what, and when. Tax meaning lives in declared, versioned rule artifacts — data, not code — executed by a thin engine over an append-only workspace record.

This is the project's third iteration. The first proved a working return generator; the second refined the development process; the third fleshed out the conceptual layer into a ratified governance set as the basis for agent-driven development.

## Where things stand

- **Governance** (`docs/governance/`): the ratified v0.1 set — Constitution, Ontology, Engineering Constraints, Principles, Commentary. The sole contract authority for this repository.
- **Phase state** (`docs/phase-state.md`): the active phase and milestone. Currently the Foundation phase: governance installation, workspace kernel, derivation machinery, and first tax slice are complete; the Source Completeness And Interest Slice milestone is in implementation. Its product is the recorded closure/horizon substrate plus an honest Form 1099-INT box-1 subtotal — deliberately not Form 1040 line 2b, because box-1 closure never authorizes a claim about total taxable interest (ADR-0016).
- **Planning** (`PROJECT_PLANNING.md`, `docs/phases/`): the planning protocol and phase/milestone/track documents.
- **Agent guide** (`AGENTS.md`): operating rules for development agents.
- **Decisions** (`docs/adr/`) and **retrospectives** (`docs/milestone-retrospectives/`).
- **Archive** (`archive/`): the pre-governance v2 engine and historical docs. Reference only; not a source of contracts.

## Verification

```sh
pytest                         # full suite, parallel gate run (~26s; pytest.ini sets -n auto)
python3 -m unittest tests.<module>  # targeted run while iterating (~seconds); e.g. tests.derivation.test_explanation_cli
python3 tools/governance_lint.py   # governance set structural checks
python3 -m mypy                # type checks (tools)
python3 tools/foreman_context.py --ref HEAD --format markdown  # advisory foreman re-entry routing
python3 tools/audit_push_envelope_posture.py  # local synthetic hook/bypass posture
python3 -m packages.kernel.runners.inspect_workspace --workspace packages/sample_data/kernel/demo_workspace
python3 -m packages.derivation.runners.derive --scenario packages/sample_data/derivation/scenarios/first_slice/scenario.json
python3 -m packages.derivation.runners.derive --scenario packages/sample_data/tax/scenarios/two_w2_same_employer/scenario.json
python3 -m packages.derivation.runners.derive --scenario packages/sample_data/tax/scenarios/closure_backed_zero_1099int/scenario.json
```

The `derive` runner executes a rule package over the operation-semantics canon and prints each derived value with an explanation tree — the rule that produced it, the findings it consumed (recursing into derived inputs), and the parameters, canon, adoption, and governance it stood on. Explanation is a walk of the finding's pins, never a re-evaluation. The `first_slice` scenario is synthetic demo machinery; the `packages/sample_data/tax/scenarios/` scenarios exercise the real tax content — synthetic W-2 box-1 findings deriving 2025 Form 1040 line 1a, and synthetic Form 1099-INT box-1 findings deriving the B1 source subtotal, including the closure-backed empty-family zero that pins its adopted mapping and closure authority.

`audit_push_envelope_posture.py` is deliberately not a push guard. It builds a
disposable local Git fixture to demonstrate two facts: the installed hook
refuses a seeded marker when Git runs it, and `git push --no-verify` bypasses
that hook. Its `credential_confinement: "unestablished"` result is the point;
it neither examines this clone's credentials/hooks nor protects an owner push.

`python3 tools/audit_push_envelope_posture.py` creates only a fresh temporary
repository and local bare remote. Its JSON record verifies installed hook bytes
and a hooked seeded-marker refusal, then honestly reports that a raw
`git push --no-verify` can reach that synthetic remote. It reports credential
confinement as `unestablished`; it neither contacts a network remote nor
inspects credential material.

## Data safety

Nothing personal is committed: no real tax documents, no personal fact instances, no artifacts derived from personal data. Committed fixtures are synthetic and publishable. Personal work stays under ignored paths (`local-data/`, `temp/`, `private-archive/`, `uploads/`, `generated/user/`). See Article 18 (Quarantine) and the data safety rules in `AGENTS.md`.
