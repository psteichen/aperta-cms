
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Q

from .models import Member, Role

def get_active_members():
  return Member.objects.filter(Q(status=Member.ACT)|Q(status=Member.WBE)).order_by('last_name')

def gen_member_fullname(member):
  return unicode(member.first_name) + u' ' + unicode.upper(member.last_name)

def gen_member_initial(m):
  initial_data = {}

  initial_data['first_name'] = m.first_name
  initial_data['last_name'] = m.last_name
  initial_data['email'] = m.email
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

  initial_data['title'] = r.title
  initial_data['desc'] = r.desc
  initial_data['member'] = r.member
  initial_data['start_date'] = r.start_date
  initial_data['end_date'] = r.end_date

  return initial_data

def gen_member_overview(template,member):
  content = { 'overview' : settings.TEMPLATE_CONTENT['members']['profile']['overview'] }

  content['name'] = gen_member_fullname(member)
  content['username'] = member.user.username
  content['email'] = member.email
  try:
    content['role'] = Role.objects.get(member=member).title
  except: pass

  return render_to_string(template,content)
