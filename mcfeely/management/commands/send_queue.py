from django.core.management.base import BaseCommand
from django.core.mail import get_connection
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings

from socket import error as socket_error
import smtplib

from mcfeely.models import Email
from mcfeely.models import Queue
from mcfeely.models import Unsubscribe
from mcfeely.models import Alternative
from mcfeely.models import Attachment
from mcfeely.models import Header

EMAIL_BACKEND = getattr(
    settings,
    'MCFEELY_EMAIL_BACKEND',
    'django.core.mail.backends.smtp.EmailBackend'
)


class Command(BaseCommand):
    args = '<queue_name>'
    help = 'send all mail in the specified queue'

    def handle(self, *args, **options):
        if len(args) == 0:
            args = [x['queue'] for x in Queue.objects.all().values()]

        for queue_name in args:
            queue_type = Queue.objects.get(queue=queue_name)

            messages = Email.objects.filter(queue=queue_type, sent=False)
            connection = get_connection(backend=EMAIL_BACKEND)

            for message in messages:

                alternatives = Alternative.objects.filter(
                    email=message).values_list('content', 'mimetype')
                attachments = Attachment.objects.filter(email=message)

                headers = Header.objects.filter(
                    email=message).values('key', 'value')
                mail_headers = {}
                for header in headers:
                    mail_headers[header['key']] = header['value']

                if alternatives:
                    email = EmailMultiAlternatives(
                        message.subject,
                        message.body,
                        message.m_from,
                        message.m_to.split(', '),
                        message.m_bcc.split(', '),
                        connection,
                        None,
                        headers=mail_headers,
                        alternatives=alternatives
                    )
                else:
                    email = EmailMessage(
                        message.subject,
                        message.body,
                        message.m_from,
                        message.m_to.split(', '),
                        message.m_bcc.split(', '),
                        connection,
                        None,
                        headers=mail_headers,
                    )

                if attachments:
                    for attachment in attachments:
                        email.attach(
                            attachment.filename,
                            attachment.content,
                            attachment.mimetype
                        )

                try:
                    email.send()
                    message.sent = True
                    message.save()

                except (socket_error, smtplib.SMTPSenderRefused,
                        smtplib.SMTPRecipientsRefused,
                        smtplib.SMTPAuthenticationError) as err:
                    print(err)
                    message.deferred = True
                    message.save()
