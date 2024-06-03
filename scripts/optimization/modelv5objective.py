"""
File: modelv5objective.py
--------------------

Set up objective function that calculates cost of a model solution
across all three tracer experiments.
"""

import numpy as np

from .costfxn import costfxn

from .. import modelv5

# define objective function
def modelv5objective(
    x,
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
):

    tracersNH4 = modelv5(x, bgcNH4, isos, trNH4, params)  # run model with this solution

    costNH4 = costfxn(
        trainingdata=gridded_dataNH4,  # calculate cost for this solution from model run
        modeled_44=tracersNH4.n2o_44,
        modeled_45a=tracersNH4.n2o_45a,
        modeled_45b=tracersNH4.n2o_45b,
        modeled_46=tracersNH4.n2o_46,
        weights=np.array(
            [1, 1, 1, 1]
        ),  # these are the weights for each individual isotopocule
    )

    tracersNO2 = modelv5(x, bgcNO2, isos, trNO2, params)

    costNO2 = costfxn(
        trainingdata=gridded_dataNO2,
        modeled_44=tracersNO2.n2o_44,
        modeled_45a=tracersNO2.n2o_45a,
        modeled_45b=tracersNO2.n2o_45b,
        modeled_46=tracersNO2.n2o_46,
        weights=np.array([1, 1, 1, 1]),
    )

    tracersNO3 = modelv5(x, bgcNO3, isos, trNO3, params)

    costNO3 = costfxn(
        trainingdata=gridded_dataNO3,
        modeled_44=tracersNO3.n2o_44,
        modeled_45a=tracersNO3.n2o_45a,
        modeled_45b=tracersNO3.n2o_45b,
        modeled_46=tracersNO3.n2o_46,
        weights=np.array([1, 1, 1, 1]),  # np.array([0,0,0,4])
    )

    cost = np.array([costNH4, costNO2, costNO3])

    # print(cost * weights)  # these are the weights for each tracer experiment

    cost = np.sum(cost * weights)

    return cost
