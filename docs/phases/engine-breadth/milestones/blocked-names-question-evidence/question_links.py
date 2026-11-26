"""Which reasons on a blocked line ask the filer a question.

Shared by the blocked-names-question and preferential-base-reason evidence
probes (question-filter milestone, Decision 1).

From presentation-model.v3 onward the saved model says which reasons are
questions. ``resolved.questionRefs[]`` lists each question group a blocked line
asks, and each entry's ``reasonIndices`` names the positions in
``resolved.reasons`` that carry the group's question sentence. The projection
writes these indices (``_closure_question_reasons`` and
``_finalize_question_references`` in
``packages/derivation/presentation_projection.py``) and its validator rejects
an index whose sentence differs from the group's question. A reason is a
question here when an index points at it, whatever its punctuation.

Models older than v3 carry no question links. For those, and only those, a
reason counts as a question when its sentence contains a question mark.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

LINKED_SCHEMAS = frozenset({"presentation-model.v3"})


def links_questions(schema: Any) -> bool:
    """True when a model of this schema marks its questions by link."""
    return str(schema) in LINKED_SCHEMAS


def asked(resolved: Mapping[str, Any], schema: Any,
          clean: Callable[[str], str] = lambda text: text) -> list[str]:
    """The question sentences among ``resolved``'s reasons, in reason order.

    ``clean`` is applied to each stripped sentence (the probes scrub paths).
    Empty sentences are never questions.
    """
    reasons = resolved.get("reasons") or []
    if links_questions(schema):
        linked: set[int] = set()
        for reference in resolved.get("questionRefs") or []:
            if isinstance(reference, Mapping):
                for index in reference.get("reasonIndices") or []:
                    if isinstance(index, int) and not isinstance(index, bool):
                        linked.add(index)
        chosen = [reason for index, reason in enumerate(reasons) if index in linked]
    else:
        chosen = [reason for reason in reasons
                  if isinstance(reason, Mapping) and "?" in str(reason.get("sentence") or "")]
    sentences = []
    for reason in chosen:
        if not isinstance(reason, Mapping):
            continue
        text = str(reason.get("sentence") or "").strip()
        if text:
            sentences.append(clean(text))
    return sentences
