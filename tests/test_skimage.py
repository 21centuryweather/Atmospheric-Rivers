from pathlib import Path
import sys
from skimage import measure
import xarray as xr
import numpy as np
from scipy.io import loadmat

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
    regions = np.array([[r.centroid[1]+1,r.centroid[0]+1,r.axis_major_length,r.axis_minor_length,[np.rad2deg(r.orientation),90+np.rad2deg(r.orientation)][r.orientation<0],r.mean_intensity,r.max_intensity] for r in regions])

    #Load expected data from MATLAB
    
    expected =loadmat('data/B.mat')["B"]

    # Write code using assert statements so the regions you have loaded are what you expect
    expected = np.array([ [float(r[0][0][0]),float(r[0][0][1]),float(r[1][0][0]),float(r[2][0][0]),[float(r[3][0][0]),90+float(r[3][0][0])][float(r[3][0][0])<0],float(r[5][0][0]),float(r[6][0][0])] for r in expected])
    expected=expected[expected[:, 0].argsort()]
    regions=regions[regions[:, 0].argsort()]

    Zero_expected = [e for e in expected if np.isclose(e[3],1.15470054)]
    Zero_regions = [r for r in regions if np.isclose(r[3],0)]
    Zero_expected = [[e[0],e[1],e[5],e[6]] for e in Zero_expected]
    Zero_regions = [[r[0],r[1],r[5],r[6]] for r in Zero_regions]
    assert np.allclose(Zero_expected, Zero_regions, equal_nan=True,rtol=0.1)

    expected = [e for e in expected if not np.isclose(e[3],1.15470054)]
    regions = [r for r in regions if not np.isclose(r[3],0)]

    np.set_printoptions(suppress=True)
    assert np.allclose(expected, regions, equal_nan=True,rtol=0.1)