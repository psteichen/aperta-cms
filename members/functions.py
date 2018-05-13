
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

from attendance.models import Meeting_Attendance

from .models import Member, Role


def gen_username(fn, ln, pad=0):
  username = ''
  i=0
  j=1
  while i<=pad:
    try:
      username += fn[i]
    except:
      username += str(j)
      j += 1

    i += 1
  username = str.lower(username + ln)
  if login_exists(username): return gen_username(fn, ln, pad+1)
  else: return username

def gen_random_password():
  return User.objects.make_random_password(length=10)

def create_user(first_name,last_name,email):
  # create user
  U = User.objects.create_user(gen_username(first_name,last_name), email, make_password(gen_random_password()))
  U.first_name = first_name
  U.last_name = last_name
  U.save()
  U.groups.add(Group.objects.get(name='MEMBER'))

  return U

def is_board(user):
  if user.is_superuser: return True

  for g in user.groups.all():
    if g.name == 'BOARD': return True

  return False

def is_member(user):
  if user.is_superuser: return True

  for g in user.groups.all():
    if g.name == 'MEMBER': return True

  return False


def get_active_members():
  return Member.objects.filter(Q(status=Member.ACT)|Q(status=Member.WBE)|Q(status=Member.HON)).order_by('last_name')

def gen_member_fullname(member):
  return str(member.first_name) + u' ' + str.upper(member.last_name)

def gen_member_fullname_n_role(member):
  role = ''
  try:
    role = ' (' + str(Role.objects.get(member=member).title) + ')'
  except: pass
  return str(member.first_name) + u' ' + str.upper(member.last_name) + role

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
      initial_data['role'] = str(role.title) + ' (' + str(role.start_date) + ' - ' + str(role.end_date) +')'
    else:
      initial_data['role'] = str(role.title) + ' (depuis ' + str(role.start_date) + ')'
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
      content['role'] = str(role.title) + ' (' + str(role.start_date) + ' - ' + str(role.end_date) +')'
    else:
      content['role'] = str(role.title) + ' (depuis ' + str(role.start_date) + ')'
  except: pass

  return render_to_string(template,content)

def login_exists(username):
  try:
    User.objects.get(username=username)
    return  True
  except User.DoesNotExist:
    return False


def get_meeting_missing_active_members(meeting):
  members = ()
  for m in get_active_members():
    try:
      Meeting_Attendance.objects.get(meeting=meeting,member=m)
    except Meeting_Attendance.DoesNotExist:
      members.add(m)

  return members

