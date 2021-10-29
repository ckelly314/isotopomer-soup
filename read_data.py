"""
File: read_data.py
------------------

Read in incubation data to train N2O production model.
"""

import pandas as pd

def get_experiment(station, feature, tracer):
	
	data = pd.read_csv("00_incubationdata.csv")
		#"../../isotopomer-soup/00_incubationdata.csv")  

	return data[(data.Station==station)&(data.Feature==feature)&(data.Tracer==tracer)]
 