import scripts as sc
import numpy as np

sc.runmontecarlo("PS2", "Interface", 100, weights=np.array([0.45, 0.1, 0.45]))
