from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone
from .forms import *
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.contrib.auth.models import Group
from django.http import Http404
from django.utils.crypto import get_random_string

from django.core.mail import EmailMultiAlternatives


def portal(request):
    return render(request,'polling/portal.html')

def signup(request):
    if request.method=="POST":
        form=ModUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
            username=form.cleaned_data.get('username')
            raw_password=form.cleaned_data.get('password1')
            user=authenticate(username=username, password=raw_password)
            new_group=Group()
            new_group.name=username
            new_group.save()
            new_group.user_set.add(user)
            if user is not None:
                login(request,user)
                groupList=QuestionGroup.objects.filter(user_group__name__exact=new_group)
                return render(request, 'polling/userGroups.html', {'groupList':groupList })

            else:
                return render(request,"polling/signup.html",{
                    "error_message":"Vos identifiants sont incorrects",
                })
    else:
        form=ModUserCreationForm()
    return render(request,'polling/signup.html',{'form':form})


def userGroups(request,user_group):
    if not request.user.is_authenticated:
        raise Http404("Poll does not exist")
        return render(request,'polling/portal.html')
    else:
        try:
            current_group=Group.objects.get(name=user_group)
        except(KeyError, Group.DoesNotExist):
            raise Http404("This user group does not exist")
            return render(request,'polling/portal.html')
    
    groupList=QuestionGroup.objects.filter(user_group__name__exact=user_group)

    return render(request, 'polling/userGroups.html', {'groupList':groupList })


def userGroupsDetail(request,user_group,group_name):
    invite_code=request.session.get('invite_access_code')

    if not request.user.is_authenticated and not invite_code:
        raise Http404("Poll does not exist")
        return render(request,'polling/portal.html')
    else:
        try:
            current_group=Group.objects.get(name=user_group)
        except(KeyError, Group.DoesNotExist):
            raise Http404("This user group does not exist")
            return render(request,'polling/portal.html')

    try:
        group=QuestionGroup.objects.filter(user_group__name__exact=user_group).get(name=group_name)
    except(QuestionGroup.DoesNotExist):
        raise Http404("This question group does not exist")
        return render(request,'polling/portal.html')
    
    user=Group.objects.get(name__exact=user_group)

    if invite_code or group.creator==request.user:
        return render(request, 'polling/userGroupsDetail.html', {'user_group':user,'group':group })
        #return HttpResponseRedirect(reverse('polling:userGroupsDetail', args=(instance.user_group,instance.name,)))
    else:
        raise Http404("Poll does not exist")
        return render(request,'polling/portal.html')
    #if user is creator,list all questions and link.
    #f user is invited, show everything but give only first link

def userGroupsThankyou(request,user_group,group_name):
    invite_code=request.session.get('invite_access_code')
    group=QuestionGroup.objects.filter(user_group__name__exact=user_group).get(name=group_name)
    user=Group.objects.get(name__exact=user_group)

    if invite_code:
        return render(request, 'polling/userGroupsThankyou.html', {'user_group':user,'group':group })
    else:
        return render(request,'polling/portal.html')


def userGroupsNew(request,user_group):

    GroupAmount=QuestionGroup.objects.filter(creator=request.user).count()
    groupList=QuestionGroup.objects.filter(user_group__name__exact=user_group).count()



    if GroupAmount>=3:
        groupList=QuestionGroup.objects.filter(creator=request.user)
        errorMessage='Vous avez atteint le nombre maximum de sondages autorisés.'
        return render(request, 'polling/userGroups.html', {'groupList':groupList,'errorMessage':errorMessage })

    else:
        pass

    CurrentUser=User.objects.get(pk=request.user.id)

    if request.method=="POST":
        GroupForm=QuestionGroupForm(request.POST)
        if GroupForm.is_valid():
            instance=GroupForm.save(commit=False)
            instance.creator=CurrentUser
            currentUserGroup=QuestionGroup.objects.filter(user_group__name__exact=user_group).first()
            instance.user_group=CurrentUser.groups.first()
            instance.save()
        return HttpResponseRedirect(reverse('polling:userGroupsNewQuestion', args=(instance.user_group,instance.name,)))
    else:
        GroupForm=QuestionGroupForm()

    return render(request, 'polling/userGroupsNew.html', {'GroupForm':GroupForm})

def userGroupsEdit(request,user_group,group_name):
    group=QuestionGroup.objects.filter(user_group__name__exact=user_group).get(name=group_name)

    if request.method=="POST":
        GroupForm=QuestionGroupForm(request.POST,instance=group)
        if GroupForm.is_valid():
            instance=GroupForm.save()
            return HttpResponseRedirect(reverse('polling:userGroups', args=(instance.user_group,)))
    else:
        GroupForm=QuestionGroupForm(instance=group)
    return render(request, 'polling/userGroupsEdit.html', {'GroupForm':GroupForm})

def userGroupsDelete(request,user_group,group_name):
    group=QuestionGroup.objects.filter(user_group__name__exact=user_group).get(name=group_name)
    group.delete()
    groupList=QuestionGroup.objects.filter(user_group__name__exact=user_group)
    return render(request, 'polling/userGroups.html', {'groupList':groupList })


def userGroupsNewQuestion(request,user_group,group_name):
    group=QuestionGroup.objects.filter(user_group__name__exact=user_group).get(name=group_name)
    question=QuestionForm()
    ChoiceFormset=inlineformset_factory(Question, Choice,fields=('choice_text',),extra=4,can_delete=True)

    if request.method=="POST":
        question=QuestionForm(request.POST)
        if question.is_valid():
            instance=question.save(commit=False)
            instance.question_group=group
            questionsCount=Question.objects.filter(question_group=group).count()
            instance.question_number=questionsCount
            instance.user_group=group.user_group
            instance.save()

        formset=ChoiceFormset(request.POST,instance=instance)
        if formset.is_valid():
            formset.save()

        return HttpResponseRedirect(reverse('polling:userGroupsDetail', args=(group.user_group,group.name,)))
    else:
        formset=ChoiceFormset()
        question=QuestionForm()

    return render(request, 'polling/userGroupsNewQuestion.html', {'question':question,'formset': formset,'group':group})

