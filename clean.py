# cleaning functions
import re


# increments tigertag counter for a stat
tigertags_count = 0 # counter for tigertags
def increment_tigertags(): 
    global tigertags_count
    tigertags_count += 1

# Sets to be used for the cleaning and insertion of data
ROOTTAGS = [ 'node', 'way', 'relation'] #the three map elements
CREATED = [ 'version', 'changeset', 'timestamp', 'user', 'uid']
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Function to find and fix bad url's
def fix_urls(element):
    if element.tag == 'node' or element.tag == 'way':
        if len(element.findall('tag')) > 0:
                for tag in element.findall('tag'):
                    if tag.attrib['k'] == 'website':
                        url = tag.attrib['v']                        
                        url = url.lower().strip()
                        if not url.startswith('http'):
                            print 'old url', url
                            url = 'http://' + url
                            print 'fixed url', url
                        tag.attrib['v'] = url
    return element

# Function to remove tiger: tags
def remove_tigertags(element):
    if element.tag == 'way':
        tt = False
        if len(element.findall('tag')) > 0:
                for tag in element.findall('tag'):
                    if tag.attrib['k'].startswith('tiger'):
                        element.remove(tag)
                        increment_tigertags()
    return element
#Function that takes a Elementtree element and returns cleaned up json ready dictionary
#This function is modified from 12: Quiz Preparing for Database MongDB in the Udacity material

def shape_element(element):
    node = {}
    if element.tag in ROOTTAGS:
        
        fix_urls(element) #Fixes bad URL's
        remove_tigertags(element)#Removes tiger tags
        
        node['type'] = element.tag
        node['id'] = element.attrib['id']
        if 'visible' in element.attrib:
            node['visible'] = element.attrib['visible']
        node['created'] = {}
        
        for x in CREATED: #Rolls up created info tags
            node['created'][x] = element.attrib[x]
            
        if 'lat' in element.attrib: #adds Long and Lat tuple to document
            node['pos'] = (float(element.attrib['lat']), float(element.attrib['lon']))
        
        # Rolls up address tags and adds other tags to document
        if len(element.findall('tag')) > 0:
            node['address'] = {}
            for tag in element.findall('tag'):
                
                if problemchars.search(tag.attrib['k']): #checks for bad characters
                    pass
                elif tag.attrib['k'] == 'type':
                    node['relation_type'] = tag.attrib['v']
                elif 'addr:' in tag.attrib['k']:
                    if len(tag.attrib['k'].split(':')) > 2:
                        pass
                    else:
                        addc = tag.attrib['k'].split(':')[1]
                        node['address'][addc] = tag.attrib['v']
                else:
                    node[tag.attrib['k']] = tag.attrib['v']
                    
        #makes list of node_refs tags            
        if len(element.findall('nd')) > 0: 
            node['node_refs'] = []
            for nd in element.findall('nd'):
                node['node_refs'].append(nd.attrib['ref'])
                
        # removes empty address tags                
        if 'address' in node: 
                if len(node['address']) == 0:
                    del node['address']
        
        return node
    else:
        return None

