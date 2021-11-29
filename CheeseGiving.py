# coding: utf-8
'''
------------------------------------------------------------------------------
Copyright 2021 Jerome Lefebvre
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
------------------------------------------------------------------------------
'''

import requests
import json
from random import choice, shuffle, randrange
import re

# Generate a key here: https://bonus.ly/api
# Make sure it have write access
APIKEY = ''
URL = "https://bonus.ly/api/v1/bonuses?access_token=" + APIKEY

HEADERS = {
  'Content-Type': 'application/json',
}

CHEERS_RAW = '''"Alone we can do so little; together we can do so much." - Helen Keller
"Talent wins games, but teamwork and intelligence win championships." - Michael Jordan
"Teamwork begins by building trust. And the only way to do that is to overcome our need for invulnerability." - Patrick Lencioni
"It is literally true that you can succeed best and quickest by helping others to succeed." - Napolean Hill
"If you want to lift yourself up, lift up someone else." - Booker T. Washington
"None of us, including me, ever do great things. But we can all do small things, with great love, and together we can do something wonderful." - Mother Teresa
"Alone we can do so little; together we can do so much." - Helen Keller
"If everyone is moving forward together, then success takes care of itself." - Henry Ford
"Many ideas grow better when transplanted into another mind than the one where they sprang up." - Oliver Wendell Holmes
"If I have seen further, it is by standing on the shoulders of giants." - Isaac Newton
"Teamwork is the ability to work together toward a common vision. The ability to direct individual accomplishments toward organizational objectives. It is the fuel that allows common people to attain uncommon results." - Andrew Carnegie
"It is the long history of humankind (and animal kind, too) that those who learned to collaborate and improvise most effectively have prevailed." - Charles Darwin
"Coming together is a beginning, staying together is progress, and working together is success." - Henry Ford
"Talent wins games, but teamwork and intelligence win championships." - Michael Jordan
"The strength of the team is each individual member. The strength of each member is the team." - Phil Jackson
"The best teamwork comes from men who are working independently toward one goal in unison." - James Cash Penney
"Politeness is the poison of collaboration." - Edwin Land
"Find a group of people who challenge and inspire you, spend a lot of time with them, and it will change your life." - Amy Poehler
"Effectively, change is almost impossible without industry-wide collaboration, cooperation, and consensus." - Simon Mainwaring
"Teamwork begins by building trust. And the only way to do that is to overcome our need for invulnerability." - Patrick Lencioni
"You need to be aware of what others are doing, applaud their efforts, acknowledge their successes, and encourage them in their pursuits. When we all help one another, everybody wins." - Jim Stovall
"It is literally true that you can succeed best and quickest by helping others to succeed." -Napolean Hill
"The whole is other than the sum of the parts." - Kurt Koffka
"A group becomes a team when each member is sure enough of himself and his contribution to praise the skills of others." - Norman Shidle'''
CHEERS = CHEERS_RAW.split('\n')

# Can use outlook to extract this list of users
USERS_RAW = '''First1 Last1  <fLast1@osisoft.com>;
First2 Last2  <fLast2@osisoft.com>;
First3 Last3  <fLast3@osisoft.com>;'''

USERS = list(set([re.search('<([^>]+)>', user, re.IGNORECASE).group(1) for user in USERS_RAW.split('\n')]))
shuffle(USERS)

remainingCheese = 35 # The amount of cheese you want to give out
MEAN = int(remainingCheese/len(USERS))

# The last user get all remaining cheese if any
for user in USERS[:-1]:
  if remainingCheese <= 0:
    break
  randomCheese = min(remainingCheese, randrange(1,2*MEAN-2))
  remainingCheese -= randomCheese
  payload = json.dumps({
    "receiver_email": user,
    "amount": randomCheese,
    "hashtag": "#teamwork",
    "reason": choice(CHEERS)
  })
  print(payload)
  response = requests.request("POST", URL, headers=HEADERS, data=payload)
  
# The last person in the list gets all the cheese
if (remainingCheese > 0):
  payload = json.dumps({
    "receiver_email": USERS[-1],
    "amount": remainingCheese,
    "hashtag": "#teamwork",
    "reason": choice(CHEERS)
  })
  response = requests.request("POST", URL, headers=HEADERS, data=payload)
