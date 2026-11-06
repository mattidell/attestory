"""P0 probe: inventory core v77 form-field texts, and read them on a return.

Usage, from the repo root:

    python3 docs/phases/engine-breadth/milestones/line-explanations-evidence/probe.py
    python3 docs/phases/engine-breadth/milestones/line-explanations-evidence/probe.py --inventory-only

The full run classifies every form-field text on core v77, drafts a replacement
for each generic one, then runs two synthetic returns through live_coordinate_run
and the presentation page. --inventory-only skips the returns.

Writes probe-output.json beside this file. Synthetic demo.* data only.
Does not edit packages/.
"""

from __future__ import annotations

import copy
import json
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))

OUT = HERE / "probe-output.json"
CONTENT_NAME = "packages/content/tax/2025"
PACKAGE_NAME = "package.core-calculations.v77.json"
DISPOSITIONS = (
    "published_value",
    "computed_zero",
    "closure_backed_zero",
    "blocked",
    "guard_inapplicable",
)
SPOKEN_FORM = {
    "1040": "Form 1040",
    "1040-SCH-D": "Schedule D",
    "1040-SCH-1": "Schedule 1",
    "1040-SCH-A": "Schedule A",
    "1040-Schedule-3": "Schedule 3",
    "Schedule 8812": "Schedule 8812",
    "1040-EIC-WS-A": "EIC Worksheet A",
}
# Exact explain strings that name no line and say none of: what it adds,
# why this zero, or why this line shows no value.
STOCK = frozenset({
    "blocked",
    "guard false",
    "closure zero",
    "computed zero",
    "Blocked.",
    "Inapplicable.",
    "Computed zero.",
    "Closure-backed zero.",
    "Not used.",
    "Not evaluated.",
    "This field does not publish a value.",
    "Current derived finding publishes this line.",
    "A current derived finding publishes this line.",
    "A current derived finding publishes this nonzero amount.",
    "A current derived finding publishes a numeric zero.",
    "No published value exists because required state is absent.",
    "No value exists because the declared rule guard is false.",
    "No value exists because the rule guard is false.",
    "A current derived finding publishes a computed zero.",
    "A current derived finding publishes a computed zero under complete authority.",
    "A current derived finding publishes a computed zero from present inputs that net to zero.",
    "A current derived finding publishes zero because the supporting source family is attested closed-empty under complete authority.",
    "A current derived finding publishes a zero from closure-backed inputs with no recorded members.",
    "A current derived finding publishes zero through honest closed-empty or zero-credit authority on the direct-election path.",
    "No value is published because a completeness or guard condition is not satisfied.",
    "No value is published because a scope, election, threshold, or creditability component is not satisfied for the bounded class.",
})
ROUTE_ONLY = re.compile(r"^No line \S+ value exists for this route\.?$")
BARE_PUBLISHED = re.compile(r"^published .+$", re.IGNORECASE)
BARE_PUBLISHED_KEEP = re.compile(r"because|equals|always|zero|closed", re.IGNORECASE)
ID_LEAK = re.compile(r"\b(?:tax\.us|demo)\.[A-Za-z0-9_.|-]+")
PATH_LEAK = re.compile(r"(?:/Users|/private|/tmp|/var|/home)/\S+")


def content_dir() -> Path:
    return REPO / CONTENT_NAME


def load_json(path: Path) -> dict[str, Any]:
    body = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(body, dict):
        raise SystemExit(f"expected an object: {path.name}")
    return body


def corpus() -> dict[tuple[str, str], dict[str, Any]]:
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for path in sorted(content_dir().glob("*.json")):
        try:
            body = load_json(path)
        except (OSError, ValueError):
            continue
        if isinstance(body.get("id"), str) and isinstance(body.get("version"), str):
            index[(body["id"], body["version"])] = body
    return index


def english_join(items: list[str]) -> str:
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + ", and " + items[-1]


