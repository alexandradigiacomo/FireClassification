# FireClassification
ESTCP project to understand forest burn area from UAS imagery.

Orthomosaic rasters uploaded to Duke Box due to github file size limitations. 
Fire Surveys (1 and 2): https://duke.app.box.com/folder/113625452147

Method 1: Python script (ArcPy interface) developed to filter out high vegetation values from the DSM and mask the ortho accordingly 

Method 2: Pick distinguishifiable points from 01 Pix4D point cloud (with mesh) and create 3D gcps for 02 Pix4D project (with XYZ input from 01). Reoptimize 02. This is to pull up both orthos to be on the same plane - so that we can subtract the DTMs / DSMs 
