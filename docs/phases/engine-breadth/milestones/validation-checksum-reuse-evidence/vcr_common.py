"""Shared workload for validation-checksum-reuse Track 1 (published core v100).

Loads rust-kernel-experiment's p0_workload.py by path (finish, Social Security
handover with reconfirm, live_coordinate_run, page render) and its per-list
identity hashing (track1_dump.py). Nothing is written inside the repository
except the small JSON summaries the scripts name.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

HERE = Path(__file__).resolve().parent
SIB = HERE.parent / "rust-kernel-experiment-evidence"
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

CORE = "v100"
# The median and slowest lists rust-kernel-experiment P0 chose (p0-timing.json),
# kept so the profiles compare with every earlier speed milestone.
MEDIAN = "v81/case/m_8949_no_ic3_yes_q3_no"
SLOWEST = "v83/returns/v80/carried_covered_flag_no_w_lt/recorded"


def load(name: str, path: Path) -> Any:
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        sys.modules[name] = module
        spec.loader.exec_module(module)  # type: ignore[union-attr]
    return sys.modules[name]


wl = load("vcr_workload", SIB / "p0_workload.py")
dump = load("vcr_dump_sibling", SIB / "track1_dump.py")
rr = wl.rr


def core() -> Any:
    return rr.resolve_core(CORE)


def release_evidence_owner() -> None:
    from tests import evidence_loader
    owner = evidence_loader.current_owner()
    if owner:
        evidence_loader.release(owner)


def workload(name: str) -> tuple[str, list[dict[str, Any]]]:
    key = {"median": MEDIAN, "slowest": SLOWEST}[name]
    return key, dict(rr.recorded_lists())[key]


def write(path: Path, body: Any) -> None:
    text = json.dumps(body, indent=1, sort_keys=True) + "\n"
    rr._check_no_local_paths(text, path.name)
    path.write_text(text, encoding="utf-8")
