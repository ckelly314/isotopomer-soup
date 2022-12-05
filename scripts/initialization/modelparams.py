"""
File: modelparams.py
--------------------

Initialize model parameters.
"""

import numpy as np

def modelparams():

    ### INITIALIZE MODEL PARAMETERS ###

    # time step (d)
    dt = 0.001  # 0.001 days/timestep or 1,000 timesteps/day
    # dt = 0.2 # 0.2 days/timestep or 5 timesteps/day

    # number of timesteps (y)
    # increasing n(timesteps) by a factor of 10 decreases rate constants by the same factor
    T = 1050  # this gets us up to timestep 999
    times = np.array(list(range(1, T + 1)))  # vector of timesteps

    return (dt,T,times)
