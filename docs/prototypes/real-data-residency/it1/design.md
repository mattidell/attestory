# D1 Iteration 1 — Design (Incumbent): Real-Data Residency Boundary

Charter: `charter-it1.md`. Evidence rung 2: paper rule/scan diffs plus throwaway
probes run in a scratch directory outside the repository (scratch git repo,
scratch bare remote, prototype hooks, synthetic out-of-repo workspace). Every
value, payer, path, and identifier below is synthetic. No repo code, test,
fixture, or scan was modified; no git write command touched this repository.

## D1-P1(a) — Location rule for live workspaces

**Rule L1 (residency).** A live workspace is a directory whose real path is
(i) outside the repository working tree, (ii) outside every path that any git
operation of this repository can read into an object (not a submodule, not a
symlink target reachable from a tracked path), and (iii) chosen by the owner at
bootstrap. The rule constrains the *relation* to the repo, never the bytes of
the path.

**Rule L2 (indirection).** Tracked content never contains the residency path.
The repository refers to the workspace only through a **pointer indirection**:
an environment variable (e.g. `TAXLIVE_WORKSPACE`) or a pointer file under an
ignored root (e.g. `local-data/workspace-pointer.json`). A run resolves the
pointer at runtime; that is why a run can read the workspace while the repo
cannot contain it — reading is a runtime act against the local filesystem,
containment is a git act against tracked content, and the pointer exists only
on the ignored side of that line. Governance fit: Constitution Article 18
(personal data lives in the workspace, nowhere else; the boundary is structural
where structure can hold it) and E18.1 (no route from the repo's committed
surface to personal data — the pointer indirection is the audited non-route).

**Rule L3 (write direction).** Live runs write outputs and ledgers only inside
the residency (or other ignored roots). Nothing under the residency is ever a
source for tracked content except through the D1-P2 derivation rule.

## D1-P1(b) — Deterministic classification rule (v2)

Classification is a **total function** over candidate artifacts (anything git
could track, plus git metadata carriers). Totality comes from **default-deny**:
an artifact is *may-cross* only if an affirmative class admits it **and** no
content screen fires; everything else is *never-crosses*. There is no third
outcome, so no artifact is undecidable — the case-5 requirement.

Affirmative may-cross classes (membership checkable from path + manifest):

| Class | Membership | Extra obligation |
|---|---|---|
| CODE | `packages/`, `tools/`, `tests/` source | content screens |
| CONTRACT | `docs/` markdown, governance, schemas | content screens; may *name* ignored roots (declaration privilege, R4b) |
| SYNTHETIC-FIXTURE | fixture roots (`packages/sample_data/`, test fixtures) | **provenance manifest** naming generator + constraints (E18.3); synthetic-lexicon identifiers |
| GOLDEN | expected outputs under fixture roots | provenance chain: derived only from SYNTHETIC-FIXTURE inputs |
| META | `.gitignore`, repo config | declaration privilege (R4b) |

Content screens (any class):

- **R4** absolute residency markers — `/Users/`, `/private/`, `/home/`, and the
  resolved residency pointer value — forbidden in every artifact, including
  declaration artifacts.
- **R4b** relative never-crosses root *names* (`local-data/`, `uploads/`,
  `private-archive/`, `generated/user/`) — permitted only in declaration
  artifacts (META, CONTRACT); forbidden in CODE/fixtures/goldens. Probing
  forced this split: a naive tree-wide marker scan rejects `.gitignore` itself,
  which must name the roots it ignores. Root *names* carry no data; absolute
  paths and values do.
- **R5** value shapes: SSN-shaped tokens; EIN-shaped tokens outside the
  reserved synthetic range (`00-000NNNN`); account-number shapes; any token
  matching the seeded canary markers planted in live workspaces (E18.2).
- **R1** path class: anything under a declared never-crosses root (defeats
  `git add -f`).
- **R0** default-deny: no affirmative class ⇒ never-crosses.

Versioned diff v1 → v2 (v1 = `test_committed_kernel_fixtures_have_no_absolute_local_paths`):

