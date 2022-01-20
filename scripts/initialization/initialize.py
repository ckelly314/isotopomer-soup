"""
initialize.py
-------------

Initialize inputs for model.
"""

from .. import grid_data, datapath
from .bgc import BioGeoChemistry
from .modelparams import modelparams
from .tracers import Tracers
from .isotope_effects import IsotopeEffects

def initialize(station=None, feature=None, tracer=None):

    stn = station
    ft = feature
    t = tracer
    bgckey = stn+ft

    ### INITIALIZATION ###

    ### MODEL PARAMS ###
    params = modelparams()
    (dt, nT, times) = params

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
    tr = Tracers(nT, bgc, gridded_data) 

    return gridded_data, bgc, isos, tr, params