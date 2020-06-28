from django import forms

from .models import *
from django.forms import inlineformset_factory
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput


class ChoiceForm(forms.ModelForm):

    class Meta:
        model=Choice
        fields = ('choice_text',)
        # fields = '__all__'
        labels={
            'choice_text':('Texte du choix'),
        }


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        exclude = ['question_group','question_number','user_group']
        labels={
            'question_text':('Texte de la question'),
            'has_multiple_choices':('A choix multiples'),
        }

class QuestionGroupForm(forms.ModelForm):

    class Meta:
        model = QuestionGroup
        exclude = ('max_responders','user_group','creator')
        labels={
            'name':('Nom du sondage'),
            'created':('Date de publication'),
        }

class InvitationForm(forms.ModelForm):

    class Meta:
        model=Invitation
        fields = '__all__'

class ModUserCreationForm(UserCreationForm):

    class Meta:
        model=User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(ModUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'input'
        self.fields['username'].widget.attrs['placeholder'] = 'Martin DURAND ou JoliMome94'
        self.fields['username'].widget.attrs['required'] = 'True'
        self.fields['username'].widget.attrs['size'] = '20'

        self.fields['password1'].widget.attrs['class'] = 'input'
        self.fields['password2'].widget.attrs['class'] = 'input'

    

    

