import datetime

from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse

class QuestionModelTest(TestCase):
    def test_was_published_recently__with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.published_recently(), False)

    def test_was_published_recently__with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.published_recently(), False)

    def test_was_published_recently__with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.published_recently(), True)

def create_question(question_text,days):
    time=timezone.now()+datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionIndexTest(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse('polling:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_past_question(self):
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polling:index'))
        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polling:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_future_question_and_past_question(self):
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polling:index'))
        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question: Past question.>']
