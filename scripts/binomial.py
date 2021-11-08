"""
File:  binomial.py
------------------

Probabilities of formation of different isotopic species of N2O
based on binomial probability tree.
"""


def binomial(af1, af2):

    p1 = af1 * af2
    p2 = af1 * (1 - af2)
    p3 = (1 - af1) * af2
    p4 = (1 - af1) * (1 - af2)

    return p1, p2, p3, p4
