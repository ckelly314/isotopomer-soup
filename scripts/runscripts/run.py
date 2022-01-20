import pandas as pd

from .datapath import datapath

from .. import *


def run():

    stn = "PS2"
    ft = "Interface"
    t = "NO2-"
    bgckey = stn+ft

    ### INITIALIZATION ###

    # training data
    path_to_data = datapath()
    filename = '00_incubationdata.csv'

    gridded_data = grid_data(filename=f'{path_to_data}{filename}',
                              station=stn, feature=ft, tracer=t, 
                              T=1000)

    ### SUBSTRATE CONCENTRATIONS AND RATES OF EXCHANGE ###
    bgc = BioGeoChemistry(bgckey, tracer=t)

    ### ISOTOPE EFFECTS ###
    isos = IsotopeEffects()

    ### STATE VARIABLES ###
    tr = Tracers(bgc, gridded_data) 

    ### MODEL PARAMS ###
    params = modelparams()

    print("test complete")
