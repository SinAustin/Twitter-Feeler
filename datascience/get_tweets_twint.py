import pandas as pd
import time
import twint
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class Tweets():
    ''' function to scrap and analysis tweets'''
    def __init__(self):
        ''' head node is just a place holder to give a pointer to the first node '''
        self.limit = 100000
    def getTweets(limit,subject,start, end, file_name):
        ''' retrieves tweets using twint and save them to a json'''
        
        # twint config
        #config.Username = ''
        config = twint.Config()
        #config.Username = ''
        config.Search = subject
        config.Limit = limit
        config.Lang = "en"

        #config.Timedelta
        config.Show_hashtags = True
        config.Since = start
        config.Until = end
        #config.Database = 
        config.Hide_output = True
        config.Store_csv = True
        config.Output = 'biden_tweets_biden_speech.csv'

        # searching
        print('STARTING SEARCH\n')
        
        try:
            twint.run.Search(config)
        except:
            raise ValueError('\n Tweet retrieval FAILED\n')

    def tweets_analyser(tweets):
        ''' takes series of tweets and outputs a text file with 
        pos or neg to represent the tweets sentiment.
        This text file will be used to graph a feed to show the
        displayed sentiment during the speech.'''
        tweets_done = 0
        for i in tweets:
            time.sleep(.001)
            if analyzer.polarity_scores(i)['compound'] >= 0:
                sentiment = 'pos'
            else:
                sentiment = 'neg'
            tweets_done += 1
            print('tweets done:', tweets_done,sentiment)
            output = open('biden_speech_trump_sentiment.txt','a')
            output.write(sentiment)
            output.write('\n')
            output.close() 
        return 'Done'   
    
#grabbing tweets with 'trump in them   
Tweets.getTweets(100000,'debate','2020-08-20 22:18:00','2020-08-20 22:27:00', 'biden_tweets_biden_speech.csv')    

#loading in the data scraped with twint
#tweets_df = pd.read_csv('./trump_tweets_biden_speech') 

# inst our analyser
#analyzer = SentimentIntensityAnalyzer()

#calling the analyser function
#Tweets.tweets_analyser(tweets_df.tweet)   

        
