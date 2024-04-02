from django.db.models import F
from django.db.models.functions import Greatest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.db.models import Max, Sum
from django.urls import reverse, reverse_lazy
from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]
    
class IndexView2(generic.ListView):
    template_name = "polls/index2.html"
    context_object_name = "zerovote_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        mostvote_dict = {}
        question_votes = Question.objects.annotate(total_votes=Sum('choice__votes'))

        for question in question_votes:
            if type(question.total_votes) != int:
                mostvote_dict[question.question_text] = question.total_votes

        return mostvote_dict
    
class IndexView3(generic.ListView):
    template_name = "polls/index3.html"
    context_object_name = "mostvote_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        mostvote_dict = {}
        question_votes = Question.objects.annotate(total_votes=Max('choice__votes'))

        for question in question_votes:
            if type(question.total_votes) == int:
                mostvote_dict[question.question_text] = question.total_votes

        return dict(sorted(mostvote_dict.items(), key=lambda x:x[1], reverse=True))


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_object(self):
        question_id = self.kwargs['question_id']
        question = get_object_or_404(Question, pk=question_id)
        return question
    
class QuestionCreateView(CreateView):
    model = Question
    fields = ['question_text', 'pub_date']
    template_name = 'polls/question_form.html'
    success_url = reverse_lazy('polls:index')

class ChoiceCreateView(CreateView):
    model = Choice
    fields = ['choice_text']
    template_name = 'polls/choice_form.html'

    def form_valid(self, form):
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('polls:detail', kwargs={'question_id': self.kwargs['pk']})

class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['question_text', 'pub_date']
    template_name = 'polls/question_update.html'  # 재사용하거나 적절한 템플릿 지정
    success_url = reverse_lazy('polls:index')  # 예시 URL, 실제 프로젝트에 맞게 수정 필요

class ChoiceUpdateView(UpdateView):
    model = Choice
    fields = ['choice_text']
    template_name = 'polls/choice_update_form.html'  # 새로운 템플릿 또는 기존 템플릿 지정

    def get_success_url(self):
        # 선택지가 업데이트된 후, 선택지가 속한 질문의 상세 페이지로 리다이렉션
        choice = self.object
        return reverse('polls:detail', kwargs={'question_id': choice.question.pk})
    
class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'polls/question_confirm_delete.html'
    success_url = reverse_lazy('polls:index') 



class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


# def index(request):
#     total_question_number = Question.objects.count()
#     question_list = Question.objects.all()
#     context = {"total_question_number": total_question_number,
#                "question_list": question_list}
#     return render(request, "polls/index.html", context)

# def detail(request, question_id):   # 매개변수 이름과 polls.urls.py의 path에 있는 <int:>안의 이름이 같아야 함.
#     question = get_object_or_404(Question, pk=question_id)
#     choice_list = question.choice_set.all()
#     return render(request, "polls/detail.html", {"question": question, "choice_list": choice_list})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

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
