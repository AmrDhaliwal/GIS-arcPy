# Setup
This script can only be used if ArcGIS is downloaded on the host computer
because, arcPy the library needed to create a feature class and insert
the extracted data into a Geodatabase. If ArcGIS is installed then the script
can be used. Please see the requirements.txt file for the libraries. Listed below
are changes that will be needed for the script so it works for you.

* In line 8 change the workpath destination to one that works for you.
* Create a geodatabse and insert the file path into line 9 and replace it with 'Venting_Index.gdb'.
* Line 14 you can change the name of the feature class to something that works better for you.
* In line 21 replace 'Venting_Index.kml' with your own path to a KML file.
* In lines 28 and 29 change the outlocation path and change the path of the master Geodatabase.

Once the appropriate changes have been made run the script and it will create the feature class
and extract the data from the KML file.
