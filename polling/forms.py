from django import forms

from .models import *
from django.forms import inlineformset_factory
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput,Textarea


class ChoiceForm(forms.ModelForm):

    class Meta:
        model=Choice
        fields = ('choice_text',)
        # fields = '__all__'
        widgets={'choice_text': Textarea(attrs={'cols': 80, 'rows': 20})}



class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        #exclude = ['question_group','question_number','user_group']
        fields = ('question_text', 'has_multiple_choices')
        labels={
            'question_text':('Texte de la question'),
            'has_multiple_choices':('Cochez ici pour une question à choix multiples'),
        }

    
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        self.fields['question_text'].widget.attrs['class'] = 'input'
        self.fields['question_text'].widget.attrs['placeholder'] = 'On décide quoi ?'
        self.fields['question_text'].widget.attrs['required'] = 'True'
        self.fields['question_text'].widget.attrs['size'] = '20'

        self.fields['has_multiple_choices'].widget.attrs['class'] = 'checkbox'




class QuestionGroupForm(forms.ModelForm):

    class Meta:
        model = QuestionGroup
        exclude = ('max_responders','user_group','creator','created')
        labels={
            'name':('Nom du sondage'),

        }

        def __init__(self, *args, **kwargs):
            super(QuestionGroupForm, self).__init__(*args, **kwargs)

            self.fields['name'].widget.attrs['class'] = 'input'
            self.fields['name'].widget.attrs['placeholder'] = 'Titre de votre sondage'
            self.fields['name'].widget.attrs['required'] = 'True'
            self.fields['name'].widget.attrs['size'] = '20'


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

    

    

