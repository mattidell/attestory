"""Widened core v102 successors: Step 4 is skipped for every filing status.

A qualifying child who has no valid SSN is still a qualifying child. The 2025
Schedule EIC instructions say that filer claims the self-only credit and
attaches Schedule EIC. No sentence in the 2025 Form 1040 instructions or
Publication 596 sends a filer whose qualifying children all lack a valid SSN
to Step 4 or chapter 3.

This keeps the P0 successors and changes three of them. Age and main home
skip when a qualifying child is present, with no status-class test. Not
claimable as a dependent does the same. The amount column stays
``rule.eic-child.counts``, which still requires the SSN test.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent


def _p0():
    spec = importlib.util.spec_from_file_location("ens_t1_p0_design", HERE / "design.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


d = _p0()

NOT_CLAIMABLE_RULE = d.P + "rule.eic-answer.not-claimable-as-dependent"
NOT_CLAIMABLE_FILE = "rule.eic-answer.not-claimable-as-dependent.v4.json"
NOT_CLAIMABLE_SOURCE = "rule.eic-answer.not-claimable-as-dependent.v3.json"

P = d.P
PRESENT = d.PRESENT
STATUS_CLASS = d.STATUS_CLASS
QUALIFIES_RULE = d.QUALIFIES_RULE
PRESENT_RULE = d.PRESENT_RULE
CLASS_RULE = d.CLASS_RULE
EARLY_RULE = d.EARLY_RULE
QUESTIONS_RULE = d.QUESTIONS_RULE
SEP_RULE = d.SEP_RULE
NOT_MARRIED_RULE = d.NOT_MARRIED_RULE
AGE_RULE = d.AGE_RULE
HOME_RULE = d.HOME_RULE
QUALIFIES_FILE = d.QUALIFIES_FILE
PRESENT_FILE = d.PRESENT_FILE
CLASS_FILE = d.CLASS_FILE
EARLY_FILE = d.EARLY_FILE
QUESTIONS_FILE = d.QUESTIONS_FILE
SEP_FILE = d.SEP_FILE
NOT_MARRIED_FILE = d.NOT_MARRIED_FILE
AGE_FILE = d.AGE_FILE
HOME_FILE = d.HOME_FILE
dump = d.dump

REPLACED = {**d.REPLACED, NOT_CLAIMABLE_RULE: "v3"}

_AGE = (
    "v4: also 1 when a qualifying child is present, so Step 4 question 2 is not "
    "asked of any filing status, including a filer whose qualifying child has no valid SSN."
)
_HOME = (
    "v4: also 1 when a qualifying child is present, so Step 4 question 3 is not "
    "asked of any filing status, including a filer whose qualifying child has no valid SSN."
)
_CLAIM = (
    " v4: also 1 when a qualifying child is present, so the no-child question is not "
    "asked of a filer whose qualifying child has no valid SSN."
)


def _present_skip(prior: dict[str, Any], version: str, sentence: str) -> dict[str, Any]:
    out = json.loads(json.dumps(prior))
    out["version"] = version
    d._depend(out, PRESENT)
    d._skip_any(out).append(d._gt(PRESENT, 0))
    out["notes"] = prior["notes"] + " " + sentence
    assert STATUS_CLASS not in out["requires"] or STATUS_CLASS in prior["requires"]
    assert PRESENT in out["requires"]
    return out


def written(content: Path) -> dict[str, dict[str, Any]]:
    bodies = d.written(content)
    read = lambda name: json.loads((content / name).read_text(encoding="utf-8"))  # noqa: E731
    bodies[AGE_FILE] = _present_skip(read(d.SOURCES[AGE_FILE]), "v4", _AGE)
    bodies[HOME_FILE] = _present_skip(read(d.SOURCES[HOME_FILE]), "v4", _HOME)
    bodies[NOT_CLAIMABLE_FILE] = _present_skip(read(NOT_CLAIMABLE_SOURCE), "v4", _CLAIM)
    assert STATUS_CLASS not in bodies[AGE_FILE]["requires"]
    assert STATUS_CLASS not in bodies[HOME_FILE]["requires"]
    assert set(bodies) == set(d.SOURCES) | {NOT_CLAIMABLE_FILE}
    return bodies
