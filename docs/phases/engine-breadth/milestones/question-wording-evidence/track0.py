"""Track 0 adversarial closure of question wording: live v86 against scratch core v87.

Evidence for docs/phases/engine-breadth/milestones/question-wording.md.
Charter: docs/reviews/question-wording/charter-track0.md.
Gate: PROJECT_PLANNING.md, "Track 0 Adversarial Closure Gate".

Every case is one live_coordinate_run of synthetic demo.* findings, on
published core v86 and on the scratch core v87 that prototype.py builds
outside the repository. A question is answered the way a truthful filer
reads its words on that core, so one case can carry a different act list per
core. Hand values come from the 2025 instructions (law.json), never from a
publication. On v87 the act log also adopts the three bundle successors, the
way a workspace re-adopts a revised bundle (the kernel supersedes the fact
type on re-adoption).

This module assigns nothing on another module. It loads probe.py and the
recorded v83 test under names no other module uses, and reads them. The
scratch core's two loader entries are lent for one run by the audit
harness's own ``loader_entries`` context, which restores them.

    python3 track0.py cases <scratch>/core.json <i> <n> <scratch>/part-<i>.json
    python3 track0.py merge-cases <scratch>/core.json <scratch>/part-*.json
    python3 track0.py reuse <scratch>/core.json
    python3 track0.py neighbour <scratch>/core.json <i> <n> <scratch>/nb-<i>.json
    python3 track0.py merge-neighbour <scratch>/nb-*.json
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

P = "tax.us.2025."
CONTENT = REPO / "packages/content/tax/2025"
Acts = list[dict[str, Any]]

WATCH = (
    "schedule-d.line-1a", "schedule-d.line-1b", "schedule-d.line-7", "schedule-d.line-8a",
    "schedule-d.line-8b", "schedule-d.line-15", "schedule-d.line-16",
    "form1040.line-7a", "form1040.line-7b", "form1040.line-12e", "form1040.line-13b",
    "form1040.line-15", "form1040.line-16", "schedule1.line-21",
)
SYMBOLS = (
    "schedule-d-required.conclusion", "schedule1.line21-sli-deduction", "schedule1a.line36a-taxpayer",
    "schedule1a.line36b-spouse", "f1099b.covered-w-st-adjustment-subtotal",
    "f1099b.covered-w-lt-adjustment-subtotal",
)
TITLED = (
    P + "exception1.only-box2a-capital-gains", P + "sli-scope.not-claimed-as-dependent",
    P + "taxpayer-over-65", P + "taxpayer-blind", P + "spouse-over-65", P + "spouse-blind",
)
SUCCESSOR_BUNDLES = ("exception1.bundle.v2.json", "sli-scope.bundle.v2.json", "core_calculations.bundle.v3.json")
ONLY2A = P + "exception1.only-box2a-capital-gains"
NO_LOSSES = P + "exception1.no-capital-losses"
SLI_FACT = P + "sli-scope.not-claimed-as-dependent"
MFJ = "married_filing_jointly"


# ---- loading ---------------------------------------------------------------------------


def _module(name: str, path: Path) -> Any:
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def probe() -> Any:
    return _module("qw_t0_probe", HERE / "probe.py")


def rerun() -> Any:
    return _module("qw_t0_rerun", HERE / "rerun.py")


def harness() -> Any:
    return probe().load_harness()


def v86() -> Any:
    return harness().Core("v86", "v84", "v84")


def v87(core_path: Path) -> Any:
    body = json.loads(core_path.read_text(encoding="utf-8"))
    return harness().Core(body["version"], body["registry"], body["release_version"],
                          content=Path(body["content"]), releases=Path(body["releases"]),
                          loader_from=body.get("loader_from"))


def words(core: Any) -> dict[str, str]:
    """The sentence each changed question carries on ``core``, read from its own content."""
    def read(name: str, field: str) -> str:
        return str(json.loads((core.content / name).read_text(encoding="utf-8"))[field])
    new = core.version != "v86"
    w = "v4" if new else "v3"
    return {
        "wash_st": read(f"closure-mapping.f1099b-covered-w-st-adjustment.{w}.json", "closure_question"),
        "wash_lt": read(f"closure-mapping.f1099b-covered-w-lt-adjustment.{w}.json", "closure_question"),
        "only_box2a": read(f"input-question.exception1-only-box2a-capital-gains.{'v3' if new else 'v2'}.json", "question"),
        "sli": read(f"input-question.sli-scope-not-claimed-as-dependent.{'v2' if new else 'v1'}.json", "question"),
    }


def titles(core: Any) -> dict[str, str]:
    found = {}
    names = SUCCESSOR_BUNDLES if core.version != "v86" else (
        "exception1.bundle.json", "sli-scope.bundle.json", "core_calculations.bundle.v2.json")
    for name in names:
        for fact in json.loads((core.content / name).read_text(encoding="utf-8"))["fact_types"]:
            if fact["id"] in TITLED:
                found[fact["id"].removeprefix(P)] = str(fact["title"])
    return found


# ---- running ---------------------------------------------------------------------------


def scrub(text: str) -> str:
    text = text.replace(str(REPO), ".")
    return re.sub(r"/(?:Users|private|tmp|var|opt)/\S+", "<path>", text)


def _num(value: Any) -> Any:
    """A whole number as an int, whether the publication carries it as a float or a decimal string."""
    if isinstance(value, str):
        try:
            number = float(value)
        except ValueError:
            return value
        return int(number) if number.is_integer() else number
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def readopt(acts: Acts, core: Any) -> Acts:
    """On a successor core, the workspace re-adopts the three revised bundles."""
    if core.version == "v86":
        return acts
    h = harness()
    out = copy.deepcopy(acts)
    for name in SUCCESSOR_BUNDLES:
        body = json.loads((core.content / name).read_text(encoding="utf-8"))
        h._add(out, "bundle-adoption", {"bundle": body})
    return h.renumber(out)


def summarize(outcome: Any) -> dict[str, Any]:
    if outcome.refusal is not None:
        return {"outcome": "refused", "reason": outcome.refusal.reason,
                "detail": scrub(str(outcome.refusal.detail))[:300]}
    report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
    model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    lines: dict[str, Any] = {}
    asked: dict[str, list[str]] = {}
    for section in model.get("sections") or []:
        field_id = str((section.get("field") or {}).get("id") or "").removeprefix(P)
        resolved = section.get("resolved") or {}
        disposition = str(resolved.get("disposition"))
        sentences = [scrub(str(r.get("sentence") or "").strip()) for r in resolved.get("reasons") or []
                     if isinstance(r, dict) and str(r.get("sentence") or "").strip()]
        if sentences and "blocked" in disposition:
            asked[field_id] = sentences
        if field_id in WATCH:
            value = resolved.get("value")
            lines[field_id] = disposition if value is None or "blocked" in disposition else _num(value)
    shown_titles: dict[str, list[str]] = {}

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            fact = node.get("factTypeId")
            if fact in TITLED and isinstance(node.get("factTypeTitle"), str):
                bucket = shown_titles.setdefault(str(fact).removeprefix(P), [])
                if node["factTypeTitle"] not in bucket:
                    bucket.append(node["factTypeTitle"])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(model)
    symbols = {}
    for pub in outcome.publications or ():
        short = str(pub.finding.get("symbol") or "").removeprefix(P)
        if short in SYMBOLS:
            symbols[short] = _num(pub.finding.get("value"))
    questions = sorted({s for sentences in asked.values() for s in sentences if s.endswith("?")})
    return {
        "outcome": "success",
        "stop": report.get("stop_reason"),
        "lines": lines,
        "symbols": symbols,
        "questions": questions,
        "asked_on": {key: value for key, value in sorted(asked.items())},
        "titles_shown": shown_titles,
    }


def execute(core: Any, acts: Acts, run_id: str) -> dict[str, Any]:
    """The audit harness's coordinator call, with this module's own summary."""
    h = harness()
    surface = core.surface()
    with h.loader_entries(core):
        try:
            finished = h._handover(h._finish(readopt(acts, core), package_path=core.package_path,
                                             package_version=core.version, release_path=core.release_path,
                                             release_version=core.release_version, note=run_id),
                                   surface=surface, reconfirm=True)
            with tempfile.TemporaryDirectory() as tmp:
                outcome = h.live_coordinate_run(
                    h.WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO, authoritative_acts=finished,
                    workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": h.YEAR},
                    scope_user=h.ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
                    governance_pins=[], surface=surface, output_name="out.json")
                return summarize(outcome)
        except Exception as exc:  # noqa: BLE001 - a rejected act list is a result
            return {"outcome": "error", "error": type(exc).__name__, "message": scrub(str(exc))[:300]}


# ---- act building ----------------------------------------------------------------------


def complete() -> Acts:
    return probe().complete(harness())


def sales(kind_term: list[tuple[str, str, float, float, float]], *, only2a: str | None, losses: str = "yes") -> Acts:
    """Sales answered as the recorded returns are, with the Exception 1 answers given."""
    p, h = probe(), harness()
    acts = p.sale_return(h, kind_term)
    if only2a is None:
        acts = h.strip(acts, ONLY2A)
    else:
        acts = h.say(acts, ONLY2A, only2a, "only2a")
    return h.say(acts, NO_LOSSES, losses, "noloss")


def strip(acts: Acts, fact: str) -> Acts:
    return harness().strip(acts, fact)


def say(acts: Acts, fact: str, value: object, tag: str) -> Acts:
    return harness().say(acts, fact, value, tag)


def closure(term: str) -> str:
    return P + f"f1099b.covered-w-{term}-adjustment.source-closure"


def close_no(acts: Acts, term: str) -> Acts:
    """The adjustment closure answered no: a false closure assertion at the family's current horizon."""
    h = harness()
    fam = P + f"f1099b.covered-w-{term}-adjustment"
    out = strip(acts, closure(term))
    head = h.horizons(out, fam)[-1]
    h._add(out, "assertion", {"finding": h._attested(
        f"demo.qw.t0.{term}.closure-no", f"{closure(term)}|family-horizon={head},tax-year={h.YEAR}", False)})
    return h.renumber(out)


