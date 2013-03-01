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

setup(
    name='django-mcfeely',
    version='0.1',
    description='Email queuing system for django',
    author='Richard Cox',
    author_email='richard@pixelatedninja.com',
    url='https://github.com/Khabi/django-mcfeely',
    packages=[
        'mcfeely',
        'mcfeely.management',
    ],
    package_data={
        'mcfeely': ['fixtures/*'],
    },
    classifiers=[
        'Development Status :: 1 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
    cmdclass={'test': TestCommand, 'shell': ShellCommand}
)
