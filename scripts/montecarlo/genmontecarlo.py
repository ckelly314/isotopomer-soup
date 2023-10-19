"""
File: genmontecarlo.py
--------------------

Create nxm Numpy array of model parameters randomly sampled from a range of values
from 75% to 125% of the parameter value, where n is the number of rows and m is the
number of parameters.
"""

import numpy as np
from numpy.random import rand


def genmontecarlo(bgc, iters):
    """
    Generate Numpy array of randomly sampled model params.

    Inputs:
    bgc = "BioGeoChemistry" object from bgc.py
    iters = desired number of rows in output array

    Outputs:
    nxm Numpy array of model parameters randomly sampled from a range of values
    from 75% to 125% of the parameter value, where n is the number of rows and m is the
    number of parameters.
    """

    # pull model params from bgc object and store in 1xm Numpy array
    # means =  np.array([bgc.nh4_14_i, bgc.nh4_15_i, bgc.no2_14_i, bgc.no2_15_i, bgc.no3_14_i, bgc.no3_15_i, bgc.AFNH4_init, bgc.AFNO2_init, bgc.AFNO3_init, bgc.kNH4TONO2, bgc.kNO2TONO3, bgc.kNO3TONO2, bgc.kN2OCONS])
    means = np.array(
        [
            bgc.nh4_14_i,
            bgc.nh4_15_i,
            bgc.no2_14_i,
            bgc.no2_15_i,
            bgc.no3_14_i,
            bgc.no3_15_i,
            bgc.kNH4TONO2,
            bgc.kNO2TONO3,
            bgc.kNO3TONO2,
            bgc.kN2OCONS,
        ]
    )

    mins = means * 0.75  # create 1xm Numpy array of minimum values
    maxs = means * 1.25  # create 1xm Numpy array of maximum values

    # create nxm array of ones to multiply by means
    arr = np.ones((iters, len(means)))
    # create nxm array of mean model params to add variability on top of
    arr = (
        arr * means
    )

    # create nxm array of random values sampled between 0 and 1
    randvals = rand(
        iters, len(means)
    )

    # create nxm array of mean values + variability
    output = arr + randvals * (
        maxs - mins
    )

    return output
