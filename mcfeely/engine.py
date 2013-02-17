from django.core.mail import EmailMessage, EmailMultiAlternatives


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
        self.queue = queue


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
        self.queue = queue
