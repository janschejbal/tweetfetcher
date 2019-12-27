#!/usr/bin/python3

import html
import json
import re
import requests  # must be installed
import sys
import time

USER = 'realdonaldtrump'
DEBUG = True

def err(msg):
  print(msg, file=sys.stderr)
  
def fail(msg):
  err(msg)
  sys.exit(1)

def process(tweet):
  text = tweet['full_text']
  text = text.replace('\n', ' ')
  text = html.unescape(text)
  if re.search(r'https://t\.co/[a-zA-Z0-9]+\s*$', text):
    return None
  return (text, tweet['id'])

try:
  token = open('bearer.secret').read().strip()
except Exception as e:
  fail('Failed to load bearer.secret: %s' % e)

def fetch():
  response = requests.get(url, headers={'Authorization': 'Bearer %s' % token})
  response.raise_for_status()
  return response.json()

def fake_fetch():
  return json.loads(open('example.json').read())

url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?exclude_replies=true&include_rts=false&screen_name=%s&count=200&tweet_mode=extended' % USER

if DEBUG:
  fetch = fake_fetch

seen_texts = set()
highest_seen = 0
first_pass = True

while True:
  try:
    found_new = False
    j = fetch()
    j.reverse()  # oldest first
    for tw in map(process, j):
      if not tw:
        continue
      (text, snowflake) = tw
      # Double check both against seen tweets and highest seen ID
      is_seen = text in seen_texts or highest_seen >= snowflake
      seen_texts.add(text)
      highest_seen = max(snowflake, highest_seen)
      if is_seen:
        continue
      found_new = True
      if not first_pass:
        print(text)
    if first_pass:
      first_pass = False
      err(' -- First pass done, saw %d unique tweets.' % len(seen_texts))
    elif not found_new:
      err(' -- Fetch successful; found nothing new.')
  except Exception as e:
    err(' -- Fetch loop failed: %s' % e)
  time.sleep(1 if DEBUG else 60)
