"""Synthetic W-2 entry loop over the existing contribution and live-run paths.

The browser owns no fact-writing authority.  It submits an ``act.v1`` whose
kind is ``contribution``; this module admits that event with its ordinary
successor carriers, appends only acts to the workspace log, and recomputes the
return through ``live_coordinate_run``.

This first product slice is intentionally narrow: one committed synthetic
fixture and loopback serving.  It admits contributions for a small, fixed
set of fact families declared in ``_FACT_FAMILIES`` (currently W-2 Box 1 and
1099-DIV Box 1b) rather than an arbitrary caller-declared one.  Nothing here
accepts a caller-supplied workspace locator through HTTP or exposes one in a
response.
"""

from __future__ import annotations

import json
import mimetypes
import re
import shutil
import subprocess
from contextlib import AbstractContextManager
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from hashlib import sha256
from hmac import compare_digest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from secrets import token_urlsafe
from threading import Lock, Thread
from typing import Any, Mapping, Sequence
from urllib.parse import urlsplit

import jsonschema

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import (
    WorkspaceCapability,
    bootstrap_workspace,
)
from packages.derivation.loader import DerivationSchemas
from packages.derivation.production_resolver import PublicationSurface, Refusal
from packages.derivation.surface_resolver import (
    ResolvedSurface,
    resolve_surface_artifact,
)
from packages.kernel.act_log import ActLog
from packages.kernel.contribution import ContributionError, apply_contribution_batch
from packages.kernel.currency import compute_currency
from packages.kernel.findings import project


ENTRY_FIXTURE = Path("packages/sample_data/entry_loop_t1")
SEED_LOG = ENTRY_FIXTURE / "workspace" / "acts.jsonl"
SURFACE_CONTENT = ENTRY_FIXTURE / "surface" / "content" / "app"
SURFACE_MANIFESTS = ENTRY_FIXTURE / "surface" / "manifest"
SURFACE_REGISTRY = (
    ENTRY_FIXTURE / "surface" / "registry" / "published-surface-artifacts.json"
)
SURFACE_RELEASES = ENTRY_FIXTURE / "surface" / "publication_surface" / "releases"
SURFACE_ADOPTION = (
    ENTRY_FIXTURE / "surface" / "adoptions" / "adopt-entry-loop-v1.json"
)

SCOPE_USER = "demo.user.filer-1"
RUN_SCOPE = {"jurisdiction": "us", "year": "2055"}
W2_FAMILY = {"id": "tax.us.2025.w2", "version": "v2"}
W2_SCOPE = {"tax-year": "2025", "subject": "demo.primary"}
W2_PREDECESSOR = "demo.presentation-l2.w2.h0"
W2_SUCCESSOR = "demo.entry-loop.w2.h1"
W2_EVIDENCE_ID = "demo.presentation-l2.evidence.w2"
W2_FACT_ID = (
    "tax.us.2025.w2.box1-wages|"
    "employer=demo.presentation-l2.employer,"
    "w2-slip=demo.presentation-l2.w2,tax-year=2025"
)
W2_CLOSURE_FACT_ID = (
    "tax.us.2025.w2.source-closure|"
    f"family-horizon={W2_SUCCESSOR},tax-year=2025"
)

DIV1B_FAMILY = {"id": "tax.us.2025.f1099div.1b", "version": "v1"}
DIV1B_SCOPE = {"tax-year": "2025", "subject": "demo.primary"}
DIV1B_PREDECESSOR = "demo.presentation-l2.div1b.h0"
DIV1B_SUCCESSOR = "demo.entry-loop.div1b.h1"
# Shared with the 1099-DIV box 1a contribution that stays committed in the
# seed -- the same physical statement backs both boxes, which is exactly
# what the original production-shaped fixture already models.
DIV1B_EVIDENCE_ID = "demo.presentation-l2.evidence.div"
DIV1B_FACT_ID = (
    "tax.us.2025.f1099div.box1b-qualified|"
    "payer=demo.presentation-l2.payer,"
    "statement=demo.presentation-l2.divstmt,tax-year=2025"
)
DIV1B_CLOSURE_FACT_ID = (
    "tax.us.2025.f1099div.1b.source-closure|"
    f"family-horizon={DIV1B_SUCCESSOR},tax-year=2025"
)

EXPECTED_IMPACT_LINES = ("1a", "9", "11", "15", "16")
COMPARISON_LINES = ("2b", "3a", "3b", "12")
EVALUATION_LINES = EXPECTED_IMPACT_LINES + COMPARISON_LINES
EXPLAINED_LINES = EVALUATION_LINES
# The record's own correctable entry points -- one per enterable fact
# family, keyed by the line each one's contribution ultimately answers.
# A line's explanation traces to whichever of these its dependency chain
# actually reaches (zero, one, or in principle more than one), not to a
# single fixed line the way the loop's first fact assumed.
ENTRY_LINES = {"1a": "w2-box1", "3a": "div1b-qualified"}
W2_BOX1_FORMAT = (
    ENTRY_FIXTURE / "surface" / "content" / "app" / "src" / "w2-box1-format.js"
)
W2_BOX1_FIELD = (
    ENTRY_FIXTURE / "surface" / "content" / "app" / "src" / "w2-box1-field.js"
)
DIV1B_FORMAT_PATH = (
    ENTRY_FIXTURE / "surface" / "content" / "app" / "src" / "div1b-format.js"
)
DIV1B_FIELD_PATH = (
    ENTRY_FIXTURE / "surface" / "content" / "app" / "src" / "div1b-field.js"
)
ENTRY_FIELD_SCHEMA = Path("packages/schemas/entry/entry-field.v1.schema.json")

_MAX_REQUEST_BYTES = 16_384
_LINE_TITLES = {
    "1a": "Wages, salaries, tips",
    "2b": "Taxable interest",
    "3a": "Qualified dividends",
    "3b": "Ordinary dividends",
    "9": "Total income",
    "11": "Adjusted gross income",
    "12": "Standard deduction",
    "15": "Taxable income",
    "16": "Tax",
}


