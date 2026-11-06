// Bounded diagnostic data only: no browser output, URLs, paths or environment.
import { appendFile, readdir, readFile, open, opendir } from "node:fs/promises";

// Only this test opts into multi-record progress. Legacy users keep one final
// record. Bounds apply per observation, not to other writers sharing its file.
export const PROGRESS_RECORD_LIMIT = 64;
export const PROCESS_TREE_LIMIT = 64;
const stages = new Set(["test_started", "launch_started", "browser_ready", "client_connected",
  "contexts_created", "targets_loaded", "isolation_checked", "contexts_disposed",
  "child_wait_started", "child_ready", "child_reaped", "child_context_cleaned",
  "error_client_wait_started", "error_client_closed", "waiting_client_started",
  "waiting_client_context", "waiting_client_reaped", "waiting_client_cleaned",
  "browser_close_started", "browser_close_observed", "cleanup_started", "cleanup_finished"]);
async function shortFile(path) {
  const file = await open(path, "r");
  try { const buffer = Buffer.alloc(8192); const { bytesRead } = await file.read(buffer, 0, buffer.length, 0);
    return { text: buffer.subarray(0, bytesRead).toString("utf8"), truncated: bytesRead === buffer.length }; }
  finally { await file.close(); }
}
async function sampleTree(pid) {
  if (process.platform !== "linux" || !pid) return { available: false };
  const pending = [pid], seen = new Set();
  let user = 0, system = 0, rss = 0, rssKnown = true, sampled = 0, complete = true, reads = 0;
  while (pending.length && seen.size < PROCESS_TREE_LIMIT && reads < 256) {
    const current = pending.shift();
    if (seen.has(current)) continue;
    seen.add(current);
    try {
      const status = await shortFile(`/proc/${current}/stat`); reads++;
      const fields = status.text.slice(status.text.lastIndexOf(")") + 2).split(" ");
      const u = Number(fields[11]), s = Number(fields[12]);
      if (!Number.isFinite(u) || !Number.isFinite(s)) { complete = false; continue; }
      user += u; system += s; sampled++;
      const memory = await shortFile(`/proc/${current}/status`); reads++;
      const resident = memory.text.match(/^VmRSS:\s*(\d+)/m)?.[1];
      if (resident === undefined) rssKnown = false;
      else rss += Number(resident);
      const tasks = await opendir(`/proc/${current}/task`);
      let taskCount = 0;
      for await (const task of tasks) {
        if (++taskCount > 64) { complete = false; break; }
        if (reads >= 256) { complete = false; break; }
        const children = await shortFile(`/proc/${current}/task/${task.name}/children`); reads++;
        if (children.truncated) complete = false;
        for (const child of children.text.trim().split(/\s+/)) {
          if (/^\d+$/.test(child) && pending.length < PROCESS_TREE_LIMIT) pending.push(Number(child));
          else if (/^\d+$/.test(child)) complete = false;
        }
      }
    } catch { complete = false; rssKnown = false; }
  }
  return { available: sampled > 0, sampled_processes: sampled, complete: complete && pending.length === 0,
    cpu_user_ticks: sampled ? user : null, cpu_system_ticks: sampled ? system : null,
    // Summed RSS includes shared pages; it is not unique physical memory.
    summed_rss_kb: sampled && rssKnown ? rss : null, tick_seconds: null,
    counter_scope: "currently_visible_processes_not_exited_children" };
}

async function numberFile(path) {
  try { const s = (await readFile(path, "utf8")).trim(); return /^\d+$/.test(s) ? Number(s) : null; } catch { return null; }
}
async function sampleProcess(pid) {
  if (!pid) return { available: false };
  try {
    const status = await readFile(`/proc/${pid}/status`, "utf8");
    const field = name => { const match = status.match(new RegExp(`^${name}:\\s*(\\d+)`, "m")); return match ? Number(match[1]) : null; };
    const state = status.match(/^State:\s*([RSDZTIX])/m)?.[1] || null;
    let cpu_user_ticks = null, cpu_system_ticks = null;
    try {
      const procstat = await readFile(`/proc/${pid}/stat`, "utf8");
      const fields = procstat.slice(procstat.lastIndexOf(")") + 2).split(" ");
      cpu_user_ticks = Number(fields[11]); cpu_system_ticks = Number(fields[12]);
      if (!Number.isFinite(cpu_user_ticks)) cpu_user_ticks = null;
      if (!Number.isFinite(cpu_system_ticks)) cpu_system_ticks = null;
    } catch { /* unavailable */ }
    let fds = null;
    try { fds = (await readdir(`/proc/${pid}/fd`)).length; } catch { /* unavailable */ }
    return { available: true, state, threads: field("Threads"),
      rss_kb: field("VmRSS"), fds, cpu_user_ticks, cpu_system_ticks,
      voluntary_switches: field("voluntary_ctxt_switches"),
      involuntary_switches: field("nonvoluntary_ctxt_switches"),
      cgroup_memory_current: await numberFile("/sys/fs/cgroup/memory.current"),
      cgroup_pids_current: await numberFile("/sys/fs/cgroup/pids.current"),
      cgroup_memory_max: await numberFile("/sys/fs/cgroup/memory.max"),
      cgroup_pids_max: await numberFile("/sys/fs/cgroup/pids.max") };
  } catch { return { available: false }; }
}

