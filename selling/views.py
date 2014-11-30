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

from .functions import gen_hash
from .forms import MultiOrderModelFormSet
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


# send #
########
@permission_required('cms.BOARD',raise_exception=True)
def send(r):
  r.breadcrumbs( ( ('home','/'),
                   ('selling','/selling/'),
                   ('send event invitations','/selling/send/'),
               ) )

  if r.POST:
    e_template =  settings.TEMPLATE_CONTENT['selling']['send']['done']['email']['template']

    lef = ListEventsForm(r.POST)
    if lef.is_valid():
      Ev = lef.cleaned_data['selling']

      title = settings.TEMPLATE_CONTENT['selling']['send']['done']['title'] % unicode(Ev.title)
      
      email_error = { 'ok': True, 'who': (), }
      for m in get_active_members():
   
        #invitation email with "YES/NO button"
        subject = settings.TEMPLATE_CONTENT['selling']['send']['done']['email']['subject'] % { 'title': unicode(Ev.title) }
        invitation_message = gen_invitation_message(e_template,Ev,Event.OTH,m)
        message_content = {
          'FULLNAME'    : gen_member_fullname(m),
          'MESSAGE'     : invitation_message,
        }
        #send email
        ok=notify_by_email(r.user.email,m.email,subject,message_content)
        if not ok: 
          email_error['ok']=False
          email_error['who'].add(m.email)

      # error in email -> show error messages
      if not email_error['ok']:
        return render(r, settings.TEMPLATE_CONTENT['selling']['send']['done']['template'], {
	                'title': title, 
        	        'error_message': settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']]),
                      })

      # all fine -> done
      else:
        return render(r, settings.TEMPLATE_CONTENT['selling']['send']['done']['template'], {
	                'title': title, 
        	        'message': settings.TEMPLATE_CONTENT['selling']['send']['done']['message'] + ' ; '.join([gen_member_fullname(m) for m in get_active_members()]),
                      })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['selling']['send']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['selling']['send']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in lef.errors]),
                })
  # no post yet -> empty form
  else:
    form = ListEventsForm()
    return render(r, settings.TEMPLATE_CONTENT['selling']['send']['template'], {
                'title': settings.TEMPLATE_CONTENT['selling']['send']['title'],
                'desc': settings.TEMPLATE_CONTENT['selling']['send']['desc'],
                'submit': settings.TEMPLATE_CONTENT['selling']['send']['submit'],
                'form': form,
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

    ofs = MultiOrderModelFormSet(r.POST)
    if ofs.is_valid():
      order = ofs.save(commit=False)

      date = date.today().strftime(u'%Y-%m-%d à %H:%M')
      total = order.amount.all().count()

      title = settings.TEMPLATE_CONTENT['selling']['order']['done']['title'] % { 'date': date }

      for m in get_active_members():
        if gen_hash(m.email) == hash:
      
          overview = gen_receipt(o_template,order,m)

          #send full order including receipt by email
          subject = settings.TEMPLATE_CONTENT['selling']['order']['done']['email']['subject']
          e_receipt = gen_e_receipt(e_template,order,m)
          message_content = {
              'FULLNAME'    : gen_member_fullname(m),
              'MESSAGE'     : e_receipt,
          }
          #send email
          ok=notify_by_email(False,m.email,subject,message_content)
          if not ok: 
            # error in email -> show error messages
            return render(r, settings.TEMPLATE_CONTENT['selling']['order']['done']['template'], {
	                'title': title, 
        	        'error_message': settings.TEMPLATE_CONTENT['error']['email'],
                         })

          # all fine -> done
          else:
            try:
              order.save()
              R = Receipt(member=m,date=date,order=order,total=total)
	      return render(r, settings.TEMPLATE_CONTENT['selling']['send']['done']['template'], {
				'title': title, 
	        	        'message': overview,
			   })

            except:
              return render(r, settings.TEMPLATE_CONTENT['selling']['order']['done']['template'], {
	                	'title': title, 
        	        	'error_message': settings.TEMPLATE_CONTENT['error']['receipt'],
                           })
            
    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['selling']['order']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['selling']['order']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in ofs.errors]),
                })

  # no post yet -> empty form
  else:
    form = MultiOrderModelFormSet()
    return render(r, settings.TEMPLATE_CONTENT['selling']['order']['template'], {
                'title': settings.TEMPLATE_CONTENT['selling']['order']['title'],
                'desc': settings.TEMPLATE_CONTENT['selling']['order']['desc'],
                'submit': settings.TEMPLATE_CONTENT['selling']['order']['submit'],
                'form': form,
                })

