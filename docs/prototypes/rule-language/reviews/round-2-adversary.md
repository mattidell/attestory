# Review Round 2 — Adversary (comparative: it2 vs it1)

Reviewer: fresh resumption, 2026-07-10. Seat reopened after a prior session (codex, claimed `bc8dc33`) halted mid-review with nothing landed; this is a from-scratch attack run per `reviews/round-2.md`.

Artifact under review: rival design on branch `prototypes/rule-language/it2` at `623957c`, directory `rival-rule-language/`, plus `docs/prototypes/rule-language/examination-it2.md` and charter v2. Comparison baseline: `reviews/round-1-adversary.md` (attacks against `exhibits/rule-language/it1`).

Process disclosure: I read `SEAT.md`, `process-log.md` (event-only entries per v3 hygiene — no round-2 outcome summaries present for governance or expressiveness), `harvest-notes.md` was not needed, `charter-it1.md` v2, `examination-it2.md`, `reviews/round-1-adversary.md`, and the governance set (`constitution.md`, `engineering-constraints.md`). I did **not** read `reviews/round-2-governance.md`, `reviews/round-2-expressiveness.md`, or any round-2 commit-message body before writing this review, per independence rule v3.

Verification command run in a worktree at `$CLAUDE_JOB_DIR/tmp/rule-language-it2-adversary-r2` (outside `main`, per builder/reviewer hygiene):

```sh
python3 -m unittest discover -s rival-rule-language/tests -v
```

Result: 8/8 passed, matching the examination's claim (fixture expectations/blocking, double-run equality, shuffled-order equality, F13 divergence, package closure/scope, negative identity validation, bridge-deletion attribution, no tax identifiers in evaluator code).

