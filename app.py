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
    result = request.form['title']
    listvid = youtube_search(result)

    list_tweets = twitter_search(result)

    #result_json = json.dumps(listvid, sort_keys=True, indent=4)
    #result = "zalupa"
    print(list_tweets)


    return render_template('results.html', res = listvid, tweets = list_tweets)
    #return render_template('results.html', tweets=list_tweets)





if __name__ == '__main__':
    app.run()