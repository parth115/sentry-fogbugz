"""
sentry_fogbugz
~~~~~~~~~~~~~~
"""

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('sentry-fogbugz').version
except Exception, e:
    VERSION = 'unknown'