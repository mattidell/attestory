"""Classify every saved replay result against the actual recorded statements.

Run: python3 <this-file> <part-file> [--out classification-output.json]
No live runs. The replay part is retained outside the repository.
"""
from __future__ import annotations
import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
sys.path.insert(0,str(REPO))
from tools.recorded_replay import recorded_lists
P='tax.us.2025.'
AMOUNT=P+'f1099b.statement-box4-withholding'
REPORTED=P+'f1099b.statement-box4-withholding-reported'

def answers(acts):
    reported,amount={},{}
    for a in acts:
        payload=a.get('payload') or {}
        finding=payload.get('finding') or (payload.get('member') or {}).get('finding') or {}
        fact=finding.get('fact_id','')
        head=fact.split('|',1)[0]
        if head not in (AMOUNT,REPORTED):continue
        keys=dict(x.split('=',1) for x in fact.split('|',1)[1].split(',') if '=' in x)
        if 'statement' in keys:
            (amount if head==AMOUNT else reported)[keys['statement']]=finding.get('value')
    return {'reported':reported,'amount':amount,
            'no_without_amount':sorted(s for s,v in reported.items() if v=='no' and s not in amount)}

PAYMENT_ROWS = frozenset('form1040-line' + n for n in ('25b', '25d', '33', '34', '35a', '37'))
PAYMENT_FIELDS = frozenset(n.replace('form1040-line', 'form1040.line-') for n in PAYMENT_ROWS)
OLD_MISSING = 'f1099b.statement-box4-withholding'
NEW_MISSING = 'f1099b.no-sale-box4-present'


def question_words():
    content = REPO / 'packages/content/tax/2025'
    return tuple(json.loads((content / name).read_text())['question'] for name in (
        'input-question.f1099b-box4.v1.json',
        'input-question.f1099b-box4.v2.json',
        'input-question.f1099b-no-sale-box4-present.v1.json'))


def exact(a, b):
    """JSON equality also distinguishes booleans from numeric amounts."""
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def classify_pair(a, b, facts, allow_amount_wording=False):
    """Only enumerated row/missing and complete sentence substitutions pass.

    A recorded no is contextual support, never permission for an arbitrary diff.
    All other pin fields, including errors and line values, must match exactly.
    """
    old_question, new_question, return_question = question_words()
    ar, br = a.get('rows', {}), b.get('rows', {})
    if ar.keys() != br.keys():
        return 'unexpected'
    routed = set()
    for name in ar:
        if exact(ar[name], br[name]):
            continue
        before, after = ar[name], br[name]
        if (name not in PAYMENT_ROWS or not facts['no_without_amount']
                or before != ['blocked', 'DEPENDENCY_ABSENT', [OLD_MISSING]]
                or after != ['blocked', 'DEPENDENCY_ABSENT', [NEW_MISSING]]):
            return 'unexpected'
        routed.add(name)
    expected = json.loads(json.dumps(a))
    for name in routed:
        expected['rows'][name] = br[name]

    # Routing changes the explanatory sentence on 25b and its dependants.
    # Wording changes may occur on any explanation, but only as a whole sentence.
    def sentences(value, route=False):
        if not isinstance(value, list):
            return value
        replaced = [return_question if route and text == old_question else
                new_question if allow_amount_wording and text == old_question else text
                for text in value]
        # The saved presentation sentence collections are alphabetically sorted.
        return sorted(replaced) if replaced != value else value

    route = 'form1040-line25b' in routed
    if 'questions' in expected:
        expected['questions'] = sentences(expected['questions'], route)
    for field in ('reasons', 'blocked_reasons'):
        if field in expected:
            expected[field] = {name: sentences(text, route and name in PAYMENT_FIELDS)
                               for name, text in expected[field].items()}
    if not exact(expected, b):
        return 'unexpected'
    if exact(a, b):
        return 'same_error' if a.get('error') else 'identical_success'
    if routed:
        return 'no_without_amount_changed'
    return 'amount_sentence_only'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('part',type=Path)
    parser.add_argument('--out',default='classification-output.json')
    parser.add_argument('--allow-amount-wording',action='store_true')
    args=parser.parse_args()
    part=json.loads(args.part.read_text())
    results=part['results']
    lists=recorded_lists()
    assert set(results)=={k for k,_ in lists}
    _, new_question, _ = question_words()
    rows={}
    for key,acts in lists:
        result=results[key]
        a,b=result['pins']['v93'],result['pins']['v94']
        facts=answers(acts)
        label=classify_pair(a,b,facts,args.allow_amount_wording)
        rows[key]={'classification':label, 'tool_class':result['class'],
                   'no_without_amount':facts['no_without_amount'],
                   'line_changes':[n for n in set(a.get('lines',{}))|set(b.get('lines',{}))
                                   if a.get('lines',{}).get(n)!=b.get('lines',{}).get(n)]}
        rows[key]['sentence_fields']=[f for f in ('questions','reasons','blocked_reasons') if a.get(f)!=b.get(f)]
        rows[key]['row_changes']={name:{'v93':a.get('rows',{}).get(name),'v94':b.get('rows',{}).get(name)}
            for name in set(a.get('rows',{}))|set(b.get('rows',{}))
            if name not in a.get('rows',{}) or name not in b.get('rows',{})
            or not exact(a['rows'][name],b['rows'][name])}
        rows[key]['nonpayment_changes']=[f for f in ('base','attachments','presentation_valid') if a.get(f)!=b.get(f)]
        if a!=b:
            rows[key]['reported']=facts['reported']
            rows[key]['amount']=facts['amount']
    output={'lists':len(rows), 'counts':dict(Counter(r['classification'] for r in rows.values())),
            'tool_counts':dict(Counter(r['tool_class'] for r in rows.values())),
            'lists_with_no_without_amount':sum(bool(r['no_without_amount']) for r in rows.values()),
            'line_value_changes':sum(bool(r['line_changes']) for r in rows.values()),
            'nonpayment_changes':sum(bool(r['nonpayment_changes']) for r in rows.values()),
            'row_disposition_or_code_changes':sum(any(
                not isinstance(v['v93'],list) or not isinstance(v['v94'],list)
                or not exact(v['v93'][:2],v['v94'][:2])
                for v in r['row_changes'].values()) for r in rows.values()),
            'added_rows':sum(v['v93'] is None for r in rows.values() for v in r['row_changes'].values()),
            'removed_rows':sum(v['v94'] is None for r in rows.values() for v in r['row_changes'].values()),
            'changed_row_names':dict(Counter(name for r in rows.values() for name in r['row_changes'])),
            'results':rows}
    if args.allow_amount_wording:
        output['p0_equivalent_counts']={'identical_success':output['counts'].get('identical_success',0)+output['counts'].get('amount_sentence_only',0),
            'same_error':output['counts'].get('same_error',0),'no_without_amount_changed':output['counts'].get('no_without_amount_changed',0)}
        output['question_words']=new_question
    spec=importlib.util.spec_from_file_location('b4n_classification_writer',HERE/'probe.py')
    m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
    m.write(HERE/args.out,output)
    print(json.dumps({k:v for k,v in output.items() if k!='results'},indent=2),flush=True)

if __name__=='__main__':main()
