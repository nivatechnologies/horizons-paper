"""Extract numeric paper prose, keeping original TeX line numbers and structural inventory."""
import re,json,hashlib,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def detex(line):
    line=re.split(r'(?<!\\)%',line,maxsplit=1)[0]
    # Scientific notation is a single literal at its stated mantissa precision.
    line=re.sub(r'(?P<m>\d+(?:\.\d+)?)\s*\\times\s*10\s*\^\s*\{(?P<e>-?\d+)\}',lambda m:m['m']+'e'+m['e'],line)
    line=re.sub(r'(?<![\w.])10\s*\^\s*\{(?P<e>-?\d+)\}',lambda m:'1e'+m['e'],line)
    # Visible thousands separators, not independent numeric claims.
    line=re.sub(r'\d{1,3}(?:,\d{3})+(?!\d)',lambda m:m[0].replace(',',''),line)
    line=line.replace(r'\%','%')
    line=re.sub(r'\\(?:cite[tp]|ref|label|includegraphics|bibliography|bibliographystyle)(?:\[[^\]]*\])?\{[^}]*\}','',line)
    line=re.sub(r'\\(?:begin|end)\{[^}]*\}(?:\[[^\]]*\])?','',line)
    line=re.sub(r'\\multicolumn\{\d+\}\{[^}]*\}','',line)
    line=re.sub(r'\\[A-Za-z]+(?:\*)?',lambda m:' LT ' if m[0]==r'\LT' else ' Jbar ' if m[0]==r'\Jbar' else ' ',line)
    line=re.sub(r'\\[^A-Za-z]',' ',line)
    line=line.replace('--','–').replace('~',' ').replace('$','').replace('{','').replace('}','')
    return re.sub(r'[ \t]+',' ',line).strip()
def run():
    source=ROOT/'paper/main.tex'
    original=source.read_text().splitlines()
    visible=[]
    for i,line in enumerate(original,1):
        visible.append(detex(line) if i>=26 else '')
    output=ROOT/'paper/main.detex.txt';output.write_text('\n'.join(visible).rstrip()+'\n')
    from check_acd import tokens,match
    numbers=json.loads((ROOT/'numbers_acd.json').read_text())['numbers']
    structural=[];unmatched=[]
    for line,raw in tokens(output.read_text()):
        if (line==63 and raw=='38') or (line==66 and raw=='28') or (line==75 and raw=='512'):
            structural.append(dict(line=line,token=raw,reason='Declared structural question/pair count or thin-draw count; explicitly exempted by Todd'))
        if not match(raw,numbers):unmatched.append(dict(line=line,token=raw,structural=any(r['line']==line and r['token']==raw for r in structural)))
    # Keep raw check output, including exempt unmatched literals; do not silently register exceptions.
    p=subprocess.run([sys.executable,str(ROOT/'check_acd.py'),'--text',str(output)],capture_output=True,text=True)
    (ROOT/'receipts/acd_stage5b_paper_check.txt').write_text(p.stdout+p.stderr)
    bibliography=[]
    for i,line in enumerate((ROOT/'paper/refs.bib').read_text().splitlines(),1):
        m=re.match(r'\s*(year|volume|number|pages|eprint|doi|version|booktitle)\s*=\s*\{(.*)\}',line)
        if m: bibliography.append(dict(line=i,field=m[1],value=m[2],numeric_literals=re.findall(r'\d+(?:\.\d+)?',m[2]),category='bibliographic year/volume/page/identifier metadata; no empirical receipt'))
    structural+= [dict(line=i,token=None,reason='Section/equation/table reference label; resolved numbers belong to document structure') for i,line in enumerate(original,1) if re.search(r'\\(?:ref|label)\{',line)]
    manifest=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),detex_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),line_numbers='same as original main.tex',raw_checker_exit=p.returncode,unmatched=unmatched,empirical_unmatched=[r for r in unmatched if not r['structural']],structural_constants=structural,bibliographic_numbers=bibliography,scope='Numeric matching checks stated rounding only; independent audit supplies semantic provenance. No TeX build.')
    (ROOT/'receipts/acd_stage5b_numeric_check.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('RAW EXIT',p.returncode,'UNMATCHED',json.dumps(unmatched),'STRUCTURAL explicit',len(structural),'BIB FIELDS',len(bibliography))
    return bool(manifest['empirical_unmatched'])
if __name__=='__main__':sys.exit(run())
