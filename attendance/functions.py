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
  h.update(email.encode('utf-8')) #salt (email)
  if yes: h.update('YES'.encode('utf-8')) #second salt (YES)
  else: h.update('NO'.encode('utf-8')) #second salt (NO)
  h.update(str(event.pk).encode('utf-8') + str(event.when).encode('utf-8')) #message
  return h.hexdigest()

def gen_attendance_hashes(event,event_type,member):
  yes_hash = gen_hash(event,member.email)
  no_hash = gen_hash(event,member.email,False)
  if event_type == Event.MEET:
    mm = MtoM(meeting=event,member=member,yes_hash=yes_hash,no_hash=no_hash)
    mm.save()
  if event_type == Event.OTH:
    em = EtoM(event=event,member=member,yes_hash=yes_hash,no_hash=no_hash)
    em.save()

def get_attendance_hash(e,t,m,yes):
  if t == Event.MEET:
    mm = MtoM.objects.get(meeting=e,member=m)
    if yes: return mm.yes_hash
    else: return mm.no_hash
    
  if t == Event.OTH:
    em = EtoM.objects.get(event=e,member=m)
    if yes: return em.yes_hash
    else: return em.no_hash

def gen_attendance_links(event,event_type,member):
  attendance_url = ''

  if event_type == Event.MEET:
    attendance_url = path.join(settings.MEETINGS_ATTENDANCE_URL, unicode(event.pk))
    
  if event_type == Event.OTH:
    attendance_url = path.join(settings.EVENTS_ATTENDANCE_URL, unicode(event.pk))

  links = {
    'YES' : path.join(attendance_url, get_attendance_hash(event,event_type,member,True)),
    'NO'  : path.join(attendance_url, get_attendance_hash(event,event_type,member,False)),
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


