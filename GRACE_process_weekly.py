# ---------------------------------------------------------------------------
# GRACE_process_weekly.py
# Created on: 2014-11-20
# Description: Downloads and converts GRACE data products and produces a
# variety of maps
# ---------------------------------------------------------------------------

from ftplib import FTP
import shutil
import time
import os
import datetime
from datetime import date
from datetime import timedelta
import arcpy
##########################################################
##  Returns the the monday associated with the .bin file
##########################################################
def monday(delta):
    # Get today.
    today = date.today()
    # Subtract time-delta of 1 day.
    processday = today - timedelta(days=delta)
    return processday
###########################################################
## Gets the offset days base of the day the script runs
###########################################################
def thedelta(day):
    if day == 'Tue':
        delta = 1
    elif day=='Wed':
        delta = 2
    elif day == 'Thu':
        delta = 3
    elif day=='Fri':
        delta = 4
    elif day == 'Sat':
        delta = 5
    elif day == 'Sun':
        delta = 6
    elif day == 'Mon':
        delta = 7
    else:
        delta = -9999
    return delta
###########################################################
## Copy File to production
###########################################################
def copyFile (src, dest):
    try:
        shutil.copyfile(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('File not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('File not copied. Error: %s' % e)
###########################################################
## Copy Directory to the production
###########################################################
def copyDirectory(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)
###########################################################
## Start of Processing
###########################################################
sday = time.strftime("%a")
sdelta = thedelta(sday)
thedate = (monday(sdelta))
isodate = thedate.strftime("%Y"+"%m"+"%d")
## Full date for use in maps
thetextdate = thedate.strftime("%B %d, %Y")
res = 300
## Set up the FTP session
ftp = FTP("128.183.163.40")
ftp.login()
ftp.cwd('/pub/DM/RT_run/')
filedate = (((ftp.sendcmd('MDTM ' + 'sfsm_perc_0125deg_US.bin')).split(" "))[1])[0:8]
## Check to see if the file is the correct date based on the timestamp
print "Checking file date..." 
while isodate > filedate: # first while loop code
    print "The file date "+filedate+" is older than this weeks pull date "+isodate
    print "Waiting 30 minutes to retry the retrieval..."
    time.sleep(1800) 
    filedate = (((ftp.sendcmd('MDTM ' + 'sfsm_perc_0125deg_US.bin')).split(" "))[1])[0:8]
print "File date "+filedate+" correct, proceeding with process."
## Operational Directories
##webarchive = "\\\\seca\\e\\web_archive\\NASA\\GRACE\\"
##webcurrent = "\\\\sucho\\E\\Web\\Drought\\nasa_grace\\"
##nasapub = "\\\\seca\\e\\web_archive\\NASA\\GRACE\\NASApublication\\"
##webmaparchive = "\\\\sucho\\web\\Drought\\archive\\NASA\\GRACE\\"
##webmaparchive2 = "\\\\seca\\e\\web_archive\\NASA\\GRACE\\Web\\"
webarchive = "C:\\GRACEGroundwaterEval\\Operational\\ndmc-005\\web_data\\NASA\\GRACE\\"
webcurrent = "C:\\GRACEGroundwaterEval\\Operational\\ndmc-005\\web\\Drought\\nasa_grace\\"
nasapub = "C:\\GRACEGroundwaterEval\\Operational\\ndmc-005\\web_data\\NASA\\GRACE\\NASApublication\\"
webmaparchive = "C:\\GRACEGroundwaterEval\\Operational\\ndmc-005\\web\\Drought\\archive\\NASA\\GRACE\\"
webmaparchive2 = "C:\\GRACEGroundwaterEval\\Operational\\ndmc-005\\web_data\\NASA\\GRACE\\Web\\"
## Production Directories
outdir = "C:\\GRACEGroundwaterEval\\Operational\\ndmc-005\\Production\\GRACE\\output\\Archive\\"
currentdir = "C:\\GRACEGroundwaterEval\\Operational\\ndmc-005\\Production\\GRACE\\output\\Current\\"
webdir = "C:\\GRACEGroundwaterEval\\Operational\\ndmc-005\\Production\\GRACE\\output\\Web\\"
pubdir = "C:\\GRACEGroundwaterEval\\Operational\\ndmc-005\\Production\\GRACE\\output\\NASApublication\\"
workdir = "C:\\GRACEGroundwaterEval\\Operational\\ndmc-005\\Production\\GRACE\\working\\"
mxddir = "C:\\GRACEGroundwaterEval\\Operational\\ndmc-005\\Production\\GRACE\\BaseData\\mxds\\"
layerdir = "C:\\GRACEGroundwaterEval\\Operational\\ndmc-005\\Production\\GRACE\\BaseData\\Files\\"
## Set Global Constants
Projection = "C:\\GRACEGroundwaterEval\\Operational\\ndmc-005\\Production\\GRACE\\BaseData\\Files\\RasterProjection.tif"
Header = "C:\\GRACEGroundwaterEval\\Operational\\ndmc-005\\Production\\GRACE\\BaseData\\Files\\template2.hdr"
TFW = "C:\\GRACEGroundwaterEval\\Operational\\ndmc-005\\Production\\GRACE\\BaseData\\Files\\.tfw"
FinalPRJ = "C:\\GRACEGroundwaterEval\\Operational\\ndmc-005\\Production\\GRACE\\Basedata\\Shapes\\Conus_Mask.prj"
thebinaries = ["gws_perc_0125deg_US","rtzsm_perc_0125deg_US","sfsm_perc_0125deg_US"]
arcpy.env.overwriteOutput = True
if not os.path.exists(outdir+isodate):
    os.makedirs(outdir+isodate)
for bin in thebinaries:
    # Set the current workspace
    arcpy.env.workspace = workdir
    print "Retrieving bin file "+bin
    thetype = bin.split("_")[0]
    print thetype
    localfile = outdir+isodate+"\\"+bin+"_"+isodate+".bin"
    ftp.retrbinary('RETR '+bin+'.bin', open(localfile, 'wb').write)
    workfile = workdir+bin+"_"+isodate+".bin"
    fltwork = workdir+bin+"_"+isodate+".flt"
    binhdr = workdir+bin+"_"+isodate+".hdr"
    rtif = workdir+bin+"_"+isodate+"_raw.tif"
    ftif = workdir+bin+"_"+isodate+".tif"
    ftfw = workdir+bin+"_"+isodate+".tfw"
    fimg = workdir+bin+"_"+isodate+".img"
    fpimg = outdir+isodate+"\\"+bin+"_"+isodate+".img"
    fptif = outdir+isodate+"\\"+bin+"_"+isodate+".tif"
    fptfw = outdir+isodate+"\\"+bin+"_"+isodate+".tfw"
    shutil.copyfile(outdir+isodate+"\\"+bin+"_"+isodate+".bin", workfile)
    shutil.copyfile(outdir+isodate+"\\"+bin+"_"+isodate+".bin", fltwork)
    shutil.copyfile(outdir+isodate+"\\"+bin+"_"+isodate+".bin",pubdir+"\\data\\"+bin+"_"+isodate+".bin")
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
    arcpy.ProjectRaster_management (fimg, fpimg, FinalPRJ, "NEAREST", 14225.65114, "NAD_1983_To_WGS_1984_1")
##  Mapping the data
    ## Set the path for the layer files
    publyr = layerdir+"GRACE_Red2Blue_img.lyr"
    reglyr = layerdir+"GRACE_WebColors_img.lyr"
    if thetype=="gws":
        print "Processing "+thetype+" maps"
        mxd = arcpy.mapping.MapDocument(mxddir+"GRACE_GWS_automated2.mxd")
        mxdweb = arcpy.mapping.MapDocument(mxddir+"GRACE_web.mxd")
        mxdpub = arcpy.mapping.MapDocument(mxddir+"GRACE_pub.mxd")
        graceimg = arcpy.mapping.Layer(fpimg)
        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
        arcpy.mapping.AddLayer(df, graceimg,"BOTTOM")
        graceLayer =arcpy.mapping.ListLayers(mxd, "*perc_0125deg_US*", df)
        for mapLayer in graceLayer:
            arcpy.ApplySymbologyFromLayer_management (mapLayer, reglyr)
        # Change the layout text
        mapdate = (arcpy.mapping.ListLayoutElements(mxd,"TEXT_ELEMENT","MapDate"))[0]
        mapdate.text = thetextdate
        arcpy.mapping.ExportToPDF(mxd,currentdir+"GRACE_"+ thetype.upper()+".pdf",resolution=res)
        arcpy.mapping.ExportToPNG(mxd,currentdir+"GRACE_"+ thetype.upper()+".png",resolution=res)
        arcpy.mapping.ExportToPDF(mxd,outdir+isodate+"\\GRACE_"+ thetype.upper()+"_"+isodate+".pdf",resolution=res)
        arcpy.mapping.ExportToPNG(mxd,outdir+isodate+"\\GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
        dfw = arcpy.mapping.ListDataFrames(mxdweb, "Layers")[0]
        arcpy.mapping.AddLayer(dfw, graceimg,"BOTTOM")
        graceLayerw =arcpy.mapping.ListLayers(mxdweb, "*perc_0125deg_US*", dfw)
        for mapLayerw in graceLayerw:
            arcpy.ApplySymbologyFromLayer_management (mapLayerw, reglyr)
        arcpy.mapping.ExportToPNG(mxdweb,webdir+"GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
        ## NASA Pub Maps
        dfp = arcpy.mapping.ListDataFrames(mxdpub, "Layers")[0]
        arcpy.mapping.AddLayer(dfp, graceimg,"BOTTOM")
        graceLayerp =arcpy.mapping.ListLayers(mxdpub, "*perc_0125deg_US*", dfp)
        for mapLayerp in graceLayerp:
            arcpy.ApplySymbologyFromLayer_management (mapLayerp, publyr)
        arcpy.mapping.ExportToPNG(mxdpub,pubdir+"maps\\GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
    elif thetype=="rtzsm":
        print "Processing "+thetype+" maps"
        mxd = arcpy.mapping.MapDocument(mxddir+"GRACE_RTZSM_automated2.mxd")
        mxdweb = arcpy.mapping.MapDocument(mxddir+"GRACE_web.mxd")
        mxdpub = arcpy.mapping.MapDocument(mxddir+"GRACE_pub.mxd")
        graceimg = arcpy.mapping.Layer(fpimg)
        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
        arcpy.mapping.AddLayer(df, graceimg,"BOTTOM")
        graceLayer =arcpy.mapping.ListLayers(mxd, "*perc_0125deg_US*", df)
        for mapLayer in graceLayer:
            arcpy.ApplySymbologyFromLayer_management (mapLayer, reglyr)
        # Change the layout text
        mapdate = (arcpy.mapping.ListLayoutElements(mxd,"TEXT_ELEMENT","MapDate"))[0]
        mapdate.text = thetextdate
        arcpy.mapping.ExportToPDF(mxd,currentdir+"GRACE_"+ thetype.upper()+".pdf",resolution=res)
        arcpy.mapping.ExportToPNG(mxd,currentdir+"GRACE_"+ thetype.upper()+".png",resolution=res)
        arcpy.mapping.ExportToPDF(mxd,outdir+isodate+"\\GRACE_"+ thetype.upper()+"_"+isodate+".pdf",resolution=res)
        arcpy.mapping.ExportToPNG(mxd,outdir+isodate+"\\GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
        dfw = arcpy.mapping.ListDataFrames(mxdweb, "Layers")[0]
        arcpy.mapping.AddLayer(dfw, graceimg,"BOTTOM")
        graceLayerw =arcpy.mapping.ListLayers(mxdweb, "*perc_0125deg_US*", dfw)
        for mapLayerw in graceLayerw:
            arcpy.ApplySymbologyFromLayer_management (mapLayerw, reglyr)
        arcpy.mapping.ExportToPNG(mxdweb,webdir+"GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
        ## NASA Pub Maps
        dfp = arcpy.mapping.ListDataFrames(mxdpub, "Layers")[0]
        arcpy.mapping.AddLayer(dfp, graceimg,"BOTTOM")
        graceLayerp =arcpy.mapping.ListLayers(mxdpub, "*perc_0125deg_US*", dfp)
        for mapLayerp in graceLayerp:
            arcpy.ApplySymbologyFromLayer_management (mapLayerp, publyr)
        arcpy.mapping.ExportToPNG(mxdpub,pubdir+"maps\\GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
    elif thetype=="sfsm":
        print "Processing "+thetype+" maps"
        mxd = arcpy.mapping.MapDocument(mxddir+"GRACE_SFSM_automated2.mxd")
        mxdweb = arcpy.mapping.MapDocument(mxddir+"GRACE_web.mxd")
        mxdpub = arcpy.mapping.MapDocument(mxddir+"GRACE_pub.mxd")
        graceimg = arcpy.mapping.Layer(fpimg)
        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
        arcpy.mapping.AddLayer(df, graceimg,"BOTTOM")
        graceLayer =arcpy.mapping.ListLayers(mxd, "*perc_0125deg_US*", df)
        for mapLayer in graceLayer:
            arcpy.ApplySymbologyFromLayer_management (mapLayer, reglyr)
        # Change the layout text
        mapdate = (arcpy.mapping.ListLayoutElements(mxd,"TEXT_ELEMENT","MapDate"))[0]
        mapdate.text = thetextdate
        arcpy.mapping.ExportToPDF(mxd,currentdir+"GRACE_"+ thetype.upper()+".pdf",resolution=res)
        arcpy.mapping.ExportToPNG(mxd,currentdir+"GRACE_"+ thetype.upper()+".png",resolution=res)
        arcpy.mapping.ExportToPDF(mxd,outdir+isodate+"\\GRACE_"+ thetype.upper()+"_"+isodate+".pdf",resolution=res)
        arcpy.mapping.ExportToPNG(mxd,outdir+isodate+"\\GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
        dfw = arcpy.mapping.ListDataFrames(mxdweb, "Layers")[0]
        arcpy.mapping.AddLayer(dfw, graceimg,"BOTTOM")
        graceLayerw =arcpy.mapping.ListLayers(mxdweb, "*perc_0125deg_US*", dfw)
        for mapLayerw in graceLayerw:
            arcpy.ApplySymbologyFromLayer_management (mapLayerw, reglyr)
        arcpy.mapping.ExportToPNG(mxdweb,webdir+"GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
        ## NASA Pub Maps
        dfp = arcpy.mapping.ListDataFrames(mxdpub, "Layers")[0]
        arcpy.mapping.AddLayer(dfp, graceimg,"BOTTOM")
        graceLayerp =arcpy.mapping.ListLayers(mxdpub, "*perc_0125deg_US*", dfp)
        for mapLayerp in graceLayerp:
            arcpy.ApplySymbologyFromLayer_management (mapLayerp, publyr)
        arcpy.mapping.ExportToPNG(mxdpub,pubdir+"maps\\GRACE_"+ thetype.upper()+"_"+isodate+".png",resolution=res)
    else:
        print "Unrecognised Type"

    print "Cleaning up work files."
    os.remove(workfile)
    arcpy.Delete_management(fltwork)
    arcpy.Delete_management(rtif)
    arcpy.Delete_management(ftif)
    arcpy.Delete_management(fimg)
## Copy the files to the production side
copyDirectory(outdir+isodate, webarchive+isodate)
thetypos = ['gws','rtzsm','sfsm']
for typo in thetypos:
    ## NASA publication maps
    srcppng = pubdir+"maps\\GRACE_"+ typo.upper()+"_"+isodate+".png"
    dstppng = nasapub+"maps\\GRACE_"+ typo.upper()+"_"+isodate+".png"
    copyFile(srcppng,dstppng)
    ## NASA Publication Binaries
    srcpbin = pubdir+"data\\"+typo+"_perc_0125deg_US_"+isodate+".bin"
    dstpbin = nasapub+"data\\"+typo+"_perc_0125deg_US_"+isodate+".bin"
    copyFile(srcpbin,dstpbin)
    ## Web Maps current
    srcppng = currentdir+"GRACE_"+ typo.upper()+".png"
    dstppng = webcurrent+"GRACE_"+ typo.upper()+".png"
    srcppdf = currentdir+"GRACE_"+ typo.upper()+".pdf"
    dstppdf = webcurrent+"GRACE_"+ typo.upper()+".pdf"
    copyFile(srcppng,dstppng)
    copyFile(srcppdf,dstppdf)
    ## Web Maps archive viewer 
    srcapng =webdir+"GRACE_"+ typo.upper()+"_"+isodate+".png"
    dstapng = webmaparchive2+"GRACE_"+ typo.upper()+"_"+isodate+".png"
    copyFile(srcapng,dstapng)
    ## Web Maps archive viewer 
    dstapng2 = webmaparchive2+"GRACE_"+ typo.upper()+"_"+isodate+".png"
    copyFile(srcapng,dstapng2)
