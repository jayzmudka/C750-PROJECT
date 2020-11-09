#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pprint import pprint as pp
import json
from zipfile import ZipFile
import pymongo
outfile = 'openstreetmapdata.json'

# insert into MongoDB database
connection = pymongo.MongoClient('localhost', 27017)
if 'openstreetmap' in connection.list_database_names():
    db = connection['openstreetmap']
    db.main.drop() 
    print('Deleted existing database')

print 'Making new database openstreetmap'
db = connection['openstreetmap']

with open(outfile) as f:
    data = [json.loads(line) for line in f]
    db.main.insert_many(data)
	
# explore the db with PyMongo
#find size stats of database

# database stats
stats = 'dbstats', db.command('dbstats')  
pp(stats)
#size of file in KB
print db.command('dbstats')['storageSize'] / 1024, 'KB file'

# how many nodes, ways, and relations
print
print db.main.find().count(), 'total documents\n'
print db.main.count_documents({'type':'node'}), 'nodes'
print db.main.count_documents({'type':'way'}), 'ways'
print db.main.count_documents({'type':'relation'}), 'relations\n'

#how many unique users
print len(db.main.distinct('created.user')), 'unique users\n'


#Which 5 users contributed the most to the data?
result = db.main.aggregate([{'$group' : { '_id' : '$created.user',
                                       'count' : {'$sum': 1}}},
                            {'$sort' : {'count' : -1 }},
                            {'$limit' : 5}])
print 'Top 5 contributers'
for doc in result:
    print doc
	
# number of busstops

print db.main.count_documents({'highway':'bus_stop'}), 'bus stops'

# which node is referenced the most?
    
result = db.main.aggregate([ {'$match' : {'type' : {'$in': ['way', 'relation']}}},
                           {'$unwind': '$node_refs'},
                           {'$group': {'_id' : '$node_refs',
                                      'count' :{'$sum': 1}}},
                           {'$sort' : { 'count' : -1 }},
                           {'$limit' : 1 }])
print 'Here is the most referenced node:\n'
for doc in result:    
    id = doc['_id']
    for i in db.main.find({'id' : id}):
        pp(i)
        print 'Referenced in', doc['count'], 'records'
        coords = i['pos']

# 5 closest retaurants to that node

#build index on id, geo2d index on pos field
db.main.create_index([('pos', pymongo.GEO2D)])

closest_restaurants = db.main.find({'pos' : {'$near':  coords}, 'amenity' : 'restaurant'}).limit(5)
print '\nFive nearest restaurants \n'
for i in closest_restaurants:    
    print i['name']
    if 'address' in i:
        print i['address']['housenumber'], i['address']['street']
    else:
        print 'No address given'
    if 'cuisine' in i:
        print 'Cuisine', i['cuisine']
    print '----------------'
# give us 3 restaurants that are missing address data
sample_restaurants = db.main.find({'type' : 'node', 'amenity':'restaurant', 'address': {'$exists' : False}}).limit(3)

print 'Restaurants'
for doc in sample_restaurants:
    pp(doc)
    print
# give us 3 shops that are missing address data
sample_stores = db.main.find({'shop' : {'$exists' : True}, 'address' : {'$exists' : False}}).limit(3)

print 'Shops'
for doc in sample_stores:
    pp(doc)
    print
	