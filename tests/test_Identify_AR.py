import pytest
from pathlib import Path
import sys
from skimage import measure
import xarray as xr
import numpy as np

from atmospheric_rivers import logger
from atmospheric_rivers.find_rivers import Identify_AR

LOG = logger.get_logger(__name__)

def test_config(pytestconfig):

    LOG.info(f'testconfig.rootdir = {pytestconfig.rootdir}')
    DATA_DIR = Path(pytestconfig.rootdir / 'data')
    print(f'DATA_DIR = {DATA_DIR}')

def test_Identify_AR(pytestconfig):
    """
    Run the skimage.measure regionprops module against a set of input data
    This test is valid for skimage version 0.25.2
    """
    LOG.info(f'testconfig.rootdir = {pytestconfig.rootdir}')
    DATA_DIR = Path(pytestconfig.rootdir / 'data')
    
    DATA_PATH = DATA_DIR / 'IVT_input_slice.nc'
    mask = Identify_AR(DATA_PATH)


    LOG.info(f'Mask was {mask.size}')

    """
    Load expected data
    """
    from scipy.io import loadmat
    expected =loadmat('data/mask.mat')["mask"]

    # Write code using assert statements so the regions you have loaded are what you expect
    assert np.array_equal(mask, expected,equal_nan=True)

def test_Identify_AR_version(pytestconfig):
    """
    Run the skimage.measure regionprops module against a set of input data
    This test is valid for skimage version 0.25.2
    """
    LOG.info(f'testconfig.rootdir = {pytestconfig.rootdir}')
    DATA_DIR = Path(pytestconfig.rootdir / 'data')
    
    DATA_PATH = DATA_DIR / 'IVT_input_slice.nc'
    mask = Identify_AR(DATA_PATH)
    
    # use
    # mask.tofile(DATA_DIR/"IVT_input_slice8.8.25.bin")
    # to store the file

    LOG.info(f'Mask was {mask.size}')

    """
    Load expected data
    """
    from scipy.io import loadmat
    
    expected =np.fromfile(DATA_DIR/"IVT_input_slice8.8.25.bin",dtype = np.float64)
    expected = expected.reshape(mask.shape)
    
    # Write code using assert statements so the regions you have loaded are what you expect
    assert np.array_equal(mask, expected,equal_nan=True)