<script>
  import { onMount } from "svelte";
  import { formatW2Box1Hint } from "./w2-box1-format.js";
  import {
    W2_BOX1_FIELD,
    formatSourceLabel,
    formatDestinationPurpose
  } from "./w2-box1-field.js";

  let state = null;
  let amount = "";
  let error = "";
  let busy = false;
  let outcomeUncertain = false;
  let wageInput;
  let statusRegion;

  const MAX_SNAPSHOT_BYTES = 64 * 1024;
  const MAX_ROWS = 16;
  const MAX_TEXT = 500;

  const money = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2
  });

  function stateUrl(name) {
    return new URL(`./api/${name}`, window.location.href);
  }

  function setState(next) {
    state = next;
    if (next.answered?.length) {
      amount = String(next.answered[0].value);
    }
  }

  function isRecord(value) {
    return value !== null && typeof value === "object" && !Array.isArray(value);
  }

  function isBoundedText(value, maxLength = MAX_TEXT) {
    return typeof value === "string" && value.length > 0 && value.length <= maxLength;
  }

  function isTextList(value, maxItems = 8) {
    return Array.isArray(value) && value.length <= maxItems &&
      value.every((item) => isBoundedText(item));
  }

  function isAuthorization(value) {
    return isRecord(value) &&
      (typeof value.current === "boolean" || value.current === null) &&
      isBoundedText(value.status, 80);
  }

  function isUsableSnapshot(value) {
    if (!isRecord(value) || typeof value.saved !== "boolean" ||
        typeof value.accepted !== "boolean" ||
        typeof value.last_action !== "string" || value.last_action.length > 32 ||
        !Array.isArray(value.answered) || value.answered.length > 1 ||
        !Array.isArray(value.missing) || value.missing.length > MAX_ROWS ||
        !Array.isArray(value.lines) || value.lines.length > MAX_ROWS ||
        !isRecord(value.calculation) ||
        !["calculated", "blocked", "unavailable"].includes(value.calculation.status) ||
        !Number.isSafeInteger(value.calculation.revision) || value.calculation.revision < 0 ||
        !isAuthorization(value.authorization)) {
      return false;
    }
    if (value.saved !== (value.answered.length === 1)) return false;
    if (!value.answered.every((answer) =>
      isRecord(answer) &&
      isBoundedText(answer.id, 80) &&
      isBoundedText(answer.label, 200) &&
      Number.isFinite(answer.value) && answer.value >= 0 &&
      isBoundedText(answer.target, 80)
    )) return false;
    if (!value.missing.every((item) =>
      isRecord(item) &&
      isBoundedText(item.label, 200) &&
      isBoundedText(item.document, 120) &&
      isBoundedText(item.box, 80) &&
      isBoundedText(item.target, 80)
    )) return false;
    if (!value.lines.every((line) =>
      isRecord(line) &&
      isBoundedText(line.line, 40) &&
      isBoundedText(line.title, 200) &&
      ["expected-impact", "untouched-comparison"].includes(line.group) &&
      isBoundedText(line.change, 40) &&
      typeof line.computed === "boolean" &&
      (line.computed
        ? Number.isFinite(line.value)
        : line.value === null) &&
      isTextList(line.reason_sentences) &&
      isTextList(line.reason_codes)
    )) return false;
    const contribution = value.contribution;
    return isRecord(contribution) &&
      isRecord(contribution.payload) &&
      isRecord(contribution.payload.contribution) &&
      isRecord(contribution.payload.contribution.content);
  }

  async function readJson(response) {
    const contentLength = response.headers.get("content-length");
    if (contentLength && /^\d+$/.test(contentLength) &&
        Number(contentLength) > MAX_SNAPSHOT_BYTES) {
      await response.body?.cancel().catch(() => {});
      throw new Error("response-too-large");
    }
    if (!response.body?.getReader) {
      const text = await response.text();
      if (new TextEncoder().encode(text).byteLength > MAX_SNAPSHOT_BYTES) {
        throw new Error("response-too-large");
      }
      return JSON.parse(text);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let byteLength = 0;
    let text = "";
    while (true) {
      const { done, value: chunk } = await reader.read();
      if (done) {
        text += decoder.decode();
        break;
      }
      byteLength += chunk.byteLength;
      if (byteLength > MAX_SNAPSHOT_BYTES) {
        await reader.cancel().catch(() => {});
        throw new Error("response-too-large");
      }
      text += decoder.decode(chunk, { stream: true });
    }
    return JSON.parse(text);
  }

  function uncertainError(message) {
    outcomeUncertain = true;
    error = message;
  }

  function authorizationMessage(authorization) {
    if (authorization?.current === true) {
      return "Current calculation authorization is recorded for this result.";
    }
    if (authorization?.status === "AUTHORIZATION_ABSENT") {
      return "No current calculation authorization is recorded for this result.";
    }
    if (authorization?.status === "UNKNOWN" || authorization?.current === null) {
      return "Authorization status has not been confirmed for this update.";
    }
    return "The figures were calculated, but current calculation authorization is not confirmed.";
  }

  function lineGuidance(line) {
    if (line.reason_sentences?.length) return line.reason_sentences.join(" ");
    if (line.reason_codes?.includes("DEPENDENCY_ABSENT")) {
      return "More return information is needed before this figure can be calculated. This screen cannot identify which answer.";
    }
    return "This figure is unavailable from the saved calculation. This screen cannot identify a next answer.";
  }

  async function loadState() {
    busy = true;
    error = "";
    try {
      const response = await fetch(stateUrl("state"), {
        headers: { "Accept": "application/json" }
      });
      if (!response.ok) throw new Error("state");
      const next = await readJson(response);
      if (!isUsableSnapshot(next)) throw new Error("state-snapshot-unusable");
      setState(next);
      outcomeUncertain = false;
    } catch {
      error = outcomeUncertain
        ? "We could not check whether the last update was saved. Reload to check the current entry before trying again."
        : "The current entry could not be loaded. Reload before making a change.";
    } finally {
      busy = false;
    }
  }

  function goToWages() {
    wageInput?.focus();
  }

  async function submitWages(event) {
    event.preventDefault();
    if (!state?.contribution || busy) return;
    if (outcomeUncertain) {
      error = "Check the current saved amount before trying another update.";
      return;
    }
    busy = true;
    error = "";
    const eventBody = structuredClone(state.contribution);
    eventBody.payload.contribution.content.w2_box1 = amount;
    let responseReceived = false;
    try {
      const response = await fetch(stateUrl("contributions"), {
        method: "POST",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify(eventBody)
      });
      responseReceived = true;
      if (!response.ok) {
        if ([400, 415, 422].includes(response.status)) {
          let body;
          try {
            body = await readJson(response);
          } catch {
            body = null;
          }
          error = isRecord(body) && isBoundedText(body.error, 300)
            ? body.error
            : "The update was rejected before saving. No entry was changed.";
        } else {
          uncertainError("The update could not be confirmed. It may have been saved. Check the current entry before trying again.");
        }
        return;
      }
      const body = await readJson(response);
      if (!isUsableSnapshot(body)) {
        uncertainError("The server responded, but this page could not confirm the saved entry. It may have been saved. Check the current entry before trying again.");
        return;
      }
      setState(body);
      outcomeUncertain = false;
      requestAnimationFrame(() => statusRegion?.focus());
    } catch {
      uncertainError(responseReceived
        ? "The server response could not be read, so this update could not be confirmed. It may have been saved. Check the current entry before trying again."
        : "The connection ended before this update could be confirmed. It may have been saved. Check the current entry before trying again.");
    } finally {
      busy = false;
    }
  }

  onMount(loadState);
</script>

<svelte:head>
  <meta
    name="description"
    content="A synthetic guided W-2 entry loop for a demo federal return."
  />
</svelte:head>

<main class:complete={state?.calculation?.status === "calculated"}>
  <header class="masthead">
    <a class="wordmark" href="./index.html" aria-label="Attestory entry home">
      attestory
    </a>
    <span class="synthetic">Synthetic evaluation</span>
  </header>

  <section class="hero" aria-labelledby="page-title">
    <p class="eyebrow">2025 federal return · W-2</p>
    <h1 id="page-title">
      {#if !state}
        Entry status unavailable.
      {:else if outcomeUncertain}
        Update status not confirmed.
      {:else if !state.saved}
        Enter W-2 wages.
      {:else if state.calculation.status === "blocked"}
        Your W-2 change is saved.
      {:else if state.calculation.status === "unavailable"}
        Your W-2 change is saved.
      {:else}
        Your W-2 entry is saved.
      {/if}
    </h1>
    <p class="lede">
      {#if !state}
        The current saved amount could not be confirmed. Reload this entry
        before making a change.
      {:else if outcomeUncertain}
        This update may have been saved. Check the current entry before trying
        again; this page will not resubmit it.
      {:else if !state.saved}
        Enter the W-2 Box 1 amount to add it to this return. Until it is saved,
        this page cannot show the corrected wages.
      {:else if state.calculation.status === "blocked"}
        The W-2 amount is recorded. Some return figures are unavailable because
        required information is missing. Review the rest of the return, then
        reload this page; this screen cannot identify which answer is needed.
      {:else if state.calculation.status === "unavailable"}
        The W-2 amount is recorded, but this update could not be recalculated.
        Figures shown below are from the last calculation before this change.
        Reload the current entry to confirm the saved amount; this page will not
        resubmit it.
      {:else}
        The W-2 amount is recorded and the displayed return figures were
        calculated. You can review or correct Box 1 below.
      {/if}
    </p>
  </section>

  {#if error}
    <div class="error" role="alert">
      <strong>Check this entry.</strong>
      <span>{error}</span>
      {#if outcomeUncertain}
        <button type="button" disabled={busy} on:click={loadState}>Check saved status</button>
      {/if}
    </div>
  {/if}

  {#if !state}
    <section class="loading" aria-live="polite">
      {busy ? "Loading the synthetic return…" : "The entry session is unavailable."}
    </section>
  {:else}
    <section
      class="status-card"
      class:done={!outcomeUncertain && state.saved && state.calculation.status === "calculated"}
      aria-labelledby="status-title"
      aria-live="polite"
      tabindex="-1"
      bind:this={statusRegion}
    >
      <div class="status-mark" aria-hidden="true">
        {outcomeUncertain ? "?" : state.saved ? (state.calculation.status === "calculated" ? "✓" : "!") : "1"}
      </div>
      <div>
        <p class="status-kicker">
          {outcomeUncertain ? "Update status" : state.saved ? "Saved answer" : "Entry needed"}
        </p>
        <h2 id="status-title">
          {outcomeUncertain
            ? "Saved status needs checking"
            : state.saved
              ? "W-2 Box 1 is saved in this return"
              : "W-2 Box 1 is not saved yet"}
        </h2>
        {#if outcomeUncertain}
          <p class="currentness">The last confirmed result may be from before this update.</p>
        {:else if state.accepted && !error && !busy}
          <p class="accepted">
            Your W-2 {state.last_action === "corrected" ? "correction" : "entry"} was saved.
          </p>
        {/if}
        {#if !outcomeUncertain && state.saved && state.calculation.status !== "unavailable"}
          <p class="currentness">{authorizationMessage(state.authorization)}</p>
        {/if}
      </div>
    </section>

    {#if outcomeUncertain}
      <section class="outcome-notice" aria-live="polite" aria-label="Update status">
        <strong>This update may already be in the saved history.</strong>
        <p>Check the saved status before attempting another update.</p>
        <button type="button" disabled={busy} on:click={loadState}>Check saved status</button>
      </section>
    {:else if state.calculation.status === "unavailable"}
      <section class="outcome-notice" aria-live="polite" aria-label="Calculation status">
        <strong>The latest update is saved; no new calculation is available.</strong>
        <p>
          The figures below are from the prior calculation. For that result,
          {authorizationMessage(state.calculation.prior_authorization)} No authorization
          status was produced for the latest update.
        </p>
        <button type="button" disabled={busy} on:click={loadState}>Check saved status</button>
      </section>
    {:else if state.saved && state.calculation.status === "blocked"}
      <section class="outcome-notice" aria-live="polite" aria-label="Calculation status">
        <strong>The W-2 answer is saved, but some figures are blocked.</strong>
        <p>Review other return answers, then reload this page to check the result.</p>
      </section>
    {/if}

    {#if state.missing.length && !outcomeUncertain}
      <section class="missing" aria-labelledby="missing-title">
        <div class="section-heading">
          <p class="step">Step 1 · Know what is missing</p>
          <h2 id="missing-title">Bring this document to the entry</h2>
        </div>
        <ul>
          {#each state.missing as item}
            <li>
              <div>
                <strong>{item.label}</strong>
                <span>{item.document}, {item.box}</span>
              </div>
              <button type="button" on:click={goToWages}>Enter this fact</button>
            </li>
          {/each}
        </ul>
      </section>
    {/if}

    <div class="workspace">
      <section class="entry-panel" aria-labelledby="entry-title">
        <div class="section-heading">
          <p class="step">
            {state.answered.length
              ? "Step 4 · Correct an entered fact"
              : "Step 2 · Enter the fact"}
          </p>
          <h2 id="entry-title">
            {state.answered.length ? "Review W-2 wages" : "Enter W-2 wages"}
          </h2>
        </div>

        <form aria-label="W-2 Box 1 entry" on:submit={submitWages}>
          <label for="w2-box1">
            <span class="field-label">{formatSourceLabel()}</span>
            <span class="field-name">{W2_BOX1_FIELD.source.label}</span>
          </label>
          <p id="w2-box1-purpose" class="field-purpose">
            {formatDestinationPurpose()}
          </p>
          <div class="money-input">
            <span aria-hidden="true">$</span>
            <input
              id="w2-box1"
              name="w2-box1"
              bind:this={wageInput}
              bind:value={amount}
              inputmode="decimal"
              autocomplete="off"
              spellcheck="false"
              aria-describedby="w2-box1-purpose w2-box1-format"
              required
            />
          </div>
          <p id="w2-box1-format" class="format">
            {formatW2Box1Hint()}
          </p>
          <button class="primary" type="submit" disabled={busy || outcomeUncertain}>
            {busy
              ? "Checking…"
              : outcomeUncertain
                ? "Check saved status first"
              : state.answered.length
                ? "Update W-2 Box 1"
                : "Add W-2 Box 1"}
          </button>
        </form>

        {#if !outcomeUncertain && state.saved && state.answered.length}
          <div class="answered">
            <span>Saved in this return</span>
            <strong>{state.answered[0].label}: {money.format(state.answered[0].value)}</strong>
            <button type="button" class="text-button" on:click={goToWages}>
              Correct this fact
            </button>
          </div>
        {/if}
      </section>

      <section class="impact-panel" aria-labelledby="impact-title">
        <div class="section-heading">
          <p class="step">Step 3 · See it land</p>
          <h2 id="impact-title">What the accepted fact changed</h2>
        </div>

        <h3>{outcomeUncertain ? "Last confirmed impact" : "Expected impact"}</h3>
        <ul class="line-list">
          {#each state.lines.filter((line) => line.group === "expected-impact") as line}
            <li>
              <div>
                <span class="line-number">1040 · {line.line}</span>
                <strong>{line.title}</strong>
              </div>
              <div class="line-result">
                <span class:changed={line.change === "changed"}>{line.change}</span>
                <strong>{line.computed ? money.format(line.value) : "Unavailable"}</strong>
                {#if !line.computed}
                  <small>{lineGuidance(line)}</small>
                {/if}
              </div>
            </li>
          {/each}
        </ul>

        <h3 class="comparison-title">Held still for comparison</h3>
        <ul class="line-list comparison">
          {#each state.lines.filter((line) => line.group === "untouched-comparison") as line}
            <li>
              <div>
                <span class="line-number">1040 · {line.line}</span>
                <strong>{line.title}</strong>
              </div>
              <div class="line-result">
                <span>{line.change}</span>
                <strong>{line.computed ? money.format(line.value) : "Unavailable"}</strong>
                {#if !line.computed}
                  <small>{lineGuidance(line)}</small>
                {/if}
              </div>
            </li>
          {/each}
        </ul>
      </section>
    </div>

    {#if !outcomeUncertain && state.saved && state.calculation.status === "calculated"}
      <section class="review" aria-labelledby="review-title">
        <p class="step">Calculated figures</p>
        <h2 id="review-title">Review the result or correct W-2 Box 1</h2>
        <p>
          The displayed figures were calculated from the saved return. Their
          authorization status is shown above. You can correct W-2 Box 1 here.
        </p>
        <button type="button" on:click={goToWages}>Review W-2 Box 1</button>
      </section>
    {/if}
  {/if}
</main>

<style>
  :global(*) {
    box-sizing: border-box;
  }

  :global(html) {
    background: #f2efe8;
    color: #17251f;
    font-family:
      Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI",
      sans-serif;
  }

  :global(body) {
    margin: 0;
  }

  :global(button),
  :global(input) {
    font: inherit;
  }

  /* Every focusable control gets one focus indicator, stated once: a light
     outline plus a dark 5px ring, both !important. The rule is per control
     (every button/input/a/[tabindex="-1"] in this document), not per
     background -- a control inherits it automatically by being one of those
     elements, rather than needing its own focus rule remembered when added.
     !important is load-bearing, not decorative: Svelte's scoped-style
     compilation gives an unscoped element rule like `input { outline: 0 }`
     the same specificity as this :global(...:focus-visible) selector, and
     whichever rule sits later in the stylesheet wins a tie -- which is
     exactly how `#w2-box1`'s own resting `outline: 0` and
     `box-shadow: 0 0 0 2px #fffdf8` silently cancelled this rule twice
     before. !important makes the focus indicator win regardless of a
     control's own resting-state declarations or where they sit in the file,
     so the next control added inherits the same guarantee without anyone
     needing to notice the ordering risk. */
  :global(button:focus-visible),
  :global(input:focus-visible),
  :global(a:focus-visible),
  :global([tabindex="-1"]:focus-visible) {
    outline: 2px solid #fffdf8 !important;
    outline-offset: 2px !important;
    box-shadow: 0 0 0 5px #17251f !important;
  }

  main {
    min-height: 100vh;
    padding: 0 5vw 5rem;
    background:
      radial-gradient(circle at 88% 4%, rgba(194, 151, 84, 0.18), transparent 28rem),
      #f2efe8;
  }

  main.complete {
    background:
      radial-gradient(circle at 88% 4%, rgba(24, 115, 91, 0.18), transparent 28rem),
      #edf4ef;
  }

  .masthead {
    max-width: 1180px;
    margin: 0 auto;
    padding: 1.35rem 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #a8aaa2;
  }

  .wordmark {
    color: #17251f;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1.35rem;
    font-weight: 700;
    text-decoration: none;
  }

  .synthetic,
  .status-kicker,
  .step,
  .eyebrow,
  .line-number,
  .answered span {
    color: #3f5149;
    font-size: 0.75rem;
    font-weight: 750;
    letter-spacing: 0.09em;
    text-transform: uppercase;
  }

  .synthetic {
    padding: 0.45rem 0.7rem;
    border: 1px solid #6f7772;
    border-radius: 999px;
  }

  .hero {
    max-width: 850px;
    margin: 5rem auto 2.5rem;
    text-align: center;
  }

  h1,
  h2,
  h3,
  p {
    margin-top: 0;
  }

  h1,
  h2 {
    font-family: Georgia, "Times New Roman", serif;
    letter-spacing: -0.025em;
  }

  h1 {
    margin-bottom: 1rem;
    font-size: clamp(2.6rem, 7vw, 5.5rem);
    line-height: 0.98;
    font-weight: 500;
  }

  .lede {
    max-width: 650px;
    margin: 0 auto;
    color: #35463f;
    font-size: 1.08rem;
    line-height: 1.65;
  }

  .status-card,
  .missing,
  .workspace,
  .review,
  .error,
  .loading {
    max-width: 1180px;
    margin-left: auto;
    margin-right: auto;
  }

  .status-card {
    display: flex;
    gap: 1rem;
    align-items: center;
    padding: 1.3rem 1.5rem;
    background: #fffdf8;
    border: 1px solid #8d928c;
    border-radius: 1rem;
    box-shadow: 0 12px 38px rgba(23, 37, 31, 0.08);
  }

  .status-card.done {
    border-color: #18735b;
    background: #f5fff8;
  }

  .status-mark {
    width: 2.8rem;
    height: 2.8rem;
    display: grid;
    place-items: center;
    flex: 0 0 auto;
    border-radius: 50%;
    background: #8a5a00;
    color: #fff;
    font-size: 1.1rem;
    font-weight: 800;
  }

  .done .status-mark {
    background: #075e4f;
  }

  .status-card h2 {
    margin: 0.12rem 0 0;
    font-size: clamp(1.45rem, 3vw, 2rem);
  }

  .accepted {
    margin: 0.45rem 0 0;
    color: #075e4f;
    font-weight: 700;
  }

  .currentness {
    margin: 0.45rem 0 0;
    color: #35463f;
    line-height: 1.5;
  }

  .outcome-notice {
    max-width: 1180px;
    margin: 1.1rem auto 0;
    padding: 1.2rem 1.4rem;
    background: #fff3d7;
    border: 1px solid #9a6b16;
    border-radius: 0.8rem;
    color: #35270d;
  }

  .outcome-notice p {
    margin: 0.45rem 0 0.9rem;
    line-height: 1.55;
  }

  .missing {
    margin-top: 1.4rem;
    padding: 2rem;
    background: #fff3d7;
    border: 1px solid #9a6b16;
    border-radius: 1rem;
  }

  .section-heading h2 {
    margin-bottom: 1.25rem;
    font-size: clamp(1.65rem, 3vw, 2.25rem);
  }

  .missing ul,
  .line-list {
    margin: 0;
    padding: 0;
    list-style: none;
  }

  .missing li {
    display: flex;
    gap: 1rem;
    align-items: center;
    justify-content: space-between;
    padding-top: 1rem;
    border-top: 1px solid #b28d49;
  }

  .missing li div {
    display: grid;
    gap: 0.35rem;
  }

  button {
    min-height: 44px;
    padding: 0.7rem 1rem;
    border: 1px solid #075e4f;
    border-radius: 0.6rem;
    background: #fffdf8;
    color: #075e4f;
    font-weight: 750;
    cursor: pointer;
  }

  button:hover {
    background: #e5f3ed;
  }

  button:disabled {
    cursor: wait;
    opacity: 0.72;
  }

  .workspace {
    display: grid;
    grid-template-columns: minmax(0, 0.88fr) minmax(0, 1.12fr);
    gap: 1.4rem;
    margin-top: 1.4rem;
  }

  .entry-panel,
  .impact-panel {
    padding: clamp(1.4rem, 4vw, 2.4rem);
    background: #fffdf8;
    border: 1px solid #9da19b;
    border-radius: 1rem;
  }

  form {
    padding-top: 1rem;
    border-top: 1px solid #c5c4bd;
  }

  label {
    display: grid;
    gap: 0.35rem;
  }

  .field-label {
    color: #075e4f;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.055em;
    text-transform: uppercase;
  }

  .field-name {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1.35rem;
    font-weight: 700;
  }

  .field-purpose,
  .format {
    color: #3f5149;
    line-height: 1.55;
  }

  .field-purpose {
    margin: 0.7rem 0 1rem;
  }

  .money-input {
    display: flex;
    align-items: stretch;
    background: #fff;
    overflow: hidden;
  }

  .money-input span {
    display: flex;
    align-items: center;
    padding: 0 0.9rem 0 1rem;
    color: #35463f;
    font-size: 1.4rem;
    font-weight: 700;
    border: 2px solid #17251f;
    border-right-width: 0;
    border-radius: 0.65rem 0 0 0.65rem;
    background: #f8fbf9;
  }

  input {
    flex: 1;
    min-height: 3.4rem;
    padding: 0.75rem;
    border: 2px solid #17251f;
    border-left-width: 0;
    border-radius: 0 0.65rem 0.65rem 0;
    box-shadow: 0 0 0 2px #fffdf8;
    outline: 0;
    background: #fff;
    color: #17251f;
    font-size: 1.35rem;
    font-weight: 700;
  }

  .format {
    margin: 0.55rem 0 1rem;
    font-size: 0.86rem;
  }

  .primary {
    width: 100%;
    background: #075e4f;
    color: #fff;
  }

  .primary:hover {
    background: #03483c;
  }

  .answered {
    margin-top: 1.3rem;
    padding: 1rem;
    display: grid;
    gap: 0.45rem;
    background: #edf4ef;
    border-left: 4px solid #18735b;
  }

  .text-button {
    justify-self: start;
    min-height: 36px;
    padding: 0.35rem 0;
    border: 0;
    background: transparent;
    text-decoration: underline;
  }

  .impact-panel h3 {
    margin: 0;
    color: #3f5149;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .line-list {
    margin-top: 0.6rem;
    border-top: 1px solid #a8aaa2;
  }

  .line-list li {
    display: flex;
    gap: 1rem;
    align-items: center;
    justify-content: space-between;
    min-height: 4rem;
    padding: 0.75rem 0;
    border-bottom: 1px solid #d0cfc8;
  }

  .line-list li > div {
    display: grid;
    gap: 0.2rem;
  }

  .line-result {
    text-align: right;
  }

  .line-result span {
    color: #4b5c54;
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
  }

  .line-result span.changed {
    color: #075e4f;
  }

  .line-result small {
    max-width: 25rem;
    color: #4b5c54;
    line-height: 1.4;
  }

  .comparison-title {
    margin-top: 2rem !important;
  }

  .comparison {
    background: #f2f1ec;
    padding: 0 0.75rem;
  }

  .review {
    margin-top: 1.4rem;
    padding: clamp(1.6rem, 5vw, 3rem);
    text-align: center;
    background: #075e4f;
    color: #fff;
    border-radius: 1rem;
  }

  .review .step {
    color: #cde9dd;
  }

  .review h2 {
    margin-bottom: 0.6rem;
    font-size: clamp(2rem, 5vw, 3.3rem);
  }

  .review p:not(.step) {
    max-width: 650px;
    margin: 0 auto 1.25rem;
    color: #eef9f4;
    line-height: 1.6;
  }

  .review button {
    border-color: #fff;
    color: #075e4f;
  }

  .error,
  .loading {
    margin-bottom: 1.4rem;
    padding: 1rem 1.2rem;
    border-radius: 0.7rem;
  }

  .error {
    display: grid;
    gap: 0.25rem;
    background: #fff0ec;
    border: 2px solid #9b2c17;
    color: #671a0c;
  }

  .error button {
    justify-self: start;
    margin-top: 0.35rem;
  }

  .loading {
    text-align: center;
    background: #fffdf8;
    border: 1px solid #8d928c;
  }

  @media (max-width: 800px) {
    main {
      padding-left: 1rem;
      padding-right: 1rem;
    }

    .hero {
      margin-top: 3.5rem;
    }

    .workspace {
      grid-template-columns: 1fr;
    }

    .missing li,
    .line-list li {
      align-items: flex-start;
    }
  }

  @media (max-width: 520px) {
    .missing li {
      flex-direction: column;
    }

    .missing button {
      width: 100%;
    }

    .line-list li {
      gap: 0.5rem;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
      scroll-behavior: auto !important;
      transition: none !important;
    }
  }
</style>
