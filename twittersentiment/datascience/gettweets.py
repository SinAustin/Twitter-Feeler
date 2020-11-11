from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from .config import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
import json


class listener(StreamListener):
    """ twitter streaming class s"""
    
    def on_data(self, data):
        """ uses nltk sentiment model to classify tweets"""
        all_data = json.loads(data)
        
        try:
            tweet = all_data['text']
            
            if analyzer.polarity_scores(tweet)['compound'] >= -.1:
                sentiment_value = 'pos'
            else: 
                sentiment_value ='neg'
            print(tweet, sentiment_value)
            c

            confidence =.8
            if confidence*100>=80:
                output = open('tweets.txt','a')
                output.write(tweet)
                output.write(sentiment_value)
                output.write('\n')
                output.close()

            return(True)
        except:
            print('cant')

    def on_error(self, status):
        print(status)

