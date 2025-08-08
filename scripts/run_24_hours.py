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
"""
PUT ERA5_IVT_hourly_19880201.nc IN

data\24Hpython\
"""



DATA_PATH = Path('data\ERA5_AR_250_Australia_19880201.nc')
expected = xr.open_dataset(DATA_PATH)
expected = [expected.sel(time=t) for t in expected.time]

for i, page in enumerate([dataset.sel(time=t) for t in dataset.time]):

    mask = Identify_AR(page["ivt"])

    mask.tofile(DATA_DIR/f"Hour{i}.bin")
    

    assert np.array_equal(mask, expected[i],equal_nan=True)