def form_line(raw: str) -> str | None:
    """A filer line number, or None when the token is an internal id.

    ``sch1-8b`` is Schedule 1 line 8b. ``1a-h`` is line 1a, column (h).
    ``f1098-unresolved`` and ``sch1-top`` are not form line numbers.
    """
    line = re.sub(r"^(?:sch-d-|1040-|8812-|eic-a-)", "", raw)
    line = re.sub(r"^(?:sch1-|Sch3-)", "", line)
    column = re.fullmatch(r"(\d+[a-z])-([a-z])", line)
    if column:
        return f"{column.group(1)}, column ({column.group(2)})"
    if re.fullmatch(r"\d+[a-z]?", line):
        return line
    return None


def spoken(field: dict[str, Any]) -> str:
    form = SPOKEN_FORM.get(field["form"]["form_id"], field["form"]["form_id"])
    label = str(field["label"]).strip().rstrip(".")
    lowered = label.lower()
    if lowered.startswith(form.lower()) or lowered.startswith("line ") or lowered.startswith("worksheet "):
        return label
    line = form_line(str(field["line"]))
    if line is None:
        return f"{form}, {label[0].lower() + label[1:]}" if label else form
    return f"{form} line {line} ({label})"


def condition_count(when: Any) -> int:
    """How many guard conditions a static sentence would have to choose among.

    ``true`` is no guard. ``all`` / ``any`` add their parts. A ``choose`` adds
    its condition. One part is one condition.
    """
    if when is True or when is None:
        return 0
    if not isinstance(when, dict):
        return 1
    op = when.get("op")
    if op in {"all", "any"}:
        args = when.get("args") if isinstance(when.get("args"), list) else []
        total = sum(condition_count(arg) for arg in args)
        return total or 1
    if op == "choose":
        return condition_count(when.get("when")) or 1
    return 1


def ref_names(node: Any) -> list[str]:
    found: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if value.get("op") == "ref" and isinstance(value.get("name"), str):
                found.append(value["name"])
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(node)
    ordered: list[str] = []
    for name in found:
        if name not in ordered:
            ordered.append(name)
    return ordered


def classify(text: str, *, shared_lines: int) -> tuple[str, str]:
    """Return (specific|generic, reason).

    Generic: a stock token, boilerplate shared by two lines, a bare
    "published …" label, or a sentence that only says "this route".
    Specific: the text says what this line adds, why it is zero, or why it
    shows no value, in words that are not that shared boilerplate.
    """
    stripped = text.strip()
    if stripped in STOCK:
        return "generic", "stock"
    if shared_lines > 1:
        return "generic", "shared_boilerplate"
    if BARE_PUBLISHED.match(stripped) and not BARE_PUBLISHED_KEEP.search(stripped):
        return "generic", "bare_label"
    if ROUTE_ONLY.match(stripped):
        return "generic", "unnamed_route"
    return "specific", "names_the_line"


