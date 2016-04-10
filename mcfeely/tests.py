from email.mime.base import MIMEBase

from django.test import TestCase
from django.test.client import Client

from django.core.management import call_command
from django.conf import settings
from django.core import mail
from django.core.mail import send_mail as orig_send_mail
from django.core.mail import mail_admins as orig_mail_admins
from django.core.mail import mail_managers as orig_mail_managers

from uuid import uuid4

from mcfeely import urls
from mcfeely.mail import send_mail
from mcfeely.mail import mail_admins
from mcfeely.mail import mail_managers

from mcfeely.engine import QueueEmailMessage
from mcfeely.engine import QueueEmailMultiAlternatives
from mcfeely.models import Email
from mcfeely.models import Queue
from mcfeely.models import Unsubscribe


default_to = ['tester@example.com']
default_from = 'testemail@example.com'
default_message = "Test E-Mail body"


def django_send_mail(mail_to=default_to):
    subject = str(uuid4())
    results = orig_send_mail(
        subject,
        default_message,
        default_from,
        mail_to,
        fail_silently=False)
    return [subject, results]


def django_mail_admins():
    subject = str(uuid4())
    results = orig_mail_admins(
        subject,
        default_message)
    return [subject, results]


def django_mail_managers():
    subject = str(uuid4())
    results = orig_mail_managers(
        subject,
        default_message)
    return [subject, results]


def mcfeely_send_mail(mail_to=default_to, queue=None):
    subject = str(uuid4())
    results = send_mail(
        subject,
        default_message,
        default_from,
        mail_to,
        queue=queue,
        fail_silently=False)
    return [subject, results]


def mcfeely_mail_admins(queue=None):
    subject = str(uuid4())
    results = mail_admins(
        subject,
        default_message,
        queue,
        html_message='<b>%s</b>' % default_message)
    return [subject, results]


def mcfeely_mail_managers(queue=None):
    subject = str(uuid4())
    results = mail_managers(
        subject,
        default_message,
        queue,
        html_message='<b>%s</b>' % default_message)
    return [subject, results]


def simple_mail(mail_to=default_to, queue=None):
    subject = str(uuid4())
    email = QueueEmailMessage(
        subject,
        default_message,
        default_from,
        mail_to,
        queue=queue)
    return [subject, email]


def simple_alternative_mail(mail_to=default_to, queue=None):
    subject = str(uuid4())
    email = QueueEmailMultiAlternatives(
        subject,
        default_message,
        default_from,
        mail_to,
        queue=queue)
    return [subject, email]


def mail_attachment(mail_to=default_to, queue=None):
    subject, email = simple_mail(mail_to, queue)
    email.attach(
        'sample.txt',
        'Sample attachement Text',
        'text/plain')

    results = email.send()
    return [subject, results]


def mail_attachment_mimebase(mail_to=default_to, queue=None):
    subject, email = simple_mail(mail_to, queue)
    data = MIMEBase('text', 'plain')
    data.add_header('content-disposition', 'attachment', filename='test.txt')
    data.set_payload('TEST DATA')
    email.attach(data)
    results = email.send()
    return [subject, results]


def mail_alternative(mail_to=default_to, queue=None):
    subject, email = simple_alternative_mail(mail_to, queue)
    email.attach_alternative(
        '<b>Test Alternative</b>',
        'text/html')

    results = email.send()
    return [subject, results]


def mail_advanced(mail_to=default_to, mail_cc=None, mail_bcc=None,
                  headers=None, queue=None):
    subject = str(uuid4())
    email = QueueEmailMessage(
        subject,
        default_message,
        default_from,
        mail_to,
        cc=mail_cc,
        bcc=mail_bcc,
        queue=queue,
        headers=headers)

    email.send()
    return str(subject)


