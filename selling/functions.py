# coding = utf-8

import hashlib
from os import path

from django.conf import settings
from django.template.loader import render_to_string

from members.functions import get_active_members
from events.models import Event

################################
# SELLING SUPPORTING FUNCTIONS #
################################

def gen_hash(email):
  #hash
  h = hashlib.md5()
  h.update(unicode(email)) #salt (email)
  if yes: h.update('YES') #second salt (YES)
  else: h.update('NO') #second salt (NO)
  h.update(unicode(event.pk) + unicode(event.when)) #message
  return unicode(h.hexdigest())

def gen_attendance_links(event,event_type,email):
  attendance_url = ''
  if event_type == Event.MEET:
    attendance_url = path.join(settings.MEETINGS_ATTENDANCE_URL, unicode(event.pk))
  if event_type == Event.OTH:
    attendance_url = path.join(settings.EVENTS_ATTENDANCE_URL, unicode(event.pk))

  links = {
    'YES' : path.join(attendance_url, gen_hash(event,email)),
    'NO'  : path.join(attendance_url, gen_hash(event,email,False)),
  }

  return links

def gen_invitation_message(template,event,event_type,invitee,sponsor=False):
  content = {}

  if sponsor: content['sponsor'] = gen_member_fullname(sponsor)

  content['title'] = event.title
  content['when'] = event.when
  content['time'] = event.time
  content['location'] = event.location
  content['deadline'] = event.deadline
  content['attendance'] = gen_attendance_links(event,event_type,invitee.email)

  return render_to_string(template,content)


