from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone
from .forms import *
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import transaction

class questionList(generic.ListView):
    template_name='polling/index.html'
    context_object_name='question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
    
class questionDetail(generic.DetailView):
    model=Question
    template_name='polling/questionDetail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request,"polling/questionDetail.html",{
            "question":question,
            "error_message":"Vous n'avez pas donné de réponse",
        })
    else:
        selected_choice.votes = F('votes')+1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polling:questionDetail', args=(question.id,)))

class questionNew(CreateView):
    model=Question
    template_name='polling/questionEdit.html'
    form_class=QuestionForm
    object=None

    def get(self,request,*args,**kwargs):
        self.object=None
        form_class=self.get_form_class()
        form=self.get_form(form_class)
        choice_form=ChoiceFormset()
        return self.render_to_response(
            self.get_context_data(form=form,choice_form=choice_form,)
        )

    def post(self, request, *args, **kwargs):
        self.object=None
        form_class=self.get_form_class()
        form=self.get_form(form_class)
        choice_form=ChoiceFormset(self.request.POST,instance=form.instance)

        if form.is_valid() and choice_form.is_valid():
            return self.form_valid(form,choice_form)
        else:
            return self.form_invalid(form,choice_form)
    
    def form_valid(self,form,form_question):
        self.object = form.save(commit=False)
        self.object.save()

        choice_form=choice_form.save(commit=False)
        choice.save()
        # for choice in choice_form:
        #     choice.question=form.question_text
        #     choice.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form,choice_form):
        return self.render_to_response(self.get_context_data(form=form,choice_form=choice_form))

