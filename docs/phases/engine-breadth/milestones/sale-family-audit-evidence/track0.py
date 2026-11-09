"""Track 0 adversarial closure runs for the sale family audit.

Evidence for track0-closure.md beside this file and the "Track 0 adversarial
closure" section of docs/phases/engine-breadth/milestones/sale-family-audit.md.
Every case runs through ``live_coordinate_run`` on a scratch core v82 built by
``prototype.py`` outside the repository. Nothing under packages/ is written.

    python3 docs/phases/engine-breadth/milestones/sale-family-audit-evidence/track0.py cases [workers] [prefix ...] [--design=final]
    python3 .../track0.py rerun <acts.json> [workers] [raw.json] [max]   # the 213 pinned v81 returns
                                                     # (export_v81_returns.py); raw.json (outside the repository)
                                                     # keeps the runs, and a rerun resumes, at most max runs at a time
    python3 .../track0.py surface                         # the static integration surface of the final v82
    python3 .../track0.py shrink                          # rewrite track0-output.json in its small form

Two designs are built:

- ``decided``: prototype.FIXES, the seven fixes Decisions 1-5 take;
- ``final``: FIXES plus prototype.REPAIRS, the Track 0 repairs and the
  Track 1 ``exception1_words`` repair (Decision 2).

Writes track0-output.json beside this file (``cases`` and ``surface`` merge
into it; ``rerun`` writes its section). Modules are loaded under unique names:
this file loads prototype.py as ``sale_family_audit_prototype``,
audit_harness.py as ``sale_family_audit_harness``, probe.py as
``sale_family_audit_probe`` and rerun_v81.py as ``sale_family_audit_rerun``.
It sets no attribute on any of them; the only in-process change is the
harness's own per-run ``loader_entries``.
"""

from __future__ import annotations

import atexit
import copy
import importlib.util
import json
import shutil
import sys
import tempfile
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
OUT = HERE / "track0-output.json"
Acts = list[dict[str, Any]]


def load(name: str, path: Path) -> Any:
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


h: Any = load("sale_family_audit_harness", HERE / "audit_harness.py")
probe: Any = load("sale_family_audit_probe", HERE / "probe.py")
proto: Any = load("sale_family_audit_prototype", HERE / "prototype.py")
rerun_mod: Any = load("sale_family_audit_rerun", HERE / "rerun_v81.py")
assert probe.h is h and rerun_mod.harness() is h

P = h.P
YEAR = h.YEAR
# The repairs of the fresh-reader review (docs/reviews/sale-family-audit/review.md).
REVIEW_REPAIRS = ("row_needs_sale", "line7b_activity", "field_truth")
# ``track1``: the v82 Track 1 published, which the review read (final without the review repairs).
DESIGNS = {"decided": set(proto.FIXES), "final": set(proto.SWITCHES),
           "track1": set(proto.SWITCHES) - set(REVIEW_REPAIRS)}
SALE_OBJECTS = tuple(P + s for s in proto.SALE_OBJECTS)
SALE_FAMILIES = tuple(s.removesuffix("-txn") for s in SALE_OBJECTS)

# ---- cores -----------------------------------------------------------------------


def core_of(spec: dict[str, Any] | None) -> Any:
    if spec is None:
        return h.V81
    return h.Core(spec["version"], spec["registry"], spec["release_version"], Path(spec["content"]),
                  Path(spec["releases"]), spec.get("loader_from"),
                  tuple(tuple(p) for p in spec.get("presence_pairs") or ()))


def build_designs(names: tuple[str, ...]) -> dict[str, dict[str, Any]]:
    """Build each design's scratch core outside the repository; removed at exit."""
    root = Path(tempfile.mkdtemp(prefix="sfa-track0-")).resolve()
    atexit.register(shutil.rmtree, root, True)
    cores: dict[str, dict[str, Any]] = {}
    for name in names:
        summary = proto.build(root / name, set(DESIGNS[name]))
        cores[name] = {"version": proto.TO["package"], "registry": proto.TO["registry"],
                       "release_version": proto.TO["release"], "content": str(root / name / "content"),
                       "releases": str(root / name / "releases"), "loader_from": proto.FROM["package"],
                       # In packages/tax/loader.py's order: the kernel's reverse check reads the last pair per sale.
                       "presence_pairs": list(proto.presence_pairs(set(DESIGNS[name])).items()),
                       "build": {k: summary[k] for k in ("fixes", "repairs", "members_edited", "added", "replaced",
                                                           "inherited_inconsistencies")}}
        print(name, json.dumps(cores[name]["build"]), flush=True)
    return cores


# ---- recording helpers -------------------------------------------------------------


def sale_statements(acts: Acts) -> list[str]:
    """The statement entity of every current Form 1099-B sale (asserted and not removed), in order."""
    current: dict[str, str] = {}
    for act in acts:
        payload = act.get("payload") or {}
        if act.get("kind") != "member-transition" or (payload.get("family") or {}).get("id") not in SALE_FAMILIES:
            continue
        member = payload.get("member") or {}
        if member.get("action") == "remove":
            current.pop(str(member.get("fact_id")), None)
            continue
        fact_id = str((member.get("finding") or {}).get("fact_id", ""))
        keys = dict(part.split("=", 1) for part in fact_id.split("|", 1)[1].split(",")) if "|" in fact_id else {}
        if "statement" in keys:
            current[fact_id] = keys["statement"]
    return list(dict.fromkeys(current.values()))


def say_statement(acts: Acts, core: Any, fact: str, statement: str, value: str) -> Acts:
    """A per-statement answer (statement_box4 / statement_box7), replacing an earlier one for that statement."""
    fact_type = P + fact
    fact_id = h.fact_id_for(fact_type, (("statement", statement), ("tax-year", YEAR)))
    kept = []
    for act in acts:
        finding = (act.get("payload") or {}).get("finding") if isinstance(act.get("payload"), dict) else None
        if isinstance(finding, dict) and finding.get("fact_id") == fact_id:
            continue
        kept.append(act)
    acts = kept
    body = h.bundle_for(fact_type, core.content)
    assert body is not None, fact_type
    if not {f["id"] for f in body["fact_types"]} & h._adopted(acts):
        h._add(acts, "bundle-adoption", {"bundle": body})
    h._add(acts, "assertion", {"finding": h._attested(f"demo.sfa.t0.{fact.split('.')[-1]}.{statement}", fact_id, value)})
    return h.renumber(acts)


BoxAnswer = str | dict[str, str | None] | None


def box_answers(acts: Acts, core: Any, fixes: set[str], box4: BoxAnswer = "no", box7: BoxAnswer = "no") -> Acts:
    """The box 4 and box 7 answers a core asks, when a Form 1099-B sale is recorded.

    A str answers every statement (or the one return-level question). A dict maps a
    statement entity to its answer, with ``"*"`` for the rest; None leaves it unanswered.
    """
    statements = sale_statements(acts)
    if not statements:
        return acts
    for box, value in ((4, box4), (7, box7)):
        if f"box{box}_question" not in fixes or value is None:
            continue
        fact = proto.box_fact(box, fixes)
        per = value if isinstance(value, dict) else {"*": value}
        if fact in (proto.BOX4_STATEMENT, proto.BOX7_STATEMENT):
            for statement in statements:
                answer = per.get(statement, per.get("*"))
                if answer is not None:
                    acts = say_statement(acts, core, fact, statement, answer)
        else:
            # One return-level answer: "yes" when any statement's is, else "no"; nothing when none is given.
            answers = [a for a in (per.get(s, per.get("*")) for s in statements) if a is not None]
            if answers:
                acts = h.say(acts, P + fact, "yes" if "yes" in answers else "no", f"box{box}", core.content)
    return acts


def orphan_yes(acts: Acts, core: Any) -> Acts:
    """A statement entity with a box 4 yes and no sale recorded on it."""
    acts = copy.deepcopy(acts)
    h._introduce(acts, "demo.sfa.orphan.statement", "tax.us.f1099b-statement")
    return say_statement(h.renumber(acts), core, proto.BOX4_STATEMENT, "demo.sfa.orphan.statement", "yes")


def statement_of(tag: str) -> str:
    return f"demo.sfa.{tag}.statement"


def sale_on(acts: Acts, kind: str, term: str, tag: str, *, statement_tag: str, **kw: Any) -> Acts:
    """A sale recorded on another sale's statement (same broker and statement, its own transaction)."""
    acts = h.sale(acts, kind, term, tag=tag, **kw)
    mapping = {f"demo.sfa.{tag}.broker": f"demo.sfa.{statement_tag}.broker",
               f"demo.sfa.{tag}.statement": f"demo.sfa.{statement_tag}.statement"}
    out: Acts = []
    for act in acts:
        if act.get("kind") == "entity-introduced" and act["payload"]["entity"]["id"] in mapping:
            continue
        text = json.dumps(act)
        for old, new in mapping.items():
            text = text.replace(old + ",", new + ",").replace(old + '"', new + '"')
        out.append(json.loads(text))
    return h.renumber(out)


