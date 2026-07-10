# Intake Constitution

**The Constitution**

*Nineteen articles in five parts. Each article: norm, foreclosures, aphorism. Terms in italics resolve in the Ontology; rationale lives in the Commentary; implementation patterns and detection tests live in the Engineering Constraints. Articles cite each other by name.*

---

**Part I — Authority**

**Article 1 — Peerage.** A *finding* stands on the *act* that made it, never on a document. *Evidence* grounds *claims*; only acts admit them. A fact's identity never derives from a file, and no document's arrival, replacement, or removal rewrites or deletes a finding — it changes evidentiary standing only. *Forecloses:* any intake where a document is the only door; any rewrite of findings on re-upload; any component but an *actor* admitting a claim. *Every finding stands on its own act; no document owns one.*

**Article 2 — Proposal.** Nothing system-produced becomes a finding except by presented *assertion*: the claim shown to the user exactly as it will stand, the act capturing it verbatim. Unaddressed *proposals* evaporate; the workspace keeps no pending store. Rejection is a recorded act that resolves nothing and suppresses re-proposal of the declined claim. *Forecloses:* acceptance implied by proceeding; bulk assertion of the unshown; defaults that harden with time; any load-bearing queue of proposals. *The system proposes; the user signs.*

**Article 3 — Judgment.** Where facts and rules leave more than one open path, the path taken enters only by assertion. Computation may surface alternatives, recommend, or declare that judgment is required; it may not make a choice operative. *Forecloses:* computation resolving a permissible choice internally; any rule encoding a discretionary position as deterministic consequence; any default operative without assertion. *Every open path is closed by an act, never by computation.*

**Article 4 — Adoption.** Derivation runs only under machinery the user has *adopted*: a specific, versioned body of artifacts, taken up by a recorded act with actor, scope, and provenance. Adoption is bounded because the machinery is legible (Article 11) and versioned (Article 9): the user adopts declared artifacts, never the disposition of a codebase. Every derived finding traces through its run to an adoption act. *Forecloses:* derivation without an adoption on the record; adoption of anything unversioned or illegible; silent re-adoption. *What the user did not assert, the user adopted; nothing else runs.*

---

**Part II — State**

**Article 5 — Containment.** The workspace is the totality of authoritative state. Everything else holds derived representations, discardable and rebuildable without loss. A second store violates this the moment its contents become necessary — synchronization is no defense. No flow holds accepted input outside the workspace pending a later step. *Forecloses:* shadow records awaiting commit; external stores holding the only copy of anything accepted; any component whose destruction loses workspace truth. *Destroy anything but the workspace; nothing authoritative is lost.*

**Article 6 — Atomicity.** The workspace changes only by complete transitions, each an act against a specific workspace revision. An incomplete workspace is valid; a workspace that misstates what happened is not. Nothing is maintained in lockstep to stay true. *Forecloses:* partial results committed as current; mutations whose interruption leaves the workspace wrong rather than incomplete; totals synchronized with inputs rather than published (Article 13). *No committed change requires a future commit to become valid.*

**Article 7 — Supersession.** Effects are displaced only by later acts; history only accumulates. One mechanism serves all kinds; the freedom to supersede is governed by declared rules per *fact type*. Displacement propagates along *derivation edges* and *individuation edges* — no third edge — and is a consequence of the record, not a fan-out of writes. Currency is derived, never stored. *Forecloses:* editing any act or finding; deletion as a state change; a stored currency flag; any dependency affecting standing that is not one of the two edges. *Currency moves; the record stays.*

**Article 8 — Reachability.** Everything the workspace holds, the user can reach, unconditionally on progress, mode, or flow. A flow is a lens, not a door; leaving one preserves everything it collected. Incompleteness is visible, never withheld. *Forecloses:* state visible only by completing or replaying a flow; modes that conceal existing state; any gap between what the system holds and what the user may see. *What the workspace holds, the user can reach.*

---

**Part III — Meaning**

**Article 9 — Canon.** Every *citizen* names the *schema version* that defines it, and the schema is the sole authority on what it is. Published versions are immutable. Consumers conform; none carries a private notion of meaning, accepts an undeclared shape, or repairs a malformed instance. Boundary tolerance may inform proposals; it may not create a second workspace contract. *Forecloses:* tolerant readers and repairing parsers; instances unbound to a version; schema change by drift of use. *The schema, not the reader, says what a thing is.*

**Article 10 — Declaration.** The vocabulary grows only by declaration: before anything new exists in the workspace, its schema exists. A representation that acquires identity, lifecycle, or dependents has become a citizen and must be declared or discarded. *Forecloses:* provisional shapes; generic containers whose real type lives in a tag; schemas repurposed to carry new meaning under old names; nouns schematized after instances exist. *If it is in the workspace, its schema was there first.*

