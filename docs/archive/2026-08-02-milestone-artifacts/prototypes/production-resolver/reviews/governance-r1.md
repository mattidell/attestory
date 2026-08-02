# D3 Round 1 — Governance Review

Date: 2026-07-16  
Seat: Governance reviewer (Medium)  
Evidence: Rung 2 paper/probe review; all cited package examples are synthetic.

## Result

- **D3-P1:** the rival is conformant at Rung 2; the incumbent has one
  decision-blocking package-publication-anchor gap noted under Measure 2.
- **D3-P2:** the incumbent ledger is conformant at Rung 2; the rival ledger has
  a decision-blocking completeness gap under Measure 5.

## Findings by measure

### 1. Exclusive projection beyond fixtures — **not decision-blocking**

Both designs conform to ADR-0027 Decisions 1 and 7. Incumbent §4 steps 6, 11,
and 12 construct the graph only from exact `package.members` pins and give no
catalog-only object to execution or rendering; Case 2 probes that result. Rival
R6 constructs supply by pinned-key lookup and makes an unpinned co-located
synthetic member unreadable. That strengthens d7's required inertness rather
than changing membership authority. Both retain a reject, rather than a clean
subset, when validation has issues (ADR-0027 d4; ADR-0028).

### 2. Byte verification and package rewrite — **decision-blocking for incumbent**

Rival R1/R3/R4 is conformant to ADR-0027 Decision 6 and PC3: its
repo-resident publication registries authenticate the package and every member;
the package self-check and registry check jointly reject a recomputed-checksum
rewrite. Its mandatory production checksum input closes the fixture optionality.

Incumbent §2 and §4 instead make an adoption-pinned `installed-content-catalog`
the checksum source passed to `verify_published_package`. The text requires no
publication-registry provenance or verification for that catalog. A new catalog
plus adoption can therefore present new bytes for an existing `(id, version)`
without comparison to the published package-instance checksum, contrary to
Decision 6/PC3's registry-verified-content requirement. A catalog checksum
anchors a chosen catalog; it is not, on the stated contract, a published
package/citizen registry. Thus its claim that PC3 is discharged (§6) is not yet
established.

### 3. Strict-superset guarantee — **not decision-blocking for rival**

Rival R4/R5/R8 uses the committed validator with mandatory citizen checksums,
mandatory package verification, pin-directed supply, and `ok == True` before a
graph exists. These are additive constraints over the fixture path in
`runners/derive.py`, which supplies a corpus by glob and explicitly ignores
`validation.ok`; this is a construction argument, not merely a parity probe.
Incumbent has the same intended all-or-nothing construction (§4), but cannot
complete the strict-superset claim until Measure 2's publication-anchor defect is
closed.

### 4. R5 no-leniency gate and RG-1 — **not decision-blocking; MUST condition**

`ok == True` is the conformant reading of ADR-0027 d4's contained issues and
the plan's no-silent-partial case: containment records all defects; it never
authorizes execution of the remaining members. ADR-0028 likewise makes missing
or unclosed fact/composition obligations reject. A leniency or issue allowlist
would be non-conformant. Rival R5/RG-1 correctly makes repair of the synthetic
currently-invalid package (validator reachability edge and v1-generation debt)
a production prerequisite, not a reason to bend the gate.

Incumbent §4 step 11 also has the correct hard gate, but its clean-case framing
and §6 migration deferral do not name that current-package prerequisite. This
understates a real production obligation; it does not make its stated gate soft.
The accepted synthesis must carry RG-1 as a MUST production condition.

### 5. Discharge/defer ledger — **decision-blocking for rival D3-P2**

Incumbent §6 explicitly accounts for ADR-0027 Decisions 1–7/PC1–PC4 and
ADR-0028 Decisions 1–9/PC1–PC3, including the required rejection (not deferral)
of embedded schema-byte checksums. Its Track-3 evidence deferrals are explicit.

Rival §5 claims every named condition but omits explicit dispositions for
ADR-0027 Decisions 1 (sole package authority), 2 (role canon), 4 (typed
outbound/inbound closure and contained issues), 5 (producer integrity), and 6
(member immutability). R2–R6 discuss portions of them, but the mandatory ledger
is the required no-silent-partial accounting surface (plan Gate 2 case 6), not
an inference exercise. This is a completeness gap, not a disagreement about
the underlying mechanisms. Its rejection of embedded schema-byte checksums is
faithful to ADR-0027 Decision 3.

### 6. D1/D2 interlocks — **not decision-blocking**

Both designs consume ADR-0031 rather than create an egress exception: live
reads/writes remain within `L`, repository/publication surfaces are unavailable,
and descriptive records remain quarantined (incumbent §3; rival R7). Both keep
raw inputs and contributions out of resolution and require the ADR-0032
marshal-only `RunContext` interlock (incumbent §4; rival R6). The unresolved
marshaller and installed-wall kill tests remain their owning Tracks 2/3
production conditions, not D3 discharge claims.

## Verdict

Do not accept either design wholesale yet. The R5 hard gate is required and
RG-1 must be carried as a production condition. Resolve the incumbent's missing
published-registry anchor and the rival's incomplete D3-P2 ledger before
declaring both propositions converged.
