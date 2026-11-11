"""Core v82 runs every sale family audit Track 0 case and every v81 return through the real coordinator.

v82 is package core-calculations v82, registry v80 and release v80: the seven
decided fixes of the sale family audit, the three Track 0 repairs, the
Exception 1 rewording (Decision 2) and the review repairs. Every run goes
through ``live_coordinate_run`` and the presentation model on the published
v82.

- ``track0``: each Track 0 case the final design runs
  (``sale-family-audit-evidence/track0.py``), in its honest answer mode, and
  in its base-answer mode only where Track 0 recorded a different final result
  for it (review F5; the others repeat their honest run). Each run is held to
  the harness's hand values, blocked states, pinned rows and questions
  (``track0.verdict``), and must reach the verdict Track 0 recorded for the
  final design (``track0-output.json``).
- ``v81``: each return ``tests/test_code_b_sales_v81.py`` pins, built by that
  test's own harness in a subprocess (``export_v81_returns.py``), so its
  module state never meets this module's. Three corrections are made to each
  act list. The earlier harnesses record a direct or code W sale's rows on
  other transactions, so each row is moved to its own sale's transaction
  (Decision 3, ``own_rows``). They remove such a sale before its rows, which
  v82 refuses, so the sale is removed after them (review F1,
  ``rows_removed_first``). Each recorded Form 1099-B statement then gets "no"
  to the box 4 and box 7 questions. Each return runs with its own recorded
  answers. (Honest Exception 1 answers beside a recorded sale are not read,
  Decision 1; the Track 0 polarity cases witness that through the
  coordinator, so the v81 returns are not run a second time with them.)

Each projection pins the Schedule D and Form 1040 lines, the attachment
dispositions, the page questions, each of those lines' reason sentences when
it is blocked, the preferential base and
the (disposition, code, missing) of every row Track 0 watches that is not a
plain publication. The table is ``tests/fixtures/sale_family_audit_v82/expected.json``.
``python3 tests/test_sale_family_audit_v82.py <raw.json> [workers] [max]``
regenerates it. The raw runs are kept in ``raw.json``, outside the
repository, and a command resumes from them. Regeneration also runs every
corrected v81 return on v81, and records how the v82 run differs from it
(``class``). Act lists that are the same are run once, under the first key
(``duplicates``).

Synthetic demo.* data only.
"""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from types import ModuleType
from typing import Any, Iterator, cast

import pytest

from tests import evidence_loader

# Each case is one full live_coordinate_run (about 5 to 20 s), so the module is an
# integration test and runs in the live lane.
pytestmark = pytest.mark.live

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence"
EXPECTED_PATH = REPO / "tests/fixtures/sale_family_audit_v82/expected.json"
V81_TABLE = REPO / "tests/fixtures/code_b_sales_v81/expected.json"
TRACK0_MODULE = "sale_family_audit_track0"
P = "tax.us.2025."
YEAR = "2025"
V81_GROUPS = ("case", "v80", "neighbour")
MODES = ("recorded",)
Acts = list[dict[str, Any]]
PUBLISHED_ROW: list[Any] = ["published", None, []]

# Direct (lines 1a and 8a) and code W families: the rows the earlier harnesses put on other transactions.
OWN_ROW_FAMILIES = tuple(P + f"f1099b.{k}-{t}" for k in ("covered", "covered-w") for t in ("st", "lt"))
SALE_KEYS = ("broker", "statement", "transaction")


# ---- the harness ---------------------------------------------------------------------


def track0() -> ModuleType:
    """The Track 0 harness, loaded once under its own name. Nothing in it is assigned."""
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    return evidence_loader.load(EVIDENCE / "track0.py", TRACK0_MODULE)


def v82(t: ModuleType) -> Any:
    """The published core v82: the harness's Core with no scratch loader entries (packages/tax/loader.py has them)."""
    core = t.h.Core("v82", "v80", "v80")
    assert core.loader_from is None and core.content == REPO / "packages/content/tax/2025"
    return core


def final_fixes(t: ModuleType) -> set[str]:
    fixes = set(t.DESIGNS["final"])
    assert fixes == set(t.proto.SWITCHES)
    return fixes


