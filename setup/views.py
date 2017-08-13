
# coding=utf-8
#
from datetime import date, timedelta, datetime

from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.utils import timezone

from headcrumbs.decorators import crumb
from headcrumbs.util import name_from_pk

from cms.functions import notify_by_email, show_form, visualiseDateTime

from members.models import Member

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
  done_url	= settings.TEMPLATE_CONTENT['setup']['init']['done']['url']

  if r.POST:
    sf = SetupForm(r.POST,r.FILES)
    if sf.is_valid():
      # all fine -> create (local) settings file
      name		= sf.cleaned_data['name']
      logo		= sf.cleaned_data['logo']
      admin_email	= sf.cleaned_data['admin_email']
      default_sender 	= sf.cleaned_data['default_sender']
      default_email 	= sf.cleaned_data['default_email']
      default_footer 	= sf.cleaned_data['default_footer']
      apps		= sf.cleaned_data['apps']
      # HERE

    # form not valid -> error
    else:
      return TemplateResponse(r, done_template, {
                	'title'		: done_title, 
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in sf.errors]),
                   })
  # no post yet -> empty form
  else:
    form = SetupForm()
    return TemplateResponse(r, form_template, {
                	'title'	: form_title,
                	'desc'	: form_desc,
                	'submit': form_submit,
                	'form'	: form,
                })


