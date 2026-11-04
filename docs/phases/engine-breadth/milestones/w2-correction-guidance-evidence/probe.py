"""P0 evidence probe for the v6/v70 synthetic W-2 entry loop.

The probe drives the entry HTTP route, which calls the real contribution
recorder and then live_coordinate_run. It records only bounded summaries of
the synthetic act log, durable run output, and presentation model.
"""

from __future__ import annotations

import copy
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[5]
EVIDENCE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))

from packages.derivation.entry_loop import (
    ENTRY_CORE_PROFILES,
    SyntheticW2EntryRuntime,
    load_seed_acts,
)
from packages.derivation.entry_loop import EntryLoopServer
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.kernel.act_log import ActLog


OMITTED_DEPENDENT_ANSWER = (
    "tax.us.2025.standard-deduction.can-be-claimed-as-dependent|tax-year=2025"
)


def _json_request(
    url: str, *, method: str = "GET", payload: dict[str, Any] | None = None
) -> tuple[int, dict[str, Any]]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Accept": "application/json",
            **({"Content-Type": "application/json"} if body is not None else {}),
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            return response.status, result
    except urllib.error.HTTPError as exc:
        try:
            result = json.loads(exc.read().decode("utf-8"))
        finally:
            exc.close()
        if not isinstance(result, dict):
            raise RuntimeError("entry route returned a non-object error") from None
        return exc.code, result


def _event(snapshot: dict[str, Any], amount: object) -> dict[str, Any]:
    event = copy.deepcopy(snapshot["contribution"])
    event["payload"]["contribution"]["content"]["w2_box1"] = amount
    return event


def _line_snapshot(
    snapshot: dict[str, Any], lines: tuple[str, ...]
) -> list[dict[str, Any]]:
    return [
        {
            "line": row["line"],
            "group": row["group"],
            "computed": row["computed"],
            "value": row["value"],
            "change": row["change"],
        }
        for row in snapshot["lines"]
        if row["line"] in lines
    ]


def _presentation_line(model: dict[str, Any], line: str) -> dict[str, Any]:
    rows = [
        section
        for section in model.get("sections", [])
        if isinstance(section, dict)
        and section.get("field", {}).get("line") == line
    ]
    if len(rows) != 1:
        raise RuntimeError(f"expected one presentation section for line {line}")
    section = rows[0]
    resolved = section.get("resolved", {})
    return {
        "line": line,
        "disposition": resolved.get("disposition"),
        "value": resolved.get("value"),
        "active_codes": resolved.get("activeCodes", []),
        "reason_sentences": [
            reason["sentence"]
            for reason in resolved.get("reasons", [])
            if isinstance(reason, dict) and isinstance(reason.get("sentence"), str)
        ],
    }


def _saved_run(
    workspace: Path, revision: int, lines: tuple[str, ...]
) -> dict[str, Any]:
    report_path = workspace / "outputs" / f"entry-state-{revision}.json"
    presentation_path = (
        workspace
        / "outputs"
        / f"entry-state-{revision}.presentation.json"
    )
    if not report_path.is_file() or not presentation_path.is_file():
        raise RuntimeError("live coordinator did not leave both saved outputs")
    report = json.loads(report_path.read_text("utf-8"))
    model = json.loads(presentation_path.read_text("utf-8"))
    presentation_authorization = model.get("authorization")
    if not isinstance(presentation_authorization, dict):
        presentation_authorization = {}
    blocked_rows = [
        {
            "artifact_id": row.get("artifact_id"),
            "code": row.get("code"),
            "missing": row.get("missing", []),
        }
        for row in report.get("dispositions", [])
        if isinstance(row, dict) and row.get("disposition") == "blocked"
    ]
    return {
        "report_file": report_path.name,
        "presentation_file": presentation_path.name,
        "run_id": report.get("run_id"),
        "stop_reason": report.get("stop_reason"),
        "current": report.get("current"),
        "authorization_status": report.get("authorization_status"),
        "authorization_grant_id": report.get("authorization_grant_id"),
        "blocked_dispositions": blocked_rows[:8],
        "presentation_lines": [
            _presentation_line(model, line) for line in lines
        ],
        "presentation_authorization": {
            key: presentation_authorization.get(key)
            for key in ("status", "grant_id", "admitted")
        },
    }


