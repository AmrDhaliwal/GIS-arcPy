# -*- coding: utf-8 -*-

import arcpy
from pykml import parser
from os import path

# input_data  = arcpy.GetParameterAsText(0)
work_path = r'C:\Users\Amrit\PycharmProjects\pyKMLProject'
out_gdb = path.join(work_path, 'Venting_Index.gdb')
print('out path and gdb: {0}'.format(out_gdb))

# create empty Feature Class
overwriteFC = True
e = 'extended_data_pulled'
if not arcpy.Exists(path.join(out_gdb, e)) or overwriteFC:
    sr = arcpy.SpatialReference(4326)
    arcpy.CreateFeatureclass_management(out_gdb, e, 'POLYGON', '#', '#', '#', sr)

# parse Venting_Index.kml
nmsp = '{http://www.opengis.net/kml/2.2}'
kml_file = path.join(work_path, 'Venting_Index.kml')

# Set workspace
arcpy.env.workspace = out_gdb
arcpy.env.overwriteOutput = True

# Set local variables and location for the consolidated file database
# outLocation = "C:\Users\Amrit\PycharmProjects\pyKMLProject"
# MasterGDB = 'Venting_Index.gdb'
# MasterGDBLocation = path.join(outLocation, MasterGDB)

# Create the master FileDatabase
# arcpy.CreateFileGDB_management(outLocation, MasterGDB)

# Change the workspace to fGDB location
# arcpy.env.workspace = outLocation

# wks = arcpy.ListWorkspaces('*', 'FileGDB')
# wks.remove(MasterGDBLocation)

# Change the workspace to the current FileDatabase
# arcpy.env.workspace = fgdb

# Use the pyKML library to parse the kml file
with open(kml_file) as f:
    doc = parser.parse(f).getroot()

# for loop to list feature classes
for fds in arcpy.ListDatasets('', 'feature') + ['']:
    for fc in arcpy.ListFeatureClasses('', '', fds):
        print(path.join(arcpy.env.workspace, fds, fc))

# Automate adding fields
currentFields = arcpy.ListFields(e)
fields = []
for simple in doc.findall('.//{0}Schema/{0}SimpleField'.format(nmsp)):
    fieldType = simple.attrib['type']
    fieldName = simple.attrib['name']
    arcpy.AddField_management(e, fieldName, fieldType)
    fields.append(simple.attrib['name'])

# add SHAPE@ to fields list
fields.append('SHAPE@')
print(fields)

# Create an insert cursor
cursor = arcpy.da.InsertCursor(e, fields)
# Placemarkers contains the extended data that we are parsing for
Placemarkers = doc.findall(".//{0}Placemark".format(nmsp))
for Placemarker in Placemarkers:
    # final geometry array
    final_geoms = arcpy.Array()
    print(Placemarker.tag)
    # placeData contains the fully parsed data
    placeData = Placemarker.findall('.//{0}ExtendedData/{0}SchemaData/{0}SimpleData'.format(nmsp))

    # geoms is coordinates pulled from the kml file
    geoms = Placemarker.findall(
        './/{0}MultiGeometry/{0}Polygon/{0}outerBoundaryIs/{0}LinearRing/{0}coordinates'.format(nmsp))
    # turn geoms into a string and split at the coordinate spaces
    for geom in geoms:
        # an array for parts of geoms
        part_array = arcpy.Array()

        # Loop through geom to create xy coordinates
        for xy in str(geom).split(" "):
            xy_split = xy.split(',')
            X = float(xy_split[0])
            Y = float(xy_split[1])
            # make X and Y into points and add to part_array
            point = arcpy.Point(X, Y)
            part_array.add(point)

        # add part_array to final_geoms
        final_geoms.add(part_array)
    # create Polygon objects and append to placeDate
    placeData.append(arcpy.Polygon(final_geoms))
    try:
        print(placeData)
        cursor.insertRow(placeData)
        # print('.')
    except Exception as e:
        # print('error: {0}'.format(e))
        pass

# Delete cursor object
del cursor

# -------------------------------------------------------------------------------
# Name: KML EXTRACTION USING PYKML
#
# Purpose: To parse KML files and pull data inaccessible to ESRI software
#
# Author: Amrit Dhaliwal
#
# Created: March, 22, 2021
#
# -------------------------------------------------------------------------------
