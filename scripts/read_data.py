"""
File: read_data.py
------------------

Read in incubation data to train N2O production model.
"""

import pandas as pd

def read_data(filename):

    return pd.read_csv(filename)

def get_experiment(data=None, station=None, feature=None, tracer=None):

    trainingdata = data[(data.Station==station)&(data.Feature==feature)&(data.Tracer==tracer)]

    timepoints = trainingdata.groupby('Incubation_time_hrs').mean().reset_index()

    timepoints = timepoints[['Incubation_time_hrs', '44N2O','45N2Oa', '45N2Ob', '46N2O']]

    return timepoints

if __name__=="__main__":
    print(get_experiment(data = read_data(filename = "../../isotopomer-soup/00_incubationdata.csv"),
     station="PS2", feature="SCM", tracer="NO2-").head())
 