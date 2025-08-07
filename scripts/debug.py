import numpy as np
from skimage import measure
import xarray as xr
from scipy.io import loadmat 
from geopy.distance import great_circle
from pathlib import Path
import sys

# Find the project root directory and then add it to sys.path
pwd = Path(__file__).parent
PROJECT_DIR = pwd.parent 

#print (pwd)
sys.path.insert(0,str(PROJECT_DIR))
#print (sys.path)

from atmospheric_rivers.find_rivers import Identify_AR
import matplotlib.pyplot as plt

DATA_DIR = PROJECT_DIR / 'data'

mask = Identify_AR(PATH= DATA_DIR / 'IVT_input_slice.nc')
fig, axes = plt.subplots(1, 2)

axes[0].imshow(mask, cmap='jet')

inp=loadmat( DATA_DIR / 'mask.mat')
axes[1].imshow(inp['mask'], cmap='jet')

plt.tight_layout()
plt.show()
