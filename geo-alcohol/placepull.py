import time
import json
import urllib2
import requests
import sys
import re
from numpy import genfromtxt
import math
import numpy
#from geopy import geocoders
from googleplaces import GooglePlaces, types
import random

#g = geocoders.GoogleV3()
print "START RUN"
locations = []

apikeys = []
apikeys.append("AIzaSyAYy7IsAx236vus3dpeFXzmo_LkivJVIns")
#apikeys.append("AIzaSyAVhsPRBPyoNrCr_S3HR3UkWtc4OEecyH0")
#apikeys.append("AIzaSyDeWwKKvrTXgCebZgimtgtdrxAGp1Ik6Tk")
# apikeys.append("AIzaSyA-pf7Zg_TlScNWJYio3al9Ro0bfU7Y_b8")
# apikeys.append("AIzaSyC7VCLlJiWigChOxNF5CyOxXivI0WAUeNg")
# apikeys.append("AIzaSyB4HUQnRT3KpzyM0ig8Cnp-_TP1dzQIRgw")
# apikeys.append("AIzaSyD9DyEtsaBqBG5JwPlFuPjVq2zBFfghxwU")
# apikeys.append("AIzaSyAVADPSydOMi9TsyhxbBOXviuDBkoRKe6M")
# apikeys.append("AIzaSyCVjRaFZ5Pi6Yreo80vta0uRk9oxljsYDg")
# apikeys.append("AIzaSyC97GsTmRZrf5p7rGGPhX1P4io0BH-WHmA")
# apikeys.append("AIzaSyBncqUGltE6roL8lJVtUQyGyZfGDbJDNas")
# apikeys.append("AIzaSyBUnwGVE-qnEJk3r490V4PYgDpHECh80IU")
# apikeys.append("AIzaSyCXE-eMnf5v73WG4JkQaI3v2NO70InjZ0I")
# apikeys.append("AIzaSyC7FNfSRndQ_1SX6djsswxFP8c2J6TIXRw")
# apikeys.append("AIzaSyAudOmNMhFom1LnkTYrd58nq9b3dUABVwk")
# apikeys.append("AIzaSyDtVsgQqJ_bsnynTuURrYAf6pivybRf1ZU")
# apikeys.append("AIzaSyDtkJeF-F9eyjoPrOwZ_q1HIyHsFSO9SVw")
# apikeys.append("AIzaSyA313xYCMy3UUDmpro0rMFBq2KdEWzudO0")
# apikeys.append("AIzaSyBqZT4JqCp7BrCKsG6PBfizYbnuYVJFukE")
# apikeys.append("AIzaSyB573HTLBXhDZYgDnr-DDHRum3_XzS3x6k")
# apikeys.append("AIzaSyC9mlmKB2psVKEEIo_aP2vgl9qkfeo6Ldw")
# apikeys.append("AIzaSyACMaDOF2XmQGKrtcbO3Jh3H5aWB19Da28")
outfile = ""


def rad(x):
    return x * math.pi/180


def getDistance(p1_lat, p1_lng, p2_lat, p2_lng):
    R = 6378137 #meters
    dLat = rad(p2_lat - p1_lat)
    dLong = rad(p2_lng - p1_lng)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(rad(p1_lat)) * math.cos(rad(p2_lat)) * math.sin(dLong / 2) * math.sin(dLong / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d # returns the distance in meter




def gridsearch():
    SW = (42.00027541, -78.5401367286)
    NE = (43.3301514 , -76.18272114)
    NW = (NE[0],SW[1])
    SE = (SW[0],NE[1])
    numCellsOneSide = 10 #the more cells in the grid, the more api's calls.  This will more likely ensure better results but will take longer, and may hit daily api limit.


    minLat = min(SW[0], SE[0])
    maxLat = max(NW[0], NE[0])
    minLon = min(NW[1], SW[1])
    maxLon = min(NE[1], SE[1])



    pTypes = [types.TYPE_RESTAURANT, types.TYPE_CAFE, types.TYPE_BAR, types.TYPE_BAKERY, types.TYPE_FOOD,types.TYPE_MEAL_TAKEAWAY]
    #print str(pTypes)
    typestring = ""
    for type in pTypes:
        typestring = typestring + "|" + type
    
    #print getDistance(NW[0], NW[1], SW[0], SW[1])
    
    offsetMetersPerCell = numpy.mean([getDistance(NW[0], NW[1], SW[0], SW[1]),getDistance(NW[0], NW[1], NE[0], NE[1])]) / numCellsOneSide

    output_file = open(output_path, 'wb')
    ids = []

    for lat in numpy.linspace(minLat, maxLat, numCellsOneSide):
        for lon in numpy.linspace(minLon, maxLon, numCellsOneSide):
            thekey = getapikey()


            while True:
                try:
                    baseurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key="+thekey+"&"
                    theurl = baseurl+"location="+str(lat)+","+str(lon)+"&radius="+str(round(offsetMetersPerCell))+"&types="+str(typestring)
                    theurl = theurl.replace(" ","+")
                    print theurl
                    req = urllib2.Request(theurl)
                    
                    res = urllib2.urlopen(req,timeout=30)
                    place = res.read()
             
                    jsonplace = json.loads(place)
                    if jsonplace['status'] == "OVER_QUERY_LIMIT":
                        print "over limit"
                        removeapikey(thekey)
                    else:
                        print "got result: %r" % jsonplace
                        break
                except:
                    print 'Error caught, sleeping...'
                    time.sleep(60)
        
 
        

        
        
            for place in jsonplace['results']:
                if ids.count(place['id']) == 0:
                    output = {
                        "name": place['name'],
                        "geometry": place['geometry'],
                        "id": place['id'],
                        "types": place['types'],
                        "vicinity": place['vicinity']}
                    #print "theoutput: " + output['name']
                    json.dump(output, output_file)#, separators=(',',':'))
                    output_file.write("\n")
                    ids.append(place['id'])
                    print "gotone: %r" % output




def getapikey():
     #print "Keys left:" + str(len(apikeys))
     if len(apikeys)>=1:
        key = apikeys[random.randint(1,len(apikeys))-1]
        return key
     else:
        print "No Keys Left"
        quit()
        return "empty"


def removeapikey(thekey):
     apikeys.remove(thekey)
     print "Removing key:"+thekey
     return



if __name__ == "__main__":

    output_path = sys.argv[1]


    gridsearch()
