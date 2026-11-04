# P0: which scope answers the record already proves

Role: Builder. Source HEAD on milestone/derived-answers-2025.
Plan: docs/phases/engine-breadth/milestones/derived-answers.md.
Read the plan, the scope-answer-questions plan and its evidence
(scope-answer-questions-evidence/p0-questions.md for the 80 facts, their
polarity and their 41 questions), the line 25b v4 rule
(packages/content/tax/2025/rule.form1040-line25b.v4.json) as the existing
"answer, or a count over the record" shape, and the rules that read each
candidate. Do not read governance or unrelated proposals.

Assigned evidence only:
docs/phases/engine-breadth/milestones/derived-answers-evidence/
(p0-trace-and-design.md, probe scripts and their outputs).

Candidates: Form 1098 scope; line 2a Form 1099-INT tax-exempt interest;
the other-dependent answer; Form 1116 required; the Form 1099-OID and
Exception 1 capital-gain facts. Add any other of the 80 facts you find the
record proves; say why each is in or out.

1. For each candidate on core v73 through `live_coordinate_run`: the fact,
   its polarity (asserts presence or absence), the recorded value each
   answer writes, the rules that read it and the lines it holds.
2. Name the basis: which recorded facts prove which value. The record proves
   presence, never absence; no recorded Form 1098 does not prove none was
   received. Classify each as derivable, partly derivable (one value only;
   say which), or not derivable, with the reasoning.
3. For each derivable value, the smallest successor rule shape that accepts
   either the answer or the proof (an `any` of the `ref` and a count over the
   record, as line 25b v4 does, if it fits). Say what happens when the
   filer's answer contradicts the record, today on v73 and under the design.
4. Prototype on a scratch v74 outside the repo: each derived case releases
   its lines with the values a filer answering the question gets; an
   answered return is byte-identical to v73; a silent record still asks.
   Count the lines released and any committed fixture or golden that moves.
5. Say how the line's explanation and presentation show a derived answer
   (what proved it) using existing mechanisms only, and what is missing.

No production, test, content or schema edits. Stop if any candidate needs a
schema, expression-operation or engine change, and report. Synthetic
demo.* only; no absolute paths in committed files. Commit evidence
incrementally with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
if held, retry every 10 s up to 5 min, never remove another holder's lock);
never --no-verify; never bare git stash. Foreground commands only; no
`pgrep` or sleep waiters. No push or spawn. Report the table, the
classification, the design, the counts and limitations.
