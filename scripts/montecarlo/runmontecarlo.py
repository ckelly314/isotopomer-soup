"""
File: runmontecarlo.py
--------------------

Run Monte Carlo simulation, running the model n times
and varying key model parameters randomly by up to 25%
for each iteration.
"""
import pandas as pd
import numpy as np

# use for nelder-mead optimization of a convex function
from scipy.optimize import minimize
from numpy.random import rand
import time  # for calculating execution time

from .genmontecarlo import genmontecarlo

from .. import *


def runmontecarlo(station, feature, iters, weights=None):
    """
    Run Monte Carlo simulation to estimate rate error.

    Inputs:
    station: "PS1", etc.
    feature: "SCM", etc.
    iters: number of model iterations

    Outputs:
    output: Pandas DataFrame with one row per iteration (model solution)
    """

    ### KEYWORDS ###
    stn = station
    ft = feature
    bgckey = stn + ft

    # weights for each tracer experiment
    # in some cases, these should be adjusted to ensure model-data fit for each tracer experiment
    if weights is None:
        weights = np.array([1.0 / 3, 1.0 / 3, 1.0 / 3])

    ### INITIALIZE MEAN STATES FOR EACH TRACER EXPERIMENT ###

    gridded_dataNH4, bgcNH4, isos, trNH4, params = initialize(
        station=stn, feature=ft, tracer="NH4+"
    )
    gridded_dataNO2, bgcNO2, isos, trNO2, params = initialize(
        station=stn, feature=ft, tracer="NO2-"
    )
    gridded_dataNO3, bgcNO3, isos, trNO3, params = initialize(
        station=stn, feature=ft, tracer="NO3-"
    )
    (dt, nT, times) = params

    ### INITIAL GUESS FOR OPTIMIZATION ###
    guess = x0(station=stn, feature=ft, key=bgckey)

    [
        kestimateNH4,
        kestimateNO,
        kestimateNO2,
        kestimateNO3,
        kestimate_hybrid1,
        kestimate_hybrid2,
        kestimate_hybrid3,
        kestimate_hybrid4,
        kestimate_hybrid5,
        kestimate_hybrid6,
    ] = guess

    fguess = 0.5

    x = [kestimateNH4, kestimateNO2, kestimateNO3, kestimate_hybrid2, fguess]

    ### INITIALIZE MONTE CARLO ARRAYS ###
    # each row in each array contains model parameters that have been varied by up to 25%
    # pre-calculating these values (instead of calculating at each iteration) saves memory
    montecarloNH4 = genmontecarlo(bgcNH4, iters)
    montecarloNO2 = genmontecarlo(bgcNO2, iters)
    montecarloNO3 = genmontecarlo(bgcNO3, iters)

    ### OPTIMIZATION PARAMETERS ###
    # define bounds: no negative rate constants, f between 0 and 1
    bnds = ((0, None), (0, None), (0, None), (0, None), (0, 1))  # for model v5

    ### SET UP OUTPUT DF TO STORE MODEL SOLUTIONS ###
    outputdf = pd.DataFrame([])

    ### START ITERATING ###
    for i in range(iters):

        # reset model parameters to the values in row "i" of precalculated randomly varied values
        [
            bgcNH4.nh4_14_i,
            bgcNH4.nh4_15_i,
            bgcNH4.no2_14_i,
            bgcNH4.no2_15_i,
            bgcNH4.no3_14_i,
            bgcNH4.no3_15_i,
            bgcNH4.kNH4TONO2,
            bgcNH4.kNO2TONO3,
            bgcNH4.kNO3TONO2,
            bgcNH4.kN2OCONS,
        ] = montecarloNH4[i, :]

        [
            bgcNO2.nh4_14_i,
            bgcNO2.nh4_15_i,
            bgcNO2.no2_14_i,
            bgcNO2.no2_15_i,
            bgcNO2.no3_14_i,
            bgcNO2.no3_15_i,
            bgcNO2.kNH4TONO2,
            bgcNO2.kNO2TONO3,
            bgcNO2.kNO3TONO2,
            bgcNO2.kN2OCONS,
        ] = montecarloNO2[i, :]

        [
            bgcNO3.nh4_14_i,
            bgcNO3.nh4_15_i,
            bgcNO3.no2_14_i,
            bgcNO3.no2_15_i,
            bgcNO3.no3_14_i,
            bgcNO3.no3_15_i,
            bgcNO3.kNH4TONO2,
            bgcNO3.kNO2TONO3,
            bgcNO3.kNO3TONO2,
            bgcNO3.kN2OCONS,
        ] = montecarloNO3[i, :]

        # re-calculate initial tracer concentrations & atom fractions;
        # re-initialize tracer arrays
        trNH4 = Tracers(nT, bgcNH4, gridded_dataNH4)
        trNO2 = Tracers(nT, bgcNO2, gridded_dataNO2)
        trNO3 = Tracers(nT, bgcNO3, gridded_dataNO3)

        # input args: "bgc" and "tr" values are specific to this iteration
        args = (
            bgcNH4,
            trNH4,
            gridded_dataNH4,
            bgcNO2,
            trNO2,
            gridded_dataNO2,
            bgcNO3,
            trNO3,
            gridded_dataNO3,
            isos,
            params,
            weights,
        )

        # perform the search with intelligently selected x0
        # increasing option "fatol" from factory setting of 0.0001 to 0.1 reduces the amount of time to solve
        st = time.time()
        result = minimize(
            modelv5objective, x, args=args, method="nelder-mead", bounds=bnds
        )  # , options={'maxfev' : 500, 'fatol': 0.1})
        et = time.time()

        # evaluate solution
        solution = result["x"]
        evaluation = modelv5objective(
            solution,
            bgcNH4,
            trNH4,
            gridded_dataNH4,
            bgcNO2,
            trNO2,
            gridded_dataNO2,
            bgcNO3,
            trNO3,
            gridded_dataNO3,
            isos,
            params,
            weights,
        )

        # summarize the result - probably want to take out some of these print statements
        print("Status : %s" % result["message"])
        print("Total Evaluations: %d" % result["nfev"])
        print("Execution time:", (et - st), "seconds")  # get the execution time
        print("Solution: f(%s) = %.5f" % (solution, evaluation))

        # run model with solution from this iteration and process output into mean rates
        tracersNH4 = modelv5(result.x, bgcNH4, isos, trNH4, params)
        tracersNO2 = modelv5(result.x, bgcNO2, isos, trNO2, params)
        tracersNO3 = modelv5(result.x, bgcNO3, isos, trNO3, params)

        outputNH4 = postprocess(bgcNH4, isos, tracersNH4, result.x, model="modelv5")
        outputNO2 = postprocess(bgcNO2, isos, tracersNO2, result.x, model="modelv5")
        outputNO3 = postprocess(bgcNO3, isos, tracersNO3, result.x, model="modelv5")

        saveout = np.array(
            [
                outputNH4[["nitrification", "denitno2", "denitno3", "hybrid2"]].mean(),
                outputNO2[["nitrification", "denitno2", "denitno3", "hybrid2"]].mean(),
                outputNO3[["nitrification", "denitno2", "denitno3", "hybrid2"]].mean(),
            ]
        )

        saveout = saveout.mean(axis=0)

        saveout = pd.DataFrame([saveout]).rename(
            columns={
                0: "Nitrification (nM/day)",
                1: "Denit from NO2- (nM/day)",
                2: "Denit from NO3- (nM/day)",
                3: "Hybrid2 (nM/day)",
            }
        )

        # add some metadata to identify each simulation
        saveout["Station"] = stn
        saveout["Feature"] = ft
        saveout["Key"] = bgckey
        saveout["iteration"] = i
        saveout["cost"] = evaluation
        saveout["f"] = result.x[4]
        saveout["weightNH4"] = weights[0]
        saveout["weightNO2"] = weights[1]
        saveout["weightNO3"] = weights[2]

        # add saveout to output df
        saveout = saveout.set_index("Key")
        outputdf = pd.concat([outputdf, saveout])

    outputdf.to_csv(f"{datapath()}montecarlo.csv")  # save results from this simulation
    print("monte carlo simulation terminated")
