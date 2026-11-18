"""Member-file read counts per recorded list, before any change.

Run: python3 mro_counts.py median|slowest|k13 <label>
Loads the sibling rust-kernel-experiment evidence scripts by path under unique
names, warms one list, then runs the workload with counters on: every
Path.read_bytes/read_text under the content directory, every call of
``_json_candidates`` (by caller), ``_load_json`` and ``citizen_checksum``.
Writes counts-<label>-<workload>.json beside this file.
"""
from __future__ import annotations

import collections
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SIB = HERE.parent / "rust-kernel-experiment-evidence"


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        sys.modules[name] = module
        spec.loader.exec_module(module)  # type: ignore[union-attr]
    return sys.modules[name]


prof = load("mro_counts_profile", SIB / "track1_profile.py")
wl = prof.wl
rr = prof.rr
REPO = wl.REPO


def main() -> None:
    name, label = sys.argv[1], sys.argv[2]
    import pathlib
    from packages.derivation import production_resolver as pr
    from packages.derivation import package_validation as pv
    from packages.derivation import surface_resolver as sr

    content = str(rr.CONTENT)
    reads: collections.Counter[str] = collections.Counter()
    read_callers: collections.Counter[str] = collections.Counter()
    cand_callers: collections.Counter[str] = collections.Counter()
    load_json_calls = [0]
    checksum_calls: collections.Counter[str] = collections.Counter()
    on = [False]

    def caller_chain(depth: int = 6) -> str:
        frame = sys._getframe(2)
        out = []
        while frame is not None and len(out) < depth:
            fn = frame.f_code.co_filename
            if "/packages/" in fn:
                out.append(f"{fn.split('/packages/', 1)[1]}:{frame.f_code.co_name}")
            frame = frame.f_back
        return " < ".join(out[:3])

    orig_bytes, orig_text = pathlib.Path.read_bytes, pathlib.Path.read_text

    def read_bytes(self, *a, **k):  # type: ignore[no-untyped-def]
        if on[0] and str(self).startswith(content):
            reads[str(self)] += 1
            read_callers[caller_chain()] += 1
        return orig_bytes(self, *a, **k)

    def read_text(self, *a, **k):  # type: ignore[no-untyped-def]
        if on[0] and str(self).startswith(content):
            reads[str(self)] += 1
            read_callers[caller_chain()] += 1
        return orig_text(self, *a, **k)

    orig_cand, orig_lj, orig_cc = pr._json_candidates, pr._load_json, pr.citizen_checksum

    def cand(directory):  # type: ignore[no-untyped-def]
        if on[0]:
            cand_callers[caller_chain(1)] += 1
        return orig_cand(directory)

    def lj(path):  # type: ignore[no-untyped-def]
        if on[0]:
            load_json_calls[0] += 1
        return orig_lj(path)

    def cc(body):  # type: ignore[no-untyped-def]
        if on[0]:
            checksum_calls[caller_chain(1)] += 1
        return orig_cc(body)

    pathlib.Path.read_bytes, pathlib.Path.read_text = read_bytes, read_text  # type: ignore[method-assign]
    pr._json_candidates = sr._json_candidates = cand  # type: ignore[assignment]
    pr._load_json = lj  # type: ignore[assignment]
    pr.citizen_checksum = cc  # type: ignore[assignment]
    pv.citizen_checksum = cc  # type: ignore[assignment]

    core = rr.resolve_core(wl.CORE)
    from tests import evidence_loader
    body: dict = {"workload": name, "label": label}
    if name == "k13":
        prof.k13_module()
        prof.run_k13("K1", None)
        on[0] = True
        body["run"] = prof.run_k13("K13", None)
        on[0] = False
    else:
        key, acts = prof.recorded(name)
        owner = evidence_loader.current_owner()
        if owner:
            evidence_loader.release(owner)
        body["list"] = key
        h = rr._get_harness()
        with h.loader_entries(core):
            prof.run_recorded("demo.rke.warmup", h.ccr.base_return(), core, None)
            on[0] = True
            body["run"] = prof.run_recorded(key, acts, core, None)
            on[0] = False
    per_file = collections.Counter(reads.values())
    body["member_dir_reads_total"] = sum(reads.values())
    body["distinct_files_read"] = len(reads)
    body["reads_per_file_histogram"] = {str(k): v for k, v in sorted(per_file.items())}
    body["read_callers"] = dict(read_callers.most_common())
    body["json_candidates_calls_by_caller"] = dict(cand_callers)
    body["load_json_calls"] = load_json_calls[0]
    body["citizen_checksum_calls_by_caller"] = dict(checksum_calls)
    wl.write(HERE / f"counts-{label}-{name}.json", body)
    print(json.dumps({k: v for k, v in body.items() if k != "run"}, indent=1))


if __name__ == "__main__":
    main()
