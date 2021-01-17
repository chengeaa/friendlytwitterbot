from utils import *

analyze_friends = False

#load user's tweets
user = "elonmusk"
try:
    user_tweets = load_tweets(user)
except:
    user_tweets = get_tweets(user)


#subsample
user_tweets = user_tweets.iloc[:100, :]
#load friends and friends' tweets
if analyze_friends:
    try:
        friends = load_friends(user)
    except:
        friends = get_friends(user)

    friendtweets = []

    for friend in friends:
        try:
            friendtweets += [load_tweets(friends)]
        except:
            friendtweets += [get_tweets(friends)]


sentiments = [get_sentiment(tweet)[0] for tweet in user_tweets['text']]
user_tweets['sentiment'] = sentiments

print(user_tweets)
user_tweets.to_csv("with sentiment.csv")
