from django.urls import path
from . import views
from .views import (
    HomeView,
    FeedbackView,
    QuestionView,
    UserQuestionListView,
    AnswerCreateView,
    AnswerShowView,
    AnswerOutputView,
    BitsOfPythonInformationView,
    BitsOfPythonInformationFilterView,
    PostDetailView
)


urlpatterns = [
    path('', HomeView.as_view(), name='pd-home'),

    path('about/', views.about, name='pd-about'),
    path('bopi/', BitsOfPythonInformationView.as_view(), name='pd-bopi'),
    path('bopi/filter/<str:category>/', BitsOfPythonInformationFilterView.as_view(), name='pd-bopi-filter'),
    path('bopi/<int:pk>/', PostDetailView.as_view(), name='pd-post-detail'),
    path('feedback/', FeedbackView.as_view(), name='pd-feedback'),

    path('question/<str:pk>/', QuestionView.as_view(), name='pd-question-show'),
    path('user/<str:user_mail>/', UserQuestionListView.as_view(), name='pd-user-questions'),

    path('answer/prepare/<str:pk>/<str:question_id>/', AnswerCreateView.as_view(), name='pd-answer-prepare'),
    path('answer/show/<str:pk>/<str:question_id>/', AnswerShowView.as_view(), name='pd-answer-show'),
    path('answer/send/<str:pk>/<str:question_id>/', AnswerOutputView.as_view(), name='pd-answer-send')
]
