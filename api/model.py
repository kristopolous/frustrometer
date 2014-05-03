#!/usr/bin/python
import re
import math

snark = [
 "Lick those boots!",
 "You appear to be groveling.",
 "Walking on eggshells?",
 "Apologizing for something?",
 "Is this a job interview?",
 "Just delightful.",
 "Quite polite.",
 "So charming!",
 "You're doing fine.",
 "Such diplomatic prose!",
 "Nothing wrong with this.",
 "Everything is going nicely",
 "Tactful like a chess game.",
 "We're doing ok.",
 "Not too worried yet...",
 "Assertive and confident?!",
 "Forward and direct?",
 "What's your goal?",
 "Blunt. Is that what you want?",
 "What's your desired impact?",
 "Editing is a great idea.",
 "Having a bad day?",
 "Different wording?",
 "Starting to get saucy?",
 "Being a bit snippy?",
 "Approach this from a different angle.",
 "Rather imposing.",
 "Look at your word choice.",
 "Would YOU like to receive this?",
 "A bit too aggressive.",
 "Really, what will you gain from posting this?",
 "Step back for a few minutes.",
 "Maybe you shouldn't say anything?",
 "Read it outloud to yourself.",
 "Very contemptuous. Breath in...",
 "Perhaps finish this tomorrow?",
 "That's flippant and combative!",
 "People Will read this you know, right?",
 "Danger Will Robinson!",
 "You are crossing the Rubicon.",
 "What Audacious Language!", 
 "Careful careful...",
 "You may be offending many people here.",
 "These are fighting words.",
 "You're starting fires here.",
 "This is a bad idea.",
 "You can't be serious...",
 "The bridges are burning.",
 "1, 2, 3, 4 I declare War!",
 "Pack up your things and leave the building."
]

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
empty = set(['this', 'its', 'how', 'did', 'i', 'in', 'you', 'ok', 'to'])

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
  'motherfucker': 'fuck',
  'fucker': 'fuck',

# insults
  'asshole': 'idiot',
  'dickhead': 'idiot',
  'nigger': 'idiot',
  'chink': 'idiot',
  'bitch': 'idiot',
  'cocksucker': 'idiot',
  'cunt': 'idiot',
  'fag': 'idiot',
  'faggot': 'idiot',
  'whore': 'idiot',
  'slut': 'idiot',
  'dipshit': 'idiot',
  'dumbfuck': 'idiot',
  'fucktard': 'idiot',
  'moron': 'idiot',
  'retarded': 'idiot',
  'retard': 'idiot',
  'shithead': 'idiot',

# For our purposes, these adjectives will be reduced to just
# a negative "bad"
  'stupid': 'bad',
  'incompetent': 'bad',
  'horrible': 'bad',
  'terrible': 'bad',

# Should probably avoid these things too
  'crazy': 'bad',
  'insane': 'bad',
  'nuts': 'bad',

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
  'dumb': 0.5,
  'bad': 0.4,

# really bad idea here.
  'suck i': 0.95,
  'kiss i': 0.95,
  'lick i': 0.95,
  'in ass': 0.95,
  'you suck': 0.8,
  'you ugly': 0.95,
  'you fat': 0.95,
  'you idiot': 0.95,

# racist vs. racial
# Saying "he is black" is ok. 
# But the plural "black(s)" is almost 
# always pretty inflammatory
  'blacks': 1.0,
  'asians': 1.0,
  'whites': 1.0,
# Not as bad, but still pretty racy.
  'black people': 0.8,
  'asian people': 0.8,
  'white people': 0.8,
# Nationalities and religion identifiers
# are more ambiguous. Saying "Most muslims believe ..."
# is perfectly acceptable in some contexts.  
# "Most blacks believe ..." is totally not.

# Sarcastometer!
  'oh look': 0.3,
  'duh': 0.6,
  'bingo': 0.4,

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
  'real pain': 0.7,
  'was waiting': 0.6,
  'am waiting': 0.6,
  'im so tired': 0.4,
  'so tired of': 0.4,
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
  'hell': 0.5,
  'to hell': 0.6,
  'i mean': 0.15,
  'we went over': 0.2,
  'way i can': 0.3,
  'so late': 0.3,
  'dont care': 0.2,
  'dont want': 0.3,
  'dont want to': 0.3,
  'i sick': 0.2,
  'move on': 0.3,

# why is generally pretty bad.  Try
# to put it in a few sentances.  It 
# usually suggests an error or at 
# best states a challenge
#
# A way around "why" could be something like
# "Could you help me better understand " ... how or "what"
# or "Your reasoning" ... etc.  It's more gentle and 
# specific.
  'why': 0.2,
# probably love *of* god
  'love god': 0.4,
# accusatory
  'do you': 0.2,
  'you fire': 0.5,
  'i fire': 0.5,

# Defeatist
  'impossible': 0.2,
  'not possible': 0.2,

# This is the blanket term for all insults
  'idiot': 0.9,

# Fairly insensitive
  'oriental': 0.5,
# maybe, maybe not --- depends on who is saying it
  'jews': 0.3,

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
  'didnt': 0.15,
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
  'stfu': 1.0,
  'wtf': 1.0,
  'rtm': 0.8,
  'omg': 0.7,
  'omfg': 0.9,

# versus MINE, also somewhat bad
  'i error': 0.3,
  'not mine': 0.2,
  'not i': 0.2,
  'not i problem': 0.4,

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

# vapid positive things
  'cute': -0.15,
  'lovely': -0.2,
  'adorable': -0.3,
  'you good': -0.4,
  'you great': -0.4,
  'beautiful': -0.25,
  'charming': -0.3,

# careful careful ... that's pretty sarcastic
  'would be fantastic': 0.7,
  'a fantastic job': -0.1,

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
  'pleasure to meet': -0.3,
  'you time': -0.2,
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
  'sir': -0.2,
  'madam': -0.2,
  'was so nice': -0.2,
  'how nice': -0.2,
  'nice to see': -0.2,
  'dear': -0.3,
  'dearest': -0.3,
  'enjoy': -0.2,
  'enjoyed': -0.2,
  'id like': -0.3,
  'hope to hear': -0.2,
  'from you soon': -0.2,
  'be able': -0.15,
  'thanks': -0.2,
  'thank you': -0.2,
  'hi': -0.3,
  'hello': -0.3,
  'sincerely': -0.3,
  'please': -0.2,
  'feel free': -0.2,
}

def analyze(content):
  if len(content) == 0:
    return ({ 'score': 0, 'snark': "" })

  show = False
  wordcount = 0
  score = 0
  lastword = ''
  lastlastword = ''
  analysis = []

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
      show = True
      analysis.append([ threegram, point ])
      score += (point * 3)

# If the 2-gram was found
# we add that * 2
    elif twogram in scorelist:
      point = scorelist[twogram]
      show = True
      analysis.append([ twogram, point ])
      score += (point * 2)

    elif i in scorelist:
      point = scorelist[i]
      show = True
      analysis.append([ i, point ])
      score += point

    else:
# we will take a small positive read on every word we
# see
      if i not in empty:
        score += -0.07 

# now we'll do the score divided by the length of words 
  wordcount = max([wordcount, 1])
  score = (float(score) / float(wordcount))

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
  score += 1.0
  score /= 2.0

# no words at all
  if show == False: #len(analysis) == 0:
    score = 0

# score is weighted between 0 and 1
# We multiply it by the length of our snarky list,
# then round it, discard the precision to an int, and reference
# into the table.
  comment = snark[int(round((len(snark) - 1) * score))]

  return ({ 'snark': comment, 'score': score })
