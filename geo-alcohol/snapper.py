import Levenshtein
import sys
import re
from rtree import index
from pytz import timezone
from datetime import date, datetime, time, timedelta
import math
import logging
import json



def parse_created_at(created_at):
    try:
        return datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    except ValueError as e:
        return datetime.strptime(created_at, '%a, %d %b %Y %H:%M:%S +0000')


def loadEntities(entity_path):
    print "Load  file: " + entity_path
    entity_index = index.Index()

    with open(entity_path, 'r') as entity_file:

        	counter = 0
        	for line in entity_file:

           	 	r = json.loads(line)
            		entity_id = str(r['id']) 
            		entity_lat = float(r['geometry']['location']['lat'])
            		entity_lng = float(r['geometry']['location']['lng'])
            
            		entity_index.insert(counter, (entity_lng,entity_lat,entity_lng,entity_lat), obj = r) 
            
    		return entity_index


def parsetweet(tweetdata):
    tweet_id = ""
    tweet_lat = ""
    tweet_lng = ""
    tweet_created_at = ""
    try:
        tweet_id = tweetdata['id_str']
        tweet_lat = tweetdata['coordinates']['coordinates'][1]
        tweet_lng = tweetdata['coordinates']['coordinates'][0]
    except:
        try:
        	tweet_id = tweetdata['id']
        	tweet_lat = tweetdata['geo']['latitude']
        	tweet_lng = tweetdata['geo']['longitude']
	except:        
        	tweet_id = tweetdata['id']
		tweet_lat = ""
        	tweet_lng = ""

    try:
        tweet_created_at = tweetdata["created_at"]
    except:
	tweet_created_at = ""


    return tweet_id,tweet_lat,tweet_lng, tweet_created_at



def processTweets(entity_index, tweet_path, writealltweets, output_path, business_range_meters):
    print "Load tweet file: " + tweet_path
    tweetsprocessed=0
    tweet_map = {}
    matchtweet = 0
    
    with open(tweet_path, 'r') as tweet_file:
        with open(output_path, 'wb') as output_file:
            matchcounttotal = 0
            matchedtweettotal = 0
            matchedtweetavg = 0
	    tweetsmissingdata = 0
            for line in tweet_file:
                tweetsprocessed=tweetsprocessed+1
                if tweetsprocessed%10000 == 0:
                    print "Processed " + str(tweetsprocessed)


                tweetdata = json.loads(line)


                tweet_id, tweet_lat, tweet_lng, tweet_created_dt = parsetweet(tweetdata)

                if tweet_id =="" or tweet_lat == "" or tweet_lng == "" or tweet_created_dt == "":
   			tweetsmissingdata=tweetsmissingdata+1 
	                continue

                nearbyEntities = getEntitiesNearPoint(entity_index, business_range_meters, tweet_lat, tweet_lng)

                if len(nearbyEntities) > 0:
                	matchedtweettotal = matchedtweettotal + 1

		matchcounttotal = matchcounttotal + len(nearbyEntities)
    
	        if matchedtweettotal > 0:
		    matchedtweetavg = 1. * matchcounttotal/matchedtweettotal
                
		if len(nearbyEntities) > 0 or writealltweets == "True":
			tweetdata['placematchcount']=len(nearbyEntities)
			tweetdata['placematches']=nearbyEntities
			output_file.write(json.dumps(tweetdata) + "\n")	


    print "Matched Tweet match average: " + str(float(matchedtweetavg))
    print str(matchedtweettotal) + " of " + str(tweetsprocessed) + " tweets were within range of a fun place that has alcohol"
    print "Number of tweets missing data to match on: " + str(tweetsmissingdata)




    
def getEntitiesNearPoint(index, slack, tweet_lat, tweet_lng):
    
    
    try:
	
        #note these are for rochester - go to http://www.csgnetwork.com/degreelenllavcalc.html to calculate for a different latitude
        dX = slack * 0.000012297
        dY = slack * 0.000009001
        lng_low = tweet_lng - dX
        lng_high = tweet_lng + dX
            
        lat_low = tweet_lat - dY
        lat_high = tweet_lat + dY
        
        
        
        intersect = index.intersection((tweet_lng - dX, tweet_lat - dY, tweet_lng + dX, tweet_lat + dY), objects = True)
        return [n.object for n in intersect]
    
    except KeyError:
        return []



 

if __name__ == "__main__":
    entity_path = sys.argv[1]
    tweet_path = sys.argv[2]
    output_path = sys.argv[3]
    writealltweets = sys.argv[4]
    business_range_meters = float(sys.argv[5])
    print writealltweets

    entity_index = loadEntities(entity_path)
    
    processTweets(entity_index, tweet_path, writealltweets, output_path,business_range_meters)
