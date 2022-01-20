"""
File: metadata.py
-----------------

Giant dictionary containing relevant metadata for all N2O experiments.
"""

from collections import namedtuple


def metadata(key):
    """
    Define ambient NH4, NO2, and NO3 concentrations and d15N;
    define rates of nitrification, nitrite oxidation, and nitrate reduction.

    Inputs:
    key = which experiment to reference:
    "PS1Surface", "PS1Top of oxycline", "PS1Mid-oxycline", "PS1Interface", "PS1SCM",
    "PS2Top of oxycline", "PS2PNM", "PS2Interface", "PS2SCM", "PS2SNM",
    "PS2Deep ODZ core", "PS2Base of ODZ", [...]

    Outputs:
    datadict = dictionary containing metadata for that experiment.
    """

    # access values using descriptive field names instead of integer indices
    experiment = namedtuple(
        "experiment",
        [
            "depth",  # meters, depth measured by CTD where incubation samples were collected
            "sigma_theta",  # kg/m3, neutral density measured by CTD
            "station",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
            "feature",  # descriptive name of the target water column feature
            "NH4_ambient",  # nmol/L, source: shipboard nutrient concentrations
            "NO2_ambient",  # nmol/L, source: shipboard nutrient concentrations
            "NO3_ambient",  # nmol/L, source: Kelly et al. (2021), data: https://www.bco-dmo.org/dataset/832995
            "d15NO2_ambient",  # per mil, source: Kelly et al. (2021), data: https://www.bco-dmo.org/dataset/832995
            "d15NO3_ambient",  # per mil, source: Kelly et al. (2021), data: https://www.bco-dmo.org/dataset/832995
            "kNH4TONO2",  # nmol/L/day, source: nitrification rate in 15NH4+ experiment
            "kNO2TONO3",  # nmol/L/day, source: nitrite oxidation rate in 15NO2- experiment
            "kNO3TONO2",  # nmol/L/day, source: nitrate reduction rate in 15NO3- experiment
            "kN2OCONS",  # /day, source: Sun et al. (2020), "Microbial N2O consumption in and above marine N2O production hotspots"
        ],
    )

    datadict = {}  # use dict because quick access to data items is important

    # key/value pairs are experiment names (strings) and "experiment" namedtuples
    datadict["PS1Surface"] = experiment(
        depth=30.65,  # meters
        sigma_theta=21.473,  # kg/m3
        station="PS1",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Surface",  # mixed layer
        NH4_ambient=0.0,  # nmol/L
        NO2_ambient=0.02 * 1000,  # nmol/L
        NO3_ambient=0.10 * 1000,  # nmol/L
        d15NO2_ambient=0.0,  # per mil, NO PS1 DATA
        d15NO3_ambient=4.27,  # per mil
        kNH4TONO2=None,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=None,  # nmol/L/day
        kN2OCONS=0.079,  # /day
    )

    datadict["PS1Top of oxycline"] = experiment(
        depth=49.855,  # meters
        sigma_theta=21.602,  # kg/m3
        station="PS1",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Top of oxycline",  # inflection point where oxygen starts to decline
        NH4_ambient=89.79,  # nmol/L
        NO2_ambient=0.74 * 1000,  # nmol/L
        NO3_ambient=0.09 * 1000,  # nmol/L
        d15NO2_ambient=0.0,  # per mil, NO PS1 DATA
        d15NO3_ambient=4.44,  # per mil
        kNH4TONO2=None,  # nmol/L/day
        kNO2TONO3=77.79,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        kN2OCONS=0.024,  # /day
    )

    datadict["PS1Mid-oxycline"] = experiment(
        depth=60.017,  # meters
        sigma_theta=23.4607,  # kg/m3
        station="PS1",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Mid-oxycline",  # oxycline mid-point
        NH4_ambient=8.75,  # nmol/L
        NO2_ambient=1.065 * 1000,  # nmol/L
        NO3_ambient=8.35 * 1000,  # nmol/L
        d15NO2_ambient=0.0,  # per mil, NO PS1 DATA
        d15NO3_ambient=11.43,  # per mil
        kNH4TONO2=0.519953713,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        kN2OCONS=0.024,  # /day
    )

    datadict["PS1Interface"] = experiment(
        depth=100.113,  # meters
        sigma_theta=26.1163,  # kg/m3
        station="PS1",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Interface",  # oxic-anoxic interface
        NH4_ambient=3.7,  # nmol/L
        NO2_ambient=0.01 * 1000,  # nmol/L
        NO3_ambient=28.29 * 1000,  # nmol/L
        d15NO2_ambient=0.0,  # per mil, NO PS1 DATA
        d15NO3_ambient=7.73,  # per mil
        kNH4TONO2=0.192451418,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=None,  # nmol/L/day
        kN2OCONS=0.019,  # /day
    )

    datadict["PS1SCM"] = experiment(
        depth=120.824,  # meters
        sigma_theta=26.2633,  # kg/m3
        station="PS1",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="SCM",  # Secondary (deep) chlorophyll maximum
        NH4_ambient=2.14,  # nmol/L
        NO2_ambient=0.02 * 1000,  # nmol/L
        NO3_ambient=29.56 * 1000,  # nmol/L
        d15NO2_ambient=0.0,  # per mil, NO PS1 DATA
        d15NO3_ambient=7.79,  # per mil
        kNH4TONO2=0.432715909,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=24.8941754,  # nmol/L/day
        kN2OCONS=0.0,  # /day
    )

    datadict["PS2Top of oxycline"] = experiment(
        depth=54.777,  # meters
        sigma_theta=23.2412,  # kg/m3
        station="PS2",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Top of oxycline",  # inflection point where oxygen starts to decline
        NH4_ambient=34.8,  # nmol/L
        NO2_ambient=0.01 * 1000,  # nmol/L
        NO3_ambient=0.58 * 1000,  # nmol/L
        d15NO2_ambient=-0.25,  # per mil, PS2 PNM, sigma-theta=24.11
        d15NO3_ambient=11.77,  # per mil
        kNH4TONO2=None,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        kN2OCONS=0.031,  # /day
    )

    datadict["PS2PNM"] = experiment(
        depth=75.152,  # meters
        sigma_theta=24.4554,  # kg/m3
        station="PS2",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="PNM",  # primary nitrite maximum
        NH4_ambient=12.2,  # nmol/L
        NO2_ambient=0.13 * 1000,  # nmol/L
        NO3_ambient=19.73 * 1000,  # nmol/L
        d15NO2_ambient=-0.25,  # per mil, PS2 PNM, sigma-theta=24.11
        d15NO3_ambient=10.98,  # per mil
        kNH4TONO2=1.348781554,  # nmol/L/day
        kNO2TONO3=11.35684936,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        kN2OCONS=0.042,  # /day
    )

    datadict["PS2Interface"] = experiment(
        depth=92.279,  # meters
        sigma_theta=25.4618,  # kg/m3
        station="PS2",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Interface",  # oxic-anoxic interface
        NH4_ambient=13.7,  # nmol/L
        NO2_ambient=0.06 * 1000,  # nmol/L
        NO3_ambient=25.63 * 1000,  # nmol/L
        d15NO2_ambient=-21.72,  # per mil, PS2 SNM, sigma-theta=26.34
        d15NO3_ambient=10.18,  # per mil
        kNH4TONO2=2.700574986,  # nmol/L/day
        kNO2TONO3=27.60796281,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        kN2OCONS=0.019,  # /day
    )

    datadict["PS2SCM"] = experiment(
        depth=119.368,  # meters
        sigma_theta=26.0997,  # kg/m3
        station="PS2",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="SCM",  # secondary (deep) chlorophyll maximum
        NH4_ambient=50.0,  # nmol/L
        NO2_ambient=0.02789 * 1000,  # nmol/L
        NO3_ambient=26.48 * 1000,  # nmol/L
        d15NO2_ambient=-22.82,  # per mil
        d15NO3_ambient=15.25,  # per mil
        kNH4TONO2=0.0,  # nmol/L/day
        kNO2TONO3=73.23197829,  # nmol/L/day
        kNO3TONO2=25.75670779,  # nmol/L/day
        kN2OCONS=0.056,  # /day
    )

    datadict["PS2SNM"] = experiment(
        depth=253.247,  # meters
        sigma_theta=26.5088,  # kg/m3
        station="PS2",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="SNM",  # secondary nitrite maximum
        NH4_ambient=3.86,  # nmol/L
        NO2_ambient=1.74 * 1000,  # nmol/L
        NO3_ambient=24.52 * 1000,  # nmol/L
        d15NO2_ambient=-19.68,  # per mil
        d15NO3_ambient=19.74,  # per mil
        kNH4TONO2=0.0,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        kN2OCONS=0.065,  # /day
    )

    datadict["PS2Deep ODZ core"] = experiment(
        depth=600.767,  # meters
        sigma_theta=27.0395,  # kg/m3
        station="PS2",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Deep ODZ core",  # deep ODZ
        NH4_ambient=4.76,  # nmol/L
        NO2_ambient=0.0 * 1000,  # nmol/L
        NO3_ambient=35.16 * 1000,  # nmol/L
        d15NO2_ambient=-19.68,  # per mil, PS2 SNM, sigma-theta=26.509
        d15NO3_ambient=12.33,  # per mil
        kNH4TONO2=0.0,  # nmol/L/day
        kNO2TONO3=10.78305924,  # nmol/L/day NO DATA YET
        kNO3TONO2=41.69345556,  # nmol/L/day
        kN2OCONS=0.025,  # /day
    )

    datadict["PS2Base of ODZ"] = experiment(
        depth=800.883,  # meters
        sigma_theta=27.242,  # kg/m3
        station="PS2",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Base of ODZ",  # inflection point where oxygen starts to increase again
        NH4_ambient=2.615,  # nmol/L
        NO2_ambient=0.0 * 1000,  # nmol/L
        NO3_ambient=42.58 * 1000,  # nmol/L
        d15NO2_ambient=-19.68,  # per mil, PS2 SNM, sigma-theta=26.509
        d15NO3_ambient=8.86,  # per mil
        kNH4TONO2=0.462805244,  # nmol/L/day
        kNO2TONO3=272.8172186,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        kN2OCONS=0.075,  # /day
    )

    datadict["PS2Deep oxycline"] = experiment(
        depth=1001.209,  # meters
        sigma_theta=27.3598,  # kg/m3
        station="PS2",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Deep oxycline",  # within the oxycline below the ODZ
        NH4_ambient=1.615,  # nmol/L
        NO2_ambient=0.0 * 1000,  # nmol/L
        NO3_ambient=44.66 * 1000,  # nmol/L
        d15NO2_ambient=-19.68,  # per mil, PS2 SNM, sigma-theta=26.509
        d15NO3_ambient=7.72,  # per mil
        kNH4TONO2=0.205963228,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        kN2OCONS=0.075,  # /day
    )

    datadict["PS3Top of oxycline"] = experiment(
        depth=14.595,  # meters
        sigma_theta=23.0983,  # kg/m3
        station="PS3",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Top of oxycline",  # within the oxycline below the ODZ
        NH4_ambient=399.62,  # nmol/L
        NO2_ambient=0.4 * 1000,  # nmol/L
        NO3_ambient=9.48 * 1000,  # nmol/L
        d15NO2_ambient=-1.25,  # per mil, PS3 PNM, sigma-theta=24.0672
        d15NO3_ambient=14.37,  # per mil
        kNH4TONO2=0.0,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        kN2OCONS=0.043,  # /day
    )

    return datadict[key]
