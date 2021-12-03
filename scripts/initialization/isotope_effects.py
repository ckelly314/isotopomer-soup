"""
isotope_effects.py
------------------

Define isotope effects to be used in the model.
"""


class IsotopeEffects:
    """
    Define isotope effects to be used in the model.

    Contains:
    alpha15NH4TON2Oa = isotope effect on 45N2O-alpha for nitrification by AOA
            Citation: Santoro et al., 2011 (adjusted based on δ15NH4+ value)
    alpha15NH4TON2Ob = isotope effect on 45N2O-beta for nitrification by AOA
            Citation: Santoro et al., 2011 (adjusted based on δ15NH4+ value)
    alpha15NH4TON2O46 = isotope effect on 46N2O-alpha for nitrification by AOA
            Citation: average of alpha15NH4TON2Oa & alpha15NH4TON2Ob

    alpha15NOxTON2Oa = isotope effect on 45N2O-alpha for denitrification from nitrite or nitrate
            Citation: Toyoda et al., 2005
    alpha15NOxTON2Ob = isotope effect on 45N2O-beta for denitrification from nitrite or nitrate
            Citation: Toyoda et al., 2005
    alpha15NOxTON2O46 = isotope effect on 46N2O for denitrification from nitrite or nitrate
            Citation: average of alpha15NH4TON2Oa & alpha15NH4TON2Ob

    alpha15NH4TONO2 = isotope effect for ammonia oxidation to nitrite
            Citation: Santoro and Casciotti, 2011
    alpha15NO2TONO3 = (inverse!) isotope effect for nitrite oxidation to nitrate
            Citation: Casciotti, 2009
    alpha15NO3TONO2 = isotope effect for nitrate reduction to nitrite
            Citation: Granger et al., 2004

    alpha15N2OatoN2 = isotope effect on 45N2O-alpha for N2O consumption
            Citation: Kelly et al., 2021
    alpha15N2ObtoN2 = isotope effect on 45N2O-alpha for N2O consumption
            Citation: Kelly et al., 2021
    alpha46N2OtoN2 = isotope effect on 46N2O for N2O consumption
            Citation: assume this is the same as the alpha effect
    """

    def __init__(self):

        # Isotope effects, translated into fractionation factors
        self.alpha15NH4TON2Oa = (
            -21.3 / 1000 + 1
        )  # AOA, Santoro et al., 2011 (adjusted based on δ15NH4+ value)
        self.alpha15NH4TON2Ob = (
            9.0 / 1000 + 1
        )  # AOA, Santoro et al., 2011 (adjusted based on δ15NH4+ value)
        self.alpha15NH4TON2O46 = (self.alpha15NH4TON2Oa + self.alpha15NH4TON2Ob) / 2

        self.alpha15NOxTON2Oa = 22.0 / 1000.0 + 1  # Toyoda et al., 2005
        self.alpha15NOxTON2Ob = 22.0 / 1000.0 + 1  # Toyoda et al., 2005
        self.alpha15NOxTON2O46 = 22.0 / 1000.0 + 1  # Toyoda et al., 2005

        self.alpha15NH4TONO2 = 22.0 / 1000 + 1  # AOA, Santoro and Casciotti, 2011
        self.alpha15NO2TONO3 = -15.0 / 1000 + 1  # Casciotti, 2009
        self.alpha15NO3TONO2 = 5.0 / 1000 + 1  # Granger et al., 2004

        self.alpha15N2OatoN2 = 11.8 / 1000.0 + 1  # Kelly et al., 2021
        self.alpha15N2ObtoN2 = 0.0 / 1000.0 + 1  # Kelly et al., 2021
        self.alpha46N2OtoN2 = (
            11.8 / 1000.0 + 1
        )  # assume this is the same as the alpha effect

    def __repr__(self):
        return f"Isotope effects initialized!"
