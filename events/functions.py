import hashlib
from os import path

from django.conf import settings
from django.template.loader import render_to_string

from cms.functions import visualiseDateTime

from attendance.models import Event_Attendance
from members.functions import get_active_members

from .models import Invitation, Participant

###############################
# EVENTS SUPPORTING FUNCTIONS #
###############################

def gen_events_calendar(overview,events):
  content = { 'overview' : overview }

  content['events'] = events

  return render_to_string(overview['template'],content)


def get_event_attendance(event):
  out=''
  for p in Participant.objects.filter(event=event):
    out += '''
''' + unicode(p)

  return out

def gen_event_overview(overview,event,p=False):
  content = { 'overview' : overview }

  content['title'] = event.title
  content['when'] = visualiseDateTime(event.when)
  content['time'] = visualiseDateTime(event.time)
  content['location'] = event.location
  content['agenda'] = event.agenda
  try:
    I = Invitation.objects.get(event=event)
    content['invitation'] = I.message
    if I.attachement: content['attachement'] = I.attachement
  except Invitation.DoesNotExist:
    pass
  content['attendance'] = get_event_attendance(event)
  content['registration'] = settings.EVENTS_REG_BASE_URL + event.registration
  if p: content['regcode'] = p.regcode

  return render_to_string(overview['template'],content)

def gen_event_initial(e):
  initial_data = {}
  initial_data['title'] = e.title
  initial_data['when'] = e.when
  initial_data['time'] = e.time
  initial_data['location'] = e.location
  initial_data['deadline'] = e.deadline

  return initial_data

def gen_current_attendance(e):

  initial_data = {}
  initial_data['subscribe'] = Event_Attendance.objects.filter(event=e,present=True).only('member')
  initial_data['excuse'] = Event_Attendance.objects.filter(event=e,present=False).only('member')

  return initial_data

def gen_reg_hash(event):
  #hash
  h = hashlib.md5()
  h.update(str(event.agenda).encode('utf-8')) #salt
  h.update(str(event.title).encode('utf-8') + str(event.when).encode('utf-8')) #message
  return str(h.hexdigest()[:10])

def gen_reg_code(e,p):
  #hash
  h = hashlib.md5()
  h.update(str(p.email).encode('utf-8')) #salt
  h.update(str(e.title).encode('utf-8') + str(e.when).encode('utf-8')) #message
  return str(h.hexdigest()[:15])

def gen_registration_message(template,event,participant):
  content = {}

  content['title'] = event.title
  content['when'] = event.when
  content['time'] = visualiseDateTime(event.time)
  content['location'] = event.location
  content['agenda'] = event.agenda
  content['code'] = participant.regcode

  return render_to_string(template,content)
