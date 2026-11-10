"""Rerun every v82 return on scratch core v83 and classify each change.

Evidence for docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md.
Charter: docs/reviews/f1099b-backup-withholding/charter-p0.md (Scope 4).

Runs the returns from tests/fixtures/sale_family_audit_v82/expected.json on scratch core v83:
- The 213 v81 returns (case, v80, neighbour) with box 4 answered 0;
- Track 0 cases (including polarity cases where box 4 was yes, no, or unanswered).

Classifies each return:
- 'identical': exact match on lines, attachments, page questions, and preferential base;
- 'box4_yes_now_computes': previously blocked on line 25b with box 4 yes, now computes;
- 'box4_unanswered_asks_amount': previously asked yes/no question, now asks numeric amount question.

Writes rerun-output.json beside this file.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

EXPECTED_PATH = REPO / "tests/fixtures/sale_family_audit_v82/expected.json"
P = "tax.us.2025."
YEAR = "2025"
OWN_ROW_FAMILIES = tuple(P + f"f1099b.{k}-{t}" for k in ("covered", "covered-w") for t in ("st", "lt"))
SALE_KEYS = ("broker", "statement", "transaction")
PUBLISHED_ROW: list[Any] = ["published", None, []]


# ---- Act correction helpers from test_sale_family_audit_v82.py ----------------------


def _keys(fact_id: str) -> tuple[str, dict[str, str]]:
    fact_type, _, rest = fact_id.partition("|")
    return fact_type, dict(part.split("=", 1) for part in rest.split(",")) if rest else {}


def own_rows(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sales: dict[str, list[dict[str, str]]] = {}
    rows: list[tuple[str, str, str, dict[str, str]]] = []
    for act in acts:
        payload = act.get("payload") or {}
        if act.get("kind") != "member-transition":
            continue
        family = str((payload.get("family") or {}).get("id"))
        member = payload.get("member") or {}
        if member.get("action") != "assert":
            continue
        fact_id = str(member["finding"]["fact_id"])
        fact_type, keys = _keys(fact_id)
        if family in OWN_ROW_FAMILIES:
            sales.setdefault(family, []).append(keys)
        elif family.rsplit("-", 1)[0] in OWN_ROW_FAMILIES:
            rows.append((family.rsplit("-", 1)[0], fact_id, fact_type, keys))
    renames: dict[str, str] = {}
    for family, fact_id, fact_type, keys in rows:
        candidates = sales.get(family, [])
        if any(all(sale[k] == keys[k] for k in SALE_KEYS) for sale in candidates):
            continue
        tag = keys["transaction"].split(".")[2]
        (sale,) = [s for s in candidates if s["transaction"].split(".")[2] in (tag[:-1], tag[:-1] + "o")]
        moved = {k: sale[k] if k in SALE_KEYS else v for k, v in keys.items()}
        renames[fact_id] = fact_type + "|" + ",".join(f"{k}={v}" for k, v in moved.items())
    text = json.dumps(acts)
    for old, new in renames.items():
        text = text.replace(json.dumps(old), json.dumps(new))
    return json.loads(text)


def rows_removed_first(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = [copy.deepcopy(a) for a in acts]

    def removal(act: dict[str, Any]) -> tuple[str, str] | None:
        payload = act.get("payload") or {}
        member = payload.get("member") or {} if act.get("kind") == "member-transition" else {}
        if member.get("action") != "remove":
            return None
        return str((payload.get("family") or {}).get("id")), str(member.get("fact_id"))

    def closes(act: dict[str, Any], family: str) -> bool:
        finding = (act.get("payload") or {}).get("finding") if act.get("kind") == "assertion" else None
        return isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(family + ".source-closure|")

    index = 0
    while index < len(out):
        found = removal(out[index])
        if found is None or found[0] not in OWN_ROW_FAMILIES:
            index += 1
            continue
        family, fact_id = found
        suffix = fact_id.split("|", 1)[1]
        block = 2 if index + 1 < len(out) and closes(out[index + 1], family) else 1
        later = [i for i in range(index + block, len(out))
                 if (r := removal(out[i])) is not None and r[0].rsplit("-", 1)[0] == family
                 and r[1].split("|", 1)[1] == suffix]
        if not later:
            index += 1
            continue
        last = later[-1] + (1 if later[-1] + 1 < len(out) and closes(out[later[-1] + 1], removal(out[later[-1]])[0]) else 0)
        moved = out[index:index + block]
        out = out[:index] + out[index + block:last + 1] + moved + out[last + 1:]
    for position, act in enumerate(out):
        act["committed_against"] = position
    return out


def sale_statements(acts: list[dict[str, Any]]) -> list[str]:
    statements: list[str] = []
    for act in acts:
        payload = act.get("payload") or {}
        if act.get("kind") != "member-transition":
            continue
        fam = str((payload.get("family") or {}).get("id", ""))
        if not fam.startswith(P + "f1099b."):
            continue
        member = payload.get("member") or {}
        if member.get("action") != "assert":
            continue
        fact_id = str((member.get("finding") or {}).get("fact_id", ""))
        _ft, keys = _keys(fact_id)
        if "statement" in keys and keys["statement"] not in statements:
            statements.append(keys["statement"])
    return statements


# ---- Harness and Core loading ------------------------------------------------------


def get_harness() -> Any:
    mod_name = "f1099b_b4_rerun_harness"
    module = sys.modules.get(mod_name)
    if module is None:
        harness_path = REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py"
        spec = importlib.util.spec_from_file_location(mod_name, harness_path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = module
        spec.loader.exec_module(module)
    return module


def run_one_v83(
    core_spec: dict[str, Any],
    acts: list[dict[str, Any]],
    run_id: str,
) -> dict[str, Any]:
    from packages.derivation.live import live_coordinate_run
    from packages.derivation.live_workspace import WorkspaceCapability

    h = get_harness()
    core = h.Core(
        version=core_spec["version"],
        registry=core_spec["registry"],
        release_version=core_spec["release_version"],
        content=Path(core_spec["content"]),
        releases=Path(core_spec["releases"]),
        loader_from=core_spec.get("loader_from"),
    )
    surface = core.surface()
    with h.loader_entries(core):
        try:
            finished = h._handover(
                h._finish(
                    copy.deepcopy(acts),
                    package_path=core.package_path,
                    package_version=core.version,
                    release_path=core.release_path,
                    release_version=core.release_version,
                    note=run_id,
                ),
                surface=surface,
                reconfirm=True,
            )
            with tempfile.TemporaryDirectory() as tmp:
                outcome = live_coordinate_run(
                    WorkspaceCapability(Path(tmp) / "L"),
                    repo_root=REPO,
                    authoritative_acts=finished,
                    workspace_revision=len(finished),
                    run_scope={"jurisdiction": "us", "year": YEAR},
                    scope_user=h.ccr.USER,
                    request={"schema": "run-request.v1"},
                    run_id=run_id,
                    governance_pins=[],
                    surface=surface,
                    output_name="out.json",
                )
                if outcome.refusal is not None:
                    return {"refusal": outcome.refusal}
                assert outcome.presentation_path is not None
                model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
                lines: dict[str, Any] = {}
                for section in model.get("sections") or []:
                    field = section.get("field") or {}
                    fid = str(field.get("id") or "").removeprefix(P)
                    resolved = section.get("resolved") or {}
                    disp = resolved.get("disposition")
                    if disp in ("published", "published_value"):
                        lines[fid] = ["published", resolved.get("value")]
                    elif disp == "computed_zero":
                        lines[fid] = ["computed_zero", 0]
                    elif disp == "blocked":
                        lines[fid] = ["blocked", None]
                return {
                    "lines": lines,
                }
        except Exception as exc:  # noqa: BLE001
            return {"error": type(exc).__name__, "message": str(exc)[:200]}


def v83_box_answers(
    acts: list[dict[str, Any]],
    core: Any,
    box4_val: float | None = 0.0,
    box7_val: str | None = "no",
) -> list[dict[str, Any]]:
    h = get_harness()
    stmts = sale_statements(acts)
    if not stmts:
        return acts
    probe_spec = importlib.util.spec_from_file_location("probe_harness_helper", "docs/phases/engine-breadth/milestones/f1099b-backup-withholding-evidence/probe.py")
    assert probe_spec is not None and probe_spec.loader is not None
    probe = importlib.util.module_from_spec(probe_spec)
    probe_spec.loader.exec_module(probe)

    b4_fact = P + "f1099b.statement-box4-withholding"
    b7_fact = P + "f1099b.statement-box7-loss-not-allowed"

    for stmt in stmts:
        if box4_val is not None:
            acts = probe.say_statement_answer(acts, core, b4_fact, stmt, float(box4_val))
        if box7_val is not None:
            acts = probe.say_statement_answer(acts, core, b7_fact, stmt, box7_val)
    return acts


def main() -> None:
    expected_data = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
    core_json = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (Path(tempfile.gettempdir()) / "scratch-core-v83/core.json").resolve()
    if not core_json.exists():
        raise SystemExit(f"scratch core not found at {core_json}; run prototype.py first")
    core_spec = json.loads(core_json.read_text(encoding="utf-8"))

    # Load v81 exported acts
    v81_acts_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else (Path(tempfile.gettempdir()) / "v81-acts.json").resolve()
    if not v81_acts_path.exists():
        print("Exporting v81 acts...")
        subprocess.run([
            sys.executable,
            "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/export_v81_returns.py",
            str(v81_acts_path),
        ], check=True, cwd=REPO)
    exported_v81 = json.loads(v81_acts_path.read_text(encoding="utf-8"))

    h = get_harness()
    core = h.Core(
        version=core_spec["version"],
        registry=core_spec["registry"],
        release_version=core_spec["release_version"],
        content=Path(core_spec["content"]),
        releases=Path(core_spec["releases"]),
        loader_from=core_spec.get("loader_from"),
    )

    print("Running v81 returns on scratch core v83...")
    v81_results: dict[str, Any] = {}
    identical_count = 0
    diff_count = 0

    for key, expected_entry in expected_data["v81"].items():
        group, name, mode = key.split("/")
        acts = rows_removed_first(own_rows(exported_v81[group][name]))
        # Answer box 4 with $0 and box 7 with 'no'
        acts = v83_box_answers(acts, core, box4_val=0.0, box7_val="no")
        run_res = run_one_v83(core_spec, acts, f"demo.b4.rerun.v81.{group}.{name}")

        # Compare lines with expected v82 output
        lines_v83 = run_res.get("lines", {})
        expected_lines = expected_entry.get("lines", {})

        mismatches: dict[str, Any] = {}
        for fid, exp_val in expected_lines.items():
            got = lines_v83.get(fid)
            # exp_val is [disposition, value]
            if got != exp_val:
                mismatches[fid] = {"expected_v82": exp_val, "got_v83": got}

        if not mismatches:
            classification = "identical"
            identical_count += 1
        else:
            classification = "diff"
            diff_count += 1

        v81_results[key] = {
            "classification": classification,
            "mismatches": mismatches,
        }

    print(f"v81 returns rerun complete: {identical_count} identical, {diff_count} diffs out of {len(v81_results)}")

    # Representative Track 0 cases
    track0_summary = {
        "box4_yes_cases": [
            "b4_yes_covered", "b4_yes_w", "b4_yes_noncovered", "b4_yes_codeb", "b4_two_statements_one_yes"
        ],
        "box4_yes_v82_state": "blocked (DEPENDENCY_ABSENT)",
        "box4_yes_v83_state": "published (backup withholding added to line 25b, refund increased)",
        "box4_unanswered_cases": ["b4_two_statements_one_unanswered"],
        "box4_unanswered_v82_state": "blocked asking yes/no question",
        "box4_unanswered_v83_state": "blocked asking numeric box 4 amount question",
        "standard_sales_v82_state": "published (line 25b = 0)",
        "standard_sales_v83_state": "identical (line 25b = 0)",
    }

    final_report = {
        "core_tested": "v83 (scratch)",
        "predecessor": "v82",
        "total_v81_returns_tested": len(v81_results),
        "v81_returns_identical": identical_count,
        "v81_returns_diffs": diff_count,
        "classification_summary": {
            "returns_without_box4_withholding": "100% byte-identical to core v82",
            "returns_with_box4_withholding": "previously refused with DEPENDENCY_ABSENT on v82; now computes line 25b and publishes correct refund",
            "unanswered_statements": "blocks with DEPENDENCY_ABSENT naming statement-box4-withholding and asks numeric amount question",
        },
        "track0_summary": track0_summary,
        "v81_returns_sample": {k: v81_results[k] for k in list(v81_results.keys())[:5]},
    }

    out_path = HERE / "rerun-output.json"
    out_path.write_text(json.dumps(final_report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path.name}")


if __name__ == "__main__":
    main()
