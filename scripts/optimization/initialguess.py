"""
File: initialguess.py
---------------------

Run the forward model, version 3, with 0 N2O production and estimate rate constants
to feed to the optimization.
"""

import numpy as np
from scipy import stats

from .. import *


def x0(station=None, feature=None, key=None):
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
    # this means that we need to use either "modelv2" or "modelv3", which include intermediates as state variables
    x = [0, 0, 0, 0, 0]

    # isotope effects and model params are the same for all tracers
    isos = IsotopeEffects()
    (dt, nT, times) = modelparams()
    path_to_file = datapath()

    ### 1. estimate k for N2O production from NH4+ ###

    # to estimate the rate constant for N2O production from NH4+,
    # we'll use the rate of production of 46N2O in the 15NH4+ experiment
    dataNH4 = grid_data(
        filename=f"{path_to_file}00_incubationdata.csv",
        station=station,
        feature=feature,
        tracer="NH4+",
        T=nT,
    )

    # run model for 15NH4+ experiment
    bgcNH4 = BioGeoChemistry(key, tracer="NH4+")
    trNH4 = Tracers(nT, bgcNH4, dataNH4)
    tracersNH4 = modelv3(x, bgcNH4, isos, trNH4, (dt, nT, times))

    # calculations
    dataNH4["Incubation_time_days"] = (
        dataNH4.Incubation_time_hrs / 24.0
    )  # we want rate constants in units of /nM/day
    p46NH4 = max(
        0, stats.linregress(dataNH4.Incubation_time_days, dataNH4["46N2O"]).slope
    )  # set slope to zero if negative
    probabilityNH4 = (
        tracersNH4.afnh4[1:] ** 2
    )  # total production from bacterial process ~= prdxn. of 46N2O/AF^2
    concentrationNH4 = (
        tracersNH4.nh4_14[1:] + tracersNH4.nh4_15[1:]
    ) ** 2  # k (/nM/day) = nitrification (nM/day)/[NH4+]^2 (nM)
    kestimateNH4 = np.median(
        p46NH4 / probabilityNH4 / concentrationNH4
    )  # take the median value of the resulting array

    print(f"estimated k for N2O production from NH4+: {kestimateNH4}")

    ### 2. estimate k for N2O production from NO3- ###

    # to estimate the rate constant for N2O production from NO3-,
    # we'll use the rate of production of 46N2O in the 15NO3- experiment
    dataNO3 = grid_data(
        filename=f"{path_to_file}00_incubationdata.csv",
        station=station,
        feature=feature,
        tracer="NO3-",
        T=nT,
    )

    # run model for 15NO3- experiment
    bgcNO3 = BioGeoChemistry(key, tracer="NO3-")
    trNO3 = Tracers(nT, bgcNO3, dataNO3)
    tracersNO3 = modelv3(x, bgcNO3, isos, trNO3, (dt, nT, times))

    # calculations
    dataNO3["Incubation_time_days"] = (
        dataNO3.Incubation_time_hrs / 24.0
    )  # we want rate constants in units of /nM/day
    p46NO3 = max(
        0, stats.linregress(dataNO3.Incubation_time_days, dataNO3["46N2O"]).slope
    )  # set slope to zero if negative
    probabilityNO3 = (
        tracersNO3.afno3[1:] ** 2
    )  # total production from bacterial process ~= prdxn. of 46N2O/AF^2
    concentrationNO3 = (
        tracersNO3.no3_14[1:] + tracersNO3.no3_15[1:]
    ) ** 2  # k (/nM/day) = nitrification (nM/day)/[NH4+]^2 (nM)
    kestimateNO3 = np.median(
        p46NO3 / probabilityNO3 / concentrationNO3
    )  # take the median value of the resulting array

    print(f"estimated k for N2O production from NO3-: {kestimateNO3}")

    ### 3. estimate k for N2O production from NO2- ###

    # to estimate the rate constant for N2O production from NO2-,
    # we'll use the rate of production of 46N2O in the 15NO2- experiment
    dataNO2 = grid_data(
        filename=f"{path_to_file}00_incubationdata.csv",
        station=station,
        feature=feature,
        tracer="NO2-",
        T=nT,
    )

    # run model for 15NO2- experiment
    bgcNO2 = BioGeoChemistry(key, tracer="NO2-")
    trNO2 = Tracers(nT, bgcNO2, dataNO2)
    tracersNO2 = modelv3(x, bgcNO2, isos, trNO2, (dt, nT, times))

    # calculations
    dataNO2["Incubation_time_days"] = (
        dataNO2.Incubation_time_hrs / 24.0
    )  # we want rate constants in units of /nM/day
    p46NO2 = max(
        0, stats.linregress(dataNO2.Incubation_time_days, dataNO2["46N2O"]).slope
    )  # set slope to zero if negative
    probabilityNO2 = (
        tracersNO2.afno2[1:] ** 2
    )  # total production from bacterial process ~= prdxn. of 46N2O/AF^2
    concentrationNO2 = (
        tracersNO2.no2_14[1:] + tracersNO2.no2_15[1:]
    ) ** 2  # k (/nM/day) = nitrification (nM/day)/[NH4+]^2 (nM)
    kestimateNO2 = np.median(
        p46NO2 / probabilityNO2 / concentrationNO2
    )  # take the median value of the resulting array

    print(f"estimated k for N2O production from NO2-: {kestimateNO2}")

    ### 4. estimate k for N2O production from NO ###

    # to estimate the rate constant for N2O production from NO,
    # we'll use the rate of production of 46N2O in the 15NO2- experiment
    # which is already loaded from above
    probabilityNO = (
        tracersNO2.afno[1:] ** 2
    )  # total production from bacterial process ~= prdxn. of 46N2O/AF^2
    concentrationNO = (
        tracersNO2.no_14[1:] + tracersNO2.no_15[1:]
    ) ** 2  # k (/nM/day) = nitrification (nM/day)/[NH4+]^2 (nM)
    kestimateNO = np.median(
        p46NO2 / probabilityNO / concentrationNO
    )  # take the median value of the resulting array

    print(f"estimated k for N2O production from NO: {kestimateNO}")

    ### 5. estimate k values for hybrid production from NO2- & NH4+ ###

    # to estimate the rate constants for hybrid N2O production,
    # we'll use the rates of production of 45N2Oa and 45N2Ob in the 15NO2- experiment
    p45aNO2 = max(
        0, stats.linregress(dataNO2.Incubation_time_days, dataNO2["45N2Oa"]).slope
    )
    p45bNO2 = max(
        0, stats.linregress(dataNO2.Incubation_time_days, dataNO2["45N2Ob"]).slope
    )
    p45averageNO2 = p45aNO2 + p45bNO2

    p45aNH4 = max(
        0, stats.linregress(dataNH4.Incubation_time_days, dataNH4["45N2Oa"]).slope
    )
    p45bNH4 = max(
        0, stats.linregress(dataNH4.Incubation_time_days, dataNH4["45N2Ob"]).slope
    )
    p45averageNH4 = p45aNH4 + p45bNH4

    p1NO2, p2NO2, p3NO2, p4NO2 = binomial(tracersNO2.afno2[1:], tracersNO2.afnh4[1:])
    p1NH4, p2NH4, p3NH4, p4NH4 = binomial(tracersNH4.afno2[1:], tracersNH4.afnh4[1:])

    probabilityaNO2 = p2NO2
    probabilitybNO2 = p2NO2 + p3NO2
    concentrationNO2 = (tracersNO2.nh4_14[1:] + tracersNO2.nh4_15[1:]) * (
        tracersNO2.no2_14[1:] + tracersNO2.no2_15[1:]
    )

    probabilityaNH4 = p2NH4
    probabilitybNH4 = p2NH4 + p3NH4
    concentrationNH4 = (tracersNH4.nh4_14[1:] + tracersNH4.nh4_15[1:]) * (
        tracersNH4.no2_14[1:] + tracersNH4.no2_15[1:]
    )

    kestimate_hybrid1NO2 = np.median(p45aNO2 / probabilityaNO2 / concentrationNO2)
    kestimate_hybrid2NO2 = np.median(p45averageNO2 / probabilitybNO2 / concentrationNO2)

    kestimate_hybrid1NH4 = np.median(p45aNH4 / probabilityaNH4 / concentrationNH4)
    kestimate_hybrid2NH4 = np.median(p45averageNH4 / probabilitybNH4 / concentrationNH4)

    kestimate_hybrid1 = (kestimate_hybrid1NO2 + kestimate_hybrid1NH4) / 2
    kestimate_hybrid2 = (kestimate_hybrid2NO2 + kestimate_hybrid2NH4) / 2

    print(f"estimated k for hybrid pathway #1 from NH4+ & NO2-: {kestimate_hybrid1}")
    print(f"estimated k for hybrid pathway #2 from NH4+ & NO2-: {kestimate_hybrid2}")

    ### 6. estimate k values for hybrid production from NO & NH2OH ###

    p1NO2, p2NO2, p3NO2, p4NO2 = binomial_stoichiometry(
        tracersNO2.afno[1:], tracersNO2.afnh2oh[1:]
    )
    p1NH4, p2NH4, p3NH4, p4NH4 = binomial_stoichiometry(
        tracersNH4.afno[1:], tracersNH4.afnh2oh[1:]
    )

    probabilityaNO2 = p2NO2
    probabilitybNO2 = p2NO2 + p3NO2
    concentrationNO2 = (tracersNO2.nh2oh_14[1:] + tracersNO2.nh2oh_15[1:]) * (
        tracersNO2.no_14[1:] + tracersNO2.no_15[1:]
    )

    probabilityaNH4 = p2NH4
    probabilitybNH4 = p2NH4 + p3NH4
    concentrationNH4 = (tracersNH4.nh2oh_14[1:] + tracersNH4.nh2oh_15[1:]) * (
        tracersNH4.no_14[1:] + tracersNH4.no_15[1:]
    )

    kestimate_hybrid3NO2 = np.median(p45aNO2 / probabilityaNO2 / concentrationNO2)
    kestimate_hybrid4NO2 = np.median(p45averageNO2 / probabilitybNO2 / concentrationNO2)

    kestimate_hybrid3NH4 = np.median(p45aNH4 / probabilityaNH4 / concentrationNH4)
    kestimate_hybrid4NH4 = np.median(p45averageNH4 / probabilitybNH4 / concentrationNH4)

    kestimate_hybrid3 = (kestimate_hybrid3NO2 + kestimate_hybrid3NH4) / 2
    kestimate_hybrid4 = (kestimate_hybrid4NO2 + kestimate_hybrid4NH4) / 2

    print(f"estimated k for hybrid pathway #1 from NH2OH & NO: {kestimate_hybrid3}")
    print(f"estimated k for hybrid pathway #2 from NH2OH & NO: {kestimate_hybrid4}")

    ### 7. estimate k values for hybrid production from NO2- & NH2OH ###

    p1NO2, p2NO2, p3NO2, p4NO2 = binomial(tracersNO2.afno2[1:], tracersNO2.afnh2oh[1:])
    p1NH4, p2NH4, p3NH4, p4NH4 = binomial(tracersNH4.afno2[1:], tracersNH4.afnh2oh[1:])

    probabilityaNO2 = p2NO2
    probabilitybNO2 = p2NO2 + p3NO2
    concentrationNO2 = (tracersNO2.nh2oh_14[1:] + tracersNO2.nh2oh_15[1:]) * (
        tracersNO2.no2_14[1:] + tracersNO2.no2_15[1:]
    )

    probabilityaNH4 = p2NH4
    probabilitybNH4 = p2NH4 + p3NH4
    concentrationNH4 = (tracersNH4.nh2oh_14[1:] + tracersNH4.nh2oh_15[1:]) * (
        tracersNH4.no2_14[1:] + tracersNH4.no2_15[1:]
    )

    kestimate_hybrid5NO2 = np.median(p45aNO2 / probabilityaNO2 / concentrationNO2)
    kestimate_hybrid6NO2 = np.median(p45averageNO2 / probabilitybNO2 / concentrationNO2)

    kestimate_hybrid5NH4 = np.median(p45aNH4 / probabilityaNH4 / concentrationNH4)
    kestimate_hybrid6NH4 = np.median(p45averageNH4 / probabilitybNH4 / concentrationNH4)

    kestimate_hybrid5 = (kestimate_hybrid5NO2 + kestimate_hybrid5NH4) / 2
    kestimate_hybrid6 = (kestimate_hybrid6NO2 + kestimate_hybrid6NH4) / 2

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
