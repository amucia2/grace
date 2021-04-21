# ---------------------------------------------------------------------------
# GRACE_process_weekly.py
# Created on: 2011-09-13
# Description: Downloads and converts GRACE data products and produces a
# variety of maps
# ---------------------------------------------------------------------------

import shutil
import time
import os
import glob
import datetime
from datetime import timedelta, date
import arcpy

## Set Global Constants
res = 300
historicdata = "C:\\GRACEGroundwaterEval\\Operational\\GRACE\\historical_data\\"
outdir = "C:\\GRACEGroundwaterEval\\Operational\\GRACE\\output_new\\Archive\\ArchiveNew\\"
currentdir = "C:\\GRACEGroundwaterEval\\Operational\\GRACE\\output_new\\Current\\"
webdir = "C:\\GRACEGroundwaterEval\\Operational\\GRACE\\output_new\\Web\\"
pubdir = "C:\\GRACEGroundwaterEval\\Operational\\GRACE\\output_new\\NASApublication\\"
workdir = "C:\\GRACEGroundwaterEval\\Operational\\GRACE\\working\\"
mxddir = "C:\\GRACEGroundwaterEval\\Operational\\GRACE\\BaseData\\mxds\\"
basedir = "C:\\GRACEGroundwaterEval\\Operational\\GRACE\\"
layerdir = "C:\\GRACEGroundwaterEval\\Operational\\GRACE\\BaseData\\Files\\"
Projection = "C:\\GRACEGroundwaterEval\\Operational\\GRACE\\BaseData\\Files\\RasterProjection.tif"
Header = "C:\\GRACEGroundwaterEval\\Operational\\GRACE\\BaseData\\Files\\gws_perc_0125deg_US.hdr"
TFW = "C:\\GRACEGroundwaterEval\\Operational\\GRACE\\BaseData\\Files\\template.tfw"
FinalPRJ = "C:\\GRACEGroundwaterEval\\Operational\\GRACE\\Basedata\\Shapes\\Conus_Mask.prj"
thebinaries = []#"gws_perc_0125deg_US"]#,"rtzsm_perc_0125deg_US","sfsm_perc_0125deg_US"]
#thebinaries = []
baselist = []
theyears = [2007]#2008,2009,2010,2011,2012,2013,2014,2015]#list(range(2013))
thetypes = ['gws','rtzsm','sfsm']
for year in theyears:
    for type in thetypes:
        print historicdata+str(year)+"\\"+type
        baselist = glob.glob(historicdata+str(year)+"\\"+type+"\\*_US_*.bin")
        thebinaries = thebinaries+baselist
thebinaries.sort(reverse=True)
arcpy.env.overwriteOutput = True
for fbin in thebinaries:
    # Set the current workspace
    arcpy.env.workspace = workdir
    isodate = (os.path.splitext(os.path.basename(fbin))[0]).split("_")[4]
    bin = (os.path.splitext(os.path.basename(fbin))[0]).replace("_"+isodate,"")
    print "Retrieving bin file "+bin
    thetype = (bin).split("_")[0]
    print thetype
    print isodate
    thedate = datetime.datetime(year=int(isodate[0:4]), month=int(isodate[4:6]), day=int(isodate[6:8]))
    thetextdate = thedate.strftime("%B %d, %Y")
    print thetextdate
    localfile = fbin #outdir+isodate+"\\"+bin+"_"+isodate+".bin"
    if not os.path.exists(outdir+isodate):
        os.makedirs(outdir+isodate)
    workfile = workdir+bin+"_"+isodate+".bin"
    fltwork = workdir+bin+"_"+isodate+".flt"
    binhdr = workdir+bin+"_"+isodate+".hdr"
    rtif = workdir+bin+"_"+isodate+"_raw.tif"
    ## If this doesn't work, ad "+bin" between workdir and "_"
    ftif = workdir+bin+"_"+isodate+".tif" 
    ftfw = workdir+bin+"_"+isodate+".tfw"
    fimg = workdir+bin+"_"+isodate+".img"
    fpimg = outdir+isodate+"\\"+bin+"_"+isodate+".img"
    fptif = outdir+isodate+"\\"+isodate+".tif"
    fptfw = outdir+isodate+"\\"+bin+"_"+isodate+".tfw"
    shutil.copyfile(localfile, workfile)
    shutil.copyfile(localfile, fltwork)
    shutil.copyfile(localfile,pubdir+"data\\"+bin+"_"+isodate+".bin")
    shutil.copyfile(localfile,outdir+isodate+"\\"+bin+"_"+isodate+".bin")
    shutil.copyfile(Header, binhdr)
    shutil.copyfile(TFW, ftfw)
    arcpy.FloatToRaster_conversion(fltwork, rtif)
    arcpy.Flip_management(rtif, ftif)
    shutil.copyfile(ftif, fptif)
    shutil.copyfile(TFW, fptfw)
