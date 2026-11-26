"""P0 probes for line 12d's boxes on published v89 and scratch v90.

Evidence for docs/phases/engine-breadth/milestones/line12d-boxes.md.
Charter: docs/reviews/line12d-boxes/charter-p0.md.

Every case is one live_coordinate_run of synthetic demo.* findings on the
question-wording harness's wage return (wages 50,000, 4,500 withheld, every
other question answered, no-sale box 4 answered no). Box states are read
from the presentation model against the 2025 instructions in law.json.

    python3 probe.py <scratch>/core.json
"""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def _sibling(name: str, file: str) -> Any:
    """A sibling evidence module, loaded by path under a name no other milestone uses."""
    if name in sys.modules:
        return sys.modules[name]
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


proto = _sibling("l12d_evidence_prototype", "prototype.py")

QW = REPO / "docs/phases/engine-breadth/milestones/question-wording-evidence"
P = "tax.us.2025."
Acts = list[dict[str, Any]]

AGE, BLIND, S_AGE, S_BLIND = (
    P + "taxpayer-over-65",
    P + "taxpayer-blind",
    P + "spouse-over-65",
    P + "spouse-blind",
)
COND = P + "standard-deduction.spouse-separate-condition"
STATUS = P + "filing-status"
DEPENDENT = P + "standard-deduction.can-be-claimed-as-dependent"
SSN = P + "senior-deduction.taxpayer-valid-ssn"
MFJ, MFS, HOH, QSS = (
    "married_filing_jointly",
    "married_filing_separately",
    "head_of_household",
    "qualifying_surviving_spouse",
)
BOX_KEYS = tuple(box["key"] for box in proto.BOXES)


def _module(name: str, path: Path) -> Any:
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def qw_probe() -> Any:
    return _module("l12d_p0_qw_probe", QW / "probe.py")


def harness() -> Any:
    return qw_probe().load_harness()


def core(path: Path | None) -> Any:
    h = harness()
    if path is None:
        return h.Core("v89", "v87", "v87")
    body = json.loads(path.read_text(encoding="utf-8"))
    return h.Core(
        body["version"],
        body["registry"],
        body["release_version"],
        content=Path(body["content"]),
        releases=Path(body["releases"]),
        loader_from=body.get("loader_from"),
    )


def scrub(text: str) -> str:
    text = text.replace(str(REPO), ".")
    return re.sub(r"/(?:Users|private|tmp|var|opt)/\S+", "<path>", text)


def boxes_from_model(model: dict[str, Any]) -> dict[str, str]:
    """checked / not_checked / hidden / blocked, one state per line 12d box."""
    by_slug: dict[str, dict[str, str]] = {}
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        ident = str(field.get("id") or "").removeprefix(P)
        if not ident.startswith("form1040.line-12d-"):
            continue
        rest = ident.removeprefix("form1040.line-12d-")
        not_checked = rest.endswith("-not-checked")
        slug = rest.removesuffix("-not-checked")
        disposition = str((section.get("resolved") or {}).get("disposition") or "")
        render = str(
            ((field.get("dispositions") or {}).get("published_value") or {}).get("render") or ""
        )
        by_slug.setdefault(slug, {})
        if disposition == "published_categorical":
            by_slug[slug]["checked" if not not_checked else "not_checked"] = render
        elif disposition == "blocked":
            by_slug[slug]["blocked"] = "blocked"
        elif disposition == "guard_inapplicable":
            by_slug[slug]["hidden"] = "hidden"
        else:
            by_slug[slug]["other"] = disposition
    out: dict[str, str] = {}
    for box in proto.BOXES:
        row = by_slug.get(box["slug"], {})
        if row.get("checked") == "checked":
            out[box["key"]] = "checked"
        elif row.get("not_checked") == "not_checked":
            out[box["key"]] = "not_checked"
        elif "blocked" in row:
            out[box["key"]] = "blocked"
        elif row.get("hidden") == "hidden" and len(row) == 1:
            out[box["key"]] = "hidden"
        elif not row:
            out[box["key"]] = "absent"
        else:
            out[box["key"]] = "conflict:" + ",".join(sorted(row))
    return out


def shown(states: dict[str, str]) -> dict[str, str]:
    return {key: state for key, state in states.items() if state in {"checked", "not_checked"}}


def expected_boxes(answers: dict[str, Any], status: str) -> dict[str, str]:
    """Where the 2025 instructions check each box, from the recorded answers."""
    you = {
        "you_age": "checked" if answers.get(AGE) else "not_checked",
        "you_blind": "checked" if answers.get(BLIND) else "not_checked",
    }
    spouse_shown = status == MFJ or (
        status == MFS and answers.get(COND) is True
    )
    if not spouse_shown:
        spouse = {"spouse_age": "hidden", "spouse_blind": "hidden"}
    else:
        spouse = {
            "spouse_age": "checked" if answers.get(S_AGE) else "not_checked",
            "spouse_blind": "checked" if answers.get(S_BLIND) else "not_checked",
        }
    return {**you, **spouse}


