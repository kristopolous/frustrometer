#!/bin/env python
import io

def logit(text):
  fh = io.open('/var/log/frust-log', 'a')
  fh.write(unicode(text))
  fh.close()

def faveit(text):
  print text
