from pathlib import Path
import numpy as np
import xarray as xr

from scipy.io import loadmat

from atmospheric_rivers.find_rivers import Identify_AR

DATA_DIR = Path('data/24Hpython')
DATA_PATH = DATA_DIR/'ERA5_IVT_hourly_19880201.nc'
dataset =xr.open_dataset(DATA_PATH)

dataset = dataset.sel(
    lon=slice(90.0, 170.0),
    lat=slice(-50.0, 0.0)
)

for i, page in enumerate([dataset.sel(time=t) for t in dataset.time]):

    
    mask = Identify_AR(DATA_PATH,IVT_threshold=200)

    mask.tofile(DATA_DIR/"Hour{i}.bin")
    
    

    assert np.array_equal(mask, expected,equal_nan=True)
