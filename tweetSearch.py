#!/usr/bin/env python
# -*- coding: utf-8 -*-

#http://api.wunderground.com/api/9a1f64821c43cacf/conditions/q/-33.410953,-70.549393.json

import os,sys
from twython import Twython
APP_KEY='vb4ZZNQh8Z8chiq1kREKZg'
APP_SECRET = 'l1UnrkyWApYa9c8m7CnrqvYDw8VLXpnM448aVDMo'
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
tweets= twitter.search(q=sys.argv[1],count=100000)
textos = [t['text'] for t in tweets['statuses']]
print textos
print textos.__len__()
twitter.update_status(status='See how easy using Twython is!')