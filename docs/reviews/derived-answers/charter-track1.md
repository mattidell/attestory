# Track 1: derive the four proved answers (core v74)

Role: Builder. Source HEAD on milestone/derived-answers-2025.
Plan: docs/phases/engine-breadth/milestones/derived-answers.md (read P0
result and Decisions). Evidence: derived-answers-evidence/
p0-trace-and-design.md and its scratch successors. Do not read governance.

1. Land the seven successors P0 prototyped (line 12e v4, line 2a v5,
   Schedule 3 line 1 direct-ftc v4, odc-dependent-present v2,
   ctc-sch8812-line-6 v3, odc-child-marked-conflict v2,
   odc-relative-marked-conflict v2) under packages/content/tax/2025/, and
   build core v74, registry v72, release v72 with
   `tools/package_successor.py`. Add any loader companion entry v74 needs
   (packages/tax/loader.py), as earlier successors did. Published files are
   immutable: only new versions; inspect every manifest diff for adds only.
2. Decision 1 condition, first: for each candidate, run the answered return
   (agreed answer, and the answer that takes the other path) with the
   proof's family left open (no closure recorded) on v73 and on v74. If v73
   publishes the line and v74 newly blocks, that candidate is held: do not
   land its successors, record the case, and continue with the rest. Say
   what you held and why in the evidence.
3. tests/test_derived_answers.py, through the real coordinator
   (`live_coordinate_run`, no hand-built run context): for each delivered
   candidate, the proved return publishes without the question and with the
   agreed return's amounts; the silent record still asks the v73 question;
   the answered return publishes v73's amounts; the contradicting answer
   publishes the record's value (Decision 2); joint cases P0 ran; the
   Form 1116 caps (400 single, 500 and 700 joint, 30). v73 pinned: the same
   cases on v73 behave as today, including the two contradiction blocks.
   OID and Exception 1 unchanged on v74.
4. Run the inner loop and `pytest -m "not live"`, then the full suite once
   (substrate is not touched, but goldens may be). Do not regenerate any
   earlier core's golden. If a committed golden pinning v73 or earlier
   moves, stop and report.
5. Record a short track evidence note
   (derived-answers-evidence/track1.md): what landed, what was held,
   counts, and the full-suite result line.

Stop if anything needs a schema, operation or engine change. Synthetic
demo.* only; no absolute paths in committed files. Commit incrementally
with explicit paths under `$(git rev-parse --git-dir)/collaboration-commit.lock`
(mkdir … rmdir; if held, retry every 10 s up to 5 min, never remove
another holder's lock); never --no-verify; never bare git stash.
Foreground commands only; no pgrep or sleep waiters. No push or spawn.
