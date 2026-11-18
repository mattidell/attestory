"""P0 steps 2 and 3: cProfile one workload in one process, or time act-log prefixes.

Run (one process per call):
  python3 track1_profile.py profile median|slowest|k13 <scratch-outside-repo>
  python3 track1_profile.py prefix  slowest|median    <scratch-outside-repo>
The raw .prof stays in the scratch directory; a small JSON summary
(track1-profile-<workload>.json or track1-prefix-<workload>.json) is written here.
Each process warms up on a different list first (imports, schema and package
loads), then times the workload once without the profiler and once with it.
"""
from __future__ import annotations

import argparse
import cProfile
import importlib.util
import json
from pathlib import Path
import pstats
import sys
import time
from typing import Any
import unittest

HERE = Path(__file__).resolve().parent


def load(name: str, path: Path) -> Any:
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        sys.modules[name] = module
        spec.loader.exec_module(module)  # type: ignore[union-attr]
    return sys.modules[name]


wl = load("rke_t1_profile_workload", HERE / "p0_workload.py")
rr = wl.rr
REPO = wl.REPO

# ---- layers -----------------------------------------------------------------

KERNEL = {
    "act_log.py": "kernel: act log",
    "findings.py": "kernel: finding model",
    "facts.py": "kernel: fact store",
    "horizons.py": "kernel: fact store",
    "contribution.py": "kernel: fact store",
    "read_models.py": "kernel: fact store",
    "currency.py": "kernel: fact store",
    "schema_registry.py": "kernel: schema registry wrapper",
}
DERIVATION_EVAL = {"evaluator.py", "runner.py", "reference_runner.py", "marshal.py", "subject_dispatch.py",
                   "pairing_dispatch.py", "derived_enumeration.py", "records.py", "authorization.py",
                   "authorization_closure.py", "source_authority.py", "declarative_validation.py", "projection.py"}
PRESENTATION = {"presentation_projection.py", "explanation.py", "explanation_graph.py", "live_viewing.py",
                "live_session.py", "entry_loop.py"}
STDLIB_IO = ("/io.py", "/os.py", "/pathlib/", "/shutil.py", "/tempfile.py", "/genericpath.py", "/posixpath.py",
             "/fnmatch.py", "/glob.py")


def layer(key: tuple[str, int, str]) -> str:
    filename, _line, name = key
    rel = filename.replace("\\", "/")
    if "/site-packages/jsonschema" in rel or "/site-packages/referencing" in rel \
            or "/site-packages/rpds" in rel or "/site-packages/jsonschema_specifications" in rel:
        return "jsonschema validation"
    if "/packages/kernel/" in rel:
        return KERNEL.get(rel.rsplit("/", 1)[-1], "kernel: other")
    if "/packages/derivation/" in rel:
        base = rel.rsplit("/", 1)[-1]
        if base in DERIVATION_EVAL:
            return "derivation: evaluator/runner"
        if base in PRESENTATION:
            return "presentation projection"
        if base == "package_validation.py":
            return "derivation: package validation"
        return "derivation: live coordination/resolution"
    if "/packages/presentation/" in rel:
        return "presentation projection"
    if "/packages/tax/" in rel:
        return "tax domain loader"
    if "/tests/" in rel or "/docs/" in rel or "/tools/" in rel:
        return "test/evidence harness"
    if rel.endswith("/json/__init__.py") or "/json/" in rel or "_json" in name or "json" in name.lower():
        return "JSON (de)serialization"
    if rel.endswith("/copy.py") or name.startswith("<method '__deepcopy__"):
        return "copy.deepcopy"
    if any(s in rel for s in STDLIB_IO) or name in (
            "<built-in method io.open>", "<built-in method posix.fsync>", "<built-in method posix.stat>",
            "<built-in method posix.open>", "<built-in method posix.replace>", "<built-in method posix.rename>",
            "<built-in method posix.mkdir>", "<built-in method posix.unlink>", "<built-in method posix.rmdir>",
            "<built-in method posix.listdir>", "<built-in method posix.scandir>", "<built-in method posix.lstat>",
            "<built-in method posix.fstat>", "<built-in method posix.close>", "<built-in method posix.write>",
            "<built-in method posix.read>") or name.startswith("<method 'read' of '_io") \
            or name.startswith("<method 'write' of '_io") or name.startswith("<method 'close' of '_io") \
            or name.startswith("<method '__exit__' of '_io") or "_io." in name:
        return "file I/O"
    if "hashlib" in rel or "_hashlib" in name or "sha256" in name:
        return "hashing"
    if "/re/" in rel or "_sre" in name or "re.Pattern" in name:
        return "regex"
    if rel.startswith("~"):
        return "builtins (dict/list/set/str etc.)"
    return "other stdlib"


