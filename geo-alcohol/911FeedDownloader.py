# 911 Feed data is coming from this place http://mcsafetyfeed.org/
# Monroe County 911 Feed collector by date




from multiprocessing import Process, Pool
import json
import time
import urllib2
import requests

def http_get(url):
    print 'getting data from: ', url
    r = requests.get(url)
    return r.json()



if __name__ == '__main__':
    urls = [
    'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-1',
    'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-2',
    'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-3',
    'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-4',
    'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-5',
    'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-6',]# 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-7', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-8', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-9', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-10', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-11', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-12', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-13', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-14', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-15', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-16', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-17', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-18', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-19', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-20', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-21', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-22', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-23', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-24', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-25', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-26', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-27', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-28', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-29', 'http://mcsafetyfeed.org/api/getgeo.php?date=2015-6-30']
    pool = Pool(processes=5)

    results = pool.map(http_get, urls)
    with open('data.txt', 'w') as outfile:
        for result in results:
            for feed in result:
                json.dump(feed, outfile)
                outfile.write("\n")
            print '=========='
