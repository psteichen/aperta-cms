
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

from members.models import Member
from members.functions import get_active_members, gen_member_fullname
from attendance.functions import gen_invitation_message, gen_hash

from .functions import gen_event_overview, gen_event_initial, gen_current_attendance
from .models import Event, Invitation
from .forms import ListEventsForm
from .tables  import EventTable


# index #
#########
@permission_required('cms.COMM',raise_exception=True)
def index(r):
  r.breadcrumbs( ( ('home','/'),
                   ('events','/events/'),
               ) )

  return render(r, settings.TEMPLATE_CONTENT['events']['template'], {
                   'title': settings.TEMPLATE_CONTENT['events']['title'],
                   'actions': settings.TEMPLATE_CONTENT['events']['actions'],
               })


################
# EVENTS VIEWS #
################

# add #
#######

#add helper functions
def show_location_form(wizard):
  return show_form(wizard,'event','new_location',True)

#add formwizard
class AddEventWizard(SessionWizardView):

  file_storage = FileSystemStorage()

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(AddEventWizard, self).get_context_data(form=form, **kwargs)

    #add breadcrumbs to context
    self.request.breadcrumbs( ( ('home','/'),
                                ('events','/events/'),
                                ('add an event','/events/add/'),
                            ) )

    if self.steps.current != None:
      context.update({'title': settings.TEMPLATE_CONTENT['events']['add']['title']})
      context.update({'first': settings.TEMPLATE_CONTENT['events']['add']['first']})
      context.update({'prev': settings.TEMPLATE_CONTENT['events']['add']['prev']})
      context.update({'step_title': settings.TEMPLATE_CONTENT['events']['add'][self.steps.current]['title']})
      context.update({'next': settings.TEMPLATE_CONTENT['events']['add'][self.steps.current]['next']})

    return context

  def done(self, fl, form_dict, **kwargs):
    self.request.breadcrumbs( ( ('home','/'),
                                ('events','/events/'),
                                ('add an event','/events/add/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['events']['add']['done']['template']
    e_template =  settings.TEMPLATE_CONTENT['events']['add']['done']['email']['template']
    error_message = ''

    E = L = None
    ef = form_dict['event']
    location = ef.cleaned_data['new_location']
    if location: 
      lf = form_dict['location']
      if lf.is_valid():
        L = lf.save()

    if ef.is_valid():
      E = ef.save()

      I = Invitation(event=E,message=ef.cleaned_data['additional_message'])

      send = ef.cleaned_data['send']
      if send:
        email_error = { 'ok': True, 'who': (), }
        for m in get_active_members():
   
          #invitation email with "YES/NO button"
          subject = settings.TEMPLATE_CONTENT['events']['add']['done']['email']['subject'] % { 'title': unicode(E.title) }
          invitation_message = gen_invitation_message(e_template,E,Event.OTH,m) + ef.cleaned_data['additional_message']
          message_content = {
            'FULLNAME'    : gen_member_fullname(m),
            'MESSAGE'     : invitation_message,
          }
          #send email
          ok=notify_by_email(self.request.user.email,m.email,subject,message_content)
          if not ok: 
            email_error['ok']=False
            email_error['who'].add(m.email)

        # error in email
        if not email_error['ok']:
          I.sent = datetime.now()
          error_message = settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']]),

      I.save()

      title = settings.TEMPLATE_CONTENT['events']['add']['done']['title'] % unicode(E)
      invitation_message = gen_invitation_message(e_template,E,Event.OTH,Member(user=self.request.user)) + ef.cleaned_data['additional_message']
      message = settings.TEMPLATE_CONTENT['events']['add']['done']['message'] % { 'email': invitation_message, 'list': ' ; '.join([gen_member_fullname(m) for m in get_active_members()]), },

      return render(self.request, template, {
                        'title': title,
     		        'message': message,
                	'error_message': error_message,
                   })


# send #
########
@permission_required('cms.COMM',raise_exception=True)
def send(r):
  r.breadcrumbs( ( ('home','/'),
                   ('events','/events/'),
                   ('send event invitations','/events/send/'),
               ) )

  if r.POST:
    e_template =  settings.TEMPLATE_CONTENT['events']['send']['done']['email']['template']

    lef = ListEventsForm(r.POST)
    if lef.is_valid():
      Ev = lef.cleaned_data['events']

      title = settings.TEMPLATE_CONTENT['events']['send']['done']['title'] % unicode(Ev.title)
      
      email_error = { 'ok': True, 'who': (), }
      for m in get_active_members():
   
        #invitation email with "YES/NO button"
        subject = settings.TEMPLATE_CONTENT['events']['send']['done']['email']['subject'] % { 'title': unicode(Ev.title) }
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
        return render(r, settings.TEMPLATE_CONTENT['events']['send']['done']['template'], {
	                'title': title, 
        	        'error_message': settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']]),
                      })

      # all fine -> done
      else:
        return render(r, settings.TEMPLATE_CONTENT['events']['send']['done']['template'], {
	                'title': title, 
        	        'message': settings.TEMPLATE_CONTENT['events']['send']['done']['message'] + ' ; '.join([gen_member_fullname(m) for m in get_active_members()]),
                      })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['events']['send']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['events']['send']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in lef.errors]),
                })
  # no post yet -> empty form
  else:
    form = ListEventsForm()
    return render(r, settings.TEMPLATE_CONTENT['events']['send']['template'], {
                'title': settings.TEMPLATE_CONTENT['events']['send']['title'],
                'desc': settings.TEMPLATE_CONTENT['events']['send']['desc'],
                'submit': settings.TEMPLATE_CONTENT['events']['send']['submit'],
                'form': form,
                })
 

