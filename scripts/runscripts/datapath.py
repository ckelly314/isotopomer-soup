"""
File: datapath.py
-----------------

Define paths to data files.
"""
import os


def datapath():

    # path for Sherlock: "/home/users/clkelly/isotopomer-soup/scripts/Data/"
    #return "/Users/colette/Google Drive/My Drive/PhD Research/ETNP 2018/Data/isotopomer-soup/scripts/Data/"  
    #return "/home/users/clkelly/isotopomer-soup/scripts/Data/" 

    return f"{os.getcwd()}/scripts/Data/"