# Published sentences the generator cannot recover without the rule's
# internal notes. Each one is the line's own label, or the rule's plain
# arithmetic, with the version and ADR chatter left out.
PUBLISHED_OVERRIDE = {
    "tax.us.2025.form1040.line-12e": (
        "Form 1040 line 12e is the larger of the standard deduction and the itemized deductions."
    ),
    "tax.us.2025.form1040.line-15": (
        "Form 1040 line 15 is taxable income: adjusted gross income minus the line 14 deduction total, and not below zero."
    ),
    "tax.us.2025.form1040.line-16": (
        "Form 1040 line 16 is the tax. With no qualified dividends and no preferential gain, it is the tax on taxable income. Otherwise it is the tax from the qualified dividends and capital gain worksheet."
    ),
    "tax.us.2025.form1040.line-1a": (
        "Form 1040 line 1a is the total of box 1 wages, tips, and other compensation on Forms W-2."
    ),
    "tax.us.2025.schedule-d.line-1a": (
        "Schedule D line 1a, column (h), is short-term proceeds minus basis for the transactions reported directly on Schedule D."
    ),
    "tax.us.2025.schedule-d.line-1b": (
        "Schedule D line 1b, column (h), is the short-term gain or loss from Form 8949."
    ),
    "tax.us.2025.schedule-d.line-8b": (
        "Schedule D line 8b, column (h), is the long-term gain or loss from Form 8949."
    ),
    "tax.us.2025.schedule-d.line-6": "Schedule D line 6 is the short-term capital loss carryover.",
    "tax.us.2025.schedule-d.line-14": "Schedule D line 14 is the long-term capital loss carryover.",
    "tax.us.2025.schedule-d.line-21": "Schedule D line 21 is the capital loss allowed this year, after the yearly limit.",
    "tax.us.2025.form.f1098.residence-interest-unresolved": (
        "This line names an open condition on the home mortgage interest statement. It does not show an amount."
    ),
    "tax.us.2025.form.f1099k.unresolved.form-field": (
        "This line names an open condition on a Form 1099-K. It does not show an amount."
    ),
}
BLOCKED_OVERRIDE = {
    "tax.us.2025.form1040.line-1a": (
        "Form 1040 line 1a has no value yet. It is waiting for the box 1 wage amounts, or for that wage record to be confirmed complete."
    ),
    "tax.us.2025.form1040.line-12e": (
        "Form 1040 line 12e has no value yet. It is waiting for the standard deduction or the itemized deductions."
    ),
    "tax.us.2025.form1040.line-16": (
        "Form 1040 line 16 has no value yet. It is waiting for taxable income and the facts the tax worksheet needs."
    ),
}


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.])\s+", text.strip()) if part.strip()]


def plain_sentence(text: str) -> str:
    """The first sentence a filer could read. Drops ids, ADRs, and version talk."""
    for sentence in _sentences(text):
        sentence = re.sub(r"\s*\(ADR-\d+[^)]*\)", "", sentence).strip()
        if ID_LEAK.search(sentence):
            continue
        if re.search(r"\bADR-\d+\b|\bsuccessor\b|\bCore v\d+\b|\bTrack \d|\bpresentation section\b", sentence):
            continue
        if re.search(r"\bv\d+\b", sentence):
            continue
        if not sentence.endswith("."):
            sentence += "."
        return sentence
    return ""


def short_label(label: str) -> str:
    return re.sub(r"\s*\(see instructions\)", "", label).strip()


def value_phrase(rule: dict[str, Any], labels: dict[str, str]) -> str:
    value = rule.get("value")
    if not isinstance(value, dict):
        return ""
    if value.get("op") == "add":
        names = [short_label(labels[name]) for name in ref_names(value) if name in labels]
        if len(names) >= 2:
            return "adds " + english_join(names)
    if value.get("op") == "max" and isinstance(value.get("args"), list) and value["args"]:
        if value["args"][0] == 0 and len(value["args"]) > 1 and isinstance(value["args"][1], dict):
            inner = value["args"][1]
            if inner.get("op") == "subtract":
                left = inner.get("left", {}).get("name") if isinstance(inner.get("left"), dict) else None
                right = inner.get("right", {}).get("name") if isinstance(inner.get("right"), dict) else None
                if isinstance(left, str) and isinstance(right, str) and left in labels and right in labels:
                    return f"is {short_label(labels[left])} minus {short_label(labels[right])}, and not below zero"
    return ""