def sli(claimed: str | None, joint: bool = False) -> Acts:
    acts = probe().sli_return(harness(), claimed)
    return probe().mfj(harness(), acts) if joint else acts


def unclosed_member(acts: Acts, kind: str, term: str, scalar: str | None, value: object, tag: str) -> Acts:
    """A member added to a family after its closure was answered, with no new closure answer.

    The audit harness's ``sale`` re-closes each family it adds to. This adds the
    member transition alone, so the earlier closure stays on the earlier horizon.
    """
    h = harness()
    fam = h.family_id(kind, term, scalar)
    out = copy.deepcopy(acts)
    declared = h._identity(out, kind, tag)
    head = h.horizons(out, fam)[-1]
    count = len(h.horizons(out, fam))
    h._add(out, "member-transition", {
        "family": {"id": fam, "version": h.SALE_KINDS[kind]["version"]},
        "scope": {"tax-year": h.YEAR, "subject": "demo.primary"},
        "member": {"action": "assert", "finding": h._attested(
            f"demo.qw.t0.{tag}.{fam.removeprefix(P)}.member{count}",
            h.fact_id_for(h.member_fact(kind, term, scalar), declared), value)},
        "successor": {"id": f"demo.qw.t0.{tag}.{fam.removeprefix(P)}.h{count}", "predecessor": head},
    })
    return h.renumber(out)


