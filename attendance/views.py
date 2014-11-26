#
# coding=utf-8
#
from datetime import date, datetime

from django.shortcuts import render
from django.conf import settings

from cms.functions import notify_by_email

from members.models import Member
from members.functions import get_active_members, gen_member_fullname

from meetings.models import Meeting
from events.models import Event

from .functions import gen_hash
from .models import Meeting_Attendance, Event_Attendance


####################
# ATTENDANCE VIEWS #
####################

# attendance #
##############
def attendance(r, event_type, event_id, attendance_hash):
  E = M = title = deadline = e_yes = e_no = message = None

  if event_type == 'meetings':
    M = Meeting.objects.get(num=event_id)
    deadline = M.deadline
    title = settings.TEMPLATE_CONTENT['attendance']['meeting']['title'] % { 'meeting': M.title, }
    e_yes = settings.TEMPLATE_CONTENT['attendance']['meeting']['email']['yes'] % { 'meeting': M.title, }
    e_no = settings.TEMPLATE_CONTENT['attendance']['meeting']['email']['no'] % { 'meeting': M.title, }
  if event_type == 'events':
    E = Event.objects.get(pk=event_id)
    deadline = E.deadline
    title = settings.TEMPLATE_CONTENT['attendance']['event']['title'] % { 'event': E.title, }
    e_yes = settings.TEMPLATE_CONTENT['attendance']['event']['email']['yes'] % { 'event': E.title, }
    e_no = settings.TEMPLATE_CONTENT['attendance']['event']['email']['no'] % { 'event': E.title, }

  if date.today() >= deadline:
    message = settings.TEMPLATE_CONTENT['attendance']['too_late']
  else:
    for m in get_active_members():
      notify = False
      e_message = None
      A = None
      if event_type == 'meetings':
        try:
          A = Meeting_Attendance.objects.get(meeting=M,member=m)
        except:
          A = Meeting_Attendance(meeting=M,member=m)

        if gen_hash(M,m.email) == attendance_hash:
          # it's a YES
          A.present = True
          A.timestamp = datetime.now()
          A.save()
          notify=True
          message = settings.TEMPLATE_CONTENT['attendance']['yes'] % { 'name': gen_member_fullname(m), }
          e_message = e_yes
  
        if gen_hash(M,m.email,False) == attendance_hash:
          # it's a NO
          A.present = False
          A.timestamp = datetime.now()
          A.save()
          notify=True
          message = settings.TEMPLATE_CONTENT['attendance']['no'] % { 'name': gen_member_fullname(m), }
          e_message = e_no

      if event_type == 'events':
        try:
          A = Event_Attendance.objects.get(event=E,member=m)
        except:
          A = Event_Attendance(event=E,member=m)

        if gen_hash(E,m.email) == attendance_hash:
          # it's a YES
          A.present = True
          A.timestamp = datetime.now()
          A.save()
          notify=True
          message = settings.TEMPLATE_CONTENT['attendance']['yes'] % { 'name': gen_member_fullname(m), }
          e_message = e_yes
  
        if gen_hash(E,m.email,False) == attendance_hash:
          # it's a NO
          A.present = False
          A.timestamp = datetime.now()
          A.save()
          notify=True
          message = settings.TEMPLATE_CONTENT['attendance']['no'] % { 'name': gen_member_fullname(m), }
          e_message = e_no
  
      if notify:
        #notify by email
        message_content = {
          'FULLNAME'	: gen_member_fullname(m),
          'MESSAGE'     : e_message,
        }
        #send email
        ok=notify_by_email(False,m.email,title,message_content)

  return render(r, settings.TEMPLATE_CONTENT['attendance']['template'], {
                   'title': title,
                   'message': message,
               })

