from django.db import models
from fields import Base64Field



class Queue(models.Model):
    queue = models.CharField(max_length=50)

    class Meta:
        verbose_name = ('Queue Type')
        verbose_name_plural = ('Queue Types')

    def __unicode__(self):
        return(self.queue)


class Email(models.Model):
    """ Queued up Emails to be sent out. """
    m_to = models.TextField('To')
    m_from = models.TextField('From')
    m_cc = models.TextField('CC', null=True, blank=True)
    m_bcc = models.TextField('BCC', null=True, blank=True)

    # Subjects can be be longer if they're split byt CRLF, but this is a good
    # default
    subject = models.CharField(max_length=78)
    body = models.TextField()
    queue = models.ForeignKey(Queue)
    deferred = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)

    class Meta:
        verbose_name = ('Message Queue')
        verbose_name_plural = ('Message Queue')

    def __unicode__(self):
        return('[ %s ] - %s' % (self.queue, self.subject))


STATUS = (
    ('1', 'success'),
    ('2', 'blocked'),
    ('3', 'failure')
)

class Alternative(models.Model):
    email = models.ForeignKey(Email, related_name='alternatives')
    content = models.TextField()
    mimetype = models.CharField(max_length=255)

class Attachment(models.Model):
    email = models.ForeignKey(Email, related_name='attachments')
    filename = models.CharField(max_length=255, null=True, blank=True, default=None)
    content = Base64Field(null=True, blank=True, default=None)
    mimetype = models.CharField(max_length=255, null=True, blank=True, default=None)

class Header(models.Model):
    email = models.ForeignKey(Email, related_name='headers')
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)


class Unsubscribe(models.Model):
    """ Any email addresses in this table we will not send mail to.  """
    address = models.EmailField()
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ('Usubscribe')
        verbose_name_plural = ('Unsubscribe')

    def __unicode__(self):
        return(self.address)