export const OBSERVER_GRACE_MS = 60000;
export function createObservation({ label, output, graceMs = OBSERVER_GRACE_MS, progress = false }) {
  const safeLabel = ["correction-calculate-dropped", "correction-other", "isolated", "parallel", "resource-controls"].includes(label) ? label : "other";
  const live = progress && safeLabel === "resource-controls";
  let start = performance.now();
  const observationStarted = start;
  let wallStart = Date.now();
  const record = { label: safeLabel, outcome: null, readiness_ms: null, advertised_ms: null,
    elapsed_ms: null, queue_ms: 0, stderr_bytes: null, exit_kind: null, exit_code: null, exit_signal: null, spawn_code: null, stderr_categories: [], deadline_monotonic_ms: null, deadline_wall_ms: null, file_metadata: null, file_states: [], samples: [], diagnostic_error: false };
  let lastFile = null;
  let nextSample = 0;
  let lastPoll = null, lastSample = null, rootPid = null, sampling = false;
  let writes = 0, writing = null, closed = false, dirty = false;
  if (live) Object.assign(record, { stages: [], progress: true, sampling_interval_process_cpu_us: 0, poll_count: 0, max_poll_gap_ms: 0 });
  const elapsed = () => Math.round(performance.now() - start);
  const observationElapsed = () => Math.round(performance.now() - observationStarted);
  function persist() {
    if (!live || writes >= PROGRESS_RECORD_LIMIT || record.diagnostic_error) return;
    if (writing) { dirty = true; return; }
    dirty = false;
    writes++;
    const text = JSON.stringify({ ...record, snapshot_ms: observationElapsed(), progress_sequence: writes });
    if (Buffer.byteLength(text) > 65536) { record.diagnostic_error = true; return; }
    // One outstanding write, no unbounded promise queue and no awaited disk I/O
    // on the test path. Failed diagnostics never print paths or change results.
    writing = appendFile(output, text + "\n").catch(() => { record.diagnostic_error = true; }).finally(() => { writing = null; if (dirty) persist(); });
  }
  async function sample(pid, alive) {
    if (sampling || record.samples.length >= 40) return;
    sampling = true;
    const ms = elapsed(), lifetime = observationElapsed(), cpu = process.cpuUsage(), started = performance.now();
    try {
      const root = await sampleProcess(pid);
      const tree = live ? await sampleTree(pid) : undefined;
      if (live && closed) return;
      const gap = lastSample === null ? null : lifetime - lastSample; lastSample = lifetime;
      record.samples.push({ ms, alive, ...root, ...(live ? { tree, tick_seconds: null, sample_gap_ms: gap,
        sampling_elapsed_ms: Math.round(performance.now() - started) } : {}) });
      // Includes unrelated Node/event-loop work while diagnostic I/O awaits;
      // this is NOT isolated observer overhead.
      if (live) { const used = process.cpuUsage(cpu); record.sampling_interval_process_cpu_us += used.user + used.system; }
      persist();
    } catch { /* best effort only */ } finally { sampling = false; }
  }
  const timer = live ? setInterval(() => { if (!closed) { if (rootPid) void sample(rootPid, null); persist(); } }, 2000) : null;
  timer?.unref();
  return {
    graceMs: Math.max(0, Math.min(OBSERVER_GRACE_MS, graceMs)),
    beginActive(queueMs) { record.queue_ms = Math.round(queueMs); start = performance.now(); wallStart = Date.now(); },
    deadline() { record.deadline_monotonic_ms = elapsed(); record.deadline_wall_ms = Date.now() - wallStart; },
    recognize(name) { if (!record.stderr_categories.includes(name)) record.stderr_categories.push(name); },
    advertised() { if (record.advertised_ms === null) record.advertised_ms = elapsed(); },
    stage(name, pid = null) {
      if (!live || !stages.has(name) || closed) return;
      if (Number.isInteger(pid) && pid > 0) rootPid = pid;
      if (record.stages.length < 32) record.stages.push({ name, ms: observationElapsed() });
      persist();
    },
    close() { closed = true; if (timer) clearInterval(timer); persist(); },
    async flushed() { while (writing) await writing; },
    async observe(fileState, pid, alive, metadata) {
      const ms = elapsed();
      rootPid = pid;
      if (live) { record.poll_count++; if (lastPoll !== null) record.max_poll_gap_ms = Math.max(record.max_poll_gap_ms, ms - lastPoll); lastPoll = ms; }
      if (metadata) record.file_metadata = { size: metadata.size, mtime_from_start_ms: Math.round(metadata.mtime_wall_ms - wallStart), observed_ms: ms };
      if (fileState !== lastFile && record.file_states.length < 32) {
        record.file_states.push({ ms, state: fileState }); lastFile = fileState;
      }
      if (ms >= nextSample && record.samples.length < 40) {
        nextSample = ms + 2000;
        if (live) void sample(pid, alive);
        else await sample(pid, alive);
      }
    },
    async finish(outcome, ready, details = {}) {
      Object.assign(record, details);
      record.outcome = outcome; record.elapsed_ms = outcome === "queue_failed" ? null : elapsed();
      if (ready) record.readiness_ms = elapsed();
      if (live) persist();
      else try { await appendFile(output, JSON.stringify(record) + "\n"); } catch { record.diagnostic_error = true; process.stderr.write("chrome-observation-write-failed\n"); }
    },
  };
}
