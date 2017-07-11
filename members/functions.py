
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Member, Role

def get_active_members():
  return Member.objects.filter(Q(status=Member.ACT)|Q(status=Member.WBE)).order_by('last_name')

def gen_member_fullname(member):
  return unicode(member.first_name) + u' ' + unicode.upper(member.last_name)

def gen_member_fullname_n_role(member):
  role = ''
  try:
    role = ' (' + unicode(Role.objects.get(member=member).title) + ')'
  except: pass
  return unicode(member.first_name) + u' ' + unicode.upper(member.last_name) + role

def gen_member_initial(m):
  initial_data = {}

  initial_data['first_name'] = m.first_name
  initial_data['last_name'] = m.last_name
  initial_data['email'] = m.email
  initial_data['address'] = m.address
  initial_data['prefix'] = m.prefix
  initial_data['phone'] = m.phone
  initial_data['mobile'] = m.mobile
  initial_data['start_date'] = m.start_date
  initial_data['end_date'] = m.end_date
  initial_data['status'] = m.status
  try:
    role = Role.objects.get(member__pk=m.pk)
    if role.end_date:
      initial_data['role'] = unicode(role.title) + ' (' + unicode(role.start_date) + ' - ' + unicode(role.end_date) +')'
    else:
      initial_data['role'] = unicode(role.title) + ' (depuis ' + unicode(role.start_date) + ')'
  except:
    initial_data['role'] = ''

  return initial_data

def gen_role_initial(r):
  initial_data = {}

  initial_data['type'] = r.type
  initial_data['year'] = r.year
  initial_data['member'] = r.member

  return initial_data

def gen_member_overview(template,member):
  content = { 'overview' : settings.TEMPLATE_CONTENT['members']['profile']['overview'] }

  content['photo'] 	= settings.MEDIA_URL + member.photo.name
  content['name'] 	= gen_member_fullname(member)
  content['username'] 	= member.user.username
  content['address'] 	= member.address
  content['phone'] 	= member.phone
  content['mobile'] 	= member.mobile
  content['email'] 	= member.email
  try:
    role = Role.objects.get(member=member)
    if role.end_date:
      content['role'] = unicode(role.title) + ' (' + unicode(role.start_date) + ' - ' + unicode(role.end_date) +')'
    else:
      content['role'] = unicode(role.title) + ' (depuis ' + unicode(role.start_date) + ')'
  except: pass

  return render_to_string(template,content)

def login_exists(username):
  try:
    User.objects.get(username=username)
    return  True
  except User.DoesNotExist:
    return False

def gen_username(fn, ln, pad=0):
  username = ''
  i=0
  j=1
  while i<=pad:
    try:
      username += fn[i]
    except:
      username += unicode(j)
      j += 1

    i += 1
  username = unicode.lower(username + ln)
  if login_exists(username): return gen_username(fn, ln, pad+1)
  else: return username

def gen_random_password():
  return User.objects.make_random_password(length=10)
