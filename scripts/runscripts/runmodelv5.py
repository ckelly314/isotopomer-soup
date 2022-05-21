import pandas as pd
import numpy as np
# use for nelder-mead optimization of a convex function
from scipy.optimize import minimize
from numpy.random import rand

from .datapath import datapath

from .. import *


def runmodelv5(station, feature):

    ### KEYWORDS ###
    ### KEYWORDS ###
    stn = station
    ft = feature
    bgckey = stn+ft

    ### INITIALIZATION ###

    gridded_dataNH4, bgcNH4, isos, trNH4, params = initialize(station=stn,
                                          feature=ft,
                                          tracer="NH4+")
    gridded_dataNO2, bgcNO2, isos, trNO2, params = initialize(station=stn,
                                          feature=ft,
                                          tracer="NO2-")
    gridded_dataNO3, bgcNO3, isos, trNO3, params = initialize(station=stn,
                                          feature=ft,
                                          tracer="NO3-")

    ### INITIAL GUESS FOR OPTIMIZATION ###
    guess = x0(station=stn, feature=ft, key=bgckey)

    [kestimateNH4, kestimateNO, kestimateNO2, kestimateNO3, kestimate_hybrid1,
     kestimate_hybrid2, kestimate_hybrid3, kestimate_hybrid4,
    kestimate_hybrid5, kestimate_hybrid6] = guess

    def objective(x): #, bgc, isos, tracers, modelparams):
        
        tracersNH4 = modelv5(x, bgcNH4, isos, trNH4, params)
        
        costNH4 = costfxn(trainingdata = gridded_dataNH4,
                    modeled_44 = tracersNH4.n2o_44,
                    modeled_45a = tracersNH4.n2o_45a,
                    modeled_45b = tracersNH4.n2o_45b,
                    modeled_46 = tracersNH4.n2o_46,
                    weights = np.array([1,1000,1000,1000]))
        
        tracersNO2 = modelv5(x, bgcNO2, isos, trNO2, params)
        
        costNO2 = costfxn(trainingdata = gridded_dataNO2,
                    modeled_44 = tracersNO2.n2o_44,
                    modeled_45a = tracersNO2.n2o_45a,
                    modeled_45b = tracersNO2.n2o_45b,
                    modeled_46 = tracersNO2.n2o_46,
                    weights = np.array([1,1000,1000,1000]))
        
        tracersNO3 = modelv5(x, bgcNO3, isos, trNO3, params)
        
        costNO3 = costfxn(trainingdata = gridded_dataNO3,
                    modeled_44 = tracersNO3.n2o_44,
                    modeled_45a = tracersNO3.n2o_45a,
                    modeled_45b = tracersNO3.n2o_45b,
                    modeled_46 = tracersNO3.n2o_46,
                    weights = np.array([1,1000,1000,1000]))
        
        cost = costNH4 + costNO2 + costNO3
        
        print(cost)
        
        return cost

    f = 0.5

    x = [kestimateNH4, kestimateNO2, kestimateNO3, kestimate_hybrid2, f] # for modelv5

    print(f"objective(x0) = {objective(x)}")

    xguess = x

    # define bounds: no negative rate constants, f between 0 and 1
    bnds = ((0, None), (0, None), (0, None), (0, None), (0, 1)) # for model v5   

    # perform the search with intelligently selected x0
    #result = minimize(objective, x, args = (bgc, isos, tr, modelparams), method='nelder-mead', bounds=bnds)
    # increasing option "fatol" from factory setting of 0.0001 to 0.1 reduces the amount of time to solve
    result = minimize(objective, x, method='nelder-mead', bounds=bnds)#, options={'maxfev' : 500, 'fatol': 0.1})
    # summarize the result
    print('Status : %s' % result['message'])
    print('Total Evaluations: %d' % result['nfev'])
    # evaluate solution
    solution = result['x']
    evaluation = objective(solution)#, bgc, isos, tr, params)
    print('Solution: f(%s) = %.5f' % (solution, evaluation))

    tracersNH4 = modelv5(result.x, bgcNH4, isos, trNH4, params)
    tracersNO2 = modelv5(result.x, bgcNO2, isos, trNO2, params)
    tracersNO3 = modelv5(result.x, bgcNO3, isos, trNO3, params)

    outputNH4 = postprocess(bgcNH4, isos, tracersNH4, result.x, model="modelv5")
    outputNO2 = postprocess(bgcNO2, isos, tracersNO2, result.x, model="modelv5")
    outputNO3 = postprocess(bgcNO3, isos, tracersNO3, result.x, model="modelv5")

    outputNH4.to_excel("scripts/data/outputNH4.xlsx")
    outputNO2.to_excel("scripts/data/outputNO2.xlsx")
    outputNO3.to_excel("scripts/data/outputNO3.xlsx")

    saveout = np.array([outputNH4[['nitrification', 'denitno2', 'denitno3', 'hybrid2']].mean(),
                outputNO2[['nitrification', 'denitno2', 'denitno3', 'hybrid2']].mean(),
                outputNO3[['nitrification', 'denitno2', 'denitno3', 'hybrid2']].mean()])

    saveout = saveout.mean(axis=0)

    saveout = pd.DataFrame([saveout]).rename(columns = {0:"Nitrification (nM/day)",
            1:"Denit from NO2- (nM/day)",
            2:"Denit from NO3- (nM/day)",
            3:"Hybrid2 (nM/day)"})

    saveout["Station"] = stn
    saveout["Feature"] = ft
    saveout["Key"] = bgckey
    saveout["cost"] = objective(result.x)
    saveout["f"] = result.x[4]
    saveout = saveout.set_index("Key")
    modeloutput = pd.read_excel("scripts/data/modelv5.xlsx",
                               index_col="Key")
    modeloutput = modeloutput.append(saveout)
    modeloutput = modeloutput.drop_duplicates()
    modeloutput.to_excel("scripts/data/modelv5.xlsx")

    inputdata=pd.read_csv(f'{datapath()}00_incubationdata.csv')

    scatter_plot(data=inputdata, station=stn, feature=ft, tracer="NH4+",
                 modeloutput=outputNH4, filename=f"Figures/modelv5/{stn}{ft}NH4+modelv5.pdf")

    scatter_plot(data=inputdata, station=stn, feature=ft, tracer="NO2-",
                 modeloutput=outputNO2, filename=f"Figures/modelv5/{stn}{ft}NO2-modelv5.pdf")

    scatter_plot(data=inputdata, station=stn, feature=ft, tracer="NO3-",
                 modeloutput=outputNO3, filename=f"Figures/modelv5/{stn}{ft}NO3-modelv5.pdf")
