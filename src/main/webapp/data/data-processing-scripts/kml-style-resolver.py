###
### Copyright Dan Cunnington 2017
###

import re,os
p = r"<styleUrl>#(\w+)<\/styleUrl>"
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, 'great-britain-latest/doc.kml'), 'r+') as f:
    lines = f.readlines()
    f.seek(0)
    f.truncate()
    for line in lines:
        matches = re.finditer(p, line.strip())
        # match = p.match(line.strip())
        for matchNum, match in enumerate(matches):
            matchNum = matchNum + 1
            match = match.group(1)
            replacement = ''
            if match == 'lineStyle0':
                replacement = '<LineStyle><color>F000E010</color><width>3</width></LineStyle>'
            elif match == 'lineStyle1':
                replacement = '<LineStyle><color>F000FFFF</color><width>3</width></LineStyle>'
            elif match == 'lineStyle2':
                replacement = '<LineStyle><color>F000AAFF</color><width>3</width></LineStyle>'
            elif match == 'lineStyle3':
                replacement = '<LineStyle><color>F00055FF</color><width>3</width></LineStyle>'
            elif match == 'lineStyle4':
                replacement = '<LineStyle><color>F00000FF</color><width>3</width></LineStyle>'
            elif match == 'elminiated':
                replacement = '<LineStyle><color>F0000000</color><width>3</width></LineStyle>'
            elif match == 'folderStyle':
                replacement = '<ListStyle><listItemType>checkHideChildren</listItemType></ListStyle>'
            if replacement != '':
                existing = '<styleUrl>#'+match+'</styleUrl>'
                line = line.replace(existing, replacement)
        f.write(line)