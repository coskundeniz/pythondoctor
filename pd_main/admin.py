from django.contrib import admin
from .models import (
    Feedback,
    Question,
    Questioner,
    QuestionAdmin,
    FeedbackAdmin,
    Answer,
    AnswerAdmin,
    QuestionAnswer
)

admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Questioner)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuestionAnswer)

