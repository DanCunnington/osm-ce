###
### Copyright Dan Cunnington 2017
###

def folder(filename, startPattern, endPattern):
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

startPattern = '<Folder>'
endPattern = '</Folder>'
outputDirectory = 'dan_kml_split_output'
commonKmlStartContents = '''<?xml version="1.0" encoding="utf-8" ?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document id="root_doc">
'''
commonKmlEndContents = '</Document></kml>'
numberOfFoldersPerFile = 15
currentNumberOfFolders = 0
currentFileId = 0
currentFileContents = ''

for line in folder('great-britain-latest/doc.kml', startPattern, endPattern):
  currentFileContents += line
  if (line.strip().startswith(endPattern)):
    currentNumberOfFolders +=1
    if currentNumberOfFolders == numberOfFoldersPerFile:
      # write currentFileContents to file and reset counters
      with open(outputDirectory+'/doc-'+str(currentFileId)+'.kml', 'w') as file:
        file.write(commonKmlStartContents + currentFileContents + commonKmlEndContents)
      currentNumberOfFolders = 0
      currentFileContents = ''
      currentFileId+=1
      print 'processed file '+str(currentFileId)
