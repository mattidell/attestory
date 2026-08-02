# Examination — Iteration 3 (targeted repair)

Builder seat: `roles/builder.md` (iteration 3). Branch:
`prototypes/tax-citizen-families/it3`. This is **not** a clean-room iteration:
it patches the it2 exhibit (`989d9fe`) against the round-2 review gates R1–R13,
with clean-room mini-spikes only where patching would entrench a disputed
assumption. Round-2 reviews were read only as defect input for these gates.

All exhibit paths are under `docs/archive/2026-08-02-milestone-artifacts/prototypes/tax-citizen-families/it3/`. One
command reproduces every result:

```
PYTHONPATH=. python3 docs/archive/2026-08-02-milestone-artifacts/prototypes/tax-citizen-families/it3/tools/harness.py
```

It prints **203 checks, all `[PASS]`, exit 0** (captured at `it3/EVIDENCE.txt`).
The harness validates every citizen against the **published** kernel/derivation
schemas (Article 9) and the it3 schemas, runs all 17 scenarios on **both**
shipped runners (forward + reference, E11.2), and executes the gate-specific
checks. Section numbers below refer to the harness output / `EVIDENCE.txt`.

## Reused vs patched vs mini-spike

- **Reused from it2 unchanged:** `form-field.v1` schema; the box-1/box-3
  membership model for line 2b (F2); the derived-finding pin/parity machinery
  approach; the inert-citation principle.
- **Patched it2 design:** the fact-type bundle (W-2 identity keys, closure
  nature/basis); the rule set (line 1z, line-12 and line-16 guards);
  `source-citation.v1` (in-schema `resolved` invariant); the fixtures
  (now `scenario.v1` with provenance); the harness (real record rebuild,
  per-state walks, dual-runner still).
- **Mini-spikes (adopt/reject/escalate):** closure semantics
  (`it3/spikes/closure-semantics.md`, adopted fact-type reuse with corrected
  nature + a declared machinery projection contract). Source-instance identity,
  citation attachment, and the line-16 method boundary were resolved by direct
  patch (their disputes had a clear repair), documented in-line below.

## R1–R13 checklist (gate → disposition → new it3 evidence → command)

Every gate is **closed with artifact evidence**. Two carry an escalation note;
none is failed or deferred. Run the one command above; the named checks appear
in the cited section.

| Gate | Disposition | New it3 artifact(s) | Harness check (section) |
|---|---|---|---|
| **R1** two-source W-2 identity | closed | `content/bundle.tax-2025.json` (`w2-instance` entity key); `fixtures/scenarios.json` → `two_w2_same_employer` | §6 peerage; §2 `[two_w2_same_employer]` line1a=42000 |
| **R2** closure semantics decision | closed | `spikes/closure-semantics.md`; closures `nature=determinable`; `instances/positive/finding.closure-attested.json` (`basis=attested`) | §7 R2 checks |
| **R3** closure load-bearing | closed (+ escalation) | `content/closure-projection.md`; `project_closed_sets` | §7 R3(a)(b)(c) |
| **R4** coverage from records | closed | `coverage_from_record` over a real `derivation-record.v1` | §8 R4 checks |
| **R5** citation attachment model | closed | `schemas/citation-attachment.v1.schema.json`; `content/citation-attachments.2025.json`; in-schema `resolved` | §4 R5 checks |
| **R6** cross-citizen + year checks | closed | `content/evolution/*` 2026 slice; `fixtures/scenarios.2026.json` | §3 later-year positive; §4 R6 mixed-year (rule + param, both directions) |
| **R7** line 1z boundary | closed | `line1-other.closure` fact; `line1z` rule + form field | §2 `[line1z_unclosed]` blocks; `w2_and_interest` line1z=42000 |
| **R8** standard-deduction eligibility | closed | `standard-deduction-eligibility` fact; guarded `line12.standard` | §2 `std_special_condition`, `std_eligibility_unknown` |
| **R9** line 16 method boundary | closed | `tax-computation-method` fact; tax-table/rate-schedule split; `tax-table.2025.json` | §2 `high_income_rate_schedule`, `alternate_method_blocked` |
| **R10** all-elective-open saturation | closed | `fixtures/scenarios.json` → `all_open` | §2 `[all_open] no publications` |
| **R11** complete absence explanations | closed | `check_explanation_walks` (5 states) | §9 walks (1)–(5) |
| **R12** scenario/package provenance | closed | `schemas/scenario.v1`, `symbol-binding.v1`; `content/symbol-bindings.2025.json` | §1 scenario conformance; §4 provenance used |
| **R13** committed pos/neg examples | closed | `instances/positive/*`, `instances/negative/*`, `instances/expected.json` | §5 R13 checks |

