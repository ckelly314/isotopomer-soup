import scripts as sc
import numpy as np

# PS1 Interface: default tracer weights + new NO3- weighting scheme gives the best fit
sc.runmodelv5("PS1", "Interface")

#sc.runmodelv5("PS2", "SCM")

#sc.runmodelv5("PS2", "Base of ODZ")

#sc.runmodelv5("PS2", "Deep ODZ core")#, weights = np.array([0.45, 0.1, 0.45]))

#sc.runmodelv5("PS2", "Interface", weights = np.array([0.45, 0.1, 0.45]))

#sc.runmodelv5("PS2", "SCM", weights = np.array([0.8, 0.1, 0.1]))

#sc.runmodelv5("PS2", "SNM", weights = np.array([0.45, 0.1, 0.45]))

#sc.runmodelv5("PS3", "Interface", weights = np.array([0.45, 0.1, 0.45]))

#sc.runmodelv5("PS3", "Mid-oxycline")

#sc.runmodelv5("PS3", "SCM", weights = np.array([0.45, 0.1, 0.45]))