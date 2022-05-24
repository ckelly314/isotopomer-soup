import scripts as sc
import numpy as np

#sc.errors("PS1", "SCM", weights = np.array([0.1, 0.1, 0.8]))

# PS1 Interface: default tracer weights + new NO3- weighting scheme gives the best fit
#sc.errors("PS1", "Interface")

#sc.errors("PS1", "Mid-oxycline")

#sc.errors("PS1", "Top of oxycline")

#sc.errors("PS1", "Surface")

#sc.errors("PS2", "Deep ODZ core", weights = np.array([0.45, 0.1, 0.45]))

sc.errors("PS2", "Deep oxycline")

#sc.errors("PS2", "SCM")

#sc.errors("PS2", "Base of ODZ")

#sc.errors("PS2", "Interface", weights = np.array([0.45, 0.1, 0.45]))

#sc.errors("PS2", "SCM", weights = np.array([0.8, 0.1, 0.1]))

#sc.errors("PS2", "SNM", weights = np.array([0.45, 0.1, 0.45]))

#sc.errors("PS3", "Interface", weights = np.array([0.45, 0.1, 0.45]))

#sc.errors("PS3", "Mid-oxycline")

#sc.errors("PS3", "SCM", weights = np.array([0.45, 0.1, 0.45]))