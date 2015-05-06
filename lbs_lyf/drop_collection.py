#coding=utf-8
import urllib
import urllib2

url = 'http://211.152.60.33:8888'
values = {"storeID" : ["106Z"],
          "item_count" : 1}

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()