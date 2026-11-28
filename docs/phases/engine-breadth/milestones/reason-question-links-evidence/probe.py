"""Read the declared asking reasons and their saved links for P0 evidence."""

from __future__ import annotations

from collections import defaultdict
from functools import cache
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))

from tools import recorded_replay as rr
from selection import selection_declarations

BASE = "5993ce933"
CORE = "v109"
PROJECTION = "packages/derivation/presentation_projection.py"
PAGE = "packages/presentation/pages/citation-walk.v1.html"
PROMPT = "questionPrompt"


@cache
def baseline_source(path):
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"],
                   cwd=REPO, timeout=20, check=True)
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"],
                                   cwd=REPO, timeout=20, text=True)


def producer(member):
    return {key: member[key] for key in ("schema", "id", "version")}


def producer_key(ref):
    return ref["schema"], ref["id"], ref["version"]


def ordered_producers(refs):
    return [ref for _, ref in sorted({producer_key(ref): ref for ref in refs}.items())]


def declarations(members):
    """Index only the adopted declarations that the two question routes read."""
    input_by_type = defaultdict(list)
    family_by_id = defaultdict(list)
    for member in members:
        schema = member.get("schema")
        if schema == "input-question.v1":
            input_by_type[member["fact_type"]["id"]].append(member)
        elif schema in {f"source-closure-mapping.v{n}" for n in range(1, 5)}:
            if schema == "source-closure-mapping.v4":
                families = [row["family"] for row in member["families"]]
            else:
                families = [member["family"]]
            for family in families:
                family_by_id[family["id"]].append(member)
    return input_by_type, family_by_id


def declaration_text(member):
    return member.get("question", member.get("closure_question"))


def prompt_id(section, index):
    return f"question-prompt-{section}-{index}"


def linked_positions(resolved):
    return {i for ref in resolved.get("questionRefs", ()) for i in ref["reasonIndices"]}


def asking_positions(resolved):
    """Indices in reason order, counting both forms of saved presentation link."""
    linked = linked_positions(resolved)
    return [i for i, reason in enumerate(resolved.get("reasons", ())) if i in linked or PROMPT in reason]


def baseline_prompts(model, members):
    """Independent inventory by adopted wording, including imperative prompts.

    The scratch projector has to prove the same positions from walked origins.
    An exact-wording collision with unwalked content is a replay discrepancy.
    """
    by_input, by_family = declarations(members)
    by_text = defaultdict(list)
    for index in (by_input, by_family):
        for declarations_for_subject in index.values():
            for member in declarations_for_subject:
                if text := declaration_text(member):
                    by_text[text].append(producer(member))
    for text, member in selection_declarations(members):
        by_text[text].append(producer(member))
    found = {}
    for section in model["sections"]:
        resolved = section["resolved"]
        linked = linked_positions(resolved)
        for index, reason in enumerate(resolved.get("reasons", ())):
            if index not in linked and reason["sentence"] in by_text:
                found[section["id"], index] = ordered_producers(by_text[reason["sentence"]])
    return found


def prompt_positions(model):
    return {
        (section["id"], index): reason[PROMPT]
        for section in model["sections"]
        for index, reason in enumerate(section["resolved"].get("reasons", ()))
        if PROMPT in reason
    }


def digest(value):
    return rr.snapshot_sha256(value)


def summary_json(value):
    encoded = json.dumps(value, indent=2, sort_keys=True) + "\n"
    rr._check_no_local_paths(encoded, "P0 reason-question-links summary")
    return encoded
