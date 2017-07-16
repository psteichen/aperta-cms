#
# coding=utf-8
#
import datetime
import locale
from sys import stderr as errlog
from os.path import splitext
from re import search, findall
import csv

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Permission

from cms.functions import debug

from members.functions import gen_username, gen_random_password
from members.models import Member
from meetings.models import Meeting
from events.models import Event
from locations.models import Location

def import_data(ty,data):
 
  nb=0
  ok = True
  errors = False
  for l in csv.DictReader(data.read().splitlines(),delimiter=';',quoting=csv.QUOTE_NONE):
#  for line in c_data:
#    l = findall(r'\"(.+?)\"',str(line))
#  for line in c_data:
#    l = findall(r'\"(.+?)\"',str(line))
    debug('upload','Line : '+unicode(l))

    Model = None
    if ty == 'members':  #import members
      try:
        Model = Member.objects.get(first_name=unicode(l['PRENOM']),last_name=unicode(l['NOM']),email=unicode(l['EMAIL']))
        debug('upload','Found member : '+unicode(Model))
      except Member.DoesNotExist:
	Model = Member (
			first_name    	= unicode(l['PRENOM']),
			last_name	= unicode(l['NOM']),
			address		= unicode(l['ADRESSE']),
			phone		= unicode(l['TEL']),
			mobile		= unicode(l['MOBILE']),
			email		= unicode(l['EMAIL'])
	)
        debug('upload','New member : '+unicode(Model))
        # create user
        U = User.objects.create_user(gen_username(Model.first_name,Model.last_name), Model.email, make_password(gen_random_password()))
        U.first_name = Model.first_name
        U.last_name = Model.last_name
        U.save()
        debug('upload','Created user : '+unicode(U))
        U.user_permissions.add(Permission.objects.get(codename='MEMBER'))
	Model.user = U
        Model.save()
        debug('upload','Saved member : '+unicode(Model))
        nb+=1

    if ty == 'calendar': #import calendar
      if l['TYPE'] == '0': #meeting
        debug('upload',"it's a meeting")
        try:
	  Model = Meeting.objects.get(when=unicode(l['DATE']),title=unicode(l['TITRE']))
          debug('upload','Found meeting : '+unicode(Model))
        except Meeting.DoesNotExist:
	  Model = Meeting (
			title  		= unicode(l['TITRE']),
			when		= unicode(l['DATE']),
			time		= unicode(l['HEURE']),
		)
          debug('upload','New meeting : '+unicode(Model))


      if l['TYPE'] == '1': #event
        debug('upload',"it's an event")
        try:
	  Model = Event.objects.get(when=unicode(l['DATE']),title=unicode(l['TITRE']))
          debug('upload','Found event : '+unicode(Model))
        except Event.DoesNotExist:
	  Model = Event (
			title  		= unicode(l['TITRE']),
			when		= unicode(l['DATE']),
		)
          debug('upload','New event : '+unicode(Model))

      # check/create location
      location = None
      try:
        location = Location.objects.get(name=l['LIEU'])
        debug('upload','Found location : '+unicode(location))
      except Location.DoesNotExist:
        location = Location (name=l['LIEU'])
        debug('upload','New location : '+unicode(location))

      Model.location = location
      Model.save()
      debug('upload','Saved meeting/event : '+unicode(Model))
      nb+=1
      if l['TYPE'] == '0':  #add num to meeting title
        Model.title = Model.num + u'. ' + Model.title
        Model.save()

  if not ok: return errors
  else: return nb
