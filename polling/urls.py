from django.urls import path

from . import views

app_name='polling'
urlpatterns = [
    path('', views.questionList.as_view(), name='questionList'),
    path('<int:pk>/', views.questionDetail.as_view(), name='questionDetail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('new/', views.questionNew.as_view(), name='questionNew'),
    # path('edit/', views.questionEdit, name='edit'),
]