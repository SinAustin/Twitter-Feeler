from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Questions



class QuestionModelTests(TestCase):
    """ fixing was_published_recently function returning True on questions from the future,
    should return false 
    
    """
    def test_was_pubished_recently_with_future_question(self):

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Questions(pub_date = time)
        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Questions(pub_date=time)    
        self.assertIs(old_question.was_published_recently(),False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Questions(pub_date=time)    
        self.assertIs(recent_question.was_published_recently(),True)    