def short(key: tuple[str, int, str]) -> str:
    filename, line, name = key
    rel = filename.replace("\\", "/")
    for anchor in ("/packages/", "/tests/", "/docs/", "/tools/", "/site-packages/"):
        if anchor in rel:
            rel = anchor.strip("/").split("/")[0] + "/" + rel.split(anchor, 1)[1] \
                if anchor != "/site-packages/" else rel.split(anchor, 1)[1]
            break
    else:
        if "/lib/python" in rel:
            rel = "stdlib/" + rel.split("/lib/python", 1)[1].split("/", 1)[-1]
    return f"{rel}:{line}({name})" if rel != "~" else name


def summarize(stats: pstats.Stats) -> dict[str, Any]:
    raw = stats.stats  # type: ignore[attr-defined]
    total = stats.total_tt  # type: ignore[attr-defined]
    own: dict[str, float] = {}
    inclusive: dict[str, float] = {}
    builtin = "builtins (dict/list/set/str etc.)"
    for func, (cc, nc, tt, ct, callers) in raw.items():
        lay = layer(func)
        if (lay == builtin or func[0].startswith("<string>")) and callers:
            # A C builtin's own time is charged to the layers that call it,
            # in proportion to each calling edge's own time.
            edge_total = sum(e[2] for e in callers.values()) or 1.0
            for caller, edge in callers.items():
                charged = layer(caller)
                charged = charged if charged != builtin else "builtins (called from builtins)"
                own[charged] = own.get(charged, 0.0) + tt * edge[2] / edge_total
        else:
            own[lay] = own.get(lay, 0.0) + tt
        # Inclusive time of a layer: time entered from a caller outside it.
        for caller, edge in callers.items():
            if layer(caller) != lay:
                inclusive[lay] = inclusive.get(lay, 0.0) + edge[3]
    def row(func: Any, v: Any) -> dict[str, Any]:
        cc, nc, tt, ct, _ = v
        return {"function": short(func), "layer": layer(func), "calls": nc, "primitive_calls": cc,
                "own_s": round(tt, 3), "cum_s": round(ct, 3)}
    by_cum = sorted(raw.items(), key=lambda kv: kv[1][3], reverse=True)
    by_own = sorted(raw.items(), key=lambda kv: kv[1][2], reverse=True)
    return {
        "profiled_total_s": round(total, 3),
        "layers_own_s": {k: round(v, 3) for k, v in sorted(own.items(), key=lambda kv: -kv[1])},
        "layers_own_pct": {k: round(100 * v / total, 1) for k, v in sorted(own.items(), key=lambda kv: -kv[1])},
        "layers_inclusive_s": {k: round(v, 3) for k, v in sorted(inclusive.items(), key=lambda kv: -kv[1])},
        "top_cumulative": [row(f, v) for f, v in by_cum[:40]],
        "top_own": [row(f, v) for f, v in by_own[:25]],
    }


# ---- workloads ----------------------------------------------------------------

def timing() -> dict[str, Any]:
    return json.loads((HERE / "p0-timing.json").read_text())


def recorded(name: str) -> tuple[str, list[dict[str, Any]]]:
    key = timing()["chosen"][name]
    found = dict(rr.recorded_lists())
    return key, found[key]


