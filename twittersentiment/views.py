from django.shortcuts import render
from django.template import loader
from django.views.generic import View,TemplateView
from django import forms
from .datascience.get_tweets import *
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

from .datascience.config import *
from .datascience.sentiment_analysis import *
import pandas as pd
import os

# Create your views here.
# everything takes a request object!python
class HomeView(View):
    def get(self, request):
        print("\n ===== Home View =====\n")
        query = str(request.POST.get("query", False))
        context = {'query': query}
        return render(request, 'twittersentiment/home.html',  context)

    
    
class GraphView(View):
    authentication_classes = []
    permission_classes = []
    def post(self, request):

        print("\n ===== Graph View =====\n")
        if request.method == 'POST':
            query = request.POST.get('query')
            # get_tweets.py - using tweepy to retrieves tweets
            twitterStream.filter(track=[query])
            
            # reading in tweets
            df = pd.read_csv('./tweets.txt')
            # nltk analyzer
            positive_count, negative_count, positives, negatives, negative_list, positive_list, count, total_count= analyzer.vader_sentiment(df=df)

            context = {'query':query,
                        'positive_count': positive_count,
                        'negative_count': negative_count,
                        'positives': positives,
                        'negatives': negatives,
                        'positive_list':positive_list,
                        'negative_list':negative_list,
                        'count': count,
                        'total_count': total_count,
                        }
            
            output = open('tweets.txt','w').close()
            output = open('tweets.txt','a')
            output.write('tweet, time\n')
            output.close()
            return render(request, 'twittersentiment/livegraph.html', context)