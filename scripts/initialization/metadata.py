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
        kNH4TONO2=0.0,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.542931378,  # nmol/L/day
        # kN2OCONS=0.079,  # /day, no O2 correction
        kN2OCONS=0.0,  # /day, corrected for O2
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
        kNH4TONO2=0.0,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        # kN2OCONS=0.024,  # /day, no O2 correction
        kN2OCONS=0.0,  # /day, corrected for O2
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
        kNH4TONO2=0.524855743,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        # kN2OCONS=0.024,  # /day, no O2 correction
        kN2OCONS=0.0,  # /day, corrected for O2
    )

    datadict["PS1Interface"] = experiment(
        depth=100.113,  # meters
        sigma_theta=26.1163,  # kg/m3
        station="PS1",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Interface",  # oxic-anoxic interface
        NH4_ambient=3.7,  # nmol/L
        NO2_ambient=0.01 * 1000,  # nmol/L
        NO3_ambient=29.56 * 1000,  # nmol/L
        d15NO2_ambient=0.0,  # per mil, NO PS1 DATA
        d15NO3_ambient=7.79,  # per mil
        kNH4TONO2=0.192410197,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        # kN2OCONS=0.019,  # /day, no O2 correction
        kN2OCONS=0.019233554,  # /day, corrected for O2
    )

    datadict["PS1SCM"] = experiment(
        depth=120.824,  # meters
        sigma_theta=26.2633,  # kg/m3
        station="PS1",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="SCM",  # Secondary (deep) chlorophyll maximum
        NH4_ambient=2.14,  # nmol/L
        NO2_ambient=0.02 * 1000,  # nmol/L
        NO3_ambient=31.13 * 1000,  # nmol/L
        d15NO2_ambient=0.0,  # per mil, NO PS1 DATA
        d15NO3_ambient=7.46,  # per mil
        kNH4TONO2=0.453745664,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        # kN2OCONS=0.0,  # /day, no O2 correction
        kN2OCONS=0.0,  # /day, corrected for O2
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
        d15NO3_ambient=5.35,  # per mil
        kNH4TONO2=0.054284951,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        # kN2OCONS=0.031,  # /day, no O2 correction
        kN2OCONS=0.0,  # /day, corrected for O2
    )

    datadict["PS2PNM"] = experiment(
        depth=75.152,  # meters
        sigma_theta=24.4554,  # kg/m3
        station="PS2",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="PNM",  # primary nitrite maximum
        NH4_ambient=12.2,  # nmol/L
        NO2_ambient=0.13 * 1000,  # nmol/L
        NO3_ambient=19.73 * 1000,  # nmol/L
        d15NO2_ambient=-2.01,  # per mil, PS2 PNM, sigma-theta=24.11
        d15NO3_ambient=10.06,  # per mil
        kNH4TONO2=1.394599328,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        # kN2OCONS=0.042,  # /day, no O2 correction
        kN2OCONS=0.0,  # /day, corrected for O2
    )

    datadict["PS2Interface"] = experiment(
        depth=92.279,  # meters
        sigma_theta=25.4618,  # kg/m3
        station="PS2",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Interface",  # oxic-anoxic interface
        NH4_ambient=13.7,  # nmol/L
        NO2_ambient=0.06 * 1000,  # nmol/L
        NO3_ambient=25.63 * 1000,  # nmol/L
        d15NO2_ambient=-2.01,  # per mil, PNM value
        d15NO3_ambient=10.18,  # per mil
        kNH4TONO2=2.209999378,  # nmol/L/day
        kNO2TONO3=27.01023342,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        # kN2OCONS=0.019,  # /day, no O2 correction
        kN2OCONS=0.0,  # /day, corrected for O2
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
        d15NO3_ambient=12.80,  # per mil
        kNH4TONO2=0.0,  # nmol/L/day
        kNO2TONO3=81.00040564,  # nmol/L/day
        kNO3TONO2=24.32319863,  # nmol/L/day
        # kN2OCONS=0.056,  # /day, no O2 correction
        kN2OCONS=0.056356302,  # /day, corrected for O2
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
        # kN2OCONS=0.065,  # /day, no O2 correction
        kN2OCONS=0.065454872,  # /day, corrected for O2
    )

    datadict["PS2Deep ODZ core"] = experiment(
        depth=600.767,  # meters
        sigma_theta=27.0395,  # kg/m3
        station="PS2",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Deep ODZ core",  # deep ODZ
        NH4_ambient=4.76,  # nmol/L
        NO2_ambient=0.0 * 1000,  # nmol/L
        NO3_ambient=35.16 * 1000,  # nmol/L
        d15NO2_ambient=-19.68,  # per mil, SNM value
        d15NO3_ambient=12.33,  # per mil
        kNH4TONO2=0.0,  # nmol/L/day
        kNO2TONO3=13.05188381,  # nmol/L/day
        kNO3TONO2=33.24400098,  # nmol/L/day
        # kN2OCONS=0.025,  # /day, no O2 correction
        kN2OCONS=0.024690915,  # /day, corrected for O2
    )

    datadict["PS2Base of ODZ"] = experiment(
        depth=800.883,  # meters
        sigma_theta=27.242,  # kg/m3
        station="PS2",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Base of ODZ",  # inflection point where oxygen starts to increase again
        NH4_ambient=2.615,  # nmol/L
        NO2_ambient=0.0 * 1000,  # nmol/L
        NO3_ambient=42.58 * 1000,  # nmol/L
        d15NO2_ambient=-19.68,  # per mil, SNM value
        d15NO3_ambient=8.86,  # per mil
        kNH4TONO2=0.514303603,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        # kN2OCONS=0.075,  # /day, no O2 correction
        kN2OCONS=0.074883646,  # /day, corrected for O2
    )

    datadict["PS2Deep oxycline"] = experiment(
        depth=1001.209,  # meters
        sigma_theta=27.3598,  # kg/m3
        station="PS2",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Deep oxycline",  # within the oxycline below the ODZ
        NH4_ambient=1.615,  # nmol/L
        NO2_ambient=0.0 * 1000,  # nmol/L
        NO3_ambient=44.66 * 1000,  # nmol/L
        d15NO2_ambient=-19.68,  # per mil, SNM value
        d15NO3_ambient=7.72,  # per mil
        kNH4TONO2=0.265294945,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        # kN2OCONS=0.075,  # /day, no O2 correction
        kN2OCONS=0.0,  # /day, corrected for O2
    )

    datadict["PS3Top of oxycline"] = experiment(
        depth=14.595,  # meters
        sigma_theta=23.0983,  # kg/m3
        station="PS3",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Top of oxycline",  # within the oxycline below the ODZ
        NH4_ambient=399.62,  # nmol/L
        NO2_ambient=0.4 * 1000,  # nmol/L
        NO3_ambient=0.33 * 1000,  # nmol/L
        d15NO2_ambient=-1.25,  # per mil, PNM value
        d15NO3_ambient=14.37,  # per mil
        kNH4TONO2=0.0,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        # kN2OCONS=0.043,  # /day, no O2 correction
        kN2OCONS=0.0,  # /day, corrected for O2
    )

    datadict["PS3Mid-oxycline"] = experiment(
        depth=24.74,  # meters
        sigma_theta=24.0276,  # kg/m3
        station="PS3",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Mid-oxycline",  # mixed layer
        NH4_ambient=12.39,  # nmol/L
        NO2_ambient=0.33 * 1000,  # nmol/L
        NO3_ambient=8.03 * 1000,  # nmol/L
        d15NO2_ambient=-1.25,  # per mil
        d15NO3_ambient=13.13,  # per mil
        kNH4TONO2=0.0,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        # kN2OCONS=0.048,  # /day, no O2 correction
        kN2OCONS=0.0,  # /day, corrected for O2
    )

    datadict["PS3Interface"] = experiment(
        depth=34.856,  # meters
        sigma_theta=25.0034,  # kg/m3
        station="PS3",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Interface",  # mixed layer
        NH4_ambient=9.31,  # nmol/L
        NO2_ambient=0.26 * 1000,  # nmol/L
        NO3_ambient=18.81 * 1000,  # nmol/L
        d15NO2_ambient=1.55,  # per mil
        d15NO3_ambient=9.61,  # per mil
        kNH4TONO2=0.87647943,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        # kN2OCONS=0.0,  # /day, no O2 correction
        kN2OCONS=0.0,  # /day, corrected for O2
    )

    datadict["PS3Interface2"] = experiment(
        depth=62.873,  # meters
        sigma_theta=25.4397,  # kg/m3
        station="PS3",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Interface2",  # mixed layer
        NH4_ambient=15.85,  # nmol/L
        NO2_ambient=0.6 * 1000,  # nmol/L
        NO3_ambient=23.47 * 1000,  # nmol/L
        d15NO2_ambient=-18.82,  # per mil
        d15NO3_ambient=9.88,  # per mil
        kNH4TONO2=4.678976829,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        # kN2OCONS=0.050,  # /day, no O2 correction
        kN2OCONS=0.050236324,  # /day, corrected for O2
    )

    datadict["PS3SCM"] = experiment(
        depth=66.496,  # meters
        sigma_theta=25.6229,  # kg/m3
        station="PS3",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="SCM",  # mixed layer
        NH4_ambient=15.85,  # nmol/L
        NO2_ambient=0.6 * 1000,  # nmol/L
        NO3_ambient=22.83 * 1000,  # nmol/L
        d15NO2_ambient=-18.82,  # per mil
        d15NO3_ambient=9.79,  # per mil
        kNH4TONO2=0.574729614,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=19.20078995,  # nmol/L/day
        # kN2OCONS=0.050,  # /day, no O2 correction
        kN2OCONS=0.050236324,  # /day, corrected for O2
    )

    datadict["PS3SNM"] = experiment(
        depth=181.738,  # meters
        sigma_theta=26.3429,  # kg/m3
        station="PS3",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="SNM",  # mixed layer
        NH4_ambient=4.18,  # nmol/L
        NO2_ambient=2.67 * 1000,  # nmol/L
        NO3_ambient=21.88 * 1000,  # nmol/L
        d15NO2_ambient=-22.47,  # per mil
        d15NO3_ambient=15.88,  # per mil
        kNH4TONO2=0.0,  # nmol/L/day
        kNO2TONO3=465.3351641,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        # kN2OCONS=0.0,  # /day, no O2 correction
        kN2OCONS=0.0,  # /day, corrected for O2
    )

    datadict["PS3Deep ODZ core"] = experiment(
        depth=600.35,  # meters
        sigma_theta=27.0482,  # kg/m3
        station="PS3",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Deep ODZ core",  # mixed layer
        NH4_ambient=5.26,  # nmol/L
        NO2_ambient=0.28 * 1000,  # nmol/L
        NO3_ambient=42.55 * 1000,  # nmol/L
        d15NO2_ambient=-22.47,  # per mil, SNM value
        d15NO3_ambient=10.38,  # per mil
        kNH4TONO2=0.0,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=10.88213623,  # nmol/L/day
        # kN2OCONS=0.0,  # /day, no O2 correction
        kN2OCONS=0.0,  # /day, corrected for O2
    )

    datadict["PS3Deep oxycline"] = experiment(
        depth=898.247,  # meters
        sigma_theta=27.3044,  # kg/m3
        station="PS3",  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        feature="Deep oxycline",  # mixed layer
        NH4_ambient=9,  # nmol/L
        NO2_ambient=0 * 1000,  # nmol/L
        NO3_ambient=46.23 * 1000,  # nmol/L
        d15NO2_ambient=-22.47,  # per mil, SNM value
        d15NO3_ambient=8.70,  # per mil
        kNH4TONO2=0.302506387,  # nmol/L/day
        kNO2TONO3=0.0,  # nmol/L/day
        kNO3TONO2=0.0,  # nmol/L/day
        # kN2OCONS=0.0,  # /day, no O2 correction
        kN2OCONS=0.0,  # /day, corrected for O2
    )

    return datadict[key]
