import arcpy
from arcpy import env
from arcpy.sa import *

env.workspace = r"L:\SNR\GRACE\USDM\Raster\Tif"
env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

rasters = arcpy.ListRasters("*","tif")
USDM = rasters[0:900]
USDM.sort()
out_dir = r"L:\SNR\GRACE\USDM\usdm_gws_2/"
rasterMask = r"L:\SNR\GRACE\gws_new\gws_usdm\gws20020401.tif"
temp1 = temp2 = temp3 = 0

for raster in USDM:
	arcpy.env.resamplingMethod = "BILINEAR"
	arcpy.env.snapRaster = r"L:\SNR\GRACE\gws_new\gws_usdm\gws20020401.tif"
	arcpy.env.extent = rasterMask
	temp1 = ExtractByMask(raster,rasterMask)
	temp2 = Con(IsNull(temp1),-1,temp1)
	outras = ExtractByMask(temp2,rasterMask)
	outras.save(out_dir+raster)
	print(raster + "Complete")

print("COMPLETE")