def run(t: ModuleType, core: Any, acts: Acts, run_id: str) -> dict[str, Any]:
    """``track0.run`` (the same coordinator call), keeping each blocked line's reason sentences."""
    from packages.derivation.live import live_coordinate_run
    from packages.derivation.live_workspace import WorkspaceCapability

    h = t.h
    surface = core.surface()
    with h.loader_entries(core):
        try:
            finished = h._handover(h._finish(copy.deepcopy(acts), package_path=core.package_path,
                                             package_version=core.version, release_path=core.release_path,
                                             release_version=core.release_version, note=run_id),
                                   surface=surface, reconfirm=True)
            with tempfile.TemporaryDirectory() as tmp:
                outcome = live_coordinate_run(
                    WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO, authoritative_acts=finished,
                    workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": YEAR},
                    scope_user=h.ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
                    governance_pins=[], surface=surface, output_name="out.json")
                result: dict[str, Any] = t.summarize(core, outcome)
                if outcome.refusal is None:
                    assert outcome.presentation_path is not None
                    model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
                    reasons: dict[str, list[str]] = {}
                    for section in model.get("sections") or []:
                        resolved = section.get("resolved") or {}
                        if resolved.get("disposition") == "blocked":
                            field_id = str((section.get("field") or {}).get("id") or "").removeprefix(P)
                            reasons[field_id] = [str(r.get("sentence") or "") for r in resolved.get("reasons") or []
                                                 if isinstance(r, dict)]
                    result["reasons"] = reasons
                return result
        except Exception as exc:  # noqa: BLE001 — a rejected act list is a result, not a crash
            return {"error": type(exc).__name__, "message": h.scrub(str(exc))[:400]}


def projection(result: dict[str, Any]) -> dict[str, Any]:
    """The parts of a run the table pins."""
    if "error" in result or "refusal" in result:
        return {"error": result.get("error") or "refusal", "message": str(result.get("message") or result.get("refusal"))[:160]}
    rows = {name: row for name, row in sorted((result.get("rows") or {}).items()) if row != PUBLISHED_ROW}
    lines = result.get("lines") or {}
    reasons = {name: sentences for name, sentences in (result.get("reasons") or {}).items() if name in lines}
    return {"lines": lines, "attachments": result.get("attachments"),
            "questions": result.get("page_questions"), "reasons": reasons,
            "base": (result.get("symbols") or {}).get("capital-gains.selected-preferential-base"), "rows": rows}


def assert_sound(t: ModuleType, core: Any, result: dict[str, Any]) -> None:
    """A saturated run, a valid model, and one row from each watched publisher."""
    assert result.get("stop") == "saturated", result.get("stop")
    assert result.get("valid_model") is True, result.get("valid_model")
    assert result.get("duplicate_fields") == [], result.get("duplicate_fields")
    assert result.get("rows_not_one") == [], result.get("rows_not_one")
    assert set(result.get("rows") or {}) == {t.short(a) for a in t.publishers(core)}


# ---- act lists ------------------------------------------------------------------------


def _keys(fact_id: str) -> tuple[str, dict[str, str]]:
    fact_type, _, rest = fact_id.partition("|")
    return fact_type, dict(part.split("=", 1) for part in rest.split(",")) if rest else {}


def own_rows(acts: Acts) -> Acts:
    """Decision 3: each direct or code W sale's proceeds, basis and column (g) rows on that sale's own transaction.

    The earlier harnesses record a sale under the tag ``x`` or ``xo`` and its rows
    under ``xp``, ``xb`` and ``xa``, each with its own broker, statement and
    transaction. Each such row is moved to the identity of the one sale its tag
    names. A row already on a sale's transaction is left as it is.
    """
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
    corrected: Acts = json.loads(text)
    return corrected


