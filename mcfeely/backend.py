from django.core.mail.backends.base import BaseEmailBackend
from email.mime.base import MIMEBase

from mcfeely.models import Email, Attachment, Alternative, Header
from mcfeely.models import Recipient
from mcfeely.engine import default_queue


class DbBackend(BaseEmailBackend):

    def send_messages(self, email_messages):
        num_sent = 0

        if not email_messages:
            return num_sent

        for message in email_messages:

            if not hasattr(message, 'queue'):
                message.queue = default_queue(None)

            email = Email.objects.create(
                m_from=message.from_email,
                subject=message.subject,
                body=message.body,
                queue=message.queue
            )

            for address in message.to:
                Recipient.objects.create(
                    email=email,
                    address=address,
                    recipient_type='to')

            for address in message.cc:
                Recipient.objects.create(
                    email=email,
                    address=address,
                    recipient_type='cc')

            for address in message.bcc:
                Recipient.objects.create(
                    email=email,
                    address=address,
                    recipient_type='bcc')

            for attachment in message.attachments:
                if isinstance(attachment, tuple):
                    filename, content, mimetype = attachment
                elif isinstance(attachment, MIMEBase):
                    filename = attachment.get_filename()
                    content = attachment.get_payload(decode=True)
                    mimetype = "%s/%s" % (attachment.get_content_maintype(), attachment.get_content_subtype())
                else:
                    continue
                Attachment.objects.create(
                    email=email,
                    filename=filename,
                    content=content,
                    mimetype=mimetype
                )

            for header in message.extra_headers:
                Header.objects.create(
                    email=email,
                    key=header,
                    value=message.extra_headers[header],
                )

            try:
                for alternative in message.alternatives:
                    content, mimetype = alternative
                    Alternative.objects.create(
                        email=email,
                        content=content,
                        mimetype=mimetype
                    )
            except AttributeError:
                pass

            if(email):
                num_sent += 1

        return num_sent
