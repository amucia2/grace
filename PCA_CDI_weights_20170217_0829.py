import numpy as np
import glob
import pdb
import numpy.ma as ma
import time
from datetime import datetime, timedelta
import arcpy as ap
from arcpy.sa import *

outDir = 'F://Research//VegOUT-Africa//VegOUT_2016//USDM//CDI_Part_USA//02Long-term Blend//PCA_Based_LTn//Part_03//WeightsPart03_4//'
theDir = 'F://Research//VegOUT-Africa//VegOUT_2016//USDM//CDI_Part_USA//02Long-term Blend//PCA_Based_LTn//Part_03//'

theSPI6s = sorted(glob.glob(theDir+"SPI6_part03_4\\*.tif"))
theSPI24s = sorted(glob.glob(theDir+"SPI24_part03_4\\*.tif"))
theSMs = sorted(glob.glob(theDir+"SM_part03_4n\\*.tif"))
theSPI60s = sorted(glob.glob(theDir+"SPI60_part03_4\\*.tif"))
theSPI12s = sorted(glob.glob(theDir+"SPI12_part03_4\\*.tif"))
thePHDIs = sorted(glob.glob(theDir+"PHDI_part03_4\\*.tif"))

therefrast = Raster(theSPI6s[0])
rowCount = therefrast.height
rowRound = int(round(rowCount,-2))
arcpy.AddMessage(str(rowRound))
columnCount = therefrast.width
theCellSize = therefrast.meanCellHeight
halfCS = theCellSize/2
#print halfCS
gridExtent = therefrast.extent
theXMin = gridExtent.XMin
##theXMax = gridExtent.XMax - halfCS
theYMin = gridExtent.YMin
##theYMax = gridExtent.YMax - halfCS
sr = arcpy.Describe(therefrast).spatialReference

theSPI6arrays =[]
theSPI24arrays =[]
theSMarrays =[]
theSPI60arrays =[]
theSPI12arrays =[]
thePHDIarrays =[]
the_date_list = []


print 'converting SPI6 data'
for p in theSPI6s:
    thep = ap.RasterToNumPyArray(p, nodata_to_value=-9999)
    theSPI6arrays.append(thep)
#print theSPI6arrays
print 'converting SPI24 data'
for l in theSPI24s:
    thel = ap.RasterToNumPyArray(l, nodata_to_value=-9999)
    theSPI24arrays.append(thel)
    the_date = l[-10:-4]
    the_date_list.append(the_date)
#print the_date_list
print 'converting SM data'
for s in theSMs:
    thes = ap.RasterToNumPyArray(s, nodata_to_value=-9999)
    theSMarrays.append(thes)
print 'converting SPI60 data'
for n in theSPI60s:
    then = ap.RasterToNumPyArray(n, nodata_to_value=-9999)
    theSPI60arrays.append(then)
print 'converting SPI12 data'
for y in theSPI12s:
    they = ap.RasterToNumPyArray(y, nodata_to_value=-9999)
    theSPI12arrays.append(they)
print 'converting PHDI data'
for e in thePHDIs:
    thee = ap.RasterToNumPyArray(e, nodata_to_value=-9999)
    thePHDIarrays.append(thee)

al_length = len(theSPI24arrays)
#print al_length

