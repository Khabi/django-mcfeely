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
from mcfeely.models import Email, Recipient
from mcfeely.models import Queue
from mcfeely.models import Unsubscribe
from django.conf import settings
from django.core import mail


class SimpleTest(TestCase):
    def setUp(self):
        mcfeely_backend = 'mcfeely.backend.DbBackend'
        test_sender = 'django.core.mail.backends.locmem.EmailBackend'

        settings.EMAIL_BACKEND = mcfeely_backend
        settings.MCFEELY_EMAIL_BACKEND = test_sender

        default_q = getattr(
            settings, 'DEFAULT_EMAIL_QUEUE', 'Default'
        )
        self.default_q = Queue.objects.get(queue=default_q)

        self.q = Queue(queue='Test_Queue')
        self.q.save()

        self.unsub_all = Unsubscribe(address='unsub1@example.com')
        self.unsub_all.save()

        self.unsub_testqueue = Unsubscribe(
            address='unsub2@example.com',
            queue=self.q)
        self.unsub_testqueue.save()

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def _send_mail_simple(self, subject=uuid4(), mail_to=['tester@example.com'], queue=None):
        send_mail(
            str(subject),
            'test email',
            'test@example.com',
            mail_to,
            queue=queue,
            fail_silently=False)
        return str(subject)

    def _send_mail_advanced(self, subject=uuid4(), mail_to=['tester@example.com'],
                   mail_cc=None, mail_bcc=None, headers=None, queue=None):
        email = QueueEmailMessage(
            str(subject),
            'test email',
            'test@example.com',
            mail_to,
            cc=mail_cc,
            bcc=mail_bcc,
            queue=queue,
            headers=headers)

        email.send()
        return str(subject)

    def _send_mail_attachment(self, subject=uuid4(),
                              mail_to=['tester@example.com'], queue=None):
        email = QueueEmailMessage(
            str(subject),
            'test email',
            'test@example.com',
            mail_to,
            queue=queue)

        email.attach(
            'sample.txt',
            'Sample attachement Text',
            'text/plain')

        email.send()
        return str(subject)

    def _send_mail_alternative(self, subject=uuid4(),
                               mail_to=['tester@example.com'], queue=None):
        email = QueueEmailMultiAlternatives(
            str(subject),
            'test email',
            'test@example.com',
            mail_to,
            queue=queue)

        email.attach_alternative(
            '<b>Test Alternative</b>',
            'text/html')

        email.send()
        return str(subject)

    def test_simple_mail(self):
        subject = self._send_mail_simple()
        Email.objects.get(subject=subject)

        call_command('send_queue')
        self.assertEqual(len(mail.outbox), 1)

    def test_advanced_mail(self):
        subject = self._send_mail_advanced(
            mail_cc = ['cctest@example.com'],
            mail_bcc = ['bcctest@example.com'],
            headers={'Reply-To': 'another@example.com'},
            queue = self.q)
        Email.objects.get(subject=subject, queue=self.q)

        call_command('send_queue', 'Test_Queue')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].to), 1)
        self.assertEqual(len(mail.outbox[0].bcc), 1)
        self.assertEqual(len(mail.outbox[0].cc), 1)
        self.assertEqual(
            mail.outbox[0].extra_headers['Reply-To'],
            'another@example.com')

    def test_queue_mail(self):
        subject = self._send_mail_simple(queue=self.q)
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

    def test_unsubscribe(self):
        subject = self._send_mail_simple(
            mail_to=['unsub1@example.com',
            'tester@example.com'])
        Email.objects.get(subject=subject)

        call_command('send_queue')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].to), 1)