##  Assign a Spatial reference to the GeoTIFFs
    descRaster = arcpy.Describe(Projection)
    SR = descRaster.spatialReference
    arcpy.DefineProjection_management(ftif, SR)
    arcpy.RasterToOtherFormat_conversion(ftif,workdir,"IMAGINE Image")
##    print fimg
##    print fpimg
##    print FinalPRJ
    arcpy.ProjectRaster_management (fimg, fpimg, FinalPRJ, "NEAREST", 14225.65114, "NAD_1983_To_WGS_1984_1")
####  Mapping the data
##    ## Set the path for the layer files
##    publyr = layerdir+"GRACE_Red2Blue_img.lyr"
##    reglyr = layerdir+"GRACE_WebColors_img.lyr"
##    if thetype=="gws":
##        print "Processing "+thetype+" maps"
##        mxd = arcpy.mapping.MapDocument(mxddir+"GRACE_GWS_automated.mxd")
##        mxdweb = arcpy.mapping.MapDocument(mxddir+"GRACE_web.mxd")
##        mxdpub = arcpy.mapping.MapDocument(mxddir+"GRACE_pub.mxd")
##        graceimg = arcpy.mapping.Layer(fpimg)
##        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
##        arcpy.mapping.AddLayer(df, graceimg,"BOTTOM")
##        graceLayer =arcpy.mapping.ListLayers(mxd, "*perc_0125deg_US*", df)
##        for mapLayer in graceLayer:
##            arcpy.ApplySymbologyFromLayer_management (mapLayer, reglyr)
##        # Change the layout text
##        mapdate = (arcpy.mapping.ListLayoutElements(mxd,"TEXT_ELEMENT","MapDate"))[0]
##        mapdate.text = thetextdate
##        arcpy.mapping.ExportToPDF(mxd,outdir+isodate+"\\GRACE_"+ thetype.upper()+"_"+isodate+".pdf",resolution=res)
##        arcpy.mapping.ExportToPNG(mxd,outdir+isodate+"\\GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
##        dfw = arcpy.mapping.ListDataFrames(mxdweb, "Layers")[0]
##        arcpy.mapping.AddLayer(dfw, graceimg,"BOTTOM")
##        graceLayerw =arcpy.mapping.ListLayers(mxdweb, "*perc_0125deg_US*", dfw)
##        for mapLayerw in graceLayerw:
##            arcpy.ApplySymbologyFromLayer_management (mapLayerw, reglyr)
##        arcpy.mapping.ExportToPNG(mxdweb,webdir+"GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
##        ## NASA Pub Maps
##        dfp = arcpy.mapping.ListDataFrames(mxdpub, "Layers")[0]
##        arcpy.mapping.AddLayer(dfp, graceimg,"BOTTOM")
##        graceLayerp =arcpy.mapping.ListLayers(mxdpub, "*perc_0125deg_US*", dfp)
##        for mapLayerp in graceLayerp:
##            arcpy.ApplySymbologyFromLayer_management (mapLayerp, publyr)
##        arcpy.mapping.ExportToPNG(mxdpub,pubdir+"maps\\GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
##    elif thetype=="rtzsm":
##        print "Processing "+thetype+" maps"
##        mxd = arcpy.mapping.MapDocument(mxddir+"GRACE_RTZSM_automated.mxd")
##        mxdweb = arcpy.mapping.MapDocument(mxddir+"GRACE_web.mxd")
##        mxdpub = arcpy.mapping.MapDocument(mxddir+"GRACE_pub.mxd")
##        graceimg = arcpy.mapping.Layer(fpimg)
##        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
##        arcpy.mapping.AddLayer(df, graceimg,"BOTTOM")
##        graceLayer =arcpy.mapping.ListLayers(mxd, "*perc_0125deg_US*", df)
##        for mapLayer in graceLayer:
##            arcpy.ApplySymbologyFromLayer_management (mapLayer, reglyr)
##        # Change the layout text
##        mapdate = (arcpy.mapping.ListLayoutElements(mxd,"TEXT_ELEMENT","MapDate"))[0]
##        mapdate.text = thetextdate
##        arcpy.mapping.ExportToPDF(mxd,outdir+isodate+"\\GRACE_"+ thetype.upper()+"_"+isodate+".pdf",resolution=res)
##        arcpy.mapping.ExportToPNG(mxd,outdir+isodate+"\\GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
##        dfw = arcpy.mapping.ListDataFrames(mxdweb, "Layers")[0]
##        arcpy.mapping.AddLayer(dfw, graceimg,"BOTTOM")
##        graceLayerw =arcpy.mapping.ListLayers(mxdweb, "*perc_0125deg_US*", dfw)
##        for mapLayerw in graceLayerw:
##            arcpy.ApplySymbologyFromLayer_management (mapLayerw, reglyr)
##        arcpy.mapping.ExportToPNG(mxdweb,webdir+"GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
##        ## NASA Pub Maps
##        dfp = arcpy.mapping.ListDataFrames(mxdpub, "Layers")[0]
##        arcpy.mapping.AddLayer(dfp, graceimg,"BOTTOM")
##        graceLayerp =arcpy.mapping.ListLayers(mxdpub, "*perc_0125deg_US*", dfp)
##        for mapLayerp in graceLayerp:
##            arcpy.ApplySymbologyFromLayer_management (mapLayerp, publyr)
##        arcpy.mapping.ExportToPNG(mxdpub,pubdir+"maps\\GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
##    elif thetype=="sfsm":
##        print "Processing "+thetype+" maps"
##        mxd = arcpy.mapping.MapDocument(mxddir+"GRACE_SFSM_automated.mxd")
##        mxdweb = arcpy.mapping.MapDocument(mxddir+"GRACE_web.mxd")
##        mxdpub = arcpy.mapping.MapDocument(mxddir+"GRACE_pub.mxd")
##        graceimg = arcpy.mapping.Layer(fpimg)
##        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
##        arcpy.mapping.AddLayer(df, graceimg,"BOTTOM")
##        graceLayer =arcpy.mapping.ListLayers(mxd, "*perc_0125deg_US*", df)
##        for mapLayer in graceLayer:
##            arcpy.ApplySymbologyFromLayer_management (mapLayer, reglyr)
##        # Change the layout text
##        mapdate = (arcpy.mapping.ListLayoutElements(mxd,"TEXT_ELEMENT","MapDate"))[0]
##        mapdate.text = thetextdate
##        arcpy.mapping.ExportToPDF(mxd,outdir+isodate+"\\GRACE_"+ thetype.upper()+"_"+isodate+".pdf",resolution=res)
##        arcpy.mapping.ExportToPNG(mxd,outdir+isodate+"\\GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
##        dfw = arcpy.mapping.ListDataFrames(mxdweb, "Layers")[0]
##        arcpy.mapping.AddLayer(dfw, graceimg,"BOTTOM")
##        graceLayerw =arcpy.mapping.ListLayers(mxdweb, "*perc_0125deg_US*", dfw)
##        for mapLayerw in graceLayerw:
##            arcpy.ApplySymbologyFromLayer_management (mapLayerw, reglyr)
##        arcpy.mapping.ExportToPNG(mxdweb,webdir+"GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
##        ## NASA Pub Maps
##        dfp = arcpy.mapping.ListDataFrames(mxdpub, "Layers")[0]
##        arcpy.mapping.AddLayer(dfp, graceimg,"BOTTOM")
##        graceLayerp =arcpy.mapping.ListLayers(mxdpub, "*perc_0125deg_US*", dfp)
##        for mapLayerp in graceLayerp:
##            arcpy.ApplySymbologyFromLayer_management (mapLayerp, publyr)
##        arcpy.mapping.ExportToPNG(mxdpub,pubdir+"maps\\GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
##    else:
##        print "Unrecognised Type"
    print "Cleaning up work files."
    os.remove(workfile)
    arcpy.Delete_management(fltwork)
    arcpy.Delete_management(rtif)
    arcpy.Delete_management(ftif)
    arcpy.Delete_management(fimg)
