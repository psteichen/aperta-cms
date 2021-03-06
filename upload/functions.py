#
# coding=utf-8
#
import locale
from datetime import datetime, timedelta
from sys import stderr as errlog
from os.path import splitext
from re import search, findall
import csv

from django.utils import timezone

from cms.functions import debug

from members.functions import gen_username, gen_random_password, create_user
from members.models import Member
from meetings.models import Meeting
from events.models import Event
from locations.models import Location


def UnicodeDictReader(utf8_data, **kwargs):
  csv_reader = csv.DictReader(utf8_data, **kwargs)
  for row in csv_reader:
    yield {str(key, 'utf-8'):str(value, 'utf-8') for key, value in row.iteritems()}

def import_data(ty,data):
 
  nb=0
  ok = True
  errors = False
  for l in UnicodeDictReader(data,delimiter=';',quoting=csv.QUOTE_NONE):
    debug('upload',u'Line : '+str(l))

    Model = None
    if ty == 'members':  #import members
      try:
        Model = Member.objects.get(first_name=str(l['PRENOM']),last_name=str(l['NOM']),email=str(l['EMAIL']))
      except Member.DoesNotExist:
        Model = Member(
		first_name    = str(l['PRENOM']),
		last_name	= str(l['NOM']),
		address	= str(l['ADRESSE']),
		phone		= str(l['TEL']),
		mobile	= str(l['MOBILE']),
		email		= str(l['EMAIL'])
	)
        # create user
        U = create_user(Model.first_name,Model.last_name, Model.email)
        Model.user = U
        Model.save()
        nb+=1

    if ty == 'calendar': #import calendar
      deadline = timezone.make_aware(datetime.strptime(l['DATE'] + ' ' + l['HEURE'],"%Y-%m-%d %H:%M")-timedelta(hours=24),None)
      if l['TYPE'] == '0': #meeting
        debug('upload',u"it's a meeting")
        try:
          Model = Meeting.objects.get(when=str(l['DATE']),title=str(l['TITRE']))
        except Meeting.DoesNotExist:
          Model = Meeting(
		title  		= str(l['TITRE']),
		when		= str(l['DATE']),
		time		= str(l['HEURE']),
		deadline	= deadline,
	  )

      if l['TYPE'] == '1': #event
        debug('upload',u"it's an event")
        try:
          Model = Event.objects.get(when=str(l['DATE']),title=str(l['TITRE']))
        except Event.DoesNotExist:
          Model = Event (
		title  		= str(l['TITRE']),
		when		= str(l['DATE']),
		time		= str(l['HEURE']),
		deadline	= deadline,
	  )

      # check/create location
      location = None
      try:
        location = Location.objects.get(name=str(l['LIEU']))
      except Location.DoesNotExist:
        location = Location(name=str(l['LIEU']))
        location.save()

      Model.location = location
      if l['TYPE'] == '0':  #add num to meeting title
        latest = Meeting.objects.values().latest('num')
        next_num = latest['num'] + 1
        Model.num = next_num
        Model.title = str(next_num) + u'. ' + str(Model.title)
      Model.save()
      nb+=1

  if not ok: return errors
  else: return nb
