from django.core.management.base import BaseCommand
from django.core.mail import get_connection
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.db.models import Q

from socket import error as socket_error
import smtplib

from mcfeely.models import Email
from mcfeely.models import Queue
from mcfeely.models import Unsubscribe
from mcfeely.models import Alternative
from mcfeely.models import Attachment
from mcfeely.models import Header
from mcfeely.models import ToRecipient, CcRecipient, BccRecipient

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

            messages = Email.objects.filter(queue=queue_type).filter(
                Q(torecipient__status='in_queue') |
                Q(ccrecipient__status='in_queue') |
                Q(bccrecipient__status='in_queue')).distinct()

            connection = get_connection(backend=EMAIL_BACKEND)

            for message in messages:
                for recipient in message.torecipient_set.all():
                    try:
                        Unsubscribe.objects.get(
                            Q(queue=queue_type) | Q(queue=None),
                            address=recipient.address)
                        print(recipient.address)


                    except Unsubscribe.DoesNotExist:
                        pass

                # recipients = [i for i in recip_list if i != '']

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
                    message.status = 'sent_success'
                    message.save()

                except (socket_error, smtplib.SMTPSenderRefused,
                        smtplib.SMTPRecipientsRefused,
                        smtplib.SMTPAuthenticationError) as err:
                    print(err)
                    message.status = 'deferred'
                    message.save()
