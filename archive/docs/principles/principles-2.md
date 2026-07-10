**1. Facts are peers, not document children.**

A fact is authoritative because it was asserted, not because a document contains it. Documents are evidence for facts, never containers of them.

A fact is an asserted claim. The claim is content: a value, a circumstance, a relationship, a judgment about the situation the return describes. The assertion is the act that admits it — someone, at some time, on some basis, took the claim to be true here. Evidence grounds claims; assertion makes facts. The assertion event, with its basis, is the fact’s provenance.

The user decides what is a fact. That is the discrepancy with the ordinary word, and its resolution: in ordinary usage no one decides facts, but here the decision is precisely what confers fact-status, and once made, the ordinary usage takes over — the claim is relied on, computed from, built upon, like any fact, until a later assertion supersedes it. The system records the decision and its basis; it never makes one.

A document is a source. It supports, corroborates, or originates claims, and a fact’s link to its source is provenance, not parentage. Extraction yields claims; assertion makes them facts. Replacing or removing a document changes the evidentiary standing of the facts it supported — it does not rewrite or delete them.

This does not prohibit document-driven intake. Extract, propose, accept is an expected path. The constraint is on the resulting state, not the entry path: however a claim arrived, once asserted it stands as a peer.

This forecloses any intake model where a document is the only door a fact can enter through; any data model where facts are children of a document record; any flow where re-uploading a document silently rewrites facts; any fact whose identity is a field of a file; and any component other than the user that confers fact-status.

Every fact stands on its own assertion; no document owns one, and no system makes one.


**2. No new noun without a schema.**

Every first-class thing in the system must be declared before it can exist. If a concept has identity, state, provenance, lifecycle, relationships, or authority, it requires a schema that defines what it is.

Naming a concept in code, UI, documentation, or conversation does not make it part of the system. A noun becomes real only when its structure, boundaries, and relationships are declared in schema and instances can identify the schema version they instantiate.

This applies when introducing new facts, documents, decisions, runs, artifacts, form instances, filing records, or other workspace citizens. It also applies when an existing representation begins to acquire independent meaning. A view, cache, grouping, status, or convenience object that gains identity or becomes load-bearing has crossed the boundary and must either receive a schema or remain a discardable representation.

This does not require a distinct schema for every label, field, temporary value, or implementation type. The test is whether the concept has become independently meaningful to the product. If its loss would erase information, if users or rules may refer to it, if it has its own lifecycle, or if another object depends on its identity, it is a noun.

This principle governs vocabulary growth. Schema is canon once a noun exists; this principle governs whether a new noun may enter the canon at all.

This forecloses concepts that exist only as code classes, database tables, API payloads, UI state, or undocumented conventions; representations that quietly become authoritative; product behavior built around unnamed intermediate objects; and architectural abstractions that acquire identity or lifecycle without an explicit schema.

If the system needs to refer to a thing as a thing, that thing must have a schema.


**3. Schema is canon.**

Everything the workspace holds is an instance of a declared schema, and the schema is the sole authority on what that thing is. Asserted facts, derived facts, form instances, and published intermediate products of computation each name the schema they instantiate. Their meaning is what the schema says, not what any consumer takes it to be.

Schemas are themselves workspace citizens: versioned, inspectable data. Every instance is bound to a specific schema version. “Declared” means declared here. A shape that exists only as an assumption in code, a parser’s tolerance, or a convention between components is not a schema; it is a private understanding, and private understandings allow meaning to escape the record.

The distinction is between definition and interpretation. A schema defines; consumers conform. No renderer, rule, mapping, or engine may carry its own notion of what workspace state means, accept a second undeclared shape, or repair a malformed instance into a plausible one. If two components disagree about an instance, the schema adjudicates: one of them is wrong, and it is discoverable which.

This restriction applies to workspace state, not to interpretation at an external boundary. An extractor or importer may tolerate ambiguous or malformed source material while producing proposed claims. Before anything enters the workspace, however, it must conform to a declared schema. Boundary tolerance may inform a proposal; it may not create a second workspace contract.

This is what makes the workspace enterable anywhere. Every committed state and every published intermediate result is a schema instance, so there is always a defined state to inspect, stop at, or begin from. The lattice of forms and facts has no private interiors — no published stretch where the data is “between shapes” and only one component knows how to read it.

This does not prohibit derived representations such as renders, denormalizations, indexes, or convenience shapes for a screen. Those are discardable views, not workspace state. Nor does it require schemas to be simple. The contract permits obtuse; it forbids hidden.

