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
    old_question=json.loads((REPO/'packages/content/tax/2025/input-question.f1099b-box4.v1.json').read_text())['question']
    new_question=json.loads((REPO/'packages/content/tax/2025/input-question.f1099b-box4.v2.json').read_text())['question'] if args.allow_amount_wording else old_question
    def normalize(value):
        if isinstance(value,str):return value.replace(old_question,new_question)
        if isinstance(value,list):return [normalize(v) for v in value]
        if isinstance(value,dict):return {k:normalize(v) for k,v in value.items()}
        return value
    rows={}
    for key,acts in lists:
        result=results[key]
        a,b=result['pins']['v93'],result['pins']['v94']
        facts=answers(acts)
        if a==b:
            label='same_error' if a.get('error') else 'identical_success'
        elif args.allow_amount_wording and normalize(a)==b:
            label='amount_sentence_only'
        else:
            copy_a=json.loads(json.dumps(a))
            copy_b=json.loads(json.dumps(b))
            copy_a.get('rows',{}).pop('form1040-line25b',None)
            copy_b.get('rows',{}).pop('form1040-line25b',None)
            if copy_a==copy_b:
                label='line25b_dependency_route_only'
            elif facts['no_without_amount']:
                label='no_without_amount_changed'
            else:
                label='unexpected_change'
        rows[key]={'classification':label, 'tool_class':result['class'],
                   'no_without_amount':facts['no_without_amount'],
                   'line_changes':[n for n in set(a.get('lines',{}))|set(b.get('lines',{}))
                                   if a.get('lines',{}).get(n)!=b.get('lines',{}).get(n)]}
        rows[key]['sentence_fields']=[f for f in ('questions','reasons','blocked_reasons') if a.get(f)!=b.get(f)]
        rows[key]['row_changes']={name:{'v93':a.get('rows',{}).get(name),'v94':b.get('rows',{}).get(name)}
            for name in set(a.get('rows',{}))|set(b.get('rows',{}))
            if a.get('rows',{}).get(name)!=b.get('rows',{}).get(name)}
        rows[key]['nonpayment_changes']=[f for f in ('base','attachments','presentation_valid') if a.get(f)!=b.get(f)]
        if a!=b:
            rows[key]['reported']=facts['reported']
            rows[key]['amount']=facts['amount']
    output={'lists':len(rows), 'counts':dict(Counter(r['classification'] for r in rows.values())),
            'tool_counts':dict(Counter(r['tool_class'] for r in rows.values())),
            'lists_with_no_without_amount':sum(bool(r['no_without_amount']) for r in rows.values()),
            'line_value_changes':sum(bool(r['line_changes']) for r in rows.values()),
            'nonpayment_changes':sum(bool(r['nonpayment_changes']) for r in rows.values()),
            'row_disposition_or_code_changes':sum(any(v['v93'][:2]!=v['v94'][:2] for v in r['row_changes'].values()
                 if isinstance(v['v93'],list) and isinstance(v['v94'],list)) for r in rows.values()),
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
