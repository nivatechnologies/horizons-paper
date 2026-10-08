"""Promote stored validation states at the physics boundary; frozen generator unchanged."""
import numpy as np
import acd_stage18_data as frozen
original=frozen.physics.simulate
def simulate(initial,forcing,*args,**kwargs):
    return original(np.asarray(initial,dtype=np.float64),np.asarray(forcing,dtype=np.float64),*args,**kwargs)
frozen.physics.simulate=simulate
frozen.generate()
