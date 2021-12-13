"""
File: postprocess.py
--------------------

Calculate rates in nM/day from solved rate constants (x)
and modeled substrate concentrations.
"""

import pandas as pd
import numpy as np


def postprocess(bgc, isos, tracers, x, model):

    ### CALCULATE OUTPUT ###

    ### ISOTOPE CONSTANTS ###
    R15std = 0.00367647 # air N2
    R18std = 0.00200517 # VSMOW

    
    nh4_concentration = pd.DataFrame(tracers.nh4_14+tracers.nh4_15, columns={'[NH4+]_nM'})
    nh4_14 = pd.DataFrame(tracers.nh4_14, columns={'[14NH4+]_nM'})
    nh4_15 = pd.DataFrame(tracers.nh4_15, columns={'[15NH4+]_nM'})
    d15nh4 = pd.DataFrame((((tracers.nh4_15/(tracers.nh4_14))/R15std)-1)*1000, columns={'d15NH4+'})
    afnh4_df = pd.DataFrame(tracers.afnh4, columns={'AFNH4+'})

    nh2oh_concentration = pd.DataFrame(tracers.nh2oh_15+tracers.nh2oh_14, columns = {'[NH2OH]_nM'})
    nh2oh_14 = pd.DataFrame(tracers.nh2oh_14, columns = {'[14NH2OH]_nM'})
    nh2oh_15 = pd.DataFrame(tracers.nh2oh_15, columns = {'[15NH2OH]_nM'})

    no_concentration = pd.DataFrame(tracers.no_15+tracers.no_14, columns = {'[NO]_nM'})
    no_14 = pd.DataFrame(tracers.no_14, columns = {'[14NO]_nM'})
    no_15 = pd.DataFrame(tracers.no_15, columns = {'[15NO]_nM'})

    no2_concentration = pd.DataFrame(tracers.no2_14+tracers.no2_15, columns={'[NO2-]_nM'})
    no2_14 = pd.DataFrame(tracers.no2_14+tracers.no2_15, columns={'[14NO2-]_nM'})
    no2_15 = pd.DataFrame(tracers.no2_14+tracers.no2_15, columns={'[15NO2-]_nM'})
    d15no2 = pd.DataFrame((((tracers.no2_15/(tracers.no2_14))/R15std)-1)*1000, columns={'d15NO2-'})
    afno2_df = pd.DataFrame(tracers.afno2, columns={'AFNO2-'})

    no3_concentration = pd.DataFrame(tracers.no3_14+tracers.no3_15, columns={'[NO3-]_nM'})
    no3_14 = pd.DataFrame(tracers.no3_14, columns={'[14NO3-]_nM'})
    no3_15 = pd.DataFrame(tracers.no3_15, columns={'[15NO3-]_nM'})
    d15no3 = pd.DataFrame((((tracers.no3_15/(tracers.no3_14))/R15std)-1)*1000, columns={'d15NO3-'})
    afno3_df = pd.DataFrame(tracers.afno3, columns={'AFNO3-'})

    n2o_concentration = pd.DataFrame(tracers.n2o_44+tracers.n2o_45a+tracers.n2o_45b+tracers.n2o_46, columns={'[N2O]_nM'})
    n2o_44 = pd.DataFrame(tracers.n2o_44, columns={'[N2O_44]_nM'})
    n2o_45a = pd.DataFrame(tracers.n2o_45a, columns={'[N2O_45a]_nM'})
    n2o_45b = pd.DataFrame(tracers.n2o_45b, columns={'[N2O_45b]_nM'})
    n2o_46 = pd.DataFrame(tracers.n2o_46, columns={'[N2O_46]_nM'})
    d15Na = pd.DataFrame((((tracers.n2o_45a/(tracers.n2o_44))/R15std)-1)*1000, columns={'d15N2Oa'})
    d15Nb = pd.DataFrame((((tracers.n2o_45b/(tracers.n2o_44))/R15std)-1)*1000, columns={'d15N2Ob'})
    d18O = pd.DataFrame((((tracers.n2o_46/(tracers.n2o_44))/R15std)-1)*1000, columns={'d18O'})

    n2_concentration = pd.DataFrame(tracers.n2_28+tracers.n2_29+tracers.n2_30, columns = {'[N2]_nM'})

    outputs = [
    nh4_14,
    nh4_15,
    d15nh4,
    afnh4_df,
    nh2oh_concentration,
    nh2oh_14,
    nh2oh_15,
    no_concentration,
    no_14,
    no_15,
    no2_concentration,
    no2_14,
    no2_15,
    d15no2,
    afno2_df,
    no3_concentration,
    no3_14,
    no3_15,
    d15no3,
    afno3_df,
    n2o_concentration,
    n2o_44,
    n2o_45a,
    n2o_45b,
    n2o_46,
    n2_concentration
    ]
    
    output = nh4_concentration.join(outputs)

    ### RATES COMMON TO ALL MODELS ###

    output["NO2TONO3"] = bgc.kNO2TONO3*tracers.no2_14 + bgc.kNO2TONO3/isos.alpha15NO2TONO3*tracers.no2_15
    output["NO3TONO2"] = bgc.kNO3TONO2*tracers.no3_14 + bgc.kNO3TONO2/isos.alpha15NO3TONO2*tracers.no3_15

    ### MODEL-SPECIFIC RATES ###

    if model=="modelv1":

        output["NH4TONO2"] = bgc.kNH4TONO2*tracers.nh4_14 + bgc.kNH4TONO2/isos.alpha15NH4TONO2AOA*tracers.nh4_15

        [knitrification, kdenitno2, kdenitno3, khybrid1, khybrid2] = x

        output['nitrification'] = knitrification*((tracers.nh4_14+tracers.nh4_15)**2)
        output['denitno2'] = kdenitno2*((tracers.no2_14+tracers.no2_15)**2)
        output['denitno3'] = kdenitno3*((tracers.no3_14+tracers.no3_15)**2)
        output['hybrid1'] = khybrid1*(tracers.nh4_14+tracers.nh4_15)*(tracers.no2_14+tracers.no2_15)
        output['hybrid2'] = khybrid2*(tracers.nh4_14+tracers.nh4_15)*(tracers.no2_14+tracers.no2_15)

        print(f'Nit. (nM/day): {output.nitrification.mean()}')
        print(f'Denit. from NO2- (nM/day): {output.denitno2.mean()}')
        print(f'Denit. from NO3- (nM/day): {output.denitno3.mean()}')
        print(f'Hybrid 1 (nM/day): {output.hybrid1.mean()}')
        print(f'Hybrid 2 (nM/day): {output.hybrid2.mean()}')

    elif model=="modelv2":

        kAOB = bgc.kNH4TONO2
        kAOA = bgc.kNH4TONO2

        output["NH4TONO2AOB"] = kAOB *tracers.nh4_14 + kAOB*isos.alpha15NH4TONO2AOB*tracers.nh4_15
        output["NH4TONH2OH"] = kAOA*tracers.nh4_14 + kAOA/isos.alpha15NH4TONO2AOA*tracers.nh4_15
        output["NH2OHTONO"] = kAOA*tracers.nh2oh_14 + kAOA/isos.alpha15NH4TONO2AOA*tracers.nh2oh_15
        output["NOTONO2"] = kAOA*tracers.no_14 + kAOA/isos.alpha15NH4TONO2AOA*tracers.no_15
        output["NO2TONO"] = bgc.kNO2TONO*tracers.no2_14 + bgc.kNO2TONO/isos.alpha15NO2TONO*tracers.no2_15

        [knitrification, kdenitno2, kdenitno3, khybrid1, khybrid2] = x

        output['nitrification'] = knitrification*((tracers.nh4_14+tracers.nh4_15)**2)
        output['denitno2'] = kdenitno2*((tracers.no2_14+tracers.no2_15)**2)
        output['denitno3'] = kdenitno3*((tracers.no3_14+tracers.no3_15)**2)
        output['hybrid1'] = khybrid1*(tracers.nh2oh_14+tracers.nh2oh_15)*(tracers.no_14+tracers.no_15)
        output['hybrid2'] = khybrid2*(tracers.nh2oh_14+tracers.nh2oh_15)*(tracers.no_14+tracers.no_15)

        print(f'Nit. (nM/day): {output.nitrification.mean()}')
        print(f'Denit. from NO2- (nM/day): {output.denitno2.mean()}')
        print(f'Denit. from NO3- (nM/day): {output.denitno3.mean()}')
        print(f'Hybrid 1 (nM/day): {output.hybrid1.mean()}')
        print(f'Hybrid 2 (nM/day): {output.hybrid2.mean()}')

        
    elif model=="modelv3":

        kAOB = bgc.kNH4TONO2
        kAOA = bgc.kNH4TONO2

        output["NH4TONO2AOB"] = kAOB *tracers.nh4_14 + kAOB*isos.alpha15NH4TONO2AOB*tracers.nh4_15
        output["NH4TONH2OH"] = kAOA*tracers.nh4_14 + kAOA/isos.alpha15NH4TONO2AOA*tracers.nh4_15
        output["NH2OHTONO"] = kAOA*tracers.nh2oh_14 + kAOA/isos.alpha15NH4TONO2AOA*tracers.nh2oh_15
        output["NOTONO2"] = kAOA*tracers.no_14 + kAOA/isos.alpha15NH4TONO2AOA*tracers.no_15
        output["NO2TONO"] = bgc.kNO2TONO*tracers.no2_14 + bgc.kNO2TONO/isos.alpha15NO2TONO*tracers.no2_15

        [knitrification, kdenitno2, kdenitno3, khybrid1, khybrid2] = x

        output['nitrification'] = knitrification*((tracers.nh4_14+tracers.nh4_15)**2)
        output['denitno'] = kdenitno*((tracers.no_14+tracers.no_15)**2)
        output['denitno3'] = kdenitno3*((tracers.no3_14+tracers.no3_15)**2)
        output['hybrid1'] = khybrid1*(tracers.nh2oh_14+tracers.nh2oh_15)*(tracers.no_14+tracers.no_15)
        output['hybrid2'] = khybrid2*(tracers.nh2oh_14+tracers.nh2oh_15)*(tracers.no_14+tracers.no_15)

        print(f'Nit. (nM/day): {output.nitrification.mean()}')
        print(f'Denit. from NO (nM/day): {output.denitno.mean()}')
        print(f'Denit. from NO3- (nM/day): {output.denitno3.mean()}')
        print(f'Hybrid 1 (nM/day): {output.hybrid1.mean()}')
        print(f'Hybrid 2 (nM/day): {output.hybrid2.mean()}')

    output["Incubation_time_hrs"] = output.index/1000*24
    
    output['check_mass_conservation'] = output.loc[:,['[NH4+]_nM','[NH2OH]_nM','[NO]_nM','[NO3-]_nM','[NO2-]_nM','[N2O]_nM','[N2]_nM']].sum(axis=1)
    
    return output
