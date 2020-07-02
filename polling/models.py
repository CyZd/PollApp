import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group


class QuestionGroup(models.Model):
    name=models.CharField(max_length=600)
    creator=models.ForeignKey(User, on_delete=models.CASCADE)
    max_responders=models.IntegerField(blank=True,default=0)
    created=models.DateTimeField('date published')
    user_group=models.ForeignKey(Group, on_delete=models.CASCADE,blank=True,default=0)

    def __str__(self):
        return self.name

    def published_recently(self):
        now=timezone.now()
        return now - datetime.timedelta(days=2)<=self.pub_date <=now
    
    


class Question(models.Model):
    question_text = models.CharField(max_length=600)
    has_multiple_choices=models.BooleanField(default=False)
    question_group=models.ForeignKey(QuestionGroup, on_delete=models.CASCADE,null=True)
    question_number=models.IntegerField(blank=True,default=0)
    user_group=models.ForeignKey(Group, on_delete=models.CASCADE,blank=True,default=0)

    # def published_recently(self):
    #     now=timezone.now()
    #     return now - datetime.timedelta(days=2)<=self.pub_date <=now
    

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, name="Question",on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=600)
    votes = models.IntegerField(default=0)

    class Meta:
        verbose_name = "choice"
        verbose_name_plural = "choices"

    def __str__(self):
        return self.choice_text

class Tag(models.Model):
    question_group = models.ManyToManyField(QuestionGroup, name="QuestionGroup",blank=True)
    tag_text = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_text



class Invitation(models.Model):
    question_group = models.ForeignKey(QuestionGroup, name="QuestionGroup",on_delete=models.CASCADE)
    user_group=models.ForeignKey(Group, on_delete=models.CASCADE,blank=True,null=True)
    code=models.SlugField(blank=True)
    
    
    # def __str__(self):
    #     return ('sent to {}-for group {}', self.email,self.question_group)