```
- scope: one directory (packages/sample_data/kernel)
+ scope: every tracked artifact + git metadata carriers (messages, tag
+        annotations, ref names)
- rule: 4 substring markers, reject on hit
+ rule: default-deny affirmative classes + screens R0/R1/R4/R4b/R5
+ new:  fixture provenance manifests mandatory (E18.3)
+ new:  synthetic lexicon (demo-*/synth-* ids, reserved EIN range 00-000NNNN)
```

## D1-P1(c) — Enforcement surface (commit and push)

Enforcement is a ladder; each rung re-applies the same classification rule v2,
so surfaces cannot drift apart:

1. **Commit surface** — `pre-commit` hook: classify every staged blob
   (`git diff --cached`). Earliest preventive point.
2. **Push surface** (ADR-0030 §C.8) — `pre-push` hook, **independent of rung
   1**: for each pushed ref, (i) scan the pushed *object itself* (R7 — catches
   annotated-tag annotations, probed below), (ii) walk every commit not on any
   remote (`rev-list <sha> --not --remotes`) and classify the **full tree** and
   **message** of each. Because it walks history rather than the stage, it
   rejects leaks that entered via `--no-verify`, merges, or rebases. This is
   the last *preventive* point before publication.
3. **Repo-side detection** — the in-repo test suite runs the same scan
   tree-wide (Track-1/3 implementation), and a CI required check runs it on
   every PR. CI is *detective* (the push has already published); it exists to
   catch clones with missing hooks, not to be the boundary.

**Honest residual:** git hooks are per-clone and bypassable. Mitigations that
keep the private remote non-load-bearing: bootstrap tooling installs both
hooks (and the run entrypoint refuses to run if they are absent — structural,
per Article 18); CI detection plus a purge-and-rotate incident procedure
covers the bypass window. The residual is named, not hidden: rung 2 is the
boundary, rung 3 is the alarm.

Scan surface-list diff (versioned):

```
v1:   { kernel fixture dir }                             (in-repo test only)
v2:   + all tracked blobs at commit (staged)             (pre-commit)
      + all new commits' trees at push                   (pre-push)
      + commit messages at push (R6)                     (pre-push)
v2.1: + pushed objects themselves: tag annotations (R7)  (pre-push)
      + ref names at push                                (pre-push)
      + tree-wide in-repo test + CI required check       (detection)
```

v2.1 exists because probing found the gap (below): v2 let a marker cross
inside an annotated tag's annotation.

## D1-P1(d) — Kill-test enumeration

Every surface where data could cross, each with an enforcement point or an
explicit no-carry argument. P = probed in the scratch environment.

