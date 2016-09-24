#!/usr/bin/env python

from distutils.core import setup

setup(name='webapis',
    version='1.0',
    description='Octronic Web APIs',
    author="Ash '80' Thompson",
    author_email='ash@octronic.co.uk',
    url='https://octronic.co.uk/',
    packages=[
        'octronic.webapis.event',
        'octronic.webapis.session',
        'octronic.webapis.user'
    ],
)