class EntryLoopError(RuntimeError):
    """A locator-free refusal suitable for the synthetic entry surface."""


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text("utf-8"))
    if not isinstance(value, dict):
        raise EntryLoopError("entry-loop-fixture-invalid")
    return value


def _load_currency_format(repo_root: Path, path: Path, marker_name: str) -> dict[str, Any]:
    full_path = repo_root / path
    try:
        text = full_path.read_text("utf-8")
    except OSError:
        raise EntryLoopError("entry-format-unavailable") from None
    marker = f"export const {marker_name} = "
    try:
        start = text.index(marker) + len(marker)
        end = text.index(";\n", start)
    except ValueError:
        raise EntryLoopError("entry-format-unavailable") from None
    try:
        spec = json.loads(text[start:end])
    except json.JSONDecodeError:
        raise EntryLoopError("entry-format-unavailable") from None
    if not isinstance(spec, dict):
        raise EntryLoopError("entry-format-unavailable")
    currency_symbol = spec.get("currencySymbol")
    if not isinstance(currency_symbol, str) or not currency_symbol:
        raise EntryLoopError("entry-format-unavailable")
    if spec.get("commaGrouping") not in {"accepted", "refused"}:
        raise EntryLoopError("entry-format-unavailable")
    if spec.get("currencyPrefix") not in {"accepted", "refused"}:
        raise EntryLoopError("entry-format-unavailable")
    max_fraction_digits = spec.get("maxFractionDigits")
    if (
        not isinstance(max_fraction_digits, int)
        or isinstance(max_fraction_digits, bool)
        or max_fraction_digits < 0
    ):
        raise EntryLoopError("entry-format-unavailable")
    if not isinstance(spec.get("requirePositive"), bool):
        raise EntryLoopError("entry-format-unavailable")
    max_value = spec.get("maxValue")
    if not isinstance(max_value, str):
        raise EntryLoopError("entry-format-unavailable")
    try:
        parsed_max_value = Decimal(max_value)
    except InvalidOperation:
        raise EntryLoopError("entry-format-unavailable") from None
    if not parsed_max_value.is_finite() or parsed_max_value <= 0:
        raise EntryLoopError("entry-format-unavailable")
    return spec


def _entry_field_validator(repo_root: Path) -> jsonschema.Draft202012Validator:
    path = repo_root / ENTRY_FIELD_SCHEMA
    try:
        document = json.loads(path.read_text("utf-8"))
    except (OSError, json.JSONDecodeError):
        raise EntryLoopError("entry-field-unavailable") from None
    try:
        jsonschema.Draft202012Validator.check_schema(document)
    except jsonschema.SchemaError:
        raise EntryLoopError("entry-field-unavailable") from None
    return jsonschema.Draft202012Validator(document)


def _load_entry_field(
    repo_root: Path,
    path: Path,
    marker_name: str,
    format_marker_name: str,
    format_spec: Mapping[str, Any],
) -> dict[str, Any]:
    """Load an entry-field.v1 declaration (see the schema of that name).

    Generalized from the loop's first field loader, which loaded exactly
    ``W2_BOX1_FIELD`` from ``w2-box1-field.js`` -- everything below is that
    same function with the module's own marker names as parameters, not a
    new design.

    The field module's ``format`` property is the imported format binding
    rather than a duplicated literal, so it is not itself valid JSON at that
    key. This substitutes the already-parsed and already-validated
    ``format_spec`` there before decoding the rest as JSON, which is the
    same brittle string-marker seam Track 2d used for the format declaration
    alone -- generalised, not made any less brittle. See Track 3's seam
    recommendation for what should replace it (still not built here, per the
    Track 3 repair charter's F4).

    The parsed declaration is validated against ``entry-field.v1`` itself
    (Track 3 repair, F2) rather than against a hand-rolled restatement of the
    schema's own rules -- the schema is the loader's contract, not a second,
    independent one.

    There is no separate check that the declared ``format`` equals this
    runtime's own ``format_spec`` (Track 3 repair 2, F2). An earlier version
    of this function had one, and it was a tautology: the ``format`` value in
    ``contract`` *is* ``format_spec`` -- the substitution below writes
    ``format_spec`` into the only text this parser accepts at that key, so
    the two can never disagree on any declaration this function successfully
    parses. That is a structural guarantee of the marker-and-regex seam
    itself, not a runtime check earning its keep, and it does not survive the
    seam recommendation's canonical-JSON migration: once the field's
    ``format`` is parsed independently from its own JSON rather than
    substituted in from the side, a real equality (or non-equality) becomes
    possible again, and a genuine check belongs there.
    """

    full_path = repo_root / path
    try:
        text = full_path.read_text("utf-8")
    except OSError:
        raise EntryLoopError("entry-field-unavailable") from None
    marker = f"export const {marker_name} = "
    try:
        start = text.index(marker) + len(marker)
        end = text.index("\n};\n", start) + len("\n}")
    except ValueError:
        raise EntryLoopError("entry-field-unavailable") from None
    body, count = re.subn(
        rf'"format":\s*{format_marker_name}',
        lambda _match: f'"format": {json.dumps(format_spec)}',
        text[start:end],
    )
    if count != 1:
        raise EntryLoopError("entry-field-unavailable")
    try:
        contract = json.loads(body)
    except json.JSONDecodeError:
        raise EntryLoopError("entry-field-unavailable") from None
    if not isinstance(contract, dict):
        raise EntryLoopError("entry-field-unavailable")
    validator = _entry_field_validator(repo_root)
    if not validator.is_valid(contract):
        raise EntryLoopError("entry-field-unavailable")
    return contract


def _accepted_formatting_text(format_spec: Mapping[str, Any]) -> str:
    currency_symbol = format_spec.get("currencySymbol")
    if not isinstance(currency_symbol, str):
        raise EntryLoopError("entry-format-unavailable")
    parts = [
        (
            "with or without comma grouping"
            if format_spec.get("commaGrouping") == "accepted"
            else "without commas"
        ),
        (
            f"an optional {currency_symbol} prefix"
            if format_spec.get("currencyPrefix") == "accepted"
            else f"no leading {currency_symbol} prefix"
        ),
    ]
    return " and ".join(parts)


