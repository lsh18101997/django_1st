from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Question, Choice
from datetime import datetime

current_day = datetime.today().day
current_year = datetime.today().year

def index(request):
    total_question_number = Question.objects.count()
    latest_question_list = Question.objects.order_by("-pub_date")[:10]
    before_today_question_list = Question.objects.filter(pub_date__day__lt=current_day)[:10]
    question_list = Question.objects.all()
    vote_morethanzero_question_list = [i.choice_set.filter(votes__gt=0) for i in question_list]
    context = {"total_question_number": total_question_number,
               "latest_question_list": latest_question_list, 
               "before_today_question_list": before_today_question_list,
               "vote_morethanzero_question_list": vote_morethanzero_question_list}
    return render(request, "polls/index.html", context)

def index1(request):
    question_list = Question.objects.filter(pub_date__day=current_day)
    context = {"question_list" : question_list}
    return render(request, "polls/index1.html", context)

def index2(request):
    response = "Hello, world!"
    return HttpResponse(response)

def index3(request):
    year_question_list = Question.objects.filter(pub_date__year=current_year)
    context = {"year_question_list" : year_question_list}
    return render(request, "polls/index3.html", context)

def detail(request, question_id):   # 매개변수 이름과 polls.urls.py의 path에 있는 <int:>안의 이름이 같아야 함.
    question = get_object_or_404(Question, pk=question_id)
    choice_list = question.choice_set.all()
    return render(request, "polls/detail.html", {"question": question, "choice_list": choice_list})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def question_id(request, question_id):
    return HttpResponse("This Question's question_id is %s" % question_id)