def execute(c: Any, acts: Acts, run_id: str) -> dict[str, Any]:
    h = harness()
    surface = c.surface()
    with h.loader_entries(c):
        try:
            finished = h._handover(
                h._finish(
                    acts,
                    package_path=c.package_path,
                    package_version=c.version,
                    release_path=c.release_path,
                    release_version=c.release_version,
                    note=run_id,
                ),
                surface=surface,
                reconfirm=True,
            )
            with tempfile.TemporaryDirectory() as tmp:
                outcome = h.live_coordinate_run(
                    h.WorkspaceCapability(Path(tmp) / "L"),
                    repo_root=REPO,
                    authoritative_acts=finished,
                    workspace_revision=len(finished),
                    run_scope={"jurisdiction": "us", "year": h.YEAR},
                    scope_user=h.ccr.USER,
                    request={"schema": "run-request.v1"},
                    run_id=run_id,
                    governance_pins=[],
                    surface=surface,
                    output_name="out.json",
                )
                if outcome.refusal is not None:
                    return {
                        "outcome": "refused",
                        "reason": outcome.refusal.reason,
                        "detail": scrub(str(outcome.refusal.detail))[:300],
                    }
                model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
                report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
                states = boxes_from_model(model)
                line12e = None
                for section in model.get("sections") or []:
                    ident = str((section.get("field") or {}).get("id") or "").removeprefix(P)
                    if ident != "form1040.line-12e":
                        continue
                    resolved = section.get("resolved") or {}
                    value = resolved.get("value")
                    line12e = (
                        str(resolved.get("disposition"))
                        if value is None
                        else int(value) if isinstance(value, float) and value.is_integer() else value
                    )
                return {
                    "outcome": "success",
                    "stop": report.get("stop_reason"),
                    "boxes": states,
                    "boxes_shown": shown(states),
                    "form1040.line-12e": line12e,
                }
        except Exception as exc:  # noqa: BLE001 - a rejected act list is a result
            return {
                "outcome": "error",
                "error": type(exc).__name__,
                "message": scrub(str(exc))[:300],
            }


def base(status: str = "single") -> Acts:
    p, h = qw_probe(), harness()
    acts = h.say(p.complete(h), P + "f1099b.no-sale-box4-present", "no", "box4-present")
    if status != "single":
        acts = h.say(acts, STATUS, status, "fs")
    return acts


def answer(acts: Acts, answers: dict[str, Any]) -> Acts:
    h = harness()
    acts = copy.deepcopy(acts)
    # The condition fact lives only in vocabulary v4. The wage return has
    # already adopted an earlier vocabulary that shares other fact ids, so
    # harness.say skips v4. Adopt v4 before asserting that fact (same order
    # age-blindness-asked-evidence/probe.py readopt uses).
    if COND in answers:
        body = json.loads(
            (proto.CONTENT / "core_calculations.bundle.v4.json").read_text(encoding="utf-8")
        )
        h._add(acts, "bundle-adoption", {"bundle": body})
        acts = h.renumber(acts)
    for fact, value in answers.items():
        acts = h.say(acts, fact, value, fact.removeprefix(P).replace(".", "-"))
    return acts


CASES: list[dict[str, Any]] = [
    {
        "id": "single-age-yes-blind-no",
        "says": "Single; born before January 2, 1961; not blind.",
        "status": "single",
        "extra": {SSN: "yes"},
        "truthful": {AGE: True, BLIND: False},
        "hand_12e": 17750,
    },
    {
        "id": "single-both-no",
        "says": "Single; not 65; not blind.",
        "status": "single",
        "extra": {},
        "truthful": {AGE: False, BLIND: False},
        "hand_12e": 15750,
    },
    {
        "id": "joint-spouse-age-yes",
        "says": "Joint; taxpayer not 65; spouse born before January 2, 1961; neither blind.",
        "status": MFJ,
        "extra": {},
        "truthful": {AGE: False, BLIND: False, S_AGE: True, S_BLIND: False},
        "hand_12e": 33100,
    },
    {
        "id": "joint-both-blind",
        "says": "Joint; both blind; neither 65.",
        "status": MFJ,
        "extra": {},
        "truthful": {AGE: False, BLIND: True, S_AGE: False, S_BLIND: True},
        "hand_12e": 34700,
    },
    {
        "id": "separate-condition-yes",
        "says": "Separate; spouse 65; condition yes (no income, not filing, not claimable).",
        "status": MFS,
        "extra": {},
        "truthful": {AGE: False, BLIND: False, S_AGE: True, S_BLIND: False, COND: True},
        "hand_12e": 17350,
    },
    {
        "id": "separate-condition-no",
        "says": "Separate; spouse 65 recorded; condition no. Spouse boxes are not shown.",
        "status": MFS,
        "extra": {},
        "truthful": {AGE: False, BLIND: False, S_AGE: True, S_BLIND: False, COND: False},
        "hand_12e": 15750,
    },
    {
        "id": "head-of-household",
        "says": "Head of household; not 65; not blind. Spouse boxes are not shown.",
        "status": HOH,
        "extra": {},
        "truthful": {AGE: False, BLIND: False},
        "hand_12e": 23625,
    },
    {
        "id": "qualifying-surviving-spouse",
        "says": "Qualifying surviving spouse; not 65; not blind. Spouse boxes are not shown.",
        "status": QSS,
        "extra": {},
        "truthful": {AGE: False, BLIND: False},
        "hand_12e": 31500,
    },
    {
        "id": "dependent-65",
        "says": "Single dependent filer; born before January 2, 1961; not blind.",
        "status": "single",
        "extra": {DEPENDENT: "yes", SSN: "yes"},
        "truthful": {AGE: True, BLIND: False},
        "hand_12e": 17750,
    },
]


