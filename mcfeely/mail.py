from django.core.mail import get_connection
from django.conf import settings
from mcfeely.engine import QueueEmailMessage
from mcfeely.engine import QueueEmailMultiAlternatives


def send_mail(subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              queue=None, connection=None):

    connection = connection or get_connection(username=auth_user,
                                              password=auth_password,
                                              fail_silently=fail_silently)

    return QueueEmailMessage(subject, message, from_email, recipient_list,
                             queue=queue, connection=connection).send()


# Todo: add send_mass_mail

def mail_admins(subject, message, queue=None, fail_silently=False,
                connection=None, html_message=None):
    if not settings.ADMINS:
        return
    mail = QueueEmailMultiAlternatives(
        '%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject),
        message,
        settings.SERVER_EMAIL,
        [a[1] for a in settings.ADMINS],
        queue=queue,
        connection=connection)
    if html_message:
        mail.attach_alternative(html_message, 'text/html')
    mail.send(fail_silently=fail_silently)


def mail_managers(subject, message, queue=None, fail_silently=False,
                  connection=None, html_message=None):
    if not settings.MANAGERS:
        return
    mail = QueueEmailMultiAlternatives(
        '%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject),
        message,
        settings.SERVER_EMAIL,
        [a[1] for a in settings.MANAGERS],
        queue=queue,
        connection=connection)
    if html_message:
        mail.attach_alternative(html_message, 'text/html')
    mail.send(fail_silently=fail_silently)
