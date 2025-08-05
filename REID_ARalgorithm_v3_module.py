import numpy as np
from skimage import measure

def REID_ARalgorithm_v3(dataset,IVT_threshold,lati,latf,lat_res,loni,lonf,lon_res,length_threshold,aspect_ratio):
    lat=[i for i in range(lati,latf,lat_res)]
    lon=[i for i in range(loni,lonf,lon_res)]
    dataset = dataset['f']
    #print(dataset)
    #it flips it back to col,rows at the end. Algorthim was designed in Matlab hence rows,col
    mask_temp=np.zeros(dataset.ndim)
    #create binary mask based on input threshold
    A1=np.ones(dataset.ndim)
    A2=dataset

    A1 = dataset>IVT_threshold
    A2[dataset<IVT_threshold]=np.nan


    regions = measure.regionprops(measure.label(A1),dataset)#,properties=('centroid', 'orientation', 'axis_major_length', 'axis_minor_length'))

    centroid= [[i.centroid[0]+1,i.centroid[1]+1] for i in regions]
    M1= [i.axis_major_length for i in regions]
    m1= [i.axis_minor_length for i in regions]
    orientation = [i.orientation for i in regions]#in rad from -pi/2 to pi/2
    #orientation = [[i,i+360][int(i<0)] for i in np.rad2deg(orientation)]
    pixelList = [i.coords for i in regions]
    intensity_mean = [i.intensity_mean for i in regions]
    intensity_max= [i.intensity_max for i in regions]
    
    #B = [(np.array([[x,y]]),np.array([[M1]]),np.array([[m1]]),np.array([[np.negative(np.rad2deg(orientation))]]),np.array([[i+1,j+1] for [i,j] in pixelList]),np.array([[intensity_mean]]),np.array([[intensity_max]]))]
    #Centroid,MajorAxisLength,MinorAxisLength,Orientation,PixelList,MeanIntensity,MaxIntensity

    h=1
    #B=struct2cell(B);
    #B=np.swapaxes(B)
    #converts centroid info from index to lat lon

    B=[centroid,M1,m1,orientation,pixelList,intensity_mean,intensity_max,[0]*len(centroid)]
    
    C = [[j[i] for j in B] for i in range(len(B[0]))]


    for i in C:
        i[0][1]=lon[int(i[0][1])]
        i[0][0]=lat[int(i[0][0])]

    

    #Calculate length in km from 'major axis length'

    for i in C:
        a1=i[1] #centroid lat
        b1=i[0] #centroid lon
        o=-1*i[5] #orientation
        L=(i[3]/2) * ((lat_res+lon_res)/2)
        a2=a1+(L*np.sin(o))
        r=6371000

        arc=np.acos(round(np.sin(a1)*np.sin(a2)+np.cos(a1)*(np.cos(a2)*np.cos(L*np.cos(o))),15))#remove rounding errors
    
        AR_length=r*arc/1000; #km
        i[7]=AR_length 
    

    

    b=B[4]
    D=[]
    d=[]
    #length of river must exceed...
    for i in range(len(C)):
        if C[i][7]>length_threshold:
            D.append(C[i])
            d.append(b[i])


    
    #aspect ratio and orientation angle test. Excludes systems within 5 degrees of equator (mostly artifacts)
    E=[]
    e=[]
    for i in range(len(D)):
        if D[i][2]/D[i][3] >= aspect_ratio and abs(D[i][1])>5:
            E.append(D[i])
            e.append(d[i])
    
    #Orientation angle is just to get rid of artifacts
    F=[]
    f=[]
    for i in range(len(E)):
        if abs(E[i][5])>10:
            F.append(E[i])
            f.append(e[i])

    
    #maps pixels in the AR onto lat-lon array
    for l in range(len(F)):
        for i in range(len(g)):
            mask_temp[f[i][1]][f[i][0]]=1

    return A1,A2,mask_temp
