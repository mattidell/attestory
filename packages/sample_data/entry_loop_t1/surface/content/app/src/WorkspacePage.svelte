<script>
  import { onMount } from "svelte";

  let state = null;
  let error = "";
  let busy = false;

  const money = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2
  });

  function stateUrl(name) {
    return new URL(`./api/${name}`, window.location.href);
  }

  // "Fact families" has no field of its own in /api/state -- field_contract
  // is keyed one entry per fact the workspace can accept, so its key count
  // *is* that number today. Reading it here instead of writing "1" keeps
  // this card honest if a second family is ever added; a literal wouldn't
  // notice.
  function factFamilyDocuments(currentState) {
    return Object.values(currentState.field_contract).map(
      (field) => field.source.document
    );
  }

  async function loadState() {
    busy = true;
    error = "";
    try {
      const response = await fetch(stateUrl("state"), {
        headers: { "Accept": "application/json" }
      });
      if (!response.ok) throw new Error("state");
      state = await response.json();
    } catch {
      error = "The workspace could not be loaded. Nothing was changed.";
    } finally {
      busy = false;
    }
  }

  onMount(loadState);
</script>

<svelte:head>
  <meta
    name="description"
    content="The workspace for a synthetic W-2 return: scope, attention, and the record."
  />
</svelte:head>