def remove_sale(acts: Acts, kind: str, term: str, tag: str,
                parts: tuple[str | None, ...] | None = None) -> Acts:
    """Remove one sale and its amount rows; a per-family (covered, code W) family is closed again.

    ``parts`` names what is removed, in order (a scalar kind, or None for the sale
    object); by default every row, then the sale.
    """
    per_family = h.SALE_KINDS[kind]["grouped"] is None
    out = copy.deepcopy(acts)
    for scalar in (parts if parts is not None else (*h.SALE_KINDS[kind]["kinds"], None)):
        fam = h.family_id(kind, term, scalar)
        member = h.member_fact(kind, term, scalar)
        fact_ids = [str(a["payload"]["member"]["finding"]["fact_id"]) for a in out
                    if a.get("kind") == "member-transition" and a["payload"]["family"]["id"] == fam
                    and (a["payload"]["member"].get("finding") or {}).get("fact_id", "").startswith(member + "|")
                    and f"demo.sfa.{tag}." in a["payload"]["member"]["finding"]["fact_id"]]
        for fact_id in fact_ids:
            if per_family:
                out = h.strip(out, fam + ".source-closure")
            head = h.horizons(out, fam)[-1]
            successor = f"demo.sfa.rm.{tag}.{fam.removeprefix(P)}.h{len(h.horizons(out, fam))}"
            h._add(out, "member-transition", {
                "family": {"id": fam, "version": h.SALE_KINDS[kind]["version"]},
                "scope": {"tax-year": YEAR, "subject": "demo.primary"},
                "member": {"action": "remove", "fact_id": fact_id},
                "successor": {"id": successor, "predecessor": head}})
            if per_family:
                h._close(out, fam + ".source-closure", successor, f"demo.sfa.rm.{tag}.{fam.removeprefix(P)}.closure")
    return h.renumber(out)


# ---- running ----------------------------------------------------------------------

WATCH_SYMBOLS = tuple(P + s for s in (
    "tax.total-tax", "tax.line24-total-tax", "payments.line25b", "payments.line33", "payments.line34-overpaid",
    "payments.line37-amount-owed", "capital-gains.line7a-total", "capital-gains.selected-preferential-base",
    "form8949.disposition", "schedule-d.disposition",
    *(f"schedule-d.line-{n}" for n in ("1a-gain", "1b", "2", "3", "7", "8a-gain", "8b", "9", "10", "15", "16", "21")),
    *(f"f1099b.{k}-{t}-count" for k in ("covered", "covered-w", "noncovered", "code-b") for t in ("st", "lt")),
    *(f"f8949.no1099b-{t}-count" for t in ("st", "lt")),
    *(f"f1099b.{k}-{t}-txn.admission-check" for k in ("covered", "covered-w") for t in ("st", "lt")),
    *(f"f1099b.{k}-{t}-txn.amounts-check" for k in ("noncovered", "code-b") for t in ("st", "lt")),
    *(f"f8949.no1099b-{t}-txn.amounts-check" for t in ("st", "lt")),
))
PROBED_FIELDS = tuple(P + f for f in (
    "form1040.line-7a", "form1040.line-7b", "form1040.line-16", "form1040.line-24", "form1040.line-25b", "form1040.line-33",
    "form1040.line-34", "form1040.line-37", "schedule-d.line-1a", "schedule-d.line-8a", "schedule-d.line-1b",
    "schedule-d.line-8b", "schedule-d.line-2", "schedule-d.line-3", "schedule-d.line-9", "schedule-d.line-10",
    "schedule-d.line-16"))
_PUBLISHERS: dict[str, dict[str, str]] = {}


def publishers(core: Any) -> dict[str, str]:
    """Rule id -> symbol, for every member of ``core``'s package that publishes a watched symbol."""
    key = str(core.package_path)
    if key not in _PUBLISHERS:
        package = json.loads(core.package_path.read_text(encoding="utf-8"))
        wanted = {(m["id"], m["version"]) for m in package["members"]}
        found: dict[str, str] = {}
        for path in core.content.glob("*.json"):
            try:
                body = json.loads(path.read_text(encoding="utf-8"))
            except ValueError:
                continue
            if not isinstance(body, dict) or (body.get("id"), body.get("version")) not in wanted:
                continue
            if body.get("publishes") in WATCH_SYMBOLS:
                found[str(body["id"])] = str(body["publishes"])
            elif str(body.get("schema", "")).startswith("attachment-rule"):
                found[str(body["id"])] = str(body["id"])  # every attachment the package declares
        _PUBLISHERS[key] = found
    return _PUBLISHERS[key]


def short(name: Any) -> str:
    return str(name).removeprefix(P).removeprefix("rule.")


def summarize(core: Any, outcome: Any) -> dict[str, Any]:
    from packages.derivation.presentation_projection import validate_presentation_model

    base = h.summarize(outcome)
    if outcome.refusal is not None:
        return base
    report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
    model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    try:
        validate_presentation_model(model)
        valid = True
    except Exception as exc:  # noqa: BLE001 — recorded, and the case fails on it
        valid = f"{type(exc).__name__}: {h.scrub(str(exc))[:200]}"
    field_ids = [str((s.get("field") or {}).get("id")) for s in model.get("sections") or []]
    duplicates = sorted(k for k, v in Counter(field_ids).items() if v > 1 and k != "None")
    pubs = publishers(core)
    rows: dict[str, list[Any]] = {}
    row_count: Counter[str] = Counter()
    for row in report.get("dispositions") or []:
        artifact = str(row.get("artifact_id", ""))
        if artifact in pubs:
            row_count[artifact] += 1
            rows[short(artifact)] = [row.get("disposition"), row.get("code"),
                                     [short(m) for m in row.get("missing") or []]]
    fields: dict[str, Any] = {}
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        if field.get("id") not in PROBED_FIELDS:
            continue
        resolved = section.get("resolved") or {}
        disposition = str(resolved.get("disposition"))
        explain = (((field.get("dispositions") or {}).get(
            {"published": "published_value"}.get(disposition, disposition)) or {}).get("explain"))
        fields[short(field["id"])] = {
            "version": field.get("version"), "disposition": disposition, "explain": explain,
            "reasons": [str(r.get("sentence")) for r in resolved.get("reasons") or [] if isinstance(r, dict)]}
    base.update({
        "valid_model": valid, "duplicate_fields": duplicates, "rows": rows,
        "rows_not_one": sorted(short(a) for a in pubs if row_count[a] != 1 and a in row_count) +
        sorted(short(a) for a in pubs if a not in row_count and _expected_row(a)),
        "fields": fields,
        "page_questions": sorted({r for f in fields.values() for r in f["reasons"]} | set(base.get("questions") or [])),
    })
    return base


def _expected_row(artifact: str) -> bool:
    """Every watched publisher records a row in every saturated run."""
    return True


def run(core: Any, acts: Acts, run_id: str) -> dict[str, Any]:
    """``audit_harness.run`` with the richer summary (same coordinator call, same loader entries)."""
    from packages.derivation.live import live_coordinate_run
    from packages.derivation.live_workspace import WorkspaceCapability

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
                return summarize(core, outcome)
        except Exception as exc:  # noqa: BLE001 — a rejected act list is a result, not a crash
            return {"error": type(exc).__name__, "message": h.scrub(str(exc))[:400]}


# ---- cases ------------------------------------------------------------------------

CASES: dict[str, dict[str, Any]] = {}
MODES = ("honest", "base_exception1")


def case(name: str, *, group: str, note: str, expect: str, kinds: set[str] = frozenset(),
         sales: Callable[[Acts], Acts] | None = None, hand: dict[str, Any] | None = None, loss: bool = False,
         answers: dict[str, Any] | None = None, box4: BoxAnswer = "no", box7: BoxAnswer = "no",
         modes: tuple[str, ...] = MODES, designs: tuple[str, ...] = ("final", "decided"),
         asks: tuple[str, ...] = (), pins: dict[str, list[Any]] | None = None,
         post: Callable[[Acts, Any, set[str], str], Acts] | None = None, keep_exc1: bool = False,
         rejects: str | None = None) -> None:
    """``expect``: "values" (``hand`` must publish), "block" (Form 1040 must not publish) or "observe".

    ``rejects``: the act list must be rejected at entry, with this text in the reason.

    ``asks``: substrings each of which some question on the page must contain.
    ``pins``: row (short artifact id) -> [disposition, code, missing] it must record.
    ``post``: applied after the answers (a stage transition that follows them).
    ``keep_exc1``: the case's own Exception 1 answers stand in both modes.
    """
    assert name not in CASES, name
    CASES[name] = dict(group=group, note=note, expect=expect, kinds=set(kinds), sales=sales, hand=hand, loss=loss,
                       answers=answers or {}, box4=box4, box7=box7, modes=modes, designs=designs, asks=asks,
                       pins=pins or {}, post=post, keep_exc1=keep_exc1, rejects=rejects)


