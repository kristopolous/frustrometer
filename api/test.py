#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import sys
import log
import model

content = sys.stdin.read()
log.logit(content)
print json.dumps(model.analyze(content))
