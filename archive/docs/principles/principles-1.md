**Facts are peers, not document children.**

A fact is authoritative because it was asserted, not because a document contains it. Documents are evidence for facts, never containers of them.

A fact is an asserted claim. The claim is content: a value, a circumstance, a relationship, a judgment about the situation the return describes. The assertion is the act that admits it — someone, at some time, on some basis, took the claim to be true here. Evidence grounds claims; assertion makes facts. The assertion event, with its basis, is the fact's provenance.

The user decides what is a fact. That is the discrepancy with the ordinary word, and its resolution: in ordinary usage no one decides facts, but here the decision is precisely what confers fact-status, and once made, the ordinary usage takes over — the claim is relied on, computed from, built upon, like any fact, until a later assertion supersedes it. The system records the decision and its basis; it never makes one.

A document is a source. It supports, corroborates, or originates claims, and a fact's link to its source is provenance, not parentage. Extraction yields claims; assertion makes them facts. Replacing or removing a document changes the evidentiary standing of the facts it supported — it does not rewrite or delete them.

This does not prohibit document-driven intake. Extract, propose, accept is an expected path. The constraint is on the resulting state, not the entry path: however a claim arrived, once asserted it stands as a peer.

This forecloses any intake model where a document is the only door a fact can enter through; any data model where facts are children of a document record; any flow where re-uploading a document silently rewrites facts; any fact whose identity is a field of a file; any component other than the user that confers fact-status.

Every fact stands on its own assertion; no document owns one, and no system makes one.

---

**Judgment lives with the facts.**

Every judgment enters the workspace as an asserted fact. Computation applies judgments; it never makes them.

A judgment is a choice among permissible alternatives — an election, a characterization, an allocation, or a position taken where the applicable facts and rules leave more than one open path. Where they determine one result, computation derives it. Where they permit more than one, the selected path must be asserted before computation may apply it.

Once asserted, a judgment is an ordinary fact: visible, attributable, and available wherever facts are used. There is no separate place decisions live.

This does not prohibit computation from surfacing alternatives, recommending a choice, evaluating scenarios, or identifying that judgment is required. It may inform a choice; it may not silently make one operative.

This forecloses any computation that resolves a permissible choice internally; any rule artifact that encodes a discretionary position as deterministic logic; any default that becomes operative without assertion; any separate decision store; and any output whose operative judgments must be extracted from code or reverse-engineered from results.

Every decision is findable as an assertion; no computation contains one.

---

**The system proposes; you sign.**

Nothing the system produces becomes a fact except by the user asserting it, presented.

A system-produced claim — an extracted value, a suggested judgment, a computed candidate — is a claim like any other. It is not workspace state, needs no schema, and may live only in derived representations, regenerated at will. It becomes a fact the one way anything does: the user asserts it.

Asserting a system-produced claim carries one precondition: the claim was presented to the user as it will be asserted. A signature over something unseen is not a signature.

An unsigned claim simply remains unasserted. Coverage showing what awaits decision is a derived view, rebuilt from sources and facts; nothing is stored, promoted, or escalated, and no flow requires resolving a claim to proceed.

This forecloses any path from system output to fact that bypasses presented assertion: acceptance implied by proceeding, bulk operations that assert what was never shown, defaults that harden with time, any store of pending proposals that becomes load-bearing.

Every system-produced fact was seen, then signed; everything unsigned is merely not yet asserted.

---

**No state exists outside the workspace.**

The workspace is the totality of authoritative state. Everything else in the system, whatever it is — anything that renders, computes, transports, or remembers — holds at most a derived representation: discardable and rebuildable from the workspace at any time, with nothing lost.

This is a claim about scope, not synchronization. The problem with an outside copy is not that it might go stale; it is that it exists. A perfectly maintained second store is as foreclosed as a drifting one, because the moment state elsewhere becomes load-bearing, the workspace stops being the record and starts being one participant in it.

This does not prohibit transient representations — renders, computed views, in-flight buffers. The constraint is that none of them are ever the only place something true lives.

This forecloses any component whose destruction loses information: any flow that holds accepted user input outside the workspace until final submission; any execution state that becomes the only place an accepted fact, decision, or completed result exists; any store that must be written back to be preserved.

Destroy anything but the workspace; rebuild it; nothing is lost.

---

**Every change is complete.**

The workspace changes only by complete state transitions. Multi-step work may occur, but intermediate execution is never authoritative workspace state. A result enters the workspace only when it is complete and valid as a result.

