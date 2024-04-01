"""
File: plotmodeloutput2.py
------------------------

Plot model output with incubation data and save figure as a PDF.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def scatter_plot(
    data=None, station=None, feature=None, tracer=None, modeloutput=None, filename=None
):
    """
    Plot measured timepoints and model output for four N2O isotopocules.

    Inputs:
    inputdata = Pandas Dataframe containing ALL N2O incubation data (not means)
    station = "PS1", "PS2", or "PS3"
    feature = "Surface", "PNM","Top of oxycline", "Mid-soxycline", "Interface",
        "SCM", "SNM", "Deep ODZ core", "Base of ODZ", or "Deep oxycline"
    tracer: "NH4+", "NO2-", or "NO3-"
    modeloutput = Pandas Dataframe containing model output
    filename = filename (string) to use when saving figure
    """

    # colors from https://towardsdatascience.com/making-matplotlib-beautiful-by-default-d0d41e3534fd
    CB91_Blue = "#2CBDFE"
    CB91_Green = "#47DBCD"
    CB91_Pink = "#F3A0F2"
    CB91_Purple = "#9D2EC5"
    CB91_Violet = "#661D98"
    CB91_Amber = "#F5B14C"

    trainingdata = data[
        (data.Station == station) & (data.Feature == feature) & (data.Tracer == tracer)
    ]

    trainingdata = trainingdata[trainingdata.Flag != 4]

    fig, axes = plt.subplots(2, 2, figsize=(7, 6))

    ax = axes[0, 0]
    ax.text(0.05, 0.05, "(a)",
         horizontalalignment = "left",
         verticalalignment = "bottom",
        transform = ax.transAxes)

    ax.plot(
        modeloutput["Incubation_time_hrs"],
        modeloutput["[N2O_44]_nM"],
        label="model output",
        color=CB91_Blue,
        zorder=0,
    )
    ax.scatter(
        trainingdata["Incubation_time_hrs"],
        trainingdata["44N2O"],
        color=CB91_Blue,
        edgecolor="k",
        label="data",
    )

    ax.set_xlabel("Incubation time (hrs)")
    ax.set_ylabel(r"$^{44}N_2O$ (nM)")

    ax = axes[0, 1]
    ax.text(0.95, 0.05, "(b)",
         horizontalalignment = "right",
         verticalalignment = "bottom",
        transform = ax.transAxes)

    ax.plot(
        modeloutput["Incubation_time_hrs"],
        modeloutput["[N2O_46]_nM"],
        label="model output",
        color=CB91_Green,
        zorder=0,
    )
    ax.scatter(
        trainingdata["Incubation_time_hrs"],
        trainingdata["46N2O"],
        color=CB91_Green,
        edgecolor="k",
        label="data",
    )

    ax.set_xlabel("Incubation time (hrs)")
    ax.set_ylabel(r"$^{46}N_2O$ (nM)")

    ax = axes[1, 0]
    ax.text(0.95, 0.05, "(c)",
         horizontalalignment = "right",
         verticalalignment = "bottom",
        transform = ax.transAxes)

    ax.plot(
        modeloutput["Incubation_time_hrs"],
        modeloutput["[N2O_45a]_nM"],
        label="model output",
        color=CB91_Purple,
        zorder=0,
    )
    ax.scatter(
        trainingdata["Incubation_time_hrs"],
        trainingdata["45N2Oa"],
        color=CB91_Purple,
        edgecolor="k",
        label="data",
    )

    ax.set_xlabel("Incubation time (hrs)")
    ax.set_ylabel(r"$^{45}N_2O^{\alpha}$ (nM)")
    ax.legend(fancybox = True, framealpha = 1.0)

    ax = axes[1, 1]
    ax.text(0.95, 0.05, "(d)",
         horizontalalignment = "right",
         verticalalignment = "bottom",
        transform = ax.transAxes)

    ax.plot(
        modeloutput["Incubation_time_hrs"],
        modeloutput["[N2O_45b]_nM"],
        label="model output",
        color=CB91_Amber,
        zorder=0,
    )
    ax.scatter(
        trainingdata["Incubation_time_hrs"],
        trainingdata["45N2Ob"],
        color=CB91_Amber,
        edgecolor="k",
        label="data",
    )

    ax.set_xlabel("Incubation time (hrs)")
    ax.set_ylabel(r"$^{45}N_2O^{\beta}$ (nM)")

    fig.suptitle(f"Station: {station}, Feature: {feature}, Tracer: {tracer}")

    plt.tight_layout()
    plt.savefig(filename)
    plt.show()
