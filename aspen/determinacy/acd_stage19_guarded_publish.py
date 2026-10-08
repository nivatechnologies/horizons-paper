"""Publish an isolated completed step, preserving every prior registry value."""
import fcntl,json,os,shutil,subprocess,time
from pathlib import Path
BRANCH='paper/aspen-2026-10-determinacy';PY='/mnt/niva-array/work/aspen-stage19-env-20261007/bin/python'
BASE=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007')
def network(args,cwd=None):
 while True:
  p=subprocess.run(list(map(str,args)),cwd=cwd)
  if not p.returncode:return
  time.sleep(60)
def checked(args,cwd=None):return subprocess.check_output(list(map(str,args)),cwd=cwd,text=True).strip()
def registry_values(root):
 d=json.loads((root/'numbers_acd.json').read_text());v=dict(d['numbers'])
 for n in d.get('additional_registries',[]):v.update(json.loads((root/n).read_text())['numbers'])
 return {k:r['value'] for k,r in v.items()}
def configure_registry(root,receipts):
 p=root/'acd_numbers.py';s=p.read_text()
 for filename,prefix in receipts:
  line=f"    stage13_receipts.append(('{filename}', '{prefix}'))\n"
  if line not in s:s=s.replace('    for filename,prefix in stage13_receipts:',line+'    for filename,prefix in stage13_receipts:')
  # Insert an exact per-receipt omitted-field branch without changing old keys.
  if "if filename=="+repr(filename) not in s:
   s=s.replace('                 omit=',"                 omit=('source_hashes','code_hashes','first_panel','records','case_records','case_differences','case_mean_differences','defined_seeds_per_instance','case_indices','output_hashes','executions') if filename=="+repr(filename)+" else ")
 groups={'stage21':('ACD_21',),'continuation':('ACD_FRESH_19_L3',),'stage19_part3b':('ACD_FRESH_19_3B',),'stage20_followup':('ACD_POSTHOC_20C','ACD_POSTHOC_20B_UNIFORM'),'stage18_followup':('ACD_POSTHOC_18D','ACD_POSTHOC_18C')}
 start=s.index('def write():');end=s.index("if __name__=='__main__':write()",start)
 writer="def write():\n    d=build()\n    groups="+repr(groups)+"\n    supplemental={}\n    selected=set()\n    for name,prefixes in groups.items():\n        values={k:v for k,v in d['numbers'].items() if k.startswith(prefixes)}\n        if values:\n            supplemental[name]=dict(schema=d['schema'],source_hashes={},numbers=values);selected.update(values)\n    core={k:v for k,v in d['numbers'].items() if k not in selected}\n    primary=dict(d,numbers=core,additional_registries=['numbers_acd_'+n+'.json' for n in supplemental])\n    (ROOT/'numbers_acd.json').write_text(json.dumps(primary,separators=(',',':'),allow_nan=False)+'\\n')\n    (ROOT/'NUMBERS_ACD.md').write_text(render(primary))\n    for name,values in supplemental.items():\n        (ROOT/('numbers_acd_'+name+'.json')).write_text(json.dumps(values,separators=(',',':'),allow_nan=False)+'\\n')\n        (ROOT/('NUMBERS_ACD_'+name.upper()+'.md')).write_text(render(values))\n    print('NUMBERS',len(d['numbers']))\n"
 s=s[:start]+writer+s[end:];p.write_text(s)
 p=root/'check_acd.py';p.write_text(p.read_text().replace("markdown=ROOT/'NUMBERS_ACD_STAGE21.md'","markdown=ROOT/('NUMBERS_ACD_'+name.removeprefix('numbers_acd_').removesuffix('.json').upper()+'.md')"))
def publish(source,step,files,receipts=(),section=None,marker=None):
 source=Path(source);marker=Path(marker) if marker else None
 if marker and marker.exists():return json.loads(marker.read_text())
 with open('/tmp/acd_publication.lock','w') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  network(['git','-C',BASE,'fetch','origin',BRANCH])
  repo=Path('/mnt/niva-array/work/aspen-publication-'+step);branch='publish-'+step
  if not repo.exists():checked(['git','-C',BASE,'worktree','add','-b',branch,repo,'origin/'+BRANCH])
  subprocess.run(['git','rebase','--abort'],cwd=repo,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  checked(['git','reset','--hard','origin/'+BRANCH],repo)
  root=repo/'aspen/determinacy';before=registry_values(root)
  for name in files:
   target=root/name;target.parent.mkdir(parents=True,exist_ok=True)
   if section and name==section[0]:
    body=(source/name).read_text();heading=section[1];assert heading in body
    body=body[body.index(heading):];old=target.read_text()
    if heading in old:old=old[:old.index(heading)]
    target.write_text(old.rstrip()+'\n'+body)
   else:shutil.copy2(source/name,target)
  configure_registry(root,receipts)
  subprocess.run([PY,root/'acd_numbers.py'],cwd=root,check=True)
  after=registry_values(root);assert all(k in after and after[k]==v for k,v in before.items())
  subprocess.run([PY,root/'check_acd.py'],cwd=root,check=True)
  d=json.loads((root/'numbers_acd.json').read_text());registry=['acd_numbers.py','check_acd.py','numbers_acd.json','NUMBERS_ACD.md']
  for n in d.get('additional_registries',[]):registry.extend([n,'NUMBERS_ACD_'+n.removeprefix('numbers_acd_').removesuffix('.json').upper()+'.md'])
  checked(['git','add','-f',*[str(root/f) for f in list(files)+registry]],repo)
  if checked(['git','diff','--cached','--name-only'],repo):checked(['git','commit','-m','Report '+step+' with complete receipt registry'],repo)
  while True:
   network(['git','fetch','origin',BRANCH],repo)
   if subprocess.run(['git','rebase','FETCH_HEAD'],cwd=repo).returncode:
    subprocess.run(['git','rebase','--abort'],cwd=repo,check=True)
    raise RuntimeError('Remote moved with overlapping generated files; retry rebuilds from remote without changing prior values')
   subprocess.run([PY,root/'check_acd.py'],cwd=root,check=True)
   if subprocess.run(['git','push','origin','HEAD:'+BRANCH],cwd=repo).returncode==0:break
   time.sleep(60)
  sha=checked(['git','rev-parse','HEAD'],repo)
  p=root/'ACD_PIPELINE_STATUS.md';p.write_text(p.read_text()+f'\nPipeline | {step} | {sha} | {time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())} | Completed, registry PASS, every prior value unchanged; downstream controllers continue.\n')
  checked(['git','add',p],repo);checked(['git','commit','-m','Record '+step+' continuation'],repo)
  while True:
   network(['git','fetch','origin',BRANCH],repo)
   checked(['git','rebase','FETCH_HEAD'],repo)
   subprocess.run([PY,root/'check_acd.py'],cwd=root,check=True)
   if subprocess.run(['git','push','origin','HEAD:'+BRANCH],cwd=repo).returncode==0:break
   time.sleep(60)
  result=dict(commit=sha,registry_before=len(before),registry_after=len(after),utc=time.time())
  if marker:marker.parent.mkdir(parents=True,exist_ok=True);marker.write_text(json.dumps(result,indent=2)+'\n')
  print('PUBLISHED',step,result,flush=True);return result
