#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import sys
import model

content = sys.stdin.read()
print json.dumps(model.analyze(content))
