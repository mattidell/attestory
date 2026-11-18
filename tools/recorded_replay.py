"""Replay recorded return act lists in parallel across worker processes.

Importable and runnable tool for recorded act list replay and neighbour diffs.
Part of the parallel-replay tooling milestone (Engine Breadth).

Two comparisons exist.  The older pin (`pin_run`, `classify`, `neighbour`)
keeps only watched lines and rule rows and stays as it was.  The full-surface
comparison (full-surface-replay milestone) holds the whole saved return:

    python3 tools/recorded_replay.py full v95 v96 --expect expect.json \
        --part part.json --out summary.json

`snapshot(model, report)` flattens every saved page field, attachment,
explanation-graph node and report row into typed records; `diff_snapshots`
returns every difference (kind, identity, attribute, before, after);
`classify_full` fails any difference no `Expectation` names.  An expectation
must name a kind and an attribute, never "anything on this list".  Example:

    text_change("tax.us.2025.form1040.line-6a",
                "dispositions.computed_zero.explain", "old text", "new text")
    version_change("tax.us.2025.rule.attachment.f8949", "v6", "v7")

`standard_controls(model, report)` mutates a saved output before the snapshot
so a milestone can show the comparison sees every field and row.  See
docs/phases/engine-breadth/milestones/full-surface-replay-evidence/track1.md.

What a passing full-surface comparison does and does not mean
-------------------------------------------------------------
"Nothing else changed" holds only for the saved surfaces the recorded corpus
reaches.  The optional model blocks (`provenanceGroups`, `calculationView`,
`line21Explanation`, `mortgageInterestExplanation`,
`mortgageBorrowingExplanation`, `f1099kStatementExplanation`) are held by the
snapshot, but no recorded list produces most of them; a milestone that touches
one needs its own list (see the mortgage control in track1.md) and should state
which blocks the run reached (`optional_blocks_reached` in the `run_full`
summary).  Named blind spots, all of them narrower than the snapshot itself:

* Order of hash-keyed list items.  Pins and graph edges that name a derived
  finding sit in the order of the masked hashes, so their relative order is not
  recorded as a sequence.  One boolean per list stands in for it: whether every
  derived node's edges, and every page finding's pins, are in the (role, raw id)
  order the page requires (`graph|edges-in-role-id-order`,
  `page|pins-in-role-id-order`).
* Dictionary key order is not recorded, except the keys of
  `recordedApplicableClaims`, the one place the page renders it
  (`recordedApplicableClaims@keys`).
* Generated finding and act hashes, run ids and graph-node keys are aliased or
  masked (see `_generated_aliases`).  Local paths are masked only in the
  messages of failed lists (`failure_snapshot`), not in saved strings.
* Unused expectations are reported (`unused_expectations`), not failed: a
  declared change no list exercised cannot hide a difference but is not proof.
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


# ---------------------------------------------------------------------------
# Full-surface snapshot, diff, classification and controls
# ---------------------------------------------------------------------------

SNAPSHOT_FORMAT = "full-surface.v1"
GENERATED_ID = re.compile(r"(?:finding:derived|act:publication):[0-9a-f]{24}")
LOCAL_PATH = re.compile(r"/(?:Users|private|tmp|var|opt)/\S+")
IDENTITY_KEYS = ("id", "siteId", "artifact_id", "symbol", "role", "target")
OPTIONAL_BLOCKS = ("provenanceGroups", "calculationView", "line21Explanation", "mortgageInterestExplanation",
                   "mortgageBorrowingExplanation", "f1099kStatementExplanation")
KEY_ORDER_RENDERED = "recordedApplicableClaims"  # the one dictionary whose key order the page renders
MODEL_KINDS = {"sections": "page", "attachments": "attachment", "explanationGraph": "graph"}


class _AnyType:
    """Picklable wildcard for an expectation's before or after value."""

    def __repr__(self) -> str:
        return "ANY"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _AnyType)

    def __hash__(self) -> int:
        return 0


ANY = _AnyType()


