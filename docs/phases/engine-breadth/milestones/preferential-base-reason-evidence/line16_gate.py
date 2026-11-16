"""Show line 16 v9 against v8 on the ten blocked-names-question cases.

The line 16 case is ``exception1_personal_loss_8949``. v9 may be published
only when every case has the same missing names, questions, and values.

    python3 line16_gate.py <line16-only-core.json>
"""

from __future__ import annotations

import json
import multiprocessing
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
BNQ = REPO / "docs/phases/engine-breadth/milestones/blocked-names-question-evidence"
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tests import evidence_loader  # noqa: E402

OWNER = "pbr_line16_gate"
LINE16_CASE = "exception1_personal_loss_8949"


def _ten() -> list[tuple[str, Any]]:
    evidence_loader.activate(OWNER)
    evidence_loader.load(BNQ / "common.py", "common")
    probe = evidence_loader.load(BNQ / "probe.py", "probe")
    return [
        (case_id, build)
        for case_id, (group, build, _note) in probe.CASES.items()
        if group != "internal-subtotal"
    ]


def _view(result: dict[str, Any]) -> dict[str, Any]:
    blocked = result.get("blocked") or {}
    line16 = blocked.get("form1040.line-16") or {}
    return {
        "outcome": result.get("outcome"),
        "error": result.get("message"),
        "lines": result.get("lines"),
        "questions": result.get("questions"),
        "line16_missing": line16.get("missing"),
        "line16_questions": line16.get("questions"),
        "line16_value": (result.get("lines") or {}).get("form1040.line-16"),
        "blocked": {
            field: {"missing": row.get("missing"), "questions": row.get("questions")}
            for field, row in sorted(blocked.items())
        },
    }


def _worker(payload: tuple[str, list[str]]) -> list[dict[str, Any]]:
    core_json, shard = payload
    evidence_loader.activate(OWNER)
    try:
        common = evidence_loader.load(BNQ / "common.py", "common")
        probe = evidence_loader.load(BNQ / "probe.py", "probe")
        builders = {
            case_id: build
            for case_id, (group, build, _note) in probe.CASES.items()
            if group != "internal-subtotal"
        }
        published = common.harness().Core("v90", "v88", "v88")
        scratch = common.scratch(Path(core_json))
        rows = []
        for case_id in shard:
            acts = builders[case_id]()
            v8 = _view(common.run(published, acts, "demo.pbr.line16.v8." + case_id))
            v9 = _view(common.run(scratch, acts, "demo.pbr.line16.v9." + case_id))
            rows.append({
                "id": case_id,
                "line16_case": case_id == LINE16_CASE,
                "same": v8 == v9,
                "v8": v8,
                "v9": v9,
            })
        return rows
    finally:
        evidence_loader.finish(OWNER)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: line16_gate.py <line16-only-core.json>")
    core_json = str(Path(sys.argv[1]).resolve())
    case_ids = [case_id for case_id, _build in _ten()]
    evidence_loader.finish_all()
    workers = max(1, (os_cpu()) - 1)
    shards = [(core_json, case_ids[index::workers]) for index in range(workers) if case_ids[index::workers]]
    found: list[dict[str, Any]] = []
    context = multiprocessing.get_context("spawn")
    with context.Pool(len(shards)) as pool:
        for part in pool.map(_worker, shards):
            found.extend(part)
    found.sort(key=lambda row: row["id"])
    differs = [row["id"] for row in found if not row["same"]]
    core_body = json.loads(Path(core_json).read_text(encoding="utf-8"))
    package = json.loads(
        (Path(core_body["content"]) / "package.core-calculations.v91.json").read_text(encoding="utf-8")
    )
    members = {
        row["id"].removeprefix("tax.us.2025.rule."): row["version"]
        for row in package["members"]
        if row["id"].endswith("form1040-line16") or row["id"].endswith("selected-preferential-base")
    }
    payload = {
        "cases": len(found),
        "line16_case": LINE16_CASE,
        "members": members,
        "same": differs == [],
        "differ_ids": differs,
        "rows": found,
    }
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit("line16 gate contains a local path")
    (HERE / "line16-gate.json").write_text(text, encoding="utf-8")
    print(json.dumps({"cases": len(found), "same": not differs, "differ_ids": differs}, indent=2))
    if differs:
        raise SystemExit("line 16 v9 changes a blocked-names-question case")


def os_cpu() -> int:
    import os
    return os.cpu_count() or 2


if __name__ == "__main__":
    main()
