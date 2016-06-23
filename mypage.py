#!/usr/bin/env python
# mypage
# steve mookie kong
# licensed under gplv3
# http://www.gnu.org/licenses/gpl-3.0.html

import re
import feedparser
import time
import os
import binascii
import json

def read_config():
  config_location = 'config.json'
  if os.path.isfile(config_location):
    with open(config_location) as config_file:    
      config = json.load(config_file)
    return config
  else:
    print 'config file %s is missing' % config_location
    sys.exit()

def printRSS(config,rss,file):
  limit = int(config['itemlimit'])
  timelimit = int(config['timelimit'])
  count = 0
  feed = feedparser.parse(rss)
  try:
    feedtitle = feed.feed.title.split("-")
    title = feedtitle[0]
    file.write("<br /><b>%s</b>" % (title))
    file.write("<ul />")
  except AttributeError:
    print "%s has issues. Please check the URL." % (rss)
    pass
  for item in feed.entries:
    try:
      feeddate = item.updated_parsed
    except AttributeError:
      try:
        feeddate = item.published_parsed
      except AttributeError:
        feeddate = time.localtime()
    pubhours = int((time.mktime(time.gmtime()) - time.mktime(feeddate))/60/60)

    if (count == limit) or (pubhours > timelimit):
      break

    realtext = ""
    link = item.link
    actualtext = item.title.encode('ascii','ignore').strip()
    if (pubhours == 0):
      printpubhours = "<b>%s</b>" % (str(pubhours).zfill(2))
    else:
      printpubhours = "%s" % (str(pubhours).zfill(2))
    file.write("<li><a href=\"%s\" target=\"_new\">%s</a> %sh" % (link, actualtext, printpubhours))
    count = count + 1
  file.write("</ul>")

def writeHeader(file):
  file.write("<html><head>")
  file.write("<meta http-equiv=\"Cache-Control\" content=\"no-cache, no-store, must-revalidate\" />")
  file.write("<meta http-equiv=\"Pragma\" content=\"no-cache\" />")
  file.write("<meta http-equiv=\"Expires\" content=\"0\" />")
  file.write("<meta http-equiv=\"Refresh\" content=\"600\" />")
  file.write("<meta name=viewport content=\"width=device-width, initial-scale=1.0, minimum-scale=0.5 maximum-scale=1.0\">")
  file.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"feedstyle.css\"/>")
  file.write("<title>Feeds</title></head><body>")

def processFeeds(config,file):
  feeds = config['rssfeeds']
  for feed in feeds:
    printRSS(config,feed,file)

def writeFooter(config,file,randfile):
  file.write("<br /><hr />")
  file.write("<b>last update:</b> %s" % (time.strftime("%c")))
  file.write("</body></html")
  file.close()
  realfile = config['output']
  os.rename(randfile,realfile)

def go():
  config = read_config()
  tmp = config['tmp']
  randfile = '%s/%s' % (tmp,binascii.b2a_hex(os.urandom(15)))
  file = open(randfile,'w+')
  writeHeader(file)
  processFeeds(config,file)
  writeFooter(config,file,randfile)
  
go()