This forecloses any workspace state without a schema; any instance unbound to a schema version; any component that becomes a second authority on meaning; any consumer that accepts or repairs undeclared workspace shapes; and any schema change that occurs through drift of use rather than a new version.

Every thing in the workspace names its schema; the schema, not the reader, says what it is.


**4. No authoritative state exists outside the workspace.**

The workspace is the totality of authoritative state. Everything else in the system — anything that renders, transports, indexes, caches, or temporarily processes workspace state — holds at most a derived representation: discardable and rebuildable from the workspace without loss.

This is a claim about authority, not synchronization. The problem with an outside copy is not that it might become stale. A perfectly synchronized second store violates the principle once its contents become necessary to preserve meaning. At that point, the workspace has stopped being the record and become one participant in a distributed authority.

This does not prohibit caches, indexes, queues, temporary files, execution checkpoints, or external projections. Their loss may cost time or performance, but it may not lose an accepted fact, judgment, completed derivation, filed return, or other authoritative record.

This forecloses private state held by flows or components; shadow records that must later be committed; external stores that contain the only copy of accepted information; synchronized projections that become load-bearing; and any component whose destruction loses workspace truth.

Destroy anything but the workspace; rebuild it; nothing authoritative is lost.


**5. Every change is complete.**

The workspace changes only by complete state transitions. Multi-step work may occur, but intermediate execution is never authoritative workspace state. A result enters the workspace only when it is complete and valid as a result.

An incomplete workspace is valid. Facts may be missing, proposals unresolved, or current computations unavailable. What cannot exist is a workspace that misstates what has happened because an operation stopped partway.

Authoritative inputs are recorded directly. Dependent results are published as complete outputs against a specific workspace revision. Nothing must be updated in lockstep to keep the workspace valid. Every pipeline may have intermediate execution, but it crosses into workspace state only by publishing a complete, versioned output.

This does not prohibit transactions, temporary files, queues, checkpoints, caches, or persisted execution progress. These may support execution and recovery, but they may not carry unfinished truth on which the validity of the workspace depends.

No committed change requires a future commit to become valid.


**6. Every value carries its explanation.**

A value is not valid merely because it appears in the workspace, a worksheet, a form, or a generated return. Every value must remain connected to the facts, sources, rules, decisions, assumptions, transformations, and computations that justify it.

Provenance is part of the explanation. The system must be able to show where a value came from, what touched it, how it changed, and why its current form is justified. Explanation is not a narrative generated after the fact. It is grounded in the record.

This does not mean every explanation must be shown in full all the time. The product may summarize, collapse, simplify, or guide. But simplification must sit on top of the record, not replace it. A user must be able to move from any value to the evidence and reasoning underneath it.

This forecloses any code path that writes, imports, infers, transforms, overrides, or renders a value without preserving the explanation needed to interrogate it.

A value without explanation is invalid state.


**7. Judgment lives with the facts.**

Every judgment enters the workspace as an asserted fact. Computation applies judgments; it never makes them.

A judgment is a choice among permissible alternatives — an election, a characterization, an allocation, or a position taken where the applicable facts and rules leave more than one open path. Where they determine one result, computation derives it. Where they permit more than one, the selected path must be asserted before computation may apply it.

Once asserted, a judgment is an ordinary fact: visible, attributable, and available wherever facts are used. There is no separate place decisions live.

This does not prohibit computation from surfacing alternatives, recommending a choice, evaluating scenarios, or identifying that judgment is required. It may inform a choice; it may not silently make one operative.

This forecloses any computation that resolves a permissible choice internally; any rule artifact that encodes a discretionary position as deterministic logic; any default that becomes operative without assertion; any separate decision store; and any output whose operative judgments must be extracted from code or reverse-engineered from results.

Every open path is closed by an asserted fact, never by computation.


**8. Derivation logic is legible data.**

The tax meaning that drives derivation is declared as versioned, inspectable data in the workspace, not hidden in executable code or discoverable only through outputs.

Legibility means more than machine readability. A declared rule identifies the inputs it depends on, the operation it applies, the conditions under which it applies, and the result it may produce. Its complete tax meaning must be recoverable from the artifact itself, without inspecting or experimentally probing the engine.

Rule artifacts are workspace citizens. Each has identity and version and is typed against the schema states it consumes and produces. Derived facts name the specific rule versions that produced them. Publishing a new rule creates a new version; an existing version may not silently change, because a pinned version that can change pins nothing.

