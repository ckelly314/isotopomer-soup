"""
bgc.py
------------------

Initialize concentrations of substrates.
"""


class BioGeoChemistry:
	"""
	Define initial parameters to be used in the model.

	Outputs:
	BioGeoChemistry.NH4_ambient = realtime NH4+ concentration (same for NO2- and NO3-)
	BioGeoChemistry.NH4_carrier = NH4+ carrier concentration (same for NO2- and NO3-)
	BioGeoChemistry.NH4_sokie = NH4+ spike concentration (same for NO2- and NO3-)
	"""

	def __init__(self):

		### REAL-TIME NUTRIENT DATA ###

		self.NH4_ambient = 50.0 # nmol/L
		self.NO2_ambient = 0.027885*1000 #nmol/L
		self.NO3_ambient = 28.101655*1000 # nmol/L

		### SPIKE & CARRIER INJECTIONS ###

		self.NH4_carrier = 0.50*1000 # nmol/L; these are used in kestimates.py
		self.NO2_carrier = 1.00*1000 # nmol/L
		self.NO3_carrier = 0.0 # nmol/L

		self.NH4_spike = 0.50*1000 # nmol/L
		self.NO2_spike = 4.80*1000 # nmol/L
		self.NO3_spike = 1.00*1000 # nmol/L

	def __repr__(self):

		return f"BioGeoChemistry initialized!"

if __name__=="__main__":
	print(BioGeoChemistry())