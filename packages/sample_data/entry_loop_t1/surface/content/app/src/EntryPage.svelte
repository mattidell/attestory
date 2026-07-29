<script>
  import { onMount } from "svelte";
  import { formatW2Box1Hint } from "./w2-box1-format.js";

  let state = null;
  let amount = "";
  let error = "";
  let busy = false;
  let wageInput;
  let statusRegion;

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

  async function loadState() {
    busy = true;
    error = "";
    try {
      const response = await fetch(stateUrl("state"), {
        headers: { "Accept": "application/json" }
      });
      if (!response.ok) throw new Error("state");
      setState(await response.json());
    } catch {
      error = "The entry session could not be loaded. No entry was changed.";
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
    busy = true;
    error = "";
    const eventBody = structuredClone(state.contribution);
    eventBody.payload.contribution.content.w2_box1 = amount;
    try {
      const response = await fetch(stateUrl("contributions"), {
        method: "POST",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify(eventBody)
      });
      const body = await response.json();
      if (!response.ok) {
        error = body.error || "The contribution was not accepted. No entry was changed.";
        return;
      }
      setState(body);
      requestAnimationFrame(() => statusRegion?.focus());
    } catch {
      error = "The contribution was not accepted. No entry was changed.";
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

<main class:complete={state?.complete}>
  <header class="masthead">
    <a class="wordmark" href="./index.html" aria-label="Attestory entry home">
      attestory
    </a>
    <span class="synthetic">Synthetic evaluation</span>
  </header>

  <section class="hero" aria-labelledby="page-title">
    <p class="eyebrow">2025 federal return · W-2</p>
    <h1 id="page-title">
      {state?.complete ? "Your entry is complete." : "One document closes the gap."}
    </h1>
    <p class="lede">
      {#if state?.complete}
        Every required fact in this evaluation is present and the return is fully
        computed. You can still review or correct W-2 Box 1 below.
      {:else}
        Your other synthetic facts are already in place. Enter the outstanding
        W-2 wages to compute the return.
      {/if}
    </p>
  </section>

  {#if error}
    <div class="error" role="alert">
      <strong>Check this entry.</strong>
      <span>{error}</span>
    </div>
  {/if}

  {#if !state}
    <section class="loading" aria-live="polite">
      {busy ? "Loading the synthetic return…" : "The entry session is unavailable."}
    </section>
  {:else}
    <section
      class="status-card"
      class:done={state.complete}
      aria-labelledby="status-title"
      aria-live="polite"
      tabindex="-1"
      bind:this={statusRegion}
    >
      <div class="status-mark" aria-hidden="true">{state.complete ? "✓" : "1"}</div>
      <div>
        <p class="status-kicker">{state.complete ? "Return status" : "Still needed"}</p>
        <h2 id="status-title">
          {state.complete
            ? "0 missing facts · fully computed"
            : "1 missing fact · W-2 Box 1"}
        </h2>
        {#if state.accepted}
          <p class="accepted">
            Accepted. The {state.last_action === "corrected" ? "correction" : "entry"}
            landed through a contribution.
          </p>
        {/if}
      </div>
    </section>

    {#if state.missing.length}
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
            <span class="field-label">Form W-2 · Box 1</span>
            <span class="field-name">Wages, tips, other compensation</span>
          </label>
          <p id="w2-box1-purpose" class="field-purpose">
            This amount feeds Form 1040 line 1a and resolves the missing wages
            needed to compute income.
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
          <button class="primary" type="submit" disabled={busy}>
            {busy
              ? "Checking…"
              : state.answered.length
                ? "Update W-2 Box 1"
                : "Add W-2 Box 1"}
          </button>
        </form>

        {#if state.answered.length}
          <div class="answered">
            <span>Answered fact</span>
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

        <h3>Expected impact</h3>
        <ul class="line-list">
          {#each state.lines.filter((line) => line.group === "expected-impact") as line}
            <li>
              <div>
                <span class="line-number">1040 · {line.line}</span>
                <strong>{line.title}</strong>
              </div>
              <div class="line-result">
                <span class:changed={line.change === "changed"}>{line.change}</span>
                <strong>{line.computed ? money.format(line.value) : "Waiting for W-2"}</strong>
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
                <strong>{money.format(line.value)}</strong>
              </div>
            </li>
          {/each}
        </ul>
      </section>
    </div>

    {#if state.complete}
      <section class="review" aria-labelledby="review-title">
        <p class="step">Step 5 · Know it is complete</p>
        <h2 id="review-title">Done — no further required entry</h2>
        <p>
          Zero facts are missing and every evaluation line is computed. Review
          the result above, or return to W-2 Box 1 to make a correction.
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

  :global(button:focus-visible),
  :global(input:focus-visible),
  :global(a:focus-visible),
  :global([tabindex="-1"]:focus-visible) {
    outline: 2px solid #fffdf8;
    outline-offset: 2px;
    box-shadow: 0 0 0 5px #17251f;
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
