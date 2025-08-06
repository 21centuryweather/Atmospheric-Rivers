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

    mask_temp=np.zeros_like(dataset)
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
        region.lat_c = lat[round(region.centroid[0])]
        region.lon_c = lon[round(region.centroid[1])]

        a2 = region.lon_c + L*np.sin(region.orientation)
        
        arc=acosd(round(sind(region.lon_c)*\
                          sind(a2)+cosd(region.lon_c)*\
                          (cosd(a2)*cosd(L*cosd(region.orientation))),15))#remove rounding errors
        
        AR_length=2*RADIUS_EARTH*arc*np.pi/180/1000.
        region.AR_length = AR_length
        AR_lengths.append(AR_length)
        coords.append([region.lat_c,region.lon_c])
    
    #length of river must exceed...
    regions = [region for region in regions if region.AR_length>length_threshold]

    #aspect ratio and orientation angle test. Excludes systems within 5 degrees of equator (mostly artifacts)
    regions = [region for region in regions if region.axis_major_length/region.axis_minor_length>=aspect_ratio and abs(region.lat_c) >5]
    #print([r.AR_length for r in regions])
    #Orientation angle is just to get rid of artifacts
    regions = [region for region in regions if abs(np.rad2deg(region.orientation))>10]
    #print([r.AR_length for r in regions])
    #maps pixels in the AR onto lat-lon array
    for region in regions:
        for pixel in region.coords:
            mask_temp[pixel[0]][pixel[1]] = dataset[pixel[0]][pixel[1]]
    import matplotlib.pyplot as plt
    plt.imshow(mask_temp, cmap='jet')
    plt.show()
