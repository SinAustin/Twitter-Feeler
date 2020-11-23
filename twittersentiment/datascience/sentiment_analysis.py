import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer 
from textblob import Word, TextBlob
import re
from nltk.stem import WordNetLemmatizer 
  
lemmatizer = WordNetLemmatizer() 

class analyzer:
    """ Analyzer class 
        1 - NLTK Vader
        2 - preprocessing via NLTK and Textblob for sentiment

         """
    def __init__(self):
        self.count = 0
    
    #NLTK
    def vader_sentiment(self,df):    
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
        total_count = positive_count+negative_count
        positive_list = [_ for _ in range(1,positive_count+1)]
        negative_list = [_ for _ in range(1,negative_count+1)]
            
        return positive_count, negative_count, positives, negatives, negative_list, positive_list, count, total_count

    # TEXTBLOB
    
    def tweet_preprocessor(self,tweet):
        custom_stopwords= ['RT']
        p_tweet = tweet
        p_tweet = p_tweet.replace('"', ' ')
        p_tweet = p_tweet.replace("'"," ")
        try:
            p_tweet = re.sub(r'[^\w]', ' ', tweet)
            p_tweet = ' '.join(token.lower() for token in nltk.word_tokenize(p_tweet)  if token not in stopwords.words('english'))
            p_tweet = ' '.join(token.lower() for token in nltk.word_tokenize(p_tweet)  if token not in custom_stopwords)
            p_tweet = ' '.join(lemmatizer.lemmatize(word) for word in p_tweet.split())
            return p_tweet
        except:
            print('*** Problem removing symbols from ', tweet)    
     
                            

    def tb_sentiment(self,df):
        df = df.dropna()
        df['processed_tweets'] = df['tweets'].apply(lambda x: analyzer.tweet_preprocessor(self,x))
        df = df.dropna()
        df['sentiment'] = df['processed_tweets'].apply(lambda x: TextBlob(x).sentiment[0])
        
        #sentiment over tweets/time series?
        df.loc[(df.sentiment > 0), 'wave'] = 1
        df.loc[(df.sentiment < 0), 'wave'] = -1
        df.loc[(df.sentiment == 0), 'wave'] = 0

        wave = df.wave
        l = [0]
        for i in df.wave:
            temp = i + l[-1]
            l.append(temp)
        wave = l
        wave_max = max(wave)
        wave_min = min(wave)

        wave_color_shift = []
        for i in wave:
            if i >=0 :
                wave_color_shift.append("rgba(54, 236, 162, 0.6)")
            else:
                wave_color_shift.append("rgba(255, 99, 132, 0.6)")

        # data for histogram
        count10 = sum(map(lambda x : 1>=x>.8, df.sentiment.values))
        count8 = sum(map(lambda x : .8>=x>.6, df.sentiment.values))
        count6 = sum(map(lambda x : .6>=x>.4, df.sentiment.values))
        count4 = sum(map(lambda x : .4>=x>.2, df.sentiment.values))
        count2 = sum(map(lambda x : .2>=x>0, df.sentiment.values))
        count0 = sum(map(lambda x : x==0, df.sentiment.values))
        countsub10 = sum(map(lambda x : (-1)<=x<(-.8), df.sentiment.values))
        countsub8 = sum(map(lambda x : (-.8)<=x<(-.6), df.sentiment.values))
        countsub6 = sum(map(lambda x : (-.6)<=x<(-.4), df.sentiment.values))
        countsub4 = sum(map(lambda x : (-.4)<=x<(-.2), df.sentiment.values))
        countsub2 = sum(map(lambda x : (-.2)<=x<0, df.sentiment.values)) 

        #variables to return and build charts
        hist_counts = [countsub10,countsub8,countsub6,countsub4,countsub2,count2,count4,count6,count8,count10]
        positive_count = len(df[df.sentiment>0])
        negative_count = len(df[df.sentiment<0])
        neutral_count = len(df[df.sentiment==0])
        total_count = negative_count + positive_count+neutral_count
        count_list = [_ for _ in range(1,total_count+1)]
        positive_list = [_ for _ in range(1,positive_count+1)]
        negative_list = [_ for _ in range(1,negative_count+1)]

        return positive_count, negative_count,neutral_count, negative_list, positive_list, total_count, count_list, wave, wave_max, wave_min, wave_color_shift, hist_counts
