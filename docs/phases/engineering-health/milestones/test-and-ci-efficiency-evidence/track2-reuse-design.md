# Track 2 reuse — schema check and historical lattice

Audience: Builder, reviewer.

Two pure repeats from the P0 ranking. Neither memo changes a result, a refusal, or a contract. Current-lattice rebuilds after the fact state changes stay out of scope.

## Fact-type `value_schema` check

**Reused.** A successful `Draft202012Validator.check_schema` of one fact type's `value_schema`.

**Key.** `(canonical JSON, jsonschema version, draft)`. Canonical JSON is `json.dumps(value_schema, sort_keys=True, separators=(",", ":"), allow_nan=False)`. The version is the installed jsonschema distribution version, read once with `importlib.metadata.version("jsonschema")`. The draft is `Draft202012`, the validator class the check calls. `check_schema` depends only on that document, that library, and that draft. The fact-type id does not change the verdict. A document that cannot be serialized, or that is not strictly a JSON tree (dicts with string keys, lists and JSON scalars), is not keyed and is checked on every call: `json.dumps` writes a tuple like a list, yet `check_schema` accepts a list where Draft 2020-12 requires an array and rejects the tuple, so a dump that collides with a different object is not a key.

**Why the key is enough.** Two calls with the same canonical document, the same jsonschema version, and the same draft ask the same question. A changed schema, including a readoption that keeps the fact-type id, is a different document and a miss. A different library version or draft is a different key.

**Lifetime.** Process-local ordered map, capped at 4096 successes. Past the cap, the oldest success is dropped and checked again if it returns. Nothing is written to disk and nothing is shared across processes. Only a success is stored. An invalid schema is not stored, so the next fold misses, calls `check_schema`, and raises again.

**Every call still runs** `registry.validate_declared(fact_type)` and the duplicate identity-key check. This memo does not cover them, so they are not skipped. `validate_declared` may hit the registry's own verdict memo; that is a separate memo and this track does not change it. On failure, `SchemaError` is raised as `FactModelError` with the same message as before, including the fact-type id of this call.

## Historical lattice

**Reused.** The dict returned by `facts_of(state, include_displaced=True)`. Currency builds it in `_declared_edges`. The memo sits on that call, so every historical build shares one identity key. `facts_of(state)` without the flag is the current lattice. It is not this memo. It stays on `_CurrentLatticeHolder` in `findings.py`.

**Key.** Exact `KernelState` object identity (`is`), the same boundary as `_CurrentLatticeHolder.for_state`. Not equality, not a digest, and not the fact-type ids.

**Why the key is enough.** `KernelState` is a frozen dataclass. Assigning a field raises `FrozenInstanceError`. Each applier copies the top-level `fact_types` and `entities` mappings and returns `replace(...)`, a new object. The historical lattice reads fact-type id, nature, and identity keys, and entity id, kind, and status. The fold does not write those nested documents after the object exists, so an identical object cannot have gained or lost a fact. Findings are not an input to the lattice. A later finding act that keeps the same `fact_state` may reuse it. `compute_currency` still walks corrections, withdrawals, retractions, migration roots, superseded entities, and the closure on every call.

Nested fact-type and entity documents are the act-payload objects, stored by reference. A caller that mutates a payload already held by a live state could change that projection without a new object. The kernel fold does not do this. It is the same limit the current-lattice holder already accepts inside one projection.

**Lifetime.** One entry per live state: `id` plus a weak reference. `KernelState` is not hashable, because `fact_types` and `entities` are dicts, so this is not a `WeakKeyDictionary`. Lookup still requires the weak reference to be that object. When the state is collected, the callback drops the entry. The lattice does not outlive the state, and a recycled id cannot hit a dead entry. A different object is a miss. `replace` after an entity supersession or a member transition returns a new object, so that state builds its own lattice.

**Failure.** The build has no soft failure. The lattice is stored only after it returns. Currency refusals are computed from the record on every call, not from a stored view.
