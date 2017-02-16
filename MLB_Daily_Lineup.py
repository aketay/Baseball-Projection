import datetime
import time
import urllib2
import re
from bs4 import BeautifulSoup
from datetime import timedelta, date
from urllib2 import HTTPError

# Get Webpage Data
def playerget(s):
    try:
        sock2 = ""
        sock2 = urllib2.urlopen('http://www.google.com')

    except urllib2.HTTPError, e:
        urlerrorCode = e.code
        print urlerrorCode
        print e.fp.read()

    if hasattr(sock2, 'read'):
        dataslerp = sock2.read()
    else:
        print "Error!"
        return

playerget("yoyoyo")

soup = BeautifulSoup(sock2, 'html.parser', from_encoding = 'UTF-8')


TestTitle = soup.find_all('title')

for item in TestTitle:
    print item




