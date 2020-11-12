from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Questions, Choices
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.generic import View,TemplateView
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Questions, Choices
from django import forms
from .datascience.gettweets import listener  
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from .config import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
# Create your views here.
# everything takes a request object!python
class HomeView(View):
    def get(self, request):
        #do something with 'GET' method
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
            """auth = OAuthHandler(ckey, csecret)
            auth.set_access_token(atoken, asecret)

            twitterStream = Stream(auth, listener())
            twitterStream.filter(track=[query], count = 10)"""
            
            context = {'query':query}
            
            return render(request, 'twittersentiment/livegraph.html', context)


def index(request):
    latest_question_list = Questions.objects.all()
    #template = loader.get_template('twittersentiment/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }

    return render(request, 'twittersentiment/index.html', context)

def detail(request, question_id):
    """try:
        question = Questions.objects.get(pk=question_id)
    except Questions.DoesNotExist:
        raise Http404('Question not found')

    return render(request, 'twittersentiment/detail.html', {'question': question})"""
    question = get_object_or_404(Questions, pk=question_id)
    return render(request, 'twittersentiment/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    return render(request, 'twittersentiment/results.html', {'question': question})

def vote(request,question_id):
    question = get_object_or_404(Questions, pk=question_id)
    try:
        selected_choice = question.choices_set.get(pk=request.POST['choice'])
    except (KeyError, Choices.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'twittersentiment/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('twittersentiment:results', args=(question.id,)))
