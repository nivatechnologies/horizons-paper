"""Checksum retained artifacts; scientific records are never overwritten."""
import argparse
import hashlib
import importlib.metadata
import json
import platform
import sys
from common import ROOT,write_json,sha

def main(system):
    root=ROOT/'runs'/system;records=[]
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.name=='artifact_manifest.json' or path.suffix=='.tmp':continue
        digest=hashlib.sha256()
        with path.open('rb') as file:
            while chunk:=file.read(8*1024*1024):digest.update(chunk)
        records.append(dict(path=str(path.relative_to(ROOT)),bytes=path.stat().st_size,sha256=digest.hexdigest()))
    versions={}
    for package in ['numpy','scipy','numba','torch']:
        try:versions[package]=importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:versions[package]=None
    write_json(root/'artifact_manifest.json',dict(system=system,files=records,git_sha=sha(),
               manifest_interpreter=sys.executable,python=platform.python_version(),packages=versions,
               note='Packages describe manifest interpreter; numerical launches retain their own interpreter/source records.'))
    print('Manifest',system,len(records),'files',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('system',choices=['l96','kolmo']);main(p.parse_args().system)
