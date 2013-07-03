#!/usr/bin/env python
"""
sentry-pivotal
==============

An extension for Sentry which integrates with Pivotal Tracker. Specifically, it allows you to easily create
issues from events within Sentry.

:copyright: (c) 2012 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from setuptools import setup, find_packages




install_requires = [
    'sentry>=5.0.0',
    'fogbugz',
]

setup(
    name='sentry-fogbugz',
    version='0.1.0',
    author='David Cramer',
    author_email='dcramer@gmail.com',
    url='http://github.com/getsentry/sentry-pivotal',
    description='A Sentry extension which integrates with Pivotal Tracker.',
    long_description=__doc__,
    license='BSD',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
       'sentry.apps': [
            'sentry_fogbugz = sentry_fogbugz',
        ],
       'sentry.plugins': [
            'sentry_fogbugz = sentry_fogbugz.plugin:FogbugzPlugin'
        ],
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)