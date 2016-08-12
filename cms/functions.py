#
# coding=utf-8
#
import datetime
import locale
from sys import stderr as errlog
from os import sep
from os.path import splitext
from re import search, findall
from unicodedata import normalize

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


###############################
# GLOBAL SUPPORTING FUNCTIONS #
###############################
def debug(app,message):
  if settings.DEBUG:
    print >>errlog, 'DEBUG ['+unicode(app)+']: '+unicode(message)

def notify_by_email(sender,to,subject,message_content,cc=False,attachment=False,template='default.txt'):

  if not sender: sender = settings.EMAILS['sender']['default']
  email = EmailMessage(
                subject=subject,
                from_email=sender,
                to=[to]
          )
  message_content['FOOTER'] = settings.EMAILS['footer']
  email.body = render_to_string(template,message_content)
  if attachment: email.attach_file(attachment)
  if cc: email.cc=[cc]
  try:
    email.send()
    return True
  except:
    return False

def show_form(wiz,step,field,const):
  cleaned_data = wiz.get_cleaned_data_for_step(step) or {}
  d = cleaned_data.get(field) or 666
  return int(d) == const

def visualiseDecimal(decIn,currency=''):
  s = '{:,.12g}'.format(decIn)
  s = s.replace(',', ' ')
  s = s.replace('.', ',')
  if ',' in s:
    s = s.rstrip('0')
    s = s.rstrip(',')
  if not currency:
    return s
  elif currency != '' :
    s = s + ' ' + currency
  return s

def visualiseDateTime(dtIn):
  locale.setlocale(locale.LC_ALL, settings.LC_ALL)

  if type(dtIn) is datetime.date: return dtIn.strftime('%a le ') + dtIn.strftime('%d %b %Y').lstrip('0')
  if type(dtIn) is datetime.time: return dtIn.strftime('%Hh%M').lstrip('0')
  if type(dtIn) is datetime.datetime: return dtIn.strftime('%a le ') + dtIn.strftime('%d %b %Y').lstrip('0') + u' à ' + dtIn.strftime('%Hh%M').lstrip('0')


# rename uploaded files
def rmf(dir, old, new=None):
  orig_name, orig_ext = splitext(old)

  if new:
    fn=unicode(new).replace(' ','-') #remove whitespaces
  else:
    fn=unicode(orig_name).replace(' ','-') #remove whitespaces

  fn=unicode(fn).replace('.','') #remove dots
  fn=dir.upper() + sep + fn #add dir

  return {'name': normalize('NFKD', fn).encode('ascii','ignore'),'ext': orig_ext}


def import_data(ty,data):
  from members.models import Member
  from meetings.models import Meeting

  error = False
  for line in data:
    l = findall(r'\"(.+?)\"',str(line))

    Model = None
    try:
      if ty == "MEMBER": Model = Member.objects.get(first_name=l[0],last_name=l[1],email=l[2])
      if ty == "MEETING": Model = Meeting.objects.get(title=l[0],when=l[1],time=l[2])
    except DoesNotExist:
      if ty == "MEMBER": 
	Model = Member (
			first_name    	= l[0],
			last_name	= l[1],
			email		= l[2]
		)
        # create user
        user = User.objects.create_user(gen_username(Model.first_name,Model.last_name), Model.email, make_password(gen_random_password()))
	Model.user = user
      if ty == "MEETING": 
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
