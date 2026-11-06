// Bounded foreground experiment; no downloads, raw trace output or system scan.
// Run from repository root with an ignored output directory argument.
import { spawn } from "node:child_process";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve, sep } from "node:path";
import { pathToFileURL } from "node:url";

// A killed append may leave one partial tail. Never let it erase earlier
// complete snapshots, and never include offending bytes or error messages.
export function parseResourceTrace(text) {
  const records = [];
  let malformed = 0, incomplete = false;
  const lines = text.split("\n"), unterminated = text.length > 0 && !text.endsWith("\n");
  for (let i = 0; i < lines.length; i++) {
    if (!lines[i].trim()) continue;
    try {
      const value = JSON.parse(lines[i]);
      if (value === null || typeof value !== "object" || Array.isArray(value)) malformed++;
      else if (value.label === "resource-controls") records.push(value);
    } catch {
      // Without a delimiter an invalid last record may be a killed write;
      // distinguish it from a malformed complete (newline-delimited) record.
      if (unterminated && i === lines.length - 1) incomplete = true;
      else malformed++;
    }
  }
  return { records, trace_status: "read", trace_read_error: null,
    malformed_records: malformed, incomplete_trailing_record: incomplete,
    unterminated_trailing_record: unterminated };
}
export async function readResourceTrace(path) {
  try { return parseResourceTrace(await readFile(path, "utf8")); }
  catch (error) {
    return { records: [], trace_status: error.code === "ENOENT" ? "missing" : "unreadable",
      trace_read_error: ["ENOENT", "EACCES", "EPERM", "EISDIR", "EIO"].includes(error.code) ? error.code : "other",
      malformed_records: 0, incomplete_trailing_record: false, unterminated_trailing_record: false };
  }
}
const direct = process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url;
if (direct && process.argv[2] === "--burn") {
  const end = performance.now() + 40000;
  while (performance.now() < end) Math.sqrt(Math.random());
} else if (direct) {
  const output = process.argv[2];
  if (!output || !resolve(output).startsWith(resolve("temp/lattice-rebuild-p0") + sep)) throw new Error("use own ignored temp output");
  await mkdir(output, { recursive: true });
  const deadline = performance.now() + 300000;
  const results = [];
  const python = `import json,os,resource,subprocess,time
start=time.perf_counter(); before=resource.getrusage(resource.RUSAGE_CHILDREN)
try:
 r=subprocess.run([os.sys.executable,"-m","pytest","tests/test_chrome_test_resources.py::test_node_browser_resource_controls"],capture_output=True,text=True,timeout=55)
 code=r.returncode; text=r.stdout+r.stderr
except subprocess.TimeoutExpired:
 code=124; text="probe outer deadline"
after=resource.getrusage(resource.RUSAGE_CHILDREN)
print(json.dumps({"exitstatus":code,"elapsed_seconds":time.perf_counter()-start,"waited_children_user_seconds":after.ru_utime-before.ru_utime,"waited_children_system_seconds":after.ru_stime-before.ru_stime,"wrapper_timeout": "TimeoutExpired" in text,"passed": "1 passed" in text}))
`;
  function stop(child) {
    try { process.kill(-child.pid, "SIGKILL"); } catch { /* already reaped */ }
  }
  for (const [mode, count] of [["control", 1], ["isolated", 3], ["loaded", 3]]) {
    for (let iteration = 1; iteration <= count; iteration++) {
      if (performance.now() >= deadline) throw new Error("bounded experiment window exhausted");
      const burners = [], children = [];
      let timer;
      try {
        if (mode === "loaded") for (let i = 0; i < 4; i++) {
          const child = spawn(process.execPath, [new URL(import.meta.url).pathname, "--burn"], { detached: true, stdio: "ignore" });
          burners.push(child); children.push(new Promise(resolve => child.once("close", resolve)));
        }
        const trace = join(output, `demo-${mode}-${iteration}.jsonl`);
        const env = { ...process.env };
        if (mode === "control") delete env.DEMO_CHROME_TRACE;
        else env.DEMO_CHROME_TRACE = trace;
        const child = spawn(process.env.DEMO_PROBE_PYTHON || "python3", ["-c", python], { env, detached: true, stdio: ["ignore", "pipe", "pipe"] });
        let stdout = "", stderrBytes = 0;
        child.stdout.on("data", data => { stdout = (stdout + data).slice(-8192); });
        child.stderr.on("data", data => { stderrBytes += data.length; });
        const done = new Promise((resolve, reject) => { child.once("error", reject); child.once("close", resolve); });
        timer = setTimeout(() => stop(child), Math.min(60000, Math.max(1, deadline - performance.now())));
        let exit;
        try { exit = await done; } finally { stop(child); }
        const measurement = exit === 0 ? JSON.parse(stdout.trim()) : { driver_exitstatus: exit, stderr_bytes: stderrBytes };
        const parsed = mode === "control" ? { records: [], trace_status: "disabled", trace_read_error: null,
          malformed_records: 0, incomplete_trailing_record: false, unterminated_trailing_record: false } : await readResourceTrace(trace);
        const { records: observations, ...traceFlags } = parsed;
        const last = observations.at(-1);
        const row = { mode, iteration, burners: burners.length, ...measurement, ...traceFlags,
          progress_records: observations.length, readiness_ms: last?.readiness_ms ?? null,
          stages: last?.stages ?? [], samples: last?.samples ?? [],
          max_poll_gap_ms: last?.max_poll_gap_ms ?? null,
          sampling_interval_process_cpu_us: last?.sampling_interval_process_cpu_us ?? null };
        results.push(row);
        await writeFile(join(output, "demo-results.json"), JSON.stringify(results, null, 2) + "\n");
        console.log(JSON.stringify({ ...row, samples: undefined, stages: undefined }));
      } finally {
        clearTimeout(timer);
        for (const child of burners) stop(child);
        await Promise.all(children);
      }
    }
  }
}