An incomplete workspace is valid. Facts may be missing, proposals unresolved, current computations unavailable. What cannot exist is a workspace that misstates what has happened because an operation stopped partway.

Authoritative inputs are recorded directly. Dependent results are published as complete outputs, each tied to the exact versions of the inputs it consumed. Nothing must be updated in lockstep to keep the workspace valid: a pipeline may hold intermediate execution, but it crosses into workspace state only by publishing a complete output.

This does not prohibit transactions, temporary files, queues, checkpoints, caches, or persisted execution progress. These may support execution and recovery, but they may not carry unfinished truth on which the validity of the workspace depends.

This forecloses any committed change that requires a future commit to become valid. Including: mutations whose partial completion leaves the workspace wrong rather than merely incomplete; computations that publish partial results as current; derived values maintained in lockstep with their inputs rather than published as complete outputs; artifacts registered before their generation has succeeded.

No committed change requires a future commit to become valid.

---

**Nothing is gated.**

Everything the workspace holds, the user can reach. Access to workspace state is never conditioned on progress, mode, completion, or passage through a flow. A guided path is a view over the workspace, not a gate in front of it.

This is the access half of wholeness. The consistency half — now carried by the atomicity and containment principles — says the workspace never misstates itself; this half says it never hides itself. Incompleteness is visible, not withheld: a missing fact, an unresolved proposal, an unavailable computation appear as what they are, wherever the user looks.

This does not prohibit guided flows, progressive disclosure, or opinions about what to surface first. Guidance shapes attention; it may not withhold state. The test is whether the user can, at any moment, step off the path and see everything.

This forecloses any flow that must be completed before workspace state becomes visible; any mode that renders parts of the workspace unreachable; any staging that holds accepted state out of view until a later step; any distinction between what the system knows and what the user may see.

What the workspace holds, the user can reach.

---

**Every value carries its explanation.**

A value is not valid merely because it appears in the workspace, a worksheet, a form, or a generated return. Every value must remain connected to the facts, sources, rules, decisions, assumptions, and computations that justify it.

Provenance is part of the explanation. The system must be able to show where a value came from, what touched it, how it changed, and why its current form is justified.

Explanation is grounded in the record, never reconstructed after the fact. A plausible story about where a value probably came from is not an explanation.

This does not mean every explanation must be shown in full all the time. The product may summarize, collapse, simplify, or guide. But simplification must sit on top of the record, not replace it. A user must be able to move from any value to the evidence and reasoning underneath it.

This forecloses any code path that produces or alters a value without preserving its explanation, and any feature that substitutes post-hoc narrative for the record.

A value without explanation is invalid state.

---

**Schema is canon.**
Everything the workspace holds is an instance of a declared schema, and the schema is the sole authority on what that thing is. Asserted facts, derived facts, form instances, intermediate products of computation — each names the schema it instantiates, and its meaning is what the schema says, not what any consumer takes it to be.
Schemas are themselves workspace citizens: versioned, inspectable data. Every instance is bound to a specific schema version. "Declared" means declared here — a shape that exists only as an assumption in code, a parser's tolerance, or a convention between two components is not a schema, it is a private understanding, and private understandings are how meaning escapes the record.
The distinction is between definition and interpretation. A schema defines; consumers conform. No renderer, rule, mapping, or engine may carry its own notion of what a state means, be liberal in what it accepts, or repair malformed instances into plausible ones. If two components disagree about an instance, the schema adjudicates — one of them is wrong, and it is discoverable which. Tolerance at the boundary is not robustness; it is a second, unwritten schema.
This is what makes the workspace enterable anywhere. Because every state between transitions is a schema instance, there is always a defined state to inspect, to stop at, or to begin from. The lattice of forms and facts has no private interiors — no stretch where the data is "between shapes" and only one component knows how to read it.
This does not prohibit derived representations — renders, denormalizations, convenience shapes for a screen or an index. Those are discardable views, already governed by containment; this principle claims workspace state. Nor does it require schemas to be simple. The contract permits obtuse; it forbids hidden.
This forecloses any workspace state without a schema; any instance unbound to a schema version; any component that is a second authority on meaning — tolerant readers, repairing parsers, consumers with private interpretations; and any schema change that occurs by drift of use rather than by a new version.
Every thing in the workspace names its schema; the schema, not the reader, says what it is.

---