The artifacts carry the tax meaning; the engine supplies general execution mechanics. Code may parse, validate, schedule, compile, and faithfully execute declared rules, but it may not supply an undeclared tax rule, dependency, default, mapping, bridge, parameter, or transition.

Derivation logic includes more than arithmetic. Form applicability, thresholds, parameters, conditions, field mappings, dependency relationships, cross-form bridges, defaults, and rules governing whether a value may be derived are all part of the declared logic. Modeling formulas while leaving traversal or form relationships in an orchestrator does not make the system legible.

Every derived fact remains connected to the exact rule artifacts that produced it. Its explanation may present those rules more simply, but it may not terminate at a code location, an opaque execution trace, or a statement that the software calculated the result.

This legibility is what makes adoption of the derivation machinery bounded. The user asserts facts individually and adopts a specific, versioned body of derivation logic wholesale. That adoption is meaningful because the machinery contains no operative tax meaning that is unavailable for inspection. The user adopts declared artifacts, not the current behavior of a codebase.

This does not require rules to be simple, friendly, or readable by everyone. Obtuse is permitted; hidden is not. Rules may be generated, compiled, indexed, or presented through more accessible views, but generation does not exempt them from identity, versioning, legibility, or provenance.

Declared logic may identify permissible alternatives, evaluate scenarios, or state that judgment is required. It may not encode a discretionary choice as though it were a deterministic consequence.

This forecloses any tax meaning that exists only in implementation code; any rule without identity or immutable version; any undeclared threshold, parameter, default, dependency, mapping, bridge, or execution transition; any engine whose domain behavior exceeds the declared artifacts; and any derived value whose operative logic can be found only by reading code or reverse-engineering results.

Given any derived fact, its operative tax logic is findable in the versioned artifacts it names; the engine contains no hidden tax meaning.


**9. Derived facts carry their contract.**

A derived fact is authoritative because it follows reproducibly from authoritative facts and judgments through an adopted set of schemas, rules, mappings, parameters, and bridges. It requires no separate assertion because its derivation introduces no undeclared judgment or tax meaning.

The derivation contract is part of the fact’s provenance. Every derived fact pins the exact versions of its inputs and the artifacts that produced it. Its value cannot be separated from that lineage, and changing an input or adopted artifact does not rewrite the earlier fact.

When a dependency is superseded, affected derived facts remain valid records of the derivations that produced them but cease to belong to the current computational state. Successor derivations publish new facts against the revised lineage.

Derived facts are peers of asserted facts in visibility, addressability, and use as inputs to later derivation. Their authority differs only in source: asserted facts are admitted by user assertion; derived facts are admitted by reproducible execution of the contract the user adopted.

This forecloses any derived fact without pinned inputs and rule versions; any result whose authority depends on the current behavior of a codebase; any silent rewriting of derived facts after their dependencies change; any computation that introduces an unasserted judgment; and any value whose derivation cannot be reproduced from workspace state.

Given the same authoritative inputs and adopted artifacts, the same derived fact and provenance must return.


**10. Computation publishes facts.**

Computation touches the workspace in one way: it publishes complete derived facts. It does not mutate form state in place, maintain synchronized totals, or assemble authoritative results outside the fact record.

The runner discovers eligible derivations from workspace state. Eligibility is declared by rule dependencies and conditions, never by code order or a procedural return flow. It publishes complete results, then evaluates again as newly derived facts make further derivations eligible. A completed run reaches saturation when no further facts are reachable, or when progress requires missing facts or an asserted judgment.

A derivation may involve many internal operations, but unfinished execution has no authority. If a run stops, facts already published remain valid and later execution continues from workspace state.

This does not prohibit staging, caching, checkpoints, parallelism, or incremental recomputation. These may support execution, but they may not become the only place an authoritative result exists.

This forecloses computation that mutates dependent state in place; totals or form values maintained in lockstep with their inputs; fixed form-order orchestration; eligibility determined by runner code; partial results exposed as workspace truth; and monolithic return generation whose results exist only when the entire process completes.

The runner discovers what can run, publishes complete facts, and repeats until nothing more is derivable.


**11. A run leaves a record.**

Every run produces an immutable account of the execution it performed. The run record identifies the workspace state, schema versions, rule versions, parameters, and engine version it evaluated. It records what became eligible, what executed, what facts were published or displaced from current use, what remained blocked, and why execution stopped.

Coverage belongs to the run record. Field and form coverage describe the boundary reached by a particular run against particular facts and contracts. Coverage is derived rather than authoritative: a run may preserve its coverage assessment, but coverage is never maintained as a second copy of current form state.

