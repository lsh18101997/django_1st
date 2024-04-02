from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("zerovote/", views.IndexView2.as_view(), name="index2"),
    path("mostvote/", views.IndexView3.as_view(), name="index3"),
    # ex: /polls/5/
    path("<int:question_id>/", views.DetailView.as_view(), name="detail"),
    path('question/new/', views.QuestionCreateView.as_view(), name='question_new'),
    path('question/<int:pk>/choice/new/', views.ChoiceCreateView.as_view(), name='choice_new'),
    path('question/<int:pk>/update/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('choice/<int:pk>/update/', views.ChoiceUpdateView.as_view(), name='choice_update'),
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    # ex: /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/question/", views.question_id, name="question_id")
]