from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from django_tables2  import RequestConfig

from cms.functions import show_form, getSaison

from meetings.models import Meeting
from events.models import Event
from attendance.functions import gen_attendance_hashes

from .functions import gen_member_initial, gen_role_initial, gen_member_overview, gen_member_fullname, gen_username, gen_random_password
from .models import Member, Role
from .forms import MemberForm, RoleForm, RoleTypeForm
from .tables  import MemberTable, MgmtMemberTable, RoleTable


# list #
#########
@permission_required('cms.MEMBER')
def list(request):
  request.breadcrumbs( ( ('home','/'),
                         ('members','/members/'),
                     ) )

  table = MemberTable(Member.objects.all().order_by('status', 'last_name'),request,username=request.user.username)
  if request.user.has_perm('cms.BOARD'):
    table = MgmtMemberTable(Member.objects.all().order_by('status', 'last_name'))
  RequestConfig(request, paginate={"per_page": 75}).configure(table)

  return render(request, settings.TEMPLATE_CONTENT['members']['template'], {
                        'title': settings.TEMPLATE_CONTENT['members']['title'],
                        'actions': settings.TEMPLATE_CONTENT['members']['actions'],
			'username': request.user.username,
                        'table': table,
                        })


# add #
#######
@permission_required('cms.BOARD')
def add(r):
  r.breadcrumbs( ( 
			('home','/'),
                   	('members','/members/'),
                   	('add a member','/members/add/'),
                ) )

  if r.POST:
    mf = MemberForm(r.POST)
    if mf.is_valid():
      Me = mf.save(commit=False)
      Me.save()

      # create user
      user = User.objects.create_user(gen_username(Me.first_name,Me.last_name), Me.email, make_password(gen_random_password()))

      #gen attendance hashes (to avoid errors with future events & meetings)
      for meeting in Meeting.objects.all():
        gen_attendance_hashes(meeting,Event.MEET,Me)
      for event in Event.objects.all():
        gen_attendance_hashes(event,Event.OTH,Me)
      
      # all fine -> done
      return render(r, settings.TEMPLATE_CONTENT['members']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['add']['done']['title'], 
                'message': '',
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['members']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in mf.errors]),
                })
  # no post yet -> empty form
  else:
    form = MemberForm()
    return render(r, settings.TEMPLATE_CONTENT['members']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['members']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['members']['add']['submit'],
                'form': form,
                })


# modify #
##########
@permission_required('cms.BOARD')
def modify(r,mem_id):
  r.breadcrumbs( ( 
			('home','/'),
                   	('members','/members/'),
                ) )

  M = Member.objects.get(pk=mem_id)

  if r.POST:
    mf = MemberForm(r.POST,r.FILES,instance=M)
    if mf.is_valid():
      M = mf.save()
      
      # all fine -> done
      return render(r, settings.TEMPLATE_CONTENT['members']['modify']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['modify']['done']['title'].format(unicode(M)), 
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['members']['modify']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['modify']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in mf.errors]),
                })
  # no post yet -> empty form
  else:
    form = MemberForm()
    form.initial = gen_member_initial(M)
    form.instance = M
    return render(r, settings.TEMPLATE_CONTENT['members']['modify']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['modify']['title'],
                'desc': settings.TEMPLATE_CONTENT['members']['modify']['desc'],
                'submit': settings.TEMPLATE_CONTENT['members']['modify']['submit'],
                'form': form,
                })


# roles #
#########
@permission_required('cms.BOARD')
def roles(request):
  request.breadcrumbs( ( ('home','/'),
                         ('members','/members/'),
                         ('roles','/members/roles/'),
                     ) )

  table = RoleTable(Role.objects.all().order_by('year', 'type'))
  RequestConfig(request, paginate={"per_page": 75}).configure(table)

  return render(request, settings.TEMPLATE_CONTENT['members']['roles']['template'], {
                        'title': settings.TEMPLATE_CONTENT['members']['roles']['title'],
                        'actions': settings.TEMPLATE_CONTENT['members']['roles']['actions'],
                        'table': table,
                        })