**No new noun without a schema.**
The system's vocabulary grows only by declaration. Before anything new can exist in the workspace — a new kind of fact, artifact, record, or relationship — its schema exists first. There is no provisional state, no experimental shape, no "we'll formalize it later."
Schema-is-canon governs the stock; this principle governs the flow. The stock principle says everything in the workspace names its schema; this one says the moment of vocabulary growth is the moment of maximum scrutiny, because an undeclared noun admitted once is a private understanding forever — every consumer that touched it while it was shapeless carries its own notion of what it was, and no later schema can recall those interpretations.
New nouns arrive in families, not one at a time. Most vocabulary growth is not new nouns at all: a new form, a new field, a new rule is a new instance of an existing family — form schemas, field schemas, rule artifacts — manufactured by declared generators from declared sources. The thousandth field schema is data entry. What this principle guards is the rarer event: a claim that cannot be expressed as an instance of any existing family. That claim is a modeling decision, and the friction is the point — the demand for a schema forces the question "what is this thing?" to be answered before the thing exists, not archaeologically after.
The friction is deliberate and it is cheap where it should be cheap. Declaring a schema for a genuinely new noun is a small act — identity, shape, version. What it prevents is expensive: the untyped payload that a tag and three consumers "understand," the side table that accretes meaning, the field repurposed to carry something its schema never said.
This does not prohibit exploration. Derived representations, prototypes outside the workspace, and claims not yet asserted need no schema — they are not workspace state. The gate stands where the workspace begins.
This forecloses any workspace state admitted before its schema; any generic container whose real type lives in a tag and its consumers; any repurposing of an existing schema to carry a new meaning under an old name; and any noun whose schema was reconstructed after instances already existed.
If it's in the workspace, its schema was there first.

---

**Derivation logic is legible data.**
The rules that determine form applicability, field values, dependencies, mappings, and movement across forms are declared as inspectable data, not hidden in executable code. The artifacts carry the tax meaning; nothing else does.
Legibility means more than machine readability. A declared rule identifies the inputs it depends on, the operation it applies, the conditions under which it applies, and the result it may produce. The complete computational meaning of a form is discoverable from its declared artifacts — a configuration file a human cannot recover the rule from is sealed behavior in a data format.
Every rule artifact has identity and version, and is typed against the schema states it consumes and produces. Changing a rule means publishing a new version; a published version is immutable. Derived facts pin the exact rule versions that produced them, and a pinned version that can silently change pins nothing.
Derivation logic includes more than arithmetic. Thresholds, parameters, applicability conditions, field mappings, dependency relationships, cross-form bridges, and the rules governing whether a value may be derived at all are declared logic. This closes the common loophole: a system whose formulas are declarative while traversal, triggering, and form relationships remain hardcoded has sealed its most consequential meaning and exposed the rest.
The artifacts carry the meaning; code executes it. The runner may parse, validate, schedule, compile, and optimize, but it may not supply a rule, dependency, default, mapping, bridge, or execution-order effect that the artifacts do not declare. The engine is thin: it contains no tax meaning.
This legibility is what the contract stands on. The user signs asserted facts individually and adopts the derivation machinery wholesale, and that adoption is bounded rather than blank precisely because the machinery holds nothing that could not be read. What was adopted is a specific, versioned set of artifacts — not the current disposition of a codebase.
Every derived fact remains connected to the exact declared logic that produced it. An explanation may present that logic in simpler terms, but it may not terminate at a code location, an opaque runner trace, or a statement that the software calculated the result.
This does not require the logic to be simple, nontechnical, or stored in one format. It may be generated, compiled, indexed, or rendered through more accessible views — a schema or rule generator is itself a rule artifact of this kind, legible and versioned, its outputs carrying provenance through generator and source alike. The authoritative meaning must remain inspectable in the declared artifacts. Declared logic may identify permissible alternatives or state that judgment is required; it may not encode a discretionary choice as a deterministic consequence.
This forecloses any tax rule whose meaning exists only in implementation code; any dependency or cross-form transition created by runner behavior; any hardcoded threshold, parameter, mapping, or undocumented default absent from the declared artifacts; any rule without version identity, and any change that alters what a published version means; and any derived value whose operative logic can be discovered only by inspecting code or reverse-engineering results.
Given any derived value, its operative tax logic is findable in declared, versioned data; the runner contains no hidden tax meaning.

---