## Gate detail

**R1 — two-source W-2 identity (round-2 A4/F1).** it2 keyed the wage fact only on
`{employer, tax-year}`, so two same-employer W-2s collided and the peerage check
merely hashed one key twice. it3 adds a third identity key: the **W-2 slip as a
thing** (`us.w2-slip` entity, e.g. a control number) — never the evidence
document. Two slips from one employer are now two `w2-instance` entities → two
distinct facts, executed in `two_w2_same_employer` (both aggregate to line 1a =
42000 on the runner). A reissued W-2 with the same control number is the same
fact (a correction, not a new question); evidence swap/removal leaves value and
identity byte-stable (§6). Peerage holds: the entity is a thing-citizen, the
scan is separate evidence (E1.1).

**R2 — closure semantics (A9).** Mini-spike `spikes/closure-semantics.md`
weighed elective-fact reuse, a new family, and a projection contract. Adopted:
keep `fact-type.v1` but fix the semantics — closure is `nature=determinable`
(the world determines whether you have more W-2s) with an **attested** finding
basis, not an elective tax choice. A9's specific charge (closure mis-modeled as
an election) is answered; no new schema is forced (the it2 Q1 result stands).

**R3 — closure load-bearing (A8).** it2 claimed `closed_sets` had "degraded to a
projection"; A8 correctly showed it is load-bearing. it3 stops hiding this and
**declares the machinery contract** (`content/closure-projection.md`):
`closed_sets = π(current closure findings)`, a pure total function. §7 proves all
three directions: (a) finding + projection → the closure-backed zero pins the
closure finding; (b) a stale `closed_sets` string with no finding blocks (no
zero); (c) **honestly**, finding present but projection withheld →
`SOURCE_SET_UNCLOSED` (the machinery is load-bearing). *Escalation:* whether the
ratified runner should read closure findings natively — removing the
`closed_sets` dependency — is a **machinery** decision (a separate ADR/patch),
surfaced, not worked around.

**R4 — coverage from records (A7).** it2's `coverage_report` ignored the run and
returned fixture booleans. it3 builds a real `derivation-record.v1` (via the
kernel `closing_record`) and rebuilds coverage **only** from that record: a
family is open iff its mapping rule blocked on the missing closure symbol. §8
shows a byte-identical rebuild, the interest set correctly OPEN from the
`unclosed_interest` record, and a stale stored "closed" projection **overridden**
by the record rebuild.

**R5 — citation attachment (A5).** it2 left rules/parameters/fact-types with no
citation binding and accepted a line-1a field citing the line-2b citation. it3
adds `citation-attachment.v1`: a citizen binding a citation to a subject with a
content role and an `expected` fingerprint (tax year, locator kind, locator
substring) that the validator matches against the referenced citation. §4
rejects the wrong-line and wrong-year probes, and citations are now attached
across fact-types, parameters, rules, and form fields. `source-citation.v1` also
moves the `resolved` invariant into the schema (governance-Q7): `resolved: true`
now *requires* a non-null tax year and locator.

**R6 — cross-citizen + year (A6).** it2 checked one parameter member. it3 adds a
runnable 2026 slice (verified Rev. Proc. 2025-32 rate schedule) and a later-year
positive (§3: same $130k taxpayer, 2026 line 16 = 19934 vs 2025 = 20267). §4
rejects mixed-year packages in both directions (2025 param and 2025 rule in a
2026 package; 2026 rule in a 2025 package) and catches a 2026 form field binding
a 2025 symbol.

