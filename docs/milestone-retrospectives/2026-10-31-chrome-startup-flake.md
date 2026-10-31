# Retrospective — Chrome Starts Before the Gate Gives Up

## Result

- **The startup allowance matches what CI does.** A Chrome launch has 45
  seconds to start, inside the existing startup slot. The one traced failure
  started in 11.2 seconds and would now pass.
- **A dead Chrome still fails with its own error.** The Python owner waits
  240 seconds, past the 225-second worst case.
- **Slow launches are visible.** A launch over ten seconds writes a
  sanitized line; the trace keeps its time.

## What the evidence changed

- **#229's observer paid off on its first natural failure.** It showed the
  launch was late, not dead: alive, in disk-wait, memory growing, ready 1.2
  seconds after the deadline. That ruled out a relaunch and pointed at the
  allowance.
- **Only one failure was traced.** The other eight predate the observer and
  are assumed to be the same cold-start pattern; 45 seconds is about four
  times the slowest passing launch, an extrapolation.
- **Counting every timer mattered.** The first build fitted queue plus
  launch inside the owner's wait and missed the observer's 60-second grace;
  the worst case exceeded the wait until the repair.

## Process

- Five Sonnet 5.5 units: P0, a build, two repairs, a review. API calls were
  paced after the earlier rate-limit hit.
- The flake cost about seven extra full runs during this queue before the
  fix.

## Follow-ups

- Warm the Chrome binary in the workflow, if first launches stay slow.
- A dead launch can hold the startup slot for 105 seconds (accepted).
