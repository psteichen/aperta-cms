# coding=utf-8
import hashlib
from os import path

from django.conf import settings
from django.template.loader import render_to_string

from cms.functions import visualiseDateTime

from attendance.models import Meeting_Attendance
from members.models import Member
from members.functions import get_active_members, gen_member_fullname, gen_member_fullname_n_role

from .models import Invitation, Invitee

#################################
# MEETINGS SUPPORTING FUNCTIONS #
#################################

def gen_meeting_listing(template,meeting):
  content = { 'content' : settings.TEMPLATE_CONTENT['meetings']['listing']['content'] }

  #get attendance / excused / invited
  present = Meeting_Attendance.objects.filter(meeting=meeting,present=True).only('member')
  excused = Meeting_Attendance.objects.filter(meeting=meeting,present=False).only('member')
  invited = Invitee.objects.filter(meeting=meeting)

  content['listing'] = {}
  #header row
  # name (role) / present / excuse / non-excuse / email
  content['listing']['header'] = [
    u'Nom (rôle)', u'présent', u'excusé', u'non excusé',
  ]

  #records table (alphabetical order on last_name)
  members = Member.objects.all().order_by('last_name')
  content['listing']['members'] = []
  ok = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i class="fa fa-check"></i>&nbsp;'
  nok = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i class="fa fa-times"></i>&nbsp;'
  for m in members:
    p = e = n = ''
    for x in present:
      if m.id == x.member.id: p=ok
    for y in excused:
      if m.id == y.member.id: e=ok
    if p == '' and e == '': n=nok
    
    content['listing']['members'].append([
      	gen_member_fullname_n_role(m), 
	p, 
	e, 
	n,
    ])

  #invitees table
  content['listing']['invitees'] = []
  for i in invited:
    content['listing']['invitees'].append([
      	i.first_name + ' ' + str.upper(i.last_name), 
    ])


  #resume table
  content['listing']['resume'] = []
  # presents / invités  / total
  P = present.count()
  M = members.all().count()
  E = excused.count()
  I = invited.count()
  N = M-P-E
  content['listing']['resume'].append([
  	u'Présents : &emsp;&emsp;' + str(P) + '/' + str(M) + '&emsp;&emsp;&emsp;' + str(int(round((float(P)/M)*100))) + '%',
  	u'Invités : &emsp;&emsp;' + str(I),
  	u'Total : &emsp;&emsp;' + str(P+I),
  ])
  # excusés  / non exc. /
  content['listing']['resume'].append([
  	u'Excusés : &emsp;&emsp;' + str(E) + '/' + str(M) + '&emsp;&emsp;&emsp;' + str(int(round((float(E)/M)*100))) + '%',
  	u'Non-excusés : &emsp;&emsp;' + str(N) + '/' + str(M) + '&emsp;&emsp;&emsp;' + str(int(round((float(N)/M)*100))) + '%',
  ])

  return render_to_string(template,content)


def gen_meeting_overview(template,meeting):
  content = { 'overview' : settings.TEMPLATE_CONTENT['meetings']['details']['overview'] }

  content['title'] = meeting.title
  content['modify'] = '/meetings/modify/' + str(meeting.num)
  content['when'] = visualiseDateTime(meeting.when)
  content['time'] = visualiseDateTime(meeting.time)
  content['location'] = meeting.location.name
  content['address'] = meeting.location.address
  if meeting.report:  content['report'] = settings.MEDIA_URL + str(meeting.report)
  try:   
    invitation = Invitation.objects.get(meeting=meeting)
    if invitation.attachement: content['attach'] = settings.MEDIA_URL + str(invitation.attachement)
  except: pass
  content['print'] =  '/meetings/print/' + str(meeting.num)
  content['listing'] = gen_meeting_listing(settings.TEMPLATE_CONTENT['meetings']['listing']['content']['template'],meeting)
  content['attendance'] = Meeting_Attendance.objects.filter(meeting=meeting,present=True).only('member')
  content['invitee'] = Invitee.objects.filter(meeting=meeting)
  content['excused'] = Meeting_Attendance.objects.filter(meeting=meeting,present=False).only('member')

  return render_to_string(template,content)

def gen_meeting_initial(m):
  initial_data = {}
  initial_data['title'] = m.title
  initial_data['when'] = m.when
  initial_data['time'] = m.time
  initial_data['location'] = m.location
  initial_data['deadline'] = m.deadline

  return initial_data

def gen_invitee_message(template,event,member):
  content = {}

  content['title'] = event.title
  content['member'] = gen_member_fullname(member)
  content['when'] = event.when
  content['time'] = event.time
  content['location'] = event.location
  content['address'] = event.location.address

  return render_to_string(template,content)


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


