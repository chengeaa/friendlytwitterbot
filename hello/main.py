from .utils import *

def main(user, analyze_friends = False):

    try:
        user_tweets = load_tweets(user)
        print('load user tweets')
    except:
        user_tweets = get_tweets(user)
        print('fetch user tweets')

    #subsample
    user_tweets = user_tweets.iloc[:100, :]
    #load friends and friends' tweets
    if analyze_friends:
        try:
            friends = load_friends(user)
        except: friends = get_friends(user)

        print('friends loaded')

        friend_tweets = {}

        for friend in friends['friends']:
            try:
                print('loading tweets for', friend)
                friend_tweets[friend] = load_tweets(friend)
            except:
                print('fetching tweets for', friend)
                friend_tweets[friend] = get_tweets(friend)


    try:
        user_tweets = pd.read_csv("with sentiment.csv")
    except:
        sentiments = [get_sentiment(tweet)[0] for tweet in user_tweets['text']]
        user_tweets['sentiment'] = sentiments
        user_tweets.to_csv("with sentiment.csv")


    for friend in friends['friends']:
        try:
            print('loading sentiment for', friend)
            friend_tweets[friend] = pd.read_csv(f"{friend}_sentiments.csv")
        except:
            print('fetching sentiment for', friend)
            friend_sentiments= [get_sentiment(tweet)[0] for tweet in friend_tweets[friend]['text']]
            friend_tweets[friend]['sentiment'] = [get_sentiment(tweet)[0] for tweet in friend_tweets[friend]['text']]
            friend_tweets[friend].to_csv(f"{friend}_sentiments.csv")
    allsentiments = np.concatenate([data['sentiment'] for friend, data in friend_tweets.items()])
    network_average_sentiment = np.mean(allsentiments)

    user_average_sentiment = np.mean(user_tweets['sentiment'])

    print("user sentiment =", user_average_sentiment)
    try:
        print('average network sentiment = ', network_average_sentiment)
        return user_average_sentiment, network_average_sentiment
    except:
        print('no network sentiment')
        return user_average_sentiment




