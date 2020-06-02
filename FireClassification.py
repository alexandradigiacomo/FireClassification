##-------------------------------------------
## FireClassification.py
## too built for MarineUAS ESTCP Project Summer 2020
## Description: Classification of Fire Burn Area
## Created: Summer 2019
## Author: Alexandra DiGiacomo (alexandraedigiacomo@gmail.com)
##-------------------------------------------
###

#import modules
import arcpy, os, sys
arcpy.CheckOutExtension("Spatial")
from arcpy.sa import *
import arcpy.mp

import pandas as pd
import numpy as np

#set relative paths
scriptPath = sys.argv[0]
scriptWS = os.path.dirname(scriptPath) #gives you script folder
rootWS = os.path.dirname(scriptWS) #goes up one folder into project folder
dataWS = os.path.join(rootWS, "data") #go into data folder from project folder'
resultsWS = os.path.join(rootWS, "results") #go into results folder from project folder

mxd = arcpy.mp.ArcGISProject("CURRENT")
mxd.relativePaths = True

#set environmental variables
arcpy.env.workspace = dataWS # arc environment is the data folder
arcpy.env.overwriteOutput = True # overwrite outputs: yes

##USER INPUTS
scratchWS = arcpy.GetParameterAsText(0) #this is the path to the desired scratch folder
arcpy.env.scratchWorkspace = scratchWS #set the environmental variable for the scratch folder after knowing the scratch folder

#input files
inputORTHO = arcpy.GetParameterAsText(1) #the input orthomosaic file
inputDSM = arcpy.GetParameterAsText(2) #the input dsm file

#terrain points
terrainPoints = arcpy.GetParameterAsText(3) #ground points that will be averaged later

#prefix to be attached to results file
#resultName = arcpy.GetParameterAsText(4)

##-------------------------------------------
# Part 1: Terrain Development
terr = scratchWS + "\\terr.shp"
ExtractValuesToPoints(terrainPoints, inputDSM, terr, "NONE", "VALUE_ONLY") # get elevation value at each points
arcpy.Statistics_analysis(terr, scratchWS + "\\terrainvalues.csv", [["RASTERVALU", "MAX"]], "") # extract max terrain height
arcpy.AddMessage("terrain values made table")

terr_table_loc = scratchWS + "\\terrainvalues.csv" # location of table of max terrain dsm val
terr_table =  pd.read_csv(terr_table_loc) # read in terr_table
maxterr = terr_table.iloc[0]['MAX_RASTERVALU'] # extract just the max raster value (elevation)

arcpy.AddMessage("Ground threshold is {val}".format(val = maxterr))

## 1A: Make DSM Mask of Low Terrain Values (without high veg)
inSQLClause = "VALUE < {val}".format(val = maxterr) # filter for dsm values lower than highest input terrain
dsm_terrain = scratchWS + "\\dsm_terrain.tif"
dsmTerr = ExtractByAttributes(inputDSM, inSQLClause) # create filtered dsm
dsmTerr.save(dsm_terrain) # save to scratch workspace

arcpy.AddMessage("DSM Terrain Mask Created")

# 1B: Mask Orthomosaic to extent of terrain/low veg raster created in 1A
orthoFilt = scratchWS + "\\ortho_filtveg.tif"
outExtractByMask = ExtractByMask(inputORTHO, dsmTerr)
outExtractByMask.save(orthoFilt)

arcpy.AddMessage("Orthomosaic Clipped to Terrain Extent")

##-------------------------------------------
## Part 2: Filter Based on RGB Vals

# Make individual rasters for each band: Red, Green, Blue
redRast = scratchWS + "\\redRaster.tif"
greenRast = scratchWS + "\\greenRaster.tif"
blueRast = scratchWS + "\\blueRaster.tif"

arcpy.MakeRasterLayer_management(orthoFilt, redRast, band_index = "1")
arcpy.MakeRasterLayer_management(orthoFilt, greenRast, band_index = "2")
arcpy.MakeRasterLayer_management(orthoFilt, blueRast, band_index = "3")

arcpy.AddMessage("Individual Band Rasters Generated")


# Look at area where Green > Red & Green > Blue
highGreen = scratchWS + "\\highGreen.tif"
RasterCalculator(("greenRast" > "redRast") & ("greenRast" > "blueRast"), highGreen)
