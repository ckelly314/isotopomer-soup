"""
File:  convert_delta.py
------------------

Convert concentration and d15N into concentrations of 15N and 14N
as well as atom fraction.
"""

def convert_delta(concentration, d15N):
    
    '''
    INPUTS:
    d = delta value
    i = isotope ("d15N" or "d18O") - to determine standard
    
    OUTPUT:
    R = 15/14 ratio
    af = atom fraction = R/(1 + R)
    '''
    
    R15std = 0.00367647 # air N2
    R18std = 0.00200517 # VSMOW
    
    R = ((d15N/1000)+1)*R15std
    
    af = R/(1+R)
    
    n15 = concentration*af
    n14 = n15/R
    
    return n14, n15, af