def questionList(request,user,pk):
    group=QuestionGroup.objects.filter(creator=user).get(pk=pk)
    questions=Questions.objects.filter(question_group=group)

    return render(request, 'polling/questionList.html', {'questions':questions })
    
def questionDetail(request,user_group,group_name,question):
    group=QuestionGroup.objects.filter(user_group__name__exact=user_group).get(name=group_name)
    question=Question.objects.filter(question_group=group).get(id=question)

    return render(request, 'polling/questionDetail.html', {'group':group,'question':question })


def vote(request,user_group,group_name,question_id):
    group=QuestionGroup.objects.filter(user_group__name__exact=user_group).get(name=group_name)
    queryset=Question.objects.filter(question_group=group)
    question = get_object_or_404(queryset, pk=question_id)

    numberSequence=int(question.question_number)+1


    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        error_message="Vous n'avez pas donné de réponse"
        return render(request, 'polling/questionDetail.html', {'group':group,'question':question,'error_message':error_message })
    else:
        selected_choice.votes = F('votes')+1
        selected_choice.save()

        nextQuestion=0

        try:
            nextQuestion=Question.objects.filter(question_group=group).get(question_number=numberSequence)
        except(Question.DoesNotExist):
            pass

        questionsCount=Question.objects.filter(question_group=group).count()


        if nextQuestion!=0 and questionsCount>1 and nextQuestion.question_number<=questionsCount:
            return HttpResponseRedirect(reverse('polling:questionDetail', args=(group.user_group,group.name,nextQuestion.id,)))
        else:
            return HttpResponseRedirect(reverse('polling:userGroupsThankyou', args=(group.user_group,group.name,)))


def questionEdit(request,user_group,group_name,question_id):
    group=QuestionGroup.objects.filter(user_group__name__exact=user_group).get(name=group_name)
    question=Question.objects.filter(question_group=group).get(id=question_id)
    
    ChoiceFormset=inlineformset_factory(Question, Choice,fields=('choice_text',),extra=2,can_delete=True)

    if request.method=="POST":
        question_form=QuestionForm(request.POST,instance=question)
        if question_form.is_valid():
            instance=question.save()
            # astonishingly, it works
        formset=ChoiceFormset(request.POST,instance=question)
        if formset.is_valid():
            instances=formset.save(commit=False)
            for instance in instances:
                instance.question=question
                instance.save()
        return HttpResponseRedirect(reverse('polling:questionDetail', args=(group.user_group,group.name,question.id,)))
    else:
        question_form=QuestionForm(instance=question)
        formset=ChoiceFormset(instance=question)
    return render(request, 'polling/questionEdit.html', {'question':question_form,'formset': formset,'group':group})

def questionDelete(request,user_group,group_name,question_id):
    group=QuestionGroup.objects.filter(user_group__name__exact=user_group).get(name=group_name)
    question=Question.objects.filter(question_group=group).get(id=question_id)
    question.delete()

    return render(request, 'polling/userGroupsDetail.html', {'group':group })

def userGroupsInvite(request,user_group,group_name):
    

    question_group=QuestionGroup.objects.filter(user_group__name__exact=user_group).get(name=group_name)

    inviteInstance=Invitation()
    inviteInstance.user_group=Group.objects.get(name__exact=user_group)
    inviteInstance.QuestionGroup=question_group
    inviteInstance.code=get_random_string(8)

    inviteInstance.save()

    invite_link=request.build_absolute_uri(reverse('polling:userGroupsParticipate', args=(inviteInstance.code,)))

    return render(request, 'polling/userGroupsDetail.html', {'group':question_group,'invite_link':invite_link })



def userGroupsParticipate(request,slug):
    try:
        code=Invitation.objects.get(code__exact=slug)
        print(code)
        request.session['invite_access_code']=code.code
    except(KeyError, Invitation.DoesNotExist):
        raise Http404("Can't find code")
        return render(request,'polling/portal.html')
    
    try:
        user_group=Group.objects.get(name=code.user_group)
        question_group=QuestionGroup.objects.filter(user_group=user_group).get(name=code.QuestionGroup)
    except(KeyError, Invitation.DoesNotExist):
        pass
    #return HttpResponse("{},usergroup:{},question_group:{}".format(vars(code),vars(user_group),vars(question_group)))
    return HttpResponseRedirect(reverse('polling:userGroupsDetail', args=(user_group.name,question_group.name,)))



def questionSearch(request):
    url_catch=request.GET.get("q")

    if url_catch:
        groups=QuestionGroup.objects.filter(name__icontains=url_catch)
        questions=Question.objects.filter(question_text__icontains=url_catch)
        for question in questions:
            reverseGroup=QuestionGroup.objects.get(name__exact=question.question_group)
            question.reverseGroup=reverseGroup.name
    else:
        questions=None
        groups=None
    context={
        "questions":questions,
        "groups":groups,
        "user":request.user,
    }

    if request.is_ajax():
        html=render_to_string(
            template_name="polling/search.html",
            context=context
        )
        data_dict={"html_from_view":html}

        return JsonResponse(data=data_dict,safe=False)

    return render(request,"polling/search.html",context=context)

def error_404(request,exception):
    context={}
    return render(request,"polling/404.html",context=context)