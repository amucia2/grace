import sys, os, glob, shutil, fnmatch, winsound
import arcpy
from arcpy import env
from arcpy.sa import *

env.workspace = r"I:\Data\SPI\Original\24_month"
env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")
rasters = arcpy.ListRasters("*","img")

mask = r"I:\Data\SPI\Original\Clip\1Month\spi_sc_cm_2002_05_01.img"
output = r"I:\Data\SPI\Original\Clip\24Month/"

for raster in rasters:
	arcpy.env.snapRaster = mask
	outRas = arcpy.env.snapRaster
	outRas = ExtractByMask(raster, mask)
	outRas.save(output + raster)
	print(raster+" COMPLETE")
print("Extract by Mask Complete")

print("Cleaning up work files...")
file_name = os.listdir(output)
for item in file_name:
	if item.endswith(".xml") or item.endswith(".tfw") or item.endswith(".ovr") or item.endswith(".cpg") or item.endswith(".dbf"):
		os.remove(os.path.join(output, item))
winsound.Beep(1000,1000)
print("COMPLETE")