def late_wash_sale(acts: Acts, term: str) -> Acts:
    """A covered wash sale (500, 700, box 1g 200) added to all four of its families, closures not re-answered."""
    h = harness()
    tag = f"late-w-{term}"
    value = {"proceeds": 500.0, "basis": 700.0, "covered_security": "yes", "basis_reported_to_irs": "yes",
             "long_term": "yes" if term == "lt" else "no", "box_1g_wash_sale_adjustment": "yes",
             "box_1g_wash_sale_disallowed_amount": 200.0, **{flag: "no" for flag in h.FLAGS}}
    acts = unclosed_member(acts, "w", term, None, value, tag)
    for scalar, amount in (("proceeds", 500.0), ("basis", 700.0), ("adjustment", 200.0)):
        acts = unclosed_member(acts, "w", term, scalar, amount, tag)
    test = probe().v83_track0()
    track = test.track0()
    acts = track.sfa_t0.box_answers(acts, track.V82, set(track.sfa_t0.DESIGNS["final"]), "no", "no")
    return test.with_zero(track, acts, v86())


def reclose(acts: Acts, term: str, tag: str) -> Acts:
    """Every covered-w family of ``term`` closed again at its current horizon (the truthful yes)."""
    h = harness()
    out = copy.deepcopy(acts)
    for scalar in (None, "proceeds", "basis", "adjustment"):
        fam = h.family_id("w", term, scalar)
        out = h.strip(out, fam + ".source-closure")
        h._close(out, fam + ".source-closure", h.horizons(out, fam)[-1], f"demo.qw.t0.{tag}.{fam.removeprefix(P)}.close")
    return h.renumber(out)


def late_gain_sale(acts: Acts) -> Acts:
    """A covered short-term gain sale (1,000, 800) added after Exception 1 was answered yes; Exception 1 kept."""
    p, h = probe(), harness()
    acts = h.sale(acts, "covered", "st", proceeds=1000.0, basis=800.0, tag="late-gain")
    answers = h.honest({"covered"})
    answers["exc1_only_2a"] = None
    acts = h.answer(acts, **answers)
    test = p.v83_track0()
    track = test.track0()
    acts = track.sfa_t0.box_answers(acts, track.V82, set(track.sfa_t0.DESIGNS["final"]), "no", "no")
    return test.with_zero(track, acts, v86())


# ---- cases -----------------------------------------------------------------------------

ST_GAIN = [("covered", "st", 1000.0, 800.0, 0.0)]
LT_GAIN = [("covered", "lt", 1000.0, 800.0, 0.0)]
ST_WASH = [("w", "st", 500.0, 700.0, 200.0)]
ZERO = [("covered", "st", 1000.0, 1000.0, 0.0)]
NOSALE = {"form1040.line-7a": 0, "form1040.line-15": 34250, "form1040.line-16": 3875}
ST_200 = {"form1040.line-7a": 200, "form1040.line-15": 34450, "form1040.line-16": 3899}
LT_200 = {"form1040.line-7a": 200, "form1040.line-15": 34450, "form1040.line-16": 3875}


def case(case_id: str, group: str, build86: Callable[[], Acts], build87: Callable[[], Acts] | None = None, *,
         hand: dict[str, Any], asks: tuple[str, ...] = (), note: str, v86_hand: bool = True) -> dict[str, Any]:
    """``build87`` is the truthful act list under the v87 words when it differs from v86's.

    ``asks`` names the changed questions (keys of ``words``) the page must show on each core.
    ``v86_hand`` is False where the v86 words lead a truthful filer to a different result.
    """
    return {"id": case_id, "group": group, "build86": build86, "build87": build87 or build86, "hand": hand,
            "asks": list(asks), "note": note, "v86_hand": v86_hand, "same_acts": build87 is None}


