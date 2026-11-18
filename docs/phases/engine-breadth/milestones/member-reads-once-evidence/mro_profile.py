"""Re-profile one workload as rust-kernel-experiment did (cProfile layers, sampler layers, cost centres).

Run: python3 mro_profile.py profile|sample|centres median|slowest|k13 <label> <scratch-outside-repo> [--cold]
Loads track1_profile.py by path and redirects its JSON output to
<func>-<label>-<workload>.json beside this file. Without ``--cold`` the
process-lifetime member cache stays warm from the warm-up list (the replay
setting for every list after a worker's first); ``--cold`` empties it before
the measured run (the saving inside one list). Before the cache exists the two
are identical.
"""
from __future__ import annotations

import importlib.util
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


prof = load("mro_profile_sibling", SIB / "track1_profile.py")


def main() -> None:
    func, name, label, scratch = sys.argv[1], sys.argv[2], sys.argv[3], Path(sys.argv[4])
    cold = "--cold" in sys.argv
    scratch.mkdir(parents=True, exist_ok=True)
    assert prof.wl.REPO not in scratch.resolve().parents
    from packages.derivation import production_resolver as pr
    clear_members = getattr(pr, "clear_member_cache", lambda: None)
    orig_write = prof.wl.write

    def write(path, body):  # type: ignore[no-untyped-def]
        body = dict(body, label=label, member_cache="cold per run" if cold else "warm from warm-up")
        orig_write(HERE / f"{func}-{label}-{name}.json", body)

    prof.wl.write = write
    if "_member_candidates" in dir(pr):
        prof.CENTRES = tuple(c for c in prof.CENTRES if c[1] != "_json_candidates") + (
            ("packages.derivation.production_resolver", "_member_candidates"),)
    if cold:
        for fn in ("run_recorded", "run_k13"):
            original = getattr(prof, fn)

            def wrapped(*a, __o=original, **k):  # type: ignore[no-untyped-def]
                clear_members()
                return __o(*a, **k)
            setattr(prof, fn, wrapped)
    {"profile": lambda: prof.profile(name, scratch), "sample": lambda: prof.sample(name),
     "centres": lambda: prof.centres(name)}[func]()


if __name__ == "__main__":
    main()
