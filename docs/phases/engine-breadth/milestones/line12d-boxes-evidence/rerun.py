"""Replay the recorded act lists on published v89 and scratch v90.

Evidence for docs/phases/engine-breadth/milestones/line12d-boxes.md.
Charter: docs/reviews/line12d-boxes/charter-p0.md.

The lists are ``tools.recorded_replay.recorded_lists()``: every distinct act
list earlier milestones replay (the v81, v82, v83, v84 and v85 fixtures).
Each list runs once on each core, in parallel through
``tools.recorded_replay.replay`` (at most 8 workers, resumable part file in a
scratch directory outside the repository).

Answer rule. No recorded list states an age or blindness fact; each relied on
the default false before core v88 made them required. Every list is answered
with ``tests/helpers/current_core_returns.state_taxpayer_facts(acts,
core="v88")``: taxpayer-over-65 and taxpayer-blind false where unstated, the
same acts on both cores. (The Track 0 harness's own call to that helper only
fires for core v88, so it is applied here, explicitly, for v89 and v90.)

Two comparisons per list:

- ``pin``: the recorded-replay pin (``tools.recorded_replay`` / the v83 test's
  ``pin``) classified by ``tools.recorded_replay.classify``. That pin lists
  numeric lines and non-published rule rows, so a new line 12d rule that is
  inapplicable or blocked appears as an added row.
- ``page``: every presentation section's field id, disposition and numeric
  value. v89's sections must reappear unchanged on v90; v90 may add only
  ``form1040.line-12d-*`` sections.

For each list the v90 line 12d box states are read from the dispositions
(checked / not_checked / hidden / blocked), and every published_categorical
section is checked against the saved citation-walk renderer's rule
(packages/presentation/pages/citation-walk.v1.html, ``renderLine``): a field
whose published_value.render is "checked" or "not_checked" draws; any other
render string is a "missing-instruction" alert on the page.

    python3 rerun.py <scratch>/core.json [--workers N]
"""

from __future__ import annotations

import argparse
import json
import signal
import sys
import time
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tests.helpers import current_core_returns as ccr  # noqa: E402
from tools import recorded_replay as rr  # noqa: E402

P = "tax.us.2025."
NEW_FIELD = "form1040.line-12d-"
NEW_RULE = "form1040-line12d-"
SLUGS = ("you-age", "you-blind", "spouse-age", "spouse-blind")
Acts = list[dict[str, Any]]


def answer_implied(acts: Acts) -> Acts:
    """Taxpayer age and blindness false where unstated (tests/helpers, Decision 6)."""
    return ccr.state_taxpayer_facts(acts, core="v88")


@lru_cache(maxsize=None)
def _render(content: str, fid: str) -> str | None:
    path = Path(content) / f"{fid}.form-field.json"
    if not path.is_file():
        return None
    body = json.loads(path.read_text(encoding="utf-8"))
    return str(((body.get("dispositions") or {}).get("published_value") or {}).get("render"))


def _run(core: Any, acts: Acts, run_id: str) -> dict[str, Any]:
    test = rr._get_test()
    track = test.track0()
    with track.h.loader_entries(core):
        return track.run_coordinate(core, acts, run_id)  # type: ignore[no-any-return]


def _page(core: Any, result: dict[str, Any]) -> dict[str, Any]:
    dispositions = result.get("dispositions") or {}
    values = result.get("lines") or {}
    sections = {fid: [disp, values.get(fid)] for fid, disp in sorted(dispositions.items())}
    drawn = {"checked", "not_checked"}
    alerts = sorted(
        fid for fid, disp in dispositions.items()
        if disp == "published_categorical" and _render(str(core.content), fid) not in drawn
    )
    return {"sections": sections, "categorical_alerts": alerts}