def rows_removed_first(acts: Acts) -> Acts:
    """Review F1: a direct or code W sale is removed after its own rows, not before them.

    The earlier harnesses correct a sale by removing the sale object and then
    each of its rows. On v82 a row may not stand without its sale (the covered
    and code W presence pairs), so that order is refused at the sale's removal.
    Each such removal, with the closure that follows it, is moved after the last
    removal of a row on the same identity (after ``own_rows``). The acts of one
    family keep their order.
    """
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
        last = later[-1] + (1 if later[-1] + 1 < len(out) and closes(out[later[-1] + 1], removal(out[later[-1]])[0])  # type: ignore[index]
                            else 0)
        moved = out[index:index + block]
        out = out[:index] + out[index + block:last + 1] + moved + out[last + 1:]
        # the act now at ``index`` is the first row removal; continue from there
    for position, act in enumerate(out):
        act["committed_against"] = position
    return out


def v81_acts(t: ModuleType, exported: dict[str, dict[str, Acts]], group: str, name: str, mode: str,
             core: Any) -> Acts | None:
    assert mode in MODES, mode
    acts = rows_removed_first(own_rows(exported[group][name]))
    if core.version == "v81":  # v81 asks no box 4 or box 7 question
        return acts
    return cast(Acts, t.box_answers(acts, core, final_fixes(t), "no", "no"))


def track0_acts(t: ModuleType, name: str, mode: str, core: Any) -> Acts:
    return cast(Acts, t.build_case(t.CASES[name], mode, core, final_fixes(t)))


def track0_stored() -> dict[str, Any]:
    cases: dict[str, Any] = json.loads((EVIDENCE / "track0-output.json").read_text(encoding="utf-8"))["cases"]
    return cases


def repeats_honest(entry: dict[str, Any], mode: str) -> bool:
    """Track 0 recorded the same final result and verdict for ``mode`` as for the honest mode."""
    run_, honest = entry.get(f"final/{mode}"), entry.get("final/honest")
    return mode != "honest" and run_ is not None and honest is not None and \
        (run_["result"], run_["verdict"]) == (honest["result"], honest["verdict"])


def track0_keys(t: ModuleType) -> list[tuple[str, str]]:
    """Each final-design Track 0 run, less the base-answer runs that repeat their honest run (review F5)."""
    stored = track0_stored()
    return [(name, mode) for name, spec in t.CASES.items() if "final" in spec["designs"] for mode in spec["modes"]
            if not repeats_honest(stored.get(name, {}), mode)]


def v81_names() -> list[tuple[str, str]]:
    table = json.loads(V81_TABLE.read_text(encoding="utf-8"))
    return [(group, name) for group in V81_GROUPS for name in sorted(table[group])]


def export_v81_returns(directory: Path) -> dict[str, dict[str, Acts]]:
    """The v81 returns, built by their own harness in another process."""
    out = directory / "v81-acts.json"
    subprocess.run([sys.executable, str(EVIDENCE / "export_v81_returns.py"), str(out)], check=True, cwd=REPO,
                   stdout=subprocess.DEVNULL)
    exported: dict[str, dict[str, Acts]] = json.loads(out.read_text(encoding="utf-8"))
    return exported


def digest(acts: Acts) -> str:
    return hashlib.sha256(json.dumps(acts, sort_keys=True).encode("utf-8")).hexdigest()


# ---- the table -------------------------------------------------------------------------


def _expected() -> dict[str, Any]:
    if not EXPECTED_PATH.exists():  # only while the table is being regenerated
        return {"track0": {}, "v81": {}, "duplicates": {"track0": {}, "v81": {}}}
    return cast(dict[str, Any], json.loads(EXPECTED_PATH.read_text(encoding="utf-8")))


EXPECTED = _expected()


@pytest.fixture(scope="module")
def t0() -> ModuleType:
    return track0()


@pytest.fixture(scope="module")
def exported(tmp_path_factory: pytest.TempPathFactory) -> dict[str, dict[str, Acts]]:
    return export_v81_returns(tmp_path_factory.mktemp("sale-family-audit-v82"))


@pytest.fixture(scope="module")
def track0_verdicts() -> dict[str, Any]:
    return track0_stored()


