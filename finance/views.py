#
# coding=utf-8
#
from datetime import date, timedelta, datetime

from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.conf import settings
from django.utils import timezone

from django_tables2  import RequestConfig
from headcrumbs.decorators import crumb
from headcrumbs.util import name_from_pk

from cms.functions import notify_by_email, show_form, visualiseDateTime, group_required

from members.models import Member

from .models import Payment, BankExtract, BalanceSheet
from .forms import BankExtractForm, BalanceSheetForm
from .tables  import BankExtractTable, BalanceSheetTable


#################
# FINANCE VIEWS #
#################

# list #
########
@group_required('BOARD')
@crumb(u'Trésorerie')
def list(r):
  return TemplateResponse(r, settings.TEMPLATE_CONTENT['finance']['template'], { 'actions': settings.TEMPLATE_CONTENT['finance']['actions'], })


# balance #
###########
@group_required('MEMBER')
@crumb(u'Balance',parent=list)
def balance(r):
  table = BalanceSheetTable(BalanceSheet.objects.all().order_by('-year'))
  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return TemplateResponse(r, settings.TEMPLATE_CONTENT['finance']['balance']['template'], {
                   'title': settings.TEMPLATE_CONTENT['finance']['balance']['title'],
                   'desc': settings.TEMPLATE_CONTENT['finance']['balance']['desc'],
                   'actions': settings.TEMPLATE_CONTENT['finance']['balance']['actions'],
                   'table': table,
                })

# bank #
########
@group_required('BOARD')
@crumb(u'Bank',parent=list)
def bank(r):

  table = BankExtractTable(BankExtract.objects.all().order_by('-year').order_by('-num'))
  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return TemplateResponse(r, settings.TEMPLATE_CONTENT['finance']['bank']['template'], {
                   'title': settings.TEMPLATE_CONTENT['finance']['bank']['title'],
                   'desc': settings.TEMPLATE_CONTENT['finance']['bank']['desc'],
                   'actions': settings.TEMPLATE_CONTENT['finance']['bank']['actions'],
                   'table': table,
                })

# upload #
##########
@group_required('BOARD')
@crumb(u'Upload',parent=list)
def upload(r,ty):

  name = ''
  if ty == 'bank':
    name = 'bank extract'
    title = u'un extrait bancaire'
    form = BankExtractForm()
  if ty == 'balance':
    name = 'balance sheet'
    title = u'les comptes annuels'
    form = BalanceSheetForm()

  form_template       	= settings.TEMPLATE_CONTENT['finance']['upload']['template']
  form_title  		= settings.TEMPLATE_CONTENT['finance']['upload']['title'].format(name=title)
  form_desc   		= settings.TEMPLATE_CONTENT['finance']['upload']['desc']
  form_submit 		= settings.TEMPLATE_CONTENT['finance']['upload']['submit']

  done_template		= settings.TEMPLATE_CONTENT['finance']['upload']['done']['template']
  done_url		= settings.TEMPLATE_CONTENT['finance']['upload']['done']['url']

  if r.POST:
    f = form(r.POST,r.FILES)
    if f.is_valid():
      F = f.save(commit=False)
      F.save()
      
      # all fine -> done
      return redirect(done_url)

    # form not valid -> error
    else:
      return TemplateResponse(r, done_template, {
                	'title'		: done_title, 
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in bef.errors]),
                   })
  # no post yet -> empty form
  else:
    return TemplateResponse(r, form_template, {
                	'title'	: form_title,
                	'desc'	: form_desc,
                	'submit': form_submit,
                	'form'	: form,
                })


