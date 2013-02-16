"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.management import call_command

from uuid import uuid4
from mail import send_mail
from models import Email
from models import Queue
from django.conf import settings
from django.core import mail


class SimpleTest(TestCase):
    def setUp(self):
        settings.EMAIL_BACKEND = 'mcfeely.backend.DbBackend'
        settings.MCFEELY_EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
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
