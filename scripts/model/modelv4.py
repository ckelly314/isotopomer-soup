"""
File: modelv4.py
----------------

Version of the model containing intermediates NH2OH and NO;
N2O is produced from NH4+, NO2-, NO3-, and two hybrid pathways,
which produce N2O from a combination of NH2OH and NO2-.
"""

from .. import binomial
import numpy as np

# produce n2o from intermediates, plus denitrification from nitrite
def modelv4(x, bgc, isos, tracers, modelparams):

    ### UNPACK X ###
    [knitrification, kdenitno2, kdenitno3, khybrid5, khybrid6] = x

    ### UNPACK MODEL PARAMS ###
    (dt, T, times) = modelparams

    ### TIME STEPPING ###
    for iT in range(T-1):

        Jhybrid1 = khybrid5*(tracers.nh2oh_14[iT]+tracers.nh2oh_15[iT])*(tracers.no2_14[iT]+tracers.no2_15[iT])
        Jhybrid2 = khybrid6*(tracers.nh2oh_14[iT]+tracers.nh2oh_15[iT])*(tracers.no2_14[iT]+tracers.no2_15[iT]) 
        
        Jnitrification = knitrification*((tracers.nh4_14[iT]+tracers.nh4_15[iT])**2)
        Jdenitno2 = kdenitno2*((tracers.no2_14[iT]+tracers.no2_15[iT])**2)
        Jdenitno3 = kdenitno3*((tracers.no3_14[iT]+tracers.no3_15[iT])**2)
        
        kAOA = bgc.kNH4TONO2
        kAOB = bgc.kNH4TONO2
        kNO2TONO = 0.017 #bgc.kNO2TONO

        # update substrate values
        tracers.nh4_14[iT+1,:] = tracers.nh4_14[iT,:] + dt*(
            -kAOB*tracers.nh4_14[iT]
            -kAOA*tracers.nh4_14[iT]
            -Jnitrification*(1-tracers.afnh4[iT,:]))

        tracers.nh4_15[iT+1,:] = tracers.nh4_15[iT,:] + dt*(
            -kAOB/isos.alpha15NH4TONO2AOB*tracers.nh4_15[iT]
            -kAOA/isos.alpha15NH4TONO2AOA*tracers.nh4_15[iT]
            -Jnitrification*tracers.afnh4[iT,:])

        tracers.nh2oh_14[iT+1, :] = tracers.nh2oh_14[iT, :] + dt*(
            +kAOA*tracers.nh4_14[iT]
            -kAOA*tracers.nh2oh_14[iT]
            -Jhybrid1*(1-tracers.afnh2oh[iT])
            -Jhybrid2*(1-tracers.afnh2oh[iT])
        )

        tracers.nh2oh_15[iT+1, :] = tracers.nh2oh_15[iT, :] + dt*(
            +kAOA/isos.alpha15NH4TONO2AOA*tracers.nh4_15[iT]
            -kAOA/isos.alpha15NH4TONO2AOA*tracers.nh2oh_15[iT]
            -Jhybrid1*(tracers.afnh2oh[iT])
            -Jhybrid2*(tracers.afnh2oh[iT])
        )
            
        tracers.no_14[iT+1, :] = tracers.no_14[iT, :] + dt*(
            +kAOA*tracers.nh2oh_14[iT]
            +kNO2TONO*tracers.no2_14[iT]
            -kAOA*tracers.no_14[iT]
        )

        tracers.no_15[iT+1, :] = tracers.no_15[iT, :] + dt*(
            +kAOA/isos.alpha15NH4TONO2AOA*tracers.nh2oh_15[iT]
            +kNO2TONO/isos.alpha15NO2TONO*tracers.no2_15[iT]
            -kAOA/isos.alpha15NH4TONO2AOA*tracers.no_15[iT]
        )
        
        tracers.no2_14[iT+1,:] = tracers.no2_14[iT,:] + dt*(
            +kAOB*tracers.nh4_14[iT]
            +kAOA*tracers.no_14[iT]
            +bgc.kNO3TONO2*tracers.no3_14[iT]
            -bgc.kNO2TONO3*tracers.no2_14[iT]
            -kNO2TONO*tracers.no2_14[iT]
            -Jdenitno2*(1-tracers.afno2[iT,:])
            -Jhybrid1*(1-tracers.afno2[iT])
            -Jhybrid2*(1-tracers.afno2[iT])
        )

        tracers.no2_15[iT+1,:] = tracers.no2_15[iT,:] + dt*(
            kAOB/isos.alpha15NH4TONO2AOB*tracers.nh4_15[iT]
            +kAOA/isos.alpha15NH4TONO2AOA*tracers.no_15[iT]
            +bgc.kNO3TONO2/isos.alpha15NO3TONO2*tracers.no3_15[iT]
            -bgc.kNO2TONO3/isos.alpha15NO2TONO3*tracers.no2_15[iT]
            -kNO2TONO/isos.alpha15NO2TONO*tracers.no2_15[iT]
            -Jdenitno2*tracers.afno2[iT,:]
            -Jhybrid1*(tracers.afno2[iT])
            -Jhybrid2*(tracers.afno2[iT])
        )

        tracers.no3_14[iT+1,:] = tracers.no3_14[iT,:] + dt*(
            bgc.kNO2TONO3*tracers.no2_14[iT]
            -bgc.kNO3TONO2*tracers.no3_14[iT]
            -Jdenitno3*(1-tracers.afno3[iT,:]))

        tracers.no3_15[iT+1,:] = tracers.no3_15[iT,:] + dt*(
            bgc.kNO2TONO3/isos.alpha15NO2TONO3*tracers.no2_15[iT]
            -bgc.kNO3TONO2/isos.alpha15NO3TONO2*tracers.no3_15[iT]
            -Jdenitno3*tracers.afno3[iT,:])

        # recalculate atom fractions at each time step
        tracers.afnh4[iT+1,:] = tracers.nh4_15[iT+1,:]/(tracers.nh4_14[iT+1,:] + tracers.nh4_15[iT+1,:])
        tracers.afnh2oh[iT+1,:] = tracers.nh2oh_15[iT+1,:]/(tracers.nh2oh_14[iT+1,:] + tracers.nh2oh_15[iT+1,:])
        tracers.afno[iT+1,:] = tracers.no_15[iT+1,:]/(tracers.no_14[iT+1,:] + tracers.no_15[iT+1,:])
        tracers.afno2[iT+1,:] = tracers.no2_15[iT+1,:]/(tracers.no2_14[iT+1,:] + tracers.no2_15[iT+1,:])
        tracers.afno3[iT+1,:] = tracers.no3_15[iT+1,:]/(tracers.no3_14[iT+1,:] + tracers.no3_15[iT+1,:])

        # calculate total rates of N2O production from substrates

        total_nitrification = Jnitrification/2 # need to multiply by 1/2 to convert nmols N/L/day into nmols N2O/L/day
        total_denit_no2 = Jdenitno2/2
        total_denit_no3 = Jdenitno3/2
        total_hybrid1 = Jhybrid1/2
        total_hybrid2 = Jhybrid2/2

        # calculate probabilities of isotopomer formation

        f = (0.02*np.random.randn() + 0.5)

        p1, p2, p3, p4 = binomial(tracers.afno2[iT], tracers.afnh2oh[iT])

        p46hybrid1 = p1
        p45ahybrid1 = p2
        p45bhybrid1 = p3
        p44hybrid1 = p4

        p46hybrid2 = p1
        p45ahybrid2 = (p2+p3)*f
        p45bhybrid2 = (p2+p3)*(1-f)
        p44hybrid2 = p4
        
        p46nh4, p45anh4, p45bnh4, p44nh4 = binomial(tracers.afnh4[iT], tracers.afnh4[iT])
        p46no2, p45ano2, p45bno2, p44no2 = binomial(tracers.afno2[iT], tracers.afno2[iT])
        p46no3, p45ano3, p45bno3, p44no3 = binomial(tracers.afno3[iT], tracers.afno3[iT])

        # update N2O values
        tracers.n2o_46[iT+1,:] = tracers.n2o_46[iT,:] + dt*(
            +total_hybrid1*p46hybrid1
            +total_hybrid2*p46hybrid2
            +total_nitrification*p46nh4
            +total_denit_no2*p46no2
            +total_denit_no3*p46no3
            -bgc.kN2OCONS/isos.alpha46N2OtoN2*tracers.n2o_46[iT])

        tracers.n2o_45a[iT+1, :] = tracers.n2o_45a[iT,:] + dt*(
            +total_hybrid1*p45ahybrid1
            +total_hybrid2*p45ahybrid2
            +total_nitrification*p45anh4
            +total_denit_no2*p45ano2
            +total_denit_no3*p45ano3
            -bgc.kN2OCONS/isos.alpha15N2OatoN2*tracers.n2o_45a[iT])

        tracers.n2o_45b[iT+1, :] = tracers.n2o_45b[iT,:] + dt*(
            +total_hybrid1*p45bhybrid1
            +total_hybrid2*p45bhybrid2
            +total_nitrification*p45bnh4
            +total_denit_no2*p45bno2
            +total_denit_no3*p45bno3
            -bgc.kN2OCONS/isos.alpha15N2ObtoN2*tracers.n2o_45b[iT])

        tracers.n2o_44[iT+1,:] = tracers.n2o_44[iT,:] + dt*(
            +total_hybrid1*p44hybrid1
            +total_hybrid2*p44hybrid2
            +total_nitrification*p44nh4
            +total_denit_no2*p44no2
            +total_denit_no3*p44no3
            -bgc.kN2OCONS*tracers.n2o_44[iT])

        # update N2 values

        tracers.n2_28[iT+1,:] = tracers.n2_28[iT,:] + dt*(bgc.kN2OCONS*tracers.n2o_44[iT])

        tracers.n2_29[iT+1,:] = tracers.n2_29[iT,:] + dt*(
            bgc.kN2OCONS/isos.alpha15N2OatoN2*tracers.n2o_45a[iT]
            +bgc.kN2OCONS/isos.alpha15N2ObtoN2*tracers.n2o_45b[iT])

        tracers.n2_30[iT+1,:] = tracers.n2_30[iT,:] + dt*(bgc.kN2OCONS/isos.alpha46N2OtoN2*tracers.n2o_46[iT])
    
    return tracers