def _profile_case(
    profile: str,
    *,
    rejected_input: bool = False,
    seed_acts: list[dict[str, Any]] | None = None,
    blocked_lines: tuple[str, ...] = (),
) -> dict[str, Any]:
    with TemporaryDirectory(prefix="demo-w2-guidance-") as temporary:
        root = Path(temporary)
        static_root = root / "static"
        static_root.mkdir()
        (static_root / "index.html").write_text(
            "<!doctype html><title>synthetic probe</title>\n", encoding="utf-8"
        )
        workspace = root / "workspace"
        capability = WorkspaceCapability(workspace)
        runtime = SyntheticW2EntryRuntime(
            capability,
            repo_root=REPO_ROOT,
            seed_profile=profile,
            seed_acts=seed_acts,
        )
        with EntryLoopServer(runtime, static_root) as server:
            api_root = server.url.rsplit("/", 1)[0]
            state_status, initial = _json_request(f"{api_root}/api/state")
            if state_status != 200:
                raise RuntimeError("entry state route did not return 200")

            rejection: dict[str, Any] | None = None
            if rejected_input:
                before = ActLog(
                    capability.location, DerivationSchemas().registry, read_only=True
                ).read()
                status, body = _json_request(
                    f"{api_root}/api/contributions",
                    method="POST",
                    payload=_event(initial, "synthetic-not-an-amount"),
                )
                after = ActLog(
                    capability.location, DerivationSchemas().registry, read_only=True
                ).read()
                rejection = {
                    "http_status": status,
                    "message": body.get("error"),
                    "revision_before": before.revision,
                    "revision_after": after.revision,
                    "act_count_before": len(before.acts),
                    "act_count_after": len(after.acts),
                }

            first_status, entered = _json_request(
                f"{api_root}/api/contributions",
                method="POST",
                payload=_event(initial, 90000),
            )
            if first_status != 200:
                raise RuntimeError("synthetic first entry was not accepted")
            correction_status, corrected = _json_request(
                f"{api_root}/api/contributions",
                method="POST",
                payload=_event(entered, 91000),
            )
            if correction_status != 200:
                raise RuntimeError("synthetic correction was not accepted")

        recovered = ActLog(
            capability.location, DerivationSchemas().registry, read_only=True
        ).read()
        w2_contribution_values = [
            act["payload"]["contribution"]["content"]["w2_box1"]
            for act in recovered.acts
            if act.get("kind") == "contribution"
            and isinstance(act.get("payload"), dict)
            and isinstance(act["payload"].get("contribution"), dict)
            and isinstance(
                act["payload"]["contribution"].get("content"), dict
            )
            and "w2_box1" in act["payload"]["contribution"]["content"]
        ]
        core = ENTRY_CORE_PROFILES[
            ("tax.us.2025.package.core-calculations", profile)
        ]
        all_lines = tuple(field.line for field in core.fields)
        latest_run = _saved_run(workspace, corrected["revision"], blocked_lines)
        return {
            "profile": profile,
            "initial": {
                "revision": initial["revision"],
                "missing_ids": [item["id"] for item in initial["missing"]],
                "complete": initial["complete"],
            },
            "rejected_input": rejection,
            "first_entry": {
                "http_status": first_status,
                "accepted": entered["accepted"],
                "last_action": entered["last_action"],
                "complete": entered["complete"],
                "answered": entered["answered"],
            },
            "correction": {
                "http_status": correction_status,
                "accepted": corrected["accepted"],
                "last_action": corrected["last_action"],
                "complete": corrected["complete"],
                "missing_ids": [item["id"] for item in corrected["missing"]],
                "answered": corrected["answered"],
                "lines": _line_snapshot(corrected, all_lines),
            },
            "recovered_log": {
                "revision": recovered.revision,
                "w2_box1_contribution_values": w2_contribution_values,
                "last_act_kinds": [act.get("kind") for act in recovered.acts[-5:]],
            },
            "saved_live_run": latest_run,
        }


def _blocked_answer_case() -> tuple[dict[str, Any], str]:
    acts = load_seed_acts(REPO_ROOT, seed_profile="v70")
    original_count = len(acts)
    acts = [
        act
        for act in acts
        if not (
            act.get("kind") == "assertion"
            and act.get("payload", {}).get("finding", {}).get("fact_id")
            == OMITTED_DEPENDENT_ANSWER
        )
    ]
    if len(acts) != original_count - 1:
        raise RuntimeError("expected one synthetic dependent answer in the seed")
    for revision, act in enumerate(acts):
        act["committed_against"] = revision
    return (
        _profile_case(
            "v70",
            seed_acts=acts,
            blocked_lines=("12e", "15", "16"),
        ),
        OMITTED_DEPENDENT_ANSWER,
    )


def main() -> None:
    v70 = _profile_case(
        "v70",
        rejected_input=True,
        blocked_lines=("1a", "15", "16"),
    )
    v6 = _profile_case("v6", blocked_lines=("1a", "11", "16"))
    blocked, omitted_fact = _blocked_answer_case()
    output = {
        "probe": "w2-correction-guidance-p0",
        "synthetic_only": True,
        "route": "EntryLoopServer /api/state and /api/contributions",
        "v70_success_and_rejection": v70,
        "v6_comparison": v6,
        "v70_saved_correction_with_one_answer_omitted": {
            "omitted_fact_id": omitted_fact,
            "case": blocked,
        },
    }
    destination = EVIDENCE_DIR / "probe-output.json"
    destination.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