def _boxes(sections: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for slug in SLUGS:
        on = (sections.get(NEW_FIELD + slug) or [None])[0]
        off = (sections.get(NEW_FIELD + slug + "-not-checked") or [None])[0]
        if on == "published_categorical" and off == "guard_inapplicable":
            out[slug] = "checked"
        elif off == "published_categorical" and on == "guard_inapplicable":
            out[slug] = "not_checked"
        elif on == off == "guard_inapplicable":
            out[slug] = "hidden"
        elif on == off == "blocked":
            out[slug] = "blocked"
        elif on is None and off is None:
            out[slug] = "absent"
        else:
            out[slug] = f"conflict:{on}/{off}"
    return out


def per_list(key: str, acts: Acts, cores: tuple[Any, Any]) -> dict[str, Any]:
    core_a, core_b = cores
    answered = answer_implied(acts)
    slug = key.replace("/", ".")
    result_a = _run(core_a, answered, "demo.l12d.rr.v89." + slug)
    result_b = _run(core_b, answered, "demo.l12d.rr.v90." + slug)
    test = rr._get_test()
    pin_a, pin_b = test.pin(result_a), test.pin(result_b)
    row = rr.classify(pin_a, pin_b, name_a="v89", name_b="v90")
    page_a, page_b = _page(core_a, result_a), _page(core_b, result_b)
    sec_a, sec_b = page_a["sections"], page_b["sections"]
    row["page_changed"] = sorted(f for f in sec_a if sec_b.get(f) != sec_a[f])
    row["page_added"] = sorted(f for f in sec_b if f not in sec_a)
    row["boxes_v90"] = _boxes(sec_b)
    row["alerts_v89"] = page_a["categorical_alerts"]
    row["alerts_v90"] = page_b["categorical_alerts"]
    row["outcome_v89"] = result_a.get("outcome")
    row["outcome_v90"] = result_b.get("outcome")
    row["line34_v89"] = sec_a.get("form1040.line-34")
    row["line34_v90"] = sec_b.get("form1040.line-34")
    return row


def pin_new_only(row: dict[str, Any]) -> bool:
    """The pins differ only by rows of the new line 12d rules."""
    if row["class"] == "identical":
        return True
    if row["class"] != "numbers_changed" or row.get("sentence_fields"):
        return False
    if row.get("v89_error") or row.get("v90_error") or row.get("lines"):
        return False
    return all(name.startswith("rows.rule." + NEW_RULE) for name in row.get("number_fields") or [])


def final_class(row: dict[str, Any]) -> str:
    page_new_only = not row["page_changed"] and all(
        f.startswith(NEW_FIELD) for f in row["page_added"]
    )
    if row["class"] == "identical" and not row["page_added"] and not row["page_changed"]:
        return "identical"
    if pin_new_only(row) and page_new_only:
        return "numbers_identical_new_fields_only"
    return "changed:" + row["class"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("core", type=Path, help="<scratch>/core.json from prototype.py")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument(
        "--partial", action="store_true",
        help="summarize the lists already in the part file; run nothing",
    )
    args = parser.parse_args()
    if args.workers > 8:
        raise SystemExit("at most 8 workers")
    core_b = rr.resolve_core(args.core)
    core_a = rr.resolve_core("v89")
    lists = rr.recorded_lists()
    part = args.core.resolve().parent / "rerun-part.json"
    # The replay resumes from its part file, so a run may span several
    # foreground invocations; the wall time is their sum, kept in scratch.
    clock = part.with_name("rerun-wall.json")
    spent = json.loads(clock.read_text(encoding="utf-8")) if clock.exists() else []
    if args.partial:
        done = json.loads(part.read_text(encoding="utf-8"))["results"]
        results = {key: done[key] for key in sorted(done)}
    else:
        signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
        started = time.time()
        try:
            results = rr.replay(lists, (core_a, core_b), per_list, workers=args.workers, part=part)
        finally:
            spent.append(round(time.time() - started, 1))
            clock.write_text(json.dumps(spent) + "\n", encoding="utf-8")
    wall = round(sum(spent), 1)

    by_set: dict[str, Counter[str]] = {}
    boxes: Counter[str] = Counter()
    alerts_v89: Counter[str] = Counter()
    alerts_v90: Counter[str] = Counter()
    outcomes: Counter[str] = Counter()
    changes = []
    line34_same = 0
    line34_v89: Counter[str] = Counter()
    for key, row in results.items():
        cls = final_class(row)
        row["final"] = cls
        by_set.setdefault(key.split("/", 1)[0], Counter())[cls] += 1
        boxes[json.dumps(row["boxes_v90"], sort_keys=True)] += 1
        for fid in row["alerts_v89"]:
            alerts_v89[fid] += 1
        for fid in row["alerts_v90"]:
            alerts_v90[fid] += 1
        outcomes[f"{row['outcome_v89']}/{row['outcome_v90']}"] += 1
        line34_same += row["line34_v89"] == row["line34_v90"]
        line34_v89[str((row["line34_v89"] or [None])[0])] += 1
        if cls.startswith("changed"):
            changes.append({"id": key, **{k: v for k, v in row.items() if k != "final"}})

    counts = Counter(row["final"] for row in results.values())
    payload = {
        "cores": {"v89": "published", "v90": "published"},
        "lists": "tools.recorded_replay.recorded_lists(): every distinct recorded act list",
        "answer_rule": (
            "tests/helpers/current_core_returns.state_taxpayer_facts(acts, core='v88') on both "
            "cores: taxpayer-over-65 and taxpayer-blind false where unstated; spouse facts and the "
            "separate-return condition not stated"
        ),
        "classes_defined": {
            "identical": "pins equal and every presentation section equal",
            "numbers_identical_new_fields_only": (
                "pins differ only by rows of the new line 12d rules; every v89 section "
                "reappears unchanged on v90; v90 adds only form1040.line-12d-* sections"
            ),
            "changed:<pin class>": "anything else",
        },
        "status": (
            f"PARTIAL: {len(results)} of {len(lists)} recorded lists replayed; "
            "the full replay has not finished"
            if len(results) < len(lists) else "complete"
        ),
        "workers": args.workers,
        "distinct_lists": len(results),
        "live_runs": len(results) * 2,
        "wall_time_s": wall,
        "invocations_s": spent,
        "counts": dict(sorted(counts.items())),
        "by_set": {k: dict(sorted(v.items())) for k, v in sorted(by_set.items())},
        "outcomes_v89_v90": dict(sorted(outcomes.items())),
        "line34_equal": line34_same,
        "line34_disposition_v89": dict(sorted(line34_v89.items())),
        "boxes_v90": {k: n for k, n in sorted(boxes.items(), key=lambda kv: -kv[1])},
        "page_alerts_v89": dict(sorted(alerts_v89.items())),
        "page_alerts_v90": dict(sorted(alerts_v90.items())),
        "changes": changes,
        "classes": {key: row["final"] for key, row in sorted(results.items())},
    }
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"rerun output contains {needle}")
    (HERE / "rerun-output.json").write_text(text, encoding="utf-8")
    print(json.dumps({k: payload[k] for k in (
        "live_runs", "wall_time_s", "counts", "outcomes_v89_v90", "line34_equal",
        "line34_disposition_v89",
        "page_alerts_v89", "page_alerts_v90", "boxes_v90",
    )}, indent=1))


if __name__ == "__main__":
    main()
