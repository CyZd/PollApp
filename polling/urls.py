from django.urls import path, include

from . import views

app_name='polling'
urlpatterns = [
    path('', views.portal, name='portal'),
    #section handling groups of question
    path('polls/<str:user_group>', views.userGroups, name='userGroups'),
    path('polls/<str:user_group>/new', views.userGroupsNew, name='userGroupsNew'),
    path('polls/<str:user_group>/<str:group_name>/edit', views.userGroupsEdit, name='userGroupsEdit'),
    path('polls/<str:user_group>/<str:group_name>/delete', views.userGroupsDelete, name='userGroupsDelete'),
    path('polls/<str:user_group>/<str:group_name>', views.userGroupsDetail, name='userGroupsDetail'),
    path('polls/<str:user_group>/<str:group_name>/thankyou', views.userGroupsThankyou, name='userGroupsThankyou'),
    #section for inserting questions in groups
    #path('<int:user>/<int:pk>/list', views.questionList, name='questionList'),
    path('polls/<str:user_group>/<str:group_name>/<int:question>', views.questionDetail, name='questionDetail'),
    path('polls/<str:user_group>/<str:group_name>/<int:question_id>/vote', views.vote, name='vote'),
    path('polls/<str:user_group>/<str:group_name>/<int:question_id>/edit', views.questionEdit, name='questionEdit'),
    path('polls/<str:user_group>/<str:group_name>/<int:question_id>/delete', views.questionDelete, name='questionDelete'),
    path('polls/<str:user_group>/<str:group_name>/new', views.userGroupsNewQuestion, name='userGroupsNewQuestion'),
    path('polls/<str:user_group>/<str:group_name>/invite', views.userGroupsInvite, name='userGroupsInvite'),
    path('participate/<slug:slug>/', views.userGroupsParticipate, name='userGroupsParticipate'),
    #path('new/', views.questionNew, name='questionNew'),
    #path('<int:question_id>/edit/', views.questionEdit, name='questionEdit'),
    path('search/',views.questionSearch,name='search'),
    #user authentification
    path('signup/',views.signup,name='signup'),
    path('accounts/',include('django.contrib.auth.urls')),
]

