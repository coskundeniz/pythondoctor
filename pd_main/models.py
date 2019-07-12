import uuid
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import admin


class Feedback(models.Model):

    message = models.TextField()
    email = models.EmailField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback from {self.email}'

    def get_absolute_url(self):
        return reverse_lazy('pd-home')

    class Meta:
        ordering = ['-date_submitted']


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_submitted')
    list_filter = ('email', 'date_submitted')


class Questioner(models.Model):

    email = models.EmailField(primary_key=True)

    def __str__(self):
        return f'{self.email}'

    def get_absolute_url(self):
        return reverse_lazy('pd-user-questions', kwargs={"user_mail": self.email})

    def get_username(self):
        return self.email.split('@')[0]


class Question(models.Model):

    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.TextField()
    question_text = models.TextField()
    questioner = models.EmailField()
    answered = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'questioner={self.questioner}, id={self.question_id}'

    def get_absolute_url(self):
        return reverse_lazy('pd-question-show', kwargs={'pk': self.question_id})

    def code_line_count(self):
        return len(self.code.split('\n'))

    def question_line_count(self):
        return len(self.question_text.split('\n'))

    class Meta:
        ordering = ['-date_submitted', 'questioner']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('questioner', 'question_id', 'date_submitted', 'answered')
    list_filter = ('questioner', 'date_submitted', 'answered')


class Answer(models.Model):

    code = models.TextField(default='')
    explanation = models.TextField(default='')
    date_prepared = models.DateTimeField(default=timezone.now)
    sent = models.BooleanField(default=False)

    def __str__(self):
        qa = QuestionAnswer.objects.get(answer=self)

        return f'id: {self.pk}, question={qa.question.question_id}'

    def get_absolute_url(self):
        qa = QuestionAnswer.objects.get(answer=self)

        return reverse_lazy('pd-answer-show', kwargs={
            'question_id': qa.question.question_id,
            'pk': self.pk
        })

    def get_answer_filename(self):
        qa = QuestionAnswer.objects.get(answer=self)
        questioner = Questioner.objects.get(email=qa.question.questioner)
        username = questioner.get_username()
        uid_part = str(qa.question.question_id).split('-')[-1]
        filename = f'{username}_{uid_part}.png'

        return filename

    def code_line_count(self):
        return len(self.code.split('\n'))

    def explanation_line_count(self):
        return len(self.explanation.split('\n'))

    class Meta:
        ordering = ['-date_prepared']


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_prepared', 'sent')
    list_filter = ('date_prepared', 'sent')


class QuestionAnswer(models.Model):

    answer = models.ForeignKey(Answer, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'answer: {self.answer.pk}, question={self.question.question_id}'