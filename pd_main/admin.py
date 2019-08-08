from django.contrib import admin
from .models import (
    Feedback,
    Question,
    Questioner,
    QuestionAdmin,
    FeedbackAdmin,
    Answer,
    AnswerAdmin,
    QuestionAnswer,
    Category,
    Post,
    PostAdmin
)

admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Questioner)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuestionAnswer)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)

