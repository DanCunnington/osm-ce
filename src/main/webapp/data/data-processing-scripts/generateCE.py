###
### Copyright Dan Cunnington 2017
###

import json, os, uuid
from pprint import pprint

#for every file in data directory, build query
ceToWrite = []
inputDir = '../store/curvature'
outputDir = '../../ce/facts'
numberOfFiles = str(len(os.listdir(inputDir)))
currentFileProcessed = 0

def generateCEForFile(path):
  with open(path) as data_file:    
    data = json.load(data_file)
    road_properties = data["road_properties"]

    road_name = road_properties["road-name"]
    overall_distance = road_properties["overall-distance"]
    overall_curvature = road_properties["overall-curvature"]
    road_type = road_properties["road-type"]

    ceToWrite.append("there is a road named '"+road_name+"' that has '"+overall_distance+"' as distance and has '"+overall_curvature+"' as overall curvature and has '"+road_type+"' as road type.")

    features = data["features"]
    featureLength = len(features)
    for feature in features:
      coordinates = feature["geometry"]["coordinates"]
      strokeColour = feature["properties"]["stroke"]
      featureType = feature["geometry"]["type"]
      ceToWrite.append("there is a road segment named '"+str(uuid.uuid4())+"' that has '"+strokeColour+"' as curvature stroke colour and has '"+str(coordinates)+"' as coordinates and has '"+featureType+"' as geojson type and corresponds to the road '"+road_name+"'.") 

#main entry point
for filename in os.listdir(inputDir):
  if filename != '.DS_Store':
    generateCEForFile(inputDir+'/'+filename)
    currentFileProcessed += 1
    print (str(currentFileProcessed) + '/' + numberOfFiles)

#write to file
with open(outputDir+'/curvature.ce', 'w') as file:
  file.write("\n".join(ceToWrite).encode("utf-8").strip())