**Computation publishes facts.**
Computation touches the workspace in exactly one way: it publishes complete derived facts. It does not mutate form state in place, maintain synchronized totals, or assemble an opaque result at the end. Whatever happens inside a run, only whole facts cross the boundary.
The runner works by saturation. It applies eligible derivations to workspace facts and publishes their complete results as derived facts; published facts become inputs to further derivation, and the runner repeats from the resulting workspace state until no additional derivations are eligible or progress requires missing facts or judgment. The return is done when the terminal forms' derivations have fired; otherwise the workspace honestly shows how far derivation could reach.
Eligibility is determined by declared state. A derivation may run only when its declared inputs, conditions, schema versions, rule versions, and required judgments are satisfied — an unasserted judgment is an unsatisfied dependency, not a choice the runner may make. The runner discovers what can run from workspace facts and derivation artifacts; it does not contain a procedural return flow or privately decide what comes next.
A derivation may involve many internal operations, but its results enter the workspace only as a complete publication. Once published, a derived fact is valid workspace state; it does not depend on a later derivation or a completed run to become true. A run may therefore stop at any point without leaving the workspace wrong: facts already published remain valid, unfinished execution has no authority, and a later run continues from workspace state rather than repairing partial computation or reconstructing a private result model.
Coverage — what could fire now, what blocks it, what is missing one step back — is a query over declared dependencies against present facts: derived, never stored, visible to anyone. No backward chain from an empty line to its distant causes is promised; a hole appears as a visible ineligible derivation, not a runtime surprise.
This does not prohibit caching, checkpoints, queues, parallel execution, or incremental evaluation. They may support execution, but no authoritative result may exist only inside them. Determinism and the absence of computational memory are granted by the state principles, not re-argued here.
This forecloses any monolithic return-generation operation whose authoritative result exists only at completion; any fixed form order or hidden orchestration sequence; any runner behavior that makes a derivation eligible without declared dependencies; any partial result exposed as workspace truth; any total or rollup maintained in lockstep with its inputs; and any computed value that exists only inside a run.
Delete every derived fact; rerun; the same facts return.

---

**Every run leaves a record.**
Every execution of derivation produces an immutable run record: an account of what happened, kept as authoritative workspace state.
A run record identifies the run — the workspace, schema, and rule versions it executed against — and reports its course: the derivations considered and executed, the facts published, the paths blocked and why, the dependencies or judgments still required, any execution errors, and the field and form coverage reached. It is the record of an event, so it is immutable by nature: a past run cannot become stale, only superseded in relevance by later runs.
The run record is what grounds explanation in the record rather than reconstruction. Version pins on a derived fact say what produced it; the run record says what occurred — including what did not fire, which no version pin can carry. When the explanation principle demands that a value's story never be reconstructed after the fact, this is the record it stands on.
A run record is evidence, not a fact. It does not participate in derivation, supply missing values, determine tax treatment, or serve as a maintained copy of form state. Facts survive the run and feed later runs; the record describes the boundary one run reached. The two never trade roles: coverage observed by a past run lives here; coverage available now is a query against present facts, computed fresh.
Run records are workspace state in full standing: they cannot be rebuilt from current facts — the blocked paths and errors of a past run are not derivable from what the workspace holds today — so their destruction loses information, and by the containment test that makes them authoritative, not scaffolding. They are a noun, and they carry a schema, like every noun.
This does not require records be verbose, eternally retained at full granularity, or surfaced by default. Retention and presentation are product decisions; existence and immutability are not.
This forecloses any execution that leaves no record; any record implemented as a discardable log outside the workspace; any mutation of a record after its run ends; any record that becomes a load-bearing input to derivation; and any explanation of a value that terminates at a reconstruction because the record was never kept.
For every derived fact, there is a run on the record that published it.

---

**Derived facts carry their contract.**
A derived fact needs no signature, because it carries one: its provenance pins the exact versions of the asserted facts and rule artifacts that produced it, and everything so pinned was already vouched for — the inputs individually, the machinery wholesale.
The vouching has two forms, and the system rests on both. Asserted facts are signed one at a time, each presented before assertion. The derivation machinery is adopted in bulk: by using the system, the user adopts its rules, mappings, bridges, and schemas as the terms under which derivation runs. That adoption is bounded rather than blank for two reasons, each guaranteed elsewhere: the machinery is legible — there is nothing in it that could not be read — and it is versioned, so what was adopted is a specific set of artifacts, not the current disposition of a codebase. Obtuse terms are permitted; hidden terms are not.
Authority is therefore compositional. A derived fact contains nothing but signed inputs transformed by adopted rules; determinism guarantees the transformation added no information of its own. Requiring a signature on each derived fact would be theater — the user approving mechanical consequences of what they already committed to. The absence of per-output signatures is not a gap in the signature model; it is the signature model working.
This principle is where the two paths meet, and the boundary runs on both sides of derivation. Before it: nondeterministic production — extraction, suggestion, drafting — yields claims, which become facts only by presented assertion; derivation begins after assertion, where the inputs are fixed. After it: the return the runner reaches is a view over derived facts, not a noun. The filed return is a noun — an asserted fact, sealed by the jurat, its provenance pinning every fact, rule, and schema version it comprised at the moment of signature. Filing is the largest assertion in the system, not the last derivation.
This does not make derived facts immune from challenge. Superseding an input fact, or adopting a new rule version, changes what derivation produces — the contract binds a derived fact to what it was derived from, not to permanence.
This forecloses any derived fact that does not pin the versions of its inputs and rules; any per-output approval flow that re-signs mechanical consequences; any derivation from unasserted claims; any output whose authority rests on machinery the user could not have read; and any treatment of the pre-filing return as an object with standing of its own.
Every derived fact names what it came from; everything it names, you signed or adopted.