A later workspace change does not rewrite an earlier run. It creates a new run and a new record. Failed and interrupted runs remain inspectable even when they publish no facts.

This does not require preservation of every internal instruction or temporary value. The record must contain enough information to explain the run’s inputs, eligibility decisions, publications, blocked paths, coverage, failure state, and termination without reconstructing them from logs or runner code.

This forecloses opaque execution; mutable latest-run state without history; coverage detached from the run that produced it; failures with no durable account; and computed facts that cannot be connected to the execution that published them.

Every run can answer what it evaluated, what it produced, what it displaced, what blocked it, and why it stopped.


**12. The workspace is always reachable.**

All workspace state is reachable from every point in the product. No flow, mode, checklist, or stage owns access to facts, documents, judgments, rules, derived facts, or unresolved work.

Flows may guide attention, impose a useful sequence, or present only what is relevant to the current task. A flow is a lens, not a door. It may change what is emphasized; it may not change what is reachable. Leaving a flow at any point preserves everything it collected and returns the user to the full workspace.

This constraint is on access, not attention. Progressive disclosure, focused views, and simplified interfaces are legitimate presentation choices. Completing a step may advance work, but it may never be the price of seeing or touching state that already exists.

This forecloses wizard-owned state; prerequisites imposed only to gate navigation; answers visible only by replaying an interview; modes that conceal existing workspace state; and flows that discard or quarantine work when exited.

Every element of workspace state is reachable without completing a flow.


**13. The user controls the context.**

The system may focus, retrieve, summarize, and assemble workspace state for a task, but the operative context remains visible and controllable by the user. Context is a declared selection from the record, not a hidden model of what matters.

The user can inspect what was included, what was excluded, and why. The user may add, remove, preserve, or replace context without reconstructing the system’s internal reasoning. A summary may stand in for detail during use, but it may not replace, discard, or silently alter the underlying record.

This does not require the user to select every item manually. The system may propose context, apply declared relevance rules, and remember user-approved context policies. It may distill for convenience, but it may not silently turn an undisclosed distillation into the operative record.

This forecloses hardcoded context windows that cannot be inspected or changed; hidden retrieval and summarization policies; AI actions whose source context is unknowable; destructive distillation; and any feature that treats the system’s relevance judgment as authoritative over the user’s.

The system may propose what matters; the user decides what is in context.


**14. Filing is an assertion.**

Before filing, the return is a derived view over workspace state. It may be rendered, inspected, discarded, and rebuilt. It is not an independent authority and does not become a filed return merely because computation or artifact generation has completed.

Filing occurs when the user adopts a specific representation, makes the required declaration, and submits it. That assertion event creates a filed return: an asserted fact and fixed historical record that pins the facts, judgments, schemas, rules, artifacts, and representation placed before the user, together with the jurat, signature, and transmission record.

A filed return is not rewritten when the workspace changes. A correction or amendment produces another assertion and another filed return. The later filing may supersede the earlier filing operationally, but it does not erase it historically.

This does not require every filing representation to be stored as authoritative state. Only the representation actually adopted and submitted, together with its assertion and transmission record, crosses the filing boundary.

This forecloses treating generated forms as filed merely because they are complete; filing a representation the user was not shown; reconstructing a historical filing from current workspace state and treating it as the original; silently altering a filed return; and allowing rendering or transmission to introduce operative values not present in the adopted workspace state.

A return becomes filed only through the user’s assertion over a fixed representation.


**15. Synthetic by default; personal data is quarantined.**

Development, testing, demonstrations, fixtures, and examples use synthetic data by default. Personal data enters those environments only through an explicit, bounded exception and remains identifiable as personal wherever it is permitted to exist.

Synthetic data is not produced by lightly modifying a real person’s record. It is constructed independently or generated from declared structural constraints so that its provenance does not lead back to personal source material.

Personal data required for production operation remains within its declared security and retention boundaries. It is not copied into fixtures, prompts, screenshots, logs, analytics, support tools, or lower environments merely because doing so is convenient.

This does not prohibit controlled testing against personal data when the product cannot otherwise be validated. It requires the purpose, access, environment, retention, and disposal of that data to be explicit.

This forecloses fixtures derived from real returns; production records copied into development; personal documents used as demonstration material; prompts or logs that silently retain personal content; and datasets described as synthetic when their provenance begins with identifiable records.

Assume data must be synthetic unless a recorded exception says otherwise.