def cases() -> list[dict[str, Any]]:
    out = [
        # authority
        case("alc_wash_st_unanswered", "authority", lambda: strip(sales(ST_GAIN, only2a="no"), closure("st")),
             hand={"schedule-d.line-1b": "blocked"}, asks=("wash_st",),
             note="Plain covered short-term sale, adjustment closure unanswered: asked."),
        case("alc_wash_st_no", "authority", lambda: close_no(sales(ST_GAIN, only2a="no"), "st"),
             hand={"schedule-d.line-1b": "blocked"},
             note="The closure answered no (false at the current horizon): line 1b stays blocked."),
        case("alc_wash_st_yes", "authority", lambda: sales(ST_GAIN, only2a="no"),
             hand={"schedule-d.line-1a": 200, "schedule-d.line-1b": 0, **ST_200},
             note="The closure answered yes: line 1b 0."),
        case("alc_wash_lt_unanswered", "authority", lambda: strip(sales(LT_GAIN, only2a="no"), closure("lt")),
             hand={"schedule-d.line-8b": "blocked"}, asks=("wash_lt",),
             note="Plain covered long-term sale, adjustment closure unanswered: asked."),
        case("alc_wash_lt_yes", "authority", lambda: sales(LT_GAIN, only2a="no"),
             hand={"schedule-d.line-8a": 200, "schedule-d.line-8b": 0, **LT_200},
             note="Long-term closure yes."),
        case("alc_exc1_unanswered", "authority", lambda: strip(complete(), ONLY2A),
             hand={"form1040.line-7a": "blocked", "form1040.line-7b": "blocked"}, asks=("only_box2a",),
             note="No sale, only-box-2a unanswered: asked; lines 7a and 7b wait on it."),
        case("alc_exc1_yes", "authority", complete,
             hand={"form1040.line-7b": "published_categorical", "schedule-d-required.conclusion": "no", **NOSALE},
             note="No sale, all four yes: conclusion no, line 7b checked."),
        case("alc_exc1_sale_unanswered", "authority", lambda: sales(ST_GAIN, only2a=None),
             hand={"form1040.line-7a": "blocked"}, asks=("only_box2a",),
             note="A gain sale and only-box-2a unanswered: still asked (who is asked does not change)."),
        case("alc_exc1_sale_no", "authority", lambda: sales(ST_GAIN, only2a="no"),
             hand={"schedule-d-required.conclusion": "yes", "form1040.line-7b": "guard_inapplicable", **ST_200},
             note="A gain sale, only-box-2a no: conclusion yes; line 7b guard_inapplicable."),
        case("alc_sli_unanswered", "authority", lambda: sli(None),
             hand={"schedule1.line-21": "blocked"}, asks=("sli",),
             note="Form 1098-E interest 500, dependency unanswered: asked."),
        case("alc_sli_not_claimed", "authority", lambda: sli("yes"),
             hand={"schedule1.line-21": 500, "form1040.line-15": 33750, "form1040.line-16": 3815},
             note="Nobody claims the filer: the page's no records fact yes; 500."),
        case("alc_sli_claimed", "authority", lambda: sli("no"),
             hand={"schedule1.line-21": 0, "form1040.line-15": 34250, "form1040.line-16": 3875},
             note="The filer is claimed: the page's yes records fact no; legal 0."),
        case("alc_title_age", "authority",
             lambda: say(say(complete(), P + "taxpayer-over-65", True, "age"), P + "senior-deduction.taxpayer-valid-ssn", "yes", "ssn"),
             hand={"form1040.line-12e": 17750, "schedule1a.line36a-taxpayer": 6000, "form1040.line-16": 2915},
             note="Born before January 2, 1961 (for example January 1, 1961): true; 17,750 and 6,000."),
        case("alc_title_blind", "authority", lambda: say(complete(), P + "taxpayer-blind", True, "blind"),
             hand={"form1040.line-12e": 17750, "form1040.line-16": 3635}, note="Blind under the instruction's test."),
        case("alc_title_spouse_age", "authority",
             lambda: say(say(probe().mfj(harness(), complete()), P + "spouse-over-65", True, "sage"),
                         P + "senior-deduction.spouse-valid-ssn", "yes", "sssn"),
             hand={"form1040.line-12e": 33100, "schedule1a.line36b-spouse": 6000, "form1040.line-16": 1093},
             note="Joint; spouse born February 14, 1960, died February 13, 2025: true."),
        case("alc_title_spouse_died_before_65", "authority", lambda: probe().mfj(harness(), complete()),
             hand={"form1040.line-12e": 31500, "schedule1a.line36b-spouse": 0, "form1040.line-16": 1853},
             note="Joint; the same spouse died February 12, 2025: false (the default)."),
        # matrix: wash sale
        case("m_wash_none", "matrix", complete,
             hand={"schedule-d.line-1a": 0, "schedule-d.line-1b": 0, **NOSALE},
             note="No covered sale; the adjustment family closed empty."),
        case("m_wash_none_unanswered", "matrix", lambda: strip(complete(), closure("st")),
             hand={"schedule-d.line-1b": "blocked"}, asks=("wash_st",),
             note="No covered sale, adjustment closure unanswered: asked. Truthful answer on both cores: yes (no such sale)."),
        case("m_wash_plain", "matrix", lambda: strip(sales(ST_GAIN, only2a="no"), closure("st")),
             lambda: sales(ST_GAIN, only2a="no"),
             hand={"schedule-d.line-1a": 200, "schedule-d.line-1b": 0, **ST_200}, v86_hand=False,
             note="Covered sales with no adjustment. v86 words: truthful no (unanswered here), blocked. v87 words: yes."),
        case("m_wash_one", "matrix", lambda: sales(ST_WASH, only2a="no", losses="no"),
             hand={"schedule-d.line-1a": 0, "schedule-d.line-1b": 0, "form1040.line-7a": 0,
                   "f1099b.covered-w-st-adjustment-subtotal": 200, **NOSALE},
             note="One covered wash sale only (500, 700, 200): column (h) 0. Both words: yes once the 200 is recorded."),
        case("m_wash_both", "matrix", lambda: strip(sales(ST_GAIN + ST_WASH, only2a="no", losses="no"), closure("st")),
             lambda: sales(ST_GAIN + ST_WASH, only2a="no", losses="no"),
             hand={"schedule-d.line-1a": 200, "schedule-d.line-1b": 0,
                   "f1099b.covered-w-st-adjustment-subtotal": 200, **ST_200}, v86_hand=False,
             note="Both kinds. v86 words: truthful no (the plain sale has no adjustment), blocked. v87: yes."),
        # matrix: Exception 1
        case("m_exc1_nosale", "matrix", complete,
             hand={"form1040.line-7b": "published_categorical", **NOSALE}, note="No sale: all yes."),
        case("m_exc1_zero", "matrix", lambda: sales(ZERO, only2a="yes"), lambda: sales(ZERO, only2a="no"),
             hand={"schedule-d.line-1a": 0, "form1040.line-7b": "guard_inapplicable", **NOSALE},
             note="Zero-net sale. v86 truthful yes/yes (conclusion no beside a sale); v87 truthful no/yes. Same numbers."),
        case("m_exc1_gain", "matrix", lambda: sales(ST_GAIN, only2a="no"),
             hand={"schedule-d.line-1a": 200, "form1040.line-7b": "guard_inapplicable", **ST_200},
             note="Gain sale: only-box-2a no on both cores."),
        # matrix: student loan
        case("m_sli_single_not", "matrix", lambda: sli("yes"),
             hand={"schedule1.line-21": 500, "form1040.line-16": 3815}, note="Single, not claimed."),
        case("m_sli_single_claimed", "matrix", lambda: sli("no"),
             hand={"schedule1.line-21": 0, "form1040.line-16": 3875}, note="Single, claimed."),
        case("m_sli_joint_neither", "matrix", lambda: sli("yes", joint=True),
             hand={"schedule1.line-21": 500, "form1040.line-15": 18000, "form1040.line-16": 1803},
             note="Joint, neither spouse claimed."),
        case("m_sli_joint_filer_claimed", "matrix", lambda: sli("no", joint=True),
             hand={"schedule1.line-21": 0, "form1040.line-15": 18500, "form1040.line-16": 1853},
             note="Joint, the filer claimed: yes on both cores."),
        case("m_sli_joint_spouse_claimed", "matrix", lambda: sli("yes", joint=True), lambda: sli("no", joint=True),
             hand={"schedule1.line-21": 0, "form1040.line-15": 18500, "form1040.line-16": 1853}, v86_hand=False,
             note="Joint, only the spouse claimed. v86 words ask about 'you': truthful no, records fact yes, 500. v87: yes, 0."),
    ]
    return out


