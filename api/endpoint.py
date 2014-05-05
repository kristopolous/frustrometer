#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import log
import model

def application(environ, start_response):
    write = start_response('200 OK', [
      ('Access-Control-Allow-Origin', '*'),
      ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),
      ('Content-Type', 'application/json')
    ])

    raw = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', '0')))
    log.logit(raw)
    content = json.loads(raw)
    if 'id' in content and content['id'] == 'fave':
      log.faveit(raw)
    else:
      res = model.analyze(content['data'])

    return [json.dumps(res)]
