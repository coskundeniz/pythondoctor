import os
import logging
from django.core.mail import BadHeaderError, send_mail
from django.core.mail import EmailMessage
from smtplib import SMTPException
from django.conf import settings
from .models import QuestionAnswer

logger = logging.getLogger(__name__)

def notify_new_question(subject, message):

    from_email = settings.EMAIL_HOST_USER
    to_email = from_email

    try:
        send_mail(subject, message, from_email, [to_email])
        logger.info(message)
    except (BadHeaderError, SMTPException) as err:
        logger.error('An error occurred during mail notification!')
        logger.error(err)


def send_answer(answer, questioner, output_file):

    full_path = os.path.join(settings.BASE_DIR, 'answers', output_file)
    if os.path.exists(full_path):
        subject = 'Your answer is ready'
        message = 'You can see your answer in the attachment.\n\n\nHappy coding...\nDoctor Python'
        from_email = settings.EMAIL_HOST_USER
        to_email = questioner

        try:
            email = EmailMessage(subject, message, from_email, [to_email])
            email.bcc = [from_email]
            email.attach_file(full_path, 'image/png')
            email.send()
        except (BadHeaderError, SMTPException) as err:
            logger.error(f'An error occurred while sending answer to {to_email}!')
            logger.error(err)
        else:
            # update answer sent field
            qa = QuestionAnswer.objects.get(answer=answer)
            qa.answer.sent = True
            qa.answer.save()
    else:
        logger.error('Answer output does not exist in server!')

