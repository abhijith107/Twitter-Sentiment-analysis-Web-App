from http import client
import re
from sqlite3 import apilevel 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
from textblob.sentiments import NaiveBayesAnalyzer

from flask import Flask, render_template , redirect, url_for, request



def clean_tweet( tweet): 

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 
         
def get_tweet_sentiment( tweet): 
        
        
        analysis = TextBlob(clean_tweet(tweet)) 
        if analysis.sentiment.polarity > 0:
            return "positive"
        elif analysis.sentiment.polarity == 0:
            return "neutral"
        else:
            return "negative"

auth = tweepy.OAuthHandler('rgMGUb6XxGIgITnzZJ3DH0NCf', '6lHgO1b1MqEPgbLTsubjHTy1gb05ITZz1qovyDTr1hRZadMKnH')
auth.set_access_token('1573342016465149952-m4j1RJfrSPOvaRwDkE1rx9oUftXxue','7eY10P8Um2APWNcOIk45PfWNDwZWPuF5oBEzP2lLBT7Vp' )

class TwitterClient:
    api = tweepy.API(auth)
    def get_tweets(self, query, count=5): 
        
        count = int(count)
        tweets = [] 
        try: 
            
            fetched_tweets = self.api.search_tweets(q = query, count = count)
            
            for tweet in fetched_tweets: 
                
                parsed_tweet = {} 

                if 'retweeted_status' in dir(tweet):
                    parsed_tweet['text'] = tweet.text
                else:
                    parsed_tweet['text'] = tweet.text

                parsed_tweet['sentiment'] = get_tweet_sentiment(parsed_tweet['text']) 

                if tweet.retweet_count > 0: 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
            return tweets 
        except tweepy.TweepyException as e: 
            print("Error : " + str(e)) 

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def home():
  return render_template("index.html")

# ******handle level sentiment analysis
@app.route("/predict", methods=['POST','GET'])
def pred():
    #api = query.Check for ?rtweet::search_tweets()
	if request.method=='POST':
            query=request.form['query']
            count=request.form['num']
            client= TwitterClient()
            fetched_tweets = client.get_tweets(query, count) 
            return render_template('result.html', result=fetched_tweets)


@app.route("/predict1", methods=['POST','GET'])
def pred1():
	if request.method=='POST':
            text = request.form['txt']
            blob = TextBlob(text)
            if blob.sentiment.polarity > 0:
                text_sentiment = "positive"
            elif blob.sentiment.polarity == 0:
                text_sentiment = "neutral"
            else:
                text_sentiment = "negative"
            return render_template('result1.html',msg=text, result=text_sentiment)


if __name__ == '__main__':
    
    consumer_key = 'rgMGUb6XxGIgITnzZJ3DH0NCf' 
    consumer_secret = '6lHgO1b1MqEPgbLTsubjHTy1gb05ITZz1qovyDTr1hRZadMKnH'
    access_token = '1573342016465149952-m4j1RJfrSPOvaRwDkE1rx9oUftXxue'
    access_token_secret = '7eY10P8Um2APWNcOIk45PfWNDwZWPuF5oBEzP2lLBT7Vp'

    try: 
        auth = OAuthHandler(consumer_key, consumer_secret)  
        auth.set_access_token(access_token, access_token_secret) 
        api = tweepy.API(auth)
    except: 
        print("Error: Authentication Failed") 

    app.debug=True
    app.run(host='localhost')

