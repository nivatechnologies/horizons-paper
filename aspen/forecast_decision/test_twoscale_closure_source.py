"""Source-only adversarial closure check. Never imports kernels or reads panel data."""
import ast,json
from pathlib import Path
source=Path(__file__).with_name('twoscale_campaign.py').read_text()
tree=ast.parse(source)
selected=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in {'require_twoscale_open','metadata','panel_directory2'}]
class GuardRoot:
    def __init__(self,kind):self.kind=kind;self.reads=[]
    def __truediv__(self,name):return GuardPath(self,name)
class GuardPath:
    def __init__(self,root,name):self.root=root;self.name=name
    def exists(self):
        if self.name=='runs/closure/control.json':return self.root.kind=='permanent'
        if self.name=='runs/training/closure_control.json':return self.root.kind=='training'
        raise AssertionError('artifact existence accessed before closure')
    def read_text(self):
        self.root.reads.append(self.name)
        if self.name=='runs/training/closure_control.json':return json.dumps({'campaign_closed':True})
        raise AssertionError('data or old sampler-go accessed before closure')
    def __truediv__(self,name):raise AssertionError('data path accessed before closure')
for kind in ['permanent','training','hold']:
    root=GuardRoot(kind)
    env={'ROOT':root,'json':json,'hold_active':lambda _:True}
    exec(compile(ast.Module(body=selected,type_ignores=[]),'<closure-functions>','exec'),env)
    for function,args in [('metadata',()),('panel_directory2',('val',)),('panel_directory2',('test',))]:
        try:env[function](*args)
        except PermissionError:pass
        else:raise AssertionError('closure failed to reject '+function)
    assert all(name=='runs/training/closure_control.json' for name in root.reads)
print('source-only permanent/training/hold closure rejection before artifact or sampler-go access PASS')
