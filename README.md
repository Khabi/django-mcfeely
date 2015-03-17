[![Build Status](https://travis-ci.org/Khabi/django-mcfeely.png?branch=master)](https://travis-ci.org/Khabi/django-mcfeely)
[![Coverage Status](https://coveralls.io/repos/Khabi/django-mcfeely/badge.png?branch=master)](https://coveralls.io/r/Khabi/django-mcfeely?branch=master)

django-mcfeely
==============

Requires Django 1.3 and higher

Django mail queue backend.  Allows for putting email in specific queues to be sent out in batches (via a management command), editing emails from the admin and more.


Configuration
==============

Add mcfeely to your INSTALLED_APPS settings:
```python
INSTALLED_APPS = ( 'mcfeely', )
```

django-mcfeely supplies its own email backend that you must add to your settings.py file.  This stores all the information needed to create an email at sendtime in the database.
```python
EMAIL_BACKEND = 'mcfeely.backend.DbBackend'
```

Usage with django's buit in send_mail.
==============
For basic queueing with only a default queue (usefull if you just want to delay sending of emails) there is no other configuration required.  django-mcfeely will work out of the box with djangos built in send_mail function.
```python
from django.core.mail import send_mail

send_mail('Subject here', 'Here is the message.', 'from@example.com',
    ['to@example.com'], fail_silently=False)
```

This will only place mail in the "Default" queue.  If you want to place email into defined queues you have to use mcfeely's custom send_mail function

Usage with mcfeely's send_mail 
===============
django-mcfeely provides its own send_mail function that can be used to place emails into custom queues.

```python
from mcfeely.models import Queue
from mcfeely.mail import send_mail

mail_queue =  Queue.objects.get(queue='sample_queue')
send_mail('Subject here', 'Here is the message.', 'from@example.com',
     ['to@example.com'], queue=mail_queue, fail_silently=False)
```

Or you can pass it the name of a queue instead.
```python
from mcfeely.mail import send_mail

send_mail('Subject here', 'Here is the message.', 'from@example.com',
     ['to@example.com'], queue='sample_queue', fail_silently=False)
```

Sending Queued Mail
===============
Queued Mail is sent via a management command
```bash
python manage.py send_queue <queue_name>
```