@pytest.mark.parametrize("key", sorted(EXPECTED["track0"]))
def test_v82_matches_track0(t0: ModuleType, track0_verdicts: dict[str, Any], key: str) -> None:
    name, mode = key.split("/")
    core = v82(t0)
    result = run(t0, core, track0_acts(t0, name, mode, core), f"demo.sfa.t1.track0.{name}.{mode}")
    word, problems = t0.verdict(t0.CASES[name], result)
    assert problems == {}, problems
    assert word == track0_verdicts[name][f"final/{mode}"]["verdict"], word
    if word != "rejected at entry":
        assert_sound(t0, core, result)
    assert projection(result) == EXPECTED["track0"][key]


@pytest.mark.parametrize("key", sorted(EXPECTED["v81"]))
def test_v81_returns_on_v82(t0: ModuleType, exported: dict[str, dict[str, Acts]], key: str) -> None:
    group, name, mode = key.split("/")
    core = v82(t0)
    acts = v81_acts(t0, exported, group, name, mode, core)
    assert acts is not None
    result = run(t0, core, acts, f"demo.sfa.t1.v81.{group}.{name}.{mode}")
    if "error" not in result:
        assert_sound(t0, core, result)
    assert projection(result) == EXPECTED["v81"][key]["v82"]


# ---- what the table says, read without a run -----------------------------------------

# Final-design Track 0 runs the table covers, and the base-answer runs left out as repeats (review F5).
TRACK0_RUNS = 176
TRACK0_DROPPED = 134

# How each v81 return's v82 run differs from its v81 run (both on the corrected act list).
CLASSES = {
    "recorded": {
        "identical": 16,
        "F2 line 7b is not checked beside a recorded sale": 168,
        "D5 line 25b waits on an unclosed family + F2 line 7b waits on an unclosed family": 18,
        "D5 line 25b waits on an unclosed family + F2 line 7b is not checked beside a recorded sale": 5,
        "D1 a count row waits on an unclosed family + F2 line 7b waits on an unclosed family": 4,
        "D1 a count row waits on an unclosed family + F2 line 7b is not checked beside a recorded sale": 1,
        "D3 a direct or code W sale with no rows of its own + F2 line 7b is not checked beside a recorded sale": 1,
    },
}


def test_the_table_covers_every_run_once(t0: ModuleType) -> None:
    duplicates = EXPECTED["duplicates"]
    want = {f"{name}/{mode}" for name, mode in track0_keys(t0)}
    assert len(want) == TRACK0_RUNS
    assert set(EXPECTED["track0"]) | set(duplicates["track0"]) == want
    assert not set(EXPECTED["track0"]) & set(duplicates["track0"])
    names = v81_names()
    assert len(names) == 213
    recorded = {f"{g}/{n}/recorded" for g, n in names}
    assert {k for k in set(EXPECTED["v81"]) | set(duplicates["v81"]) if k.endswith("/recorded")} == recorded
    assert not set(EXPECTED["v81"]) & set(duplicates["v81"])
    for group in ("track0", "v81"):
        for duplicate, kept in duplicates[group].items():
            assert kept in EXPECTED[group], (duplicate, kept)


def test_no_v81_return_changes_class_beyond_the_decisions() -> None:
    for mode, classes in CLASSES.items():
        got: dict[str, int] = {}
        for key, entry in EXPECTED["v81"].items():
            if key.endswith("/" + mode):
                got[entry["class"]] = got.get(entry["class"], 0) + 1
        for duplicate, kept in EXPECTED["duplicates"]["v81"].items():
            if duplicate.endswith("/" + mode):
                label = EXPECTED["v81"][kept]["class"]
                got[label] = got.get(label, 0) + 1
        assert got == classes, (mode, got)


def _lines(entry: dict[str, Any]) -> dict[str, Any]:
    return cast(dict[str, Any], entry.get("lines") or {})


def test_no_published_v81_number_changes_on_v82() -> None:
    """Against the committed v81 table: a line that publishes a number on both cores publishes the same number."""
    table = json.loads(V81_TABLE.read_text(encoding="utf-8"))
    checked = 0
    for group, name in v81_names():
        key = f"{group}/{name}/recorded"
        key = EXPECTED["duplicates"]["v81"].get(key, key)
        pinned = table[group][name] if group == "case" else table[group][name]["v81"]
        if "error" in pinned:
            assert "error" in EXPECTED["v81"][key]["v82"], key
            continue
        now = _lines(EXPECTED["v81"][key]["v82"])
        for line, (_disposition, value) in (pinned.get("lines") or {}).items():
            if isinstance(value, (int, float)) and isinstance(now.get(line), (int, float)):
                assert now[line] == value, (key, line, value, now[line])
                checked += 1
    assert checked == 2035


