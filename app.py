from flask import Flask, render_template, request
import json
from TwitterSearch import *
from youtube_search import youtube_search
from twitter_search import twitter_search

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')



@app.route('/results', methods=['POST'])
def show():
    form_query = request.form['title']
    youtube_videos = youtube_search(form_query)

    youtube_videos_json = json.dumps(youtube_videos)

    youtube_videos_list = json.loads(youtube_videos_json)

    list_tweets = twitter_search(form_query)

    twitter_json = json.dumps(list_tweets)

    twitter_list_template = json.loads(twitter_json)

    #print(list_tweets)


    return render_template('results.html', yt_vid = youtube_videos_list, tweets = twitter_list_template)
    #return render_template('results.html', tweets=list_tweets)





if __name__ == '__main__':
    app.run()