# KML file extraction of Polygon data
The purpose of this project was to pull Polygon data from a
File Geodatabase(.gdb) created by the software ESRI. By using the 
pyKML and arcPy libraries the Polygon data was able to 
succesfully extracted and the data was succesfully exported
to another Geodatabase.

# Setup
This script can only be used if ArcGIS is downloaded on the host computer
because, arcPy the library needed to create a feature class and insert
the extracted data into a Geodatabase. If ArcGIS is installed then the script
can be used. Please see the requirements.txt file for the libraries.
## Please be aware this script was built using Python 2
