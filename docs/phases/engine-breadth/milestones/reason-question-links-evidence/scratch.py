"""Overlay the ratified projector and page in memory for the P0 experiment."""

from __future__ import annotations

from collections import defaultdict
from functools import cache
import re
import sys
from types import ModuleType

from probe import (
    PAGE, PROJECTION, PROMPT, baseline_source, declaration_text, declarations,
    linked_positions, ordered_producers, producer,
)

PRODUCER_SCHEMAS = {"input-question.v1", *(f"source-closure-mapping.v{n}" for n in range(1, 5))}


def refs_for_text(members, sentence):
    return ordered_producers(producer(member) for member in members if declaration_text(member) == sentence)


def reached_prompts(indexes, families, facts):
    """Keep declared producer origin from accepted family and fact walks."""
    by_type, by_family = indexes
    plain = defaultdict(list)
    for index, keys in ((by_type, facts), (by_family, families)):
        for key in keys:
            for member in index.get(key, ()):
                plain[declaration_text(member)].append(member)
    return plain


def attach_prompts(resolved, plain):
    linked = linked_positions(resolved)
    for i, reason in enumerate(resolved.get("reasons", ())):
        if i in linked:
            continue
        if "memberLabel" not in reason and (refs := refs_for_text(plain.get(reason["sentence"], ()), reason["sentence"])):
            reason[PROMPT] = refs


def validate_prompts(model, error):
    for section in model["sections"]:
        resolved = section["resolved"]
        linked = linked_positions(resolved)
        for i, reason in enumerate(resolved.get("reasons", ())):
            if PROMPT not in reason:
                continue
            refs = reason[PROMPT]
            if (resolved["disposition"] != "blocked" or i in linked or not isinstance(refs, list)
                    or not refs or any(not isinstance(ref, dict) or set(ref) != {"schema", "id", "version"}
                        or ref["schema"] not in PRODUCER_SCHEMAS or not isinstance(ref["id"], str)
                        or not ref["id"] or not isinstance(ref["version"], str)
                        or not re.fullmatch(r"v[0-9]+", ref["version"]) for ref in refs)
                    or refs != ordered_producers(refs)):
                raise error("invalid display-only question prompt")


def replace_once(source, anchor, replacement):
    if source.count(anchor) != 1:
        raise ValueError(f"expected exactly one scratch anchor {anchor!r}")
    return source.replace(anchor, replacement, 1)


def scratch_projection(source):
    edits = (
        (
            "    sale_reasons_out: dict[str, list[dict[str, Any]]] | None = None,\n",
            "    sale_reasons_out: dict[str, list[dict[str, Any]]] | None = None,\n    prompt_origins_out=None,\n    prompt_indexes=None,\n",
        ),
        (
            "        reasons = []\n        for text in sorted(sentences):",
            "        if prompt_origins_out is not None:\n"
            "            prompt_origins_out.update(reached_prompts(prompt_indexes, families, facts))\n"
            "        reasons = []\n        for text in sorted(sentences):",
        ),
        (
            "            reasons.append(member_reason)",
            "            if prompt_origins_out is not None:\n"
            "                by_type, _ = prompt_indexes\n"
            "                declarations_for_member = [member for fact, keys in member_facts if keys == _keys\n"
            "                                           for member in by_type.get(fact, ())]\n"
            "                if refs := refs_for_text(declarations_for_member, member_sentence):\n"
            "                    member_reason[PROMPT] = refs\n"
            "            reasons.append(member_reason)",
        ),
        (
            "        question = questions[partial_family]\n        reasons =",
            "        question = questions[partial_family]\n"
            "        if prompt_origins_out is not None:\n"
            "            _, by_family = prompt_indexes\n"
            "            prompt_origins_out[question] = by_family.get(partial_family, ())\n"
            "        reasons =",
        ),
        (
            "    def field_closure_reasons(",
            "    prompt_indexes = declarations(resolved_members)\n\n    def field_closure_reasons(",
        ),
        (
            '            "sale_reasons_out": sale_reasons,',
            '            "sale_reasons_out": sale_reasons,\n            "prompt_origins_out": prompt_origins,\n            "prompt_indexes": prompt_indexes,',
        ),
        (
            "        sale_reasons: dict[str, list[dict[str, Any]]] = {}",
            "        sale_reasons: dict[str, list[dict[str, Any]]] = {}\n        prompt_origins = {}",
        ),
        (
            '                selection_reasons = resolved["reasons"]',
            '                selection_reasons = resolved["reasons"]\n'
            '                for selection_reason in selection_reasons:\n'
            '                    prompt_origins.pop(selection_reason["sentence"], None)',
        ),
        (
            "        if answer_sentences:\n            # Append",
            "        attach_prompts(resolved, prompt_origins)\n"
            "        if answer_sentences:\n            # Append",
        ),
        (
            '"factId", "statementLabel", "statementPayerLabel", "memberLabel", "memberOrdinal", "saleLabel",',
            '"factId", "statementLabel", "statementPayerLabel", "memberLabel", "memberOrdinal", "saleLabel", PROMPT,',
        ),
        (
            'if set(reason) != {"sentence", "saleLabel"} or not has_sale_label_text(name):',
            'if set(reason) - {PROMPT} != {"sentence", "saleLabel"} or not has_sale_label_text(name):',
        ),
        (
            "                _validate_question_groups(model)",
            "                _validate_question_groups(model)\n"
            "                validate_prompts(model, PresentationModelError)",
        ),
    )
    for anchor, replacement in edits:
        source = replace_once(source, anchor, replacement)
    return source


