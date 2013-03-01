"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.management import call_command

from uuid import uuid4
from mcfeely.mail import send_mail
from mcfeely.engine import QueueEmailMessage
from mcfeely.engine import QueueEmailMultiAlternatives
from mcfeely.models import Email
from mcfeely.models import Queue
from django.conf import settings
from django.core import mail


class SimpleTest(TestCase):
    def setUp(self):
        mcfeely_backend = 'mcfeely.backend.DbBackend'
        test_sender = 'django.core.mail.backends.locmem.EmailBackend'

        settings.EMAIL_BACKEND = mcfeely_backend
        settings.MCFEELY_EMAIL_BACKEND = test_sender

        self.q = Queue(queue='Test_Queue')
        self.q.save()

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def _send_mail(self, subject=uuid4(), queue=None):
        send_mail(
            str(subject),
            'test email',
            'test@example.org',
            ['tester@example.org'],
            queue=queue,
            fail_silently=False)
        return str(subject)

    def _send_mail_attachment(self, subject=uuid4(), queue=None):
        email = QueueEmailMessage(
            str(subject),
            'test email',
            'test@example.org',
            ['tester@example.org'],
            queue=queue)

        email.attach(
            'sample.txt',
            'Sample attachement Text',
            'text/plain')

        email.send()
        return str(subject)

    def _send_mail_alternative(self, subject=uuid4(), queue=None):
        email = QueueEmailMultiAlternatives(
            str(subject),
            'test email',
            'test@example.org',
            ['tester@example.org'],
            queue=queue)

        email.attach_alternative(
            '<b>Test Alternative</b>',
            'text/html')

        email.send()
        return str(subject)

    def test_basic_mail(self):
        subject = self._send_mail()
        Email.objects.get(subject=subject)

        call_command('send_queue')
        self.assertEqual(len(mail.outbox), 1)

    def test_queue_mail(self):
        subject = self._send_mail(queue=self.q)
        Email.objects.get(subject=subject, queue=self.q)

        call_command('send_queue', 'Test_Queue')
        self.assertEqual(len(mail.outbox), 1)

    def test_attachment(self):
        subject = self._send_mail_attachment(queue=self.q)
        Email.objects.get(subject=subject, queue=self.q)

        call_command('send_queue', 'Test_Queue')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].attachments), 1)

    def test_alternative(self):
        subject = self._send_mail_alternative(queue=self.q)
        Email.objects.get(subject=subject, queue=self.q)

        call_command('send_queue', 'Test_Queue')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].alternatives), 1)
