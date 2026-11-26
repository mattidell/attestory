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

A link marks only the questions the projection can tie to one answer
target. Some reasons ask for an answer by design without a link: a roster
member's question (ADR 0087, beside ``memberLabel``), a question whose
answer target is not unique, and a question about a fact not yet recorded
(for example the per-statement Form 1099-B box 4 prompt). This rule does not
count them; a caller that needs them must read them separately.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from typing import Any

FIRST_LINKED_VERSION = 3


def links_questions(schema: Any) -> bool:
    """True when a model of this schema marks its questions by link (v3 onward)."""
    match = re.fullmatch(r"presentation-model\.v(\d+)", str(schema))
    return match is not None and int(match.group(1)) >= FIRST_LINKED_VERSION


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