def run_recorded(key: str, acts: list[dict[str, Any]], core: Any, prof: cProfile.Profile | None) -> dict[str, Any]:
    # A fresh process holds an empty validation memo; the warm-up list must not
    # leave a verdict behind that the measured list then hits.
    from packages.derivation.production_resolver import clear_validation_memo
    clear_validation_memo()
    if prof:
        prof.enable()
    t0 = time.perf_counter()
    finished = wl.prepare(key, acts, core)
    t1 = time.perf_counter()
    out = wl.run(key, finished, core)
    t2 = time.perf_counter()
    if prof:
        prof.disable()
    out.update(wl.sizes(finished))
    out.update({"prep_s": round(t1 - t0, 3), "run_s": round(out["run_s"], 3),
                "render_s": round(out["render_s"], 3), "total_s": round(t2 - t0, 3)})
    return out


def k13_module() -> Any:
    return load("rke_p0_k13", REPO / "tests/test_sli_track1_combined_standing.py")


def run_k13(case_name: str, prof: cProfile.Profile | None) -> dict[str, Any]:
    """The test's own _run_v42 (record, adopt, live run, both runners, checks)."""
    mod = k13_module()
    from packages.derivation.production_resolver import clear_validation_memo
    clear_validation_memo()
    seen: dict[str, Any] = {}
    original = mod.run_v42

    def timed_run(acts: Any, run_id: str) -> Any:
        seen["acts"] = list(acts)
        t = time.perf_counter()
        result = original(acts, run_id)
        seen["run_v42_s"] = time.perf_counter() - t
        return result
    mod.run_v42 = timed_run
    try:
        if prof:
            prof.enable()
        t0 = time.perf_counter()
        mod._run_v42(unittest.TestCase(), case_name)
        total = time.perf_counter() - t0
        if prof:
            prof.disable()
    finally:
        mod.run_v42 = original
    out = wl.sizes(seen["acts"])
    out.update({"test": f"tests/test_sli_track1_combined_standing.py::CoverDetail::test_case_{case_name}",
                "total_s": round(total, 3), "run_v42_s": round(seen["run_v42_s"], 3),
                "record_and_check_s": round(total - seen["run_v42_s"], 3)})
    return out


def profile(name: str, scratch: Path) -> None:
    core = rr.resolve_core(wl.CORE)
    from tests import evidence_loader
    body: dict[str, Any] = {"workload": name, "core": wl.CORE, "profiler": "cProfile (py-spy not installed)"}
    if name == "k13":
        t = time.perf_counter(); run_k13("K1", None); body["warmup_s"] = round(time.perf_counter() - t, 3)
        body["unprofiled"] = run_k13("K13", None)
        prof = cProfile.Profile()
        body["profiled"] = run_k13("K13", prof)
    else:
        key, acts = recorded(name)
        owner = evidence_loader.current_owner()
        if owner:
            evidence_loader.release(owner)
        body["list"] = key
        h = rr._get_harness()
        with h.loader_entries(core):
            t = time.perf_counter()
            run_recorded("demo.rke.warmup", h.ccr.base_return(), core, None)
            body["warmup_s"] = round(time.perf_counter() - t, 3)
            body["unprofiled"] = run_recorded(key, acts, core, None)
            prof = cProfile.Profile()
            body["profiled"] = run_recorded(key, acts, core, prof)
    prof.dump_stats(str(scratch / f"track1-{name}.prof"))
    stats = pstats.Stats(prof)
    body.update(summarize(stats))
    wl.write(HERE / f"track1-profile-{name}.json", body)
    print(json.dumps({k: body[k] for k in ("unprofiled", "profiled_total_s", "layers_own_pct")}, indent=1))


