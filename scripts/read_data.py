"""
File: read_data.py
------------------

Read in incubation data to train N2O production model.
"""

import pandas as pd


def read_data(filename):

    return pd.read_csv(filename)


def get_experiment(data=None, station=None, feature=None, tracer=None):
    """
    Select data, compute timepoint means, and remove extra columns.
    """

    trainingdata = data[
        (data.Station == station) & (data.Feature == feature) & (data.Tracer == tracer)
    ]

    timepoints = trainingdata.groupby("Incubation_time_hrs").mean().reset_index()

    timepoints = timepoints[
        ["Incubation_time_hrs", "44N2O", "45N2Oa", "45N2Ob", "46N2O"]
    ]

    return timepoints


def grid_data(filename=None, station=None, feature=None, tracer=None, T=None):
    """
    Obtain 44N2O, 45N2Oa, 45N2Ob, and 46N2O data from desired incubation at each
    of 2-3 timepoints (some experiments did not have data from all three timepoints
    post-QC). Compute integer timepoints from incubation time in hours. Add an
    "adjusted timepoint" column that slides the incubation data left, such that
    model timepoint 0 matches up with data timepoint 0: the model's "timepoint 0"
    is actually something non-zero, such as 12, because incubation t0's were
    typically taken within the first half-hour.

    Inputs:
    filename = name of .csv file containing all incubation data
    station = "PS1", "PS2", or "PS3"
    feature = "Surface", "PNM","Top of oxycline", "Mid-oxycline", "Interface",
        "SCM", "SNM", "Deep ODZ core", "Base of ODZ", or "Deep oxycline"
    tracer: "NH4+", "NO2-", or "NO3-"
    T = number of timepoints in the model, typically 1000

    Outputs:
    gridded_data = Pandas DataFrame object containing the mean value at each of
        2-3 timepoints for columns ['Incubation_time_hrs', '44N2O', '45N2Oa',
        '45N2Ob', '46N2O', 'x', 'timepoint', 'adjusted_timepoint']

    """

    data = read_data(filename)

    experiment = get_experiment(
        data=data, station=station, feature=feature, tracer=tracer
    )

    gridded_data = experiment

    gridded_data["x"] = (  # time(timepoints) = time(hrs) * (1 day/24 hrs) * (T timepoints/day)
        gridded_data.Incubation_time_hrs / 24 * T
    )
    gridded_data["timepoint"] = round(  # round timepoints to nearest integer to match w/ model output
        gridded_data.x, 0
    )
    gridded_data["adjusted_timepoint"] = (   # "slide" data to the left to match model output
        gridded_data["timepoint"] - gridded_data["timepoint"][0]
    )

    return gridded_data


if __name__ == "__main__":
    print(
        get_experiment(
            data=read_data(filename="../../isotopomer-soup/00_incubationdata.csv"),
            station="PS2",
            feature="SCM",
            tracer="NO2-",
        ).head()
    )
