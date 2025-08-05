import xarray as xr
from REID_ARalgorithm_v3_module import REID_ARalgorithm_v3
from scipy.io import loadmat
import numpy as np

'''try:
    ds = xr.open_dataset('IVT_Aust_daily_2deg_ERA5_1960-2014.nc')
    print("Dataset loaded successfully.")
    print(ds)
except Exception as e:
    print(f"An error occurred while opening the dataset: {e}")'''

try:
    observedA1,observedA2,observedB = REID_ARalgorithm_v3(loadmat("data/ivt_3rd_timestep.mat"),250,-90,0,1,0,370,1,2000,2)
except Exception as e:
    print(f"Module threw error when testing:{e}")
    exit()

try:
    expectedA1 = np.swapaxes(loadmat("data/A1.mat")["A1"], 0, 1)
    expectedA2 = np.swapaxes(loadmat("data/A2.mat")["A2"], 0, 1)
    #print(expectedB[0].dtype)
    #exit(0)
except Exception as e:
    print(f"Eception while loading expected data{e}")
    exit()

print("started testing")
#print(type(expectedA1),type(observedA1))
if np.array_equal(expectedA1, observedA1):
    print("A1 same")
else:
    print(f"A1 test failed\nexpected:{expectedA1}\nobserved:{observedA1}")

if np.array_equal(expectedA2, observedA2,equal_nan=True):
    print("A2 same")
else:
    print(f"A2 test failed\nexpected:{expectedA2}\nobserved:{observedA2}")


#Centroid,MajorAxisLength,MinorAxisLength,Orientation,PixelList,MeanIntensity,MaxIntensity