def prefix(name: str, scratch: Path, steps: tuple[int, ...]) -> None:
    core = rr.resolve_core(wl.CORE)
    key, acts = recorded(name)
    from tests import evidence_loader
    owner = evidence_loader.current_owner()
    if owner:
        evidence_loader.release(owner)
    h = rr._get_harness()
    rows = []
    with h.loader_entries(core):
        run_recorded("demo.rke.warmup", h.ccr.base_return(), core, None)
        for pct in steps:
            n = round(len(acts) * pct / 100)
            cut = [dict(a) for a in acts[:n]]
            try:
                out = run_recorded(f"{key}#{pct}", cut, core, None)
            except Exception as exc:
                out = {"outcome": "error", "error": type(exc).__name__}
            rows.append({"pct": pct, "recorded_acts": n, **{k: out.get(k) for k in (
                "outcome", "error", "acts", "assertions", "prep_s", "run_s", "render_s", "total_s", "rows",
                "publications")}})
            print(rows[-1], flush=True)
    wl.write(HERE / f"track1-prefix-{name}.json", {"workload": name, "list": key, "core": wl.CORE,
             "note": "prefix of the recorded act list, then the census finish (package adoption) and SSA handover",
             "rows": rows})


# ---- unprofiled cost centres --------------------------------------------------

CENTRES = (
    ("packages.derivation.production_resolver", "resolve_production_package"),
    ("packages.derivation.production_resolver", "_json_candidates"),
    ("packages.derivation.package_validation", "validate_package"),
    ("packages.derivation.marshal", "marshal_run_context"),
    ("packages.derivation.production_executor", "execute_and_record_marshaled"),
    ("packages.derivation.presentation_projection", "build_presentation_model"),
    ("packages.derivation.presentation_projection", "_closure_question_reasons"),
    ("packages.kernel.findings", "project"),
    ("packages.kernel.facts", "_lattice_metadata"),
    ("packages.kernel.facts", "facts_of"),
    ("packages.kernel.act_log", "ActLog._contents_of"),
    ("packages.kernel.schema_registry", "SchemaRegistry.validate"),
)


def instrument() -> dict[str, list[float]]:
    """Wrap each cost centre with an outermost-call wall-clock accumulator.

    Runtime wrapping in this evidence process only: the attribute is replaced
    on its module (or class) and on every loaded module that imported the same
    function object by name. No file under packages/ changes.
    """
    import functools
    import importlib
    acc: dict[str, list[float]] = {}
    for module_name, dotted in CENTRES:
        module = importlib.import_module(module_name)
        owner: Any = module
        parts = dotted.split(".")
        for part in parts[:-1]:
            owner = getattr(owner, part)
        original = getattr(owner, parts[-1])
        label = f"{module_name.rsplit('.', 1)[-1]}.{dotted}"
        slot = acc.setdefault(label, [0.0, 0])
        depth = [0]

        def make(original: Any, slot: list[float], depth: list[int]) -> Any:
            @functools.wraps(original)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                if depth[0]:
                    return original(*args, **kwargs)
                depth[0] += 1
                t = time.perf_counter()
                try:
                    return original(*args, **kwargs)
                finally:
                    slot[0] += time.perf_counter() - t
                    slot[1] += 1
                    depth[0] -= 1
            return wrapper
        wrapped = make(original, slot, depth)
        setattr(owner, parts[-1], wrapped)
        if len(parts) == 1:
            for other in list(sys.modules.values()):
                if other is not None and getattr(other, parts[-1], None) is original:
                    setattr(other, parts[-1], wrapped)
    return acc


def centres(name: str) -> None:
    core = rr.resolve_core(wl.CORE)
    from tests import evidence_loader
    body: dict[str, Any] = {"workload": name, "core": wl.CORE,
                            "method": "outermost-call perf_counter accumulators, no profiler, after one warmup"}
    if name == "k13":
        k13_module()
        run_k13("K1", None)
        acc = instrument()
        for slot in acc.values():
            slot[:] = [0.0, 0]
        body["run"] = run_k13("K13", None)
    else:
        key, acts = recorded(name)
        owner = evidence_loader.current_owner()
        if owner:
            evidence_loader.release(owner)
        body["list"] = key
        h = rr._get_harness()
        with h.loader_entries(core):
            run_recorded("demo.rke.warmup", h.ccr.base_return(), core, None)
            acc = instrument()
            body["run"] = run_recorded(key, acts, core, None)
    body["centres_s"] = {k: {"s": round(v[0], 3), "outer_calls": v[1]} for k, v in acc.items()}
    wl.write(HERE / f"track1-centres-{name}.json", body)
    print(json.dumps(body, indent=1))


