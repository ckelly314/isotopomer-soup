import scripts as sc
import numpy as np

sc.runmontecarlo("PS1", "SCM", 100, weights = np.array([0.1, 0.1, 0.8]))
