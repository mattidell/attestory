// A minimal test double standing in for lib/cdp.mjs's CDPClient, so the
// executor's lifecycle/reason-code logic can be exercised without a real
// Chrome process. `handlers` maps a CDP method name to
// `(params, sessionId, callIndex) => result` (may throw/reject); anything
// not listed resolves to `{}`. `waitForImpl` maps an event method name to
// `(sessionId, timeoutMs) => Promise`.

export function makeFakeCDPClient({ handlers = {}, waitForImpl = {} } = {}) {
  const callCounts = new Map();
  const listeners = new Map();

  return {
    async send(method, params, sessionId) {
      const count = callCounts.get(method) || 0;
      callCounts.set(method, count + 1);
      const impl = handlers[method];
      if (!impl) return {};
      return impl(params, sessionId, count);
    },
    on(method, handler, sessionId) {
      if (!listeners.has(method)) listeners.set(method, new Set());
      const entry = { handler, sessionId };
      listeners.get(method).add(entry);
      return () => listeners.get(method).delete(entry);
    },
    emit(method, params, sessionId) {
      const set = listeners.get(method);
      if (!set) return;
      for (const entry of set) {
        if (entry.sessionId !== undefined && entry.sessionId !== sessionId) continue;
        entry.handler(params, sessionId);
      }
    },
    async waitFor(method, sessionId, timeoutMs) {
      const impl = waitForImpl[method];
      if (impl) return impl(sessionId, timeoutMs);
      return {};
    },
    close() {},
  };
}

let targetCounter = 0;
export function nextTargetId() {
  targetCounter += 1;
  return `fake-target-${targetCounter}`;
}

export function makeFakeChromeHandle({ wsUrl = "ws://fake", exited = () => false } = {}) {
  return {
    wsUrl,
    isExited: exited,
    onExit() {},
    async dispose() {},
  };
}
