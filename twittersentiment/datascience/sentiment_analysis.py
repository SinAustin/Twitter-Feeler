import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
class analyzer():
    """ Analyzer class 
        1 - NLTK Vader
        2 - 
         """
    def __init__(self):
        self.count = 0

    def vader_sentiment(df):    
        """ nltk vader sentiment analzer
            INPUT= Dataframes with column named tweets
            OUPUT =  pos and neg sentiment counts"""
        #inst. analyszer
        analyzer = SentimentIntensityAnalyzer()

        # pos and neg count and lists
        positive_count = 0
        negative_count = 0

        positives = []
        negatives = []
        try:
            count = len(df)
            count = [ _ for _ in range(1,count)]
            # analyze tweets
            for tweet in df.tweet:
                if analyzer.polarity_scores(tweet)['compound'] >= .1:
                    sentiment_value  = 'pos'
                    positive_count += 1
                else:
                    sentiment_value = 'neg'
                    negative_count += 1
                positives.append(positive_count)
                negatives.append(negative_count)
        except:
            raise Exception('Vader Sentiment Analysis failed ') 
            
        return positive_count, negative_count, positives, negatives, count