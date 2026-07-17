# D3 it2 — Examination (Clean-Room Rival)

Builder self-examination per charter-it2.md. Rung 2. Design under examination:
`it2/design.md`. Seal held: no incumbent material read. All probe content
synthetic (committed public fixtures staged into an out-of-repo scratch `L`);
probes were throwaway and read-only against the repository.

## D3-P1 — Production resolution contract: **settled at Rung 2**

The contract (design R1–R8) is fully representable as paper diffs over the
committed machinery — one new module boundary, one additive strictness wrapper
on `validate_package`, no schema changes — and every behavior the contract
requires was either probed directly or is carried verbatim by the committed
validator it wraps. Case-by-case:

- **Case 1 (clean resolution + parity): probed, holds.** The committed runner
  on a scenario staged in scratch `L` produced a byte-identical JSON report to
  the repo-fixture run of the same scenario; direct validation resolved 44/44
  member pins. Parity is exact because finding ids are content-addressed.
  One material fact surfaced: the committed ratified package validates with
  `ok == False` (seven contained issues), and the fixture runner knowingly
  ignores that. The R5 hard gate would refuse today's committed package.
  I examined whether this makes the contract wrong and concluded no: bending
  the gate (leniency carve-outs, issue allowlists) would reproduce exactly the
  silent-partial posture the plan's case 5 forbids. The refusal is honest
  fail-closed; the repair is a named obligation (RG-1), part owed by a
  validator defect (missing reachability edge for `optional_default`
  parameters), part by v1-generation content debt already deferred under
  ADR-0028 PC2. This is the design's most committee-contestable point and is
  flagged as such (design §6b).
- **Case 2 (exclusive projection): probed, holds.** A co-located unpinned
  rule entered the fixture loader's corpus but not the resolved graph, and the
  run report was unchanged — d7 holds at projection today; R6 (pin-directed
  supply) moves the guarantee a layer earlier so unpinned bytes are never read
  at all. The same-key impostor probe additionally exposed that the fixture
  glob is unsorted (enumeration-order race on corpus admission); checksum
  arbitration (R3) closes the race independently of ordering.
- **Case 3 (byte-verification, mandatory): probed both directions, holds
  fail-closed.** Member byte mutation → `MEMBER_CHECKSUM_MISMATCH`, nothing
  published; package-instance mutation → `PACKAGE_CHECKSUM_MISMATCH` (stale
  field) and `PACKAGE_VERSION_REWRITE` (recomputed-field attack), both raised
  before member work. No probe found a fail-open path. Residual honesty: the
  committed runner's downstream failure mode is an uncontained `KeyError`
  (exit 1), i.e. fail-closed in effect but untyped; R5's typed refusal is a
  contract commitment verified only at implementation (Track 3).
- **Case 4 (D1 interlock): argued structurally + hygiene-checked.** The
  resolver's write surface is `L` only; the repo mount is read-only inside the
  ADR-0031 run capability, and resolution ledgers classify `NEVER_CROSSES` by
  description inheritance. After all probes the repository shows no change
  beyond the two authored topic documents; all probe artifacts live in the
  out-of-repo scratchpad. Consistent with the charter, this case consumes the
  ADR-0031 wall rather than re-proving it — its full enforcement evidence is
  owned by Tracks 1/3.
- **Case 5 (no silent partial load): probed, holds with the same typing
  residual.** Deleting one pinned rule produced `MEMBER_ABSENT` plus honest
  cascade issues; the committed runner exited nonzero with nothing published —
  no silent partial *result* today, and R5 makes the refusal first-class.
- **Superset claim: holds by construction, not just by test.** The production
  path invokes the same committed validator (one code path) with strictly more
  mandatory inputs (citizen checksums, instance verification) and a strictly
  stricter gate (`ok == True` enforced vs. ignored). Every fixture guarantee
  is therefore present verbatim; the four added guarantees are tabulated in
  design §2 R8 and each is probe-backed (cases 1, 2, 3, 5).

**What Rung 2 does not establish** (named, not hidden): the typed-refusal
ledger and the `SupplyIndex`/`TrustAnchor` module boundary exist only on
paper; RG-1's repair scope (validator edge vs. content debt split) is
diagnosed from probe output, not from a fix; and case 4's enforcement depth is
deliberately Track-1/3 evidence. None of these is a contract-shape
uncertainty; all are implementation discharge items.

## D3-P2 — Discharge/defer ledger: **settled at Rung 2**

The ledger (design §5, cited by case 6) enumerates every named production
condition of ADR-0027 (d3, d7, PC1–PC4, N1/N2 pointer) and ADR-0028
(PC1, PC1b, PC1c, PC2, PC3), plus the consumed-interlock items from ADR-0031
(production conditions → Tracks 1/3) and ADR-0032 (marshal-only `RunContext`
MUST → Tracks 2/3). Each row is one of discharged-by-this-contract,
carried-verbatim-inside-the-gate, deferred-with-owner-and-reason, or
acknowledged-N/A — no silent partial discharge. Completeness check performed:
the condition list was re-derived from the ADR texts at `HEAD`, not from
memory; ADR-0028 PC2 was upgraded from routine deferral to *load-bearing*
deferral because probe P1 shows the committed package's v1-generation debt is
what the R5 gate will refuse (the ledger and case 1 corroborate each other).
The round also surfaced three new obligations (RG-1 gate-clean package,
RG-2 deterministic corpus, RG-3 typed refusals) and names owners for each
rather than absorbing them into the contract silently.

## Verdict summary

- **D3-P1: settled at Rung 2.** Contract representable as versioned paper
  diffs; all six required behaviors probed or carried; strict superset shown
  by construction and by probe. Committee attention requested on the R5
  no-leniency gate given RG-1 (it refuses the currently committed package
  until repaired — I judge this correct, but it is a real cost).
- **D3-P2: settled at Rung 2.** Ledger complete over every named condition,
  no unaccounted item, deferrals reasoned and owned.
- Cases cited: 1 (parity, probed), 2 (exclusive projection, probed),
  3 (byte-verification, probed both directions, mandatory), 4 (D1 interlock,
  structural + hygiene), 5 (no silent partial, probed), 6 (ledger, design §5).

Stop condition reached: this file and `it2/design.md` are the round's only
outputs; no code, schema, fixture, or test was modified; no git write
commands were run.