def honest_answers(acts: Acts, kinds: set[str], loss: bool) -> dict[str, str | None]:
    """``audit_harness.honest`` for these kinds, with Exception 1 answered from the recorded sales.

    The v2 questions read literally (``audit_harness.honest_exception1``, review F4):
    a sale that nets zero is neither a gain nor a loss.
    """
    answers = h.honest(kinds, loss=loss)
    answers.update({k: v for k, v in h.honest_exception1(acts).items() if v is not None})
    return answers


def build_case(spec: dict[str, Any], mode: str, core: Any, fixes: set[str]) -> Acts:
    acts = h.opened()
    if spec["sales"] is not None:
        acts = spec["sales"](acts)
    answers = {**honest_answers(acts, spec["kinds"], spec["loss"]), **spec["answers"]}
    answers = {k: v for k, v in answers.items() if k not in ("box4", "box7")}
    if mode == "base_exception1" and not spec["keep_exc1"]:
        answers = {k: v for k, v in answers.items() if not k.startswith("exc1")}
    acts = h.answer(acts, core.content, **answers)
    acts = box_answers(acts, core, fixes, spec["box4"], spec["box7"])
    if spec["post"] is not None:
        acts = spec["post"](acts, core, fixes, mode)
    return acts


def verdict(spec: dict[str, Any], result: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    if "error" in result or "refusal" in result:
        reason = str(result.get("message") or result.get("refusal") or "")
        if spec.get("rejects") and spec["rejects"] not in reason:
            return ("rejected at entry BUT CHECK FAILED", {"rejects": [reason[:200], spec["rejects"]]})
        return ("rejected at entry", {})
    problems: dict[str, Any] = {}
    if spec.get("rejects"):
        problems["rejects"] = ["accepted", spec["rejects"]]
    if result.get("valid_model") is not True:
        problems["valid_model"] = result.get("valid_model")
    if result.get("duplicate_fields"):
        problems["duplicate_fields"] = result["duplicate_fields"]
    if result.get("rows_not_one"):
        problems["rows_not_one"] = result["rows_not_one"]
    if result.get("stop") != "saturated":
        problems["stop"] = result.get("stop")
    for needle in spec["asks"]:
        if not any(needle in q for q in result.get("page_questions") or result.get("questions") or []):
            problems.setdefault("asks_missing", []).append(needle)
    for row, want in spec["pins"].items():
        got = (result.get("rows") or {}).get(row)
        if got != want:
            problems.setdefault("pins", {})[row] = [got, want]
    lines = result.get("lines") or {}
    published = all(isinstance(lines.get(k), int) for k in ("form1040.line-16", "form1040.line-34", "form1040.line-37"))
    wrong = probe.mismatches({"hand": spec["hand"]}, result) if spec["hand"] else {}
    if spec["expect"] == "values":
        word = "right" if published and not wrong else ("BLOCKS A RETURN IT SHOULD COMPUTE" if not published
                                                         else "WRONG RETURN PUBLISHED")
    elif spec["expect"] == "block":
        word = "blocks (correct)" if not published else "WRONG RETURN PUBLISHED"
    else:
        word = "observed"
    if wrong and spec["expect"] == "values":
        problems["mismatches"] = wrong
    if problems and word in ("right", "blocks (correct)", "observed"):
        word += " BUT CHECK FAILED"
    return word, problems


# Hand values on the harness wage return (probe.hand).
hand = probe.hand
S = probe.S
seq = probe.seq
with_2a = probe.with_2a
ONLY_1040 = ("form1040.line-7a", "form1040.line-7b", "form1040.line-15", "form1040.line-16", "form1040.line-25b", "form1040.line-34",
             "form1040.line-37")


def hand1040(**kw: Any) -> dict[str, Any]:
    out = hand(**kw)
    return {k: v for k, v in out.items() if k in ONLY_1040}


def strip_answer(key: str) -> Callable[[Acts, Any, set[str], str], Acts]:
    def post(acts: Acts, core: Any, fixes: set[str], mode: str) -> Acts:
        return h.strip(acts, h.ANSWER_FACT[key])
    return post


def strip_closure(fam: str) -> Callable[[Acts, Any, set[str], str], Acts]:
    def post(acts: Acts, core: Any, fixes: set[str], mode: str) -> Acts:
        return h.strip(acts, P + fam + ".source-closure")
    return post


def then(*steps: Callable[[Acts], Acts], kinds: set[str] | None = None, loss: bool = False,
         answers: dict[str, Any] | None = None, box4: BoxAnswer = None, box7: BoxAnswer = None,
         earlier: Callable[[Acts, Any, set[str], str], Acts] | None = None) -> Callable[[Acts, Any, set[str], str], Acts]:
    """A later stage: ``earlier`` (a previous stage's post), then record ``steps`` after the answers already
    given, then (when ``kinds`` is given) answer again as a filer with those sales does, and the box answers."""
    def post(acts: Acts, core: Any, fixes: set[str], mode: str) -> Acts:
        if earlier is not None:
            acts = earlier(acts, core, fixes, mode)
        for step in steps:
            acts = step(acts)
        if kinds is not None:
            again = {**honest_answers(acts, kinds, loss), **(answers or {})}
            again = {k: v for k, v in again.items() if k not in ("box4", "box7")}
            if mode == "base_exception1":
                again = {k: v for k, v in again.items() if not k.startswith("exc1")}
            acts = h.answer(acts, core.content, **again)
        elif answers:
            acts = h.answer(acts, core.content, **answers)
        return box_answers(acts, core, fixes, box4, box7)
    return post


# ---- 2. Empty/nonempty matrix ------------------------------------------------------

case("m_empty", group="M", expect="values", note="Wage return, every sale family closed empty (Q1, Q2, Q3 no; the "
     "covered and code W literal closures), base Exception 1 answers.",
     hand=hand(schedule_d=False))
case("m_empty_exc1_only2a_no", group="M", expect="observe", keep_exc1=True, answers={"exc1_only_2a": "no"},
     designs=("final", "decided", "v81"), note="No sale and no box 2a distribution, but 'only box 2a gains' answered no (false: Exception 1 holds).")
case("m_empty_exc1_nolosses_no", group="M", expect="observe", keep_exc1=True, answers={"exc1_no_losses": "no"},
     designs=("final", "decided", "v81"), note="No sale, 'no capital losses' answered no (false).")
for key, fam in (("q1", "noncovered"), ("q2", "no1099b"), ("q3", "code-b")):
    case(f"m_empty_{key}_unanswered", group="M", expect="block", post=strip_answer(key),
         note=f"Every family closed except the {fam} families: their grouped question is unanswered.")
case("m_empty_covered_unclosed", group="M", expect="block", post=strip_closure("f1099b.covered-st"),
     note="The line 1a family's literal closure is missing.")
case("m_empty_w_unclosed", group="M", expect="block", post=strip_closure("f1099b.covered-w-lt"),
     note="The long-term code W family's literal closure is missing.")
case("m_empty_box4_yes_no_sale", group="M", expect="values", hand=hand(schedule_d=False),
     post=lambda acts, core, fixes, mode: orphan_yes(acts, core) if "statement_box4" in fixes else acts,
     note="No Form 1099-B sale is recorded, but a box 4 yes stands for a statement with no sale: it is not read.")



def strip_exception1(acts: Acts, core: Any, fixes: set[str], mode: str) -> Acts:
    for fact in proto.EXCEPTION1_QUESTIONS:
        acts = h.strip(acts, P + fact)
    return acts


case("m_empty_exc1_unanswered", group="M", expect="block", post=strip_exception1, designs=("final",),
     asks=tuple(proto.EXCEPTION1_QUESTIONS.values()),
     note="Every family closed empty and no Exception 1 answer recorded: the page asks the four Exception 1 "
          "questions in their Decision 2 words (repair exception1_words).")

case("m_2a_only", group="M", expect="values", sales=with_2a(1000), hand=hand1040(cgd=1000, schedule_d=False),
     note="A 1,000 box 2a distribution and no sale; Exception 1 holds (base answers in both modes). Line 7a 1,000, "
          "base 1,000 (line 13), TI 35,250, tax 3,875 (0% band).")
case("m_2a_only_exc1_only2a_no", group="M", expect="observe", sales=with_2a(1000), keep_exc1=True,
     answers={"exc1_only_2a": "no"}, designs=("final", "decided", "v81"), note="A box 2a distribution and no sale, 'only box 2a gains' answered no (false).")
case("m_2a_box_f_loss", group="M", expect="values", kinds={"no1099b"}, loss=True,
     sales=seq(with_2a(1000), S("no1099b", "lt", "m2f", proceeds=0, basis=500)),
     hand=hand(lt=-500, cgd=1000, f8949=True),
     note="A box F sale for 0 with basis 500 beside a 1,000 box 2a distribution: line 15 500, line 16 500, base 500 "
          "(min of lines 15 and 16), TI 34,750, tax 3,875.")

# Exception 1 in both polarities beside a sale: the Schedule D route must not depend on the answers.
POLARITY_SALES = {
    "covered_st": ("covered", "st", {"proceeds": 10000, "basis": 7000}, 3000),
    "noncovered_lt": ("noncovered", "lt", {"proceeds": 6000, "basis": 2000}, 4000),
    "no1099b_st": ("no1099b", "st", {"proceeds": 2500, "basis": 3000}, -500),
    "w_lt": ("w", "lt", {"proceeds": 4000, "basis": 5000, "wash": 300}, -700),
    "codeb_st": ("codeb", "st", {"proceeds": 10000, "basis": 7000, "corrected": 4000}, 6000),
}
for label, (kind, term, kw, gain) in POLARITY_SALES.items():
    for only2a in ("yes", "no"):
        for nolosses in ("yes", "no"):
            case(f"p_{label}_only2a_{only2a}_nolosses_{nolosses}", group="P", expect="values", kinds={kind},
                 loss=gain < 0, sales=S(kind, term, f"p{label}", **kw), keep_exc1=True, modes=("honest",),
                 answers={"exc1_only_2a": only2a, "exc1_no_losses": nolosses},
                 hand=hand(**{term: gain}, f8949=None if kind == "covered" else True),
                 note=f"Exception 1 answered only-box-2a {only2a}, no-capital-losses {nolosses}, beside one sale "
                      f"({kind} {term}, column (h) {gain}).")

# Nonempty and ineligible: the admission reads, paired rows and stale closures.
case("n_covered_lt_says_short", group="N", expect="block", kinds={"covered"},
     sales=S("covered", "lt", "n1", proceeds=10000, basis=7000, long_term="no"),
     pins={"f1099b.covered-lt-txn.admission-check": ["blocked", "DEPENDENCY_INVALID", []]},
     note="A short-term sale (long_term no) recorded on the long-term line 8a family.")
case("n_w_lt_says_short", group="N", expect="block", kinds={"w"}, loss=True,
     sales=S("w", "lt", "n2", proceeds=4000, basis=5000, wash=300, long_term="no"),
     pins={"f1099b.covered-w-lt-txn.admission-check": ["blocked", "DEPENDENCY_INVALID", []]},
     note="A short-term code W sale recorded on the long-term code W family.")
case("n_covered_lt_box1g", group="N", expect="block", kinds={"covered"},
     sales=S("covered", "lt", "n3", proceeds=10000, basis=7000, box_1g_wash_sale_adjustment="yes"),
     pins={"f1099b.covered-lt-txn.admission-check": ["blocked", "DEPENDENCY_INVALID", []]},
     note="A line 8a sale with box 1g checked: it is a code W sale.")
case("n_w_proceeds_row_disagrees", group="N", expect="block", kinds={"w"}, loss=True,
     sales=S("w", "st", "n4", proceeds=4000, basis=5000, wash=300, rows={"proceeds": 3000}),
     pins={"f1099b.covered-w-st-txn.admission-check": ["blocked", "DEPENDENCY_INVALID", []]},
     note="A code W sale of 4,000 whose proceeds row says 3,000.")
case("n_w_adjustment_row_missing", group="N", expect="block", kinds={"w"}, loss=True,
     sales=S("w", "st", "n5", proceeds=4000, basis=5000, wash=300, rows={"adjustment": None}),
     note="A code W sale recorded without its column (g) row.")
case("n_covered_basis_row_missing", group="N", expect="block", kinds={"covered"},
     sales=S("covered", "st", "n6", proceeds=10000, basis=7000, rows={"basis": None}),
     pins={"f1099b.covered-st-txn.admission-check": ["blocked", "DEPENDENCY_ABSENT", ["f1099b.covered-st-txn.basis"]]},
     note="A line 1a sale recorded with its proceeds row and without its basis row.")
case("n_covered_two_sales", group="N", expect="values", kinds={"covered"},
     sales=seq(S("covered", "st", "n7a", proceeds=10000, basis=7000), S("covered", "st", "n7b", proceeds=6000, basis=2000)),
     hand=hand(st=7000), note="Two line 1a sales, each with its own rows: 3,000 + 4,000.")
case("n_w_two_sales", group="N", expect="values", kinds={"w"}, loss=True,
     sales=seq(S("w", "st", "n8a", proceeds=4000, basis=5000, wash=300), S("w", "st", "n8b", proceeds=3000, basis=2000)),
     hand=hand(st=300, f8949=True), note="Two code W sales on one family: -700 and +1,000 (W 0).")
case("n_covered_two_sales_one_disagrees", group="N", expect="block", kinds={"covered"},
     sales=seq(S("covered", "st", "n9a", proceeds=10000, basis=7000),
               S("covered", "st", "n9b", proceeds=6000, basis=2000, rows={"basis": 1000})),
     pins={"f1099b.covered-st-txn.admission-check": ["blocked", "DEPENDENCY_INVALID", []]},
     note="Two line 1a sales; the second's basis row (1,000) differs from the sale (2,000).")
case("n_covered_two_sales_one_rowless", group="N", expect="block", kinds={"covered"},
     sales=seq(S("covered", "st", "n10a", proceeds=10000, basis=7000),
               S("covered", "st", "n10b", proceeds=6000, basis=2000, rows={"proceeds": None, "basis": None})),
     note="Two line 1a sales; the second has no rows while the first has both.")
case("n_box_e_q1_no", group="N", expect="block", kinds={"noncovered"}, answers={"q1": "no"},
     sales=S("noncovered", "lt", "n11", proceeds=6000, basis=2000), note="A box E sale with Q1 answered no.")
case("n_box_c_q2_no", group="N", expect="block", kinds={"no1099b"}, answers={"q2": "no"},
     sales=S("no1099b", "st", "n12", proceeds=2500, basis=1000), note="A box C sale with Q2 answered no.")
case("n_code_b_q3_no", group="N", expect="block", kinds={"codeb"}, answers={"q3": "no"},
     sales=S("codeb", "st", "n13", proceeds=10000, basis=7000, corrected=4000), note="A code B sale with Q3 no.")

# Box 4 and box 7.
for kind in ("covered", "w", "noncovered", "codeb"):
    kw = dict(POLARITY_SALES[{"covered": "covered_st", "w": "w_lt", "noncovered": "noncovered_lt",
                              "codeb": "codeb_st"}[kind]][2])
    term = {"covered": "st", "w": "lt", "noncovered": "lt", "codeb": "st"}[kind]
    case(f"b4_yes_{kind}", group="B", expect="block", kinds={kind}, loss=kind == "w", box4="yes",
         sales=S(kind, term, f"b4{kind}", **kw), pins={"form1040-line25b": ["blocked", "DEPENDENCY_ABSENT", []]},
         note=f"Box 4 withholding on the one {kind} sale's statement: line 25b is refused.")
    case(f"b7_yes_{kind}", group="B", expect="block", kinds={kind}, loss=kind == "w", box7="yes",
         sales=S(kind, term, f"b7{kind}", **kw), pins={"schedule-d-line16": ["blocked", "DEPENDENCY_ABSENT", []]},
         note=f"Box 7 checked on the one {kind} sale's statement: Schedule D line 16 is refused.")
TWO_E = seq(S("noncovered", "lt", "bxa", proceeds=6000, basis=2000), S("noncovered", "lt", "bxb", proceeds=3000, basis=1000))
case("b4_two_statements_one_yes", group="B", expect="block", kinds={"noncovered"}, sales=TWO_E,
     box4={statement_of("bxb"): "yes", "*": "no"}, pins={"form1040-line25b": ["blocked", "DEPENDENCY_ABSENT", []]},
     note="Two box E sales on two statements; the second shows box 4 withholding.")
case("b4_two_statements_one_unanswered", group="B", expect="block", kinds={"noncovered"}, sales=TWO_E,
     box4={statement_of("bxb"): None, "*": "no"}, asks=("box 4",),
     designs=("final",),
     note="Two box E sales on two statements; the second statement's box 4 answer is missing.")
case("b4_same_statement_two_sales", group="B", expect="values", kinds={"noncovered"},
     sales=lambda acts: sale_on(S("noncovered", "lt", "bsa", proceeds=6000, basis=2000)(acts), "noncovered", "lt",
                                "bsb", statement_tag="bsa", proceeds=3000, basis=1000),
     hand=hand(lt=6000, f8949=True), note="Two box E sales on one statement, answered once for that statement.")
case("b4_box_c_only", group="B", expect="values", kinds={"no1099b"},
     sales=S("no1099b", "st", "bc", proceeds=2500, basis=1000), hand=hand(st=1500, f8949=True),
     note="A box C sale only: no Form 1099-B, so neither box question is asked.")
case("b7_yes_gain", group="B", expect="block", kinds={"noncovered"}, box7="yes",
     sales=S("noncovered", "lt", "b7g", proceeds=6000, basis=2000),
     note="Box 7 checked on a statement whose only sale is a gain (no loss to disallow).")
case("b7_two_statements_one_unanswered", group="B", expect="block", kinds={"noncovered"}, sales=TWO_E,
     box7={statement_of("bxb"): None, "*": "no"}, asks=("box 7",),
     designs=("final",),
     note="Two box E sales on two statements; the second statement's box 7 answer is missing.")
case("b47_unanswered", group="B", expect="block", kinds={"noncovered"}, sales=S("noncovered", "lt", "bu",
     proceeds=6000, basis=2000), box4=None, box7=None, asks=("box 4", "box 7"),
     note="One box E sale; neither box question answered.")

# Review F1: a covered or code W amount row with no sale of its own (row_needs_sale).
# h._member records one row under its own tag: a new broker, statement and transaction.
ROW_NEEDS_SALE = "companion presence violated"


def rows(kind: str, term: str, tag: str, **amounts: float) -> Callable[[Acts], Acts]:
    def build(acts: Acts) -> Acts:
        for scalar, amount in amounts.items():
            acts = h._member(acts, kind, term, scalar, amount, tag)
        return h.renumber(acts)
    return build


case("r_f1_covered_extra_rows", group="R", expect="block", kinds={"covered"}, rejects=ROW_NEEDS_SALE,
     sales=seq(S("covered", "st", "rf1a", proceeds=10000, basis=7000), rows("covered", "st", "rf1x", proceeds=5000,
                                                                              basis=1000)),
     modes=("honest",), designs=("final", "track1"),
     note="A line 1a sale 10,000 / 7,000 with its own rows, plus a 5,000 proceeds row and a 1,000 basis row on "
          "another transaction. v81 and the published v82 before the repair: line 1a 7,000, tax 4,715. Correct: "
          "refuse (or line 1a 3,000). The rows have no sale of their own.")
case("r_f1_covered_rows_alone", group="R", expect="block", kinds={"covered"}, rejects=ROW_NEEDS_SALE,
     sales=rows("covered", "st", "rf1b", proceeds=5000, basis=1000), modes=("honest",), designs=("final", "track1"),
     note="The same two rows with no sale recorded. Before the repair: line 1a 4,000, tax 4,355. Correct: refuse "
          "(or 0).")
case("r_f1_covered_lt_rows_alone", group="R", expect="block", kinds={"covered"}, rejects=ROW_NEEDS_SALE,
     sales=rows("covered", "lt", "rf1c", proceeds=5000, basis=1000), modes=("honest",), designs=("final", "track1"),
     note="The same rows on the line 8a family, no sale. Before the repair: line 8a 4,000, line 7a 4,000.")
case("r_f1_w_extra_rows", group="R", expect="block", kinds={"w"}, loss=True, rejects=ROW_NEEDS_SALE,
     sales=seq(S("w", "st", "rf1d", proceeds=4000, basis=5000, wash=300), rows("w", "st", "rf1y", proceeds=5000,
                                                                              basis=1000)),
     modes=("honest",), designs=("final", "track1"),
     note="A code W sale 4,000 / 5,000 (W 300) with its own rows, plus 5,000 / 1,000 rows on another transaction. "
          "Before the repair: line 1b 3,300, tax 4,271. Correct: refuse (or line 1b -700).")
case("r_f1_w_adjustment_row_alone", group="R", expect="block", kinds={"w"}, rejects=ROW_NEEDS_SALE,
     sales=rows("w", "lt", "rf1e", adjustment=300), modes=("honest",), designs=("final",),
     note="A code W column (g) row of 300 with no sale recorded.")
COV_RM = S("covered", "st", "rf1f", proceeds=10000, basis=7000)
case("r_f1_covered_sale_removed", group="R", expect="block", kinds={"covered"}, sales=COV_RM,
     rejects=ROW_NEEDS_SALE, modes=("honest",), designs=("final", "track1"),
     post=then(lambda a: remove_sale(a, "covered", "st", "rf1f", parts=(None,))),
     note="A line 1a sale 10,000 / 7,000, then only the sale removed; its rows stay. Before the repair: line 1a "
          "3,000, tax 4,235. Correct: refuse the removal (or 0, tax 3,875).")
case("r_f1_covered_sale_removed_after_basis_row", group="R", expect="block", kinds={"covered"}, sales=COV_RM,
     rejects="f1099b.covered-st-txn.proceeds|broker=demo.sfa.rf1f.broker", modes=("honest",), designs=("final",),
     post=then(lambda a: remove_sale(a, "covered", "st", "rf1f", parts=("basis", None))),
     note="The basis row removed first, then the sale; the 10,000 proceeds row stays. Correct: refuse (or 0). The "
          "kernel's reverse presence check reads one row per sale (the last pair the loader declares, basis), so "
          "the sale's removal is admitted; the run then refuses (companion provenance missing for the proceeds "
          "row) and nothing publishes.")
case("r_f1_covered_sale_and_rows_removed", group="R", expect="values", kinds={"covered"}, sales=COV_RM,
     modes=("honest",), designs=("final",), hand=hand(schedule_d=False),
     post=then(lambda a: remove_sale(a, "covered", "st", "rf1f"), answers={"exc1_only_2a": "yes"}),
     note="The rows removed, then the sale: nothing is left. Answered again as a filer with no sale (only box 2a "
          "gains yes), the wage return computes (tax 3,875).")

# Review F2: line 7b "Schedule D not required" beside a required Schedule D (line7b_activity).
# The four Exception 1 facts stay at the harness base ("yes" to each). Under the v2 questions those are the
# truthful replies of a filer whose only sale nets zero: no capital gain other than box 2a, and no capital loss.
V2_TRUTHFUL_ZERO = {"exc1_only_2a": None, "exc1_no_losses": None}
case("r_f2_box_c_zero", group="R", expect="values", kinds={"no1099b"}, answers=V2_TRUTHFUL_ZERO,
     sales=S("no1099b", "st", "rf2a", proceeds=0, basis=0), hand=hand(f8949=True), modes=("honest",),
     designs=("final", "track1"),
     note="A box C sale for 0 with basis 0, the Exception 1 facts left yes (truthful under the v2 words). Both "
          "attachments are required, so line 7b must not say Schedule D is not required. Before the repair: "
          "line 7b checked beside both attachments.")
case("r_f2_covered_zero_net_beside_2a", group="R", expect="values", kinds={"covered"}, answers=V2_TRUTHFUL_ZERO,
     sales=seq(with_2a(1000), S("covered", "st", "rf2b", proceeds=5000, basis=5000)), hand=hand(cgd=1000),
     modes=("honest",), designs=("final", "track1"),
     note="A line 1a sale 5,000 / 5,000 beside a 1,000 box 2a distribution, Exception 1 facts yes. Line 15 1,000, "
          "line 16 1,000, base 1,000, TI 35,250, tax 3,875; Schedule D required, so line 7b not checked.")
case("r_f2_box_e_zero_net_beside_2a", group="R", expect="values", kinds={"noncovered"}, answers=V2_TRUTHFUL_ZERO,
     sales=seq(with_2a(1000), S("noncovered", "lt", "rf2c", proceeds=5000, basis=5000)),
     hand=hand(cgd=1000, f8949=True), modes=("honest",), designs=("final", "track1"),
     note="A box E sale 5,000 / 5,000 beside a 1,000 box 2a distribution, Exception 1 facts yes: as above, with "
          "Form 8949.")
case("r_f2_box_e_gain_base_answers", group="R", expect="values", kinds={"noncovered"}, answers=V2_TRUTHFUL_ZERO,
     sales=S("noncovered", "lt", "rf2d", proceeds=6000, basis=2000), hand=hand(lt=4000, f8949=True),
     modes=("honest",), designs=("final", "track1"),
     note="A box E gain with the Exception 1 facts left yes (false: the sale is a gain). The tax does not read them "
          "beside a sale (Decision 1), and line 7b now does not either.")

# ---- 3. Late-member traces ---------------------------------------------------------
V81_TOO = ("final", "decided", "v81")
E1 = S("noncovered", "lt", "t1", proceeds=6000, basis=2000)
case("t1_s0", group="T1", expect="values", hand=hand(schedule_d=False), designs=V81_TOO,
     note="Wage return; every family closed empty (Q1 no). It computes.")
case("t1_s1", group="T1", expect="block", post=then(E1), designs=V81_TOO,
     note="A box E sale (6,000 / 2,000) is recorded after the Q1 no. The no is stale.")
case("t1_s2", group="T1", expect="values", post=then(E1, kinds={"noncovered"}, box4="no", box7="no"),
     designs=V81_TOO, hand=hand(lt=4000, f8949=True),
     note="Q1 yes and the in-class answers; in honest mode Exception 1 answered as the filer must. The tax is "
          "computed through the Schedule D route: TI 38,250, tax 3,875 (0% band), refund 625.")
E2a = S("noncovered", "lt", "t2a", proceeds=6000, basis=2000)
E2b = S("noncovered", "lt", "t2b", proceeds=3000, basis=1000)
case("t2_s0", group="T2", expect="values", kinds={"noncovered"}, sales=E2a, hand=hand(lt=4000, f8949=True),
     note="One box E sale on statement A; box 4 and box 7 answered no. It computes, line 25b 0.")
case("t2_s1", group="T2", expect="block", kinds={"noncovered"}, sales=E2a, post=then(E2b),
     note="A second box E sale, on a new statement B, is recorded after the answers. Statement B shows 1,440 "
          "of box 4 withholding. Q1 yes is stale.")
case("t2_s2", group="T2", expect="block", kinds={"noncovered"}, sales=E2a, post=then(E2b, answers={"q1": "yes"}),
     asks=("box 4",), hand=None,
     note="Q1 yes again. Nothing has asked about statement B's box 4. Correct: line 25b is 1,440 (refund 2,065), "
          "which this return does not compute, so line 25b must not publish 0.")
case("t2_s3_yes", group="T2", expect="block", kinds={"noncovered"}, sales=E2a,
     post=then(E2b, answers={"q1": "yes"}, box4={statement_of("t2b"): "yes", "*": None}),
     pins={"form1040-line25b": ["blocked", "DEPENDENCY_ABSENT", []]},
     note="Statement B answered yes (on decided, the return-level answer becomes yes): line 25b refused.")
case("t2_s3_no", group="T2", expect="values", kinds={"noncovered"}, sales=E2a,
     post=then(E2b, answers={"q1": "yes"}, box4={statement_of("t2b"): "no", "*": None}, box7="no"),
     hand=hand(lt=6000, f8949=True), note="The variant where statement B shows no box 4: it computes.")
case("t2_same_statement", group="T2", expect="values", kinds={"noncovered"}, sales=E2a,
     post=then(lambda a: sale_on(a, "noncovered", "lt", "t2s", statement_tag="t2a", proceeds=3000, basis=1000),
               answers={"q1": "yes"}), hand=hand(lt=6000, f8949=True),
     note="The second sale is on statement A, which the answer already covers: it computes without asking again.")
C2a = S("covered", "st", "t2ca", proceeds=10000, basis=7000)
C2b = S("covered", "st", "t2cb", proceeds=6000, basis=2000)
case("t2c_s1", group="T2", expect="block", kinds={"covered"}, sales=C2a, post=then(C2b), asks=("box 4",),
     note="The same on line 1a: a second covered sale on a new statement (with box 4 withholding) is recorded and "
          "its family closed again. No grouped question goes stale.")
E3b = S("noncovered", "lt", "t3b", proceeds=3000, basis=5000)
case("t3_s0", group="T3", expect="values", kinds={"noncovered"}, sales=S("noncovered", "lt", "t3a", proceeds=6000,
     basis=2000), hand=hand(lt=4000, f8949=True), note="One box E gain on statement A; box 7 answered no.")
case("t3_s2", group="T3", expect="block", kinds={"noncovered"}, loss=False,
     sales=S("noncovered", "lt", "t3a", proceeds=6000, basis=2000), post=then(E3b, answers={"q1": "yes"}),
     asks=("box 7",),
     note="A box E loss (3,000 / 5,000) on a new statement B whose box 7 is checked; Q1 yes again. Correct: the "
          "loss based on the box 1d gross proceeds is not allowed, so Schedule D line 16 must not publish 2,000.")
case("t3_s3_yes", group="T3", expect="block", kinds={"noncovered"},
     sales=S("noncovered", "lt", "t3a", proceeds=6000, basis=2000),
     post=then(E3b, answers={"q1": "yes"}, box7={statement_of("t3b"): "yes", "*": None}),
     pins={"schedule-d-line16": ["blocked", "DEPENDENCY_ABSENT", []]}, note="Statement B answered yes: refused.")
COV4 = S("covered", "st", "t4", proceeds=10000, basis=7000)
case("t4_s0", group="T4", expect="values", kinds={"covered"}, sales=COV4, hand=hand(st=3000), designs=V81_TOO,
     note="A line 1a sale; in honest mode only-box-2a no.")
case("t4_s1_removed", group="T4", expect="observe", kinds={"covered"}, sales=COV4, designs=V81_TOO,
     post=then(lambda a: remove_sale(a, "covered", "st", "t4")),
     note="The sale is removed (the record was a mistake) and its family closed again. In honest mode the "
          "only-box-2a no now has no sale beside it.")
C5 = S("no1099b", "st", "t5", proceeds=0, basis=0)
case("t5_s1", group="T5", expect="block", post=then(C5), designs=V81_TOO,
     note="Wage return, then a box C sale for 0 with basis 0 recorded after the Q2 no.")
case("t5_s2", group="T5", expect="values", post=then(C5, kinds={"no1099b"}), designs=V81_TOO,
     hand=hand(f8949=True), note="Q2 yes and the in-class answers: zero, both attachments required.")

# P0's 81 cases, rerun on the final design (their decided results are probe-output-v82.json).
for name, spec in probe.CASES.items():
    answers = dict(spec["answers"])
    b4, b7 = answers.pop("box4", "no"), answers.pop("box7", "no")
    extra = spec["extra"]
    case(f"p0_{name}", group="P0", expect=spec["expect"], kinds=set(spec["kinds"]), loss=spec["loss"],
         sales=(seq(extra, spec["sales"]) if extra is not None else spec["sales"]), hand=spec["hand"],
         answers=answers, box4=b4, box7=b7, designs=("final",), note=spec["note"])


# ---- execution ----------------------------------------------------------------------

DESIGNS["v81"] = set()


def execute(task: tuple[str, str, str, str]) -> tuple[str, str, str, dict[str, Any]]:
    name, mode, design, core_json = task
    spec = CASES[name]
    core = core_of(json.loads(core_json))
    started = time.monotonic()
    try:
        acts = build_case(spec, mode, core, DESIGNS[design])
    except Exception as exc:  # noqa: BLE001 — an act list the harness cannot build is a result
        result: dict[str, Any] = {"error": type(exc).__name__, "message": h.scrub(str(exc))[:300]}
    else:
        result = run(core, acts, f"demo.sfa.t0.{name}.{mode}.{design}")
    result["seconds"] = round(time.monotonic() - started, 1)
    return name, mode, design, result


FIELD_SENTENCES: dict[str, dict[str, str]] = {}


def compact(result: dict[str, Any]) -> dict[str, Any]:
    if "error" in result or "refusal" in result:
        return {k: result[k] for k in ("error", "message", "refusal") if k in result}
    lines = result.get("lines") or {}
    fields = {}
    for name, field in (result.get("fields") or {}).items():
        FIELD_SENTENCES.setdefault(f"{name} {field['version']}", {})[field["disposition"]] = field["explain"]
        if field["reasons"]:
            fields[name] = field["reasons"]
    rows = {k: v for k, v in (result.get("rows") or {}).items() if v[0] != "published"}
    return {"lines": {k: lines.get(k) for k in probe.KEPT_LINES if k in lines}, "attachments": result.get("attachments"),
            "base": (result.get("symbols") or {}).get("capital-gains.selected-preferential-base"),
            "rows": rows, "field_reasons": fields, "questions": result.get("page_questions")}


def run_cases(workers: int, prefixes: list[str]) -> None:
    """``prefixes``: case-name prefixes; ``--design=<name>`` runs only that design's runs (repeatable)."""
    only = {p.split("=", 1)[1] for p in prefixes if p.startswith("--design=")}
    prefixes = [p for p in prefixes if not p.startswith("--design=")]
    names = [n for n in CASES if not prefixes or any(n.startswith(p) for p in prefixes)]
    chosen = {n: [d for d in CASES[n]["designs"] if not only or d in only] for n in names}
    used = sorted({d for n in names for d in chosen[n]} - {"v81"})
    cores = build_designs(tuple(used))
    core_json = {d: json.dumps(cores[d]) for d in used} | {"v81": "null"}
    tasks = [(n, m, d, core_json[d]) for n in names for m in CASES[n]["modes"] for d in chosen[n]]
    payload = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    section = payload.setdefault("cases", {})
    counts: Counter[str] = Counter()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for name, mode, design, result in pool.map(execute, tasks):
            spec = CASES[name]
            word, problems = verdict(spec, result)
            entry = section.setdefault(name, {})
            entry.update({"group": spec["group"], "note": spec["note"], "expect": spec["expect"], "hand": spec["hand"]})
            entry[f"{design}/{mode}"] = {"verdict": word, "problems": problems, "result": compact(result)}
            counts[f"{design}: {word}"] += 1
            print(f"{name:44s} {design:8s} {mode:16s} {word:44s} {json.dumps(problems)[:160]} {result.get('seconds')}",
                  flush=True)
    payload["designs"] = payload.get("designs", {}) | {d: cores[d]["build"] for d in used}
    sentences = payload.setdefault("field_sentences", {})
    for field_key, by_disposition in FIELD_SENTENCES.items():
        sentences.setdefault(field_key, {}).update(by_disposition)
    payload["verdicts"] = verdict_counts(section)
    OUT.write_text(dump(payload), encoding="utf-8")
    print(json.dumps(dict(sorted(counts.items())), indent=1))


# Rows kept in the output: the ones that say why a watched line is blocked (the lines carry the rest).
WHY = ("form1040-line16", "form1040-line7a", "selected-preferential-base", "form1040-line25b", "schedule-d-line16")
# Cases whose field reasons are kept (the presentation probe); elsewhere ``questions`` lists the sentences.
PRESENTATION_CASES = ("m_empty", "m_empty_q1_unanswered", "m_empty_covered_unclosed", "t1_s1", "t1_s2", "t2_s2",
                      "t2_s3_yes", "t3_s2", "b47_unanswered", "b4_yes_noncovered", "b7_yes_noncovered",
                      "n_covered_basis_row_missing", "n_w_proceeds_row_disagrees", "t5_s2", "m_2a_only",
                      "p0_c2_w_full_disallowance", "p0_d3_covered_zero_zero", "p0_a1_direct_flagged_wash",
                      "m_empty_exc1_unanswered")


def shrink(payload: dict[str, Any]) -> dict[str, Any]:
    for name, entry in (payload.get("cases") or {}).items():
        final = {k: v for k, v in entry.items() if k.startswith("final/")}
        for key, run_ in entry.items():
            if not isinstance(run_, dict) or "result" not in run_:
                continue
            result = run_["result"]
            result["rows"] = {k: v for k, v in (result.get("rows") or {}).items()
                              if k in WHY or k.startswith("attachment.") or k.endswith(("-check", "-count"))}
            if name not in PRESENTATION_CASES:
                result.pop("field_reasons", None)
            result = {k: v for k, v in result.items() if v not in (None, [], {})}
            run_["result"] = result
        for key, run_ in list(entry.items()):
            if key.startswith("decided/") and isinstance(run_, dict) and "result" in run_:
                twin = final.get("final/" + key.split("/", 1)[1])
                if twin is not None and twin.get("result") == run_["result"] and twin.get("verdict") == run_["verdict"]:
                    entry[key] = {"same_as_final": True, "verdict": run_["verdict"]}
    return payload


def dump(payload: dict[str, Any]) -> str:
    """One line per case, so the output stays small and diffs stay readable."""
    payload = shrink(payload)
    lines = ["{"]
    keys = sorted(payload)
    for i, key in enumerate(keys):
        end = "," if i < len(keys) - 1 else ""
        value = payload[key]
        if isinstance(value, dict) and key in ("cases", "field_sentences", "surface"):
            lines.append(f" {json.dumps(key)}: {{")
            names = sorted(value)
            for j, name in enumerate(names):
                comma = "," if j < len(names) - 1 else ""
                lines.append(f"  {json.dumps(name)}: {json.dumps(value[name], sort_keys=True)}{comma}")
            lines.append(f" }}{end}")
        else:
            lines.append(f" {json.dumps(key)}: {json.dumps(value, sort_keys=True)}{end}")
    lines.append("}")
    return h.scrub("\n".join(lines)) + "\n"


def verdict_counts(section: dict[str, Any]) -> dict[str, int]:
    out: Counter[str] = Counter()
    for entry in section.values():
        for key, run_ in entry.items():
            if isinstance(run_, dict) and "verdict" in run_:
                out[f"{key.split('/')[0]}: {run_['verdict']}"] += 1
    return dict(sorted(out.items()))


def main() -> None:
    args = sys.argv[1:]
    command = args.pop(0) if args else "cases"
    if command == "cases":
        workers = int(args.pop(0)) if args and args[0].isdigit() else 8
        run_cases(workers, args)
    elif command == "rerun":
        run_rerun(args)
    elif command == "surface":
        run_surface()
    elif command == "shrink":
        OUT.write_text(dump(json.loads(OUT.read_text(encoding="utf-8"))), encoding="utf-8")
    else:
        raise SystemExit(f"unknown command {command}")



# ---- 5. The 213 pinned v81 returns ---------------------------------------------------

RERUN_ACTS: dict[str, Any] = {}
DESIGNS["final_no_paired"] = set(proto.SWITCHES) - {"paired_rows"}
COUNT_ROW = ("count",)
LINE_NUMBERS = ("form1040.line-7a", "form1040.line-15", "form1040.line-16", "form1040.line-25b", "form1040.line-34",
                "form1040.line-37")


def rerun_init(acts_path: str) -> None:
    RERUN_ACTS.update(json.loads(Path(acts_path).read_text(encoding="utf-8")))


def rerun_execute(task: tuple[str, str, str, str]) -> tuple[str, str, str, dict[str, Any]]:
    group, name, variant, core_json = task
    acts = RERUN_ACTS[group][name]
    design = {"v81": "v81", "final": "final", "final_unanswered": "final", "final_no_paired": "final_no_paired"}[variant]
    core = core_of(json.loads(core_json))
    if variant in ("final", "final_no_paired"):
        acts = box_answers(acts, core, DESIGNS[design], "no", "no")
    return group, name, variant, run(core, acts, f"demo.sfa.t0.rerun.{group}.{name}.{variant}")


def numbers_changed(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    """Lines that publish a number on both runs and differ: a different published number."""
    la, lb = a.get("lines") or {}, b.get("lines") or {}
    return {k: [la[k], lb.get(k)] for k in la if isinstance(la[k], (int, float)) and isinstance(lb.get(k), (int, float))
            and la[k] != lb[k]}


# What a row may newly wait on under Decisions 1 and 5: a sale count, or line 25b and what adds it up.
GROWN_ALLOWED = ("payments.line25b", "payments.line25d")


def row_change_allowed(a: list[Any] | None, b: list[Any] | None, *, may_appear: bool, new_publisher: bool) -> bool:
    """A watched row's change that only says the row now also waits on a sale count (Decisions 1 and 5)."""
    if a == b:
        return True
    if a is None and b is not None and new_publisher:
        return True  # a publisher v82 adds (the box C and F counts) records its row
    if a is None or b is None:
        return may_appear and a is None and b is not None and b[0] == "blocked"
    grown = [m for m in b[2] if m not in a[2]]
    return a[0] == b[0] and a[1] == b[1] and [m for m in b[2] if m in a[2]] == a[2] and all(
        m.endswith("-count") or m in GROWN_ALLOWED for m in grown)


def watched_rows_explained(a: dict[str, Any], b: dict[str, Any]) -> list[str]:
    """Watched rows (untruncated) whose change is not a count dependency; empty when every change is one."""
    ra, rb = a.get("rows") or {}, b.get("rows") or {}
    bad = []
    for key in sorted(set(ra) | set(rb)):
        may_appear = key in ("form1040-line25b",) or key.endswith("-count")
        new_publisher = key in ("f8949-no1099b-st-count", "f8949-no1099b-lt-count")
        if not row_change_allowed(ra.get(key), rb.get(key), may_appear=may_appear, new_publisher=new_publisher):
            if key == "form1040-line25b" and (ra.get(key) or [None])[0] != "blocked" and (rb.get(key) or [None])[0] == "blocked" \
                    and all(m.endswith("-count") for m in rb[key][2]):
                continue
            bad.append(key)
    return bad


def classify(runs: dict[str, dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    """Which decided change explains the difference between v81 and the final v82, or "UNCLASSIFIED".

    Compared: every watched line and attachment disposition, every page question, and the untruncated
    (disposition, code, missing) of every watched publisher (``rows``).
    """
    v81, final = runs["v81"], runs["final"]
    diff = rerun_mod.difference(v81, final)
    if not diff:
        return "identical", {}
    if "error" not in v81 and ROW_NEEDS_SALE in str(final.get("message") or ""):
        # row_needs_sale (review F1): the act list records a direct or code W row with no sale of its own.
        return "D3 row_needs_sale: a row with no sale of its own is refused at entry", diff
    if numbers_changed(v81, final):
        return "UNCLASSIFIED: a published number changed", diff
    no_paired = runs["final_no_paired"]
    if numbers_changed(no_paired, final):
        return "UNCLASSIFIED: paired_rows changed a number", diff
    label = []
    if rerun_mod.difference(no_paired, final):
        label.append("D3 paired_rows")
    rest = rerun_mod.difference(v81, no_paired)
    if rest:
        if set(rest) - {"lines", "blocked_rows", "attachments"}:
            return "UNCLASSIFIED", diff
        line_changes = rest.get("lines") or {}
        v81_1040_blocked = not all(isinstance((v81.get("lines") or {}).get(k), (int, float))
                                   for k in ("form1040.line-16", "form1040.line-34", "form1040.line-37"))
        attachments_same = all((v81.get("attachments") or {}).get(k) == (no_paired.get("attachments") or {}).get(k)
                               for k in set(v81.get("attachments") or {}) | set(no_paired.get("attachments") or {}))
        if watched_rows_explained(v81, no_paired) or not attachments_same:
            return "UNCLASSIFIED", diff
        if line_changes:
            if set(line_changes) != {"form1040.line-25b"} or not v81_1040_blocked or \
                    line_changes["form1040.line-25b"][1] != "blocked":
                return "UNCLASSIFIED", diff
            label.append("D5 line 25b waits on an unclosed family")
        else:
            label.append("D1 a count row waits on an unclosed family")
    return " + ".join(label) or "UNCLASSIFIED", diff


def run_rerun(args: list[str]) -> None:
    """``rerun <acts.json> [workers] [raw.json] [max]``.

    With ``raw.json`` (outside the repository) the runs are kept there and the
    command resumes: it runs only the runs ``raw.json`` lacks, at most ``max``
    of them, and writes the report once every run is present.
    """
    acts_path = args[0]
    workers = int(args[1]) if len(args) > 1 else 8
    limit = int(args[3]) if len(args) > 3 else None
    expected = json.loads(rerun_mod.EXPECTED.read_text(encoding="utf-8"))
    names = [(g, n) for g in ("case", "v80", "neighbour") for n in sorted(expected[g])]
    variants = ("v81", "final", "final_unanswered", "final_no_paired")
    results: dict[tuple[str, str], dict[str, Any]] = {}

    def go(tasks: list[tuple[str, str, str, str]]) -> None:
        with ProcessPoolExecutor(max_workers=workers, initializer=rerun_init, initargs=(acts_path,)) as pool:
            for group, name, variant, result in pool.map(rerun_execute, tasks, chunksize=2):
                results.setdefault((group, name), {})[variant] = result
                print(group, name, variant, flush=True)

    raw = Path(args[2]).resolve() if len(args) > 2 else None
    if raw is not None and REPO in raw.parents:
        raise SystemExit("keep the raw runs outside the repository")
    if raw is not None and raw.exists():
        results.update({tuple(k.split("/", 1)): v for k, v in json.loads(raw.read_text(encoding="utf-8")).items()})
    todo = [(g, n, v) for g, n in names for v in variants if v not in results.get((g, n), {})]
    if limit is not None:
        todo = todo[:limit]
    if todo:
        cores = build_designs(("final", "final_no_paired"))
        core_json = {"v81": "null", "final": json.dumps(cores["final"]),
                     "final_unanswered": json.dumps(cores["final"]), "final_no_paired": json.dumps(cores["final_no_paired"])}
        go([(g, n, v, core_json[v]) for g, n, v in todo])
        if raw is not None:
            raw.write_text(json.dumps({f"{g}/{n}": v for (g, n), v in results.items()}) + "\n", encoding="utf-8")
    missing = sum(1 for g, n in names for v in variants if v not in results.get((g, n), {}))
    if missing:
        print(f"{missing} runs still to go; run the command again", flush=True)
        return
    p0 = json.loads((HERE / "rerun-output.json").read_text(encoding="utf-8"))
    report: dict[str, Any] = {"returns": len(names), "fixture_check": {}, "classes": {}, "changed": {},
                              "same_as_p0_decided": [], "differs_from_p0_decided": [], "unanswered": {},
                              "rows_not_one": {}, "invalid_models": []}
    for g, n in names:
        key = f"{g}/{n}"
        runs = results[(g, n)]
        pinned = expected[g][n] if g == "case" else expected[g][n]["v81"]
        mismatch = rerun_mod.fixture_mismatch(pinned, runs["v81"])
        if mismatch:
            report["fixture_check"][key] = mismatch
        label, diff = classify(runs)
        report["classes"].setdefault(label, []).append(key)
        if diff:
            p0_diff = {k: v for k, v in (p0["changed"].get(key) or {}).items() if not k.startswith("form1040_")}
            (report["same_as_p0_decided"] if p0_diff == diff else report["differs_from_p0_decided"]).append(key)
            report["changed"][key] = {"form1040_v81": rerun_mod.form1040(runs["v81"]),
                                      "form1040_final": rerun_mod.form1040(runs["final"]), "class": label, **diff}
        unanswered = runs["final_unanswered"]
        report["unanswered"][key] = {"form1040": rerun_mod.form1040(unanswered),
                                     "records_1099b_sale": bool(sale_statements(RERUN_ACTS[g][n])) if RERUN_ACTS else None,
                                     "line25b": (unanswered.get("lines") or {}).get("form1040.line-25b"),
                                     "sd16": (unanswered.get("lines") or {}).get("schedule-d.line-16"),
                                     "box_questions": [q for q in unanswered.get("page_questions") or []
                                                       if "box 4" in q or "box 7" in q]}
        for variant, result in runs.items():
            if result.get("rows_not_one"):
                report["rows_not_one"][f"{key} {variant}"] = result["rows_not_one"]
            if "valid_model" in result and result["valid_model"] is not True:
                report["invalid_models"].append(f"{key} {variant}")
    if not RERUN_ACTS:
        rerun_init(acts_path)
        for key, entry in report["unanswered"].items():
            g, n = key.split("/", 1)
            entry["records_1099b_sale"] = bool(sale_statements(RERUN_ACTS[g][n]))
    report["summary"] = {"fixture_mismatches": len(report["fixture_check"]),
                         "classes": {k: len(v) for k, v in sorted(report["classes"].items())},
                         "same_as_p0_decided": len(report["same_as_p0_decided"]),
                         "differs_from_p0_decided": len(report["differs_from_p0_decided"]),
                         "unanswered_publishing_1040": sorted(k for k, u in report["unanswered"].items()
                                                              if isinstance(u["form1040"][2], (int, float))
                                                              and isinstance(u["form1040"][4], (int, float))),
                         "unanswered_publishing_1040_with_a_1099b_sale": sorted(
                             k for k, u in report["unanswered"].items() if u["records_1099b_sale"]
                             and isinstance(u["form1040"][2], (int, float)) and isinstance(u["form1040"][4], (int, float))),
                         "rows_not_one": len(report["rows_not_one"]), "invalid_models": len(report["invalid_models"])}
    (HERE / "track0-rerun-output.json").write_text(h.scrub(json.dumps(report, indent=1, sort_keys=True)) + "\n",
                                                    encoding="utf-8")
    print(json.dumps(report["summary"], indent=1))


# ---- 6. The static integration surface -------------------------------------------------

SURFACE_SYMBOLS = (
    "tax.total-tax", "tax.line24-total-tax", "payments.line25b", "payments.line33", "payments.line34-overpaid",
    "payments.line37-amount-owed", "capital-gains.line7a-total", "capital-gains.selected-preferential-base",
    "form8949.disposition", "schedule-d.disposition", "schedule-d.line-16",
    "f8949.no1099b-st-count", "f8949.no1099b-lt-count",
    *(f"f1099b.{k}-{t}-txn.admission-check" for k in ("covered", "covered-w") for t in ("st", "lt")),
    proto.BOX4_STATEMENT, proto.BOX7_STATEMENT, proto.BOX4, proto.BOX7,
)


def run_surface() -> None:
    cores = build_designs(("final",))
    content = Path(cores["final"]["content"])
    package = json.loads((content / f"package.core-calculations.{proto.TO['package']}.json").read_text(encoding="utf-8"))
    wanted = {(m["id"], m["version"]) for m in package["members"]}
    bodies: dict[tuple[str, str], dict[str, Any]] = {}
    for path in content.glob("*.json"):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(body, dict) and (body.get("id"), body.get("version")) in wanted:
            bodies[(body["id"], body["version"])] = body
    out: dict[str, Any] = {"members_resolved": len(bodies), "members_listed": len(wanted)}
    for name in SURFACE_SYMBOLS:
        symbol = P + name
        quoted = json.dumps(symbol)
        publishers_, fields, consumers = [], [], []
        for (mid, ver), body in sorted(bodies.items()):
            tag = f"{short(mid)} {ver}"
            text = json.dumps({k: v for k, v in body.items() if k not in ("id", "notes", "title", "label")})
            if body.get("publishes") == symbol:
                publishers_.append(tag)
            elif body.get("binds_symbol") == symbol:
                fields.append(tag)
            elif quoted in text:
                consumers.append(tag)
        out[name] = {"publishers": publishers_, "form_fields": fields, "consumers": consumers}
    payload = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    payload["surface"] = out
    OUT.write_text(dump(payload), encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