def test_every_track0_case_keeps_a_run_and_every_dropped_run_repeats_one(t0: ModuleType) -> None:
    """Review F5: a base-answer run is left out only when Track 0 recorded the same final result for it as for
    the case's honest run, which the table keeps; no case loses its last run."""
    stored = track0_stored()
    kept = {name for name, _mode in track0_keys(t0)}
    dropped = []
    for name, spec in t0.CASES.items():
        if "final" not in spec["designs"]:
            continue
        assert name in kept, name
        for mode in spec["modes"]:
            if (name, mode) not in track0_keys(t0):
                assert repeats_honest(stored[name], mode) and "honest" in spec["modes"], (name, mode)
                dropped.append(name)
    assert len(dropped) == TRACK0_DROPPED


# ---- regeneration ---------------------------------------------------------------------

_STATE: dict[str, Any] = {}


def _init(acts_path: str) -> None:
    _STATE["exported"] = json.loads(Path(acts_path).read_text(encoding="utf-8"))
    _STATE["t"] = track0()


def _build(task: tuple[str, ...]) -> Acts | None:
    t = _STATE["t"]
    kind = task[0]
    if kind == "track0":
        _, name, mode = task
        return track0_acts(t, name, mode, v82(t))
    _, group, name, mode, core_name = task
    core = v82(t) if core_name == "v82" else t.h.V81
    return v81_acts(t, _STATE["exported"], group, name, mode, core)


def _execute(task: tuple[str, ...]) -> tuple[tuple[str, ...], dict[str, Any]]:
    t = _STATE["t"]
    acts = _build(task)
    assert acts is not None
    core = t.h.V81 if task[-1] == "v81" else v82(t)
    return task, run(t, core, acts, "demo.sfa.t1." + ".".join(task))


FORM1040_TAX = ("form1040.line-16", "form1040.line-34", "form1040.line-37")


def _number(value: Any) -> bool:
    return isinstance(value, (int, float))


