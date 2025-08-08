from pathlib import Path
import sys
from skimage import measure
import xarray as xr
import numpy as np

from atmospheric_rivers import logger
from atmospheric_rivers.find_rivers import region_props

LOG = logger.get_logger(__name__)

def test_region_props(pytestconfig):
    """
    Run the skimage.measure regionprops module against a set of input data
    This test is valid for skimage version 0.25.2
    """
    LOG.info(f'testconfig.rootdir = {pytestconfig.rootdir}')

    DATA_DIR = Path(pytestconfig.rootdir / 'data')
    
    DATA_PATH = DATA_DIR / 'IVT_input_slice.nc'
    regions = region_props(DATA_PATH)


    LOG.info(f'Found {len(regions)} regions')

    """
    Load expected data
    """
    from scipy.io import loadmat
    expected =loadmat('data/B.mat')["B"]

    # Write code using assert statements so the regions you have loaded are what you expect
    assert np.array_equal(expected, regions,equal_nan=True)