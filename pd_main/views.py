import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView
)
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from .models import (
    Feedback,
    Question,
    Questioner,
    Answer,
    QuestionAnswer
)
from .forms import (
    FeedbackForm,
    QuestionForm,
    AnswerForm,
    AnswerOutputForm
)
from .utils import send_answer

logger = logging.getLogger(__name__)


class HomeView(SuccessMessageMixin, CreateView):

    model = Question
    form_class = QuestionForm
    template_name = 'pd_main/home.html'
    success_message = 'Your question has been sent.'
    success_url = '/'

    def form_valid(self, form):
        user_mail = form.cleaned_data['questioner']

        # create a questioner instance if not exists
        try:
            Questioner.objects.get(email=user_mail)
        except Questioner.DoesNotExist:
            logger.info(f'Questioner object does not exist. Creating for {user_mail}')
            Questioner.objects.create(email=user_mail)

        return super().form_valid(form)


class FeedbackView(SuccessMessageMixin, CreateView):

    model = Feedback
    form_class = FeedbackForm
    template_name = 'pd_main/feedback.html'
    success_message = 'Thank you for your feedback.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Feedback'

        return context


def about(request):
    return render(request, 'pd_main/about.html', {'title': 'About'})


class QuestionView(UserPassesTestMixin, DetailView):

    model = Question
    template_name = 'pd_main/question.html'
    login_url = '/admin/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = Question.objects.get(question_id=self.kwargs['pk'])
        qa = QuestionAnswer.objects.get(question=question)
        context['answer'] = qa.answer

        context['title'] = 'Question'

        return context

    def test_func(self):
        return self.request.user.is_superuser


class UserQuestionListView(UserPassesTestMixin, ListView):

    template_name = 'pd_main/user_questions.html'
    context_object_name = 'questions'
    login_url = '/admin/'

    def get_queryset(self):
        user = get_object_or_404(Questioner, email=self.kwargs.get('user_mail'))
        return Question.objects.filter(questioner=user).order_by('-date_submitted')

    def test_func(self):
        return self.request.user.is_superuser


class AnswerCreateView(UserPassesTestMixin, SuccessMessageMixin, UpdateView):

    model = Answer
    form_class = AnswerForm
    success_message = 'Answer created successfully.'
    template_name_suffix = '_prepare'
    success_url = '/admin/pd_main/answer/'
    login_url = '/admin/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = Question.objects.get(question_id=self.kwargs['question_id'])

        context['title'] = 'Answer Preparation'

        return context

    def test_func(self):
        return self.request.user.is_superuser


class AnswerShowView(UserPassesTestMixin, SuccessMessageMixin, ListView):

    model = Answer
    template_name = 'pd_main/answer.html'
    success_message = 'Answer sent successfully.'
    login_url = '/admin/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = Question.objects.get(question_id=self.kwargs['question_id'])
        context['answer'] = Answer.objects.get(pk=self.kwargs['pk'])

        context['title'] = 'Answer Show'

        return context

    def test_func(self):
        return self.request.user.is_superuser


class AnswerOutputView(UserPassesTestMixin, SuccessMessageMixin, FormView):

    template_name = 'pd_main/answer_output.html'
    form_class = AnswerOutputForm
    success_url = '/admin/pd_main/question/'
    success_message = 'Answer image saved and sent successfully.'
    login_url = '/admin/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = Question.objects.get(question_id=self.kwargs['question_id'])
        context['answer'] = Answer.objects.get(pk=self.kwargs['pk'])

        context['title'] = 'Answer Output Send'

        return context

    def form_valid(self, form, *args, **kwargs):
        question = Question.objects.get(question_id=self.kwargs['question_id'])
        qa = QuestionAnswer.objects.get(question=question)
        output_filename = qa.answer.get_answer_filename()

        logger.info(f'Saving screenshot of answer as {output_filename}')
        form.save_screenshot(output_filename)

        logger.info(f'Sending answer to user {qa.question.questioner}')
        send_answer(qa.answer, qa.question.questioner, output_filename)

        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser


