"""
File: modelparams.py
--------------------

Initialize model parameters and arrays of state variables.
"""

import numpy as np

from .initialize_n2o import initialize_n2o


def modelparams(bgc, trainingdata):

	### INITIALIZE MODEL PARAMETERS ###

	# time step (d)
	dt = 0.001 # 0.001 days/timestep or 1,000 timesteps/day
	#dt = 0.2 # 0.2 days/timestep or 5 timesteps/day

	# number of timesteps (y)
	# increasing n(timesteps) by a factor of 10 decreases rate constants by the same factor
	T = 1000 # this gets us up to timestep 999
	times = np.array(list(range(1,T+1))) # vector of timesteps

	### INITIALIZE STATE VARIABLES ###

	N2O44_init, N2O45a_init, N2O45b_init, N2O46_init = initialize_n2o(trainingdata = trainingdata)

	# initialize arrays of state variables
	n2o_44 = np.zeros(shape = (T,1))
	n2o_45a = np.zeros(shape = (T,1))
	n2o_45b = np.zeros(shape = (T,1))
	n2o_46 = np.zeros(shape = (T,1))
	nh4_14 = np.zeros(shape = (T,1))
	nh4_15 = np.zeros(shape = (T,1))
	no2_14 = np.zeros(shape = (T,1))
	no2_15 = np.zeros(shape = (T,1))
	no3_14 = np.zeros(shape = (T,1))
	no3_15 = np.zeros(shape = (T,1))
	n2_28 = np.zeros(shape = (T,1))
	n2_29 = np.zeros(shape = (T,1))
	n2_30 = np.zeros(shape = (T,1))

	afnh4 = np.zeros(shape = (T,1))
	afno2 = np.zeros(shape = (T,1))
	afno3 = np.zeros(shape = (T,1))

	# initial values of state variables
	
	n2o_44[0,:] = N2O44_init
	n2o_45a[0,:] = N2O45a_init
	n2o_45b[0,:] = N2O45b_init
	n2o_46[0,:] = N2O46_init
	nh4_14[0,:] = bgc.nh4_14_i
	nh4_15[0,:] = bgc.nh4_15_i
	no2_14[0,:] = bgc.no2_14_i
	no2_15[0,:] = bgc.no2_15_i
	no3_14[0,:] = bgc.no3_14_i
	no3_15[0,:] = bgc.no3_15_i
	n2_28[0,:] = 0
	n2_29[0,:] = 0
	n2_30[0,:] = 0

	afnh4[0,:] = bgc.AFNH4_init
	afno2[0,:] = bgc.AFNO2_init
	afno3[0,:] = bgc.AFNO3_init

	return (dt, T, times,
			n2o_44, n2o_45a, n2o_45b, n2o_46,
			nh4_14, nh4_15, no2_14, no2_15, no3_14, no3_15,
			n2_28, n2_29, n2_30,
			afnh4, afno2, afno3)
