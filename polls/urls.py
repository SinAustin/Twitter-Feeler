from django.urls import path
from .views import *
app_name = 'polls'
urlpatterns = [
    #<int= is number, question id>
    #polls/
    #home/
    path('home', home, name='home'),
    path('api/get_data/', get_data, name='get_data'),
    path('api/chart/get_data/', ChartData.as_view()),
    path('', index, name='index'),
    # polls/*
    path('specifics/<int:question_id>/', detail, name='detail'),
    # poll/*/result
    path('<int:question_id>/results/',results, name='results'),
    # pools/*/vote
    path('<int:question_id>/vote/',vote, name='vote'),
    

]