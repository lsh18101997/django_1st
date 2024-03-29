from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index1/",views.index1, name="index1"),
    path("index2/", views.index2, name="index2"),
    path("index3/", views.index3, name="index3"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/question/", views.question_id, name="question_id")
]