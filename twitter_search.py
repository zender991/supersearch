from TwitterSearch import *
import json

def twitter_search(query):

    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    #tso.set_keywords(['Guttenberg', 'Doktorarbeit']) # let's define all words we would like to have a look for
    #tso.set_language('en')
    #query = "Tony Croos"
    query_list = query.split()

    tso.set_keywords(query_list)


    tso.set_include_entities(False)

    ts = TwitterSearch(
        consumer_key='RQfEhM8ZeWjHBwYsR5T8Rkivp',
        consumer_secret='ib4YMVrccLZCv5vxc3mHumXw102SAcFj7N4N2CWexnbdFv87CJ',
        access_token='836684282001297408-bk82K2vxYklhsDPiCME22DnfZAcRluL',
        access_token_secret='gJYRJ68kVGcM9RxR6e9BWou077a7Jk5te3pQ9HxwbBMih'
    )

    tweets = []
    tweets_list = []
    temp_list = []

    for tweet in ts.search_tweets_iterable(tso):
        #print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))

        #tweets.append('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))

        temp_list.append(tweet['user']['screen_name'])
        temp_list.append(tweet['text'])

        tweets.append(temp_list)

        temp_list = []

    #print(tweets)
    for tweet in tweets:
        temp_tweet = { }
        temp_tweet['tweeter_user'] = tweet[0]
        temp_tweet['tweeter_text'] = tweet[1]
        tweets_list.append(temp_tweet)


    return tweets_list



#twitter_search("Justin Bieber")