class Simple_Email(TestCase):

    def setUp(self):
        mcfeely_backend = 'mcfeely.backend.DbBackend'
        test_sender = 'django.core.mail.backends.locmem.EmailBackend'

        settings.EMAIL_BACKEND = mcfeely_backend
        settings.MCFEELY_EMAIL_BACKEND = test_sender
        settings.ADMINS = (
            ('Admin One', 'admin_one@example.com'),
            ('Admin Two', 'admin_two@example.com')
        )
        settings.MANAGERS = (
            ('Manager One', 'manager_one@example.com'),
            ('Manager Two', 'manager_two@example.com')
        )

        self.queue = Queue(queue='Default', description='Default Queue')
        self.queue.save()
        self.queue = Queue(queue='Test_Queue', description='Testing')
        self.queue.save()


    def test_django_send_mail(self):
        """
            Tests django's send_mail function with the mcfeely backend
        """
        subject, results = django_send_mail()
        call_command('send_queue')

        self.assertEqual(Email.objects.filter(subject=subject).count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(results, 1)

    def test_django_mail_admins(self):
        """
            Tests the django mail_admins() function
        """
        subject, results = django_mail_admins()
        call_command('send_queue')

        self.assertEqual(Email.objects.filter(
            subject="[Django] %s" % subject).count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_django_mail_managers(self):
        """
            Tests the django mail_managers() function
        """
        subject, results = django_mail_managers()
        call_command('send_queue')

        self.assertEqual(Email.objects.filter(
            subject="[Django] %s" % subject).count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_send_mail(self):
        """
            Tests the mcfeely send_mail() function
        """
        subject, results = mcfeely_send_mail()
        call_command('send_queue')

        self.assertEqual(Email.objects.filter(subject=subject).count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(results, 1)

    def test_queue_mail(self):
        """
            Tests the mcfeely send_mail() function with queue
        """
        subject, results = mcfeely_send_mail(queue=self.queue)
        call_command('send_queue', 'Test_Queue')

        self.assertEqual(Email.objects.filter(
            subject=subject, queue=self.queue).count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(results, 1)

    def test_queue_name_mail(self):
        """
            Tests email sending with just a queue name and not a object
        """
        subject, results = mcfeely_send_mail(queue='Test_Queue')
        call_command('send_queue', 'Test_Queue')

        self.assertEqual(Email.objects.filter(
            subject=subject, queue=self.queue).count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(results, 1)

    def test_mail_admins(self):
        """
            Tests the mcfeely mail_admins() function
        """
        subject, results = mcfeely_mail_admins()
        call_command('send_queue')

        self.assertEqual(Email.objects.filter(
            subject="[Django] %s" % subject).count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_mail_managers(self):
        """
            Tests the mcfeely mail_admins() function
        """
        subject, results = mcfeely_mail_managers()
        call_command('send_queue')

        self.assertEqual(Email.objects.filter(
            subject="[Django] %s" % subject).count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_simple_mail(self):
        subject, email = simple_mail()
        results = email.send()
        call_command('send_queue')

        self.assertEqual(Email.objects.filter(subject=subject).count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(results, 1)


class Advanced_Email(TestCase):

    def setUp(self):
        mcfeely_backend = 'mcfeely.backend.DbBackend'
        test_sender = 'django.core.mail.backends.locmem.EmailBackend'

        settings.EMAIL_BACKEND = mcfeely_backend
        settings.MCFEELY_EMAIL_BACKEND = test_sender

        self.queue = Queue(queue='Default', description='Default Queue')
        self.queue.save()
        self.queue = Queue(queue='Test_Queue', description='Testing')
        self.queue.save()

    def test_attachment(self):
        """
            Simple mail attachment
        """
        subject, results = mail_attachment(queue=self.queue)
        call_command('send_queue', 'Test_Queue')

        self.assertEqual(Email.objects.filter(
            subject=subject, queue=self.queue).count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEqual(mail.outbox[0].attachments[0][1], 'Sample attachement Text')


    def test_attachment_mimebase(self):
        """
            Simple mail attachment of a mimebase object
        """
        subject, results = mail_attachment_mimebase()
        call_command('send_queue')

        attachments = Email.objects.get(subject=subject).attachments.get()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEqual(attachments.filename, 'test.txt')
        self.assertEqual(attachments.mimetype, 'text/plain')
        self.assertEqual(mail.outbox[0].attachments[0][1], 'TEST DATA')

    def test_alternative(self):
        """
            Alternative email test
        """
        subject, results = mail_alternative(queue=self.queue)
        call_command('send_queue', 'Test_Queue')

        self.assertEqual(Email.objects.filter(
            subject=subject, queue=self.queue).count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].alternatives), 1)

    def test_advanced_mail(self):
        """
            Test advanced mail sending with extra headers
        """
        subject = mail_advanced(
            mail_cc=['cctest@example.com'],
            mail_bcc=['bcctest@example.com'],
            headers={'Reply-To': 'another@example.com'},
            queue=self.queue)
        call_command('send_queue', 'Test_Queue')

        self.assertEqual(Email.objects.filter(
            subject=subject, queue=self.queue).count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].to), 1)
        self.assertEqual(len(mail.outbox[0].bcc), 1)
        self.assertEqual(len(mail.outbox[0].cc), 1)
        self.assertEqual(
            mail.outbox[0].extra_headers['Reply-To'],
            'another@example.com')


class Unsubscribe_Email(TestCase):

    def setUp(self):
        mcfeely_backend = 'mcfeely.backend.DbBackend'
        test_sender = 'django.core.mail.backends.locmem.EmailBackend'

        settings.EMAIL_BACKEND = mcfeely_backend
        settings.MCFEELY_EMAIL_BACKEND = test_sender
        settings.ROOT_URLCONF = 'mcfeely.urls'

        self.queue = Queue(queue='Default', description='Default Queue')
        self.queue.save()
        self.queue = Queue(queue='Test_Queue', description='Testing')
        self.queue.save()

        self.unsub_all = Unsubscribe(address='unsub1@example.com',)
        self.unsub_all.save()

        self.unsub_testqueue = Unsubscribe(
            address='unsub2@example.com',
            queue=self.queue)
        self.unsub_testqueue.save()

        self.client = Client()

    def test_usubscribe_view(self):
        """
            Generic unsubscribe view
        """
        response = self.client.get('/unsubscribe/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/unsubscribe/', {'address': 'unsub_test@example.com'})
        self.assertEqual(Unsubscribe.objects.filter(
            address='unsub_test@example.com').count(), 1)

    def test_unsub_all(self):
        """
            Tests unsubscribing from all emails
        """
        subject, email = simple_mail(mail_to=['unsub1@example.com'])
        results = email.send()
        call_command('send_queue')
        self.assertEqual(Email.objects.filter(subject=subject).count(), 1)
        self.assertEqual(len(mail.outbox), 0)

    def test_unsub_queue(self):
        """
            Tests unsubscribing from specific email queues
        """
        subject, email = simple_mail(
            mail_to=['unsub2@example.com'], queue=self.queue)
        results = email.send()
        call_command('send_queue')

        self.assertEqual(Email.objects.filter(subject=subject).count(), 1)
        self.assertEqual(len(mail.outbox), 0)
