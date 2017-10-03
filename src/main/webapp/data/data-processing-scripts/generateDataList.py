import os
inputDir = '../store/curvature'

stringToWrite = '['

for filename in os.listdir(inputDir):
  if filename != '.DS_Store':
    with open(inputDir +'/'+ filename) as f:
      contents = f.read()
      stringToWrite += contents + ','

stringToWrite = stringToWrite[:-1]
stringToWrite += ']'
#write to file
with open('../store/curvature_combined.json', 'w') as file:
  file.write(stringToWrite)