# roles  modify #
#################
@permission_required('cms.BOARD')
def r_modify(r,role_id):
  r.breadcrumbs( ( 
			('home','/'),
                   	('members','/members/'),
                   	('roles','/members/roles/'),
                ) )

  R = Role.objects.get(pk=role_id)

  if r.POST:
    rf = RoleForm(r.POST,instance=R)
    if rf.is_valid():
      Rl = rf.save()
      
      # all fine -> done
      return render(r, settings.TEMPLATE_CONTENT['members']['roles']['modify']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['roles']['modify']['done']['title'], 
                'message': settings.TEMPLATE_CONTENT['members']['roles']['modify']['done']['message'] + unicode(Rl),
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['members']['roles']['modify']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['roles']['modify']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in rf.errors]),
                })

  # no post yet -> empty form
  else:
    form = RoleForm()
    form.initial = gen_role_initial(R)
    form.instance = R
    return render(r, settings.TEMPLATE_CONTENT['members']['roles']['modify']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['roles']['modify']['title'],
                'desc': settings.TEMPLATE_CONTENT['members']['roles']['modify']['desc'],
                'submit': settings.TEMPLATE_CONTENT['members']['roles']['modify']['submit'],
                'form': form,
                })

# roles  add #
##############
@permission_required('cms.BOARD')
def r_add(r):
  r.breadcrumbs( ( 
			('home','/'),
                   	('members','/members/'),
                   	('roles','/members/roles/'),
                ) )

  if r.POST:
    rf = RoleForm(r.POST)
    if rf.is_valid():
      R = rf.save()
      
      # all fine -> done
      return render(r, settings.TEMPLATE_CONTENT['members']['roles']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['roles']['add']['done']['title'], 
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['members']['roles']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['roles']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in rf.errors]),
                })

  # no post yet -> empty form
  else:
    form = RoleForm(initial = { 'year'	: getSaison(), })
    return render(r, settings.TEMPLATE_CONTENT['members']['roles']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['roles']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['members']['roles']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['members']['roles']['add']['submit'],
                'form': form,
                })

# roles  type #
#################
@permission_required('cms.BOARD')
def r_type(r):
  r.breadcrumbs( ( 
			('home','/'),
                   	('members','/members/'),
                   	('roles','/members/roles/'),
                ) )

  if r.POST:
    rtf = RoleTypeForm(r.POST)
    if rtf.is_valid():
      Rt = rtf.save()
      
      # all fine -> done
      return render(r, settings.TEMPLATE_CONTENT['members']['roles']['type']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['roles']['type']['done']['title'], 
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['members']['roles']['type']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['roles']['type']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in rtf.errors]),
                })

  # no post yet -> empty form
  else:
    form = RoleTypeForm()
    return render(r, settings.TEMPLATE_CONTENT['members']['roles']['type']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['roles']['type']['title'],
                'desc': settings.TEMPLATE_CONTENT['members']['roles']['type']['desc'],
                'submit': settings.TEMPLATE_CONTENT['members']['roles']['type']['submit'],
                'form': form,
                })



# profile #
###########
@login_required
def profile(r, username):
  r.breadcrumbs( ( 
			('home','/'),
                   	('members','/members/'),
                   	('user profile','/members/profile/'+username),
               ) )

  member 	= Member.objects.get(user=r.user)
  title 	= settings.TEMPLATE_CONTENT['members']['profile']['title'] % { 'name' : gen_member_fullname(member), }
  actions 	= settings.TEMPLATE_CONTENT['members']['profile']['actions']
  for a in actions:
      a['url'] = a['url'].format(username)

  message 	= gen_member_overview(settings.TEMPLATE_CONTENT['members']['profile']['overview']['template'],member)

  return render(r, settings.TEMPLATE_CONTENT['members']['profile']['template'], {
                   'title'	: title,
                   'actions'	: actions,
                   'message'	: message,
                })


# profile  modify #
###################
@login_required
def p_modify(r, username):
  r.breadcrumbs( ( 
			('home','/'),
                   	('members','/members/'),
                   	('user profile','/members/profile/'+username),
               ) )

  M = Member.objects.get(user=r.user)

  if r.POST:
    mf = MemberForm(r.POST,r.FILES,instance=M)
    if mf.is_valid():
      Me = mf.save(commit=False)
      Me.save()

      # all fine -> done
      return render(r, settings.TEMPLATE_CONTENT['members']['profile']['modify']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['profile']['modify']['done']['title'], 
                'message': '',
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['members']['profile']['modify']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['profile']['modify']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in mf.errors]),
                })
  # no post yet -> empty form
  else:
    form = MemberForm()
    form.initial = gen_member_initial(M)
    form.instance = M
    return render(r, settings.TEMPLATE_CONTENT['members']['profile']['modify']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['profile']['modify']['title'],
                'desc': settings.TEMPLATE_CONTENT['members']['profile']['modify']['desc'],
                'submit': settings.TEMPLATE_CONTENT['members']['profile']['modify']['submit'],
                'form': form,
                })