def draft_for(
    field: dict[str, Any],
    code: str,
    rule: dict[str, Any],
    labels: dict[str, str],
) -> dict[str, Any]:
    """A short replacement. Words come from the label, the description, the
    rule's own plain notes, and the labels of the amounts the rule adds.
    No internal ids.
    """
    name = spoken(field)
    description = plain_sentence(str(field.get("description") or ""))
    label_words = set(re.findall(r"[a-z0-9]+", str(field["label"]).lower()))
    desc_words = set(re.findall(r"[a-z0-9]+", description.lower()))
    if len(desc_words - label_words - {"form", "line", "the", "a", "of", "or", "and", "from", "on"}) < 2:
        description = ""
    adds = value_phrase(rule, labels)
    notes = plain_sentence(str(rule.get("notes") or ""))
    guards = condition_count(rule.get("when"))
    missing = rule.get("blocked", {}).get("missing") if isinstance(rule.get("blocked"), dict) else []
    waiting = [short_label(labels[item]) for item in missing if isinstance(item, str) and item in labels]
    source = "label"
    if code == "published_value" and field["id"] in PUBLISHED_OVERRIDE:
        text, source = PUBLISHED_OVERRIDE[field["id"]], "rule_plain"
    elif code == "blocked" and field["id"] in BLOCKED_OVERRIDE:
        text, source = BLOCKED_OVERRIDE[field["id"]], "rule_plain"
    elif code == "published_value":
        if adds:
            text, source = f"{name} {adds}.", "rule_inputs"
        elif description:
            text, source = description, "description"
        elif notes:
            text, source = notes, "rule_notes"
        else:
            label = str(field["label"]).strip().rstrip(".")
            text = f"{name} is {label[0].lower() + label[1:]}."
    elif code == "computed_zero":
        if adds.startswith("adds "):
            text, source = f"{name} is zero because those amounts come to zero.", "rule_inputs"
        elif adds.startswith("is "):
            text, source = f"{name} is zero because that subtraction is not above zero.", "rule_inputs"
        else:
            text = f"{name} is zero because the calculation comes to zero."
    elif code == "closure_backed_zero":
        text = f"{name} is zero because nothing was recorded and that record is complete."
    elif code == "blocked":
        if adds.startswith("adds "):
            text, source = f"{name} has no value yet. It is waiting for the amounts it adds.", "rule_inputs"
        elif waiting:
            text, source = f"{name} has no value yet. It is waiting for {english_join(waiting)}.", "rule_inputs"
        else:
            text = f"{name} has no value yet. It is waiting for an answer it needs."
    else:
        if guards == 0:
            text = f"{name} has no condition that turns it off, so this sentence is not shown."
        elif guards == 1:
            text = f"{name} shows no value because its condition does not hold."
        else:
            text = (
                f"{name} shows no value because one of its conditions does not hold. "
                "One sentence cannot say which condition."
            )
        source = "rule_guard"
    if ID_LEAK.search(text):
        raise SystemExit(f"draft leaked an id for {field['id']} {code}")
    return {
        "text": text,
        "source": source,
        "guard_conditions": guards,
        "several_guards": guards > 1,
        "guard_never_selected": code == "guard_inapplicable" and guards == 0,
    }


def selectable(field: dict[str, Any], code: str, guards: int) -> bool:
    """Whether a filer can be shown this disposition's explain.

    A checkbox field uses the published_value explain for its checked state.
    Its zero explains are not selected. A rule whose guard is ``true`` never
    selects guard_inapplicable.
    """
    render = str(field["dispositions"]["published_value"].get("render") or "")
    categorical = render not in {"{value}", "0", ""}
    if code == "guard_inapplicable":
        return guards > 0
    if code in {"computed_zero", "closure_backed_zero"} and categorical:
        return False
    return True