def classify(t: ModuleType, before: dict[str, Any], after: dict[str, Any]) -> str:
    """Which decisions explain how a corrected v81 return's v82 run differs from its v81 run.

    - D1 (honest answers): v81 refuses line 16 (guard_inapplicable) beside a Form 8949 sale when
      Exception 1 is answered truthfully; on v82 line 16 computes or waits on another input.
    - D1 (count rows): a box C or F count row waits on an unclosed family; no line changes.
    - D3: a direct or code W sale with no rows of its own is refused, and its line blocks.
    - D5: line 25b waits on an unclosed sale family beside a Form 1040 that was already blocked.
    - F2: line 7b, "Schedule D not required", is not checked beside a recorded sale, or waits on an
      unclosed sale family beside a Form 1040 that was already blocked (and the page may then also ask
      that family's question). Both cores read the same Exception 1 answers, so a line 7b that v81
      checks and v82 does not is v82 reading a recorded sale.

    A line that published a number may only become blocked, and only through D3 or D5.
    """
    diff = t.rerun_mod.difference(before, after)
    if not diff:
        return "identical"
    if t.numbers_changed(before, after) or set(diff) - {"lines", "blocked_rows", "attachments", "questions"}:
        return "UNCLASSIFIED"
    v81_lines, v82_lines = before.get("lines") or {}, after.get("lines") or {}
    line_changes: dict[str, list[Any]] = dict(diff.get("lines") or {})
    v81_1040_blocked = not all(_number(v81_lines.get(k)) for k in FORM1040_TAX)
    line7b_labels: list[str] = []
    if "form1040.line-7b" in line_changes:
        old, new = line_changes.pop("form1040.line-7b")
        if old == "published_categorical" and new == "guard_inapplicable":
            line7b_labels.append("F2 line 7b is not checked beside a recorded sale")
        elif new == "blocked" and old != "blocked" and v81_1040_blocked:
            line7b_labels.append("F2 line 7b waits on an unclosed family")
            if "questions" in diff:
                old_questions, new_questions = diff["questions"]
                if not set(old_questions) <= set(new_questions):
                    return "UNCLASSIFIED"
                diff = {k: v for k, v in diff.items() if k != "questions"}
        else:
            return "UNCLASSIFIED"
        if not line_changes:
            diff = {k: v for k, v in diff.items() if k != "lines"}
        if not diff:
            return " + ".join(line7b_labels)
    honest_d1 = v81_lines.get("form1040.line-16") == "guard_inapplicable" != v82_lines.get("form1040.line-16")
    labels: list[str] = []
    if honest_d1:
        computes = all(_number(v82_lines.get(k)) for k in FORM1040_TAX)
        labels.append("D1 the honest Exception 1 answer: " + ("the tax computes" if computes
                                                               else "line 16 waits on another input"))
    elif "attachments" in diff or "questions" in diff or any(not _number(old) for old, _ in line_changes.values()):
        return "UNCLASSIFIED"
    rows = diff.get("blocked_rows") or {}
    rowless = [k for k, (old, new) in rows.items() if k.endswith("txn.admission-check") and old is None
               and new is not None and new[0] == "DEPENDENCY_ABSENT"
               and all(m.rsplit(".", 1)[-1] in ("proceeds", "basis", "adjustment") for m in new[1])]
    for line, (old, new) in sorted(line_changes.items()):
        if not _number(old):
            continue  # a refused or blocked v81 line: only the honest D1 change reaches here
        if new != "blocked" or not v81_1040_blocked:
            return "UNCLASSIFIED"
        if line == "form1040.line-25b":
            labels.append("D5 line 25b waits on an unclosed family")
        elif line.startswith("schedule-d.") and rowless:
            labels.append("D3 a direct or code W sale with no rows of its own")
        else:
            return "UNCLASSIFIED"
    if not honest_d1:
        if rowless and not any(label.startswith("D3") for label in labels):
            return "UNCLASSIFIED"
        if not rowless and t.watched_rows_explained(before, after):
            return "UNCLASSIFIED"
        if not labels and not line7b_labels:
            labels.append("D1 a count row waits on an unclosed family")
        elif not labels and (diff.get("blocked_rows") or diff.get("attachments") or diff.get("questions")):
            labels.append("D1 a count row waits on an unclosed family")
    return " + ".join(dict.fromkeys(labels + line7b_labels))


def _tasks(t: ModuleType, exported: dict[str, dict[str, Acts]]) -> tuple[list[tuple[str, ...]], dict[str, dict[str, str]]]:
    """Every run to make, each distinct act list once, and the keys left out as duplicates."""
    _STATE.update({"exported": exported, "t": t})
    tasks: list[tuple[str, ...]] = []
    duplicates: dict[str, dict[str, str]] = {"track0": {}, "v81": {}}
    seen: dict[str, str] = {}
    for name, mode in track0_keys(t):
        key, task = f"{name}/{mode}", ("track0", name, mode)
        acts = _build(task)
        assert acts is not None
        found = seen.setdefault(name + ":" + digest(acts), key)  # a case's own modes only: cases differ in hand values
        if found != key:
            duplicates["track0"][key] = found
        else:
            tasks.append(task)
    seen = {}
    for group, name in v81_names():
        for mode in MODES:
            key = f"{group}/{name}/{mode}"
            acts = _build(("v81", group, name, mode, "v82"))
            if acts is None:
                continue
            found = seen.setdefault(digest(acts), key)
            if found != key:
                duplicates["v81"][key] = found
            else:
                tasks += [("v81", group, name, mode, "v82"), ("v81", group, name, mode, "v81")]
    return tasks, duplicates


def _chunks(items: list[Any], size: int) -> Iterator[list[Any]]:
    for start in range(0, len(items), size):
        yield items[start:start + size]


