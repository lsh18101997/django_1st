from django.db.models import F
from django.db.models.functions import Greatest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Question, Choice


def index(request):
    total_question_number = Question.objects.count()
    question_list = Question.objects.all()
    context = {"total_question_number": total_question_number,
               "question_list": question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):   # 매개변수 이름과 polls.urls.py의 path에 있는 <int:>안의 이름이 같아야 함.
    question = get_object_or_404(Question, pk=question_id)
    choice_list = question.choice_set.all()
    return render(request, "polls/detail.html", {"question": question, "choice_list": choice_list})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # selected_choice.votes = Greatest(F("votes") - 1, 0)
        # selected_choice.votes = F("votes") * 2
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def question_id(request, question_id):
    return HttpResponse("This Question's question_id is %s" % question_id)
