# A function which wraps skimage.measure.regionprops
import numpy as np
from skimage import measure
from geopy.distance import great_circle
import xarray as xr

EQUATOR_TOL = 5 #Exclude rivers whithin this tolerance (+/-) of the equator
ORIENTATION_ANGLE = 85 # Excludes objects that don't have the correct angle 

def region_props(PATH,IVT_threshold=250):

    # Load some input sample data
    inp = xr.open_dataarray(PATH)
    dataset = inp.values

    #create binary mask based on input threshold
    A1 = dataset>IVT_threshold

    return measure.regionprops(measure.label(A1),dataset)


def Identify_AR(inp,IVT_threshold=250,length_threshold=2000,aspect_ratio_threshold=2):
    """
    A function where which returns a mask of the river location for a given input netCDF data
    This will use region_props defined above
    """

    # Load some input sample data
    dataset = inp.values

    lat = inp.lat.values
    lon = inp.lon.values
    lat_res=lat[1]-lat[0]
    lon_res=lon[1]-lon[0]
    
    #create binary mask based on input threshold
    A1 = dataset>IVT_threshold

    regions = measure.regionprops(measure.label(A1),dataset)

    # Convert centroid coords from pixelspace to lat/lon space
    for region in regions:
        L = region.major_axis_length/2 * ((lat_res + lon_res)/2.)

        region.lat_c = lat[round(region.centroid[0])]
        region.lon_c = lon[round(region.centroid[1])]

        a2 = region.lon_c + L*np.sin(region.orientation)
        a3 = region.lat_c + L*np.cos(region.orientation)

        region.AR_length = 2*great_circle((a3,a2),(region.lat_c,region.lon_c)).kilometers
    
    #length of river must exceed...
    regions = [region for region in regions if region.AR_length>length_threshold]

    #aspect ratio test.
    regions = [region for region in regions if region.axis_major_length/region.axis_minor_length>=aspect_ratio_threshold]
    
    #orientation angle test. Excludes systems within 5 degrees of equator (mostly artifacts)
    regions = [region for region in regions if abs(region.lat_c) > EQUATOR_TOL]

    #Orientation angle is just to get rid of artifacts
    regions = [region for region in regions if abs(np.rad2deg(region.orientation))< ORIENTATION_ANGLE]

    #maps pixels in the AR onto lat-lon array
    mask=np.zeros_like(dataset)
    for region in regions:
        for pixel in region.coords:
            mask[pixel[0]][pixel[1]] = 1
    
    return mask
