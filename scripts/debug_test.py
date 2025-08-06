import numpy as np
from skimage import measure
import xarray as xr
from scipy.io import loadmat 
#from REID_ARalgorithm_v3_module import REID_ARalgorithm_v3

RADIUS_EARTH=6371000

def sind(angle):
    return np.sin(np.deg2rad(angle))

def cosd(angle):
    return np.cos(np.deg2rad(angle))

def acosd(angle):
    return np.rad2deg(np.acos(angle))

if __name__ == "__main__":

    # Load some input sample data
    inp=loadmat('data/ivt_3rd_timestep.mat')

    IVT_threshold=250
    lati=-90
    latf=1
    lat_res=1
    loni=0
    lonf=370
    lon_res=1
    length_threshold=2000
    aspect_ratio=2
    dataset = inp['f']
    lat=[i for i in range(lati,latf,lat_res)]
    lon=[i for i in range(loni,lonf,lon_res)]

    mask_temp=np.zeros(dataset.ndim)
    #create binary mask based on input threshold
    A1=np.ones(dataset.ndim)
    A2=dataset

    A1 = dataset>IVT_threshold
    A2[dataset<IVT_threshold]=np.nan


    regions = measure.regionprops(measure.label(A1),dataset)#,properties=('centroid', 'orientation', 'axis_major_length', 'axis_minor_length'))

    # Convert centroid coords from pixelspace to lat/lon space

    coords = []
    for region in regions:
        lat_c = lat[round(region.centroid[0])]
        lon_c = lon[round(region.centroid[1])]
        coords.append([lat_c,lon_c])

    AR_lengths =  []
    for region in regions:
        L = region.major_axis_length/2 * ((lat_res + lon_res)/2.)
        lat_c = lat[round(region.centroid[0])]
        a1 = lon[round(region.centroid[1])]

        a2 = a1 + L*np.sin(region.orientation)
        
        arc=acosd(round(sind(a1)*\
                          sind(a2)+cosd(a1)*\
                          (cosd(a2)*cosd(L*cosd(region.orientation))),15))#remove rounding errors
        
        AR_length=2*RADIUS_EARTH*arc*np.pi/180/1000.
        
        AR_lengths.append(AR_length)
        coords.append([lat_c,lon_c])
    print(AR_lengths)