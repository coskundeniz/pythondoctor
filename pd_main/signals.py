from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Question, Answer, QuestionAnswer
from .utils import notify_new_question


@receiver(post_save, sender=Question)
def new_question_handler(sender, instance, created, **kwargs):

    subject = f'New question from {instance.questioner}'
    message = f'A question with id {instance.question_id} is just sent by {instance.questioner}'

    if created:
        notify_new_question(subject, message)

        # create answer instance
        related_answer = Answer()
        related_answer.save()

        # create questionanswer instance
        QuestionAnswer.objects.create(answer=related_answer, question=instance)


@receiver(post_save, sender=Answer)
def update_question(sender, instance, created, **kwargs):

    if not created:
        qa = QuestionAnswer.objects.get(answer=instance)
        qa.question.answered = True
        qa.question.save()
