#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import log
import model
import uuid

def application(environ, start_response):
    write = start_response('200 OK', [
      ('Access-Control-Allow-Origin', '*'),
      ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),
      ('Content-Type', 'application/json')
    ])

    my_guid = environ.get('QUERY_STRING', uuid.uuid4())

    raw = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', '0')))
    if len(raw) > 0:
      log.logit(raw)

      try:
        content = json.loads(raw)
      except ValueError:
        return [json.dumps({"error": "I need JSON, with your input as the value to the data key"})]

      if 'id' in content and content['id'] == 'fave':
        log.faveit(raw)
      else:
        res = model.analyze(content['data'])

      res['id'] = my_guid

      return [json.dumps(res)]

    return [json.dumps({"error": "I need some POST input to analyze, dumbfuck."})]
