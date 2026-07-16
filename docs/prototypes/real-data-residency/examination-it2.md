# Examination — D1 Real-Data Residency, Iteration 2 Rival

Status: clean-room rival examination. Evidence ceiling: Rung 2. All probe
material was synthetic and lived under a throwaway scratch root outside the
repository. No Git command or production enforcement change was used.

## D1-P1 — Settled at Rung 2

The contract shape is settled: the live workspace root is owner-selected local
quarantine state, declared by rule rather than concrete path, topologically
disjoint from every worktree/Git store/remote, and unreachable from the
authoring/publication environment. A live runner receives an explicit capability,
mounts repository code read-only, writes only inside quarantine, and has no
publication path. This explains why a run may read live state while the
repository cannot carry it.

Classification is a total binary function. Personal provenance or description
always yields `NEVER_CROSSES`, including values, locators, hashes, summaries,
live dispositions, and ledgers. `MAY_CROSS` requires exactly one proven kind:
public-origin code, public-origin contract, or independently constructed
synthetic fixture. Missing, conflicting, unknown, or unreadable proof is itself
a deterministic `NEVER_CROSSES` reason; there is no undecided class and no
declassification by scrubbing.

The paper enforcement diff replaces the fixture-only boundary with one versioned
classifier over complete crossing envelopes. Commit scans the full proposed
index plus message metadata. Push separately scans every object and metadata item
reachable from each outgoing ref before transport, independent of remote state
or visibility. Remote CI is audit-only because receipt is already publication.
Guarded transport and hook integrity are production conditions; an advisory,
bypassable hook is insufficient.

Case evidence:

1. **Clean boundary:** disjoint topology, explicit synthetic workspace read, and
   zero live markers in the public tree; exit 0. A clean commit envelope with a
   public contract and proved synthetic fixture accepted both artifacts.
2. **Commit leak:** a contract-looking blob with personal provenance rejected at
   the commit surface; exit 42, reason `sensitive-provenance:personal`; no
   transport.
3. **Push leak:** a live-run artifact reachable from synthetic unit ref
   `refs/heads/unit-demo` rejected by the independently invoked pre-push logic;
   exit 42, reason `sensitive-provenance:live_run`; transport not invoked. This
   is distinct from case 2.
5. **Classification ambiguity:** a contract-looking config with unknown origin
   and a concrete workspace-locator form rejected; exit 42. Fail-closed behavior
   removed the would-be third class.
6. **Kill enumeration:** the complete ten required surfaces accepted; deleting
   `push` made the checker exit 43 and name the missing surface. The design also
   covers links/mounts, Git metadata, archives, CI artifacts, terminal/telemetry,
   remote API text, and manual-copy ingress.

The mandatory kill surfaces each have a gate or structural no-carry argument:
commit; push; test fixture; golden; charter; review; process log; retrospective;
scratch directory; run output/ledger. In particular, a live disposition report
inherits sensitivity even without amounts and remains quarantined.

## D1-P2 — Settled at Rung 2

The synthetic rule is independent construction, not sanitization. A public shape
grammar defines fields, ordering, schema-permitted presence, cardinality classes,
closure topology, and constraints. A versioned generator consumes only that
grammar/profile plus a synthetic seed and reserved demo value domains. A live
document may be matched to an already-public profile inside quarantine, but the
match and selected profile never cross.

If coverage is missing, no fixture is copied or scrubbed. The public grammar may
be expanded only from independent public specifications or general schema
capability, then regenerated without the live record. Otherwise the case stays
quarantined. The fixture manifest pins generator, public constraints, seed,
namespace, cardinality, closure, and allowed input kinds; byte regeneration and
input-edge validation are the check.

4. **Synthetic derivation:** the probe's independently authored public profile
and generator reproduced the declared field/cardinality/closure projection with
reserved demo values. It exited 0 with equal shape and zero overlap with the
synthetic quarantine canary's payer, identifier, or values. The live document
was not a generator input.

Name replacement, amount offsets, row shuffling, hashing, copied presence
patterns, redacted ledgers, and model rewrites remain personal-derived and are
therefore invalid regardless of apparent anonymity.

## Sufficiency and production conditions

Rung 2 settles both propositions' contract shapes and all six charter cases.
It does not claim production enforcement. Ratification must name implementation
of policy schemas, whole-envelope gates, topology/capability audit, guarded
transport, reproducible synthetic generation, fixture provenance, and the kill
suite as production conditions. The current private-remote posture and ignored
directories carry no part of the proof.
