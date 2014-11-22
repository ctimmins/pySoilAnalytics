import requests
import soilQuery
from xml.etree import ElementTree as ET
from pymongo import MongoClient

# client = MongoClient('mongodb://localhost')
# db = client['test-root-db']

#URL for service returning features in NAD83 Geographic (EPSG4269) coordinates
URL = "http://SDMDataAccess.nrcs.usda.gov/Spatial/SDMNAD83Geographic.wfs?REQUEST=GetFeature&SERVICE=WFS&VERSION=1.0.0&TYPENAME=MapunitPolyExtended"
testCoords = [{38.5330, -121.7983}, {38.5315, -121.7400}, {38.5316, -121.7362}, {38.5331, -121.7363}]
testParam = "<Filter><Intersect><PropertyName>Geometry</PropertyName><gml:Polygon><gml:outerBoundaryIs><gml:LinearRing><gml:coordinates>-121.7983,38.5330 -121.7400,38.5315 -121.7362,38.5316 -121.7363,38.5331</gml:coordinates></gml:LinearRing></gml:outerBoundaryIs></gml:Polygon></Intersect></Filter>"

URL = URL + "&FILTER=" + testParam
r = requests.get(URL, headers={'Content-Type': 'application/xml'})
root = ET.fromstring(r.content)

myData = soilQuery.getSoilData(root)
for sub in myData:
	print(sub)
	print("")