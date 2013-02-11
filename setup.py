#!/usr/bin/env python

from distutils.core import setup

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
    package_data=[
        'mcfeely': ['fixtures/*']
    ],
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
)