for m in range(0,52):
    theSPI6list = []    
    theSPI24list = []
    theSMlist = []
    theSPI60list = []
    theSPI12list = []
    thePHDIlist = []
    themdlist = []
    n = m
    print "creating month/year arrays"
    while n < al_length:
        theSPI6list.append(ma.masked_equal(theSPI6arrays[n],-9999))
        theSPI24list.append(ma.masked_equal(theSPI24arrays[n],-9999))
        theSMlist.append(ma.masked_equal(theSMarrays[n],-9999))
        theSPI60list.append(ma.masked_equal(theSPI60arrays[n],-9999))
        theSPI12list.append(ma.masked_equal(theSPI12arrays[n],-9999))
        thePHDIlist.append(ma.masked_equal(thePHDIarrays[n],-9999))
        themdlist.append(the_date_list[n])
        n = n + 52
    thecoeff_array = ma.empty([rowCount,columnCount,6])
    #print thecoeff_array
    print "creating weight array"
    for r in range(0,rowCount):
        for c in range(0,columnCount):
            var_array = ma.empty([6,33])
            #print var_array
            for q in range(0,33):
                #print q
                var_array[0,q] = theSPI6list[q][r,c]
                var_array[1,q] = theSPI24list[q][r,c]
                var_array[2,q] = theSMlist[q][r,c]
                var_array[3,q] = theSPI60list[q][r,c]
                var_array[4,q] = theSPI12list[q][r,c]
                var_array[5,q] = thePHDIlist[q][r,c]
            the_eig = np.linalg.eig(ma.corrcoef(var_array))
            thecoeffs = the_eig[1][:,ma.argmax(the_eig[0])]
            thecoeff_array[r,c,:] = thecoeffs
            
    theSPI6co = thecoeff_array[:,:,0].filled(-9999)     
    theoutSPI6raster = ap.NumPyArrayToRaster(theSPI6co,lower_left_corner = arcpy.Point(theXMin,theYMin),
                                           x_cell_size=theCellSize, y_cell_size=theCellSize, value_to_nodata = -9999)
    theyear = themdlist[0][4:6]
    #print theyear
    theoutSPI6raster.save(outDir + theyear + "SPI6weights.tif")
    arcpy.DefineProjection_management(outDir + theyear + "SPI6weights.tif",sr)

    theSPI24co = thecoeff_array[:,:,1].filled(-9999)     
    theoutSPI24raster = ap.NumPyArrayToRaster(theSPI24co,lower_left_corner = arcpy.Point(theXMin,theYMin),
                                           x_cell_size=theCellSize, y_cell_size=theCellSize, value_to_nodata = -9999)
    theoutSPI24raster.save(outDir + theyear + "SPI24weights.tif")
    arcpy.DefineProjection_management(outDir + theyear + "SPI24weights.tif",sr)

    theSMco = thecoeff_array[:,:,2].filled(-9999)     
    theoutSMraster = ap.NumPyArrayToRaster(theSMco,lower_left_corner = arcpy.Point(theXMin,theYMin),
                                           x_cell_size=theCellSize, y_cell_size=theCellSize, value_to_nodata = -9999)
    theoutSMraster.save(outDir + theyear + "SMweights.tif")
    arcpy.DefineProjection_management(outDir + theyear + "SMweights.tif",sr)

    theSPI60co = thecoeff_array[:,:,3].filled(-9999)     
    theoutSPI60raster = ap.NumPyArrayToRaster(theSPI60co,lower_left_corner = arcpy.Point(theXMin,theYMin),
                                           x_cell_size=theCellSize, y_cell_size=theCellSize, value_to_nodata = -9999)
    theoutSPI60raster.save(outDir + theyear + "SPI60weights.tif")
    arcpy.DefineProjection_management(outDir + theyear + "SPI60weights.tif",sr)

    theSPI12co = thecoeff_array[:,:,4].filled(-9999)     
    theoutSPI12raster = ap.NumPyArrayToRaster(theSPI12co,lower_left_corner = arcpy.Point(theXMin,theYMin),
                                           x_cell_size=theCellSize, y_cell_size=theCellSize, value_to_nodata = -9999)
    theoutSPI12raster.save(outDir + theyear + "SPI12weights.tif")
    arcpy.DefineProjection_management(outDir + theyear + "SPI12weights.tif",sr)

    thePHDIco = thecoeff_array[:,:,4].filled(-9999)     
    theoutPHDIraster = ap.NumPyArrayToRaster(thePHDIco,lower_left_corner = arcpy.Point(theXMin,theYMin),
                                           x_cell_size=theCellSize, y_cell_size=theCellSize, value_to_nodata = -9999)
    theoutPHDIraster.save(outDir + theyear + "PHDIweights.tif")
    arcpy.DefineProjection_management(outDir + theyear + "PHDIweights.tif",sr)

    
