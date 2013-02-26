from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from email.mime.base import MIMEBase

from mcfeely.models import Email, Queue, Attachment, Alternative, Header


class DbBackend(BaseEmailBackend):

    def send_messages(self, email_messages):
        num_sent = 0
        default_queue = getattr(
            settings, 'DEFAULT_EMAIL_QUEUE', 'Default'
        )

        if not email_messages:
            return num_sent

        for message in email_messages:
            queue = getattr(
                message,
                'queue',
                default_queue
            )
            if queue is None:
                queue = default_queue

            message_queue = Queue.objects.get(
                queue=queue
            )

            email = Email.objects.create(
                m_from='%s' % message.from_email,
                m_to=', '.join(message.to),
                m_cc=', '.join(message.cc),
                m_bcc=', '.join(message.bcc),
                subject='%s' % message.subject,
                body='%s' % message.body,
                queue=message_queue
            )

            for attachment in message.attachments:
                if isinstance(attachment, tuple):
                    filename, content, mimetype = attachment
                elif isinstance(attachment, MIMEBase):
                    filename = attachment.get_filename()
                    content = attachment.get_payload(decode=True)
                    mimetype = None
                else:
                    continue
                Attachment.objects.create(
                    email=email,
                    filename=filename,
                    content=content,
                    mimetype=mimetype
                )

            for header in message.extra_headers:
                print(header)
                print(message.extra_headers[header])

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
