"""
File: tracers.py
--------------------

Initialize model parameters and arrays of state variables.
"""

import numpy as np

from .initialize_n2o import initialize_n2o


class Tracers:

    def __init__(self, bgc, trainingdata):

        ### INITIALIZE STATE VARIABLES ###

        T = 1000

        N2O44_init, N2O45a_init, N2O45b_init, N2O46_init = initialize_n2o(
            trainingdata=trainingdata
        )

        # initialize arrays of state variables
        # specify dtype to prevent overflow errors
        self.n2o_44 = np.zeros(shape=(T, 1), dtype='float64')
        self.n2o_45a = np.zeros(shape=(T, 1), dtype='float64')
        self.n2o_45b = np.zeros(shape=(T, 1), dtype='float64')
        self.n2o_46 = np.zeros(shape=(T, 1), dtype='float64')

        self.nh4_14 = np.zeros(shape=(T, 1), dtype='float64')
        self.nh4_15 = np.zeros(shape=(T, 1), dtype='float64')

        self.nh2oh_14 = np.zeros(shape=(T, 1), dtype='float64')
        self.nh2oh_15 = np.zeros(shape=(T, 1), dtype='float64')

        self.no_14 = np.zeros(shape=(T, 1), dtype='float64')
        self.no_15 = np.zeros(shape=(T, 1), dtype='float64')

        self.no2_14 = np.zeros(shape=(T, 1), dtype='float64')
        self.no2_15 = np.zeros(shape=(T, 1), dtype='float64')

        self.no3_14 = np.zeros(shape=(T, 1), dtype='float64')
        self.no3_15 = np.zeros(shape=(T, 1), dtype='float64')

        self.n2_28 = np.zeros(shape=(T, 1), dtype='float64')
        self.n2_29 = np.zeros(shape=(T, 1), dtype='float64')
        self.n2_30 = np.zeros(shape=(T, 1), dtype='float64')

        self.afnh4 = np.zeros(shape=(T, 1), dtype='float64')
        self.afno2 = np.zeros(shape=(T, 1), dtype='float64')
        self.afno3 = np.zeros(shape=(T, 1), dtype='float64')

        self.afnh2oh = np.zeros(shape=(T, 1), dtype='float64')
        self.afno = np.zeros(shape=(T, 1), dtype='float64')

        # initial values of state variables

        self.n2o_44[0, :] = N2O44_init
        self.n2o_45a[0, :] = N2O45a_init
        self.n2o_45b[0, :] = N2O45b_init
        self.n2o_46[0, :] = N2O46_init

        self.nh4_14[0, :] = bgc.nh4_14_i
        self.nh4_15[0, :] = bgc.nh4_15_i

        self.nh2oh_14[0, :] = 0
        self.nh2oh_15[0, :] = 0

        self.no_14[0, :] = 0
        self.no_15[0, :] = 0

        self.no2_14[0, :] = bgc.no2_14_i
        self.no2_15[0, :] = bgc.no2_15_i

        self.no3_14[0, :] = bgc.no3_14_i
        self.no3_15[0, :] = bgc.no3_15_i
        

        self.n2_28[0, :] = 0
        self.n2_29[0, :] = 0
        self.n2_30[0, :] = 0

        self.afnh4[0, :] = bgc.AFNH4_init
        self.afno2[0, :] = bgc.AFNO2_init
        self.afno3[0, :] = bgc.AFNO3_init

        self.afnh2oh[0, :] = 0
        self.afno[0, :] = 0

    def __repr__(self):
        return "state variable arrays initialized!"
