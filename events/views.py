
# coding=utf-8
#
from datetime import date, timedelta, datetime

from django.template.response import TemplateResponse
from django.conf import settings
from django.utils import timezone

from django_tables2  import RequestConfig
from formtools.wizard.views import SessionWizardView

from headcrumbs.decorators import crumb
from headcrumbs.util import name_from_pk
	
from cms.functions import notify_by_email, group_required

from members.models import Member
from members.functions import get_active_members, gen_member_fullname, is_board

from .functions import gen_event_overview, gen_event_initial, gen_reg_hash, gen_events_calendar
from .models import Event, Invitation, Distribution
from .forms import EventForm, ListEventsForm, RegistrationForm
from .tables  import EventTable, MgmtEventTable


################
# EVENTS VIEWS #
################

# calendar #
############
@group_required('MEMBER')
@crumb(u'Calendrier')
def calendar(r):

#  events = Event.objects.filter(when__gt=timezone.now())
  events = Event.objects.all()

  title = settings.TEMPLATE_CONTENT['events']['calendar']['title']
  message = gen_events_calendar(settings.TEMPLATE_CONTENT['events']['calendar']['overview'],events)

  return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['calendar']['template'], {
                   'title': title,
                   'message': message,
                })


# list #
########
@group_required('MEMBER')
@crumb(u'Évènements')
def list(r):

  table = EventTable(Event.objects.all().order_by('-id'))
  if is_board(r.user):
    table = MgmtEventTable(Event.objects.all().order_by('-id'))

  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['template'], {
                   'title': settings.TEMPLATE_CONTENT['events']['title'],
                   'actions': settings.TEMPLATE_CONTENT['events']['actions'],
                   'table': table,
                })



# add #
#######
@group_required('BOARD')
@crumb(u'Ajouter un évènement',parent=list)
def add(r):

  if r.POST:

    ef = EventForm(r.POST)
    if ef.is_valid():
      Ev = ef.save(commit=False)
      Ev.registration=gen_reg_hash(Ev)
      Ev.save()

      #invitation
      if r.FILES:
        I = Invitation(event=Ev,message=ef.cleaned_data['additional_message'],attachement=r.FILES['attachement'])
      else:
        I = Invitation(event=Ev,message=ef.cleaned_data['additional_message'])
      I.save()

      # distribution
      sel_partners = ef.cleaned_data['partners']
      invitees = ef.cleaned_data['others']
      D = Distribution(event=Ev)
      if sel_partners: D.partners=sel_partners
      if invitees: D.others=invitees
      D.save()

      # all fine -> done
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['add']['done']['template'], {
                	'title': settings.TEMPLATE_CONTENT['events']['add']['done']['title'], 
                	'message': settings.TEMPLATE_CONTENT['events']['add']['done']['message'].format(
													event		= Ev,
													message		= I.message,
													attachement	= I.attachement,
													partners	= sel_partners,
													invitees	= invitees), 
		   })

    # form not valid -> error
    else:
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['events']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in ef.errors]),
                })
  # no post yet -> empty form
  else:
    form = EventForm()
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['add']['template'], {
                	'title': settings.TEMPLATE_CONTENT['events']['add']['title'],
                	'desc': settings.TEMPLATE_CONTENT['events']['add']['desc'],
                	'submit': settings.TEMPLATE_CONTENT['events']['add']['submit'],
                	'form': form,
                })


# send #
########
def send_invitation(event,m,invitation):
  e_template =  settings.TEMPLATE_CONTENT['events']['send']['done']['email']['template']

  #invitation email with registration link
  subject = settings.TEMPLATE_CONTENT['events']['send']['done']['email']['subject'] % { 'title': str(event.title) }
  message_content = {
      'FULLNAME'    : gen_member_fullname(m),
      'MESSAGE'     : str(invitation.message),
  }

  #send email
  try:
    return notify_by_email(r.user.email,m.email,subject,message_content,False,settings.MEDIA_ROOT + unicode(invitation.attachement))
  except:
    return notify_by_email(r.user.email,m.email,subject,message_content)

