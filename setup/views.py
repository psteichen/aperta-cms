
# coding=utf-8
#
from datetime import date, timedelta, datetime
from fileinput import  FileInput

from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.utils import timezone
from django.contrib.sites.models import Site
from django.core import management
from django.core.management.commands import loaddata

from headcrumbs.decorators import crumb
from headcrumbs.util import name_from_pk

from cms.functions import notify_by_email, show_form, visualiseDateTime

from members.models import Member

from .models import Setup
from .forms import SetupForm


###############
# SETUP VIEWS #
###############

# init #
########
@staff_member_required
@crumb(u'Setup')
def init(r):

  form_template	= settings.TEMPLATE_CONTENT['setup']['init']['template']
  form_title	= settings.TEMPLATE_CONTENT['setup']['init']['title']
  form_desc	= settings.TEMPLATE_CONTENT['setup']['init']['desc']
  form_submit	= settings.TEMPLATE_CONTENT['setup']['init']['submit']

  done_template	= settings.TEMPLATE_CONTENT['setup']['init']['done']['template']
  done_title	= settings.TEMPLATE_CONTENT['setup']['init']['done']['title']
  done_message	= settings.TEMPLATE_CONTENT['setup']['init']['done']['message']

  if r.POST:
    sf = SetupForm(r.POST,r.FILES)
    if sf.is_valid():
      S = sf.save(commit=False)
      S.cfg_date = timezone.now()
      S.save()

      # adjust site to actual site (this removes 'config' alert)
      site = Site.objects.get(pk=settings.SITE_ID)
      site.name=settings.ALLOWED_HOSTS[0]
      site.save()

      # load initial data for groups
      management.call_command('loaddata', 'groups', verbosity=0)

      # all fine -> redirect to "import members and calendar"
      return TemplateResponse(r, done_template, {
                	'title'		: done_title, 
                	'message'	: done_message,
                   })

    # form not valid -> error
    else:
      return TemplateResponse(r, done_template, {
                	'title'		: done_title, 
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in sf.errors]),
                   })

  # no post yet -> empty form
  else:
    setup_initials = {
      'org_name' 	: settings.TEMPLATE_CONTENT['meta']['logo']['title'],
      'org_logo'	: settings.TEMPLATE_CONTENT['meta']['logo']['img'],
      'admin_email'	: settings.SERVER_EMAIL,
      'default_email'	: settings.DEFAULT_FROM_EMAIL,
      'default_footer'	: settings.EMAILS['footer'],
    }
    form = SetupForm(initial=setup_initials)

    return TemplateResponse(r, form_template, {
                	'title'	: form_title,
                	'desc'	: form_desc,
                	'submit': form_submit,
                	'form'	: form,
                })


