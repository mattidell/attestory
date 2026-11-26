"""Package-validation controls for the proposed answer-explanation.v1 (scratch only).

Run inside the scratch export (scratch_build.py), from its root:
  python3 docs/phases/engine-breadth/milestones/line16-next-step-evidence/validation_controls.py

validate_package (no published checksums passed, so only the rules are
tested) must accept scratch v109 as built and reject each mutation with
exactly the issue code named: a value outside the fact type's domain, a fact
type with no adopted input question, a fact type outside the package's fact
surface, a duplicate (fact type, value), and a member pinned with another
role. It must also reject answer-explanation.v1 members on artifact-package.v44.
Writes validation-controls.json next to this script.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))

from packages.derivation.loader import DerivationSchemas  # noqa: E402
from packages.derivation.package_validation import validate_package  # noqa: E402
from tools.package_successor import load_corpus  # noqa: E402

P = "tax.us.2025."
CONTENT = REPO / "packages/content/tax/2025"
TARGET = (P + "answer-explanation.exception1-no-capital-losses-no", "v1")


def codes(package: dict, corpus: dict, schemas: DerivationSchemas) -> list[str]:
    try:
        outcome = validate_package(package, corpus, schemas)
    except Exception as exc:  # a schema-level refusal is a rejection too
        return ["REFUSED:" + type(exc).__name__]
    return sorted({issue.code for issue in outcome.issues}) if not outcome.ok else []


def main() -> None:
    schemas = DerivationSchemas()
    corpus, _ = load_corpus(CONTENT)
    package = json.loads((CONTENT / "package.core-calculations.v109.json").read_text(encoding="utf-8"))
    rows = {"as_built": codes(package, corpus, schemas)}

    def mutated(change) -> list[str]:
        c = copy.deepcopy(corpus)
        p = copy.deepcopy(package)
        change(c, p)
        return codes(p, c, schemas)

    def value(c, p):
        c[TARGET]["value"] = "maybe"

    def no_question(c, p):
        c[TARGET]["fact_type"] = {"id": P + "schedule-d-required.conclusion", "version": "v1"}

    def outside_surface(c, p):
        c[TARGET]["fact_type"] = {"id": P + "exception1.no-capital-losses", "version": "v9"}

    def duplicate(c, p):
        c[TARGET]["fact_type"] = {"id": P + "exception1.only-box2a-capital-gains", "version": "v1"}

    def role(c, p):
        for member in p["members"]:
            if (member["id"], member["version"]) == TARGET:
                member["role"] = "input-question"

    def old_package_schema(c, p):
        p["schema"] = "artifact-package.v44"

    for name, change in (("value_outside_domain", value), ("question_absent", no_question),
                         ("fact_type_outside_surface", outside_surface), ("duplicate", duplicate),
                         ("role_mismatch", role), ("on_artifact_package_v44", old_package_schema)):
        rows[name] = mutated(change)
    expected = {"as_built": [], "value_outside_domain": ["ANSWER_EXPLANATION_VALUE_OUTSIDE_DOMAIN"],
                "question_absent": ["ANSWER_EXPLANATION_QUESTION_ABSENT"],
                "duplicate": ["ANSWER_EXPLANATION_DUPLICATE"], "role_mismatch": ["ROLE_MISMATCH"]}
    verdicts = {name: ("PASS" if (expected[name] == got if name in expected else bool(got)) else "FAIL")
                for name, got in rows.items()}
    body = {"format": "line16-next-step-validation-controls.v1", "package": "scratch v109",
            "issue_codes": rows, "verdicts": verdicts, "all_pass": all(v == "PASS" for v in verdicts.values())}
    (HERE / "validation-controls.json").write_text(json.dumps(body, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(body, indent=1))


if __name__ == "__main__":
    main()
