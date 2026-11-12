"""Replay recorded return act lists in parallel across worker processes.

Importable and runnable tool for recorded act list replay and neighbour diffs.
Part of the parallel-replay tooling milestone (Engine Breadth).
"""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
from dataclasses import dataclass
import hashlib
import importlib.util
import inspect
import json
import multiprocessing
import os
from pathlib import Path
import re
import sys
import tempfile
from collections import Counter
from typing import Any, Callable

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
RELEASE_STEM = "demo.release.sli-worksheet-integration.2025"
SENTENCE_FIELDS = ("questions", "reasons", "blocked_reasons")
PRESENT_NO_SALE_BOX4 = "tax.us.2025.f1099b.no-sale-box4-present"

Acts = list[dict[str, Any]]


@dataclass(frozen=True)
class ReplayCore:
    """One core: package, registry and release, and directory locations."""

    version: str
    registry: str
    release_version: str
    content: Path = CONTENT
    releases: Path = RELEASES
    loader_from: str | None = None
    presence_pairs: tuple[tuple[str, str], ...] = ()

    @property
    def package_path(self) -> Path:
        return self.content / f"package.core-calculations.{self.version}.json"

    @property
    def release_path(self) -> Path:
        return self.releases / f"{RELEASE_STEM}.{self.release_version}.json"

    def surface(self) -> Any:
        from packages.derivation.production_resolver import PublicationSurface

        return PublicationSurface(
            self.releases,
            self.content / f"published-packages.{self.registry}.json",
            self.content,
        )


def _module(name: str, path: Path) -> Any:
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


_CACHED_TEST: Any = None
_CACHED_HARNESS: Any = None


def _get_test() -> Any:
    global _CACHED_TEST
    if _CACHED_TEST is None:
        _CACHED_TEST = _module(
            "rr_v83_test",
            REPO / "tests/test_f1099b_backup_withholding_v83.py",
        )
    return _CACHED_TEST


def _get_harness() -> Any:
    global _CACHED_HARNESS
    if _CACHED_HARNESS is None:
        _CACHED_HARNESS = _module(
            "rr_audit_harness",
            REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py",
        )
    return _CACHED_HARNESS


def resolve_core(core_spec: Any, harness: Any | None = None) -> Any:
    """Resolve a core specification into a Core object.

    Accepts:
    - An existing Core or ReplayCore object.
    - A Path or string path to a core.json file.
    - A published version string such as 'v86' or 'v87'.
    """
    if hasattr(core_spec, "version") and hasattr(core_spec, "package_path"):
        return core_spec
    if isinstance(core_spec, (str, Path)):
        p = Path(core_spec)
        if p.is_file():
            body = json.loads(p.read_text(encoding="utf-8"))
            return ReplayCore(
                version=body["version"],
                registry=body["registry"],
                release_version=body["release_version"],
                content=Path(body.get("content", CONTENT)),
                releases=Path(body.get("releases", RELEASES)),
                loader_from=body.get("loader_from"),
                presence_pairs=tuple(tuple(pair) for pair in body.get("presence_pairs", ())),
            )
        s = str(core_spec).strip()
        m = re.match(r"^v(\d+)$", s)
        if m:
            n = int(m.group(1))
            reg_rel = f"v{n - 2}"
            return ReplayCore(
                version=s,
                registry=reg_rel,
                release_version=reg_rel,
            )
    raise ValueError(f"Cannot resolve core from specification: {core_spec!r}")


_RECORDED_LISTS_CACHE: list[tuple[str, Acts]] | None = None


