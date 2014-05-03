#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import model

def application(environ, start_response):
    write = start_response('200 OK', [('Content-Type', 'application/json')])

    content = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', '0')))
    res = model.analyze(content)

    return [json.dumps(res)]
