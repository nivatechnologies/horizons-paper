"""Standalone exact inherited CNN and frozen direct-cost head."""
import torch
from torch import nn
class Emulator(nn.Module):
    def __init__(self):
        super().__init__()
        sizes=[12,256,256,256,256,1];layers=[]
        for i in range(5):
            k=5 if i<4 else 1
            layers.append(nn.Conv1d(sizes[i],sizes[i+1],k,padding=k//2,padding_mode="circular"))
            if i<4:layers.append(nn.GELU())
        self.net=nn.Sequential(*layers)
    def forward(self,frames,action):
        return frames[:,-1]+self.net(torch.cat([frames,action[:,None]],1))[:,0]
class CostModel(nn.Module):
    def __init__(self):
        super().__init__()
        sizes=[12,256,256,256,256];layers=[]
        for i in range(4):
            layers.extend([nn.Conv1d(sizes[i],sizes[i+1],5,padding=2,padding_mode="circular"),nn.GELU()])
        self.trunk=nn.Sequential(*layers)
        self.head=nn.Sequential(nn.Linear(256,64),nn.GELU(),nn.Linear(64,1))
    def forward(self,frames,action):
        return self.head(self.trunk(torch.cat([frames,action[:,None]],1)).mean(-1))[:,0]
def cuda_rules():
    torch.set_num_threads(1)
    torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False
    torch.backends.cudnn.deterministic=True
    torch.backends.cudnn.benchmark=False

