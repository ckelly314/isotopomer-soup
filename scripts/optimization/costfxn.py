"""
File: costfxn.py

Calculate cost from model output and N2O incubation data at
each of 2-3 timepoints.
"""


import numpy as np
import pandas as pd


def rmse(array):
    """
    Root mean squared error helper function.
    """

    return np.sqrt(np.sum(array ** 2) / len(array))


def costfxn(
    trainingdata=None,
    modeled_44=None,
    modeled_45a=None,
    modeled_45b=None,
    modeled_46=None,
    weights=None,
):
    """
    Compute differences between measured and modeled data at each incubation
    timepoint, for each isotopomer. Compute root mean squared error for each
    isotopomer, multiply by array of weights, and compute cost from the sum.

    Inputs:
    trainingdata = Pandas Dataframe output from read_data.grid_data
    modeled_44 = numpy array of modeled 44N2O with dimensions (T, 1), where T 
    is the number of model timepoints.
    modeled_45a = modeled 45N2Oa
    modeled_45b = modeled 45N2Ob
    modeled_46 = modeled 46N2O
    weights = numpy array with dimensions (4,) containing weights for model
    error associated with 44N2O, 45N2Oa, 45N2Ob, and 46N2O, in that order.

    Outputs:
    cost = numpy.float64 object containing sum of weights*errors

    """

    t0 = trainingdata.iloc[0] # get adjusted_timepoint at timepoint 0
    t1 = trainingdata.iloc[1] # get adjusted_timepoint at timepoint 1
    
    try: # IF a timepoint 2 exists, get adjusted timepoint
        t2 = trainingdata.iloc[2]
        indices = [
            int(t0["adjusted_timepoint"]),
            int(t1["adjusted_timepoint"]),
            int(t2["adjusted_timepoint"]),
        ] # we'll use the indices array to slice the model output numpy arrays

    except IndexError: # if a timepoint 2 does not exist, indices are just timepoints 0 & 1
        print("No t2 available from incubation data")
        indices = [int(t0["adjusted_timepoint"]), int(t1["adjusted_timepoint"])]

    # compute difference of modeled and measured isotopomers at each timepoint
    error44 = modeled_44[indices] - np.array(trainingdata[["44N2O"]])
    error45a = modeled_45a[indices] - np.array(trainingdata[["45N2Oa"]])
    error45b = modeled_45b[indices] - np.array(trainingdata[["45N2Ob"]])
    error46 = modeled_46[indices] - np.array(trainingdata[["46N2O"]])

    # condense error arrays into an RMSE and return array of RMSE's
    errors = np.array([rmse(error44), rmse(error45a), rmse(error45b), rmse(error46)])

    if weights is None: # allow for weights to be an optional input
        weights = np.array([1, 1, 1, 1]) # default is that weights are all equal to 1

    cost = np.sum(weights * errors) # cost is simply the sum of weights*errors

    return cost
