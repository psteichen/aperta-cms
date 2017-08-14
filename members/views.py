#
# coding=utf-8
#

from django.conf import settings
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required, permission_required

from formtools.wizard.views import SessionWizardView

from django_tables2  import RequestConfig

from headcrumbs.decorators import crumb
from headcrumbs.util import name_from_pk

from cms.functions import show_form, getSaison

from meetings.models import Meeting
from events.models import Event
from attendance.functions import gen_attendance_hashes

from .functions import gen_member_initial, gen_role_initial, gen_member_overview, gen_member_fullname, gen_username, gen_random_password
from .models import User, Member, Role
from .forms import MemberForm, RoleForm, RoleTypeForm
from .tables  import MemberTable, MgmtMemberTable, RoleTable


# list #
#########
@permission_required('cms.MEMBER')
@crumb(u'Membres')
def list(request):

  table = MemberTable(Member.objects.all().order_by('status', 'last_name'),request,username=request.user.username)
  if request.user.has_perm('cms.BOARD'):
    table = MgmtMemberTable(Member.objects.all().order_by('status', 'last_name'))
  RequestConfig(request, paginate={"per_page": 75}).configure(table)

  return TemplateResponse(request, settings.TEMPLATE_CONTENT['members']['template'], {
                        'title': settings.TEMPLATE_CONTENT['members']['title'],
                        'actions': settings.TEMPLATE_CONTENT['members']['actions'],
			'username': request.user.username,
                        'table': table,
                        })


# add #
#######
@permission_required('cms.BOARD')
@crumb(u'Ajouter un membre', parent=list)
def add(r):

  if r.POST:
    mf = MemberForm(r.POST)
    if mf.is_valid():
      M = mf.save(commit=False)

      # create user
      U = User.objects.create_user(gen_username(M.first_name,M.last_name), M.email, make_password(gen_random_password()))
      U.first_name = M.first_name
      U.last_name = M.last_name
      U.user_permissions.add(Permission.objects.get(codename='MEMBER'))
      U.save()
      M.user = U
      M.save()

      #gen attendance hashes (to avoid errors with future events & meetings)
      for meeting in Meeting.objects.all():
        gen_attendance_hashes(meeting,Event.MEET,M)
      for event in Event.objects.all():
        gen_attendance_hashes(event,Event.OTH,M)
      
      # all fine -> done
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['add']['done']['title'], 
                'message': '',
                })

    # form not valid -> error
    else:
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in mf.errors]),
                })
  # no post yet -> empty form
  else:
    form = MemberForm()
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['members']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['members']['add']['submit'],
                'form': form,
                })


# modify #
##########
@permission_required('cms.BOARD')
@crumb(u'Modifier le membre [{member}]'.format(member=name_from_pk(Member)),parent=list)
def modify(r,mem_id):

  M = Member.objects.get(pk=mem_id)
  if r.POST:
    mf = MemberForm(r.POST,r.FILES,instance=M)
    if mf.is_valid():
      M = mf.save()

      # all fine -> done
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['modify']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['modify']['done']['title'].format(unicode(M)),
                })

    # form not valid -> error
    else:
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['modify']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['modify']['done']['title'],
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in mf.errors]),
                })
  # no post yet -> empty form
  else:
    form = MemberForm()
    form.initial = gen_member_initial(M)
    form.instance = M
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['modify']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['modify']['title'],
                'desc': settings.TEMPLATE_CONTENT['members']['modify']['desc'],
                'submit': settings.TEMPLATE_CONTENT['members']['modify']['submit'],
                'form': form,
                })


# roles #
#########
@permission_required('cms.BOARD')
@crumb(u"Rôles")
def roles(request):

  table = RoleTable(Role.objects.all().order_by('year', 'type'))
  RequestConfig(request, paginate={"per_page": 75}).configure(table)
  return TemplateResponse(request, settings.TEMPLATE_CONTENT['members']['roles']['template'], {
                        'title': settings.TEMPLATE_CONTENT['members']['roles']['title'],
                        'actions': settings.TEMPLATE_CONTENT['members']['roles']['actions'],
                        'table': table,
                        })


