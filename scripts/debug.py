import numpy as np
from skimage import measure
import xarray as xr
from scipy.io import loadmat 
from geopy.distance import great_circle
import os
os.chdir("..")

from atmospheric_rivers.find_rivers import Identify_AR

import matplotlib.pyplot as plt
mask = Identify_AR()
fig, axes = plt.subplots(1, 2)

axes[0].imshow(mask, cmap='jet')

inp=loadmat('data/mask.mat')
axes[1].imshow(inp['mask'], cmap='jet')

plt.tight_layout()
plt.show()