def inventory() -> dict[str, Any]:
    index = corpus()
    package = load_json(content_dir() / PACKAGE_NAME)
    members = [member for member in package["members"] if member.get("role") == "form-field"]
    entrypoints = {(item["id"], item["version"]) for item in package.get("entrypoints", [])}
    rules: dict[str, dict[str, Any]] = {}
    for member in package["members"]:
        body = index.get((member["id"], member["version"]))
        if body and isinstance(body.get("publishes"), str) and str(body.get("schema", "")).startswith("rule-artifact"):
            rules[body["publishes"]] = body
    fields = [index[(member["id"], member["version"])] for member in members]
    labels = {field["binds_symbol"]: str(field["label"]).strip().rstrip(".") for field in fields}
    owners: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for field in fields:
        for row in field["dispositions"].values():
            owners[row["explain"]].add((field["form"]["form_id"], field["line"]))
    rows: list[dict[str, Any]] = []
    for member, field in zip(members, fields, strict=True):
        rule = rules[field["binds_symbol"]]
        guards = condition_count(rule.get("when"))
        citation = field.get("citation")
        citation_body = index.get((citation["id"], citation["version"])) if isinstance(citation, dict) else None
        authority = citation_body.get("authority") if isinstance(citation_body, dict) else None
        dispositions: dict[str, Any] = {}
        for code in DISPOSITIONS:
            row = field["dispositions"][code]
            text = row["explain"]
            kind, reason = classify(text, shared_lines=len(owners[text]))
            item: dict[str, Any] = {
                "explain": text,
                "render": row.get("render"),
                "class": kind,
                "reason": reason,
                "shared_lines": len(owners[text]),
                "selectable": selectable(field, code, guards),
            }
            if "codes" in row:
                item["codes"] = row["codes"]
            if kind == "generic":
                item["draft"] = draft_for(field, code, rule, labels)
            dispositions[code] = item
        rows.append({
            "id": field["id"],
            "version": field["version"],
            "schema": field["schema"],
            "form": field["form"]["form_id"],
            "line": field["line"],
            "label": field["label"],
            "description": field["description"],
            "binds_symbol": field["binds_symbol"],
            "entrypoint": (field["id"], field["version"]) in entrypoints,
            "citation": citation,
            "citation_authority": authority,
            "rule_id": rule["id"],
            "rule_version": rule["version"],
            "guard_conditions": guards,
            "dispositions": dispositions,
        })
    return {
        "package": package["id"],
        "package_version": package["version"],
        "fields": rows,
        "citation_note": (
            "An irs-instructions citation names a form and a tax year. "
            "The schema has no line, page, or quoted instruction. "
            "Three fields have no citation. Drafts use the field's label and "
            "description, the rule's plain notes, and the labels of the amounts the rule adds."
        ),
    }


