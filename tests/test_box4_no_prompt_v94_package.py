"""Fast publication checks against accepted P0 bytes and the prior publication."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, cast

from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.tax.loader import covered_flag_refusal_map, domain_package_companion_declarations, selection_collect_satisfied_by_family

REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / 'packages/content/tax/2025'
EVIDENCE = REPO / 'docs/phases/engine-breadth/milestones/box4-no-prompt-evidence'
RELEASES = REPO / 'packages/sample_data/student_loan_worksheet_integration/publication_surface/releases'
CORE = 'tax.us.2025.package.core-calculations'
STEM = 'demo.release.sli-worksheet-integration.2025'
QUESTION = 'Enter the federal income tax withheld in box 4 of each Form 1099-B or substitute statement you recorded a sale from, except a statement you said shows no federal income tax withheld in box 4 or whose amount you already entered. If box 4 is blank, enter $0.'


def _read(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text()))


def _index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    result = {(r['id'], r['version']): r for r in rows}
    assert len(result) == len(rows)
    return result


def _prototype_members() -> list[dict[str, Any]]:
    return cast(list[dict[str, Any]], _read(EVIDENCE / 'prototype-build.json')['artifacts'])


def test_nineteen_content_files_are_byte_identical_to_accepted_p0() -> None:
    # Track 0 froze actual scratch bytes independently of the production copy.
    expected = _read(EVIDENCE / 'track0-replay.json')['p0_content_hashes']
    members = _prototype_members()
    assert len(expected) == len(members) == 19
    assert set(expected) == {r['filename'] for r in members}
    for row in members:
        path = CONTENT / row['filename']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected[row['filename']]
        body = _read(path)
        for key in ('id', 'version', 'schema'):
            assert body[key] == row[key]


def test_question_v2_is_exact_decision_7_with_the_same_answer_shape() -> None:
    before = _read(CONTENT / 'input-question.f1099b-box4.v1.json')
    after = _read(CONTENT / 'input-question.f1099b-box4.v2.json')
    assert after == {**before, 'version': 'v2', 'question': QUESTION}
    assert after['fact_type'] == {'id': 'tax.us.2025.f1099b.statement-box4-withholding', 'version': 'v1'}


def test_core_adopts_exactly_the_prototype_and_question_successor() -> None:
    before = _read(CONTENT / 'package.core-calculations.v93.json')
    after = _read(CONTENT / 'package.core-calculations.v94.json')
    expected = {key: dict(row) for key, row in _index(before['members']).items()}
    for row in _prototype_members():
        if row['id'] == 'tax.us.2025.rule.form1040-line25b':
            del expected[(row['id'], 'v8')]
        expected[(row['id'], row['version'])] = {k: row[k] for k in ('id', 'version', 'schema', 'role')}
    question_id = 'tax.us.2025.input-question.f1099b-box4'
    old_question = expected.pop((question_id, 'v1'))
    expected[(question_id, 'v2')] = {**old_question, 'version': 'v2'}
    assert _index(after['members']) == expected
    entries = _index(before['entrypoints'])
    entries.pop((question_id, 'v1'))
    entries[(question_id, 'v2')] = {'id': question_id, 'version': 'v2'}
    bundle_id = 'tax.us.2025.f1099b.box4-amount-requirement.vocabulary'
    assert (bundle_id, 'v1') not in entries
    entries[(bundle_id, 'v1')] = {'id': bundle_id, 'version': 'v1'}
    assert _index(after['entrypoints']) == entries
    skip = {'version', 'members', 'entrypoints', 'package_checksum'}
    assert {k: v for k, v in after.items() if k not in skip} == {k: v for k, v in before.items() if k not in skip}
    assert after['version'] == 'v94'
    assert after['package_checksum'] == package_instance_checksum(after)


def test_registry_v92_is_add_only_with_exactly_twenty_new_citizens() -> None:
    before = _read(CONTENT / 'published-packages.v91.json')
    after = _read(CONTENT / 'published-packages.v92.json')
    bodies = [_read(CONTENT / row['filename']) for row in _prototype_members()]
    bodies.append(_read(CONTENT / 'input-question.f1099b-box4.v2.json'))
    assert len(bodies) == 20
    for kind in ('citizens', 'packages'):
        old, new = _index(before[kind]), _index(after[kind])
        assert all(new[key] == row for key, row in old.items())
        added = {k: v for k, v in new.items() if k not in old}
        if kind == 'citizens':
            assert added == {(b['id'], b['version']): {'id': b['id'], 'version': b['version'], 'checksum': citizen_checksum(b)} for b in bodies}
        else:
            package = _read(CONTENT / 'package.core-calculations.v94.json')
            assert added == {(CORE, 'v94'): {'id': CORE, 'version': 'v94', 'checksum': package['package_checksum']}}


def test_release_integrity_and_v94_loader_declarations_carry_v93() -> None:
    before = _read(RELEASES / f'{STEM}.v91.json')
    after = _read(RELEASES / f'{STEM}.v92.json')
    assert after == {**before, 'version': 'v92', 'package_registry_sha256': hashlib.sha256((CONTENT / 'published-packages.v92.json').read_bytes()).hexdigest()}
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, 'v94')] == declarations[(CORE, 'v93')]
    assert covered_flag_refusal_map(CORE, 'v94') == covered_flag_refusal_map(CORE, 'v93')
    assert covered_flag_refusal_map(CORE, 'v94')
    assert selection_collect_satisfied_by_family(CORE, 'v94') is True


def test_v93_and_earlier_publication_bytes_are_unchanged() -> None:
    expected = cast(dict[str, str], _read(EVIDENCE / 'track1-historical-hashes.json')['files'])
    assert len(expected) == 96
    for relative, sha in expected.items():
        assert hashlib.sha256((REPO / relative).read_bytes()).hexdigest() == sha, relative


def test_subject_dispatch_requirements_have_narrow_allowlist_reasons() -> None:
    entries = _read(REPO / 'tools/required_versus_read_allowlist.json')['entries']
    checked = 0
    for row in _prototype_members():
        body = _read(CONTENT / row['filename'])
        if row['role'] != 'computation' or 'subject' not in body:
            continue
        subject = body['subject']['id']
        assert subject in body['requires']
        matches = [e for e in entries if (e['rule_id'], e['version'], e['symbol']) == (body['id'], body['version'], subject)]
        assert len(matches) == 1
        assert 'per-subject dispatch' in matches[0]['reason']
        checked += 1
    assert checked == 16
