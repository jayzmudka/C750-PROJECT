#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from pprint import pprint as pp
from zipfile import ZipFile

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
# writes out json file#auditing functions

ROOTTAGS = [ 'node', 'way', 'relation'] #the three map elements

# Lists the total tags in .osm file
def list_totals(usefile):
    tagslist ={}
    total = 0
    for _, element in ET.iterparse(usefile):
        total += 1
        if element.tag not in tagslist:
            tagslist[element.tag] = 1
        else:
            tagslist[element.tag] = tagslist[element.tag] + 1
    print 'Counting all the tags: \n'
    print total, 'tags in total \n'
    pp(tagslist)

# Lists websites with bad URL's    
def list_websites(usefile):
    websites = []
    for _, element in ET.iterparse(usefile):
        if len(element.findall('tag')) > 0:
            for tag in element.findall('tag'):
                if tag.attrib['k'] == 'website':
                    websites.append(tag.attrib['v'])
    print 'List of websites'
    pp(websites)
    badurls = []
    for w in websites:
        if not w.startswith('http'):
            badurls.append(w)
    print "\nThese websites are not proper URL's" 
    pp(badurls)
    
# Lists some ways with redundant tiger tags  
def find_tiger(usefile):
    tigertags = 0
    print 'Samples of ways containing redundant tiger street data:'
    for _, element in ET.iterparse(usefile):
        if element.tag == 'way':
            if len(element.findall('tag')) > 0:
                for tag in element.findall('tag'):
                    if tag.attrib['k'].startswith('tiger'):
                        print ET.tostring(element)
                        tigertags += 1
                        break           
                pass
        if tigertags > 1:
            break
                  
#compiles and prints list of street suffixes
def street_endings(usefile):
    street_endings = set()
    for _, element in ET.iterparse(usefile):
        if element.tag == 'way':        
            if len(element.findall('tag')) > 0:
                for tag in element.findall('tag'):
                    if tag.attrib['k'] == 'name':
                        street_endings.add(tag.attrib['v'].split()[-1])
    print street_endings

# How many total tags are in the file?	
list_totals(usefile)
print

# Print a set of street name endings
street_endings(usefile)
print

# Print a list of websites and which one have bad urls
list_websites(usefile)
print

# Print some redundant TIGER data
find_tiger(usefile)

