from django.urls import path
from .views import *
from . import views
app_name = 'twittersentiment'
urlpatterns = [
    #<int= is number, question id>
    #twittersentiment/
    #home/
    path('home', views.HomeView.as_view(), name='home'),
    path('graph-results', views.GraphView.as_view(), name='graph'),
    path('', index, name='index'),
    # twittersentiment/*
    path('specifics/<int:question_id>/', detail, name='detail'),
    # poll/*/result
    path('<int:question_id>/results/',results, name='results'),
    # pools/*/vote
    path('<int:question_id>/vote/',vote, name='vote'),
    

]