# ##
# Description: Python code to calculate correlation coefficients between two raster datasets
# Author: Anthony Mucia
# Date: May 2018
# Notes: This code is based around a community answer by ESRI Community user Xander Bakker
# https://community.esri.com/thread/200534-re-correlation-between-two-different-rasters
# ##

def main():
    import arcpy, glob, winsound, os
    import numpy as np
    import numpy.ma as ma
    import pandas as pd
    arcpy.env.overwriteOutput = True
    dataPath1 = r'I:\Data\GRACE\Reprojected\AlbertEqualAreaNAD1983\Nearest\Levels\Seasonal\rtzsm\New\All\2012'
    dataPath2 = r'I:\Data\USDM\GRACE_Grid\Seasonal\2012'
    L1 = glob.glob(dataPath1+'\*.tif')
    L2 = glob.glob(dataPath2+'\*.tif')

    nodata = -999
    out_ras = r'I:\Research\GRACE\Correlations\Spearman\USDM/rzsm_usdm_S_levels_complete_2012.tif'
    outDataPath = r'I:\Research\GRACE\Correlations\Spearman\USDM/'
    print("         List 1 Raster Count = "+str(len(L1)))
    print("         List 2 Raster Count = "+str(len(L2)))

    L1 = sorted(L1)
    L2 = sorted(L2)

    print "Creating arrays..."
    lst_np_ras = []
    for i in range(0, len(L1)):
        ras_path1 = L1[i]
        print " - ", ras_path1
        ras_np1 = arcpy.RasterToNumPyArray(ras_path1)
        ras_path2 = L2[i]
        print " - ", ras_path2
        ras_np2 = arcpy.RasterToNumPyArray(ras_path2)
        lst_np_ras.append([ras_np1, ras_np2])

    print "Reading numPy rasters..."
    ras_np = lst_np_ras[0][0]
    rows = ras_np.shape[0]
    cols = ras_np.shape[1]
    print " - rows:", rows
    print " - cols:", cols

    print "Creating output numPy array..."
    ras_path = L1[0]
    raster = arcpy.Raster(ras_path)
    ras_np_res = np.ndarray((rows, cols))
    ras_np_res2 = np.ndarray((rows, cols))
    print " - rows:", ras_np_res.shape[0]
    print " - cols:", ras_np_res.shape[1]

    print "Looping through pixels..."
    pix_cnt = 0
    for row in range(rows):
        for col in range(cols):
            pix_cnt += 1
            if pix_cnt % 5000 == 0:
                print " - row:", row, "  col:", col, "  pixel:", pix_cnt
            lst_vals1 = []
            lst_vals2 = []
            try:
                for lst_pars in lst_np_ras:
                    lst_vals1.append(lst_pars[0][row, col])
                    lst_vals2.append(lst_pars[1][row, col])
                lst_vals1 = ReplaceNoData(lst_vals1, nodata)
                lst_vals2 = ReplaceNoData(lst_vals2, nodata)
                correlation = SpearmanCorrelation(lst_vals1, lst_vals2, nodata)
                ras_np_res[row, col] = correlation
            except Exception as e:
                print "ERR:", e
                print " - row:", row, "  col:", col, "  pixel:", pix_cnt
                print " - lst_vals1:", lst_vals1
                print " - lst_vals2:", lst_vals2

    pnt = arcpy.Point(raster.extent.XMin, raster.extent.YMin)
    xcellsize = raster.meanCellWidth
    ycellsize = raster.meanCellHeight
    dsc = arcpy.Describe(L1[0])
    coord_sys = dsc.spatialReference

    print "Writing output raster..."
    print " - ", out_ras
    ras_res = arcpy.NumPyArrayToRaster(ras_np_res, lower_left_corner=pnt, x_cell_size=xcellsize,
                                 y_cell_size=ycellsize, value_to_nodata=nodata)
    ras_res.save(out_ras)
    arcpy.DefineProjection_management(in_dataset=out_ras, coor_system=coord_sys)
    print("Cleaning up work files...")
    FileCleanup(outDataPath)
    print ("Complete")

def FileCleanup(path):
    import os, glob, winsound
    file_name = os.listdir(path)
    for item in file_name:
      if item.endswith(".xml") or item.endswith(".tfw") or item.endswith(".ovr"):
          os.remove(os.path.join(path, item))
    winsound.Beep(1000,1000)

def PearsonCorrelation(a, b, nodata):
    import numpy
    try:
        coef = numpy.corrcoef(a,b)
        return coef[0][1]
    except:
        return nodata

def SpearmanCorrelation(a, b, nodata):
    import pandas as pd
    try:
        a = pd.Series(a)
        b = pd.Series(b)
        coef = a.corr(b,method = "spearman")
        return coef
    except:
        return nodata

def ReplaceNoData(lst, nodata):
    res = []
    for a in lst:
        if a == nodata:
            res.append(None)
        else:
            res.append(a)
    return res

if __name__ == '__main__':
    main()
