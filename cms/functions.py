#
# coding=utf-8
#
from datetime import date, datetime, time, timedelta
from os import sep
from os.path import splitext
from unicodedata import normalize

from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils import timezone

###############################
# GLOBAL SUPPORTING FUNCTIONS #
###############################
def debug(app,message):
  if settings.DEBUG:
    from sys import stderr as errlog
    print >>errlog, 'DEBUG ['+str(app)+']: '+str(message)


def check_if_setup():
  from django.contrib.sites.models import Site

  sid = settings.SITE_ID
  S = Site.objects.get(pk=sid)
  if S.domain in settings.ALLOWED_HOSTS: return True
  return False

def group_required(*group_names):

  """Requires user membership in at least one of the groups passed in."""
  def in_groups(user):
    if user.is_authenticated():
      if bool(user.groups.filter(name__in=group_names)) or user.is_superuser:
        return True
      else:
        raise PermissionDenied

  return user_passes_test(in_groups)

def attach_to_email(email,attachment):
  from os import path
  from django.core.files.storage import default_storage
  from django.core.files.base import ContentFile

  try: email.attach(attachment)
  except:
    try: email.attach_file(attachment)
    except:
      tmp_file = default_storage.save(path.join(settings.MEDIA_ROOT, 'tmp', attachment.name), ContentFile(attachment.read()))
      email.attach_file(tmp_file)
      tmp_file = default_storage.delete(path.join(settings.MEDIA_ROOT, 'tmp', attachment.name))

def notify_by_email(sender,to,subject,message_content,cc=False,attachment=False,template='default.txt'):
  from django.core.mail import EmailMessage
  from django.core.mail import EmailMultiAlternatives
  is_array = lambda var: isinstance(var, (list, tuple))

  if not sender: sender = settings.EMAILS['sender']['default']
  email = EmailMultiAlternatives(
                subject=settings.EMAILS['tag'] + " " + subject,
                from_email=sender,
                to=[to]
          )
#  email.esp_extra = {"sender_domain": settings.EMAIL_SENDER_DOMAIN}
  if template:
    message_content['FOOTER'] = settings.EMAILS['footer']
    email.body = render_to_string(template,message_content)
  else: email.body = str(message_content)
  if attachment:
    if is_array(attachment):
      for a in attachment: attach_to_email(email,a)
    else: attach_to_email(email,attachment)
  if cc: email.cc=[cc]

  try:
    email.send()
    return True
  except:
    return False

def genIcal(event):
  from icalendar import Calendar, Event, Alarm

  #get details from event instance
  title         = event.title
  desc          = event.title
  duration    = 3
  start         = datetime.combine(event.when, event.time)
  end           = datetime.combine(event.when, event.time) + timedelta(hours=duration)
  location      = event.location

  # Timezone to use for our dates - change as needed
  reminderHours = 3

  cal = Calendar()
  cal.add('prodid', '-//APERTA calendar application//aperta.lu//')
  cal.add('version', '2.0')
  cal.add('method', "REQUEST")

  vevent = Event()
#  event.add('attendee', self.getEmail())
  vevent.add('organizer', settings.EMAILS['sender']['default'])
  vevent.add('status', "confirmed")
  vevent.add('category', "Event")
  vevent.add('summary', title)
  vevent.add('description', desc)
  vevent.add('location', location)
  vevent.add('dtstart', start)
  vevent.add('dtend', end)
  from attendance.functions import gen_hash
  vevent['uid'] = gen_hash(event,settings.EMAILS['sender']['default'])[:10] # Generate some unique ID
  vevent.add('priority', 5)
  vevent.add('sequence', 1)
  vevent.add('created', timezone.now())

  alarm = Alarm()
  alarm.add("action", "DISPLAY")
  alarm.add('description', "Reminder")
  alarm.add("trigger", timedelta(hours=-reminderHours))
  # The only way to convince Outlook to do it correctly
  alarm.add("TRIGGER;RELATED=START", "-PT{0}H".format(reminderHours))
  vevent.add_component(alarm)
  cal.add_component(vevent)

  #gen file to be attached to an email
  from email import MIMEBase, Encoders

  filename = "invite.ics"
  invite = MIMEBase.MIMEBase('text', "calendar", method="REQUEST", name=filename)
  invite.set_payload( cal.to_ical() )
  Encoders.encode_base64(invite)
  invite.add_header('Content-Description', desc)
  invite.add_header("Content-class", "urn:content-classes:calendarmessage")
  invite.add_header("Filename", filename)
  invite.add_header("Path", filename)

  return invite

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
  import locale
  locale.setlocale(locale.LC_ALL, settings.LC_ALL)

  if type(dtIn) is date: return dtIn.strftime('%a le ') + dtIn.strftime('%d %b %Y').lstrip('0')
  if type(dtIn) is time: return dtIn.strftime('%Hh%M').lstrip('0')
  if type(dtIn) is datetime: return dtIn.strftime('%a le ') + dtIn.strftime('%d %b %Y').lstrip('0') + u' à ' + dtIn.strftime('%Hh%M').lstrip('0')

def getSaison():
  if int(date.today().strftime('%M')) < 8: # we are after August -> new season started
    y1 = str(int(date.today().strftime('%Y')) - 1)
  else:
    y1 = date.today().strftime('%Y')
  
  y2 = (datetime.strptime(y1,'%Y') + timedelta(days=+365)).strftime('%Y')

  return y1 + u'-' + y2

# rename uploaded files
def rmf(dir, old, new=None):
  orig_name, orig_ext = splitext(old)

  if new:
    fn=str(new).replace(' ','-') #remove whitespaces
  else:
    fn=str(orig_name).replace(' ','-') #remove whitespaces

  fn=str(fn).replace('.','') #remove dots
  fn=dir.upper() + sep + fn #add dir

  return {'name': normalize('NFKD', fn).encode('ascii','ignore'),'ext': orig_ext}

