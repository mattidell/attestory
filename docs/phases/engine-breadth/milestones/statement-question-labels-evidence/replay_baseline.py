"""Load the published evaluator and projection from before the statement-label build."""

from __future__ import annotations

import subprocess
import sys
from functools import lru_cache
from pathlib import Path
from types import ModuleType

from packages.derivation import evaluator, presentation_projection

REPO = Path(__file__).resolve().parents[5]


@lru_cache(maxsize=1)
def baseline_ref() -> str:
    builds = subprocess.check_output(
        ["git", "log", "--format=%H", "--grep=^build(statement-question-labels)", "HEAD"],
        cwd=REPO, text=True, timeout=15,
    ).splitlines()
    if len(builds) != 1:
        raise ValueError(f"expected one statement-question-labels build in HEAD history, found {len(builds)}")
    return subprocess.check_output(
        ["git", "rev-parse", "--verify", f"{builds[0]}^"], cwd=REPO, text=True, timeout=15,
    ).strip()


@lru_cache(maxsize=2)
def baseline(name: str) -> ModuleType:
    ref = baseline_ref()
    source = subprocess.check_output(
        ["git", "show", f"{ref}:packages/derivation/{name}.py"], cwd=REPO, timeout=15,
    )
    module = ModuleType(f"statement_labels_baseline_{name}")
    sys.modules[module.__name__] = module
    exec(compile(source, f"{ref}:{name}.py", "exec"), vars(module))
    if name == "evaluator":
        vars(module)["EvalBlocked"] = evaluator.EvalBlocked
    else:
        vars(module)["PresentationModelError"] = presentation_projection.PresentationModelError
    return module
