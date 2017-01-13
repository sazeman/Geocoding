# Import system modules
import arcpy
import csv

# Set workspace
arcpy.env.workspace = "C:\Personal\ArcGIS\Projects\Geocoding"

# Set local variables:
address_table = "customers.csv"
address_locator = "Atlanta"
address_fields = "Street Address;City City;State State;ZIP Zip"
geocode_result = "geocode_result.shp"

# Perform geocoding
arcpy.GeocodeAddresses_geocoding(address_table, address_locator, address_fields, geocode_result)

# Add result to map
mxd = arcpy.mapping.MapDocument("CURRENT")
df = mxd.activeDataFrame
layer = arcpy.mapping.Layer(geocode_result)
arcpy.mapping.AddLayer(df, layer, "TOP")

# Select matched addresses and create new layer
arcpy.MakeFeatureLayer_management (geocode_result, "matched_addresses", " \"Status\" = 'M' ")
arcpy.CopyFeatures_management("matched_addresses", "C:\Personal\ArcGIS\Projects\Geocoding\matched_addresses.shp")

layer = arcpy.mapping.Layer("matched_addresses")
arcpy.mapping.AddLayer(df, layer, "TOP")

# Create file for unmatched addresses
outfile = "unmatched_addresses.csv"      
fields = arcpy.ListFields(geocode_result)
field_names = [field.name for field in fields]

# Write rows to file for all unmatched addresses
with open(outfile,'wb') as f:
    w = csv.writer(f)
    w.writerow(field_names)
    for row in arcpy.SearchCursor(geocode_result):
		field_vals = [row.getValue(field.name) for field in fields]
		if row.getValue("Status") != "M":	
			w.writerow(field_vals)
    del row

# Add unmatched table to map
layer = arcpy.mapping.TableView("unmatched_addresses.csv")
arcpy.mapping.AddTableView(df, layer)