# list #
#########
@permission_required('cms.COMM',raise_exception=True)
def list(r, event_id):
  r.breadcrumbs( ( ('home','/'),
                   ('events','/events/'),
                   ('list event n. '+event_id,'/events/list/'+event_id+'/'),
               ) )

  event = Event.objects.get(pk=event_id)
  title = settings.TEMPLATE_CONTENT['events']['list']['title'] % { 'event' : event.title, }
  message = gen_event_overview(settings.TEMPLATE_CONTENT['events']['list']['overview']['template'],event)

  return render(r, settings.TEMPLATE_CONTENT['events']['list']['template'], {
                   'title': title,
                   'message': message,
                })

# list_all #
############
@permission_required('cms.COMM',raise_exception=True)
def list_all(r):
  r.breadcrumbs( ( ('home','/'),
                   ('events','/events/'),
                   ('list events','/events/list_all/'),
               ) )

  table = EventTable(Event.objects.all())
  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return render(r, settings.TEMPLATE_CONTENT['events']['list_all']['template'], {
                   'title': settings.TEMPLATE_CONTENT['events']['list_all']['title'],
                   'desc': settings.TEMPLATE_CONTENT['events']['list_all']['desc'],
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
                                ('events','/events/'),
                                ('modify an event','/events/modify/'),
                            ) )

    if self.steps.current != None:
      title = ''
      event_id = self.kwargs['event_id']
      context.update({'title': settings.TEMPLATE_CONTENT['events']['modify']['title']})
      context.update({'first': settings.TEMPLATE_CONTENT['events']['modify']['first']})
      context.update({'prev': settings.TEMPLATE_CONTENT['events']['modify']['prev']})
      context.update({'step_title': settings.TEMPLATE_CONTENT['events']['modify'][self.steps.current]['title'] % { 'event': title,} })
      context.update({'next': settings.TEMPLATE_CONTENT['events']['modify'][self.steps.current]['next']})

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
                                ('events','/events/'),
                                ('modify an event','/events/modify/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['events']['modify']['done']['template']

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

    title = settings.TEMPLATE_CONTENT['events']['modify']['done']['title'] % E

    return render(self.request, template, {
                        'title': title,
                 })