def _field_hint(format_spec: Mapping[str, Any]) -> str:
    examples = format_spec.get("examples")
    if not isinstance(examples, list) or len(examples) < 2:
        raise EntryLoopError("entry-format-unavailable")
    label = format_spec.get("hintLabel")
    if not isinstance(label, str):
        raise EntryLoopError("entry-format-unavailable")
    return (
        f"Enter {label} {_accepted_formatting_text(format_spec)}, "
        f"for example {examples[0]} or {examples[1]}."
    )


def _field_error(format_spec: Mapping[str, Any]) -> str:
    field = format_spec.get("field")
    error_label = format_spec.get("errorLabel")
    max_fraction_digits = format_spec.get("maxFractionDigits")
    if not isinstance(field, str) or not isinstance(error_label, str):
        raise EntryLoopError("entry-format-unavailable")
    if not isinstance(max_fraction_digits, int):
        raise EntryLoopError("entry-format-unavailable")
    return (
        f"Enter {field} as a {error_label} {_accepted_formatting_text(format_spec)} "
        f"and with no more than {max_fraction_digits} decimal places."
    )


def load_seed_acts(repo_root: Path) -> list[dict[str, Any]]:
    """Read and validate the committed, newline-terminated seed act log."""

    path = repo_root / SEED_LOG
    try:
        raw = path.read_bytes()
    except OSError:
        raise EntryLoopError("entry-loop-fixture-unavailable") from None
    if not raw.endswith(b"\n"):
        raise EntryLoopError("entry-loop-fixture-invalid")
    acts: list[dict[str, Any]] = []
    try:
        for line in raw.splitlines():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError
            acts.append(value)
    except (json.JSONDecodeError, UnicodeError, ValueError):
        raise EntryLoopError("entry-loop-fixture-invalid") from None
    return acts


def _surface_publication(repo_root: Path) -> PublicationSurface:
    root = repo_root / ENTRY_FIXTURE / "surface"
    return PublicationSurface(
        release_dir=root / "publication_surface" / "releases",
        package_registry_path=root / "registry" / "published-surface-artifacts.json",
        member_dir=root / "manifest",
    )


def resolve_entry_surface(repo_root: Path) -> ResolvedSurface:
    """Resolve the entry program through the ADR-0049 surface artifact route."""

    adoption = _load_json(repo_root / SURFACE_ADOPTION)
    resolved = resolve_surface_artifact(
        [adoption],
        run_scope={"jurisdiction": "us", "year": "2025"},
        scope_user=SCOPE_USER,
        workspace_revision=1,
        surface=_surface_publication(repo_root),
        content_dir=repo_root / SURFACE_CONTENT,
    )
    if isinstance(resolved, Refusal):
        raise EntryLoopError(f"entry-surface-refused:{resolved.reason}")
    return resolved


