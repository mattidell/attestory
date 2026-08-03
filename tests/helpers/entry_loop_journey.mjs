// Shared knowledge of the entry loop's known fact fields and how to walk
// them to completion in a real browser, used by every script that drives
// the compiled entry surface end to end. Before this, each script re-typed
// its own "set #w2-box1, submit, wait for complete" sequence; a second
// fact meant three near-identical, independently-drifting patches instead
// of one. This mirrors the loop's own backend and template shape: exactly
// two known facts, described once, walked by one shared routine -- not
// generalized to an unbounded N.
//
// Every function here takes `evaluate` and `waitUntil` as plain,
// single-argument async callbacks rather than importing or assuming a CDP
// session -- each caller already owns its own session and binds these to
// it, so this module stays decoupled from how any particular script talks
// to the browser.

export const ENTRY_LOOP_FIELDS = [
  { id: "w2-box1", value: "90000" },
  { id: "div1b-qualified", value: "600" }
];

export function fieldSelector(id) {
  return `#${id}`;
}

// Sets an input's value and fires the same "input" event a real keystroke
// would, without submitting -- lets a caller populate a field and still
// drive its own, separately-measured activation of the submit button
// (see entry_loop_keyboard_operability_client.mjs's "Data population
// only" step, which this generalizes rather than replaces).
export async function populateField(evaluate, id, value) {
  const found = await evaluate(`
    (() => {
      const input = document.querySelector(${JSON.stringify(fieldSelector(id))});
      if (!input) return false;
      input.value = ${JSON.stringify(String(value))};
      input.dispatchEvent(new Event("input", { bubbles: true }));
      return true;
    })()
  `);
  if (!found) throw new Error(`entry-loop-journey-field-not-found:${id}`);
}

export async function populateAllFields(evaluate, waitUntil, fields = ENTRY_LOOP_FIELDS) {
  for (const { id, value } of fields) {
    await waitUntil(`document.querySelector(${JSON.stringify(fieldSelector(id))}) !== null`);
    await populateField(evaluate, id, value);
  }
}

export async function submitField(evaluate, id) {
  const submitted = await evaluate(`
    (() => {
      const input = document.querySelector(${JSON.stringify(fieldSelector(id))});
      if (!input || !input.form) return false;
      input.form.requestSubmit();
      return true;
    })()
  `);
  if (!submitted) throw new Error(`entry-loop-journey-submit-failed:${id}`);
}

// The full walk: populate and submit every field in the given order,
// waiting for each round trip to settle before moving to the next, then
// waiting for the record to report complete. This is the routine most
// callers want -- population and submission driven directly through the
// DOM rather than through measured keyboard activation, which is exactly
// right for a script whose subject is something other than the loop
// itself (rendered focus indicators, the compiled client's own network
// calls) and wrong for one whose subject is keyboard activation, which
// populates fields with this module but submits through its own measured
// Enter/Space presses instead.
export async function completeJourney(evaluate, waitUntil, fields = ENTRY_LOOP_FIELDS) {
  for (const { id, value } of fields) {
    await waitUntil(`document.querySelector(${JSON.stringify(fieldSelector(id))}) !== null`);
    await populateField(evaluate, id, value);
    await submitField(evaluate, id);
    await waitUntil(`document.querySelector(".primary[disabled]") === null`);
  }
  await waitUntil(
    `document.body.textContent.includes("0 missing facts") && document.body.textContent.includes("fully computed")`
  );
}
