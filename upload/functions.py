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

from members.functions import gen_username, gen_random_password
from members.models import Member
from meetings.models import Meeting

def import_data(ty,data):
 
  nb=0
  ok = True
  errors = False
  for l in csv.DictReader(data.read().splitlines(),delimiter=';',quoting=csv.QUOTE_NONE):
#  for line in c_data:
#    l = findall(r'\"(.+?)\"',str(line))
#  for line in c_data:
#    l = findall(r'\"(.+?)\"',str(line))

    Model = None
    try:
      if ty == "members": 
	Model = Member.objects.get(first_name=unicode(l['PRENOM']),last_name=unicode(l['NOM']),email=unicode(l['EMAIL']))
      if ty == "calendar": 
	Model = Meeting.objects.get(when=unicode(l['DATE']),title=unicode(l['TITRE']))
    except:
      if ty == "members": 
	Model = Member (
			first_name    	= unicode(l['PRENOM']),
			last_name	= unicode(l['NOM']),
			address		= unicode(l['ADRESSE']),
			phone		= unicode(l['TEL']),
			mobile		= unicode(l['MOBILE']),
			email		= unicode(l['EMAIL'])
	)
        # create user
        U = User.objects.create_user(gen_username(Model.first_name,Model.last_name), Model.email, make_password(gen_random_password()))
        U.first_name = Model.first_name
        U.last_name = Model.last_name
        U.save()
        U.user_permissions.add(Permission.objects.get(codename='MEMBER'))
	Model.user = U
      if ty == "calendar": 
	Model = Meeting (
			title  		= unicode(l['TITRE']),
			when		= unicode(l['DATE']),
		)

        # check/create location
        location = None
	try:
          location = Location.objects.get(name=l[3])
        except Location.DoesNotExist:
          location = Location (name=l[3])

	Model.location = location

      Model.save()
      nb+=1

  if not ok: return errors
  else: return nb