All attacks below were run via `evaluator.run_case(..., rules_override=, package_override=, adoption_override=)` against the shipped artifacts, without modifying any committed file. The attack script is not committed (scratch tooling in the worktree, per the round's evidence-via-command convention — commands are reproducible from the snippets below).

## Part 1 — Attack parity (round-1 successful attacks re-run against it2)

### Parity 1 (was round-1 Attack 2) — Misleading artifact: undeclared operation smuggling

**Still succeeds, and reveals a sharper problem: the published JSON Schema is never invoked at runtime.**

`schemas/prototype.schema.json` declares a closed `expr.op` enum and `additionalProperties: false` — on paper, tighter than it1's schema, which admitted arbitrary JSON. But grep across the branch shows no `jsonschema` import and no reference to `prototype.schema.json` anywhere in `evaluator.py` or `tests/test_prototype.py`. The only runtime gate is the hand-rolled `validate_citizen`, which checks solely `kind`, `schema_version` (a `const` match), and an identity-prefix regex — it never inspects `when`, `value`, `role`, `requires`, or `blocked`.

Exhibit: constructed a rule artifact copying `f1.wages-to-1040-line1a`'s shape but with `"value": {"op": "executor_secret_tax_rule", "meaning": "not declared anywhere in the expr grammar"}`, added to both the rules list and the package's member list (to satisfy closure).

```text
validate_contract: PASSED (bogus op artifact accepted as contract-conformant)
run_case: CRASHED (uncaught Invalid) -> Invalid("undeclared expression operation 'executor_secret_tax_rule'")
```

Outcome: successful attack, comparable severity to it1's, with a worse blast radius. Like it1, the artifact passes every static check the design actually runs (`validate_contract`) — the "misleading" property holds. Unlike it1 (where the finding stopped at "schema_errors 0"), it2's failure mode at evaluation time is not silent misbehavior but an **uncaught exception that propagates out of `run_case` and aborts the entire run** — every other rule's pending publications for that revision are lost, not just the bogus rule's. This is a bigger blast radius than a single wrong finding: one schema-conformant (by the design's own enforced contract) artifact takes the whole derivation down. It also means the design's central legibility claim — Article 9, "the schema is the sole authority on what it is... none carries a private notion of meaning" — is unverified for this design: `schemas/prototype.schema.json` and the runtime contract are two different, disconnected things, and only the looser one (`validate_citizen`) actually governs.

Disposition pressure: same as round 1 — not ratifiable as-is. The fix is not "write a tighter schema file" (it2 already has one); it is wiring that file (or an equivalent) into the actual validation path, with `Invalid` from evaluation treated as a blocked-with-reason outcome rather than an unrecoverable crash.

### Parity 2 (was round-1 Attack 3, secondary finding) — Smuggled default: absent source vs. asserted zero

**Still succeeds, and it2 has no declared mechanism at all to close this — narrower than it1's partial answer.**

Exhibit: ran the Schedule B fixture with `int1099.box3` fact omitted entirely versus explicitly asserted at `"0"`:

```text
no int1099.box3 fact at all        -> interest.taxable, schedule_b.line3 = ('1900', '0')
explicit int1099.box3 = 0 asserted -> interest.taxable, schedule_b.line3 = ('1900', '0')
identical: True
```

Same probe on wages — no W-2 fact at all versus an asserted `w2.box1 = 0`:

```text
no w2.box1 fact at all (no W-2 income) -> form1040.line1a = 0
explicit w2.box1 = 0 asserted           -> form1040.line1a = 0
```

Outcome: successful attack, same class as it1's secondary finding. `collect` returns `[]` for a symbol with zero matching facts, and `add([])` is `0` — a taxpayer who never had a 1099-INT, or a workspace still missing a W-2 the user hasn't entered yet, is computationally indistinguishable from one who affirmatively asserted a zero-value source. it1 at least had an explicit (if permissive) `required: false, cardinality: many` declaration naming this behavior; it2's rule-artifact schema has **no requiredness or cardinality vocabulary at all** for `collect` targets — there is no artifact-level place to declare "this source set is closed" versus "this source set is simply unpopulated so far." On the contract-tightness axis this round is scoring, it2 is looser here, not tighter.

Disposition pressure: unchanged from round 1 — require source-set closure (or fact-universe closure) to be artifact-declared before an optional-many `collect` can publish a zero. it2's flatter `requires` list needs an additional declared concept to carry this; it currently has nowhere to put it.

### Parity 3 (was round-1 Attack 4) — Ordering trap: duplicate output ownership

**Contract hole still present; the specific symptom round 1 demonstrated (corpus-array-order dependence) is fixed.**

Exhibit: added two rules both `publishes: "form1040.line1a"` (`rule:a.rogue-first` → 999, `rule:z.rogue-last` → 100000), added both to the package member list.

```text
validate_contract: PASSED (two artifacts may claim the same 'publishes' symbol)
form1040.line1a resolves to: 999 (winner picked by sorted artifact_id, not declared conflict semantics)
same attack, source array order reversed -> form1040.line1a = 999 (same winner: confirms winner is candidate-sort-deterministic, not corpus-order-dependent)
```

Outcome: partial success, and a genuine comparative finding for the governance reviewer's tightness axis. Neither the schema (on paper) nor `validate_contract` (in practice) forbids two artifacts from declaring the same `publishes` symbol — the same contract hole as it1. But it2's evaluator sorts candidates by `artifact_id` before resolving conflicts (`for _, rule, value in sorted(candidates)`), so the outcome is deterministic and reproducible regardless of the artifacts' order in the source file or in memory — round 1's specific complaint ("array order is tax-significant") does not reproduce here. The underlying problem is unchanged, though: two schema-conformant artifacts can silently contest the same output, and the winner is decided by an implicit, undeclared rule (lexicographically-smallest `artifact_id`) that lives in evaluator code, not in any artifact. That is precisely what Article 11 forecloses — "traversal or form relationships supplied by an orchestrator" — dressed as tie-breaking instead of sequencing.

Disposition pressure: softened relative to round 1 (determinism restored) but not closed — the package or rule-artifact schema must enforce unique output ownership across a package, or the language must declare multi-publisher conflict semantics as artifact content, not evaluator convention.

### Parity 4 (was round-1 Attack 5) — Evolution trap: year identity — **attack now fails; it2 is tighter**

Exhibit: mutated a rule's `scope.tax_year` to 2026 while leaving its package-membership entry (citizen_id + version) in the 2025 package unchanged:

```text
D2 scope-escape: REJECTED as expected -> rule:f5.standard-deduction escapes package scope
```

Outcome: failed attack (design held). `validate_contract` checks every member's `scope.tax_year`/`jurisdiction`/`family` against the package's own scope, dimension by dimension, and raises `Invalid` on any mismatch. This is real evidence for the round's comparative axis: it1's rule ids embedded the year literally (`rule.2025.standard_deduction...`), which round 1 found ambiguous under a hypothetical 2026 package reusing the id. it2's rule ids carry no year (`rule:f5.standard-deduction`), and year lives only in the `scope` content field, cross-checked at validation time. `evolution-probe.md`'s F10 answer (rules persist by id, gain a new *version* when their scope changes) is consistent with what the code actually enforces — I could not make the code accept a scope-inconsistent package. This is the strongest tightening it2 offers over it1 on the identity axis.

### Parity 5 (was round-1 Attack 6) — Package integrity: closure — **attack now fails; it2 is tighter**

Exhibit: removed `rule:f6.taxable-income-floor` from the package's `members` list while leaving it in the rules corpus:

```text
D1 closure-drop: REJECTED as expected -> package closure mismatch: missing={('rule:f6.taxable-income-floor', 'v1')}; unknown=set()
```

Outcome: failed attack (design held). `validate_contract` computes the symmetric difference between `{(identity, version) for rules+parameters}` and `{(citizen_id, version) for package.members}` and rejects any mismatch in either direction (extra corpus artifacts or extra declared members). This directly closes round 1's finding that "package membership is advisory" — for id+version membership, it now is not. (See Parity 6 below for a narrower gap in the same area the closure check does not reach: the package's own `role` label per member.)

### Parity 6 (was round-1 Attack 7) — Record/act schemas too loose for the governance guarantees

**Still succeeds, same root cause as Parity 1: `validate_citizen` does not check citizen internals.**

Exhibit: constructed a `derivation-record` instance with `phase: "started"` yet carrying populated `published`/`blocked` arrays and a free-form (non-schema-shaped) `blocked` entry:

```text
bad_record (started phase, non-empty published/blocked, free-form blocked entries): ACCEPTED by validate_citizen
```

And a `rule-artifact` with a non-enum `role`, a `requires` that is a string instead of an array, and a `blocked` that is a bare string instead of an object:

```text
bad_rule (bogus role, requires not a list, blocked not an object): ACCEPTED by validate_citizen
```

Outcome: successful attack, same shape as it1's finding but for a different reason. it1's record/act *schemas themselves* were declared too loosely. it2's declared schemas (`schemas/prototype.schema.json`) are actually adequate on paper — `phase` is an enum, `blocked` items would be typed if the schema were applied, `role` is constrained — but none of that is enforced, because (as Parity 1 found) the schema file is never loaded. The governance guarantees Article 12 (pinned lineage), Article 13 (eligibility read from declared state), and Article 14 (records identifying what they operated on, under which versions) all rest on citizens actually being well-shaped; right now that rests entirely on the shipped corpus's own good behavior, not on anything the design enforces against a hostile or buggy input.

## Part 2 — New attacks earned by it2's own shapes

### Attack 7 — Package member `role` label is never cross-checked against the citizen's own `role`

Exhibit: package member for `rule:f1.wages-to-1040-line1a` says `"role":"mapping"`; the rule artifact itself declares `"role":"field-mapping"` — already two different vocabularies for the same concept, unreconciled in the schema. Relabeling that member as `"role":"bridge"` in the package:

```text
D3 role-label mismatch: PASSED (package member 'role' need not match citizen's own 'role')
```

Outcome: successful attack. Package closure (Parity 5) checks identity and version exactly, but the package's per-member `role` tag — the thing a fresh reader or an explanation renderer would use to answer "is this a bridge or a mapping?" without opening the artifact — is decorative. A package could legitimately validate while mislabeling every member's role. This bears directly on Q7 (fresh-reader recovery) and Q8 (pin roles): the design earns credit for *artifact-level* role tagging but the *package-level* copy of that same information is unconstrained, which is a legibility regression specific to introducing a second place the same fact is recorded.

### Attack 8 — A mistyped-but-well-typed elective value leaks a raw internal string as a block reason

Exhibit: asserted `filing_status = "singel"` (a plausible typo, correctly typed as a string, just not one of the five enumerated statuses) alongside otherwise-complete facts:

```text
{
  "artifact_id": "rule:f5.standard-deduction",
  "code": "OPEN_ELECTIVE_FACT",
  "missing": ["parameter:standard-deduction.2025[singel]"]
}
```

Outcome: successful attack. Charter Q3 requires "a blocked run yields schema'd reasons, not narrative," and the examination claims `blocked` supplies "a stable code and declared missing symbols." Here the `code` is stable (`OPEN_ELECTIVE_FACT`, matching the artifact's static `blocked.code`), but the `missing` entry is not the declared static reason (`["filing_status"]`) — it is the literal string form of a Python `Missing` exception raised deep inside `parameter_value`, which happens to embed the parameter id and the user's mistyped value verbatim (`parameter:standard-deduction.2025[singel]`). The code path: an elective value with an unrecognized key is not a *missing* dependency (the fact is present) but an *invalid* one, and the design has no vocabulary for that distinction — it falls through the same exception-to-narrative pipe as a genuinely absent value, quietly violating the "schema'd, not narrative" claim in the one place a real user's typo would hit it. (The same pipe would leak `"unsupported asserted rounding convention 'whatever'"` verbatim for a mistyped rounding convention — not independently re-tested, but the code path is identical.)

Disposition pressure: distinguish "dependency absent" from "dependency present but its value is not in the domain the rule needs" as declared block reasons, rather than letting the latter degrade into a formatted exception message.

### Attack 9 — A saturated, complete run can be silently indistinguishable from an incomplete one

Exhibit: ran F8 with `form1040.line33 == form1040.line24` (an exact payment, not covered by any charter F8 fixture, which only exercises strict `>`/`<`):

```text
line34 published: False   line37 published: False
line34/37 in blocked list: []
```

Outcome: successful attack, and a charter gap in the "missing fixture" sense (Attack 1's category from round 1) as much as a design hole. Q3's own framing — "a false guard is inapplicable, not blocked" — is a deliberate, declared design choice, so this is not a bug in the sense of contradicting the design's stated semantics. But it produces a real legibility trap: after a completed, saturated run, a reader inspecting the `derivation-record` for `form1040.line34`/`line37` sees neither a published finding nor a blocked entry for either — the identical signature a mid-run, unsaturated snapshot would show for those same two rules before their guards were ever evaluated. Nothing in the record distinguishes "these rules ran, their guards were false, they correctly produced nothing" from "these rules haven't been reached yet." A fresh reader needs outside knowledge of the charter (F8 is mutually exclusive, so exactly one of the two should be either present or explicitly-inapplicable) to know the run is actually complete on this point.

Disposition pressure: charter should add an F8 tie fixture; the design should consider whether a completed record should list "evaluated-and-inapplicable" rules distinctly from rules never reached, or accept this as a known, disclosed limit of "saturation" as the sole completeness signal.

## Failed attacks

- Parity 4 and Parity 5 above (year-scope escape, package closure) — both held; reported in Part 1 as the strongest comparative evidence that it2 tightened the specific holes round 1 found in it1.
- Attempted to make `range_lookup`/`bracket_fold` mis-evaluate at a bracket boundary (value exactly on a `lower`/`upper` seam) by hand-checking the F7 worksheet fixture's expected value against an independent calculation; the shipped result (`20447` for `$115,000` taxable income, single) matches a manual bracket-fold computation from `artifacts/parameters.json`'s own table. No divergence found — this is expressiveness-reviewer territory and I did not pursue it further as an adversary attack surface.
- Attempted to find a case where `pins_for` omits a governance or adoption pin for a fired rule; the pin-collection walk covers `when`, `value`, `requires`-implied facts, and always appends the firing rule's own artifact pin. Did not find a gap in the sampled fixtures; a full audit of `pins_for` against every `expr` op shape was not attempted (time-bounded, disclosed rather than silently skipped).

Nine distinct attacks attempted (six parity, three new), exceeding the five-attack minimum; two of the parity attacks failed (design held) and are reported as evidence for the comparative axis rather than as a hole.

## Observations

The comparative picture is genuinely mixed, which is itself the useful round-2 finding. it2 closed exactly the two holes round 1 found in it1's *envelope* contract — package closure and year-scope escape — with real, load-bearing runtime checks (`validate_contract`'s symmetric-difference closure test and per-dimension scope comparison). Those are the strongest, most legible improvements in the branch. But it2 did not close, and in the schema-authority case actively worsened, the *content* contract: the same gap that let round 1 smuggle an undeclared operation into it1 as a validating artifact reproduces identically here, and it2's specific version of it is worse in two ways — (a) the design ships a materially tighter JSON Schema file than it1 ever had, but that file is decorative (never loaded, never invoked), so the design's own Article 9 claim ("the schema is the sole authority") is false for the implementation as built, only true for the implementation as documented; (b) the failure mode on a bad artifact is not contained misbehavior but an unhandled exception that aborts the whole run.

The absent-source/asserted-zero hole (Parity 2) generalizes worse in it2 than in it1: it1 at least had an explicit (permissive) `required`/`cardinality` declaration site that a future revision could tighten; it2's flat `requires` list has no corresponding concept, so closing this hole needs new vocabulary, not just a stricter check on existing vocabulary.

The two new attacks in Part 2 (role-label duplication, exception-string leakage into blocked reasons) both stem from the same root pattern: it2 introduces a second, informal copy of information the primary artifact already declares (the package's per-member `role` tag; the runtime exception's message versus the artifact's declared `blocked.missing`), and neither copy is cross-checked against its primary. This is worth naming as a general watch-item for whichever design proceeds: every place a fact is expressible in two places invites exactly this class of silent divergence.

## Dissent

I dissent from treating it2 as ratifiable as-is, for the same reason as round 1's dissent against it1: the expression/citizen contract (Parity 1, Parity 6) is not yet schema-enforced in practice regardless of what the schema file says on paper, and Parity 2's absent-source hole has no declared vocabulary to close it. I do not dissent from the comparative evidence itself — the closure and scope-escape improvements (Parity 4, Parity 5) are real and should carry weight in the evaluation analysis; they are the strongest evidence yet that a schema-enumerated, closed-package design can mechanically enforce the guarantees round 1 found missing, when the checks are actually wired to run. The unresolved question for the next iteration or the ADR is not "expression trees vs. flat operations" (both builders converged there) but "how does the declared schema become the thing that actually runs" — that is a contract-wiring problem, not a grammar problem, and it2's own gap between its schema file and its validator is the clearest evidence for it produced by either iteration so far.

## Source material

- `docs/governance/constitution.md` — Articles 3, 9, 11, 12, 13, 14 (cited above).
- `docs/governance/engineering-constraints.md` — E3.1, E4.1, E6.1, E11.2, E11.3, E14.1 (contract detections these attacks probe).
- `reviews/round-1-adversary.md` — attacks 1–7 and their exhibits, re-run above.
- `rival-rule-language/evaluator.py`, `artifacts/*.json`, `schemas/*.json`, `tests/test_prototype.py` on `prototypes/rule-language/it2` @ `623957c`.

## Evaluation-analysis sign-off — 2026-07-11

Scope: bounded delta-confirmation only. I read `evaluation-analysis.md` and this review file, and did not re-run attacks, read same-round peer reviews, or perform new review work.

Result: sign off; no dispute. The analysis traces the adversary findings faithfully:

- Parity 1 and Parity 6 are represented by C6 and ratification condition §5.1: the declared schema must be the runtime authority, not a decorative file beside a looser validator.
- Parity 2 is represented by C10(a) and §5.3: absent-source versus asserted-zero needs source-set closure vocabulary.
- Parity 3 is represented by C8: duplicate output ownership is deterministic in it2 but still contract-open without package-level unique ownership or declared conflict semantics.
- Parity 4 and Parity 5 are represented by C7: it2's year-scope and package-closure checks are real comparative wins.
- Attack 7 is represented by §5.7's role-vocabulary condition: duplicated package-member roles and artifact roles must collapse into one governed vocabulary.
- Attack 8 is represented by C10(b): present-but-invalid values must not leak exception strings as block reasons.
- Attack 9 is represented by C10(c): evaluated-and-inapplicable must be distinguishable from never-reached if the record is to explain completion.

The §5 conditions cover the adversary dissent. I continue to dissent from treating either prototype corpus as ratifiable as-is, but do not dissent from using the synthesized contract as the basis for ADRs if those conditions are carried forward.
