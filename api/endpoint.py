#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import model

def application(environ, start_response):
    write = start_response('200 OK', [
      ('Access-Control-Allow-Origin', '*'),
      ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),
      ('Content-Type', 'application/json')
    ])

    content = json.loads(environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', '0'))))
    res = model.analyze(content['data'])

    return [json.dumps(res)]
