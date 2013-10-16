from django.core.management.base import BaseCommand
from django.core.mail import get_connection
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.db.models import Q

from socket import error as socket_error
import smtplib
from optparse import make_option

from mcfeely.models import Email
from mcfeely.models import Queue
from mcfeely.models import Unsubscribe
from mcfeely.models import Alternative
from mcfeely.models import Attachment
from mcfeely.models import Header
from mcfeely.models import Recipient

EMAIL_BACKEND = getattr(
    settings,
    'MCFEELY_EMAIL_BACKEND',
    'django.core.mail.backends.smtp.EmailBackend'
)

class Command(BaseCommand):
    args = '<queue_name>'
    option_list = BaseCommand.option_list + (
        make_option('--retry',
            action='store_true',
            dest='retry',
            default=False,
            help='retry Deferred email'),
        )
    help = 'send all mail in the specified queue'

    def __messages(self, queue, status):
        messages = Email.objects.filter(
            queue=queue,
            recipient__status=status).distinct()

        for message in messages:
            for recipient in message.recipient_set.all():
                if self.__check_unsubscribe(recipient.address):
                    recipient.status = 'blocked_unsubscribe'
                    recipient.save()

        return(messages)

    def __check_unsubscribe(self, address):
        try:
            Unsubscribe.objects.get(address=address)
            return True
        except Unsubscribe.DoesNotExist:
            return False


    def handle(self, *args, **options):
        connection = get_connection(backend=EMAIL_BACKEND)

        if options['retry']:
            status='deferred'
        else:
            status='in_queue'

        if len(args) == 0:
            args = [x['queue'] for x in Queue.objects.all().values()]

        for queue_name in args:
            queue = Queue.objects.get(queue=queue_name)

            messages = self.__messages(queue, status=status)
            if messages:
                for message in messages:
                    alternatives = Alternative.objects.filter(
                        email=message).values_list('content', 'mimetype')
                    attachments = Attachment.objects.filter(email=message)

                    headers = Header.objects.filter(
                        email=message).values('key', 'value')
                    mail_headers = {}
                    for header in headers:
                        mail_headers[header['key']] = header['value']

                    recipients = message.recipient_set.filter(
                        status=status)
                    message_to = recipients.filter(
                        recipient_type='to',
                        ).values_list('address', flat=True)
                    message_bcc = message.recipient_set.filter(
                        recipient_type='bcc',
                        ).values_list('address', flat=True)
                    message_cc = message.recipient_set.filter(
                        recipient_type='cc',
                        ).values_list('address', flat=True)

                    if alternatives:
                        email = EmailMultiAlternatives(
                            message.subject,
                            message.body,
                            message.m_from,
                            message_to,
                            message_bcc,
                            connection,
                            None,
                            headers=mail_headers,
                            alternatives=alternatives,
                            cc=message_cc,
                        )
                    else:
                        email = EmailMessage(
                            message.subject,
                            message.body,
                            message.m_from,
                            message_to,
                            message_bcc,
                            connection,
                            None,
                            headers=mail_headers,
                            cc=message_cc,
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
                        for recipient in recipients:
                                recipient.status = 'sent_success'
                                recipient.save()

                    except (socket_error, smtplib.SMTPSenderRefused,
                            smtplib.SMTPRecipientsRefused,
                            smtplib.SMTPAuthenticationError):
                        for recipient in recipients:
                            recipient.status = 'deferred'
                            recipient.save()