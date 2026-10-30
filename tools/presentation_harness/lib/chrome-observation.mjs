// Bounded diagnostic data only: no browser output, URLs, paths or environment.
import { appendFile, readdir, readFile } from "node:fs/promises";

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

export function createObservation({ label, output, graceMs = 60000 }) {
  const safeLabel = ["correction-calculate-dropped", "correction-other", "isolated", "parallel"].includes(label) ? label : "other";
  let start = performance.now();
  let wallStart = Date.now();
  const record = { label: safeLabel, outcome: null, readiness_ms: null, advertised_ms: null,
    elapsed_ms: null, queue_ms: 0, stderr_bytes: null, exit_kind: null, exit_code: null, exit_signal: null, spawn_code: null, stderr_categories: [], deadline_monotonic_ms: null, deadline_wall_ms: null, file_metadata: null, file_states: [], samples: [], diagnostic_error: false };
  let lastFile = null;
  let nextSample = 0;
  const elapsed = () => Math.round(performance.now() - start);
  return {
    graceMs: Math.max(0, Math.min(60000, graceMs)),
    beginActive(queueMs) { record.queue_ms = Math.round(queueMs); start = performance.now(); wallStart = Date.now(); },
    deadline() { record.deadline_monotonic_ms = elapsed(); record.deadline_wall_ms = Date.now() - wallStart; },
    recognize(name) { if (!record.stderr_categories.includes(name)) record.stderr_categories.push(name); },
    advertised() { if (record.advertised_ms === null) record.advertised_ms = elapsed(); },
    async observe(fileState, pid, alive, metadata) {
      const ms = elapsed();
      if (metadata) record.file_metadata = { size: metadata.size, mtime_from_start_ms: Math.round(metadata.mtime_wall_ms - wallStart), observed_ms: ms };
      if (fileState !== lastFile && record.file_states.length < 32) {
        record.file_states.push({ ms, state: fileState }); lastFile = fileState;
      }
      if (ms >= nextSample && record.samples.length < 40) {
        nextSample = ms + 2000;
        record.samples.push({ ms, alive, ...(await sampleProcess(pid)) });
      }
    },
    async finish(outcome, ready, details = {}) {
      Object.assign(record, details);
      record.outcome = outcome; record.elapsed_ms = outcome === "queue_failed" ? null : elapsed();
      if (ready) record.readiness_ms = elapsed();
      try { await appendFile(output, JSON.stringify(record) + "\n"); } catch { record.diagnostic_error = true; process.stderr.write("chrome-observation-write-failed\n"); }
    },
  };
}
