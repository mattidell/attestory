# Examination — D1 Iteration 1 (Incumbent)

Design: `it1/design.md`. Charter: `charter-it1.md`. Rung 2: paper rule/scan
diffs plus throwaway probes in a scratch directory outside the repository
(scratch git repo + bare remote + prototype hooks + synthetic out-of-repo
workspace). All values, payers, paths, and identifiers synthetic. No repo
enforcement code, test, fixture, or scan modified; no git writes to this repo.

## Case results (claim → rule/enforcement change → gate behavior → observed)

**Case 1 — Clean boundary. PASS (probed).** Live workspace at a scratch
out-of-repo path holding a synthetic real-shaped W-2; repo tree carries code,
contract markdown, a synthetic fixture *with* provenance manifest, and an
indirected workspace pointer (`env:TAXLIVE_WORKSPACE`). Rule: L1/L2 residency +
classification v2. Observed: pre-commit clean, push accepted, `git ls-files`
shows no workspace content, and a tree-wide grep for the synthetic SSN token
over `HEAD` returned nothing. Note: the first clean attempt *failed* — a naive
tree-wide marker scan rejected `.gitignore` for naming the ignored roots. That
false positive forced the R4/R4b split (absolute markers forbidden everywhere;
relative root *names* permitted only in declaration artifacts). Determinism
survived: the split is by artifact class, not judgment.

**Case 2 — Leak attempt, commit surface. PASS (probed).** The workspace W-2
copied to `fixtures/w2-real.json` and staged. Rule: content screens + fixture
obligations. Observed REJECT with named rules: R5 (SSN-shaped token), R5
(non-synthetic EIN `98-7654321`), R2 (no provenance manifest). Variant: forced
add under an ignored root (`git add -f local-data/notes.json`) REJECTED via R1
path class. Commit exit nonzero; nothing entered history.

**Case 3 — Leak attempt, push surface. PASS (probed, distinct from case 2).**
Same leak committed with `--no-verify` (simulating an absent/bypassed local
pre-commit), so it *reached local history*. Rule: pre-push walks
`rev-list <sha> --not --remotes` and classifies each new commit's full tree and
message — a different mechanism from the staged-diff scan. Observed REJECT
(R2, R5×2) at push; push exit nonzero; the scratch remote's log contained zero
leak commits. Also probed on this surface: a commit *message* carrying
`/Users/…` — REJECT (R6).

**Case 4 — Synthetic derivation. PASS (probed).** Rule D: real doc → shape
descriptor (schema expresses only field names, kinds, cardinality, closure
structure — it cannot hold a value) → seeded lexicon fill. Observed: fixture
carried the shape with `synth-*` identifiers and generator amounts, and the
token-intersection check printed `source-value tokens surviving into fixture:
NONE`. The unre-expressed doc committed directly is case 2's REJECT — the
boundary mechanically forces the derivation path. Manifest obligation (R2)
makes the rule checkable rather than an ad-hoc scrub.

**Case 5 — Classification ambiguity. PASS (probed).** Borderline artifact: a
tracked run-config carrying a workspace path. The rule decides both forms with
no third outcome: literal absolute path (`"/Users/demo-owner/tax-live"`) →
REJECT (R4); indirected pointer (`"env:TAXLIVE_WORKSPACE"`) → ACCEPT (it is
case 1's committed content). Totality argument: default-deny (R0) means an
artifact matching no affirmative class is never-crosses by construction —
"cannot decide" is unrepresentable in the rule's type.

**Case 6 — Kill-test enumeration. PASS (probed where guardable).** Sixteen
surfaces enumerated in the design (§D1-P1(d)), each with an enforcement point
or a no-carry argument: commit tree, forced adds, push trees, commit messages,
tag annotations, ref names, fixtures, goldens, governance/process markdown,
scratch dirs, run outputs/ledgers, the workspace itself, PR/issue text, other
pushed refs (notes), stash/reflog (no-carry to remote), author fields. Probes
beyond cases 1–3: commit-message leak REJECTED (R6); **tag-annotation leak
CROSSED under gate v2** — the marker reached the scratch remote inside an
annotated tag — the gap was recorded, the surface list versioned to v2.1
(pushed-object scan, R7), the re-probe REJECTED, the leaked synthetic tag was
purged from the scratch remote, and a clean push still passed (regression).
This live capture-and-close is the enumeration doing its job at Rung 2 rather
than being asserted complete on paper.

## Proposition verdicts

**D1-P1 — settled at Rung 2.** The location rule (L1–L3) needs no bytes to be
decidable; the classification rule v2 is total by default-deny and decided
every artifact put to it (cases 1, 2, 5), including the borderline config and
the `.gitignore` false positive it had to absorb; enforcement was observed
rejecting on **both** surfaces, with the push gate demonstrably independent of
the commit gate (case 3, per ADR-0030 §C.8); the kill-test enumeration covers
sixteen surfaces and survived one live adversarial find (case 6). Named
residuals for ratification, not gaps in the rung: (i) local hooks are
per-clone and bypassable — the design couples the run entrypoint to hook
presence and adds CI as a detective rung, keeping the private remote
non-load-bearing, but the reviewers should pressure this seam; (ii) PR/issue
text (surface 13) is enforceable only by CI-side scan plus rule, not by git
hooks — an inherent platform limit, stated rather than papered over.

**D1-P2 — settled at Rung 2.** The two-stage rule is checkable at three
points: the shape descriptor's schema cannot represent source values
(structural, not procedural); the provenance manifest is mechanically required
(R2 fired when absent); and the token-intersection check observed zero
surviving values (case 4). Residual for reviewers: value-shaped *field names*
or pathological shapes (e.g., a cardinality that is itself sensitive) cross by
design — the adversary reviewer should test whether shape alone can encode a
real value.

## Stop-condition compliance

Exactly two files produced. Probes ran only in the out-of-repo scratch
directory; throwaway `guard.py`/`derive.py` remain there and are cited as
evidence, not shipped. No contract change was made — all are expressed as
versioned diffs (design §Contract changes). No git command wrote to this
repository or its remotes.
