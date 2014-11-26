import hashlib
from os import path

from django.conf import settings
from django.template.loader import render_to_string

from members.models import Member
from attendance.models import Event_Attendance
from members.functions import get_active_members

###############################
# EVENTS SUPPORTING FUNCTIONS #
###############################

def gen_event_overview(template,event):
  content = { 'overview' : settings.TEMPLATE_CONTENT['events']['list']['overview'] }

  content['title'] = event.title
  content['modify'] = '/events/modify/' + unicode(event.pk)
  content['when'] = event.when
  content['time'] = event.time
  content['location'] = event.location.name
  content['address'] = event.location.address
  content['attendance'] = Event_Attendance.objects.filter(event=event,present=True).only('member')
  content['excused'] = Event_Attendance.objects.filter(event=event,present=False).only('member')
  content['attachement'] = settings.MEDIA_URL+unicode(event.attachement)
  content['invitation_message'] = event.invitation.message
  content['sent'] = event.invitation.sent

  return render_to_string(template,content)

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
  initial_data['subscribed'] = Member.objects.filter(event_attendance__event=e,event_attendance__present=True)
  initial_data['excused'] = Member.objects.filter(event_attendance__event=e,event_attendance__present=False)

  return initial_data