def late_traces() -> list[dict[str, Any]]:
    """Each trace: attest, close, compute, change the authority, reclose, recompute (all on both cores)."""
    def wash() -> list[tuple[str, Acts, dict[str, Any]]]:
        step1 = sales(ST_GAIN, only2a="no")
        step2 = late_wash_sale(step1, "st")
        step3 = reclose(step2, "st", "late-w")
        return [
            ("answered_yes", step1, {"schedule-d.line-1a": 200, "schedule-d.line-1b": 0, **ST_200}),
            ("wash_sale_added_unclosed", step2, {"schedule-d.line-1b": "blocked", "form1040.line-7a": "blocked"}),
            ("reclosed_yes", step3, {"schedule-d.line-1a": 200, "schedule-d.line-1b": 0,
                                     "f1099b.covered-w-st-adjustment-subtotal": 200, **ST_200}),
        ]

    def exc1() -> list[tuple[str, Acts, dict[str, Any]]]:
        step1 = complete()
        step2 = late_gain_sale(step1)
        step3 = say(step2, ONLY2A, "no", "only2a-late")
        return [
            ("nosale_yes", step1, {"form1040.line-7b": "published_categorical",
                                   "schedule-d-required.conclusion": "no", **NOSALE}),
            ("sale_added_yes_kept", step2, {"form1040.line-7b": "guard_inapplicable", "schedule-d.line-1a": 200, **ST_200}),
            ("only2a_superseded_no", step3, {"form1040.line-7b": "guard_inapplicable",
                                             "schedule-d-required.conclusion": "yes", **ST_200}),
        ]

    def sli_trace() -> list[tuple[str, Acts, dict[str, Any]]]:
        step1 = sli("yes")
        step2 = say(step1, SLI_FACT, "no", "sli-late-no")
        step3 = say(step2, SLI_FACT, "yes", "sli-late-yes")
        return [
            ("not_claimed", step1, {"schedule1.line-21": 500}),
            ("superseded_claimed", step2, {"schedule1.line-21": 0, "form1040.line-16": 3875}),
            ("superseded_not_claimed", step3, {"schedule1.line-21": 500, "form1040.line-16": 3815}),
        ]

    return [{"id": "late_wash_member", "steps": wash},
            {"id": "late_exc1_sale_after_yes", "steps": exc1},
            {"id": "late_sli_superseded", "steps": sli_trace}]


# ---- checks ----------------------------------------------------------------------------


def hand_failures(result: dict[str, Any], hand: dict[str, Any]) -> list[str]:
    if result.get("outcome") != "success":
        return [f"outcome {result.get('outcome')}: {result.get('error') or result.get('reason')}"]
    bad = []
    for key, expected in hand.items():
        got = (result.get("lines") or {}).get(key, (result.get("symbols") or {}).get(key))
        if isinstance(expected, str) and expected in {"blocked", "guard_inapplicable", "published_categorical"}:
            if expected not in str(got):
                bad.append(f"{key}: hand {expected} got {got!r}")
        elif _num(got) != expected:
            bad.append(f"{key}: hand {expected} got {got!r}")
    return bad


def ask_failures(result: dict[str, Any], keys: list[str], own: dict[str, str], other: dict[str, str]) -> list[str]:
    bad = []
    questions = result.get("questions") or []
    for key in keys:
        if own[key] not in questions:
            bad.append(f"{key}: own words not shown")
    for key, sentence in other.items():
        if sentence != own[key] and sentence in json.dumps(result):
            bad.append(f"{key}: the other core's words shown")
    return bad


# ---- commands --------------------------------------------------------------------------


def run_cases(core_path: Path, shard: int, count: int, part: Path) -> None:
    cores = {"v86": v86(), "v87": v87(core_path)}
    w = {name: words(core) for name, core in cores.items()}
    found: dict[str, Any] = json.loads(part.read_text(encoding="utf-8")) if part.exists() else {}
    work: list[tuple[str, Callable[[], dict[str, Any]]]] = []
    for spec in cases():
        def one(spec: dict[str, Any] = spec) -> dict[str, Any]:
            row: dict[str, Any] = {k: spec[k] for k in ("id", "group", "hand", "asks", "note", "v86_hand", "same_acts")}
            for name, core in cores.items():
                acts = (spec["build86"] if name == "v86" else spec["build87"])()
                result = execute(core, acts, f"demo.qw.t0.{name}.{spec['id']}")
                row[name] = result
                other = w["v87" if name == "v86" else "v86"]
                row[f"{name}_hand_failures"] = hand_failures(result, spec["hand"])
                row[f"{name}_ask_failures"] = ask_failures(result, spec["asks"], w[name], other)
            row["pass"] = not row["v87_hand_failures"] and not row["v87_ask_failures"] and not row["v86_ask_failures"] \
                and (not spec["v86_hand"] or not row["v86_hand_failures"])
            if not spec["v86_hand"]:
                row["v86_counterexample_fixed"] = bool(row["v86_hand_failures"])
            if spec["same_acts"]:
                row["numbers_identical"] = (row["v86"].get("lines"), row["v86"].get("symbols")) == \
                    (row["v87"].get("lines"), row["v87"].get("symbols"))
            return row
        work.append((spec["id"], one))
    for trace in late_traces():
        def steps(trace: dict[str, Any] = trace) -> dict[str, Any]:
            row: dict[str, Any] = {"id": trace["id"], "group": "late", "steps": []}
            for step_id, acts, hand in trace["steps"]():
                entry: dict[str, Any] = {"step": step_id, "hand": hand}
                for name, core in cores.items():
                    result = execute(core, acts, f"demo.qw.t0.{name}.{trace['id']}.{step_id}")
                    entry[name] = result
                    entry[f"{name}_hand_failures"] = hand_failures(result, hand)
                row["steps"].append(entry)
            row["pass"] = all(not s["v87_hand_failures"] and not s["v86_hand_failures"] for s in row["steps"])
            return row
        work.append((trace["id"], steps))
    for index, (key, fn) in enumerate(work):
        if index % count != shard or key in found:
            continue
        found[key] = fn()
        part.write_text(json.dumps(found, indent=1) + "\n", encoding="utf-8")
        print(f"shard {shard}: {key} pass={found[key]['pass']}", flush=True)


