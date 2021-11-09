"""
File: plotmodeloutput.py
------------------------

Plot model output with incubation data and save figure as a PDF.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interp


def plot_interpolation(ax, x, y):
    """
    Helper function to plot interpolation of measured timepoints.
    """

    x_fine = np.linspace(x.min(), x.max())  # define range of x to interpolate over
    ax.plot(x, y, "bo", label="measured timepoints")  # plot measured timepoints
    ax.plot(
        x_fine,
        interp.interp1d(x, y, kind="quadratic")(x_fine), # perform 1-D interpolation in-line with plotting
        zorder=0,
        label="quadratic interpolation",
    )


def plot_outputs(incubationdata=None, modeloutput=None, filename=None):
    """
    Plot measured timepoints and model output for four N2O isotopocules.

    Inputs:
    incubationdata = Pandas Dataframe output from read_data.grid_data
    modeloutput = Pandas Dataframe containing model output
    filename = filename (string) to use when saving figure
    """

    fig, axes = plt.subplots(2, 2, figsize=(8, 6))

    ax = axes[0, 0]

    ax.plot(
        modeloutput["Incubation_time_hrs"],
        modeloutput["[N2O_44]_nM"],
        label="model output",
    )
    x = incubationdata["Incubation_time_hrs"]
    y = incubationdata["44N2O"]
    plot_interpolation(ax, x, y)

    ax.set_xlabel("Incubation time (hrs)")
    ax.set_ylabel(r"$^{44}N_2O$ (nM)")
    ax.legend()

    ax = axes[0, 1]

    ax.plot(
        modeloutput["Incubation_time_hrs"],
        modeloutput["[N2O_46]_nM"],
        label="model output",
    )
    x = incubationdata["Incubation_time_hrs"]
    y = incubationdata["46N2O"]
    plot_interpolation(ax, x, y)

    ax.set_xlabel("Incubation time (hrs)")
    ax.set_ylabel(r"$^{46}N_2O$ (nM)")

    ax = axes[1, 0]

    ax.plot(
        modeloutput["Incubation_time_hrs"],
        modeloutput["[N2O_45a]_nM"],
        label="model output",
    )
    x = incubationdata["Incubation_time_hrs"]
    y = incubationdata["45N2Oa"]
    plot_interpolation(ax, x, y)

    ax.set_xlabel("Incubation time (hrs)")
    ax.set_ylabel(r"$^{45}N_2O^{\alpha}$ (nM)")

    ax = axes[1, 1]

    ax.plot(
        modeloutput["Incubation_time_hrs"],
        modeloutput["[N2O_45b]_nM"],
        label="model output",
    )
    x = incubationdata["Incubation_time_hrs"]
    y = incubationdata["45N2Ob"]
    plot_interpolation(ax, x, y)

    ax.set_xlabel("Incubation time (hrs)")
    ax.set_ylabel(r"$^{45}N_2O^{\beta}$ (nM)")

    fig.suptitle("PS2 SCM 15NO2-")

    plt.tight_layout()

    plt.savefig(filename)
