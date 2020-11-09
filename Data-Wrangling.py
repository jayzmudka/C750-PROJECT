
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from pprint import pprint as pp
import re
import codecs
import json
from zipfile import ZipFile
from clean import *


samplefile = 'sample.osm'
zipfile = 'openstreetmapdata.zip'
filename = 'openstreetmapdata'
outfile = 'openstreetmapdata.json'

# uncomment the data you want to use
usefile = samplefile # smaller sample file
#usefile = openzipfile(zipfile, filename) #Full size file 70mb
# extracts osm file from zip archive
def openzipfile(zipf, filename):
    with ZipFile(zipf) as osmzip:
        xfile = osmzip.open(filename)
        return xfile
# read data into elementtree objects
# calls shape_element fuction
# writes out json file

data = []
with codecs.open(outfile, "w") as fo:
    for _, element in ET.iterparse(usefile):
        piece = shape_element(element)
        if piece != None:
            data.append(piece)
            fo.write(json.dumps(piece) + "\n")
    print 'Removed', tigertags_count, 'tiger tags'
    print 'Output saved to file:', outfile
