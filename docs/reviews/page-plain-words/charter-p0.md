# Charter: P0 of the saved page writes its own words plainly

Role: Builder. Source HEAD on milestone/page-plain-words-2025.
Plan: docs/phases/engine-breadth/milestones/page-plain-words.md (read it
whole). Precedents: plain-line-texts-evidence (the content-text census and
its term list), the blocked-sale-pages retrospective, and
tools/recorded_replay.py (`full`). Do not read governance.

## Scope

1. **Inventory.** Every string `packages/presentation/pages/citation-walk.v1.html`
   writes itself that a filer can see: badges, banners, captions, button
   labels, error texts, headings, empty states. For each: file:line, the
   condition that shows it, an example of what it shows today, and how
   many of the 775 recorded lists show it (render the saved page model for
   each list; count by string kind, not by value).
2. **Pins.** Every test, golden, harness manifest, harness example page and
   Chrome observation that pins each string (grep the repo; name file:line).
3. **Wording.** Draft plain wording for each filer-facing string, with the
   string it replaces. Engine enums, symbols, rule, finding and fact ids,
   and words like "disposition", "dependency", "published", "closure",
   "guard" must not be the text a filer reads first. Where an id is the
   evidence an auditor follows, say how it stays reachable (for example a
   secondary details line or a title attribute) without being the caption.
4. **Harness example page.** Say whether
   `tools/presentation_harness/examples/pages/citation-walk.v1.html` shows
   the same strings and must follow.
5. **Risks.** Any string a test or a consumer parses (not only displays);
   any place where changing the words changes behaviour.

## Deliverables

In docs/phases/engine-breadth/milestones/page-plain-words-evidence/:
p0.md (inventory table, pins, drafted wording, auditor reachability,
risks, decisions for the foreman), the census script, and small JSON.
Fill a "P0 result" section in the plan. No page, test, package or
content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn. Do not edit packages/ or
  tests/.
