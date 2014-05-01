#!/usr/bin/python
import sys
import time
import re
import os
import math
import json
from pprint import pprint

round0 = re.compile('\'')

# markup
round0a = re.compile('<[^>]*>|&\w*;')
round1 = re.compile('[-,|<>;:\/\.!\"?)(\n]')

# something like stop words
round2 = re.compile(' (a |of |as |is |am |had |that |those |are |the |and |for )*')

# endings - primitive stemming
round2a = re.compile('(ly) ')

round3 = re.compile('\s+')

# this set of words shouldn't count in our idf calculations
empty = set(['i', 'in', 'you', 'ok', 'to'])

# The words on the left get replaced with the ones on the right.
wordmap = {
# parts of speech
  'youre': 'you',
  'your': 'you',
  'im': 'i',
  'my': 'i',
  'ive': 'i',
   
# profanity
  'shit' : 'fuck',
  'fucking': 'fuck',

# insults
  'moron': 'idiot',
  'stupid': 'idiot',
  'fucktard': 'idiot',
  'shithead': 'idiot',
  'dipshit': 'idiot',

# For our purposes, these adjectives will be reduced to just
# a negative "bad"
  'stupid': 'bad',
  'incompetent': 'bad',
  'horrible': 'bad',
  'terrible': 'bad',

# Blame game
  'fault': 'error',
  'mistake': 'error',
  'sorry': 'error',

  'told': 'said',
  'stated': 'said',
  'claimed': 'said',
  'wrote': 'said',

# Certainty
  'precise' : 'exact',

# Arrogance
  'obvious': 'clear',

# Calling someone out
  'incorrect': 'wrong',
};

scorelist = {
# This anywhere is a bad idea.
  'fuck': 1,

  'crap': 0.9,
  'bad': 0.4,

# Frustration
  'alright': 0.2,
  'whatever': 0.2,
  'alright whatever': 0.3,
  'real dont': 0.4,
  'ridiculous': 0.6,
  'asinine': 0.9,
  'pain': 0.2,
  'painful': 0.3,
  'putting up with': 0.5,
  'utter': 0.4,
  'utter ridiculous': 0.6,
  'final': 0.3,
  'many times': 0.4,
  'how many times': 0.6,
  'jesus christ': 0.8,
  'perhaps you': 0.6,
  'stop bugging': 0.3,
  'stop bugging you': 0.4,
  'stop bugging me': 0.9,
  'so indecisive': 0.7,
  'i mean': 0.15,
  'we went over': 0.2,
  'way i can': 0.3,
  'why': 0.2,
  'dont care': 0.2,
  'i sick': 0.2,
  'move on': 0.3,
# probably love *of* god
  'love god': 0.4,
# accusatory
  'do you': 0.2,

# This is the blanket term for all insults
  'idiot': 0.9,

# Really bad
  'you idiot': 1,
  'you dense': 0.9,
# as in you're really blah
  'you real': 0.7,
# eh, still pretty awful
  'i idiot': 0.8,

# YOUR mistake
  'you error': 0.7,
  'you wrong': 0.5,

# really bad idea here...
  'you said': 0.9,
# man, even worse
  'i said': 1.0,

# angry things
  'putting up': 0.7,
  'i just': 0.7,
  'endure': 0.5,
  'troll': 0.4,
  'mo': 0.3,

# defensive
  'just trying': 0.3,
  'just thought': 0.3,

# pointing out something you've said before isn't a great one
  'again': 0.1,
# unless it's a thank you!
  'thanks again': -0.2,

# This would normally be "over and over" but 'and' is removed.
  'over over': 1.0,
  'over again': 0.3,
  'you keep': 0.2,
  'before': 0.2,

# Even if it is the same, it's best not to point it out.
  'identical': 0.2,
  'same': 0.25,

# confidence is usually bad form.
  'i sure': 0.2,
  'i know': 0.2,
# careful careful
  'simple': 0.15,
  'easy': 0.2,
# but this is too
  'dont understand': 0.1,
  'dont know': 0.15,

# big no no talking to clients
# even if it's i should rtfm
  'rtfm': 1.0,
  'rtm': 0.8,

# versus MINE, also somewhat bad
  'i error': 0.3,

  'clear': 0.1,

# Now for some good ones.

# as in 'get to you'
  'to you': -0.2,
  'eod': -0.3,

# presuming this is associated with CTAs
  'document': -0.2,
#  'email': -0.15,
  'proposal': -0.2,

# acknowledging without blame
  'i see': -0.2,

# slapping someone in the face and 
# stating something is obvious
  'you see': 0.2,

# you've gone out of your way!
  'arranged': -0.4,
  'prepared': -0.3,
  'i prepared': -0.5,
  'inspection': -0.4,
  'visual inspection': -0.4,
  'i building': -0.2,
  'ill do': -0.15,
  'finish': -0.2,

# or at least you intend to
  'will arrange': -0.2,
  'will prepare': -0.15,
  'to do': -0.15,
# eh, maybe not
  'to do this': 0.15,
  'i was': 0.05,

# this is an interesting one. From there is positive
  'from there': -0.3,
# from here is probably frustration.
  'from here': 0.2,

# you don't know for sure, that's good!
  'i think': -0.2,
  'pretty close': -0.3,
  'i know where': -0.15,
  'its difficult': -0.1,
  'i dont know': 0.15,

# kissing ass
  'honored': -0.5,
  'pleasure': -0.5,
  'your time': -0.2,
  'i value': -0.3,
  'great': -0.05,
  'splendid': -0.1,
# over the top eh?
  'been such pleasure': -0.7,
  'such pleasure': -0.7,
  'flattered': -0.3,
  'esteemed': -0.4,
  'delight': -0.4,
  'delightful': -0.4,

# manners!
  'enjoy': -0.2,
  'enjoyed': -0.2,
  'id like': -0.2,
  'hope to hear': -0.2,
  'from you soon': -0.2,
  'be able': -0.15,
  'thanks': -0.2,
  'thank you': -0.2,
  'please': -0.2

}


content = sys.stdin.read()

wordcount = 0
score=0
lastword=''
lastlastword=''
analysis=[]

words = content.lower()
words = re.sub(round0,'',words)
words = re.sub(round0a,' ',words)
words = re.sub(round1,' ',words)
# articles -- this makes the ngrams better ... because of adjacency we run it twice
words = re.sub(round2,' ',words)
words = re.sub(round2a,' ',words)
words = re.sub(round3,' ',words).split()

for i in words: 

# Here's where we do the word reduction
  if i in wordmap:
    i = wordmap[i]  

  if i not in empty:
    wordcount += 1

  twogram = lastword + ' ' + i
  threegram = lastlastword + ' ' + lastword + ' ' + i

  lastlastword = lastword
  lastword = i

  if threegram in scorelist:
    point = scorelist[threegram]
    analysis.append([ threegram, point ])
    score += (point * 3)

# If the 2-gram was found
# we add that * 2
  elif twogram in scorelist:
    point = scorelist[twogram]
    analysis.append([ twogram, point ])
    score += (point * 2)

  elif i in scorelist:
    point = scorelist[i]
    analysis.append([ i, point ])
    score += point

# now we'll do the score divided by the length of words 
score = (score / (wordcount))

# take our multiplier
multiplier = 1
if score < 0:
  multiplier = -1
  score *= -1

# do a double square-root for sciency reasons
score = math.sqrt(math.sqrt(score))

# and put our multiplier back in
score *= multiplier

# now we normalize it
score += 1
score /= 2

print json.dumps({ 'score': score, 'analysis': analysis, 'norm': wordcount })
