from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
import json

#consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        try:
            tweet = all_data['text']
            print(1)
            if analyzer.polarity_scores(tweet)['compound'] >= -.1:
                sentiment_value = 'pos'
            else: 
                sentiment_value ='neg'
            print(tweet, sentiment_value)

            confidence =.8
            if confidence*100>=80:
                output = open('tweets','a')
                output.write(sentiment_value)
                output.write('\n')
                output.close()

            return(True)
        except:
            print('cant')

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["election"])