def build_entry_surface(
    capability: WorkspaceCapability,
    *,
    repo_root: Path,
    timeout_seconds: float = 60.0,
) -> Path:
    """Verify, copy, and build the adopted surface inside the workspace."""

    workspace = bootstrap_workspace(capability, repo_root=repo_root)
    resolved = resolve_entry_surface(repo_root)
    build_root = workspace.live_output_path(
        Path(".entry-surface") / resolved.manifest["id"]
    )
    if build_root.exists():
        raise EntryLoopError("entry-surface-build-target-exists")
    shutil.copytree(resolved.content_dir, build_root)
    command = str(resolved.manifest["build_command"]).split()
    try:
        result = subprocess.run(
            command,
            cwd=build_root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        raise EntryLoopError("entry-surface-build-failed") from None
    if result.returncode != 0:
        raise EntryLoopError("entry-surface-build-failed")
    entrypoint = build_root / str(resolved.manifest["entrypoint_html"])
    if not entrypoint.is_file():
        raise EntryLoopError("entry-surface-build-failed")
    return entrypoint.parent


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _derived_id(prefix: str, value: Any) -> str:
    return f"{prefix}{sha256(_canonical_bytes(value)).hexdigest()[:24]}"


def _line_values(model: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    values: dict[str, dict[str, Any]] = {}
    sections = model.get("sections")
    if not isinstance(sections, list):
        raise EntryLoopError("entry-state-unavailable")
    for section in sections:
        if not isinstance(section, dict):
            continue
        field = section.get("field")
        resolved = section.get("resolved")
        if not isinstance(field, dict) or not isinstance(resolved, dict):
            continue
        line = str(field.get("line", ""))
        if line not in EVALUATION_LINES:
            continue
        disposition = str(resolved.get("disposition", ""))
        if disposition in {
            "published_value",
            "computed_zero",
            "closure_backed_zero",
        }:
            values[line] = {
                "line": line,
                "title": _LINE_TITLES[line],
                "computed": True,
                "value": resolved.get("value"),
            }
        else:
            values[line] = {
                "line": line,
                "title": _LINE_TITLES[line],
                "computed": False,
                "value": None,
            }
    if set(values) != set(EVALUATION_LINES):
        raise EntryLoopError("entry-state-unavailable")
    return values


_RULE_ROLES = frozenset({"field-mapping", "computation"})
_DEPENDENCY_ROLES = frozenset({"input", "choice"})
_OPERATION_ROLE = "operation-semantics"
_PARAMETER_ROLE = "parameter"


def _line_index(model: Mapping[str, Any]) -> dict[str, tuple[str, str, Any]]:
    """Map each evaluation line's own finding id to (line, title, value).

    Lets a dependency pin on one line's finding be recognized as *another
    evaluation line* rather than raw evidence, without inventing that link --
    the finding ids are exactly the ids the record itself already assigned.
    """
    index: dict[str, tuple[str, str, Any]] = {}
    for section in model.get("sections") or []:
        if not isinstance(section, dict):
            continue
        field = section.get("field")
        resolved = section.get("resolved")
        if not isinstance(field, dict) or not isinstance(resolved, dict):
            continue
        line_id = str(field.get("line", ""))
        if line_id not in EVALUATION_LINES:
            continue
        act = resolved.get("act")
        finding = act.get("finding") if isinstance(act, dict) else None
        if isinstance(finding, dict) and isinstance(finding.get("id"), str):
            index[finding["id"]] = (line_id, _LINE_TITLES.get(line_id, line_id), resolved.get("value"))
    return index


def _dependency_graph(
    model: Mapping[str, Any], line_index: Mapping[str, tuple[str, str, Any]]
) -> dict[str, set[str]]:
    """Each evaluation line's own immediate line dependencies, as a graph."""
    graph: dict[str, set[str]] = {}
    for section in model.get("sections") or []:
        if not isinstance(section, dict):
            continue
        field = section.get("field")
        resolved = section.get("resolved")
        if not isinstance(field, dict) or not isinstance(resolved, dict):
            continue
        line_id = str(field.get("line", ""))
        if line_id not in EVALUATION_LINES:
            continue
        act = resolved.get("act")
        finding = act.get("finding") if isinstance(act, dict) else None
        pins = finding.get("pins") if isinstance(finding, dict) else None
        deps: set[str] = set()
        for pin in pins if isinstance(pins, list) else []:
            if not isinstance(pin, dict) or pin.get("role") not in _DEPENDENCY_ROLES:
                continue
            pin_id = pin.get("id")
            reference = line_index.get(pin_id) if isinstance(pin_id, str) else None
            if reference is not None:
                deps.add(reference[0])
        graph[line_id] = deps
    return graph


def _entry_targets(graph: Mapping[str, set[str]], line_id: str) -> list[str]:
    """Which of the record's entry points (see ENTRY_LINES) this line reaches.

    Generalizes the loop's original single-entry-point "tracesToEntry"
    predicate to however many correctable facts exist. Order follows
    ENTRY_LINES so the result is deterministic regardless of dict iteration.
    """
    return [
        field_key
        for entry_line, field_key in ENTRY_LINES.items()
        if _reaches(graph, line_id, entry_line)
    ]


def _reaches(graph: Mapping[str, set[str]], start: str, target: str) -> bool:
    if start == target:
        return True
    seen = {start}
    stack = [start]
    while stack:
        current = stack.pop()
        for dep in graph.get(current, ()):
            if dep == target:
                return True
            if dep not in seen:
                seen.add(dep)
                stack.append(dep)
    return False


def _line_explanation(
    model: Mapping[str, Any],
    line_id: str,
    line_index: Mapping[str, tuple[str, str, Any]],
    dependency_graph: Mapping[str, set[str]],
) -> dict[str, Any] | None:
    """The walkable, dependency-aware explanation for one line.

    A line whose immediate inputs are other evaluation lines (an aggregation
    or a bracket computation) shows those lines as its dependencies -- a
    reader walks the chain rather than a flat evidence dump. A line with no
    such dependency (a directly entered or directly sourced amount) falls
    back to the presentation model's own recursive citation walk, filtered to
    leaves that carry a declared evidence label. The governing rule and any
    declared operation/parameter pins are surfaced verbatim either way.
    Nothing here is computed, labeled, or invented beyond what the record
    already declared.
    """
    sections = model.get("sections")
    if not isinstance(sections, list):
        return None
    pin_labels = model.get("pinLabels")
    if not isinstance(pin_labels, dict):
        pin_labels = {}
    for section in sections:
        if not isinstance(section, dict):
            continue
        field = section.get("field")
        resolved = section.get("resolved")
        if not isinstance(field, dict) or not isinstance(resolved, dict):
            continue
        if str(field.get("line", "")) != line_id:
            continue

        act = resolved.get("act")
        finding = act.get("finding") if isinstance(act, dict) else None
        pins = finding.get("pins") if isinstance(finding, dict) else None
        pins = pins if isinstance(pins, list) else []

        rules = [
            {"id": pin.get("id"), "role": pin.get("role")}
            for pin in pins
            if isinstance(pin, dict) and pin.get("role") in _RULE_ROLES
        ]
        operations = [
            pin.get("id") for pin in pins if isinstance(pin, dict) and pin.get("role") == _OPERATION_ROLE
        ]
        parameters = [
            pin.get("id") for pin in pins if isinstance(pin, dict) and pin.get("role") == _PARAMETER_ROLE
        ]

        depends_on: list[dict[str, Any]] = []
        for pin in pins:
            if not isinstance(pin, dict) or pin.get("role") not in _DEPENDENCY_ROLES:
                continue
            pin_id = pin.get("id")
            reference = line_index.get(pin_id) if isinstance(pin_id, str) else None
            if reference is not None:
                dep_line, dep_title, dep_value = reference
                depends_on.append({
                    "line": dep_line,
                    "title": dep_title,
                    "value": dep_value,
                    # Same predicate that gates this line's own "jump to
                    # entry" action, applied to the dependency instead of the
                    # line itself -- lets a chip say where it leads before
                    # it's clicked, not just after.
                    "entryTargets": _entry_targets(dependency_graph, dep_line),
                })

        cited_evidence: list[dict[str, Any]] = []
        if not depends_on:
            for site in section.get("citationSites") or []:
                if not isinstance(site, dict):
                    continue
                pin_id = site.get("pinId")
                label = pin_labels.get(pin_id)
                if label is None:
                    continue
                cited_evidence.append({
                    "siteId": site.get("siteId"),
                    "pinId": pin_id,
                    "pinVersion": site.get("pinVersion"),
                    "context": site.get("context"),
                    "label": label,
                })

        return {
            "label": field.get("label"),
            "description": field.get("description"),
            "disposition": resolved.get("disposition"),
            "value": resolved.get("value"),
            "rules": rules,
            "operations": operations,
            "parameters": parameters,
            "dependsOn": depends_on,
            "citedEvidence": cited_evidence,
            "hasSupport": bool(depends_on or cited_evidence),
            # Which of the record's correctable facts this line's own
            # dependency chain actually reaches -- scopes the "jump to
            # entry" action(s) to facts a correction can actually change,
            # per the record's own dependency graph rather than a fixed
            # line list.
            "entryTargets": _entry_targets(dependency_graph, line_id),
        }
    return None


def _parse_amount_with_format(
    value: object,
    format_spec: Mapping[str, Any],
) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise EntryLoopError("entry-value-invalid")
    # Keep the string-normalising branch on its own name. `value` is a union,
    # and reusing it here left the comma/prefix handling below typed as
    # `int | float | str`, which mypy correctly refuses.
    normalized: str | int | float = value
    if isinstance(normalized, str):
        negative = normalized.startswith("-")
        if negative:
            if format_spec.get("requirePositive") is True:
                raise EntryLoopError("entry-value-invalid")
            normalized = normalized[1:]
        currency_symbol = format_spec.get("currencySymbol")
        if not isinstance(currency_symbol, str):
            raise EntryLoopError("entry-format-unavailable")
        if normalized.startswith(currency_symbol):
            if format_spec.get("currencyPrefix") != "accepted":
                raise EntryLoopError("entry-value-invalid")
            normalized = normalized[len(currency_symbol) :]
            if normalized.startswith(currency_symbol):
                raise EntryLoopError("entry-value-invalid")
        elif currency_symbol in normalized:
            raise EntryLoopError("entry-value-invalid")

        max_fraction_digits = format_spec.get("maxFractionDigits")
        if (
            not isinstance(max_fraction_digits, int)
            or isinstance(max_fraction_digits, bool)
            or max_fraction_digits < 0
        ):
            raise EntryLoopError("entry-format-unavailable")
        fraction = (
            rf"(?:\.\d{{1,{max_fraction_digits}}})?"
            if max_fraction_digits
            else ""
        )
        if format_spec.get("commaGrouping") == "accepted":
            pattern = rf"^(?:\d{{1,3}}(?:,\d{{3}})*|\d+){fraction}$"
        else:
            pattern = rf"^\d+{fraction}$"
        if not re.fullmatch(pattern, normalized):
            raise EntryLoopError("entry-value-invalid")
        normalized = normalized.replace(",", "")
        if negative:
            normalized = "-" + normalized
    try:
        amount = Decimal(str(normalized))
    except (InvalidOperation, ValueError):
        raise EntryLoopError("entry-value-invalid") from None
    if not amount.is_finite():
        raise EntryLoopError("entry-value-invalid")
    require_positive = format_spec.get("requirePositive")
    if not isinstance(require_positive, bool):
        raise EntryLoopError("entry-format-unavailable")
    if require_positive and amount <= 0:
        raise EntryLoopError("entry-value-invalid")
    max_fraction_digits = format_spec.get("maxFractionDigits")
    max_value = format_spec.get("maxValue")
    if (
        not isinstance(max_fraction_digits, int)
        or isinstance(max_fraction_digits, bool)
        or max_fraction_digits < 0
        or not isinstance(max_value, str)
    ):
        raise EntryLoopError("entry-format-unavailable")
    exponent = amount.as_tuple().exponent
    if not isinstance(exponent, int) or exponent < -max_fraction_digits:
        raise EntryLoopError("entry-value-invalid")
    try:
        maximum = Decimal(max_value)
    except InvalidOperation:
        raise EntryLoopError("entry-format-unavailable") from None
    # Fail closed on a malformed ceiling independently of the loader path:
    # non-finite or non-positive maxValue is a format defect, not a value defect.
    if not maximum.is_finite() or maximum <= 0:
        raise EntryLoopError("entry-format-unavailable")
    if amount > maximum:
        raise EntryLoopError("entry-value-invalid")
    return int(amount) if amount == amount.to_integral_value() else float(amount)


@dataclass(frozen=True)
class _FactFamily:
    """Everything the loop needs to admit contributions for one enterable fact.

    The loop's first fact (W-2 box 1) had every one of these fields inlined
    as its own constant and its own hand-written block in every method
    below. This is that same shape, named, so a second fact is one more
    instance rather than a second copy of every method -- generalized to
    exactly the two concrete cases this loop has, not to an unbounded N.
    """

    key: str
    content_key: str
    family: Mapping[str, str]
    scope: Mapping[str, str]
    predecessor_horizon: str
    successor_horizon: str
    fact_id: str
    closure_fact_id: str
    evidence_id: str
    missing_label: str
    missing_document: str
    missing_box: str
    answered_label: str
    format_path: Path
    format_marker: str
    field_path: Path
    field_marker: str


_FACT_FAMILIES: tuple[_FactFamily, ...] = (
    _FactFamily(
        key="w2-box1",
        content_key="w2_box1",
        family=W2_FAMILY,
        scope=W2_SCOPE,
        predecessor_horizon=W2_PREDECESSOR,
        successor_horizon=W2_SUCCESSOR,
        fact_id=W2_FACT_ID,
        closure_fact_id=W2_CLOSURE_FACT_ID,
        evidence_id=W2_EVIDENCE_ID,
        missing_label="W-2 from Demo Workshop — Box 1 wages",
        missing_document="Form W-2",
        missing_box="Box 1",
        answered_label="W-2 Box 1",
        format_path=W2_BOX1_FORMAT,
        format_marker="W2_BOX1_FORMAT",
        field_path=W2_BOX1_FIELD,
        field_marker="W2_BOX1_FIELD",
    ),
    _FactFamily(
        key="div1b-qualified",
        content_key="div1b_qualified",
        family=DIV1B_FAMILY,
        scope=DIV1B_SCOPE,
        predecessor_horizon=DIV1B_PREDECESSOR,
        successor_horizon=DIV1B_SUCCESSOR,
        fact_id=DIV1B_FACT_ID,
        closure_fact_id=DIV1B_CLOSURE_FACT_ID,
        evidence_id=DIV1B_EVIDENCE_ID,
        missing_label="1099-DIV from Synthetic dividend payer — Box 1b qualified dividends",
        missing_document="Form 1099-DIV",
        missing_box="Box 1b",
        answered_label="1099-DIV Box 1b",
        format_path=DIV1B_FORMAT_PATH,
        format_marker="DIV1B_FORMAT",
        field_path=DIV1B_FIELD_PATH,
        field_marker="DIV1B_FIELD",
    ),
)


@dataclass(frozen=True)
class EntrySnapshot:
    revision: int
    payload: dict[str, Any]


class SyntheticW2EntryRuntime:
    """One synthetic workspace, serialized contribution admission, live recompute."""

    _FAMILIES: tuple[_FactFamily, ...] = _FACT_FAMILIES

    def __init__(
        self,
        capability: WorkspaceCapability,
        *,
        repo_root: Path,
        seed_acts: Sequence[Mapping[str, Any]] | None = None,
    ) -> None:
        self._capability = capability
        self._repo_root = repo_root
        self._schemas = DerivationSchemas()
        self._lock = Lock()
        self._workspace = bootstrap_workspace(capability, repo_root=repo_root)
        self._log = ActLog(self._workspace.location, self._schemas.registry)
        self._surface = PublicationSurface(
            repo_root / "packages" / "sample_data" / "frrs_t3" / "publication_surface" / "releases",
            repo_root / "packages" / "content" / "tax" / "2025" / "published-packages.json",
            repo_root / "packages" / "content" / "tax" / "2025",
        )
        self._formats: dict[str, dict[str, Any]] = {}
        self._fields: dict[str, dict[str, Any]] = {}
        for fact in self._FAMILIES:
            format_spec = _load_currency_format(repo_root, fact.format_path, fact.format_marker)
            self._formats[fact.key] = format_spec
            self._fields[fact.key] = _load_entry_field(
                repo_root, fact.field_path, fact.field_marker, fact.format_marker, format_spec
            )
        self._previous_lines: dict[str, dict[str, Any]] | None = None
        self._last_accepted = False
        self._last_action = ""
        self._seed(seed_acts or load_seed_acts(repo_root))
        self._snapshot = self._compute_snapshot()

    def _seed(self, seed_acts: Sequence[Mapping[str, Any]]) -> None:
        if self._log.read().revision:
            raise EntryLoopError("entry-workspace-not-empty")
        for expected, act in enumerate(seed_acts):
            body = dict(act)
            if body.get("committed_against") != expected:
                raise EntryLoopError("entry-loop-fixture-invalid")
            self._log.append(body, expected_revision=expected)

    def _current_fact(
        self, fact: _FactFamily, acts: Sequence[Mapping[str, Any]]
    ) -> dict[str, Any] | None:
        state = project(tuple(dict(act) for act in acts), self._schemas.registry)
        currency = compute_currency(state)
        matches = [
            state.findings[finding_id]
            for finding_id in sorted(currency.current_finding_ids)
            if finding_id in state.findings
            and state.findings[finding_id].get("fact_id") == fact.fact_id
        ]
        if len(matches) > 1:
            raise EntryLoopError("entry-state-unavailable")
        return matches[0] if matches else None

    def _contribution_template(self, fact: _FactFamily, revision: int) -> dict[str, Any]:
        nonce = token_urlsafe(18)
        contribution_id = f"demo.entry-loop.contribution.{nonce}"
        payload = {
            "contribution": {
                "schema": "contribution.v1",
                "id": contribution_id,
                "evidence_id": fact.evidence_id,
                "content": {
                    "mode": "manual-entry",
                    "synthetic": True,
                },
            }
        }
        return {
            "schema": "act.v1",
            "act_id": f"demo.entry-loop.act.contribution.{nonce}",
            "kind": "contribution",
            "actor": SCOPE_USER,
            "at": "2026-07-29T00:00:00Z",
            "committed_against": revision,
            "payload": payload,
        }

    def _compute_snapshot(self) -> EntrySnapshot:
        contents = self._log.read()
        revision = contents.revision
        output_name = f"entry-state-{revision}.json"
        outcome = live_coordinate_run(
            self._capability,
            repo_root=self._repo_root,
            authoritative_acts=contents.acts,
            workspace_revision=revision,
            run_scope=RUN_SCOPE,
            scope_user=SCOPE_USER,
            request={"schema": "run-request.v1"},
            run_id=f"demo.entry-loop.run.{revision}",
            governance_pins=[],
            surface=self._surface,
            output_name=output_name,
            schemas=self._schemas,
        )
        if outcome.refusal is not None or outcome.output_path is None:
            reason = outcome.refusal.reason if outcome.refusal is not None else "unknown"
            raise EntryLoopError(f"entry-run-refused:{reason}")
        if outcome.presentation_path is None:
            raise EntryLoopError("entry-state-unavailable")
        try:
            report = json.loads(outcome.output_path.read_text("utf-8"))
            model = json.loads(outcome.presentation_path.read_text("utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            raise EntryLoopError("entry-state-unavailable") from None

        lines_by_id = _line_values(model)
        line_index = _line_index(model)
        dependency_graph = _dependency_graph(model, line_index)
        current_by_key = {
            fact.key: self._current_fact(fact, contents.acts) for fact in self._FAMILIES
        }
        missing_facts = [fact for fact in self._FAMILIES if current_by_key[fact.key] is None]
        blocked = [
            row
            for row in report.get("dispositions", [])
            if isinstance(row, dict) and row.get("disposition") == "blocked"
        ]
        fully_computed = not missing_facts and not blocked and all(
            line["computed"] for line in lines_by_id.values()
        )
        lines: list[dict[str, Any]] = []
        for line_id in EVALUATION_LINES:
            line = dict(lines_by_id[line_id])
            line["group"] = (
                "expected-impact"
                if line_id in EXPECTED_IMPACT_LINES
                else "untouched-comparison"
            )
            before = (
                self._previous_lines.get(line_id)
                if self._previous_lines is not None
                else None
            )
            if before is None:
                line["change"] = "blocked" if not line["computed"] else "baseline"
            elif (
                before["computed"] == line["computed"]
                and before["value"] == line["value"]
            ):
                line["change"] = "unchanged"
            else:
                line["change"] = "changed"
            # Graph-structural, unlike the rest of a line's explanation --
            # computable whether or not the line itself has resolved yet, so
            # a still-blocked line can still say which missing fact(s) would
            # unblock it, not only a computed one say which fact corrected it.
            line["entryTargets"] = _entry_targets(dependency_graph, line_id)
            if line_id in EXPLAINED_LINES and line["computed"]:
                line["explanation"] = _line_explanation(model, line_id, line_index, dependency_graph)
            lines.append(line)

        payload = {
            "revision": revision,
            "missing": [
                {
                    "id": fact.key,
                    "label": fact.missing_label,
                    "document": fact.missing_document,
                    "box": fact.missing_box,
                    "target": fact.key,
                }
                for fact in missing_facts
            ],
            "answered": [
                {
                    "id": fact.key,
                    "label": fact.answered_label,
                    "value": current["value"],
                    "target": fact.key,
                }
                for fact in self._FAMILIES
                if (current := current_by_key[fact.key]) is not None
            ],
            "lines": lines,
            "accepted": self._last_accepted,
            "last_action": self._last_action,
            "complete": fully_computed,
            "computed": fully_computed,
            "field_contract": dict(self._fields),
            "contributions": {
                fact.key: self._contribution_template(fact, revision)
                for fact in self._FAMILIES
            },
        }
        self._previous_lines = lines_by_id
        return EntrySnapshot(revision=revision, payload=payload)

    def snapshot(self) -> EntrySnapshot:
        with self._lock:
            return self._snapshot

    @staticmethod
    def _validate_template(
        submitted: Mapping[str, Any],
        expected: Mapping[str, Any],
        content_key: str,
    ) -> None:
        if set(submitted) != set(expected):
            raise EntryLoopError("entry-event-invalid")
        for key in ("schema", "act_id", "kind", "actor", "at", "committed_against"):
            if submitted.get(key) != expected.get(key):
                raise EntryLoopError("entry-event-invalid")
        submitted_payload = submitted.get("payload")
        expected_payload = expected.get("payload")
        if not isinstance(submitted_payload, dict) or not isinstance(expected_payload, dict):
            raise EntryLoopError("entry-event-invalid")
        submitted_contribution = submitted_payload.get("contribution")
        expected_contribution = expected_payload.get("contribution")
        if not isinstance(submitted_contribution, dict) or not isinstance(
            expected_contribution, dict
        ):
            raise EntryLoopError("entry-event-invalid")
        for key in ("schema", "id", "evidence_id"):
            if submitted_contribution.get(key) != expected_contribution.get(key):
                raise EntryLoopError("entry-event-invalid")
        content = submitted_contribution.get("content")
        if not isinstance(content, dict) or set(content) != {
            "mode",
            "synthetic",
            content_key,
        }:
            raise EntryLoopError("entry-event-invalid")
        if content.get("mode") != "manual-entry" or content.get("synthetic") is not True:
            raise EntryLoopError("entry-event-invalid")

    def _fact_for_evidence(self, evidence_id: object) -> _FactFamily:
        for fact in self._FAMILIES:
            if fact.evidence_id == evidence_id:
                return fact
        raise EntryLoopError("entry-event-invalid")

    def contribute(self, submitted: Mapping[str, Any]) -> EntrySnapshot:
        """Admit one browser-originated contribution and recompute the return.

        Which fact family the submission targets is read from its own
        ``evidence_id`` -- unique per family -- rather than a caller-supplied
        discriminator, so a submission can't claim to be one fact while
        actually carrying another's evidence.
        """

        with self._lock:
            submitted_payload = (
                submitted.get("payload") if isinstance(submitted, Mapping) else None
            )
            submitted_contribution = (
                submitted_payload.get("contribution")
                if isinstance(submitted_payload, Mapping)
                else None
            )
            evidence_id = (
                submitted_contribution.get("evidence_id")
                if isinstance(submitted_contribution, Mapping)
                else None
            )
            fact = self._fact_for_evidence(evidence_id)

            expected = self._snapshot.payload["contributions"].get(fact.key)
            if not isinstance(expected, dict):
                raise EntryLoopError("entry-state-unavailable")
            self._validate_template(submitted, expected, fact.content_key)
            contribution_act = json.loads(json.dumps(submitted))
            contribution = contribution_act["payload"]["contribution"]
            try:
                amount = _parse_amount_with_format(
                    contribution["content"][fact.content_key],
                    self._formats[fact.key],
                )
            except EntryLoopError as exc:
                if str(exc) == "entry-value-invalid":
                    raise EntryLoopError(f"entry-value-invalid:{fact.key}") from None
                raise
            contribution["content"][fact.content_key] = amount

            contents = self._log.read()
            if contribution_act["committed_against"] != contents.revision:
                raise EntryLoopError("entry-event-stale")
            current = self._current_fact(fact, contents.acts)
            contribution_id = contribution["id"]
            finding_body = {
                "schema": "finding.v2",
                "id": _derived_id(
                    "demo.entry-loop.finding.",
                    {"contribution": contribution_id, "value": amount},
                ),
                "fact_id": fact.fact_id,
                "value": amount,
                "basis": "documentary",
                "evidence_ids": [fact.evidence_id],
                "contribution_id": contribution_id,
            }
            successor_index = contents.revision + 1
            successor_base = {
                "schema": "act.v1",
                "actor": SCOPE_USER,
                "at": "2026-07-29T00:00:01Z",
                "committed_against": successor_index,
            }
            successor_acts: list[dict[str, Any]] = []
            if current is None:
                payload = {
                    "family": dict(fact.family),
                    "scope": dict(fact.scope),
                    "member": {"action": "assert", "finding": finding_body},
                    "successor": {
                        "id": fact.successor_horizon,
                        "predecessor": fact.predecessor_horizon,
                    },
                }
                successor_acts.append(
                    {
                        **successor_base,
                        "act_id": _derived_id(
                            "demo.entry-loop.act.member.", payload
                        ),
                        "kind": "member-transition",
                        "payload": payload,
                    }
                )
                closure_finding = {
                    "schema": "finding.v2",
                    "id": _derived_id(
                        "demo.entry-loop.closure.",
                        {"contribution": contribution_id, "horizon": fact.successor_horizon},
                    ),
                    "fact_id": fact.closure_fact_id,
                    "value": True,
                    "basis": "documentary",
                    "evidence_ids": [fact.evidence_id],
                    "contribution_id": contribution_id,
                }
                closure_payload = {"finding": closure_finding}
                successor_acts.append(
                    {
                        **successor_base,
                        "act_id": _derived_id(
                            "demo.entry-loop.act.closure.", closure_payload
                        ),
                        "kind": "assertion",
                        "at": "2026-07-29T00:00:02Z",
                        "committed_against": successor_index + 1,
                        "payload": closure_payload,
                    }
                )
                action = "entered"
            else:
                payload = {"finding": finding_body}
                successor_acts.append(
                    {
                        **successor_base,
                        "act_id": _derived_id(
                            "demo.entry-loop.act.correction.", payload
                        ),
                        "kind": "assertion",
                        "payload": payload,
                    }
                )
                action = "corrected"

            state = project(tuple(contents.acts), self._schemas.registry)
            try:
                admitted = apply_contribution_batch(
                    state,
                    contribution_act=contribution_act,
                    successor_acts=successor_acts,
                    registry=self._schemas.registry,
                    record_id=_derived_id(
                        "demo.entry-loop.record.", contribution_id
                    ),
                    workspace_revision=contents.revision,
                )
            except (ContributionError, KeyError, TypeError):
                raise EntryLoopError("entry-event-rejected") from None
            if admitted.terminal_record["phase"] != "completed":
                raise EntryLoopError("entry-event-rejected")

            revision = self._log.append(
                contribution_act, expected_revision=contents.revision
            )
            for act in successor_acts:
                revision = self._log.append(act, expected_revision=revision)

            self._last_accepted = True
            self._last_action = action
            self._snapshot = self._compute_snapshot()
            return self._snapshot


class _EntryHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(
        self,
        runtime: SyntheticW2EntryRuntime,
        static_root: Path,
        route: str,
    ) -> None:
        self.runtime = runtime
        self.static_root = static_root.resolve(strict=True)
        self.route = route.rstrip("/")
        super().__init__(("127.0.0.1", 0), _EntryRequestHandler)


class _EntryRequestHandler(BaseHTTPRequestHandler):
    server: _EntryHTTPServer

    def log_message(self, _format: str, *_args: object) -> None:
        return

    def _json(self, status: int, body: Mapping[str, Any]) -> None:
        encoded = _canonical_bytes(body)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(encoded)

    def _target(self) -> tuple[str, str] | None:
        try:
            parsed = urlsplit(self.path)
        except ValueError:
            return None
        if parsed.query or parsed.fragment:
            return None
        prefix = f"{self.server.route}/"
        if not parsed.path.startswith(prefix):
            return None
        return parsed.path, parsed.path[len(prefix) :]

    def _serve_static(self, relative: str) -> None:
        relative = relative or "index.html"
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts:
            self.send_error(404)
            return
        candidate = (self.server.static_root / Path(*pure.parts)).resolve(
            strict=False
        )
        try:
            candidate.relative_to(self.server.static_root)
        except ValueError:
            self.send_error(404)
            return
        if not candidate.is_file():
            self.send_error(404)
            return
        try:
            body = candidate.read_bytes()
        except OSError:
            self.send_error(404)
            return
        mime = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; connect-src 'self'; "
            "img-src 'self' data:; object-src 'none'; base-uri 'none'",
        )
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        target = self._target()
        if target is None:
            self.send_error(404)
            return
        _, relative = target
        if compare_digest(relative, "api/state"):
            self._json(200, self.server.runtime.snapshot().payload)
            return
        self._serve_static(relative)

    def do_POST(self) -> None:  # noqa: N802
        target = self._target()
        if target is None or not compare_digest(target[1], "api/contributions"):
            self.send_error(404)
            return
        if self.headers.get_content_type() != "application/json":
            self._json(415, {"error": "Contribution request must be JSON."})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            size = 0
        if size <= 0 or size > _MAX_REQUEST_BYTES:
            self._json(400, {"error": "Contribution request is invalid."})
            return
        try:
            submitted = json.loads(self.rfile.read(size))
            if not isinstance(submitted, dict):
                raise ValueError
            snapshot = self.server.runtime.contribute(submitted)
        except EntryLoopError as exc:
            reason = str(exc)
            if reason.startswith("entry-value-invalid"):
                _, _, key = reason.partition(":")
                field_contract = self.server.runtime.snapshot().payload["field_contract"]
                format_spec = field_contract.get(key, {}).get("format") if key else None
                message = (
                    _field_error(format_spec)
                    if format_spec
                    else "The contribution was not accepted. No entry was changed."
                )
            elif reason == "entry-event-stale":
                message = "The entry session changed. Reload the current entry."
            else:
                message = "The contribution was not accepted. No entry was changed."
            self._json(422, {"error": message})
            return
        except (json.JSONDecodeError, UnicodeError, ValueError):
            self._json(400, {"error": "Contribution request is invalid."})
            return
        self._json(200, snapshot.payload)

    def do_HEAD(self) -> None:  # noqa: N802
        self.send_error(405)


class EntryLoopServer(AbstractContextManager["EntryLoopServer"]):
    """Owned loopback server for one synthetic entry runtime."""

    def __init__(
        self,
        runtime: SyntheticW2EntryRuntime,
        static_root: Path,
    ) -> None:
        route = f"/entry/{token_urlsafe(32)}"
        self._http = _EntryHTTPServer(runtime, static_root, route)
        self._thread = Thread(
            target=self._http.serve_forever,
            name="synthetic-entry-loopback",
            daemon=True,
        )
        self._thread.start()
        self.url = (
            f"http://127.0.0.1:{self._http.server_address[1]}"
            f"{route}/index.html"
        )
        self._closed = False

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            self._http.shutdown()
        finally:
            self._http.server_close()
        self._thread.join(timeout=3)
        if self._thread.is_alive():
            raise EntryLoopError("entry-server-teardown-failed")

    def __exit__(self, _type: Any, _value: Any, _traceback: Any) -> None:
        self.close()


__all__ = [
    "COMPARISON_LINES",
    "ENTRY_FIXTURE",
    "EVALUATION_LINES",
    "EXPECTED_IMPACT_LINES",
    "EntryLoopError",
    "EntryLoopServer",
    "EntrySnapshot",
    "SyntheticW2EntryRuntime",
    "build_entry_surface",
    "load_seed_acts",
    "resolve_entry_surface",
]
