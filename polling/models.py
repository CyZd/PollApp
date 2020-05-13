import datetime
from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=600)
    pub_date = models.DateTimeField('date published')

    def published_recently(self):
        now=timezone.now()
        return now - datetime.timedelta(days=1)<=self.pub_date <=now

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, name="Question",on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=600)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Tag(models.Model):
    question = models.ManyToManyField(Question,blank=True)
    tag_text = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_text