# ---- sampling ------------------------------------------------------------------

class Sampler:
    """A stack sampler thread (py-spy is not installed; nothing is installed).

    Every ``interval`` seconds it reads the target thread's frame stack via
    sys._current_frames. Unlike cProfile it adds no per-call overhead, so
    layer shares are not inflated for code that makes many small calls. C
    builtins are charged to the Python frame that called them.
    """

    def __init__(self, interval: float = 0.002) -> None:
        import threading
        self.interval = interval
        self.target = threading.get_ident()
        self.samples: list[tuple[tuple[str, int, str], ...]] = []
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)

    def _loop(self) -> None:
        while not self._stop.wait(self.interval):
            frame = sys._current_frames().get(self.target)
            stack = []
            while frame is not None:
                code = frame.f_code
                stack.append((code.co_filename, frame.f_lineno, code.co_name))
                frame = frame.f_back
            self.samples.append(tuple(stack))

    def __enter__(self) -> "Sampler":
        self._old = sys.getswitchinterval()
        sys.setswitchinterval(0.0005)
        self._thread.start()
        return self

    def __exit__(self, *exc: Any) -> None:
        self._stop.set()
        self._thread.join()
        sys.setswitchinterval(self._old)


def sample_summary(samples: list[tuple[tuple[str, int, str], ...]]) -> dict[str, Any]:
    n = len(samples) or 1
    own: dict[str, int] = {}
    inclusive: dict[str, int] = {}
    func_own: dict[tuple[str, int, str], int] = {}
    func_incl: dict[tuple[str, int, str], int] = {}
    lines: dict[tuple[str, int, str], int] = {}
    def fkey(frame: tuple[str, int, str]) -> tuple[str, int, str]:
        return (frame[0], 0, frame[2])
    for stack in samples:
        if not stack:
            continue
        leaf = stack[0]
        # Generated code (<string>: namedtuple __new__, dataclass __init__)
        # is charged to the frame that called it.
        charge = next((f for f in stack if not f[0].startswith("<string>")), leaf)
        lay = layer(fkey(charge))
        own[lay] = own.get(lay, 0) + 1
        func_own[fkey(leaf)] = func_own.get(fkey(leaf), 0) + 1
        lines[leaf] = lines.get(leaf, 0) + 1
        for name in {layer(fkey(f)) for f in stack}:
            inclusive[name] = inclusive.get(name, 0) + 1
        for f in {fkey(f) for f in stack}:
            func_incl[f] = func_incl.get(f, 0) + 1
    pct = lambda d: {short(k) if isinstance(k, tuple) else k: round(100 * v / n, 1)  # noqa: E731
                     for k, v in sorted(d.items(), key=lambda kv: -kv[1])}
    return {
        "samples": len(samples),
        "layers_own_pct": pct(own),
        "layers_inclusive_pct": pct(inclusive),
        "top_functions_own_pct": dict(list(pct(func_own).items())[:20]),
        "top_functions_inclusive_pct": dict(list(pct(func_incl).items())[:30]),
        "top_lines_own_pct": dict(list(pct(lines).items())[:20]),
    }


def sample(name: str) -> None:
    core = rr.resolve_core(wl.CORE)
    from tests import evidence_loader
    body: dict[str, Any] = {"workload": name, "core": wl.CORE, "method": "stack sampler thread, 2 ms"}
    if name == "k13":
        k13_module()
        run_k13("K1", None)
        with Sampler() as sampler:
            body["run"] = run_k13("K13", None)
    else:
        key, acts = recorded(name)
        owner = evidence_loader.current_owner()
        if owner:
            evidence_loader.release(owner)
        body["list"] = key
        h = rr._get_harness()
        with h.loader_entries(core):
            run_recorded("demo.rke.warmup", h.ccr.base_return(), core, None)
            with Sampler() as sampler:
                body["run"] = run_recorded(key, acts, core, None)
    body.update(sample_summary(sampler.samples))
    wl.write(HERE / f"track1-sample-{name}.json", body)
    print(json.dumps({k: body[k] for k in ("run", "samples", "layers_own_pct", "layers_inclusive_pct")}, indent=1))