**Article 11 — Legibility.** All tax meaning lives in declared, versioned *rule artifacts* — inputs, conditions, operations, results, applicability, thresholds, mappings, bridges, dependencies, and whether a value may be derived at all. Rules are pure functions of declared inputs. The engine is thin: it executes what artifacts declare and contributes no tax meaning; any conforming runner yields the same findings. Generated artifacts carry full obligations plus lineage. *Forecloses:* tax meaning existing only in code; undeclared parameters, defaults, or transitions; mutable published versions; traversal or form relationships supplied by an orchestrator. *Obtuse is permitted; hidden is not.*

---

**Part IV — Computation and Record**

**Article 12 — Contract.** A *derived finding* pins the exact versions of the findings and artifacts that produced it, and everything pinned was vouched for — inputs by assertion (Article 2), machinery by adoption (Article 4). Derivation consumes findings and artifacts only, never unasserted claims, never records. When a pinned dependency is superseded, the derived finding is displaced, never rewritten. *Forecloses:* derived findings without pinned lineage; authority resting on current code behavior; per-output approval of mechanical consequences; any derivation from an unasserted claim. *Everything a derived finding names, the user signed or adopted.*

**Article 13 — Publication.** Computation touches the workspace one way: publishing complete derived findings. Eligibility is read from declared state — an unmade judgment is an unsatisfied dependency. A run may stop anywhere leaving the workspace incomplete, never wrong; published findings stand and later runs continue from workspace state. *Forecloses:* in-place mutation of dependent state; fixed form-order orchestration; eligibility decided by runner code; partial results exposed as truth; results existing only inside a run. *The runner discovers, publishes whole findings, and repeats.*

**Article 14 — Record.** Every process that reads or writes authoritative state leaves an immutable *process record* of its declared kind, identifying what it operated on, under which versions — including the governance versions of Article 19 — what it produced or displaced, what blocked it, and why it stopped. Failed executions record. Coverage observed belongs to the record; coverage available now is computed fresh. *Forecloses:* unrecorded execution; records as discardable logs; mutation after the fact; records consumed by derivation; coverage stored as a second copy of form state. *Every execution can answer for itself.*

**Article 15 — Explanation.** Every value connects to the findings, evidence, rules, acts, and runs that justify it, grounded in the record — never reconstructed. Presentation may summarize atop the record; it may not replace it. No explanation terminates at a code location or at "the software calculated it." *Forecloses:* values written, imported, transformed, or rendered without preserved justification; post-hoc narrative standing in for the record. *A value without explanation is invalid state.*

---

**Part V — Boundary**

**Article 16 — Grant.** No process consults the user's situation except under a *grant*: specific to material and purpose, visible, revocable, on the record. Holding data is not license to consult it. Every consultation leaves a record (Article 14) naming its grant and what it read. Crossing the *quarantine* is a grant like any other, made by the data's owner. *Forecloses:* context assembled from the workspace at large; ambient learning without a naming grant; presumed or bundled grants; function conditioned on unrelated grants; consultations absent from the record. *What read your data, and why, is on the record — and was yours to allow.*

**Article 17 — Context.** What is operative for a task is a declared selection the user can inspect and change: what was included, what excluded, what stands in summary for what. The system may propose context and apply declared relevance rules; its relevance judgment is never authoritative over the user's, and no distillation silently becomes the record. *Forecloses:* uninspectable context assembly; destructive distillation; hidden retrieval policy standing in for user control. *The system proposes what matters; the user decides what is in context.*

**Article 18 — Quarantine.** Personal data lives in the workspace and the pipelines serving it, nowhere else; the boundary is structural wherever structure can hold it, and grants complement walls, never replace them. Sensitivity attaches at submission and propagates by description. Everything else runs synthetic: constructed, never derived from identifiable records. *Forecloses:* fixtures, logs, prompts, or telemetry carrying personal data; development paths requiring production data; policy where architecture could stand; "synthetic" data with personal provenance. *Everything outside could be published; everything inside serves only its owner.*

**Article 19 — Filing.** Before filing, the return is a rendering with no standing. Filing is the user's assertion over a fixed representation — shown, declared, signed, transmitted — pinning everything it comprised. It is the declared boundary where a workspace act and a legal act coincide; nothing upstream carries legal weight. Amendments supersede operationally and erase nothing. *Forecloses:* treating generated forms as filed; filing what was not shown; reconstructing a historical filing from current state; transmission introducing values absent from the adopted representation. *A return is filed only by the user's act over what the user saw.*

---

Governance note, closing the document: this Constitution is a versioned artifact per the Ontology's schema entry; conflicts with the Ontology are defects requiring versioned correction; where both are silent, the Principles interpret.

Two drafting calls to flag: Article 4's aphorism states the two-vouching-forms doctrine as the whole authority model in one line — it's doing Contract's argument in Adoption's article, deliberately, since adoption is where the doctrine becomes act-shaped. And Article 14 absorbed governance-version pinning rather than giving D17 its own article; if governance versioning grows, it splits out. Engineering Constraints next — the table already routed their contents, so that draft is mostly assembly plus writing the detection clause for each entry.
