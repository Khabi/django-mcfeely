#!/usr/bin/env python

from distutils.core import setup
from distutils.core import Command


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings
        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3'}},
            INSTALLED_APPS=('mcfeely',))
        from django.core.management import call_command
        call_command('test', 'mcfeely')


class ShellCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings
        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3'}},
            INSTALLED_APPS=('mcfeely',))
        from django.core.management import call_command
        call_command('shell')


class RunserverCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings
        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3'}},
            INSTALLED_APPS=('mcfeely',),
            ALLOWED_HOSTS='127.0.0.1',
            ROOT_URLCONF = 'mcfeely.urls',
            DEBUG=True)
        from django.core.management import call_command
        call_command('syncdb')
        call_command('runserver')

setup(
    name='django-mcfeely',
    version='0.3',
    description='Email queuing system for django',
    author='Richard Cox',
    author_email='code@bot37.com',
    url='https://github.com/Khabi/django-mcfeely',
    long_description="""
        Django mail queue backend.  Allows for putting email in specific queues
        to be sent out in batches (via a management command), editing emails
        from the admin and more.
    """,
    packages=[
        'mcfeely',
        'mcfeely.management',
    ],
    package_data={
        'mcfeely': ['fixtures/*', 'templates/*'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        'Topic :: Utilities'
    ],
    cmdclass={'test': TestCommand, 'shell':
              ShellCommand, 'runserver': RunserverCommand}
)
