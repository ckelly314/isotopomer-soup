"""
File: kestimates.py
-------------------

Estimate second-order rate constants to feed as initial guess for optimization.
"""

import pandas as pd
from scipy import stats
from collections import namedtuple

from .. import get_experiment # script for averaging isotopomers
from .. import BioGeoChemistry # initialization script


bgc = BioGeoChemistry() # get concentrations of substrates, spikes, and carriers

def kestimate(inputdata = None, station=None, feature=None, tracer=None, hybrid=False):
    """
    Estimate a second-order rate constant for N2O production from a given substrate.

    Inputs:
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

    try: # add Try and Except to handle instances where I forget to specify required kwargs
        data = get_experiment( # obtain average isotopomer concentrations at each timepoint
            data=inputdata,
            station=station,
            feature=feature,
            tracer=tracer
            )

        data['Incubation_time_days'] = data.Incubation_time_hrs/24. # needed to estimate rate in terms of nM/day

        # use linear regression through 46N2O timepoints to estimate production of 46N2O in nM/day
        # if the rate is negative, set it to 0
        p46 = max(0,stats.linregress(data.Incubation_time_days, data['46N2O']).slope)

        # store key parameters for estimating k in a named tuple for access with dot notation
        substrate = namedtuple('substrate', ['AFsquared','substrate_squared']) 

        # combine named tuples for each substrate into a dict for access during calculations
        if hybrid==False:
            substratedict = {
                'NH4+':substrate(AFsquared=(bgc.NH4_spike/(bgc.NH4_ambient + bgc.NH4_spike))**2, 
                        substrate_squared=(bgc.NH4_ambient + bgc.NH4_spike)**2),
                'NO2-':substrate(AFsquared=(bgc.NO2_spike/(bgc.NO2_ambient + bgc.NO2_spike))**2, 
                        substrate_squared=(bgc.NO2_ambient + bgc.NO2_spike)**2),
                'NO3-':substrate(AFsquared=(bgc.NO3_spike/(bgc.NO3_ambient + bgc.NO3_spike))**2, 
                        substrate_squared=(bgc.NO3_ambient + bgc.NO3_spike)**2)
                }

        elif hybrid==True: # calculation of second-order rate constant is slightly different for hybrid process
            substratedict = {
                'NH4+':substrate(AFsquared=(bgc.NH4_spike/(bgc.NH4_ambient + bgc.NH4_spike))**2, 
                        substrate_squared=(bgc.NH4_ambient + bgc.NH4_spike)*(bgc.NO2_ambient + bgc.NO2_carrier)),
                'NO2-':substrate(AFsquared=(bgc.NO2_spike/(bgc.NO2_ambient + bgc.NO2_spike))**2, 
                        substrate_squared=(bgc.NH4_ambient + bgc.NH4_carrier)*(bgc.NO2_ambient + bgc.NO2_carrier))
                }

        # prdxn of N2O, nM/day, estimated by dividing production of 46N2O by binomial probability of producing 46N2O
        pN2O = p46/substratedict[tracer].AFsquared

        k = pN2O/substratedict[tracer].substrate_squared # 2nd order rate constant, 1/(nM*day)

    except AttributeError: # reminders to myself
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

def kestimates(inputdata = None, station=None, feature=None, hybridtracer=None):
    """
    Return estimated second-order rate constants from the suite of tracer experiments
    at a given station and depth/feature. 

    Inputs:
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

    knh4 = kestimate(inputdata=inputdata, station=station, feature=feature, tracer="NH4+")
    kno2 = kestimate(inputdata=inputdata, station=station, feature=feature, tracer="NO2-")
    kno3 = kestimate(inputdata=inputdata, station=station, feature=feature, tracer="NO3-")
    khybrid = kestimate(inputdata=inputdata, station=station, feature=feature, tracer=hybridtracer, hybrid=True)

    return [knh4, kno2, kno3, khybrid]
