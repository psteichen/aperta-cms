import hashlib
from os import path

from django.conf import settings
from django.template.loader import render_to_string

from cms.functions import visualiseDateTime

from .models import Invitation

from attendance.models import Meeting_Attendance
from members.models import Member
from members.functions import get_active_members

################################
# MEETINGS SUPPORTING FUNCTIONS #
################################

def gen_meeting_overview(template,meeting):
  content = { 'overview' : settings.TEMPLATE_CONTENT['meetings']['details']['overview'] }

  content['title'] = meeting.title
  content['modify'] = '/meetings/modify/' + unicode(meeting.num)
  content['when'] = visualiseDateTime(meeting.when)
  content['time'] = visualiseDateTime(meeting.time)
  content['location'] = meeting.location.name
  content['address'] = meeting.location.address
  if meeting.report:  content['report'] = settings.MEDIA_URL + unicode(meeting.report)
  invitation = Invitation.objects.get(meeting=meeting)
  if invitation.attachement:  content['attach'] = settings.MEDIA_URL + unicode(invitation.attachement)
  content['attendance'] = Meeting_Attendance.objects.filter(meeting=meeting,present=True).only('member')
  content['excused'] = Meeting_Attendance.objects.filter(meeting=meeting,present=False).only('member')

  return render_to_string(template,content)

def gen_meeting_initial(m):
  initial_data = {}
  initial_data['title'] = m.title
  initial_data['when'] = m.when
  initial_data['time'] = m.time
  initial_data['location'] = m.location

  return initial_data

def gen_current_attendance(m):

  initial_data = {}
  initial_data['subscribed'] = Member.objects.filter(meeting_attendance__meeting=m,meeting_attendance__present=True)
  initial_data['excused'] = Member.objects.filter(meeting_attendance__meeting=m,meeting_attendance__present=False)

  return initial_data

def gen_report_message(template,meeting,member):
  content = {}

  content['title'] = meeting.title
  content['when'] = meeting.when
  content['time'] = meeting.time
  content['location'] = meeting.location

  return render_to_string(template,content)

