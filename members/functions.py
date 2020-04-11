
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

from cms.functions import getSaison, debug

from attendance.models import Meeting_Attendance

from .models import Member, Role, RoleType


def get_active_members():
  return Member.objects.filter(Q(status=Member.ACT)|Q(status=Member.WBE)|Q(status=Member.HON)).order_by('last_name')

#
## gandi.net mailinglist functions
#
from requests import request
GANDI_ML_URL = "https://api.gandi.net/v5/email/forwards/aperta.lu"

def ML_get(name):
  headers = {'authorization': 'Apikey '+settings.GANDI_API_KEY}
  response = request("GET", GANDI_ML_URL, headers=headers)
  data = response.json()
  for d in data: 
    if d['source'] == settings.EMAILS['ml'][name]: return d['destinations']
    
  return False
 
def ML_create(name,dest):
  import json

  p = {}
  p['source'] = settings.EMAILS['ml'][name]
  p['destinations'] = dest

  debug('members.functions.ML_create','create ML '+settings.EMAILS['ml'][name])
  debug('members.functions.ML_create','emails: '+str(dest))

  payload = json.dumps(p)
  headers = {
	'authorization': 'Apikey '+settings.GANDI_API_KEY,
	'content-type': "application/json"
  }
  debug('members.functions.ML_create','POST url: '+str(GANDI_ML_URL))
  debug('members.functions.ML_create','POST headers: '+str(headers))
  debug('members.functions.ML_create','POST paylod as json: '+str(payload))
  response = request("POST", GANDI_ML_URL, data=payload, headers=headers)
  debug('members.functions.ML_create','POST (create ML via API): '+str(response))

  return response.status_code
 
def ML_update(name):
  r = ML_get(name)
  debug('members.functions.ML_update','get ML ('+settings.EMAILS['ml'][name]+'): '+str(r))
  emails = list(User.objects.filter(groups__name=str(name)).values_list('email',flat=True))
  debug('members.functions.ML_update','emails for list: ['+settings.EMAILS['ml'][name]+']: '+str(emails))
  if emails == []: return False
  if r == False: return ML_create(name,emails)
  else: 
    import json
    p = {}
    p['destinations'] = emails
    debug('members.functions.ML_update','put emails in paylod: '+str(p))

    url = GANDI_ML_URL+"/"+settings.EMAILS['ml'][name]
    payload = json.dumps(p)
    debug('members.functions.ML_update','paylod as json: '+str(payload))
    headers = {
	'authorization': 'Apikey '+settings.GANDI_API_KEY,
	'content-type': "application/json"
    }
    response = request("PUT", url, data=payload, headers=headers)
    debug('members.functions.ML_update','PUT (update ML via API): '+str(response))

    return response.text

def ML_updates():
  r=[]
  r.append(ML_update('MEMBER'))
  r.append(ML_update('BOARD'))
  return r

#
## user creation and management functions
#
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

  # add to members ML
  ML_add(settings.EMAILS['ml']['members'],U.email)

  return U

def update_user(member):
  U = member.user
  U.first_name = member.first_name
  U.last_name = member.last_name
  U.email = member.email
  U.save()

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

def gen_member_fullname(member):
  return str(member.first_name) + u' ' + str.upper(member.last_name)

def gen_member_fullname_n_role(member):
  roles = u''
  try:
    R = Role.objects.filter(member__id=member.id,year=getSaison())
    for r in R:
      roles += str(r.type.title)
      if r != R.last(): roles += u' ; '
  except Role.DoesNotExist:
    pass

  if roles != u'': 
    return str(member.first_name) + u' ' + str.upper(member.last_name) + u' (' + roles + ') '
  else:
    return str(member.first_name) + u' ' + str.upper(member.last_name)

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
  members = []
  for m in get_active_members():
    try:
      Meeting_Attendance.objects.get(meeting=meeting,member=m)
    except Meeting_Attendance.DoesNotExist:
      members.append(m)

  return members

          
def remove_from_board(M):
  U = M.user
  g = Group.objects.get(name='BOARD') 
  g.user_set.remove(U)

def remove_from_groups(M):
  U = M.user
  g = Group.objects.get(name='MEMBER') 
  g.user_set.remove(U)
  h = Group.objects.get(name='BOARD') 
  h.user_set.remove(U)

def add_to_board(M):
  U = M.user
  g = Group.objects.get(name='BOARD') 
  g.user_set.add(U)

def update_board():
  # update board group based on roles
  board = Group.objects.get(name='BOARD') 
  users = User.objects.all()
  for u in users:
    board.user_set.remove(u)
    R = Role.objects.filter(member__user=u,year=getSaison())
    for r in R:
      if r.type.type == RoleType.A: board.user_set.add(u)

def has_role(M):
  try:
    Role.objects.get(member=M)
    return True
  except Role.DoesNotExist:
    return False

def add_to_groups(M):
  U = M.user
  g = Group.objects.get(name='MEMBER') 
  g.user_set.add(U)
  if has_role(M):
    h = Group.objects.get(name='BOARD') 
    h.user_set.add(U)