def write(name: str, payload: dict[str, Any]) -> None:
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"{name} contains {needle}")
    (HERE / name).write_text(text, encoding="utf-8")


def judge(row: dict[str, Any], w: dict[str, dict[str, str]]) -> None:
    """The hand and question checks of one stored row, recomputed from its saved results."""
    if row["group"] == "late":
        for step in row["steps"]:
            for name in ("v86", "v87"):
                step[f"{name}_hand_failures"] = hand_failures(step[name], step["hand"])
        row["pass"] = all(not s["v87_hand_failures"] and not s["v86_hand_failures"] for s in row["steps"])
        return
    for name in ("v86", "v87"):
        row[f"{name}_hand_failures"] = hand_failures(row[name], row["hand"])
        row[f"{name}_ask_failures"] = ask_failures(row[name], row["asks"], w[name], w["v87" if name == "v86" else "v86"])
    row["pass"] = not row["v87_hand_failures"] and not row["v87_ask_failures"] and not row["v86_ask_failures"] \
        and (not row["v86_hand"] or not row["v86_hand_failures"])
    if not row["v86_hand"]:
        row["v86_counterexample_fixed"] = bool(row["v86_hand_failures"])


def merge_cases(parts: list[Path], core_path: Path) -> None:
    found: dict[str, Any] = {}
    for part in parts:
        found.update(json.loads(part.read_text(encoding="utf-8")))
    cores = {"v86": v86(), "v87": v87(core_path)}
    w_all = {name: words(core) for name, core in cores.items()}
    for row in found.values():
        judge(row, w_all)
    for group, name in (("authority", "track0-authority.json"), ("matrix", "track0-matrix.json"),
                        ("late", "track0-late.json")):
        rows = [found[key] for key in sorted(found) if found[key]["group"] == group]
        write(name, {
            "cores": {"v86": "published core v86, registry v84, release v84",
                      "v87": "scratch core v87, registry v85, release v85 (prototype.py)"},
            "words": {key: words(core) for key, core in cores.items()},
            "count": len(rows),
            "passed": sum(1 for row in rows if row["pass"]),
            "cases": rows,
        })
    surface = []
    w86, w87 = words(cores["v86"]), words(cores["v87"])
    for row in found.values():
        if row["group"] == "late" or not row.get("asks"):
            continue
        for key in row["asks"]:
            surface.append({
                "case": row["id"], "question": key,
                "v86_text": w86[key], "v86_fields": sorted(f for f, s in (row["v86"].get("asked_on") or {}).items() if w86[key] in s),
                "v87_text": w87[key], "v87_fields": sorted(f for f, s in (row["v87"].get("asked_on") or {}).items() if w87[key] in s),
            })
    for row in surface:
        # Asked on the same fields on both cores: the words change, not who is asked.
        row["same_fields"] = row["v86_fields"] == row["v87_fields"]
        row["pass"] = bool(row["v87_fields"]) and row["same_fields"]
    shown: dict[str, Any] = {}
    for row in found.values():
        for name in ("v86", "v87"):
            for step in ([row] if row["group"] != "late" else row["steps"]):
                for fact, values in ((step.get(name) or {}).get("titles_shown") or {}).items():
                    bucket = shown.setdefault(name, {}).setdefault(fact, [])
                    for value in values:
                        if value not in bucket:
                            bucket.append(value)
    write("track0-surface.json", {
        "questions": surface,
        "passed": sum(1 for row in surface if row["pass"]),
        "count": len(surface),
        "titles_declared": {"v86": titles(cores["v86"]), "v87": titles(cores["v87"])},
        "titles_shown_on_any_page": shown,
    })
    print(json.dumps({key: (sum(1 for r in found.values() if r["group"] == key),
                            sum(1 for r in found.values() if r["group"] == key and r["pass"]))
                      for key in ("authority", "matrix", "late")}))


