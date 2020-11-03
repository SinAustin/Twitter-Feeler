from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Questions, Choices
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import View
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Questions, Choices
# Create your views here.
# everything takes a request object!python

def home(request):
    return render(request, 'polls/home.html', {})


class ChartData(APIView):
   
    authentication_classes = []
    permission_classes = []

    def get_data(self, **kwargs):
        context = super().get_data(**kwargs)
        context['qs'] = polls.objects.all()
        return context


def get_data(request, *args, **kwargs):
    data = {
        'sales': 100,
        'customers':10,
    }
    return JsonResponse(data)


def index(request):
    latest_question_list = Questions.objects.all()
    #template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }

    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    """try:
        question = Questions.objects.get(pk=question_id)
    except Questions.DoesNotExist:
        raise Http404('Question not found')

    return render(request, 'polls/detail.html', {'question': question})"""
    question = get_object_or_404(Questions, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request,question_id):
    question = get_object_or_404(Questions, pk=question_id)
    try:
        selected_choice = question.choices_set.get(pk=request.POST['choice'])
    except (KeyError, Choices.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

         