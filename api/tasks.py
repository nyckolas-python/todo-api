import os

from django.core.mail import send_mail
from celery import shared_task
from celery.utils.log import get_task_logger
from time import sleep


logger = get_task_logger(__name__)

EMAIL_HOST_USER = os.getenv('DEFAULT_FROM_EMAIL')

@shared_task
def sample_task():
    logger.info("The sample task just ran.")

def send_mail_to(subject, message, receivers):
    send_mail(subject,message,EMAIL_HOST_USER,[receivers],
    fail_silently= False)
    
@shared_task
def send_email_task(subject, message, receivers):
    sleep(10)
    subject= 'Celery'
    message= 'My task done successfully'
    receivers= 'nyckolas.pyhton@gmail.com'
    is_task_completed= False
    error=''
    try:
        is_task_completed= True
    except Exception as err:
        error= str(err)
        logger.error(error)
    if is_task_completed:
        send_mail_to(subject,message,receivers)
    else:
        send_mail_to(subject,error,receivers)
    return('first_task_done')
