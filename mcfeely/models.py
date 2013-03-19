from django.db import models
from mcfeely.fields import Base64Field

STATUS = (
    ('in_queue', 'In Queue'),
    ('sent_success', 'Sent Successfuly'),
    ('deferred', 'Deferred'),
    ('blocked_unsubscribe', 'Blocked by unsubscribe'),
    ('failure', 'Failure'),
)
RECIPIENT_TYPE = (
    ('to', 'To'),
    ('cc', 'CC'),
    ('bcc', 'BCC'),
)


class Queue(models.Model):
    queue = models.CharField(max_length=50)
    description = models.CharField('Queue Description',max_length=200)
    display_to_user = models.BooleanField(default=False)

    def __unicode__(self):
        return(self.description)


class Email(models.Model):
    """ Queued up Emails to be sent out. """
    m_from = models.TextField('From')

    # Subjects can be be longer if they're split byt CRLF, but this is a good
    # default
    subject = models.CharField(max_length=78)
    body = models.TextField()
    queue = models.ForeignKey(Queue)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return('[ %s ] - %s' % (self.queue, self.subject))


class Recipient(models.Model):
    email = models.ForeignKey(Email)
    address = models.CharField(max_length=254)
    recipient_type =  models.CharField(max_length=3, choices=RECIPIENT_TYPE)
    status = models.CharField(max_length='100', default='in_queue', choices=STATUS)


class Alternative(models.Model):
    email = models.ForeignKey(Email, related_name='alternatives')
    content = models.TextField()
    mimetype = models.CharField(max_length=255)


class Attachment(models.Model):
    email = models.ForeignKey(Email, related_name='attachments')
    filename = models.CharField(
        max_length=255, null=True, blank=True, default=None)
    content = Base64Field(null=True, blank=True, default=None)
    mimetype = models.CharField(
        max_length=255, null=True, blank=True, default=None)


class Header(models.Model):
    email = models.ForeignKey(Email, related_name='headers')
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)


class Unsubscribe(models.Model):
    """ Any email addresses in this table we will not send mail to.  """
    address = models.EmailField('Email Address')
    added = models.DateTimeField(auto_now_add=True)
    queue = models.ForeignKey(Queue, blank=True, null=True)


    class Meta:
        verbose_name = ('Usubscribe')
        verbose_name_plural = ('Unsubscribe')
        unique_together = ('address', 'queue')

    def __unicode__(self):
        return(self.address)

