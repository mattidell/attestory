"""Eight distinct lists, once each on published v94, through the saved page.

Real coordinate runs plus projection exceed the 3 s lane: the same entry
path's Track 0 lifecycle shard measured 45.337 s for five live calls.
The module is explicitly live: the v94 targeted run measured 6.59-21.13 s
per case. Its per-case durations are recorded in the evidence report.
Evidence code loads only through evidence_loader, with bare sibling names
bound by path before any parent harness runs.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_session import _render_page
from tests import evidence_loader

pytestmark = pytest.mark.live
REPO = Path(__file__).resolve().parents[1]
MILESTONES = REPO / 'docs/phases/engine-breadth/milestones'
EVIDENCE = MILESTONES / 'box4-no-prompt-evidence'
CONTENT = REPO / 'packages/content/tax/2025'
P = 'tax.us.2025.'
AMOUNT = P + 'f1099b.statement-box4-withholding'
REPORTED = P + 'f1099b.statement-box4-withholding-reported'
PRESENT = P + 'f1099b.no-sale-box4-present'
QUESTION = 'Enter the federal income tax withheld in box 4 of each Form 1099-B or substitute statement you recorded a sale from, except a statement you said shows no federal income tax withheld in box 4 or whose amount you already entered. If box 4 is blank, enter $0.'
CASES = ('one-no', 'yes-no-amount', 'mixed-no-unanswered', 'two-sales-one-no', 'no-with-200', 'second-subject-no', 'no-return-unanswered', 'no-1099b')
Acts = list[dict[str, Any]]


def _harness() -> Any:
    # The inherited line-12d harness has bare imports. Never let an unrelated
    # evidence directory on PYTHONPATH supply its probe or prototype.
    line12d = MILESTONES / 'line12d-boxes-evidence'
    evidence_loader.load(line12d / 'prototype.py', 'prototype')
    evidence_loader.load(line12d / 'probe.py', 'probe')
    return evidence_loader.load(MILESTONES / 'sale-family-audit-evidence/audit_harness.py', 'b4n_v94_harness')


def _statement_answer(h: Any, acts: Acts, fact: str, value: object, tag: str) -> None:
    if fact not in h._adopted(acts):
        bundle = h.bundle_for(fact, h.CONTENT)
        assert bundle is not None
        h._add(acts, 'bundle-adoption', {'bundle': bundle})
    fact_id = h.fact_id_for(fact, (('statement', 'demo.sfa.b4nv94.s0.statement'), ('tax-year', h.YEAR)))
    h._add(acts, 'assertion', {'finding': h._attested('demo.b4nv94.' + tag, fact_id, value)})


def _fixture(case: str) -> Acts:
    h = _harness()
    acts: Acts = h.opened()
    kind, term = ('noncovered', 'lt') if case == 'second-subject-no' else ('covered', 'st')
    count = 0 if case == 'no-1099b' else 2 if case in {'two-sales-one-no', 'mixed-no-unanswered'} else 1
    for i in range(count):
        acts = h.sale(acts, kind, term, proceeds=5000, basis=4000, tag=f'b4nv94.s{i}')
    if case == 'two-sales-one-no':
        raw = json.dumps(acts)
        for key in ('broker', 'statement'):
            raw = raw.replace(f'demo.sfa.b4nv94.s1.{key}', f'demo.sfa.b4nv94.s0.{key}')
        seen: set[str] = set()
        kept: Acts = []
        for act in json.loads(raw):
            if act['kind'] == 'entity-introduced':
                ident = act['payload']['entity']['id']
                if ident in seen:
                    continue
                seen.add(ident)
            kept.append(act)
        acts = h.renumber(kept)
    answers = h.honest({kind} if count else set())
    answers.update(h.honest_exception1(acts))
    acts = h.answer(acts, **{k: v for k, v in answers.items() if v is not None})
    if count:
        _statement_answer(h, acts, P + 'f1099b.statement-box7-loss-not-allowed', 'no', 'box7.s0')
        _statement_answer(h, acts, REPORTED, 'yes' if case == 'yes-no-amount' else 'no', 'reported.s0')
        if case == 'mixed-no-unanswered':
            # Only box 7 is answered on the second statement. Box 4 remains
            # absent there, so the first statement's no must not satisfy it.
            fact = P + 'f1099b.statement-box7-loss-not-allowed'
            fid = h.fact_id_for(fact, (('statement', 'demo.sfa.b4nv94.s1.statement'), ('tax-year', h.YEAR)))
            h._add(acts, 'assertion', {'finding': h._attested('demo.b4nv94.box7.s1', fid, 'no')})
        if case == 'no-with-200':
            _statement_answer(h, acts, AMOUNT, 200, 'amount.s0')
    acts = h.say(acts, PRESENT, 'no', 'b4nv94.present')
    if case == 'no-return-unanswered':
        acts = h.strip(acts, PRESENT)
    # Match the completed single-filing Track 0 neighbour's scope answers.
    fact = P + 'standard-deduction.spouse-separate-condition'
    if fact not in h._adopted(acts):
        h._add(acts, 'bundle-adoption', {'bundle': json.loads((CONTENT / 'core_calculations.bundle.v4.json').read_text())})
    for slug, value in (('filing-status', 'single'), ('taxpayer-over-65', False), ('taxpayer-blind', False),
                        ('spouse-over-65', False), ('spouse-blind', False), ('mfs-lived-apart-all-year', 'yes'),
                        ('standard-deduction.spouse-separate-condition', True)):
        acts = h.say(acts, P + slug, value, 'b4nv94.' + slug)
    return cast(Acts, h.renumber(acts))


def _facts(acts: Acts, fact: str) -> list[dict[str, Any]]:
    return [f for a in acts if isinstance(f := a.get('payload', {}).get('finding'), dict)
            and str(f.get('fact_id', '')).startswith(fact + '|')]


def _field(model: dict[str, Any], line: str) -> dict[str, Any]:
    return next(cast(dict[str, Any], s) for s in model['sections'] if s['field']['id'] == P + 'form1040.line-' + line)


def _sentences(section: dict[str, Any]) -> list[str]:
    return [r['sentence'] for r in section['resolved'].get('reasons', [])]


def _states(model: dict[str, Any]) -> dict[str, Any]:
    return {s['field']['id']: {'disposition': s['resolved']['disposition'], 'value': s['resolved'].get('value'),
                               'sentences': _sentences(s)} for s in model['sections']}


def _run(acts: Acts, case: str, root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    h = _harness()
    core = h.Core('v94', 'v92', 'v92')
    assert core.loader_from is None
    finished = h._handover(h._finish(acts, package_path=core.package_path, package_version=core.version,
        release_path=core.release_path, release_version=core.release_version, note='demo.b4nv94.' + case),
        surface=core.surface(), reconfirm=True)
    assert _facts(acts, AMOUNT) == _facts(finished, AMOUNT)
    assert _facts(acts, REPORTED) == _facts(finished, REPORTED)
    assert _facts(acts, PRESENT) == _facts(finished, PRESENT)
    cap = h.WorkspaceCapability(root / 'L')
    outcome = live_coordinate_run(cap, repo_root=REPO, authoritative_acts=finished, workspace_revision=len(finished),
        run_scope={'jurisdiction': 'us', 'year': h.YEAR}, scope_user=h.ccr.USER,
        request={'schema': 'run-request.v1'}, run_id='demo.b4nv94.' + case, governance_pins=[],
        surface=core.surface(), output_name='out.json')
    assert outcome.refusal is None
    assert outcome.output_path is not None and outcome.presentation_path is not None
    report = cast(dict[str, Any], json.loads(outcome.output_path.read_text()))
    assert report['stop_reason'] == 'saturated'
    projected = cast(dict[str, Any], json.loads(outcome.presentation_path.read_text()))
    page = root / 'demo.b4nv94.page.html'
    page.write_bytes(_render_page(REPO, cap, outcome.presentation_path))
    text = page.read_text()
    marker = 'const MODEL = Object.freeze('
    saved, _ = json.JSONDecoder().raw_decode(text, text.index(marker) + len(marker))
    assert saved == projected
    return cast(dict[str, Any], saved), report


@pytest.mark.parametrize('case', CASES)
def test_box4_no_on_published_v94_once(case: str, tmp_path: Path) -> None:
    acts = _fixture(case)
    # Hand values: the wage fixture withholds 4500; no gives zero 1099
    # withholding; its one explicit box 4 amount gives 200, hence 4700 total.
    assert [f['value'] for f in _facts(acts, P + 'w2.box2-withholding')] == [4500]
    if case != 'no-with-200':
        assert _facts(acts, AMOUNT) == []
    model, report = _run(acts, case, tmp_path)
    line25b, line25d = _field(model, '25b'), _field(model, '25d')
    if case in {'yes-no-amount', 'mixed-no-unanswered', 'no-return-unanswered'}:
        wanted = (json.loads((CONTENT / 'input-question.f1099b-no-sale-box4-present.v1.json').read_text())['question']
                  if case == 'no-return-unanswered' else QUESTION)
        missing = PRESENT if case == 'no-return-unanswered' else AMOUNT
        row = next(r for r in report['dispositions'] if r['artifact_id'] == P + 'rule.form1040-line25b')
        assert row['disposition'] == 'blocked'
        assert row['code'] == 'DEPENDENCY_ABSENT'
        assert row['missing'] == [missing]
        for section in (line25b, line25d):
            assert section['resolved']['disposition'] == 'blocked'
            assert _sentences(section) == [wanted]
        if case == 'mixed-no-unanswered':
            assert [f['value'] for f in _facts(acts, REPORTED)] == ['no']
        if case == 'no-return-unanswered':
            assert _facts(acts, PRESENT) == []
    else:
        hand25b = 200 if case == 'no-with-200' else 0
        assert line25b['resolved']['value'] == hand25b
        assert line25d['resolved']['value'] == 4500 + hand25b
        assert line25b['resolved']['disposition'] != 'blocked'
        assert line25d['resolved']['disposition'] == 'published_value'
        assert _sentences(line25b) == _sentences(line25d) == []
    if case == 'no-1099b':
        old = json.loads((EVIDENCE / 'track0-matrix.json').read_text())
        before = next(r['baseline_fields'] for r in old['cases'] if r['id'] == 'neighbour.single.no-1099b')
        assert _states(model) == before
