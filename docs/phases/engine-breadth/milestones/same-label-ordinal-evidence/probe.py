"""Track 1 probe: same-named members told apart by entry order (same-label-ordinal, ADR 0090).

Evidence for docs/phases/engine-breadth/milestones/same-label-ordinal.md, Track 1.

Reuses same-label-members' ``probe.py`` (loaded by path under a unique name):
the same 23 synthetic demo.* returns, built and run the same way. ``observe``
adds what the page draws: for every blocked line with a member reason, the
line is rendered alone through the page-plain-words DOM checker and the
member reason items are read back as drawn text, in order
(``drawn``: line -> ["<prefix>: <sentence>", ...]).

Run: python3 probe.py [--core v108] [--only CASE] [--out FILE]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import multiprocessing
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
MILESTONES = HERE.parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def _load(name: str, path: Path) -> Any:
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


slm = _load("slo_t1_slm_probe", MILESTONES / "same-label-members-evidence/probe.py")
PAGE = REPO / "packages/presentation/pages/citation-walk.v1.html"
CASES = slm.CASES
LABELS = slm.LABELS


def drawn_member_items(page: Path, model: dict[str, Any]) -> dict[str, list[str]]:
    """Per blocked line with a member reason, the member reason items the page draws, as text, in order."""
    lines = []
    for section in model.get("sections") or []:
        resolved = section.get("resolved") or {}
        if any(isinstance(r, dict) and r.get("memberLabel") for r in resolved.get("reasons") or []):
            lines.append(json.dumps({"key": slm.p0.short((section.get("field") or {}).get("id")),
                                     "model": {**model, "sections": [section]}}))
    if not lines:
        return {}
    env = os.environ.copy()
    env["PPW_CHECK_DETAIL"] = "1"
    proc = subprocess.run(["node", str(slm.CHECKER), str(page)], input="\n".join(lines) + "\n",
                          text=True, capture_output=True, timeout=300, check=True, env=env)
    drawn: dict[str, list[str]] = {}
    for key, result in json.loads(proc.stdout).items():
        assert not result.get("section_errors"), (key, result.get("section_errors"))
        texts = [line.strip() for line in str(result.get("first_read_text") or "").split("\n")]
        items: list[str] = []
        for index, text in enumerate(texts):
            if any(text.startswith(label + ":") or text.startswith(label + " (") for label in LABELS.values()):
                # The bold prefix ("<name>:") and the sentence are separate text nodes.
                sentence = texts[index + 1] if index + 1 < len(texts) else ""
                items.append(f"{text} {sentence}".strip())
        drawn[key] = items
    return drawn


def observe(core: Any, case: str, page: Path = PAGE) -> dict[str, Any]:
    """same-label-members' observation, plus the member items the page draws."""
    drawn: dict[str, list[str]] = {}
    original = slm.dom_member_items

    def capture(page_path: Path, model: dict[str, Any]) -> dict[str, int]:
        drawn.update(drawn_member_items(page_path, model))
        return {line: len(items) for line, items in drawn.items()}

    slm.dom_member_items = capture
    try:
        found = dict(slm.observe(core, case, page=page))
    finally:
        slm.dom_member_items = original
    if "dom" in found:
        found["drawn"] = drawn
    return found


def _worker(args: tuple[Any, list[str]]) -> list[tuple[str, dict[str, Any]]]:
    core, cases = args
    out = []
    for case in cases:
        try:
            out.append((case, observe(core, case)))
        except Exception as exc:  # noqa: BLE001 - a rejected list is a result
            out.append((case, {"error": type(exc).__name__, "message": slm.h.scrub(str(exc))[:500]}))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", default="v108")
    parser.add_argument("--core-json")
    parser.add_argument("--only", action="append")
    parser.add_argument("--workers", type=int, default=max(1, min(9, (os.cpu_count() or 2) - 1)))
    parser.add_argument("--out")
    args = parser.parse_args()
    core = slm.p0.core_from(args)
    todo = list(args.only) if args.only else list(CASES)
    started = time.monotonic()
    workers = min(args.workers, len(todo))
    if workers <= 1:
        found = dict(_worker((core, todo)))
    else:
        with multiprocessing.get_context("spawn").Pool(workers) as pool:
            parts = pool.map(_worker, [(core, todo[i::workers]) for i in range(workers)])
        found = dict(pair for part in parts for pair in part)
    body = {"core": {"package": core.version, "registry": core.registry, "release": core.release_version},
            "wall_time_s": round(time.monotonic() - started, 1),
            "runs": {c: found[c] for c in todo}}
    text = json.dumps(body, indent=1, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    print(text[:4000])


if __name__ == "__main__":
    main()
