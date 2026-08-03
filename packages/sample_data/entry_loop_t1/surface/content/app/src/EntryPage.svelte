<script>
  import { onMount, tick } from "svelte";
  import { formatW2Box1Hint } from "./w2-box1-format.js";
  import {
    W2_BOX1_FIELD,
    formatSourceLabel as formatW2SourceLabel,
    formatDestinationPurpose as formatW2DestinationPurpose
  } from "./w2-box1-field.js";
  import { formatDiv1bHint } from "./div1b-format.js";
  import {
    DIV1B_FIELD,
    formatSourceLabel as formatDiv1bSourceLabel,
    formatDestinationPurpose as formatDiv1bDestinationPurpose
  } from "./div1b-field.js";

  // One entry per fact this workspace can accept, mirroring the backend's
  // own _FactFamily list (entry_loop.py) -- exactly two concrete fields,
  // each described once here, rendered by one shared template below rather
  // than one hand-written block per field. A field's label/purpose/format
  // text is still compiled in from its own imported declaration module, not
  // read from the API response -- that's what lets a mutated declaration
  // file provably reach the rendered DOM (see RenderedFieldDerivation).
  const FIELDS = [
    {
      key: "w2-box1",
      contentField: "w2_box1",
      field: W2_BOX1_FIELD,
      hint: formatW2Box1Hint(),
      sourceLabel: formatW2SourceLabel(),
      destinationPurpose: formatW2DestinationPurpose()
    },
    {
      key: "div1b-qualified",
      contentField: "div1b_qualified",
      field: DIV1B_FIELD,
      hint: formatDiv1bHint(),
      sourceLabel: formatDiv1bSourceLabel(),
      destinationPurpose: formatDiv1bDestinationPurpose()
    }
  ];
  const FIELDS_BY_KEY = Object.fromEntries(FIELDS.map((f) => [f.key, f]));

  let state = null;
  let error = "";
  let busy = false;
  // One input value and one input ref per fact key, not a single pair --
  // the loop's original single-field shape assumed there was only ever one
  // form on the page.
  let amounts = {};
  let inputRefs = {};
  let statusRegion;
  // The trail of lines opened so far, in the order opened. A dependency
  // chip appends rather than replaces, so the whole path stays visible --
  // the reader's own click history becomes the breadcrumb, with real values
  // at each step rather than just line numbers.
  let expandedLines = [];

  // A trip to the workspace and back is a real page reload, not an
  // in-memory view swap, so the trail above would otherwise reset to
  // closed on return. sessionStorage survives that reload (and clears
  // itself when the tab closes), so restoring from it here is what makes
  // "back to workspace" not also mean "lost your place."
  const EXPANDED_LINES_KEY = "attestory-entry-expanded-lines";

  function restoreExpandedLines() {
    try {
      const raw = sessionStorage.getItem(EXPANDED_LINES_KEY);
      if (raw) expandedLines = JSON.parse(raw);
    } catch {
      // Storage unavailable (e.g. private browsing) -- start with nothing
      // expanded rather than failing the page load over it.
    }
  }

  function persistExpandedLines() {
    try {
      sessionStorage.setItem(EXPANDED_LINES_KEY, JSON.stringify(expandedLines));
    } catch {
      // Nothing recoverable to do here; the trail just won't survive the
      // round trip this time.
    }
  }

  function toggleExplanation(lineId) {
    expandedLines = expandedLines.includes(lineId)
      ? expandedLines.filter((id) => id !== lineId)
      : [...expandedLines, lineId];
    persistExpandedLines();
  }

  async function jumpToLine(lineId) {
    if (!expandedLines.includes(lineId)) {
      expandedLines = [...expandedLines, lineId];
      persistExpandedLines();
    }
    await tick();
    const row = document.getElementById(`line-${lineId}`);
    row?.scrollIntoView({ behavior: "smooth", block: "center" });
    row?.focus();
  }

  function focusField(key) {
    inputRefs[key]?.focus();
  }

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
    const updated = { ...amounts };
    for (const item of next.answered ?? []) {
      updated[item.id] = String(item.value);
    }
    amounts = updated;
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

  // The workspace's record map deep-links straight to one line via a URL
  // fragment, not a query string -- the server's own request handler
  // rejects any request carrying a query string (`_target()` in
  // entry_loop.py), a data-safety boundary this page has no business
  // trying to work around. A fragment never leaves the browser, so it
  // reaches this page without ever touching the server at all. A second,
  // distinct fragment shape (#field=) does the same for a specific
  // outstanding fact's input, since a line and a field are different
  // targets on this page.
  function consumeLineFromHash() {
    const match = location.hash.match(/^#line=(.+)$/);
    if (!match) return null;
    return decodeURIComponent(match[1]);
  }

  function consumeFieldFromHash() {
    const match = location.hash.match(/^#field=(.+)$/);
    if (!match) return null;
    return decodeURIComponent(match[1]);
  }

  async function submitField(event, fieldDef) {
    event.preventDefault();
    const template = state?.contributions?.[fieldDef.key];
    if (!template || busy) return;
    busy = true;
    error = "";
    const eventBody = structuredClone(template);
    eventBody.payload.contribution.content[fieldDef.contentField] =
      amounts[fieldDef.key];
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

  onMount(async () => {
    restoreExpandedLines();
    await loadState();
    const targetLine = consumeLineFromHash();
    if (targetLine) {
      await jumpToLine(targetLine);
      history.replaceState(null, "", location.pathname + location.search);
    }
    const targetField = consumeFieldFromHash();
    if (targetField) {
      await tick();
      focusField(targetField);
      history.replaceState(null, "", location.pathname + location.search);
    }
  });
</script>

<svelte:head>
  <meta
    name="description"
    content="A synthetic guided entry loop for a demo federal return."
  />
</svelte:head>

<main class:complete={state?.complete}>
  <header class="masthead">
    <a class="wordmark" href="./index.html" aria-label="Attestory entry home">
      attestory
    </a>
    <div class="masthead-actions">
      <a class="workspace-link" href="./workspace.html">← Back to workspace</a>
      <span class="synthetic">Synthetic evaluation</span>
    </div>
  </header>

  <section class="hero" aria-labelledby="page-title">
    <p class="eyebrow">2025 federal return</p>
    <h1 id="page-title">
      {state?.complete ? "Your entry is complete." : "A few facts close the gap."}
    </h1>
    <p class="lede">
      {#if state?.complete}
        Every required fact in this evaluation is present and the return is fully
        computed. You can still review or correct an entered fact below.
      {:else}
        Enter the outstanding facts below to compute the return.
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
      <div class="status-mark" aria-hidden="true">
        {state.complete ? "✓" : state.missing.length}
      </div>
      <div>
        <p class="status-kicker">{state.complete ? "Return status" : "Still needed"}</p>
        <h2 id="status-title">
          {state.complete
            ? "0 missing facts · fully computed"
            : `${state.missing.length} missing fact${state.missing.length === 1 ? "" : "s"}`}
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
          <p class="step">Know what is missing</p>
          <h2 id="missing-title">Bring these documents to the entry</h2>
        </div>
        <ul>
          {#each state.missing as item}
            <li>
              <div>
                <strong>{item.label}</strong>
                <span>{item.document}, {item.box}</span>
              </div>
              <button type="button" on:click={() => focusField(item.target)}>
                Enter {item.document} {item.box}
              </button>
            </li>
          {/each}
        </ul>
      </section>
    {/if}

    <div class="entry-grid">
      <div class="entry-panels">
        {#each FIELDS as fieldDef (fieldDef.key)}
          {@const answered = state.answered.find((a) => a.id === fieldDef.key)}
          <section class="entry-panel" aria-labelledby={`entry-title-${fieldDef.key}`}>
            <div class="section-heading">
              <p class="step">{answered ? "Correct an entered fact" : "Enter the fact"}</p>
              <h2 id={`entry-title-${fieldDef.key}`}>
                {answered
                  ? `Review ${fieldDef.field.source.label}`
                  : `Enter ${fieldDef.field.source.label}`}
              </h2>
            </div>

            <form
              aria-label={`${fieldDef.field.source.document} ${fieldDef.field.source.box} entry`}
              on:submit={(event) => submitField(event, fieldDef)}
            >
              <label for={fieldDef.key}>
                <span class="field-label">{fieldDef.sourceLabel}</span>
                <span class="field-name">{fieldDef.field.source.label}</span>
              </label>
              <p id={`${fieldDef.key}-purpose`} class="field-purpose">
                {fieldDef.destinationPurpose}
              </p>
              <div class="money-input">
                <span aria-hidden="true">$</span>
                <input
                  id={fieldDef.key}
                  name={fieldDef.key}
                  bind:this={inputRefs[fieldDef.key]}
                  bind:value={amounts[fieldDef.key]}
                  inputmode="decimal"
                  autocomplete="off"
                  spellcheck="false"
                  aria-describedby={`${fieldDef.key}-purpose ${fieldDef.key}-format`}
                  required
                />
              </div>
              <p id={`${fieldDef.key}-format`} class="format">
                {fieldDef.hint}
              </p>
              <button class="primary" type="submit" disabled={busy}>
                {busy
                  ? "Checking…"
                  : answered
                    ? `Update ${fieldDef.field.source.label}`
                    : `Add ${fieldDef.field.source.label}`}
              </button>
            </form>

            {#if answered}
              <div class="answered">
                <span>Answered fact</span>
                <strong>{answered.label}: {money.format(answered.value)}</strong>
                <button
                  type="button"
                  class="text-button"
                  on:click={() => focusField(fieldDef.key)}
                >
                  Correct {answered.label}
                </button>
              </div>
            {/if}
          </section>
        {/each}
      </div>

      <section class="impact-panel" aria-labelledby="impact-title">
        <div class="section-heading">
          <p class="step">See it land</p>
          <h2 id="impact-title">What the accepted facts changed</h2>
        </div>

        <h3>Expected impact</h3>
        <ul class="line-list">
          {#each state.lines.filter((line) => line.group === "expected-impact") as line (line.line)}
            {@render lineRow(line)}
          {/each}
        </ul>

        <h3 class="comparison-title">Held still for comparison</h3>
        <ul class="line-list comparison">
          {#each state.lines.filter((line) => line.group === "untouched-comparison") as line (line.line)}
            {@render lineRow(line)}
          {/each}
        </ul>
      </section>
    </div>

    {#if state.complete}
      <section class="review" aria-labelledby="review-title">
        <p class="step">Know it is complete</p>
        <h2 id="review-title">Done — no further required entry</h2>
        <p>
          Zero facts are missing and every evaluation line is computed. Review
          the result above, or correct any entered fact in its own panel.
        </p>
      </section>
    {/if}

    {#snippet lineRow(line)}
      <li id={`line-${line.line}`} tabindex="-1">
        <div class="line-row">
          <div>
            <span class="line-number">1040 · {line.line}</span>
            <strong>{line.title}</strong>
          </div>
          <div class="line-result">
            <span class:changed={line.change === "changed"}>{line.change}</span>
            <strong>{line.computed ? money.format(line.value) : "Waiting"}</strong>
          </div>
        </div>

        {#if line.explanation}
          <button
            type="button"
            class="explain-toggle"
            aria-expanded={expandedLines.includes(line.line)}
            aria-controls={`explain-${line.line}`}
            on:click={() => toggleExplanation(line.line)}
          >
            {expandedLines.includes(line.line)
              ? `Hide how line ${line.line} was reached`
              : `How was line ${line.line} reached?`}
          </button>

          {#if expandedLines.includes(line.line)}
            <div class="explanation" id={`explain-${line.line}`}>
              <p class="explanation-description">{line.explanation.description}</p>

              {#if line.explanation.rules.length}
                <p class="explanation-kicker">Rule identifier</p>
                <ul class="detail-list">
                  {#each line.explanation.rules as rule}
                    <li>{rule.id} <span>({rule.role})</span></li>
                  {/each}
                </ul>
              {/if}

              {#if line.explanation.dependsOn.length}
                <p class="explanation-kicker">Depends on</p>
                <ul class="dependency-list">
                  {#each line.explanation.dependsOn as dep}
                    <li>
                      <button
                        type="button"
                        class="dependency-chip"
                        class:traces-to-entry={dep.entryTargets.length > 0}
                        on:click={() => jumpToLine(dep.line)}
                      >
                        1040 · {dep.line} — {dep.title}: {money.format(dep.value)}
                        {#if dep.entryTargets.length}
                          <span class="chip-trace">· traces to entry</span>
                        {/if}
                      </button>
                    </li>
                  {/each}
                </ul>
              {/if}

              {#if line.explanation.citedEvidence.length}
                <p class="explanation-kicker">Cited evidence</p>
                <ul class="citation-list">
                  {#each line.explanation.citedEvidence as site}
                    <li>
                      <strong>{site.label}</strong>
                      <span>{site.context}</span>
                    </li>
                  {/each}
                </ul>
              {/if}

              {#if line.explanation.operations.length || line.explanation.parameters.length}
                <p class="explanation-kicker">Operation and parameter identifiers</p>
                <ul class="detail-list">
                  {#each line.explanation.operations as operation}
                    <li>{operation}</li>
                  {/each}
                  {#each line.explanation.parameters as parameter}
                    <li>{parameter}</li>
                  {/each}
                </ul>
              {/if}

              {#if !line.explanation.hasSupport}
                <p class="explanation-note">
                  No dependency or evidence is declared for this line beyond its rule.
                </p>
              {/if}

              {#if line.explanation.entryTargets.length}
                <div class="actions">
                  {#each line.explanation.entryTargets as targetKey}
                    <button
                      type="button"
                      class="text-button"
                      on:click={() => focusField(targetKey)}
                    >
                      Jump to {FIELDS_BY_KEY[targetKey].field.source.label} entry (from line {line.line})
                    </button>
                  {/each}
                </div>
              {/if}
            </div>
          {/if}
        {/if}
      </li>
    {/snippet}
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

  .masthead-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .workspace-link {
    color: #075e4f;
    font-size: 0.85rem;
    font-weight: 750;
    text-decoration: underline;
  }

  .synthetic,
  .status-kicker,
  .step,
  .eyebrow,
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
  .entry-grid,
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

  .entry-grid {
    display: grid;
    grid-template-columns: minmax(0, 0.88fr) minmax(0, 1.12fr);
    gap: 1.4rem;
    margin-top: 1.4rem;
  }

  .entry-panels {
    display: grid;
    gap: 1.4rem;
    align-content: start;
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
    padding: 0.75rem 0;
    border-bottom: 1px solid #d0cfc8;
  }

  .line-row {
    display: flex;
    gap: 1rem;
    align-items: center;
    justify-content: space-between;
    min-height: 4rem;
  }

  .line-row > div {
    display: grid;
    gap: 0.2rem;
  }

  .line-number {
    color: #3f5149;
    font-size: 0.75rem;
    font-weight: 750;
    letter-spacing: 0.09em;
    text-transform: uppercase;
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

  .explain-toggle {
    min-height: 36px;
    margin-top: 0.35rem;
    padding: 0.35rem 0;
    border: 0;
    background: transparent;
    color: #075e4f;
    font-weight: 700;
    text-decoration: underline;
    cursor: pointer;
  }

  .explanation {
    margin-top: 0.6rem;
    padding: 1rem;
    background: #f2f1ec;
    border-left: 4px solid #075e4f;
    border-radius: 0.4rem;
  }

  .explanation-description {
    margin: 0;
    color: #17251f;
    line-height: 1.55;
  }

  .explanation-kicker {
    margin: 0.85rem 0 0.4rem;
    color: #3f5149;
    font-size: 0.75rem;
    font-weight: 750;
    letter-spacing: 0.09em;
    text-transform: uppercase;
  }

  .explanation-note {
    margin: 0.85rem 0 0;
    color: #3f5149;
    font-size: 0.85rem;
    font-style: italic;
  }

  .citation-list,
  .detail-list,
  .dependency-list {
    margin: 0;
    padding: 0;
    list-style: none;
    display: grid;
    gap: 0.5rem;
  }

  .citation-list li,
  .detail-list li {
    display: grid;
    gap: 0.1rem;
    padding: 0;
    border: 0;
  }

  .citation-list span,
  .detail-list li span {
    color: #3f5149;
    font-size: 0.85rem;
  }

  .detail-list li {
    color: #17251f;
    font-size: 0.9rem;
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
  }

  .dependency-list li {
    padding: 0;
    border: 0;
  }

  .dependency-chip {
    min-height: 40px;
    padding: 0.5rem 0.85rem;
    border: 1px solid #075e4f;
    border-radius: 0.5rem;
    background: #fff;
    color: #075e4f;
    font-weight: 700;
    cursor: pointer;
  }

  .dependency-chip:hover {
    background: #e5f3ed;
  }

  .dependency-chip.traces-to-entry {
    border-width: 2px;
  }

  .chip-trace {
    display: block;
    margin-top: 0.2rem;
    color: #3f5149;
    font-size: 0.72rem;
    font-weight: 750;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  .actions {
    margin-top: 1rem;
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .actions .text-button {
    padding: 0;
    min-height: 36px;
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

    .entry-grid {
      grid-template-columns: 1fr;
    }

    .missing li {
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
