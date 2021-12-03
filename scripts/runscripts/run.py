

import pandas as pd

from .datapath import datapath

from .. import *

def run():
	
	### READ IN TRAINING DATA ###
	data = pd.read_csv(f"{datapath()}00_incubationdata.csv")
	PS2SCM15NO2 = grid_data(filename=f'{datapath()}00_incubationdata.csv',
                          station="PS2", feature="SCM", tracer="NO2-", 
                          T=1000)
	N2O44_init, N2O45a_init, N2O45b_init, N2O46_init = initialize_n2o(trainingdata = PS2SCM15NO2)

	### ISOTOPE EFFECTS ###
	isos = IsotopeEffects()

	bgc = BioGeoChemistry()
	
	x = kestimates(bgc, inputdata = data, station="PS2", feature="SCM", hybridtracer="NO2-")
	
	print(x)