# ---- kernel projection growth ---------------------------------------------------

def kernel_growth(name: str, steps: tuple[int, ...]) -> None:
    """Time packages.kernel.findings.project on prefixes of one finished log.

    The registry is built as live_coordinate_run builds it (live.py, before its
    project call). Each prefix is projected three times; the minimum is kept.
    """
    from packages.derivation.loader import DerivationSchemas
    from packages.kernel.findings import companion_registry_for_package, project
    from packages.tax.loader import (
        install_domain_companion_equalities,
        install_domain_companion_presence,
        install_domain_declaration_signal_contradictions,
    )
    core = rr.resolve_core(wl.CORE)
    key, acts = recorded(name)
    from tests import evidence_loader
    owner = evidence_loader.current_owner()
    if owner:
        evidence_loader.release(owner)
    finished = wl.prepare(key, acts, core)
    schemas = DerivationSchemas()
    install_domain_companion_presence(schemas.registry)
    install_domain_companion_equalities(schemas.registry)
    install_domain_declaration_signal_contradictions(schemas.registry)
    registry = companion_registry_for_package(
        schemas.registry, ("tax.us.2025.package.core-calculations", core.version))
    run_acts = tuple(dict(a) for a in finished)
    project(run_acts, registry)  # warm
    rows = []
    for pct in steps:
        n = round(len(run_acts) * pct / 100)
        best = None
        for _ in range(3):
            t = time.perf_counter()
            state = project(run_acts[:n], registry)
            took = time.perf_counter() - t
            best = took if best is None else min(best, took)
        rows.append({"pct": pct, "acts": n, "assertions": sum(a["kind"] == "assertion" for a in run_acts[:n]),
                     "findings": len(state.findings), "fact_types": len(state.fact_state.fact_types),
                     "project_s": round(best, 4), "per_act_ms": round(1000 * best / max(n, 1), 3)})
        print(rows[-1], flush=True)
    wl.write(HERE / f"track1-kernel-growth-{name}.json", {
        "workload": name, "list": key, "core": wl.CORE, "function": "packages/kernel/findings.py:project",
        "note": "minimum of three runs per prefix of the finished log (census finish and SSA handover appended)",
        "rows": rows})


def resummarize(name: str, scratch: Path) -> None:
    """Recompute the profile summary from the saved .prof (classification changes only)."""
    body = json.loads((HERE / f"track1-profile-{name}.json").read_text())
    body.update(summarize(pstats.Stats(str(scratch / f"track1-{name}.prof"))))
    wl.write(HERE / f"track1-profile-{name}.json", body)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("profile", "prefix", "centres", "sample", "kernel-growth", "resummarize"))
    parser.add_argument("workload", choices=("median", "slowest", "k13"))
    parser.add_argument("scratch", type=Path)
    parser.add_argument("--steps", default="25,50,75,100")
    args = parser.parse_args()
    scratch = args.scratch.resolve()
    assert REPO not in scratch.parents
    scratch.mkdir(parents=True, exist_ok=True)
    if args.mode == "profile":
        profile(args.workload, scratch)
    elif args.mode == "resummarize":
        resummarize(args.workload, scratch)
    elif args.mode == "kernel-growth":
        kernel_growth(args.workload, tuple(int(x) for x in args.steps.split(",")))
    elif args.mode == "sample":
        sample(args.workload)
    elif args.mode == "centres":
        centres(args.workload)
    else:
        prefix(args.workload, scratch, tuple(int(s) for s in args.steps.split(",")))


if __name__ == "__main__":
    main()
