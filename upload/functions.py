#
# coding=utf-8
#
import datetime
import locale
from sys import stderr as errlog
from os import sep
from os.path import splitext
from re import search, findall

def import_data(ty,data):
  from members.models import Member
  from meetings.models import Meeting

  error = False
  for line in data:
    l = findall(r'\"(.+?)\"',str(line))

    Model = None
    try:
      if ty == "members": Model = Member.objects.get(first_name=l[0],last_name=l[1],email=l[2])
      if ty == "calendar": Model = Meeting.objects.get(title=l[0],when=l[1],time=l[2])
    except DoesNotExist:
      if ty == "members": 
	Model = Member (
			first_name    	= l[0],
			last_name	= l[1],
			email		= l[2]
		)
        # create user
        user = User.objects.create_user(gen_username(Model.first_name,Model.last_name), Model.email, make_password(gen_random_password()))
	Model.user = user
      if ty == "calendar": 
	Model = Meeting (
			title  		= l[0],
			when		= l[1],
			time		= l[2]
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
