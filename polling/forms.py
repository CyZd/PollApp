from django import forms

from .models import Question, Choice
from django.forms import BaseInlineFormSet
from django.forms import inlineformset_factory

class ChoiceForm(forms.ModelForm):

    class Meta:
        model=Choice
        fields = ('choice_text',)
        # fields = '__all__'


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = '__all__'

ChoiceFormset=inlineformset_factory(Question,Choice,form=QuestionForm,fields='__all__',extra=2)