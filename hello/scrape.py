# code from https://gist.githubusercontent.com/yanofsky/5436496/raw/962d4c2433e02cb486f583b832700330be973016/tweet_dumper.py

#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv

import pandas as pd

from keys import *


def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print(f"...{len(alltweets)} tweets downloaded so far")
    
    #transform the tweepy tweets into a 2D array that will populate the csv 
    outtweets = [[screen_name, tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    
    #write the csv  
#    with open(f'new_{screen_name}_tweets.csv', 'w') as f:
#        writer = csv.writer(f)
#        writer.writerow(["user_id","tweet_id","created_at","text"])
#        writer.writerows(outtweets)

    outtweets = pd.DataFrame(outtweets)
    outtweets.columns = ["user_id","tweet_id","created_at","text"]
    outtweets.to_csv("test.csv")
    return outtweets
    


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("elonmusk")