**R7 — line 1z (A1).** it2's line 9 summed only 1a + 2b, silently omitting 1b–1h.
it3 adds line 1z gated by a `line1-other` completeness attestation: line 9 now
sums line 1z, and line 1z blocks unless the taxpayer attests 1b–1h are complete
(`line1z_unclosed` scenario). Line 9 can no longer pretend omitted siblings are
included.

**R8 — standard-deduction eligibility (A2).** it2's base-table rule published for
any filer. it3 guards it on an attested `standard-deduction-eligibility` fact
(dependency, age 65, blindness, spouse-itemizing, dual-status). A special-condition
taxpayer is inapplicable and line 12 does not publish (`std_special_condition`);
unknown eligibility blocks rather than silently publishing (`std_eligibility_unknown`).
Additional-standard-deduction amounts are out of scope; those taxpayers block.

**R9 — line 16 method boundary (A3).** it2 applied the rate schedule to all
incomes. it3 guards line 16 on an attested `tax-computation-method` fact and
splits it: Tax Table below $100,000 (fixture-minimal, values re-derived from the
rate-schedule midpoint construction), rate schedule at or above
(`high_income_rate_schedule` crosses the boundary the reviewers said no fixture
reached). When an alternate worksheet is required, both rules are inapplicable
and line 16 does not publish (`alternate_method_blocked`).

**R10 — all-open saturation.** `all_open` scenario opens filing status, rounding,
itemize, eligibility, method, and all closures with no sources; §2 asserts zero
publications and every rule blocked — no default becomes operative (E3.1).

**R11 — complete absence explanations.** §9 executes five walks: present numeric
zero (pins the $0.00 source), closure-backed zero (pins the closure finding),
and three record-terminating states — no-source-no-closure (record blocked,
DEPENDENCY_ABSENT on the closure symbol), invalid source (record blocked,
DEPENDENCY_INVALID), and false-guard (record inapplicable, guard_result false).
Each terminates at declared content + findings/records, never renderer convention.

**R12 — provenance.** Fixtures are now `scenario.v1` citizens declaring package,
bundle, tax year, jurisdiction, and the form-field/citation/symbol-binding files
(§1). `symbol-binding.v1` (`content/symbol-bindings.2025.json`) closes the
legibility gap where the bundle said `us.filing-status` but rules read
`filing_status`: the correspondence is now declared content.

**R13 — committed examples.** `instances/` holds hand-written positive and
negative example files per new/changed family, driven by `instances/expected.json`;
§5 validates positives valid and negatives rejected by the declared authority
(schema, fact value_schema, attachment cross-check, or cross-year check). The
harness mutations from it2 remain as supplements, not replacements.

## Residual scope and honest limitations (within closed gates)

- **R3 escalation** (above): the `closed_sets` machinery dependency is declared,
  not eliminated; native closure reading is a machinery decision left to the owner.
- **R9 Tax Table is fixture-minimal** (only the bands the fixtures hit;
  `on_miss=block`); full-table materialization is deferred breadth. Values are
  the real IRS midpoint construction, re-derivable.
- **R8 conditions project to one boolean** (`std-ordinary-eligible`); the five
  underlying conditions are declared in the fact `value_schema` and committed as a
  positive example, but additional-deduction *amounts* remain out of scope.
- **R1 correction is shown by identity stability**, not by a materialized
  workspace supersession act; the same-fact correction is argued from the entity
  key + evidence-standing invariance, consistent with ADR-0010 rather than
  re-implementing it in the prototype.
- **2026 slice is minimal** (rate-schedule high-income path only; no 2026 Tax
  Table or itemized branch), sufficient for the later-year positive and the
  cross-year negatives, not a second full corpus.
- Storage-level fault injection (E6.1/E14.1) remains the machinery's ratification
  condition, not re-proven here.

## Exhibit index

See `it3/README.md` for the file map. Schemas: `it3/schemas/`. Content:
`it3/content/` (+ `evolution/` for 2026). Fixtures: `it3/fixtures/`. Committed
examples: `it3/instances/`. Mini-spike: `it3/spikes/`. Harness + captured run:
`it3/tools/harness.py`, `it3/EVIDENCE.txt`.
