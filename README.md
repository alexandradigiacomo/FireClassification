# FireClassification

## Overview

This repository contains scripts developed to estimate forest burn area from Unoccupied Aircraft System (UAS) imagery. The project is conducted as part of the Environmental Security Technology Certification Program (ESTCP) within the Marine Robotics and Remote Sensing Laboratory at Duke University.

The primary script, `FireClassification.py`, can be integrated into ArcGIS to create a user-friendly geoprocessing tool.

## Inputs

The tool requires the following inputs:

- **Orthomosaic** derived from UAS imagery  
- **Digital Surface Model (DSM)** generated from UAS imagery  
- **Manually identified ground points**  

The orthomosaic and DSM are produced through Structure-from-Motion (SfM) processing workflows using software such as Pix4D or Agisoft Metashape.

## Workflow

The ArcGIS graphical user interface (GUI) guides the user through the following steps:

1. Identification of 10–30 ground points using the orthomosaic.
2. Filtering of low-lying vegetation in the DSM using elevations derived from manually identified ground points.
3. Masking of low vegetation in the corresponding orthomosaic.
4. Computation of relationships between optical indices to distinguish burned from non-burned areas.

## Output

The tool produces a **binary classification raster** that delineates:

- Burned areas  
- Non-burned areas  
