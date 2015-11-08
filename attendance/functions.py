# coding = utf-8

import hashlib
from os import path

from django.conf import settings
from django.template.loader import render_to_string

from .models import MtoM, EtoM
from members.functions import get_active_members
from events.models import Event

###################################
# ATTENDANCE SUPPORTING FUNCTIONS #
###################################

def gen_hash(event,email,yes=True):
  #hash
  h = hashlib.md5()
  h.update(unicode(email)) #salt (email)
  if yes: h.update('YES') #second salt (YES)
  else: h.update('NO') #second salt (NO)
  h.update(unicode(event.pk) + unicode(event.when)) #message
  return unicode(h.hexdigest())

def gen_attendance_links(event,event_type,member):
  attendance_url = ''
  yes_hash = gen_hash(event,member.email)
  no_hash = gen_hash(event,member.email,False)

  if event_type == Event.MEET:
    attendance_url = path.join(settings.MEETINGS_ATTENDANCE_URL, unicode(event.pk))
    mm = MtoM(meeting=event,member=member,yes_hash=yes_hash,no_hash=no_hash)
    mm.save()
    
  if event_type == Event.OTH:
    attendance_url = path.join(settings.EVENTS_ATTENDANCE_URL, unicode(event.pk))
    em = EtoM(event=event,member=member,yes_hash=yes_hash,no_hash=no_hash)
    em.save()

  links = {
    'YES' : path.join(attendance_url, yes_hash),
    'NO'  : path.join(attendance_url, no_hash),
  }

  return links

def gen_invitation_message(template,event,event_type,member):
  content = {}

  content['title'] = event.title
  content['when'] = event.when
  content['time'] = event.time
  content['location'] = event.location
  content['deadline'] = event.deadline
  content['attendance'] = gen_attendance_links(event,event_type,member)

  return render_to_string(template,content)


