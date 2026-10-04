"""Numerical reference, convergence and CPU throughput checks on synthetic states."""
import time
import numpy as np
import torch
from kolmo import KolmoAction
from kolmo_cpu import CPUWorldD
from common import ROOT,write_json,sha

def main():
    torch.set_num_threads(1)
    reference=KolmoAction(np.full(2,40.),.02,np.array([0,3]))
    cpu=CPUWorldD(np.full(2,40.),.02,np.array([0,3]),workers=2)
    z=reference.random_ic(np.random.default_rng(17),2)
    expected=reference.flow(z.clone(),100).numpy()
    actual=cpu.flow(z.numpy().copy(),100)
    relative=float(np.linalg.norm(actual-expected)/np.linalg.norm(expected))
    assert relative<1e-11,relative
    v,d=reference.budget(torch.from_numpy(actual))
    assert np.allclose(cpu.budget(actual),(v+d).numpy(),rtol=1e-12)
    solutions=[]
    for dt in (.01,.005,.0025):
        cpu.set_dt(dt)
        solutions.append(cpu.flow(z.numpy().copy(),int(round(1/dt))))
    coarse=float(np.linalg.norm(solutions[0]-solutions[1]))
    fine=float(np.linalg.norm(solutions[1]-solutions[2]))
    assert coarse/fine>8,(coarse,fine)
    print('reference-relative error',relative,'convergence ratio',coarse/fine,flush=True)
    timings=[]
    for workers in (1,2,4,8):
        model=CPUWorldD(np.full(384,40.),.01,np.repeat(np.arange(6),64),workers=workers)
        x=model.to_spec(np.random.default_rng(123).normal(size=(384,64,64)))
        start=time.perf_counter()
        for _ in range(40):x=model.step(x)
        elapsed=(time.perf_counter()-start)/40
        timings.append(dict(workers=workers,seconds_per_step=elapsed))
        print(timings[-1],flush=True)
    write_json(ROOT/'results/kolmo_cpu_verification.json',dict(reference_relative_error=relative,
               dt_halving_ratio=coarse/fine,timings=timings,git_sha=sha(),data='synthetic timing/verification states; no scientific score'))

if __name__=='__main__':main()
