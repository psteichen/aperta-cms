#
# coding=utf-8
#
from datetime import date, timedelta, datetime

from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django_tables2  import RequestConfig

from cms.functions import notify_by_email, show_form

from members.functions import get_active_members, gen_member_fullname

from .functions import gen_order_hash, check_order_hash, gen_order_initial, gen_information_message
from .forms import OrderModelFormSet
from .models import Product, Packaging, Price, Order, Receipt
from .tables import ProductTable


# index #
#########
@permission_required('cms.BOARD',raise_exception=True)
def index(r):
  r.breadcrumbs( ( ('home','/'),
                   ('selling','/selling/'),
               ) )

  return render(r, settings.TEMPLATE_CONTENT['selling']['template'], {
                   'title': settings.TEMPLATE_CONTENT['selling']['title'],
                   'actions': settings.TEMPLATE_CONTENT['selling']['actions'],
               })


#################
# SELLING VIEWS #
#################

# add #
#######

#add formwizard
class AddProductWizard(SessionWizardView):

  file_storage = FileSystemStorage()

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(AddProductWizard, self).get_context_data(form=form, **kwargs)

    #add breadcrumbs to context
    self.request.breadcrumbs( ( ('home','/'),
                                ('selling','/selling/'),
                                ('add a product','/selling/add/'),
                            ) )

    if self.steps.current != None:
      context.update({'title': settings.TEMPLATE_CONTENT['selling']['add']['title']})
      context.update({'first': settings.TEMPLATE_CONTENT['selling']['add']['first']})
      context.update({'prev': settings.TEMPLATE_CONTENT['selling']['add']['prev']})
      context.update({'step_title': settings.TEMPLATE_CONTENT['selling']['add'][self.steps.current]['title']})
      context.update({'next': settings.TEMPLATE_CONTENT['selling']['add'][self.steps.current]['next']})

    return context

  def done(self, fl, form_dict, **kwargs):
    self.request.breadcrumbs( ( ('home','/'),
                                ('selling','/selling/'),
                                ('add a product','/selling/add/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['selling']['add']['done']['template']
    error_message = ''

    P = Pa = Pr = None
    pf = form_dict['product']
    paf = form_dict['packaging']
    pif = form_dict['price']
    errors = { 'ok': True, 'where': (), }

    if paf.is_valid():
      Pa = paf.save()
    else: 
      errors['ok'] = False
      errors['where'].add(paf)

    if pif.is_valid():
      Pi = pif.save()
    else: 
      errors['ok'] = False
      errors['where'].add(pif)

    if pf.is_valid():
      P = pf.save(commit=False)
      P.packaging = Pa
      P.price = Pi
      P.save()

      title = settings.TEMPLATE_CONTENT['selling']['add']['done']['title']

      # errors detected -> show error messages
      if not errors['ok']:
        return render(self.request, settings.TEMPLATE_CONTENT['selling']['add']['done']['template'], {
	                'title': title, 
        	        'error_message': settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in errors['where']]),
                      })

      # all fine -> done
      else:
        return render(self.request, settings.TEMPLATE_CONTENT['selling']['add']['done']['template'], {
	                'title': title, 
        	        'message': settings.TEMPLATE_CONTENT['selling']['add']['done']['message'] + P.title,
                      })


# notify #
##########
@permission_required('cms.BOARD',raise_exception=True)
def notify(r):
  r.breadcrumbs( ( ('home','/'),
                   ('selling','/selling/'),
                   ('notify members','/selling/notify/'),
               ) )

  template =  settings.TEMPLATE_CONTENT['selling']['notify']['template']
  title = settings.TEMPLATE_CONTENT['selling']['notify']['title']
  e_template =  settings.TEMPLATE_CONTENT['selling']['notify']['email']['template']
  subject = settings.TEMPLATE_CONTENT['selling']['notify']['email']['subject']
      
  email_error = { 'ok': True, 'who': [], }
  for m in get_active_members():
    #information email
    information_message = gen_information_message(e_template,m)
    message_content = {
      'FULLNAME'    : gen_member_fullname(m),
      'MESSAGE'     : information_message,
    }
    #notify email
    ok=notify_by_email(False,m.email,subject,message_content)
    if not ok: 
      email_error['ok']=False
      email_error['who'].append(m.email)

  message = settings.TEMPLATE_CONTENT['selling']['notify']['message'] % { 'message': information_message, 'recipients': ' ; '.join([gen_member_fullname(m) for m in get_active_members()]), }

  # error in email -> error message
  if not email_error['ok']:
    message += settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']])

  return render(r, template, {
	             'title': title, 
       		     'message': message
                })


# list #
#########
@permission_required('cms.BOARD',raise_exception=True)
def list(r, event_id):
  r.breadcrumbs( ( ('home','/'),
                   ('selling','/selling/'),
                   ('list event n. '+event_id,'/selling/list/'+event_id+'/'),
               ) )

  event = Event.objects.get(pk=event_id)
  title = settings.TEMPLATE_CONTENT['selling']['list']['title'] % { 'event' : event.title, }
  message = gen_event_overview(settings.TEMPLATE_CONTENT['selling']['list']['overview']['template'],event)

  return render(r, settings.TEMPLATE_CONTENT['selling']['list']['template'], {
                   'title': title,
                   'message': message,
                })

# list_all #
############
@permission_required('cms.BOARD',raise_exception=True)
def list_all(r):
  r.breadcrumbs( ( ('home','/'),
                   ('selling','/selling/'),
                   ('list products','/selling/list_all/'),
               ) )

  table = ProductTable(Product.objects.all())
  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return render(r, settings.TEMPLATE_CONTENT['selling']['list_all']['template'], {
                   'title': settings.TEMPLATE_CONTENT['selling']['list_all']['title'],
                   'desc': settings.TEMPLATE_CONTENT['selling']['list_all']['desc'],
                   'table': table,
                })


# modify #
##########

#modify helper functions
def show_attendance_form(wizard):
  return show_form(wizard,'event','attendance',True)

#modify formwizard
class ModifyEventWizard(SessionWizardView):

  file_storage = FileSystemStorage()

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(ModifyEventWizard, self).get_context_data(form=form, **kwargs)

    #add breadcrumbs to context
    self.request.breadcrumbs( ( ('home','/'),
                                ('selling','/selling/'),
                                ('modify an event','/selling/modify/'),
                            ) )

    if self.steps.current != None:
      title = ''
      event_id = self.kwargs['event_id']
      context.update({'title': settings.TEMPLATE_CONTENT['selling']['modify']['title']})
      context.update({'first': settings.TEMPLATE_CONTENT['selling']['modify']['first']})
      context.update({'prev': settings.TEMPLATE_CONTENT['selling']['modify']['prev']})
      context.update({'step_title': settings.TEMPLATE_CONTENT['selling']['modify'][self.steps.current]['title'] % { 'event': title,} })
      context.update({'next': settings.TEMPLATE_CONTENT['selling']['modify'][self.steps.current]['next']})

    return context

  def get_form(self, step=None, data=None, files=None):
    form = super(ModifyEventWizard, self).get_form(step, data, files)

    # determine the step if not given
    if step is None:
      step = self.steps.current

    event_id = self.kwargs['event_id']
    E = Event.objects.get(pk=event_id)

    if step == 'event':
      form.initial = gen_event_initial(E)
      form.instance = E

    if step == 'attendance':
      form.initial = gen_current_attendance(E)

    return form

  def done(self, fl, form_dict, **kwargs):
    self.request.breadcrumbs( ( ('home','/'),
                                ('selling','/selling/'),
                                ('modify an event','/selling/modify/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['selling']['modify']['done']['template']

    E = None
    ef = form_dict['event']
    if ef.is_valid():
      E = ef.save()

      attendance = ef.cleaned_data['attendance']
      if attendance == True: 
        af = form_dict['attendance']
        if af.is_valid() and af.has_changed():
          for s in af.cleaned_data['subscribed']:
            try:
              Event_Attendance(event=E,member=s,timestamp=datetime.now(),present=True).save()
            except:
              pass
          for e in af.cleaned_data['excused']:
            try:
              Event_Attendance(event=E,member=e,timestamp=datetime.now(),present=False).save()
            except:
              pass

    title = settings.TEMPLATE_CONTENT['selling']['modify']['done']['title'] % E

    return render(self.request, template, {
                        'title': title,
                 })


# order #
#########
def order(r, hash):
  r.breadcrumbs( ( ('home','/'),
                   ('selling','/selling/'),
                   ('order products','/selling/order/'),
               ) )

  if r.POST:
    e_template =  settings.TEMPLATE_CONTENT['selling']['order']['done']['email']['template']

    ofs = OrderModelFormSet(r.POST)
    if ofs.is_valid():
      order = ofs.save(commit=False)

      o_date = date.today().strftime(u'%Y-%m-%d %H:%M')
      total = 0
      for o in order:
        total += o.amount

      title = settings.TEMPLATE_CONTENT['selling']['order']['done']['title'] % { 'date': o_date }
      overview = ''

      member = None
      ch = check_order_hash(hash)
      if not ch['ok']:
        # error in hash
        return render(r, settings.TEMPLATE_CONTENT['selling']['order']['done']['template'], {
        	        	'error_message': settings.TEMPLATE_CONTENT['error']['hash'],
                     })
      else:
        member = ch['member']

      overview = gen_receipt_message(o_template,order,member)

      #send full order including receipt by email
      subject = settings.TEMPLATE_CONTENT['selling']['order']['done']['email']['subject'] % { 'date': o_date }

      e_receipt = gen_receipt_message(e_template,order,member)
      message_content = {
        'FULLNAME'    : gen_member_fullname(member),
        'MESSAGE'     : e_receipt,
      }
      #send email
      ok=notify_by_email(False,member.email,subject,message_content)
      if not ok: 
        # error in email -> show error messages
        return render(r, settings.TEMPLATE_CONTENT['selling']['order']['done']['template'], {
				'title': title, 
        	        	'error_message': settings.TEMPLATE_CONTENT['error']['email'],
                     })
      order.save()
      R = Receipt(member=member,date=o_date,order=order,total=total)
      # all fine -> done
      return render(r, settings.TEMPLATE_CONTENT['selling']['order']['done']['template'], {
			'title': title, 
        	        'message': overview,
		   })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['selling']['order']['done']['template'], {
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in ofs.errors]),
                })

  # no post yet -> empty form
  else:
    ch = check_order_hash(hash)
    if not ch['ok']:
      # error in hash
      return render(r, settings.TEMPLATE_CONTENT['selling']['order']['done']['template'], {
        	        	'error_message': settings.TEMPLATE_CONTENT['error']['hash'],
                   })

    formset = OrderModelFormSet(initial=gen_order_initial())
    return render(r, settings.TEMPLATE_CONTENT['selling']['order']['template'], {
                'title': settings.TEMPLATE_CONTENT['selling']['order']['title'],
                'desc': settings.TEMPLATE_CONTENT['selling']['order']['desc'],
                'submit': settings.TEMPLATE_CONTENT['selling']['order']['submit'],
                'formset': formset,
                })

