"""
File: initialguess_modelv1.py
---------------------

Run the forward model, version 3, with 0 N2O production and estimate rate constants
to feed to the optimization.
"""

import numpy as np
from scipy import stats

from .. import *


def x0_v1(station=None, feature=None, key=None):
    """
    Estimate second-order rate constants for N2O production from
    different combinations of substrate.

    Inputs:
    station = "PS1", "PS2", or "PS3"
    feature = "Surface", "PNM","Top of oxycline", "Mid-oxycline", "Interface",
        "SCM", "SNM", "Deep ODZ core", "Base of ODZ", or "Deep oxycline"
    key = which experiment to reference:
    "PS1Surface", "PS1Top of oxycline", "PS1Mid-oxycline", "PS1Interface", "PS1SCM",
    "PS2Top of oxycline", "PS2PNM", "PS2Interface", "PS2SCM", "PS2SNM",
    "PS2Deep ODZ core", "PS2Base of ODZ", [...]

    Outputs:
    x0 = [kestimateNH4, kestimateNO, kestimateNO2, kestimateNO3, kestimate_hybrid1,
        kestimate_hybrid2, kestimate_hybrid3, kestimate_hybrid4]
    """

    # we'll estimate k values by first running the model with 0 N2O production,
    # getting estimated concentrations of substrates throughout the model run
    # this means that we need to use either "modelv2" or "modelv1", which include intermediates as state variables
    x = [0, 0, 0, 0, 0]

    # isotope effects and model params are the same for all tracers
    isos = IsotopeEffects()
    (dt, nT, times) = modelparams()
    path_to_file = datapath()

    ### 1. estimate k for N2O production from NH4+ ###

    # to estimate the rate constant for N2O production from NH4+,
    # we'll use the rate of production of 46N2O in the 15NH4+ experiment
    data = grid_data(
        filename=f"{path_to_file}00_incubationdata.csv",
        station=station,
        feature=feature,
        tracer="NH4+",
        T=nT,
    )

    # run model for 15NH4+ experiment
    bgc = BioGeoChemistry(key, tracer="NH4+")
    tr = Tracers(nT, bgc, data)
    tracers = modelv1(x, bgc, isos, tr, (dt, nT, times))

    # calculations
    data["Incubation_time_days"] = (
        data.Incubation_time_hrs / 24.0
    )  # we want rate constants in units of /nM/day
    p46 = max(
        0, stats.linregress(data.Incubation_time_days, data["46N2O"]).slope
    )  # set slope to zero if negative
    probability = (
        tracers.afnh4[1:] ** 2
    )  # total production from bacterial process ~= prdxn. of 46N2O/AF^2
    concentration = (
        tracers.nh4_14[1:] + tracers.nh4_15[1:]
    ) ** 2  # k (/nM/day) = nitrification (nM/day)/[NH4+]^2 (nM)
    kestimateNH4 = np.median(
        p46 / probability / concentration
    )  # take the median value of the resulting array

    print(f"estimated k for N2O production from NH4+: {kestimateNH4}")

    ### 2. estimate k for N2O production from NO3- ###

    # to estimate the rate constant for N2O production from NO3-,
    # we'll use the rate of production of 46N2O in the 15NO3- experiment
    data = grid_data(
        filename=f"{path_to_file}00_incubationdata.csv",
        station=station,
        feature=feature,
        tracer="NO3-",
        T=nT,
    )

    # run model for 15NO3- experiment
    bgc = BioGeoChemistry(key, tracer="NO3-")
    tr = Tracers(nT, bgc, data)
    tracers = modelv1(x, bgc, isos, tr, (dt, nT, times))

    # calculations
    data["Incubation_time_days"] = (
        data.Incubation_time_hrs / 24.0
    )  # we want rate constants in units of /nM/day
    p46 = max(
        0, stats.linregress(data.Incubation_time_days, data["46N2O"]).slope
    )  # set slope to zero if negative
    probability = (
        tracers.afno3[1:] ** 2
    )  # total production from bacterial process ~= prdxn. of 46N2O/AF^2
    concentration = (
        tracers.no3_14[1:] + tracers.no3_15[1:]
    ) ** 2  # k (/nM/day) = nitrification (nM/day)/[NH4+]^2 (nM)
    kestimateNO3 = np.median(
        p46 / probability / concentration
    )  # take the median value of the resulting array

    print(f"estimated k for N2O production from NO3-: {kestimateNO3}")

    ### 3. estimate k for N2O production from NO2- ###

    # to estimate the rate constant for N2O production from NO2-,
    # we'll use the rate of production of 46N2O in the 15NO2- experiment
    data = grid_data(
        filename=f"{path_to_file}00_incubationdata.csv",
        station=station,
        feature=feature,
        tracer="NO2-",
        T=nT,
    )

    # run model for 15NO2- experiment
    bgc = BioGeoChemistry(key, tracer="NO2-")
    tr = Tracers(nT, bgc, data)
    tracers = modelv1(x, bgc, isos, tr, (dt, nT, times))

    # calculations
    data["Incubation_time_days"] = (
        data.Incubation_time_hrs / 24.0
    )  # we want rate constants in units of /nM/day
    p46 = max(
        0, stats.linregress(data.Incubation_time_days, data["46N2O"]).slope
    )  # set slope to zero if negative
    probability = (
        tracers.afno2[1:] ** 2
    )  # total production from bacterial process ~= prdxn. of 46N2O/AF^2
    concentration = (
        tracers.no2_14[1:] + tracers.no2_15[1:]
    ) ** 2  # k (/nM/day) = nitrification (nM/day)/[NH4+]^2 (nM)
    kestimateNO2 = np.median(
        p46 / probability / concentration
    )  # take the median value of the resulting array

    print(f"estimated k for N2O production from NO2-: {kestimateNO2}")

    ### 4. estimate k for N2O production from NO ###

    # to estimate the rate constant for N2O production from NO,
    # we'll use the rate of production of 46N2O in the 15NO2- experiment
    # which is already loaded from above
    probability = (
        tracers.afno[1:] ** 2
    )  # total production from bacterial process ~= prdxn. of 46N2O/AF^2
    concentration = (
        tracers.no_14[1:] + tracers.no_15[1:]
    ) ** 2  # k (/nM/day) = nitrification (nM/day)/[NH4+]^2 (nM)
    kestimateNO = np.median(
        p46 / probability / concentration
    )  # take the median value of the resulting array

    print(f"estimated k for N2O production from NO: {kestimateNO}")

    ### 5. estimate k values for hybrid production from NO2- & NH4+ ###

    # to estimate the rate constants for hybrid N2O production,
    # we'll use the rates of production of 45N2Oa and 45N2Ob in the 15NO2- experiment
    p45a = max(0, stats.linregress(data.Incubation_time_days, data["45N2Oa"]).slope)
    p45b = max(0, stats.linregress(data.Incubation_time_days, data["45N2Ob"]).slope)
    p45average = p45a + p45b

    p1, p2, p3, p4 = binomial(tracers.afno2[1:], tracers.afnh4[1:])

    probabilitya = p2
    probabilityb = p2 + p3
    concentration = (tracers.nh4_14[1:] + tracers.nh4_15[1:]) * (
        tracers.no2_14[1:] + tracers.no2_15[1:]
    )

    kestimate_hybrid1 = np.median(p45a / probabilitya / concentration)
    kestimate_hybrid2 = np.median(p45average / probabilityb / concentration)

    print(f"estimated k for hybrid pathway #1 from NH4+ & NO2-: {kestimate_hybrid1}")
    print(f"estimated k for hybrid pathway #2 from NH4+ & NO2-: {kestimate_hybrid2}")

    ### 6. estimate k values for hybrid production from NO & NH2OH ###

    p1, p2, p3, p4 = binomial_stoichiometry(tracers.afno[1:], tracers.afnh2oh[1:])

    probabilitya = p2
    probabilityb = p2 + p3
    concentration = (tracers.nh2oh_14[1:] + tracers.nh2oh_15[1:]) * (
        tracers.no_14[1:] + tracers.no_15[1:]
    )

    kestimate_hybrid3 = np.median(p45a / probabilitya / concentration)
    kestimate_hybrid4 = np.median(p45average / probabilityb / concentration)

    print(f"estimated k for hybrid pathway #1 from NH2OH & NO: {kestimate_hybrid3}")
    print(f"estimated k for hybrid pathway #2 from NH2OH & NO: {kestimate_hybrid4}")

    ### 7. estimate k values for hybrid production from NO2- & NH2OH ###

    p1, p2, p3, p4 = binomial(tracers.afno2[1:], tracers.afnh2oh[1:])

    probabilitya = p2
    probabilityb = p2 + p3
    concentration = (tracers.nh2oh_14[1:] + tracers.nh2oh_15[1:]) * (
        tracers.no2_14[1:] + tracers.no2_15[1:]
    )

    kestimate_hybrid5 = np.median(p45a / probabilitya / concentration)
    kestimate_hybrid6 = np.median(p45average / probabilityb / concentration)

    print(f"estimated k for hybrid pathway #1 from NH2OH & NO2-: {kestimate_hybrid5}")
    print(f"estimated k for hybrid pathway #2 from NH2OH & NO2-: {kestimate_hybrid6}")

    # function returns:
    return [
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
    ]
