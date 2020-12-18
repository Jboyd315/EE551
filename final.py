#Justin Boyd
#EE-551WS Final Project
#18 December 2020

import tweepy
import datetime
import os
import json
import geocoder
import csv

#Twitter API keys

CONSUMER_KEY = "xehe5pG7TGdEYSZjRhZoo6Wnr"
CONSUMER_KEY_SECRET = "5F7E95lQqvuO6D5xBbd65zgKlkE6MsikjZoJvtHiqh8fDAs6XC"
ACCESS_TOKEN = "2598322188-OZrDljjUUuj5WzmgvSkePGXutjWcVboPxkmHn2L"
ACCESS_TOKEN_SECRET = "KsNoYFgGPBV9eiaYn2MR7aUCSdRNZR9R2m5FRgBCCTXOQ"

authenticate = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#Checks to make sure data is being pulled at the right rate and stops if it does
api = tweepy.API(authenticate, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

#Writes to json file with trending tweets from loc
u = input("Enter city for trending data: ")
g = geocoder.osm(u)
closest_loc = api.trends_closest(g.lat, g.lng)
data = api.trends_place(closest_loc[0]['woeid'])
with open("TrendByLocation.json".format(u),"w") as wp:
    wp.write(json.dumps(data, indent=1))

#Writes (item) number of tweets to csv with the inputed hashtag
z = input("Enter hashtag you want to look up: ")
csvFile = open('HashtagData.csv', 'a')
csvWriter = csv.writer(csvFile)
for tweet in tweepy.Cursor(api.search,q = z,count=100,
                           lang="en",
                           since="2015-12-16").items(100):
    csvWriter.writerow([tweet.text.encode('utf-8')])

#Prints top 5 hashtags to output from location
hashtags = [trend['name'] for trend in data[0]['trends'] if trend['name'].startswith('#')]
print(hashtags)  

#tweet volumes to output for the popular ones
for trend in data[0]['trends']:
    popular = [trend['tweet_volume']]
    nam = [trend['name']]
    if trend['tweet_volume'] is not None:
        print(nam)
        print(popular) 

#NBA teams specific hashtags and Woeid's

team_hashtags = ['#TruetoAtlanta', '#Celtics', '#WeGoHard', '#AllFly', '#BullsNation', '#BeTheFight', '#MFFL', '#MileHighBasketball', '#DetroitBasketball', '#DubNation', '#OneMission', '#IndianaStyle', '#ClipperNation', '#LakeShow', '#GrindCity', '#HeatTwitter', '#FearTheDeer', '#Timberwolves', '#WontBowDown', '#NewYorkForever', '#ThunderUp', '#MagicAboveAll', '#PhilaUnite', '#RisePHX', '#RipCity','#SacramentoProud', '#GoSpursGo', '#WeTheNorth', '#TakeNote', '#RepTheDistrict']
team_loc = [2357024, 2367105, 2459115, 2378426, 2379574, 2381475, 2388929, 2391279, 2391585, 2463583, 2424766, 2427032, 2442047, 2442047, 2449323, 2450022, 2451822, 2452078, 2458833, 2459115, 2464592, 2466256, 2471217, 2471390, 2475687, 2486340, 2487796, 4118, 2487610, 2514815]

#Function that goes through location woeid's, finds the trends, then a cursor looks for hashtags 
#in the trends and writes to CSV

y = 0
for x in team_loc:
    loc = x
    data = api.trends_place(loc)
    trends = json.loads(json.dumps(data, indent=1))
    for trend in trends[0]["trends"]:
        z = 0
        if z > 10:
           break
        for tweet in tweepy.Cursor(api.search, q = team_hashtags[y],count=50, lang="en", since="2020-12-12").items(10):
            csvFile = open('NBAHashtagData.csv', 'a')
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow([tweet.text.encode('utf-8')])
        z = z + 1
    y = y + 1
           
