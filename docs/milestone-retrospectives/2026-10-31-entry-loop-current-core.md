# Retrospective — The Entry Loop Calculates on the Current Core (2025)

## Result

- **No product change; closed on its trace.** The W-2 entry loop runs on
  the core its seed adopts (package v6) and refuses a later one at opening.
  Its fixed surface is not the only thing tying it to that core: its line
  set expects presentation lines that later cores split, and its seed lacks
  the closures they ask for.

## What the evidence changed

- **The same symptom had a different cause.** The correction session's
  fixed surface was the whole defect; the entry loop's is one of three, and
  the resolver alone would leave it in `entry-state-unavailable`.
- **Trace before fix paid for itself.** The builder committed the trace
  first and stopped there, so nothing was built that would not have worked.

## Follow-ups

- Move the entry loop to a current core: its line set, its seed, and the
  resolver (parked).
