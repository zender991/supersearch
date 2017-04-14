from TwitterSearch import *
import json

def twitter_search(query):

    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    query_list = query.split()
    tso.set_keywords(query_list)
    tso.set_include_entities(False)

    ts = TwitterSearch(
        consumer_key='RQfEhM8ZeWjHBwYsR5T8Rkivp',
        consumer_secret='ib4YMVrccLZCv5vxc3mHumXw102SAcFj7N4N2CWexnbdFv87CJ',
        access_token='836684282001297408-bk82K2vxYklhsDPiCME22DnfZAcRluL',
        access_token_secret='gJYRJ68kVGcM9RxR6e9BWou077a7Jk5te3pQ9HxwbBMih'
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

