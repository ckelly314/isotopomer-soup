"""
File: kestimates.py
-------------------

Estimate second-order rate constants to feed as initial guess for optimization.
"""

import pandas as pd
from scipy import stats
from collections import namedtuple

from .. import get_experiment  # script for averaging isotopomers


def kestimate(
    bgc, inputdata=None, station=None, feature=None, tracer=None, hybrid=False
):
    """
    Estimate a second-order rate constant for N2O production from a given substrate.

    Inputs:
    bgc = BioGeoChemistry object, output from bgc.py
    inputdata = Pandas DataFrame object containing isotopomer data from all incubations
    station = "PS1", "PS2", or "PS3"
    feature = "Surface", "PNM","Top of oxycline", "Mid-oxycline", "Interface",
        "SCM", "SNM", "Deep ODZ core", "Base of ODZ", or "Deep oxycline"
    tracer: "NH4+", "NO2-", or "NO3-"
    hybrid (bool, default False) = compute second-order rate constant by dividing by
        [substrate]^2 (hybrid=False), or dividing by [NH4+]*[NO2-]

    Outputs:
    k = estimated second-order rate constant (units are /nM/day)
    """

    try:  # add Try and Except to handle instances where I forget to specify required kwargs
        data = get_experiment(  # obtain average isotopomer concentrations at each timepoint
            data=inputdata, station=station, feature=feature, tracer=tracer
        )

        data["Incubation_time_days"] = (
            data.Incubation_time_hrs / 24.0
        )  # needed to estimate rate in terms of nM/day

        # use linear regression through 46N2O timepoints to estimate production of 46N2O in nM/day
        # if the rate is negative, set it to 0
        p46 = max(0, stats.linregress(data.Incubation_time_days, data["46N2O"]).slope)
        p45a = max(0, stats.linregress(data.Incubation_time_days, data["45N2Oa"]).slope)
        p45b = max(0, stats.linregress(data.Incubation_time_days, data["45N2Ob"]).slope)
        p45 = p45a + p45b

        # store key parameters for estimating k in a named tuple for access with dot notation
        substrate = namedtuple("substrate", ["probability", "concentration"])

        # define atom fraction for natural abundance 15R/14R
        na = 0.00367647 / (1 + 0.00367647)

        # combine named tuples for each substrate into a dict for access during calculations
        if hybrid == False:
            substratedict = {
                "NH4+": substrate(
                    probability=(bgc.NH4_spike / (bgc.NH4_ambient + bgc.NH4_spike)) ** 2,
                    concentration=(bgc.NH4_ambient + bgc.NH4_spike) ** 2,
                ),
                "NO2-": substrate(
                    probability=(bgc.NO2_spike / (bgc.NO2_ambient + bgc.NO2_spike)) ** 2,
                    concentration=(bgc.NO2_ambient + bgc.NO2_spike) ** 2,
                ),
                "NO3-": substrate(
                    probability=(bgc.NO3_spike / (bgc.NO3_ambient + bgc.NO3_spike)) ** 2,
                    concentration=(bgc.NO3_ambient + bgc.NO3_spike) ** 2,
                ),
            }

            # prdxn of N2O, nM/day, estimated by dividing production of 46N2O by binomial probability of producing 46N2O
            pN2O = p46 / substratedict[tracer].probability

            k = (pN2O / substratedict[tracer].concentration)  # 2nd order rate constant, 1/(nM*day)


        elif (
            hybrid == True
        ):  # calculation of second-order rate constant is slightly different for hybrid process
            afnh4 = (bgc.NH4_spike / (bgc.NH4_ambient + bgc.NH4_spike))
            afno2 = (bgc.NO2_spike / (bgc.NO2_ambient + bgc.NO2_spike))

            substratedict = {
                "NH4+": substrate(
                    probability= afnh4*(1-na) + (1-afnh4)*na,
                    concentration=(bgc.NH4_ambient + bgc.NH4_spike)* (bgc.NO2_ambient + bgc.NO2_carrier)
                    ),
                "NO2-": substrate(
                    probability= afno2*(1-na) + (1-afno2)*na,
                    concentration=(bgc.NH4_ambient + bgc.NH4_carrier)* (bgc.NO2_ambient + bgc.NO2_spike)
                    #(bgc.NH4_ambient + bgc.NH4_carrier)
                    #* (bgc.NO2_ambient + bgc.NO2_carrier),
                ),
            }

            pN2O = p45 / substratedict[tracer].probability

            k = (pN2O / substratedict[tracer].concentration)


    except AttributeError:  # reminders to myself
        if inputdata is None:
            print("Please specify input data!")
        if station is None:
            print("Please specify station!")
        if feature is None:
            print("Please specify feature!")
        if tracer is None:
            print("Please specify tracer!")

        k = "Unable to calculate k"

    return k


def kestimates(bgc, inputdata=None, station=None, feature=None, hybridtracer=None):
    """
    Return estimated second-order rate constants from the suite of tracer experiments
    at a given station and depth/feature.

    Inputs:
    bgc = BioGeoChemistry object, output from bgc.py
    inputdata = Pandas DataFrame object containing isotopomer data from all incubations
    station = "PS1", "PS2", or "PS3"
    feature = "Surface", "PNM","Top of oxycline", "Mid-oxycline", "Interface",
        "SCM", "SNM", "Deep ODZ core", "Base of ODZ", or "Deep oxycline"
    hybridtracer: "NH4+" or "NO2-". Tracer experiment from which to estimate hybrid
        rate constant

    Outputs:
    [knh4, kno2, kno3, khybrid] = estimated second-order rate constants for N2O production
        from NH4+, NO2-, NO3-, and a hybrid process combining NH4+ and NO2-
    """

    knh4 = kestimate(
        bgc, inputdata=inputdata, station=station, feature=feature, tracer="NH4+"
    )
    kno2 = kestimate(
        bgc, inputdata=inputdata, station=station, feature=feature, tracer="NO2-"
    )
    kno3 = kestimate(
        bgc, inputdata=inputdata, station=station, feature=feature, tracer="NO3-"
    )
    khybrid = kestimate(
        bgc,
        inputdata=inputdata,
        station=station,
        feature=feature,
        tracer=hybridtracer,
        hybrid=True,
    )

    return [knh4, kno2, kno3, khybrid]
