"""Regenerate receipt registry exactly and check every visible numeric literal."""
import argparse,json,re,sys
from decimal import Decimal,InvalidOperation,ROUND_HALF_EVEN,localcontext
from pathlib import Path
from acd_numbers import ROOT,build,render
def tokens(text):
    # Digests have at least two hex letters; pure decimal/scientific literals survive.
    text=re.sub(r'(?<![\w.])(?=[0-9a-f]{7,64}(?![\w.]))(?=(?:[0-9]*[a-f]){2})[0-9a-f]{7,64}(?![\w.])',lambda m:' '*len(m[0]),text)
    # Markdown link destinations are provenance, not visible prose.
    text=re.sub(r'\]\([^)]*\)',lambda m:' '*len(m[0]),text)
    pattern=r'(?<![\d.])(?:(?<!\w)[-+−])?(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+-]?\d+)?(?:[kK])?%?(?!\d|\.\d)'
    for m in re.finditer(pattern,text):
        yield text.count('\n',0,m.start())+1,m[0]
def match(raw,rows):
    percent=raw.endswith('%');x=raw.rstrip('%').replace('−','-');k=x.lower().endswith('k')
    if k:x=x[:-1]
    target=Decimal(x);quantum=Decimal(1).scaleb(target.as_tuple().exponent);matches=[]
    with localcontext() as ctx:
        ctx.prec=100
        for key,row in rows.items():
            v_float=row['value']*(100 if percent else 1)/(1000 if k else 1)
            v=Decimal(str(v_float))
            try:okay=v.quantize(quantum,rounding=ROUND_HALF_EVEN)==target
            except InvalidOperation:okay=False
            if okay:matches.append(key)
    return matches
def run():
    p=argparse.ArgumentParser();p.add_argument('--text',type=Path);a=p.parse_args();expected=build();errors=[]
    primary=json.loads((ROOT/'numbers_acd.json').read_text())
    loaded=dict(primary);loaded['numbers']=dict(primary['numbers'])
    shards=loaded.pop('additional_registries',[])
    for name in shards:
        supplemental=json.loads((ROOT/name).read_text())
        if set(loaded['numbers'])&set(supplemental['numbers']):errors.append('Duplicate supplemental registry keys')
        loaded['numbers'].update(supplemental['numbers'])
        markdown=ROOT/('NUMBERS_ACD_'+name.removeprefix('numbers_acd_').removesuffix('.json').upper()+'.md')
        if not markdown.exists() or markdown.read_text()!=render(supplemental):errors.append('Supplemental registry Markdown differs')
    if loaded!=expected:errors.append('Receipt registries differ from regenerated receipts')
    if not (ROOT/'NUMBERS_ACD.md').exists() or (ROOT/'NUMBERS_ACD.md').read_text()!=render(primary):errors.append('NUMBERS_ACD.md differs from regenerated receipts')
    if a.text:
        n=0
        for line,raw in tokens(a.text.read_text()):
            n+=1;keys=match(raw,expected['numbers'])
            if not keys:errors.append(f'UNMATCHED line {line}: {raw}')
            else:print(f'MATCH line {line}: {raw} -> '+', '.join(keys[:6])+(' (more candidates; semantic audit required)' if len(keys)>6 else ''))
        print('Extracted',n,'numbers; matches check rounding only, never claim licensing.')
    for e in errors:print(e)
    print('PASS' if not errors else 'FAIL')
    return bool(errors)
if __name__=='__main__':sys.exit(run())
