"""Budget-only adapter: preserve the frozen trainer except the authorized cap."""
from acd_stage23_common import *
import argparse,inspect
import acd_stage23_train as original

def run(args):
 cfg=ready();amend=json.loads((ROOT/'receipts/acd_stage23_cap_amendment.json').read_text())
 assert (OUT/'cap_amendment_pushed.json').exists()
 assert args.name==amend['model'] and args.response_weight==amend['weight']
 source=inspect.getsource(original.run)
 assert source.count('cap=36000-prior_charge')==1 and source.count('cap_seconds=36000')==1
 source=source.replace('cap=36000-prior_charge','cap=authorized_cap-prior_charge').replace('cap_seconds=36000','cap_seconds=authorized_cap')
 namespace=dict(original.__dict__,authorized_cap=amend['new_cap_seconds']);exec(compile(source,__file__,'exec'),namespace)
 namespace['run'](args.name,args.data,args.out,args.micro,args.torch_seed,args.batch_seed,args.response_weight)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--micro',type=int,default=128);p.add_argument('--torch-seed',type=int,required=True);p.add_argument('--batch-seed',type=int,required=True);p.add_argument('--response-weight',type=float,required=True);run(p.parse_args())