def counts_of(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_form: dict[str, Any] = {}
    by_disposition: dict[str, Counter[str]] = {code: Counter() for code in DISPOSITIONS}
    selectable_generic_fields = 0
    any_generic_fields = 0
    for field in rows:
        form = by_form.setdefault(field["form"], {"fields": 0, "dispositions": {code: {"specific": 0, "generic": 0} for code in DISPOSITIONS}})
        form["fields"] += 1
        any_generic = False
        selectable_generic = False
        for code in DISPOSITIONS:
            kind = field["dispositions"][code]["class"]
            form["dispositions"][code][kind] += 1
            by_disposition[code][kind] += 1
            if kind == "generic":
                any_generic = True
                if field["dispositions"][code]["selectable"]:
                    selectable_generic = True
        any_generic_fields += int(any_generic)
        selectable_generic_fields += int(selectable_generic)
    return {
        "fields": len(rows),
        "texts": len(rows) * len(DISPOSITIONS),
        "by_form": by_form,
        "by_disposition": {code: dict(counter) for code, counter in by_disposition.items()},
        "fields_with_any_generic_text": any_generic_fields,
        "fields_with_a_selectable_generic_text": selectable_generic_fields,
    }


def redact(value: str) -> str:
    return PATH_LEAK.sub("[path]", value)


def _browser() -> str | None:
    candidates = [
        *sorted(Path.home().glob("Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell"), reverse=True),
        *sorted(Path.home().glob(".cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell"), reverse=True),
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    ]
    found = next((str(path) for path in candidates if path.is_file()), None)
    return found or shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")


class _SectionText(HTMLParser):
    def __init__(self, ids: set[str]) -> None:
        super().__init__()
        self.ids = ids
        self.stack: list[str | None] = []
        self.current: list[str] = []
        self.sections: dict[str, list[str]] = {}
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1
        raw = dict(attrs).get("id")
        sid = raw if tag == "div" and raw in self.ids else None
        if sid:
            self.current.append(sid)
            self.sections.setdefault(sid, [])
        self.stack.append(sid)

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
        if self.stack:
            if self.stack.pop() is not None and self.current:
                self.current.pop()

    def handle_data(self, data: str) -> None:
        if self.skip or not self.current or not data.strip():
            return
        self.sections[self.current[-1]].append(" ".join(data.split()))


def rendered_text(page: bytes, ids: set[str]) -> dict[str, str] | None:
    browser = _browser()
    if browser is None:
        return None
    from tests.helpers.chrome_startup_slot import browser_startup_slot

    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "page.html"
        path.write_bytes(page)
        with browser_startup_slot():
            dom = subprocess.run(
                [browser, "--headless", "--disable-gpu", "--no-sandbox", "--dump-dom", path.as_uri()],
                check=True, capture_output=True, text=True, timeout=90,
            ).stdout
    parser = _SectionText(ids)
    parser.feed(dom)
    return {sid: " | ".join(parts) for sid, parts in parser.sections.items()}


def run_case(
    acts: list[dict[str, object]],
    run_id: str,
    *,
    content: Path | None = None,
    release_dir: Path | None = None,
    package_name: str = PACKAGE_NAME,
    package_version: str = "v77",
    registry_name: str = "published-packages.v75.json",
    release_name: str = "demo.release.sli-worksheet-integration.2025.v75.json",
    release_version: str = "v75",
) -> dict[str, Any]:
    from packages.derivation.live import live_coordinate_run
    from packages.derivation.live_session import _render_page
    from packages.derivation.live_workspace import WorkspaceCapability
    from packages.derivation.production_resolver import PublicationSurface
    from tests.helpers import current_core_returns as ccr
    from tests.test_form_1099_k_income import _handover
    from tests.test_form_1099_withholding import YEAR
    from tests.test_refund_or_amount_owed_track1 import _finish

    content = content or ccr.CONTENT
    release_dir = release_dir or ccr.RELEASE_DIR
    surface = PublicationSurface(release_dir, content / registry_name, content)
    finished = _handover(
        _finish(
            copy.deepcopy(acts),
            package_path=content / package_name,
            package_version=package_version,
            release_path=release_dir / release_name,
            release_version=release_version,
            note=run_id,
        ),
        surface=surface,
        reconfirm=True,
    )
    with TemporaryDirectory() as tmp:
        capability = WorkspaceCapability(Path(tmp) / "L")
        outcome = live_coordinate_run(
            capability,
            repo_root=REPO,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=ccr.USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            return {
                "run_id": run_id,
                "reachable": False,
                "refusal": redact(f"{outcome.refusal.reason} {outcome.refusal.detail}"),
            }
        assert outcome.output_path is not None and outcome.presentation_path is not None
        model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
        report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
        page = _render_page(REPO, capability, outcome.presentation_path)
    return {"run_id": run_id, "reachable": True, "model": model, "report": report, "page": page}


def explain_visible(disposition: str, reasons: list[Any]) -> bool:
    """The page's renderLine: the active explain, except a blocked line that
    already has reason sentences. Those sentences replace the explain.
    """
    if disposition in {"published_value", "computed_zero", "closure_backed_zero", "published_categorical", "guard_inapplicable"}:
        return True
    if disposition == "blocked":
        return not reasons
    return False


def section_view(model: dict[str, Any], rendered: dict[str, str] | None) -> list[dict[str, Any]]:
    graph = json.dumps(model.get("explanationGraph", {}))
    views = []
    seen: dict[str, int] = defaultdict(int)
    for section in model.get("sections", []):
        field = section.get("field") or {}
        resolved = section.get("resolved") or {}
        disposition = str(resolved.get("disposition"))
        key = "published_value" if disposition == "published_categorical" else disposition
        instruction = (field.get("dispositions") or {}).get(key) or {}
        explain = instruction.get("explain")
        reasons = resolved.get("reasons") or []
        sentences = [str(reason.get("sentence")) for reason in reasons if isinstance(reason, dict)]
        section_id = str(section.get("id"))
        seen[section_id] += 1
        shown = explain_visible(disposition, reasons)
        page_text = rendered.get(section_id) if rendered else None
        views.append({
            "section_id": section_id,
            "field_id": field.get("id"),
            "line": field.get("line"),
            "form": (field.get("form") or {}).get("form_id"),
            "label": field.get("label"),
            "disposition": disposition,
            "value": resolved.get("value"),
            "active_codes": resolved.get("activeCodes"),
            "explain": explain,
            "explain_in_row_or_panel": shown,
            "questions": sentences,
            "explain_in_rendered_page": (explain in page_text) if page_text is not None and isinstance(explain, str) else None,
            "explain_in_explanation_graph": isinstance(explain, str) and explain in graph,
            "rendered": page_text,
        })
    return views


def focus_lines() -> set[str]:
    return {"9", "11", "11a", "11b", "12e", "13a", "13b", "1040-14", "15", "16", "1a"}


def summarize_case(raw: dict[str, Any], *, schedule_d: bool) -> dict[str, Any]:
    if not raw.get("reachable"):
        return raw
    model = raw["model"]
    ids = {str(section.get("id")) for section in model.get("sections", [])}
    rendered = rendered_text(raw["page"], ids)
    views = section_view(model, rendered)
    census: Counter[str] = Counter(view["disposition"] for view in views)
    duplicate_ids = sorted(sid for sid, count in Counter(view["section_id"] for view in views).items() if count > 1)
    keep = []
    for view in views:
        line = str(view["line"])
        form = str(view["form"])
        wanted = line in focus_lines() and form == "1040"
        wanted = wanted or (schedule_d and form == "1040-SCH-D")
        wanted = wanted or view["disposition"] in {"blocked", "guard_inapplicable", "closure_backed_zero"}
        if wanted:
            keep.append(view)
    return {
        "run_id": raw["run_id"],
        "reachable": True,
        "browser": _browser() is not None,
        "sections": len(views),
        "disposition_census": dict(census),
        "duplicate_section_ids": duplicate_ids,
        "blocked_rows": sum(1 for row in raw["report"].get("dispositions", []) if row.get("disposition") == "blocked"),
        "shown": keep,
    }


def live(rows: list[dict[str, Any]]) -> dict[str, Any]:
    from tests.helpers import current_core_returns as ccr
    from tests.test_withholding_closure import _strip_closure

    wages_acts = ccr.base_return()
    wages = run_case(wages_acts, "demo.le.p0.wages")
    unanswered_acts = _strip_closure(copy.deepcopy(wages_acts), "tax.us.2025.w2.source-closure")
    unanswered = run_case(unanswered_acts, "demo.le.p0.wages-closure-unanswered")
    wages_summary = summarize_case(wages, schedule_d=True) if wages.get("reachable") else wages
    unanswered_summary = summarize_case(unanswered, schedule_d=False) if unanswered.get("reachable") else unanswered
    if wages.get("reachable"):
        # summarize_case drops the model; rebuild values from the summary's shown rows
        # and from a second pass stored below before discard.
        wages_summary["value_by_field"] = {
            str(view["field_id"]): view["value"]
            for view in section_view(wages["model"], None)
            if view["value"] is not None
        }
    by_id = {row["id"]: row for row in rows}
    return {
        "wages_only": wages_summary,
        "unanswered_w2_closure": unanswered_summary,
        "reading": _reading(wages_summary, unanswered_summary, by_id),
    }


def _reading(wages: dict[str, Any], unanswered: dict[str, Any], fields: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Where the five texts go, from the two returns plus the page rules."""
    return {
        "page_row": (
            "For a published value, a computed zero, and a closure-backed zero, "
            "the page row shows the amount and that disposition's explain."
        ),
        "blocked_panel": (
            "A blocked line shows its explain only when it has no reason sentences. "
            "When it has them, the page shows those sentences (the missing-input questions) "
            "and does not show the field's blocked explain."
        ),
        "explanation_walk": (
            "Trace recorded support lists symbols, values, and rule ids. "
            "It does not show a disposition explain. The saved explanation graph "
            "was checked for the active explain string."
        ),
        "never_seen": (
            "The four dispositions that are not the line's current one are not shown. "
            "A guard explain is never shown when the rule's when is true. "
            "A checkbox field does not select its zero explains."
        ),
        "fields_indexed": len(fields),
        "wages_reachable": wages.get("reachable"),
        "unanswered_reachable": unanswered.get("reachable"),
    }


def pin_scan(rows: list[dict[str, Any]]) -> dict[str, Any]:
    generic_texts = sorted({
        item["explain"]
        for field in rows
        for item in field["dispositions"].values()
        if item["class"] == "generic"
    })
    roots = [REPO / "tests", REPO / "packages" / "sample_data"]
    needles = {text: f'"explain": "{text}"' for text in generic_texts}
    hits: dict[str, list[str]] = {text: [] for text in generic_texts}
    scanned = 0
    for root in roots:
        for path in root.rglob("*"):
            if path.suffix not in {".py", ".json", ".md"} or not path.is_file():
                continue
            scanned += 1
            try:
                body = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
            relative = path.relative_to(REPO).as_posix()
            for text, needle in needles.items():
                if needle in body or (len(text) > 40 and text in body):
                    hits[text].append(relative)
    pinned = {text: paths for text, paths in hits.items() if paths}
    file_count = len({path for paths in pinned.values() for path in paths})
    schema_v2 = (REPO / "packages/schemas/tax/form-field.v2.schema.json").read_text(encoding="utf-8")
    return {
        "generic_texts": len(generic_texts),
        "generic_texts_found_outside_content": len(pinned),
        "files_outside_content_that_contain_a_generic_text": file_count,
        "files_scanned": scanned,
        "examples": {text: paths[:8] for text, paths in list(pinned.items())[:12]},
        "form_field_v2_explain": {
            "min_length": 1,
            "max_length": None,
            "pattern_on_explain": False,
            "pattern_on_version": True,
            "note": (
                "explain is a string of minLength 1, with no maxLength and no pattern. "
                "render is a string and may be empty. The schema's only pattern is on version strings."
            ),
            "schema_mentions_maxLength": "maxLength" in schema_v2,
        },
    }


def successor_touch(rows: list[dict[str, Any]]) -> dict[str, Any]:
    any_generic = [field for field in rows if any(item["class"] == "generic" for item in field["dispositions"].values())]
    selectable = [
        field for field in rows
        if any(item["class"] == "generic" and item["selectable"] for item in field["dispositions"].values())
    ]
    return {
        "new_field_files_if_every_generic_field_is_succeeded": len(any_generic),
        "new_field_files_if_only_selectable_generic_texts_change": len(selectable),
        "package_file": "package.core-calculations.v78.json",
        "registry_file": "published-packages.v76.json",
        "release_file": "demo.release.sli-worksheet-integration.2025.v76.json",
        "entrypoint_pins_inside_the_package": sum(1 for field in selectable if field["entrypoint"]),
        "loader": (
            "A live run of v78 needs packages/tax/loader.py to share v77's companion "
            "declaration. The closure-question and later-arm switches already turn on "
            "for any core at v75 and v76 or later. No schema change."
        ),
        "total_new_files_for_selectable_texts": len(selectable) + 3,
        "schemas_of_selectable_fields": dict(Counter(field["schema"] for field in selectable)),
    }


def main() -> int:
    inventory_only = "--inventory-only" in sys.argv
    built = inventory()
    rows = built["fields"]
    payload: dict[str, Any] = {
        "core": "v77",
        "field_counts": counts_of(rows),
        "citation_note": built["citation_note"],
        "fields": rows,
        "mechanics": {
            "what_pins_texts": pin_scan(rows),
            "successor": successor_touch(rows),
        },
    }
    if not inventory_only:
        payload["where_read"] = live(rows)
    text = json.dumps(payload, indent=2) + "\n"
    if PATH_LEAK.search(text):
        raise SystemExit("probe output contains a local path")
    OUT.write_text(text, encoding="utf-8")
    counts = payload["field_counts"]
    print(
        f"fields {counts['fields']} texts {counts['texts']} "
        f"generic_fields {counts['fields_with_any_generic_text']} "
        f"selectable_generic_fields {counts['fields_with_a_selectable_generic_text']}",
        flush=True,
    )
    for code, counter in counts["by_disposition"].items():
        print(f"  {code}: {counter}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
