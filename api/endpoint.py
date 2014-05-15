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

def myrand():
  m_uid = str(uuid.uuid4())
  m_uid = m_uid.replace('-','').upper()
  return base64.b64encode(base64.b16decode(m_uid)).replace('=','')

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

# The challenge makes sure that UUIDs don't get stomped
# by people who want to hijack an existing comment.
#
# Both the publically accessible uuid and the privately
# stored challenge has to match before anything is updated

      my_challenge = 0

      if 'uid' in content and content['uid'] != 0:
        my_guid = content['uid']

        if 'c' in content:
          my_challenge = content['c']

      else:
        my_guid = myrand()
        my_challenge = myrand()

      if 'id' in content and content['id'] == 'fave':
        log.faveit(raw)
      else:
        res = model.analyze(content['data'])

      res['uid'] = my_guid
      res['c'] = my_challenge

      return [json.dumps(res)]

    return [json.dumps({"error": "I need some POST input to analyze, dumbfuck."})]