def run_all(c89: Any, c90: Any) -> dict[str, Any]:
    cores = {"v89": c89, "v90": c90}
    rows = []
    for case in CASES:
        acts0 = answer(base(case["status"]), case["extra"])
        expected = expected_boxes(case["truthful"], case["status"])
        measured: dict[str, Any] = {}
        for variant, acts in (
            ("unanswered", acts0),
            ("truthful", answer(acts0, case["truthful"])),
        ):
            for name, c in cores.items():
                run_id = f"demo.l12d.p0.{name}.{case['id']}.{variant}"
                result = execute(c, acts, run_id)
                measured[f"{variant}@{name}"] = result
                print(
                    case["id"],
                    variant,
                    name,
                    result.get("boxes") or result.get("error") or result.get("reason"),
                    flush=True,
                )
        rows.append({
            "id": case["id"],
            "says": case["says"],
            "status": case["status"],
            "truthful": {k.removeprefix(P): v for k, v in case["truthful"].items()},
            "boxes_expected": expected,
            "hand_12e": case["hand_12e"],
            "measured": measured,
        })
    return {"cases": rows}


def judge(payload: dict[str, Any]) -> None:
    for row in payload["cases"]:
        verdicts: dict[str, Any] = {}
        expected = row["boxes_expected"]
        for key, result in row["measured"].items():
            variant, name = key.split("@")
            got = result.get("boxes") or {}
            if variant == "truthful" and name == "v90":
                pass_boxes = got == expected
            elif variant == "truthful" and name == "v89":
                pass_boxes = all(got.get(box) == "absent" for box in BOX_KEYS)
            elif variant == "unanswered" and name == "v90":
                you = got.get("you_age") == "blocked" and got.get("you_blind") == "blocked"
                if row["status"] in {MFJ, MFS}:
                    spouse = got.get("spouse_age") == "blocked" and got.get("spouse_blind") == "blocked"
                else:
                    spouse = got.get("spouse_age") == "hidden" and got.get("spouse_blind") == "hidden"
                pass_boxes = you and spouse
            else:
                pass_boxes = all(got.get(box) == "absent" for box in BOX_KEYS)
            line12e = result.get("form1040.line-12e")
            verdicts[key] = {
                "boxes_shown": shown(got) if result.get("outcome") == "success" else {},
                "boxes_got": got,
                "boxes_expected": expected if variant == "truthful" and name == "v90" else (
                    {box: "absent" for box in BOX_KEYS} if name == "v89" else got
                ),
                "pass": bool(pass_boxes and result.get("outcome") == "success"),
                "form1040.line-12e": line12e,
                "line12e_matches_hand": line12e == row["hand_12e"] if variant == "truthful" else None,
            }
        row["verdicts"] = verdicts


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: probe.py <scratch>/core.json")
    c90 = core(Path(sys.argv[1]))
    c89 = core(None)
    payload = run_all(c89, c90)
    judge(payload)
    payload = {
        "cores": {"v89": "published", "v90": "prototype.py (scratch)"},
        "law": "docs/phases/engine-breadth/milestones/age-blindness-asked-evidence/law.json",
        "base_return": (
            "question-wording harness wage return: wages 50,000, 4,500 withheld, "
            "every other question answered, no-sale box 4 present=no"
        ),
        **payload,
    }
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"probe output contains {needle}")
    (HERE / "probe-output.json").write_text(text, encoding="utf-8")
    summary = {
        row["id"]: {
            "v90_truthful": row["verdicts"]["truthful@v90"]["pass"],
            "boxes": row["verdicts"]["truthful@v90"]["boxes_shown"],
            "line12e": row["verdicts"]["truthful@v90"]["form1040.line-12e"],
        }
        for row in payload["cases"]
    }
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
