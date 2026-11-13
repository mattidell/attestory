"""Replay every recorded act list question-wording Track 0 replayed, on v86 and scratch v88.

Evidence for docs/phases/engine-breadth/milestones/age-blindness-asked.md.
Charter: docs/reviews/age-blindness-asked/charter-p0.md.

The lists are question-wording's ``neighbour_tasks`` (track0.py, loaded, not
copied): 775 distinct act lists from the v81, v82, v83, v84 and v85 fixtures.
Each list runs three times:

- ``v86``: published core v86, as recorded;
- ``v88``: scratch core v88, as recorded;
- ``v88_answered``: scratch core v88 with the facts the record leaves
  unstated answered false. No recorded list states an age or blindness
  fact, so each relied on the default false. The taxpayer's two facts are
  answered on every list, the spouse's two where the recorded filing
  status is joint or separate, and the separate-return condition fact on
  a separate return. A fact the record does state is left as recorded.
  A separate return, and any list that asserts the condition fact,
  re-adopts vocabulary bundle v4 before that assertion. Other lists keep
  the bundle adoptions they were recorded with.

The pin and the classes are question-wording rerun.py's (``_pin_run``,
``classify``): identical, numbers_identical_sentences_changed,
numbers_changed. A list is newly asked when its v88 pin names one of the
four new questions and its v86 pin does not.

    python3 rerun.py shard <scratch>/core-v88.json <i> <n> <scratch>/rr-<i>.json
    python3 rerun.py merge <scratch>/rr-*.json
    python3 rerun.py against-v87 <scratch>/core-v87.json <scratch>/core-v88.json

``against-v87`` reruns each list whose answered v88 pin is not identical to
v86 on scratch v87 as recorded, and classifies v87 against answered v88: an
identical pair means the difference is question-wording's, not this core's.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

QW = REPO / "docs/phases/engine-breadth/milestones/question-wording-evidence"
P = "tax.us.2025."
AGE, BLIND, S_AGE, S_BLIND = (P + "taxpayer-over-65", P + "taxpayer-blind", P + "spouse-over-65", P + "spouse-blind")
COND = P + "standard-deduction.spouse-separate-condition"
STATUS = P + "filing-status"
MARRIED = {"married_filing_jointly", "married_filing_separately"}
MFS = "married_filing_separately"
Acts = list[dict[str, Any]]


def _module(name: str, path: Path) -> Any:
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def qw_track0() -> Any:
    return _module("aba_p0_qw_track0", QW / "track0.py")


def recorded(acts: Acts, fact: str) -> list[Any]:
    found = []
    for act in acts:
        payload = act.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(fact + "|"):
            found.append(finding.get("value"))
    return found


def implied(acts: Acts) -> dict[str, Any]:
    """Facts v88 asks and the record leaves unstated, each answered false."""
    status = recorded(acts, STATUS)
    facts = [AGE, BLIND]
    if status and status[-1] in MARRIED:
        facts += [S_AGE, S_BLIND]
    if status and status[-1] == MFS:
        facts.append(COND)
    return {fact: False for fact in facts if not recorded(acts, fact)}


def adopt_v88(core: Any, acts: Acts) -> Acts:
    """Re-adopt vocabulary v4 only when this list needs the condition fact.

    A single, joint, head of household, or qualifying surviving spouse list
    does not read the fact. Leaving its adoptions untouched keeps that pin
    comparable with published v87. A separate return's worksheet line reads
    the fact, and an assertion of it is valid only after v4 is adopted.
    """
    if getattr(core, "version", None) != "v88":
        return acts
    probe = _module("aba_t0_probe", HERE / "probe.py")
    status = recorded(acts, STATUS)
    if probe._condition_assertion_index(acts) is None and not (status and status[-1] == MFS):
        return acts
    return probe.readopt(acts, core)


def answered(acts: Acts, answers: dict[str, Any]) -> Acts:
    h = qw_track0().harness()
    for fact, value in answers.items():
        acts = h.say(acts, fact, value, "aba-implied-" + fact.removeprefix(P))
    return acts


def asked(pin: dict[str, Any], sentences: dict[str, str]) -> list[str]:
    blob = json.dumps(pin)
    return sorted(slug for slug, sentence in sentences.items() if json.dumps(sentence)[1:-1] in blob)


def run_shard(core_path: Path, shard: int, count: int, part: Path) -> None:
    t0 = qw_track0()
    rr = t0.rerun()
    test = rr.load_test()
    sentences = json.loads((HERE / "prototype-build.json").read_text(encoding="utf-8"))["questions"]
    work = t0.neighbour_tasks()
    print(f"{len(work)} distinct act lists", flush=True)
    v88, v86 = rr.scratch_core(test, core_path), rr.published_v86(test)
    found: dict[str, Any] = json.loads(part.read_text(encoding="utf-8")) if part.exists() else {}
    found["_total"] = len(work)
    for index, (key, acts) in enumerate(work):
        if index % count != shard or key in found:
            continue
        slug = re.sub(r"[^A-Za-z0-9_.-]", ".", key)
        stated = {fact.removeprefix(P): recorded(acts, fact) for fact in (AGE, BLIND, S_AGE, S_BLIND)}
        answers = implied(acts)
        pin86 = rr._pin_run(test, v86, acts, "demo.aba.rr.v86." + slug)
        pin88 = rr._pin_run(test, v88, adopt_v88(v88, acts), "demo.aba.rr.v88." + slug)
        pin88a = rr._pin_run(test, v88, adopt_v88(v88, answered(acts, answers)), "demo.aba.rr.v88a." + slug)
        row = {
            "status": (recorded(acts, STATUS) or [None])[-1],
            "stated": {k: v for k, v in stated.items() if v},
            "answered": {k.removeprefix(P): v for k, v in answers.items()},
            "as_recorded": rr.classify(pin86, pin88),
            "answered_vs_v86": rr.classify(pin86, pin88a),
            "asked_v86": asked(pin86, sentences),
            "asked_v88": asked(pin88, sentences),
            "asked_v88_answered": asked(pin88a, sentences),
            "v86_error": pin86.get("error"),
            "v88_error": pin88.get("error"),
            "v88_answered_error": pin88a.get("error"),
            "v86_pin_sha256": hashlib.sha256(json.dumps(pin86, sort_keys=True).encode()).hexdigest()[:16],
        }
        found[key] = row
        part.write_text(json.dumps(found, indent=1) + "\n", encoding="utf-8")
        print(f"shard {shard}: {index} {key} {row['as_recorded']['class']} / {row['answered_vs_v86']['class']}",
              flush=True)


def merge(parts: list[Path]) -> None:
    found: dict[str, Any] = {}
    total = 0
    for part in parts:
        body = json.loads(part.read_text(encoding="utf-8"))
        total = max(total, int(body.pop("_total", 0)))
        found.update(body)
    by_set: dict[str, dict[str, Counter[str]]] = {}
    for key, row in found.items():
        prefix = key.split("/", 1)[0]
        bucket = by_set.setdefault(prefix, {"as_recorded": Counter(), "answered_vs_v86": Counter(),
                                            "newly_asked": Counter(), "errors": Counter()})
        bucket["as_recorded"][row["as_recorded"]["class"]] += 1
        bucket["answered_vs_v86"][row["answered_vs_v86"]["class"]] += 1
        newly = bool(row["asked_v88"]) and not row["asked_v86"]
        bucket["newly_asked"]["yes" if newly else "no"] += 1
        if row["v86_error"]:
            same = row["v86_error"] == row["v88_error"] == row["v88_answered_error"]
            bucket["errors"][f"{row['v86_error']} ({'same on all three runs' if same else 'differs'})"] += 1
    computing = {k: r for k, r in found.items() if not r["v86_error"]}
    newly = sorted(k for k, r in computing.items() if r["asked_v88"] and not r["asked_v86"])
    not_asked = sorted(k for k, r in computing.items() if not r["asked_v88"])
    asked_counts = Counter(tuple(r["asked_v88"]) for r in computing.values())
    status_counts = Counter(str(r["status"]) for r in computing.values())
    restored = sorted(k for k, r in computing.items() if r["answered_vs_v86"]["class"] == "identical")
    unrestored = [{"id": k, **found[k]} for k in sorted(computing) if found[k]["answered_vs_v86"]["class"] != "identical"]
    payload = {
        "sets": json.loads((QW / "track0-neighbour.json").read_text(encoding="utf-8"))["sets"],
        "source": "question-wording track0.py neighbour_tasks, loaded",
        "distinct_lists": total,
        "runs": len(found),
        "live_runs": len(found) * 3,
        "answer_rule": (
            "No list states any of the four age and blindness facts, so each relied on the default false. "
            "v88_answered adds false for taxpayer-over-65 and taxpayer-blind on every list, and for "
            "spouse-over-65 and spouse-blind where the recorded filing status is married filing jointly "
            "or separately. On a separate return it also adds false for "
            "standard-deduction.spouse-separate-condition."
        ),
        "classes_defined": json.loads((QW / "rerun-output.json").read_text(encoding="utf-8"))["classes_defined"],
        "by_set": {k: {name: dict(c) for name, c in v.items()} for k, v in sorted(by_set.items())},
        "lists_that_compute_on_v86": len(computing),
        "newly_asked": len(newly),
        "computing_lists_not_asked_on_v88": not_asked,
        "asked_on_v88": {", ".join(k) or "(none)": n for k, n in sorted(asked_counts.items())},
        "filing_status_of_computing_lists": dict(sorted(status_counts.items())),
        "answered_identical_to_v86": len(restored),
        "answered_not_identical_to_v86": unrestored,
        "stated_any_fact": sorted(k for k, r in found.items() if r["stated"]),
        "rows": {k: {"as_recorded": r["as_recorded"]["class"], "answered_vs_v86": r["answered_vs_v86"]["class"],
                     "asked_v88": r["asked_v88"], "status": r["status"], "v86_error": r["v86_error"]}
                 for k, r in sorted(found.items())},
    }
    text = re.sub(r"(?:/Users|/private|/tmp|/var)/\S+", "[path]", json.dumps(payload, indent=2) + "\n")
    (HERE / "rerun-output.json").write_text(text, encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("runs", "lists_that_compute_on_v86", "newly_asked",
                                              "answered_identical_to_v86", "asked_on_v88", "by_set")}, indent=1))


def against_v87(core87: Path, core88: Path) -> None:
    t0 = qw_track0()
    rr = t0.rerun()
    test = rr.load_test()
    out_path = HERE / "rerun-output.json"
    payload = json.loads(out_path.read_text(encoding="utf-8"))
    ids = {row["id"] for row in payload["answered_not_identical_to_v86"]}
    v87, v88 = rr.scratch_core(test, core87), rr.scratch_core(test, core88)
    found = {}
    for key, acts in t0.neighbour_tasks():
        if key not in ids:
            continue
        slug = re.sub(r"[^A-Za-z0-9_.-]", ".", key)
        answered_acts = answered(acts, implied(acts))
        h = _module("aba_t0_probe", HERE / "probe.py").harness()
        pin87 = rr._pin_run(test, v87, h.strip(answered_acts, COND), "demo.aba.rr.v87." + slug)
        pin88a = rr._pin_run(test, v88, adopt_v88(v88, answered_acts), "demo.aba.rr.v88a2." + slug)
        found[key] = {"v87_vs_v88_answered": rr.classify(pin87, pin88a)["class"]}
    payload["not_identical_against_v87"] = found
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(found, indent=1))


def main() -> None:
    args = sys.argv[1:]
    if args[:1] == ["against-v87"] and len(args) == 3:
        against_v87(Path(args[1]), Path(args[2]))
        return
    if args[:1] == ["shard"] and len(args) == 5:
        run_shard(Path(args[1]), int(args[2]), int(args[3]), Path(args[4]))
    elif args[:1] == ["merge"] and len(args) >= 2:
        merge([Path(a) for a in args[1:]])
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
