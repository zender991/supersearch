from TwitterSearch import *
import json
import config

def twitter_search(query):

    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    query_list = query.split()
    tso.set_keywords(query_list)
    tso.set_include_entities(False)

    ts = TwitterSearch(
        consumer_key=config.CONSUMER_KEY,
        consumer_secret=config.CONSUMER_SECRET,
        access_token=config.ACCESS_TOKEN,
        access_token_secret=config.ACCESS_TOKEN_SECRET
    )

    unsorted_tweets = []
    tweets_list = []
    loop_tweets = []

    for tweet in ts.search_tweets_iterable(tso):
        loop_tweets.append(tweet['user']['screen_name'])
        loop_tweets.append(tweet['text'])

        unsorted_tweets.append(loop_tweets)
        loop_tweets = []

    for tweet in unsorted_tweets:
        loop_tweet_dict = { }
        loop_tweet_dict['tweeter_user'] = tweet[0]
        loop_tweet_dict['tweeter_text'] = tweet[1]
        tweets_list.append(loop_tweet_dict)

    return tweets_list


def convert_twitter_results(search_query):

    list_tweets = twitter_search(search_query)
    twitter_json = json.dumps(list_tweets)
    twitter_list_final = json.loads(twitter_json)

    return twitter_list_final

