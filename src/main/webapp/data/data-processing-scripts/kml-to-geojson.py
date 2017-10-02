###
### Copyright Dan Cunnington 2017
###

import re,os

road_properties_pattern = r"<name>(.*)<\/name>\s*<description>.*Curvature:\s*(\d+\.?\d*|\.\d+).*Distance:\s*(\d+.?\d*\s*(km|mi)).*Type:\s*(\w+).*<\/description>(.*)"
placemark_pattern = r"<LineStyle><color>(\w*)<\/color>.*<coordinates>(.*)<\/coordinates>\s*<\/LineString>"
outputDirectory = "dan_new_geojson_convertor"
currentFileId = 0
inputDir = 'dan_kml_split_output'
numberOfFiles = str(len(os.listdir(inputDir)))
currentFilesProcessed = 0

def listOfFolders(filename, startPattern, endPattern):
  with open(filename) as file:
    recording = False
    for line in file:
      if (line.strip().startswith(startPattern)):
        yield line
        recording = not recording
      elif (line.strip().startswith(endPattern)):
        yield line
        recording = not recording
      elif recording:
        yield line

def convertPlacemarkToGeoJsonFeature(contents):
  stroke_width = '3'
  stroke_opacity = '1'
  start_geojson_feature = '{ "type": "Feature", "geometry": { "type": "LineString", "coordinates": '
  matches = re.finditer(placemark_pattern, contents)

  for matchNum, match in enumerate(matches):
    stroke_colour = match.group(1)
    coordinatesString = match.group(2).rstrip()

    #convert colour to rrggbb
    colour_split = [stroke_colour[i:i+2] for i in range(0, len(stroke_colour), 2)]
    rrggbb_colour = colour_split[3] + colour_split[2] + colour_split[1]

    end_geojson_feature = '}, "properties": { "stroke": "#'+rrggbb_colour+'", "stroke-opacity": '+stroke_opacity+', "stroke-width": '+stroke_width+'}' + '}'

    #convert coordinates string to array string
    coordinatesString = coordinatesString.replace(" ", "],[")
    jsonCoordinates = "[[" + coordinatesString + "]]"
    geojson = start_geojson_feature + jsonCoordinates + end_geojson_feature
    return geojson


def convertFolderToGeoJson(folder, currentFileId):
  #extract name, overall curvature, road type, distance, surface
  # folder = ''.join(folder.split())
  folder = re.sub(r"\s+", " ", folder)
  matches = re.finditer(road_properties_pattern, folder)

  for matchNum, match in enumerate(matches):
    road_name = match.group(1)
    overall_curvature = match.group(2)
    overall_distance = match.group(3)
    road_type = match.group(5)
    everything_else = match.group(6)

    # print(road_name, overall_curvature, overall_distance, road_type)

    currentPlacemarkContents = ''
    properties = '{ "road-name": "'+road_name+'", "overall-distance": "'+overall_distance+'", "overall-curvature": "'+overall_curvature+'", "road-type": "'+road_type+'" }'
    featureCollection = '{ "type": "FeatureCollection", "road_properties": '+properties+', "features": ['
    endFeatureCollection = ']}'
 
    splittedPlacemarks = everything_else.split('</Placemark><Placemark>')

    for placemark in splittedPlacemarks:
      placemarkGeo = convertPlacemarkToGeoJsonFeature(placemark)
      featureCollection += placemarkGeo + ','
        
    #remove last comma and close
    featureCollection = featureCollection[:-1]
    featureCollection += endFeatureCollection
    
    #write to file
    with open(outputDirectory+'/'+str(currentFileId)+'.geojson', 'w') as file:
      file.write(featureCollection)


def convertFile(path, name):
  folders = []
  currentKMLFolderContents = ''
  currentFolderId = 0

  name = name.split('.')[0]

  for line in listOfFolders(path, '<Folder>', '</Folder>'):
    currentKMLFolderContents += line
    if (line.strip().startswith('</Folder>')):
      folders.append(currentKMLFolderContents)
      currentKMLFolderContents = ''

  for index, folder in enumerate(folders):
    geojsonFileName = name + '-' + str(currentFolderId)
    convertFolderToGeoJson(folder, geojsonFileName)
    currentFolderId += 1

#main entry point
for filename in os.listdir(inputDir):
  if filename != '.DS_Store':
    path = inputDir +'/'+ filename
    convertFile(path, filename)
    currentFilesProcessed +=1
    print(str(currentFilesProcessed) + '/' + numberOfFiles)

