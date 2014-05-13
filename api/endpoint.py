#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import log
import model
import uuid

import base64
import math
import random
import struct

def encode(n):
  data = struct.pack('<Q', n).rstrip('\x00')
  if len(data)==0:
      data = '\x00'
  s = base64.urlsafe_b64encode(data).rstrip('=')
  return s

def challenge_create():
  return encode(int(random.random() * 32676))

def challenge(uid, c):
  return True

def application(environ, start_response):
    write = start_response('200 OK', [
      ('Access-Control-Allow-Origin', '*'),
      ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),
      ('Content-Type', 'application/json')
    ])

    raw = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', '0')))
    if len(raw) > 0:
      log.logit(raw)

      try:
        content = json.loads(raw)
      except ValueError:
        return [json.dumps({"error": "I need JSON, with your input as the value to the data key"})]

      my_challenge = 0

      if 'uid' in content and content['uid'] != 0:
        my_guid = content['uid']

        if 'c' in content:
          my_challenge = content['c']

      else:
        my_guid = str(uuid.uuid4())
        my_challenge = challenge_create()

      if 'id' in content and content['id'] == 'fave':
        log.faveit(raw)
      else:
        res = model.analyze(content['data'])

      res['uid'] = my_guid

      return [json.dumps(res)]

    return [json.dumps({"error": "I need some POST input to analyze, dumbfuck."})]
