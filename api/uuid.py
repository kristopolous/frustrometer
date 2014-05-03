#!/usr/bin/python
# -*- coding: UTF-8 -*-
import uuid

def application(environ, start_response):
    write = start_response('200 OK', [('Content-Type', 'application/json')])

    return ["frust.setuuid('" + str(uuid.uuid4()) + "');"]