@cache
def projectors():
    original = baseline_source(PROJECTION)
    namespace = {
        name: globals()[name] for name in
        ("PROMPT", "attach_prompts", "declarations", "reached_prompts", "refs_for_text", "validate_prompts")
    }
    modules = []
    for name, source, bindings in (
        ("reason_links_base", original, {}),
        ("reason_links_scratch", scratch_projection(original), namespace),
    ):
        module = ModuleType(f"packages.derivation.{name}")
        module.__dict__.update(bindings)
        module.__file__ = PROJECTION
        sys.modules[module.__name__] = module
        exec(compile(source, PROJECTION, "exec"), module.__dict__)
        modules.append(module)
    return tuple(modules)


def scratch_page():
    html = baseline_source(PAGE)
    html = replace_once(html, 'function renderQuestionGroups(container) {', '''
function promptAddress(section, index) {
  return "question-prompt-" + encodeURIComponent(section.id) + "-" + index;
}

function promptCard(section, index, content) {
  const root = document.getElementById("question-groups-root");
  const card = el("article", { class: "question-group", id: promptAddress(section, index) }, []);
  card.appendChild(el("h3", null, content()));
  const field = section.field;
  card.appendChild(el("p", null, [(field.label || section.id) +
    (field.line !== undefined ? " (Line " + field.line + ")" : "")]));
  root.appendChild(card);
}

function renderQuestionGroups(container) {''')
    html = replace_once(html,
        '      if (hasSaleLabelText(reason.saleLabel)) {\n'
        '        return [el("li", { id: isLine21 ? "line21-reason-" + index : undefined }, [\n'
        '          el("strong", { class: "sale-label" }, [reason.saleLabel + ": "]), reason.sentence,\n'
        '        ])];\n      }',
        '      function reasonContent() {\n'
        '      if (hasSaleLabelText(reason.saleLabel)) {\n'
        '        return [el("strong", { class: "sale-label" }, [reason.saleLabel + ": "]), reason.sentence];\n'
        '      }')
    return replace_once(html,
        '      return [el("li", { id: isLine21 ? "line21-reason-" + index : undefined }, name ? [el("strong", prefixAttrs, [name + ": "]), reason.sentence] : [reason.sentence])];',
        '      return name ? [el("strong", prefixAttrs, [name + ": "]), reason.sentence] : [reason.sentence];\n'
        '      }\n'
        '      let content = reasonContent();\n'
        '      if (MODEL.schema === "presentation-model.v3" && reason.questionPrompt) {\n'
        '        promptCard(section, index, reasonContent);\n'
        '        content = [el("a", { href: "#" + promptAddress(section, index) }, content)];\n'
        '      }\n'
        '      return [el("li", { id: isLine21 ? "line21-reason-" + index : undefined }, content)];')
