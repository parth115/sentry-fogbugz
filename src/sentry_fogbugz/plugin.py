
"""
sentry_fogbugz.plugin
~~~~~~~~~~~~~~~~~~~~~

"""

from django import forms
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from sentry.plugins.bases.issue import IssuePlugin

import fogbugz
import sentry_fogbugz


class FogbugzOptionsForm(forms.Form):
    url = forms.CharField(label=_('FogBugz URL'),
                          widget=forms.TextInput(attrs={'class': 'span3',
                                                        'placeholder': 'e.g. http://fogbugz.example.com'}),
                          help_text=mark_safe(_('Enter your FogBugz URL',)))
    project = forms.IntegerField(label=_('Project ID'),
                                 widget=forms.TextInput(attrs={'class': 'span3', 'placeholder': 'e.g. 639281'}),
                                 help_text=_('Enter your project\'s numerical ID.'))
    username = forms.CharField(label=_("FogBugz Username"),
                               widget=forms.TextInput(attrs={'class': 'span3'}))
    password = forms.CharField(label=_("FogBugz Password"),
                               widget=forms.TextInput(attrs={"class": "span3"}))


class FogbugzPlugin(IssuePlugin):
    author = 'Parth Buch'
    author_url = 'https://github.com/parth115/sentry-fogbugz'
    version = sentry_fogbugz.VERSION
    description = "Integrate FogBug stories by linking a project and account."

    slug = 'fogbugz'
    title = _('FogBugz')
    conf_title = title
    conf_key = 'fogbugz'
    project_conf_form = FogbugzOptionsForm

    def is_configured(self, request, project, **kwargs):
        return all(self.get_option(k, project) for k in ('url', 'project', 'username', 'password'))

    def get_new_issue_title(self, **kwargs):
        return 'Add Story'

    def get_api_client(self, group):
        fb = fogbugz.FogBugz(self.get_option('url', group.project))
        fb.logon(self.get_option('username', group.project), self.get_option('password', group.project))
        return fb

    def create_issue(self, request, group, form_data, **kwargs):
        client = self.get_api_client(group)

        try:
            resp = client.new(ixProject=self.get_option('project', group.project),
                              sTitle=form_data['title'],
                              ixPriority=1)
        except Exception, e:
            raise forms.ValidationError(_('Error communicating with Fogbugz: %s') % (unicode(e),))

        return dict(resp.findChild('case').attrs)['ixbug']

    def get_issue_label(self, group, issue_id, **kwargs):
        return '#%s' % issue_id

    def get_issue_url(self, group, issue_id, **kwargs):
        return "%s/default.asp?%s" % (self.get_option('url', group.project), issue_id)