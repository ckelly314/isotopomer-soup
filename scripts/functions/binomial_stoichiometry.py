"""
File: binomial_stoichiometry.py
-------------------------------

Probabilities of formation of different isotopic species of N2O
based on binomial probability tree, taking the stoichiometry of
NO+NH2OH into account:
2NH2OH + 4NO -> 3N2O + 3H2O
"""

import numpy as np


def binomial_stoichiometry(afNO, afNH2OH):
    """
    Compute binomial probabilities of producing each isotopomer
    of N2O based on the atom fractions of two substrates.

    Inputs:
    afNO = float or numpy array containing atom fraction(s) of
    nitric oxide NO, which feeds into the alpha position
    afNH2OH = float or numpy array containing atom fraction(s) of
    hydroxylamine NH2OH, which feeds into the beta position

    NOTE: afNO = afNH2OH if both nitrogens are being drawn from the same substrate

    Outputs:
    p46 = float or numpy array containing probabilit(ies) of forming 46N2O
    p45a = float or numpy array containing probabilit(ies) of forming 45N2Oa
    p45b = float or numpy array containing probabilit(ies) of forming 45N2Ob
    p44 = float or numpy array containing probabilit(ies) of forming 44N2O
    """

    p46 = 1.0 / 3 * afNO ** 2 + 2.0 / 3 * afNO * afNH2OH
    p45a = 2.0 / 3 * afNO * (1 - afNH2OH) + 1.0 / 3 * afNO * (1 - afNO)
    p45b = 2.0 / 3 * (1 - afNO) * afNH2OH + 1.0 / 3 * afNO * (1 - afNO)
    p44 = 1.0 / 3 * ((1 - afNO) ** 2) + 2.0 / 3 * (1 - afNO) * (1 - afNH2OH)

    return p46, p45a, p45b, p44


if __name__ == "__main__":
    print(sum(binomial_stoichiometry(0.99, 0.3)))
