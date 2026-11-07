# Charter: Track 0 adversarial closure of noncovered sales

Role: Builder. Source HEAD on milestone/noncovered-sales-2025.
Plan: docs/phases/engine-breadth/milestones/noncovered-sales.md (read it
whole: P0 result and Decisions). P0 evidence:
noncovered-sales-evidence/p0-law-state-design.md, its probe and
prototype. Gate: `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate"
(read that section and its closing paragraphs whole). Do not read
governance.

## Scope

Over the decided design (Decisions 2-6), produce the gate's six
artifacts, with evidence built through `live_coordinate_run` on a scratch
v79 under the evidence directory (never under packages/content):

1. Authority-lifecycle table: every contributed fact (the filer-supplied
   basis, the new boundary answer, the one question that closes eight
   families, `basis_reported_to_irs` on the covered families), with what
   invalidates each.
2. Empty/nonempty authority matrix for the new families and the covered
   families, including the misroute (Decision 2) and the boundary "no".
3. Late-member trace: attest, close (the one question "no"), compute, add
   a noncovered sale, reclose, recompute; and a covered-to-noncovered
   correction of `basis_reported_to_irs`.
4. Claim reuse: whether any existing claim (the covered closures, the
   ADR-0061 boundary pair, the preferential-base gate) is reused, and the
   three-part proof, or that none is.
5. Neighbor dependency diff: every return v78 computes, before and after;
   any new prerequisite (the one question) on a return with no sales,
   justified or removed.
6. Integration surface: every consumer of Schedule D lines 2, 7, 9, 15,
   16, 21, Form 1040 line 7a, the preferential base and the Form 8949
   attachment, with cardinality, and one built model per disposition path,
   including a presentation-model probe for each new form field.

Then the closing declaration under the plan's "Track 0 adversarial
closure" heading. A row is PASS only if no counterexample stands beside
it (Decision 1). Where the design must change to pass, change the scratch
prototype and say what changed; where it cannot without an engine,
schema or recording change, mark FAIL and stop.

## Deliverables

noncovered-sales-evidence/track0-closure.md (the six artifacts), the
scratch prototype and its output (small; no copies of the content tree),
and the plan's "Track 0 adversarial closure" section. No production,
test or content edits.

## Rules

Synthetic demo.* only; no absolute paths in committed files. Commit
incrementally with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
retry every 10 s up to 5 min if held); never --no-verify; never bare git
stash. Foreground commands only; no pgrep or sleep waiters. No push or
spawn. Do not edit packages/kernel/.
