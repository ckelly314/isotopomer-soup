"""
bgc.py
------------------

Initialize substrate concentrations and rates of transformation.
"""

from .. import convert_delta
from .. import convert_af

from .metadata import metadata


class BioGeoChemistry:
    """
    Define initial parameters to be used in the model.

    Inputs:
    key = which experiment to reference:
    "PS1Surface", "PS1Top of oxycline", "PS1Mid-oxycline", "PS1Interface", "PS1SCM",
    "PS2Top of oxycline", "PS2PNM", "PS2Interface", "PS2SCM", "PS2SNM",
    "PS2Deep ODZ core", "PS2Base of ODZ", [...]
    tracer = "NH4+", "NO2-", or "NO3-"

    Outputs:
    BioGeoChemistry() = object containing initial substrate concnetrations
    and rates.
    """

    def __init__(self, key, tracer):

        ### LOAD EXPERIMENTAL METADATA ###
        self.key = key
        data = metadata(self.key)

        ### LOCATION IN THE WATER COLUMN ###
        self.depth = data.depth  # meters
        self.sigma_theta = data.sigma_theta  # kg/m3
        self.station = (
            data.station
        )  # "PS1" = offshore, "PS2" = center of ODZ, "PS3" = coastal
        self.feature = (
            data.feature
        )  # descriptive name of the target water column feature

        ### REAL-TIME NUTRIENT DATA ###

        self.NH4_ambient = data.NH4_ambient  # nmol/L
        self.NO2_ambient = data.NO2_ambient  # nmol/L
        self.NO3_ambient = data.NO3_ambient  # nmol/L

        self.d15NH4_ambient = 7.0  # per mil, assumed
        self.d15NO2_ambient = data.d15NO2_ambient  # per mil, PS2 sigma-theta=26.27
        self.d15NO3_ambient = data.d15NO3_ambient  # per mil, PS2 sigma-theta=26.27

        __, _, self.afNH4_ambient = convert_delta(self.NH4_ambient, self.d15NH4_ambient)
        __, _, self.afNO2_ambient = convert_delta(self.NO2_ambient, self.d15NO2_ambient)
        __, _, self.afNO3_ambient = convert_delta(self.NO3_ambient, self.d15NO3_ambient)

        ### SPIKE & CARRIER INJECTIONS ###

        self.NH4_carrier = 0.50 * 1000  # nmol/L; these are
        self.NO2_carrier = 1.00 * 1000  # nmol/L
        self.NO3_carrier = 0.0  # nmol/L

        self.R15std = 0.00367647  # air N2
        self.af_carrier = self.R15std / (1 + self.R15std)

        self.NH4_spike = 0.50 * 1000  # nmol/L
        self.NO2_spike = 4.80 * 1000  # nmol/L
        self.NO3_spike = 1.00 * 1000  # nmol/L

        self.af_spike = 0.99999999
        _, self.d15N_spike = convert_af(self.af_spike)

        ### ISOTOPE MIXING ###

        if tracer == "NH4+":

            self.NO2_init = self.NO2_ambient + self.NO2_carrier  # nmol/L
            self.AFNO2_init = (
                self.afNO2_ambient * self.NO2_ambient
                + self.af_carrier * self.NO2_carrier
            ) / self.NO2_init
            _, self.d15NO2_init = convert_af(self.AFNO2_init)

            self.NH4_init = self.NH4_ambient + self.NH4_spike  # nmol/L
            self.AFNH4_init = (
                self.afNH4_ambient * self.NH4_ambient + self.af_spike * self.NH4_spike
            ) / self.NH4_init
            _, self.d15NH4_init = convert_af(self.AFNH4_init)

            self.NO3_init = self.NO3_ambient + self.NO3_carrier  # nmol/L
            self.AFNO3_init = (
                self.afNO3_ambient * self.NO3_ambient
                + self.af_carrier * self.NO3_carrier
            ) / self.NO3_init
            _, self.d15NO3_init = convert_af(self.AFNO3_init)

        elif tracer == "NO2-":

            self.NO2_init = self.NO2_ambient + self.NO2_spike  # nmol/L
            self.AFNO2_init = (
                self.afNO2_ambient * self.NO2_ambient + self.af_spike * self.NO2_spike
            ) / self.NO2_init
            _, self.d15NO2_init = convert_af(self.AFNO2_init)

            self.NH4_init = self.NH4_ambient + self.NH4_carrier  # nmol/L
            self.AFNH4_init = (
                self.afNH4_ambient * self.NH4_ambient
                + self.af_carrier * self.NH4_carrier
            ) / self.NH4_init
            _, self.d15NH4_init = convert_af(self.AFNH4_init)

            self.NO3_init = self.NO3_ambient + self.NO3_carrier  # nmol/L
            self.AFNO3_init = (
                self.afNO3_ambient * self.NO3_ambient
                + self.af_carrier * self.NO3_carrier
            ) / self.NO3_init
            _, self.d15NO3_init = convert_af(self.AFNO3_init)

        elif tracer == "NO3-":

            self.NO2_init = self.NO2_ambient + self.NO2_carrier  # nmol/L
            self.AFNO2_init = (
                self.afNO2_ambient * self.NO2_ambient
                + self.af_carrier * self.NO2_carrier
            ) / self.NO2_init
            _, self.d15NO2_init = convert_af(self.AFNO2_init)

            self.NH4_init = self.NH4_ambient + self.NH4_carrier  # nmol/L
            self.AFNH4_init = (
                self.afNH4_ambient * self.NH4_ambient
                + self.af_carrier * self.NH4_carrier
            ) / self.NH4_init
            _, self.d15NH4_init = convert_af(self.AFNH4_init)

            self.NO3_init = self.NO3_ambient + self.NO3_spike  # nmol/L
            self.AFNO3_init = (
                self.afNO3_ambient * self.NO3_ambient + self.af_spike * self.NO3_spike
            ) / self.NO3_init
            _, self.d15NO3_init = convert_af(self.AFNO3_init)

        else:
            print("please enter a valid value for tracer kwarg")

        ### SUBSTRATE 14N & 15N POOLS CALCULATED FROM ISOTOPE MIXING ###

        self.nh4_14_i, self.nh4_15_i, _ = convert_delta(
            concentration=self.NH4_init, d15N=self.d15NH4_init
        )
        self.no2_14_i, self.no2_15_i, _ = convert_delta(
            concentration=self.NO2_init, d15N=self.d15NO2_init
        )
        self.no3_14_i, self.no3_15_i, _ = convert_delta(
            concentration=self.NO3_init, d15N=self.d15NO3_init
        )

        ### RATE CONSTANTS ###

        ### SUBSTRATE EXCHANGE ###

        try:
            self.kNH4TONO2 = data.kNH4TONO2 / (
                self.NH4_ambient + self.NH4_spike
            )  # convert rate in nM/day to 1st-order rate constant
            self.kNO2TONO3 = data.kNO2TONO3 / (self.NO2_ambient + self.NO2_spike)
            self.kNO3TONO2 = data.kNO3TONO2 / (self.NO3_ambient + self.NO3_spike)
        except TypeError:
            print("Rate data missing; unable to calculate rate constants")
            self.kNH4TONO2 = data.kNH4TONO2
            self.kNO2TONO3 = data.kNO2TONO3
            self.kNO3TONO2 = data.kNO3TONO2

        ### N2O CONSUMPTION ###

        self.kN2OCONS = data.kN2OCONS  # /day

    def __repr__(self):

        return f"BioGeoChemistry for {self.key} initialized!"


if __name__ == "__main__":
    print(BioGeoChemistry())