def _encoded(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _same(left: Any, right: Any) -> bool:
    """Typed equality: 1, 1.0 and True are three different saved values."""
    return _encoded(left) == _encoded(right)


def _item_labels(items: list[dict[str, Any]]) -> list[str]:
    labels: list[str] = []
    seen: Counter[str] = Counter()
    for index, item in enumerate(items):
        parts = [
            str(item[key])
            for key in IDENTITY_KEYS
            if isinstance(item.get(key), (str, int)) and not isinstance(item.get(key), bool)
        ]
        base = "|".join(parts) if parts else f"[{index}]"
        seen[base] += 1
        labels.append(base if seen[base] == 1 else f"{base}#{seen[base]}")
    return labels


def _generated_aliases(model: dict[str, Any], report: dict[str, Any]) -> tuple[dict[str, str], dict[str, str]]:
    """Stable aliases for generated identifiers and graph node keys.

    Generated finding and act ids are hashes of the pinned citizen versions, so
    they differ between cores for identical content.  A derived finding is
    aliased by its symbol and the structure of its inputs (ids and roles, never
    versions); the version and the value stay in the snapshot as compared
    attributes.  Same-alias findings are numbered in graph order.
    """
    graph = model.get("explanationGraph")
    nodes = graph.get("nodes") if isinstance(graph, dict) else None
    nodes = nodes if isinstance(nodes, dict) else {}
    by_id = {
        node["id"]: node
        for node in nodes.values()
        if isinstance(node, dict) and node.get("kind") == "derived" and isinstance(node.get("id"), str)
    }
    base: dict[str, str] = {}
    limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max(limit, 20000))

    def shape(fid: str, active: frozenset[str]) -> str:
        if fid in base:
            return base[fid]
        node = by_id[fid]
        described = []
        for edge in node.get("edges") or []:
            pin = edge.get("pin") or {}
            target = nodes.get(edge.get("target"))
            if isinstance(target, dict) and target.get("kind") == "derived" and target.get("id") in by_id and target["id"] not in active:
                ref: Any = shape(target["id"], active | {fid})
            else:
                ref = pin.get("id")
            described.append([pin.get("role"), ref])
        described.sort(key=_encoded)
        digest = hashlib.sha1(_encoded([(node.get("produced_by") or {}).get("id"), described]).encode()).hexdigest()[:10]
        base[fid] = f"finding~{node.get('symbol')}~{digest}"
        return base[fid]

    try:
        for fid in by_id:
            shape(fid, frozenset())
    finally:
        sys.setrecursionlimit(limit)
    final: dict[str, str] = {}
    used: Counter[str] = Counter()
    for fid in by_id:
        used[base[fid]] += 1
        final[fid] = base[fid] if used[base[fid]] == 1 else f"{base[fid]}#{used[base[fid]]}"
    for row in report.get("dispositions") or []:
        if not isinstance(row, dict):
            continue
        fid = row.get("finding_id")
        row_alias = f"finding~row~{row.get('artifact_id')}~{row.get('symbol')}"
        if isinstance(fid, str) and fid not in final:
            final[fid] = row_alias
        act = row.get("act_id")
        if isinstance(act, str) and act not in final:
            final[act] = "act~" + (final.get(fid, row_alias) if isinstance(fid, str) else row_alias)

    def transform(text: str) -> str:
        return GENERATED_ID.sub(lambda m: final.get(m.group(0), m.group(0)), text)

    labels: dict[str, str] = {}
    taken: Counter[str] = Counter()
    for key, node in nodes.items():
        if isinstance(node, dict) and isinstance(node.get("id"), str) and isinstance(node.get("kind"), str):
            label = f"{node['kind']}:{transform(node['id'])}"
            taken[label] += 1
            labels[key] = label if taken[label] == 1 else f"{label}#{taken[label]}"
    return final, labels


def _canonical(node: Any, final: dict[str, str], labels: dict[str, str], masks: tuple[str, ...]) -> Any:
    def text(value: str) -> str:
        if value in labels:
            return labels[value]
        value = GENERATED_ID.sub(lambda m: final.get(m.group(0), m.group(0)), value)
        for mask in masks:
            value = value.replace(mask, "<run>")
        return value

    if isinstance(node, str):
        return text(node)
    if isinstance(node, list):
        return [_canonical(item, final, labels, masks) for item in node]
    if isinstance(node, dict):
        return {text(str(key)): _canonical(value, final, labels, masks) for key, value in node.items()}
    return node


