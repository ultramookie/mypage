#!/usr/bin/python
# mypage
# steve mookie kong
# licensed under gplv3
# http://www.gnu.org/licenses/gpl-3.0.html

import re
import urllib
import urllib2
import feedparser
import time
import os
import binascii

# Item Limit
limit = 10

# Time Limit (hours)
timelimit = 24

# Page File
realfile = 'PATH_TO_HTML/index.html'
randfile = '/tmp/' + binascii.b2a_hex(os.urandom(15))
file = open(randfile,'w+')

# RSS Feeds
feeds = [	"http://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss",
		"http://www.androidcentral.com/rss.xml",
		"http://www.tmonews.com/feed/",
		"http://www.theverge.com/rss/frontpage",
		"http://www.fiercewireless.com/feed",
		"http://bits.blogs.nytimes.com/feed/",
		"http://feeds.popsci.com/c/34567/f/632419/index.rss",
		"http://feeds.gawker.com/io9/full",
		"http://feeds.gawker.com/jalopnik/full",
		"http://feeds.feedburner.com/psblog",
		"http://readwrite.com/main/feed/articles.xml",
		"http://feeds.feedburner.com/caranddriver/blog",
		"http://feeds.wired.com/wired/index",
		"http://www.joblo.com/newsfeeds/rss.xml",
		"http://www.astronomy.com/rss/news",
		"http://stardate.org/feeds/podcast.xml",
		"http://feeds.arstechnica.com/arstechnica/index/",
		"http://feeds.mercurynews.com/mngi/rss/CustomRssServlet/568/200735.xml",
		"http://rssfeeds.usatoday.com/usatoday-NewsTopStories",
		"http://news.yahoo.com/rss/"
		 ]


def printRSS(rss,limit,file):
	count = 0
	feed = feedparser.parse(rss)
	feedtitle = feed.feed.title.split("-")
	title = feedtitle[0]
	file.write("<br /><b>" + title + "</b><hr />")
	file.write("<ul />")
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
		safelink = urllib.quote_plus(link.encode('utf8'))
		safetitle = urllib.quote_plus(actualtext.encode('utf8'))
		if (pubhours == 0):
			printpubhours = "<b>" + str(pubhours).zfill(2) + "h</b>"
		else:
			printpubhours = str(pubhours).zfill(2) + "h"
		#file.write("<li><a href=\"" + link + "\" target=\"_new\">" + actualtext + "</a> (<a href=\"https://getpocket.com/edit?url=" + safelink + "&title=" + safetitle + "\" target=\"_pocket\">p</a>)&emsp;" + printpubhours)
		file.write("<li><a href=\"" + link + "\" target=\"_new\">" + actualtext + "</a> <iframe border=\"0\" scrolling=\"no\" width=\"78\" height=\"17\" allowtransparency=\"true\" frameborder=\"0\" style=\"margin-bottom: -3px; z-index: 1338; border: 0px; background-color: transparent; overflow: hidden;\" src=\"http://www.instapaper.com/e2?url=" + safelink + "&title=" + safetitle + "\" ></iframe>&emsp;" + printpubhours)
		count = count + 1
	file.write("</ul>")

file.write("<html><head>")
file.write("<meta http-equiv=\"Cache-Control\" content=\"no-cache, no-store, must-revalidate\" />")
file.write("<meta http-equiv=\"Pragma\" content=\"no-cache\" />")
file.write("<meta http-equiv=\"Expires\" content=\"0\" />")
file.write("<meta http-equiv=\"Refresh\" content=\"600\" />")
file.write("<meta name=viewport content=\"width=device-width, initial-scale=1.0, minimum-scale=0.5 maximum-scale=1.0\">")
file.write("<title>my ultramookie</title></head><body>")

for feed in feeds:
	printRSS(feed,limit,file)

file.write("<br /><hr />")
file.write("<b>last update:</b> " + time.strftime("%c"))
file.write("</body></html")
file.close()
os.rename(randfile,realfile)
