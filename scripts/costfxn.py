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
    measured_data=None,
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
    measured_data = Pandas Dataframe output from read_data.grid_data
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

    t0 = measured_data.iloc[0]
    t1 = measured_data.iloc[1]
    try:
        t2 = measured_data.iloc[2]
        indices = [
            int(t0["adjusted_timepoint"]),
            int(t1["adjusted_timepoint"]),
            int(t2["adjusted_timepoint"]),
        ]

    except IndexError:
        print("No t2 available from incubation data")
        indices = [int(t0["adjusted_timepoint"]), int(t1["adjusted_timepoint"])]

    error44 = modeled_44[indices] - np.array(measured_data[["44N2O"]])
    error45a = modeled_45a[indices] - np.array(measured_data[["45N2Oa"]])
    error45b = modeled_45b[indices] - np.array(measured_data[["45N2Ob"]])
    error46 = modeled_46[indices] - np.array(measured_data[["46N2O"]])

    errors = np.array([rmse(error44), rmse(error45a), rmse(error45b), rmse(error46)])

    if weights is None:
        weights = np.array([1, 1, 1, 1])

    cost = np.sum(weights * errors)

    return cost
