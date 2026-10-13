# Evaluation Record

A fresh headless Opus session evaluated the trials in three passes, as the
[evaluation brief](../evaluation-brief.md) describes. Each pass was committed
before the next pass's materials were copied into the evaluator's directory.

- [pass1.md](pass1.md): problems located from the participant record alone.
- [pass2.md](pass2.md): revisited against the reference account.
- [pass3.md](pass3.md): hypotheses, usefulness, the facilitator's conduct, and
  limits.

## Departures and incidents

- **Settings.** The evaluator was launched without `--setting-sources project`,
  unlike the planners and the reviewer. User-level settings (output style,
  hooks) may therefore have applied to it. Its directory held no experiment
  material beyond each pass's files, and its tool record shows reads only of
  its directory, the clean application copy, and public sources.
- **Usage limit.** Pass 2's first turn ended at a usage limit before writing
  anything. The same session was resumed with "Your previous turn was
  interrupted by a usage limit before pass2.md was written. Continue pass 2 as
  instructed in the previous message." Nothing else was added.
- **Reference account error found by the evaluator.** The correction appended
  after the design review says the SSA-1099 recipient fact "sits outside
  package v42". Package v42 includes `tax.us.2025.ssa1099.vocabulary`, and both
  of its versions declare `tax.us.2025.ssa1099.recipient`. The facilitator
  confirmed this. The error originated in the design review's spot check and
  was carried into the reference account and one Trial 1 observer note. No
  planner saw it.
- **Reviewer tool record.** Every interval is labelled "toward S0", because the
  reviewer made no snapshot commits for the extractor to split on. The
  reviewer's replies are dated in the Trial 2 log instead.
- **Observer-note timing.** The evaluator could not verify that notes preceded
  replies. The facilitator checked afterwards. For all 7 Trial 1 replies and
  all 8 Trial 2 replies, the note or delivery commit on this branch precedes
  the planner's next recorded message by 2–4 seconds. The comparison used
  commit times against the planner sessions' message timestamps.
