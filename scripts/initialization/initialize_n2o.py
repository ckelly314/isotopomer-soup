"""
File: initialize_n2o.py
-----------------------

Initialize concentrations of N2O isotopomers based on experimental t0.
"""

import pandas as pd


def initialize_n2o(trainingdata=None):
    """
    Initialize concentrations of N2O isotopomers based on experimental t0.

    Inputs:
    trainingdata = trainingdata = Pandas Dataframe output from read_data.grid_data

    Outputs:
    N2O44_init, N2O45a_init, N2O45b_init, N2O46_init
    """

    # these are the initial values measured in one tracer experiment, such as the 15NO2- experiment
    N2O44_init = trainingdata["44N2O"][0]  # nmol/L
    N2O45a_init = trainingdata["45N2Oa"][0]  # nmol/L
    N2O45b_init = trainingdata["45N2Ob"][0]  # nmol/L
    N2O46_init = trainingdata["46N2O"][0]  # nmol/L

    return N2O44_init, N2O45a_init, N2O45b_init, N2O46_init
