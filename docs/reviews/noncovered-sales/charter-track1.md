# Charter: Track 1 of noncovered sales — engine change and core v79

Role: Builder. Source HEAD on milestone/noncovered-sales-2025.
Plan: docs/phases/engine-breadth/milestones/noncovered-sales.md
(Decisions 1–9, "P0b result", "Track 0 rerun"). Evidence:
noncovered-sales-evidence/p0b-engine-design.md, track0-closure.md
("Rerun over the P0b contract"), p0b.py, prototype-rules/. Do not read
governance. Do not edit packages/kernel/ (PR #258 owns it); stop and
report if the build needs it.

Build in production what the scratch proved. Part A commits before Part B
starts.

## Part A — engine, schema, ADR

1. `source-closure-mapping.v4` schema (new file under
   packages/schemas/derivation/; manifest via `write_manifest`, add-only;
   inspect the manifest diff). One closure fact pin, the question, yes/no,
   and a `families` list (family, member fact type, admits symbol).
2. The next artifact-package schema version admitting v4 (add-only, same
   protocol).
3. Admission in production (marshal.py, source_authority.py / runner
   `resolve_closure_admissions`, package_validation.py, both loaders):
   the shared answer is recorded and counted once; "no" admits each listed
   family with a current horizon and zero current members; "yes" admits
   each listed family; a member added to a family after the current answer
   strips that family until a later answer (Decision 8, built in
   admission, not in a run wrapper); shared horizon ids stay illegal.
4. Decision 9 in production: on a package whose companion declaration
   names the covered-flag refusal map, a current covered sale member with
   `basis_reported_to_irs` no drops that family's admission, the row is
   `DEPENDENCY_INVALID` with `BASIS_NOT_REPORTED_ON_COVERED` in `missing`,
   and the presentation projection shows the sentence telling the filer to
   record it as a noncovered sale. A blocked line must never show an empty
   reason: fix the empty page reason Track 0 saw on line 9 for
   `code_w_on_gain`.
5. All of it behind the package switch: core v78 and earlier behave
   byte-identically (goldens unchanged).
6. `docs/adr/0084-*.md`, status **proposed**, and its INDEX row: one
   answer admits several families (v4), the staleness rule, and the
   covered-flag refusal. It supplements ADR-0014; it does not edit any
   accepted ADR. The owner accepts it before the PR goes ready — do not
   mark it accepted.
7. Unit tests for each rule above, including v78 unchanged.

## Part B — content core v79

1. The P0b/Track 0 rerun successor set from prototype-rules/ into
   packages/content/tax/2025/ as new versioned citizens (never edit a
   published citizen): eight families, the shared answer fact type and its
   input question, one v4 mapping replacing the eight v3 mappings, the six
   subtotals, Schedule D lines 2 and 9, line 7 v4, line 15 v6, line 7a v6,
   preferential base v7, Form 8949 attachment v3 (boxes B and E, code W),
   Schedule D attachment v7, lines 1a v4 and 8a v5, form fields with
   `explain` text in the line-explanations wording standard, citations.
2. ADR-0082 companion pairs from each noncovered scalar to its sale
   object, and a case that records a scalar without its object (must
   block with a reason).
3. Core v79, registry v77, release v77 via `python3 -m
   tools.package_successor`; the loader companion declaration for v79
   (the covered-flag refusal map and the pairs).
4. Tests through the real coordinator and the presentation model: every
   case in the Track 0 rerun digest, the nine current-core returns under
   one "no" equal to v78 dollars, v78 and earlier pinned.
5. Run `pytest -m "not live"`, then the full suite (substrate work), and
   `python3 -m mypy` as CI runs it. Fill the plan's "Track 1 result".

## Rules

Synthetic demo.* only; no absolute paths in committed files. Published
schemas and citizens are immutable: successors only. Commit after each
numbered item with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
retry every 10 s up to 5 min if held); never --no-verify; never bare git
stash. Foreground commands only; no pgrep or sleep waiters. No push or
spawn.
