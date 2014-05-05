#!/bin/env python
import io

def logit(text):
  fh = io.open('/var/log/frust-log', 'a')
  fh.write(text)
  fh.close

def faveit(text):
  print text