def _flatten(node: Any, kind: str, ident: str, rel: str, out: list[list[Any]]) -> None:
    if isinstance(node, dict):
        if not node:
            out.append([kind, ident, rel, {}])
            return
        for key, value in node.items():
            child = f"{rel}.{key}" if rel else str(key)
            if key == KEY_ORDER_RENDERED and isinstance(value, dict):
                out.append([kind, ident, f"{child}@keys", list(value)])
            if isinstance(value, dict) and value and isinstance(value.get("id"), str):
                _flatten(value, kind, f"{ident}/{child}={value['id']}" if ident else f"{child}={value['id']}", "", out)
            else:
                _flatten(value, kind, ident, child, out)
    elif isinstance(node, list):
        if node and all(isinstance(item, dict) and item for item in node):
            labels = _item_labels(node)
            # Items labelled by an aliased generated id sit in the order of the
            # masked hashes, so only the order of the other items is recorded.
            out.append([kind, ident, f"{rel}@order", [x for x in labels if "finding~" not in x and "act~" not in x]])
            for label, item in zip(labels, node):
                seg = f"{rel}[{label}]"
                _flatten(item, kind, f"{ident}/{seg}" if ident else seg, "", out)
        else:
            out.append([kind, ident, rel, node])
    else:
        out.append([kind, ident, rel, node])


def _role_id_order(pins: Any) -> bool:
    """True when pins (or edges' pins) are in the (role, raw id) order the page requires."""
    keys = [(p.get("role"), p.get("id")) for p in pins if isinstance(p, dict)]
    try:
        return keys == sorted(keys)  # type: ignore[type-var]
    except TypeError:
        return False


def _order_invariants(model: dict[str, Any]) -> list[list[Any]]:
    """Whether hash-keyed pins and edges are in the order the page requires.

    Their relative order is not recorded as a sequence (the hashes are masked),
    so one boolean per saved output stands in for it, taken before aliasing.
    """
    graph = model.get("explanationGraph")
    nodes = graph.get("nodes") if isinstance(graph, dict) else None
    edges_ok = all(
        _role_id_order([e.get("pin") for e in node.get("edges") or [] if isinstance(e, dict)])
        for node in (nodes.values() if isinstance(nodes, dict) else ())
        if isinstance(node, dict) and node.get("kind") == "derived"
    )
    pins_ok = True
    for section in model.get("sections") or []:
        resolved = section.get("resolved") if isinstance(section, dict) else None
        act = resolved.get("act") if isinstance(resolved, dict) else None
        finding = act.get("finding") if isinstance(act, dict) else None
        if isinstance(finding, dict) and isinstance(finding.get("pins"), list) and not _role_id_order(finding["pins"]):
            pins_ok = False
    return [["graph", "", "edges-in-role-id-order", edges_ok], ["page", "", "pins-in-role-id-order", pins_ok]]


