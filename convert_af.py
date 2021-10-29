"""
File:  convert_af.py
------------------

Convert atom fraction into 15R/14R ratio and d15N.
"""

def convert_af(af):
    R15std = 0.00367647 # air N2
    
    R = 1./(1/af -1)
    
    d15N = (R/R15std - 1)*1000
    
    return R, d15N