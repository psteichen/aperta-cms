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
from members.models import Member, Address
from meetings.models import Meeting

def import_data(ty,data):
 
  error = False
  for l in csv.DictReader(data.read().splitlines(),delimiter=';',quoting=csv.QUOTE_NONE):
#  for line in c_data:
#    l = findall(r'\"(.+?)\"',str(line))
#  for line in c_data:
#    l = findall(r'\"(.+?)\"',str(line))

    Model = None
    try:
      if ty == "members": 
#	Model = Member.objects.get(first_name=l[1],last_name=l[0],email=l[6])
	Model = Member.objects.get(first_name=unicode(l['VIRNUMM']),last_name=unicode(l['NUMM']),email=unicode(l['EMAIL']))
      if ty == "calendar": Model = Meeting.objects.get(title=unicode(l[0]),when=unicode(l[1]),time=unicode(l[2]))
    except:
      if ty == "members": 
        A = Address (
		address		= unicode(l['ADRESS']),
		postal_code	= unicode(l['CP']),
		location	= unicode(l['DUERF']),
		country		= unicode(l['LAND'])
	)
	Model = Member (
			first_name    	= unicode(l['VIRNUMM']),
			last_name	= unicode(l['NUMM']),
			address		= A,
			email		= unicode(l['EMAIL'])
		)
        # create user
        U = User.objects.create_user(gen_username(Model.first_name,Model.last_name), Model.email, make_password(gen_random_password()))
        U.user_permissions.add(Permission.objects.get(codename='MEMBER'))
	Model.user = U
      if ty == "calendar": 
	Model = Meeting (
			title  		= unicode(l[0]),
			when		= unicode(l[1]),
			time		= unicode(l[2])
		)

        # check/create location
        location = None
	try:
          location = Location.objects.get(name=l[3])
        except Location.DoesNotExist:
          location = Location (name=l[3])

	Model.location = location

      Model.save()

  return error