def snapshot(model: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    """Full-surface snapshot of one saved presentation model and report.

    Every key of the model and of the report is flattened to typed records
    [kind, identity, attribute, value]: page fields (kind "page": identity,
    value, disposition, all text, reasons, questions, categorical render text),
    attachments, every explanation-graph node and edge, every other model key,
    and every report row with its full identity (kind "row") plus the
    remaining report keys.  Nothing is selected by line.  Run ids and generated
    finding/act hashes are masked or aliased (see `_generated_aliases`), and the
    relative order of list items keyed by such a hash is replaced by one boolean
    per output (`_order_invariants`).  Dictionary key order is not recorded
    except for `recordedApplicableClaims`.  The module docstring names these
    blind spots.
    """
    final, labels = _generated_aliases(model, report)
    masks = tuple(
        value
        for value in (
            model.get("runId"),
            report.get("run_id"),
            (model.get("explanationGraph") or {}).get("run_id") if isinstance(model.get("explanationGraph"), dict) else None,
        )
        if isinstance(value, str) and len(value) > 3
    )
    canon_model = _canonical(model, final, labels, masks)
    canon_report = _canonical(report, final, labels, masks)
    records: list[list[Any]] = []
    for key, value in canon_model.items():
        _flatten(value, MODEL_KINDS.get(key, "model"), "", key, records)
    for key, value in canon_report.items():
        _flatten(value, "row" if key == "dispositions" else "report", "", key, records)
    records.extend(_order_invariants(model))
    blocks = [name for name in OPTIONAL_BLOCKS if name in model]
    return {"format": SNAPSHOT_FORMAT, "outcome": "success", "blocks": blocks, "records": records}


def failure_snapshot(outcome: str, error_class: str, message: str) -> dict[str, Any]:
    """Snapshot of a list that errored or was refused: class and message only."""
    clean = LOCAL_PATH.sub("<path>", message)
    return {
        "format": SNAPSHOT_FORMAT,
        "outcome": outcome,
        "records": [["error", "", "class", error_class], ["error", "", "message", clean]],
    }


def snapshot_sha256(snap: dict[str, Any]) -> str:
    return hashlib.sha256(_encoded(snap).encode()).hexdigest()


def _record_map(snap: dict[str, Any]) -> dict[tuple[str, str, str], Any]:
    found: dict[tuple[str, str, str], Any] = {}
    for kind, ident, attribute, value in snap["records"]:
        key = (kind, ident, attribute)
        if key in found:
            raise ValueError(f"duplicate snapshot record {key}")
        found[key] = value
    return found


def diff_snapshots(left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    """Every difference between two snapshots as typed records.

    Each record: change ("changed", "added", "removed"), kind, identity,
    attribute, before, after.  Order differences appear as a changed "@order"
    attribute.  Differing outcomes are reported as kind "outcome" and the
    remaining records are still compared.
    """
    found: list[dict[str, Any]] = []
    if left["outcome"] != right["outcome"]:
        found.append({"change": "changed", "kind": "outcome", "identity": "", "attribute": "outcome",
                      "before": left["outcome"], "after": right["outcome"]})
    a, b = _record_map(left), _record_map(right)
    for key in list(a) + [k for k in b if k not in a]:
        kind, ident, attribute = key
        if key not in b:
            found.append({"change": "removed", "kind": kind, "identity": ident, "attribute": attribute,
                          "before": a[key], "after": None})
        elif key not in a:
            found.append({"change": "added", "kind": kind, "identity": ident, "attribute": attribute,
                          "before": None, "after": b[key]})
        elif not _same(a[key], b[key]):
            found.append({"change": "changed", "kind": kind, "identity": ident, "attribute": attribute,
                          "before": a[key], "after": b[key]})
    return found


@dataclass(frozen=True)
class Expectation:
    """One declared, bounded difference.

    `kind` (one or more of page, attachment, graph, model, row, report) and
    `attribute` (regular expression, full match) are required, so an
    expectation cannot bless a whole list.  `identity` is a regular expression
    searched in the record identity; `before` and `after` default to ANY.
    """

    kind: tuple[str, ...]
    attribute: str
    identity: str = ""
    change: str | None = None
    before: Any = ANY
    after: Any = ANY
    note: str = ""

    def __post_init__(self) -> None:
        kinds = (self.kind,) if isinstance(self.kind, str) else tuple(self.kind)
        object.__setattr__(self, "kind", kinds)
        if not kinds or not self.attribute:
            raise ValueError("an expectation must name a kind and an attribute")

    def matches(self, diff: dict[str, Any]) -> bool:
        if diff["kind"] not in self.kind or not re.fullmatch(self.attribute, diff["attribute"]):
            return False
        if self.identity and not re.search(self.identity, diff["identity"]):
            return False
        if self.change is not None and diff["change"] != self.change:
            return False
        if not isinstance(self.before, _AnyType) and not _same(self.before, diff["before"]):
            return False
        return isinstance(self.after, _AnyType) or _same(self.after, diff["after"])


def describe_expectation(spec: Expectation) -> dict[str, Any]:
    """An expectation by identity: its note, kinds, attribute, identity, change and values."""
    return {
        "note": spec.note, "kind": list(spec.kind), "attribute": spec.attribute, "identity": spec.identity,
        "change": spec.change,
        "before": "ANY" if isinstance(spec.before, _AnyType) else spec.before,
        "after": "ANY" if isinstance(spec.after, _AnyType) else spec.after,
    }


def _id_pattern(ident: str) -> str:
    return r"(?<![\w.-])" + re.escape(ident) + r"(?![\w.-])"


def text_change(
    citizen_id: str,
    attribute: str,
    before: str,
    after: str,
    note: str = "",
    kinds: tuple[str, ...] = ("page", "attachment", "model"),
) -> Expectation:
    """Expect one sentence of one citizen (field or attachment) to change.

    A sentence can be saved in more than one place (an attachment title is on
    the attachment and in its citation group); `kinds` names where.
    """
    return Expectation(kinds, re.escape(attribute), _id_pattern(citizen_id), "changed",
                       before, after, note or f"text:{citizen_id}:{attribute}")


def version_change(citizen_id: str, old: str, new: str, note: str = "") -> Expectation:
    """Expect the recorded version of one citizen to move from old to new."""
    return Expectation(("page", "attachment", "graph", "model", "row", "report"), r"(?:.*\.)?(?:version|pinVersion)",
                       _id_pattern(citizen_id), "changed", old, new, note or f"version:{citizen_id}")


def classify_full(
    left: dict[str, Any],
    right: dict[str, Any],
    expectations: Any = (),
) -> dict[str, Any]:
    """Classify two snapshots.  Strict: any difference not expected fails.

    Returns class "identical", "expected_changes" or "unexpected", with
    `differences`, `expected_by_note`, the indexes of the expectations that
    matched something (`used`) and the full `unexpected` list.
    """
    specs = [e if isinstance(e, Expectation) else Expectation(**e) for e in expectations]
    diffs = diff_snapshots(left, right)
    expected_by_note: Counter[str] = Counter()
    used: set[int] = set()
    unexpected: list[dict[str, Any]] = []
    for item in diffs:
        for index, spec in enumerate(specs):
            if spec.matches(item):
                expected_by_note[spec.note or spec.attribute] += 1
                used.add(index)
                break
        else:
            unexpected.append(item)
    cls = "identical" if not diffs else ("unexpected" if unexpected else "expected_changes")
    return {"class": cls, "differences": len(diffs), "expected_by_note": dict(expected_by_note),
            "used": sorted(used), "unexpected": unexpected}


def saved_output(core: Any, acts: Acts, run_id: str) -> dict[str, Any]:
    """Run one list on a core through the real coordinate run; return what is saved.

    Returns {"outcome": "success", "model": ..., "report": ...}, a refusal, or
    an error with the exception class and a path-masked message.
    """
    resolved = resolve_core(core)
    harness = _get_harness()
    try:
        with harness.loader_entries(resolved):
            finished = harness._finish(
                acts, package_path=resolved.package_path, package_version=resolved.version,
                release_path=resolved.release_path, release_version=resolved.release_version, note=run_id,
            )
            finished = harness._handover(finished, surface=resolved.surface(), reconfirm=True)
            with tempfile.TemporaryDirectory() as tmp:
                capability = harness.WorkspaceCapability(Path(tmp) / "L")
                outcome = harness.live_coordinate_run(
                    capability, repo_root=REPO, authoritative_acts=finished, workspace_revision=len(finished),
                    run_scope={"jurisdiction": "us", "year": harness.YEAR}, scope_user=harness.ccr.USER,
                    request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
                    surface=resolved.surface(), output_name="out.json",
                )
                if outcome.refusal:
                    return {"outcome": "refused", "error": "refusal", "message": str(outcome.refusal.reason)}
                return {
                    "outcome": "success",
                    "model": json.loads(outcome.presentation_path.read_text(encoding="utf-8")),
                    "report": json.loads(outcome.output_path.read_text(encoding="utf-8")),
                }
    except Exception as exc:  # the error class and message are part of the compared surface
        return {"outcome": "error", "error": type(exc).__name__, "message": str(exc)}


def snapshot_run(core: Any, acts: Acts, run_id: str) -> dict[str, Any]:
    saved = saved_output(core, acts, run_id)
    if saved["outcome"] == "success":
        return snapshot(saved["model"], saved["report"])
    return failure_snapshot(saved["outcome"], saved["error"], saved["message"])


class FullSurfaceCompare:
    """Picklable per-list function: both cores, full snapshots, strict classify."""

    def __init__(self, expectations: Any = (), max_unexpected: int = 40) -> None:
        self.expectations = [_as_expectation(e) for e in expectations]
        self.max_unexpected = max_unexpected

    def __call__(self, key: str, acts: Acts, cores: tuple[Any, Any]) -> dict[str, Any]:
        core_a, core_b = cores
        run_id = "demo.fsr." + hashlib.sha256(key.encode()).hexdigest()[:20]
        snap_a = snapshot_run(core_a, acts, run_id)
        snap_b = snapshot_run(core_b, acts, run_id)
        verdict = classify_full(snap_a, snap_b, self.expectations)
        unexpected = verdict.pop("unexpected")
        verdict["unexpected_total"] = len(unexpected)
        verdict["unexpected"] = unexpected[: self.max_unexpected]
        verdict["outcomes"] = [snap_a["outcome"], snap_b["outcome"]]
        verdict["records"] = [len(snap_a["records"]), len(snap_b["records"])]
        verdict["blocks"] = sorted(set(snap_a.get("blocks", [])) | set(snap_b.get("blocks", [])))
        verdict["sha256"] = [snapshot_sha256(snap_a), snapshot_sha256(snap_b)]
        return verdict


def _as_expectation(spec: Any) -> Expectation:
    return spec if isinstance(spec, Expectation) else Expectation(**spec)


def run_full(
    core_a_spec: Any,
    core_b_spec: Any,
    expectations: Any = (),
    workers: int | None = None,
    part: Path | str | None = None,
    out: Path | str | None = None,
    lists: list[tuple[str, Acts]] | None = None,
) -> dict[str, Any]:
    """Full-surface comparison of two cores over the recorded lists (parallel)."""
    core_a, core_b = resolve_core(core_a_spec), resolve_core(core_b_spec)
    chosen = recorded_lists() if lists is None else lists
    results = replay(chosen, (core_a, core_b), FullSurfaceCompare(expectations), workers=workers, part=part)
    classes = Counter(row["class"] for row in results.values())
    specs = [_as_expectation(e) for e in expectations]
    used_anywhere = {index for row in results.values() for index in row.get("used", [])}
    unused = [describe_expectation(spec) for index, spec in enumerate(specs) if index not in used_anywhere]
    by_attribute: dict[str, dict[str, Any]] = {}
    for key, row in results.items():
        for item in row["unexpected"]:
            slot = by_attribute.setdefault(
                f"{item['kind']}|{item['change']}|{re.sub(r'[0-9]+', 'N', item['attribute'])}", {"lists": set(), "samples": []}
            )
            slot["lists"].add(key)
            if len(slot["samples"]) < 3:
                slot["samples"].append({"list": key, **item})
    summary = {
        "format": "full-surface-replay.v1",
        "cores": [core_fingerprint(core_a), core_fingerprint(core_b)],
        "lists": len(results),
        "classes": dict(sorted(classes.items())),
        "passing": sum(1 for row in results.values() if row["class"] != "unexpected"),
        "failing": sum(1 for row in results.values() if row["class"] == "unexpected"),
        "unexpected_differences": sum(row["unexpected_total"] for row in results.values()),
        "unexpected_by_kind_attribute": {
            name: {"lists": len(slot["lists"]), "samples": slot["samples"]} for name, slot in sorted(by_attribute.items())
        },
        "expectations_declared": len(specs),
        "expectations_used": len(specs) - len(unused),
        "unused_expectations": unused,
        "optional_blocks_reached": dict(sorted(sum(
            (Counter(row.get("blocks", [])) for row in results.values()), Counter()).items())),
        "expected_by_note": dict(sorted(sum((Counter(row["expected_by_note"]) for row in results.values()), Counter()).items())),
        "outcomes": dict(sorted(Counter("/".join(row["outcomes"]) for row in results.values()).items())),
        "list_classes": {key: row["class"] for key, row in sorted(results.items())},
        "failing_lists": {key: row["unexpected_total"] for key, row in sorted(results.items()) if row["class"] == "unexpected"},
    }
    if out is not None:
        text = json.dumps(summary, indent=1) + "\n"
        _check_no_local_paths(text, str(out))
        Path(out).write_text(text, encoding="utf-8")
    return summary


def _find_section(model: dict[str, Any], want_value: bool = True) -> dict[str, Any] | None:
    sections = model.get("sections") or []
    for preferred in ("line-12e",):
        for section in sections:
            if section.get("id") == preferred and (not want_value or "value" in section["resolved"]):
                return section  # type: ignore[no-any-return]
    for section in sections:
        if not want_value or "value" in section["resolved"]:
            return section  # type: ignore[no-any-return]
    return None


def _first_sentence_holder(model: dict[str, Any]) -> tuple[Any, Any] | None:
    for section in model.get("sections") or []:
        resolved = section["resolved"]
        for name in ("questions", "reasons", "blocked_reasons"):
            items = resolved.get(name)
            if isinstance(items, list) and items:
                first = items[0]
                if isinstance(first, dict):
                    for field_name, field_value in first.items():
                        if isinstance(field_value, str):
                            return first, field_name
                elif isinstance(first, str):
                    return items, 0
    return None


def _first_explanation_note(model: dict[str, Any]) -> dict[str, Any] | None:
    """The first resolved member with a `notes` text in an optional explanation block, if any."""
    block = model.get("mortgageBorrowingExplanation")
    chain = block.get("calculationChain") if isinstance(block, dict) else None
    for member in (chain.get("resolvedContent") if isinstance(chain, dict) else None) or []:
        if isinstance(member, dict) and isinstance(member.get("notes"), str) and isinstance(member.get("id"), str):
            return member
    return None


def standard_controls(model: dict[str, Any], report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Mutated copies of one saved output, made before the snapshot is taken.

    Returns name -> {"model", "report", "expectations", "must" ("reject" or
    "accept"), "available"}.  A control whose target is absent from this output
    (for example a changed question on an output with no questions) has
    available False; callers choose an output where it exists.
    """
    controls: dict[str, dict[str, Any]] = {}

    def make(name: str, must: str = "reject") -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        entry: dict[str, Any] = {"model": copy.deepcopy(model), "report": copy.deepcopy(report),
                                 "expectations": [], "must": must, "available": True}
        controls[name] = entry
        return entry["model"], entry["report"], entry

    m, _r, e = make("changed_field_value")
    target = _find_section(m)
    if target is None:
        e["available"] = False
    else:
        old = target["resolved"]["value"]
        target["resolved"]["value"] = (old + 1) if isinstance(old, (int, float)) and not isinstance(old, bool) else "demo.changed-value"
        e["target"] = target["id"]

    m, r, e = make("changed_line_12e_value")
    twelve = next((x for x in m.get("sections") or [] if x.get("id") == "line-12e" and "value" in x["resolved"]), None)
    if twelve is None:
        e["available"] = False
    else:
        old = twelve["resolved"]["value"]
        twelve["resolved"]["value"] = (old + 1) if isinstance(old, (int, float)) and not isinstance(old, bool) else "demo.changed-value"
        e["target"] = "line-12e"

    m, r, e = make("changed_unwatched_row_code")
    rows = r.get("dispositions") or []
    row = next((x for x in rows if x.get("artifact_id") == "tax.us.2025.rule.interest.nominee-reduction"), rows[0] if rows else None)
    if row is None:
        e["available"] = False
    else:
        row["code"] = "demo.changed-code"
        e["target"] = row.get("artifact_id")

    m, r, e = make("removed_field")
    if m.get("sections"):
        e["target"] = m["sections"].pop()["id"]
    else:
        e["available"] = False

    m, r, e = make("added_field")
    if m.get("sections"):
        extra = copy.deepcopy(m["sections"][0])
        extra["id"] = "demo.added-field"
        m["sections"].append(extra)
    else:
        e["available"] = False

    m, r, e = make("changed_page_disposition")
    target = _find_section(m, want_value=False)
    if target is None:
        e["available"] = False
    else:
        target["resolved"]["disposition"] = "demo.changed-disposition"
        e["target"] = target["id"]

    m, r, e = make("changed_row_disposition")
    if r.get("dispositions"):
        r["dispositions"][-1]["disposition"] = "demo.changed-disposition"
    else:
        e["available"] = False

    m, r, e = make("changed_missing_name")
    row = next((x for x in r.get("dispositions") or [] if isinstance(x.get("missing"), list) and x["missing"]), None)
    if row is None:
        e["available"] = False
    else:
        row["missing"][0] = "demo.changed-missing-name"

    m, r, e = make("changed_question")
    holder = _first_sentence_holder(m)
    if holder is None:
        e["available"] = False
    else:
        holder[0][holder[1]] = "demo.changed question?"

    m, r, e = make("unexpected_sentence")
    target = _find_section(m, want_value=False)
    if target is None:
        e["available"] = False
    else:
        target["field"]["label"] = f"{target['field']['label']} demo.unplanned sentence"
        e["target"] = target["id"]

    m, r, e = make("expected_sentence", must="accept")
    target = _find_section(m, want_value=False)
    if target is None:
        e["available"] = False
    else:
        before = target["field"]["label"]
        after = f"{before} (demo.planned sentence)"
        target["field"]["label"] = after
        e["expectations"] = [text_change(target["field"]["id"], "label", before, after, note="demo planned sentence")]
        e["target"] = target["id"]

    m, r, e = make("changed_graph_node_value")
    nodes = (m.get("explanationGraph") or {}).get("nodes") or {}
    shown = {
        (x.get("resolved", {}).get("act") or {}).get("finding", {}).get("id")
        for x in m.get("sections") or []
    }
    derived = [n for n in nodes.values() if isinstance(n, dict) and n.get("kind") == "derived"]
    # prefer a worksheet finding no page field shows, so only the graph holds its value
    graph_only = [n for n in derived if n.get("id") not in shown] or derived
    if not graph_only:
        e["available"] = False
    else:
        graph_only[0]["value"] = "demo.changed-graph-value"
        e["target"] = graph_only[0].get("id")

    m, r, e = make("changed_disposition_node")
    disposition_nodes = m.get("dispositionNodes") or {}
    holder = next((n for n in disposition_nodes.values() if isinstance(n, dict) and n.get("records")), None)
    if holder is None:
        e["available"] = False
    else:
        holder["records"][0]["disposition"] = "demo.changed-disposition"
        e["target"] = holder.get("symbol")

    m, r, e = make("changed_section_root")
    roots = m.get("sectionRoots") or {}
    if not roots:
        e["available"] = False
    else:
        first = next(iter(roots))
        roots[first]["root"] = "demo.changed-root"
        e["target"] = first

    m, r, e = make("changed_authorization")
    if isinstance(m.get("authorization"), dict):
        m["authorization"]["status"] = "demo.changed-status"
    else:
        e["available"] = False

    m, r, e = make("changed_explanation_block_note")
    member = _first_explanation_note(m)
    if member is None:
        e["available"] = False
    else:
        member["notes"] = member["notes"] + " demo.unplanned sentence"
        e["target"] = member.get("id")

    m, r, e = make("expected_explanation_block_note", must="accept")
    member = _first_explanation_note(m)
    if member is None:
        e["available"] = False
    else:
        before = member["notes"]
        member["notes"] = after = before + " (demo.planned sentence)"
        e["expectations"] = [text_change(member["id"], "notes", before, after, note="demo planned note")]
        e["target"] = member.get("id")
    return controls


def run_controls(model: dict[str, Any], report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Take the snapshot of the unmodified output, then of each control, and judge."""
    base = snapshot(model, report)
    verdicts: dict[str, dict[str, Any]] = {}
    for name, entry in standard_controls(model, report).items():
        if not entry["available"]:
            verdicts[name] = {"available": False}
            continue
        result = classify_full(base, snapshot(entry["model"], entry["report"]), entry["expectations"])
        failed = result["class"] == "unexpected"
        verdicts[name] = {
            "available": True,
            "target": entry.get("target"),
            "must": entry["must"],
            "class": result["class"],
            "differences": result["differences"],
            "ok": failed if entry["must"] == "reject" else result["class"] == "expected_changes",
        }
    return verdicts


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

    full_parser = subparsers.add_parser("full", help="Full-surface comparison of two cores on every recorded list.")
    full_parser.add_argument("core_a")
    full_parser.add_argument("core_b")
    full_parser.add_argument("--expect", type=Path, default=None, help="JSON list of expectations")
    full_parser.add_argument("--workers", "-w", type=int, default=None)
    full_parser.add_argument("--part", type=Path, default=None)
    full_parser.add_argument("--out", type=Path, default=None)

    args = parser.parse_args()
    if args.subcommand == "full":
        expectations = json.loads(args.expect.read_text(encoding="utf-8")) if args.expect else []
        full = run_full(args.core_a, args.core_b, expectations, workers=args.workers, part=args.part, out=args.out)
        print(json.dumps({k: full[k] for k in (
            "lists", "classes", "passing", "failing", "unexpected_differences",
            "expectations_declared", "expectations_used", "unused_expectations", "optional_blocks_reached")}, indent=2))
    elif args.subcommand == "neighbour":
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