def recorded_lists() -> list[tuple[str, Acts]]:
    """Return every recorded fixture's act lists, once each by digest.

    Returns the same (key, acts) list, in the same order, as question-wording's
    neighbour_tasks():
    - v83: the 298 lists the v86 test replays.
    - v84: the box 7 Track 0 grid.
    - v85: the no-sale box 4 Track 0 grid.
    - v82: the sale family audit Track 0 runs.
    - v81: the 213 code B returns as exported, uncorrected.
    """
    global _RECORDED_LISTS_CACHE
    if _RECORDED_LISTS_CACHE is not None:
        return list(_RECORDED_LISTS_CACHE)
    test = _get_test()
    harness = _get_harness()
    expected = json.loads((REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json").read_text(encoding="utf-8"))
    asks = set(json.loads((REPO / "docs/phases/engine-breadth/milestones/f1099b-box4-only-evidence/track0-neighbour.json").read_text(encoding="utf-8"))["asks_no_sale_present_ids"])

    track = test.track0()
    cases = dict(test.decided_cases(track))
    with tempfile.TemporaryDirectory() as tmp:
        exported = test.export_returns(Path(tmp))
    returns = test.return_acts(track, exported)
    core = harness.Core("v86", "v84", "v84")

    v83_raw: list[tuple[str, Acts]] = []
    for key in expected["track0"]:
        v83_raw.append((f"track0/{key}", cases[key]))
    for key in expected["returns"]:
        v83_raw.append((f"returns/{key}", returns[key]))
    for key in expected["zero_sample"]:
        v83_raw.append((f"zero/{key}", test.with_zero(track, returns[key], core)))

    out: list[tuple[str, Acts]] = []
    for key, acts in v83_raw:
        if key in asks:
            acts = harness.say(acts, PRESENT_NO_SALE_BOX4, "no", "qw.restore")
        out.append((f"v83/{key}", acts))

    b7 = _module("rr_box7_test", REPO / "tests/test_f1099b_box7_loss_v84.py").box7_cases()
    for group in ("authority", "matrix", "surface", "reuse"):
        for case_id, spec in sorted(b7[group].items()):
            out.append((f"v84/{group}/{case_id}", spec["acts"]))
    for trace in b7["late"]:
        for index, step in enumerate(trace.get("steps") or []):
            if isinstance(step, dict) and "acts" in step:
                out.append((f"v84/late/{trace['id']}/{index}", step["acts"]))

    b4 = _module("rr_box4_test", REPO / "tests/test_f1099b_box4_only_v85.py").box4_cases()
    for group in ("authority", "matrix", "surface", "reuse"):
        for case_id, spec in sorted(b4[group].items()):
            out.append((f"v85/{group}/{case_id}", spec["acts"]))
    for trace in b4["late"]:
        for index, step in enumerate(trace.get("steps") or []):
            if isinstance(step, dict) and "acts" in step:
                out.append((f"v85/late/{trace['id']}/{index}", step["acts"]))

    sfa = _module("rr_sfa_test", REPO / "tests/test_sale_family_audit_v82.py")
    t = sfa.track0()
    core82 = sfa.v82(t)
    for name, mode in sfa.track0_keys(t):
        out.append((f"v82/{name}/{mode}", sfa.track0_acts(t, name, mode, core82)))

    for group in ("case", "v80", "neighbour"):
        for name in sorted(exported.get(group, {})):
            out.append((f"v81/{group}/{name}", exported[group][name]))

    # Release evidence loader owner if set to avoid leaking engine state
    try:
        from tests import evidence_loader

        owner = evidence_loader.current_owner()
        if owner:
            evidence_loader.release(owner)
    except (ImportError, AttributeError):
        pass

    seen: dict[str, str] = {}
    unique: list[tuple[str, Acts]] = []
    for key, acts in out:
        digest = hashlib.sha256(json.dumps(acts, sort_keys=True).encode("utf-8")).hexdigest()
        if digest in seen:
            continue
        seen[digest] = key
        unique.append((key, acts))
    _RECORDED_LISTS_CACHE = unique
    return list(unique)


def _diff(left: Any, right: Any) -> list[str]:
    if left == right:
        return []
    if not isinstance(left, dict) or not isinstance(right, dict):
        return ["pin"]
    found = []
    for key in sorted(set(left) | set(right)):
        if left.get(key) == right.get(key):
            continue
        if isinstance(left.get(key), dict) and isinstance(right.get(key), dict):
            for name in sorted(set(left[key]) | set(right[key])):
                if left[key].get(name) != right[key].get(name):
                    found.append(f"{key}.{name}")
        else:
            found.append(str(key))
    return found


def _view(pin: dict[str, Any], fields: tuple[str, ...], keep: bool) -> dict[str, Any]:
    if keep:
        return {key: pin.get(key) for key in fields}
    return {key: value for key, value in pin.items() if key not in fields}


def _scalar(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return type(value).__name__


def classify(
    left_pin: dict[str, Any],
    right_pin: dict[str, Any],
    name_a: str = "v86",
    name_b: str = "v87",
) -> dict[str, Any]:
    """Classify comparison between two pins."""
    if left_pin == right_pin:
        err = _scalar(left_pin.get("error")) if isinstance(left_pin, dict) else None
        res: dict[str, Any] = {"class": "identical"}
        if err is not None:
            res["error"] = err
            res[f"{name_a}_error"] = err
            if name_a == "v86":
                res["v86_error"] = err
        elif name_a == "v86":
            res["v86_error"] = None
        return res

    number_fields = _diff(_view(left_pin, SENTENCE_FIELDS, False), _view(right_pin, SENTENCE_FIELDS, False))
    sentence_fields = _diff(_view(left_pin, SENTENCE_FIELDS, True), _view(right_pin, SENTENCE_FIELDS, True))
    if number_fields or "error" in left_pin or "error" in right_pin:
        lines = []
        left = left_pin.get("lines") or {}
        right = right_pin.get("lines") or {}
        if isinstance(left, dict) and isinstance(right, dict):
            for name in sorted(set(left) | set(right)):
                if left.get(name) != right.get(name):
                    lines.append({"line": name, name_a: _scalar(left.get(name)), name_b: _scalar(right.get(name))})
        res = {
            "class": "numbers_changed",
            "number_fields": number_fields[:40],
            "sentence_fields": sentence_fields[:40],
            "lines": lines[:30],
            f"{name_a}_error": _scalar(left_pin.get("error")),
            f"{name_b}_error": _scalar(right_pin.get("error")),
        }
        if name_a == "v86":
            res["v86_error"] = _scalar(left_pin.get("error"))
        return res
    if sentence_fields:
        res = {"class": "numbers_identical_sentences_changed", "sentence_fields": sentence_fields[:40]}
        if name_a == "v86":
            res["v86_error"] = None
        return res
    res = {"class": "numbers_changed", "number_fields": ["unclassified"]}
    if name_a == "v86":
        res["v86_error"] = None
    return res


def fake_per_list(key: str, acts: Acts, cores: Any = None) -> dict[str, Any]:
    """A cheap dummy per-list function for tests and benchmarks."""
    return {"key": key, "acts_count": len(acts)}


def pin_run(core: Any, acts: Acts, run_id: str) -> dict[str, Any]:
    """Run a coordinate run against a core and return the projected pin."""
    test = _get_test()
    resolved_core = resolve_core(core)
    track = test.track0()
    with track.h.loader_entries(resolved_core):
        return test.pin(track.run_coordinate(resolved_core, acts, run_id))  # type: ignore[no-any-return]


_pin_run = pin_run


def neighbour_classify_per_list(key: str, acts: Acts, cores: tuple[Any, Any]) -> dict[str, Any]:
    """Per-list classification for neighbour comparison between two cores."""
    core_a, core_b = cores
    slug = re.sub(r"[^A-Za-z0-9_.-]", ".", key)
    run_id_b = f"demo.qw.t0.nb.{core_b.version}.{slug}" if core_b.version == "v87" else f"demo.replay.nb.{core_b.version}.{slug}"
    run_id_a = f"demo.qw.t0.nb.{core_a.version}.{slug}" if core_a.version == "v86" else f"demo.replay.nb.{core_a.version}.{slug}"
    pin_b = pin_run(core_b, acts, run_id_b)
    pin_a = pin_run(core_a, acts, run_id_a)
    row = classify(pin_a, pin_b, name_a=core_a.version, name_b=core_b.version)
    row["pins"] = {core_a.version: pin_a, core_b.version: pin_b}
    return row


def _invoke_per_list(per_list: Callable[..., Any], key: str, acts: Acts, cores: Any) -> Any:
    try:
        sig = inspect.signature(per_list)
        params = list(sig.parameters.values())
        has_varargs = any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in params)
        positional = [p for p in params if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)]
        if has_varargs:
            if isinstance(cores, (list, tuple)):
                return per_list(key, acts, *cores)
            return per_list(key, acts, cores)
        if len(positional) == 2:
            return per_list(key, acts)
        if len(positional) == 3:
            return per_list(key, acts, cores)
        if len(positional) > 3 and isinstance(cores, (list, tuple)):
            return per_list(key, acts, *cores)
    except (ValueError, TypeError):
        pass
    try:
        return per_list(key, acts, cores)
    except TypeError:
        try:
            return per_list(key, acts, *cores)
        except TypeError:
            return per_list(key, acts)


def _worker_exec(per_list: Callable[..., Any], key: str, acts: Acts, cores: Any) -> tuple[str, Any]:
    res = _invoke_per_list(per_list, key, acts, cores)
    return key, res


def core_fingerprint(core: Any) -> dict[str, Any]:
    """Compute an identity fingerprint for a core."""
    try:
        resolved = resolve_core(core)
    except Exception:
        resolved = core

    if not hasattr(resolved, "version"):
        return {"repr": str(resolved)}

    fp: dict[str, Any] = {
        "version": resolved.version,
        "registry": getattr(resolved, "registry", None),
        "release_version": getattr(resolved, "release_version", None),
        "loader_from": getattr(resolved, "loader_from", None),
        "presence_pairs": list(getattr(resolved, "presence_pairs", ())),
    }
    pkg_path = getattr(resolved, "package_path", None)
    if pkg_path and Path(pkg_path).exists():
        fp["package_sha256"] = hashlib.sha256(Path(pkg_path).read_bytes()).hexdigest()
    rel_path = getattr(resolved, "release_path", None)
    if rel_path and Path(rel_path).exists():
        fp["release_sha256"] = hashlib.sha256(Path(rel_path).read_bytes()).hexdigest()
    return fp


def _write_part(part_path: Path, data: dict[str, Any], metadata: dict[str, Any] | None = None) -> None:
    payload = {
        "_metadata": metadata or {},
        "results": data,
    }
    text = json.dumps(payload, indent=1) + "\n"
    _check_no_local_paths(text, str(part_path))
    tmp = part_path.with_name(f"{part_path.name}.tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(part_path)


def _check_no_local_paths(text: str, label: str) -> None:
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise ValueError(f"{label} contains local path pattern {needle}")


def replay(
    lists: list[tuple[str, Acts]],
    cores: Any,
    per_list: Callable[..., Any],
    workers: int | None = None,
    part: Path | str | None = None,
) -> dict[str, Any]:
    """Run per_list over every list in a concurrent.futures process pool.

    Writes a resumable part file as results arrive, skips keys already present,
    and returns results keyed and sorted by list key.
    """
    max_workers = workers if (workers is not None and workers > 0) else max(1, (os.cpu_count() or 2) - 1)
    part_path = Path(part) if part is not None else None
    found: dict[str, Any] = {}

    cores_list = cores if isinstance(cores, (list, tuple)) else (cores,)
    expected_fingerprint = [core_fingerprint(c) for c in cores_list] if cores not in ((), None) else []
    metadata = {"cores": expected_fingerprint}

    if part_path is not None and part_path.exists():
        try:
            loaded = json.loads(part_path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict) and "_metadata" in loaded and "results" in loaded:
                part_meta = loaded.get("_metadata") or {}
                part_cores = part_meta.get("cores")
                if expected_fingerprint and part_cores != expected_fingerprint:
                    raise ValueError(
                        f"Part file {part_path} was recorded for different cores: "
                        f"{part_cores} != {expected_fingerprint}"
                    )
                found = loaded.get("results") or {}
            elif isinstance(loaded, dict):
                if expected_fingerprint:
                    raise ValueError(f"Part file {part_path} does not match expected core metadata")
                found = loaded
        except ValueError:
            raise
        except Exception:
            found = {}

    pending = [(key, acts) for key, acts in lists if key not in found]
    if pending:
        total = len(lists)
        done = len(found)
        ctx = multiprocessing.get_context("spawn")
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers, mp_context=ctx) as pool:
            futures = {pool.submit(_worker_exec, per_list, key, acts, cores): key for key, acts in pending}
            for future in concurrent.futures.as_completed(futures):
                key, result = future.result()
                found[key] = result
                done += 1
                if part_path is not None:
                    _write_part(part_path, found, metadata)
                if done % 25 == 0 or done == total:
                    print(f"[{done}/{total}] {key} -> {result.get('class', 'ok') if isinstance(result, dict) else 'ok'}", flush=True)

    requested_keys = {key for key, _ in lists}
    return {k: found[k] for k in sorted(requested_keys) if k in found}


def run_neighbour(
    core_a_spec: Any,
    core_b_spec: Any,
    workers: int | None = None,
    part: Path | str | None = None,
    out: Path | str | None = None,
) -> dict[str, Any]:
    """Run neighbour comparison between two cores and produce classification rows."""
    core_a = resolve_core(core_a_spec)
    core_b = resolve_core(core_b_spec)
    lists = recorded_lists()
    results = replay(lists, (core_a, core_b), neighbour_classify_per_list, workers=workers, part=part)

    by_set: dict[str, Counter[str]] = {}
    errors: dict[str, Counter[str]] = {}
    for key, row in results.items():
        prefix = key.split("/", 1)[0]
        by_set.setdefault(prefix, Counter())[row["class"]] += 1
        if row.get("class") == "identical":
            err = row.get(f"{core_a.version}_error") or row.get("error") or row.get("v86_error")
            if err:
                errors.setdefault(prefix, Counter())[str(err)] += 1

    changes = [
        {"id": key, **{k: v for k, v in row.items() if k != "pins"}}
        for key, row in sorted(results.items())
        if row["class"] != "identical"
    ]
    summary = {
        "sets": {
            "v83": "tests/fixtures/f1099b_backup_withholding_v83/expected.json: the 298 lists the v86 test replays",
            "v84": "tests/fixtures/f1099b_box7_loss_v84/expected.json: the box 7 Track 0 grid (box7_cases)",
            "v85": "tests/fixtures/f1099b_box4_only_v85/expected.json: the no-sale box 4 Track 0 grid (box4_cases)",
            "v82": "tests/fixtures/sale_family_audit_v82/expected.json: the Track 0 runs, built for v82",
            "v81": "tests/fixtures/code_b_sales_v81/expected.json: the 213 exported returns, uncorrected",
        },
        "distinct_lists": len(results),
        "runs": len(results),
        "counts": {key: dict(value) for key, value in sorted(by_set.items())},
        "same_error_on_both_cores": {key: dict(value) for key, value in sorted(errors.items())},
        "changes": changes,
        "classes": {key: row["class"] for key, row in sorted(results.items())},
    }

    if out is not None:
        out_path = Path(out)
        text = json.dumps(summary, indent=2) + "\n"
        _check_no_local_paths(text, str(out_path))
        out_path.write_text(text, encoding="utf-8")

    return summary


def recorded_pin_from_expected(expected: dict[str, Any], key: str) -> dict[str, Any]:
    """Look up the recorded fixture pin for a key in v83 expected.json."""
    group, _, name = key.partition("/")
    if group == "track0":
        return expected["track0"][name]  # type: ignore[no-any-return]
    if group == "returns":
        return expected["returns"][name]["v83"]  # type: ignore[no-any-return]
    return expected["zero_sample"][name]["v83"]  # type: ignore[no-any-return]


def summarize_rerun(
    results: dict[str, Any],
    baseline_version: str = "v86",
    comparison_version: str = "v87",
    expected_fixture: Path | dict[str, Any] | None = None,
    neighbour_fixture: Path | dict[str, Any] | None = None,
    out: Path | str | None = None,
) -> dict[str, Any]:
    """Derive P0 rerun-output summary from parallel replay results."""
    if expected_fixture is None:
        expected_fixture = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
    if isinstance(expected_fixture, (str, Path)):
        expected_data = json.loads(Path(expected_fixture).read_text(encoding="utf-8"))
    else:
        expected_data = expected_fixture

    if neighbour_fixture is None:
        neighbour_fixture = REPO / "docs/phases/engine-breadth/milestones/f1099b-box4-only-evidence/track0-neighbour.json"
    if isinstance(neighbour_fixture, (str, Path)):
        nb_data = json.loads(Path(neighbour_fixture).read_text(encoding="utf-8"))
    else:
        nb_data = neighbour_fixture
    asks = set(nb_data.get("asks_no_sale_present_ids") or [])

    v83_results: dict[str, Any] = {}
    for key, row in sorted(results.items()):
        if not key.startswith("v83/"):
            continue
        short_key = key.removeprefix("v83/")
        pins = row.get("pins") or {}
        pin_a = pins.get(baseline_version)

        rerun_row: dict[str, Any] = {
            "class": row["class"],
        }
        for field in ("number_fields", "sentence_fields", "lines", f"{baseline_version}_error", f"{comparison_version}_error"):
            if field in row:
                rerun_row[field] = row[field]

        if pin_a is not None:
            expected_pin = recorded_pin_from_expected(expected_data, short_key)
            rerun_row[f"{baseline_version}_matches_fixture"] = (pin_a == expected_pin)
        rerun_row["restored_present_no"] = (short_key in asks)
        v83_results[short_key] = rerun_row

    counts = dict(Counter(row["class"] for row in v83_results.values()))
    changes = [{"id": k, **v} for k, v in sorted(v83_results.items()) if v["class"] != "identical"]
    matches_count = sum(1 for row in v83_results.values() if row.get(f"{baseline_version}_matches_fixture"))
    restored_count = sum(1 for row in v83_results.values() if row.get("restored_present_no"))

    payload = {
        "fixture": "tests/fixtures/f1099b_backup_withholding_v83/expected.json",
        "replay": (
            "298 act lists from tests/test_f1099b_selection_keyed_collect_v86.py: "
            "207 as recorded, 91 restored with no-sale box 4 present=no"
        ),
        "cores": f"core {baseline_version} and core {comparison_version}, answered as recorded",
        "classes_defined": {
            "identical": f"the {baseline_version} and {comparison_version} pins are equal",
            "numbers_identical_sentences_changed": "only questions, reasons or blocked reasons differ",
            "numbers_changed": "a line, attachment, base or row differs, or one core errors",
        },
        "runs": len(v83_results),
        "live_runs": len(v83_results) * 2,
        "restored_present_no": restored_count,
        f"{baseline_version}_matches_fixture": matches_count,
        "counts": counts,
        "classes": {k: v["class"] for k, v in sorted(v83_results.items())},
        "changes": changes,
        "change_count": len(changes),
    }

    if out is not None:
        out_path = Path(out)
        text = json.dumps(payload, indent=2) + "\n"
        _check_no_local_paths(text, str(out_path))
        out_path.write_text(text, encoding="utf-8")

    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay recorded returns in parallel.")
    subparsers = parser.add_subparsers(dest="subcommand")

    nb_parser = subparsers.add_parser("neighbour", help="Replay neighbour comparison between two cores.")
    nb_parser.add_argument("core_a", help="First (baseline) core, e.g. v86 or path to core.json")
    nb_parser.add_argument("core_b", help="Second (comparison) core, e.g. v87 or path to core.json")
    nb_parser.add_argument("--workers", "-w", type=int, default=None, help="Worker count")
    nb_parser.add_argument("--part", type=Path, default=None, help="Resumable part file path")
    nb_parser.add_argument("--out", type=Path, default=None, help="Output JSON path")

    rerun_parser = subparsers.add_parser("rerun", help="Derive P0 rerun summary from a replay part file.")
    rerun_parser.add_argument("--part", required=True, type=Path, help="Part file path")
    rerun_parser.add_argument("--out", type=Path, default=None, help="Output JSON path")
    rerun_parser.add_argument("--baseline", default="v86", help="Baseline core version")
    rerun_parser.add_argument("--comparison", default="v87", help="Comparison core version")

    args = parser.parse_args()
    if args.subcommand == "neighbour":
        summary = run_neighbour(
            args.core_a,
            args.core_b,
            workers=args.workers,
            part=args.part,
            out=args.out,
        )
        print(json.dumps({
            "runs": summary["runs"],
            "counts": summary["counts"],
            "changes": len(summary["changes"]),
        }, indent=2))
    elif args.subcommand == "rerun":
        loaded = json.loads(args.part.read_text(encoding="utf-8"))
        results: dict[str, Any]
        if isinstance(loaded, dict) and isinstance(loaded.get("results"), dict):
            results = loaded["results"]
        elif isinstance(loaded, dict):
            results = loaded
        else:
            raise ValueError(f"Invalid part file format in {args.part}")
        payload = summarize_rerun(
            results,
            baseline_version=args.baseline,
            comparison_version=args.comparison,
            out=args.out,
        )
        print(json.dumps({
            "runs": payload["runs"],
            "counts": payload["counts"],
            f"{args.baseline}_matches_fixture": payload[f"{args.baseline}_matches_fixture"],
        }, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