| # | Surface | Enforcement / no-carry |
|---|---|---|
| 1 | Commit (staged tree) | pre-commit scan; P — REJECT observed (R5, R2) |
| 2 | Forced add of ignored root | R1 path class; P — REJECT observed |
| 3 | Push (branch: trees) | pre-push rev-list tree scan; P — REJECT observed after `--no-verify` bypass; remote held 0 leak commits |
| 4 | Push (commit messages) | R6 message scan; P — REJECT observed |
| 5 | Push (tag annotations) | R7 pushed-object scan; P — v2 gap found (marker reached scratch remote), v2.1 REJECT observed |
| 6 | Push (ref/branch names) | ref-name screen in pre-push (v2.1 list); same mechanism as R6 |
| 7 | Test fixtures | SYNTHETIC-FIXTURE class: manifest + lexicon + screens, at rungs 1–3 |
| 8 | Goldens | GOLDEN class: provenance chain from synthetic inputs only; screens |
| 9 | Charters / reviews / process logs / retrospectives / handoff | tracked markdown ⇒ CONTRACT class; full tree scan at commit and push (surfaces 1,3). Procedural rule (milestone Data-safety) is backed by the same mechanical scan |
| 10 | Scratch directories | outside the repo (this iteration's probes) or under ignored roots (R1 if force-added); never a source for tracked content except via D1-P2 |
| 11 | Run output / ledger | Rule L3: live runs write only inside the residency; in-repo goldens derive only from synthetic runs (class GOLDEN). Live-run *reports* cite dispositions, never values (milestone Verification) |
| 12 | Live workspace itself | Rules L1/L2: outside the tree; only referenced via ignored pointer; R4 rejects any literal residency path in tracked content; P — clean case observed |
| 13 | PR titles/descriptions, issue text | GitHub-side text outside git objects. Not mechanically scanned by hooks; enforcement: authored under the same agent/owner data-safety rule, CI scan of PR body as a required check (Track 1/3), and §C.8 treats anything on the remote as published — so the rule is "never type a value there," mechanized where the platform allows |
| 14 | Git notes / other pushed refs | pushed objects ⇒ R7 object scan + rev-list walk (any ref, not just branches) |
| 15 | Stash / reflog / local clones | never pushed ⇒ no remote crossing; local machine is inside the owner's trust boundary (residency lives there too). No-carry to the publication surface by construction; hygiene only |
| 16 | Commit author/committer fields | fixed identity strings configured once; R6-style screen extends to author lines in the pushed-object scan (v2.1) |

## D1-P2 — Synthetic-derivation rule

**Rule D (two-stage, value-blind).** A real document becomes an in-repo
fixture only through:

1. **Extract** — real doc → **shape descriptor**. The descriptor schema can
   express only: field names, node kinds (record/list/scalar type), list
   cardinality, and closure structure (which families/boxes are present). It
   has **no field that can hold a source value**, so no value can survive this
   stage — the guarantee is the intermediate's expressiveness, not a scrub.
2. **Fill** — shape descriptor + seeded synthetic lexicon → fixture. Every
   scalar is generated (`synth-*`/`demo-*` identifiers, reserved EIN range,
   generator amounts), so every value in the fixture has generator provenance
   by construction.

Obligations making it checkable (not ad-hoc): the fixture commits **with a
provenance manifest** naming the generator, seed, and constraints (E18.3;
class SYNTHETIC-FIXTURE requires it — R2 rejected the manifest-less fixture in
the probe); identifiers must match the synthetic lexicon; and the derivation
tool emits a **token-intersection check** — the set of source value tokens ∩
fixture tokens must be empty, recorded in the manifest. Field *names* cross by
design (they are the shape); the intersection check applies to values.

Probe: a synthetic real-shaped W-2 (payer "Demo Payer One Inc", SSN-shaped
`123-45-6789`, EIN `98-7654321`) → descriptor (types/cardinality only) →
fixture (`synth-name-3`, `synth-ein-6`, generator amounts). Observed:
`source-value tokens surviving into fixture: NONE`. The same doc committed
*directly* was rejected (R5 twice, R2) — the boundary forces the rule.

## Probe record (all outside the repository)

Scratch layout: `live-workspace/` (synthetic W-2), `repo/` (scratch git repo
with prototype hooks), `remote.git` (bare). Sequence: clean commit+push
accepted, workspace absent from tree/index (grep for the synthetic SSN over
`HEAD` returned nothing); commit leak rejected naming R5/R2/R1; `--no-verify`
leak rejected at pre-push with remote unchanged; commit-message leak rejected
(R6); tag-annotation leak crossed under v2 — gap recorded, v2.1 object scan
added, re-probe rejected (R7) and the leaked synthetic tag was purged from the
scratch remote; clean push regression under v2.1 accepted. Throwaway code
(`guard.py`, `derive.py`) stays in the scratch directory and is not part of
this design; the rules above are the contract, the probes are the evidence.

## Contract changes required (paper only)

1. Replace the v1 single-directory test with the v2.1 tree-wide classification
   scan (Track 1/3 implementation of this rule).
2. Add pre-commit and pre-push hooks + bootstrap installer; run entrypoint
   refuses without them (structural coupling).
3. CI required check running the same scan on PRs (detection rung).
4. Fixture provenance manifests become mandatory for fixture roots (E18.3).

None of these are made in this iteration; all are expressed above as versioned
diffs, per the charter's stop conditions.
