from django.contrib import admin

from .models import Question, Choice, QuestionGroup, Tag, Invitation

class ChoiceInline(admin.TabularInline):
    model=Choice
    extra=2

class QuestionAdmin(admin.ModelAdmin):
    fieldsets=[
        (None,{'fields':['question_text']}),
        ('Groupe',{'fields':['user_group']}),
        ('Choix multiples ?',{'fields':['has_multiple_choices']}),
        ('Questionnaire',{'fields':['question_group']})
    ]
    inlines=[ChoiceInline]
    list_display = ('question_text','question_number')
    search_fields = ['question_text']

class QuestionGroupAdmin(admin.ModelAdmin):
    model=QuestionGroup

class TagAdmin(admin.ModelAdmin):
    model=Tag

class InvitationAdmin(admin.ModelAdmin):
    model=Invitation

admin.site.register(Question,QuestionAdmin)
admin.site.register(QuestionGroup,QuestionGroupAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Invitation,InvitationAdmin)
