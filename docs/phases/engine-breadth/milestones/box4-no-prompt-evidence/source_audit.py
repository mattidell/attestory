"""Check the local 2025 IRS sources; commit identities and assessments only.

Run: python3 <this-file> <1040-instructions.pdf> <1099b-instructions.pdf> <1099b-form.pdf>
No new filer-facing sentences are proposed by this repair.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser()
    p.add_argument('sources',type=Path,nargs=3)
    args=p.parse_args()
    specs=[('2025 Instructions for Form 1040','Line 25b—Form(s) 1099',
            'include the amount withheld',
            'Line 25b includes the withholding shown on Forms 1099. A truthful no to the statement question supplies no box 4 withholding to carry from that statement.'),
           ('2025 Instructions for Form 1099-B','Box 4. Federal Income Tax Withheld',
            'Enter backup withholding',
            'Box 4 is the reported federal withholding amount. No is statement-local, not a declaration about all withholding or all statements.'),
           ('2025 Form 1099-B, Copy B instructions for recipient','Box 4.',
            'Shows backup withholding',
            'The recipient instructions direct inclusion of this amount as tax withheld. An explicit positive amount beside no is contradictory; retaining the explicit amount preserves the existing recorded amount rather than claiming the pair is truthful.')]
    sources=[]
    for path,(title,heading,quote,assessment) in zip(args.sources,specs):
        assert path.read_bytes().startswith(b'%PDF-'), 'source is not a PDF'
        text=subprocess.check_output(['pdftotext','-layout',str(path),'-'],text=True)
        normalized=' '.join(text.split())
        assert quote in normalized
        pages=[i+1 for i,t in enumerate(text.split('\f')) if heading in ' '.join(t.split())]
        sources.append({'title':title,'local_filename':path.name,'pdf_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                        'text_sha256':hashlib.sha256(text.encode()).hexdigest(), 'pdf_pages':pages,
                        'heading':heading,'short_quote':quote,'assessment':assessment})
    result={'sources':sources,'new_filer_sentences':[],
            'published_questions':'Both the yes/no question and amount prompt remain byte-for-byte unchanged.',
            'inference_limit':'No is zero withholding to carry from the identified statement as reported. It does not resolve an incorrect information return or other statements.'}
    (HERE/'law.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