<main class:complete={state?.complete}>
  <header class="masthead">
    <span class="wordmark">attestory</span>
    <span class="synthetic">Synthetic evaluation</span>
  </header>

  {#if error}
    <div class="error" role="alert">
      <strong>Check the workspace.</strong>
      <span>{error}</span>
    </div>
  {/if}

  {#if !state}
    <section class="loading" aria-live="polite">
      {busy ? "Loading the synthetic workspace…" : "The workspace is unavailable."}
    </section>
  {:else}
    <section class="hero" aria-labelledby="workspace-title">
      <p class="eyebrow">2025 federal return · workspace</p>
      <h1 id="workspace-title">
        {state.complete ? "Your record is complete." : "Here's where your record stands."}
      </h1>
      <p class="lede">
        {#if state.complete}
          Every required fact in this evaluation is present and the return is
          fully computed. Open the record below to review it or make a
          correction.
        {:else}
          This workspace currently tracks one synthetic fact family. See
          what's outstanding below, or open the record to look around.
        {/if}
      </p>
    </section>

    <section class="scope-card" aria-labelledby="scope-title">
      <h2 id="scope-title">Scope</h2>
      <dl>
        <div>
          <dt>Fact families</dt>
          <dd>
            {factFamilyDocuments(state).length} · {factFamilyDocuments(state).join(", ")}
          </dd>
        </div>
        <div>
          <dt>Facts entered</dt>
          <dd>{state.answered.length} of {factFamilyDocuments(state).length}</dd>
        </div>
        <div>
          <dt>Evaluation lines computed</dt>
          <dd>{state.lines.filter((line) => line.computed).length} of {state.lines.length}</dd>
        </div>
      </dl>
    </section>

    {#if state.missing.length}
      <section class="attention" aria-labelledby="attention-title">
        <div class="section-heading">
          <p class="step">Needs attention</p>
          <h2 id="attention-title">What's outstanding, and why</h2>
        </div>
        <ul>
          {#each state.missing as item}
            <li>
              <div>
                <strong>{item.label}</strong>
                <span>{item.document}, {item.box}</span>
                <span class="why">
                  {state.lines.filter((line) => line.group === "expected-impact").length}
                  evaluation line(s) are waiting on this fact.
                </span>
              </div>
              <a class="button-link" href="./index.html">Enter this fact</a>
            </li>
          {/each}
        </ul>
      </section>
    {:else}
      <section class="attention done" aria-labelledby="attention-title">
        <p class="step">Needs attention</p>
        <h2 id="attention-title">Nothing outstanding</h2>
        <p>
          Every fact this workspace tracks has been entered and every line is
          computed.
        </p>
      </section>
    {/if}

    <section class="record-map" aria-labelledby="map-title">
      <div class="section-heading">
        <p class="step">The record</p>
        <h2 id="map-title">Open the record</h2>
      </div>
      <p class="map-note">
        Each line below is part of the walkable explanation in the entry
        surface. Opening a line takes you straight to its explanation there;
        this view does not repeat it.
      </p>
      <ul class="line-list map-list">
        {#each state.lines as line (line.line)}
          <li>
            <a
              class="map-row"
              href={"./index.html#line=" + encodeURIComponent(line.line)}
            >
              <span class="line-number">1040 · {line.line}</span>
              <span class="map-row-title">{line.title}</span>
              <span class="map-row-value">
                <span class:changed={line.change === "changed"}>{line.change}</span>
                <strong>{line.computed ? money.format(line.value) : "Waiting for W-2"}</strong>
              </span>
            </a>
          </li>
        {/each}
      </ul>
      <a class="primary button-link" href="./index.html">
        {state.answered.length ? "Open W-2 entry" : "Start entry"}
      </a>
    </section>
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

  :global(a),
  :global(button) {
    font: inherit;
  }

  :global(a:focus-visible),
  :global(button:focus-visible),
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
  }

  .synthetic,
  .step,
  .eyebrow {
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

  .scope-card,
  .attention,
  .record-map,
  .error,
  .loading {
    max-width: 1180px;
    margin-left: auto;
    margin-right: auto;
  }

  .scope-card {
    margin-top: 1.4rem;
    padding: 1.5rem 2rem;
    background: #fffdf8;
    border: 1px solid #8d928c;
    border-radius: 1rem;
  }

  .scope-card h2 {
    margin-bottom: 1rem;
    font-size: 1.2rem;
  }

  .scope-card dl {
    margin: 0;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr));
    gap: 1rem;
  }

  .scope-card dl div {
    display: grid;
    gap: 0.2rem;
  }

  .scope-card dt {
    color: #3f5149;
    font-size: 0.75rem;
    font-weight: 750;
    letter-spacing: 0.09em;
    text-transform: uppercase;
  }

  .scope-card dd {
    margin: 0;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1.35rem;
    font-weight: 700;
  }

  .section-heading h2 {
    margin-bottom: 1.25rem;
    font-size: clamp(1.65rem, 3vw, 2.25rem);
  }

  .attention {
    margin-top: 1.4rem;
    padding: 2rem;
    background: #fff3d7;
    border: 1px solid #9a6b16;
    border-radius: 1rem;
  }

  .attention.done {
    background: #f5fff8;
    border-color: #18735b;
  }

  .attention ul {
    margin: 0;
    padding: 0;
    list-style: none;
  }

  .attention li {
    display: flex;
    gap: 1rem;
    align-items: center;
    justify-content: space-between;
    padding-top: 1rem;
    border-top: 1px solid #b28d49;
  }

  .attention li div {
    display: grid;
    gap: 0.35rem;
  }

  .why {
    color: #3f5149;
    font-size: 0.85rem;
  }

  .record-map {
    margin-top: 1.4rem;
    padding: clamp(1.4rem, 4vw, 2.4rem);
    background: #fffdf8;
    border: 1px solid #9da19b;
    border-radius: 1rem;
  }

  .map-note {
    margin: 0 0 1rem;
    color: #3f5149;
    font-size: 0.85rem;
    line-height: 1.5;
  }

  .line-list {
    margin: 0;
    padding: 0;
    list-style: none;
    border-top: 1px solid #a8aaa2;
  }

  .map-list li {
    border-bottom: 1px solid #d0cfc8;
  }

  .map-row {
    min-height: 4rem;
    padding: 0.75rem 0.5rem;
    display: flex;
    gap: 1rem;
    align-items: center;
    justify-content: space-between;
    color: inherit;
    text-decoration: none;
    border-radius: 0.5rem;
  }

  .map-row:hover {
    background: #f2f1ec;
  }

  .line-number {
    color: #3f5149;
    font-size: 0.75rem;
    font-weight: 750;
    letter-spacing: 0.09em;
    text-transform: uppercase;
  }

  .map-row-title {
    flex: 1;
    font-weight: 700;
  }

  .map-row-value {
    display: grid;
    gap: 0.2rem;
    text-align: right;
  }

  .map-row-value span {
    color: #4b5c54;
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
  }

  .map-row-value span.changed {
    color: #075e4f;
  }

  .button-link {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 44px;
    padding: 0.7rem 1rem;
    border: 1px solid #075e4f;
    border-radius: 0.6rem;
    background: #fffdf8;
    color: #075e4f;
    font-weight: 750;
    text-decoration: none;
    cursor: pointer;
  }

  .button-link:hover {
    background: #e5f3ed;
  }

  .primary.button-link {
    margin-top: 1.2rem;
    width: 100%;
    background: #075e4f;
    color: #fff;
  }

  .primary.button-link:hover {
    background: #03483c;
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
  }

  @media (max-width: 520px) {
    .attention li {
      flex-direction: column;
      align-items: flex-start;
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