def run_reuse(core_path: Path) -> None:
    """Package identity: only question citizens and bundles differ, and every reader composes unchanged."""
    new = v87(core_path)
    old_pkg = json.loads((CONTENT / "package.core-calculations.v86.json").read_text(encoding="utf-8"))
    new_pkg = json.loads(new.package_path.read_text(encoding="utf-8"))
    old_m = {m["id"]: m for m in old_pkg["members"]}
    new_m = {m["id"]: m for m in new_pkg["members"]}
    changed = sorted(k for k in set(old_m) | set(new_m) if old_m.get(k) != new_m.get(k))
    diffs = []
    for member_id in changed:
        a, b = old_m.get(member_id), new_m.get(member_id)
        row: dict[str, Any] = {"id": member_id.removeprefix(P), "v86": a and a["version"], "v87": b and b["version"],
                               "role": (b or a or {}).get("role")}
        old_body = _member_body(CONTENT, a) if a else None
        new_body = _member_body(new.content, b) if b else None
        if old_body is not None and new_body is not None:
            row["fields_changed"] = _changed_fields(old_body, new_body)
        diffs.append(row)
    allowed = {"closure_question", "question", "version", "title"}
    readers = []
    pinned_old, pinned_new = _computation(CONTENT, old_pkg), _computation(new.content, new_pkg)
    needles = [P + "f1099b.covered-w-st-adjustment", P + "f1099b.covered-w-lt-adjustment", ONLY2A, NO_LOSSES,
               P + "schedule-d-required.conclusion", SLI_FACT, "taxpayer_over_65", "spouse_over_65",
               "taxpayer_blind", "spouse_blind", P + "standard-deduction.can-be-claimed-as-dependent"]
    for rule_id, (version, body, digest) in sorted(pinned_old.items()):
        blob = json.dumps(body)
        if not any(f'"{needle}' in blob for needle in needles):
            continue
        twin = pinned_new.get(rule_id)
        readers.append({"id": rule_id.removeprefix(P), "v86": version, "v87": twin and twin[0],
                        "bytes_identical": bool(twin) and twin[2] == digest})
    checks = {
        "only_question_and_bundle_members_changed": all(
            row["role"] in {"source-closure-mapping", "input-question", "fact-type-bundle"} for row in diffs),
        "only_words_titles_and_versions_changed": all(
            set(row.get("fields_changed") or []) <= allowed for row in diffs),
        "every_reader_unchanged": all(row["bytes_identical"] and row["v86"] == row["v87"] for row in readers),
        "input_bindings_unchanged": old_pkg.get("input_bindings") == new_pkg.get("input_bindings"),
        "seven_members": len(diffs) == 7,
        "fact_type_identities_unchanged": all(
            _fact_identities(CONTENT, old_m[f"{P}{row['id']}"]) == _fact_identities(new.content, new_m[f"{P}{row['id']}"])
            for row in diffs if row["role"] == "fact-type-bundle"),
        "question_pins_unchanged": all(
            (_member_body(CONTENT, old_m[f"{P}{row['id']}"]) or {}).get(key)
            == (_member_body(new.content, new_m[f"{P}{row['id']}"]) or {}).get(key)
            for row in diffs if row["role"] != "fact-type-bundle"
            for key in ("fact_type", "closure_fact_type", "family", "member_fact_type", "admits_symbol", "admission")),
    }
    write("track0-reuse.json", {"changed_members": diffs, "readers": readers, "checks": checks,
                                "pass": all(checks.values())})
    print(json.dumps(checks, indent=1))


def _member_body(content: Path, member: dict[str, Any]) -> dict[str, Any] | None:
    stem = str(member["id"]).removeprefix(P)
    version = member["version"]
    candidates = [f"{stem}.{version}.json", f"{stem}.json"]
    if member.get("role") == "fact-type-bundle":
        base = stem.removesuffix(".vocabulary")
        candidates = [f"{base}.bundle.{version}.json", f"{base}.bundle.json"]
    for name in candidates:
        path = content / name
        if path.exists():
            body = json.loads(path.read_text(encoding="utf-8"))
            if body.get("version") == version:
                return body
    return None


def _fact_identities(content: Path, member: dict[str, Any]) -> list[Any]:
    """Each fact type a bundle declares, without its title."""
    body = _member_body(content, member) or {}
    return sorted(json.dumps({k: v for k, v in fact.items() if k != "title"}, sort_keys=True)
                  for fact in body.get("fact_types") or [])


def _changed_fields(old: Any, new: Any, prefix: str = "") -> list[str]:
    if old == new:
        return []
    if isinstance(old, dict) and isinstance(new, dict):
        out: list[str] = []
        for key in set(old) | set(new):
            out += _changed_fields(old.get(key), new.get(key), key)
        return sorted(set(out))
    if isinstance(old, list) and isinstance(new, list) and len(old) == len(new):
        out = []
        for a, b in zip(old, new):
            out += _changed_fields(a, b, prefix)
        return sorted(set(out))
    return [prefix or "<root>"]


def _computation(content: Path, package: dict[str, Any]) -> dict[str, tuple[str, Any, str]]:
    found = {}
    for member in package["members"]:
        if member.get("role") != "computation":
            continue
        slug = str(member["id"]).removeprefix(P + "rule.")
        for name in (f"rule.{slug}.{member['version']}.json", f"rule.{slug}.json"):
            path = content / name
            if path.exists():
                raw = path.read_bytes()
                found[member["id"]] = (member["version"], json.loads(raw), hashlib.sha256(raw).hexdigest())
                break
    return found


# ---- neighbour dependency diff ---------------------------------------------------------