# roles  modify #
#################
@permission_required('cms.BOARD')
@crumb(u'Modifier le rôle [{role}]'.format(role=name_from_pk(Role)), parent=roles)
def r_modify(r,role_id):

  R = Role.objects.get(pk=role_id)
  if r.POST:
    rf = RoleForm(r.POST,instane=R)
    if rf.is_valid():
      Rl = rf.save()
      
      # all fine -> done
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['role']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['role']['add']['done']['title'], 
                'message': settings.TEMPLATE_CONTENT['members']['role']['add']['done']['message'] + unicode(Rl),
                })

    # form not valid -> error
    else:
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['role']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['role']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in rf.errors]),
                })

  # no post yet -> empty form
  else:
    form = RoleForm()
    form.initial = gen_role_initial(R)
    form.instance = R
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['role']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['role']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['members']['role']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['members']['role']['add']['submit'],
                'form': form,
                })

# roles  add #
##############
@permission_required('cms.BOARD')
@crumb(u'Ajouter un rôle', parent=roles)
def r_add(r):

  if r.POST:
    rf = RoleForm(r.POST)
    if rf.is_valid():
      R = rf.save()

      # all fine -> done
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['roles']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['roles']['add']['done']['title'],
                })

    # form not valid -> error
    else:
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['roles']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['roles']['add']['done']['title'],
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in rf.errors]),
                })

  # no post yet -> empty form
  else:
    form = RoleForm(initial = { 'year'        : getSaison(), })
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['roles']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['roles']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['members']['roles']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['members']['roles']['add']['submit'],
                'form': form,
                })

# roles  type #
#################
@permission_required('cms.BOARD')
@crumb(u'Créer un type de rôle', parent=roles)
def r_type(r):

  if r.POST:
    rtf = RoleTypeForm(r.POST)
    if rtf.is_valid():
      Rt = rtf.save()

      # all fine -> done
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['roles']['type']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['roles']['type']['done']['title'],
                })

    # form not valid -> error
    else:
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['roles']['type']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['roles']['type']['done']['title'],
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in rtf.errors]),
                })

  # no post yet -> empty form
  else:
    form = RoleTypeForm()
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['roles']['type']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['roles']['type']['title'],
                'desc': settings.TEMPLATE_CONTENT['members']['roles']['type']['desc'],
                'submit': settings.TEMPLATE_CONTENT['members']['roles']['type']['submit'],
                'form': form,
                })


# profile #
###########
@login_required
@crumb(u'Profile utilisateur: {user}'.format(user=name_from_pk(User)))
def profile(r, username):

  try:
    member 	= Member.objects.get(user=r.user)
  except Member.DoesNotExist:
    # non-member user, probably an admin -> redirect to admin console
    return redirect('/admin/')
    
  title 	= settings.TEMPLATE_CONTENT['members']['profile']['title'] % { 'name' : gen_member_fullname(member), }
  actions 	= settings.TEMPLATE_CONTENT['members']['profile']['actions']
  for a in actions:
      a['url'] = a['url'].format(username)

  message 	= gen_member_overview(settings.TEMPLATE_CONTENT['members']['profile']['overview']['template'],member)

  return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['profile']['template'], {
                   'title'	: title,
                   'actions'	: actions,
                   'message'	: message,
                })


# profile modify #
##################
@login_required
@crumb(name_from_pk(User), parent=list)
def p_modify(r, username):

  M = Member.objects.get(user=r.user)

  if r.POST:
    mf = MemberForm(r.POST,r.FILES,instance=M)
    if mf.is_valid():
      Me = mf.save(commit=False)
      Me.save()

      # all fine -> done
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['profile']['modify']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['profile']['modify']['done']['title'], 
                'message': '',
                })

    # form not valid -> error
    else:
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['profile']['modify']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['profile']['modify']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in mf.errors]),
                })
  # no post yet -> empty form
  else:
    form = MemberForm()
    form.initial = gen_member_initial(M)
    form.instance = M
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['members']['profile']['modify']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['profile']['modify']['title'],
                'desc': settings.TEMPLATE_CONTENT['members']['profile']['modify']['desc'],
                'submit': settings.TEMPLATE_CONTENT['members']['profile']['modify']['submit'],
                'form': form,
                })

