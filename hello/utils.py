import tweepy #https://github.com/tweepy/tweepy
import csv
import numpy as np
import os
import pandas as pd

# from keys import *

from google.cloud import language_v1

consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']

access_key = os.environ['TWITTER_ACCESS_KEY']
access_secret = os.environ['TWITTER_ACCESS_SECRET']



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def get_tweets(screen_name, limit = 100):
    """
    Takes a screen name, returns a df of their recent tweets.
    Also saves it as a csv of tweets in  new_{screen_name}_tweets.csv
    """
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab or we've hit 200 tweets
    while len(new_tweets) > 0 and len(alltweets) < limit:
        print(f"getting tweets before {oldest}")
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=limit,max_id=oldest)
        
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
    outtweets.to_csv(f"new_{screen_name}_tweets.csv")
    return outtweets
 

def load_tweets(screen_name):
    return pd.read_csv(f"new_{screen_name}_tweets.csv", index_col = 0)
def get_sentiment(text_content):
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze

    Returns document sentiment score, magnitude
    """

    client = language_v1.LanguageServiceClient()


    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}
#    document = {"content": text_content, "type_": type_}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})

    return response.document_sentiment.score, response.document_sentiment.magnitude


def get_friends(screen_name):
    """get friends of user with entered screen name"""
    friends = pd.DataFrame({'friends': [user.screen_name for user in tweepy.Cursor(api.friends, screen_name=screen_name).items()]})
    friends.to_csv(f"{screen_name}_friends.csv")
    return friends

def load_friends(screen_name):
    """load friends of user from saved csv"""
    return pd.read_csv(f"{screen_name}_friends.csv")


def message_friend(user, friends):
    """ send a friendly DM to a friend """ 

    friend = np.random.choice(friends)

    # text to be sent
    text = "hi from friendly bot :) your pal {} looks like they could use a friend right now. reach out and have a nice conversation!".format(user)

    # sending the direct message
    direct_message = api.send_direct_message(friend, text)



