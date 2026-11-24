# Retrospective: The Age Fact's Title (Closed on P0)

Milestone key: eic-age-title. Plan:
`docs/phases/engine-breadth/milestones/eic-age-title.md`.
Closed 2026-11-24 on P0. No package change.

## What happened

EAQ-R7 noted that the earned income credit age fact's title omits age at
death. A grok P0 first checked where that title reaches a person and how a
successor would treat saved answers. It found the title is shown nowhere:
the page, question groups, explanation graph and reports all omit it, and
the question the filer reads already states age at death. It also found a
safe route if a surface ever shows it. The foreman closed on P0.

## What worked

- Charter P0 to ask "who sees this?" and "what does a successor do to saved
  answers?" before any build. Both answers came back in one short run.

## What to change

- Before parking a wording item, record whether any surface shows the text;
  this one would have been closed when it was parked.
