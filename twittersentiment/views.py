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
            
            df = pd.read_csv('./tweets.txt')
            # nltk analyzer
            positive_count, negative_count, positives, negatives, count = analyzer.vader_sentiment(df=df)
            print(count)
            
            context = {'query':query,
                        'positives': positives,
                        'count': count}
            
            return render(request, 'twittersentiment/livegraph.html', context)