---

**Synthetic by default, personal data quarantined.**
Everything in the system runs on synthetic data unless it is doing the one thing personal data exists for: preparing this user's return. Development, testing, demonstration, evaluation, tooling, and every generated artifact default to synthetic; personal data appears only inside a quarantine whose boundary is architectural, not procedural.
The quarantine is a place, not a practice. Personal data lives in the user's workspace and in the pipelines that serve it, and nowhere else — not in fixtures, logs, error reports, traces, examples, prompts, caches, or telemetry. The boundary is enforced by structure: components outside the quarantine cannot reach personal data, rather than being trusted not to look. A policy that says "don't copy real data into tests" is a procedure; a test environment with no path to real data is a quarantine.
Synthetic-by-default is what makes the quarantine livable. The system's full surface — every form, rule, bridge, and edge case — must be exercisable, demonstrable, and debuggable on synthetic workspaces that are structurally identical to real ones: same schemas, same rule versions, same pipelines. Because schemas and rules are legible, versioned data, a synthetic workspace is cheap to manufacture and indistinguishable to the machinery. If a bug can only be reproduced with real data, that is a defect in the synthetic tooling, and the fix is better synthesis — never a copy.
Run records and provenance sit inside the quarantine with the facts they describe. A record of what derivations fired on a real workspace is personal data — coverage of a person's return discloses the shape of their circumstances. Evidence inherits the sensitivity of what it evidences.
This does not prohibit the user moving their own data — export, sharing with a preparer, filing itself are user-controlled crossings of the boundary, which is the adjacent principle's territory. Nor does it prohibit aggregate or derived measures leaving quarantine where they are constructed not to carry any individual's data — but constructed-not-to-carry is a property to be demonstrated, not assumed of anything that looks statistical.
This forecloses any test fixture, example, demo, or benchmark drawn from real workspaces; any log, trace, or error report that captures personal data outside the quarantine; any development path that requires production data access; and any boundary maintained by policy where architecture could maintain it instead.
Everything outside the quarantine could be published; everything inside serves only its owner.

---

**The user controls the context.**
Nothing about the user's situation enters the working context of any assistive process except by the user's grant, and every grant is visible, specific, and revocable. What the system's intelligence knows about you is a decision you made, not a side effect of using the product.
The workspace holds everything; the context holds what you offered. These are different scopes with different masters. The workspace is total by design — that is the containment principle's job. The context of any process that reads your situation — an extraction pass, a suggestion engine, a drafting aid, any model consulted along the way — is assembled per grant, from what the user placed in reach. Holding data is not license to consult it.
A grant is specific to purpose and scope. "Use my uploaded W-2 to propose facts" is a grant; a standing ambient permission to "improve suggestions" is not — it is the absence of one. Grants compose the way facts do: visible, attributable, revocable, on the record. Revocation ends future use; what a past grant produced is governed by the record, which shows what was consulted and when.
Every consultation is on the record. Which sources, facts, and artifacts entered a process's context is part of that process's run record — so "what did the system read to produce this suggestion?" is answered from evidence, never from trust. A claim proposed to you carries the provenance of what was consulted to produce it, before you decide whether to sign it.
This does not require consent theater. Grants can be sensible in grain — a document offered for extraction is offered for extraction, without per-field ceremony — and the product may propose useful grants. It may not presume them, bundle them, or condition unrelated function on their acceptance.
This forecloses any process whose context is assembled from the workspace at large rather than from grants; any ambient learning from the user's data without a grant that names it; any consultation absent from the record; any grant whose scope is discoverable only by observing what the system seems to know; and any function held hostage to an unrelated grant.
What read your data, and why, is always on the record — and it was always yours to allow.
