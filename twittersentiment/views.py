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
            df = pd.read_csv('./tweets.txt',error_bad_lines=False, engine="python")
            # analyzer
            
            positive_count, negative_count,neutral_count, negative_list, positive_list, total_count,count_list, wave, wave_max, wave_min, wave_color_shift, hist_counts= analyzer.tb_sentiment(self, df=df)
           
            context = {'query':query,
                        'positive_count': positive_count,
                        'negative_count': negative_count,
                        'neutral_count': neutral_count,
                     
                        'positive_list':positive_list,
                        'negative_list':negative_list,
                       
                        'total_count': total_count,
                        'count_list': count_list,
                        'wave': list(wave),
                        'wave_max': wave_max,
                        'wave_min': wave_min,
                        'wave_color_shift': list(wave_color_shift),
                        'hist_counts':hist_counts
                        }
            
            output = open('tweets.txt','w').close()
            output = open('tweets.txt','a')
            output.write('tweets, time\n')
            output.close()
            return render(request, 'twittersentiment/livegraph.html', context)