def neighbour_tasks() -> list[tuple[str, Acts]]:
    """Every recorded fixture's act lists, once each by digest.

    - v83: the 298 lists the v86 test replays (rerun.py ``tasks``).
    - v84: the box 7 Track 0 grid (tests/fixtures/f1099b_box7_loss_v84).
    - v85: the no-sale box 4 Track 0 grid (tests/fixtures/f1099b_box4_only_v85).
    - v82: the sale family audit Track 0 runs (tests/fixtures/sale_family_audit_v82), built for v82.
    - v81: the 213 code B returns as tests/test_code_b_sales_v81.py exports them, uncorrected.
    """
    rr = rerun()
    test = rr.load_test()
    expected = json.loads(rr.EXPECTED.read_text(encoding="utf-8"))
    asks = set(json.loads(rr.NEIGHBOUR.read_text(encoding="utf-8"))["asks_no_sale_present_ids"])
    out: list[tuple[str, Acts]] = [(f"v83/{key}", acts) for key, acts in rr.tasks(test, rr.load_harness(), expected, asks)]
    b7 = _module("qw_t0_box7_test", REPO / "tests/test_f1099b_box7_loss_v84.py").box7_cases()
    for group in ("authority", "matrix", "surface", "reuse"):
        for case_id, spec in sorted(b7[group].items()):
            out.append((f"v84/{group}/{case_id}", spec["acts"]))
    for trace in b7["late"]:
        for index, step in enumerate(trace.get("steps") or []):
            if isinstance(step, dict) and "acts" in step:
                out.append((f"v84/late/{trace['id']}/{index}", step["acts"]))
    b4 = _module("qw_t0_box4_test", REPO / "tests/test_f1099b_box4_only_v85.py").box4_cases()
    for group in ("authority", "matrix", "surface", "reuse"):
        for case_id, spec in sorted(b4[group].items()):
            out.append((f"v85/{group}/{case_id}", spec["acts"]))
    for trace in b4["late"]:
        for index, step in enumerate(trace.get("steps") or []):
            if isinstance(step, dict) and "acts" in step:
                out.append((f"v85/late/{trace['id']}/{index}", step["acts"]))
    sfa = _module("qw_t0_sfa_test", REPO / "tests/test_sale_family_audit_v82.py")
    t = sfa.track0()
    core82 = sfa.v82(t)
    for name, mode in sfa.track0_keys(t):
        out.append((f"v82/{name}/{mode}", sfa.track0_acts(t, name, mode, core82)))
    with tempfile.TemporaryDirectory() as tmp:
        exported = test.export_returns(Path(tmp))
    for group in ("case", "v80", "neighbour"):
        for name in sorted(exported.get(group, {})):
            out.append((f"v81/{group}/{name}", exported[group][name]))
    seen: dict[str, str] = {}
    unique: list[tuple[str, Acts]] = []
    for key, acts in out:
        digest = hashlib.sha256(json.dumps(acts, sort_keys=True).encode("utf-8")).hexdigest()
        if digest in seen:
            continue
        seen[digest] = key
        unique.append((key, acts))
    return unique


def run_neighbour(core_path: Path, shard: int, count: int, part: Path) -> None:
    rr = rerun()
    test = rr.load_test()
    work = neighbour_tasks()
    print(f"{len(work)} distinct act lists", flush=True)
    new, old = rr.scratch_core(test, core_path), rr.published_v86(test)
    found: dict[str, Any] = json.loads(part.read_text(encoding="utf-8")) if part.exists() else {}
    found.setdefault("_total", len(work))
    for index, (key, acts) in enumerate(work):
        if index % count != shard or key in found:
            continue
        slug = re.sub(r"[^A-Za-z0-9_.-]", ".", key)
        pin87 = rr._pin_run(test, new, acts, "demo.qw.t0.nb.v87." + slug)
        pin86 = rr._pin_run(test, old, acts, "demo.qw.t0.nb.v86." + slug)
        row = rr.classify(pin86, pin87)
        row["v86_error"] = pin86.get("error") if isinstance(pin86, dict) else None
        found[key] = row
        part.write_text(json.dumps(found, indent=1) + "\n", encoding="utf-8")
        print(f"shard {shard}: {key} {row['class']}", flush=True)


def merge_neighbour(parts: list[Path]) -> None:
    found: dict[str, Any] = {}
    total = 0
    for part in parts:
        body = json.loads(part.read_text(encoding="utf-8"))
        total = max(total, int(body.pop("_total", 0)))
        found.update(body)
    by_set: dict[str, Counter[str]] = {}
    errors: dict[str, Counter[str]] = {}
    for key, row in found.items():
        prefix = key.split("/", 1)[0]
        by_set.setdefault(prefix, Counter())[row["class"]] += 1
        if row.get("v86_error"):
            errors.setdefault(prefix, Counter())[str(row["v86_error"])] += 1
    changes = [{"id": key, **row} for key, row in sorted(found.items()) if row["class"] != "identical"]
    write("track0-neighbour.json", {
        "sets": {
            "v83": "tests/fixtures/f1099b_backup_withholding_v83/expected.json: the 298 lists the v86 test replays",
            "v84": "tests/fixtures/f1099b_box7_loss_v84/expected.json: the box 7 Track 0 grid (box7_cases)",
            "v85": "tests/fixtures/f1099b_box4_only_v85/expected.json: the no-sale box 4 Track 0 grid (box4_cases)",
            "v82": "tests/fixtures/sale_family_audit_v82/expected.json: the Track 0 runs, built for v82",
            "v81": "tests/fixtures/code_b_sales_v81/expected.json: the 213 exported returns, uncorrected",
        },
        "distinct_lists": total,
        "runs": len(found),
        "counts": {key: dict(value) for key, value in sorted(by_set.items())},
        "same_error_on_both_cores": {key: dict(value) for key, value in sorted(errors.items())},
        "changes": changes,
        "classes": {key: row["class"] for key, row in sorted(found.items())},
    })
    print(json.dumps({"runs": len(found), "of": total, "counts": {k: dict(v) for k, v in by_set.items()}}, indent=1))


def main() -> None:
    args = sys.argv[1:]
    if args[:1] == ["cases"] and len(args) == 5:
        run_cases(Path(args[1]), int(args[2]), int(args[3]), Path(args[4]))
    elif args[:1] == ["merge-cases"] and len(args) >= 3:
        merge_cases([Path(a) for a in args[2:]], Path(args[1]))
    elif args[:1] == ["reuse"] and len(args) == 2:
        run_reuse(Path(args[1]))
    elif args[:1] == ["neighbour"] and len(args) == 5:
        run_neighbour(Path(args[1]), int(args[2]), int(args[3]), Path(args[4]))
    elif args[:1] == ["merge-neighbour"] and len(args) >= 2:
        merge_neighbour([Path(a) for a in args[1:]])
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