@group_required('BOARD')
def send(r,event_id):

  Ev = Event.objects.get(id=event_id)
  I = Invitation.objects.get(event=Ev)

  title = settings.TEMPLATE_CONTENT['events']['send']['done']['title'] % str(Ev.title)
      
  email_error = { 'ok': True, 'who': (), }
  recipient_list = []
  for m in get_active_members():
   
    recipient_list.append(m.email)
    ok=send_invitation(Ev,m,I)
    if not ok:
      email_error['ok']=False
      email_error['who'].add(m.email)


  # error in email -> show error messages
  if not email_error['ok']:
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['send']['done']['template'], {
	                'title': title, 
        	        'error_message': settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']]),
                  })

  # all fine -> done
  else:
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['send']['done']['template'], {
	                'title': title, 
			'message': settings.TEMPLATE_CONTENT['events']['send']['done']['message'] % { 'email': I.message, 'attachement': I.attachement, 'list': ' ; '.join([e for e in recipient_list]), },
                  })
 

# register #
############
def register(r, event_hash):

  E = Event.objects.get(registration=event_hash)

  title         = settings.TEMPLATE_CONTENT['events']['register']['title'].format(E.title)
  header        = settings.TEMPLATE_CONTENT['events']['register']['header']
  submit        = settings.TEMPLATE_CONTENT['events']['register']['submit']

  e_subject     = settings.TEMPLATE_CONTENT['events']['register']['email']['subject']
  e_template    = settings.TEMPLATE_CONTENT['events']['register']['email']['template']

  done_title    = settings.TEMPLATE_CONTENT['events']['register']['done']['title'].format(E.title)

  if r.POST:
    rf = RegistrationForm(r.POST)
    if rf.is_valid():
      P = rf.save(commit=False)
      P.event = E
      P.regcode = gen_reg_code(E,P)
      try:
        P.save()
      except IntegrityError:
        #error duplicate registration
        return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['register']['done']['template'], {
                        'title'         : title,
                        'error_message' : settings.TEMPLATE_CONTENT['error']['duplicate'],
                     })

      e_message = gen_registration_message(e_template,E,P)

      #notify by email
      message_content = {
        'FULLNAME'    : P.first_name + ' ' + P.last_name.upper(),
        'MESSAGE'     : e_message,
      }
      #send email
      ok=notify_by_email(P.email,e_subject,message_content,False)
      if not ok:
        #error in sending email
        return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['register']['done']['template'], {
                        'title'         : title,
                        'error_message' : settings.TEMPLATE_CONTENT['error']['email'],
                     })

      #all fine done page
      done_message = gen_event_overview(settings.TEMPLATE_CONTENT['events']['register']['done']['overview'],E,P)
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['register']['done']['template'], {
                        'title'         : done_title,
                        'message'       : done_message,
                   })
    #error in form
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['register']['done']['template'], {
                        'title'         : title,
                        'error_message' : settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in rf.errors]),
                   })

  else: #empty form
    form = RegistrationForm()
    teaser_message = gen_event_overview(settings.TEMPLATE_CONTENT['events']['register']['teaser'],E)
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['register']['template'], {
                        'title'         : title,
                        'header'        : header,
                        'form'          : form,
                        'teaser'        : teaser_message,
                        'submit'        : submit,
                })




# details #
###########
@group_required('MEMBER')
@crumb(u"Détail d'un évènement",parent=list)
def details(r, event_id):

  event = Event.objects.get(pk=event_id)
  title = settings.TEMPLATE_CONTENT['events']['details']['title'] % { 'event' : event.title, }
  message = gen_event_overview(settings.TEMPLATE_CONTENT['events']['details']['overview'],event)

  return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['details']['template'], {
                   'title': title,
                   'message': message,
                })


# modify #
##########
@group_required('BOARD')
@crumb(u"Modifier un évènement",parent=list)
def modify(r, event_id):

  E = Event.objects.get(pk=event_id)

  if r.POST:

    ef = EventForm(r.POST,instance=E)
    if ef.is_valid():
      Ev = ef.save(commit=False)
      Ev.save()
      
      # all fine -> done
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['modify']['done']['template'], {
                	'title': settings.TEMPLATE_CONTENT['events']['modify']['done']['title'].format(event=str(Ev)), 
		   })

    # form not valid -> error
    else:
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['modify']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['events']['modify']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in ef.errors]),
                })

  # no post yet -> empty form
  else:
    form = EventForm()
    form.initial = gen_event_initial(E)
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['modify']['template'], {
                'title': settings.TEMPLATE_CONTENT['events']['modify']['title'],
                'desc': settings.TEMPLATE_CONTENT['events']['modify']['desc'],
                'submit': settings.TEMPLATE_CONTENT['events']['modify']['submit'],
                'form': form,
                })




