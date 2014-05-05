#!/usr/bin/env python
def autocorrect(original, analysis):
  synonym = {
    'fuck you': [
      'We have really had some difficulties',
      'I need to discuss a few things with you',
      'I should really work on my relationship with you'
    ],
    'you motherfucker': [
    ],
    'you suck': [
      'I see a lot of need for improvement'
    ]
  }
