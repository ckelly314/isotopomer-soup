

import pandas as pd

from .datapath import datapath

from .. import *

def run():

	data = pd.read_csv(f"{datapath()}00_incubationdata.csv")
	x = kestimates(inputdata = data, station="PS2", feature="SCM", hybridtracer="NO2-")
	
	### READ IN TRAINING DATA ###
	PS2SCM15NO2 = grid_data(filename=f'{datapath()}00_incubationdata.csv',
                          station="PS2", feature="SCM", tracer="NO2-", 
                          T=1000)
	N2O44_init, N2O45a_init, N2O45b_init, N2O46_init = initialize_n2o(trainingdata = PS2SCM15NO2)

	### ISOTOPE EFFECTS ###
	isos = IsotopeEffects()
	
	print(x)