def regenerate(raw_path: Path, workers: int, limit: int | None) -> None:
    if REPO in raw_path.resolve().parents:
        raise SystemExit("keep the raw runs outside the repository")
    t = track0()
    with tempfile.TemporaryDirectory() as tmp:
        exported = export_v81_returns(Path(tmp))
        acts_path = Path(tmp) / "v81-acts.json"
        tasks, duplicates = _tasks(t, exported)
        raw: dict[str, dict[str, Any]] = json.loads(raw_path.read_text(encoding="utf-8")) if raw_path.exists() else {}
        todo = [task for task in tasks if "/".join(task) not in raw]
        todo = todo[:limit] if limit is not None else todo
        if todo:
            with ProcessPoolExecutor(workers, initializer=_init, initargs=(str(acts_path),)) as pool:
                for chunk in _chunks(todo, workers * 8):
                    for task, result in pool.map(_execute, chunk):
                        raw["/".join(task)] = result
                        print(*task, result.get("error") or "", flush=True)
                    raw_path.write_text(json.dumps(raw) + "\n", encoding="utf-8")
    missing = [task for task in tasks if "/".join(task) not in raw]
    if missing:
        print(f"{len(missing)} runs still to go; run the command again", flush=True)
        return
    stored = json.loads((EVIDENCE / "track0-output.json").read_text(encoding="utf-8"))["cases"]
    v81_table = json.loads(V81_TABLE.read_text(encoding="utf-8"))
    table: dict[str, Any] = {"track0": {}, "v81": {}, "duplicates": duplicates}
    problems: list[str] = []
    for task in tasks:
        result = raw["/".join(task)]
        if task[0] == "track0":
            _, name, mode = task
            word, found = t.verdict(t.CASES[name], result)
            if found or word != stored[name][f"final/{mode}"]["verdict"]:
                problems.append(f"track0 {name} {mode}: {word} {found}")
            table["track0"][f"{name}/{mode}"] = projection(result)
        elif task[-1] == "v82":
            _, group, name, mode, _core = task
            before = raw["/".join((*task[:-1], "v81"))]
            label = classify(t, before, result)
            if label.startswith("UNCLASSIFIED"):
                problems.append(f"v81 {group} {name} {mode}: {label}")
            if mode == "recorded":
                pinned = v81_table[group][name] if group == "case" else v81_table[group][name]["v81"]
                mismatch = t.rerun_mod.fixture_mismatch(pinned, before)
                if mismatch:
                    problems.append(f"v81 {group} {name}: own_rows changed the v81 run {mismatch}")
            table["v81"][f"{group}/{name}/{mode}"] = {"class": label, "v82": projection(result),
                                                     "v81_difference": t.rerun_mod.difference(before, result)}
    lines = ["{"]
    keys = ("duplicates", "track0", "v81")
    for i, group in enumerate(keys):
        lines.append(f" {json.dumps(group)}: {{")
        names = sorted(table[group])
        for j, name in enumerate(names):
            comma = "," if j < len(names) - 1 else ""
            lines.append(f"  {json.dumps(name)}: {json.dumps(table[group][name], sort_keys=True)}{comma}")
        lines.append(" }" + ("," if i < len(keys) - 1 else ""))
    lines.append("}")
    EXPECTED_PATH.parent.mkdir(parents=True, exist_ok=True)
    EXPECTED_PATH.write_text(t.h.scrub("\n".join(lines)) + "\n", encoding="utf-8")
    print(f"wrote {EXPECTED_PATH.relative_to(REPO)}", flush=True)
    for mode in MODES:
        counts: dict[str, int] = {}
        for key, entry in table["v81"].items():
            if key.endswith("/" + mode):
                counts[entry["class"]] = counts.get(entry["class"], 0) + 1
        for duplicate, kept in duplicates["v81"].items():
            if duplicate.endswith("/" + mode):
                counts[table["v81"][kept]["class"]] = counts.get(table["v81"][kept]["class"], 0) + 1
        print(mode, json.dumps(counts, sort_keys=True), flush=True)
    if problems:
        print("\n".join(problems), flush=True)
        raise SystemExit(1)


if __name__ == "__main__":
    regenerate(Path(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 8,
               int(sys.argv[3]) if len(sys.argv) > 3 else None)
