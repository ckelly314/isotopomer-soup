"""
bgc.py
------------------

Initialize concentrations of state variables.
"""

from .. import convert_delta
from .. import convert_af


class BioGeoChemistry:
	"""
	Define initial parameters to be used in the model.

	Outputs:
	BioGeoChemistry.NH4_ambient = realtime NH4+ concentration (same for NO2- and NO3-)
	BioGeoChemistry.NH4_carrier = NH4+ carrier concentration (same for NO2- and NO3-)
	BioGeoChemistry.NH4_sokie = NH4+ spike concentration (same for NO2- and NO3-)
	"""

	def __init__(self):

		### N2O DATA ###

		self.N2O44_init = 17.29 #nmol/L
		self.N2O45a_init = 0.07970 #nmol/L
		self.N2O45b_init = 0.06709 #nmol/L
		self.N2O46_init = 0.03882 #nmol/L

		### REAL-TIME NUTRIENT DATA ###

		self.NH4_ambient = 50.0 # nmol/L
		self.NO2_ambient = 0.027885*1000 #nmol/L
		self.NO3_ambient = 28.101655*1000 # nmol/L

		self.d15NH4_ambient = 7.0 # per mil, assume
		self.d15NO2_ambient = -22.82 # per mil, PS2 sigma-theta=26.27
		self.d15NO3_ambient = 15.25 # per mil, PS2 sigma-theta=26.27

		__, _, self.afNH4_ambient = convert_delta(self.NH4_ambient, self.d15NH4_ambient)
		__, _, self.afNO2_ambient = convert_delta(self.NO2_ambient, self.d15NO2_ambient)
		__, _, self.afNO3_ambient = convert_delta(self.NO3_ambient, self.d15NO3_ambient)

		### SPIKE & CARRIER INJECTIONS ###

		self.NH4_carrier = 0.50*1000 # nmol/L; these are
		self.NO2_carrier = 1.00*1000 # nmol/L
		self.NO3_carrier = 0.0 # nmol/L

		self.R15std = 0.00367647 # air N2
		self.af_carrier = self.R15std/(1+self.R15std)

		self.NH4_spike = 0.50*1000 # nmol/L
		self.NO2_spike = 4.80*1000 # nmol/L
		self.NO3_spike = 1.00*1000 # nmol/L

		self.af_spike = 0.99999999
		_, self.d15N_spike = convert_af(self.af_spike)

		### ISOTOPE MIXING - TRACER ###

		self.NO2_init = self.NO2_ambient + self.NO2_spike # nmol/L
		self.AFNO2_init = (self.afNO2_ambient*self.NO2_ambient + self.af_spike*self.NO2_spike)/self.NO2_init
		_, self.d15NO2_init = convert_af(self.AFNO2_init)

		### ISOTOPE MIXING - NATURAL ABUNDANCE SPECIES ###

		self.NH4_init = self.NH4_ambient + self.NH4_carrier # nmol/L
		self.AFNH4_init = (self.afNH4_ambient*self.NH4_ambient + self.af_carrier*self.NH4_carrier)/self.NH4_init
		_, self.d15NH4_init = convert_af(self.AFNH4_init)

		self.NO3_init = self.NO3_ambient + self.NO3_carrier # nmol/L
		self.AFNO3_init = (self.afNO3_ambient*self.NO3_ambient + self.af_carrier*self.NO3_carrier)/self.NO3_init
		_, self.d15NO3_init = convert_af(self.AFNO3_init)

		### SUBSTRATE 14N & 15N POOLS CALCULATED FROM ISOTOPE MIXING ###

		self.nh4_14_i, self.nh4_15_i, _ = convert_delta(concentration=self.NH4_init, d15N=self.d15NH4_init)
		self.no2_14_i, self.no2_15_i, _ = convert_delta(concentration=self.NO2_init, d15N=self.d15NO2_init)
		self.no3_14_i, self.no3_15_i, _ = convert_delta(concentration=self.NO3_init, d15N=self.d15NO3_init)

	def __repr__(self):

		return f"BioGeoChemistry initialized!"

if __name__=="__main__":
	print(BioGeoChemistry())
