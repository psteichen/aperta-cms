
# coding=utf-8
#
from datetime import date, timedelta, datetime
from fileinput import  FileInput

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
  done_title	= settings.TEMPLATE_CONTENT['setup']['init']['done']['title']
  done_message	= settings.TEMPLATE_CONTENT['setup']['init']['done']['message']

  if r.POST:
    sf = SetupForm(r.POST,r.FILES)
    if sf.is_valid():
      # all fine -> create (local) settings file
      name		= sf.cleaned_data['org_name']
      logo		= sf.cleaned_data['org_logo']
      admin_email	= sf.cleaned_data['admin_email']
      default_email 	= sf.cleaned_data['default_email']
      default_footer 	= sf.cleaned_data['default_footer']
      optional_apps	= sf.cleaned_data['optional_apps']

# HERE
      # adjust settings file
# file method:
#      with FileInput(fileToSearch, inplace=True, backup='.bak') as file:
#      for line in file:
#        line.replace(textToSearch, textToReplace)

# configure method:
#      settings.configure(ADMIN_EMAIL=admin_email)
#      settings.configure(SERVER_EMAIL=admin_email)
#      settings.configure(DEFAULT_FROM_EMAIL=default_email)
#      settings.configure(EMAILS['sender']['default']="'"+name+"' <"+default_email+">")
#      settings.configure(EMAILS['footer']=default_footer)
#      settings.configure(TEMPLATE_CONTENT['meta']['title']=name+" - Club Management System (CMS)")
#      settings.configure(TEMPLATE_CONTENT['meta']['logo']['title']=name)
#      settings.configure(TEMPLATE_CONTENT['meta']['logo']['img']=logo)

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
    form = SetupForm()
    return TemplateResponse(r, form_template, {
                	'title'	: form_title,
                	'desc'	: form_desc,
                	'submit': form_submit,
                	'form'	: form,
                })


