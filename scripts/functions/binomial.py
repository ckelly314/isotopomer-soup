"""
File:  binomial.py
------------------

Probabilities of formation of different isotopic species of N2O
based on binomial probability tree.
"""


def binomial(af1, af2):
    """
    Compute binomial probabilities of producing each isotopomer
    of N2O based on the atom fractions of two substrates.

    Inputs:
    af1 = float or numpy array containing atom fraction(s) of
    substrate #1, where substrate #1 feeds into the alpha position
    af2 = float or numpy array containing atom fraction(s) of
    substrate #2, where substrate #2 feeds into the beta position

    NOTE: af1 = af2 if both nitrogens are being drawn from the same substrate

    Outputs:
    p1 = float or numpy array containing probabilit(ies) of forming 46N2O
    p2 = float or numpy array containing probabilit(ies) of forming 45N2Oa
    p3 = float or numpy array containing probabilit(ies) of forming 45N2Ob
    p4 = float or numpy array containing probabilit(ies) of forming 44N2O
    """

    p1 = af1 * af2
    p2 = af1 * (1 - af2)
    p3 = (1 - af1) * af2
    p4 = (1 - af1) * (1 - af2)

    return p1, p2, p3, p4


if __name__ == "__main__":
    print(sum(binomial(0.99, 0.003)))
