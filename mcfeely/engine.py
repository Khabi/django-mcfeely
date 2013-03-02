from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from mcfeely.models import Queue

def default_queue(queue):
    if queue is None:
        default_queue = getattr(
            settings, 'DEFAULT_EMAIL_QUEUE', 'Default'
        )
        return(Queue.objects.get(queue=default_queue))
    else:
        return queue


class QueueEmailMessage(EmailMessage):
    """ Override EmailMessage to allow the addition of queues """
    def __init__(self, subject='', body='', from_email=None, to=None,
                 bcc=None, connection=None, attachments=None, headers=None,
                 cc=None, queue=None):

        super(QueueEmailMessage, self).__init__(
            subject,
            body,
            from_email,
            to,
            bcc,
            connection,
            attachments,
            headers,
            cc)
        self.queue = default_queue(queue)


class QueueEmailMultiAlternatives(EmailMultiAlternatives):
    """ Override EmailMultiAlternatives to allow the addition of
    queues """
    def __init__(self, subject='', body='', from_email=None, to=None, bcc=None,
                 connection=None, attachments=None, headers=None,
                 alternatives=None, cc=None, queue=None):
        super(QueueEmailMultiAlternatives, self).__init__(
            subject,
            body,
            from_email,
            to,
            bcc,
            connection,
            attachments,
            headers,
            cc)
        self.queue = default_queue(queue)
