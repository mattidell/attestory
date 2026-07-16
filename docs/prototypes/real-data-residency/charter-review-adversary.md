# Charter: Round 1 Committee — Adversary Reviewer (D1)

Date: 2026-07-16. Topic D1, First Real Return Slice. Reviews both builds:
`it1/design.md` + `examination-it1.md` (incumbent), `it2/design.md` +
`examination-it2.md` (rival). Independent context; you do not see the governance
reviewer's in-progress work.

- **Seat:** Adversary reviewer, **High tier** — the failure mode is irreversible
  (a leak cannot be unleaked), so this is the crux seat.
- **Mandate:** break the boundary. Construct a concrete synthetic personal
  artifact that reaches the repository, its index, or a pushed remote through a
  surface the converged design does **not** guard, or defeat the derivation rule
  so a real value survives. A single working leak path is a decision-blocking
  finding.

## Read

Both builds, topic `plan.md`, both charters, `docs/governance/` (Article 18,
E18.1–E18.3, Ontology sensitivity inheritance), ADR-0030 §C.8,
`tests/test_kernel_fixtures.py`.

## Attack (at least these, all synthetic)

1. **17th surface.** The incumbent enumerated 16 surfaces (and found a live
   tag-annotation gap → v2.1); the rival enumerated 10 required + more with
   omission detection (delete `push` → exit 43). Find a crossing surface the
   **union** still misses — git notes, alternates/submodules, LFS pointers,
   bundles/archives, PR/issue API text, CI artifacts, reflog-to-remote, hooks
   that rewrite content, packfile side-channels, filename/mode/symlink-target
   channels. Show the artifact reaching a remote.
2. **Load-bearing ignore.** Attack the incumbent's ignored-root pointer file:
   construct a case where the ignore *is* load-bearing (§C.8 forbids this) — a
   force-add, an ignore-rule change, a clone without the ignore, a tool that
   reads the pointer and copies content into a tracked artifact.
3. **Hook bypass.** Exploit the per-clone bypassable-hook seam both builders
   name: `--no-verify`, a fresh clone with no hooks, a rewritten hook, a
   direct-to-remote path that skips the guarded transport. Show whether the
   named production conditions actually close it or merely relocate it.
4. **Shape channel (D1-P2).** Make **shape alone** carry a real value: a
   value-shaped field name, an observed string length, a cardinality that is
   itself sensitive, a closure topology unique to the real document. Test
   whether the rival's grammar exclusions ("no observed string lengths; no
   feature whose only authority is a live document") actually close this, and
   whether the incumbent's shape-descriptor schema leaks it.
5. **Ambiguity → third class.** Find an artifact the classifier cannot decide
   deterministically, defeating the fail-closed totality claim.

## Output

`reviews/adversary-r1.md` (≤120 lines): each attack as a concrete synthetic
scenario with the observed or argued outcome (crossed / rejected), marked
decision-blocking or not. If you cannot break a surface, say the surface holds
and why — a clean bill on a probed surface is evidence. State separately whether
**D1-P1** and **D1-P2** survive at Rung 2.

## Stop conditions

One review file. No repo changes, no git writes, no real data — every leak
scenario uses synthetic markers. If breaking a surface would require a real
value, describe the attack with a synthetic stand-in and stop.
