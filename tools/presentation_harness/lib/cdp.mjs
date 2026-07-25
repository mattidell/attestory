// Minimal dependency-free CDP client. Node's runtime WebSocket global is
// used directly (no npm package) per the Track 1 evidence-rung ceiling.
// Uses the "flattened" session protocol: one WebSocket to the browser
// endpoint, one Target per case, one attach session per Target.

export class CDPClient {
  constructor(ws) {
    this._ws = ws;
    this._nextId = 1;
    this._pending = new Map();
    this._eventListeners = new Map(); // method -> Set<{sessionId, handler}>
    this._closed = false;
    ws.addEventListener("message", (ev) => this._onMessage(ev));
    ws.addEventListener("close", () => this._onClose());
  }

  static connect(wsUrl) {
    return new Promise((resolve, reject) => {
      const ws = new WebSocket(wsUrl);
      const onOpen = () => {
        ws.removeEventListener("error", onError);
        resolve(new CDPClient(ws));
      };
      const onError = (err) => {
        ws.removeEventListener("open", onOpen);
        reject(err instanceof Error ? err : new Error("CDP websocket error"));
      };
      ws.addEventListener("open", onOpen, { once: true });
      ws.addEventListener("error", onError, { once: true });
    });
  }

  _onMessage(ev) {
    const msg = JSON.parse(ev.data);
    if (Object.prototype.hasOwnProperty.call(msg, "id")) {
      const pending = this._pending.get(msg.id);
      if (!pending) return;
      this._pending.delete(msg.id);
      if (msg.error) {
        pending.reject(new Error(`CDP error: ${JSON.stringify(msg.error)}`));
      } else {
        pending.resolve(msg.result);
      }
      return;
    }
    const listeners = this._eventListeners.get(msg.method);
    if (!listeners) return;
    for (const entry of listeners) {
      if (entry.sessionId !== undefined && entry.sessionId !== msg.sessionId) continue;
      entry.handler(msg.params, msg.sessionId);
    }
  }

  _onClose() {
    this._closed = true;
    for (const pending of this._pending.values()) {
      pending.reject(new Error("CDP connection closed"));
    }
    this._pending.clear();
  }

  send(method, params = {}, sessionId) {
    if (this._closed) {
      return Promise.reject(new Error("CDP connection closed"));
    }
    return new Promise((resolve, reject) => {
      const id = this._nextId;
      this._nextId += 1;
      const message = { id, method, params };
      if (sessionId !== undefined) message.sessionId = sessionId;
      this._pending.set(id, { resolve, reject });
      this._ws.send(JSON.stringify(message));
    });
  }

  /** Register a listener for one CDP event, optionally scoped to a session. */
  on(method, handler, sessionId) {
    if (!this._eventListeners.has(method)) {
      this._eventListeners.set(method, new Set());
    }
    const entry = { sessionId, handler };
    this._eventListeners.get(method).add(entry);
    return () => this._eventListeners.get(method).delete(entry);
  }

  /** Wait for one occurrence of a session-scoped event. */
  waitFor(method, sessionId, timeoutMs) {
    return new Promise((resolve, reject) => {
      let timer;
      const off = this.on(
        method,
        (params) => {
          if (timer) clearTimeout(timer);
          off();
          resolve(params);
        },
        sessionId,
      );
      if (timeoutMs) {
        timer = setTimeout(() => {
          off();
          reject(new Error(`timed out waiting for ${method}`));
        }, timeoutMs);
      }
    });
  }

  close() {
    if (this._closed) return;
    this._closed = true;
    try {
      this._ws.close();
    } catch {
      // already closing
    }
  }
}
