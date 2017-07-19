#
# coding=utf-8
#
from datetime import date, timedelta, datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.utils import timezone

from django_tables2  import RequestConfig

from cms.functions import notify_by_email, show_form, visualiseDateTime

from members.models import Member

from .models import Payment, BankExtract, BalanceSheet
from .forms import BankExtractForm, BalanceSheetForm
from .tables  import BankExtractTable, BalanceSheetTable


#################
# FINANCE VIEWS #
#################

# list #
########
@permission_required('cms.BOARD',raise_exception=True)
def list(r):
  r.breadcrumbs( ( 
			('home','/'),
                  	('finance','/finance/'),
              ) )

  return render(r, settings.TEMPLATE_CONTENT['finance']['template'], { 'actions': settings.TEMPLATE_CONTENT['finance']['actions'], })


# balance #
###########
@permission_required('cms.MEMBER',raise_exception=True)
def balance(r):
  r.breadcrumbs( ( 
			('home','/'),
                   	('finance','/finance/'),
                   	('balance','/finance/balance/'),
               ) )

  table = BalanceSheetTable(BalanceSheet.objects.all().order_by('-year'))
  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return render(r, settings.TEMPLATE_CONTENT['finance']['balance']['template'], {
                   'title': settings.TEMPLATE_CONTENT['finance']['balance']['title'],
                   'desc': settings.TEMPLATE_CONTENT['finance']['balance']['desc'],
                   'actions': settings.TEMPLATE_CONTENT['finance']['balance']['actions'],
                   'table': table,
                })


# bank #
########
@permission_required('cms.BOARD',raise_exception=True)
def bank(r):
  r.breadcrumbs( ( 
			('home','/'),
                   	('finance','/finance/'),
                   	('bank','/finance/bank/'),
               ) )

  table = BankExtractTable(BankExtract.objects.all().order_by('-year').order_by('-num'))
  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return render(r, settings.TEMPLATE_CONTENT['finance']['bank']['template'], {
                   'title': settings.TEMPLATE_CONTENT['finance']['bank']['title'],
                   'desc': settings.TEMPLATE_CONTENT['finance']['bank']['desc'],
                   'actions': settings.TEMPLATE_CONTENT['finance']['bank']['actions'],
                   'table': table,
                })


# upload #
##########
@permission_required('cms.BOARD',raise_exception=True)
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

  r.breadcrumbs( ( 
			('home','/'),
                   	('finance','/finance/'),
                   	('upload '+name,'/finance/upload/'+ty+'/'),
               ) )

  form_template	= settings.TEMPLATE_CONTENT['finance']['upload']['template']
  form_title	= settings.TEMPLATE_CONTENT['finance']['upload']['title'].format(name=title)
  form_desc	= settings.TEMPLATE_CONTENT['finance']['upload']['desc']
  form_submit	= settings.TEMPLATE_CONTENT['finance']['upload']['submit']

  done_template	= settings.TEMPLATE_CONTENT['finance']['upload']['done']['template']
  done_url	= settings.TEMPLATE_CONTENT['finance']['upload']['done']['url'].fomrat(type=ty)

  if r.POST:
    f = form(r.POST,r.FILES)
    if f.is_valid():
      F = f.save(commit=False)
      F.save()
      
      # all fine -> done
      return redirect(done_url)

    # form not valid -> error
    else:
      return render(r, done_template, {
                	'title'		: done_title, 
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in f.errors]),
                   })
  # no post yet -> empty form
  else:
    return render(r, form_template, {
                	'title'	: form_title,
                	'desc'	: form_desc,
                	'submit': form_submit,
                	'form'	: form,
                })


